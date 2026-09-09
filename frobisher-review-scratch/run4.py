import sys
sys.path.insert(0, '/data/dev/arctic-history/frobisher-review-scratch')
from verify2 import check

Q = [
 ('bit tongue', "bit his tong in twaine within his mouth", ['coll']),
 ('crow embalm', "William Crow", ['chesh']),
 ('de heere', "de Heere", ['chesh']),
 ('adams ducke', "he would hit a ducke at a good distance of", ['chesh']),
 ('adams linen', "no linen or woolle at all", ['chesh']),
 ('colston', "Colston", ['chesh']),
 ('nutaaq months', "fourteen", ['chesh']),
 ('three swans', "Three Swans", ['chesh']),
 ('gymblet', "Iohn gymblet surgione", ['chesh']),
 ('cheshire capture date', "at the very end of July or beginning of August", ['chesh']),
 ('conger trick', "showed his companion", ['chesh']),
 ('dodding date', "Bristol, November 8th", ['chesh']),
]
for lab, ph, keys in Q:
    check(lab, ph, keys)
