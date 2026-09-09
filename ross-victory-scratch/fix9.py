import sys, json, sqlite3
sys.path.insert(0,'/data/dev/arctic-history/ross-victory-scratch')
from upd import upd, get
F=(69.9783,-92.0183); S=(70.0167,-91.90); V=(70.155,-91.509)

# --- track 001: correct Felix and Sheriff positions
w=json.loads(get('ross-victory-001')['waypoints'])
for p in w:
    if p['date']=='1829-10-01': p['lat'],p['lon']=F
    if p['date']=='1830-09-17': p['lat'],p['lon']=(69.995,-92.00)
    if p['date']=='1830-10-31':
        p['lat'],p['lon']=S
        p['note']="Sheriff's Harbour, observed 70 deg 01 min N, 91 deg 54 min W: four miles gained in the whole of 1830, 850 feet of it cut by hand in October"
    if p['date']=='1831-08-29':
        p['note']='under sail for the last time; four miles north to the berth Ross named Victory, later Victoria, Harbour. The narrative and the magnetic table disagree over its latitude by nine minutes of arc'
upd('ross-victory-001', waypoints=json.dumps(w,ensure_ascii=False), lat=F[0], lon=F[1])

# --- track 002: the sledge journey began at SHERIFF'S Harbour, not Victoria Harbour
w=json.loads(get('ross-victory-002')['waypoints'])
w[0]={'date':'1831-05-27','lat':S[0],'lon':S[1],
      'note':"leaves the Victory at Sheriff's Harbour, a party of six, with John Ross's party in company as far as the western sea"}
for p in w:
    if p['date']=='1831-05-30': p['lon']=-95.8197
upd('ross-victory-002', lat=S[0], lon=S[1], waypoints=json.dumps(w,ensure_ascii=False),
    description="Five of the seven points are James Clark Ross's own observed positions, printed to the second in his narrative of the journey, which makes this one of the best-fixed sledge tracks of the period: the halts of 28, 29 and 30 May and the pole itself. The party left the ship at Sheriff's Harbour, where she had lain since October 1830; the Victory did not reach Victoria Harbour until the end of that August. The departure and the crossing of the Stanley river inlet on 27 May, and the camp of 31 May, are interpolated between the observed positions. The return to the ship is not drawn. The dip he recorded rose from 89 deg 41 min on 28 May to 89 deg 59 min at the pole, within one minute of vertical. The observed positions are: 28 May, 69 deg 34 min 45 sec N, 94 deg 54 min 23 sec W; 29 May, 69 deg 40 min 27 sec N, 95 deg 22 min 35 sec W; 30 May, 69 deg 46 min 25 sec N, 95 deg 49 min 11 sec W; 1 June, 70 deg 05 min 17 sec N, 96 deg 46 min 45 sec W. The summary magnetic table at the end of the same chapter prints the pole's longitude as 96 deg 45 min 48 sec, about half a mile east of the journal's figure; the journal's is used here.")

# --- track 003: Fury Beach start, and the abandonment position
w=json.loads(get('ross-victory-003')['waypoints'])
upd('ross-victory-003')
