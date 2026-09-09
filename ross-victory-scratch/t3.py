import sys
sys.path.insert(0,'/data/dev/arctic-history/ross-victory-scratch')
from verify import best,flat,FILES
tests=[("N","William Lee"),("N","Possession Bay"),("N","5000"),("N","five thousand pounds"),
("N","Mount Sherrar"),("N","Humphreys"),("N","Long Hope"),
("H","in a great measure the chief command"),("H","entire direction of the navigation"),
("H","second in command"),("N","Krusenstern"),("N","Leopold"),
("N","thirteen of our number"),("N","twenty-one"),("N","twenty-two"),
("N","the whole of our party"),("H","Light"),
]
m={'N':'ross1835narrative','H':'huish1835last','A':'ross1835appendix'}
for k,q in tests:
    s,seg=best(flat(FILES[m[k]]),q)
    print(f"{s:.3f} | [{k}] {q}")
    if 0<s<1.0: print("      ->",seg[:200])
