#!/bin/bash
# caps.sh <pdf> <out.png> <leaves> [band]
# Crop the LOWER band of each leaf, where an engraved plate carries its title,
# so a batch of plates can be captioned from one look.
set -e
PDF="$1"; OUT="$2"; LEAVES="$3"; BAND="${4:-22}"
TMP=$(mktemp -d); i=0
for p in ${LEAVES//,/ }; do
  i=$((i+1)); f="$TMP/$(printf %03d $i)"
  pdftoppm -png -r 150 -f "$p" -l "$p" -singlefile "$PDF" "$f" 2>/dev/null
  convert "$f.png" -gravity south -crop 100%x${BAND}%+0+0 +repage \
    -resize 1300x \
    -background white -gravity west -splice 100x0 \
    -pointsize 24 -fill black -annotate +4+0 "L$p" "$f.png"
done
montage "$TMP"/*.png -tile 1x -geometry +2+2 -background gray80 "$OUT"
rm -rf "$TMP"; echo "$OUT"
