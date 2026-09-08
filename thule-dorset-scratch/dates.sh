#!/bin/bash
set -e
cd /data/dev/arctic-history
P=/usr/bin/python3
T="--topic thule-dorset"

# --- the long spans, each as two atomic endpoints -------------------------
$P tools/history-db.py activity $T --title "Paleo-Inuit occupation of the eastern Arctic" \
  --date=-2500 --date-end 1300 --precision century --qualifier circa \
  --place "Qikiqtaaluk" --lat 68.0 --lon -70.0 --bibkey helmer1991palaeoeskimo \
  --tags paleo-inuit,pre-dorset,dorset \
  --detail "From the first crossing out of Alaska to the disappearance of the last Dorset communities. Genome-wide data published in 2014 read the whole of it as one metapopulation, in near-isolation, for more than four thousand years."

$P tools/history-db.py activity $T --title "Independence I in the High Arctic" \
  --date=-2400 --date-end=-1900 --precision century --qualifier circa \
  --place "Port Refuge" --lat 76.3 --lon -94.7167 --bibkey mcghee1979palaeoeskimo \
  --tags paleo-inuit,independence-i \
  --detail "The first people into the High Arctic islands and northeast Greenland: tiny chipped-stone tools, mid-passage hearths, no soapstone, no dogs to speak of, camps of a few families at a time. Named from Independence Fiord in Greenland; the Canadian material comes largely from Port Refuge on Devon Island."

$P tools/history-db.py activity $T --title "Pre-Dorset in Foxe Basin and Hudson Strait" \
  --date=-2500 --date-end=-800 --precision century --qualifier circa \
  --place "Iglulik" --lat 69.377 --lon -81.799 --bibkey lynnerup2003human \
  --tags paleo-inuit,pre-dorset \
  --detail "The southern branch of the same Arctic Small Tool tradition, in the walrus and caribou country of northern Foxe Basin and the Hudson Strait coasts. The raised beaches at Iglulik and Alarnerk carry the sequence continuously into the Dorset."

$P tools/history-db.py activity $T --title "The Dorset culture" \
  --date=-800 --date-end 1300 --precision century --qualifier circa \
  --place "Iglulik" --lat 69.377 --lon -81.799 --bibkey jenness1925new \
  --tags dorset,tuniit \
  --detail "Named by Diamond Jenness in 1925 from a collection sent to Ottawa from Cape Dorset (Kinngait). Soapstone lamps and pots, ground slate and chipped quartz, harpoon heads without a drilled line hole, remarkable carving - and no bow, no drill, no dog team, no large skin boat."

$P tools/history-db.py activity $T --title "Dorset occupation at Alarnerk" \
  --date=-700 --date-end 1150 --precision century --qualifier circa \
  --place "Alarnerk" --lat 69.28 --lon -81.45 --bibkey lynnerup2003human \
  --tags dorset,alarnerk,igloolik \
  --detail "208 house remains along 2.5 km of raised limestone beaches, from the 22 m terrace down to the 8 m terrace. Radiocarbon dates, the beach chronology and Meldgaard's harpoon-head typology together give the site a span of roughly 800-600 BC to AD 1100-1200; the endpoints entered here are the mid-points of those two ranges."

$P tools/history-db.py activity $T --title "Late Dorset" \
  --date 500 --date-end 1300 --precision century --qualifier circa \
  --place "Button Point" --lat 72.8486 --lon -76.1169 --bibkey helmer1991palaeoeskimo \
  --tags dorset,late-dorset,art \
  --detail "A late expansion back into the High Arctic and northwest Greenland, with longhouses, communal structures and the greatest concentration of Dorset art: the driftwood masks and figures from Button Point on Bylot Island, the carved bears and human faces from Alarnerk and Nunguvik."

$P tools/history-db.py activity $T --title "The Thule migration east from Alaska" \
  --date 1200 --date-end 1300 --precision century --qualifier circa \
  --place "Iglulik" --lat 69.377 --lon -81.799 --bibkey friesen2008timing \
  --tags thule,migration \
  --detail "Whale-hunting people out of north Alaska, carrying the umiaq, the dog sledge, the sinew-backed bow, the drill and the float harpoon. Mathiassen argued in 1927 that it had to be a migration and not a fashion; Friesen and Arnold's radiocarbon dates in 2008 moved its start from the AD 1000 long assumed to some time after 1200."

$P tools/history-db.py activity $T --title "Thule whale-hunting settlement of the eastern Arctic" \
  --date 1250 --date-end 1600 --precision century --qualifier circa \
  --place "Brooman Point" --lat 75.3833 --lon -97.2917 --bibkey mcghee1984thule \
  --tags thule,bowhead,winter-house \
  --detail "Winter villages of semi-subterranean houses framed in bowhead jaw and rib, roofed with skin and turf, sited where whales could be taken from the umiaq at the floe edge. Brooman Point on Bathurst Island, Qaummaarviit near Iqaluit, Nunguvik on Navy Board Inlet and the Ruin Island phase sites on Ellesmere and in northwest Greenland all belong to this span."

$P tools/history-db.py activity $T --title "The Little Ice Age contraction" \
  --date 1400 --date-end 1850 --precision century --qualifier circa \
  --place "Qikiqtaaluk" --lat 68.0 --lon -70.0 --bibkey mcghee1984thule \
  --tags little-ice-age,thule,historic-inuit \
  --detail "Heavier and longer-lasting sea ice closed the leads the bowhead needed. Whaling villages in the High Arctic were abandoned, the big winter houses gave way to the snow house and the sealing camp on the ice, and regional groups drew back to the coasts where ringed seal and caribou could be had. What Europeans met from the sixteenth century on is the far end of this adjustment, not the Thule pattern itself."

$P tools/history-db.py activity $T --title "Guy Mary-Rousseliere's excavations at Nunguvik" \
  --date 1967 --date-end 1989 --precision year \
  --place "Nunguvik" --lat 73.025 --lon -80.6333 --bibkey lynnerup2003human \
  --tags nunguvik,excavation \
  --detail "More than eighty dwelling remains recorded on Navy Board Inlet, spanning Middle Dorset, Late Dorset and Thule, by the Oblate missionary at Mittimatalik."

$P tools/history-db.py activity $T --title "Meldgaard's fieldwork on the Iglulik raised beaches" \
  --date 1954 --date-end 1965 --precision year \
  --place "Alarnerk" --lat 69.28 --lon -81.45 --bibkey lynnerup2003human \
  --tags excavation,igloolik,chronology \
  --detail "The Danish National Museum and University of Pennsylvania expedition located and mapped Pre-Dorset and Dorset sites around Iglulik in 1954, 1957 and 1965, and built the beach-terrace chronology from them."

$P tools/history-db.py activity $T --title "McGhee's excavations at Brooman Point" \
  --date 1979 --date-end 1980 --precision year \
  --place "Brooman Point" --lat 75.3833 --lon -97.2917 --bibkey mcghee1984thule \
  --tags excavation,brooman-point \
  --detail "Ten of the twenty Thule winter houses dug, and the Late Dorset settlement beneath them."

# --- single moments --------------------------------------------------------
$P tools/history-db.py event $T --date=-2500 --title "Paleo-Inuit cross into the eastern Arctic" \
  --precision century --qualifier circa --lat 69.377 --lon -81.799 --place "Iglulik" \
  --bibkey helmer1991palaeoeskimo --tags paleo-inuit,arrival \
  --detail "The Arctic Small Tool tradition appears east of the Mackenzie, in a landscape no human being had ever entered. Within a few centuries there are camps from Foxe Basin to northeast Greenland."

$P tools/history-db.py event $T --date 1902 --title "The last Sadlermiut die at Native Point" \
  --precision year --lat 63.7333 --lon -82.5167 --place "Native Point" \
  --bibkey jenness1925new --tags sadlermiut,epidemic \
  --detail "A disease brought ashore from the Scottish whaler Active in the autumn of 1902 killed the whole Sadlermiut population of Southampton Island over the following winter except a woman and four children. Their archaic-looking tools made them, for most of the twentieth century, the presumed last of the Dorset; ancient DNA published in 2014 makes them Thule people who had taken up Dorset stone technology instead. Dated to 1902 with year precision: the deaths ran through the winter of 1902-03."

$P tools/history-db.py event $T --date 1925 --title "Jenness names the Dorset culture" \
  --precision year --lat 64.2306 --lon -76.5386 --place "Kinngait" \
  --bibkey jenness1925new --people "Diamond Jenness" --tags dorset,discovery \
  --detail "From carved ivory and chipped stone sent to Ottawa from Cape Dorset, with no excavation context whatever, Diamond Jenness argued in the Geographical Review that these objects belonged to an older people than the Inuit, and named them for the place the collection came from."

$P tools/history-db.py event $T --date 1927 --title "Mathiassen defines the Thule culture" \
  --precision year --lat 66.52 --lon -86.25 --place "Naujaat" \
  --bibkey mathiassen1927archaeology --people "Therkel Mathiassen" --tags thule,archaeology \
  --detail "Archaeology of the Central Eskimos, from the Fifth Thule Expedition's digging at Naujan, Mittimatalik, Southampton Island and Malerualik, establishes a whale-hunting culture that spread east from Alaska and whose people are the ancestors of the modern Inuit."

$P tools/history-db.py event $T --date 1954 --title "Meldgaard maps 208 Dorset houses at Alarnerk" \
  --precision year --lat 69.28 --lon -81.45 --place "Alarnerk" \
  --bibkey lynnerup2003human --people "Jorgen Meldgaard;Guy Mary-Rousseliere;Alraq" \
  --tags excavation,chronology,alarnerk \
  --detail "Houses on beach terraces from 22 m down to 8 m above the sea, read as a sequence in time. Four Dorset individuals - three adults and an infant of about nine months - were recovered, part of a total of only twenty Dorset skeletons known anywhere."

$P tools/history-db.py event $T --date 1958 --title "Taylor excavates Tyara" \
  --precision year --lat 62.2 --lon -75.6 --place "Qikirtaq" \
  --bibkey jenness1925new --people "William E. Taylor Jr." --tags dorset,art,tyara \
  --detail "Three sites dug on Qikirtaq at the mouth of Sugluk Inlet, Nunavik: Keataina, Tyara and Toonoo. Tyara became the reference collection for early Dorset, and produced the ivory maskette 35 mm high that is now the most reproduced object of Dorset art."

$P tools/history-db.py event $T --date 2014 --title "Ancient DNA separates the Paleo-Inuit from the Inuit" \
  --precision year --lat 69.377 --lon -81.799 --place "Iglulik" \
  --bibkey raghavan2014genetic --tags genetics,dorset,thule \
  --detail "Genome-wide data from ancient and living Arctic peoples, published in Science, show the Paleo-Inuit as a migration into the Americas separate from both the earlier Native American and the later Inuit expansions. They persist in near-isolation for over four thousand years and vanish about seven hundred years ago, with no sign of having been absorbed."

echo DATES-OK
