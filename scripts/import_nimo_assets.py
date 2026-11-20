#!/usr/bin/env python3
"""Restore exact original PNG bytes from GitHub-friendly Base64 shards.

Only runs from this repository's checked-out workspace. All paths are scoped
to a specific project's asset directory and SHA-256 verified before commit.
"""
from __future__ import annotations
import base64
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
PROJECT = BASE / "projects" / "逆墨：第七位造物主"
PARTS = PROJECT / "00_资产登记" / "上传分块"
PLAN = PARTS / "上传计划.json"
ASSETS = PROJECT / "00_资产登记" / "asset-manifest.json"


def main() -> None:
    if not PLAN.exists():
        print("No pending upload plan; nothing to restore.")
        return
    jobs = json.loads(PLAN.read_text(encoding="utf-8"))["assets"]
    manifest = json.loads(ASSETS.read_text(encoding="utf-8"))
    asset_index = {item["id"]: item for item in manifest["images"]}
    restored = []
    for job in jobs:
        asset_id = str(job["id"])
        rel = Path(str(job["target"]))
        if rel.is_absolute() or ".." in rel.parts or rel.suffix.lower() != ".png":
            raise ValueError(f"Unsafe image path for {asset_id}")
        if asset_id not in asset_index or asset_index[asset_id]["target_path"] != rel.as_posix():
            raise ValueError(f"Unregistered image asset: {asset_id}")
        prefix = asset_id.replace("-", "_")
        parts = [PARTS / f"{prefix}.part{n:02d}.b64" for n in range(int(job["part_count"]))]
        if not all(part.is_file() for part in parts):
            raise FileNotFoundError(f"Missing shards: {asset_id}")
        b64 = "".join(part.read_text(encoding="ascii") for part in parts)
        data = base64.b64decode(b64, validate=True)
        digest = hashlib.sha256(data).hexdigest()
        if digest != job["sha256"] or len(data) != job["size"] or data[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError(f"Integrity check failed for {asset_id}")
        target = PROJECT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise FileExistsError(f"Different image already exists: {target}")
        target.write_bytes(data)
        asset_index[asset_id]["status"] = "committed"
        asset_index[asset_id]["sha256"] = digest
        asset_index[asset_id]["bytes"] = len(data)
        restored.append((asset_id, target.relative_to(BASE), len(data)))
    ASSETS.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for job in jobs:
        prefix = job["id"].replace("-", "_")
        for index in range(int(job["part_count"])):
            (PARTS / f"{prefix}.part{index:02d}.b64").unlink()
    PLAN.unlink()
    for asset_id, path, size in restored:
        print(f"Verified {asset_id}: {path} ({size:,} bytes)")
    print(f"Restored {len(restored)} original PNG assets.")


if __name__ == "__main__":
    main()
