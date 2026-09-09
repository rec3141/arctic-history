#!/usr/bin/python3
"""look.py <index.json> <printed pages, comma sep>  -> pdf page for each"""
import json, sys
d = json.load(open(sys.argv[1]))
p2p = {int(k): v for k, v in d["printed2pdf"].items()}
obs = {int(k): v for k, v in d["obs"].items()}
for pr in sys.argv[2].split(","):
    pr = pr.strip()
    if not pr: continue
    n = int(pr)
    if n in p2p:
        print(f"{n}\t{p2p[n]}\texact")
    else:
        best = min(obs, key=lambda k: abs(obs[k] - n))
        print(f"{n}\t{best + (n - obs[best])}\tinterp(p.{obs[best]})")
