#!/usr/bin/env python3

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def load_engine(engine_path: Path):
    spec = importlib.util.spec_from_file_location("bento_engine_module", engine_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load engine from {engine_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize_slides(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        if isinstance(payload.get("slides"), list):
            return payload["slides"]
        if isinstance(payload.get("deck"), list):
            return payload["deck"]
    raise ValueError("Input JSON must be a list or an object with a 'slides' array.")


def build_engine_input(slides: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    engine_input: list[dict[str, Any]] = []
    manifest: list[dict[str, Any]] = []

    for slide in slides:
        slide_number = slide.get("slide_number")
        render_mode = slide.get("render_mode", "engine")
        page_role = slide.get("page_role", "content")
        title = slide.get("title", "")

        if render_mode != "engine":
            manifest.append(
                {
                    "slide_number": slide_number,
                    "page_role": page_role,
                    "render_mode": render_mode,
                    "status": "skipped",
                    "reason": "render_mode is not 'engine'",
                    "title": title,
                }
            )
            continue

        cards = slide.get("cards")
        if not isinstance(cards, list) or not cards:
            manifest.append(
                {
                    "slide_number": slide_number,
                    "page_role": page_role,
                    "render_mode": render_mode,
                    "status": "skipped",
                    "reason": "missing non-empty cards array",
                    "title": title,
                }
            )
            continue

        engine_input.append(
            {
                "section": slide.get("section", page_role.upper()),
                "title": title,
                "subtitle": slide.get("subtitle", ""),
                "layout": slide.get("layout"),
                "cards": cards,
            }
        )
        manifest.append(
            {
                "slide_number": slide_number,
                "page_role": page_role,
                "render_mode": render_mode,
                "status": "rendered",
                "title": title,
            }
        )

    return engine_input, manifest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render engine-compatible slides from a slide_plan.json into SVG files."
    )
    parser.add_argument("input_json", help="Path to slide_plan.json or engine deck JSON")
    parser.add_argument(
        "-o",
        "--output-dir",
        default="out/bento_svg",
        help="Directory for compiled.json, audit.json, manifest.json, and slides/",
    )
    parser.add_argument(
        "--engine",
        default=str(Path(__file__).with_name("bento_engine_v361_rhythm.py")),
        help="Path to the Bento engine Python file",
    )
    args = parser.parse_args()

    input_path = Path(args.input_json).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    engine_path = Path(args.engine).expanduser().resolve()

    payload = load_json(input_path)
    slides = normalize_slides(payload)
    engine_input, manifest = build_engine_input(slides)

    rendered = [item for item in manifest if item["status"] == "rendered"]
    if not rendered:
        print("No engine-compatible slides were found in the input.", file=sys.stderr)
        return 1

    engine_module = load_engine(engine_path)
    engine = engine_module.BentoEngineV361()
    compiled, svgs, audit = engine.build(engine_input)

    output_dir.mkdir(parents=True, exist_ok=True)
    slides_dir = output_dir / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)

    rendered_iter = iter(rendered)
    compiled_out = []
    audit_out = []

    for compiled_slide, svg, audit_slide in zip(compiled, svgs, audit):
        source = next(rendered_iter)
        slide_number = int(source["slide_number"])

        enriched_compiled = {
            "source_slide_number": slide_number,
            "page_role": source["page_role"],
            **compiled_slide,
        }
        enriched_audit = {
            "source_slide_number": slide_number,
            "page_role": source["page_role"],
            **audit_slide,
        }

        compiled_out.append(enriched_compiled)
        audit_out.append(enriched_audit)
        (slides_dir / f"slide{slide_number:02d}.svg").write_text(svg, encoding="utf-8")

    dump_json(output_dir / "compiled.json", compiled_out)
    dump_json(output_dir / "audit.json", audit_out)
    dump_json(output_dir / "manifest.json", manifest)

    print(
        json.dumps(
            {
                "input": str(input_path),
                "output_dir": str(output_dir),
                "rendered_count": len(rendered),
                "skipped_count": len([item for item in manifest if item["status"] == "skipped"]),
                "slides_dir": str(slides_dir),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
