import json,sys,os
from PIL import Image,ImageDraw,ImageFilter
Image.MAX_IMAGE_PIXELS=None
docs=['The_Cliffs_at_Volcano_ball_lake','Habitats_conflict_copy_2','Where_the_valley_turns','Modular']
out=sys.argv[1]; os.makedirs(out,exist_ok=True)
items=[]
for s in docs:
    a=json.load(open(f'data/annotations/{s}.json'))
    im=Image.open(f'extracted/{s}/composite_full.png').convert('RGB')
    for i,o in enumerate(a['objects']):
        if o.get('type') not in ('creature',None,'figure','character') and 'creature' not in o['name']: continue
        ps=o.get('polys') or ([o['poly']] if o.get('poly') else [])
        ps=[p for p in ps if len(p)>2]
        if not ps: continue
        xs=[q[0] for p in ps for q in p]; ys=[q[1] for p in ps for q in p]
        x0,y0,x1,y1=min(xs),min(ys),max(xs),max(ys)
        if x1-x0<250 or y1-y0<250: continue
        pad=20; box=tuple(int(v) for v in (x0-pad,y0-pad,x1+pad,y1+pad))
        c=im.crop(box); m=Image.new('L',c.size,0); d=ImageDraw.Draw(m)
        for p in ps: d.polygon([(q[0]-box[0],q[1]-box[1]) for q in p],fill=255)
        m=m.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(1))
        c.putalpha(m); n=f'{s[:5]}_{i:02d}'; c.save(f'{out}/{n}.png'); items.append((n,o['name'],c))
S=190;W=11
rows=len(items)//W+1
sheet=Image.new('RGB',(W*S,rows*(S+14)),'white');d=ImageDraw.Draw(sheet)
for k,(n,nm,c) in enumerate(items):
    t=c.copy();t.thumbnail((S-8,S-8));x,y=(k%W)*S+4,(k//W)*(S+14)+2
    sheet.paste(t,(x,y),t);d.text((x,y+S-8),n,fill='black')
sheet.save(out+'_sheet.jpg',quality=85);print(len(items),sheet.size)
