#!/bin/bash
# sheet.sh <pdf> <out.png> <comma-separated leaves> [tile] [size]
# Renders each leaf small and montages them with the leaf number under each,
# so a whole book's candidate plates can be identified in one look.
set -e
PDF="$1"; OUT="$2"; LEAVES="$3"; TILE="${4:-5x}"; SIZE="${5:-260}"
TMP=$(mktemp -d); i=0
for p in ${LEAVES//,/ }; do
  i=$((i+1))
  pdftoppm -png -r 40 -f "$p" -l "$p" -singlefile "$PDF" "$TMP/$(printf %03d $i)" 2>/dev/null
  convert "$TMP/$(printf %03d $i).png" -resize ${SIZE}x${SIZE} \
    -background white -gravity south -splice 0x16 \
    -pointsize 13 -fill black -annotate +0+1 "leaf $p" \
    "$TMP/$(printf %03d $i).png"
done
montage "$TMP"/*.png -tile "$TILE" -geometry +3+3 -background gray85 "$OUT"
rm -rf "$TMP"
echo "$OUT"
