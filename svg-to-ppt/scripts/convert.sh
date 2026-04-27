#!/bin/bash
# SVG → PPTX 转换 CLI
# Usage: ./convert.sh output.pptx input1.svg [input2.svg ...]

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 output.pptx input1.svg [input2.svg ...]"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONVERTER="$SKILL_DIR/assets/converter/svg2pptx.py"

OUTPUT="$1"
shift

echo "🎨 SVG → PPTX Converter"
echo "  Output: $OUTPUT"
echo "  Inputs: $@"
echo ""

python3 "$CONVERTER" "$OUTPUT" "$@"

echo ""
echo "Done! Open $OUTPUT in PowerPoint/Keynote/WPS."
