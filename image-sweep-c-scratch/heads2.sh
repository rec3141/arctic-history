#!/bin/bash
ID=$1; L=$2; OUT=$3
TMP=$(mktemp -d); i=0
for p in ${L//,/ }; do
  i=$((i+1)); f="full/$ID/n$p.jpg"; [ -s "$f" ] || continue
  convert "$f" -crop 3000x260+0+150 +repage -resize 900x -background white -gravity west -splice 90x0 -pointsize 26 -fill black -annotate +4+0 "L$p" "$TMP/$(printf %03d $i).png"
done
montage "$TMP"/*.png -tile 1x -geometry +1+1 -background gray70 "$OUT"
rm -rf "$TMP"; identify "$OUT"
