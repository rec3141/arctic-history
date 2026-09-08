#!/bin/bash
set -e
cd /data/dev/arctic-history
P=/usr/bin/python3
T="--topic thule-dorset"

$P tools/history-db.py person --name "Ivaluardjuk" --indigenous --role "Iglulingmiut hunter and storyteller" \
  --affiliation "Rasmussen's Iglulik informants, 1922" $T --bibkey rasmussen1929intellectual \
  --note "An older Iglulingmiut man who gave Knud Rasmussen a great deal of the Iglulik material published in 1929, including the fullest recorded account of the Tunit: that they had many villages at Uglit, lived in houses of stone and whale bone, hunted the walrus with a long line and a short one, and were so strong that a jerk on the short line broke the animal's neck. His telling ends with a Tunit man harpooning the rocks in grief as his people leave. He is not describing an enemy; the tone is admiring and elegiac."

$P tools/history-db.py person --name "Alraq" --indigenous --role "Iglulingmiut hunter; informant on the Tunit" \
  --affiliation "the Danish National Museum and University of Pennsylvania excavations at Alarnerk, 1954" \
  $T --bibkey lynnerup2003human \
  --note "Described in the Alarnerk report as the excavators' best informant in 1954 about the Tunit. He told Guy Mary-Rousseliere that Inuit ancestors made long rectangular graves while Tunit graves were shorter, wider and built of bigger stones - a distinction the archaeologists then found in the ground. One of the clearest instances of Inuit oral knowledge and excavation agreeing on the same evidence."

$P tools/history-db.py person --name "Therkel Mathiassen" --role "archaeologist of the Fifth Thule Expedition" \
  --born 1892 --died 1967 --affiliation "Danish National Museum; Fifth Thule Expedition 1921-24" \
  $T --bibkey mathiassen1927archaeology \
  --note "Dug Naujan near Repulse Bay, sites at Mittimatalik (Pond Inlet), Southampton Island and Malerualik while the Fifth Thule Expedition worked across the central Arctic. His 1927 report defined the Thule culture, showed that its whale-hunting people had come east from Alaska, and identified them as the ancestors of the modern Inuit. Everything since is argument about the timing and the edges of that conclusion, not about the conclusion itself."

$P tools/history-db.py person --name "Diamond Jenness" --role "anthropologist; named the Dorset culture" \
  --born 1886 --died 1969 --affiliation "Canadian Arctic Expedition 1913-18; National Museum of Canada" \
  $T --bibkey jenness1925new \
  --note "New Zealand-born anthropologist who served with the Canadian Arctic Expedition. In 1925, from a box of carved ivory and chipped stone sent to Ottawa from Cape Dorset (Kinngait), he recognised an assemblage that fitted no known Inuit culture and proposed an older, separate people. He called them the Dorset, after the place the collection came from. He was working from objects with no excavation context at all, and he was right."

$P tools/history-db.py person --name "Jorgen Meldgaard" --also "Jørgen Meldgaard" \
  --role "archaeologist of the Igloolik raised beaches" --born 1927 --died 2007 \
  --affiliation "Danish National Museum; Danish National Museum-University of Pennsylvania expedition" \
  $T --bibkey lynnerup2003human \
  --note "Worked the Iglulik area in 1954, 1957 and 1965. At Alarnerk he mapped 208 Dorset houses on beach terraces from 22 m down to 8 m above sea level and read the falling terraces as falling time, giving the eastern Arctic its first ordered sequence of Paleo-Inuit material culture. He divided the Dorset part of it into five periods."

$P tools/history-db.py person --name "Guy Mary-Rousseliere" --also "Guy Mary-Rousselière; Ataata Mari" \
  --role "Oblate missionary and archaeologist" --born 1913 --died 1994 \
  --affiliation "Oblates of Mary Immaculate, Mittimatalik (Pond Inlet); editor of Eskimo" \
  $T --bibkey lynnerup2003human \
  --note "Missionary at Mittimatalik (Pond Inlet) who became the excavator of Nunguvik on Navy Board Inlet, where he recorded more than eighty dwellings spanning Middle Dorset, Late Dorset and Thule between 1967 and 1989. He drew the Alarnerk site map with Meldgaard and recorded the Iglulingmiut hunter Alraq on Tunit graves. He died in a fire at the Pond Inlet mission in 1994."

$P tools/history-db.py person --name "Robert McGhee" --role "archaeologist of the Canadian High Arctic" \
  --born 1941 --affiliation "Archaeological Survey of Canada; Canadian Museum of Civilization" \
  $T --bibkey mcghee1984thule \
  --note "Excavated Port Refuge on Devon Island and Brooman Point on Bathurst Island, and wrote the standard accessible accounts of Paleo-Inuit and Thule prehistory. At Brooman Point he found Thule houses built straight onto a Late Dorset village. He has argued in public writing that the Dorset and the Thule are two separate peoples whose stories happen to be told in the same ground, and that the Tuniit of Inuit tradition are the Dorset."

$P tools/history-db.py person --name "William E. Taylor Jr." --role "archaeologist; defined early Dorset" \
  --born 1927 --died 1994 --affiliation "National Museum of Man, Ottawa" \
  $T --bibkey jenness1925new \
  --note "Dug the Tyara and Arnapik sites in 1958 - Tyara on Qikirtaq at the mouth of Sugluk Inlet in Nunavik - and used them to define the early Dorset. The ivory maskette from Tyara, 35 mm high, came out of his excavation and is now the most reproduced object of Dorset art. Later director of the National Museum of Man."
echo PEOPLE-OK
