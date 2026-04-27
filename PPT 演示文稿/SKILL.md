# PPTX Generator & Editor — 汇报演示专版

## Overview

本 Skill 生成面向**商业汇报**场景的 PPT 演示文稿（.pptx 格式），覆盖售前提案、战略规划、项目复盘、季度汇报、投资路演等典型场景。

核心设计哲学：**结构优于装饰，节奏优于堆砌，权重由内容驱动**。每一页都是叙事的一个节拍——hero 页制造停顿与冲击，data 页传递硬信息，收束页推动决策。页面不是模板的填空题，而是内容的 Bento 便当盒——卡片大小由信息重要性决定，最重要的放最大，辅助的放小。

## Quick Reference

| Task | Approach |
|------|----------|
| Read/analyze content | `python -m markitdown presentation.pptx` |
| Edit or create from template | See [editing.md](references/editing.md) |
| Create from scratch | See [Creating from Scratch](#creating-from-scratch-workflow) below |

| Item | Value |
|------|-------|
| **Dimensions** | 10" x 5.625" (LAYOUT_16x9) |
| **Colors** | 6-char hex without # (e.g., `"FF0000"`) |
| **English font** | Arial (default), or approved alternatives |
| **Chinese font** | Microsoft YaHei |
| **Page badge position** | x: 9.3", y: 5.1" |
| **Theme keys** | `primary`, `secondary`, `accent`, `light`, `bg` |
| **Shapes** | RECTANGLE, OVAL, LINE, ROUNDED_RECTANGLE |
| **Charts** | BAR, LINE, PIE, DOUGHNUT, SCATTER, BUBBLE, RADAR |

## Reference Files

| File | Contents |
|------|----------|
| [slide-types.md](references/slide-types.md) | 12 种汇报页面布局（含节奏标记、网格比例、适用场景） |
| [design-system.md](references/design-system.md) | 5 套汇报主题预设、字体分工、排版节奏规则、样式配方 |
| [editing.md](references/editing.md) | Template-based editing workflow, XML manipulation |
| [pitfalls.md](references/pitfalls.md) | QA process, common mistakes, critical PptxGenJS pitfalls |
| [checklist.md](references/checklist.md) | P0/P1/P2/P3 分级质量检查清单 |
| [pptxgenjs.md](references/pptxgenjs.md) | Complete PptxGenJS API reference |

---

## 核心设计原则

这些原则是从汇报场景的实际需求中提炼出来的。违反任何一条，汇报效果都会打折。

| # | 原则 | 说明 |
|---|------|------|
| 1 | **节奏靠 hero 页** | hero 页（封面/章节幕封/核心洞察）与 non-hero 页交替，才不累眼睛。连续 3 页以上同节奏 = 视觉疲劳 |
| 2 | **结构优于装饰** | 不用渐变、不用阴影浮层、不用装饰线条。信息层级靠**字号对比 + 色块 + 网格留白**定义 |
| 3 | **一页一核心信息** | 决策者每页只记住一件事。数据页只放一组关键数据，流程页只走一条线，对比页只比一个维度 |
| 4 | **约束优于自由** | 只从 5 套主题预设中选一套，不接受自定义 hex。约束越严，风格越稳 |
| 5 | **数据必须可追溯** | 所有数据必须标注来源和口径。没有来源的数据不如不放 |
| 6 | **收束必须推动决策** | 汇报的终点不是"谢谢"，而是"接下来做什么"。Summary 页必须有明确的 action items |
| 7 | **卡片权重由内容驱动** | 不对等分配空间——核心信息占大卡片，辅助信息挤小卡片。对称 = 平庸，非对称 = 层级感（Bento 便当盒法则） |
| 8 | **页内金字塔——结论先行** | 每页视觉权重最大的元素 = 该页核心结论，不是铺垫。先看到结论，再看到论据，符合决策者的注意力窗口 |

---

## Creating from Scratch — Workflow

**Use when no template or reference presentation is available.**

### Step 1 · 需求澄清（动手前必做）

**如果用户已经给了完整的大纲 + 数据** → 跳过直接进 Step 2。

**如果用户只给了主题或模糊想法** → 用以下 6 个问题逐个对齐：

| # | 问题 | 为什么要问 |
|---|------|-----------|
| 1 | **汇报对象是谁？决策权在哪？**（高管/业务负责人/投资人/采购委员会） | 决定信息密度和语言风格 |
| 2 | **汇报时长？** | 5 分钟 ≈ 5-8 页，15 分钟 ≈ 12-18 页，30 分钟 ≈ 20-28 页 |
| 3 | **有没有原始素材？**（文档/数据/旧PPT/竞品资料） | 有素材就基于素材，没有就帮搭骨架 |
| 4 | **核心结论是什么？** | 先定结论再搭论据——汇报是"倒叙"不是"顺叙" |
| 5 | **想要哪套主题色？** | 见 design-system.md，5 套预设选一 |
| 6 | **有没有硬约束？**（必须包含 XX 数据 / 不能出现 YY / 公司品牌色） | 避免返工 |

澄清完成后，先输出**大纲 + 节奏表**，对齐后再进 Step 2。

#### 叙事弧模板（汇报专用）

汇报不是从 A 讲到 Z，而是**先抛结论，再铺论据，最后推决策**：

```
钩子(Hook)       → 1 页   : 核心结论/关键数据/反差问题——让决策者停下来
背景(Context)    → 1-2 页 : 问题定义/现状描述/为什么今天要谈这个
论据(Evidence)   → 3-6 页 : 数据支撑、方案对比、案例实证
洞察(Insight)    → 1-2 页 : 从数据中提炼的核心判断——打破预期
行动(Action)     → 1-2 页 : 下一步做什么、谁负责、时间节点
```

#### 节奏表模板

在写任何代码之前，必须列出每一页的：

| 页号 | 节奏类型 | 布局 | 卡片组合 | 主题色 | 核心信息(★) |
|------|---------|------|---------|--------|------------|
| 1 | hero | L01 封面 | 单一焦点 | dark | 项目名称 |
| 2 | non-hero | L03 核心数据 | 顶部Hero+网格 | light | 关键指标 |
| 3 | non-hero | L14 非对称双栏 | 2/3+1/3 | light | 现状 vs 目标 |
| ... | ... | ... | ... | ... | ... |

**节奏硬规则**：
- hero 页与 non-hero 页**必须交替**——每 3-4 页插入 1 个 hero（封面/幕封/核心洞察/大引用）
- 连续 3 页以上同节奏 = **不允许**
- 8 页以上**必须**有 ≥ 1 个 dark hero + ≥ 1 个 light hero
- 整个 deck **不能**只有 light 正文页，**必须**有 dark 正文页制造视觉呼吸

#### 图片约定

| 约定项 | 规则 |
|--------|------|
| **文件夹位置** | `slides/imgs/` 下（和 `compile.js` 同级） |
| **命名规范** | `{页号}-{语义}.{ext}`，如 `01-cover.jpg` / `03-architecture.png` |
| **规格建议** | 单张 ≥ 1600px 宽；JPG 用于照片，PNG 用于截图/图表 |
| **如何替换** | 保持同名覆盖最稳——JS 不用改路径 |
| **没图怎么办** | 先用色块占位，后期补图；但需告知图文混排页没图无法验证效果 |

---

### Step 2 · 选定主题色（5 套预设 · 不允许自定义）

**⚠️ 硬规则：只允许从 5 套预设里选一套，不接受用户自定义 hex 值。**

| # | 主题 | 适合场景 | 色调特征 |
|---|------|---------|---------|
| 1 | 商务权威 | 战略汇报/年度报告/政府/金融 | 深蓝黑底 + 银白/金 |
| 2 | 科技蓝橙 | AI/云计算/数字化转型/售前 | 深蓝底 + 亮橙提亮 |
| 3 | 自然沉稳 | ESG/可持续发展/基础设施/建筑 | 森绿底 + 暖木色 |
| 4 | 医疗洁净 | 医疗/生物医药/健康科技 | 深靛底 + 冷白 |
| 5 | 简约墨白 | 通用/创意提案/设计展示 | 纯墨底 + 纸白 |

**操作流程**：
1. 基于内容主题推荐一套，或直接问用户选哪一套
2. 从 design-system.md 中读取对应主题的 5 个色值（primary/secondary/accent/light/bg）
3. 写入 `compile.js` 的 theme 对象

**硬规则**：
- 一份 deck **只用一套主题**，不要中途换色
- **不接受用户给的任意 hex 值**——委婉拒绝并展示 5 套让选
- **不要混搭**

---

### Step 3 · 规划页面布局与节奏

**在写任何 slide 代码之前**，必须完成两件事：

#### 3.1 · 节奏规划（和 Step 1 的节奏表对齐）

每页标记为 **hero** 或 **non-hero**：

| 页面类型 | 节奏 | 说明 |
|---------|------|------|
| 封面 | hero | 开场定调 |
| 章节幕封 | hero | 章节分隔，制造呼吸 |
| 核心数据/大字报 | hero | 关键数字冲击 |
| 核心洞察/问题 | hero | 反差/提问——打破惯性 |
| 大引用/金句 | hero | 衬线仪式感 |
| 其他内容页 | non-hero | 信息承载 |

**推荐节奏模式**：
```
Hero(Cover) → Non-hero(数据) → Non-hero(对比) → Hero(幕封) →
Non-hero(方案) → Non-hero(流程) → Non-hero(ROI) → Hero(洞察) →
Non-hero(案例) → Non-hero(能力) → Hero(行动)
```

#### 3.2 · 布局选择与 Bento 卡片组合

**设计哲学转变**：不要"先选模板再填内容"，而要"先分析内容权重，再用卡片组合呈现"。

##### 第一步：分析内容权重

每一页的内容都可以拆解为若干信息块。对每个信息块标注权重：

| 权重 | 标记 | 视觉面积占比 | 放哪里 |
|------|------|-------------|--------|
| **核心** | `★` | 40-60% 页面面积 | 大卡片（主卡片） |
| **支撑** | `◆` | 15-25% 页面面积 | 中卡片 |
| **辅助** | `●` | 5-15% 页面面积 | 小卡片/标签 |

**示例**：方案概览页 → 核心方案名称(★) + 3个支柱(◆) + 数据佐证(●)

##### 第二步：选择卡片组合模式

| 组合模式 | 骨架 | 适合 | 惊艳指数 |
|---------|------|------|---------|
| **Hero+Sub** | 1大卡(60%) + 2-3小卡(40%) | 核心结论+支撑论据 | ★★★★★ |
| **非对称双栏** | 2/3左栏 + 1/3右栏 | 文字为主+数据提亮 | ★★★★ |
| **焦点+环绕** | 中心大卡 + 4角小卡 | 系统架构/中心辐射 | ★★★★★ |
| **顶部Hero+底部网格** | 顶栏横卡 + 底2-4小卡 | 关键数据+分项说明 | ★★★★ |
| **混合网格** | 自由组合不同尺寸卡片 | 多维度信息、最适合Bento | ★★★★★ |
| **对称等分** | 2-4等宽卡片 | 并列对比（最稳也最平） | ★★ |

**硬规则**：
- **同一 deck 中对称等分布局不超过 3 页**——对称是安全牌但也是平庸之源
- **至少 40% 的内容页使用非对称组合**——这是"惊艳"的关键
- **大卡片的字号必须 ≥ 小卡片字号的 2 倍**——没有字号差就没有层级差
- **卡片间距统一 0.15-0.2"**（PptxGenJS 坐标系）——间距不一致 = 杂乱

##### 第三步：映射到 slide-types.md 的布局类型

卡片组合模式映射到 L01-L16 布局类型。打开 `references/slide-types.md` 选择。**不要从零写 slide**。

| Layout | 用途 | 节奏 | 卡片组合 |
|--------|------|------|---------|
| L01 封面 | 第 1 页 | hero | 单一焦点 |
| L02 章节幕封 | 每幕开场 | hero | 单一焦点 |
| L03 核心数据 | 关键指标展示 | hero/non-hero | 顶部Hero+底部网格 / 对称等分 |
| L04 要点陈述 | 核心论点/结论 | non-hero | Hero+Sub |
| L05 痛点/问题 | 问题定义 | hero/non-hero | 非对称双栏 / Hero+Sub |
| L06 方案概览 | 解决方案总览 | non-hero | 焦点+环绕 / 混合网格 |
| L07 流程/阶段 | 工作流/实施路径 | non-hero | 顶部Hero+底部网格 |
| L08 技术架构 | 系统架构/层次 | non-hero | 焦点+环绕 / 非对称双栏 |
| L09 对比/Before-After | 旧 vs 新/A vs B | non-hero | 非对称双栏（新侧大） |
| L10 能力矩阵 | 多维度评估 | non-hero | 混合网格 |
| L11 ROI/成效 | 量化收益 | non-hero | Hero+Sub（大数字+图表） |
| L12 总结/行动 | 收束 + 行动项 | hero/non-hero | Hero+Sub |
| L13 Hero+Sub | 核心结论+支撑 | non-hero | 1大卡+2-3小卡 |
| L14 非对称双栏 | 主+辅 | non-hero | 2/3+1/3 |
| L15 焦点+环绕 | 中心辐射 | non-hero | 中心卡+4角卡 |
| L16 混合网格 | 自由组合 | non-hero | 自由尺寸 |

**布局多样性硬规则**：
- 相邻 2 页**不允许**使用同一布局
- 整个 deck 中同一布局**不超过 3 次**
- 12 页以上的 deck 至少使用 **6 种不同布局**
- **10 页以上 deck 至少 3 页使用非对称组合**（L13/L14/L15/L16）

---

### Step 4 · Generate Slide JS Files

Create one JS file per slide in `slides/` directory. Each file must export a synchronous `createSlide(pres, theme)` function. Follow the [Slide Output Format](#slide-output-format) and the type-specific guidance in [slide-types.md](references/slide-types.md). Generate up to 5 slides concurrently using subagents if available.

**Tell each subagent:**
1. File naming: `slides/slide-01.js`, `slides/slide-02.js`, etc.
2. Images go in: `slides/imgs/`
3. Final PPTX goes in: `slides/output/`
4. Dimensions: 10" x 5.625" (LAYOUT_16x9)
5. Fonts: Chinese = Microsoft YaHei, English = Arial (or approved alternative)
6. Colors: 6-char hex without # (e.g. `"FF0000"`)
7. Must use the theme object contract (see [Theme Object Contract](#theme-object-contract))
8. Must follow the [PptxGenJS API reference](references/pptxgenjs.md)
9. **Must follow the rhythm and layout rules** from this SKILL.md

---

### Step 5 · Compile into Final PPTX

Create `slides/compile.js` to combine all slide modules:

```javascript
// slides/compile.js
const pptxgen = require('pptxgenjs');
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';

// 从 design-system.md 中选取的汇报主题
const theme = {
  primary: "0A1628",    // 深蓝黑
  secondary: "1E3A8A",  // 深蓝
  accent: "F97316",     // 橙色提亮
  light: "F8F9FA",      // 浅灰白
  bg: "FFFFFF"          // 白色背景
};

for (let i = 1; i <= 12; i++) {  // adjust count as needed
  const num = String(i).padStart(2, '0');
  const slideModule = require(`./slide-${num}.js`);
  slideModule.createSlide(pres, theme);
}

pres.writeFile({ fileName: './output/presentation.pptx' });
```

Run with: `cd slides && node compile.js`

---

### Step 6 · QA（必须执行）

打开 `references/checklist.md` 逐项对照。

**特别要注意的 P0 级问题**：
1. hero 页与 non-hero 页是否交替——连续 3+ 页同节奏 = 失败
2. 相邻 2 页是否使用了同一布局——是 = 失败
3. 数据是否标注来源——没来源 = 失败
4. 总结页是否有明确的行动项——没有 = 失败
5. 大标题字号是否足够突出（36pt+）——不够 = 失败
6. body text 是否左对齐——居中 = 失败
7. 是否有纯文字无视觉元素的页面——有 = 失败

### Output Structure

```
slides/
├── slide-01.js          # Slide modules
├── slide-02.js
├── ...
├── imgs/                # Images used in slides
└── output/              # Final artifacts
    └── presentation.pptx
```

---

## Slide Output Format

Each slide is a **complete, runnable JS file**:

```javascript
// slide-01.js
const pptxgen = require("pptxgenjs");

const slideConfig = {
  type: 'cover',        // 布局类型（对应 slide-types.md 的 L01-L12）
  rhythm: 'hero',       // 节奏标记：hero 或 non-hero
  index: 1,
  title: 'Presentation Title'
};

// MUST be synchronous (not async)
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  slide.addText(slideConfig.title, {
    x: 0.5, y: 2, w: 9, h: 1.2,
    fontSize: 48, fontFace: "Arial",
    color: theme.primary, bold: true, align: "center"
  });

  return slide;
}

// Standalone preview
if (require.main === module) {
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_16x9';
  const theme = {
    primary: "0A1628",
    secondary: "1E3A8A",
    accent: "F97316",
    light: "F8F9FA",
    bg: "FFFFFF"
  };
  createSlide(pres, theme);
  pres.writeFile({ fileName: "slide-01-preview.pptx" });
}

module.exports = { createSlide, slideConfig };
```

---

## Theme Object Contract (MANDATORY)

The compile script passes a theme object with these **exact keys**:

| Key | Purpose | Example |
|-----|---------|---------|
| `theme.primary` | Darkest color, titles, hero backgrounds | `"0A1628"` |
| `theme.secondary` | Dark accent, body text, secondary elements | `"1E3A8A"` |
| `theme.accent` | Highlight color, CTA, data emphasis | `"F97316"` |
| `theme.light` | Light accent, card backgrounds, subtle fills | `"F8F9FA"` |
| `theme.bg` | Background color | `"FFFFFF"` |

**NEVER use other key names** like `background`, `text`, `muted`, `darkest`, `lightest`.

---

## Page Number Badge (REQUIRED)

All slides **except Cover Page** MUST include a page number badge in the bottom-right corner.

- **Position**: x: 9.3", y: 5.1"
- Show current number only (e.g. `3` or `03`), NOT "3/12"
- Use palette colors, keep subtle

### Circle Badge (Default)

```javascript
slide.addShape(pres.shapes.OVAL, {
  x: 9.3, y: 5.1, w: 0.4, h: 0.4,
  fill: { color: theme.accent }
});
slide.addText("3", {
  x: 9.3, y: 5.1, w: 0.4, h: 0.4,
  fontSize: 12, fontFace: "Arial",
  color: "FFFFFF", bold: true,
  align: "center", valign: "middle"
});
```

### Pill Badge

```javascript
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 9.1, y: 5.15, w: 0.6, h: 0.35,
  fill: { color: theme.accent },
  rectRadius: 0.15
});
slide.addText("03", {
  x: 9.1, y: 5.15, w: 0.6, h: 0.35,
  fontSize: 11, fontFace: "Arial",
  color: "FFFFFF", bold: true,
  align: "center", valign: "middle"
});
```

---

## 5 套汇报主题色预设

### 1. 商务权威（Business Authority）

适合：战略汇报、年度报告、政府/金融场景

| Key | Value | 用途 |
|-----|-------|------|
| primary | `1B2A4A` | 深海军蓝，hero 背景、大标题 |
| secondary | `3D5A80` | 中蓝，副标题、body text |
| accent | `E0A526` | 金色，强调、CTA、数据高亮 |
| light | `F0F2F5` | 冷灰白，card 背景、区域分隔 |
| bg | `FFFFFF` | 纯白 |

### 2. 科技蓝橙（Tech Blue-Orange）

适合：AI/云计算/数字化转型售前、技术路线汇报

| Key | Value | 用途 |
|-----|-------|------|
| primary | `0A1628` | 深蓝黑，hero 背景、大标题 |
| secondary | `1E3A8A` | 深蓝，副标题、body text |
| accent | `F97316` | 亮橙，强调、CTA、数据高亮 |
| light | `F8F9FA` | 浅灰白，card 背景 |
| bg | `FFFFFF` | 白色 |

### 3. 自然沉稳（Nature Grounded）

适合：ESG、可持续、基础设施、建筑设计

| Key | Value | 用途 |
|-----|-------|------|
| primary | `1A2E1F` | 深森林绿，hero 背景 |
| secondary | `3A5A40` | 中绿，副标题 |
| accent | `D4A373` | 暖木色，强调 |
| light | `F5F1E8` | 暖白，card 背景 |
| bg | `FBF8F3` | 纸白 |

### 4. 医疗洁净（Medical Clean）

适合：医疗、生物医药、健康科技

| Key | Value | 用途 |
|-----|-------|------|
| primary | `0A1F3D` | 深靛蓝，hero 背景 |
| secondary | `2563EB` | 亮蓝，副标题、链接 |
| accent | `06B6D4` | 青色，强调、数据高亮 |
| light | `F0F4F8` | 冷白，card 背景 |
| bg | `FFFFFF` | 纯白 |

### 5. 简约墨白（Ink & Paper）

适合：通用、创意提案、设计展示

| Key | Value | 用途 |
|-----|-------|------|
| primary | `0A0A0B` | 纯墨，hero 背景、大标题 |
| secondary | `374151` | 深灰，body text |
| accent | `DC2626` | 红色，强调、关键数据 |
| light | `F3F4F6` | 冷灰，card 背景 |
| bg | `FFFFFF` | 纯白 |

---

## Dependencies

- `pip install "markitdown[pptx]"` — text extraction
- `npm install -g pptxgenjs` — creating from scratch
- `npm install -g react-icons react react-dom sharp` — icons (optional)
