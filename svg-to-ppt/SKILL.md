---
name: svg-to-ppt
description: 通过提示词生成 SVG 幻灯片并直接转换为可编辑 PPTX。当用户提到"做PPT"、"演示文稿"、"幻灯片"、"SVG转PPT"、"slides"、"presentation"时使用。
---

# SVG → PPT Skill

## 这个 Skill 做什么

将用户提供的主题/内容，通过两步 AI 生成流程，产出一份**完全可编辑的 PPTX**：

```
用户主题 → [PPT结构架构师] → JSON 大纲（含节奏规划）
                                    ↓
                            [SVG 编码专家] → 每页 SVG (1280×720)
                                    ↓
                            [svg2pptx-svgblip.py] → .pptx (SVG矢量嵌入)
```

**核心特性**：SVG 通过 PPT 2016+ 原生 `<a:svgBlip>` 直接嵌入，PPT 内矢量渲染，右键"转换为图形"即可编辑。

---

## 5 条设计铁律

| # | 铁律 | 说明 |
|---|------|------|
| 1 | **克制优于炫技** | 渐变背景只在封面/幕封透出，内容页必须克制 |
| 2 | **结构优于装饰** | 信息层级靠字号对比 + 字体族切换 + 网格留白实现，**禁用阴影和浮动卡片** |
| 3 | **节奏制造呼吸** | Hero 页与 Non-hero 页必须交替，连续 3 页同类型 = P0 错误 |
| 4 | **色彩有纪律** | 三色法则：纸白 + 墨色 + 一个重点色。禁用纯白 `#FFFFFF` 做底色、纯黑 `#000000` 做字色 |
| 5 | **字体有分工** | 衬线标题 + 非衬线正文 + 等宽元数据，三级分工建立层级 |
| 6 | **高亮有逻辑** | 主色标结构，辅色标结论。到处高亮=没有高亮，永远不要"最后一项用辅色" |

---

## 字体三级分工

| 层级 | 字体族 | 功能 | SVG font-family |
|------|--------|------|-----------------|
| **第一级·观点** | 衬线体 (Serif) | 大标题、金句、核心论点 | `Georgia, "Noto Serif SC", serif` |
| **第二级·信息** | 非衬线体 (Sans-serif) | 正文、列表、说明文字 | `"PingFang SC", "Microsoft YaHei", sans-serif` |
| **第三级·元数据** | 等宽体 (Monospace) | 页码、章节号、数据标注、日期 | `"SF Mono", "Fira Code", monospace` |

**核心原则**：读者无需费劲思考，眼睛自动识别"这句话是正文还是附注"。

---

## 页面类型（10 种）

### Hero 页（节奏制造者，必须有留白和视觉冲击力）

| 类型 | 说明 | 视觉特征 |
|------|------|---------|
| **开场封面** | 全局封面 | 渐变背景 + 超大衬线标题 + 等宽副标题 |
| **章节幕封** | 章节分隔页 | 等宽章节号 + 衬线大标题 + 大量留白 |
| **数据大字报** | 单一核心数据 | 超大等宽数字 + 衬线标签 + 几乎无卡片 |
| **悬念问题** | 抛出关键问题 | 居中衬线大问句 + 极简装饰 |
| **大引用** | 金句/引述 | 超大衬线引号 + 引文 + 等宽出处 |

### Non-hero 页（信息承载者，使用 Bento 网格）

| 类型 | 说明 | 对应骨架 |
|------|------|---------|
| **主从叙事** | 主卡叙事 + 嵌套子卡补充 | `nested_title_body` |
| **主卡+侧栏** | 大主卡 + 侧栏支撑 + 底部条带 | `top_main_bar` |
| **双主对比** | 两张对等主卡 + 指标高亮 | `dual_main_metrics` |
| **主卡+三等分** | 主卡 + 三个并列子卡 | `main_with_group3_equal` |
| **节奏律动** | 小卡引出 → 大卡聚焦 → 双栏收尾 | `rules_rhythm` |

### 节奏硬规则

- **Hero 页与 Non-hero 页必须交替**，制造"翻杂志的呼吸感"
- ⛔ **连续 3 页以上 Non-hero（Bento 网格页）→ 判为 P0 级错误**
- 一页密、一页疏 = 翻杂志时的呼吸感
- 推荐节奏模式：封面(H) → 目录(N) → 幕封(H) → 内容(N) → 大字报(H) → 内容(N) → 悬念(H) → 内容(N) → 大引用(H) → 结尾(H)

---

## 工作流

### Step 1 · 需求澄清

确认以下信息（缺什么问什么）：

| # | 问题 | 为什么问 |
|---|------|---------|
| 1 | **主题是什么？** | 决定内容方向 |
| 2 | **大约多少页？** | 15分钟≈10页，30分钟≈20页 |
| 3 | **有没有现成素材？**（文档/大纲/数据） | 有就基于素材，没有就帮搭 |
| 4 | **风格偏好？**（从5套主题中选） | 决定配色方案 |
| 5 | **用途？**（演讲/汇报/分享/教学） | 决定信息密度和语言风格 |

### Step 2 · 生成 PPT 大纲

读取 `<SKILL_ROOT>/assets/prompts/outline-architect.md`，按其格式输出 JSON 大纲。

**节奏规划**：大纲必须为每页标注页面类型（hero/non-hero），确保交替节奏。

将大纲保存为 `项目目录/outline.json`，确认后再进入下一步。

### Step 3 · 逐页生成 SVG

读取 `<SKILL_ROOT>/assets/prompts/slide-generator.md`，对每页内容调用 AI 生成 SVG。

**必须追加的约束**（写入每次调用的 prompt 尾部）：

```
## PPTX 兼容约束（必须遵守）
1. viewBox 固定 "0 0 1280 720"
2. 样式全部用 XML 属性，禁止 <style> 标签或 class
3. 颜色用 hex（#RRGGBB），禁止 rgb()/hsl()/currentColor
4. 只用以下元素：<rect>, <circle>, <ellipse>, <line>, <polyline>, <polygon>, <text>, <tspan>, <g>, <path>, <image>, <use>
5. 渐变：可以用 <linearGradient> 和 <radialGradient>，定义在 <defs> 中，用 fill="url(#id)" 引用
6. 透明度：可以用 opacity="0.0-1.0"
7. 禁止：<filter>, <mask>, <clipPath>, <foreignObject>, CSS 动画
8. path 可以用 M/L/C/Q/A/Z 命令
9. transform 只用 translate/rotate/scale，写在属性里
10. 每个 text 元素必须指定 font-family 和 font-size
11. 所有特殊字符必须 XML 转义（& → &amp;）
12. stroke-dasharray 可以用 "5,5" 或 "10,5" 创建虚线

## 字体分工（必须遵守）
- 大标题/金句/核心论点 → font-family="Georgia, 'Noto Serif SC', serif"
- 正文/列表/说明 → font-family="'PingFang SC', 'Microsoft YaHei', sans-serif"
- 数据/页码/章节号/标注 → font-family="'SF Mono', 'Fira Code', monospace"

## 色彩纪律（必须遵守）
- 卡片底色禁用 #FFFFFF（纯白刺眼），改用主题色中的「卡片浅」色值
- 字色禁用 #000000（纯黑暴力），改用主题色中的「文字深」色值
- 每页只使用：背景色 + 卡片色 + 主色（重点色），辅色仅在数据高亮时使用

## 高亮逻辑（必须遵守）
- 主色=结构标记（流程节点/分类标签），辅色=语义高亮（关键结论/行动项/反差数据）
- 每页辅色最多 1-2 处，到处高亮=没有高亮
- 永远不要"最后一项用辅色"
- 辅色必须回答"所以呢？"—删掉不影响理解就不该加
```

**Bento 布局约束**（参考 `<SKILL_ROOT>/references/bento-layout.md`）：
- 网格：16列×9行，gap=12px
- 卡片内边距：16px 左右
- CPL 公式：`cpl = max(6, floor(width_px / (font_pt * 1.18)))`
- 内容截断：main 标题≤18字，body 标题≤15字，bullet≤22字

每页保存为 `项目目录/slides/slide-NN.svg`

### Step 4 · 转换为 PPTX

运行转换器：

```bash
python3 <SKILL_ROOT>/assets/converter/svg2pptx-svgblip.py \
  项目目录/output.pptx \
  项目目录/slides/slide-01.svg \
  项目目录/slides/slide-02.svg \
  ...
```

### Step 5 · 自检

对照 `<SKILL_ROOT>/references/checklist.md` 逐项检查：

- [ ] PPTX 文件可正常打开（PowerPoint 2016+）
- [ ] 每页 SVG 正确嵌入，矢量渲染
- [ ] Hero / Non-hero 页交替，无连续 3 页同类型
- [ ] 字体三级分工正确（衬线/非衬线/等宽）
- [ ] 无纯白 `#FFFFFF` 底色、无纯黑 `#000000` 字色
- [ ] 封面/幕封/内容/结尾页完整

### Step 6 · 交付

输出文件：`项目目录/output.pptx`

告知用户：PowerPoint 2016+ 打开，每页为 SVG 矢量图。右键 → "转换为图形" → 元素变为可编辑 PPT 形状。

---

## 资源文件

```
svg-to-ppt/
├── SKILL.md                              ← 你正在读
├── assets/
│   ├── prompts/
│   │   ├── slide-generator.md            ← SVG 生成提示词
│   │   └── outline-architect.md          ← PPT 大纲架构师
│   └── converter/
│       ├── svg2pptx-svgblip.py           ← SVG→PPTX 转换器（svgBlip嵌入）
│       ├── svg2pptx.py                   ← 旧版元素映射转换器
│       └── svg_path_parser.py            ← SVG path 解析器
├── references/
│   ├── bento-layout.md                   ← 布局骨架 + 呼吸页规范
│   ├── element-mapping.md                ← SVG→PPTX 元素映射手册
│   ├── themes.md                         ← 5 套主题色预设 + 色彩纪律
│   └── checklist.md                      ← 质量检查清单
├── examples/
│   ├── demo-slide.svg                    ← 示例 SVG（深色主题）
│   └── demo-slide-2.svg                  ← 示例 SVG（浅色路线图）
└── scripts/
    └── convert.sh                        ← CLI 入口
```

## 支持的 SVG 元素

| SVG 元素 | PPTX 映射 | 状态 |
|----------|----------|------|
| `<rect>` | 原生矩形 / 圆角矩形 | ✅ |
| `<circle>` / `<ellipse>` | 原生椭圆 | ✅ |
| `<text>` / `<tspan>` | 文本框（自动换行） | ✅ |
| `<line>` | 线条 | ✅ |
| `<path>` (M/L/C/Q/A/Z) | 自由形状 | ✅ |
| `<polygon>` / `<polyline>` | 自由形状 | ✅ |
| `<g>` | 递归处理 | ✅ |
| `<linearGradient>` / `<radialGradient>` | 渐变填充 | ✅ |
| `opacity` | 透明度 | ✅ |
| `stroke-dasharray` | 虚线描边 | ✅ |
| `<use>` / `<defs>` | 引用复用 | ✅ |
| `<image>` (base64) | 图片 | ✅ |
