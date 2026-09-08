#!/bin/bash
set -e
cd /data/dev/arctic-history
P=/usr/bin/python3
T="--topic thule-dorset"

$P tools/history-db.py place --name "Alarnerk" --historic "Alarnerk" --inuktitut "Alaniq" \
  --lat 69.28 --lon -81.45 --kind site $T --bibkey lynnerup2003human \
  --note "Dorset site NhHd-1 on the northeast corner of the Melville Peninsula, southeast of Igloolik Island. Jorgen Meldgaard mapped 208 house remains here in 1954, strung along 2.5 km of coast on raised limestone beach ridges from 22 m down to 8 m above the sea. Because the land has risen steadily since the ice went, the highest beaches carry the oldest houses: the site is a staircase of time, and Meldgaard used it to build the relative chronology of Dorset material culture that eastern Arctic archaeology still works from. The Dorset occupation runs from about 800-600 BC to about AD 1100-1200. Coordinates approximate, from the published description; the site's own coordinates are not given in the report."

$P tools/history-db.py place --name "Brooman Point" --historic "Brooman Point" \
  --lat 75.3833 --lon -97.2917 --kind site $T --bibkey mcghee1984thule \
  --note "A low gravel point on the east coast of Bathurst Island. Robert McGhee dug ten of the twenty Thule winter houses here in 1979 and 1980 and found that the Thule builders had raised their whale-bone-and-sod houses directly on top of a Late Dorset settlement, robbing its stone and its bone. It is the clearest single place in the archipelago to see one people succeed another. Coordinates from the Canadian Geographical Names Database; the Wikipedia article on Brooman Point Village gives 75.767 N, 97.783 W instead, and the two have not been reconciled here."

$P tools/history-db.py place --name "Qaummaarviit" --historic "Qaummaarviit" --inuktitut "Qaummaarviit" \
  --lat 63.7256 --lon -68.6925 --kind site $T --bibkey nunavutparks2022qaummaarviit \
  --note "A small island in Peterhead Inlet about 12 km west of Iqaluit, now a territorial park. Eleven qarmait - winter houses of stone, sod, whale jaw and rib, roofed with skins - remain on it, with tent rings and graves. Thule people wintered here from about the thirteenth century; over 3,000 tools and 20,000 animal bones have been excavated. Chipped stone found in the sod of the Thule walls is Dorset, which means the Thule builders were cutting their turf out of an older people's settlement. The name means roughly the place that shines."

$P tools/history-db.py place --name "Port Refuge" --historic "Port Refuge" \
  --lat 76.3 --lon -94.7167 --kind harbour $T --bibkey mcghee1979palaeoeskimo \
  --note "A bay on the south side of Grinnell Peninsula, Devon Island. Robert McGhee's excavations here recovered the Independence I and Pre-Dorset camps of the first people into the High Arctic, and Late Dorset material above them: one small stretch of coast holding both ends of the Paleo-Inuit story. Coordinates from the Canadian Geographical Names Database."

$P tools/history-db.py place --name "Native Point" --historic "Native Point" --inuktitut "Tunirmiut" \
  --lat 63.7333 --lon -82.5167 --kind site $T --bibkey jenness1925new \
  --note "On the southeast coast of Southampton Island, the main village of the Sadlermiut, who lived apart from other Inuit and whose tools and speech struck every visitor as archaic. The last Sadlermiut died in the winter of 1902-03 of a disease brought ashore from the whaler Active. For most of the twentieth century they were read as the last of the Dorset; ancient DNA published in 2014 makes them Thule people who had taken up Dorset stone technology, not Dorset survivors. The Inuktitut name of the site, Tunirmiut, is built on the same root as Tuniit."

$P tools/history-db.py place --name "Button Point" --historic "Button Point" \
  --lat 73.05 --lon -78.55 --kind site $T --bibkey mcghee1984thule \
  --note "At the southeast tip of Bylot Island, off the north end of Qikiqtaaluk (Baffin Island), near Mittimatalik (Pond Inlet). Waterlogged Late Dorset deposits here preserved wood and antler that would rot anywhere drier: driftwood masks the size of a face, small drums, carved wands and figures. It is the richest single source of Dorset shamanic material in the Arctic. Coordinates approximate, read off the island's southeastern tip."

$P tools/history-db.py place --name "Uglit" --historic "Ooglit Islands" --inuktitut "Uglit" \
  --lat 69.3 --lon -81.1 --kind site $T --bibkey rasmussen1929intellectual \
  --note "Islands in northern Foxe Basin near Iglulik whose name means the place where walrus haul out. Ivaluardjuk told Rasmussen in 1922 that the Tunit had many villages at Uglit, built of stone and whale bone, and that when they were driven out one man harpooned the rocks in grief and made the stones fly about like bits of ice. Coordinates approximate."

$P tools/history-db.py place --name "Qikirtaq" --historic "Sugluk Island" --inuktitut "Qikirtaq" \
  --lat 62.2 --lon -75.6 --kind site $T --bibkey jenness1925new \
  --note "An island at the mouth of Sugluk Inlet, Nunavik, off Salluit on the south shore of Hudson Strait. William E. Taylor Jr. dug three sites here in 1958 - Keataina, Tyara and Toonoo - and the Tyara material became the type collection for early Dorset. The ivory maskette from Tyara is the best known single object of Dorset art. Coordinates are those of Salluit, the nearest community; the island lies at the inlet mouth just north of it."
echo PLACES-OK
