import sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter
files=sys.argv[2:]
rows=[]
for f in files:
    im=Image.open(f).convert('L')
    a=np.asarray(im).astype(np.float32)
    h,w=a.shape
    dark=(a<215)
    colf=dark.mean(axis=0); rowf=dark.mean(axis=1)
    cols=np.where(colf>0.35)[0]; rws=np.where(rowf>0.35)[0]
    c0,c1,r0,r1=(cols[0],cols[-1],rws[0],rws[-1]) if len(cols) and len(rws) else (0,w-1,0,h-1)
    rband=a[r0:r1, c1:min(w,c1+int(0.20*w))]
    bband=a[r1:min(h,r1+int(0.14*h)), c0:c1]
    def sc(x): return (x<205).mean() if x.size else 0
    band = np.rot90(rband,3) if sc(rband)>sc(bband) else bband
    img=Image.fromarray(np.clip(band,0,255).astype(np.uint8))
    bg=img.filter(ImageFilter.GaussianBlur(12))
    d=np.asarray(img).astype(np.float32)-np.asarray(bg).astype(np.float32)
    d=np.clip(128+d*6,0,255).astype(np.uint8)
    img=Image.fromarray(d)
    scl=1500/img.width
    img=img.resize((1500,max(1,int(img.height*scl))),Image.LANCZOS)
    lab=Image.new('L',(1500,24),255); ImageDraw.Draw(lab).text((4,6),f.split('/')[-1],fill=0)
    rows.append(lab); rows.append(img)
H=sum(r.height for r in rows)
out=Image.new('L',(1500,H),255); y=0
for r in rows: out.paste(r,(0,y)); y+=r.height
out.save(sys.argv[1]); print(out.size)
