#!/usr/bin/env python3
import sys
sys.path.insert(0, 'relocations-qtc-scratch/review')
from find import find

CASES = [
 # qausuittuq page
 ('qau-qarnartakuj','qtc-resolute','qarnartakuj'),
 ('qau-nodawn','qtc-resolute','place with no dawn'),
 ('qau-1947station','qtc-resolute','1947'),
 ('qau-winterharbour','qtc-resolute','winter harbour'),
 ('qau-rcaf1949','qtc-resolute','1949'),
 ('qau-atlas1962','qtc-resolute','atlas aviation'),
 ('qau-8km','qtc-resolute','eight kilometres'),
 ('qau-outofbounds','qtc-resolute','out of bounds'),
 ('qau-gameact1917','qtc-resolute','northwest game act'),
 ('qau-preserve1926','qtc-resolute','arctic islands game preserve'),
 ('qau-gibson','qtc-resolute','ross gibson'),
 ('qau-thousanddollars','qtc-resolute','worth of goods'),
 ('qau-echalook','qtc-resolute','echalook'),
 ('qau-kudloo','qtc-resolute','kudloo'),
 ('qau-nungak','qtc-resolute','nungak'),
 ('qau-threehouses','qtc-resolute','three houses'),
 ('qau-eleven','qtc-resolute','eleven houses'),
 ('qau-fourteen','qtc-resolute','fourteen'),
 ('qau-eighteen','qtc-resolute','eighteen'),
 ('qau-kuvinajuq','qtc-resolute','kuvinajuq'),
 ('qau-coop1960','qtc-resolute','co-operative'),
 ('qau-fourmen1960','qtc-resolute','four men'),
 ('qau-ninejobs','qtc-resolute','nine permanent full-time positions'),
 ('qau-canteen1961','qtc-resolute','canteen'),
 ('qau-measles1957','qtc-resolute','measles'),
 ('qau-100qimmiit','qtc-resolute','qimmiit'),
 ('qau-rabies','qtc-resolute','rabies'),
 ('qau-damas','qtc-resolute','damas'),
 ('qau-1959ordinance','qtc-resolute','ordinance'),
 ('qau-southcamp','qtc-resolute','south camp'),
 ('qau-erskine','qtc-resolute','erskine'),
 ('qau-1975move','qtc-resolute','1975'),
 ('qau-ludypudluk','qtc-resolute','ludy pudluk'),
 ('qau-polaris','qtc-resolute','polaris'),
 ('qau-pcsp','qtc-resolute','polar continental shelf'),
 ('qau-chretien','qtc-resolute','chretien'),
 ('qau-camsell','qtc-resolute','camsell'),
 ('qau-1961ausuittuq','qtc-grise','1961'),
]

for label, only, phrase in CASES:
    h = find(phrase, only)
    print(f'{label:22} {len(h):3} hits')
