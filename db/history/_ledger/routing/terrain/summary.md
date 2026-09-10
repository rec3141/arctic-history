# Routing the overland tracks through the terrain

2026-09-10 00:57 — 1 tracks routed in 1 s, 101 on file from this and earlier runs. Command: `python tools/digitize-tracks.py route --track haig-thomas-1937-001 --write`

**Written to the database.**

## The DEM

Copernicus GLO-90, mosaicked at 250 m in `+proj=stere +lat_0=90 +lat_ts=78 +lon_0=-85 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs` (10860 x 5593 cells), with land from GSHHG full resolution and ice from Natural Earth 10 m glaciated areas.  See the tool's docstring for the cost surface.

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

Maps in the candidate list without a fit: **kruger-1930-027**: Krüger's own sketch of the route he intended, not the one he took: nothing to route.; **kruger-1930-061**: the 1957 Geological Survey sledge journey to Meighen Island has no track artifact yet.; **nares-greely-204**: Lockwood's chart of his March to April 1883 journey north from Fort Conger; the only 1883 track in the database is the August retreat (nares-greely-025), which this map does not show.; **sverdrup-bernier-peary-154**: the Falcon's 1893 voyage to Bowdoin Bay is a ship's track, the sea router's.


## The grades

- **recommend** — every leg routed inside the DEM, and where a printed map was digitized at least half the legs follow its ink: a line to write back once the owner has looked at it.
- **review** — some legs fall outside the DEM (great circles there, which is right over the sea ice) or fewer than half follow the ink.
- **same** — the routed line is the database's line to within 3 km: nothing to write back.
- **outside** — every leg outside the DEM: not this tool's track.
- **written** — already in the database with this line, flagged terrain.

outside: 15 · recommend: 52 · review: 33 · same: 1

## Every track

| track | grade | legs | from ink | routed km | straight km | land km | ice km | highest m | from db line, max km | moved | s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cook-1908-axel-heiberg-001 | recommend | 12 | 6 | 680 | 593 | 137 | 0 | 991 | 19 | 0 | 0.3 |
| cook-1908-axel-heiberg-002 | recommend | 10 | 10 | 949 | 798 | 332 | 6 | 434 | 28 | 0 | 0.7 |
| cook-1908-axel-heiberg-003 | recommend | 5 | 0 | 541 | 486 | 1 | 0 | 38 | 33 | 0 | 0.5 |
| crocker-land-1913-002 | recommend | 30 | 0 | 2,258 | 1,907 | 325 | 60 | 1473 | 39 | 0 | 2.6 |
| crocker-land-1913-003 | recommend | 28 | 0 | 1,834 | 1,421 | 563 | 9 | 825 | 32 | 0 | 0.9 |
| crocker-land-1913-004 | recommend | 26 | 0 | 2,393 | 1,738 | 636 | 23 | 817 | 60 | 0 | 1.8 |
| franklin-search-021 | recommend | 6 | 0 | 1,222 | 1,091 | 87 | 0 | 171 | 75 | 0 | 1.4 |
| franklin-search-067 | recommend | 6 | 0 | 425 | 353 | 22 | 0 | 212 | 40 | 0 | 0.3 |
| franklin-search-082 | recommend | 14 | 0 | 1,297 | 1,100 | 317 | 0 | 310 | 46 | 0 | 1.0 |
| franklin-search-086 | recommend | 13 | 0 | 572 | 443 | 146 | 0 | 333 | 20 | 0 | 0.3 |
| greenland-inughuit-017 | recommend | 6 | 0 | 1,101 | 604 | 739 | 46 | 523 | 133 | 0 | 1.3 |
| greenland-inughuit-042 | recommend | 9 | 0 | 1,482 | 1,247 | 158 | 18 | 893 | 38 | 0 | 2.4 |
| greenland-inughuit-043 | recommend | 14 | 0 | 2,142 | 1,537 | 686 | 90 | 1442 | 84 | 0 | 1.9 |
| haig-thomas-1937-001 | recommend | 24 | 24 | 1,610 | 1,366 | 386 | 134 | 1842 | 16 | 2 | 0.8 |
| haig-thomas-1937-002 | recommend | 20 | 0 | 1,050 | 883 | 58 | 48 | 492 | 42 | 0 | 0.6 |
| kane-hall-polaris-002 | recommend | 12 | 0 | 1,005 | 929 | 140 | 50 | 506 | 16 | 0 | 0.9 |
| kruger-1930-001 | recommend | 21 | 0 | 1,476 | 1,262 | 157 | 7 | 406 | 42 | 0 | 0.9 |
| kruger-1930-002 | recommend | 7 | 0 | 1,079 | 857 | 66 | 0 | 563 | 58 | 0 | 0.9 |
| kruger-1930-003 | recommend | 22 | 0 | 1,617 | 1,367 | 195 | 3 | 433 | 35 | 0 | 1.1 |
| kruger-1930-004 | recommend | 19 | 0 | 1,316 | 1,080 | 225 | 31 | 473 | 34 | 0 | 0.8 |
| kruger-1930-005 | recommend | 5 | 0 | 278 | 208 | 65 | 5 | 658 | 21 | 0 | 0.1 |
| mcclure-investigator-006 | recommend | 12 | 0 | 729 | 583 | 260 | 0 | 380 | 25 | 0 | 0.5 |
| mcclure-investigator-007 | recommend | 5 | 0 | 637 | 571 | 99 | 0 | 380 | 32 | 0 | 1.1 |
| mcclure-investigator-008 | recommend | 4 | 0 | 325 | 288 | 165 | 0 | 380 | 24 | 0 | 0.2 |
| mcclure-investigator-009 | recommend | 31 | 0 | 1,369 | 1,149 | 401 | 0 | 235 | 31 | 0 | 0.7 |
| mcclure-investigator-010 | recommend | 23 | 0 | 1,459 | 1,277 | 273 | 0 | 227 | 34 | 0 | 1.0 |
| mcclure-investigator-011 | recommend | 8 | 0 | 626 | 550 | 89 | 0 | 215 | 56 | 0 | 0.7 |
| mcclure-investigator-012 | recommend | 5 | 0 | 217 | 206 | 0 | 0 | 0 | 9 | 0 | 0.1 |
| mcclure-investigator-013 | recommend | 5 | 0 | 330 | 304 | 25 | 0 | 212 | 31 | 0 | 0.3 |
| mcclure-investigator-054 | recommend | 3 | 0 | 254 | 227 | 152 | 0 | 380 | 25 | 0 | 0.2 |
| nares-greely-022 | recommend | 5 | 0 | 227 | 213 | 0 | 0 | 0 | 9 | 0 | 0.1 |
| nares-greely-023 | recommend | 5 | 0 | 897 | 790 | 49 | 0 | 823 | 38 | 0 | 1.0 |
| nares-greely-025 | recommend | 9 | 0 | 514 | 416 | 130 | 0 | 965 | 25 | 0 | 0.5 |
| nares-greely-038 | recommend | 24 | 0 | 1,091 | 786 | 403 | 13 | 541 | 20 | 0 | 0.8 |
| nares-greely-039 | recommend | 24 | 0 | 652 | 584 | 37 | 3 | 774 | 26 | 0 | 0.4 |
| operation-hazen-1957-041 | recommend | 6 | 0 | 661 | 617 | 69 | 0 | 28 | 15 | 0 | 0.9 |
| operation-hazen-1957-042 | recommend | 9 | 0 | 511 | 445 | 48 | 1 | 395 | 16 | 0 | 0.3 |
| oxford-ellesmere-1934-002 | recommend | 21 | 18 | 1,685 | 1,304 | 478 | 162 | 1798 | 56 | 0 | 0.9 |
| oxford-ellesmere-1934-003 | recommend | 28 | 27 | 1,498 | 1,214 | 518 | 81 | 1111 | 29 | 0 | 0.8 |
| oxford-ellesmere-1934-004 | recommend | 26 | 17 | 890 | 724 | 94 | 6 | 747 | 11 | 0 | 0.4 |
| pole-seekers-from-ellesmere-030 | recommend | 7 | 0 | 414 | 339 | 56 | 1 | 306 | 24 | 0 | 0.2 |
| pole-seekers-from-ellesmere-031 | recommend | 5 | 0 | 131 | 115 | 85 | 1 | 87 | 5 | 0 | 0.1 |
| rcmp-high-arctic-patrols-003 | recommend | 20 | 10 | 1,888 | 1,575 | 672 | 143 | 1505 | 25 | 0 | 1.2 |
| rcmp-high-arctic-patrols-005 | recommend | 7 | 4 | 952 | 712 | 103 | 99 | 1235 | 61 | 0 | 1.0 |
| rcmp-high-arctic-patrols-006 | recommend | 14 | 7 | 1,325 | 1,064 | 512 | 150 | 1505 | 29 | 0 | 1.1 |
| rcmp-high-arctic-patrols-008 | recommend | 11 | 8 | 1,369 | 1,029 | 390 | 156 | 1235 | 33 | 0 | 0.8 |
| rcmp-high-arctic-patrols-009 | recommend | 4 | 3 | 849 | 753 | 98 | 0 | 285 | 58 | 0 | 1.0 |
| rcmp-high-arctic-patrols-010 | recommend | 11 | 6 | 1,286 | 944 | 34 | 23 | 705 | 53 | 0 | 0.9 |
| sverdrup-bernier-peary-003 | recommend | 16 | 0 | 1,474 | 1,275 | 507 | 0 | 457 | 37 | 0 | 1.8 |
| sverdrup-bernier-peary-178 | recommend | 8 | 0 | 691 | 621 | 3 | 0 | 83 | 38 | 0 | 0.9 |
| sverdrup-bernier-peary-180 | recommend | 27 | 0 | 1,612 | 1,402 | 19 | 0 | 464 | 44 | 0 | 2.0 |
| sverdrup-bernier-peary-194 | recommend | 18 | 0 | 1,441 | 1,156 | 550 | 4 | 283 | 29 | 0 | 1.4 |
| franklin-search-022 | review | 7 | 0 | 224 | 576 | 5 | 0 | 171 | 10 | 0 | 0.1 |
| franklin-search-023 | review | 25 | 0 | 2,303 | 11,702 | 488 | 0 | 244 | 67 | 0 | 3.9 |
| franklin-search-027 | review | 15 | 0 | 190 | 1,029 | 0 | 0 | 0 | 15 | 0 | 0.2 |
| greenland-inughuit-016 | review | 9 | 0 | 1,133 | 1,188 | 551 | 101 | 1033 | 56 | 0 | 1.1 |
| kane-hall-polaris-035 | review | 27 | 0 | 540 | 3,216 | 36 | 3 | 227 | 44 | 0 | 0.6 |
| kane-hall-polaris-263 | review | 18 | 14 | 584 | 495 | 4 | 0 | 391 | 22 | 0 | 0.3 |
| karluk-cae-002 | review | 14 | 0 | 171 | 1,138 | 12 | 0 | 0 | 6 | 0 | 0.1 |
| karluk-cae-003 | review | 17 | 0 | 1,446 | 1,953 | 112 | 0 | 105 | 32 | 0 | 2.9 |
| karluk-cae-004 | review | 24 | 0 | 2,392 | 2,404 | 525 | 0 | 295 | 48 | 0 | 2.7 |
| karluk-cae-008 | review | 24 | 0 | 2,319 | 2,192 | 516 | 0 | 82 | 49 | 0 | 3.9 |
| mcclure-investigator-014 | review | 4 | 0 | 306 | 4,559 | 12 | 0 | 16 | 46 | 0 | 0.6 |
| operation-hazen-1957-026 | review | 11 | 0 | 834 | 4,674 | 129 | 0 | 552 | 245 | 0 | 1.1 |
| pole-seekers-from-ellesmere-006 | review | 10 | 0 | 471 | 1,670 | 0 | 0 | 6 | 14 | 0 | 0.4 |
| pole-seekers-from-ellesmere-007 | review | 6 | 0 | 311 | 1,096 | 3 | 0 | 283 | 24 | 0 | 0.4 |
| pole-seekers-from-ellesmere-038 | review | 5 | 0 | 851 | 2,015 | 6 | 1 | 146 | 456 | 0 | 1.1 |
| pole-seekers-from-ellesmere-039 | review | 6 | 0 | 248 | 2,476 | 14 | 0 | 31 | 526 | 0 | 0.2 |
| qei-from-the-air-1947-023 | review | 7 | 0 | 1,343 | 7,673 | 144 | 42 | 1639 | 1032 | 0 | 4.0 |
| qei-from-the-air-1947-024 | review | 10 | 0 | 2,271 | 13,866 | 1,294 | 774 | 362 | 439 | 0 | 3.9 |
| rcmp-high-arctic-patrols-001 | review | 11 | 5 | 693 | 549 | 273 | 251 | 1909 | 28 | 0 | 0.3 |
| rcmp-high-arctic-patrols-002 | review | 16 | 7 | 1,498 | 1,110 | 346 | 0 | 591 | 45 | 0 | 1.1 |
| rcmp-high-arctic-patrols-004 | review | 13 | 5 | 998 | 776 | 3 | 0 | 85 | 53 | 0 | 0.7 |
| rcmp-high-arctic-patrols-007 | review | 16 | 7 | 2,368 | 2,093 | 664 | 85 | 1505 | 45 | 0 | 4.4 |
| science-stations-003 | review | 7 | 0 | 498 | 3,292 | 0 | 0 | 1 | 41 | 0 | 0.7 |
| science-stations-029 | review | 4 | 0 | 488 | 2,037 | 0 | 0 | 0 | 30 | 0 | 0.5 |
| science-stations-073 | review | 5 | 0 | 1,422 | 4,697 | 1,217 | 33 | 929 | 191 | 0 | 1.5 |
| science-stations-074 | review | 5 | 0 | 254 | 4,066 | 219 | 140 | 1742 | 204 | 0 | 0.2 |
| st-roch-modern-055 | review | 10 | 0 | 2,200 | 14,992 | 159 | 0 | 81 | 2632 | 0 | 3.7 |
| sverdrup-bernier-peary-035 | review | 5 | 0 | 107 | 1,532 | 0 | 0 | 1 | 9 | 0 | 0.1 |
| sverdrup-bernier-peary-179 | review | 31 | 0 | 1,797 | 1,810 | 159 | 1 | 886 | 14 | 0 | 1.7 |
| sverdrup-bernier-peary-193 | review | 11 | 0 | 576 | 1,181 | 20 | 0 | 663 | 19 | 0 | 0.4 |
| sverdrup-bernier-peary-300 | review | 11 | 8 | 388 | 297 | 185 | 1 | 734 | 11 | 0 | 0.2 |
| sverdrup-bernier-peary-301 | review | 11 | 9 | 372 | 256 | 279 | 260 | 1625 | 18 | 0 | 0.2 |
| thule-dorset-001 | review | 9 | 0 | 102 | 4,434 | 4 | 0 | 220 | 10 | 0 | 0.1 |
| posts-rcmp-missions-023 | same | 17 | 7 | 84 | 745 | 0 | 0 | 0 | 2 | 0 | 0.0 |
| amundsen-gjoa-002 | outside | 7 | 0 | 0 | 1,288 | 0 | 0 | 0 | 0 | 0 | 0.0 |
| franklin-1845-002 | outside | 4 | 0 | 0 | 216 | 0 | 0 | 0 | 0 | 0 | 0.0 |
| franklin-search-068 | outside | 22 | 0 | 0 | 9,698 | 0 | 0 | 0 | 0 | 0 | 0.0 |
| greenland-inughuit-045 | outside | 13 | 0 | 0 | 6,528 | 0 | 0 | 0 | 0 | 0 | 0.0 |
| hudson-strait-south-baffin-015 | outside | 8 | 0 | 0 | 535 | 0 | 0 | 0 | 0 | 0 | 0.0 |
| inuit-oral-history-029 | outside | 8 | 0 | 0 | 554 | 0 | 0 | 0 | 0 | 0 | 0.0 |
| inuit-oral-history-030 | outside | 6 | 0 | 0 | 461 | 0 | 0 | 0 | 0 | 0 | 0.0 |
| karluk-cae-005 | outside | 11 | 0 | 0 | 1,109 | 0 | 0 | 0 | 0 | 0 | 0.0 |
| karluk-cae-006 | outside | 7 | 0 | 0 | 1,768 | 0 | 0 | 0 | 0 | 0 | 0.0 |
| karluk-cae-007 | outside | 19 | 0 | 0 | 10,103 | 0 | 0 | 0 | 15 | 0 | 0.0 |
| ross-victory-002 | outside | 6 | 0 | 0 | 219 | 0 | 0 | 0 | 21 | 0 | 0.0 |
| ross-victory-003 | outside | 16 | 0 | 0 | 5,538 | 0 | 0 | 0 | 0 | 0 | 0.0 |
| science-stations-030 | outside | 1 | 0 | 0 | 687 | 0 | 0 | 0 | 0 | 0 | 0.0 |
| sverdrup-bernier-peary-183 | outside | 13 | 0 | 0 | 1,104 | 0 | 0 | 0 | 2 | 0 | 0.0 |
| wrecks-disasters-038 | outside | 5 | 0 | 0 | 1,502 | 0 | 0 | 0 | 0 | 0 | 0.0 |

## Verdicts

- **cook-1908-axel-heiberg-001** (recommend) — Annoatok to Cape Stallworthy, February-March 1908  
  6 of 12 legs follow ink digitized from cook-1908-axel-heiberg-041 (georef rms 2.8 km), 1 chained through hachures or lettering and doubted; the routed line runs 2.6 km from the printed one on average; 680 km routed against 593 km straight, 137 km over land, 0 km over ice cap, highest 991 m; the line in the database is 593 km and 26 points; this one 80 points; proposed moves, not applied: 11 (inferred; moved 23 km onto the printed route); it runs 4.7 km from the line in the database on average and 19 km at most
- **cook-1908-axel-heiberg-002** (recommend) — Back to land: Hassel Sound to Cape Sparbo, June-September 1908  
  10 of 10 legs follow ink digitized from cook-1908-axel-heiberg-041 (georef rms 2.8 km); the routed line runs 2.2 km from the printed one on average; 949 km routed against 798 km straight, 332 km over land, 6 km over ice cap, highest 434 m; the line in the database is 798 km and 37 points; this one 110 points; waypoints on land whose note names water: 5; proposed moves, not applied: 2 (inferred; moved 7 km onto the printed route); 5 (inferred; moved 9 km onto the printed route); 6 (inferred; moved 15 km onto the printed route); it runs 7.4 km from the line in the database on average and 28 km at most
- **cook-1908-axel-heiberg-003** (recommend) — Cape Sparbo to Annoatok, February-April 1909  
  541 km routed against 486 km straight, 1 km over land, 0 km over ice cap, highest 38 m; the line in the database is 486 km and 23 points; this one 41 points; it runs 12.3 km from the line in the database on average and 33 km at most
- **crocker-land-1913-002** (recommend) — The search for Crocker Land: Etah to 82 30 N and back, February to May 1914  
  2,258 km routed against 1,907 km straight, 325 km over land, 60 km over ice cap, highest 1473 m; the line in the database is 1,907 km and 86 points; this one 226 points; waypoints on land whose note names water: 4, 6, 24, 29; it runs 5.2 km from the line in the database on average and 39 km at most
- **crocker-land-1913-003** (recommend) — Ekblaw across Ellesmere and Grant Land, March to June 1915  
  1,834 km routed against 1,421 km straight, 563 km over land, 9 km over ice cap, highest 825 m; the line in the database is 1,421 km and 63 points; this one 232 points; waypoints on land whose note names water: 8; it runs 7.1 km from the line in the database on average and 32 km at most
- **crocker-land-1913-004** (recommend) — MacMillan to King Christian Island and North Cornwall, March to May 1916  
  2,393 km routed against 1,738 km straight, 636 km over land, 23 km over ice cap, highest 817 m; the line in the database is 1,738 km and 78 points; this one 289 points; waypoints on land whose note names water: 22; it runs 10.4 km from the line in the database on average and 60 km at most
- **franklin-search-021** (recommend) — McClintock's sledge journey to Melville Island, April-July 1851  
  1,222 km routed against 1,091 km straight, 87 km over land, 0 km over ice cap, highest 171 m; the line in the database is 1,091 km and 53 points; this one 62 points; it runs 25.3 km from the line in the database on average and 75 km at most
- **franklin-search-067** (recommend) — Penny's dog-sledge journey to the head of Wellington Channel, May 1851  
  425 km routed against 353 km straight, 22 km over land, 0 km over ice cap, highest 212 m; the line in the database is 353 km and 16 points; this one 46 points; it runs 12.6 km from the line in the database on average and 40 km at most
- **franklin-search-082** (recommend) — Commander Richards's sledge journey from Northumberland Sound to the Resolute, April-July 1853  
  1,297 km routed against 1,100 km straight, 317 km over land, 0 km over ice cap, highest 310 m; the line in the database is 1,100 km and 51 points; this one 109 points; it runs 11.1 km from the line in the database on average and 46 km at most
- **franklin-search-086** (recommend) — Belcher's own north-east sledge journey, 2 May to 23 June 1853  
  572 km routed against 443 km straight, 146 km over land, 0 km over ice cap, highest 333 m; the line in the database is 443 km and 19 points; this one 83 points; it runs 4.7 km from the line in the database on average and 20 km at most
- **greenland-inughuit-017** (recommend) — The return that failed, about 1870 to 1873  
  1,101 km routed against 604 km straight, 739 km over land, 46 km over ice cap, highest 523 m; the line in the database is 604 km and 30 points; this one 156 points; waypoints on land whose note names water: 5; it runs 36.6 km from the line in the database on average and 133 km at most
- **greenland-inughuit-042** (recommend) — The Crocker Land sledge journey, February to May 1914  
  1,482 km routed against 1,247 km straight, 158 km over land, 18 km over ice cap, highest 893 m; the line in the database is 1,247 km and 59 points; this one 112 points; it runs 14.0 km from the line in the database on average and 38 km at most
- **greenland-inughuit-043** (recommend) — Ahwelah and Etukishook with Cook, February 1908 to April 1909  
  2,142 km routed against 1,537 km straight, 686 km over land, 90 km over ice cap, highest 1442 m; the line in the database is 1,537 km and 72 points; this one 234 points; waypoints on land whose note names water: 3; it runs 21.4 km from the line in the database on average and 84 km at most
- **haig-thomas-1937-001** (recommend) — Haig-Thomas and Nukapinguaq, Etah to Amund Ringnes Island and back, 1938  
  24 of 24 legs follow ink digitized from haig-thomas-1937-059 (georef rms 6.0 km); the routed line runs 2.5 km from the printed one on average; 1,610 km routed against 1,366 km straight, 386 km over land, 134 km over ice cap, highest 1842 m; the line in the database is 1,518 km and 217 points; this one 207 points; waypoints on land whose note names water: 20, 21; waypoints moved: 8 (the note says down Eureka Sound but the point sat 2 km inside the Ellesmere shore; moved 11 km onto the route drawn down the sound); 22 (position inferred; the printed map draws the return south of the outward crossing, over the ice cap at about 1600 m, and the waypoint is moved 30 km south onto that drawn line); proposed moves, not applied: 16 (inferred; moved 13 km onto the printed route); 20 (on land though the note names water; moved 10 km onto the printed route); it runs 1.2 km from the line in the database on average and 16 km at most
- **haig-thomas-1937-002** (recommend) — Wright and Hamilton, the survey of south-east Ellesmere Island, 1938  
  1,050 km routed against 883 km straight, 58 km over land, 48 km over ice cap, highest 492 m; the line in the database is 883 km and 39 points; this one 120 points; waypoints on land whose note names water: 6, 19; it runs 7.0 km from the line in the database on average and 42 km at most
- **kane-hall-polaris-002** (recommend) — The boat retreat from Rensselaer Harbour to Upernavik, 1855  
  1,005 km routed against 929 km straight, 140 km over land, 50 km over ice cap, highest 506 m; the line in the database is 929 km and 43 points; this one 76 points; it runs 5.1 km from the line in the database on average and 16 km at most
- **kruger-1930-001** (recommend) — The German Arctic Expedition, March to May 1930  
  1,476 km routed against 1,262 km straight, 157 km over land, 7 km over ice cap, highest 406 m; the line in the database is 1,262 km and 57 points; this one 156 points; waypoints on land whose note names water: 0, 3; it runs 6.9 km from the line in the database on average and 42 km at most
- **kruger-1930-002** (recommend) — Stallworthy's first search, 1931  
  1,079 km routed against 857 km straight, 66 km over land, 0 km over ice cap, highest 563 m; the line in the database is 857 km and 40 points; this one 80 points; waypoints on land whose note names water: 5; it runs 12.3 km from the line in the database on average and 58 km at most
- **kruger-1930-003** (recommend) — Stallworthy's search around Axel Heiberg Island, 1932  
  1,617 km routed against 1,367 km straight, 195 km over land, 3 km over ice cap, highest 433 m; the line in the database is 1,367 km and 62 points; this one 168 points; it runs 8.1 km from the line in the database on average and 35 km at most
- **kruger-1930-004** (recommend) — Hamilton's search patrol, 1932  
  1,316 km routed against 1,080 km straight, 225 km over land, 31 km over ice cap, highest 473 m; the line in the database is 1,080 km and 46 points; this one 148 points; it runs 7.1 km from the line in the database on average and 34 km at most
- **kruger-1930-005** (recommend) — Dersch's Devon Island search patrol, 1932  
  278 km routed against 208 km straight, 65 km over land, 5 km over ice cap, highest 658 m; the line in the database is 208 km and 10 points; this one 40 points; waypoints on land whose note names water: 1, 5; it runs 7.8 km from the line in the database on average and 21 km at most
- **mcclure-investigator-006** (recommend) — Pim's sledge journey from HMS Resolute to the Investigator, March-April 1853  
  729 km routed against 583 km straight, 260 km over land, 0 km over ice cap, highest 380 m; the line in the database is 583 km and 27 points; this one 87 points; waypoints on land whose note names water: 9; it runs 9.1 km from the line in the database on average and 25 km at most
- **mcclure-investigator-007** (recommend) — McClure crosses to HMS Resolute and back, April-May 1853  
  637 km routed against 571 km straight, 99 km over land, 0 km over ice cap, highest 380 m; the line in the database is 571 km and 30 points; this one 38 points; waypoints on land whose note names water: 0, 5; it runs 14.3 km from the line in the database on average and 32 km at most
- **mcclure-investigator-008** (recommend) — The Investigator's crew walk from Mercy Bay to the Resolute, June 1853  
  325 km routed against 288 km straight, 165 km over land, 0 km over ice cap, highest 380 m; the line in the database is 288 km and 14 points; this one 34 points; it runs 6.4 km from the line in the database on average and 24 km at most
- **mcclure-investigator-009** (recommend) — McClintock's sledge journey to Prince Patrick Island, April-July 1853  
  1,369 km routed against 1,149 km straight, 401 km over land, 0 km over ice cap, highest 235 m; the line in the database is 1,149 km and 46 points; this one 141 points; it runs 3.8 km from the line in the database on average and 31 km at most
- **mcclure-investigator-010** (recommend) — Mecham's sledge journey round Eglinton and Prince Patrick Islands, April-July 1853  
  1,459 km routed against 1,277 km straight, 273 km over land, 0 km over ice cap, highest 227 m; the line in the database is 1,277 km and 57 points; this one 145 points; it runs 4.5 km from the line in the database on average and 34 km at most
- **mcclure-investigator-011** (recommend) — Hamilton's sledge journey to the rendezvous with Belcher's division, 1853  
  626 km routed against 550 km straight, 89 km over land, 0 km over ice cap, highest 215 m; the line in the database is 550 km and 26 points; this one 54 points; it runs 15.3 km from the line in the database on average and 56 km at most
- **mcclure-investigator-012** (recommend) — The Resolute and Intrepid beset and drifting off Cape Cockburn, 1853-54  
  217 km routed against 206 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 206 km and 11 points; this one 18 points; it runs 2.6 km from the line in the database on average and 9 km at most
- **mcclure-investigator-013** (recommend) — The Resolute's people march to Beechey Island, 15-28 May 1854  
  330 km routed against 304 km straight, 25 km over land, 0 km over ice cap, highest 212 m; the line in the database is 304 km and 16 points; this one 26 points; it runs 8.6 km from the line in the database on average and 31 km at most
- **mcclure-investigator-054** (recommend) — McClure's sledge journey to Parry's Rock, April 1852  
  254 km routed against 227 km straight, 152 km over land, 0 km over ice cap, highest 380 m; the line in the database is 227 km and 11 points; this one 19 points; waypoints on land whose note names water: 0; it runs 7.0 km from the line in the database on average and 25 km at most
- **nares-greely-022** (recommend) — Markham and Parr's sledge journey to 83 deg 20 min 26 sec N, April-June 1876  
  227 km routed against 213 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 213 km and 10 points; this one 19 points; it runs 2.7 km from the line in the database on average and 9 km at most
- **nares-greely-023** (recommend) — Lockwood, Brainard and Christiansen's journey to 83 deg 24 min N, April-June 1882  
  897 km routed against 790 km straight, 49 km over land, 0 km over ice cap, highest 823 m; the line in the database is 790 km and 38 points; this one 90 points; it runs 6.3 km from the line in the database on average and 38 km at most
- **nares-greely-025** (recommend) — The retreat from Fort Conger to Cape Sabine, August-October 1883  
  514 km routed against 416 km straight, 130 km over land, 0 km over ice cap, highest 965 m; the line in the database is 416 km and 23 points; this one 71 points; it runs 6.5 km from the line in the database on average and 25 km at most
- **nares-greely-038** (recommend) — Aldrich's western sledge journey to Cape Alfred Ernest, April-June 1876  
  1,091 km routed against 786 km straight, 403 km over land, 13 km over ice cap, highest 541 m; the line in the database is 786 km and 38 points; this one 166 points; it runs 6.1 km from the line in the database on average and 20 km at most
- **nares-greely-039** (recommend) — Beaumont's north Greenland sledge journey, April-August 1876  
  652 km routed against 584 km straight, 37 km over land, 3 km over ice cap, highest 774 m; the line in the database is 584 km and 36 points; this one 74 points; waypoints on land whose note names water: 19, 20, 21; it runs 3.6 km from the line in the database on average and 26 km at most
- **operation-hazen-1957-041** (recommend) — Christie and Hattersley-Smith to Lands Lokk, May-June 1954  
  661 km routed against 617 km straight, 69 km over land, 0 km over ice cap, highest 28 m; the line in the database is 617 km and 31 points; this one 48 points; it runs 2.4 km from the line in the database on average and 15 km at most
- **operation-hazen-1957-042** (recommend) — The 1953 sledge journey west from Alert  
  511 km routed against 445 km straight, 48 km over land, 1 km over ice cap, highest 395 m; the line in the database is 445 km and 23 points; this one 54 points; it runs 2.5 km from the line in the database on average and 16 km at most
- **oxford-ellesmere-1934-002** (recommend) — Moore, Stallworthy, Nukapinguaq and Inuatuk to Grant Land, April-May 1935  
  18 of 21 legs follow ink digitized from oxford-ellesmere-1934-005 (georef rms 1.0 km), 1 chained through hachures or lettering and doubted; the routed line runs 1.6 km from the printed one on average; 1,685 km routed against 1,304 km straight, 478 km over land, 162 km over ice cap, highest 1798 m; the line in the database is 1,304 km and 22 points; this one 217 points; waypoints on land whose note names water: 10; proposed moves, not applied: 10 (on land though the note names water; moved 8 km onto the printed route); 14 (inferred; moved 15 km onto the printed route); it runs 12.7 km from the line in the database on average and 56 km at most
- **oxford-ellesmere-1934-003** (recommend) — Humphreys and Haig-Thomas through Grinnell Land and Ellesmere Land, April-May 1935  
  27 of 28 legs follow ink digitized from oxford-ellesmere-1934-005 (georef rms 1.0 km); the routed line runs 3.0 km from the printed one on average; 1,498 km routed against 1,214 km straight, 518 km over land, 81 km over ice cap, highest 1111 m; the line in the database is 1,214 km and 53 points; this one 226 points; waypoints on land whose note names water: 18, 23; proposed moves, not applied: 18 (on land though the note names water; moved 6 km onto the printed route); 23 (on land though the note names water; moved 7 km onto the printed route); it runs 4.0 km from the line in the database on average and 29 km at most
- **oxford-ellesmere-1934-004** (recommend) — Shackleton and Bentham to Scoresby Bay, April-May 1935  
  17 of 26 legs follow ink digitized from oxford-ellesmere-1934-005 (georef rms 1.0 km), 1 chained through hachures or lettering and doubted; the routed line runs 1.8 km from the printed one on average; 890 km routed against 724 km straight, 94 km over land, 6 km over ice cap, highest 747 m; the line in the database is 724 km and 27 points; this one 137 points; it runs 1.9 km from the line in the database on average and 11 km at most
- **pole-seekers-from-ellesmere-030** (recommend) — Hattersley-Smith's sledge journey along the north coast, April-May 1953  
  414 km routed against 339 km straight, 56 km over land, 1 km over ice cap, highest 306 m; the line in the database is 339 km and 17 points; this one 39 points; waypoints on land whose note names water: 5, 7; it runs 6.3 km from the line in the database on average and 24 km at most
- **pole-seekers-from-ellesmere-031** (recommend) — Ward Hunt Island to Crane City and back, May 1954  
  131 km routed against 115 km straight, 85 km over land, 1 km over ice cap, highest 87 m; the line in the database is 115 km and 6 points; this one 19 points; it runs 1.0 km from the line in the database on average and 5 km at most
- **rcmp-high-arctic-patrols-003** (recommend) — Joy from Bache Peninsula to King Christian Island, March to May 1927  
  10 of 20 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km), 1 chained through hachures or lettering and doubted; the routed line runs 3.0 km from the printed one on average; 1,888 km routed against 1,575 km straight, 672 km over land, 143 km over ice cap, highest 1505 m; the line in the database is 1,575 km and 72 points; this one 212 points; waypoints on land whose note names water: 17; it runs 6.0 km from the line in the database on average and 25 km at most
- **rcmp-high-arctic-patrols-005** (recommend) — Makinson and Coolitanga, and the finding of Makinson Inlet, 1928  
  4 of 7 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km); the routed line runs 2.5 km from the printed one on average; 952 km routed against 712 km straight, 103 km over land, 99 km over ice cap, highest 1235 m; the line in the database is 712 km and 36 points; this one 91 points; waypoints on land whose note names water: 4; proposed moves, not applied: 1 (inferred; moved 23 km onto the printed route); it runs 18.9 km from the line in the database on average and 61 km at most
- **rcmp-high-arctic-patrols-006** (recommend) — Anstead and Nukapinguaq to Norwegian Bay, 1928  
  7 of 14 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km); the routed line runs 3.3 km from the printed one on average; 1,325 km routed against 1,064 km straight, 512 km over land, 150 km over ice cap, highest 1505 m; the line in the database is 1,064 km and 52 points; this one 141 points; it runs 6.8 km from the line in the database on average and 29 km at most
- **rcmp-high-arctic-patrols-008** (recommend) — McLean, Beatty and Nukapinguaq: the new crossing of Ellesmere Island, 1930  
  8 of 11 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km); the routed line runs 3.0 km from the printed one on average; 1,369 km routed against 1,029 km straight, 390 km over land, 156 km over ice cap, highest 1235 m; the line in the database is 1,029 km and 47 points; this one 162 points; waypoints on land whose note names water: 7; proposed moves, not applied: 10 (inferred; moved 12 km onto the printed route); it runs 13.9 km from the line in the database on average and 33 km at most
- **rcmp-high-arctic-patrols-009** (recommend) — Timbury, Hamilton and Keepomee to Beechey Island, 1930  
  3 of 4 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km); the routed line runs 1.4 km from the printed one on average; 849 km routed against 753 km straight, 98 km over land, 0 km over ice cap, highest 285 m; the line in the database is 753 km and 37 points; this one 72 points; waypoints on land whose note names water: 0, 4; it runs 12.1 km from the line in the database on average and 58 km at most
- **rcmp-high-arctic-patrols-010** (recommend) — Stallworthy's first search for the Kruger party, 1931  
  6 of 11 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km); the routed line runs 3.8 km from the printed one on average; 1,286 km routed against 944 km straight, 34 km over land, 23 km over ice cap, highest 705 m; the line in the database is 944 km and 44 points; this one 134 points; waypoints on land whose note names water: 7, 8; proposed moves, not applied: 4 (inferred; moved 14 km onto the printed route); 6 (inferred; moved 23 km onto the printed route); it runs 12.5 km from the line in the database on average and 53 km at most
- **sverdrup-bernier-peary-003** (recommend) — Isachsen and Hassel across the Ringnes islands, spring 1901  
  1,474 km routed against 1,275 km straight, 507 km over land, 0 km over ice cap, highest 457 m; the line in the database is 1,275 km and 17 points; this one 156 points; waypoints on land whose note names water: 0, 3; it runs 5.6 km from the line in the database on average and 37 km at most
- **sverdrup-bernier-peary-178** (recommend) — Peary's winter march to Fort Conger, December 1898 to February 1899  
  691 km routed against 621 km straight, 3 km over land, 0 km over ice cap, highest 83 m; the line in the database is 621 km and 9 points; this one 43 points; waypoints on land whose note names water: 6; it runs 13.8 km from the line in the database on average and 38 km at most
- **sverdrup-bernier-peary-180** (recommend) — Peary from Cape Hecla to 84 degrees 17 minutes north, 1902  
  1,612 km routed against 1,402 km straight, 19 km over land, 0 km over ice cap, highest 464 m; the line in the database is 1,402 km and 28 points; this one 132 points; waypoints on land whose note names water: 10; it runs 9.6 km from the line in the database on average and 44 km at most
- **sverdrup-bernier-peary-194** (recommend) — Peary's summer journey west to Cape Thomas Hubbard, 1906  
  1,441 km routed against 1,156 km straight, 550 km over land, 4 km over ice cap, highest 283 m; the line in the database is 1,156 km and 19 points; this one 179 points; waypoints on land whose note names water: 6; it runs 5.8 km from the line in the database on average and 29 km at most
- **franklin-search-022** (review) — Ommanney's southern division: Cape Walker and Prince of Wales Island, April-June 1851  
  2 of 7 legs could not be routed (outside the DEM); 593 km routed against 576 km straight, 5 km over land, 0 km over ice cap, highest 171 m; the line in the database is 576 km and 27 points; this one 42 points; it runs 1.1 km from the line in the database on average and 10 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **franklin-search-023** (review) — HMS Resolute, 1852-1855: Dealy Island, the drift and the derelict  
  10 of 25 legs could not be routed (outside the DEM); 11,894 km routed against 11,702 km straight, 488 km over land, 0 km over ice cap, highest 244 m; the line in the database is 11,702 km and 576 points; this one 617 points; waypoints on land whose note names water: 16; it runs 2.9 km from the line in the database on average and 67 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **franklin-search-027** (review) — Kennedy and Bellot's sledge journey round Somerset Island, February-May 1852  
  14 of 15 legs could not be routed (outside the DEM); 1,036 km routed against 1,029 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 1,029 km and 49 points; this one 43 points; it runs 1.6 km from the line in the database on average and 15 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **greenland-inughuit-016** (review) — Qitdlarssuaq's migration, about 1852 to 1863  
  2 of 9 legs could not be routed (outside the DEM); 1,515 km routed against 1,188 km straight, 551 km over land, 101 km over ice cap, highest 1033 m; the line in the database is 1,188 km and 56 points; this one 161 points; it runs 12.4 km from the line in the database on average and 56 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **kane-hall-polaris-035** (review) — The Polaris ice-floe drift, 15 October 1872 to 30 April 1873  
  23 of 27 legs could not be routed (outside the DEM); 3,268 km routed against 3,216 km straight, 36 km over land, 3 km over ice cap, highest 227 m; the line in the database is 3,216 km and 151 points; this one 159 points; it runs 2.5 km from the line in the database on average and 44 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **kane-hall-polaris-263** (review) — Hayes's sledge journey across Smith Sound and up the Ellesmere coast, April to June 1861  
  14 of 18 legs follow ink digitized from kane-hall-polaris-193 (georef rms 0.3 km), 1 chained through hachures or lettering and doubted; the routed line runs 1.1 km from the printed one on average; 584 km routed against 495 km straight, 4 km over land, 0 km over ice cap, highest 391 m; the line in the database is 495 km and 19 points; this one 74 points; proposed moves, not applied: 4 (inferred; moved 17 km onto the printed route); 5 (inferred; moved 6 km onto the printed route); 6 (inferred; moved 19 km onto the printed route); 15 (inferred; moved 7 km onto the printed route); 16 (inferred; moved 9 km onto the printed route); 17 (inferred; moved 13 km onto the printed route); it runs 5.2 km from the line in the database on average and 22 km at most; Hayes's own chart puts the Ellesmere coast a degree too far north, so a route digitized against it is only as good as his coast
- **karluk-cae-002** (review) — Stefansson's 1914 ice journey: Martin Point to Banks Island  
  8 of 14 legs could not be routed (outside the DEM); 1,150 km routed against 1,138 km straight, 12 km over land, 0 km over ice cap, highest 0 m; the line in the database is 1,138 km and 55 points; this one 65 points; it runs 0.3 km from the line in the database on average and 6 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **karluk-cae-003** (review) — Stefansson's 1915 ice journey: the new land north of Prince Patrick Island  
  4 of 17 legs could not be routed (outside the DEM); 2,039 km routed against 1,953 km straight, 112 km over land, 0 km over ice cap, highest 105 m; the line in the database is 1,953 km and 97 points; this one 114 points; waypoints on land whose note names water: 9; it runs 6.6 km from the line in the database on average and 32 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **karluk-cae-004** (review) — Stefansson's 1916 ice journey: Banks Island to Meighen and Lougheed Islands  
  1 of 24 legs could not be routed (outside the DEM); 2,658 km routed against 2,404 km straight, 525 km over land, 0 km over ice cap, highest 295 m; the line in the database is 2,404 km and 112 points; this one 196 points; waypoints on land whose note names water: 15; it runs 8.0 km from the line in the database on average and 48 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **karluk-cae-008** (review) — Stefansson's last ice journey, 1917: Melville Island to the sea desert and back to Cape Kellett  
  1 of 24 legs could not be routed (outside the DEM); 2,391 km routed against 2,192 km straight, 516 km over land, 0 km over ice cap, highest 82 m; the line in the database is 2,192 km and 25 points; this one 147 points; waypoints on land whose note names water: 23; it runs 10.7 km from the line in the database on average and 49 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **mcclure-investigator-014** (review) — The Resolute's drift, 1854-1855, and her voyage to New London  
  3 of 4 legs could not be routed (outside the DEM); 4,583 km routed against 4,559 km straight, 12 km over land, 0 km over ice cap, highest 16 m; the line in the database is 4,559 km and 227 points; this one 222 points; it runs 1.6 km from the line in the database on average and 46 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **operation-hazen-1957-026** (review) — The drift of ice island WH-5, Ward Hunt Ice Shelf to the Grand Banks, 1962-1964  
  4 of 11 legs could not be routed (outside the DEM); 4,826 km routed against 4,674 km straight, 129 km over land, 0 km over ice cap, highest 552 m; the line in the database is 4,674 km and 231 points; this one 262 points; waypoints on land whose note names water: 2; it runs 10.0 km from the line in the database on average and 245 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **pole-seekers-from-ellesmere-006** (review) — Peary's 1909 route from Cape Columbia, by his own latitudes  
  4 of 10 legs could not be routed (outside the DEM); 1,704 km routed against 1,670 km straight, 0 km over land, 0 km over ice cap, highest 6 m; the line in the database is 1,670 km and 82 points; this one 85 points; it runs 1.5 km from the line in the database on average and 14 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **pole-seekers-from-ellesmere-007** (review) — Peary's 1906 route from Point Moss to 87 deg 06 min N  
  2 of 6 legs could not be routed (outside the DEM); 1,123 km routed against 1,096 km straight, 3 km over land, 0 km over ice cap, highest 283 m; the line in the database is 1,096 km and 54 points; this one 59 points; it runs 2.6 km from the line in the database on average and 24 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **pole-seekers-from-ellesmere-038** (review) — The Italian expedition to the North Pole, Cape Columbia to T-3, 1971  
  2 of 5 legs could not be routed (outside the DEM); 2,155 km routed against 2,015 km straight, 6 km over land, 1 km over ice cap, highest 146 m; the line in the database is 2,015 km and 6 points; this one 113 points; it runs 113.3 km from the line in the database on average and 456 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **pole-seekers-from-ellesmere-039** (review) — Jean-Louis Etienne alone from Ward Hunt Island to the Pole, 1986  
  4 of 6 legs could not be routed (outside the DEM); 2,488 km routed against 2,476 km straight, 14 km over land, 0 km over ice cap, highest 31 m; the line in the database is 2,476 km and 7 points; this one 124 points; it runs 184.6 km from the line in the database on average and 526 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **qei-from-the-air-1947-023** (review) — Fairbanks - Ellesmere - the North Pole - Edmonton, 9-10 May 1946  
  6 of 7 legs could not be routed (outside the DEM); 7,898 km routed against 7,673 km straight, 144 km over land, 42 km over ice cap, highest 1639 m; the line in the database is 7,673 km and 8 points; this one 397 points; it runs 124.2 km from the line in the database on average and 1032 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **qei-from-the-air-1947-024** (review) — Where the SHORAN survey was, season by season, 1949-1957  
  8 of 10 legs could not be routed (outside the DEM); 14,631 km routed against 13,866 km straight, 1,294 km over land, 774 km over ice cap, highest 362 m; the line in the database is 13,866 km and 690 points; this one 744 points; it runs 28.4 km from the line in the database on average and 439 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **rcmp-high-arctic-patrols-001** (review) — Joy over the Devon Island ice cap, March and April 1926  
  5 of 11 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km); the routed line runs 0.6 km from the printed one on average; 693 km routed against 549 km straight, 273 km over land, 251 km over ice cap, highest 1909 m; the line in the database is 549 km and 24 points; this one 84 points; waypoints on land whose note names water: 5, 6, 11; proposed moves, not applied: 2 (inferred; moved 20 km onto the printed route); 3 (inferred; moved 17 km onto the printed route); it runs 4.7 km from the line in the database on average and 28 km at most
- **rcmp-high-arctic-patrols-002** (review) — Joy from Craig Harbour to Axel Heiberg Island, April and May 1926  
  7 of 16 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km); the routed line runs 2.6 km from the printed one on average; 1,498 km routed against 1,110 km straight, 346 km over land, 0 km over ice cap, highest 591 m; the line in the database is 1,110 km and 50 points; this one 181 points; waypoints on land whose note names water: 0, 2, 5, 13, 15, 16; it runs 8.6 km from the line in the database on average and 45 km at most
- **rcmp-high-arctic-patrols-004** (review) — Bain and Oodee, Bache Peninsula to Craig Harbour and back, 1927  
  5 of 13 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km); the routed line runs 3.4 km from the printed one on average; 998 km routed against 776 km straight, 3 km over land, 0 km over ice cap, highest 85 m; the line in the database is 776 km and 37 points; this one 106 points; waypoints on land whose note names water: 1, 7, 8; proposed moves, not applied: 10 (inferred; moved 18 km onto the printed route); it runs 11.2 km from the line in the database on average and 53 km at most
- **rcmp-high-arctic-patrols-007** (review) — Joy, Taggart and Nukapinguaq: Dundas Harbour to Melville Island to Bache Peninsula, 1929  
  7 of 16 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km), 1 chained through hachures or lettering and doubted; the routed line runs 6.0 km from the printed one on average; 2,368 km routed against 2,093 km straight, 664 km over land, 85 km over ice cap, highest 1505 m; the line in the database is 2,093 km and 98 points; this one 209 points; waypoints on land whose note names water: 14; it runs 10.7 km from the line in the database on average and 45 km at most
- **science-stations-003** (review) — The drift of the ice island T-3, 1947-1952  
  6 of 7 legs could not be routed (outside the DEM); 3,320 km routed against 3,292 km straight, 0 km over land, 0 km over ice cap, highest 1 m; the line in the database is 3,292 km and 163 points; this one 161 points; it runs 3.2 km from the line in the database on average and 41 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **science-stations-029** (review) — The drift of the ice island T-1, 1946-1952  
  1 of 4 legs could not be routed (outside the DEM); 2,063 km routed against 2,037 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 2,037 km and 101 points; this one 94 points; it runs 2.6 km from the line in the database on average and 30 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **science-stations-073** (review) — The 1959 reconnaissance to Axel Heiberg Island, 13 July to 26 August  
  1 of 5 legs could not be routed (outside the DEM); 5,291 km routed against 4,697 km straight, 1,217 km over land, 33 km over ice cap, highest 929 m; the line in the database is 4,697 km and 6 points; this one 408 points; waypoints on land whose note names water: 3; it runs 103.9 km from the line in the database on average and 191 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **science-stations-074** (review) — The 1960 airlift: Montreal to Expedition Fiord, May 1960  
  1 of 5 legs could not be routed (outside the DEM); 4,123 km routed against 4,066 km straight, 219 km over land, 140 km over ice cap, highest 1742 m; the line in the database is 4,066 km and 6 points; this one 242 points; it runs 123.2 km from the line in the database on average and 204 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **st-roch-modern-055** (review) — USS Seadragon, Portsmouth to Pearl Harbor under the ice, 1960  
  5 of 10 legs could not be routed (outside the DEM); 15,110 km routed against 14,992 km straight, 159 km over land, 0 km over ice cap, highest 81 m; the line in the database is 14,992 km and 11 points; this one 723 points; it runs 385.7 km from the line in the database on average and 2632 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **sverdrup-bernier-peary-035** (review) — The 1909 sledge journey from Cape Columbia (claimed route)  
  4 of 5 legs could not be routed (outside the DEM); 1,540 km routed against 1,532 km straight, 0 km over land, 0 km over ice cap, highest 1 m; the line in the database is 1,532 km and 75 points; this one 75 points; it runs 0.3 km from the line in the database on average and 9 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **sverdrup-bernier-peary-179** (review) — Peary along the north coast of Greenland to Cape Morris Jesup, 1900  
  3 of 31 legs could not be routed (outside the DEM); 1,997 km routed against 1,810 km straight, 159 km over land, 1 km over ice cap, highest 886 m; the line in the database is 1,810 km and 32 points; this one 186 points; it runs 3.4 km from the line in the database on average and 14 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **sverdrup-bernier-peary-193** (review) — Peary's sledge journey from Point Moss to 87 degrees 6 minutes north, 1906 (claimed route)  
  2 of 11 legs could not be routed (outside the DEM); 1,246 km routed against 1,181 km straight, 20 km over land, 0 km over ice cap, highest 663 m; the line in the database is 1,181 km and 12 points; this one 78 points; it runs 8.2 km from the line in the database on average and 19 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **sverdrup-bernier-peary-300** (review) — The first crossing of Ellesmere Island, April and May 1899  
  8 of 11 legs follow ink digitized from sverdrup-bernier-peary-064 (georef rms 0.0 km), 1 chained through hachures or lettering and doubted; the routed line runs 3.8 km from the printed one on average; 388 km routed against 297 km straight, 185 km over land, 1 km over ice cap, highest 734 m; the line in the database is 297 km and 12 points; this one 74 points; waypoints on land whose note names water: 0, 2, 3, 4, 5, 6, 7, 9; proposed moves, not applied: 9 (on land though the note names water; moved 10 km onto the printed route); it runs 1.9 km from the line in the database on average and 11 km at most; a first-reconnaissance sketch with hachured relief: the dash-dot route is hard to tell from the shading and the chain wanders, so the corridor is weak evidence here
- **sverdrup-bernier-peary-301** (review) — Isachsen and Braskerud over the glaciers to the west coast, 1899  
  9 of 11 legs follow ink digitized from sverdrup-bernier-peary-064 (georef rms 0.0 km), 1 chained through hachures or lettering and doubted; the routed line runs 1.9 km from the printed one on average; 372 km routed against 256 km straight, 279 km over land, 260 km over ice cap, highest 1625 m; the line in the database is 256 km and 12 points; this one 63 points; it runs 3.9 km from the line in the database on average and 18 km at most; a first-reconnaissance sketch with hachured relief: the dash-dot route is hard to tell from the shading and the chain wanders, so the corridor is weak evidence here
- **thule-dorset-001** (review) — The Thule migration from Alaska, schematic  
  8 of 9 legs could not be routed (outside the DEM); 4,443 km routed against 4,434 km straight, 4 km over land, 0 km over ice cap, highest 220 m; the line in the database is 4,434 km and 218 points; this one 225 points; it runs 0.1 km from the line in the database on average and 10 km at most; the legs outside the DEM stay great circles, which is right over the sea ice; review the rest
- **posts-rcmp-missions-023** (same) — Joy's attempt on Ellesmere Island, March-April 1924  
  14 of 17 legs could not be routed (outside the DEM); 7 of 17 legs follow ink digitized from oxford-ellesmere-1934-073 (georef rms 8.5 km); the routed line runs 0.7 km from the printed one on average; 750 km routed against 745 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 745 km and 35 points; this one 40 points; it runs 0.1 km from the line in the database on average and 2 km at most; the same line as the database holds to within 3 km (a journey over the sea ice routes straight), so there is nothing to write back
- **amundsen-gjoa-002** (outside) — Amundsen's ride to the telegraph at Eagle, 1905-1906  
  7 of 7 legs could not be routed (outside the DEM); 1,288 km routed against 1,288 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 1,288 km and 64 points; this one 64 points; it runs 0.0 km from the line in the database on average and 0 km at most; every leg is outside the DEM, so this is not the terrain router's track: leave it as-given
- **franklin-1845-002** (outside) — Where the ships went after 1848: the drift the Inuit testimony describes  
  4 of 4 legs could not be routed (outside the DEM); 216 km routed against 216 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 216 km and 10 points; this one 10 points; it runs 0.0 km from the line in the database on average and 0 km at most; every leg is outside the DEM, so this is not the terrain router's track: leave it as-given
- **franklin-search-068** (outside) — Richardson and Rae's boat voyage and march, 1848  
  22 of 22 legs could not be routed (outside the DEM); 9,698 km routed against 9,698 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 9,698 km and 476 points; this one 476 points; it runs 0.0 km from the line in the database on average and 0 km at most; every leg is outside the DEM, so this is not the terrain router's track: leave it as-given
- **greenland-inughuit-045** (outside) — The Fifth Thule Expedition across Arctic America, 1921-1924  
  13 of 13 legs could not be routed (outside the DEM); 6,528 km routed against 6,528 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 6,528 km and 322 points; this one 322 points; it runs 0.0 km from the line in the database on average and 0 km at most; every leg is outside the DEM, so this is not the terrain router's track: leave it as-given
- **hudson-strait-south-baffin-015** (outside) — Patrol A-11-A: down on the Atlantic ice, and the walk back  
  8 of 8 legs could not be routed (outside the DEM); 535 km routed against 535 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 535 km and 24 points; this one 24 points; it runs 0.0 km from the line in the database on average and 0 km at most; every leg is outside the DEM, so this is not the terrain router's track: leave it as-given
- **inuit-oral-history-029** (outside) — The coast Iligliuk drew: Winter Island to the Fury and Hecla Strait  
  8 of 8 legs could not be routed (outside the DEM); 554 km routed against 554 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 554 km and 9 points; this one 26 points; it runs 0.1 km from the line in the database on average and 0 km at most; every leg is outside the DEM, so this is not the terrain router's track: leave it as-given
- **inuit-oral-history-030** (outside) — The journey to Akkoolee: the sleeping places on the Netsilingmiut chart, 1830  
  6 of 6 legs could not be routed (outside the DEM); 461 km routed against 461 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 461 km and 21 points; this one 21 points; it runs 0.0 km from the line in the database on average and 0 km at most; every leg is outside the DEM, so this is not the terrain router's track: leave it as-given
- **karluk-cae-005** (outside) — Storkerson's drift on the Beaufort Sea ice, 1918  
  11 of 11 legs could not be routed (outside the DEM); 1,109 km routed against 1,109 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 1,109 km and 52 points; this one 52 points; it runs 0.0 km from the line in the database on average and 0 km at most; every leg is outside the DEM, so this is not the terrain router's track: leave it as-given
- **karluk-cae-006** (outside) — Bartlett and Kataktovik's walk to Siberia, March-May 1914  
  7 of 7 legs could not be routed (outside the DEM); 1,768 km routed against 1,768 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 1,768 km and 85 points; this one 85 points; it runs 0.0 km from the line in the database on average and 0 km at most; every leg is outside the DEM, so this is not the terrain router's track: leave it as-given
- **karluk-cae-007** (outside) — Rasmussen's sledge journey across Arctic America, 1921-1924  
  19 of 19 legs could not be routed (outside the DEM); 10,103 km routed against 10,103 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 10,103 km and 497 points; this one 497 points; it runs 0.0 km from the line in the database on average and 15 km at most; every leg is outside the DEM, so this is not the terrain router's track: leave it as-given
- **ross-victory-002** (outside) — James Clark Ross's sledge journey to the North Magnetic Pole, 27 May to 1 June 1831  
  6 of 6 legs could not be routed (outside the DEM); 219 km routed against 219 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 237 km and 11 points; this one 10 points; it runs 1.3 km from the line in the database on average and 21 km at most; every leg is outside the DEM, so this is not the terrain router's track: leave it as-given
- **ross-victory-003** (outside) — The retreat from the Victory and the open-boat escape, 1832-1833  
  16 of 16 legs could not be routed (outside the DEM); 5,538 km routed against 5,538 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 5,538 km and 274 points; this one 274 points; it runs 0.0 km from the line in the database on average and 0 km at most; every leg is outside the DEM, so this is not the terrain router's track: leave it as-given
- **science-stations-030** (outside) — The drift of the ice island T-2, 1950-1951  
  1 of 1 legs could not be routed (outside the DEM); 687 km routed against 687 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 687 km and 35 points; this one 35 points; it runs 0.0 km from the line in the database on average and 0 km at most; every leg is outside the DEM, so this is not the terrain router's track: leave it as-given
- **sverdrup-bernier-peary-183** (outside) — Lavoie's sledge survey of Prince Regent Inlet, spring 1911  
  13 of 13 legs could not be routed (outside the DEM); 1,104 km routed against 1,104 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 1,104 km and 14 points; this one 50 points; it runs 0.6 km from the line in the database on average and 2 km at most; every leg is outside the DEM, so this is not the terrain router's track: leave it as-given
- **wrecks-disasters-038** (outside) — The Grenville Bay's winter drift, October to December 1835  
  5 of 5 legs could not be routed (outside the DEM); 1,502 km routed against 1,502 km straight, 0 km over land, 0 km over ice cap, highest 0 m; the line in the database is 1,502 km and 73 points; this one 73 points; it runs 0.0 km from the line in the database on average and 0 km at most; every leg is outside the DEM, so this is not the terrain router's track: leave it as-given

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
- crocker-land-1913-004 waypoint 22: land at 35 m — Bay Fiord, the hills crawling with Arctic hare; a day of rest and the Inughuit's
- franklin-search-023 waypoint 16: land at 65 m — within six miles of Parry's Winter Harbour and stopped by solid floe - 'the idea
- greenland-inughuit-017 waypoint 5: land at 165 m — a fish lake between Makinson Inlet and Baumann Fiord: famine, murder and canniba
- greenland-inughuit-043 waypoint 3: land at 230 m — through Flagler Bay and Sverdrup Pass (route after Cook; date approximate)
- haig-thomas-1937-001 waypoint 16: land at 5 m, 13 km from the ink; proposed 78.131 -95.745 (inferred; moved 13 km onto the printed route) — the tide crack on the east coast of Amund Ringnes Island, the island visible ahe
- haig-thomas-1937-001 waypoint 20: land at 591 m, 10 km from the ink; proposed 78.316 -84.982 (on land though the note names water; moved 10 km onto the printed route) — Trold Fiord, crossed to on foot from Eureka Sound and recognised from 1935
- haig-thomas-1937-001 waypoint 21: land at 211 m, 2 km from the ink — four days searching the plateau south of Bay Fiord for the fossil bones Nukaping
- haig-thomas-1937-002 waypoint 6: land at 110 m — second crossing of Smith Sound completed and the loaded journey begins: two sled
- haig-thomas-1937-002 waypoint 19: land at 110 m — back at Fram Havn, the Smith Sound route now plainly marked by four parties' tra
- kane-hall-polaris-263 waypoint 4: sea, 17 km from the ink; proposed 78.950 -73.235 (inferred; moved 17 km onto the printed route) — twenty-two days out and about thirty miles from Cairn Point: three miles a day m
- kane-hall-polaris-263 waypoint 5: sea, 6 km from the ink; proposed 78.950 -73.235 (inferred; moved 6 km onto the printed route) — the main party sent back - 'I SENT the main party back this morning. The separat
- kane-hall-polaris-263 waypoint 6: sea, 19 km from the ink; proposed 79.317 -73.865 (inferred; moved 19 km onto the printed route) — within ten miles of the western shore by reckoning; names the two headlands ahea
- kane-hall-polaris-263 waypoint 15: sea, 7 km from the ink; proposed 79.546 -73.452 (inferred; moved 7 km onto the printed route) — Cape Hawks again after two marches from below Cape Napoleon, and back onto the o
- kane-hall-polaris-263 waypoint 16: sea, 9 km from the ink; proposed 78.538 -73.260 (inferred; moved 9 km onto the printed route) — adrift on an ice raft a mile off Cairn Point when the crack they had stepped ove
- kane-hall-polaris-263 waypoint 17: sea, 13 km from the ink; proposed 78.538 -73.260 (inferred; moved 13 km onto the printed route) — the ice foot gone below Cairn Point: the sledges are abandoned and the party cro
- karluk-cae-003 waypoint 9: land at 67 m — Stefansson climbs and names Leffingwell Crags and sees hills at least fifty mile
- karluk-cae-004 waypoint 15: land at 39 m — thirty hours of tidal observations near latitude 78 degrees 04 minutes north in 
- karluk-cae-008 waypoint 23: land — a noon latitude is taken and Stefansson sets off alone on foot for Kellett, carr
- kruger-1930-001 waypoint 0: land at 220 m — Etah district: Krüger, Bjare and Akqioq set out across Smith Sound in early Marc
- kruger-1930-001 waypoint 3: land at 402 m — up Flagler Fiord and over the divide to Bay Fiord: the standard route, and the o
- kruger-1930-002 waypoint 5: land at 5 m — Craig Harbour: nobody had been there since Corporal McLean's visit a year before
- kruger-1930-005 waypoint 1: land at 15 m — across the mouth of Croker Bay, west towards Cuming Inlet, with long detours rou
- kruger-1930-005 waypoint 5: land at 50 m — back at Dundas Harbour
- mcclure-investigator-006 waypoint 9: land at 348 m — crosses the Bay of Mercy and at 5 p.m. is within a hundred yards of HMS Investig
- mcclure-investigator-007 waypoint 0: land at 306 m — McClure leaves the Bay of Mercy to see Kellett in person rather than answer his 
- mcclure-investigator-007 waypoint 5: land at 306 m — back in the Bay of Mercy; the letter is read to the crew next morning, and only 
- mcclure-investigator-054 waypoint 0: land at 306 m — McClure and six men leave the Investigator in the Bay of Mercy with one sledge
- nares-greely-039 waypoint 19: land at 4 m — Charles Paul dies within sight of Polaris Bay; the printed narrative gives only 
- nares-greely-039 waypoint 20: land at 4 m — Polaris Bay, Hall's Rest: the whole crew arrives with scurvy. Hans Hendrik's sea
- nares-greely-039 waypoint 21: land at 4 m — after a gale, a start for Discovery Bay in a fifteen-foot ice-boat with the sled
- operation-hazen-1957-026 waypoint 2: land at 549 m — north end of Kennedy Channel, axis parallel to the channel; position inferred fr
- oxford-ellesmere-1934-002 waypoint 10: land at 156 m, 8 km from the ink; proposed 81.798 -70.540 (on land though the note names water; moved 8 km onto the printed route) — the east end of Lake Hazen after three days: the ice only four to five feet thic
- oxford-ellesmere-1934-002 waypoint 14: ice cap at 1520 m, 15 km from the ink; proposed 82.458 -72.546 (inferred; moved 15 km onto the printed route) — the summit climbed again in clear weather. Nukapinguaq points out through the gl
- oxford-ellesmere-1934-003 waypoint 18: land at 643 m, 6 km from the ink; proposed 79.138 -78.374 (on land though the note names water; moved 6 km onto the printed route) — up Flagler Fjord over glare ice in a wind so strong the sledge is blown sideways
- oxford-ellesmere-1934-003 waypoint 23: land at 35 m, 7 km from the ink; proposed 78.917 -83.275 (on land though the note names water; moved 7 km onto the printed route) — back to Bay Fiord, collecting fossil-bearing rocks near the divide and the rest 
- pole-seekers-from-ellesmere-030 waypoint 5: land — Markham Bay: survey poles aligned on the ice shelf as movement and ablation mark
- pole-seekers-from-ellesmere-030 waypoint 7: land at 75 m — back at Alert after five days, with a detour down Clements Markham Inlet
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
- science-stations-073 waypoint 3: land at 451 m — the permanent base site chosen at the head of the fiord the party would name Exp
- sverdrup-bernier-peary-003 waypoint 0: land at 248 m — leave the Fram in Goose Fiord with the other sledge parties on Easter Monday and
- sverdrup-bernier-peary-003 waypoint 3: land at 133 m — the high mountain proves to be the north end of North Cornwall; they name Hendri
- sverdrup-bernier-peary-178 waypoint 6: land at 83 m — at midnight they stumble through the dilapidated door of Fort Conger; pulling of
- sverdrup-bernier-peary-180 waypoint 10: land at 83 m — Fort Conger, 300 miles from Payer Harbour in twelve marches. Four days of overha
- sverdrup-bernier-peary-194 waypoint 6: land — M'Clintock Bay, crossed in one long march over both its arms. Date approximate
- sverdrup-bernier-peary-300 waypoint 0: land at 110 m, 4 km from the ink — Sverdrup, Isachsen, Stolz and Bay leave the Fram at Fram Havn; the mate Oluf Raa
- sverdrup-bernier-peary-300 waypoint 2: land at 629 m, 2 km from the ink — thirty-eight miles in one day over favourable ice to the sands at the head of No
- sverdrup-bernier-peary-300 waypoint 3: land at 629 m, 2 km from the ink — Hassel and Isachsen take a meridian altitude at the head of the fiord; Sverdrup,
- sverdrup-bernier-peary-300 waypoint 4: land at 515 m, 4 km from the ink — up the valley that trends west at an even gradient from the head of Flagler Bay,
- sverdrup-bernier-peary-300 waypoint 5: land at 448 m, 3 km from the ink — Sverdrup and Bay leave the sledges at the glacier and the tarn and go on with th
- sverdrup-bernier-peary-300 waypoint 6: land at 225 m, 4 km from the ink — three in the morning at the outer edge of the sands; in the afternoon, from a co
- sverdrup-bernier-peary-300 waypoint 7: land at 225 m, 4 km from the ink — the fiord below is named Bay Fjord for the zoologist Edvard Bay; a herd of musk 
- sverdrup-bernier-peary-300 waypoint 9: land at 672 m, 10 km from the ink; proposed 79.030 -76.882 (on land though the note names water; moved 10 km onto the printed route) — down Flagler Bay and along the ice-foot of Hayes Sound
