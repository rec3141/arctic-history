import sys, subprocess
sys.path.insert(0,'/data/dev/arctic-history/ross-victory-scratch')
from upd import upd, get
from updev import evupd
R='/data/dev/arctic-history'
def run(*a):
    p=subprocess.run(['/usr/bin/python3','tools/history-db.py',*a],cwd=R,capture_output=True,text=True)
    print(('ok  ' if not p.returncode else 'FAIL ')+' '.join(a[:3])[:50], p.stderr[-300:] if p.returncode else '')

d=get('ross-victory-039')['description'].replace(
  'Three of twenty-three did not come home from four winters beset and a fifth ashore.',
  'Three of the twenty-three did not come home from four winters in the ice, three of them beset in the ship and a fourth in the hut at Fury Beach.')
upd('ross-victory-039', description=d)

d=get('ross-victory-083')['description'].replace(
  'after four winters beset and a retreat to Fury Beach',
  'after three winters beset on the Boothia coast and a fourth in a hut at Fury Beach')
upd('ross-victory-083', description=d)

evupd(384, detail="Four years and nearly five months, of which the crew spent four winters in the ice: three of them beset in the ship on one stretch of the Boothia coast, and a fourth in a hut of salvaged spars at Fury Beach. The ship's company was twenty-three: twenty paid hands and three officers - John Ross, his nephew James Clark Ross and the purser William Thom - who served without pay. Three died on the voyage and twenty came home; the Commons committee that examined the accounts put it that only one man in twenty-three was lost in consequence of the expedition.")

run('person','--name','Henry Ayre',
    '--note',"Cook of the Victory through three winters beset on the Boothia coast and a fourth in the hut at Fury Beach. He came home in the Isabella in October 1833 and the Admiralty's payment list of 28 October records his 165 pounds 2s 8d against the note 'Died soon after his return'. Ross's crew list spells him Eyre; the payment list Ayre.")

run('topic','--slug','ross-victory','--title',"John Ross's Victory, 1829-1833",
    '--summary',"A private expedition, paid for by the distiller Felix Booth after the Admiralty refused it, took the first steam vessel into the Arctic and lost it: three winters beset on the east coast of Boothia and a fourth in a hut at Fury Beach, four years and five months away. James Clark Ross fixed the North Magnetic Pole by observation on 1 June 1831, the first magnetic pole of the Earth ever reached. The crew lived because the Netsilingmiut of Boothia fed, clothed, guided and charted for them for three years - and because Parry's wrecked Fury had left her stores on a beach 200 miles north. Twenty of twenty-three came home, in the whaler Isabella, the ship John Ross himself had commanded in 1818.")
