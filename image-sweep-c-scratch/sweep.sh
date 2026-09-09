#!/bin/bash
# usage: sweep.sh <ia-id> <nleaves>
ID=$1; N=$2
mkdir -p thumbs/$ID
seq 0 $((N-1)) | xargs -P4 -I{} sh -c 'f=thumbs/'"$ID"'/n{}.jpg; [ -s "$f" ] || curl -sL -o "$f" "https://archive.org/download/'"$ID"'/page/n{}_w150.jpg"' 
find thumbs/$ID -size -2k -delete
echo "got $(ls thumbs/$ID | wc -l) of $N"
