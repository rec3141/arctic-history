#!/bin/bash
# pair.sh <id> <comma-leaves> <out>
ID=$1; L=$2; OUT=$3
TMP=$(mktemp -d); i=0
for p in ${L//,/ }; do
  i=$((i+1)); f="full/$ID/n$p.jpg"; [ -s "$f" ] || continue
  convert "$f" -resize 950x -background white -gravity north -splice 0x30 \
    -pointsize 26 -fill red -annotate +0+2 "leaf $p" "$TMP/$(printf %03d $i).png"
done
montage "$TMP"/*.png -tile 2x1 -geometry +3+3 -background gray60 "$OUT"
rm -rf "$TMP"; identify "$OUT"
