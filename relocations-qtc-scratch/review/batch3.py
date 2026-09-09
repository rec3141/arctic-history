#!/usr/bin/env python3
import sys
sys.path.insert(0, 'relocations-qtc-scratch/review')
from find import find, NORM, norm

CASES = [
 ('qim-count','qimmiit','20,000'),
 ('qim-count2','qimmiit','a few dozen'),
 ('qim-names','qimmiit','individual names'),
 ('qim-apex','qimmiit','apex'),
 ('qim-niaqunngut','qimmiit','niaqunngut'),
 ('qim-1962epi','qimmiit','hepatitis'),
 ('qim-400','qimmiit','four hundred'),
 ('qim-ukkalianuk','qimmiit','ukkalianuk'),
 ('qim-uttak','qimmiit','uttak'),
 ('qim-makivik1999','qimmiit','1999'),
 ('qim-bottom','qimmiit','get to the bottom of the matter'),
 ('qim-april2005','qimmiit','april 2005'),
 ('qim-rcmptitle','qimmiit','the rcmp and the inuit sled dogs'),
 ('qim-1966machine','qimmiit','1966'),
 ('qim-conspiracy','rcmpsleddog','no conspiracy'),
 ('tb-1945','healthcare','1945'),
 ('tb-1922','healthcare','1922'),
 ('tb-1946','healthcare','1946'),
 ('tb-58crew','healthcare','fifty-eight'),
 ('tb-30pass','healthcare','thirty inuit'),
 ('tb-helicopter','healthcare','helicopter'),
 ('tb-1000','healthcare','almost a thousand'),
 ('tb-20months','healthcare','twenty months'),
 ('tb-1in7','healthcare','one in seven'),
 ('tb-nov1964','healthcare','november 1964'),
 ('tb-1969charter','healthcare','1969'),
 ('tb-nascopie1947','healthcare','nascopie'),
 ('tb-marsh','healthcare','marsh'),
 ('tb-mountain','healthcare','mountain sanatorium'),
 ('set-hundred','nuutauniq','more than a hundred'),
 ('set-5to30','nuutauniq','five to thirty'),
 ('set-13settle','nuutauniq','thirteen'),
 ('set-kuptana','nuutauniq','kuptana'),
 ('set-rheaume','nuutauniq','rheaume'),
 ('sai-2007','finalreport','2007'),
 ('sai-igloliorte','finalreport','igloliorte'),
 ('sai-redfern','finalreport','redfern'),
 ('sai-350','finalreport','350'),
 ('sai-mandate','finalreport','mandate'),
 ('sai-excluded','finalreport','excluded'),
 ('sai-25rec','finalreport','twenty-five'),
 ('sai-poll','finalreport','2009'),
 ('sai-53','finalreport','53%'),
 ('sai-thematic','finalreport','thematic'),
]
for label, only, phrase in CASES:
    h = find(phrase, only)
    print(f'{label:18} {len(h):3}')
