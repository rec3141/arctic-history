#!/bin/bash
# reg.sh <id-num> <ia-id> <leaf> <topic> <fileprefix> <slug> <type> <title> <pages> <lat> <lon> <desc> <tags>
set -e
N=$1; IA=$2; L=$3; TOPIC=$4; PFX=$5; SLUG=$6; TYPE=$7; TITLE=$8; PAGES=$9; LAT=${10}; LON=${11}; DESC=${12}; TAGS=${13}
SRC=image-sweep-c-scratch/full/$IA/n$L.jpg
DST=db/history/$TOPIC/files/$PFX-l$(printf %03d $L)-$SLUG.jpg
cp -n "$SRC" "$DST"
/usr/bin/python3 tools/history-db.py artifact --id "$TOPIC-$N" --topic "$TOPIC" --type "$TYPE" \
  --title "$TITLE" --bibkey "$BIBKEY" --credit "$CREDIT" --licence "public domain" \
  --pages "$PAGES" --lat "$LAT" --lon "$LON" --description "$DESC" \
  --local-file "$TOPIC/files/$(basename $DST)" --source-url "https://archive.org/details/$IA" \
  --date "$DATE" --creator "$CREATOR" --tags "$TAGS" ${14:+--people} ${14:+"${14}"}
