---
name: PPT Designer
description: >
  专业PPT制作技能：基于16×9 Bento Grid编排系统，从主题到成品的全流程演示文稿设计。
  采用"结构先行→编排引擎→SVG渲染→PPTX导出"四阶段工作流。
  内置5种节奏骨架、10种页面模板、5套配色、审计评分系统。
  适用：用户要求制作PPT、演示文稿、幻灯片、演讲稿、汇报材料。
  支持中文/英文双语，SVG→PPTX可编辑转换。
---

## When to Use

用户要求制作PPT、演示文稿、幻灯片、汇报、演讲稿时使用。
也适用于：要求设计PPT结构/大纲、将文档/报告转为PPT。

## Core Workflow: 四阶段制片

### 阶段一：结构设计

参照 `references/ppt-structure-architect.md`，用金字塔原理设计PPT逻辑大纲。

1. **理解需求**：主题、受众、页数（默认10-16页）、风格
2. **背景调研**：`mimo_web_search` 搜索最新信息
3. **输出大纲**：JSON格式，`[PPT_OUTLINE]...[/PPT_OUTLINE]` 包裹

### 阶段二：编排引擎

参照 `references/bento-orchestrator.md`，将大纲内容编排为精确的网格布局。

**核心：16列×9行网格系统**
- 画布：1280×720，内容区从 y=210 开始
- 网格间距：12px（sibling/inner）、18px（group）、24px（section）
- 卡片用 `slot` 分型：`main`(L1) / `body`(L2) / `highlight`(L2) / `thin`(L2) / `group_*`(嵌套)

**5种节奏骨架（Rhythm Skeleton）：**

| 骨架 | 节奏 | 适用 |
|------|------|------|
| `nested_title_body` | hero+nested-title-body+closure | 信息密集页、方法论 |
| `top_main_bar` | hero+support+bottom-bar | 主叙事+收束条 |
| `dual_main_metrics` | compare+metric-contrast | 对比页、AB方案 |
| `main_with_group3_equal` | hero+equal-triple-group | 模块并列、三要素 |
| `rules_rhythm` | small+hero+two-column-close | 规则、要点、对比 |

**编排流程：**
1. 内容分型（narrative vs highlight）
2. 选择骨架（基于内容特征）
3. 卡片分配（主叙事→main，补充→body，数据→highlight）
4. 文案规整（main标题≤18字，body标题≤15字，bullets≤3条）
5. 审计评分（top_focus/contrast_budget/size_variety/nested_pattern）

### 阶段三：SVG渲染

参照 `references/svg-renderer.md`，将编排结果渲染为SVG。

**画布规范：**
- viewBox: `0 0 1280 720`
- 外框：x=40, y=32, w=1200, h=656, rx=30
- 标题区：y=88分割线 → y=138主标题 → y=170副标题
- 内容区：left=72, top=210, w=1136, h=414

**字体三权分立：**
- 标题：`'PingFang SC','Microsoft YaHei',serif` — 视觉重音
- 正文：`'PingFang SC','Microsoft YaHei',sans-serif` — 信息密度
- 元数据：`'SF Mono','Consolas',monospace` — 装饰节奏

**渲染规则：**
1. 卡片圆角 rx=22（主卡片）/ rx=16（子卡片）
2. Tag标签：80×24, rx=12, 左上角定位
3. Highlight卡片：大数字28px + 标签12px + 说明10px
4. Thin条带：单行文字18px，16列横跨
5. 嵌套组：父卡内14px边距，子卡间12px间距

### 阶段四：PPTX导出

使用 `scripts/svg_to_pptx.sh` 将SVG页面嵌入PPTX。

## 快速模式

用户直接给主题时：
1. 3秒简化大纲
2. 用编排引擎直接生成
3. 每页渲染后立即展示

## QA Checklist

交付前必须通过审计：
- [ ] top_focus_ok：至少1个主叙事区在上方
- [ ] contrast_budget_ok：同页高亮卡≤2个
- [ ] size_variety_ok：同页尺寸类型≤5种
- [ ] nested_pattern_ok：父子卡嵌套正确
- [ ] 每页SVG viewBox = 0 0 1280 720
- [ ] 卡片间距 ≥ 12px
- [ ] 文字无溢出
