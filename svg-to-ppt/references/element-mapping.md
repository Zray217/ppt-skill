# SVG → PPTX 元素映射手册

## 基础形状

### rect → 矩形
```
SVG:  <rect x="100" y="100" width="300" height="200" rx="12" fill="#334155" />
PPTX: add_shape(ROUNDED_RECTANGLE, x, y, w, h) + solidFill
```
- `x, y, width, height` → 位置和尺寸（乘以缩放系数）
- `rx, ry` → 圆角（PPTX ROUNDED_RECTANGLE 自带默认圆角）
- `fill` → 填充色
- `stroke` → 描边

### circle → 椭圆
```
SVG:  <circle cx="640" cy="360" r="50" fill="#3B82F6" />
PPTX: add_shape(OVAL, cx-r, cy-r, 2*r, 2*r) + solidFill
```
- 圆心坐标转换为左上角坐标

### ellipse → 椭圆
```
SVG:  <ellipse cx="640" cy="360" rx="80" ry="40" fill="none" stroke="#3B82F6" />
PPTX: add_shape(OVAL, cx-rx, cy-ry, 2*rx, 2*ry) + stroke
```

## 文本

### text → 文本框
```
SVG:  <text x="120" y="160" font-size="48" font-family="Arial" fill="#F8FAFC">标题</text>
PPTX: add_textbox(x, y, w, h) + text_frame
```
- 每个 `<text>` 创建一个独立文本框
- `<tspan>` 子元素 → 同一文本框内的多个 paragraph
- `font-size` → Pt(size)
- `font-family` → font.name
- `font-weight: bold` → font.bold = True
- `fill` → font.color.rgb
- `text-anchor: middle` → paragraph.alignment = CENTER

## 线条

### line → 线条
```
SVG:  <line x1="120" y1="240" x2="1160" y2="240" stroke="#334155" stroke-width="2" />
PPTX: add_shape(LINE_INVERSE, x1, y1, w, h) + stroke
```

## 路径

### path → 自由形状
```
SVG:  <path d="M 10 10 L 100 10 L 100 100 Z" fill="#3B82F6" />
PPTX: build_freeform() + add_line_segments() + convert_to_shape()
```
- `M` → 起点
- `L` → 直线段
- `C` → 三次贝塞尔曲线
- `Q` → 二次贝塞尔曲线（自动转为三次）
- `Z` → 闭合路径

### polygon / polyline → 自由形状
```
SVG:  <polygon points="100,10 200,90 300,10" fill="#3B82F6" />
PPTX: build_freeform() + add_line_segments() + convert_to_shape()
```

## 分组

### g → 递归处理
```
SVG:  <g transform="translate(100, 50)"><rect .../><text .../></g>
PPTX: 递归处理子元素，transform 应用到每个子元素
```

## 样式映射

| SVG 属性 | PPTX 属性 | 备注 |
|----------|----------|------|
| `fill="#RRGGBB"` | `shape.fill.solid()` + `fore_color.rgb` | hex → RGBColor |
| `fill="none"` | `shape.fill.background()` | 无填充 |
| `stroke="#RRGGBB"` | `shape.line.color.rgb` | |
| `stroke-width="N"` | `shape.line.width = Pt(N)` | |
| `opacity="0.5"` | ⚠ Phase 2 | 透明度暂不支持 |
| `font-family` | `run.font.name` | |
| `font-size` | `run.font.size = Pt(N)` | |
| `font-weight: bold` | `run.font.bold = True` | |
| `text-anchor: middle` | `paragraph.alignment = CENTER` | |

## 缩放

SVG viewBox 到 PPTX 的缩放：
```
scale_x = PPTX_slide_width / viewBox_width
scale_y = PPTX_slide_height / viewBox_height
```

默认：1280×720 viewBox → 13.33×7.5 英寸 PPTX（1:1 映射，无缩放）
