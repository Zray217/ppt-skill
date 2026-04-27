# 布局骨架参考

## 页面类型总览

### Hero 页（留白型，制造呼吸感）

Hero 页的核心是**留白和视觉冲击力**，不是信息密度。一页只传达一个核心印象。

| 类型 | 视觉特征 | 字体分工 | 适用内容 |
|------|---------|---------|---------|
| 开场封面 | 渐变背景 + 超大标题 | 标题:衬线 副标:等宽 | 全局封面 |
| 章节幕封 | 等宽章节号 + 大标题 + 大量留白 | 章节号:等宽 标题:衬线 | 章节分隔 |
| 数据大字报 | 超大数字 + 简短标签 | 数字:等宽 标签:衬线 | 核心指标展示 |
| 悬念问题 | 居中大问句 + 极简装饰 | 问句:衬线 装饰:等宽 | 抛出关键问题 |
| 大引用 | 超大引号 + 引文 + 出处 | 引文:衬线 出处:等宽 | 金句/名人名言 |

### Non-hero 页（Bento 网格型，承载信息密度）

详见下方5种布局骨架。

---

## Hero 页规范

### 开场封面

```
布局区域：全屏 1280×720
┌──────────────────────────────────────┐
│                                      │
│           渐变背景（从主题渐变起→止）    │
│                                      │
│        超大标题 (48-56px, 衬线)        │
│        副标题 (16px, 等宽, opacity 0.7) │
│                                      │
│           日期/场合 (12px, 等宽)        │
│                                      │
└──────────────────────────────────────┘

元素清单：
- 背景 rect: 全屏, fill=渐变 或 主题背景深色
- 标题 text: font-family=衬线, font-size=48-56, font-weight=700
- 副标题 text: font-family=等宽, font-size=16, opacity=0.7
- 日期/场合 text: font-family=等宽, font-size=12, y=680 (近底部)
- 装饰 line: 水平分隔线, stroke=主色, opacity=0.3
```

### 章节幕封

```
布局区域：全屏 1280×720
┌──────────────────────────────────────┐
│                                      │
│   01 /                               │  ← 等宽, 14px, 主色, 左上
│                                      │
│                                      │
│        章节标题 (40-48px, 衬线)        │  ← 垂直居中
│                                      │
│                                      │
└──────────────────────────────────────┘

元素清单：
- 背景 rect: 全屏, fill=背景深/浅
- 章节号 text: font-family=等宽, font-size=14, fill=主色, x=72, y=200
- 标题 text: font-family=衬线, font-size=40-48, font-weight=700, 居中
- 装饰 line: 短横线, stroke=主色, 标题下方
```

### 数据大字报

```
布局区域：全屏 1280×720
┌──────────────────────────────────────┐
│                                      │
│                                      │
│           97%                        │  ← 等宽, 80-120px, 主色
│        客户满意度                      │  ← 衬线, 20px
│        基于2024年Q4调研数据             │  ← 等宽, 12px, opacity 0.5
│                                      │
│                                      │
└──────────────────────────────────────┘

元素清单：
- 背景 rect: 全屏, fill=背景色
- 数字 text: font-family=等宽, font-size=80-120, fill=主色
- 标签 text: font-family=衬线, font-size=20
- 注释 text: font-family=等宽, font-size=12, opacity=0.5
```

### 悬念问题

```
布局区域：全屏 1280×720
┌──────────────────────────────────────┐
│                                      │
│                                      │
│    AI 会取代你的工作吗？                │  ← 衬线, 36-44px
│                                      │
│           ──                          │  ← 主色短横线装饰
│                                      │
│                                      │
└──────────────────────────────────────┘

元素清单：
- 背景 rect: 全屏, fill=背景色
- 问句 text: font-family=衬线, font-size=36-44, font-weight=700
- 装饰 line: 短横线, stroke=主色, opacity=0.6
```

### 大引用

```
布局区域：全屏 1280×720
┌──────────────────────────────────────┐
│                                      │
│   "                                  │  ← 衬线, 72px, 主色, opacity 0.3
│     最好的预测未来的方式                │  ← 衬线, 24-28px
│     就是创造未来。                     │
│                                      │
│              ── Alan Kay              │  ← 等宽, 14px, opacity 0.6
│                                      │
└──────────────────────────────────────┘

元素清单：
- 背景 rect: 全屏, fill=背景色
- 大引号 text: font-family=衬线, font-size=72, fill=主色, opacity=0.3
- 引文 text: font-family=衬线, font-size=24-28
- 出处 text: font-family=等宽, font-size=14, opacity=0.6
```

---

## Non-hero 页规范（Bento 网格）

### 网格系统
- 画布: 1280×720
- 内容区: left=72, top=60, w=1136, h=600
- 网格: 16列 × 9行
- gap: 12px
- 列宽: (1136 - 12*15) / 16 ≈ 59.75px
- 行高: (600 - 12*8) / 9 ≈ 56px

### 间距 Token
- inner (父子卡内): 12px
- sibling (同组卡): 12px
- group (跨组卡): 18px
- section (跨区): 24px
- 卡片内边距: 16px (left), 14px (top)
- 子卡内边距: 14px

### 字号规范
- 页面标题: 34px, weight 800, 衬线
- 页面副标题: 16px, weight 500, 等宽
- 卡片标签 (pill): 10px, weight 700, 等宽
- 主卡标题 (main): 20px, weight 700, 非衬线
- 主卡正文 (main): 13px, weight 500, 非衬线
- 普通卡标题 (body): 17px, weight 700, 非衬线
- 普通卡正文 (body): 12px, weight 500, 非衬线
- 高亮数字 (highlight): 28px(大卡)/24px(小卡), weight 800, 等宽
- 高亮标签: 12px, weight 500, 非衬线
- 条带卡 (thin): 18px, weight 700, 非衬线
- 子卡标题: 14px, weight 700, 非衬线
- 子卡正文: 12px, weight 500, 非衬线
- 页码/元数据: 11px, weight 400, 等宽

### 每行字符数估算 (CPL)
cpl = max(6, int(width_px / (font_pt * 1.18)))
- 1.18 是中文字符的平均宽高比

### 内容截断规则 (按 slot 类型)
| slot | title 上限 | bullets 上限 | 每条 bullet 上限 |
|------|-----------|-------------|-----------------|
| main | 18字 | 3条 | 30字 |
| body | 15字 | 3条 | 22字 |
| highlight | metric: 8字 | label: 12字 | sub: 12字 |
| thin | single: 30字 | — | — |
| child_title | single: 18字 | — | — |
| child_body | single: 38字 | — | — |

---

## 布局骨架 (5种 Non-hero)

### nested_title_body
rhythm: hero+nested-title-body+closure
- main: c0 r0 cs8 rs5 (level 1)
- group_title_body: c8 r0 cs8 rs5 (level 2) → child_title(0,0,8,1) + child_body(0,1,8,4)
- body: c0 r5 cs6 rs4 (level 2)
- body: c6 r5 cs5 rs4 (level 3)
- body: c11 r5 cs5 rs4 (level 3, closure)

### top_main_bar
rhythm: hero+support+bottom-bar
- main: c0 r0 cs10 rs5 (level 1)
- body: c10 r0 cs6 rs5 (level 2)
- body: c0 r5 cs8 rs2 (level 3)
- body: c8 r5 cs8 rs2 (level 3)
- thin: c0 r7 cs16 rs2 (level 2, closure)

### dual_main_metrics
rhythm: compare+metric-contrast
- main: c0 r0 cs8 rs5 (level 1)
- main: c8 r0 cs8 rs5 (level 1)
- body: c0 r5 cs8 rs4 (level 2)
- highlight: c8 r5 cs4 rs4 (level 2)
- highlight: c12 r5 cs4 rs4 (level 2, closure)

### main_with_group3_equal
rhythm: hero+equal-triple-group
- main: c0 r0 cs10 rs5 (level 1)
- group3_equal: c10 r0 cs6 rs5 (level 2) → 3× child_body(0,0-3,6,1-2)
- body: c0 r5 cs5 rs4 (level 2)
- body: c5 r5 cs5 rs4 (level 3)
- body: c10 r5 cs6 rs4 (level 3, closure)

### rules_rhythm
rhythm: small+hero+two-column-close
- body: c0 r0 cs5 rs4 (level 2)
- main: c5 r0 cs11 rs4 (level 1)
- body: c0 r4 cs8 rs5 (level 2)
- body: c8 r4 cs8 rs5 (level 3, closure)

---

## 元数据排版规范

每页四角放置元数据（等宽字体，11px，opacity 0.4）：
- 左上：章节号（如 `02 / 运营飞轮`）
- 右上：主题标签（如 `OPERATION`）
- 左下：页码（如 `5 / 10`）
- 右下：留空或品牌标识

元数据不参与内容区网格计算，固定在画布边缘（margin 24-36px）。
