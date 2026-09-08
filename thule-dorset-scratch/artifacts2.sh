#!/bin/bash
set -e
cd /data/dev/arctic-history
P=/usr/bin/python3
T="--topic thule-dorset"

$P tools/history-db.py artifact --id thule-dorset-007 $T --type quote \
  --title "Ivaluardjuk: the Tunit were driven out" --date 1929 \
  --lat 69.377 --lon -81.799 --creator "Ivaluardjuk, to Knud Rasmussen at Iglulik" \
  --bibkey rasmussen1929intellectual --pages "p. 256" \
  --credit "Knud Rasmussen, Intellectual Culture of the Iglulik Eskimos, Report of the Fifth Thule Expedition, 1929" \
  --licence "public domain" --tags tuniit,oral-history,rasmussen \
  --people "Ivaluardjuk;Knud Rasmussen" \
  --description "\"Before the present Iglulingmiut and Aivilingmiut came to the land where they now live, it was inhabited by a great and strong people called Tunit. They lived in stone houses in winter, and were mighty men in all manner of hunting by sea. But they were very quarrelsome, and easily angered. At first the tribes lived peaceably together down by the coast, but the Tunit were too easily angered, and were at last driven out of the country.\" Note what is and is not claimed: a prior population, stone houses, sea-mammal hunting, and a departure rather than a slaughter."

$P tools/history-db.py artifact --id thule-dorset-008 $T --type quote \
  --title "Ivaluardjuk: the walrus hunters of Uglit" --date 1929 \
  --lat 69.3 --lon -81.1 --creator "Ivaluardjuk, to Knud Rasmussen at Iglulik" \
  --bibkey rasmussen1929intellectual --pages "pp. 256-257" \
  --credit "Knud Rasmussen, Intellectual Culture of the Iglulik Eskimos, Report of the Fifth Thule Expedition, 1929" \
  --licence "public domain" --tags tuniit,oral-history,walrus,uglit \
  --people "Ivaluardjuk;Knud Rasmussen" \
  --description "Under the heading Tunit, the strong folk and lovers of women: \"It is said that the Tunit had many villages at Uglit near Iglulik. They lived in houses built of stone and the bones of whales. They were strong folk, skilful in hunting by sea. They hunted the walrus with a long harpoon line and a short one. When they had harpooned a walrus with the short line, they gave it a jerk, and so strong were they, that this broke the creature's neck.\" Ivaluardjuk goes on: when the exhausted hunters came in sight of home and their women came out to meet them, they forgot their weariness in a moment."

$P tools/history-db.py artifact --id thule-dorset-009 $T --type quote \
  --title "The man who harpooned the rocks" --date 1929 \
  --lat 69.3 --lon -81.1 --creator "Ivaluardjuk, to Knud Rasmussen at Iglulik" \
  --bibkey rasmussen1929intellectual --pages "p. 257" \
  --credit "Knud Rasmussen, Intellectual Culture of the Iglulik Eskimos, Report of the Fifth Thule Expedition, 1929" \
  --licence "public domain" --tags tuniit,oral-history,uglit,departure \
  --people "Ivaluardjuk;Knud Rasmussen" \
  --description "The close of Ivaluardjuk's account: \"The Tunit were a strong people, and yet they were driven from their villages by others who were more numerous, by many people of great ancestors; but so greatly did they love their country, that when they were leaving Uglit, there was a man who, out of desperate love for his village, harpooned the rocks with his harpoon and made the stones fly about like bits of ice.\" This is a story told by the winners about the losers, and it is told as a lament."

$P tools/history-db.py artifact --id thule-dorset-010 $T --type quote \
  --title "The sea woman's house is built like a Tunit house" --date 1929 \
  --lat 69.377 --lon -81.799 --creator "Iglulingmiut shamans, to Knud Rasmussen" \
  --bibkey rasmussen1929intellectual --pages "pp. 126-127" \
  --credit "Knud Rasmussen, Intellectual Culture of the Iglulik Eskimos, Report of the Fifth Thule Expedition, 1929" \
  --licence "public domain" --tags tuniit,shamanism,takanakapsaluk \
  --people "Knud Rasmussen" \
  --description "In the account of the shaman's journey to Takanakapsaluk, the mother of the sea animals, at the bottom of the sea, the shaman comes at last to \"the house of Takanakapsaluk, built of stone, with a short passage way, just like the houses of the tunit.\" The oldest and most powerful being in the Iglulingmiut cosmos lives in a house of the kind that stands in ruins on the beaches: the Tuniit are not only a memory of other people but a way of saying old."

$P tools/history-db.py artifact --id thule-dorset-011 $T --type quote \
  --title "Mathiassen: it must have been a migration" --date 1927 \
  --lat 66.52 --lon -86.25 --creator "Therkel Mathiassen" \
  --bibkey mathiassen1927archaeology --pages "p. 184" \
  --credit "Therkel Mathiassen, Archaeology of the Central Eskimos, Part 2, Report of the Fifth Thule Expedition, 1927; transcription at Wikisource" \
  --licence "public domain" --tags thule,migration,mathiassen \
  --people "Therkel Mathiassen" \
  --description "The conclusion the whole of eastern Arctic archaeology still rests on, written after digging Naujan at Repulse Bay: \"We must therefore imagine that the Thule culture, with all its peculiar whaling culture, has originated somewhere in the western regions, in an Arctic area where whales were plentiful and wood abundant... and from there it has spread eastwards right to Greenland, seeking everywhere to adapt itself to the local geographical conditions. And it can hardly have been a culture wave alone; it must have been a migration.\" Pinned at Naujaat (Repulse Bay), where Naujan lies."

$P tools/history-db.py artifact --id thule-dorset-012 $T --type text \
  --title "Alraq on how to tell a Tunit grave" --date 1957 \
  --lat 69.28 --lon -81.45 --creator "Alraq, to Guy Mary-Rousseliere" \
  --bibkey lynnerup2003human --pages "p. 351" \
  --credit "reported by Guy Mary-Rousseliere, in Lynnerup et al., Arctic 56(4), 2003" \
  --licence "quoted from an open-access article (Arctic Institute of North America)" \
  --tags tuniit,oral-history,graves,alarnerk \
  --people "Alraq;Guy Mary-Rousseliere;Jorgen Meldgaard" \
  --description "At Alarnerk in 1954 the excavators' best informant on the Tunit was an older Iglulingmiut hunter named Alraq. He told Father Guy Mary-Rousseliere: \"...our Inuit ancestors had long rectangular graves. The Tunit graves were very different: they were shorter and wider, and bigger stones were used for their walls...\" On the highest beaches at Alarnerk, 21 to 22 m above the sea, the excavators found short, wide stone chambers 1 to 1.4 m long, built of heavy stones, with Late Dorset artefacts scattered around them. The oral distinction and the excavated one are the same distinction."

echo ARTIFACTS2-OK
