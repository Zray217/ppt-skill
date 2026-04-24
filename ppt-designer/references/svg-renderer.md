# SVG渲染器 (Renderer)

## 画布结构

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <!-- 背景 -->
  <rect width="1280" height="720" fill="#F8FAFC"/>
  <!-- 外框 -->
  <rect x="40" y="32" width="1200" height="656" rx="30" fill="#F8FAFC" stroke="#E2E8F0"/>
  <!-- Section标签 -->
  <text x="72" y="68" ... font-size="12" fill="#4F46E5" font-weight="700">SECTION</text>
  <!-- 页码 -->
  <text x="1180" y="68" text-anchor="end" ... font-size="12" fill="#64748B">01</text>
  <!-- 分割线 -->
  <line x1="72" y1="88" x2="1208" y2="88" stroke="#E2E8F0"/>
  <!-- 主标题 -->
  <text x="72" y="138" ... font-size="34" fill="#0F172A" font-weight="800">标题</text>
  <!-- 副标题 -->
  <text x="72" y="170" ... font-size="18" fill="#64748B">副标题</text>
  <!-- 内容区 (从y=210开始) -->
  ...
</svg>
```

## 字体系统

| 用途 | font-family | font-size | font-weight |
|------|------------|-----------|-------------|
| Section标签 | 'PingFang SC','Microsoft YaHei',sans-serif | 12 | 700 |
| 主标题 | 同上 | 34 | 800 |
| 副标题 | 同上 | 18 | 500 |
| Card标题(main) | 同上 | 20 | 700 |
| Card标题(body) | 同上 | 17 | 700 |
| Card正文 | 同上 | 13(main)/12(body) | 500 |
| Tag标签 | 同上 | 10 | 700 |
| Highlight数字 | 同上 | 28 | 800 |
| Highlight标签 | 同上 | 12 | 500 |
| Thin条带文字 | 同上 | 18 | 700 |
| 子卡标题 | 同上 | 14 | 700 |
| 子卡正文 | 同上 | 12 | 500 |

## 主题配色 (Light)

```python
theme = {
    'bg':      '#F8FAFC',   # 页面背景
    'frame':   '#E2E8F0',   # 外框边线
    'card':    '#FFFFFF',   # 卡片背景
    'line':    '#CBD5E1',   # 分割线
    'title':   '#0F172A',   # 标题文字
    'sub':     '#64748B',   # 副标题
    'body':    '#334155',   # 正文
    'pill':    '#EEF2FF',   # Tag背景
    'accent':  '#4F46E5',   # 强调色
}
```

## 暗色主题 (Dark)

```python
theme_dark = {
    'bg':      '#0F172A',
    'frame':   '#1E293B',
    'card':    '#1E293B',
    'line':    '#334155',
    'title':   '#F1F5F9',
    'sub':     '#94A3B8',
    'body':    '#CBD5E1',
    'pill':    '#312E81',
    'accent':   '#818CF8',
}
```

## 卡片渲染

### 主卡片 (main, L1)
```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="#FFFFFF" stroke="#A5B4FC"/>
<!-- Tag -->
<rect x="{x+16}" y="{y+14}" width="80" height="24" rx="12" fill="#EEF2FF" stroke="#E2E8F0"/>
<text x="{x+30}" y="{y+30}" font-size="10" fill="#4F46E5" font-weight="700">TAG</text>
<!-- 标题 -->
<text x="{x+16}" y="{y+54}" font-size="20" fill="#0F172A" font-weight="700">标题</text>
<!-- Bullets -->
<text x="{x+16}" y="{y+84}" font-size="13" fill="#334155" font-weight="500">• 内容</text>
```

### 普通卡片 (body, L2)
```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="#FFFFFF" stroke="#CBD5E1"/>
<!-- Tag -->
<rect x="{x+16}" y="{y+14}" width="80" height="24" rx="12" fill="#EEF2FF"/>
<text x="{x+30}" y="{y+30}" font-size="10" fill="#4F46E5" font-weight="700">TAG</text>
<!-- 标题 -->
<text x="{x+16}" y="{y+54}" font-size="17" fill="#0F172A" font-weight="700">标题</text>
<!-- Bullets -->
<text x="{x+16}" y="{y+84}" font-size="12" fill="#334155" font-weight="500">• 内容</text>
```

### 高亮卡片 (highlight, L2)
```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="#FFFFFF" stroke="#CBD5E1"/>
<!-- Tag -->
<rect x="{x+16}" y="{y+14}" width="80" height="24" rx="12" fill="#EEF2FF"/>
<text x="{x+30}" y="{y+30}" font-size="10" fill="#4F46E5" font-weight="700">TAG</text>
<!-- 大数字 -->
<text x="{x+16}" y="{y+62}" font-size="28" fill="#0F172A" font-weight="800">175+</text>
<!-- 标签 -->
<text x="{x+16}" y="{y+100}" font-size="12" fill="#334155" font-weight="500">覆盖国家</text>
<!-- 说明 -->
<text x="{x+16}" y="{y+118}" font-size="10" fill="#64748B">短比例小卡</text>
```

### 条带卡片 (thin, L2)
```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="#FFFFFF" stroke="#CBD5E1"/>
<rect x="{x+16}" y="{y+14}" width="80" height="24" rx="12" fill="#EEF2FF"/>
<text x="{x+30}" y="{y+30}" font-size="10" fill="#4F46E5" font-weight="700">TAG</text>
<text x="{x+16}" y="{y+56}" font-size="18" fill="#0F172A" font-weight="700">一句话主张</text>
```

### 嵌套组 (group_title_body / group3_equal)
```xml
<!-- 父卡片 -->
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="#FFFFFF" stroke="#CBD5E1"/>
<!-- 子卡片（父卡内14px边距） -->
<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="16" fill="#FFFFFF" stroke="#E2E8F0"/>
<!-- child_title: 14px, 700 weight -->
<!-- child_body: 12px, 500 weight -->
```

子卡位置计算（父卡内坐标系）：
```
parent_inner_x = x + 14
parent_inner_y = y + 14
parent_inner_w = w - 28
parent_inner_h = h - 28

child_w = (parent_inner_w - gap*(pcs-1)) / pcs   # pcs=父卡跨列
child_h = (parent_inner_h - gap*(prs-1)) / prs   # prs=父卡跨行

child_x = parent_inner_x + cc * (child_w + gap)
child_y = parent_inner_y + rr * (child_h + gap)
```

## 文字自动换行

```python
def wrap_text(text, width_px, font_pt):
    chars_per_line = max(6, int(width_px / (font_pt * 1.18)))
    return textwrap.wrap(text, width=chars_per_line)
```

用 `<tspan>` 实现换行：
```xml
<text x="72" y="138" ...>
  <tspan x="72" dy="0">第一行</tspan>
  <tspan x="72" dy="42">第二行</tspan>
</text>
```

## 页面类型映射

| PPT大纲type | 推荐骨架 | 说明 |
|------------|---------|------|
| data_table | nested_title_body | 表格+侧边数字 |
| timeline | top_main_bar | 时间线+收束条 |
| comparison | dual_main_metrics | 双方案对比 |
| cards | main_with_group3_equal | 模块并列 |
| flow | nested_title_body | 流程+说明 |
| quote | rules_rhythm | 金句+补充 |
| big_number | dual_main_metrics | 大数字对比 |
