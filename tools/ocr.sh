#!/bin/bash
# OCR a scanned document on grid's GPU (marker + surya on the Quadro GV100).
#
#   tools/ocr.sh <file.pdf|image> [output-dir]
#
# Writes <name>/<name>.md (plus any extracted figures) under the output
# directory — the input's own directory by default — and prints the path to
# the markdown. Use it when a primary text exists only as a raw scan: OCR it
# here rather than settling for a source you cannot quote. First run loads
# ~3 GB of model weights into the GPU; a 300-page book takes some minutes.
# The models read antique typefaces well, but quote-check the long s (f/s)
# against the page image as the brief says.
set -euo pipefail
HERE=$(cd "$(dirname "$0")/.." && pwd)
VENV="$HERE/.ocr-venv"
[ -x "$VENV/bin/marker_single" ] || { echo "no OCR environment at $VENV (see README, Development)" >&2; exit 1; }
[ $# -ge 1 ] || { echo "usage: ocr.sh <file.pdf|image> [output-dir]" >&2; exit 1; }
IN=$(readlink -f "$1")
OUT=${2:-$(dirname "$IN")}
"$VENV/bin/marker_single" "$IN" --output_dir "$OUT" --output_format markdown >&2
base=$(basename "${IN%.*}")
md=$(find "$OUT/$base" -name '*.md' | head -1)
[ -n "$md" ] || { echo "marker produced no markdown under $OUT/$base" >&2; exit 1; }
echo "$md"
