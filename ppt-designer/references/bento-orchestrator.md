# Bento Grid 编排器 (Orchestrator)

## 网格系统

### 坐标系
- 画布：1280×720
- 外框：x=40, y=32, w=1200, h=656, rx=30
- 内容区：left=72, top=210, w=1136, h=414
- 网格：16列×9行
- 间距：gap=12px（计算列宽/行高时扣除）

### 列宽行高计算
```
col_w = (1136 - 12×15) / 16 = 59.5px
row_h = (414 - 12×8) / 9 = 35.3px
```

### 卡片定位
卡片位置用 (c, r, cs, rs) 表示：起始列、起始行、跨列数、跨行数
```
x = 72 + c × (col_w + 12)
y = 210 + r × (row_h + 12)
w = col_w × cs + 12 × (cs - 1)
h = row_h × rs + 12 × (rs - 1)
```

## 卡片分型 (Slot Types)

| Slot | 层级 | 用途 | 文案限制 |
|------|------|------|---------|
| `main` | L1 | 主叙事区 | 标题≤18字, bullets≤3条, 每条≤30字 |
| `body` | L2 | 补充说明 | 标题≤15字, bullets≤3条, 每条≤22字 |
| `highlight` | L2 | 大数字卡 | metric≤8字, label≤12字, sub≤12字 |
| `thin` | L2 | 底部条带 | 单行≤30字 |
| `group_title_body` | L2 | 嵌套组(标题+正文) | 子卡标题≤18字, 正文≤38字 |
| `group3_equal` | L2 | 嵌套组(三等分) | 每子卡≤18字 |
| `child_title` | L3 | 子卡-标题 | ≤18字 |
| `child_body` | L3 | 子卡-正文 | ≤38字 |

## 5种节奏骨架

### A. nested_title_body
节奏：hero+nested-title-body+closure
适用：信息密集页、方法论页
```
blocks:
  - slot: main,       c:0,  r:0, cs:8,  rs:5, level:1
  - slot: group_title_body, c:8,  r:0, cs:8,  rs:5, level:2
    children:
      - [child_title, 0, 0, 8, 1]
      - [child_body,  0, 1, 8, 4]
  - slot: body,       c:0,  r:5, cs:6,  rs:4, level:2
  - slot: body,       c:6,  r:5, cs:5,  rs:4, level:3
  - slot: body,       c:11, r:5, cs:5,  rs:4, level:3, closure:true
```

### B. top_main_bar
节奏：hero+support+bottom-bar
适用：主叙事+收束
```
blocks:
  - slot: main,  c:0,  r:0, cs:10, rs:5, level:1
  - slot: body,  c:10, r:0, cs:6,  rs:5, level:2
  - slot: body,  c:0,  r:5, cs:8,  rs:2, level:3
  - slot: body,  c:8,  r:5, cs:8,  rs:2, level:3
  - slot: thin,  c:0,  r:7, cs:16, rs:2, level:2, closure:true
```

### C. dual_main_metrics
节奏：compare+metric-contrast
适用：对比页、AB方案
```
blocks:
  - slot: main,      c:0, r:0, cs:8, rs:5, level:1
  - slot: main,      c:8, r:0, cs:8, rs:5, level:1
  - slot: body,      c:0, r:5, cs:8, rs:4, level:2
  - slot: highlight, c:8, r:5, cs:4, rs:4, level:2
  - slot: highlight, c:12,r:5, cs:4, rs:4, level:2, closure:true
```

### D. main_with_group3_equal
节奏：hero+equal-triple-group
适用：模块并列、三要素
```
blocks:
  - slot: main, c:0,  r:0, cs:10, rs:5, level:1
  - slot: group3_equal, c:10, r:0, cs:6, rs:5, level:2
    children:
      - [child_body, 0, 0, 6, 1]
      - [child_body, 0, 1, 6, 2]
      - [child_body, 0, 3, 6, 2]
  - slot: body, c:0,  r:5, cs:5,  rs:4, level:2
  - slot: body, c:5,  r:5, cs:5,  rs:4, level:3
  - slot: body, c:10, r:5, cs:6,  rs:4, level:3, closure:true
```

### E. rules_rhythm
节奏：small+hero+two-column-close
适用：规则、要点
```
blocks:
  - slot: body, c:0, r:0, cs:5,  rs:4, level:2
  - slot: main, c:5, r:0, cs:11, rs:4, level:1
  - slot: body, c:0, r:4, cs:8,  rs:5, level:2
  - slot: body, c:8, r:4, cs:8,  rs:5, level:3, closure:true
```

## 骨架选择逻辑

```python
def choose_layout(cards):
    metrics = count(cards, kind='highlight')
    if metrics >= 2:
        return 'dual_main_metrics'
    if len(cards) >= 5:
        return 'nested_title_body'
    if has_triple_modules(cards):
        return 'main_with_group3_equal'
    return 'rules_rhythm'
```

## 间距系统 (Spacing Tokens)

| 场景 | 间距 |
|------|------|
| 父子卡内部 | 14px padding |
| 同组子卡间 | 12px |
| 跨组卡片间 | 18px |
| 跨区块间 | 24px |
| 卡片内边距 | 16px (left), 14px (top) |

## 审计评分

每页生成后自动检查：
- **top_focus_ok**：至少1个main块在 r≤1 行
- **contrast_budget_ok**：同页highlight卡≤2个
- **size_variety_ok**：同页尺寸类型(cs×rs组合)≤5种
- **nested_pattern_ok**：父子卡嵌套结构正确

## 权重计算
```python
weight = cs × rs  # 基础权重
if slot == 'main': weight += 20      # 主叙事加权
if slot == 'highlight': weight += 8  # 高亮加权
```

## 文案规整函数

```python
def normalize(card, slot):
    if slot == 'main':
        card.title = card.title[:18]
        card.bullets = [b[:30]+'…' if len(b)>30 else b for b in card.bullets[:3]]
    elif slot == 'body':
        card.title = card.title[:15]
        card.bullets = [b[:22]+'…' if len(b)>22 else b for b in card.bullets[:3]]
    elif slot == 'highlight':
        card.metric = str(card.metric)[:8]
        card.label = card.title[:12]
        card.sub = (card.bullets[0] if card.bullets else '')[:12]
    elif slot == 'thin':
        card.single = (card.title or card.bullets[0])[:30]
    elif slot == 'child_title':
        card.single = (card.title or card.bullets[0])[:18]
    elif slot == 'child_body':
        card.single = ' '.join(card.bullets[:2])[:38]
    return card
```
