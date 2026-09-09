#!/bin/bash
# foot2b.sh <pdf> <out.png> <leaves> - crop a taller bottom band (22%)
set -e
PDF="$1"; OUT="$2"; LEAVES="$3"
TMP=$(mktemp -d); i=0
for p in ${LEAVES//,/ }; do
  i=$((i+1)); f="$TMP/$(printf %03d $i)"
  pdftoppm -png -r 200 -f "$p" -l "$p" -singlefile "$PDF" "$f" 2>/dev/null
  convert "$f.png" -gravity south -crop 100%x22%+0+0 +repage -resize 1100x \
    -background white -gravity west -splice 110x0 \
    -pointsize 30 -fill black -annotate +4+0 "L$p" "$f.png"
done
montage "$TMP"/*.png -tile 1x -geometry +2+2 -background gray80 "$OUT"
rm -rf "$TMP"; echo "$OUT"
