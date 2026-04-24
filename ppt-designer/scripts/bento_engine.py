#!/usr/bin/env python3
"""
Bento Grid Orchestrator + SVG Renderer
Usage: python3 bento_engine.py <deck.json> <output_dir>

Input: JSON deck file with slides, each containing section/title/subtitle/layout/cards
Output: SVG files for each slide + audit report
"""

import json, html, textwrap, sys, os
from pathlib import Path

class BentoEngine:
    def __init__(self, theme_name='light'):
        self.canvas = (1280, 720)
        self.frame = {'x':40,'y':32,'w':1200,'h':656}
        self.content = {'left':72,'top':210,'w':1136,'h':414}
        self.grid = {'cols':16,'rows':9,'gap':12}
        self.col_w = (self.content['w'] - self.grid['gap']*(self.grid['cols']-1))/self.grid['cols']
        self.row_h = (self.content['h'] - self.grid['gap']*(self.grid['rows']-1))/self.grid['rows']
        self.spacing = {'inner':12,'sibling':12,'group':18,'section':24}
        self.themes = {
            'light': {
                'bg':'#F8FAFC','frame':'#E2E8F0','card':'#FFFFFF','line':'#CBD5E1',
                'title':'#0F172A','sub':'#64748B','body':'#334155','pill':'#EEF2FF','accent':'#4F46E5',
                'l1_stroke':'#A5B4FC','font':"'PingFang SC','Microsoft YaHei',sans-serif"
            },
            'dark': {
                'bg':'#0F172A','frame':'#1E293B','card':'#1E293B','line':'#334155',
                'title':'#F1F5F9','sub':'#94A3B8','body':'#CBD5E1','pill':'#312E81','accent':'#818CF8',
                'l1_stroke':'#6366F1','font':"'PingFang SC','Microsoft YaHei',sans-serif"
            },
        }
        self.theme = self.themes[theme_name]
        self.layouts = {
            'nested_title_body': {
                'rhythm':'hero+nested-title-body+closure',
                'blocks':[
                    {'slot':'main','c':0,'r':0,'cs':8,'rs':5,'level':1},
                    {'slot':'group_title_body','c':8,'r':0,'cs':8,'rs':5,'level':2,
                     'children':[('child_title',0,0,8,1),('child_body',0,1,8,4)]},
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
                    {'slot':'group3_equal','c':10,'r':0,'cs':6,'rs':5,'level':2,
                     'children':[('child_body',0,0,6,1),('child_body',0,1,6,2),('child_body',0,3,6,2)]},
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
        limits = {
            'main': (18, 30, 3), 'body': (15, 22, 3),
            'child_title': (18, 38, 1), 'child_body': (38, 38, 2),
        }
        if slot in limits:
            tl, bl, bn = limits[slot]
            c['title'] = c['title'][:tl]
            c['bullets'] = [b[:bl]+('…' if len(b)>bl else '') for b in c['bullets'][:bn]]
        if slot == 'highlight':
            c['metric'] = str(c.get('metric', c['title']))[:8]
            c['label'] = c['title'][:12]
            c['sub'] = (c['bullets'][0] if c['bullets'] else '')[:12]
        if slot == 'thin':
            c['single'] = (c['title'] or (c['bullets'][0] if c['bullets'] else ''))[:30]
        if slot in ('child_title','child_body'):
            c['single'] = ' '.join(c['bullets'][:2])[:38] if c['bullets'] else c['title'][:38]
        return c

    def assign(self, slide):
        layout_name = self.choose_layout(slide)
        layout = self.layouts[layout_name]
        cards = [dict(c) for c in slide.get('cards',[])]
        narratives = [c for c in cards if not c.get('metric')]
        highlights = [c for c in cards if c.get('metric')]
        def pop(pool, fallback=None):
            if pool: return pool.pop(0)
            if fallback: return fallback.pop(0)
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
                    children_assigned.append({'slot':child[0],'geom':child[1:],'card':self.normalize(pop(narratives, highlights), child[0])})
                blocks.append({**b, 'children_assigned': children_assigned})
        compiled = {'section':slide['section'],'title':slide['title'],'subtitle':slide.get('subtitle',''),
                     'layout':layout_name,'rhythm':layout['rhythm'],'blocks':blocks}
        compiled['scores'] = self.score_slide(compiled)
        return compiled

    def score_slide(self, slide):
        weights, contrast, top_focus, size_types, nested_ok = [], 0, 0, set(), True
        for b in slide['blocks']:
            size_types.add((b['cs'],b['rs']))
            w = b['cs']*b['rs']
            if b['slot']=='main': w+=20
            if b['slot']=='highlight': w+=8; contrast+=1
            if b['r']<=1 and b['slot']=='main': top_focus+=1
            if b['slot']=='group_title_body':
                child_slots = [ch['slot'] for ch in b.get('children_assigned',[])]
                nested_ok = nested_ok and child_slots==['child_title','child_body']
            if b['slot']=='group3_equal':
                nested_ok = nested_ok and len(b.get('children_assigned',[]))==3
            weights.append({'slot':b['slot'],'weight':w})
        return {'top_focus_ok':top_focus>=1,'contrast_budget_ok':contrast<=2,
                'size_variety_ok':len(size_types)<=5,'nested_pattern_ok':nested_ok,
                'rhythm':slide['rhythm'],'weights':weights}

    def _wrap(self,text,width_px,font_pt):
        cpl = max(6, int(width_px/(font_pt*1.18)))
        return textwrap.wrap(text, width=cpl) or ['']

    def _text(self,x,y,text,size,fill,weight,width_px,lh=1.22):
        lines = self._wrap(text, width_px, size)
        tsp = []
        for i,line in enumerate(lines):
            dy = 0 if i==0 else size*lh
            tsp.append(f'<tspan x="{x}" dy="{dy}">{html.escape(line)}</tspan>')
        return f'<text x="{x}" y="{y}" font-family={self.theme["font"]!r} font-size="{size}" fill="{fill}" font-weight="{weight}">{"".join(tsp)}</text>'

    def _child_rect(self, gx, gy, gw, gh, geom, parent):
        cc,rr,cs,rs = geom
        pcs,prs = parent['cs'],parent['rs']
        gap = self.spacing['inner']
        cw = (gw - gap*(pcs-1))/pcs
        ch = (gh - gap*(prs-1))/prs
        x = gx + cc*(cw+gap); y = gy + rr*(ch+gap)
        w = cw*cs + gap*(cs-1); h = ch*rs + gap*(rs-1)
        return round(x),round(y),round(w),round(h)

    def render_slide_svg(self, slide, idx):
        t = self.theme
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">']
        svg += [f'<rect width="1280" height="720" fill="{t["bg"]}"/>',
                f'<rect x="40" y="32" width="1200" height="656" rx="30" fill="{t["bg"]}" stroke="{t["frame"]}"/>',
                f'<text x="72" y="68" font-family={t["font"]!r} font-size="12" fill="{t["accent"]}" font-weight="700">{html.escape(slide["section"].upper())}</text>',
                f'<text x="1180" y="68" text-anchor="end" font-family={t["font"]!r} font-size="12" fill="{t["sub"]}" font-weight="700">{idx:02d}</text>',
                f'<line x1="72" y1="88" x2="1208" y2="88" stroke="{t["frame"]}"/>',
                f'<text x="72" y="138" font-family={t["font"]!r} font-size="34" fill="{t["title"]}" font-weight="800">{html.escape(slide["title"])}</text>',
                f'<text x="72" y="170" font-family={t["font"]!r} font-size="18" fill="{t["sub"]}" font-weight="500">{html.escape(slide["subtitle"])}</text>']
        for b in slide['blocks']:
            x,y,w,h = self.cell(b['c'],b['r'],b['cs'],b['rs'])
            stroke = t['l1_stroke'] if b.get('level')==1 else t['line']
            svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{t["card"]}" stroke="{stroke}"/>')
            if b['slot'] in ('group_title_body','group3_equal'):
                for ch in b.get('children_assigned',[]):
                    ix,iy,iw,ih = self._child_rect(x+14,y+14,w-28,h-28,ch['geom'],b)
                    svg.append(f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="16" fill="#FFFFFF" stroke="{t["frame"]}"/>')
                    if ch['slot']=='child_title':
                        svg.append(self._text(ix+14,iy+28,ch['card'].get('single',''),14,t['title'],700,iw-28,1.15))
                    else:
                        svg.append(self._text(ix+14,iy+28,ch['card'].get('single',''),12,t['body'],500,iw-28,1.2))
            else:
                card = b['card']
                svg.append(f'<rect x="{x+16}" y="{y+14}" width="80" height="24" rx="12" fill="{t["pill"]}" stroke="{t["frame"]}"/>')
                svg.append(f'<text x="{x+30}" y="{y+30}" font-family={t["font"]!r} font-size="10" fill="{t["accent"]}" font-weight="700">{html.escape(card.get("tag","CARD"))}</text>')
                if b['slot']=='highlight':
                    svg.append(self._text(x+16,y+62,card.get('metric',''),28 if h>=160 else 24,t['title'],800,w-32,1.1))
                    svg.append(self._text(x+16,y+100,card.get('label',''),12,t['body'],500,w-32,1.2))
                    if card.get('sub'): svg.append(self._text(x+16,y+118,card['sub'],10,t['sub'],500,w-32,1.2))
                elif b['slot']=='thin':
                    svg.append(self._text(x+16,y+56,card.get('single',''),18,t['title'],700,w-32,1.2))
                else:
                    ts = 20 if b['slot']=='main' else 17
                    bs = 13 if b['slot']=='main' else 12
                    svg.append(self._text(x+16,y+54,card.get('title',''),ts,t['title'],700,w-32,1.2))
                    cy = y+84
                    for bullet in card.get('bullets',[]):
                        lines = self._wrap('• '+bullet,w-32,bs)
                        tsp = []
                        for i,line in enumerate(lines):
                            dy = 0 if i==0 else bs*1.2
                            tsp.append(f'<tspan x="{x+16}" dy="{dy}">{html.escape(line)}</tspan>')
                        svg.append(f'<text x="{x+16}" y="{cy}" font-family={t["font"]!r} font-size="{bs}" fill="{t["body"]}" font-weight="500">{"".join(tsp)}</text>')
                        cy += len(lines)*bs*1.2+6
        svg.append('</svg>')
        return ''.join(svg)

    def build(self, deck):
        compiled = [self.assign(slide) for slide in deck]
        svgs = [self.render_slide_svg(slide,i+1) for i,slide in enumerate(compiled)]
        audit = [{'slide_index':i+1,'title':s['title'],'layout':s['layout'],'rhythm':s['rhythm'],**s['scores']} for i,s in enumerate(compiled)]
        return compiled, svgs, audit

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <deck.json> <output_dir>")
        sys.exit(1)
    deck_path, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    deck = json.loads(Path(deck_path).read_text())
    engine = BentoEngine('light')
    compiled, svgs, audit = engine.build(deck)
    for i,svg in enumerate(svgs):
        Path(out_dir, f'slide_{i+1:02d}.svg').write_text(svg)
    Path(out_dir, 'audit.json').write_text(json.dumps(audit, indent=2, ensure_ascii=False))
    print(f"Generated {len(svgs)} slides + audit.json in {out_dir}")
