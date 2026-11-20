#!/usr/bin/env python3
"""验证并上传《逆墨：第七位造物主》V4 的两张原始 PNG。

在本仓库目录运行：
  python3 tools/import-ni-mo-v4.py /path/to/逆墨_第七位造物主_V4_独立资产包.zip --dry-run
  python3 tools/import-ni-mo-v4.py /path/to/逆墨_第七位造物主_V4_独立资产包.zip --push
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

PROJECT = "projects/逆墨：第七位造物主"
REPO_ID = "983033995/video-assets"
EXPECTED = {
    "CH-04": {
        "path": f"{PROJECT}/02_角色资产/CH-04_白檐/白檐_独立定妆_候选_v001.png",
        "size": 1863425,
        "sha256": "ee2676e4b54c7b6423171fc202d3130cfad15174cd9d394b0f8637a7ad37fd01",
    },
    "BG-02-A": {
        "path": f"{PROJECT}/03_场景资产/BG-02_R7屋顶/BG02_A_空景_v001.png",
        "size": 4031255,
        "sha256": "36408f861bcc703bf114187f2eeb4fc8661b028e0e4ceb193a2f702d5056f693",
    },
}

def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("archive", type=Path)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--push", action="store_true")
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    if not (root / ".git").exists():
        sys.exit("错误：请在 video-assets 仓库中执行。")
    if args.push:
        remote = git(root, "remote", "get-url", "origin")
        if REPO_ID not in remote:
            sys.exit(f"错误：origin 不是目标仓库 {REPO_ID}: {remote}")
        if git(root, "branch", "--show-current") != "main":
            sys.exit("错误：仅允许 main 分支 --push。")
        if git(root, "status", "--porcelain"):
            sys.exit("错误：工作区不干净，防止混入其他提交。")
        git(root, "fetch", "origin", "main")
        if git(root, "rev-parse", "HEAD") != git(root, "rev-parse", "origin/main"):
            sys.exit("错误：main 不是最新，请先 git pull --ff-only。")

    mf = root / PROJECT / "00_资产登记" / "asset-manifest.json"
    if not mf.exists():
        sys.exit("错误：找不到 asset-manifest.json。")
    manifest = json.loads(mf.read_text(encoding="utf-8"))
    images = {x.get("id"): x for x in manifest.get("images", [])}
    for asset_id in EXPECTED:
        if asset_id not in images:
            sys.exit(f"错误：manifest 缺少 {asset_id}。")

    with ZipFile(args.archive) as archive:
        payloads = {}
        for asset_id, meta in EXPECTED.items():
            try:
                blob = archive.read(meta["path"])
            except KeyError:
                sys.exit(f"错误：ZIP 内缺少 {meta['path']}")
            if len(blob) != meta["size"] or digest(blob) != meta["sha256"]:
                sys.exit(f"错误：{asset_id} 的大小或 SHA256 不正确，拒绝上传。")
            path = root / meta["path"]
            if path.exists() and digest(path.read_bytes()) != meta["sha256"]:
                sys.exit(f"错误：拒绝覆盖已有不同内容：{path}")
            if images[asset_id].get("sha256") != meta["sha256"]:
                sys.exit(f"错误：{asset_id} 在 manifest 的 SHA256 不一致。")
            payloads[asset_id] = blob
            print(f"验证通过：{asset_id} ({meta['size']} 字节，{meta['sha256']})")

    if args.dry_run:
        print("校验成功，未修改文件。")
        return

    for asset_id, meta in EXPECTED.items():
        path = root / meta["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_bytes(payloads[asset_id])
        images[asset_id]["status"] = "committed"
        images[asset_id]["review"] = "draft"
        images[asset_id]["notes"] = "原始PNG校验SHA256后提交至GitHub；美术审核仍为draft。"
    manifest["story_status"] = "V4 original PNG candidates synced; artwork review draft; EP01 standalone panels missing"
    mf.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    staged = [x["path"] for x in EXPECTED.values()] + [str(mf.relative_to(root))]
    git(root, "add", "--", *staged)
    git(root, "commit", "-m", "assets(ni-mo): sync original CH04 and BG02-A PNGs")
    try:
        git(root, "push", "origin", "main")
    except subprocess.CalledProcessError:
        sys.exit("推送失败：本地提交已保存，但不能宣称GitHub已保存图片。检查权限和网络后执行 git push origin main。")
    print("已推送 GitHub commit:", git(root, "rev-parse", "HEAD"))
    print("图片字节已提交；美术审核仍是 draft。")

if __name__ == "__main__":
    main()
