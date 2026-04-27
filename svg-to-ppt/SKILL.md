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
| 5 | **字体有分工** | 衬线标题（观点/金句） + 非衬线正文（信息） + 等宽元数据，三级分工建立层级 |
| 6 | **高亮有逻辑** | 主色标结构，辅色标结论。到处高亮=没有高亮，永远不要"最后一项用辅色" |

---

## 字体三级分工

| 层级 | 字体族 | 功能 | SVG font-family |
|------|--------|------|-----------------|
| **第一级·观点** | 微软雅黑加粗 (Bold) | 大标题、金句、核心论点 | `"Microsoft YaHei", "PingFang SC", sans-serif` (font-weight: 700/800) |
| **第二级·信息** | 微软雅黑细体 (Light) | 正文、列表、说明文字 | `"Microsoft YaHei", "PingFang SC", sans-serif` (font-weight: 300/400) |
| **第三级·元数据** | 等宽体 (Monospace) | 页码、章节号、数据标注、日期 | `"SF Mono", "Fira Code", "Consolas", monospace` |

> ⚠️ **硬性约束：中文标题统一用 Noto Serif SC，英文标题用 Georgia。严禁用宋体/Times New Roman 作为正文字体。**
>
> **字体分工**：衬线标题（视觉重音） + 非衬线正文（信息密度） + 等宽元数据（装饰节奏）——三者缺一不可，读者的眼睛靠字体自动区分层级。

---

## 页面类型（10 种）

### Hero 页（节奏制造者，必须有留白和视觉冲击力）

> 每个 Hero 页必须有 **kicker**：标题上方的一行小钩子文字，用等宽字体，是这页的"戏剧性入口"，每页都应不同。

| 类型 | 说明 | 视觉特征 |
|------|------|---------|
| **开场封面** | 全局封面 | 渐变背景 + kicker + 超大衬线标题 + 等宽副标题 |
| **章节幕封** | 章节分隔页 | 等宽章节号 + kicker + 衬线大标题 + 大量留白 |
| **数据大字报** | 单一核心数据 | 超大等宽数字 + 加粗标签 + 几乎无卡片 |
| **悬念问题** | 抛出关键问题 | 居中衬线大问句 + 短横线装饰 |
| **大引用** | 金句/引述 | 超大引号 + 衬线引文 + 等宽出处 |

### Non-hero 页（信息承载者，使用 Bento 网格）

| 类型 | 说明 | 布局结构 |
|------|------|---------|
| **主从叙事** | 主卡叙事 + 嵌套子卡补充 | 大卡占左 8 列 + 右侧上下两组子卡 |
| **主卡+侧栏** | 大主卡 + 侧栏支撑 + 底部条带 | 主卡占左 10 列 + 右 6 列侧栏 + 底部通栏条 |
| **双主对比** | 两张对等主卡 + 指标高亮 | 左右各 8 列对等 + 下方高亮数据卡 |
| **主卡+三等分** | 主卡 + 三个并列子卡 | 主卡占左 10 列 + 右侧 3 个等宽子卡 |
| **节奏律动** | 小卡引出 → 大卡聚焦 → 双栏收尾 | 左小卡(5列) + 中大卡(11列) + 下方双栏 |

> ⚠️ 这些是描述性名称，**不要在 SVG 里发明新 class**。每个 Non-hero 页直接用 `rect` + `text` 组合实现。

### 节奏硬规则

- **Hero 页与 Non-hero 页必须交替**，制造"翻杂志的呼吸感"
- ⛔ **连续 3 页以上 Non-hero（Bento 网格页）→ 判为 P0 级错误**
- 一页密、一页疏 = 翻杂志时的呼吸感
- 推荐节奏模式：封面(H) → 目录(N) → 幕封(H) → 内容(N) → 大字报(H) → 内容(N) → 悬念(H) → 内容(N) → 大引用(H) → 结尾(H)

---

## 工作流

### Step 1 · 需求澄清（6 条追问）

用户说一句「帮我做一份杂志风 PPT」，你主动反向追问 6 条：

| # | 问题 | 为什么问 |
|---|------|---------|
| 1 | **受众是谁？什么场景？** | 决定语气和深浅（行业内部 / 商业发布 / 私享会） |
| 2 | **分享时长多久？** | 决定页数（15 分钟 ≈ 10 页，30 分钟 ≈ 20 页） |
| 3 | **有没有原始素材？** | 决定从零创作还是基于素材加工（文档、数据、旧 PPT、文章链接） |
| 4 | **有没有图片？放在哪？** | 决定要不要规划配图以及图片来源 |
| 5 | **想要哪套主题色？** | 从 5 套预设里选，决定整体视觉方向 |
| 6 | **有没有硬约束？** | 拦截翻工（必须包含 XX 数据 / 不能出现 YY） |

**不需要一次说完**，一条条追问即可。答完后先出大纲和主题节奏表，对齐后再开始写代码——这一步拦截 80% 的返工。

将澄清后的需求记录在 `项目目录/demand.md` 中。

#### 叙事弧模板（用户无素材时帮搭骨架）

如果用户只给主题、没有任何素材，用叙事弧五段法帮他搭大纲：

```
钩子(Hook)       → 1 页   : 抛一个反差 / 问题 / 硬数据让人停下来
定调(Context)    → 1-2 页 : 说明背景 / 你是谁 / 为什么讲这个
主体(Core)       → 3-5 页 : 核心内容，用 Non-hero 布局穿插
转折(Shift)      → 1 页   : 打破预期 / 提出新观点
收束(Takeaway)   → 1-2 页 : 金句 / 悬念问题 / 行动建议
```

叙事弧 + 页数规划 + 主题节奏表（见下方），**三张表对齐后再进 Step 2**。

#### 节奏规划表示例（生成大纲前必填）

```
| 页 | 主题          | 布局类型      | 备注           |
|---|--------------|-------------|---------------|
| 1  | hero dark   | 开场封面      |               |
| 2  | light       | 数据大字报    | 抛硬数据        |
| 3  | dark        | 主从叙事      |               |
| 4  | light       | 主卡+三等分   |               |
| 5  | hero light  | 章节幕封      | 呼吸页          |
| ...                            |               |
```

将节奏规划保存为 `项目目录/rhythm.md`，用户确认后再生成 JSON 大纲。

### Step 2 · 生成 PPT 大纲

读取 `<SKILL_ROOT>/assets/prompts/outline-architect.md`，按其格式输出 JSON 大纲。

**节奏规划**：大纲必须为每页标注页面类型（hero/non-hero），确保交替节奏。

**图片规划**：为需要配图的页面添加 `image_prompt` 字段（英文 prompt，供 AI 生图使用）。

将大纲保存为 `项目目录/outline.json`，确认后再进入下一步。

### Step 2.5 · 图片准备（可选）

如果大纲中有 `image_prompt` 字段，用户准备对应图片：

1. 图片放入 `项目目录/images/` 目录
2. 命名规则：`{页号补零}-{英文语义}.{jpg/png}`（如 `01-cover.jpg`）
3. 照片用 JPG，截图用 PNG，单张 ≥ 1600px 宽
4. 没有图片的页面会自动生成占位色块

**换图**：同名覆盖旧图，SVG 不改，重新运行转换器即可。

详见 `<SKILL_ROOT>/references/images.md`。

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
- 大标题/金句/核心论点 → font-family="Georgia, 'Noto Serif SC', serif" font-weight="700"
- 正文/列表/说明 → font-family="'PingFang SC', 'Microsoft YaHei', sans-serif" font-weight="300" 或 "400"
- 数据/页码/章节号/标注 → font-family="'SF Mono', 'Fira Code', 'Consolas', monospace"

> ⚠️ 中文标题用 `Noto Serif SC`，英文标题用 `Georgia`。严禁用宋体/Times New Roman 作为正文字体。

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
│   ├── images.md                         ← 图片系统规范（加图/换图/AI生图）
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
