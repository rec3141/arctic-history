# Routing the overland tracks through the terrain

2026-09-11 00:15 — 3 tracks routed in 117 s, 111 on file from this and earlier runs. Command: `python tools/digitize-tracks.py route --track franklin-search-068 --track ross-victory-003 --track karluk-cae-007 --write`

**Written to the database.**

## The DEM

Copernicus GLO-90, mosaicked at 250 m in `+proj=stere +lat_0=90 +lat_ts=78 +lon_0=-85 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs` (24610 x 13326 cells), with land from GSHHG full resolution and ice from Natural Earth 10 m glaciated areas.  See the tool's docstring for the cost surface.

## The maps

| map | family | parameters | points | rms px | rms km | worst px | km/px | fit |
|---|---|---|---|---|---|---|---|---|
| cook-1908-axel-heiberg-041 | lcc | {'lat1': 75.6126890507451, 'lat2': 84.95929418681087} | 34 | 3.6 | 2.8 | 9.5 | 0.78 | accepted |
| crocker-land-1913-022 | stere | {} | 42 | 43.1 | 97.4 | 176.1 | 2.26 | REFUSED |
| haig-thomas-1937-059 | bonne | {'lat1': 60.56384926503213} | 14 | 8.0 | 6.0 | 16.8 | 0.74 | accepted |
| kane-hall-polaris-193 | eqdc | {'lat1': 72.17007859967072, 'lat2': 72.1949133911055} | 14 | 0.9 | 0.3 | 2.1 | 0.35 | accepted |
| kruger-1930-006 | eqdc | {'lat1': 45.917832300527515, 'lat2': 86.74590117145988} | 18 | 3.0 | 1.5 | 7.8 | 0.50 | accepted |
| nares-greely-154 | stere | {} | 11 | 1.7 | 0.1 | 4.1 | 0.07 | accepted |
| nares-greely-171 | stere | {} | 41 | 1.1 | 0.5 | 2.6 | 0.42 | accepted |
| oxford-ellesmere-1934-005 | aea | {'lat1': 68.40614281251455, 'lat2': 87.02213440308128} | 12 | 1.6 | 1.0 | 3.0 | 0.58 | accepted |
| oxford-ellesmere-1934-073 | aea | {'lat1': 46.435934154214266, 'lat2': 89.89999781130844} | 16 | 6.5 | 8.5 | 17.2 | 1.31 | accepted |
| sverdrup-bernier-peary-064 | laea | {} | 15 | 0.2 | 0.0 | 0.4 | 0.09 | accepted |

Maps in the candidate list with no track digitized from them: **kruger-1930-006**: Barr's locator map of the search area: georeferenced (3 px), but it draws no route at all, only coasts, names and the two posts, so there is nothing on it to digitize.; **kruger-1930-027**: Krüger's own sketch of the route he intended, not the one he took: nothing to route.; **kruger-1930-061**: the 1957 Geological Survey sledge journey to Meighen Island has no track artifact yet.; **nares-greely-154**: Lockwood's chart of the north Greenland coast: georeferenced against its own coast to 1.7 px (0.1 km), but its route is a hairline strung between small numbered camp circles and the whole sheet is dense hachured relief.  The hachure strokes are a dash's size and a dot's, so the morphology returns 7,000 of them and none of the route; skeletonizing the sheet instead gives 61,000 fragments and the chain runs up Mascart Inlet through the shading.  The sheet also covers only the last of the five legs (Cape Britannia to Lockwood Island), so even a clean extraction would leave the track short of the half the grade asks for.  nares-greely-023 is routed from its waypoints alone.; **nares-greely-204**: Lockwood's chart of his March to April 1883 journey north from Fort Conger; the only 1883 track in the database is the August retreat (nares-greely-025), which this map does not show.; **sverdrup-bernier-peary-154**: the Falcon's 1893 voyage to Bowdoin Bay is a ship's track, the sea router's.


## The grades

- **recommend** — every leg routed inside the DEM, and where a printed map was digitized at least half the legs follow its ink: a line to write back once the owner has looked at it.
- **review** — some legs fall outside the DEM (great circles there, which is right over the sea ice) or fewer than half follow the ink.
- **same** — the routed line is the database's line to within 3 km: nothing to write back.
- **outside** — every leg outside the DEM: not this tool's track.
- **written** — already in the database with this line, flagged terrain.

outside: 1 · recommend: 31 · review: 28 · same: 6 · written: 45

## Every track

| track | grade | legs | from ink | routed km | straight km | land km | ice km | highest m | from db line, max km | moved | s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cook-1908-axel-heiberg-001 | written | 12 | 6 | 680 | 593 | 137 | 0 | 991 | 0 | 0 | 0.3 |
| cook-1908-axel-heiberg-002 | written | 10 | 10 | 950 | 798 | 331 | 6 | 434 | 1 | 0 | 0.7 |
| cook-1908-axel-heiberg-003 | written | 5 | 0 | 541 | 486 | 1 | 0 | 45 | 0 | 0 | 0.5 |
| crocker-land-1913-002 | written | 30 | 0 | 2,214 | 1,907 | 310 | 115 | 1473 | 0 | 0 | 3.1 |
| crocker-land-1913-003 | written | 28 | 0 | 1,824 | 1,421 | 554 | 3 | 855 | 0 | 0 | 1.0 |
| franklin-search-021 | written | 6 | 0 | 1,222 | 1,091 | 87 | 0 | 171 | 0 | 0 | 2.3 |
| franklin-search-067 | written | 6 | 0 | 425 | 353 | 22 | 0 | 212 | 0 | 0 | 0.4 |
| franklin-search-082 | written | 14 | 0 | 1,227 | 1,100 | 216 | 0 | 310 | 0 | 0 | 1.1 |
| franklin-search-086 | written | 13 | 0 | 572 | 443 | 145 | 0 | 333 | 0 | 0 | 0.3 |
| greenland-inughuit-017 | written | 6 | 0 | 815 | 604 | 223 | 31 | 473 | 0 | 0 | 1.4 |
| greenland-inughuit-042 | written | 9 | 0 | 1,482 | 1,247 | 161 | 22 | 893 | 0 | 0 | 2.6 |
| haig-thomas-1937-001 | written | 24 | 24 | 1,609 | 1,366 | 385 | 134 | 1842 | 1 | 2 | 0.7 |
| haig-thomas-1937-002 | written | 20 | 0 | 1,050 | 883 | 58 | 48 | 492 | 0 | 0 | 0.7 |
| kruger-1930-001 | written | 21 | 0 | 1,484 | 1,262 | 163 | 7 | 600 | 0 | 0 | 1.0 |
| kruger-1930-002 | written | 7 | 0 | 1,079 | 857 | 66 | 0 | 563 | 0 | 0 | 1.1 |
| kruger-1930-003 | written | 22 | 0 | 1,617 | 1,367 | 196 | 3 | 433 | 0 | 0 | 1.3 |
| kruger-1930-004 | written | 19 | 0 | 1,312 | 1,080 | 222 | 31 | 473 | 0 | 0 | 0.9 |
| kruger-1930-005 | written | 5 | 0 | 284 | 208 | 56 | 10 | 657 | 0 | 0 | 0.1 |
| mcclure-investigator-009 | written | 31 | 0 | 1,365 | 1,149 | 397 | 0 | 235 | 0 | 0 | 0.8 |
| mcclure-investigator-010 | written | 23 | 0 | 1,457 | 1,277 | 269 | 0 | 227 | 0 | 0 | 1.2 |
| mcclure-investigator-011 | written | 8 | 0 | 626 | 550 | 89 | 0 | 215 | 0 | 0 | 0.8 |
| mcclure-investigator-013 | written | 5 | 0 | 330 | 304 | 27 | 0 | 211 | 0 | 0 | 0.4 |
| nares-greely-022 | written | 5 | 4 | 237 | 213 | 0 | 0 | 0 | 0 | 0 | 0.1 |
| nares-greely-025 | written | 9 | 0 | 526 | 416 | 15 | 0 | 965 | 0 | 0 | 0.6 |
| nares-greely-038 | written | 24 | 16 | 1,024 | 786 | 416 | 17 | 617 | 3 | 0 | 0.7 |
| nares-greely-039 | written | 24 | 13 | 662 | 584 | 78 | 3 | 774 | 2 | 0 | 0.4 |
| operation-hazen-1957-041 | written | 6 | 0 | 661 | 617 | 72 | 0 | 28 | 0 | 0 | 1.0 |
| operation-hazen-1957-042 | written | 9 | 0 | 511 | 445 | 48 | 1 | 395 | 2 | 0 | 0.4 |
| oxford-ellesmere-1934-002 | written | 21 | 18 | 1,685 | 1,304 | 478 | 162 | 1798 | 0 | 0 | 0.9 |
| oxford-ellesmere-1934-003 | written | 28 | 27 | 1,498 | 1,214 | 516 | 82 | 1111 | 1 | 0 | 0.7 |
| oxford-ellesmere-1934-004 | written | 26 | 17 | 890 | 724 | 94 | 6 | 747 | 0 | 0 | 0.4 |
| pole-seekers-from-ellesmere-030 | written | 7 | 0 | 416 | 339 | 54 | 1 | 306 | 2 | 0 | 0.3 |
| pole-seekers-from-ellesmere-031 | written | 5 | 0 | 131 | 115 | 85 | 1 | 87 | 0 | 0 | 0.1 |
| rcmp-high-arctic-patrols-003 | written | 20 | 10 | 1,874 | 1,575 | 683 | 143 | 1505 | 0 | 0 | 1.2 |
| rcmp-high-arctic-patrols-005 | written | 7 | 4 | 952 | 712 | 103 | 99 | 1235 | 0 | 0 | 0.9 |
| rcmp-high-arctic-patrols-006 | written | 14 | 7 | 1,325 | 1,064 | 513 | 150 | 1505 | 0 | 0 | 0.9 |
| rcmp-high-arctic-patrols-008 | written | 11 | 8 | 1,369 | 1,029 | 390 | 156 | 1235 | 3 | 0 | 0.8 |
| rcmp-high-arctic-patrols-009 | written | 4 | 3 | 850 | 753 | 98 | 0 | 285 | 1 | 0 | 1.1 |
| rcmp-high-arctic-patrols-010 | written | 11 | 6 | 1,286 | 944 | 34 | 23 | 705 | 0 | 0 | 0.9 |
| sverdrup-bernier-peary-003 | written | 16 | 0 | 1,467 | 1,275 | 521 | 0 | 457 | 0 | 0 | 2.0 |
| sverdrup-bernier-peary-178 | written | 8 | 0 | 691 | 621 | 3 | 0 | 96 | 0 | 0 | 1.1 |
| sverdrup-bernier-peary-180 | written | 27 | 0 | 1,611 | 1,402 | 19 | 0 | 464 | 0 | 0 | 2.2 |
| sverdrup-bernier-peary-194 | written | 18 | 0 | 1,417 | 1,156 | 504 | 15 | 283 | 0 | 0 | 1.3 |
| sverdrup-bernier-peary-302 | written | 40 | 0 | 1,770 | 1,402 | 304 | 0 | 392 | 0 | 0 | 1.1 |
| sverdrup-bernier-peary-304 | written | 33 | 0 | 1,680 | 1,425 | 389 | 21 | 794 | 0 | 0 | 1.5 |
| amundsen-gjoa-002 | recommend | 7 | 0 | 1,566 | 1,288 | 1,548 | 0 | 716 | 53 | 0 | 3.0 |
| crocker-land-1913-004 | recommend | 26 | 0 | 2,373 | 1,738 | 657 | 68 | 1487 | 60 | 0 | 2.0 |
| franklin-search-022 | recommend | 7 | 0 | 626 | 576 | 62 | 0 | 171 | 11 | 0 | 1.1 |
| franklin-search-027 | recommend | 15 | 0 | 1,121 | 1,029 | 269 | 0 | 286 | 23 | 0 | 1.1 |
| greenland-inughuit-016 | recommend | 9 | 0 | 1,446 | 1,188 | 426 | 193 | 1548 | 36 | 0 | 2.5 |
| greenland-inughuit-043 | recommend | 14 | 0 | 2,071 | 1,545 | 499 | 56 | 554 | 64 | 2 | 2.2 |
| greenland-inughuit-045 | recommend | 13 | 0 | 7,278 | 6,528 | 2,678 | 0 | 603 | 133 | 0 | 27.1 |
| hudson-strait-south-baffin-015 | recommend | 8 | 0 | 577 | 535 | 3 | 0 | 94 | 12 | 0 | 0.5 |
| inuit-oral-history-029 | recommend | 8 | 0 | 619 | 554 | 118 | 0 | 272 | 29 | 0 | 0.4 |
| inuit-oral-history-030 | recommend | 6 | 0 | 505 | 461 | 189 | 0 | 141 | 7 | 0 | 0.4 |
| kane-hall-polaris-002 | recommend | 12 | 0 | 1,006 | 929 | 62 | 8 | 397 | 3 | 0 | 1.1 |
| karluk-cae-002 | recommend | 14 | 0 | 1,205 | 1,138 | 121 | 0 | 53 | 15 | 0 | 2.8 |
| karluk-cae-003 | recommend | 17 | 0 | 2,068 | 1,953 | 463 | 0 | 224 | 14 | 0 | 4.9 |
| karluk-cae-004 | recommend | 24 | 0 | 2,652 | 2,404 | 487 | 0 | 295 | 47 | 0 | 3.9 |
| karluk-cae-008 | recommend | 24 | 0 | 2,401 | 2,192 | 588 | 0 | 167 | 49 | 0 | 4.7 |
| mcclure-investigator-006 | recommend | 12 | 0 | 750 | 583 | 239 | 0 | 369 | 25 | 0 | 0.6 |
| mcclure-investigator-007 | recommend | 5 | 0 | 634 | 571 | 39 | 0 | 343 | 24 | 0 | 1.2 |
| mcclure-investigator-008 | recommend | 4 | 0 | 320 | 288 | 134 | 0 | 343 | 24 | 0 | 0.2 |
| mcclure-investigator-054 | recommend | 3 | 0 | 252 | 227 | 122 | 0 | 343 | 25 | 0 | 0.2 |
| nares-greely-023 | recommend | 5 | 0 | 897 | 790 | 49 | 0 | 823 | 27 | 0 | 1.3 |
| pole-seekers-from-ellesmere-007 | recommend | 6 | 0 | 1,179 | 1,096 | 3 | 0 | 283 | 29 | 0 | 2.8 |
| rock-and-the-sverdrup-basin-701 | recommend | 19 | 0 | 1,349 | 1,129 | 232 | 5 | 594 | 24 | 0 | 1.1 |
| rock-and-the-sverdrup-basin-702 | recommend | 5 | 0 | 294 | 259 | 121 | 0 | 560 | 12 | 0 | 0.2 |
| ross-victory-002 | recommend | 6 | 0 | 247 | 219 | 114 | 0 | 98 | 21 | 0 | 0.2 |
| science-stations-029 | recommend | 4 | 0 | 2,084 | 2,037 | 0 | 0 | 0 | 174 | 0 | 7.9 |
| sverdrup-bernier-peary-179 | recommend | 31 | 0 | 2,012 | 1,810 | 159 | 1 | 886 | 16 | 0 | 2.3 |
| sverdrup-bernier-peary-183 | recommend | 13 | 0 | 1,264 | 1,104 | 517 | 0 | 342 | 42 | 0 | 1.7 |
| sverdrup-bernier-peary-193 | recommend | 11 | 0 | 1,340 | 1,181 | 40 | 0 | 663 | 38 | 0 | 2.3 |
| sverdrup-bernier-peary-303 | recommend | 39 | 0 | 1,586 | 1,151 | 488 | 0 | 783 | 22 | 0 | 1.0 |
| thule-dorset-001 | recommend | 9 | 0 | 5,315 | 4,434 | 3,251 | 0 | 327 | 144 | 0 | 14.3 |
| wrecks-disasters-038 | recommend | 5 | 0 | 1,658 | 1,502 | 5 | 0 | 450 | 100 | 0 | 4.1 |
| franklin-search-023 | review | 25 | 0 | 6,578 | 11,702 | 323 | 0 | 284 | 260 | 0 | 46.2 |
| franklin-search-068 | review | 22 | 0 | 3,245 | 9,698 | 2,800 | 0 | 492 | 560 | 0 | 9.0 |
| franklin-search-136 | review | 40 | 0 | 6,325 | 12,253 | 804 | 0 | 557 | 198 | 0 | 13.8 |
| ice-shelves-and-ice-islands-004 | review | 20 | 0 | 3,151 | 7,384 | 83 | 0 | 258 | 276 | 0 | 8.7 |
| ice-shelves-and-ice-islands-006 | review | 5 | 0 | 837 | 3,733 | 0 | 0 | 0 | 568 | 0 | 2.0 |
| kane-hall-polaris-035 | review | 27 | 0 | 2,721 | 3,216 | 91 | 3 | 344 | 40 | 0 | 5.5 |
| kane-hall-polaris-263 | review | 18 | 14 | 584 | 495 | 4 | 0 | 391 | 22 | 0 | 0.3 |
| karluk-cae-006 | review | 7 | 0 | 839 | 1,768 | 46 | 0 | 21 | 14 | 0 | 1.8 |
| karluk-cae-007 | review | 19 | 0 | 7,147 | 10,103 | 3,530 | 0 | 603 | 1141 | 0 | 23.8 |
| mcclure-investigator-014 | review | 4 | 0 | 1,768 | 4,559 | 119 | 0 | 284 | 86 | 0 | 6.3 |
| operation-hazen-1957-026 | review | 11 | 0 | 2,119 | 4,674 | 105 | 0 | 640 | 246 | 0 | 9.6 |
| pole-seekers-from-ellesmere-006 | review | 10 | 0 | 708 | 1,670 | 0 | 0 | 26 | 12 | 0 | 0.7 |
| pole-seekers-from-ellesmere-038 | review | 5 | 0 | 851 | 2,015 | 6 | 1 | 146 | 457 | 0 | 1.5 |
| pole-seekers-from-ellesmere-039 | review | 6 | 0 | 601 | 2,476 | 14 | 0 | 31 | 522 | 0 | 0.7 |
| posts-rcmp-missions-023 | review | 17 | 7 | 925 | 745 | 130 | 0 | 407 | 41 | 0 | 0.4 |
| qei-from-the-air-1947-023 | review | 7 | 0 | 4,800 | 7,673 | 1,214 | 42 | 1639 | 1033 | 0 | 24.2 |
| qei-from-the-air-1947-024 | review | 10 | 0 | 4,573 | 13,866 | 3,850 | 747 | 2446 | 359 | 0 | 40.8 |
| rcmp-high-arctic-patrols-001 | review | 11 | 5 | 692 | 549 | 273 | 251 | 1909 | 28 | 0 | 0.3 |
| rcmp-high-arctic-patrols-002 | review | 16 | 7 | 1,478 | 1,110 | 327 | 10 | 655 | 45 | 0 | 1.0 |
| rcmp-high-arctic-patrols-004 | review | 13 | 5 | 998 | 776 | 3 | 0 | 85 | 53 | 0 | 0.7 |
| rcmp-high-arctic-patrols-007 | review | 16 | 7 | 2,359 | 2,093 | 677 | 85 | 1505 | 45 | 0 | 3.8 |
| ross-victory-003 | review | 16 | 0 | 2,339 | 5,538 | 50 | 0 | 286 | 849 | 0 | 9.6 |
| science-stations-003 | review | 7 | 0 | 986 | 3,292 | 0 | 0 | 0 | 23 | 0 | 2.1 |
| science-stations-073 | review | 5 | 0 | 974 | 4,697 | 613 | 33 | 929 | 191 | 0 | 2.0 |
| science-stations-074 | review | 5 | 0 | 254 | 4,066 | 219 | 140 | 1742 | 204 | 0 | 0.2 |
| sverdrup-bernier-peary-300 | review | 11 | 8 | 429 | 297 | 172 | 1 | 672 | 11 | 0 | 0.1 |
| sverdrup-bernier-peary-301 | review | 11 | 9 | 372 | 256 | 279 | 260 | 1625 | 18 | 0 | 0.2 |
| the-sea-ice-trk-002 | review | 11 | 0 | 2,695 | 2,830 | 8 | 0 | 37 | 14 | 0 | 10.5 |
| franklin-1845-002 | same | 4 | 0 | 227 | 216 | 21 | 0 | 20 | 1 | 0 | 0.2 |
| ice-shelves-and-ice-islands-005 | same | 4 | 0 | 99 | 93 | 22 | 1 | 37 | 3 | 0 | 0.1 |
| karluk-cae-005 | same | 11 | 0 | 1,179 | 1,109 | 3 | 0 | 1 | 3 | 0 | 2.3 |
| mcclure-investigator-012 | same | 5 | 0 | 217 | 206 | 0 | 0 | 0 | 1 | 0 | 0.2 |
| sverdrup-bernier-peary-035 | same | 5 | 0 | 560 | 1,532 | 0 | 0 | 1 | 0 | 0 | 1.2 |
| the-sea-ice-trk-001 | same | 10 | 0 | 1,589 | 1,511 | 0 | 0 | 0 | 0 | 0 | 3.7 |
| science-stations-030 | outside | 1 | 0 | 0 | 687 | 0 | 0 | 0 | 0 | 0 | 0.0 |

## Verdicts

- **cook-1908-axel-heiberg-001** (written) — Annoatok to Cape Stallworthy, February-March 1908  
  6 of 12 legs follow ink digitized from cook-1908-axel-heiberg-041 (georef rms 2.8 km), 1 chained through hachures or lettering and doubted; the routed line runs 2.6 km from the printed one on average; 680 km routed against 593 km straight, 137 km over land, 0 km over ice cap, highest 991 m; the line in the database is 640 km and 75 points; this one 75 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 5 (27 km straight, 50 routed); proposed moves, not applied: 11 (inferred; moved 23 km onto the printed route); it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **cook-1908-axel-heiberg-002** (written) — Back to land: Hassel Sound to Cape Sparbo, June-September 1908  
  10 of 10 legs follow ink digitized from cook-1908-axel-heiberg-041 (georef rms 2.8 km); the routed line runs 2.2 km from the printed one on average; 950 km routed against 798 km straight, 331 km over land, 6 km over ice cap, highest 434 m; the line in the database is 892 km and 110 points; this one 111 points; waypoints on land whose note names water: 5; proposed moves, not applied: 2 (inferred; moved 7 km onto the printed route); 5 (inferred; moved 9 km onto the printed route); 6 (inferred; moved 15 km onto the printed route); it runs 0.0 km from the line in the database on average and 1 km at most; this line is already in the database, flagged terrain
- **cook-1908-axel-heiberg-003** (written) — Cape Sparbo to Annoatok, February-April 1909  
  541 km routed against 486 km straight, 1 km over land, 0 km over ice cap, highest 45 m; the line in the database is 514 km and 38 points; this one 38 points; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **crocker-land-1913-002** (written) — The search for Crocker Land: Etah to 82 30 N and back, February to May 1914  
  2,214 km routed against 1,907 km straight, 310 km over land, 115 km over ice cap, highest 1473 m; the line in the database is 2,104 km and 200 points; this one 200 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 24 (209 km straight, 276 routed); waypoints on land whose note names water: 4, 6, 24, 29; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **crocker-land-1913-003** (written) — Ekblaw across Ellesmere and Grant Land, March to June 1915  
  1,824 km routed against 1,421 km straight, 554 km over land, 3 km over ice cap, highest 855 m; the line in the database is 1,713 km and 203 points; this one 203 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 13 (84 km straight, 109 routed); 14 (93 km straight, 191 routed); 15 (57 km straight, 106 routed); 16 (88 km straight, 119 routed); waypoints on land whose note names water: 8; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **franklin-search-021** (written) — McClintock's sledge journey to Melville Island, April-July 1851  
  1,222 km routed against 1,091 km straight, 87 km over land, 0 km over ice cap, highest 171 m; the line in the database is 1,149 km and 69 points; this one 69 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 4 (88 km straight, 121 routed); it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **franklin-search-067** (written) — Penny's dog-sledge journey to the head of Wellington Channel, May 1851  
  425 km routed against 353 km straight, 22 km over land, 0 km over ice cap, highest 212 m; the line in the database is 402 km and 34 points; this one 34 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 0 (54 km straight, 80 routed); it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **franklin-search-082** (written) — Commander Richards's sledge journey from Northumberland Sound to the Resolute, April-July 1853  
  1,227 km routed against 1,100 km straight, 216 km over land, 0 km over ice cap, highest 310 m; the line in the database is 1,176 km and 89 points; this one 89 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 11 (147 km straight, 195 routed); it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **franklin-search-086** (written) — Belcher's own north-east sledge journey, 2 May to 23 June 1853  
  572 km routed against 443 km straight, 145 km over land, 0 km over ice cap, highest 333 m; the line in the database is 533 km and 78 points; this one 78 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 0 (51 km straight, 76 routed); 12 (51 km straight, 76 routed); it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **greenland-inughuit-017** (written) — The return that failed, about 1870 to 1873  
  815 km routed against 604 km straight, 223 km over land, 31 km over ice cap, highest 473 m; the line in the database is 774 km and 89 points; this one 89 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 3 (159 km straight, 221 routed); 4 (108 km straight, 160 routed); 5 (264 km straight, 330 routed); waypoints on land whose note names water: 4, 5; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **greenland-inughuit-042** (written) — The Crocker Land sledge journey, February to May 1914  
  1,482 km routed against 1,247 km straight, 161 km over land, 22 km over ice cap, highest 893 m; the line in the database is 1,389 km and 104 points; this one 104 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 2 (210 km straight, 278 routed); 3 (76 km straight, 129 routed); it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **haig-thomas-1937-001** (written) — Haig-Thomas and Nukapinguaq, Etah to Amund Ringnes Island and back, 1938  
  24 of 24 legs follow ink digitized from haig-thomas-1937-059 (georef rms 6.0 km); the routed line runs 2.5 km from the printed one on average; 1,609 km routed against 1,366 km straight, 385 km over land, 134 km over ice cap, highest 1842 m; the line in the database is 1,518 km and 207 points; this one 208 points; waypoints on land whose note names water: 5, 20, 21; waypoints moved: 8 (the note says down Eureka Sound but the point sat 2 km inside the Ellesmere shore; moved 11 km onto the route drawn down the sound); 22 (position inferred; the printed map draws the return south of the outward crossing, over the ice cap at about 1600 m, and the waypoint is moved 30 km south onto that drawn line); proposed moves, not applied: 5 (on land though the note names water; moved 7 km onto the printed route); 16 (inferred; moved 13 km onto the printed route); 20 (on land though the note names water; moved 10 km onto the printed route); it runs 0.0 km from the line in the database on average and 1 km at most; this line is already in the database, flagged terrain
- **haig-thomas-1937-002** (written) — Wright and Hamilton, the survey of south-east Ellesmere Island, 1938  
  1,050 km routed against 883 km straight, 58 km over land, 48 km over ice cap, highest 492 m; the line in the database is 996 km and 124 points; this one 124 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 0 (140 km straight, 177 routed); 1 (78 km straight, 98 routed); waypoints on land whose note names water: 6, 19; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **kruger-1930-001** (written) — The German Arctic Expedition, March to May 1930  
  1,484 km routed against 1,262 km straight, 163 km over land, 7 km over ice cap, highest 600 m; the line in the database is 1,403 km and 145 points; this one 145 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 3 (109 km straight, 137 routed); 8 (69 km straight, 96 routed); 9 (104 km straight, 148 routed); waypoints on land whose note names water: 0, 3; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **kruger-1930-002** (written) — Stallworthy's first search, 1931  
  1,079 km routed against 857 km straight, 66 km over land, 0 km over ice cap, highest 563 m; the line in the database is 1,028 km and 102 points; this one 102 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 4 (105 km straight, 138 routed); 5 (135 km straight, 207 routed); 6 (199 km straight, 255 routed); waypoints on land whose note names water: 5; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **kruger-1930-003** (written) — Stallworthy's search around Axel Heiberg Island, 1932  
  1,617 km routed against 1,367 km straight, 196 km over land, 3 km over ice cap, highest 433 m; the line in the database is 1,531 km and 192 points; this one 192 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 8 (65 km straight, 100 routed); 16 (36 km straight, 64 routed); 21 (128 km straight, 161 routed); waypoints on land whose note names water: 2; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **kruger-1930-004** (written) — Hamilton's search patrol, 1932  
  1,312 km routed against 1,080 km straight, 222 km over land, 31 km over ice cap, highest 473 m; the line in the database is 1,230 km and 135 points; this one 135 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 2 (53 km straight, 112 routed); 9 (60 km straight, 81 routed); 14 (97 km straight, 133 routed); waypoints on land whose note names water: 15; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **kruger-1930-005** (written) — Dersch's Devon Island search patrol, 1932  
  284 km routed against 208 km straight, 56 km over land, 10 km over ice cap, highest 657 m; the line in the database is 266 km and 34 points; this one 34 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 1 (60 km straight, 89 routed); 4 (88 km straight, 123 routed); waypoints on land whose note names water: 1, 4, 5; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **mcclure-investigator-009** (written) — McClintock's sledge journey to Prince Patrick Island, April-July 1853  
  1,365 km routed against 1,149 km straight, 397 km over land, 0 km over ice cap, highest 235 m; the line in the database is 1,295 km and 128 points; this one 128 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 11 (62 km straight, 100 routed); 12 (29 km straight, 98 routed); it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **mcclure-investigator-010** (written) — Mecham's sledge journey round Eglinton and Prince Patrick Islands, April-July 1853  
  1,457 km routed against 1,277 km straight, 269 km over land, 0 km over ice cap, highest 227 m; the line in the database is 1,376 km and 142 points; this one 142 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 17 (76 km straight, 106 routed); 20 (142 km straight, 179 routed); it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **mcclure-investigator-011** (written) — Hamilton's sledge journey to the rendezvous with Belcher's division, 1853  
  626 km routed against 550 km straight, 89 km over land, 0 km over ice cap, highest 215 m; the line in the database is 597 km and 41 points; this one 41 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 7 (201 km straight, 255 routed); it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **mcclure-investigator-013** (written) — The Resolute's people march to Beechey Island, 15-28 May 1854  
  330 km routed against 304 km straight, 27 km over land, 0 km over ice cap, highest 211 m; the line in the database is 309 km and 23 points; this one 23 points; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **nares-greely-022** (written) — Markham and Parr's sledge journey to 83 deg 20 min 26 sec N, April-June 1876  
  4 of 5 legs follow ink digitized from nares-greely-171 (georef rms 0.5 km); the routed line runs 0.6 km from the printed one on average; 237 km routed against 213 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 225 km and 28 points; this one 28 points; proposed moves, not applied: 1 (inferred; moved 6 km onto the printed route); 2 (inferred; moved 9 km onto the printed route); 3 (inferred; moved 10 km onto the printed route); 4 (inferred; moved 12 km onto the printed route); it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **nares-greely-025** (written) — The retreat from Fort Conger to Cape Sabine, August-October 1883  
  526 km routed against 416 km straight, 15 km over land, 0 km over ice cap, highest 965 m; the line in the database is 497 km and 63 points; this one 63 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 1 (161 km straight, 202 routed); 2 (45 km straight, 75 routed); it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **nares-greely-038** (written) — Aldrich's western sledge journey to Cape Alfred Ernest, April-June 1876  
  16 of 24 legs follow ink digitized from nares-greely-171 (georef rms 0.5 km), 2 chained through hachures or lettering and doubted; the routed line runs 2.4 km from the printed one on average; 1,024 km routed against 786 km straight, 416 km over land, 17 km over ice cap, highest 617 m; the line in the database is 953 km and 160 points; this one 157 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 4 (26 km straight, 51 routed); 16 (37 km straight, 67 routed); it runs 0.0 km from the line in the database on average and 3 km at most; this line is already in the database, flagged terrain
- **nares-greely-039** (written) — Beaumont's north Greenland sledge journey, April-August 1876  
  13 of 24 legs follow ink digitized from nares-greely-171 (georef rms 0.5 km), 1 chained through hachures or lettering and doubted; the routed line runs 2.1 km from the printed one on average; 662 km routed against 584 km straight, 78 km over land, 3 km over ice cap, highest 774 m; the line in the database is 627 km and 88 points; this one 86 points; waypoints on land whose note names water: 19, 20, 21; proposed moves, not applied: 3 (inferred; moved 6 km onto the printed route); 22 (inferred; moved 14 km onto the printed route); 23 (inferred; moved 16 km onto the printed route); it runs 0.0 km from the line in the database on average and 2 km at most; this line is already in the database, flagged terrain
- **operation-hazen-1957-041** (written) — Christie and Hattersley-Smith to Lands Lokk, May-June 1954  
  661 km routed against 617 km straight, 72 km over land, 0 km over ice cap, highest 28 m; the line in the database is 634 km and 43 points; this one 43 points; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **operation-hazen-1957-042** (written) — The 1953 sledge journey west from Alert  
  511 km routed against 445 km straight, 48 km over land, 1 km over ice cap, highest 395 m; the line in the database is 493 km and 54 points; this one 54 points; it runs 0.3 km from the line in the database on average and 2 km at most; this line is already in the database, flagged terrain
- **oxford-ellesmere-1934-002** (written) — Moore, Stallworthy, Nukapinguaq and Inuatuk to Grant Land, April-May 1935  
  18 of 21 legs follow ink digitized from oxford-ellesmere-1934-005 (georef rms 1.0 km), 1 chained through hachures or lettering and doubted; the routed line runs 1.6 km from the printed one on average; 1,685 km routed against 1,304 km straight, 478 km over land, 162 km over ice cap, highest 1798 m; the line in the database is 1,590 km and 216 points; this one 216 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 5 (53 km straight, 74 routed); waypoints on land whose note names water: 10; proposed moves, not applied: 10 (on land though the note names water; moved 8 km onto the printed route); 14 (inferred; moved 15 km onto the printed route); it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **oxford-ellesmere-1934-003** (written) — Humphreys and Haig-Thomas through Grinnell Land and Ellesmere Land, April-May 1935  
  27 of 28 legs follow ink digitized from oxford-ellesmere-1934-005 (georef rms 1.0 km); the routed line runs 3.0 km from the printed one on average; 1,498 km routed against 1,214 km straight, 516 km over land, 82 km over ice cap, highest 1111 m; the line in the database is 1,402 km and 226 points; this one 225 points; waypoints on land whose note names water: 11, 18, 23; proposed moves, not applied: 11 (on land though the note names water; moved 6 km onto the printed route); 18 (on land though the note names water; moved 6 km onto the printed route); 23 (on land though the note names water; moved 7 km onto the printed route); it runs 0.0 km from the line in the database on average and 1 km at most; this line is already in the database, flagged terrain
- **oxford-ellesmere-1934-004** (written) — Shackleton and Bentham to Scoresby Bay, April-May 1935  
  17 of 26 legs follow ink digitized from oxford-ellesmere-1934-005 (georef rms 1.0 km), 1 chained through hachures or lettering and doubted; the routed line runs 1.8 km from the printed one on average; 890 km routed against 724 km straight, 94 km over land, 6 km over ice cap, highest 747 m; the line in the database is 837 km and 131 points; this one 131 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 12 (10 km straight, 53 routed); it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **pole-seekers-from-ellesmere-030** (written) — Hattersley-Smith's sledge journey along the north coast, April-May 1953  
  416 km routed against 339 km straight, 54 km over land, 1 km over ice cap, highest 306 m; the line in the database is 398 km and 39 points; this one 46 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 0 (97 km straight, 134 routed); waypoints on land whose note names water: 5, 7; it runs 0.5 km from the line in the database on average and 2 km at most; this line is already in the database, flagged terrain
- **pole-seekers-from-ellesmere-031** (written) — Ward Hunt Island to Crane City and back, May 1954  
  131 km routed against 115 km straight, 85 km over land, 1 km over ice cap, highest 87 m; the line in the database is 121 km and 16 points; this one 16 points; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **rcmp-high-arctic-patrols-003** (written) — Joy from Bache Peninsula to King Christian Island, March to May 1927  
  10 of 20 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km), 1 chained through hachures or lettering and doubted; the routed line runs 3.0 km from the printed one on average; 1,874 km routed against 1,575 km straight, 683 km over land, 143 km over ice cap, highest 1505 m; the line in the database is 1,763 km and 199 points; this one 199 points; waypoints on land whose note names water: 17; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **rcmp-high-arctic-patrols-005** (written) — Makinson and Coolitanga, and the finding of Makinson Inlet, 1928  
  4 of 7 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km); the routed line runs 2.5 km from the printed one on average; 952 km routed against 712 km straight, 103 km over land, 99 km over ice cap, highest 1235 m; the line in the database is 905 km and 88 points; this one 88 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 6 (210 km straight, 277 routed); waypoints on land whose note names water: 4; proposed moves, not applied: 1 (inferred; moved 23 km onto the printed route); it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **rcmp-high-arctic-patrols-006** (written) — Anstead and Nukapinguaq to Norwegian Bay, 1928  
  7 of 14 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km); the routed line runs 3.3 km from the printed one on average; 1,325 km routed against 1,064 km straight, 513 km over land, 150 km over ice cap, highest 1505 m; the line in the database is 1,242 km and 135 points; this one 135 points; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **rcmp-high-arctic-patrols-008** (written) — McLean, Beatty and Nukapinguaq: the new crossing of Ellesmere Island, 1930  
  8 of 11 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km); the routed line runs 3.0 km from the printed one on average; 1,369 km routed against 1,029 km straight, 390 km over land, 156 km over ice cap, highest 1235 m; the line in the database is 1,288 km and 162 points; this one 161 points; waypoints on land whose note names water: 7; proposed moves, not applied: 10 (inferred; moved 12 km onto the printed route); it runs 0.0 km from the line in the database on average and 3 km at most; this line is already in the database, flagged terrain
- **rcmp-high-arctic-patrols-009** (written) — Timbury, Hamilton and Keepomee to Beechey Island, 1930  
  3 of 4 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km); the routed line runs 1.4 km from the printed one on average; 850 km routed against 753 km straight, 98 km over land, 0 km over ice cap, highest 285 m; the line in the database is 820 km and 72 points; this one 70 points; waypoints on land whose note names water: 0, 4; it runs 0.0 km from the line in the database on average and 1 km at most; this line is already in the database, flagged terrain
- **rcmp-high-arctic-patrols-010** (written) — Stallworthy's first search for the Kruger party, 1931  
  6 of 11 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km); the routed line runs 3.8 km from the printed one on average; 1,286 km routed against 944 km straight, 34 km over land, 23 km over ice cap, highest 705 m; the line in the database is 1,214 km and 131 points; this one 131 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 1 (34 km straight, 85 routed); waypoints on land whose note names water: 7, 8; proposed moves, not applied: 4 (inferred; moved 14 km onto the printed route); 6 (inferred; moved 23 km onto the printed route); it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **sverdrup-bernier-peary-003** (written) — Isachsen and Hassel across the Ringnes islands, spring 1901  
  1,467 km routed against 1,275 km straight, 521 km over land, 0 km over ice cap, highest 457 m; the line in the database is 1,386 km and 150 points; this one 150 points; waypoints on land whose note names water: 0, 3; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **sverdrup-bernier-peary-178** (written) — Peary's winter march to Fort Conger, December 1898 to February 1899  
  691 km routed against 621 km straight, 3 km over land, 0 km over ice cap, highest 96 m; the line in the database is 653 km and 52 points; this one 52 points; waypoints on land whose note names water: 6; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **sverdrup-bernier-peary-180** (written) — Peary from Cape Hecla to 84 degrees 17 minutes north, 1902  
  1,611 km routed against 1,402 km straight, 19 km over land, 0 km over ice cap, highest 464 m; the line in the database is 1,508 km and 138 points; this one 138 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 25 (124 km straight, 190 routed); waypoints on land whose note names water: 10; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **sverdrup-bernier-peary-194** (written) — Peary's summer journey west to Cape Thomas Hubbard, 1906  
  1,417 km routed against 1,156 km straight, 504 km over land, 15 km over ice cap, highest 283 m; the line in the database is 1,347 km and 144 points; this one 144 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 5 (42 km straight, 77 routed); 13 (106 km straight, 149 routed); 14 (45 km straight, 67 routed); 15 (61 km straight, 84 routed); waypoints on land whose note names water: 6; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **sverdrup-bernier-peary-302** (written) — Sverdrup and Fosheim up the west coast of Axel Heiberg Island, spring 1900  
  1,770 km routed against 1,402 km straight, 304 km over land, 0 km over ice cap, highest 392 m; the line in the database is 1,654 km and 215 points; this one 215 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 0 (44 km straight, 92 routed); 3 (34 km straight, 59 routed); 32 (76 km straight, 110 routed); 38 (70 km straight, 114 routed); 39 (88 km straight, 127 routed); waypoints on land whose note names water: 30; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **sverdrup-bernier-peary-304** (written) — Sverdrup and Schei to Lands Lokk, spring 1902  
  1,680 km routed against 1,425 km straight, 389 km over land, 21 km over ice cap, highest 794 m; the line in the database is 1,579 km and 168 points; this one 168 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 31 (42 km straight, 77 routed); waypoints on land whose note names water: 0, 21, 31, 33; it runs 0.0 km from the line in the database on average and 0 km at most; this line is already in the database, flagged terrain
- **amundsen-gjoa-002** (recommend) — Amundsen's ride to the telegraph at Eagle, 1905-1906  
  1,566 km routed against 1,288 km straight, 1,548 km over land, 0 km over ice cap, highest 716 m; the line in the database is 1,288 km and 64 points; this one 187 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 0 (66 km straight, 87 routed); 1 (167 km straight, 219 routed); it runs 15.7 km from the line in the database on average and 53 km at most
- **crocker-land-1913-004** (recommend) — MacMillan to King Christian Island and North Cornwall, March to May 1916  
  2,373 km routed against 1,738 km straight, 657 km over land, 68 km over ice cap, highest 1487 m; the line in the database is 1,738 km and 78 points; this one 283 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 3 (86 km straight, 108 routed); 6 (92 km straight, 152 routed); 7 (37 km straight, 135 routed); 8 (44 km straight, 171 routed); 21 (196 km straight, 338 routed); waypoints on land whose note names water: 7, 22; it runs 9.3 km from the line in the database on average and 60 km at most
- **franklin-search-022** (recommend) — Ommanney's southern division: Cape Walker and Prince of Wales Island, April-June 1851  
  626 km routed against 576 km straight, 62 km over land, 0 km over ice cap, highest 171 m; the line in the database is 576 km and 27 points; this one 39 points; it runs 1.5 km from the line in the database on average and 11 km at most
- **franklin-search-027** (recommend) — Kennedy and Bellot's sledge journey round Somerset Island, February-May 1852  
  1,121 km routed against 1,029 km straight, 269 km over land, 0 km over ice cap, highest 286 m; the line in the database is 1,029 km and 49 points; this one 84 points; waypoints on land whose note names water: 0, 5, 15; it runs 2.7 km from the line in the database on average and 23 km at most
- **greenland-inughuit-016** (recommend) — Qitdlarssuaq's migration, about 1852 to 1863  
  1,446 km routed against 1,188 km straight, 426 km over land, 193 km over ice cap, highest 1548 m; the line in the database is 1,188 km and 56 points; this one 156 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 0 (131 km straight, 182 routed); 2 (166 km straight, 219 routed); 6 (40 km straight, 75 routed); waypoints on land whose note names water: 0, 1, 6; it runs 9.0 km from the line in the database on average and 36 km at most
- **greenland-inughuit-043** (recommend) — Ahwelah and Etukishook with Cook, February 1908 to April 1909  
  2,071 km routed against 1,545 km straight, 499 km over land, 56 km over ice cap, highest 554 m; the line in the database is 1,892 km and 183 points; this one 191 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 2 (160 km straight, 282 routed); 3 (84 km straight, 172 routed); 6 (161 km straight, 239 routed); 7 (168 km straight, 232 routed); 9 (168 km straight, 223 routed); 11 (116 km straight, 179 routed); waypoints on land whose note names water: 3; waypoints moved: 2 (the note names Cape Rutherford, and Cook writes that 'passing Cape Rutherford on February 22, we followed the coast', but the point sat 10 km inland of the shore on the ice cap at 893 m; moved 14 km to the charted position of the cape, on the ice of the coast they followed); 7 (the position is inferred and the note says the west side of Axel Heiberg Island, but the point sat 27 km inland on the ice cap at 1424 m; moved west onto the sea ice off the west coast, the shore Cook names as the line of retreat down 'the west coast of Axel Heiberg Land'); it runs 4.1 km from the line in the database on average and 64 km at most
- **greenland-inughuit-045** (recommend) — The Fifth Thule Expedition across Arctic America, 1921-1924  
  7,278 km routed against 6,528 km straight, 2,678 km over land, 0 km over ice cap, highest 603 m; the line in the database is 6,528 km and 322 points; this one 500 points; waypoints on land whose note names water: 3, 6, 12; it runs 18.4 km from the line in the database on average and 133 km at most
- **hudson-strait-south-baffin-015** (recommend) — Patrol A-11-A: down on the Atlantic ice, and the walk back  
  577 km routed against 535 km straight, 3 km over land, 0 km over ice cap, highest 94 m; the line in the database is 535 km and 24 points; this one 26 points; it runs 1.3 km from the line in the database on average and 12 km at most
- **inuit-oral-history-029** (recommend) — The coast Iligliuk drew: Winter Island to the Fury and Hecla Strait  
  619 km routed against 554 km straight, 118 km over land, 0 km over ice cap, highest 272 m; the line in the database is 554 km and 9 points; this one 49 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 1 (102 km straight, 131 routed); it runs 5.3 km from the line in the database on average and 29 km at most
- **inuit-oral-history-030** (recommend) — The journey to Akkoolee: the sleeping places on the Netsilingmiut chart, 1830  
  505 km routed against 461 km straight, 189 km over land, 0 km over ice cap, highest 141 m; the line in the database is 461 km and 21 points; this one 54 points; waypoints on land whose note names water: 4; it runs 1.3 km from the line in the database on average and 7 km at most
- **kane-hall-polaris-002** (recommend) — The boat retreat from Rensselaer Harbour to Upernavik, 1855  
  1,006 km routed against 929 km straight, 62 km over land, 8 km over ice cap, highest 397 m; the line in the database is 965 km and 45 points; this one 50 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 7 (57 km straight, 81 routed); it runs 0.2 km from the line in the database on average and 3 km at most
- **karluk-cae-002** (recommend) — Stefansson's 1914 ice journey: Martin Point to Banks Island  
  1,205 km routed against 1,138 km straight, 121 km over land, 0 km over ice cap, highest 53 m; the line in the database is 1,138 km and 55 points; this one 33 points; it runs 2.1 km from the line in the database on average and 15 km at most
- **karluk-cae-003** (recommend) — Stefansson's 1915 ice journey: the new land north of Prince Patrick Island  
  2,068 km routed against 1,953 km straight, 463 km over land, 0 km over ice cap, highest 224 m; the line in the database is 1,953 km and 97 points; this one 89 points; waypoints on land whose note names water: 9, 15; it runs 2.7 km from the line in the database on average and 14 km at most
- **karluk-cae-004** (recommend) — Stefansson's 1916 ice journey: Banks Island to Meighen and Lougheed Islands  
  2,652 km routed against 2,404 km straight, 487 km over land, 0 km over ice cap, highest 295 m; the line in the database is 2,404 km and 112 points; this one 155 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 4 (137 km straight, 203 routed); 23 (137 km straight, 177 routed); waypoints on land whose note names water: 15; it runs 6.1 km from the line in the database on average and 47 km at most
- **karluk-cae-008** (recommend) — Stefansson's last ice journey, 1917: Melville Island to the sea desert and back to Cape Kellett  
  2,401 km routed against 2,192 km straight, 588 km over land, 0 km over ice cap, highest 167 m; the line in the database is 2,192 km and 25 points; this one 134 points; waypoints on land whose note names water: 23; it runs 4.5 km from the line in the database on average and 49 km at most
- **mcclure-investigator-006** (recommend) — Pim's sledge journey from HMS Resolute to the Investigator, March-April 1853  
  750 km routed against 583 km straight, 239 km over land, 0 km over ice cap, highest 369 m; the line in the database is 583 km and 27 points; this one 84 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 2 (84 km straight, 114 routed); 9 (105 km straight, 149 routed); 10 (50 km straight, 72 routed); waypoints on land whose note names water: 9; it runs 7.6 km from the line in the database on average and 25 km at most
- **mcclure-investigator-007** (recommend) — McClure crosses to HMS Resolute and back, April-May 1853  
  634 km routed against 571 km straight, 39 km over land, 0 km over ice cap, highest 343 m; the line in the database is 606 km and 48 points; this one 49 points; waypoints on land whose note names water: 0, 5; it runs 0.8 km from the line in the database on average and 24 km at most
- **mcclure-investigator-008** (recommend) — The Investigator's crew walk from Mercy Bay to the Resolute, June 1853  
  320 km routed against 288 km straight, 134 km over land, 0 km over ice cap, highest 343 m; the line in the database is 310 km and 31 points; this one 33 points; it runs 3.5 km from the line in the database on average and 24 km at most
- **mcclure-investigator-054** (recommend) — McClure's sledge journey to Parry's Rock, April 1852  
  252 km routed against 227 km straight, 122 km over land, 0 km over ice cap, highest 343 m; the line in the database is 243 km and 20 points; this one 24 points; waypoints on land whose note names water: 0; it runs 6.0 km from the line in the database on average and 25 km at most
- **nares-greely-023** (recommend) — Lockwood, Brainard and Christiansen's journey to 83 deg 24 min N, April-June 1882  
  897 km routed against 790 km straight, 49 km over land, 0 km over ice cap, highest 823 m; the line in the database is 861 km and 90 points; this one 59 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 3 (94 km straight, 128 routed); it runs 6.8 km from the line in the database on average and 27 km at most
- **pole-seekers-from-ellesmere-007** (recommend) — Peary's 1906 route from Point Moss to 87 deg 06 min N  
  1,179 km routed against 1,096 km straight, 3 km over land, 0 km over ice cap, highest 283 m; the line in the database is 1,096 km and 54 points; this one 18 points; it runs 9.4 km from the line in the database on average and 29 km at most
- **rock-and-the-sverdrup-basin-701** (recommend) — Thorsteinsson and Jebbedi out of Eureka, 1956  
  1,349 km routed against 1,129 km straight, 232 km over land, 5 km over ice cap, highest 594 m; the line in the database is 1,129 km and 20 points; this one 124 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 5 (59 km straight, 81 routed); 11 (118 km straight, 163 routed); 15 (128 km straight, 163 routed); it runs 3.3 km from the line in the database on average and 24 km at most
- **rock-and-the-sverdrup-basin-702** (recommend) — Tozer and Amagualik on Axel Heiberg Island, 1956  
  294 km routed against 259 km straight, 121 km over land, 0 km over ice cap, highest 560 m; the line in the database is 259 km and 6 points; this one 35 points; waypoints on land whose note names water: 1, 4; it runs 3.0 km from the line in the database on average and 12 km at most
- **ross-victory-002** (recommend) — James Clark Ross's sledge journey to the North Magnetic Pole, 27 May to 1 June 1831  
  247 km routed against 219 km straight, 114 km over land, 0 km over ice cap, highest 98 m; the line in the database is 237 km and 11 points; this one 32 points; it runs 1.6 km from the line in the database on average and 21 km at most
- **science-stations-029** (recommend) — The drift of the ice island T-1, 1946-1952  
  2,084 km routed against 2,037 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 2,037 km and 101 points; this one 6 points; it runs 54.0 km from the line in the database on average and 174 km at most
- **sverdrup-bernier-peary-179** (recommend) — Peary along the north coast of Greenland to Cape Morris Jesup, 1900  
  2,012 km routed against 1,810 km straight, 159 km over land, 1 km over ice cap, highest 886 m; the line in the database is 1,810 km and 32 points; this one 125 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 17 (41 km straight, 61 routed); it runs 1.2 km from the line in the database on average and 16 km at most
- **sverdrup-bernier-peary-183** (recommend) — Lavoie's sledge survey of Prince Regent Inlet, spring 1911  
  1,264 km routed against 1,104 km straight, 517 km over land, 0 km over ice cap, highest 342 m; the line in the database is 1,104 km and 14 points; this one 115 points; waypoints on land whose note names water: 1, 4; it runs 8.3 km from the line in the database on average and 42 km at most
- **sverdrup-bernier-peary-193** (recommend) — Peary's sledge journey from Point Moss to 87 degrees 6 minutes north, 1906 (claimed route)  
  1,340 km routed against 1,181 km straight, 40 km over land, 0 km over ice cap, highest 663 m; the line in the database is 1,181 km and 12 points; this one 38 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 10 (77 km straight, 106 routed); it runs 7.2 km from the line in the database on average and 38 km at most
- **sverdrup-bernier-peary-303** (recommend) — Sverdrup and Schei up Eureka Sound, spring 1901  
  1,586 km routed against 1,151 km straight, 488 km over land, 0 km over ice cap, highest 783 m; the line in the database is 1,151 km and 40 points; this one 228 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 5 (65 km straight, 93 routed); 10 (20 km straight, 49 routed); 14 (9 km straight, 50 routed); 17 (20 km straight, 128 routed); 32 (43 km straight, 67 routed); waypoints on land whose note names water: 3, 6, 13, 15, 17, 33; it runs 3.8 km from the line in the database on average and 22 km at most
- **thule-dorset-001** (recommend) — The Thule migration from Alaska, schematic  
  5,315 km routed against 4,434 km straight, 3,251 km over land, 0 km over ice cap, highest 327 m; the line in the database is 4,434 km and 218 points; this one 422 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 1 (546 km straight, 732 routed); 2 (766 km straight, 1,001 routed); 5 (368 km straight, 468 routed); waypoints on land whose note names water: 4, 6, 7; it runs 40.4 km from the line in the database on average and 144 km at most
- **wrecks-disasters-038** (recommend) — The Grenville Bay's winter drift, October to December 1835  
  1,658 km routed against 1,502 km straight, 5 km over land, 0 km over ice cap, highest 450 m; the line in the database is 1,502 km and 73 points; this one 66 points; waypoints on land whose note names water: 3; it runs 12.9 km from the line in the database on average and 100 km at most
- **franklin-search-023** (review) — HMS Resolute, 1852-1855: Dealy Island, the drift and the derelict  
  5 of 25 legs could not be routed (outside the DEM); 12,261 km routed against 11,702 km straight, 323 km over land, 0 km over ice cap, highest 284 m; the line in the database is 11,702 km and 576 points; this one 567 points; waypoints on land whose note names water: 16; it runs 23.4 km from the line in the database on average and 260 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **franklin-search-068** (review) — Richardson and Rae's boat voyage and march, 1848  
  3 of 22 legs lie outside the DEM, 3 of them routed through water by the sea router; 9,985 km routed against 9,698 km straight, 2,800 km over land, 0 km over ice cap, highest 492 m; the line in the database is 9,698 km and 476 points; this one 264 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 5 (109 km straight, 138 routed); waypoints on land whose note names water: 9; it runs 175.1 km from the line in the database on average and 560 km at most; the legs outside the DEM are the sea router's water paths or great circles, which is right over the sea ice; review the rest
- **franklin-search-136** (review) — The Advance and the Rescue, 1850-51: the drift out of Wellington Channel  
  2 of 40 legs could not be routed (outside the DEM); 12,819 km routed against 12,253 km straight, 804 km over land, 0 km over ice cap, highest 557 m; the line in the database is 12,253 km and 41 points; this one 677 points; waypoints on land whose note names water: 13; it runs 68.2 km from the line in the database on average and 198 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **ice-shelves-and-ice-islands-004** (review) — The drift of ice island WH-5, 1962-1964  
  5 of 20 legs could not be routed (outside the DEM); 7,648 km routed against 7,384 km straight, 83 km over land, 0 km over ice cap, highest 258 m; the line in the database is 7,384 km and 21 points; this one 319 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 1 (217 km straight, 302 routed); it runs 15.9 km from the line in the database on average and 276 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **ice-shelves-and-ice-islands-006** (review) — Ice island T-3, from Ellef Ringnes to the pole and back, 1947-1971  
  3 of 5 legs could not be routed (outside the DEM); 3,767 km routed against 3,733 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 3,733 km and 6 points; this one 149 points; it runs 176.4 km from the line in the database on average and 568 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **kane-hall-polaris-035** (review) — The Polaris ice-floe drift, 15 October 1872 to 30 April 1873  
  10 of 27 legs could not be routed (outside the DEM); 3,451 km routed against 3,216 km straight, 91 km over land, 3 km over ice cap, highest 344 m; the line in the database is 3,216 km and 151 points; this one 115 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 1 (58 km straight, 82 routed); 9 (101 km straight, 141 routed); 10 (45 km straight, 75 routed); waypoints on land whose note names water: 16; it runs 2.0 km from the line in the database on average and 40 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **kane-hall-polaris-263** (review) — Hayes's sledge journey across Smith Sound and up the Ellesmere coast, April to June 1861  
  14 of 18 legs follow ink digitized from kane-hall-polaris-193 (georef rms 0.3 km), 1 chained through hachures or lettering and doubted; the routed line runs 1.1 km from the printed one on average; 584 km routed against 495 km straight, 4 km over land, 0 km over ice cap, highest 391 m; the line in the database is 495 km and 19 points; this one 73 points; proposed moves, not applied: 4 (inferred; moved 17 km onto the printed route); 5 (inferred; moved 6 km onto the printed route); 6 (inferred; moved 19 km onto the printed route); 15 (inferred; moved 7 km onto the printed route); 16 (inferred; moved 9 km onto the printed route); 17 (inferred; moved 13 km onto the printed route); it runs 5.1 km from the line in the database on average and 22 km at most; Hayes's own chart puts the Ellesmere coast a degree too far north, so a route digitized against it is only as good as his coast
- **karluk-cae-006** (review) — Bartlett and Kataktovik's walk to Siberia, March-May 1914  
  5 of 7 legs could not be routed (outside the DEM); 1,802 km routed against 1,768 km straight, 46 km over land, 0 km over ice cap, highest 21 m; the line in the database is 1,768 km and 85 points; this one 70 points; it runs 1.0 km from the line in the database on average and 14 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **karluk-cae-007** (review) — Rasmussen's sledge journey across Arctic America, 1921-1924  
  1 of 19 legs lie outside the DEM, 1 of them routed through water by the sea router; 10,997 km routed against 10,103 km straight, 3,530 km over land, 0 km over ice cap, highest 603 m; the line in the database is 10,103 km and 497 points; this one 605 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 7 (363 km straight, 482 routed); waypoints on land whose note names water: 6; it runs 232.3 km from the line in the database on average and 1141 km at most; the legs outside the DEM are the sea router's water paths or great circles, which is right over the sea ice; review the rest
- **mcclure-investigator-014** (review) — The Resolute's drift, 1854-1855, and her voyage to New London  
  1 of 4 legs could not be routed (outside the DEM); 4,686 km routed against 4,559 km straight, 119 km over land, 0 km over ice cap, highest 284 m; the line in the database is 4,559 km and 227 points; this one 197 points; it runs 5.2 km from the line in the database on average and 86 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **operation-hazen-1957-026** (review) — The drift of ice island WH-5, Ward Hunt Ice Shelf to the Grand Banks, 1962-1964  
  3 of 11 legs could not be routed (outside the DEM); 4,897 km routed against 4,674 km straight, 105 km over land, 0 km over ice cap, highest 640 m; the line in the database is 4,674 km and 231 points; this one 195 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 1 (184 km straight, 278 routed); waypoints on land whose note names water: 2; it runs 10.0 km from the line in the database on average and 246 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **pole-seekers-from-ellesmere-006** (review) — Peary's 1909 route from Cape Columbia, by his own latitudes  
  2 of 10 legs could not be routed (outside the DEM); 1,721 km routed against 1,670 km straight, 0 km over land, 0 km over ice cap, highest 26 m; the line in the database is 1,670 km and 82 points; this one 69 points; it runs 0.5 km from the line in the database on average and 12 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **pole-seekers-from-ellesmere-038** (review) — The Italian expedition to the North Pole, Cape Columbia to T-3, 1971  
  2 of 5 legs could not be routed (outside the DEM); 2,155 km routed against 2,015 km straight, 6 km over land, 1 km over ice cap, highest 146 m; the line in the database is 2,015 km and 6 points; this one 114 points; it runs 113.4 km from the line in the database on average and 457 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **pole-seekers-from-ellesmere-039** (review) — Jean-Louis Etienne alone from Ward Hunt Island to the Pole, 1986  
  2 of 6 legs could not be routed (outside the DEM); 2,505 km routed against 2,476 km straight, 14 km over land, 0 km over ice cap, highest 31 m; the line in the database is 2,476 km and 7 points; this one 100 points; it runs 182.1 km from the line in the database on average and 522 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **posts-rcmp-missions-023** (review) — Joy's attempt on Ellesmere Island, March-April 1924  
  7 of 17 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km); the routed line runs 1.7 km from the printed one on average; 925 km routed against 745 km straight, 130 km over land, 0 km over ice cap, highest 407 m; the line in the database is 745 km and 35 points; this one 91 points; waypoints on land whose note names water: 0, 2; proposed moves, not applied: 2 (on land though the note names water; moved 8 km onto the printed route); it runs 7.2 km from the line in the database on average and 41 km at most
- **qei-from-the-air-1947-023** (review) — Fairbanks - Ellesmere - the North Pole - Edmonton, 9-10 May 1946  
  3 of 7 legs could not be routed (outside the DEM); 8,390 km routed against 7,673 km straight, 1,214 km over land, 42 km over ice cap, highest 1639 m; the line in the database is 7,673 km and 8 points; this one 415 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 0 (658 km straight, 978 routed); it runs 142.5 km from the line in the database on average and 1033 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **qei-from-the-air-1947-024** (review) — Where the SHORAN survey was, season by season, 1949-1957  
  7 of 10 legs could not be routed (outside the DEM); 14,714 km routed against 13,866 km straight, 3,850 km over land, 747 km over ice cap, highest 2446 m; the line in the database is 13,866 km and 690 points; this one 814 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 7 (2,218 km straight, 2,950 routed); it runs 31.7 km from the line in the database on average and 359 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **rcmp-high-arctic-patrols-001** (review) — Joy over the Devon Island ice cap, March and April 1926  
  5 of 11 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km); the routed line runs 0.6 km from the printed one on average; 692 km routed against 549 km straight, 273 km over land, 251 km over ice cap, highest 1909 m; the line in the database is 549 km and 24 points; this one 83 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 6 (76 km straight, 109 routed); waypoints on land whose note names water: 5, 6, 11; proposed moves, not applied: 2 (inferred; moved 20 km onto the printed route); 3 (inferred; moved 17 km onto the printed route); it runs 4.6 km from the line in the database on average and 28 km at most
- **rcmp-high-arctic-patrols-002** (review) — Joy from Craig Harbour to Axel Heiberg Island, April and May 1926  
  7 of 16 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km); the routed line runs 2.6 km from the printed one on average; 1,478 km routed against 1,110 km straight, 327 km over land, 10 km over ice cap, highest 655 m; the line in the database is 1,110 km and 50 points; this one 169 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 1 (41 km straight, 138 routed); 13 (20 km straight, 48 routed); waypoints on land whose note names water: 0, 2, 5, 13, 15, 16; it runs 8.5 km from the line in the database on average and 45 km at most
- **rcmp-high-arctic-patrols-004** (review) — Bain and Oodee, Bache Peninsula to Craig Harbour and back, 1927  
  5 of 13 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km); the routed line runs 3.4 km from the printed one on average; 998 km routed against 776 km straight, 3 km over land, 0 km over ice cap, highest 85 m; the line in the database is 776 km and 37 points; this one 99 points; waypoints on land whose note names water: 1, 7, 8; proposed moves, not applied: 10 (inferred; moved 18 km onto the printed route); it runs 11.0 km from the line in the database on average and 53 km at most
- **rcmp-high-arctic-patrols-007** (review) — Joy, Taggart and Nukapinguaq: Dundas Harbour to Melville Island to Bache Peninsula, 1929  
  7 of 16 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km), 1 chained through hachures or lettering and doubted; the routed line runs 6.0 km from the printed one on average; 2,359 km routed against 2,093 km straight, 677 km over land, 85 km over ice cap, highest 1505 m; the line in the database is 2,093 km and 98 points; this one 210 points; waypoints on land whose note names water: 14; it runs 7.9 km from the line in the database on average and 45 km at most
- **ross-victory-003** (review) — The retreat from the Victory and the open-boat escape, 1832-1833  
  2 of 16 legs lie outside the DEM, 2 of them routed through water by the sea router; 5,710 km routed against 5,538 km straight, 50 km over land, 0 km over ice cap, highest 286 m; the line in the database is 5,538 km and 274 points; this one 83 points; waypoints on land whose note names water: 8; it runs 293.2 km from the line in the database on average and 849 km at most; the legs outside the DEM are the sea router's water paths or great circles, which is right over the sea ice; review the rest
- **science-stations-003** (review) — The drift of the ice island T-3, 1947-1952  
  4 of 7 legs could not be routed (outside the DEM); 3,359 km routed against 3,292 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 3,292 km and 163 points; this one 122 points; it runs 2.5 km from the line in the database on average and 23 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **science-stations-073** (review) — The 1959 reconnaissance to Axel Heiberg Island, 13 July to 26 August  
  1 of 5 legs could not be routed (outside the DEM); 4,843 km routed against 4,697 km straight, 613 km over land, 33 km over ice cap, highest 929 m; the line in the database is 4,697 km and 6 points; this one 309 points; waypoints on land whose note names water: 3; it runs 109.7 km from the line in the database on average and 191 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **science-stations-074** (review) — The 1960 airlift: Montreal to Expedition Fiord, May 1960  
  1 of 5 legs could not be routed (outside the DEM); 4,123 km routed against 4,066 km straight, 219 km over land, 140 km over ice cap, highest 1742 m; the line in the database is 4,066 km and 6 points; this one 241 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 3 (42 km straight, 62 routed); waypoints on land whose note names water: 4; it runs 123.8 km from the line in the database on average and 204 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **sverdrup-bernier-peary-300** (review) — The first crossing of Ellesmere Island, April and May 1899  
  8 of 11 legs follow ink digitized from sverdrup-bernier-peary-064 (georef rms 0.0 km), 1 chained through hachures or lettering and doubted; the routed line runs 4.0 km from the printed one on average; 429 km routed against 297 km straight, 172 km over land, 1 km over ice cap, highest 672 m; the line in the database is 297 km and 12 points; this one 76 points; legs held by no ink that the terrain lengthens by more than a quarter, to look at: 8 (33 km straight, 95 routed); waypoints on land whose note names water: 0, 2, 3, 4, 5, 6, 7, 9; proposed moves, not applied: 9 (on land though the note names water; moved 10 km onto the printed route); it runs 2.4 km from the line in the database on average and 11 km at most; a first-reconnaissance sketch with hachured relief: the dash-dot route is hard to tell from the shading and the chain wanders, so the corridor is weak evidence here
- **sverdrup-bernier-peary-301** (review) — Isachsen and Braskerud over the glaciers to the west coast, 1899  
  9 of 11 legs follow ink digitized from sverdrup-bernier-peary-064 (georef rms 0.0 km), 1 chained through hachures or lettering and doubted; the routed line runs 2.0 km from the printed one on average; 372 km routed against 256 km straight, 279 km over land, 260 km over ice cap, highest 1625 m; the line in the database is 256 km and 12 points; this one 65 points; waypoints on land whose note names water: 10; it runs 3.9 km from the line in the database on average and 18 km at most; a first-reconnaissance sketch with hachured relief: the dash-dot route is hard to tell from the shading and the chain wanders, so the corridor is weak evidence here
- **the-sea-ice-trk-002** (review) — The drift of the Polaris floe party, 15 October 1872 to 30 April 1873  
  5 of 11 legs could not be routed (outside the DEM); 2,950 km routed against 2,830 km straight, 8 km over land, 0 km over ice cap, highest 37 m; the line in the database is 2,830 km and 12 points; this one 28 points; it runs 3.2 km from the line in the database on average and 14 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **franklin-1845-002** (same) — Where the ships went after 1848: the drift the Inuit testimony describes  
  227 km routed against 216 km straight, 21 km over land, 0 km over ice cap, highest 20 m; the line in the database is 216 km and 10 points; this one 8 points; it runs 0.2 km from the line in the database on average and 1 km at most; the same line as the database holds to within 3 km (a journey over the sea ice routes straight), so there is nothing to write back
- **ice-shelves-and-ice-islands-005** (same) — The drift of the Ayles ice island, 2005-2007  
  99 km routed against 93 km straight, 22 km over land, 1 km over ice cap, highest 37 m; the line in the database is 93 km and 5 points; this one 10 points; waypoints on land whose note names water: 4; it runs 0.7 km from the line in the database on average and 3 km at most; the same line as the database holds to within 3 km (a journey over the sea ice routes straight), so there is nothing to write back
- **karluk-cae-005** (same) — Storkerson's drift on the Beaufort Sea ice, 1918  
  1,179 km routed against 1,109 km straight, 3 km over land, 0 km over ice cap, highest 1 m; the line in the database is 1,109 km and 52 points; this one 14 points; it runs 0.9 km from the line in the database on average and 3 km at most; the same line as the database holds to within 3 km (a journey over the sea ice routes straight), so there is nothing to write back
- **mcclure-investigator-012** (same) — The Resolute and Intrepid beset and drifting off Cape Cockburn, 1853-54  
  217 km routed against 206 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 206 km and 11 points; this one 6 points; it runs 0.3 km from the line in the database on average and 1 km at most; the same line as the database holds to within 3 km (a journey over the sea ice routes straight), so there is nothing to write back
- **sverdrup-bernier-peary-035** (same) — The 1909 sledge journey from Cape Columbia (claimed route)  
  2 of 5 legs could not be routed (outside the DEM); 1,573 km routed against 1,532 km straight, 0 km over land, 0 km over ice cap, highest 1 m; the line in the database is 1,532 km and 75 points; this one 54 points; it runs 0.0 km from the line in the database on average and 0 km at most; the same line as the database holds to within 3 km (a journey over the sea ice routes straight), so there is nothing to write back
- **the-sea-ice-trk-001** (same) — The drift of the Fox in the pack of Baffin Bay and Davis Strait, 17 August 1857 to 26 April 1858  
  1,589 km routed against 1,511 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 1,511 km and 11 points; this one 11 points; it runs 0.0 km from the line in the database on average and 0 km at most; the same line as the database holds to within 3 km (a journey over the sea ice routes straight), so there is nothing to write back
- **science-stations-030** (outside) — The drift of the ice island T-2, 1950-1951  
  1 of 1 legs could not be routed (outside the DEM); 687 km routed against 687 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 687 km and 35 points; this one 35 points; it runs 0.0 km from the line in the database on average and 0 km at most; every leg is outside the DEM, so this is not the terrain router's track: leave it as-given

## Waypoints that look misplaced

A waypoint on land whose note names water, or one whose note calls it inferred and that lies more than 5 km from the digitized ink.  A proposed move is written to `digitized/<track>.moves.proposed.json`; renaming it to `<track>.moves.json` applies it on the next run, and `--write` then moves the waypoint with its note and the description saying so.

- cook-1908-axel-heiberg-001 waypoint 11: sea, 23 km from the ink; proposed 80.800 -90.900 (inferred; moved 23 km onto the printed route) — up Nansen Sound between Ellesmere and Axel Heiberg (date inferred)
- cook-1908-axel-heiberg-002 waypoint 2: land at 139 m, 7 km from the ink; proposed 76.641 -95.770 (inferred; moved 7 km onto the printed route) — Penny Strait between Bathurst Island and Grinnell Peninsula; makes for the Devon
- cook-1908-axel-heiberg-002 waypoint 5: land at 291 m, 9 km from the ink; proposed 76.696 -90.073 (inferred; moved 9 km onto the printed route) — driven on a berg past Hell Gate and Cardigan Strait, losing a fortnight in a day
- cook-1908-axel-heiberg-002 waypoint 6: land at 15 m, 15 km from the ink; proposed 76.361 -88.987 (inferred; moved 15 km onto the printed route) — lands at Cape Vera on Devon Island; a hare taken (date inferred)
- crocker-land-1913-002 waypoint 4: land at 422 m — Payer Harbour again in six hours, in a north gale at 31 below
- crocker-land-1913-002 waypoint 6: land at 305 m — across to the north side of Bay Fiord; two white wolves follow the sledges
- crocker-land-1913-002 waypoint 24: land at 89 m — Blaamanden; eleven hours' sledging, a white wolf run down the ice
- crocker-land-1913-002 waypoint 29: land at 422 m — Payer Harbour; a box of peaches, pears and marmalade left by Doctor Hunt, and th
- crocker-land-1913-003 waypoint 8: land at 285 m — over the ice-cap and down to Bay Fiord; Oobloyah and Okpuddyshao turn back for E
- crocker-land-1913-004 waypoint 7: ice cap at 398 m — Bjornesundet; Panikpa and Koo-la-ting-wa are sent back to Etah with the musk-ox 
- crocker-land-1913-004 waypoint 22: land at 35 m — Bay Fiord, the hills crawling with Arctic hare; a day of rest and the Inughuit's
- franklin-search-023 waypoint 16: land at 65 m — within six miles of Parry's Winter Harbour and stopped by solid floe - 'the idea
- franklin-search-027 waypoint 0: land at 286 m — Kennedy and five men leave the ship at Batty Bay; Bellot follows a week later wi
- franklin-search-027 waypoint 5: land at 14 m — the fatigue party of eight turns back for the ship. Kennedy and Adamson trace th
- franklin-search-027 waypoint 15: land at 286 m — back on board at Batty Bay at 5 a.m. 'after an absence of ninety-seven days, dur
- franklin-search-068 waypoint 9: land at 19 m — entering the estuary at 4 a.m., about two hundred Inuvialuit come off in kayaks 
- franklin-search-136 waypoint 13: land at 5 m — comes to a dead stand ten miles east of Barlow Inlet: the besetment begins
- greenland-inughuit-016 waypoint 0: land at 20 m — the Tununirmiut country near Mittimatalik (Pond Inlet), where Qitdlarssuaq's vil
- greenland-inughuit-016 waypoint 1: ice cap at 706 m — north across Lancaster Sound / Tallurutiup Imanga on the ice
- greenland-inughuit-016 waypoint 6: ice cap at 447 m — Talbot Inlet: the party splits, Oqe turning back with twenty-four people
- greenland-inughuit-017 waypoint 4: ice cap at 473 m — south to Makinson Inlet, eastern Ellesmere: the first wintering after his death
- greenland-inughuit-017 waypoint 5: land at 165 m — a fish lake between Makinson Inlet and Baumann Fiord: famine, murder and canniba
- greenland-inughuit-043 waypoint 3: land at 230 m — through Flagler Bay and Sverdrup Pass (route after Cook; date approximate)
- greenland-inughuit-045 waypoint 3: land at 2 m — Chesterfield Inlet
- greenland-inughuit-045 waypoint 6: land at 1 m — Bernard Harbour, Coronation Gulf
- greenland-inughuit-045 waypoint 12: land at 0 m — Kotzebue Sound
- haig-thomas-1937-001 waypoint 5: ice cap at 789 m, 7 km from the ink; proposed 79.079 -79.710 (on land though the note names water; moved 7 km onto the printed route) — the Flagler-Bay Fiord crossing, some 40 miles of rocks; a tame herd of musk-oxen
- haig-thomas-1937-001 waypoint 16: land at 5 m, 13 km from the ink; proposed 78.131 -95.745 (inferred; moved 13 km onto the printed route) — the tide crack on the east coast of Amund Ringnes Island, the island visible ahe
- haig-thomas-1937-001 waypoint 20: land at 591 m, 10 km from the ink; proposed 78.316 -84.982 (on land though the note names water; moved 10 km onto the printed route) — Trold Fiord, crossed to on foot from Eureka Sound and recognised from 1935
- haig-thomas-1937-001 waypoint 21: land at 211 m, 2 km from the ink — four days searching the plateau south of Bay Fiord for the fossil bones Nukaping
- haig-thomas-1937-002 waypoint 6: land at 110 m — second crossing of Smith Sound completed and the loaded journey begins: two sled
- haig-thomas-1937-002 waypoint 19: land at 110 m — back at Fram Havn, the Smith Sound route now plainly marked by four parties' tra
- ice-shelves-and-ice-islands-005 waypoint 4: ice cap at 37 m — lodged in the sea ice north-west of Ayles Fiord and moving little; position appr
- inuit-oral-history-030 waypoint 4: land at 23 m — round the head of Committee Bay, which the chart shows as the southern end of th
- kane-hall-polaris-035 waypoint 16: land — latitude at noon reported 59 deg; the floe now entirely detached from the main p
- kane-hall-polaris-263 waypoint 4: sea, 17 km from the ink; proposed 78.950 -73.235 (inferred; moved 17 km onto the printed route) — twenty-two days out and about thirty miles from Cairn Point: three miles a day m
- kane-hall-polaris-263 waypoint 5: sea, 6 km from the ink; proposed 78.950 -73.235 (inferred; moved 6 km onto the printed route) — the main party sent back - 'I SENT the main party back this morning. The separat
- kane-hall-polaris-263 waypoint 6: sea, 19 km from the ink; proposed 79.317 -73.865 (inferred; moved 19 km onto the printed route) — within ten miles of the western shore by reckoning; names the two headlands ahea
- kane-hall-polaris-263 waypoint 15: sea, 7 km from the ink; proposed 79.546 -73.452 (inferred; moved 7 km onto the printed route) — Cape Hawks again after two marches from below Cape Napoleon, and back onto the o
- kane-hall-polaris-263 waypoint 16: sea, 9 km from the ink; proposed 78.538 -73.260 (inferred; moved 9 km onto the printed route) — adrift on an ice raft a mile off Cairn Point when the crack they had stepped ove
- kane-hall-polaris-263 waypoint 17: sea, 13 km from the ink; proposed 78.538 -73.260 (inferred; moved 13 km onto the printed route) — the ice foot gone below Cairn Point: the sledges are abandoned and the party cro
- karluk-cae-003 waypoint 9: land at 67 m — Stefansson climbs and names Leffingwell Crags and sees hills at least fifty mile
- karluk-cae-003 waypoint 15: land at 14 m — meets Kullak of the Minto Inlet people with his wife Neriyok and their children 
- karluk-cae-004 waypoint 15: land at 39 m — thirty hours of tidal observations near latitude 78 degrees 04 minutes north in 
- karluk-cae-007 waypoint 6: land at 29 m — north through Committee Bay to Pelly Bay and the Netsilingmiut; month only
- karluk-cae-008 waypoint 23: land at 27 m — a noon latitude is taken and Stefansson sets off alone on foot for Kellett, carr
- kruger-1930-001 waypoint 0: land at 220 m — Etah district: Krüger, Bjare and Akqioq set out across Smith Sound in early Marc
- kruger-1930-001 waypoint 3: land at 402 m — up Flagler Fiord and over the divide to Bay Fiord: the standard route, and the o
- kruger-1930-002 waypoint 5: land at 5 m — Craig Harbour: nobody had been there since Corporal McLean's visit a year before
- kruger-1930-003 waypoint 2: ice cap at 433 m — an advancing glacier now blocks the old route through the pass: loads packed 800
- kruger-1930-004 waypoint 15: ice cap at 473 m — head of Makinson Inlet; two days' rest, sledges and harness repaired
- kruger-1930-005 waypoint 1: land at 15 m — across the mouth of Croker Bay, west towards Cuming Inlet, with long detours rou
- kruger-1930-005 waypoint 4: ice cap at 657 m — an inlet followed 15 km to its head looking for a break in the cliffs; none foun
- kruger-1930-005 waypoint 5: land at 50 m — back at Dundas Harbour
- mcclure-investigator-006 waypoint 9: land at 348 m — crosses the Bay of Mercy and at 5 p.m. is within a hundred yards of HMS Investig
- mcclure-investigator-007 waypoint 0: land at 306 m — McClure leaves the Bay of Mercy to see Kellett in person rather than answer his 
- mcclure-investigator-007 waypoint 5: land at 306 m — back in the Bay of Mercy; the letter is read to the crew next morning, and only 
- mcclure-investigator-054 waypoint 0: land at 306 m — McClure and six men leave the Investigator in the Bay of Mercy with one sledge
- nares-greely-022 waypoint 1: sea, 6 km from the ink; proposed 82.812 -63.105 (inferred; moved 6 km onto the printed route) — Cape Joseph Henry: the party leaves the land for the polar pack; date approximat
- nares-greely-022 waypoint 2: sea, 9 km from the ink; proposed 83.294 -63.189 (inferred; moved 9 km onto the printed route) — farthest north, 83 deg 20 min 26 sec N, proclaimed at noon; longitude approximat
- nares-greely-022 waypoint 3: sea, 10 km from the ink; proposed 82.774 -63.158 (inferred; moved 10 km onto the printed route) — eleven of fifteen men down with scurvy; Parr sets out alone for the ship; positi
- nares-greely-022 waypoint 4: sea, 12 km from the ink; proposed 82.750 -63.214 (inferred; moved 12 km onto the printed route) — George Porter dies on the floe; position approximate
- nares-greely-039 waypoint 3: land at 173 m, 6 km from the ink; proposed 82.395 -61.212 (inferred; moved 6 km onto the printed route) — start from the Cape Rawson depot across Robeson Channel for the Greenland shore;
- nares-greely-039 waypoint 19: land at 4 m, 2 km from the ink — Charles Paul dies within sight of Polaris Bay; the printed narrative gives only 
- nares-greely-039 waypoint 20: land at 4 m, 2 km from the ink — Polaris Bay, Hall's Rest: the whole crew arrives with scurvy. Hans Hendrik's sea
- nares-greely-039 waypoint 21: land at 4 m, 2 km from the ink — after a gale, a start for Discovery Bay in a fifteen-foot ice-boat with the sled
- nares-greely-039 waypoint 22: sea, 14 km from the ink; proposed 81.596 -63.380 (inferred; moved 14 km onto the printed route) — the shore of Daly Peninsula between Cape Lieber and Cape Baird reached at 7 a.m.
- nares-greely-039 waypoint 23: sea, 16 km from the ink; proposed 81.824 -65.144 (inferred; moved 16 km onto the printed route) — after twenty-two hours' dragging across Lady Franklin Sound the party camps two 
- operation-hazen-1957-026 waypoint 2: land at 549 m — north end of Kennedy Channel, axis parallel to the channel; position inferred fr
- oxford-ellesmere-1934-002 waypoint 10: land at 156 m, 8 km from the ink; proposed 81.798 -70.540 (on land though the note names water; moved 8 km onto the printed route) — the east end of Lake Hazen after three days: the ice only four to five feet thic
- oxford-ellesmere-1934-002 waypoint 14: ice cap at 1520 m, 15 km from the ink; proposed 82.458 -72.546 (inferred; moved 15 km onto the printed route) — the summit climbed again in clear weather. Nukapinguaq points out through the gl
- oxford-ellesmere-1934-003 waypoint 11: ice cap at 188 m, 6 km from the ink; proposed 79.640 -76.983 (on land though the note names water; moved 6 km onto the printed route) — the Parrish Glacier at the head of the fjord: glare ice, the glacier itself almo
- oxford-ellesmere-1934-003 waypoint 18: land at 643 m, 6 km from the ink; proposed 79.138 -78.374 (on land though the note names water; moved 6 km onto the printed route) — up Flagler Fjord over glare ice in a wind so strong the sledge is blown sideways
- oxford-ellesmere-1934-003 waypoint 23: land at 35 m, 7 km from the ink; proposed 78.917 -83.275 (on land though the note names water; moved 7 km onto the printed route) — back to Bay Fiord, collecting fossil-bearing rocks near the divide and the rest 
- pole-seekers-from-ellesmere-030 waypoint 5: land — Markham Bay: survey poles aligned on the ice shelf as movement and ablation mark
- pole-seekers-from-ellesmere-030 waypoint 7: land at 75 m — back at Alert after five days, with a detour down Clements Markham Inlet
- posts-rcmp-missions-023 waypoint 0: land at 47 m, 124 km from the ink — leaves the Pond Inlet detachment at noon with Ululijarnaat and 14 dogs; Cst Frie
- posts-rcmp-missions-023 waypoint 2: land at 300 m, 8 km from the ink; proposed 73.489 -80.614 (on land though the note names water; moved 8 km onto the printed route) — opposite Tay Bay; a cache of walrus meat cannot be found
- rcmp-high-arctic-patrols-001 waypoint 2: ice cap at 400 m, 20 km from the ink; proposed 75.602 -82.132 (inferred; moved 20 km onto the printed route) — climbs the glacier from 6.30 a.m. by a zigzag course and strikes west along a hi
- rcmp-high-arctic-patrols-001 waypoint 3: ice cap at 1492 m, 17 km from the ink; proposed 75.321 -82.145 (inferred; moved 17 km onto the printed route) — the divide at noon: Ellesmere Island visible to the north, Lancaster Sound to th
- rcmp-high-arctic-patrols-001 waypoint 5: land at 50 m, 88 km from the ink — Dundas Harbour: Constables Anstead, Maisonneuve and Makinson found in good healt
- rcmp-high-arctic-patrols-001 waypoint 6: land at 50 m, 88 km from the ink — leaves at 9 a.m. with Anstead, Maisonneuve and the Inuk Klishook and thirteen do
- rcmp-high-arctic-patrols-001 waypoint 11: land at 5 m, 31 km from the ink — Craig Harbour at 4 a.m. 340 miles in 19 days
- rcmp-high-arctic-patrols-002 waypoint 0: land at 5 m, 32 km from the ink — leaves Craig Harbour with Constable Dersch and Nukapinguaq; Constable Bain comes
- rcmp-high-arctic-patrols-002 waypoint 2: land at 566 m, 61 km from the ink — Baad Fiord; deep soft snow (position approximate)
- rcmp-high-arctic-patrols-002 waypoint 5: land at 591 m, 34 km from the ink — Trold Fiord; a gale, and Nukapinguaq strains his back on the crossing
- rcmp-high-arctic-patrols-002 waypoint 13: land at 114 m, 55 km from the ink — the head of Goose Fiord at 10.30 a.m.
- rcmp-high-arctic-patrols-002 waypoint 15: land at 375 m, 44 km from the ink — Haven Fiord; picks up a Fram record of 1899 (position approximate)
- rcmp-high-arctic-patrols-002 waypoint 16: land at 5 m, 32 km from the ink — Craig Harbour at 4 a.m. 975 miles in 40 days
- rcmp-high-arctic-patrols-003 waypoint 17: land at 278 m, 94 km from the ink — Eureka Sound; wolves eat the provisions in the night and two are shot
- rcmp-high-arctic-patrols-004 waypoint 1: land at 85 m, 50 km from the ink — Rice Strait: meet Akkommodingwa and his wife coming over from Etah, who report S
- rcmp-high-arctic-patrols-004 waypoint 7: land at 5 m, 32 km from the ink — Craig Harbour at 4 a.m. Bears had eaten the meat boxes; a note from G. P. Putnam
- rcmp-high-arctic-patrols-004 waypoint 8: land at 5 m, 32 km from the ink — leaves Craig Harbour in the afternoon
- rcmp-high-arctic-patrols-004 waypoint 10: sea, 18 km from the ink; proposed 77.911 -75.529 (inferred; moved 18 km onto the printed route) — a large bear; Oodee shoots two of his best dogs in a fit of temper (position app
- rcmp-high-arctic-patrols-005 waypoint 1: land at 37 m, 23 km from the ink; proposed 78.425 -74.287 (inferred; moved 23 km onto the printed route) — Cape Herschel; rough ice, drifting ice off Cape Isabella (date approximate)
- rcmp-high-arctic-patrols-005 waypoint 4: land at 5 m, 32 km from the ink — Craig Harbour
- rcmp-high-arctic-patrols-007 waypoint 14: land at 278 m, 40 km from the ink — Eureka Sound
- rcmp-high-arctic-patrols-008 waypoint 7: land at 5 m, 32 km from the ink — Craig Harbour at midnight, by way of Smith Bay; four bears shot on the way
- rcmp-high-arctic-patrols-008 waypoint 10: sea, 12 km from the ink; proposed 78.265 -74.581 (inferred; moved 12 km onto the printed route) — Cape Isabella; a komatik broken and repaired (date approximate)
- rcmp-high-arctic-patrols-009 waypoint 0: land at 50 m, 12 km from the ink — Corporal Timbury, Constable Hamilton and the hunter Keepomee leave Dundas Harbou
- rcmp-high-arctic-patrols-009 waypoint 4: land at 50 m, 12 km from the ink — Dundas Harbour. 750 miles in 34 days
- rcmp-high-arctic-patrols-010 waypoint 4: land at 84 m, 14 km from the ink; proposed 77.918 -75.469 (inferred; moved 14 km onto the printed route) — near Boger Point Stallworthy follows a bear's tracks along the foot of a glacier
- rcmp-high-arctic-patrols-010 waypoint 6: ice cap at 705 m, 23 km from the ink; proposed 76.127 -79.325 (inferred; moved 23 km onto the printed route) — rounds Cobourg Island; a bear killed and the dogs fed. A blizzard in Glacier Str
- rcmp-high-arctic-patrols-010 waypoint 7: land at 5 m, 32 km from the ink — Craig Harbour about midnight, two komatiks with broken handles and a third with 
- rcmp-high-arctic-patrols-010 waypoint 8: land at 5 m, 32 km from the ink — leaves Craig Harbour about midnight
- rock-and-the-sverdrup-basin-702 waypoint 1: land at 560 m — Tozer and Amagualik leave for a lake in the Sawtooth Range, forty-eight miles so
- rock-and-the-sverdrup-basin-702 waypoint 4: land at 0 m — five days at Buchanan Lake, southwest of the head of Mokka Fiord; the Buchanan L
- ross-victory-003 waypoint 8: land at 286 m — Batty Bay and the boats, in six days; the sick begin to recover
- science-stations-073 waypoint 3: land at 451 m — the permanent base site chosen at the head of the fiord the party would name Exp
- science-stations-074 waypoint 4: ice cap at 1686 m — the Upper Ice Station opens near the summit of the ice cap at 1,700 m
- sverdrup-bernier-peary-003 waypoint 0: land at 248 m — leave the Fram in Goose Fiord with the other sledge parties on Easter Monday and
- sverdrup-bernier-peary-003 waypoint 3: land at 133 m — the high mountain proves to be the north end of North Cornwall; they name Hendri
- sverdrup-bernier-peary-178 waypoint 6: land at 83 m — at midnight they stumble through the dilapidated door of Fort Conger; pulling of
- sverdrup-bernier-peary-180 waypoint 10: land at 83 m — Fort Conger, 300 miles from Payer Harbour in twelve marches. Four days of overha
- sverdrup-bernier-peary-183 waypoint 1: land at 238 m — Port Bowen, Prince Regent Inlet. Reached after crossing the Brodeur Peninsula, 1
- sverdrup-bernier-peary-183 waypoint 4: land at 121 m — "Bourassa bay," Prince Regent Inlet. Explicit observation; bay newly named by La
- sverdrup-bernier-peary-194 waypoint 6: land — M'Clintock Bay, crossed in one long march over both its arms. Date approximate
- sverdrup-bernier-peary-300 waypoint 0: land at 110 m, 4 km from the ink — Sverdrup, Isachsen, Stolz and Bay leave the Fram at Fram Havn; the mate Oluf Raa
- sverdrup-bernier-peary-300 waypoint 2: land at 629 m, 2 km from the ink — thirty-eight miles in one day over favourable ice to the sands at the head of No
- sverdrup-bernier-peary-300 waypoint 3: land at 629 m, 2 km from the ink — Hassel and Isachsen take a meridian altitude at the head of the fiord; Sverdrup,
- sverdrup-bernier-peary-300 waypoint 4: land at 515 m, 4 km from the ink — up the valley that trends west at an even gradient from the head of Flagler Bay,
- sverdrup-bernier-peary-300 waypoint 5: land at 448 m, 3 km from the ink — Sverdrup and Bay leave the sledges at the glacier and the tarn and go on with th
- sverdrup-bernier-peary-300 waypoint 6: land at 225 m, 4 km from the ink — three in the morning at the outer edge of the sands; in the afternoon, from a co
- sverdrup-bernier-peary-300 waypoint 7: land at 225 m, 4 km from the ink — the fiord below is named Bay Fjord for the zoologist Edvard Bay; a herd of musk 
- sverdrup-bernier-peary-300 waypoint 9: land at 672 m, 10 km from the ink; proposed 79.030 -76.882 (on land though the note names water; moved 10 km onto the printed route) — down Flagler Bay and along the ice-foot of Hayes Sound
- sverdrup-bernier-peary-301 waypoint 10: ice cap at 209 m, 0 km from the ink — at the end of Jokelfjord in the evening and at the top of the Leffert Glacier at
- sverdrup-bernier-peary-302 waypoint 30: land at 134 m — on the north side of a bay the two men decide to turn: the dogs are failing
- sverdrup-bernier-peary-303 waypoint 3: land at 260 m — clear weather brings them into Baumann Fjord by nightfall
- sverdrup-bernier-peary-303 waypoint 6: land at 194 m — an observation in the innermost arm of Baumann Fjord, afterwards Vendomfjord, gi
- sverdrup-bernier-peary-303 waypoint 13: land at 567 m — a three-hour bear chase in the morning; in the afternoon a long fiord opens to t
- sverdrup-bernier-peary-303 waypoint 15: land at 721 m — seventeen miles up Troldfjord, with a small bear killed and fed to the four team
- sverdrup-bernier-peary-303 waypoint 17: land at 726 m — a narrow opening at the head of Troldfjord turns out to be no passage; musk oxen
- sverdrup-bernier-peary-303 waypoint 33: land at 285 m — down the east side of the sound to a little bay south of a steep promontory
- sverdrup-bernier-peary-304 waypoint 0: land at 10 m — all three spring parties leave the Fram in Gaasefjord; Sverdrup and Schei are bo
- sverdrup-bernier-peary-304 waypoint 21: land at 557 m — the interior of Bay Fjord in the evening
- sverdrup-bernier-peary-304 waypoint 31: land at 37 m — across the bay in a ten-hour march to a large sandbank on its south side
- sverdrup-bernier-peary-304 waypoint 33: land at 10 m — south through the nearly snow-free Gaasedalen to the fiord ice and aboard the Fr
- thule-dorset-001 waypoint 4: land at 11 m — Kugaaruk and Committee Bay, at the head of the Gulf of Boothia
- thule-dorset-001 waypoint 6: land at 8 m — Iglulik and northern Foxe Basin: walrus and bowhead, and the raised beaches that
- thule-dorset-001 waypoint 7: land at 47 m — Mittimatalik (Pond Inlet) and Lancaster Sound
- wrecks-disasters-038 waypoint 3: land at 30 m — inferred; approaching the mouth of Hudson Strait
