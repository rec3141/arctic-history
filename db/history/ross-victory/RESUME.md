# Resume state for `ross-victory`

Run 1 (grid, 2026-09-08) worked this topic from nothing to `drafted`. An image sweep
(2026-09-09) added the plates. A review run (2026-09-09) verified every quotation against the
texts, corrected the plate titles and several positions, and promoted all seven pages to
`good`. Read the worklog with `tools/history-db.py resume --topic ross-victory` first; this
file records only what is on disk and how to find things inside the texts.

## Files in `files/`

| file | what it is |
| --- | --- |
| `ross-victory-narrative-1835.txt` | **THE** source. John Ross, *Narrative of a Second Voyage* (1835), full OCR of the University of Pittsburgh Darlington copy. Verified against the title page in run 1. Clean OCR; words are separated by double spaces, so grep with `\s+` collapsed or you will get false misses (`magnetic  pole`, not `magnetic pole`). 29,855 lines. |
| `ross-victory-ross1835-narrative.pdf` | The Internet Archive page scan of the same book, 854 leaves, no text layer. The plate PNGs were cut from it. |
| `ross-victory-appendix-1835.txt` | The *Appendix* volume: James Clark Ross's magnetic tables, the *Sketch of the Esquimaux found in the Territory of Boothia Felix*, the English-Danish-Esquimaux vocabulary, natural history, the surgeon's report, the crew biographies, four years of meteorological tables, and a gazetteer of latitudes. Dirty OCR; the gazetteer's names and numbers are OCR'd into separate blocks and cannot be aligned reliably. |
| `ross-victory-huish-1835.txt` / `-huish1835-lastvoyage.pdf` | Robert Huish's rival, hostile account. Use as a witness against Ross, never as independent fact. |
| `ross-victory-*-excerpt.txt` | Chapters XVI-XXVI (Netsilingmiut), XLII-XLIII (magnetic pole), XLIX-LVII (retreat). |
| `ross-victory-ross1835-*.png`, `ross-victory-huish-*.png` | 25 plates and tables. |

**Do not cite `_staging/cihm_08551.txt`.** It is not Ross 1835 despite an old manifest line.

## Finding things in the narrative

Marginal dates are printed as `Jan. 9.`, `August 12`, `Sept. i7.` and so on, often OCR'd
badly and often several lines away from the entry they belong to, and running heads
("TO THE ARCTIC REGIONS. 557", "560 SECOND VOYAGE OF DISCOVERY") cut through sentences.
Search a whitespace-collapsed copy and expect both. The table of contents (around line 1321)
lists all 57 chapters with page numbers; **the plate list, "PLATES PAGED FOR THE BINDER", is
at line 1638** and is the authority on what every plate is and which page it faces. Use it.

## Positions established from the printed record

- Felix Harbour: 69° 58′ 42″ N, 92° 01′ 06″ W (journal, p. 194); the comparative table on
  p. 209 gives 69° 59′ 00″ N, same longitude.
- Sheriff's Harbour: 70° 01′ N, 91° 54′ W (James Clark Ross's mean magnetic position).
- Victoria Harbour: 70° 09′ 18″ N, 91° 30′ 33″ W (magnetic table). **Unresolved conflict:**
  the narrative gives 70° 18′ 11″ N for the harbour entered on 29 August 1831. Nine minutes of
  arc, up to 20 km on the wreck site. Both are on the rows; the magnetic table is used.
- North Magnetic Pole: 70° 05′ 17″ N, 96° 46′ 45″ W (James Clark Ross's narrative of the
  journey). **Small conflict:** the summary magnetic table a few pages later prints the
  longitude as 96° 45′ 48″ W. The narrative figure is used everywhere in this topic; the
  variant is stated on the page and on the place row.
- Sledge halts, all observed and printed to the second: 28 May 1831, 69° 34′ 45″ N,
  94° 54′ 23″ W (dip 89° 41′); 29 May, 69° 40′ 27″ N, 95° 22′ 35″ W; 30 May, 69° 46′ 25″ N,
  95° 49′ 11″ W; 1 June, the pole (dip 89° 59′).
- Victory Point: Ross prints 69° 37′ 49″ N, 98° 40′ 49″ W, and the observing station a few
  miles back as 69° 46′ 19″ N, 98° 32′ 49″ W. **Unresolved:** the longitude is close to the
  modern feature but the latitude is some twenty minutes of arc south of it. The event row is
  pinned at the modern Victory Point (69.97, -98.55) and says so.

## Corrected in review — do not reintroduce

- **The magnetic pole journey started at Sheriff's Harbour, not Victoria Harbour.** The ship
  did not reach Victoria Harbour until 29 August 1831.
- **There were three deaths on the voyage, not two.** James Marslin (Felix Harbour,
  20 Jan 1830), **James Dixon**, stoker (Victoria Harbour, 10 Jan 1832, buried the 16th; his
  grave is lettered on Ross's plan of the harbour) and Chimham Thomas (Fury Beach,
  16 Feb 1833). Henry Ayre, the cook, died soon after the return. Twenty-three sailed —
  twenty paid hands on the Admiralty list plus three unpaid officers — and twenty came home.
- **Four winters in all, three of them beset in the ship**, not "four beset and a fifth
  ashore". Twenty-one wintered at Fury Beach, twenty left it.
- **The plates were mis-titled by the image sweep.** They are now titled from the book's own
  plate list. In particular: the plate captioned SHULANINA · TULLUACHIU · TIRIKSHIU (facing
  p. 272, artifact -070) is Tulluahiu's family, with VICTORY lettered on the wooden leg, not a
  generic "group of Netsilingmiut"; artifact -072 is UMINGMAK (Commander J. C. Ross killing a
  musk bull), not "Quingmak"; artifact -074 is Graham's Valley, not Victory Point; -077 is
  Tilson's Islands, not "the pillar"; -080 is the surveyed plan of Victoria Harbour, which
  marks the ship's berth and Dixon's grave.
- The number in James Clark Ross's magnetic-pole party is **not stated** in either book. Do
  not write "six". John Ross says only that it consisted chiefly of the mates Blanky and
  Abernethy under his nephew's orders, and that four of it were snow-blind by 28 May.

## Other unresolved conflicts on the rows

- Ross's 1833 dispatch and his journal disagree by a day over the Fury Beach week of August
  1829 (dispatch 13 and 15 August, journal 12 and 14). Both are recorded; the journal is used.
- The dispatch says Sheriff's Harbour was cut into "about the middle of November" 1830; the
  journal says the cutting was given up on 31 October. The journal is used.

## Wanted next

- **Rasmussen's *Netsilik Eskimos*** (staged at `_staging/netsilikeskimoss00rasm.txt`) is the
  Netsilingmiut side of this coast ninety years later and has still not been read against this
  topic. It is the single biggest improvement available to
  `the-netsilingmiut-and-the-victory`, which at present rests entirely on Ross.
- The appendix's *Sketch of the Esquimaux found in the Territory of Boothia Felix* names and
  describes perhaps twenty Boothians; nine are entered as people. Its portraits have not been
  cut from a scan, and its four years of meteorological tables are untouched.
- Burford's 1834 Leicester Square panorama of Boothia (`_staging/burford-boothia.txt`).
- Request #18 (Nunavut Archaeology Program) was answered: a permit, not an email, is needed.
