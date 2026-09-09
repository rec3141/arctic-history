import sys, json
sys.path.insert(0,'/data/dev/arctic-history/ross-victory-scratch')
from upd import upd, get
from updev import evupd
S=(70.0167,-91.90)
w=json.loads(get('ross-victory-002')['waypoints'])
w[0]['note']="leaves the Victory at Sheriff's Harbour with a small sledge party, John Ross's party in company as far as the western sea"
upd('ross-victory-002', waypoints=json.dumps(w,ensure_ascii=False))
evupd(308, detail="James Clark Ross's party left the ship at Sheriff's Harbour - not at Victoria Harbour, which the Victory did not reach until the end of that August - accompanied part of the way by John Ross's own party, which turned back at the western sea. A winter of magnetic observations at Sheriff's Harbour had given a dip above 89 degrees and a calculated position for the pole; the journey was made for that purpose alone. John Ross names the party as consisting chiefly of the mates Thomas Blanky and Thomas Abernethy under his nephew's orders, and does not give its number; by the morning of the 28th four of them were snow-blind.")
