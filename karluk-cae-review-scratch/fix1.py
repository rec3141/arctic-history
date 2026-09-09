#!/usr/bin/env python3
import json, sys
sys.path.insert(0, "/data/dev/arctic-history/karluk-cae-review-scratch")
from edit_artifacts import edit

# ---------------------------------------------------------- check flags: name
# the people in the description itself, plus quotation and framing corrections.

edit("karluk-cae-020", description=(
    "Captain Robert Bartlett watched his ship go down from the floe and set the moment down "
    "exactly: \"It was at 4 p. m. on January 11, 1914, with the blue Canadian Government ensign "
    "at her main-topmast-head, blowing out straight and cutting the water as it disappeared, and "
    "the Victrola in the galley sending out the strains of Chopin's Funeral March, that the Karluk "
    "sank, going down by the head in thirty-eight fathoms of water.\" As she went he bared his head "
    "and said, \"Adios, Karluk!\""))

edit("karluk-cae-021", description=(
    "The ice opened the ship's side on the evening of 10 January 1914 and Robert Bartlett gave the "
    "order: \"I went on deck again and gave the order, 'All hands abandon ship.'\" Everything that "
    "could be moved had already been carried onto the floe, which became Shipwreck Camp."))

edit("karluk-cae-022", description=(
    "Halfway between Wrangel Island and Siberia, on ice that was moving under them, Claude "
    "Kataktovik turned to Robert Bartlett and said: \"We see no land, we no get to land; my mother, "
    "my father, tell me long time ago Eskimo get out on ice and drive away from Point Barrow never "
    "come back.\" Bartlett tried to hearten him by saying that white men would come out to look for "
    "them. Position approximate."))

edit("karluk-cae-023", tags=["karluk", "siberia", "east-verified"], description=(
    "Claude Kataktovik's first sight of the Siberian coast, from the top of a pressure ridge: "
    "\"Me see him, me see him noona (land),\" he said. He and Robert Bartlett came ashore near Cape "
    "Yakan three days later. Position approximate, and the longitude is east: this is the Asian side "
    "of the 180th meridian."))

edit("karluk-cae-024", description=(
    "Robert Bartlett's written order to the chief engineer John Munro, left with him on Wrangel "
    "Island on 18 March 1914 as Bartlett and Kataktovik started for Siberia: \"You will assemble at "
    "Rodgers Harbor about the middle of July where I hope to meet you with a ship.\" It was five "
    "months before a ship came, and three men were dead by then."))

edit("karluk-cae-025", lat=70.2, lon=-176.5, description=(
    "The first words exchanged at the rescue. Robert Bartlett crossed from the revenue cutter Bear "
    "to the King and Winge when the two ships met in the ice on 8 September 1914, and William Laird "
    "McKinlay answered for the survivors: \"'All of you here?' ... 'No,' he answered; 'Malloch and "
    "Mamen and Breddy died on the island.'\" Pinned at sea about seventy-five miles southeast of "
    "Rodgers Harbour, where the ships met; position approximate."))

edit("karluk-cae-030", description=(
    "Vilhjalmur Stefansson, Storker Storkerson and Ole Andreasen came ashore on Norway Island off "
    "Banks Island on the evening of 25 June 1914: \"We landed on June 25th at 8:10 in the evening, "
    "ninety-six days out from the Alaska coast.\" And of the night that followed: \"Our first sleep "
    "on the land floe had a comfort and security about it that we had not known for over ninety "
    "days.\" The chapter heading says ninety-three days; the text says ninety-six."))

edit("karluk-cae-032", description=(
    "McClintock's Franklin-search record of 1853 is dated \"P. M., June 15, 1853\". Vilhjalmur "
    "Stefansson opened the cairn that held it, at Cape McClintock on Prince Patrick Island, exactly "
    "sixty-two years later: \"I picked it up at 9:58 P. M. local apparent time, June 15, 1915, just "
    "sixty-two years later to the nearest half day.\" He took the original away for the Department of "
    "the Naval Service and rebuilt the cairn with a copy of his own. See [[topic:franklin-search]] "
    "and [[topic:mcclure-investigator]]."))

edit("karluk-cae-040", description=(
    "Diamond Jenness describing the two-roomed snow house on Coronation Gulf that he shared with "
    "Ikpakhuak's family: \"His family consisted of his wife Higilak, his nephew and adopted son "
    "Haugak, ... Higilak's daughter (by a former husband) Kanneyuk, who was about twelve years of "
    "age, and myself, since this was the family into which I was formally adopted.\" The words "
    "left out name Haugak's own father, Haviron."))

edit("karluk-cae-058", description=(
    "Vilhjalmur Stefansson and five others - Burt McConnell, George Hubert Wilkins, Diamond Jenness "
    "and the Inupiat hunters Panyurak and Asatshak - setting out over the ice on the caribou hunt of "
    "20 September 1913, photographed from the ship. A gale that night took the Karluk west, and the "
    "six men on the ice never saw her again. It is the most argued-over photograph of the expedition."))

edit("karluk-cae-059", description=(
    "Two men carrying a load ashore from the schooner Mary Sachs on 1 September 1914. George Hubert "
    "Wilkins had got her to Cape Kellett and built the base there; ten days later Vilhjalmur "
    "Stefansson walked in off the ice and found that it existed. The community of Sachs Harbour on "
    "Banks Island is named for this ship. Canadian Museum of History negative 50855."))

edit("karluk-cae-061", description=(
    "An outcrop of sandstone above the snow-covered hillside at Liddon Gulf, with a dog team and the "
    "party's snow houses at its base, photographed by George Hubert Wilkins on 13 April 1916. The "
    "Northern Party's geology on Melville Island was done by eye between marches; Stefansson's own "
    "interest on this crossing was in the depth of the sea under the ice. Canadian Museum of History "
    "negative 51146."))

edit("karluk-cae-063", description=(
    "About 1 MB: the front matter; Therkel Mathiassen's Introduction, which sets out season by season "
    "where the expedition's diggers were - himself at Naujan, Duke of York Bay and Mittimatalik, Knud "
    "Rasmussen on King William Island, Peter Freuchen at Chesterfield Inlet and Qilalukan, Kaj "
    "Birket-Smith on Sentry Island, Helge Bangsted on Vansittart Island and Jacob Olsen helping at "
    "Naujan; Part 1 chapters 3-4 (the Sadlermiut of Southampton Island; other Thule finds); and the "
    "whole of Part 2, in which the Thule culture is defined and traced from Alaska eastward. Part 1 "
    "chapters 1 and 2, the Naujan find itself and northern Baffin Land, are missing from this "
    "transcription; for those there is the scan, [[artifact:karluk-cae-064]]. Pinned at Naujan in "
    "Repulse Bay."))

edit("karluk-cae-069", description=(
    "Therkel Mathiassen on the expedition's first autumn, from his introduction to volume IV of the "
    "Report: \"In 1921 the expedition arrived at headquarters, Danish Island near Vansittart Island, "
    "at such an advanced date - 18th September - that no excavating could be done. In the summer of "
    "1922 I excavated for two months at Naujan in Repulse Bay, helped during the last month by our "
    "Greenland interpreter Jacob Olsen.\" It is the sentence that fixes the date Knud Rasmussen's "
    "party reached its base, which the published narratives do not give."))

# ------------------------------------------------------- 'discovery' framing
edit("karluk-cae-010", tags=["meighen", "new-land", "queen-elizabeth-islands"])
edit("karluk-cae-011", tags=["meighen", "new-land"])
edit("karluk-cae-050", tags=["meighen", "new-land", "queen-elizabeth-islands"])
edit("karluk-cae-066", tags=["meighen", "new-land", "queen-elizabeth-islands", "1916"])
edit("karluk-cae-033", tags=["queen-elizabeth-islands", "possession", "borden"])
