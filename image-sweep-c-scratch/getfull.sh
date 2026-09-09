#!/bin/bash
# getfull.sh <ia-id> <comma-leaves>
ID=$1; L=$2
mkdir -p full/$ID
echo ${L//,/ } | tr ' ' '\n' | xargs -P4 -I{} sh -c 'f=full/'"$ID"'/n{}.jpg; [ -s "$f" ] || curl -sL -o "$f" "https://archive.org/download/'"$ID"'/page/n{}.jpg"'
find full/$ID -size -20k -delete
ls full/$ID | wc -l
