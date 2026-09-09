#!/bin/bash
# usage: makesheet.sh <ID> <sheetidx> <start> <end(inclusive)>
set -e
ID=$1
IDX=$2
START=$3
END=$4
cd /data/dev/arctic-history/image-sweep-c-scratch/sverdrup
ARGS=()
for n in $(seq "$START" "$END"); do
  f="thumbs/$ID/n$n.jpg"
  if [ -s "$f" ]; then
    ARGS+=(-label "$n" "$f")
  fi
done
montage "${ARGS[@]}" -tile 11x10 -geometry 150x+2+2 -background white -pointsize 16 "sheets/${ID}-${IDX}.jpg"
mogrify -resize 1400x "sheets/${ID}-${IDX}.jpg"
echo "wrote sheets/${ID}-${IDX}.jpg"
