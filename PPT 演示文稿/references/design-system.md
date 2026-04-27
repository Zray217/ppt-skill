# Design System — 汇报演示专版

## 汇报主题色预设（5 套 · 不允许自定义）

**⚠️ 硬规则：只允许从 5 套预设里选一套，不接受用户自定义 hex 值。**

### 1. 商务权威（Business Authority）

适合：战略汇报、年度报告、政府/金融场景

| Key | Value | 用途 |
|-----|-------|------|
| primary | `1B2A4A` | 深海军蓝，hero 背景、大标题 |
| secondary | `3D5A80` | 中蓝，副标题、body text |
| accent | `E0A526` | 金色，强调、CTA、数据高亮 |
| light | `F0F2F5` | 冷灰白，card 背景、区域分隔 |
| bg | `FFFFFF` | 纯白 |

**配色逻辑**：海军蓝传达权威与稳重，金色是权力的视觉锚点。所有 hero 页用 `primary` 做背景色，正文页用 `bg` 做背景色。金色只出现在需要决策者注意的地方——CTA 按钮、关键数据、行动项标记。

### 2. 科技蓝橙（Tech Blue-Orange）

适合：AI/云计算/数字化转型售前、技术路线汇报

| Key | Value | 用途 |
|-----|-------|------|
| primary | `0A1628` | 深蓝黑，hero 背景、大标题 |
| secondary | `1E3A8A` | 深蓝，副标题、body text |
| accent | `F97316` | 亮橙，强调、CTA、数据高亮 |
| light | `F8F9FA` | 浅灰白，card 背景 |
| bg | `FFFFFF` | 白色 |

**配色逻辑**：深蓝代表技术深度和可信度，亮橙制造"视觉钩子"——人眼对橙色的注意力是蓝色的 2 倍。蓝橙对比让关键数据从信息密度中跳出来。

### 3. 自然沉稳（Nature Grounded）

适合：ESG、可持续、基础设施、建筑设计

| Key | Value | 用途 |
|-----|-------|------|
| primary | `1A2E1F` | 深森林绿，hero 背景 |
| secondary | `3A5A40` | 中绿，副标题 |
| accent | `D4A373` | 暖木色，强调 |
| light | `F5F1E8` | 暖白，card 背景 |
| bg | `FBF8F3` | 纸白 |

**配色逻辑**：绿 + 木 = 自然 + 人造的对话。深绿传达可持续的严肃性，暖木色让方案看起来"落地"而非空谈。

### 4. 医疗洁净（Medical Clean）

适合：医疗、生物医药、健康科技

| Key | Value | 用途 |
|-----|-------|------|
| primary | `0A1F3D` | 深靛蓝，hero 背景 |
| secondary | `2563EB` | 亮蓝，副标题、链接 |
| accent | `06B6D4` | 青色，强调、数据高亮 |
| light | `F0F4F8` | 冷白，card 背景 |
| bg | `FFFFFF` | 纯白 |

**配色逻辑**：深靛 = 医疗的信任感，青色 = 洁净与创新。白色大面积使用传递"无污染"的潜意识。

### 5. 简约墨白（Ink & Paper）

适合：通用、创意提案、设计展示

| Key | Value | 用途 |
|-----|-------|------|
| primary | `0A0A0B` | 纯墨，hero 背景、大标题 |
| secondary | `374151` | 深灰，body text |
| accent | `DC2626` | 红色，强调、关键数据 |
| light | `F3F4F6` | 冷灰，card 背景 |
| bg | `FFFFFF` | 纯白 |

**配色逻辑**：黑白红的经典组合，删到最简。墨色只做 hero，白做正文，红只标记"必须注意"。

---

## 主题色使用硬规则

1. **一份 deck 只用一套主题**，不要中途换色
2. **不接受用户给的任意 hex 值**——委婉拒绝并展示 5 套让选
3. **不要混搭**（例如 primary 取商务权威、accent 取科技蓝橙）
4. **hero 页背景**用 `theme.primary`，正文页背景用 `theme.bg`
5. **accent 色**只用于：CTA 元素、关键数据高亮、行动项标记、当前步骤指示——不超过页面面积的 10%

---

## 字体分工体系

汇报场景的字体层级参考印刷行业的三级分工，但适配 PPT 的技术限制：

| 层级 | 字体 | 用途 | 字号范围 |
|------|------|------|---------|
| **标题层** | Arial Black / Impact | 大标题、hero 文字、章节号 | 36-96pt |
| **正文层** | Arial / Microsoft YaHei | 正文、说明、描述、列表 | 14-20pt |
| **元数据层** | Arial / Microsoft YaHei | 来源标注、日期、页码、备注 | 10-12pt |

### 字号对比硬规则

- **标题与正文的字号差 ≥ 2 倍**（标题 36pt → 正文 ≤ 18pt）
- **相邻文字元素的字号差 ≥ 20%**（避免"差不多大"的模糊感）
- **中文大标题 ≤ 8 字**，超过用 `<br>` 断行
- **数据数字 60-96pt**，必须比周围文字大 3 倍以上

### 字体使用禁区

- **不要**正文用 Bold——只有标题用 Bold
- **不要**标题和正文用同一字号
- **不要**用 3 种以上字号在同一页
- **不要**用 emoji 作图标

---

## 排版节奏规则

### hero vs non-hero 视觉差异

| 维度 | hero 页 | non-hero 页 |
|------|---------|-------------|
| 背景 | `theme.primary`（深色） | `theme.bg`（白色/浅色） |
| 文字颜色 | 白/浅色 | `theme.primary`/`theme.secondary` |
| 信息密度 | 极简（1-3 个元素） | 正常（5-10 个元素） |
| 留白 | ≥ 40% | 20-30% |
| 字号 | 偏大（48-96pt 核心） | 正常（14-36pt） |

### 节奏硬规则

1. 每 3-4 页插入 1 个 hero 页
2. 连续 3 页以上 non-hero = **不允许**
3. 连续 2 页以上 hero = **不允许**（hero 本身就是留白，连续留白 = 浪费）
4. 8 页以上 deck 必须有 ≥ 1 个 dark hero + ≥ 1 个 light hero
5. 整个 deck 不能只有 light 正文页，必须有 dark 正文页制造呼吸

### 各布局默认节奏

| Layout | 默认节奏 | 备注 |
|--------|---------|------|
| L01 封面 | hero (dark) | 开场 |
| L02 章节幕封 | hero | 多个幕封交替 dark/light |
| L03 核心数据 | hero 或 non-hero | hero 版：深底大字冲击；non-hero 版：白底卡片 |
| L04 要点陈述 | non-hero | 偶尔 hero：核心洞察 |
| L05 痛点 | hero 或 non-hero | hero 版：一个大问题 |
| L06 方案概览 | non-hero | |
| L07 流程 | non-hero | |
| L08 技术架构 | non-hero | |
| L09 对比 | non-hero | |
| L10 能力矩阵 | non-hero | |
| L11 ROI | non-hero | |
| L12 总结/行动 | hero 或 non-hero | hero 版：大结论 + 行动 |

---

## 原有设计系统（保留供参考）

### Color Palette Reference

| # | Name | Colors | Style | Use Cases | Tips |
|---|------|--------|-------|-----------|------|
| 1 | Modern & Wellness | `#006d77` `#83c5be` `#edf6f9` `#ffddd2` `#e29578` | Fresh, soothing | Healthcare, counseling, skincare, yoga/spa | Deep teal for titles, light pink for background |
| 2 | Business & Authority | `#2b2d42` `#8d99ae` `#edf2f4` `#ef233c` `#d90429` | Formal, classic | Annual reports, financial analysis, corporate intro, government | Deep blue for professionalism, bright red to highlight data |
| 3 | Nature & Outdoors | `#606c38` `#283618` `#fefae0` `#dda15e` `#bc6c25` | Grounded, earthy | Outdoor gear, environmental, agriculture, historical culture | Dark green base, cream text |
| 4 | Vintage & Academic | `#780000` `#c1121f` `#fdf0d5` `#003049` `#669bbc` | Classic, scholarly | Academic lectures, history reviews, museums, heritage brands | Strong contrast between deep red and deep blue |
| 5 | Soft & Creative | `#cdb4db` `#ffc8dd` `#ffafcc` `#bde0fe` `#a2d2ff` | Dreamy, candy-toned | Mother & baby, desserts, women's fashion, kindergarten | Use dark gray or black for text |
| 6 | Bohemian | `#ccd5ae` `#e9edc9` `#fefae0` `#faedcd` `#d4a373` | Gentle, muted | Wedding planning, home decor, organic food, slow living | Cream background, green-brown accents |
| 7 | Vibrant & Tech | `#8ecae6` `#219ebc` `#023047` `#ffb703` `#fb8500` | High energy, sporty | Sports events, gyms, startup pitches, youth education | Deep blue for stability, orange as focal accent |
| 8 | Craft & Artisan | `#7f5539` `#a68a64` `#ede0d4` `#656d4a` `#414833` | Rustic, coffee-toned | Coffee shops, handicrafts, traditional culture, bakery | Suited for paper/leather textures |
| 9 | Tech & Night | `#000814` `#001d3d` `#003566` `#ffc300` `#ffd60a` | Deep, luminous | Tech launches, astronomy, night economy, luxury automobiles | Must use dark mode |
| 10 | Education & Charts | `#264653` `#2a9d8f` `#e9c46a` `#f4a261` `#e76f51` | Clear, logical | Statistical reports, education, market analysis, general business | Perfect chart color scheme |
| 11 | Forest & Eco | `#dad7cd` `#a3b18a` `#588157` `#3a5a40` `#344e41` | Monochrome gradient, forest | Landscape design, ESG reports, environmental causes, botanical | Monochrome palette is safe and cohesive |
| 12 | Elegant & Fashion | `#edafb8` `#f7e1d7` `#dedbd2` `#b0c4b1` `#4a5759` | Muted, Morandi tones | Haute couture, art galleries, beauty brands, magazine style | Negative space is key |
| 13 | Art & Food | `#335c67` `#fff3b0` `#e09f3e` `#9e2a2b` `#540b0e` | Rich, vintage-poster | Food documentaries, art exhibitions, ethnic themes, vintage restaurants | Works well with large color blocks |
| 14 | Luxury & Mysterious | `#22223b` `#4a4e69` `#9a8c98` `#c9ada7` `#f2e9e4` | Cool, purple-toned | Jewelry showcases, hotel management, high-end consulting, psychology | Purple evokes premium atmosphere |
| 15 | Pure Tech Blue | `#03045e` `#0077b6` `#00b4d8` `#90e0ef` `#caf0f8` | Futuristic, clean | Cloud/AI, water/ocean, hospitals, clean energy | Deep ocean to sky gradient |
| 16 | Coastal Coral | `#0081a7` `#00afb9` `#fdfcdc` `#fed9b7` `#f07167` | Refreshing, summery | Travel, summer events, beverage brands, ocean themes | Teal and coral as complementary focal colors |
| 17 | Vibrant Orange Mint | `#ff9f1c` `#ffbf69` `#ffffff` `#cbf3f0` `#2ec4b6` | Bright, cheerful | Children's events, promotional posters, FMCG, social media | Orange grabs attention, mint feels fresh |
| 18 | Platinum White Gold | `#0a0a0a` `#0070F3` `#D4AF37` `#f5f5f5` `#ffffff` | Premium, professional | Agent products, corporate websites, fintech, luxury brands | White-gold base, blue for action, gold for emphasis |

> **注意**：以上 18 套调色板为原有设计系统的完整保留。汇报场景优先使用上方的 5 套汇报主题预设。如用户需要更多选择，可从这 18 套中选取，但仍须映射到 5 个 theme key。

---

## Color Palette Rules (MANDATORY)

### Strict Palette Adherence

**Use ONLY the provided color palette. Do NOT create or modify colors.**

- All colors must come from the selected theme preset
- Do NOT use colors outside the palette
- Do NOT modify palette colors (brightness, saturation, mixing)
- **Only exception**: Add transparency using the `transparency` property (0-100)

```javascript
// Correct: Using palette colors
slide.addShape(pres.shapes.RECTANGLE, { fill: { color: theme.primary } });
slide.addText("Title", { color: theme.accent });

// Wrong: Colors outside palette
slide.addShape(pres.shapes.RECTANGLE, { fill: { color: "1a1a2e" } });
```

### No Gradients

**Gradients are prohibited. Use solid colors only.**

### No Animations

**Animations and transitions are prohibited.** All slides must be static.

---

## Font Reference

### Recommended Fonts

| Language | Default Font | Alternatives |
|----------|-------------|--------------|
| **Chinese** | Microsoft YaHei | — |
| **English** | Arial | Georgia, Calibri, Cambria, Trebuchet MS |

- For mixed Chinese-English content: use Microsoft YaHei for Chinese, the chosen font for English
- Prefer system fonts for cross-platform compatibility
- Titles and body text can use different font pairings (e.g. Georgia + Calibri)

### Recommended Font Pairings

| Header Font | Body Font | 适用场景 |
|-------------|-----------|---------|
| Arial Black | Arial | 通用商务 |
| Georgia | Calibri | 偏人文/学术 |
| Impact | Arial | 强冲击/售前 |
| Cambria | Calibri | 政府汇报 |

### No Bold for Body Text

**Plain body text and caption/legend text must NOT use bold.**

- Body paragraphs, descriptions → normal weight
- Captions, legends, footnotes → normal weight
- Reserve bold for titles and headings only

---

## Style Recipes

The same design can be rendered in 4 distinct visual styles by adjusting corner radius (`rectRadius`) and spacing. Choose the style recipe that fits the presentation tone.

> **Unit note**: PptxGenJS uses inches. Slide dimensions are 10" x 5.625" (LAYOUT_16x9).

### Style Overview

| Style | Corner Radius | Spacing | Best For |
|-------|--------------|---------|----------|
| **Sharp & Compact** | 0 ~ 0.05" | Tight | 数据密集型汇报、财务报表 |
| **Soft & Balanced** | 0.08" ~ 0.12" | Moderate | 通用商务汇报、战略规划 |
| **Rounded & Spacious** | 0.15" ~ 0.25" | Relaxed | 产品介绍、售前提案 |
| **Pill & Airy** | 0.3" ~ 0.5" | Open | 品牌展示、发布会 |

### Sharp & Compact

**Visual character**: Geometric, high information density, formal and serious.

| Category | Value (inches) | Notes |
|----------|---------------|-------|
| Corner radius — small | 0" | Full right angle |
| Corner radius — medium | 0.03" | Micro-rounded |
| Corner radius — large | 0.05" | Slight rounding |
| Element padding | 0.1" ~ 0.15" | Compact |
| Element gap | 0.1" ~ 0.2" | Compact |
| Page margin | 0.3" | Narrow |
| Block gap | 0.25" ~ 0.35" | Compact |

### Soft & Balanced

**Visual character**: Moderate rounding, comfortable whitespace, professional yet approachable.

| Category | Value (inches) | Notes |
|----------|---------------|-------|
| Corner radius — small | 0.05" | Slight rounding |
| Corner radius — medium | 0.08" | Medium rounding |
| Corner radius — large | 0.12" | Larger rounding |
| Element padding | 0.15" ~ 0.2" | Moderate |
| Element gap | 0.15" ~ 0.25" | Moderate |
| Page margin | 0.4" | Standard |
| Block gap | 0.35" ~ 0.5" | Moderate |

### Rounded & Spacious

**Visual character**: Large corners, generous whitespace, friendly and modern.

| Category | Value (inches) | Notes |
|----------|---------------|-------|
| Corner radius — small | 0.1" | Medium rounding |
| Corner radius — medium | 0.15" | Large rounding |
| Corner radius — large | 0.25" | Very large rounding |
| Element padding | 0.2" ~ 0.3" | Relaxed |
| Element gap | 0.25" ~ 0.4" | Relaxed |
| Page margin | 0.5" | Wide |
| Block gap | 0.5" ~ 0.7" | Relaxed |

### Pill & Airy

**Visual character**: Full pill-shaped corners, abundant whitespace, light and open feel, strong brand presence.

| Category | Value (inches) | Notes |
|----------|---------------|-------|
| Corner radius — small | 0.2" | Large rounding |
| Corner radius — medium | 0.3" | Pill shape |
| Corner radius — large | 0.5" | Full pill |
| Element padding | 0.25" ~ 0.4" | Open |
| Element gap | 0.3" ~ 0.5" | Open |
| Page margin | 0.6" | Wide |
| Block gap | 0.6" ~ 0.9" | Open |

### Component Style Mapping

| Component | Sharp | Soft | Rounded | Pill |
|-----------|-------|------|---------|------|
| **Button / Tag** | rectRadius: 0 | rectRadius: 0.05 | rectRadius: 0.1 | rectRadius: 0.2 |
| **Card / Container** | rectRadius: 0.03 | rectRadius: 0.1 | rectRadius: 0.2 | rectRadius: 0.3 |
| **Image Container** | rectRadius: 0 | rectRadius: 0.08 | rectRadius: 0.15 | rectRadius: 0.25 |
| **Input Field** | rectRadius: 0 | rectRadius: 0.05 | rectRadius: 0.1 | rectRadius: 0.2 |
| **Badge** | rectRadius: 0.02 | rectRadius: 0.05 | rectRadius: 0.08 | rectRadius: 0.15 |
| **Avatar Frame** | rectRadius: 0 | rectRadius: 0.1 | rectRadius: 0.2 | rectRadius: 0.5 (circle) |

### Mixing Rules

#### 1. Outer container corner >= inner element corner

```javascript
// Correct: outer > inner
card:   rectRadius: 0.2
button: rectRadius: 0.1

// Wrong: inner > outer → visual overflow effect
card:   rectRadius: 0.1
button: rectRadius: 0.2
```

#### 2. Information density drives spacing

| Zone Type | Recommended Style |
|-----------|------------------|
| Data display zone | Sharp / Soft (compact spacing) |
| Content browsing zone | Rounded / Pill (relaxed spacing) |
| Title zone | Soft / Rounded (moderate spacing) |

### Typography Scale (PPT)

| Usage | Size (pt) | Notes |
|-------|-----------|-------|
| Annotations / Sources | 10 ~ 12 | Minimum readable size |
| Body / Description | 14 ~ 16 | Standard body |
| Subtitle | 18 ~ 22 | Secondary heading |
| Title | 28 ~ 36 | Page title |
| Large Title | 44 ~ 60 | Cover / section title |
| Data Callout | 60 ~ 96 | Key number display |

### Spacing Scale (PPT)

Based on 10" x 5.625" slide dimensions:

| Usage | Recommended (inches) |
|-------|---------------------|
| Icon-to-text gap | 0.08" ~ 0.15" |
| List item spacing | 0.15" ~ 0.25" |
| Card inner padding | 0.2" ~ 0.4" |
| Element group gap | 0.3" ~ 0.5" |
| Page safe margin | 0.4" ~ 0.6" |
| Major block gap | 0.5" ~ 0.8" |

### Quick Selection Guide

| Presentation Type | Recommended Style | Reason |
|------------------|------------------|--------|
| Finance / Data reports | Sharp & Compact | High density, serious and precise |
| Corporate / Business | Soft & Balanced | Balances professionalism and approachability |
| Product intro / Pre-sales | Rounded & Spacious | Modern feel, friendly |
| Launch events / Brand | Pill & Airy | Premium feel, visual impact |
| Training / Education | Soft / Rounded | Clear, readable, friendly |
| Tech sharing | Sharp / Soft | Professional, information-dense |
