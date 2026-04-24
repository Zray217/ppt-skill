---
name: bento-ppt-generator
description: 将主题、文档、研究摘要或现有大纲编排为结构化 PPT：先输出金字塔式 outline JSON，再生成 slide_plan，并按 Bento rhythm 规则准备 SVG/PPT-ready 页面规格。适用于“生成 PPT”“做汇报 deck”“把长文改成幻灯片”“Bento Grid 演示文稿”“可编辑 PPT 结构设计”等场景。
---

# Bento PPT Generator

## 这个 Skill 做什么

这个 skill 解决的不是“随便做几页幻灯片”，而是把一份主题、文档或研究材料整理成一套可以继续落地的 PPT 结构系统：

1. 先把内容整理成金字塔式大纲。
2. 再把大纲拆成页型化的 `slide_plan.json`。
3. 对适合模块化编排的页面，交给 Bento 引擎生成稳定的 SVG 页面。
4. 对封面、目录、章节页、结束页这类更偏定制构图的页面，输出 SVG 渲染提示词或继续接到可编辑 PPT 流程。

它更像一个“PPT 编排总控 skill”，而不是单一的图片生成器。

## 何时使用

适合：

- 用户要从主题、文档、PDF、旧 PPT、研究摘要生成一份新的演示文稿。
- 用户要先做 PPT 大纲，再做页级编排。
- 用户要把长文改成结构清晰的 slide deck。
- 用户想做 Bento Grid / 卡片式 / 模块化的信息页。
- 用户最终想得到 SVG 页面草稿，或继续落成可编辑 `.pptx`。

不适合：

- 用户只想润色已有某一页里的个别文字。
- 用户只要一个纯海报式单页图像。
- 用户要复杂动画、视频转场、互动式网页演示，那是另一条流水线。

## 输入约定

优先读取用户已有材料，按可信度从高到低排序：

1. 用户提供的现成大纲、旧 PPT、PRD、文档。
2. 用户提供的背景调研或最新事实。
3. 用户提供的硬约束：受众、场景、时长、必须包含或不能出现的内容。
4. 仅当上面都缺失时，再基于主题合理假设。

如果用户要求当前事实、市场情况、政策、产品信息或最新案例，先核实再写大纲，不要凭空补全。

## 默认输出顺序

除非用户明确跳过，否则默认按下面的顺序工作：

### Step 1. 对齐任务边界

先确认四件事：

- 演讲主题或核心问题是什么。
- 受众是谁，场景是什么。
- 目标页数或时长大概是多少。
- 最终要什么交付：只要大纲、要 `slide_plan`、要 SVG、还是要 `.pptx`。

如果用户没有说清楚，不要问一长串问题。只在“受众 / 时长 / 输出物”明显会改变结构时追问，否则做合理假设并在结果里说明。

### Step 2. 生成大纲

读取 [references/outline_architect.md](references/outline_architect.md)。

目标是输出一个符合金字塔原理的 `PPT_OUTLINE` JSON，至少包含：

- `cover`
- `table_of_contents`
- `parts`
- `end_page`

如果用户已经给了成熟大纲，不必重做，只需标准化成该 JSON 结构。

### Step 3. 生成 slide plan

读取 [references/page_system.md](references/page_system.md)。

把大纲转成 `slide_plan.json`。每一页都要明确：

- `page_role`
- `render_mode`
- 标题与副标题
- 内容卡片或页面要点
- 是否适合 Bento 引擎

注意：不是所有页面都应交给同一个引擎。封面、目录、章节页、结尾页通常更适合 `custom_svg`；信息页、对比页、规则页、模块页通常更适合 `engine`。

### Step 4. 选择渲染路径

分三种：

- `outline_only`
  - 只交付 `PPT_OUTLINE` 或 `slide_plan.json`
- `svg_draft`
  - 对 `render_mode=engine` 的页面，使用 `assets/build_bento_svgs.py`
  - 对 `render_mode=custom_svg` 的页面，读取 [references/svg_renderer.md](references/svg_renderer.md) 生成页面级 SVG 提示词
- `editable_pptx`
  - 先完成大纲和 `slide_plan`
  - 再把结构稳定的内容交给 PowerPoint 流程实现
  - 如果当前没有可靠的 PPT 写入路径，先交付结构化计划和 SVG 草稿，不要假装已经生成了高质量 `.pptx`

### Step 5. 质量自检

读取 [references/checklist.md](references/checklist.md)。

至少检查：

- 结构是否一页一意。
- 事实是否来自用户材料或已核实来源。
- 页型节奏是否合理。
- 引擎页是否满足字数和卡片密度约束。
- 若已生成 SVG，是否满足 `1280x720` 和审计规则。

## 资源文件怎么用

### 核心文档

- [references/outline_architect.md](references/outline_architect.md)
  - 负责“大纲怎么生”
- [references/page_system.md](references/page_system.md)
  - 负责“页面怎么拆”
- [references/svg_renderer.md](references/svg_renderer.md)
  - 负责“自定义 SVG 页怎么写”
- [references/checklist.md](references/checklist.md)
  - 负责“最后怎么验”

### 可执行资产

- [assets/bento_engine_v361_rhythm.py](assets/bento_engine_v361_rhythm.py)
  - 稳定的 Bento 内容页编排引擎
- [assets/build_bento_svgs.py](assets/build_bento_svgs.py)
  - 把 `slide_plan.json` 中的 `engine` 页面批量导出为 `compiled.json`、`audit.json` 和 SVG
- [assets/example_outline.json](assets/example_outline.json)
  - 大纲结构示例
- [assets/example_slide_plan.json](assets/example_slide_plan.json)
  - 页级计划示例

## 推荐工作方式

### 用户只给主题时

1. 先按 `outline_architect` 生成大纲。
2. 再按 `page_system` 生成页级计划。
3. 让用户确认结构方向。
4. 方向确认后再生成 SVG 或 `.pptx`。

### 用户给了长文、PDF、旧 PPT 时

1. 先抽取核心论点、证据、章节边界。
2. 压缩成 8-15 页的结构化 deck，而不是机械逐段拷贝。
3. 把事实和数据优先放进“证据页、对比页、指标页”。

### 用户明确要可编辑 PPT 时

1. 仍然先做 `slide_plan.json`。
2. 明确哪些页走 `engine`，哪些页走 `custom_svg`。
3. 输出 `.pptx` 时，优先保证文字、图表、结构可编辑，不要只塞截图。

## 强约束

- 不要伪造统计数据、日期、政策、公司信息。
- 不要把所有页面都做成同一种页型。
- 不要把段落整块粘进窄卡片。
- 不要为了“看起来饱满”而塞满每个卡片。
- 不要在没有确认结构前直接承诺“成品 PPT 已经定稿”。

## 首版能力边界

这个 skill 的首版已经能稳定完成：

- 主题到大纲
- 大纲到 `slide_plan`
- `engine` 页面到 SVG
- 结构化质量检查

它还没有内置完整的 `.pptx` 写入模板系统，所以当用户直接要“最终 PPT 文件”时，应先把结构层打稳，再接 PowerPoint 实体化流程。
