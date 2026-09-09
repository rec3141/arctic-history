import re,sys
sys.path.insert(0,'/data/dev/arctic-history/ross-victory-scratch')
from verify import best,flat,FILES
tests=[
("N","can make a valuable progress"),
("N","being perfectly useless, we were compelled to trust to our sails, under which we had the mortification to find, not only a steadily adverse breeze, but that we were beaten by every vessel that we saw"),
("N","it was very certain that we had now settled ourselves for the winter"),
("N","he who is well-fed resists cold better than the man who is stinted"),
("N","while the starvation from cold follows but too soon a starvation in food"),
("N","This, doubtless, explains in a great measure, the resisting powers of the natives of these frozen climates"),
("N","their consumption of food, it is familiar, being enormous, and often incredible"),
("N","the aid of the Esquimaux, who had formerly been of such essential service to us, by means of their sledges and dogs, and by the great ease and expedition with which they raised our temporary encampments"),
("N","ceased to traverse"),
("N","it was the ship Victory, under the command of Captain John Ross, which assigned the north-west Magnetic Pole, in the year 1831, and that this vessel was fitted out by him whom I can now call Sir"),
("N","completely exhausted by hunger and fatigue"),
("N","just as I had seen it in 1818"),
("N","It was the first of our losses which could, in any fairness, be attributed to the climate"),
("N","it was a change like that of magic, to find that solid mass of ocean"),
("N","suddenly converted into water"),
("N","We could have wished that a place so important had possessed more of mark or note"),
("H","from authentic information and original documents, transmitted by an officer attached to the last expedition"),
("H","in a great measure"),
("H","too manifest to excite any hope of obtaining any benefit from its use"),
]
m={'N':'ross1835narrative','H':'huish1835last','A':'ross1835appendix'}
for k,q in tests:
    s,seg=best(flat(FILES[m[k]]),q)
    print(f"{s:.3f} | {q[:70]}")
    if s<0.98: print("      TEXT:",seg[:230])
