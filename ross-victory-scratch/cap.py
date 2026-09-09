import sys
from PIL import Image, ImageOps, ImageEnhance
src=sys.argv[1]; out=sys.argv[2]
im=Image.open(src).convert('L')
w,h=im.size
# caption band on the right side (vertical text), crop right 18%
band=im.crop((int(w*0.78),0,w,h))
band=band.rotate(-90,expand=True)
band=ImageOps.autocontrast(band)
band=band.resize((band.width*2,band.height*2),Image.LANCZOS)
band.save(out)
print(band.size)
