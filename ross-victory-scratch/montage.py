import sys, numpy as np
from PIL import Image, ImageDraw
files=sys.argv[2:]
rows=[]
for f in files:
    im=Image.open(f).convert('L')
    a=np.asarray(im).astype(np.float32)
    h,w=a.shape
    # try bottom band and right band; pick the one with more dark text pixels in a thin strip
    bot=a[int(h*0.60):int(h*0.80),:]
    rt=a[:,int(h*0.0):0] if False else a[:,int(w*0.72):int(w*0.90)]
    def score(x): return (x<200).mean()
    if score(rt)>score(bot):
        band=np.rot90(a[:,int(w*0.68):w],3)
    else:
        band=a[int(h*0.58):int(h*0.85),:]
    lo,hi=np.percentile(band,[1,55])
    b=np.clip((band-lo)/(max(hi-lo,1))*255,0,255).astype(np.uint8)
    img=Image.fromarray(b)
    # scale to width 1400
    sc=1400/img.width
    img=img.resize((1400,max(1,int(img.height*sc))),Image.LANCZOS)
    lab=Image.new('L',(1400,26),255); d=ImageDraw.Draw(lab); d.text((4,6),f.split('/')[-1],fill=0)
    rows.append(lab); rows.append(img)
H=sum(r.height for r in rows)
out=Image.new('L',(1400,H),255); y=0
for r in rows: out.paste(r,(0,y)); y+=r.height
out.save(sys.argv[1]); print(out.size)
