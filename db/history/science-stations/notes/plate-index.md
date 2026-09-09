# Plate and table index — science-stations

Method: `pdfinfo`, `pdfimages -list`, `pdftotext -layout` split on form-feed, scripted word-count
and caption-keyword sweep (Fig./FIG./Plate/PLATE/Table/TABLE/Map/Frontispiece), plus printed-page
recovery from OCR running folios. No page images were viewed — verify visually before cutting.

---

## E. Koenig et al., "Arctic Ice Islands" (*Arctic*, 1952)

File: `science-stations/files/science-stations-koenig1952-ice-islands.pdf`
38 pages (pdfinfo) + 1 trailing blank pdftotext split. Page-scan PDF (Adobe Acrobat Capture 3.0,
CCITT fax): exactly 1 full-page image per page for all 38 pages — every page, whether body text or
illustration, is a single scanned raster, so image count cannot distinguish plate pages from text
pages here; figures are photographs (or maps/diagrams) printed inset within the running text on
the same scanned page as body copy, not on separate plate leaves. Printed pagination runs
pdf_page + 65 = printed page (pdf 1 = printed 66 title page/unnumbered, pdf 2 = printed 67, …
pdf 38 = printed 103), confirmed against running heads recovered by OCR.

The article is illustrated with numbered figures 1–20 (no plates, no tables — see notes). Most
captions were read directly from OCR; a handful of figures are referenced repeatedly in the
running text ("(Fig. N)") but their own caption text did not survive OCR (photo captions in
smaller/italic type OCR very poorly in this scan) — these are listed as "referenced only" with
the pdf pages where the reference occurs, plus the two near-blank pages that are the best
candidates for holding an un-OCR'd figure.

| pdf page | printed page | caption or subject | kind |
|---|---|---|---|
| 1 | 66 | Fig. 1. "The shelf ice on the north coast of Ellesmere Island, with Disraeli Bay upper right, and Ward Hunt Island at its mouth, 16 July 1950." Credit R.C.A.F. | photo (aerial) |
| 3 | 68 | Fig. 2. "Recent radar photograph of T1, January 1952." Credit U.S.A.F. | photo (radar) |
| 4 | 69 | Fig. 3. "Approximate paths of T1, T2, and T3 plotted at 3-monthly intervals." | map |
| 5 | 70 | Fig. 4. "T2 from a range of 45 miles, 22 July 1950." Credit U.S.A.F. | photo (aerial) |
| 7 | 72 | Fig. 6. "Low-level photograph of part of T1, 1 August 1951. The coast of Ellesmere Island in the background, with Ward Hunt Island and Disraeli Bay upper right." | photo (aerial) |
| 9 | 74 | Fig. 7. "T3 under snow from 250 feet, showing mounds probably of morainic material (cf. Fig. 16), 10 May 1951." | photo (aerial) |
| 11 | 76 | Fig. 8 (OCR misread as "Fig. II"). "Ice Island off Cape Columbia, July 1947. This island must have broken away from the shelf ice shown in Fig. 9." Credit U.S.A.F. | photo (aerial) |
| 12 | 77 | Fig. 9. "Shelf ice off Cape Nares, June 1950, showing a jagged line marking where the island in Fig. 8 has broken away. The gap left has been filled with smooth fast ice." Credit R.C.A.F. | photo (aerial) |
| 14 | 79 | Fig. 10. "Ice islands shown on air photographs in the Canadian Archipelago. The areas of the islands are not correct for scale, but do give their approximate relative sizes." | map |
| 17 | 82 | Fig. 15. "Ice island in Victoria Strait, August 1919. A smaller island is beyond it and also several slivers which have probably broken off it." Credit (garbled, likely R.C.A.F.) | photo (aerial) |
| 22 | 87 | Fig. 18. "Dobbin Bay, east Ellesmere Island, showing glaciers and their flat-topped bergs, 24 June 1950. Note the tributary glacier upper left which no longer joins the main one…" Credit R.C.A.F. | photo (aerial) |
| 25 | 90 | Fig. 19. "Vertical air photograph of old ice floes in Smith Sound, 24 June 1950. The uneven, worn-down topography of such floes might easily give rise to descriptions by ground travellers that sound like ice islands." | photo (aerial) |
| 28 | 93 | Fig. 20. "Yelverton Bay, north Ellesmere Island, 15 July 1950. Very little of the shelf ice remains in this bay. Note the ice island near the edge of the fast ice at upper left." Credit R.C.A.F. | photo (aerial) |
| 15 | 80 | *Un-OCR'd page — 0 words extracted, single full-page scan. Strongest candidate for one of the missing figures below (Fig. 5, 12, 13, and/or 14 are all referenced around this point in the text but not located).* | photo (uncaptioned/OCR failed) |
| 19 | 84 | *Near-blank page — only "Stor Island to the left." survived OCR, evidently the tail end of a caption. Best candidate for Fig. 16 or Fig. 17 (both referenced nearby but not located).* | photo (uncaptioned/OCR failed) |

Figures referenced in the running text but whose own caption/page could not be confidently
located by this sweep: **Fig. 5** (between Fig. 4 on pdf 5 and Fig. 6 on pdf 7 — likely pdf 6),
**Fig. 12, 13, 14** (referenced on pdf 13 as "(Fig. 13)" and "(Fig. 17)", and on pdf 16 as
"(Fig. 14)" and "(Fig.15)" — likely somewhere pdf 13–16), and **Fig. 16, 17** (referenced
repeatedly, e.g. pdf 9, 26, 33 for Fig. 16 — likely pdf 18–21, see the near-blank pdf 19 above).
A visual page-through of pdf 6, 8, 10, 13, 15–16, 18–21 is recommended to pin these down.

No tables of any kind (data, meteorological, or contents) were found in this article — grepped
throughout for "table"; the only hit is the substring inside "unstable," not a real table.

Total for E: 13 figures located with captions (11 photographs + 2 maps) + up to 7 further figures
(numbers 5, 12, 13, 14, 16, 17, and possibly a duplicate count) referenced in text but not
confidently located by OCR — see the two flagged near-blank pages above. No tables.

---

## D. Dick, "Muskox Land" — excerpt pp. 299–351 (in *Muskox Land: Ellesmere Island and the
Age of Contact*, 2001)

File: `oxford-ellesmere-1934/files/oxford-ellesmere-1934-dick2001-muskoxland-pp299-351.pdf`
54 pages (pdfinfo), a Scholars Portal Books download of pages 325–377 of the source book
(page 1 of this PDF is a Scholars Portal cover/permalink sheet, not part of the book). Digital
PDF (itext/pdftk-java), but every content page carries its own full-page CCITT background scan
(~1700×2650 px) plus, on four pages only, a second small JPEG image (~650×450–900 px, gray) —
that second image is the actual embedded photograph/map; pages with only the single background
scan have no embedded illustration. Printed pagination runs pdf_page + 296 = printed page
(pdf 2 = printed 298 … pdf 54 = printed 350), confirmed against running folios recovered by OCR.

| pdf page | printed page | caption or subject | kind |
|---|---|---|---|
| 4 | 300 | Figure 66: "Routes of RCMP Patrols on Ellesmere Island and adjacent islands, 1922–1940" | map |
| 26 | 322 | Figure 67: "'View taken from a point about 81° W. between Bay Fiord and Flagler Fiord [Ellesmere Island] (taken towards south).' Photograph by Christian Vibe, Van Hauen Expedition, May 1940. National Archives of Canada Photo no. C-137056." | photo |
| 42 | 338 | Figure 68: "'Robert Edwin Peary, full-length portrait, standing on deck of ship or dock, facing left, distributing gifts to Eskimos, Greenland.' Library of Congress (Washington, DC), Photo no. LC-USZC4-7505" | photo |
| 45 | 341 | Figure 69: "'Eskimo with kometaho,' Credit: American Museum of Natural History (New York City), Donald B. MacMillan Collection, Crocker Land, 1913–17, Negative no. 231657." | photo |

Notes:
- The text also references Figure 66 (p.3, "led (Figure 66)"), Figure 33 (pdf 38, faces page
  ~334), Figure 16 (pdf 50, ~page 346), and Figure 75 (pdf 52, ~page 348) — but pages 38, 50, and
  52 carry only the single full-page background scan with no second embedded image, meaning
  Figures 33, 16, and 75 belong to earlier/later parts of the source book *not included* in this
  299–351 excerpt. Do not expect to find them in this PDF.
- pdf page 1 is the Scholars Portal cover sheet (permalink, page range, download date) — not book
  content.
- pdf pages 10, 32, 34 are printed "This page intentionally left blank" (genuine blank leaves in
  the original book).
- pdf page 33 is the Part III divider page ("PART III — CHANGE: The Interplay of Cultures and the
  Environment, 1850–1940").
- No tables of any kind were found — grepped throughout for "table"; all hits are false positives
  ("Constable," "suitable").

Total for D: 4 photographs/maps, all with full captions and credits. No tables. Three
figure numbers referenced in the text are not present in this excerpt (see notes).
