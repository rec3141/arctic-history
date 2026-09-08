# Resume state for `thule-dorset`

Status after run 2 (2026-09-08): **drafted**. Eight wiki pages, 34 artifacts,
18 sources, 13 people, 8 places, 73 date rows. The worklog in the database is
the authority; read it with `tools/history-db.py resume --topic thule-dorset`.

## Downloaded into `files/` (8) — do not re-fetch

| file | what it is |
| --- | --- |
| `thule-dorset-igloolik-dorset-remains.pdf` | Lynnerup et al. 2003, *Human Dorset Remains from Igloolik*, Arctic 56(4):349- ; the four Alarnerk individuals and Meldgaard's raised-beach chronology |
| `thule-dorset-schledermann1978-bache.pdf` | Schledermann 1978, Arctic 31(4):459-474; the 1977-78 Bache Peninsula seasons, the 45 m Knud Peninsula longhouse, the cooking rows, Skraeling Island House 6 |
| `thule-dorset-schledermann-mccullough1980-western.pdf` | Schledermann & McCullough 1980, Arctic 33(4):833-841; Alaskan pottery, needle cases, brow band and Sicco harpoon heads in the Ruin Island houses |
| `thule-dorset-park2003-brooman-longhouse.pdf` | Park 2003, Etudes/Inuit/Studies 27(1-2):239-253; the Brooman Point Late Dorset longhouse and its three hearth rows |
| `thule-dorset-helmer1991-north-devon.pdf` | Helmer 1991, Arctic 44(4):301-317; six Paleo-Inuit complexes on Devon Island and the 1700-year abandonment |
| `thule-dorset-mallikjuaq-thule-site-1995.jpg` | Ansgar Walk, Thule house ruins, Mallikjuaq Island opposite Kinngait; CC BY-SA 2.5 |
| `thule-dorset-qarmaq-relicts-1996.jpg` | Ansgar Walk, qarmaq ruins, Ukkusiksalik National Park; CC BY-SA 2.5 |
| `thule-dorset-meliadine-thule-tent-ring-1995.jpg` | Ansgar Walk, Thule tent ring, Meliadine River near Kangiqliniq; CC BY-SA 2.5 |

Plain-text extractions of the PDFs were made with `pdftotext` in the run's
scratchpad and not kept; re-run `pdftotext` if you need them.

## Material elsewhere that this topic already draws on

- `../_staging/intellectualcult00rasm_1.txt` — Rasmussen, *Intellectual Culture
  of the Iglulik Eskimos*. Ivaluardjuk on the Tunit at pp. 256-257; the
  Takanakapsaluk house "just like the houses of the tunit" at p. 126.
- `../inuit-oral-history/files/inuit-oral-history-boas-central-eskimo.txt` —
  Boas, *The Central Eskimo*. Tornit narrative pp. 634-636; Songs of the Tornit
  pp. 649 and 653-654; the *tumiujang* lamp is Fig. 542 on p. 634.
- Places owned by `norse-helluland` and reused here rather than re-entered:
  Skraeling Island, Alexandra Fiord, Ruin Island, Nunguvik.

## Known not-got

- `https://www.gutenberg.org/files/42084/42084-h/images/fig542.png` (Boas's
  lamp engraving). A valid 98 x 128 PNG of 3,825 bytes; `history-fetch.py`
  refuses it as too small to be a real file, with and without `--force`.
  Registered as artifact `thule-dorset-022` with `--download-url` and no local
  file.
- Rast & Wolff 2016, *Open Archaeology* 2(1), on the Button Point drums. Open
  access, but De Gruyter refused every fetch from this network on 2026-09-08.
  Registered as `rast2016instruments` from its DOAJ record only.
- McCullough 1989, *The Ruin Islanders* (Mercury 141). Purchase only from
  University of Ottawa Press; no free copy found. Registered as
  `mccullough1989ruin`, cited but not read.
- Taylor 1968, *The Arnapik and Tyara Sites*. JSTOR, not pulled. Needed to
  settle the Tyara maskette's date (see request #36).

See `../_staging/MANIFEST.md` for everything staged, and `../BRIEF.md` for the
task.
