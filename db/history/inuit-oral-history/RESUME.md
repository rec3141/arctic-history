# Resume state for `inuit-oral-history`

Run 1 (grid, 2026-09-08) worked this topic from nothing in the database to a
drafted topic. Read `history-db.py resume --topic inuit-oral-history` first;
this file only records things the database does not hold.

## Files in `files/` (14)

All are registered as artifacts. Note the three renames:

- `inuit-oral-history-iligliuk-chart-1822-full.jpg` — 2582x3192 plate scan of
  Eskimaux Chart No. 1, fetched from Commons. It **replaces** the 1024px
  `...-iligliuk-chart-1822.jpg` the first run fetched, which was a thumbnail
  and has been deleted.
- `inuit-oral-history-boothia-inuit-map-1829-full.jpg` — 1052x860 Commons
  original of "Chart drawn by the natives". Replaces the deleted 1024px copy.
- `inuit-oral-history-ebierbing-1873-full.jpg` — 1038x1729 Smithsonian
  photograph by T. W. Smillie. Replaces the deleted 800x1333 copy.
- `inuit-oral-history-ebierbing-tookoolito-tintype.jpg` is still a 1024px
  derivative. The Commons original (File:Tintype of Ebierbing (Joe) and
  Tookoolito (Hannah).png, 1235x1030) was not fetched: Commons returned
  HTTP 429. A later run should retry it, one request at a time.
- `inuit-oral-history-ross1835-narrative.txt` — fetched by run 1 from Internet
  Archive `narrativeofsecon00ross`. The Boothia chart chapters are at roughly
  lines 12700-15700 of the OCR (January to April 1830).
- The Boas figures and Plate II/IV come from the Project Gutenberg HTML of
  ebook 42084 and are at original size; they are small line cuts.

## Relevant material in `../_staging/`

- `memoirsofhanshen00hendrich.txt` — Hans Hendrik's Memoirs, registered as
  artifact `inuit-oral-history-027` pointing at the staging copy.
- `journalofsecondv00parr.txt` — Parry 1824; the Iligliuk chart passages are at
  roughly lines 17300-17410.
- `melancholyfateof00raej.txt` — Rae 1854; the report to the Admiralty is at
  lines 130-260.
- `schwatkassearchs00gild.txt` — Gilder 1881; Ikinnelikpatolok at lines
  2900-2960, Tooktoocheer and Ogzeuckjeuwock at 3700-3900.
- `rasmussen-netsilik.txt`, `netsilikeskimoss00rasm.txt`,
  `intellectualcult00rasm_1.txt` — Rasmussen's Fifth Thule reports. **Not yet
  used.** They are the largest untouched body of Netsilik and Iglulik oral
  tradition in staging and are the obvious next job.
- `qtc-*.txt/pdf` — Qikiqtani Truth Commission. Only the Nuutauniq foreword is
  cited so far.
- `commons-meta.json`, `titles.txt`, `boas-imgs.txt` — cached Commons lookups.
  None of them cover this topic's images; run 1 queried Commons directly, one
  request at a time, and hit a 429 on the fourth.

See `../_staging/MANIFEST.md` for everything staged, and `../BRIEF.md` for the
task.
