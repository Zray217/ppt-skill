# 页型系统与 Bento 编排规则

这份参考把“大纲”进一步转成可渲染的 `slide_plan.json`。

## 什么时候读这个文件

- 你已经有了 `PPT_OUTLINE`。
- 你要把每一页定义成具体页型。
- 你要判断哪些页适合走 Bento 引擎。

## 核心原则

不是所有页面都适合同一个渲染器。

### 优先走 `custom_svg` 的页面

- `cover`
- `toc`
- `chapter`
- `quote`
- `closing`

这些页面更依赖独立构图和大标题气质。

### 优先走 `engine` 的页面

- `thesis`
- `rule`
- `module`
- `comparison`
- `metric`
- `process`
- `case`
- `summary`

这些页面更适合模块化卡片编排。

## 标准 slide_plan 结构

顶层建议结构：

```json
{
  "deck_title": "标题",
  "language": "zh-CN",
  "slides": [
    {
      "slide_number": 1,
      "page_role": "cover",
      "render_mode": "custom_svg",
      "section": "封面",
      "title": "主标题",
      "subtitle": "副标题",
      "content": ["一句定位", "一个亮点"]
    },
    {
      "slide_number": 3,
      "page_role": "thesis",
      "render_mode": "engine",
      "section": "Part 01",
      "title": "页面标题",
      "subtitle": "一句摘要",
      "layout": "nested_title_body",
      "cards": [
        {
          "title": "主卡标题",
          "tag": "MAIN",
          "bullets": ["要点一", "要点二"]
        }
      ]
    }
  ]
}
```

## 页型清单

### `cover`

- 用于封面
- 通常 `render_mode=custom_svg`
- 强调主标题、副标题、主题气质、一个主视觉钩子

### `toc`

- 用于目录
- 通常 `render_mode=custom_svg`
- 目录只列章节，不列全部页面

### `chapter`

- 用于章节开场
- 通常 `render_mode=custom_svg`
- 负责切节奏，不负责承载大量信息

### `thesis`

- 用于单一核心命题页
- 通常 `render_mode=engine`
- 适合主卡 + 辅助卡

### `module`

- 用于 3 模块或 4 模块说明
- 常走 `main_with_group3_equal` 或 `nested_title_body`

### `comparison`

- 用于 A/B、前后对比、路径对比
- 常走 `dual_main_metrics`

### `metric`

- 用于数据指标、比例、结论性数字
- 常走 `dual_main_metrics` 或 `top_main_bar`

### `process`

- 用于流程、步骤、阶段拆解
- 常走 `main_with_group3_equal` 或 `top_main_bar`

### `rule`

- 用于规则、原则、方法论
- 常走 `rules_rhythm`

### `case`

- 用于案例、证据、场景落地
- 常走 `nested_title_body`

### `summary`

- 用于阶段小结或结论页
- 可走 `top_main_bar` 或 `rules_rhythm`

### `closing`

- 用于最终结尾页
- 通常 `render_mode=custom_svg`

## Deck 节奏模板

### 6 页

1. `cover`
2. `thesis`
3. `module`
4. `metric`
5. `summary`
6. `closing`

### 10 页

1. `cover`
2. `toc`
3. `chapter`
4. `thesis`
5. `comparison`
6. `chapter`
7. `process`
8. `case`
9. `summary`
10. `closing`

### 14 页

1. `cover`
2. `toc`
3. `chapter`
4. `metric`
5. `process`
6. `chapter`
7. `module`
8. `comparison`
9. `chapter`
10. `metric`
11. `case`
12. `chapter`
13. `summary`
14. `closing`

## Bento 引擎支持的 layout

引擎资产见 [../assets/bento_engine_v361_rhythm.py](../assets/bento_engine_v361_rhythm.py)。

### `nested_title_body`

适合：

- 一个主命题
- 一个上方父卡
- 底部 3 个补充卡

典型用途：

- 方法论页
- 案例拆解页
- 主张 + 解释 + 风险 + 动作

### `top_main_bar`

适合：

- 上方主叙事
- 右侧说明
- 下方条带式收束

典型用途：

- 结论页
- 一句话主张页
- 总结页

### `dual_main_metrics`

适合：

- 两个方案或两个对象对比
- 再加 1-2 个关键指标

典型用途：

- Before / After
- 方案 A / 方案 B
- 现状 / 目标

### `main_with_group3_equal`

适合：

- 一个主区
- 三模块并列

典型用途：

- 三大能力
- 三阶段
- 三个应用场景

### `rules_rhythm`

适合：

- 规则、原则、编排说明
- 左小右大或上下收束结构

## 卡片字段约束

### 通用

- `title` 只写短标题
- `tag` 用短标签，如 `MAIN`、`RULE`、`CASE`
- `bullets` 默认 1-3 条

### 长度建议

- 主卡标题：不超过 18 个中文字符
- 正文卡标题：不超过 15 个中文字符
- 窄卡 bullet：最好不超过 22 个中文字符
- 主卡 bullet：最好不超过 30 个中文字符
- `metric`：最好不超过 8 个字符

### 结构建议

- 窄卡不放长段落
- 扁卡只放一句话
- 指标卡只保留数字、标签和一个短注释

## 布局选择建议

可以显式指定 `layout`，也可以让引擎自动选择。自动选择逻辑大致是：

- 有 2 个以上指标卡，倾向 `dual_main_metrics`
- 卡片数较多，倾向 `nested_title_body`
- 否则倾向 `rules_rhythm`

如果你知道页面意图，优先手动指定 `layout`，结果更稳。

## render_mode 选择规则

### 用 `engine`

当页面可以抽象为：

- 一个主区 + 若干辅区
- 规则/原则/模块说明
- 对比、指标、方法、案例

### 用 `custom_svg`

当页面更像：

- 大标题主视觉
- 目录
- 章节过渡
- 结束页
- 强视觉金句页

## 推荐输出文件

- `deck_outline.json`
- `slide_plan.json`
- `slides/slideNN.svg`
- `compiled.json`
- `audit.json`
- `manifest.json`

如果用 bundled wrapper：

```bash
python assets/build_bento_svgs.py assets/example_slide_plan.json -o out/demo
```
