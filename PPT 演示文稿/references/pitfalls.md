# QA Process & Common Pitfalls — 汇报演示专版

## QA Process

**Assume there are problems. Your job is to find them.**

Your first render is almost never correct. Approach QA as a bug hunt, not a confirmation step. If you found zero issues on first inspection, you weren't looking hard enough.

### Content QA

```bash
python -m markitdown output.pptx
```

Check for missing content, typos, wrong order.

**Check for leftover placeholder text:**

```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|placeholder|this.*(page|slide).*layout"
```

If grep returns results, fix them before declaring success.

### Rhythm QA（汇报场景新增）

**生成后必须检查节奏**：

1. 列出每页的 rhythm 标记（hero / non-hero）
2. 检查是否有连续 3+ 页同节奏
3. 检查是否有连续 2+ 页同布局
4. 检查 dark/light hero 是否交替
5. 检查总结页是否有行动项

### Verification Loop

1. Generate slides → Extract text with `python -m markitdown output.pptx` → Review content
2. **List issues found** (if none found, look again more critically)
3. **Check rhythm** (see Rhythm QA above)
4. Fix issues
5. **Re-verify affected slides** — one fix often creates another problem
6. Repeat until a full pass reveals no new issues

**Do not declare success until you've completed at least one fix-and-verify cycle.**

### Per-Slide QA (for from-scratch creation)

```bash
python -m markitdown slide-XX-preview.pptx
```

Check for missing content, placeholder text, missing page number badge, rhythm marker.

---

## 汇报场景特有 Pitfalls

### 节奏类

- **连续 3+ 页 non-hero** → 缺少呼吸，决策者开始走神。每 3-4 页插一个 hero（幕封/核心数据/大洞察）
- **连续 2+ 页 hero** → hero 的意义是"停顿"，连续停顿 = 浪费页面
- **全是 light 正文页** → 视觉单调，像白板堆砌。必须有 dark 正文页制造对比
- **相邻两页同一布局** → 视觉重复，像复制粘贴。换一种布局或调整网格比例

### Bento 卡片组合类

| 级别 | Pitfall | 说明 | 修复 |
|------|---------|------|------|
| P0 | **对称依赖症** | 所有内容页都是等宽等高的卡片，视觉像 Excel 表格 | 至少 40% 页面用非对称组合（L13-L16） |
| P0 | **字号无层级** | 大卡片和小卡片字号差 < 2 倍，看不出谁是重点 | 大卡字号 ≥ 小卡 × 2，数据卡 60pt+ |
| P1 | **卡片全等** | 一页 3-4 张卡片大小完全一样 | 用 ★◆● 权重标记，核心卡放大 50%+ |
| P1 | **间距不一致** | 卡片间缝隙忽大忽小 | 统一 gap = 0.15"，用变量计算坐标 |
| P2 | **大卡内容空洞** | 大卡片只放了 3 个字，空荡荡 | 大卡要么放大字号，要么增加支撑文字 |

## 金字塔原则类

| 级别 | Pitfall | 说明 | 修复 |
|------|---------|------|------|
| P0 | **铺垫先行** | 页面视觉焦点是背景/问题，结论被挤到角落 | 最大/最醒目的元素 = 结论，不是铺垫 |
| P1 | **论据无结论** | 一页塞了 5 个数据点，没有一句话总结 | 页面顶部或最大卡放 1 句结论 |
| P1 | **结论在底部** | 核心结论放在页面最下面，决策者看不到 | 结论放顶部或视觉焦点位置 |

## 内容类

- **没有行动项就结束** → 汇报的终点是决策，不是"谢谢"。L12 必须有明确的 Next Steps
- **数据没标来源** → 决策者会质疑数据可信度。每个数据必须注明"基于XX"或"来源：XX"
- **一页多个无关论点** → 决策者每页只记住一件事。拆成两页
- **只有定性没有定量** → "效率显著提升"不如"效率提升 47%"。有数据的地方必须用数字
- **核心结论藏在第 10 页** → 决策者的注意力在开场 3 分钟最集中。核心结论必须在 Hook 页或前 3 页出现

### 视觉类

- **accent 色超过页面 10%** → 强调色太多 = 没有强调。accent 只出现在 CTA/关键数据/行动项
- **标题下划线/装饰线** → AI 生成的标志性错误。用字号对比和留白区分层级，不要画线
- **正文用 Bold** → 只有标题 Bold。正文 Bold = 全部加粗 = 没有重点
- **3 种以上字号在同一页** → 层级混乱。一页最多 3 种字号：标题/正文/备注
- **图表无图例** → 图表必须有图例和轴标签，否则决策者看不懂
- **纯文字页无视觉元素** → 每页至少一个非文字元素（图标/色块/图表/图片）

---

## Common Mistakes to Avoid (PptxGenJS)

- **Don't repeat the same layout** — vary columns, cards, and callouts across slides
- **Don't center body text** — left-align paragraphs and lists; center only titles
- **Don't skimp on size contrast** — titles need 36pt+ to stand out from 14-16pt body
- **Don't default to blue** — pick colors that reflect the specific topic
- **Don't mix spacing randomly** — choose 0.3" or 0.5" gaps and use consistently
- **Don't style one slide and leave the rest plain** — commit fully or keep it simple throughout
- **Don't create text-only slides** — add images, icons, charts, or visual elements
- **Don't forget text box padding** — when aligning lines or shapes with text edges, set `margin: 0` on the text box or offset the shape to account for padding
- **Don't use low-contrast elements** — icons AND text need strong contrast against the background
- **NEVER use accent lines under titles** — these are a hallmark of AI-generated slides; use whitespace or background color instead
- **NEVER use "#" with hex colors** — causes file corruption in PptxGenJS
- **NEVER encode opacity in hex strings** — use the `opacity` property instead
- **NEVER use async/await in createSlide()** — compile.js won't await
- **NEVER reuse option objects across PptxGenJS calls** — PptxGenJS mutates objects in-place
- **NEVER use LAYOUT_WIDE** — LAYOUT_WIDE = 13.3"×7.5"，所有 slide 坐标按 10"×5.625" 设计，用 LAYOUT_WIDE 内容只占画面 75%，挤在左上角。**必须用 LAYOUT_16x9**

---

## Critical Pitfalls — PptxGenJS

### NEVER use async/await in createSlide()

```javascript
// WRONG - compile.js won't await
async function createSlide(pres, theme) { ... }

// CORRECT
function createSlide(pres, theme) { ... }
```

### NEVER use "#" with hex colors

```javascript
color: "FF0000"      // CORRECT
color: "#FF0000"     // CORRUPTS FILE
```

### NEVER encode opacity in hex strings

```javascript
shadow: { color: "00000020" }              // CORRUPTS FILE
shadow: { color: "000000", opacity: 0.12 } // CORRECT
```

### Prevent text wrapping in titles

```javascript
// Use fit:'shrink' for long titles
slide.addText("Long Title Here", {
  x: 0.5, y: 2, w: 9, h: 1,
  fontSize: 48, fit: "shrink"
});
```

### NEVER reuse option objects across calls

```javascript
// WRONG
const shadow = { type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.15 };
slide.addShape(pres.shapes.RECTANGLE, { shadow, ... });
slide.addShape(pres.shapes.RECTANGLE, { shadow, ... });

// CORRECT - factory function
const makeShadow = () => ({ type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.15 });
slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });
slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });
```
