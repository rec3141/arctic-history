#!/bin/bash
# heads.sh <pdf> <out.png> <leaves> - crop the top band of each leaf so the
# printed running-head page number can be read for a whole batch at once.
set -e
PDF="$1"; OUT="$2"; LEAVES="$3"
TMP=$(mktemp -d); i=0
for p in ${LEAVES//,/ }; do
  i=$((i+1)); f="$TMP/$(printf %03d $i)"
  pdftoppm -png -r 130 -f "$p" -l "$p" -singlefile "$PDF" "$f" 2>/dev/null
  convert "$f.png" -gravity north -crop 100%x20%+0+0 +repage -resize 900x \
    -background white -gravity west -splice 110x0 \
    -pointsize 26 -fill black -annotate +4+0 "L$p" "$f.png"
done
montage "$TMP"/*.png -tile 1x -geometry +2+2 -background gray80 "$OUT"
rm -rf "$TMP"; echo "$OUT"
