#!/bin/bash
set -e
cd /data/dev/arctic-history
P=/usr/bin/python3
T="--topic thule-dorset"
S=/data/dev/arctic-history/thule-dorset-scratch

$P tools/history-db.py track --id thule-dorset-001 $T \
  --title "The Thule migration from Alaska, schematic" \
  --date 1200 --date-end 1300 \
  --waypoints-file $S/wp-thule.json \
  --bibkey friesen2008timing \
  --credit "route schematic after Mathiassen 1927 and Friesen and Arnold 2008" \
  --licence "compiled for this project; underlying sources cited" \
  --creator "compiled from Mathiassen 1927 and Friesen and Arnold 2008" \
  --tags thule,migration,reconstructed \
  --description "A schematic line, not a route anyone travelled in one journey. The Thule people moved east out of north Alaska in small groups over several generations, and every segment here is inferred rather than recorded. What the archaeology does fix is the ends and the corridor: an Alaskan origin, a passage along the Beaufort Sea and Amundsen Gulf coasts, and Thule houses from Foxe Basin to northwest Greenland within a century or so of each other. Friesen and Arnold's 2008 radiocarbon dates from Washout on Qikiqtaruk and Nelson River on the Amundsen Gulf coast moved the departure later than the AD 1000 long assumed, to some time after AD 1200. The northern branch into the High Arctic - Bathurst Island, Devon Island, Ellesmere - and the branch down the Baffin coast are not drawn."

$P tools/history-db.py artifact --id thule-dorset-002 $T --type quote \
  --title "The Tornit shared the country" --date 1888 --precision year 2>/dev/null || true
$P tools/history-db.py artifact --id thule-dorset-002 $T --type quote \
  --title "The Tornit shared the country" --date 1888 \
  --lat 65.3 --lon -65.6 --creator "told to Franz Boas in Cumberland Sound, 1883-84" \
  --bibkey boas1888central --pages "pp. 634-635" \
  --credit "Franz Boas, The Central Eskimo, Sixth Annual Report of the Bureau of Ethnology, 1888" \
  --licence "public domain" --tags tuniit,oral-history,boas \
  --people "Franz Boas" \
  --description "Boas opens the Tornit tradition as an account of neighbours, not monsters: \"In olden times the Inuit were not the only inhabitants of the country in which they live at the present time. Another tribe similar to them shared their hunting ground. But they were on good terms, both tribes living in harmony in the villages. The Tornit were much taller than the Inuit and had very long legs and arms.\" Collected in Cumberland Sound during Boas's year among the Oqomiut, 1883-84."

$P tools/history-db.py artifact --id thule-dorset-003 $T --type quote \
  --title "The lamp under the coat" --date 1888 \
  --lat 65.3 --lon -65.6 --creator "told to Franz Boas in Cumberland Sound, 1883-84" \
  --bibkey boas1888central --pages "p. 634" \
  --credit "Franz Boas, The Central Eskimo, Sixth Annual Report of the Bureau of Ethnology, 1888" \
  --licence "public domain" --tags tuniit,oral-history,soapstone,lamp \
  --description "The single most striking piece of technical description in the Tornit tradition, and the one that matches the archaeology best. Sealing at a breathing hole in winter, a Tuniq wore a long deerskin coat pegged down to the snow at the hem: \"Under the jacket they carried a small lamp, called tumiujang (literally, resembling a footprint) or quming, over which they melted snow in a small pot.\" Boas adds that they frequently forgot the lamp, upset it when throwing the harpoon, and burned their skin. Small rectangular soapstone lamps of exactly this kind are among the commonest finds on Dorset sites."

$P tools/history-db.py artifact --id thule-dorset-004 $T --type quote \
  --title "Neither kayaks nor bows" --date 1888 \
  --lat 65.3 --lon -65.6 --creator "told to Franz Boas in Cumberland Sound, 1883-84" \
  --bibkey boas1888central --pages "p. 635" \
  --credit "Franz Boas, The Central Eskimo, Sixth Annual Report of the Bureau of Ethnology, 1888" \
  --licence "public domain" --tags tuniit,oral-history,technology \
  --description "\"All their weapons were made of stone. For the blades of their knives they used green slate (uluqsaq, literally material for women's knives), which was fastened by ivory pins to a bone or ivory handle. The points of their harpoons were made of bone, ivory, or slate; those of their lances, of flint or quartz, which was also used for drillheads; and they made neither kayaks nor bows.\" The last clause is the one archaeologists keep returning to. Dorset sites produce no bows and no drills; the tradition recorded in 1883 says the same thing, from the other direction."

$P tools/history-db.py artifact --id thule-dorset-005 $T --type quote \
  --title "The stolen kayak, and why the Tornit left" --date 1888 \
  --lat 65.3 --lon -65.6 --creator "told to Franz Boas in Cumberland Sound, 1883-84" \
  --bibkey boas1888central --pages "p. 636" \
  --credit "Franz Boas, The Central Eskimo, Sixth Annual Report of the Bureau of Ethnology, 1888" \
  --licence "public domain" --tags tuniit,oral-history,departure \
  --description "A young Tuniq borrows a young Inung's kayak without asking and stoves in the bottom; the owner runs a knife into the sleeping man's neck. \"The Tornit then became afraid that the Inuit would kill them all and preferred to leave the country for good. They assembled at Qernirtung (a place in Cumberland Sound), and in order to deceive any pursuers they cut off the tails of their jumpers and tied their hair into a bunch protruding from the crown of the head.\" A second version has an Inung break his neck at play, with the same result. In every version the Tuniit leave rather than fight."

$P tools/history-db.py artifact --id thule-dorset-006 $T --type quote \
  --title "Merrymaking among the Tornit: a song still danced in 1884" --date 1888 \
  --lat 65.3 --lon -65.6 --creator "recited to Franz Boas in Cumberland Sound, 1883-84" \
  --bibkey boas1888central --pages "p. 649" \
  --credit "Franz Boas, The Central Eskimo, Sixth Annual Report of the Bureau of Ethnology, 1888" \
  --licence "public domain" --tags tuniit,oral-history,song,dance \
  --description "Boas printed the tune with the words: \"Pika pikagning mingepignirming qijepignirming sukadla. aq! aq!\" and then the dance: \"The Eskimo reciting this song jump up and down and to the right and left with their legs bent and their hands hanging down, the palms touching each other. In crying aq! aq! they jump as high as possible.\" Two more Songs of the Tornit follow at pp. 653-654. Whatever the Tuniit were, people were still singing their songs in Cumberland Sound in the 1880s."

echo ARTIFACTS1-OK
