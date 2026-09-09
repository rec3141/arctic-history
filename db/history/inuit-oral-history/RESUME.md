# Resume state for `inuit-oral-history`

Run 1 (grid, 2026-09-08) worked this topic from nothing in the database to a
drafted topic. An image sweep added the Rink 1875 woodcuts on 2026-09-09, and a
review (grid, 2026-09-09) checked every quotation against the texts on disk and
promoted all seven pages to `good`. Read
`history-db.py resume --topic inuit-oral-history` first; this file only records
things the database does not hold.

## What the review changed, and where the evidence is

- **The Parry chart is March 1822, not February.** The account of how the charts
  were got stands at pp. 196-198 of `../_staging/journalofsecondv00parr.txt`
  (about lines 17300-17410), inside the March entries: the marginal month reads
  *March* from line 16808, and line 16756 fixes *Sat. 2* March. The weekday
  clues alone do not decide it, because 1 February and 1 March 1822 were both
  Fridays. `ross-parry` had already corrected its copy of the same plate.
- **The surviving plate is Chart No. 1, the one Parry judged wrong.** Its
  cartouche reads "THE ESKIMAUX CHART No. 1, Drawn by ILIGLIUK, at Winter
  Island. 1822. The Original in the possession of Capn. Lyon." Parry says this
  chart puts Repulse Bay, Winter Island and Amitioke nearly in line "though they
  are in fact exactly at right angles"; the second, small-scale chart, drawn
  after she boxed the compass, is the one that carried the coast west, and its
  plate is **not on disk**. Finding it would be a real addition.
- **The chart spells AMITIOKE**, one *t*, and so does Parry's text throughout.
- **Boas page numbers** come from the `name="pageNNN"` anchors in
  `../_staging/boas.html`, which is the only copy here that carries them; the
  Gutenberg plain text does not. Two quotes were off by nine pages and fig. 546
  by one.
- **The Rink plates' page positions** were checked with
  `pdftotext -f LEAF -l LEAF` on `files/inuit-oral-history-rink1875-tales.pdf`.
  The four front plates are unpaginated inserts between printed pp. 6-13, and
  several carry engraved captions after all ("Winter house.", "Woman with a
  child in the amowt", "A girl in holiday costume", "The large Lance or Spear").
  Rink names no artist: the title page says only "drawn and engraved by Eskimo",
  so the attribution to Aron of Kangeq was removed and wants a source.
- **Gilder names the Ookjoolik witness Ikinnelikpatolok** (pp. 78-79). The name
  *Puhtoorak* does not occur anywhere in `schwatkassearchs00gild.txt`.

## Files in `files/`

Every file is registered, either as an artifact or as a source's local copy.
Note the three renames:

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
- `inuit-oral-history-rink1875-tales.pdf` and the nine `...-rink-*.png` cuts
  came from the Internet Archive scan `talestraditionso01rink`.
- Seven web pages were cached by the review and attached to their source rows,
  not to artifacts: `...-dcb-tattannoeuck.html`, `...-dcb-eenoolooapik.html`,
  `...-dcb-ooligbuck.html`, `...-dickens1854-householdwords.xml` (the server
  sends XML, so the fetch tool rejects an `.html` name),
  `...-harper2018-kamookak.html` (the file name kept, though the column is of
  2025 and the bibkey is now `harper2025kamookak`),
  `...-walker2018-kamookak.html`, `...-parkscanada-guardians.html`.
- `files/faces/` holds the four crops made by `tools/faces.py`. It is not an
  artifact and `resume` will always list it as unregistered.

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

## Still open after the review

1. Rasmussen's Fifth Thule reports (see above) are still untouched and deserve a
   page, with Arnarulunnguaq and Qaavigarsuaq entered as people.
2. Boas's place-name glossary: several hundred names with meanings, none
   entered, and none checked against the Inuit Heritage Trust database at
   ihti.ca.
3. Iligliuk's **second** chart, the accurate one, is not on disk.
4. The Commons original of the Ebierbing/Tookoolito tintype (1235x1030 PNG) is
   still unfetched; run 1 got HTTP 429.
5. McDonald, *Narrative of Some Passages in the History of Eenoolooapik*
   (Edinburgh, 1841), would be a strong primary source and was never fetched.
6. Four claims about the Guardians could not be supported from anything on disk
   and were taken out of `knowledge-alive-today`: that the Nattilik Heritage
   Society administers the programme; that the Guardians have standing to report
   incidents to law enforcement; that they were the only people at the sites
   during the pandemic seasons; and the ten-year Inuit Impact and Benefit
   Agreement of March 2023, with the Erebus bell at the Nattilik Heritage Centre
   and the Umiyaqtutt Festival. All are plausible and probably true; each needs
   a citable page.
7. Request #12 (Gjoa Haven orthography, filed by `amundsen-gjoa`) is answered
   only "will see what i can do", so no orthography has landed to apply.
   Request #14, asking the Nattilik Heritage Society to review this topic, was
   denied. No page here has been read by a person from the communities it
   describes.
8. Where the original manuscript charts now are is still unknown: Ross 1835 says
   the Boothia original was in Captain Ross's possession and Parry 1824 says
   Iligliuk's was in Captain Lyon's, and neither has been traced to a holding
   institution.
9. Kamookak's great-grandmother's name, often given online, is deliberately
   omitted: neither obituary on disk confirms it. Harper's column calls William
   (Paddy) Gibson his grandfather in one paragraph and his father in another, so
   the pages say only "his forebears included".

See `../_staging/MANIFEST.md` for everything staged, and `../BRIEF.md` for the
task.
