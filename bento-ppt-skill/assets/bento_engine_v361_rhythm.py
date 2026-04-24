
from pathlib import Path
from typing import List, Dict, Any
import json, html, textwrap

class BentoEngineV361:
    def __init__(self):
        self.canvas = (1280, 720)
        self.frame = {'x':40,'y':32,'w':1200,'h':656}
        self.content = {'left':72,'top':210,'w':1136,'h':414}
        self.grid = {'cols':16,'rows':9,'gap':12}
        self.col_w = (self.content['w'] - self.grid['gap']*(self.grid['cols']-1))/self.grid['cols']
        self.row_h = (self.content['h'] - self.grid['gap']*(self.grid['rows']-1))/self.grid['rows']
        self.spacing = {'inner':12,'sibling':12,'group':18,'section':24}
        self.theme = {
            'bg':'#F8FAFC','frame':'#E2E8F0','card':'#FFFFFF','line':'#CBD5E1',
            'title':'#0F172A','sub':'#64748B','body':'#334155','pill':'#EEF2FF','accent':'#4F46E5',
            'font':"'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif"
        }
        self.layouts = {
            'nested_title_body': {
                'rhythm':'hero+nested-title-body+closure',
                'blocks':[
                    {'slot':'main','c':0,'r':0,'cs':8,'rs':5,'level':1},
                    {'slot':'group_title_body','c':8,'r':0,'cs':8,'rs':5,'level':2,'children':[('child_title',0,0,8,1),('child_body',0,1,8,4)]},
                    {'slot':'body','c':0,'r':5,'cs':6,'rs':4,'level':2},
                    {'slot':'body','c':6,'r':5,'cs':5,'rs':4,'level':3},
                    {'slot':'body','c':11,'r':5,'cs':5,'rs':4,'level':3,'closure':True},
                ]
            },
            'top_main_bar': {
                'rhythm':'hero+support+bottom-bar',
                'blocks':[
                    {'slot':'main','c':0,'r':0,'cs':10,'rs':5,'level':1},
                    {'slot':'body','c':10,'r':0,'cs':6,'rs':5,'level':2},
                    {'slot':'body','c':0,'r':5,'cs':8,'rs':2,'level':3},
                    {'slot':'body','c':8,'r':5,'cs':8,'rs':2,'level':3},
                    {'slot':'thin','c':0,'r':7,'cs':16,'rs':2,'level':2,'closure':True},
                ]
            },
            'dual_main_metrics': {
                'rhythm':'compare+metric-contrast',
                'blocks':[
                    {'slot':'main','c':0,'r':0,'cs':8,'rs':5,'level':1},
                    {'slot':'main','c':8,'r':0,'cs':8,'rs':5,'level':1},
                    {'slot':'body','c':0,'r':5,'cs':8,'rs':4,'level':2},
                    {'slot':'highlight','c':8,'r':5,'cs':4,'rs':4,'level':2},
                    {'slot':'highlight','c':12,'r':5,'cs':4,'rs':4,'level':2,'closure':True},
                ]
            },
            'main_with_group3_equal': {
                'rhythm':'hero+equal-triple-group',
                'blocks':[
                    {'slot':'main','c':0,'r':0,'cs':10,'rs':5,'level':1},
                    {'slot':'group3_equal','c':10,'r':0,'cs':6,'rs':5,'level':2,'children':[('child_body',0,0,6,1),('child_body',0,1,6,2),('child_body',0,3,6,2)]},
                    {'slot':'body','c':0,'r':5,'cs':5,'rs':4,'level':2},
                    {'slot':'body','c':5,'r':5,'cs':5,'rs':4,'level':3},
                    {'slot':'body','c':10,'r':5,'cs':6,'rs':4,'level':3,'closure':True},
                ]
            },
            'rules_rhythm': {
                'rhythm':'small+hero+two-column-close',
                'blocks':[
                    {'slot':'body','c':0,'r':0,'cs':5,'rs':4,'level':2},
                    {'slot':'main','c':5,'r':0,'cs':11,'rs':4,'level':1},
                    {'slot':'body','c':0,'r':4,'cs':8,'rs':5,'level':2},
                    {'slot':'body','c':8,'r':4,'cs':8,'rs':5,'level':3,'closure':True},
                ]
            },
        }

    def cell(self,c,r,cs,rs):
        x = self.content['left'] + c*(self.col_w+self.grid['gap'])
        y = self.content['top'] + r*(self.row_h+self.grid['gap'])
        w = self.col_w*cs + self.grid['gap']*(cs-1)
        h = self.row_h*rs + self.grid['gap']*(rs-1)
        return round(x), round(y), round(w), round(h)

    def classify(self, card):
        if card.get('kind'): return card['kind']
        if card.get('metric'): return 'highlight'
        if len(card.get('bullets',[])) >= 4: return 'step'
        return 'body'

    def choose_layout(self, slide):
        if slide.get('layout') in self.layouts: return slide['layout']
        metrics = sum(1 for c in slide.get('cards',[]) if c.get('metric'))
        if metrics >= 2: return 'dual_main_metrics'
        if len(slide.get('cards',[])) >= 5: return 'nested_title_body'
        return 'rules_rhythm'

    def normalize(self, card, slot):
        c = dict(card)
        c['kind'] = self.classify(c)
        c['title'] = c.get('title','').strip()
        c['bullets'] = [b.strip() for b in c.get('bullets',[]) if b.strip()]
        if slot == 'main':
            c['title'] = c['title'][:18]
            c['bullets'] = [b[:30] + ('…' if len(b)>30 else '') for b in c['bullets'][:3]]
        elif slot == 'body':
            c['title'] = c['title'][:15]
            c['bullets'] = [b[:22] + ('…' if len(b)>22 else '') for b in c['bullets'][:3]]
        elif slot == 'highlight':
            c['metric'] = str(c.get('metric', c['title']))[:8]
            c['label'] = (c['title'] if c.get('metric') else (c['bullets'][0] if c['bullets'] else c['title']))[:12]
            c['sub'] = (c['bullets'][0] if c.get('metric') and c['bullets'] else '')[:12]
        elif slot == 'thin':
            c['single'] = (c['title'] or (c['bullets'][0] if c['bullets'] else ''))[:30]
        elif slot == 'child_title':
            c['single'] = (c['title'] or (c['bullets'][0] if c['bullets'] else ''))[:18]
        elif slot == 'child_body':
            text = ' '.join(c['bullets'][:2]) if c['bullets'] else c['title']
            c['single'] = text[:38] + ('…' if len(text)>38 else '')
        return c

    def assign(self, slide):
        layout_name = self.choose_layout(slide)
        layout = self.layouts[layout_name]
        cards = [dict(c) for c in slide.get('cards',[])]
        narratives = [c for c in cards if not c.get('metric')]
        highlights = [c for c in cards if c.get('metric')]

        def pop(pool, fallback=None):
            if pool: return pool.pop(0)
            if fallback and fallback: return fallback.pop(0)
            return {'title':'', 'bullets':[''], 'tag':'AUTO'}

        blocks = []
        for b in layout['blocks']:
            slot = b['slot']
            if slot == 'main':
                blocks.append({**b, 'card': self.normalize(pop(narratives), 'main')})
            elif slot == 'body':
                blocks.append({**b, 'card': self.normalize(pop(narratives, highlights), 'body')})
            elif slot == 'highlight':
                blocks.append({**b, 'card': self.normalize(pop(highlights, narratives), 'highlight')})
            elif slot == 'thin':
                blocks.append({**b, 'card': self.normalize(pop(narratives, highlights), 'thin')})
            elif slot in ('group_title_body','group3_equal'):
                children_assigned = []
                for child in b['children']:
                    children_assigned.append({'slot': child[0], 'geom': child[1:], 'card': self.normalize(pop(narratives, highlights), child[0])})
                blocks.append({**b, 'children_assigned': children_assigned})
        compiled = {'section': slide['section'], 'title': slide['title'], 'subtitle': slide.get('subtitle',''), 'layout': layout_name, 'rhythm': layout['rhythm'], 'blocks': blocks}
        compiled['scores'] = self.score_slide(compiled)
        return compiled

    def score_slide(self, slide):
        weights = []
        contrast = 0
        top_focus = 0
        size_types = set()
        nested_ok = True
        for b in slide['blocks']:
            size_types.add((b['cs'], b['rs']))
            weight = b['cs']*b['rs']
            if b['slot'] == 'main': weight += 20
            if b['slot'] == 'highlight':
                weight += 8
                contrast += 1
            if b['r'] <= 1 and b['slot'] == 'main': top_focus += 1
            if b['slot'] == 'group_title_body':
                child_slots = [ch['slot'] for ch in b['children_assigned']]
                nested_ok = nested_ok and child_slots == ['child_title','child_body']
            if b['slot'] == 'group3_equal':
                spans = [tuple(ch['geom']) for ch in b['children_assigned']]
                nested_ok = nested_ok and len(spans) == 3
            weights.append({'slot': b['slot'], 'weight': weight})
        return {
            'top_focus_ok': top_focus >= 1,
            'contrast_budget_ok': contrast <= 2,
            'size_variety_ok': len(size_types) <= 5,
            'nested_pattern_ok': nested_ok,
            'rhythm': slide['rhythm'],
            'weights': weights,
        }

    def _wrap(self,text,width_px,font_pt):
        cpl = max(6, int(width_px/(font_pt*1.18)))
        return textwrap.wrap(text, width=cpl, break_long_words=False, break_on_hyphens=False) or ['']

    def _text(self,x,y,text,size,fill,weight,width_px,lh=1.22):
        lines = self._wrap(text, width_px, size)
        tsp = []
        for i,line in enumerate(lines):
            dy = 0 if i == 0 else size*lh
            tsp.append(f'<tspan x="{x}" dy="{dy}">{html.escape(line)}</tspan>')
        return f'<text x="{x}" y="{y}" font-family={self.theme["font"]!r} font-size="{size}" fill="{fill}" font-weight="{weight}">{"".join(tsp)}</text>'

    def _child_rect(self, gx, gy, gw, gh, geom, parent):
        cc, rr, cs, rs = geom
        pcs, prs = parent['cs'], parent['rs']
        gap = self.spacing['inner']
        cw = (gw - gap*(pcs-1))/pcs
        ch = (gh - gap*(prs-1))/prs
        x = gx + cc*(cw+gap)
        y = gy + rr*(ch+gap)
        w = cw*cs + gap*(cs-1)
        h = ch*rs + gap*(rs-1)
        return round(x), round(y), round(w), round(h)

    def render_slide_svg(self, slide, idx):
        t = self.theme
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">']
        svg += [
            f'<rect width="1280" height="720" fill="{t["bg"]}"/>',
            f'<rect x="40" y="32" width="1200" height="656" rx="30" fill="{t["bg"]}" stroke="{t["frame"]}"/>',
            f'<text x="72" y="68" font-family={t["font"]!r} font-size="12" fill="{t["accent"]}" font-weight="700">{html.escape(slide["section"].upper())}</text>',
            f'<text x="1180" y="68" text-anchor="end" font-family={t["font"]!r} font-size="12" fill="{t["sub"]}" font-weight="700">{idx:02d}</text>',
            f'<line x1="72" y1="88" x2="1208" y2="88" stroke="{t["frame"]}"/>',
            f'<text x="72" y="138" font-family={t["font"]!r} font-size="34" fill="{t["title"]}" font-weight="800">{html.escape(slide["title"])}</text>',
            f'<text x="72" y="170" font-family={t["font"]!r} font-size="18" fill="{t["sub"]}" font-weight="500">{html.escape(slide["subtitle"])}</text>'
        ]
        for b in slide['blocks']:
            x,y,w,h = self.cell(b['c'], b['r'], b['cs'], b['rs'])
            stroke = '#A5B4FC' if b.get('level') == 1 else t['line']
            svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{t["card"]}" stroke="{stroke}"/>')
            if b['slot'] in ('group_title_body','group3_equal'):
                for ch in b['children_assigned']:
                    ix,iy,iw,ih = self._child_rect(x+14, y+14, w-28, h-28, ch['geom'], b)
                    svg.append(f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="16" fill="#FFFFFF" stroke="{t["frame"]}"/>')
                    if ch['slot'] == 'child_title':
                        svg.append(self._text(ix+14, iy+28, ch['card']['single'], 14, t['title'], 700, iw-28, 1.15))
                    else:
                        svg.append(self._text(ix+14, iy+28, ch['card']['single'], 12, t['body'], 500, iw-28, 1.2))
            else:
                card = b['card']
                svg.append(f'<rect x="{x+16}" y="{y+14}" width="80" height="24" rx="12" fill="{t["pill"]}" stroke="{t["frame"]}"/>')
                svg.append(f'<text x="{x+30}" y="{y+30}" font-family={t["font"]!r} font-size="10" fill="{t["accent"]}" font-weight="700">{html.escape(card.get("tag","CARD"))}</text>')
                if b['slot'] == 'highlight':
                    svg.append(self._text(x+16, y+62, card.get('metric',''), 28 if h >= 160 else 24, t['title'], 800, w-32, 1.1))
                    svg.append(self._text(x+16, y+100, card.get('label',''), 12, t['body'], 500, w-32, 1.2))
                    if card.get('sub'):
                        svg.append(self._text(x+16, y+118, card.get('sub',''), 10, t['sub'], 500, w-32, 1.2))
                elif b['slot'] == 'thin':
                    svg.append(self._text(x+16, y+56, card.get('single',''), 18, t['title'], 700, w-32, 1.2))
                else:
                    title_size = 20 if b['slot'] == 'main' else 17
                    body_size = 13 if b['slot'] == 'main' else 12
                    svg.append(self._text(x+16, y+54, card.get('title',''), title_size, t['title'], 700, w-32, 1.2))
                    cur_y = y + 84
                    for bullet in card.get('bullets',[]):
                        lines = self._wrap('• ' + bullet, w-32, body_size)
                        tsp = []
                        for i,line in enumerate(lines):
                            dy = 0 if i == 0 else body_size*1.2
                            tsp.append(f'<tspan x="{x+16}" dy="{dy}">{html.escape(line)}</tspan>')
                        svg.append(f'<text x="{x+16}" y="{cur_y}" font-family={t["font"]!r} font-size="{body_size}" fill="{t["body"]}" font-weight="500">{"".join(tsp)}</text>')
                        cur_y += len(lines)*body_size*1.2 + 6
        svg.append('</svg>')
        return ''.join(svg)

    def build(self, deck):
        compiled = [self.assign(slide) for slide in deck]
        svgs = [self.render_slide_svg(slide, i+1) for i,slide in enumerate(compiled)]
        audit = []
        for i,slide in enumerate(compiled,1):
            audit.append({
                'slide_index': i,
                'title': slide['title'],
                'layout': slide['layout'],
                'rhythm': slide['rhythm'],
                'top_focus_ok': slide['scores']['top_focus_ok'],
                'contrast_budget_ok': slide['scores']['contrast_budget_ok'],
                'size_variety_ok': slide['scores']['size_variety_ok'],
                'nested_pattern_ok': slide['scores']['nested_pattern_ok'],
            })
        return compiled, svgs, audit


def sample_deck():
    return [
        {
            'section':'Bento V361','title':'节奏骨架 A','subtitle':'左上主卡，右上父卡采用标题子卡 + 正文子卡。','layout':'nested_title_body',
            'cards':[
                {'title':'主卡片：方法主线','tag':'MAIN','bullets':['主叙事区固定在上方左侧，紧贴主标题区域。','右上父卡上部只承担标题，下部承接正文说明。','这样结构更清晰，也更像成熟版式。']},
                {'title':'右上组标题','tag':'T1','bullets':['作为组标题']},
                {'title':'右上组正文','tag':'T2','bullets':['下方子卡专门承接正文内容，不再把标题和正文混写在同一狭小子卡中。']},
                {'title':'展开说明','tag':'DETAIL','bullets':['底部宽卡承接案例、限制条件和场景说明。']},
                {'title':'风险提醒','tag':'RISK','bullets':['太窄的卡片不写长句。','太扁的卡片不放多段。']},
                {'title':'动作建议','tag':'ACT','bullets':['先做内容分型。','再做 span 分配。','最后再做美化。']},
            ]
        },
        {
            'section':'Bento V361','title':'节奏骨架 B','subtitle':'主叙事在上，底部条带承担收束节奏。','layout':'top_main_bar',
            'cards':[
                {'title':'主叙事区','tag':'MAIN','bullets':['主叙事优先靠近标题，放在上部。','这样页面更稳，也更像完整汇报页。']},
                {'title':'侧边说明','tag':'SIDE','bullets':['右侧承担补充和边界说明。']},
                {'title':'应用场景','tag':'USE','bullets':['适合放场景。','适合放案例。']},
                {'title':'结论收束','tag':'WRAP','bullets':['中下部保持信息闭环。']},
                {'title':'底部条带：一句主张','tag':'BAR','bullets':['16x2 默认单层表达。']},
            ]
        },
        {
            'section':'Bento V361','title':'节奏骨架 C','subtitle':'双主卡对比 + 双高亮，控制对比预算。','layout':'dual_main_metrics',
            'cards':[
                {'title':'方案 A','tag':'A','bullets':['左侧保持完整叙事，并靠近标题区域。']},
                {'title':'方案 B','tag':'B','bullets':['右侧与左侧对称，适合双路径对比。']},
                {'title':'补充解释','tag':'DETAIL','bullets':['底部左区继续承接说明，避免上方信息过载。']},
                {'title':'覆盖国家','tag':'REACH','metric':'175+','bullets':['短比例小卡']},
                {'title':'工具内置','tag':'TOOLS','metric':'50+','bullets':['固定短比例']},
            ]
        },
        {
            'section':'Bento V361','title':'节奏骨架 D','subtitle':'上方主卡 + 右侧三等分子卡，形成三个板块。','layout':'main_with_group3_equal',
            'cards':[
                {'title':'主承接区','tag':'MAIN','bullets':['主叙事区尽量靠近主标题，优先放在上方。','多个补充块应围绕主叙事展开。','右侧父卡改成三个均分子卡，形成更稳定的三板块节奏。']},
                {'title':'模块一','tag':'01','bullets':['短说明。','短标签。']},
                {'title':'模块二','tag':'02','bullets':['短说明。','短标签。']},
                {'title':'模块三','tag':'03','bullets':['短说明。','短标签。']},
                {'title':'案例补充','tag':'CASE','bullets':['放案例。','放补充。']},
                {'title':'下一步','tag':'NEXT','bullets':['放行动建议。','放收束内容。']},
            ]
        },
        {
            'section':'Bento V361','title':'规则页','subtitle':'把新的父子卡规则正式沉淀到编排器。','layout':'rules_rhythm',
            'cards':[
                {'title':'父子卡规则','tag':'NEST','bullets':['右上双子卡优先采用 上标题 / 下正文。','右侧三子卡优先采用均分三板块。']},
                {'title':'页面节奏规则','tag':'RHYTHM','bullets':['页面必须拼满主内容区。','至少保留一个上方主叙事区。','同页高对比焦点控制在 1 到 2 个。']},
                {'title':'Spacing 规则','tag':'SPACE','bullets':['父子卡、同组卡、跨组卡使用不同间距 token。']},
                {'title':'编排器策略','tag':'ENGINE','bullets':['先做内容分型。','再套用节奏骨架。','再做安全尺寸与审计。']},
            ]
        }
    ]
