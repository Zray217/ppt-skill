#!/usr/bin/env python3
"""
SVG → PPTX: 纯 SVG 嵌入，零 PNG，零 python-pptx。

PPT 2016+ 原生 <a:svgBlip>，右键→转换为图形→可编辑。

Usage:
    python3 svg2pptx-svgblip.py output.pptx slide1.svg [slide2.svg ...]
"""

import sys, os, zipfile

CX = 12192000  # slide width EMU
CY = 6858000   # slide height EMU


def slide_xml(svg_rid="rId2"):
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr/>
      <p:pic>
        <p:nvPicPr>
          <p:cNvPr id="2" name="Picture 1"/>
          <p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>
          <p:nvPr/>
        </p:nvPicPr>
        <p:blipFill>
          <a:blip r:embed="{svg_rid}">
            <a:svgBlip r:embed="{svg_rid}"/>
          </a:blip>
          <a:stretch><a:fillRect/></a:stretch>
        </p:blipFill>
        <p:spPr>
          <a:xfrm><a:off x="0" y="0"/><a:ext cx="{CX}" cy="{CY}"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
        </p:spPr>
      </p:pic>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>'''


def slide_rels(layout_target, svg_target):
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="{layout_target}"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="{svg_target}"/>
</Relationships>'''


def convert(svg_files, output_path):
    n = len(svg_files)

    # Build content types
    slide_overrides = "\n".join(
        f'<Override PartName="/ppt/slides/slide{i+1}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(n)
    )

    content_types = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="svg" ContentType="image/svg+xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  {slide_overrides}
</Types>'''

    # presentation.xml.rels
    slide_rels_entries = "\n".join(
        f'<Relationship Id="rId{i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i+1}.xml"/>'
        for i in range(n)
    )

    pres_rels = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {slide_rels_entries}
</Relationships>'''

    # presentation.xml
    sld_id_list = "\n".join(
        f'<p:sldId id="{256+i}" r:id="rId{i+1}"/>'
        for i in range(n)
    )

    presentation = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
                saveSubsetFonts="1">
  <p:sldIdLst>{sld_id_list}</p:sldIdLst>
  <p:sldSz cx="{CX}" cy="{CY}"/>
  <p:notesSz cx="{CX}" cy="{CY}"/>
</p:presentation>'''

    # _rels/.rels
    root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>'''

    # Write PPTX
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("ppt/presentation.xml", presentation)
        z.writestr("ppt/_rels/presentation.xml.rels", pres_rels)

        for i, svg_path in enumerate(svg_files):
            slide_num = i + 1
            media_name = f"image{slide_num}.svg"

            with open(svg_path, "rb") as f:
                svg_bytes = f.read()

            z.writestr(f"ppt/media/{media_name}", svg_bytes)
            z.writestr(f"ppt/slides/slide{slide_num}.xml", slide_xml("rId2"))
            z.writestr(f"ppt/slides/_rels/slide{slide_num}.xml.rels",
                       slide_rels("../slideLayouts/slideLayout1.xml", f"../media/{media_name}"))

            print(f"  ✓ Slide {slide_num}: {os.path.basename(svg_path)} ({len(svg_bytes)/1024:.0f}KB)")

    size_kb = os.path.getsize(output_path) / 1024
    print(f"\n✅ {output_path} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} output.pptx slide1.svg [slide2.svg ...]")
        sys.exit(1)

    output = os.path.abspath(sys.argv[1])
    svgs = [os.path.abspath(s) for s in sys.argv[2:]]
    print(f"📄 {len(svgs)} 个 SVG → PPTX (纯 SVG 嵌入，零 PNG)")
    convert(svgs, output)
