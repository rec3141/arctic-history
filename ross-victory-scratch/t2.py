import sys
sys.path.insert(0,'/data/dev/arctic-history/ross-victory-scratch')
from verify import best,flat,FILES
tests=[("N","Enderby"),("N","Blackheath"),("N","tracts"),
("N","Robertson"),("N","Fearnall"),("N","seven feet six"),("N","Isle of Man"),
("N","thirteen or fourteen revolutions"),("N","hundred and fifty tons"),
("N","five feet and a half"),("N","1500 tons"),("N","the second of November"),
("N","twelve hours"),("N","evening school"),("N","Mrs. Enderby"),
("N","a hundred and ten"),("N","Braithwaite and Ericsson"),
("N","he who is well-fed"),("N","no man was absolutely sick"),
("N","greasy gormandizing"),("N","the whole land our enemies"),
]
m={'N':'ross1835narrative','H':'huish1835last','A':'ross1835appendix'}
for k,q in tests:
    s,seg=best(flat(FILES[m[k]]),q)
    print(f"{s:.3f} | {q}")
    if s<1.0: print("      ->",seg[:200])
