# Sources cleanup: archive names and entry types

474 sources. `archive` holds 126 distinct values in 359 rows; the alias table and the detail rules bring them to 78 names, rewriting 114 rows.
`entry_type` is misc on 431 rows; the rules type 374 of them and leave 57 for review.

## The archive field, before and after

A name in **bold** is the one the variants merge into. `callno` takes the identifiers of the copy, `note` the citation and the route. A citation that only repeats the row's own volume and pages is dropped, and shown here in brackets.

| rows | before | after | to callno | to note |
|---:|---|---|---|---|
| 97 | Internet Archive | (unchanged) |  |  |
| 3 | Internet Archive (University of Toronto, Robarts government publications), item 31761116488701 | **Internet Archive** | item 31761116488701 | University of Toronto, Robarts government publications |
| 2 | Internet Archive (University of Alberta Libraries, circumpolar collection) | **Internet Archive** |  | University of Alberta Libraries, circumpolar collection |
| 2 | Internet Archive (University of Toronto, Robarts government publications), item 31761116488826 | **Internet Archive** | item 31761116488826 | University of Toronto, Robarts government publications |
| 1 | Internet Archive (CIHM microfiche 29328) | **Internet Archive** | CIHM microfiche 29328 |  |
| 1 | Internet Archive (CIHM microform 22431) | **Internet Archive** | CIHM microform 22431 |  |
| 1 | Internet Archive (borrow only) | **Internet Archive** |  | borrow only |
| 1 | Internet Archive (CIHM microform 37570) | **Internet Archive** | CIHM microform 37570 |  |
| 1 | Internet Archive (CIHM microform) | **Internet Archive** |  | CIHM microform |
| 11 | Arctic Institute of North America | (unchanged) |  |  |
| 8 | Arctic (AINA) | **Arctic Institute of North America** |  |  |
| 5 | Arctic (journal), University of Calgary | **Arctic Institute of North America** |  |  |
| 4 | ARCTIC (University of Calgary) | **Arctic Institute of North America** |  |  |
| 4 | ARCTIC journal | **Arctic Institute of North America** |  |  |
| 3 | Arctic, journalhosting.ucalgary.ca | **Arctic Institute of North America** |  |  |
| 2 | ARCTIC, University of Calgary journal hosting | **Arctic Institute of North America** |  |  |
| 2 | University of Calgary Journal Hosting | **Arctic Institute of North America** |  |  |
| 1 | Arctic 32(2): 91-121 | **Arctic Institute of North America** |  |  [32(2): 91-121] |
| 1 | Arctic 36(3): 294-295 (Arctic Profiles) | **Arctic Institute of North America** |  | Arctic Profiles |
| 1 | Arctic 36(4): 380-381 (Arctic Profiles) | **Arctic Institute of North America** |  | Arctic Profiles |
| 19 | Wikimedia Commons | (unchanged) |  |  |
| 1 | Wikimedia Commons; sold at Bonhams, lot 25707/27 | **Wikimedia Commons** |  | sold at Bonhams, lot 25707/27 |
| 1 | Wikimedia Commons; originals in Toronto Public Library, Library and Archives Canada and the Royal Museums Greenwich | **Wikimedia Commons** |  | originals in Toronto Public Library, Library and Archives Canada and the Royal Museums Greenwich |
| 1 | Wikimedia Commons; Christie's LotFinder 102661 | **Wikimedia Commons** |  | Christie's LotFinder 102661 |
| 1 | Wikimedia Commons; print held in the Resolute archives | **Wikimedia Commons** |  | print held in the Resolute archives |
| 1 | Wikimedia Commons, from Flickr | **Wikimedia Commons** |  | from Flickr |
| 1 | Wikimedia Commons / Government of Canada Publications, cat. D12-19/1E-PDF | **Wikimedia Commons** | cat. D12-19/1E-PDF |  |
| 17 | Cambridge Core | (unchanged) |  |  |
| 1 | Polar Record 5(40): 543-556 | **Cambridge Core** |  |  [5(40): 543-556] |
| 1 | Polar Record 23(144): 289-299 | **Cambridge Core** |  |  [23(144): 289-299] |
| 6 | Dictionary of Canadian Biography | (unchanged) |  |  |
| 3 | Dictionary of Canadian Biography, vol. 10 | **Dictionary of Canadian Biography** |  | vol. 10 |
| 2 | Dictionary of Canadian Biography, vol. 8 | **Dictionary of Canadian Biography** |  | vol. 8 |
| 1 | Dictionary of Canadian Biography, vol. 9 | **Dictionary of Canadian Biography** |  | vol. 9 |
| 1 | Dictionary of Canadian Biography, vol. 12 | **Dictionary of Canadian Biography** |  | vol. 12 |
| 1 | Dictionary of Canadian Biography, vol. 11 | **Dictionary of Canadian Biography** |  | vol. 11 |
| 14 | Qikiqtani Truth Commission | (unchanged) |  |  |
| 9 | Publications du gouvernement du Canada / Government of Canada Publications, via the Internet Archive Wayback Machine | **Government of Canada Publications** |  | via the Internet Archive Wayback Machine |
| 1 | Government of Canada Publications | (unchanged) |  |  |
| 1 | Government of Canada Publications (via the Internet Archive Wayback Machine) | **Government of Canada Publications** |  | via the Internet Archive Wayback Machine |
| 11 | JSTOR | (unchanged) |  |  |
| 6 | Public Safety Canada Library, archived collection | **Public Safety Canada Library** |  | archived collection |
| 2 | Public Safety Canada library | **Public Safety Canada Library** |  |  |
| 4 | American Museum of Natural History (Crocker Land Expedition Collection) | **American Museum of Natural History** |  | Crocker Land Expedition Collection |
| 1 | American Museum of Natural History, Museum Archives at the Gottesman Research Library | **American Museum of Natural History** |  | Museum Archives at the Gottesman Research Library |
| 1 | American Museum of Natural History | (unchanged) |  |  |
| 5 | Canadiana / Government of Canada sessional papers | **Canadiana** |  |  |
| 1 | Canadiana / Natural Resources Canada | **Canadiana** |  |  |
| 2 | Internet Archive Wayback Machine | (unchanged) |  |  |
| 2 | Internet Archive (Wayback capture) | **Internet Archive Wayback Machine** |  |  |
| 1 | Internet Archive Wayback Machine (canada.ca times out from this host) | **Internet Archive Wayback Machine** |  | canada.ca times out from this host |
| 1 | Internet Archive Wayback Machine (science.gc.ca is not reachable direct from this host) | **Internet Archive Wayback Machine** |  | science.gc.ca is not reachable direct from this host |
| 5 | Project Gutenberg | (unchanged) |  |  |
| 2 | Parks Canada | (unchanged) |  |  |
| 1 | Canadian Parks Service | **Parks Canada** |  |  |
| 1 | Parks Canada, Directory of Federal Heritage Designations | **Parks Canada** |  |  |
| 3 | Justice Laws Website | (unchanged) |  |  |
| 3 | University of Manitoba Libraries | (unchanged) |  |  |
| 2 | Canadian Museum of History | (unchanged) |  |  |
| 2 | Erudit | (unchanged) |  |  |
| 1 | HathiTrust (University of Illinois copy, uiug.30112125862554); shelf copy University of Manitoba, Elizabeth Dafoe Library | **HathiTrust** | uiug.30112125862554 | shelf copy University of Manitoba, Elizabeth Dafoe Library; University of Illinois copy |
| 1 | HathiTrust (University of Michigan copy) | **HathiTrust** |  | University of Michigan copy |
| 2 | John Carter Brown Library | (unchanged) |  |  |
| 2 | Library and Archives Canada | (unchanged) |  |  |
| 1 | Library of Congress, Prints and Photographs Division | (unchanged) |  |  |
| 1 | Library of Congress Prints and Photographs Division | **Library of Congress, Prints and Photographs Division** |  |  |
| 1 | Nasjonalbiblioteket (National Library of Norway), Flickr Commons | **Nasjonalbiblioteket (National Library of Norway)** |  | Flickr Commons |
| 1 | Nasjonalbiblioteket (National Library of Norway) | (unchanged) |  |  |
| 1 | Natural Resources Canada | (unchanged) |  |  |
| 1 | GeoGratis / Open Maps, Natural Resources Canada | **Natural Resources Canada** |  |  |
| 2 | North American and Arctic Defence and Security Network | (unchanged) |  |  |
| 1 | Scott Polar Research Institute | (unchanged) |  |  |
| 1 | Scott Polar Research Institute, Thomas H. Manning Polar Archives | **Scott Polar Research Institute** |  | Thomas H. Manning Polar Archives |
| 1 | Wikisource (proofread from the Google Books scan, Commons File:The Caribou Eskimos.djvu) | **Wikisource** |  | proofread from the Google Books scan, Commons File:The Caribou Eskimos.djvu |
| 1 | Wikisource (proofread from the Google Books scan, Commons File:Archaeology of the Central Eskimos.djvu); DjVu original kept in files/ | **Wikisource** |  | DjVu original kept in files/; proofread from the Google Books scan, Commons File:Archaeology of the Central Eskimos.djvu |
| 1 | Archivaria | (unchanged) |  |  |
| 1 | Arktisk Institut (Danish Arctic Institute), Copenhagen | (unchanged) |  |  |
| 1 | Bibliotheque de l'Universite Laval; University of Alberta Libraries (Internet Archive) | **Bibliotheque de l'Universite Laval** |  | University of Alberta Libraries (Internet Archive) |
| 1 | Bibliotheque nationale de France | (unchanged) |  |  |
| 1 | Bodleian Libraries, University of Oxford | (unchanged) |  |  |
| 1 | British Museum | (unchanged) |  |  |
| 1 | British Parliamentary Papers, Accounts and Papers 1852, vol. 50, no. 1435 | **British Parliamentary Papers** | no. 1435 | Accounts and Papers 1852; vol. 50 |
| 1 | Canada Treaty Information, Global Affairs Canada | (unchanged) |  |  |
| 1 | Canada.ca | (unchanged) |  |  |
| 1 | Canadian Meteorological and Oceanographic Society | (unchanged) |  |  |
| 1 | Crown-Indigenous Relations and Northern Affairs Canada | (unchanged) |  |  |
| 1 | DOAJ | (unchanged) |  |  |
| 1 | David Rumsey Map Collection | (unchanged) |  |  |
| 1 | ECCC GeoMet-OGC API | (unchanged) |  |  |
| 1 | Fisheries and Oceans Canada | (unchanged) |  |  |
| 1 | Fram Museum | (unchanged) |  |  |
| 1 | Geological Survey of Canada | (unchanged) |  |  |
| 1 | Government of Nunavut | (unchanged) |  |  |
| 1 | Great Unsolved Mysteries in Canadian History | (unchanged) |  |  |
| 1 | HBC Heritage | (unchanged) |  |  |
| 1 | HUDOC, European Court of Human Rights | (unchanged) |  |  |
| 1 | Haffenreffer Museum of Anthropology, Brown University | (unchanged) |  |  |
| 1 | Hudson's Bay Company Archives, Archives of Manitoba | **Hudson's Bay Company Archives** |  | Archives of Manitoba |
| 1 | Inuit Heritage Trust Traditional Place Names Program | (unchanged) |  |  |
| 1 | Moravian Archives, Bethlehem | (unchanged) |  |  |
| 1 | Musee maritime du Quebec | (unchanged) |  |  |
| 1 | NOAA Arctic Research Office, via Wikimedia Commons | **NOAA Arctic Research Office** |  | via Wikimedia Commons |
| 1 | National Galleries of Scotland | (unchanged) |  |  |
| 1 | National Museum of Canada | (unchanged) |  |  |
| 1 | National Portrait Gallery, London | (unchanged) |  |  |
| 1 | Naval History and Heritage Command, photograph H-2875 | **Naval History and Heritage Command** | photograph H-2875 |  |
| 1 | Norfolk Museums Service polar collections, via Wikimedia Commons | **Norfolk Museums Service polar collections** |  | via Wikimedia Commons |
| 1 | Nunatsiaq News | (unchanged) |  |  |
| 1 | Ohio State University Libraries, Byrd Polar and Climate Research Center Archives | **Ohio State University Libraries** |  | Byrd Polar and Climate Research Center Archives |
| 1 | PLOS | (unchanged) |  |  |
| 1 | PRISM / Scholaris, University of Calgary | (unchanged) |  |  |
| 1 | Qikiqtani Inuit Association | (unchanged) |  |  |
| 1 | Royal Danish Library | (unchanged) |  |  |
| 1 | Royal Museums Greenwich, via Wikimedia Commons | **Royal Museums Greenwich** |  | via Wikimedia Commons |
| 1 | Scholars Portal Books | (unchanged) |  |  |
| 1 | ScienceDirect | (unchanged) |  |  |
| 1 | Special Collections of the University of Amsterdam, via Wikimedia Commons | **Special Collections of the University of Amsterdam** |  | via Wikimedia Commons |
| 1 | Statistics Greenland StatBank | (unchanged) |  |  |
| 1 | Tate | (unchanged) |  |  |
| 1 | Tekniska museet via Flickr and Wikimedia Commons | (unchanged) |  |  |
| 1 | U.S. National Archives and Records Administration | (unchanged) |  |  |
| 1 | University of Manitoba Archives and Special Collections (Andrew Taylor fonds) | **University of Manitoba Archives and Special Collections** |  | Andrew Taylor fonds |
| 1 | University of Manitoba Libraries (Scholars Portal / Canada Commons) | (unchanged) |  |  |
| 1 | Vancouver Maritime Museum | (unchanged) |  |  |
| 1 | Wellcome Collection, Iconographic Collections | **Wellcome Collection** |  | Iconographic Collections |
| 1 | private collection; sold Christie's | **private collection** |  | sold Christie's |

## The calls worth arguing with

1. **A paper in *Arctic* is held at the Arctic Institute of North America**, not
   at "Arctic", "ARCTIC journal" or "University of Calgary Journal Hosting". The
   institute publishes the journal and serves the back run at
   pubs.aina.ucalgary.ca; the University of Calgary's journal hosting is where
   the current issues sit, an address rather than a holder. The journal title is
   what `container` is for, so putting it in `archive` as well says nothing and
   spells it eight ways. Eleven variants, forty-two rows.
2. **Polar Record goes to Cambridge Core**, the platform the copies were read
   from, on the same reasoning: the journal belongs in `container`.
3. **Three merges drop words.** "Canadiana / Government of Canada sessional
   papers" becomes Canadiana (the rows carry "Sessional Paper No. N" in
   `volume`); "Parks Canada, Directory of Federal Heritage Designations" becomes
   Parks Canada; "Wikimedia Commons / Government of Canada Publications" becomes
   Wikimedia Commons, keeping the catalogue number in `callno`. Say so if the
   dropped words were worth keeping.
4. **Canadian Parks Service becomes Parks Canada**: the same institution under
   the name it uses now.
5. **Two notes now carry a remark about this host** ("canada.ca times out from
   this host"), moved out of the archive field rather than invented. They are
   reader-facing on the source page; trim them if that is wrong.
6. **A newspaper or a news site is `online`, not `article`.** The BibTeX export
   now writes the container of an `online` entry as `journal`, so
   `journal = {Nunatsiaq News}` still comes out right.
7. **A statute or a treaty read on the Justice Laws Website is `online`.** The
   vocabulary has no type for legislation and `misc` says less.
8. **Eleven rows had the journal in `publisher`.** Where the name in front of the
   citation is beyond doubt ("Arctic (Arctic Institute of North America),
   39(4), 350-359", "Polar Geography 26(1), pp. 39-52") it is copied into the
   empty `container` and the row becomes an article, so the export has a journal
   to print. Fifteen more, where the name is a society or a press rather than a
   journal, are left misc under "Still misc" for a person to finish.
9. **An artwork, a photograph, a manuscript journal and a run of expedition
   negatives stay `misc`.** That is what the type is for, and forty of the
   fifty-seven left are exactly that.

## The archives used by one source only

Not wrong, but the place drift shows first.

- Archivaria (cheshire1980frobishers)
- Arktisk Institut (Danish Arctic Institute), Copenhagen (arktiskinstitut2026billeder)
- Bibliotheque de l'Universite Laval (ulaval1909charts)
- Bibliotheque nationale de France (gerritsz1612tabula)
- Bodleian Libraries, University of Oxford (ketel1577frobisher)
- British Museum (white1577drawings)
- British Parliamentary Papers (greatbritain1852arctic)
- Canada Treaty Information, Global Affairs Canada (canada1988arctic)
- Canada.ca (wage2025kenojuak)
- Canadian Meteorological and Oceanographic Society (brunette2021ccgs)
- Crown-Indigenous Relations and Northern Affairs Canada (canada2010apology)
- DOAJ (rast2016instruments)
- David Rumsey Map Collection (mercator1595septentrionalium)
- ECCC GeoMet-OGC API (eccc2026climate)
- Fisheries and Oceans Canada (ccg2026amundsen)
- Fram Museum (frammuseum2026gjoa)
- Geological Survey of Canada (thorsteinsson1961meighen)
- Government of Nunavut (nunavutparks2008kekerten)
- Great Unsolved Mysteries in Canadian History (dickens1854lost)
- HBC Heritage (hbcheritage2026nascopie)
- HUDOC, European Court of Human Rights (echr2006hingitaq)
- Haffenreffer Museum of Anthropology, Brown University (hayeursmith2018dorset)
- Hudson's Bay Company Archives (hbca2005nascopie)
- Inuit Heritage Trust Traditional Place Names Program (iht2025placenames)
- Moravian Archives, Bethlehem (moravian1971inventory)
- Musee maritime du Quebec (mmq1909bernier)
- NOAA Arctic Research Office (noaa2005ipy)
- National Galleries of Scotland (faulkner1834ross)
- National Museum of Canada (lowther1962account)
- National Portrait Gallery, London (drummond1820parry)
- Naval History and Heritage Command (navy1884survivors)
- Norfolk Museums Service polar collections (norfolk1880feilden)
- Nunatsiaq News (harper2020panipakuttuk)
- Ohio State University Libraries (osu1909cook)
- PLOS (swanston2018franklin)
- PRISM / Scholaris, University of Calgary (heidt2022joint)
- Qikiqtani Inuit Association (qtc2024qimmiliriniq)
- Royal Danish Library (munk1624navigatio)
- Royal Museums Greenwich (domville1852belcher)
- Scholars Portal Books (dick2001muskox)
- ScienceDirect (stenton2024identification)
- Special Collections of the University of Amsterdam (petermann1876skizze)
- Statistics Greenland StatBank (statgl2026population)
- Tate (collier1881last)
- Tekniska museet via Flickr and Wikimedia Commons (tekniska1910capeyork)
- U.S. National Archives and Records Administration (nara1909pole)
- University of Manitoba Archives and Special Collections (taylor1955geographical)
- University of Manitoba Libraries (Scholars Portal / Canada Commons) (grant2002arctic)
- Vancouver Maritime Museum (vmm2026stroch)
- Wellcome Collection (wellcome1875nares)
- private collection (jackson1823lyon)

## entry_type: what the rules assign

### article (130)

| bibkey | title | evidence |
|---|---|---|
| adams1989rare | A Rare Second Year - Lake Ice Cover in the Canadian High Arctic | container 'Arctic' is a periodical, volume 42(4) |
| aina1961devon | The Devon Island Expedition (Institute News) | container from the URL: 'Arctic' |
| armstrong1990tourists | Tourists visit the North Pole, 1990 | container 'Polar Record' is a periodical, volume 27(160) |
| artfulliving2018plaisted | A Look Back at the Epic Plaisted Polar Expedition | container 'Artful Living Magazine' is a periodical |
| baird1955glaciological | Glaciological Research in the Canadian Arctic | container 'Arctic' is a periodical, volume 8(2) |
| bankes1987forty | Forty Years of Canadian Sovereignty Assertion in the Arctic, 1947-87 | container from --publisher: 'Arctic' |
| baril2024policing | Policing the Arctic: Relations Between the Mounted Police and Inuit in | container 'Arctic' is a periodical, volume 77(2) |
| barr1984sverdrup | Otto Sverdrup (1854-1930) | container 'Arctic' is a periodical, volume 37(1) |
| barr1993career | The career and disappearance of Hans K.E. Krüger, Arctic geologist, 18 | container 'Polar Record' is a periodical, volume 29 (171) |
| barrett2020ecological | Ecological globalisation, serial depletion and the medieval trade of w | container 'Quaternary Science Reviews' is a periodical, volume 229 |
| bentham1941structure | Structure and Glaciers of Southern Ellesmere Island | container 'The Geographical Journal' is a periodical, volume 97 (1) |
| bertulli2013fort | Fort Conger: A Site of Arctic History in the 21st Century | container 'Arctic' is a periodical, volume 66 |
| binachon2021continuing | The Continuing Effects of Colonisation in Avanersuaq | container 'Arctic Yearbook 2021' is a periodical |
| bowman1968relict | Relict Populations of Drepanopus bungei and Limnocalanus macrurus grim | container 'Arctic' is a periodical, volume 21(3) |
| brooks2004krugers | Krüger's Final Camp in Arctic Canada? | container from the URL: 'Arctic' |
| brunette2021ccgs | The CCGS Amundsen: A Success Story in Arctic Oceanography | container 'CMOS Bulletin SCMO' is a periodical |
| cheshire1980frobishers | Frobisher's Eskimos in England | container 'Archivaria' is a periodical, volume 10 |
| copland2007rapid | Rapid loss of the Ayles Ice Shelf, Ellesmere Island, Canada | container 'Geophysical Research Letters' is a periodical, volume 34 |
| cox1936oxford | Oxford University Ellesmere Land Expedition: Discussion | container 'The Geographical Journal' is a periodical, volume 87 (5) |
| crary1956geophysical | Geophysical Studies Along Northern Ellesmere Island | container 'Arctic' is a periodical, volume 9(3) |
| dick2005redserge | Red Serge and Polar Bear Pants: The Biography of Harry Stallworthy, RC | container 'Arctic' is a periodical, volume 58(4) |
| dickens1854lost | The Lost Arctic Voyagers | container from --publisher: 'Household Words' |
| dunbar1955review | Review: Geographical Discovery and Exploration in the Queen Elizabeth  | container 'Arctic' is a periodical, volume 8(3) |
| dunbar1956review | Review: Geographical Discovery and Exploration in the Queen Elizabeth  | container from --publisher: 'Arctic' |
| england1974note | A Note on the Holocene History of a Portion of Northernmost Ellesmere  | container 'Arctic' is a periodical, volume 27(2) |
| eno2003crystal | Crystal Two: The Origin of Iqaluit | container from the URL: 'Arctic' |
| fraser1957activities | Activities of the Geographical Branch in Northern Canada, 1947-1957 | container 'Arctic' is a periodical, volume 10(4) |
| friesen2008timing | The Timing of the Thule Migration: New Dates from the Western Canadian | container 'American Antiquity' is a periodical, volume 73(3) |
| frisch2016keith | Keith Charles Arnold (1931-2014) | container 'Arctic' is a periodical, volume 69(2) |
| geographical1937note | A Note on the Oxford University Ellesmere Land Expedition, 1934 | container 'The Geographical Journal' is a periodical, volume 89 (3) |
| greenaway1988maclure | Kenneth C. Maclure, 1914-1988 | container 'Arctic' is a periodical, volume 41(3) |
| haigthomas1940discussion | Expedition to Ellesmere Island, 1937-38: Discussion | container 'The Geographical Journal' is a periodical, volume 95 (4) |
| haigthomas1940expedition | Expedition to Ellesmere Island, 1937-38 | container 'The Geographical Journal' is a periodical, volume 95 (4) |
| hall1863frobisher | Frobisher Strait proved to be a Bay, and on the Fate of Five Men of th | container 'Proceedings of the Royal Geographical Society of London' is a periodical, volume 7 |
| harington1982joy | A.H. Joy (1887-1932) | container 'Arctic' is a periodical, volume 35(4) |
| harington1983stallworthy | H.W. Stallworthy (1895-1976) | container 'Arctic' is a periodical, volume 36(3) |
| harington1989nookapingwa | Nookapingwa (1893-1956) | container 'Arctic' is a periodical, volume 42(2) |
| harper2002minik | The Minik Affair: The Role of the American Museum of Natural History | container from --publisher: 'Polar Geography' |
| hattersleysmith1955northern | Northern Ellesmere Island, 1953 and 1954 | container 'Arctic' is a periodical, volume 8(1) |
| hattersleysmith1957rolls | The Rolls on the Ellesmere Ice Shelf | container 'Arctic' is a periodical, volume 10(1) |
| hattersleysmith1967postglacial | Postglacial Uplift at Tanquary Fiord, Northern Ellesmere Island, North | container 'Arctic' is a periodical, volume 20(4) |
| hattersleysmith1973archaeological | An Archaeological Site on the North Coast of Ellesmere Island | container 'Arctic' is a periodical, volume 26(3) |
| hayeursmith2018dorset | Dorset, Norse, or Thule? Technological Transfers, Marine Mammal Contam | container 'Journal of Archaeological Science' is a periodical, volume 96 |
| helmer1992qitdlarssuaq | Review: Qitdlarssuaq: The Story of a Polar Migration, by Guy Mary-Rous | container 'Arctic' is a periodical, volume 45(4) |
| howse2013revisiting | Revisiting an Early Thule Inuit Occupation of Skraeling Island, Canadi | container 'Etudes/Inuit/Studies' is a periodical, volume 37 |
| humphreys1936ellesmere | Ellesmere Land and Grinnell Land | container 'The Geographical Journal' is a periodical, volume 87 (5) |
| iln1851portraits | Portraits of Captain Sir John Franklin and his Crew | container 'The Illustrated London News' is a periodical |
| iln1854relics | The Franklin Relics | container 'The Illustrated London News' is a periodical |
| imbert1986solo | Solo man-hauling journey to the North Pole | container 'Polar Record' is a periodical, volume 23(144) |
| jackson1961meteorological | Meteorological Research at Lake Hazen, 1961 | container 'Arctic' is a periodical, volume 14(4) |
| jackson1965vertical | The Vertical Profile of Wind at Lake Hazen, N.W.T. | container 'Arctic' is a periodical, volume 18(1) |
| jeffries1982ward | The Ward Hunt Ice Shelf, Spring 1982 | container 'Arctic' is a periodical, volume 35(4) |
| jeffries1983recent | Recent Changes at the Front of Ward Hunt Ice Shelf, Ellesmere Island,  | container 'Arctic' is a periodical, volume 36(3) |
| jeffries1985ice | Ice Shelf Studies off Northern Ellesmere Island, Spring 1983 | container 'Arctic' is a periodical, volume 38(3) |
| jeffries1992harold | Harold Victor Serson (1926-1992) | container 'Arctic' is a periodical, volume 45(3) |
| jenness1925new | A New Eskimo Culture in Hudson Bay | container 'The Geographical Review' is a periodical, volume 15(3) |
| johnson1990establishment | The Establishment of Alert, N.W.T., Canada | container 'Arctic' is a periodical, volume 43 |
| jolicoeur2021detecting | Detecting Early Widespread Metal Use in the Eastern North American Arc | container 'American Antiquity' is a periodical, volume 86 |
| keatley2007limnological | Limnological Characteristics of a High Arctic Oasis and Comparisons ac | container 'Arctic' is a periodical, volume 60(3) |
| king1988north | To the North Pole: review of North to the Pole by Will Steger and Paul | container 'Polar Record' is a periodical, volume 24(151) |
| knuth1952outline | An Outline of the Archaeology of Peary Land | container 'Arctic' is a periodical, volume 5 |
| kobalenko2012geoffrey | Geoffrey Hattersley-Smith (1923-2012) | container 'Arctic' is a periodical, volume 65(4) |
| kock2012bathymetry | Bathymetry and Sediment Geochemistry of Lake Hazen (Quttinirpaaq Natio | container 'Arctic' is a periodical, volume 65(1) |
| koenig1952arctic | Arctic Ice Islands | container 'Arctic' is a periodical, volume 5(2) |
| konecny1966studies | Studies of Ice Movements on the Ward Hunt Ice Shelf by Means of Triang | container 'Arctic' is a periodical, volume 19(4) |
| lotz1959paul | Paul Walker 1934-1959 | container 'Arctic' is a periodical, volume 12(4) |
| lotz1990brian | Brian Sagar (1927-1990) | container 'Arctic' is a periodical, volume 43(2) |
| lotz2006john | John Powell (1933-2005) | container 'Arctic' is a periodical, volume 59(2) |
| lyons1973holocene | Holocene History of a Portion of Northernmost Ellesmere Island | container 'Arctic' is a periodical, volume 26(4) |
| maclure1949polar | Polar Navigation | container 'Arctic' is a periodical, volume 2(3) |
| maher1970ecology | Ecology of the Long-Tailed Jaeger at Lake Hazen, Ellesmere Island | container 'Arctic' is a periodical, volume 23(2) |
| marshall1955structural | Structural and Stratigraphic Studies of the Northern Ellesmere Ice She | container 'Arctic' is a periodical, volume 8(2) |
| maryrousseliere1984viking | The Thule Culture and the Norse: Discussion of the Okivilialuk Figurin | container 'Arctic' is a periodical, volume 37 |
| mcghee1984contact | Contact between Native North Americans and the Medieval Norse: A Revie | container 'American Antiquity' is a periodical, volume 49 |
| mcrae1986management | Management of Arctic Marine Transportation: A Canadian Perspective | container from --publisher: 'Arctic' |
| moore1936sledge | The Sledge Journey to Grant Land | container 'The Geographical Journal' is a periodical, volume 87 (5) |
| mueller2003breakup | Break-up of the largest Arctic ice shelf and associated loss of an epi | container 'Geophysical Research Letters' is a periodical, volume 30(20) |
| mueller2008examining | Examining Arctic Ice Shelves Prior to the 2008 Breakup | container 'Eos, Transactions American Geophysical Union' is a periodical, volume 89(49) |
| nassichuk1987forty | Forty Years of Northern Non-Renewable Natural Resource Development | container 'Arctic' is a periodical, volume 40 |
| nassichuk2000robert | Robert L. Christie (1926-1999) | container 'Arctic' is a periodical, volume 53(1) |
| nature1935explorations | Explorations in Ellesmere Island | container 'Nature' is a periodical, volume 136 (3448) |
| neatby1983frobisher | Martin Frobisher (ca. 1540-1594) | container 'Arctic' is a periodical, volume 36 |
| nutt1963note | A Note on Ice Island WH-5 | container 'Arctic' is a periodical, volume 16(3) |
| nutt1966drift | The Drift of Ice Island WH-5 | container 'Arctic' is a periodical, volume 19(3) |
| oliver1963entomological | Entomological Studies in the Lake Hazen Area, Ellesmere Island | container 'Arctic' is a periodical, volume 16(3) |
| osczevski1994disappearance | The disappearance of Hans Krüger (correspondence) | container 'Polar Record' is a periodical, volume 30 (173) |
| park1993dorset | The Dorset-Thule Succession in Arctic North America: Assessing Claims  | container 'American Antiquity' is a periodical, volume 58(2) |
| park2007hans | A Hans Krüger Arctic Expedition Cache on Axel Heiberg Island, Nunavut | container from the URL: 'Arctic' |
| park2008contact | Contact between the Norse Vikings and the Dorset Culture in Arctic Can | container 'Antiquity' is a periodical, volume 82 |
| pilot1984kyak | Lazaroosie Kyak (1919-1976) | container 'Arctic' is a periodical, volume 37(1) |
| polarrecord1934oxford | Oxford University Ellesmere Land Expedition, 1934-5 | container 'Polar Record' is a periodical, volume 1 (8) |
| polarrecord1935oxfordsummer | Oxford University Ellesmere Land Expedition, 1934-35 (July 1935 note) | container 'Polar Record' is a periodical, volume 2 (10) |
| polarrecord1935oxfordwinter | Oxford University Ellesmere Land Expedition, 1934-35 (January 1935 not | container 'Polar Record' is a periodical, volume 2 (9) |
| polarrecord1936oxford | Oxford University Ellesmere Land Expedition, 1934-35 | container 'Polar Record' is a periodical, volume 2 (11) |
| polarrecord1937bentham | Mr Bentham's Investigations in Southern Ellesmere Land, 1936-38 | container 'Polar Record' is a periodical, volume 2 (13) |
| polarrecord1938british | British Arctic Expedition, 1937-38 [note] | container 'Polar Record' is a periodical, volume 2 (15) |
| polarrecord1939british | British Arctic Expedition, 1937-38 [interim report] | container 'Polar Record' is a periodical, volume 2 (16) |
| polarrecord1939completed | British Arctic Expedition, 1937-38 [completed expeditions] | container 'Polar Record' is a periodical, volume 3 (17) |
| polarrecord1963wardhunt | The Ward Hunt Ice Shelf, Northern Ellesmere Island, 1962-63 | container 'Polar Record' is a periodical |
| polarrecord1967plaisted | R. S. Plaisted Expedition to the North Pole, 1967 | container 'Polar Record' is a periodical, volume 14(88) |
| polarrecord1968plaisted | R. L. Plaisted Expedition to the North Pole, 1968 | container 'Polar Record' is a periodical, volume 14(91) |
| polarrecord1969btae | British Trans-Arctic Expedition, 1966-69: activities in 1968-69 | container 'Polar Record' is a periodical, volume 14(92) |
| polarrecord1969simpson | H. Simpson's Expedition to the North Pole, 1969 | container 'Polar Record' is a periodical, volume 14(93) |
| poulsen1946notes | Notes on Cambro-Ordovician fossils collected by the Oxford University  | container 'Quarterly Journal of the Geological Society of London' is a periodical, volume 102 |
| powell1959glaciological | Glaciological and Botanical Studies in Northern Ellesmere Island, 1959 | container 'Arctic' is a periodical, volume 12(4) |
| priestley1939tracks | Tracks in the Snow [review] | container 'The Geographical Journal' is a periodical, volume 95 (3) |
| raghavan2014genetic | The Genetic Prehistory of the New World Arctic | container 'Science' is a periodical, volume 345(6200) |
| ross1976neptune | Canadian Sovereignty in the Arctic: The Neptune Expedition of 1903-04 | container 'Arctic' is a periodical, volume 29(2) |
| ruizpuerta2024greenland | Greenland Norse Walrus Exploitation Deep into the Arctic | container 'Science Advances' is a periodical, volume 10 |
| sabo1978possible | A Possible Thule Carving of a Viking from Baffin Island, N.W.T. | container "Canadian Journal of Archaeology / Journal Canadien d'Archeologie" is a periodical, volume 2 |
| sabo1980aspects | Aspects of Thule Culture Adaptations in Southern Baffin Island | container 'Arctic' is a periodical, volume 33 |
| savile1964general | General Ecology and Vascular Plants of the Hazen Camp Area | container 'Arctic' is a periodical, volume 17(4) |
| schledermann1977bache | An Archaeological Survey of Bache Peninsula, Ellesmere Island | container 'Arctic' is a periodical, volume 30(4) |
| schledermann1978preliminary | Preliminary Results of Archaeological Investigations in the Bache Peni | container 'Arctic' is a periodical, volume 31 |
| schledermann1980notes | Notes on Norse Finds from the East Coast of Ellesmere Island, N.W.T. | container 'Arctic' is a periodical, volume 33 |
| schledermann1980western | Western Elements in the Early Thule Culture of the Eastern High Arctic | container 'Arctic' is a periodical, volume 33 |
| schledermann2003muskox | The Muskox Patrol: High Arctic Sovereignty Revisited | container 'Arctic' is a periodical, volume 56(1) |
| serson1964stratified | Stratified Water of a Glacial Lake in Northern Ellesmere Island | container 'Arctic' is a periodical, volume 17(2) |
| shackleton1936scoresby | The Scoresby Bay Journey | container 'The Geographical Journal' is a periodical, volume 87 (5) |
| star2018ancient | Ancient DNA reveals the chronology of walrus ivory trade from Norse Gr | container 'Proceedings of the Royal Society B: Biological Sciences' is a periodical, volume 285 |
| stein2011arctic | An Arctic Execution: Private Charles B. Henry of the United States Lad | container 'Arctic' is a periodical, volume 64 |
| stenton2010retracing | Retracing the route of Hans K. E. Krüger's 1930 German Arctic expediti | container 'Polar Record' is a periodical, volume 46 (239) |
| sutherland2015evidence | Evidence of Early Metalworking in Arctic Canada | container 'Geoarchaeology' is a periodical, volume 30 |
| swithinbank1970second | Second Arctic Voyage of SS Manhattan, 1970 | container from --publisher: 'Polar Record' |
| taylor1981first | First International Polar Year, 1882-83 | container 'Arctic' is a periodical, volume 34 |
| thomas1950photographic | Photographic Operations of the Royal Canadian Air Force | container 'Arctic' is a periodical, volume 3(3) |
| thorsteinsson1957geological | Geological Investigations in Ellesmere and Axel Heiberg Islands, 1956 | container 'Arctic' is a periodical, volume 10(1) |
| vansteenburgh1966scientific | Scientific Research in the Arctic: Canada | container 'Arctic' is a periodical, volume 19(1) |
| wright1940southeast | South-East Ellesmere Island | container 'The Geographical Journal' is a periodical, volume 95 (4) |
| yaremko2025community | Community Perspectives from Pond Inlet, Nunavut, on Shipping Risk and  | container from --publisher: 'Arctic' |

### incollection (26)

| bibkey | title | evidence |
|---|---|---|
| birketsmith1929caribou | The Caribou Eskimos: Material and Social Life and their Cultural Posit | container 'Report of the Fifth Thule Expedition 1921-24, Vol. V' is a book or a report series |
| burant1985mecham | MECHAM, GEORGE FREDERICK | a life in the Dictionary of Canadian Biography |
| cooke1966frobisher | FROBISHER, Sir MARTIN | container 'Dictionary of Canadian Biography, vol. 1' is a book or a report series |
| cooke1972griffin | GRIFFIN, JANE (Franklin, Lady Franklin) | a life in the Dictionary of Canadian Biography |
| grant2002arctic | Arctic Justice: On Trial for Murder, Pond Inlet, 1923 | container "McGill-Queen's Native and Northern Series 33" is a book or a report series |
| gsc2023polar | 79. Polar Continental Shelf Project (1958) | container 'The History of the Geological Survey of Canada in 175 Objects' is a book or a report series |
| holland1976austin | AUSTIN, Sir HORATIO THOMAS | a life in the Dictionary of Canadian Biography |
| holland1985bellot | BELLOT, JOSEPH-RENE | a life in the Dictionary of Canadian Biography |
| holland1990penny | PENNY, WILLIAM | a life in the Dictionary of Canadian Biography |
| lok1582chart | Illustri viro, domino Philippo Sidnaeo Michael Lok civis Londinensis h | container 'Richard Hakluyt, Divers Voyages Touching the Discouerie of America' is a book or a report series |
| maceachern2025bernier | BERNIER, JOSEPH-ELZEAR | container 'Dictionary of Canadian Biography, vol. 16' is a book or a report series |
| mathiassen1927archaeology | Archaeology of the Central Eskimos. Report of the Fifth Thule Expediti | container 'Report of the Fifth Thule Expedition 1921-24, Vol. IV, No. 2' is a book or a report series |
| mccullough1989ruin | The Ruin Islanders: Thule Culture Pioneers in the Eastern High Arctic | container 'Mercury Series, Archaeological Survey of Canada Paper 141' is a book or a report series |
| mcghee1979palaeoeskimo | The Palaeoeskimo Occupations at Port Refuge, High Arctic Canada | container 'National Museum of Man Mercury Series, Archaeological Survey of Canada Paper No. 92' is a book or a report series |
| mcghee1984thule | The Thule Village at Brooman Point, High Arctic Canada | container 'National Museum of Man Mercury Series, Archaeological Survey of Canada Paper No. 125' is a book or a report series |
| neatby1966hudson | Hudson, Henry | container 'Dictionary of Canadian Biography, vol. 1' is a book or a report series |
| neatby1972kellett | KELLETT, Sir HENRY | a life in the Dictionary of Canadian Biography |
| rasmussen1929intellectual | Intellectual Culture of the Iglulik Eskimos | container 'Report of the Fifth Thule Expedition 1921-24, Vol. VII, No. 1' is a book or a report series |
| rasmussen1931netsilik | The Netsilik Eskimos: Social Life and Spiritual Culture | container 'Report of the Fifth Thule Expedition 1921-24, Vol. VIII, nos. 1-2' is a book or a report series |
| rowley1987tattannoeuck | TATTANNOEUCK (Augustus) | a life in the Dictionary of Canadian Biography |
| schledermann2003inuit | Inuit-Norse Contact in the Smith Sound Region | container 'Contact, Continuity, and Collapse: The Norse Colonization of the North Atlantic' is a book or a report series |
| shaw1982kennedy | KENNEDY, WILLIAM | a life in the Dictionary of Canadian Biography |
| smith1985ooligbuck | OOLIGBUCK (Oolibuck, Ouligbuck, Oullibuck, Oulybuck, Ullebuck) | a life in the Dictionary of Canadian Biography |
| stuartstubbs1972belcher | BELCHER, Sir EDWARD | a life in the Dictionary of Canadian Biography |
| taylor1955geographical | Geographical Discovery and Exploration in the Queen Elizabeth Islands | container 'Geographical Branch Memoir No. 3' is a book or a report series |
| white1910placenames | Place-names — Northern Canada, in the Ninth Report of the Geographic B | container 'Ninth Report of the Geographic Board of Canada for the year ending 30 June 1910 (Sessional Paper No. 21a, 1911)' is a book or a report series |

### report (56)

| bibkey | title | evidence |
|---|---|---|
| admiralty1855further | Further Papers Relative to the Recent Arctic Expeditions in Search of  | published by 'Eyre and Spottiswoode, for H.M. Stationery Of' |
| bernier1909report | Report on the Dominion Government Expedition to the Arctic Islands and | published by 'Government Printing Bureau' |
| bernier1910report | Report on the Dominion of Canada Government Expedition to the Arctic I | published by 'Government Printing Bureau' |
| canada1929hudson | Report of the Hudson Strait Expedition, 1927-28 | published by "F. A. Acland, King's Printer, Ottawa" |
| canada1939polar | Canadian Polar Year Expeditions, 1932-33: Terrestrial Magnetism, Earth | published by "J.O. Patenaude, King's Printer" |
| davis1876narrative | Narrative of the North Polar Expedition, U.S. Ship Polaris, Captain Ch | published by 'Government Printing Office' |
| dunbar1971winter | Winter ice reconnaissance in Nares Strait, 1970-71 | published by 'Defence Research Establishment Ottawa, Defenc' |
| dunbar1972winter | Winter ice reconnaissance in Nares Strait, 1971-72 | published by 'Defence Research Establishment Ottawa, Defenc' |
| greatbritain1852arctic | Arctic Expeditions: Report of the Committee Appointed by the Lords Com | published by 'Eyre and Spottiswoode' |
| greatbritain1855further | Further Papers relative to the Recent Arctic Expeditions in Search of  | published by 'Printed by G. E. Eyre and W. Spottiswoode for' |
| greely1888report | Report on the Proceedings of the United States Expedition to Lady Fran | published by 'Government Printing Office' |
| hattersleysmith1959research | Research in the Lake Hazen region of northern Ellesmere Island in the  | published by 'Defence Research Board' |
| hattersleysmith1969glacier | Operation Tanquary: Glacier depths in northern Ellesmere Island - airb | published by 'Defence Research Establishment Ottawa, Defenc' |
| hattersleysmith1971climate | Climate change and related problems in northern Ellesmere Island | published by 'Defence Research Establishment Ottawa, Defenc' |
| hattersleysmith1973ice | Ice shelf and fiord ice problems in Disraeli Fiord, northern Ellesmere | published by 'Defence Research Establishment Ottawa, Defenc' |
| jenness1922life | The Life of the Copper Eskimos. Report of the Canadian Arctic Expediti | published by "F. A. Acland, King's Printer" |
| keys1974radar | Radar measurement of ice drift in Robeson Channel, 1972 | published by 'Defence Research Establishment Ottawa, Defenc' |
| larsen1958northwest | The North-West Passage, 1940-1942 and 1944: The Famous Voyages of the  | published by "Edmond Cloutier, Queen's Printer and Controll" |
| lotz1958operation | "Operation Hazen" Phase III, May-August 1958: preliminary report on th | published by 'Defence Research Board / McGill University' |
| mcclean1928report | Report of the Hudson Strait Expedition to December 31, 1927 | published by "King's Printer, Ottawa" |
| nourse1879narrative | Narrative of the Second Arctic Expedition made by Charles F. Hall: His | published by 'Government Printing Office' |
| proteus1884proceedings | Proceedings of the 'Proteus' Court of Inquiry on the Greely Relief Exp | published by 'Government Printing Office' |
| qtc2013arcticbay | Qikiqtani Truth Commission Community Histories 1950-1975: Arctic Bay | 'Qikiqtani Inuit Association / Inhabit Me' publishes it and the title reads as a report |
| qtc2013clyderiver | Qikiqtani Truth Commission Community Histories 1950-1975: Clyde River | 'Qikiqtani Inuit Association / Inhabit Me' publishes it and the title reads as a report |
| qtc2013final | Qikiqtani Truth Commission Final Report: Achieving Saimaqatigiingniq | 'Qikiqtani Inuit Association / Inhabit Me' publishes it and the title reads as a report |
| qtc2013grisefiord | Qikiqtani Truth Commission Community Histories 1950-1975: Grise Fiord | 'Qikiqtani Inuit Association / Inhabit Me' publishes it and the title reads as a report |
| qtc2013health | Aaniajurliriniq: Health Care in Qikiqtaaluk (Qikiqtani Truth Commissio | 'Qikiqtani Inuit Association / Inhabit Me' publishes it and the title reads as a report |
| qtc2013keyfindings | Qikiqtani Truth Commission: Key Findings | 'Qikiqtani Inuit Association' publishes it and the title reads as a report |
| qtc2013kimmirut | Qikiqtani Truth Commission Community Histories 1950-1975: Kimmirut | 'Qikiqtani Inuit Association / Inhabit Me' publishes it and the title reads as a report |
| qtc2013kinngait | Qikiqtani Truth Commission Community Histories 1950-1975: Kinngait | 'Qikiqtani Inuit Association / Inhabit Me' publishes it and the title reads as a report |
| qtc2013nuutauniq | Nuutauniq: Moves in Inuit Life (Qikiqtani Truth Commission Thematic Re | 'Qikiqtani Inuit Association, Iqaluit' publishes it and the title reads as a report |
| qtc2013pangnirtung | Qikiqtani Truth Commission Community Histories 1950-1975: Pangnirtung | 'Qikiqtani Inuit Association / Inhabit Me' publishes it and the title reads as a report |
| qtc2013pondinlet | Qikiqtani Truth Commission Community Histories 1950-1975: Pond Inlet | 'Qikiqtani Inuit Association / Inhabit Me' publishes it and the title reads as a report |
| qtc2013qimmiit | Qimmiliriniq: Inuit Sled Dogs in Qikiqtaaluk (Qikiqtani Truth Commissi | 'Qikiqtani Inuit Association / Inhabit Me' publishes it and the title reads as a report |
| qtc2013rcmpreview | Analysis of the RCMP Final Report on the Inuit Sled Dog (Qikiqtani Tru | 'Qikiqtani Inuit Association / Inhabit Me' publishes it and the title reads as a report |
| qtc2013resolutebay | Qikiqtani Truth Commission Community Histories 1950-1975: Resolute Bay | 'Qikiqtani Inuit Association / Inhabit Me' publishes it and the title reads as a report |
| rcap1994high | The High Arctic Relocation: A Report on the 1953-55 Relocation | 'Canada Communication Group Publishing, O' publishes it and the title reads as a report |
| rcmp1921report | Report of the Royal Canadian Mounted Police for the Year Ended Septemb | published by "F. A. Acland, Printer to the King's Most Exce" |
| rcmp1922report | Report of the Royal Canadian Mounted Police for the Year Ended Septemb | published by "F. A. Acland, Printer to the King's Most Exce" |
| rcmp1923report | Report of the Royal Canadian Mounted Police for the Year Ended Septemb | published by "F. A. Acland, Printer to the King's Most Exce" |
| rcmp1924report | Report of the Royal Canadian Mounted Police for the Year Ended Septemb | published by "F. A. Acland, Printer to the King's Most Exce" |
| rcmp1925report | Report of the Royal Canadian Mounted Police for the Year Ended Septemb | published by "F. A. Acland, Printer to the King's Most Exce" |
| rcmp1927report | Report of the Royal Canadian Mounted Police for the Year Ended Septemb | published by "King's Printer" |
| rcmp1928report | Report of the Royal Canadian Mounted Police for the Year Ended Septemb | published by "King's Printer" |
| rcmp1929report | Report of the Royal Canadian Mounted Police for the Year Ended Septemb | published by "King's Printer" |
| rcmp1931report | Report of the Royal Canadian Mounted Police for the Year Ended Septemb | published by "King's Printer" |
| rcmp1932report | Report of the Royal Canadian Mounted Police for the Year Ended Septemb | published by "King's Printer" |
| rcmp1933report | Report of the Royal Canadian Mounted Police for the Year Ended Septemb | published by "King's Printer" |
| rcmp1934report | Report of the Royal Canadian Mounted Police for the Eighteen Months En | published by "J. O. Patenaude, Printer to the King's Most E" |
| rcmp1935report | Report of the Royal Canadian Mounted Police for the Year Ended March 3 | published by "J. O. Patenaude, Printer to the King's Most E" |
| rcn1954crowsnest | The Northwest Passage [HMCS Labrador], The Crowsnest, vol. 6 no. 12 | published by "The Crowsnest: The Royal Canadian Navy's Maga" |
| serson1971robeson | Robeson Channel Experiment: main and radar camp - plans and operations | published by 'Defence Research Establishment Ottawa, Defenc' |
| serson1973inventory | Inventory of portable buildings | published by 'Defence Research Establishment Ottawa, Defenc' |
| serson1974sverdrup | Sverdrup Channel | published by 'Defence Research Establishment Ottawa, Defenc' |
| tsb1997hanseatic | Marine Investigation Report M96H0016: Grounding, Passenger Vessel 'Han | 'Transportation Safety Board of Canada' publishes it and the title reads as a report |
| usher1971fur | Fur Trade Posts of the Northwest Territories, 1870-1970 | published by 'Northern Science Research Group, Department o' |

### book (94)

| bibkey | title | evidence |
|---|---|---|
| amundsen1908northwest | "The North West Passage": Being the Record of a Voyage of Exploration  | a standalone work, 'Archibald Constable and Company' 1908 |
| anon1821north | The North Georgia Gazette, and Winter Chronicle | a standalone work, 'John Murray' 1821 |
| armstrong1857personal | A Personal Narrative of the Discovery of the North-West Passage; with  | a standalone work, 'Hurst and Blackett' 1857 |
| asher1860henry | Henry Hudson the Navigator: The Original Documents in which his Career | a standalone work, 'Hakluyt Society' 1860 |
| barrett2003contact | Contact, Continuity, and Collapse: The Norse Colonization of the North | a standalone work, 'Brepols' 2003 |
| bartlett1916last | The Last Voyage of the Karluk, Flagship of Vilhjalmur Stefansson's Can | a standalone work, 'Small, Maynard and Company' 1916 |
| belcher1855last | The Last of the Arctic Voyages; being a Narrative of the Expedition in | a standalone work, 'Lovell Reeve' 1855 |
| bellot1855memoirs | Memoirs of Lieutenant Joseph Rene Bellot, with his Journal of a Voyage | a standalone work, 'Hurst and Blackett' 1855 |
| best1578true | A True Discourse of the Late Voyages of Discouerie, for the Finding of | a standalone work, 'Henry Bynnyman' 1578 |
| blake1874arctic | Arctic Experiences: Containing Capt. George E. Tyson's Wonderful Drift | a standalone work, 'Harper & Brothers' 1874 |
| brainard1929outpost | The Outpost of the Lost: An Arctic Adventure | a standalone work, 'The Bobbs-Merrill Company' 1929 |
| christy1894voyages | The Voyages of Captain Luke Foxe of Hull, and Captain Thomas James of  | a standalone work, 'Hakluyt Society' 1894 |
| coats1852geography | The Geography of Hudson's Bay: being the Remarks of Captain W. Coats,  | a standalone work, 'Hakluyt Society' 1852 |
| collinson1867three | The Three Voyages of Martin Frobisher, in Search of a Passage to Catha | a standalone work, 'Hakluyt Society' 1867 |
| collinson1889journal | Journal of H.M.S. Enterprise, on the Expedition in Search of Sir John  | a standalone work, 'Sampson Low, Marston, Searle, and Riving' 1889 |
| cook1911attainment | My Attainment of the Pole: Being the Record of the Expedition that Fir | a standalone work, 'Mitchell Kennerley' 1911 |
| cresswell1854series | A Series of Eight Sketches in Colour (together with a Chart of the Rou | a standalone work, 'Day and Son' 1854 |
| dick2001muskox | Muskox Land: Ellesmere Island in the Age of Contact | a standalone work, 'University of Calgary Press' 2001 |
| fisher1821journal | A Journal of a Voyage of Discovery to the Arctic Regions, Performed in | a standalone work, 'Longman, Hurst, Rees, Orme, and Brown' 1821 |
| foxe1635northwest | North-West Fox, or, Fox from the North-west Passage | a standalone work, 'B. Alsop and Tho. Fawcet' 1635 |
| gathornehardy1921norse | The Norse Discoverers of America: The Wineland Sagas Translated and Di | a standalone work, 'The Clarendon Press' 1921 |
| gerritsz1612tabula | Tabula nautica, qua repraesentantur orae maritimae, meatus, ac freta,  | a standalone work, 'Hessel Gerritsz' 1612 |
| gilder1881schwatkas | Schwatka's Search: Sledging in the Arctic in Quest of the Franklin Rec | a standalone work, "Charles Scribner's Sons" 1881 |
| gosch1897danish | Danish Arctic Expeditions, 1605 to 1620. Book II: The Expedition of Ca | a standalone work, 'Hakluyt Society' 1897 |
| greely1886three | Three Years of Arctic Service: An Account of the Lady Franklin Bay Exp | a standalone work, "Charles Scribner's Sons" 1886 |
| guttridge2000ghosts | Ghosts of Cape Sabine: The Harrowing True Story of the Greely Expediti | a standalone work, "G.P. Putnam's Sons" 2000 |
| haigthomas1939tracks | Tracks in the Snow | a standalone work, 'Oxford University Press' 1939 |
| hall1864life | Life with the Esquimaux: The Narrative of Captain Charles Francis Hall | a standalone work, 'Sampson Low, Son, and Marston' 1864 |
| hamersly1902military | A Military Album, Containing Over One Thousand Portraits of Commission | a standalone work, 'L.R. Hamersly Co.' 1902 |
| harper2017minik | Minik, the New York Eskimo: An Arctic Explorer, a Museum, and the Betr | a standalone work, 'Steerforth Press' 2017 |
| hayes1867open | The Open Polar Sea: A Narrative of a Voyage of Discovery towards the N | a standalone work, 'Hurd and Houghton' 1867 |
| heidt2022joint | The Joint Arctic Weather Stations: Science and Sovereignty in the High | a standalone work, 'University of Calgary Press' 2022 |
| hendrik1878memoirs | Memoirs of Hans Hendrik, the Arctic Traveller, Serving under Kane, Hay | a standalone work, 'Trubner & Co.' 1878 |
| henson1912negro | A Negro Explorer at the North Pole | a standalone work, 'Frederick A. Stokes Company' 1912 |
| herbert1969across | Across the Top of the World: The British Trans-Arctic Expedition | a standalone work, 'Longmans' 1969 |
| huish1835last | The Last Voyage of Capt. Sir John Ross, R.N. Knt. to the Arctic Region | a standalone work, 'John Saunders' 1835 |
| james1633strange | The Strange and Dangerous Voyage of Captaine Thomas Iames, in his inte | a standalone work, 'John Legatt for John Partridge' 1633 |
| kane1854grinnell | The U.S. Grinnell Expedition in Search of Sir John Franklin: A Persona | a standalone work, 'Harper and Brothers' 1854 |
| kane1856arctic | Arctic Explorations: The Second Grinnell Expedition in Search of Sir J | a standalone work, 'Childs & Peterson' 1856 |
| kennedy1853short | A Short Narrative of the Second Voyage of the Prince Albert, in Search | a standalone work, 'W. H. Dalton' 1853 |
| lackenbauer2025northwest | Northwest Passages: Navigating the Canadian Arctic from Gjoa to Harry  | a standalone work, 'Centre for Military, Security and Strate' 2025 |
| larsen1967big | The Big Ship: An Autobiography | a standalone work, 'McClelland and Stewart, Toronto' 1967 |
| lee1992death | Death and Deliverance: The True Story of the Boxtop 22 Crash | a standalone work, 'Macfarlane Walter and Ross' 1992 |
| lewis1904life | The Life and Work of the Rev. E. J. Peck among the Eskimos | a standalone work, 'Hodder and Stoughton' 1904 |
| loc1881lfbphotographs | Lady Franklin Bay Expedition photographs, 1881-1883 | a standalone work, 'Library of Congress Prints and Photograp' 1881 |
| lowther1962account | An account of an archaeological site on Cape Sparbo, Devon Island | a standalone work, 'National Museum of Canada' 1962 |
| lyon1824private | The Private Journal of Captain G. F. Lyon, of H.M.S. Hecla, during the | a standalone work, 'John Murray' 1824 |
| lyon1825brief | A Brief Narrative of an Unsuccessful Attempt to Reach Repulse Bay, thr | a standalone work, 'John Murray' 1825 |
| macinnis1982breadalbane | The Breadalbane Adventure | a standalone work, 'Optimum Publishing International' 1982 |
| macmillan1918four | Four Years in the White North | a standalone work, 'Harper & Brothers' 1918 |
| markham1875arctic | The Arctic Navy List; or, A Century of Arctic and Antarctic Officers,  | a standalone work, 'Griffin and Co.' 1875 |
| markham1880davis | The Voyages and Works of John Davis the Navigator | a standalone work, 'Hakluyt Society' 1880 |
| markham1880great | The Great Frozen Sea: A Personal Narrative of the Voyage of the 'Alert | a standalone work, 'Kegan Paul, Trench' 1880 |
| markham1881baffin | The Voyages of William Baffin, 1612-1622 | a standalone work, 'Hakluyt Society' 1881 |
| maryrousseliere1991qitdlarssuaq | Qitdlarssuaq: The Story of a Polar Migration | a standalone work, 'Wuerz Publishing' 1991 |
| mcclintock1859voyage | The Voyage of the 'Fox' in the Arctic Seas: A Narrative of the Discove | a standalone work, 'John Murray' 1859 |
| mcdougall1857eventful | The Eventful Voyage of H.M. Discovery Ship 'Resolute' to the Arctic Re | a standalone work, 'Longman, Brown, Green, Longmans, and Rob' 1857 |
| mckinlay1976karluk | Karluk: The Great Untold Story of Arctic Exploration | a standalone work, 'Weidenfeld and Nicolson' 1976 |
| moss1878shores | Shores of the Polar Sea: A Narrative of the Arctic Expedition of 1875- | a standalone work, 'Marcus Ward and Co.' 1878 |
| munk1624navigatio | Navigatio Septentrionalis. Det er: Relation eller Bescriffuelse om Sei | a standalone work, 'Henrich Waldkirch' 1624 |
| nansen1911northern | In Northern Mists: Arctic Exploration in Early Times, Volume 1 | a standalone work, 'William Heinemann' 1911 |
| nares1878narrative | Narrative of a Voyage to the Polar Sea during 1875-76 in H.M. Ships 'A | a standalone work, 'Sampson Low, Marston, Searle, and Riving' 1878 |
| niven2000ice | The Ice Master: The Doomed 1913 Voyage of the Karluk | a standalone work, 'Hyperion' 2000 |
| osborn1852stray | Stray Leaves from an Arctic Journal; or, Eighteen Months in the Polar  | a standalone work, 'Longman, Brown, Green, and Longmans' 1852 |
| osborn1856discovery | The Discovery of the North-West Passage by H.M.S. 'Investigator', Capt | a standalone work, 'Longman, Brown, Green, Longmans, and Rob' 1856 |
| parry1821journal | Journal of a Voyage for the Discovery of a North-West Passage from the | a standalone work, 'John Murray' 1821 |
| parry1824journal | Journal of a Second Voyage for the Discovery of a North-West Passage f | a standalone work, 'John Murray' 1824 |
| parry1826journal | Journal of a Third Voyage for the Discovery of a North-West Passage fr | a standalone work, 'John Murray' 1826 |
| peary1898northward | Northward over the "Great Ice": A Narrative of Life and Work along the | a standalone work, 'Frederick A. Stokes Company' 1898 |
| peary1907nearest | Nearest the Pole: A Narrative of the Polar Expedition of the Peary Arc | a standalone work, 'Doubleday, Page & Company' 1907 |
| peary1910north | The North Pole: Its Discovery in 1909 under the Auspices of the Peary  | a standalone work, 'Frederick A. Stokes Company' 1910 |
| petermann1876skizze | Skizze der Entdeckungen der englischen Polar-Expedition unter Nares, 1 | a standalone work, 'Justus Perthes' 1876 |
| purchas1625hakluytus | Hakluytus Posthumus, or Purchas his Pilgrimes | a standalone work, 'William Stansby for Henrie Fetherstone' 1625 |
| rae1854melancholy | The Melancholy Fate of Sir John Franklin and his Party, as Disclosed i | a standalone work, 'John Betts' 1854 |
| rasmussen1908people | The People of the Polar North: A Record | a standalone work, 'Kegan Paul, Trench, Trubner & Co.' 1908 |
| rasmussen1921greenland | Greenland by the Polar Sea: The Story of the Thule Expedition from Mel | a standalone work, 'William Heinemann' 1921 |
| rasmussen1927across | Across Arctic America: Narrative of the Fifth Thule Expedition | a standalone work, "G. P. Putnam's Sons" 1927 |
| reeves1890finding | The Finding of Wineland the Good: The History of the Icelandic Discove | a standalone work, 'Henry Frowde, Oxford University Press' 1890 |
| richardson1851arctic | Arctic Searching Expedition: A Journal of a Boat-Voyage through Rupert | a standalone work, 'Longman, Brown, Green, and Longmans' 1851 |
| rink1875tales | Tales and Traditions of the Eskimo, with a Sketch of Their Habits, Rel | a standalone work, 'William Blackwood and Sons' 1875 |
| ross1819voyage | A Voyage of Discovery, Made under the Orders of the Admiralty, in His  | a standalone work, 'John Murray' 1819 |
| ross1835appendix | Appendix to the Narrative of a Second Voyage in Search of a North-West | a standalone work, 'A. W. Webster' 1835 |
| ross1835narrative | Narrative of a Second Voyage in Search of a North-West Passage, and of | a standalone work, 'A. W. Webster' 1835 |
| schley1885rescue | The Rescue of Greely | a standalone work, "Charles Scribner's Sons" 1885 |
| sephton1880eirik | Eirik the Red's Saga | a standalone work, 'David Marples' 1880 |
| shackleton1937arctic | Arctic Journeys: The Story of the Oxford University Ellesmere Land Exp | a standalone work, 'Hodder and Stoughton' 1937 |
| smyth1853breadalbane | Her Majesty's Ships Phoenix and Breadalbane Landing Stores at Cape Ril | a standalone work, 'The Illustrated London News, 22 October ' 1853 |
| snow1851voyage | Voyage of the Prince Albert in Search of Sir John Franklin: A Narrativ | a standalone work, 'Longman, Brown, Green, and Longmans' 1851 |
| stefansson1921friendly | The Friendly Arctic: The Story of Five Years in Polar Regions | a standalone work, 'Macmillan' 1921 |
| steger1987north | North to the Pole | a standalone work, 'Times Books / Macmillan' 1987 |
| sutherland1852journal | Journal of a Voyage in Baffin's Bay and Barrow Straits, in the Years 1 | a standalone work, 'Longman, Brown, Green, and Longmans' 1852 |
| sverdrup1904newland | New Land: Four Years in the Arctic Regions | a standalone work, 'Longmans, Green and Co.' 1904 |
| swan1990icewalk | Icewalk | a standalone work, 'Jonathan Cape' 1990 |
| weber1996polar | Polar Attack: From Canada to the North Pole, and Back | a standalone work, 'McGraw-Hill Ryerson' 1996 |

### online (63)

| bibkey | title | evidence |
|---|---|---|
| amundsenscience2026ccgs | The CCGS Amundsen: A Success Story in Arctic Oceanography | a web page at amundsenscience.com/about-us/the-ccgs-amundse |
| arktiskinstitut2026billeder | Arktiske Billeder: the photographic archive of the Danish Arctic Insti | a web page at www.arktiskebilleder.dk/ |
| asn2024database | ASN Aviation Safety Database: accident records for the Canadian easter | a web page at asn.flightsafety.org/ |
| canada1970awppa | Arctic Waters Pollution Prevention Act (R.S.C., 1985, c. A-12) | a web page at laws-lois.justice.gc.ca/eng/acts/A-12/ |
| canada1985baselines | Territorial Sea Geographical Coordinates (Area 7) Order, SOR/85-872 | a web page at laws-lois.justice.gc.ca/eng/regulations/SOR-8 |
| canada1988arctic | Agreement Between the Government of Canada and the Government of the U | a web page at www.treaty-accord.gc.ca/text-texte.aspx?id=10 |
| canada1993nunavutact | Nunavut Act (S.C. 1993, c. 28) | a web page at laws-lois.justice.gc.ca/eng/acts/N-28.6/ |
| canada2001nunavutsites | Nunavut Archaeological and Palaeontological Sites Regulations (SOR/200 | a web page at laws-lois.justice.gc.ca/eng/regulations/SOR-2 |
| canada2010apology | Apology for the Inuit High Arctic relocation: speaking notes for the H | a web page at www.rcaanc-cirnac.gc.ca/eng/1100100016115/153 |
| canada2015alert | Governor General and Commander-in-Chief Visits Canadian Forces Station | a web page at www.canada.ca/en/news/archive/2015/01/canadia |
| canada2019tbapology | Statement of Apology on Behalf of the Government of Canada to Inuit fo | a web page at www.pm.gc.ca/en/news/speeches/2019/03/08/stat |
| cbc2015naujaat | Naujaat, Nunavut, residents celebrate official renaming | a news site: CBC News |
| cbc2020names | Hello Sanirajak and Kinngait! 2 Nunavut communities take Inuktut names | a news site: CBC News |
| ccg2026amundsen | CCG Fleet: Vessel Details - CCGS Amundsen | a web page at inter-j02.dfo-mpo.gc.ca/fdat/vessels/vessel-d |
| deabreu2020north | Top Expeditions 1970-2020, #2: North Pole Round Trip | a news site: container 'Explorersweb', https://explorersweb.com/top-expeditions |
| eccc2017ayles | Ayles Ice Shelf (Educational ice resources) | a web page at www.canada.ca/en/environment-climate-change/s |
| echr2006hingitaq | Hingitaq 53 and Others v. Denmark (application no. 18584/04): decision | a web page at hudoc.echr.coe.int/eng?i=001-72219 |
| explorersweb2021uemura | Legends Series: Naomi Uemura | a news site: container 'Explorersweb', https://explorersweb.com/legends-series- |
| frammuseum2026gjoa | Gjoa (vessel) | a web page at frammuseum.no/polar-history/vessels/the-gjoa/ |
| goose2015shoran | SHORAN Operations 1949-1957, 408 (P) Squadron | a web page at www.forfreedom.ca/?page_id=725 |
| gwr1990first | First people to reach the North Pole unsupported, emergency-assisted | a news site: container 'Guinness World Records', https://www.guinnessworldrecords.com/wor |
| halliday2008mapping | Mapping In Full Flight: Air Force, Part 28 | a news site: Legion Magazine |
| harper2006crockerland | Taissumani: April 23, 1914 - Crocker Land, an Arctic mirage | a news site: Nunatsiaq News |
| harper2006murder | Taissumani: May 1, 1914 - Getting away with murder | a news site: Nunatsiaq News |
| harper2006nuqallaq | Taissumani: Sept. 3, 1925 - Nuqallaq Returns to Pond Inlet | a news site: container 'Nunatsiaq News', https://nunatsiaq.com/stories/article/Ta |
| harper2008ittukusuk | Taissumani: 2008-10-03 - Ittukusuk and Aapilak Islands | a news site: container 'Nunatsiaq News', https://nunatsiaq.com/stories/article/It |
| harper2016expulsion | Taissumani: May 25, 1953 - The Expulsion of the Inughuit | a news site: container 'Nunatsiaq News', https://nunatsiaq.com/stories/article/ta |
| harper2018death | Taissumani, Oct. 26: One hundred years ago - The death of Minik | a news site: Nunatsiaq News |
| harper2018homecoming | Taissumani, August 3: Nunamingnut uteqihut - They have come home | a news site: Nunatsiaq News |
| harper2018mockburial | Taissumani, July 20: Minik, the New York Eskimo - A Mock Burial | a news site: Nunatsiaq News |
| harper2020panipakuttuk | Joe Panipakuttuk on the St. Roch (Taissumani, two parts) | a news site: Nunatsiaq News, 7 and 21 August 2020 |
| hbca2005nascopie | S.S./R.M.S. Nascopie: Ship History Sheet | a web page at manitoba.ca/chc/archives/_assets/docs/hbca/sh |
| hbcheritage2026nascopie | R.M.S. Nascopie | a web page at www.hbcheritage.ca/things/technology/rms-nasc |
| headland2025northwest | Northwest Passage Transits to End of the 2025 Navigation Season | a web page at www.spri.cam.ac.uk/resources/infosheets/north |
| historymuseum2024maskette | Maskette (The First Face) | a web page at www.historymuseum.ca/teachers-zone/think-like |
| jamal2023mapping | Inuit Heritage Trust maps traditional names before they're lost | a news site: Nunatsiaq News |
| konick2015rockcliffe | The Rockcliffe Years - The Photo Mapping | a web page at www.forfreedom.ca/?page_id=925 |
| lac1947nascopie | R.M.S. Nascopie, Hudson's Bay Co.: sinking of the ship when it struck  | a web page at recherche-collection-search.bac-lac.gc.ca/eng |
| macinnis2015breadalbane | Breadalbane | a news site: Historica Canada, The Canadian Encyclopedia |
| manuel2020salvage | The Salvage of the HMS Resolute | a web page at www.nlchs.org/the-salvage-of-the-hms-resolute |
| mckibbon1999kugaaruk | Pelly Bay officially changes its name to Kugaaruk | a news site: Nunatsiaq News |
| moravian1971inventory | Inventory of Moravian Mission Records from Labrador | a web page at www.moravianchurcharchives.org/inventories/LM |
| noaa2005ipy | First International Polar Year 1882-83 image collection, Arctic Resear | a web page at www.arctic.noaa.gov/aro/ipy-1/ |
| nrcan2013pcsp | History of Polar Continental Shelf Program | a web page at www.nrcan.gc.ca/the-north/polar-continental-s |
| nti2010monument | Arctic Exile Monument Project | a web page at www.tunngavik.com/initiative_pages/arctic-exi |
| nunavutparks2022qaummaarviit | Qaummaarviit Territorial Park | a web page at www.gov.nu.ca/sites/default/files/publication |
| oqaasileriffik2026names | Place Names Committee (Nunat Aqqinik Aalajangiisartut) | a web page at oqaasileriffik.gl/en/place-names/ |
| osu1909cook | Frederick A. Cook Society Collection (photographs) | a web page at library.osu.edu/projects/frederick-cook/ |
| parkscanada1962stroch | St. Roch National Historic Site of Canada | a web page at www.pc.gc.ca/apps/dfhd/page_nhs_eng.aspx?id=8 |
| parkscanada1964kodlunarn | Kodlunarn Island National Historic Site of Canada | a web page at www.pc.gc.ca/apps/dfhd/page_nhs_eng.aspx?id=3 |
| parkscanada2023wrecks | Wrecks of HMS Erebus and HMS Terror National Historic Site: Finding HM | a web page at parks.canada.ca/lhn-nhs/nu/epaveswrecks |
| parkscanada2026investigator | The History of HMS Investigator and McClure's Cache, Aulavik National  | a web page at parks.canada.ca/pn-np/nt/aulavik/investigator |
| parkscanada2026quttinirpaaq | Quttinirpaaq National Park: nature, stewardship and management | a web page at parks.canada.ca/pn-np/nu/quttinirpaaq |
| queensasu2020resolution | Resolution Island (Arctic Projects) | a web page at www.queensu.ca/asu/arctic-projects/resolution |
| rcmpvets2016resolution | Plane Crash in the Baffin Islands | a web page at rcmpveteransvancouver.com/plane-crash-in-the- |
| spri1935oxford | Oxford University Ellesmere Land Expedition, 1934-35 (Picture Library  | a web page at www.spri.cam.ac.uk/picturelibrary/catalogue/o |
| vac2025boxtop | Boxtop 22 Cairn, National Inventory of Canadian Military Memorials | a web page at www.veterans.gc.ca/en/remembrance/memorials/c |
| vmm2026stroch | St. Roch National Historic Site (exhibit) | a web page at vanmaritime.com/explore/exhibits/st-roch-nati |
| wage2025kenojuak | Kenojuak Ashevak (1927-2013), Women of Impact in Canada | a web page at www.canada.ca/en/women-gender-equality/commem |
| wbec2020history | A History of the WBEC | a web page at www.westbaffin.com/history-wbec |
| wikipedia2026ccgsamundsen | CCGS Amundsen | a web page at en.wikipedia.org/wiki/CCGS_Amundsen |
| wikipedia2026gjoa | Gjoa | a web page at en.wikipedia.org/wiki/Gj%C3%B8a |
| zarate2010high | After decades of anguish, High Arctic Exiles monument unveiled | a news site: container 'Nunatsiaq News', https://nunatsiaq.com/stories/article/09 |

### dataset (5)

| bibkey | title | evidence |
|---|---|---|
| cgndb2026names | Canadian Geographical Names Database | a data service: https://geogratis.gc.ca/services/geoname/en/geonam |
| eccc2026climate | Historical Climate Data: Eureka, Nunavut (station 2401200 and successo | a data service: https://api.weather.gc.ca/collections/climate-dail |
| nrcan2016canmatrix | CanMatrix: georeferenced raster scans of the National Topographic Syst | a data service: https://ftp.maps.canada.ca/pub/nrcan_rncan/raster/ |
| nrcan2026cgndb | Canadian Geographical Names Database | a data service: https://geogratis.gc.ca/services/geoname/en/geonam |
| statgl2026population | Population in Localities January 1st (table BEXSTD) | a data service: https://bank.stat.gl/api/v1/en/Greenland/BE/BE01/B |

## Still misc (57)

| bibkey | title | publisher | why not |
|---|---|---|---|
| ags1913crocker | The Crocker Land Expedition | American Geographical Society | the journal is in --publisher or the URL, not --container: 'American Geographical Society' |
| allen1913journal | Journal of the Crocker Land Expedition 'Q', 1913-1914 |  | an object, an image or a manuscript, not a published work |
| amnh1897peary | Peary Expedition to Greenland (1897) |  | no publisher and no container |
| bain1910bernier | Joseph-Elzear Bernier (photograph) |  | an object, an image or a manuscript, not a published work |
| balch1907crocker | Crocker Land | American Geographical Society | the journal is in --publisher or the URL, not --container: 'American Geographical Society' |
| beard1845daguerreotypes | A Set of Fourteen Daguerreotypes of the Officers of the Fran |  | an object, an image or a manuscript, not a published work |
| boas1888central | The Central Eskimo | Government Printing Office, Washington ( | the journal is in --publisher or the URL, not --container: 'Government Printing Office, Washington (Sixth' |
| boyer1875alert | HM Ships Alert and Discovery leaving Portsmouth for the Arct |  | an object, an image or a manuscript, not a published work |
| cassano2012ahnighito | Ahnighito, the 34-ton Cape York meteorite, American Museum o |  | an object, an image or a manuscript, not a published work |
| cmh2020canadian | Canadian Arctic Expedition 1913-1918 photograph collection |  | no publisher and no container |
| collier1881last | The Last Voyage of Henry Hudson |  | no publisher and no container |
| commons1897minik | Minik in New York (photograph) |  | an object, an image or a manuscript, not a published work |
| commons2011grise | Commemorative Plaque, Grise Fiord (photograph, 22 October 20 |  | an object, an image or a manuscript, not a published work |
| domville1852belcher | A View across a Bay towards the Franklin Search Ships under  | Royal Museums Greenwich | 'Royal Museums Greenwich' holds it: an object or an image, not a published work |
| drummond1820parry | Sir William Edward Parry (oil on canvas) |  | an object, an image or a manuscript, not a published work |
| faulkner1834ross | Admiral Sir John Ross, 1777-1856, Arctic Explorer (oil on ca |  | an object, an image or a manuscript, not a published work |
| finden1824oomna | 'Oomna' (engraving after a drawing by Captain George Francis |  | an object, an image or a manuscript, not a published work |
| green1913journal | Journal of the Crocker Land Expedition |  | an object, an image or a manuscript, not a published work |
| hamer1875alert | HMS Alert about to winter off Floeberg Beach in the Polar Se |  | an object, an image or a manuscript, not a published work |
| hovey1915journal | Journal, 1915-1916 |  | an object, an image or a manuscript, not a published work |
| hunt1913fieldnotebook | Field note book[s], Crocker Land Expedition, 1913-1915 |  | an object, an image or a manuscript, not a published work |
| jackson1823lyon | Portrait of Captain Lyon, RN (1795-1832), half length, in a  |  | an object, an image or a manuscript, not a published work |
| kellett1853compendium | A Compendium of the Travelling Operations during the Spring  |  | no publisher and no container |
| ketel1577frobisher | Sir Martin Frobisher (oil on canvas) |  | an object, an image or a manuscript, not a published work |
| king1988commons | Photographs of Ward Hunt Island and Cape Columbia, Kanarktis |  | an object, an image or a manuscript, not a published work |
| lac1906bernier | Photographs of the Dominion Government Arctic expeditions on |  | an object, an image or a manuscript, not a published work |
| lapointe2004cdhowe | The C. D. Howe (photograph of a print in the Resolute archiv |  | an object, an image or a manuscript, not a published work |
| macmillan1913photolists | Lists of photographs of the Crocker Land Expedition |  | an object, an image or a manuscript, not a published work |
| mercator1595septentrionalium | Septentrionalium Terrarum descriptio |  | no publisher and no container |
| mmq1909bernier | Capitaine J.E. Bernier avec des personnes Inuites (photograp |  | an object, an image or a manuscript, not a published work |
| nara1909pole | Photograph of the Robert Peary Sledge Party Posing with Flag |  | an object, an image or a manuscript, not a published work |
| nasa2002wardhunt | MODIS images of the break-up of the Ward Hunt Ice Shelf, Aug |  | an object, an image or a manuscript, not a published work |
| navy1884survivors | Greely Relief Expedition, 1884: the six survivors with their | Naval History and Heritage Command | an object, an image or a manuscript, not a published work |
| nb1900fram | Photographs of the second Fram expedition, 1898-1902 |  | an object, an image or a manuscript, not a published work |
| norfolk1880feilden | Henry Wemyss Feilden (photograph) | Norfolk Museums Service | an object, an image or a manuscript, not a published work |
| park2003dorset | The Dorset Culture Longhouse at Brooman Point, Nunavut |  | the journal is in --publisher or the URL, not --container: 'https://doi.org/10.7202/010803ar' |
| pichugina2008amundsen | CCGS Amundsen in the Arctic (photograph) |  | an object, an image or a manuscript, not a published work |
| polarrecord1934kruger | Krüger Search Expeditions, 1932 | Cambridge University Press for the Scott | the journal is in --publisher or the URL, not --container: 'Cambridge University Press for the Scott Pola' |
| polarrecord1959pcsp | Canadian Polar Continental Shelf Project, 1959 (Field Work) | Cambridge University Press for the Scott | the journal is in --publisher or the URL, not --container: 'Cambridge University Press for the Scott Pola' |
| qalaherriaq1853hunt | Crayon drawing of an Inughuit hunt |  | an object, an image or a manuscript, not a published work |
| rawlings2016alert | CFS Alert, May 2016 (photograph) |  | an object, an image or a manuscript, not a published work |
| raymond2019qiniqtiryuaq | On Board Parks Canada's Archaeology Support Barge Qiniqtiryu |  | an object, an image or a manuscript, not a published work |
| science1912crocker | The Crocker Land Expedition Under the Auspices of the Americ | American Association for the Advancement | the journal is in --publisher or the URL, not --container: 'American Association for the Advancement of S' |
| science1913crocker | The Crocker Land Expedition | American Association for the Advancement | the journal is in --publisher or the URL, not --container: 'American Association for the Advancement of S' |
| science1917crocker | The Crocker Land Expedition | American Association for the Advancement | the journal is in --publisher or the URL, not --container: 'American Association for the Advancement of S' |
| storrs1970manhattan | SS Manhattan in Arctic Waters | Canadian Geographical Journal; reprinted | the journal is in --publisher or the URL, not --container: 'Canadian Geographical Journal; reprinted in L' |
| szacinski1898sverdrup | Otto Sverdrup (photograph) |  | an object, an image or a manuscript, not a published work |
| taylor1968arnapik | The Arnapik and Tyara Sites: An Archaeological Study of Dors | Society for American Archaeology (Memoir | the journal is in --publisher or the URL, not --container: 'Society for American Archaeology (Memoirs of ' |
| tekniska1910capeyork | Women of the Inuit people at Kap York, Greenland (stereo pho | Tekniska museet, Stockholm | an object, an image or a manuscript, not a published work |
| ulaval1909charts | Charts accompanying the reports of the Dominion Government A |  | an object, an image or a manuscript, not a published work |
| walk1996nunavut | Photographs of Thule archaeological sites in Nunavut, 1995-1 |  | an object, an image or a manuscript, not a published work |
| walk1997beechey | Beechey Island Graves of Seamen from the John Franklin Exped |  | an object, an image or a manuscript, not a published work |
| walk1997eureka | Eureka Weather Station, view from the airstrip (photograph) |  | an object, an image or a manuscript, not a published work |
| walk1997hazen | Photographs of Lake Hazen and Quttinirpaaq National Park, Au |  | an object, an image or a manuscript, not a published work |
| wellcome1875nares | George Strong Nares (photograph) | Wellcome Collection | an object, an image or a manuscript, not a published work |
| white1577drawings | Drawings of Kalicho, of Arnaq and Nutaaq, and of the skirmis |  | an object, an image or a manuscript, not a published work |
| worldswork1916crockerland | Members of the Crocker Land Expedition (photograph) | Doubleday, Page and Co. | an object, an image or a manuscript, not a published work |
