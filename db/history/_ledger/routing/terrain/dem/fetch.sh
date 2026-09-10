#!/bin/bash
# GLO-90 tiles from the public Copernicus DEM bucket, once each
cd /data/gis/dem/glo90
xargs -P 8 -I{} sh -c 'f={}.tif; if [ ! -s "$f" ]; then curl -sS -f -o "$f.part" "https://copernicus-dem-90m.s3.amazonaws.com/{}/{}.tif" && mv -f "$f.part" "$f" || echo "FAIL {}"; fi' < ../wanted.txt
echo done
