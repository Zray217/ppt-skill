#!/bin/bash
# SVG to PPTX converter wrapper
# Usage: bash svg_to_pptx.sh output.pptx slide1.svg slide2.svg ...

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <output.pptx> <slide1.svg> [slide2.svg ...]"
    exit 1
fi

OUTPUT="$1"
shift
SVG_FILES=("$@")

# Check dependencies
if ! command -v rsvg-convert &>/dev/null && ! command -v sips &>/dev/null; then
    if ! python3 -c "import cairosvg" 2>/dev/null; then
        echo "WARNING: No SVG rasterizer found."
        echo "Install rsvg-convert, or fix cairosvg/cairo."
        echo "Proceeding with fallback mode..."
    fi
fi

# Check python-pptx
if ! python3 -c "import pptx" 2>/dev/null; then
    echo "Installing python-pptx..."
    pip install python-pptx -q
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/svg_to_pptx.py" "$OUTPUT" "${SVG_FILES[@]}"
