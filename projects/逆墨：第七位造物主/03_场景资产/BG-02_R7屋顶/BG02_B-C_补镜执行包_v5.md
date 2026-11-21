# BG02-B / BG02-C｜R7屋顶补镜执行包 V5

**场景母版**：`BG-02_R7屋顶/场景空间锚点_v1.md`；BG02-A RGB PNG 已在 main，审核状态 draft。B/C 视角目前只定义提示词，**正式图片 missing**。

## 坚持不变的物理空间

- 屋顶东西向长方形，作者设定约 18 m × 12 m；北侧低女儿墙有且仅有一个缺口。
- 西南两只深蓝金属水箱，锈蚀管道通到中部低矮机房；东北仅一根折断天线。
- 积水集中在中央偏北；东侧临空轨天际线，不增加新建筑；北侧外可见蓝黑城区的落差。
- 深蓝黑午夜雨夜、唯一猩红人工警报与少量电蓝高光；纯二维粗墨线、半调网点、纸纤维、无字无人物。

## BG02-B｜南侧低机位 · 北女儿墙

**目标**：EP01 P12 / S08 起跳前的空镜空间锚。画面不能出现起跳中的林燧。

**提示词**：

```text
Single standalone vertical 2D ink-comic environment anchor BG02-B for original story 逆墨：第七位造物主. CAMERA: low at the south edge of R7 rooftop, looking north, slightly upward toward the north parapet and its ONLY broken gap, with distant blue-black wet megacity below the parapet. Keep the southwest TWO steel water tanks at back left from this lens, central low equipment shed with rusty pipes and northeast ONE broken antenna. Severe nocturnal rain and wet concrete, a distant artificial crimson alarm beam. Thick irregular hand-inked contour lines, heavy navy hatching, gritty halftone paper texture, restrained #071019 / #102439 / #EF2F42 palette, shallow bone-white rain highlights. Exactly one roof, one shot, no figures, no hero, no sky moon, NO lettering, numbers, panel grid, collage, character sheet, UI, labels, photorealism or 3D.
```

**QA**：可与 A 同时放进场景空间草图，北墙缺口与双水箱不应瞬移；不将其误标为 A 的同机位。

## BG02-C｜积水极近镜 · 披风倒影预留

**目标**：EP01 P02 / S01 的可复用空水面资产；倒影红披风应在漫画 P02 的角色合成层中制作，**BG02-C 本体保持纯空景**。

**提示词**：

```text
One independent 3:4 vertical macro environment illustration BG02-C from the SAME R7 rooftop: almost top-down onto a shallow puddle at the roof's central-north zone, rain droplets forming three slightly offset concentric ripple systems, fragmented reflection of the north parapet and dim artificial crimson warning beam, dark wet cracked concrete, tiny rusty pipe detail entering from southwest margin. Original 2D hand-brushed comic linework, dense blue-black hatching, ink spatter, coarse halftone, clear separation for later adding a red-cape reflection layer. Pure empty environmental plate: NO actual character, NO prepainted human reflection, NO red cape in this plate, NO words, letters, numbers, subtitles, collage, storyboard, logo or UI, no 3D or photorealism.
```

**合成拆分**：BG02-C 空景层 + `FX-RAIN` 雨纹层 + `CH01-CAPE-REFLECTION` 红披风反射层（仅 P02/S01） + 后期字卡层。不要在模型底图上画文字。

## 文件命名与验收

- `BG02_B_低机位空景_v001.png`、`BG02_C_积水空景_v001.png`，分别独立输出，RGB PNG；不能输出 A/B/C 三宫格。
- 文件入 GitHub 前状态 `missing`；原图入库且校验通过为 `committed`；美审通过方可从 `draft` 升级为 `approved`。
- 若角色、文字、分格线或与 A 失配，立即拒收，不拿失败图凑数量。
