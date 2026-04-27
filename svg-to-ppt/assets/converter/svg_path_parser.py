"""
SVG path d attribute parser.
Parses SVG path data into a list of command dicts.
Supports: M, L, H, V, C, S, Q, T, A, Z (absolute + relative)
Arc commands (A) are converted to cubic bezier curves.
"""

import re
import math


def _arc_to_cubics(x1, y1, rx, ry, phi_deg, fa, fs, x2, y2) -> list[dict]:
    """Convert SVG arc to cubic bezier curves.
    
    Based on SVG spec arc implementation notes.
    """
    if rx == 0 or ry == 0:
        return [{'type': 'C', 'x': x2, 'y': y2,
                 'cx1': x1, 'cy1': y1, 'cx2': x2, 'cy2': y2}]
    
    rx = abs(rx)
    ry = abs(ry)
    phi = math.radians(phi_deg)
    
    cos_phi = math.cos(phi)
    sin_phi = math.sin(phi)
    
    # Step 1: transform to ellipse center
    dx = (x1 - x2) / 2
    dy = (y1 - y2) / 2
    
    x1p = cos_phi * dx + sin_phi * dy
    y1p = -sin_phi * dx + cos_phi * dy
    
    # Ensure rx, ry are large enough
    lam = (x1p / rx) ** 2 + (y1p / ry) ** 2
    if lam > 1:
        s = math.sqrt(lam)
        rx *= s
        ry *= s
    
    # Step 2: center
    rx2 = rx * rx
    ry2 = ry * ry
    x1p2 = x1p * x1p
    y1p2 = y1p * y1p
    
    num = max(0, rx2 * ry2 - rx2 * y1p2 - ry2 * x1p2)
    den = rx2 * y1p2 + ry2 * x1p2
    sq = math.sqrt(num / den) if den != 0 else 0
    
    if fa == fs:
        sq = -sq
    
    cxp = sq * rx * y1p / ry
    cyp = -sq * ry * x1p / rx
    
    cx = cos_phi * cxp - sin_phi * cyp + (x1 + x2) / 2
    cy = sin_phi * cxp + cos_phi * cyp + (y1 + y2) / 2
    
    # Step 3: angles
    def _angle(ux, uy, vx, vy):
        n = math.sqrt(ux*ux + uy*uy) * math.sqrt(vx*vx + vy*vy)
        if n == 0:
            return 0
        c = (ux*vx + uy*vy) / n
        c = max(-1, min(1, c))
        ang = math.acos(c)
        if ux*vy - uy*vx < 0:
            ang = -ang
        return ang
    
    theta = _angle(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dtheta = _angle((x1p - cxp) / rx, (y1p - cyp) / ry,
                     (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    
    if fs == 0 and dtheta > 0:
        dtheta -= 2 * math.pi
    elif fs == 1 and dtheta < 0:
        dtheta += 2 * math.pi
    
    # Step 4: split into segments (max 90° each)
    segments = max(1, int(math.ceil(abs(dtheta) / (math.pi / 2))))
    delta = dtheta / segments
    
    # Generate cubic bezier approximation
    alpha = math.sin(delta) * (math.sqrt(4 + 3 * math.tan(delta/2)**2) - 1) / 3
    
    curves = []
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)
    
    for i in range(segments):
        angle1 = theta + i * delta
        angle2 = theta + (i + 1) * delta
        
        cos_a1 = math.cos(angle1)
        sin_a1 = math.sin(angle1)
        cos_a2 = math.cos(angle2)
        sin_a2 = math.sin(angle2)
        
        # Control points in ellipse space
        epx1 = cos_a1 - alpha * sin_a1
        epy1 = sin_a1 + alpha * cos_a1
        epx2 = cos_a2 + alpha * sin_a2
        epy2 = sin_a2 - alpha * cos_a2
        
        # Transform back to user space
        def to_user(ex, ey):
            ux = cos_phi * rx * ex - sin_phi * ry * ey + cx
            uy = sin_phi * rx * ex + cos_phi * ry * ey + cy
            return ux, uy
        
        cp1x, cp1y = to_user(epx1, epy1)
        cp2x, cp2y = to_user(epx2, epy2)
        endx, endy = to_user(cos_a2, sin_a2)
        
        curves.append({
            'type': 'C', 'x': endx, 'y': endy,
            'cx1': cp1x, 'cy1': cp1y, 'cx2': cp2x, 'cy2': cp2y
        })
    
    return curves


def parse_path_d(d: str) -> list[dict]:
    """Parse SVG path d attribute into command list.
    
    Returns list of dicts:
      {'type': 'M'|'L'|'C'|'Z', 'x': float, 'y': float, 
       'cx1': float, 'cy1': float, 'cx2': float, 'cy2': float}
    Arc commands (A/a) are converted to cubic bezier curves.
    """
    if not d or not d.strip():
        return []
    
    tokens = re.findall(
        r'[MmLlHhVvCcSsQqTtAaZz]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?', d
    )
    
    commands = []
    cx, cy = 0.0, 0.0
    start_x, start_y = 0.0, 0.0
    last_cmd = None
    last_cx2, last_cy2 = 0.0, 0.0

    def _process(cmd, p):
        nonlocal cx, cy, start_x, start_y, last_cmd, last_cx2, last_cy2
        is_rel = cmd.islower()
        up = cmd.upper()

        if up == 'M':
            for i in range(0, len(p), 2):
                x, y = float(p[i]), float(p[i+1])
                if is_rel:
                    x += cx; y += cy
                if i == 0:
                    commands.append({'type': 'M', 'x': x, 'y': y})
                    start_x, start_y = x, y
                else:
                    commands.append({'type': 'L', 'x': x, 'y': y})
                cx, cy = x, y

        elif up == 'L':
            for i in range(0, len(p), 2):
                x, y = float(p[i]), float(p[i+1])
                if is_rel:
                    x += cx; y += cy
                commands.append({'type': 'L', 'x': x, 'y': y})
                cx, cy = x, y

        elif up == 'H':
            for val in p:
                x = float(val)
                if is_rel:
                    x += cx
                commands.append({'type': 'L', 'x': x, 'y': cy})
                cx = x

        elif up == 'V':
            for val in p:
                y = float(val)
                if is_rel:
                    y += cy
                commands.append({'type': 'L', 'x': cx, 'y': y})
                cy = y

        elif up == 'C':
            for i in range(0, len(p), 6):
                cx1, cy1 = float(p[i]), float(p[i+1])
                cx2, cy2 = float(p[i+2]), float(p[i+3])
                x, y = float(p[i+4]), float(p[i+5])
                if is_rel:
                    cx1 += cx; cy1 += cy
                    cx2 += cx; cy2 += cy
                    x += cx; y += cy
                commands.append({
                    'type': 'C', 'x': x, 'y': y,
                    'cx1': cx1, 'cy1': cy1, 'cx2': cx2, 'cy2': cy2
                })
                last_cx2, last_cy2 = cx2, cy2
                cx, cy = x, y

        elif up == 'S':
            for i in range(0, len(p), 4):
                cx2, cy2 = float(p[i]), float(p[i+1])
                x, y = float(p[i+2]), float(p[i+3])
                if is_rel:
                    cx2 += cx; cy2 += cy
                    x += cx; y += cy
                if last_cmd in ('C', 'S'):
                    cx1 = 2 * cx - last_cx2
                    cy1 = 2 * cy - last_cy2
                else:
                    cx1, cy1 = cx, cy
                commands.append({
                    'type': 'C', 'x': x, 'y': y,
                    'cx1': cx1, 'cy1': cy1, 'cx2': cx2, 'cy2': cy2
                })
                last_cx2, last_cy2 = cx2, cy2
                cx, cy = x, y

        elif up == 'Q':
            for i in range(0, len(p), 4):
                qx, qy = float(p[i]), float(p[i+1])
                x, y = float(p[i+2]), float(p[i+3])
                if is_rel:
                    qx += cx; qy += cy
                    x += cx; y += cy
                cx1 = cx + 2/3 * (qx - cx)
                cy1 = cy + 2/3 * (qy - cy)
                cx2 = x + 2/3 * (qx - x)
                cy2 = y + 2/3 * (qy - y)
                commands.append({
                    'type': 'C', 'x': x, 'y': y,
                    'cx1': cx1, 'cy1': cy1, 'cx2': cx2, 'cy2': cy2
                })
                last_cx2, last_cy2 = cx2, cy2
                cx, cy = x, y

        elif up == 'T':
            for i in range(0, len(p), 2):
                x, y = float(p[i]), float(p[i+1])
                if is_rel:
                    x += cx; y += cy
                if last_cmd in ('Q', 'T'):
                    qx = 2 * cx - last_cx2
                    qy = 2 * cy - last_cy2
                else:
                    qx, qy = cx, cy
                cx1 = cx + 2/3 * (qx - cx)
                cy1 = cy + 2/3 * (qy - cy)
                cx2 = x + 2/3 * (qx - x)
                cy2 = y + 2/3 * (qy - y)
                commands.append({
                    'type': 'C', 'x': x, 'y': y,
                    'cx1': cx1, 'cy1': cy1, 'cx2': cx2, 'cy2': cy2
                })
                cx, cy = x, y

        elif up == 'A':
            # Arc: rx ry x-rotation large-arc-flag sweep-flag x y
            for i in range(0, len(p), 7):
                rx = float(p[i])
                ry = float(p[i+1])
                x_rot = float(p[i+2])
                large_arc = int(float(p[i+3]))
                sweep = int(float(p[i+4]))
                x = float(p[i+5])
                y = float(p[i+6])
                if is_rel:
                    x += cx; y += cy
                
                # Convert arc to cubic beziers
                arc_curves = _arc_to_cubics(cx, cy, rx, ry, x_rot, large_arc, sweep, x, y)
                commands.extend(arc_curves)
                
                cx, cy = x, y

        elif up == 'Z':
            commands.append({'type': 'Z'})
            cx, cy = start_x, start_y

        last_cmd = up

    # Parse tokens
    current_cmd = None
    params = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if re.match(r'[A-Za-z]', token):
            if current_cmd is not None and params:
                _process(current_cmd, params)
            current_cmd = token
            params = []
        else:
            params.append(token)
        i += 1

    if current_cmd is not None and params:
        _process(current_cmd, params)

    return commands


if __name__ == '__main__':
    # Test basic shapes
    d = "M 10 10 L 100 10 L 100 100 L 10 100 Z"
    print("Rect:", len(parse_path_d(d)), "commands")
    
    d2 = "M 10 80 C 40 10, 65 10, 95 80 S 150 150, 180 80"
    print("Curve:", len(parse_path_d(d2)), "commands")
    
    # Test arc
    d3 = "M 10 80 A 30 30 0 0 1 100 80"
    cmds = parse_path_d(d3)
    print("Arc:", len(cmds), "commands (converted to cubic beziers)")
    for c in cmds:
        print(f"  {c['type']}: ({c.get('x',0):.1f}, {c.get('y',0):.1f})")
