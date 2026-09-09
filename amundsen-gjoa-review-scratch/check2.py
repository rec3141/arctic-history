import sys; sys.path.insert(0,'amundsen-gjoa-review-scratch')
from q import find
QS = [
("p20-fram-dogs","the old Fram dogs and the new ones from Godhavn"),
("p20-mylius","Mylius"),
("p30-trench","more than once we stretched our aching backs, unaccustomed to this kind of work, and wished trench-digging to the deuce"),
("p30-passedover","probably passed over"),
("p30-victoriaharbour","possibly even more interesting than at the Pole itself"),
("p30-notbrilliant","So our trip was not a brilliant success"),
("p30-sheepish","slunk away very sheepishly"),
("p40-crippled","crippled in a single day"),
("p40-neckties","like neckties"),
("p40-secondhand","when we want serviceable clothes, we buy them second hand from the wearer"),
("p40-gratedsugar","as fine as grated sugar"),
("p40-window","the most elegant window imaginable"),
("p40-snowblockhead","Many a snow-block did I get on my head when I essayed this work"),
("p40-spectre","the spectre of scurvy showed itself for the first time"),
("p40-cleverest","in reality the cleverest of them"),
("p50-windlass","Precisely at 3 a.m. on August 13th, 1905, the windlass turned"),
("p50-lead","The man attending to the soundings had his full share of work; the lead flew up and down so rapidly that it was almost a wonder it did not melt"),
("p50-tenfathoms","Ten fathoms and a clay bottom, was the report; then again, eight fathoms, stone; ten fathoms and clay"),
("p50-shuddered","we had long talked about and shuddered at"),
("p50-thickice","just as if we were in thick ice"),
("p50-beeline","I can vouch for it, as it was my turn at the helm, that the passage did not, by any means, resemble a bee-line"),
("p50-drunk","We bungled through zigzag, as if we were drunk"),
("p50-maniac","jumping about like a maniac, throwing his arms about for starboard and port"),
("p50-distracted","utterly distracted"),
("p60-villa","for all the world like a villa residence"),
("p60-telegram","I despatched my precious telegram, which was only just in time, as shortly afterwards the wires broke down, owing to the intense cold"),
]
for tag,text in QS:
    r=find(text,60)
    if r: print(f"OK   {tag}: " + ", ".join(k for k,_,_ in r))
    else: print(f"MISS {tag}: {text[:90]}")
