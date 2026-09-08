# Resume state for `ross-victory`

Run 1 (grid, 2026-09-08) worked this topic from nothing to `drafted`. Read the worklog with
`tools/history-db.py resume --topic ross-victory` first; this file only records what is on
disk and how to find things inside the texts.

## Files in `files/` (8)

| file | what it is |
| --- | --- |
| `ross-victory-narrative-1835.txt` | **THE** source. John Ross, *Narrative of a Second Voyage* (1835), full OCR of the University of Pittsburgh Darlington copy. This IS the real Ross 1835 - it was verified against the title page in run 1. Clean OCR; words are separated by double spaces, so grep with `\s+` collapsed or you will get false misses (`magnetic  pole`, not `magnetic pole`). 29,855 lines. |
| `ross-victory-appendix-1835.txt` | The *Appendix* volume: James Clark Ross's magnetic tables, the *Sketch of the Esquimaux found in the Territory of Boothia Felix* with individual portraits and descriptions, the English-Danish-Esquimaux vocabulary, natural history, the surgeon's report and the biography of the crew. Dirtier OCR than the narrative. |
| `ross-victory-huish-1835.txt` | Robert Huish's rival, hostile account. Use as a witness against Ross, never as independent fact. |
| `ross-victory-netsilingmiut-excerpt.txt` | Cut in run 1: narrative chapters XVI-XXVI, pp. 239-381. |
| `ross-victory-magneticpole-excerpt.txt` | Cut in run 1: narrative chapters XLII-XLIII, pp. 549-572. |
| `ross-victory-retreat-excerpt.txt` | Cut in run 1: narrative chapters XLIX-LVII, pp. 632-730. |
| `ross-victory-somerset-house.jpg` | Commons plate of Somerset House, 955x719. |
| `notes/ross-dispatch-1833.md` | Ross's dispatch to the Admiralty, September 1833, transcribed whole. **Start here**: it is the entire voyage chronology in about 2,500 words in his own hand. |

**Do not cite `_staging/cihm_08551.txt`.** It is not Ross 1835 despite an old manifest line.
A second OCR of the same narrative, from the Internet Archive scan `narrativeofsecon00ross`,
lives at `inuit-oral-history/files/inuit-oral-history-ross1835-narrative.txt`; it is an HTML
page wrapping the text and is harder to read than the copy here. Both carry bibkey
`ross1835narrative`.

## Finding things in the narrative

Marginal dates are printed as `Jan. 9.`, `August 12`, `Sept. i7.` and so on, often OCR'd
badly and often several lines away from the entry they belong to. The table of contents
(around line 1321) lists all 57 chapters with page numbers and is the fastest index.
A search helper that collapses whitespace was used in run 1; rebuild it in a scratchpad
rather than editing anything under `tools/`.

## What run 1 could not settle

- Ross's dispatch and his journal disagree by a day over the Fury Beach week of August 1829
  (dispatch 13 and 15 August, journal 12 and 14). Both are recorded on the event rows.
- The dispatch says Sheriff's Harbour was cut into "about the middle of November" 1830; the
  journal says the cutting was abandoned on 31 October. The journal is followed.
- Victoria Harbour's position: James Clark Ross's magnetic table gives 70 09 18 N /
  91 30 33 W, the narrative gives 70 18 11 N for the harbour entered on 29 August 1831.
  Unreconciled; the magnetic table is used.
- James Clark Ross prints Victory Point as 69 37 49 N, well south of the modern feature of
  that name at 69.97. Either his error or the OCR's.
- Sheriff's Harbour and Cape Garry positions are inferred from distances, not observed.

## Wanted

- The plates of Ross 1835 at full size, especially *Ikmallik and Apelagliu*, *Tulluachiu and
  Family*, *Felix Harbour (Summer)* and *(Winter)*, *Victory under sail for the last time*,
  *Victory's Crew saved*, and the general chart at the end. Only *Somerset House* was found
  on Commons in run 1; the rest should come from the Internet Archive page images of
  `narrativeofsecon00ross`, which were not fetched.
- Rasmussen's *Netsilik Eskimos* (staged at `_staging/netsilikeskimoss00rasm.txt` and
  `rasmussen-netsilik.txt`) is the Netsilingmiut side of this coast ninety years later and
  has not been read against this topic at all.
- The Commons panorama item *Description of a view of the continent of Boothia, discovered
  by Captain Ross* (Burford's Leicester Square panorama, 1834) - `_staging/burford-boothia.txt`
  is the staged text and was not used in run 1. It is how the British public saw Boothia.
- Request #18 is open with the Nunavut Archaeology Program about whether the wintering sites,
  the engine at Felix Harbour and the magnetic pole cairn are recorded.
