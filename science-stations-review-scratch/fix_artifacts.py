#!/usr/bin/env python3
import sys
sys.path.insert(0, "science-stations-review-scratch")
from reenter import reenter

D = {}

D["science-stations-007"] = (
    "Named on 6 January 1949 for HMS Alert, in which Nares wintered a few kilometres away at "
    "Floeberg Beach in 1875-76. Twelve men built it in the summer of 1950 under the Canadian "
    "officer-in-charge J. Leo Lafranchise, working from an ice runway on Dumbbell Bay; one of "
    "them, the airstrip mechanic J. Peter Johnson, Jr., wrote the account of it forty years "
    "later. It stands at 82 deg 30'N, about 830 km from the Pole, and with the military station "
    "that grew beside it from 1958 it is the northernmost permanently inhabited place on Earth."
)

D["science-stations-017"] = (
    "Adolphus W. Greely opens his official report on the Lady Franklin Bay expedition by putting "
    "the science first: 'In its scientific work it formed one of the circumpolar international "
    "stations, which grew out of the exertions of Lieut. Charles Weyprecht, Austrian Navy, and "
    "which were finally determined upon by the International Polar Conferences of Hamburg, Berne, "
    "and St. Petersburg. Eleven nations participated in this great work, and fourteen stations "
    "were occupied, three of which were in the southern hemisphere.'"
)

D["science-stations-018"] = (
    "Adolphus W. Greely counts the day's work at Fort Conger: 'The number of observations made "
    "and recorded each day were as follows: Meteorological, 234; tidal, 28; magnetical, 264 - "
    "aggregating 526 daily. On term-days the number of magnetical observations were increased to "
    "over twelve hundred, so that the observers were always busy.'"
)

D["science-stations-021"] = (
    "Counted from Weyprecht it is the fourth polar year, though it is usually written IPY "
    "2007-08; the period ran from 1 March 2007 to 1 March 2009 so that both poles got two full "
    "annual cycles. Canada's contribution was the largest it had ever made to a polar year, and "
    "much of it went to sea: the Amundsen - the icebreaker Louis Fortier and fifty-three fellow "
    "researchers had made the case for in 2001 - spent fifteen months in the Arctic on the "
    "Circumpolar Flaw Lead study, overwintering in the Beaufort Sea with the ship as the station. "
    "The arc closes here. In 1882 the way to hold a station through the winter was to build a "
    "house and leave men in it; in 2007 it was to freeze a ship in on purpose and keep the "
    "laboratories warm."
)

D["science-stations-023"] = (
    "On the evening the spring airlift ended, six of the twelve men building Alert took a weasel "
    "across Ravine Bay and the neck of Mushroom Point and climbed to the two cairns on Cape "
    "Sheridan. At the cairn surmounted by a wooden cross, at about midnight, they found an old "
    "powdered-egg tin wedged behind a rock on its side, holding a message left by Commander R.E. "
    "Peary in 1907. J. Peter Johnson, Jr., who was there, wrote that for a moment the find created "
    "a sense of the remoteness of this coast that none of them had felt before. The message was "
    "collected by a Canadian official that August and sent to the museum of the U.S. Naval "
    "Academy. Below on the shore the party found the memorial cairn to Ross G. Marvin, one of "
    "Peary's party (Johnson calls it the 1907 expedition; Marvin drowned in April 1909); its cross "
    "had fallen, and they set it upright again."
)

D["science-stations-027"] = (
    "Saroomie Manik, on the 1975 move of the settlement across Resolute Bay to Ralph Erskine's new "
    "townsite: 'I was satisfied with the way it was set up [before 1975]. I'm sorry we moved [to "
    "the new settlement]. We were close to the shore and we are too far from the shore right "
    "now... This is the part I don't like about the relocation from the other settlement.'"
)

D["science-stations-031"] = (
    "The three drifting Ts in the Arctic Ocean are famous. The more useful finding for anyone "
    "working in these channels is Moira Dunbar's: going through RCAF trimetrogon air photographs "
    "of the Archipelago she identified twenty-eight more ice islands, from a quarter of a mile to "
    "seven or eight miles across, plus a great many fragments, scattered from north Ellesmere to "
    "Victoria Strait. Three in the Arctic Ocean off Alert Point, on the very edge of the pack; "
    "three in the Nansen Sound-Eureka Sound reach; five in Peary Channel 15 miles north of Amund "
    "Ringnes; one in the Prince Gustaf Adolf Sea; three in Maclean Strait, one of which moved 60 "
    "miles south between August 1950 and July 1951; one in Byam Martin Channel east of Sabine "
    "Peninsula; four in Hecla and Griper Bay; one in Peel Sound off the western entrance to Bellot "
    "Strait; three in James Ross Strait between Cape Felix and Cape Adelaide Regina; and four in "
    "Erebus Bay on the west coast of King William Island, the farthest south any has been found. "
    "The points plotted here are the ones for which a position is printed, plus a few whose "
    "described location is unambiguous; the rest are described in words only. Ice islands drift "
    "with the current rather than the wind, which is why they behave unlike the pack around them "
    "and why they are worth watching from a ship."
)

D["science-stations-033"] = (
    "Four papers under one title, and the first full public account of the ice islands. Part I, by "
    "Major L.S. Koenig of the USAF, tells how T-1, T-2 and T-3 were found on radar and by eye from "
    "weather reconnaissance aircraft. Part II, by Squadron-Leader K.R. Greenaway of the RCAF, "
    "identifies T-3 retrospectively in 1947 and 1948 photographs. Part III, by Moira Dunbar of the "
    "Defence Research Board, identifies twenty-eight more in air photographs of the Archipelago "
    "and combs the older narratives for earlier sightings; it is Dunbar who sets Aldrich's 1875 "
    "description of 'ice waves' or 'ice rollers' and Peary's of 1906 beside the 1950 photographs "
    "and concludes that the shelf then reached further west, and in the previous century further "
    "east, than it does now. Part IV, by Geoffrey Hattersley-Smith, argues that the islands calve "
    "from the shelf ice fringing the north coast of Ellesmere between Cape Columbia and Yelverton "
    "Bay - the position given here. All measurements in the paper are in nautical miles."
)

for aid, desc in D.items():
    reenter(aid, description=desc)
