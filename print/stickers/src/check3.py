
import sys,json,glob,itertools,numpy as np,zxingcpp,os
from PIL import Image
import pypdfium2 as p
from scipy import ndimage as nd
O=sys.argv[1];U='https://megazine.org/?ref=sticker'
grid=list(itertools.product((300,200,150),(.8,1.6),(0,5,-9)))
for tag,dd,suf in (('bw',O,''),('col',O+'/color','-color')):
    low=[];n=0
    for j in sorted(glob.glob(O+'/*.json')):
        nm=os.path.basename(j)[:-5];pg=p.PdfDocument(f'{dd}/{nm}{suf}.pdf')[0].render(scale=300/72).to_pil().convert('L')
        for i,(x,y,cw,ch) in enumerate(json.load(open(j))):
            t=pg.crop((int(x*300),int(y*300),int((x+cw)*300),int((y+ch)*300)));ok=0;n+=1
            for dpi,bl,rot in grid:
                s=t.rotate(rot,fillcolor=255,expand=True);s=s.resize((int(s.width*dpi/300),int(s.height*dpi/300)),Image.LANCZOS)
                a=nd.gaussian_filter(np.asarray(s,dtype=float),bl)
                ok+=any(q.text==U for q in zxingcpp.read_barcodes(Image.fromarray(a.astype('uint8'))))
            if ok<len(grid): low.append((nm[9:],i+1,ok))
    print(tag,n,'stickers; below',len(grid),':',low)
