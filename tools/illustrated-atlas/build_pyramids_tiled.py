from pathlib import Path
from PIL import Image
import json,math,sys,functools,gc,numpy as np
Image.MAX_IMAGE_PIXELS=None
r=Path(__file__).resolve().parents[2]/'ilustrado';d=json.load(open(r/'tiles.json'));U=2048;b=d['bounds'];W=round((b['maxX']-b['minX'])*U);H=round((b['maxY']-b['minY'])*U);L=math.ceil(math.log2(max(W,H)));name=sys.argv[1];mode='RGBA'if name=='atlas'else'RGB';folder=r/(name+'_files')
@functools.lru_cache(maxsize=3)
def load(p):
 with Image.open(p)as im:return im.convert(mode)
rects=[(r/t['url'],round((t['x']-b['minX'])*U),round((t['y']-b['minY'])*U),round(t['width']*U),round(t['height']*U))for t in d['tiles']]
if name=='comparison':rects=[(r/d['comparison']['url'],0,0,W,H)]
mm_path=Path('/tmp')/('tiny-albacete-'+name+'-native.mmap')
channels=4 if mode=='RGBA'else 3
if len(sys.argv)>2 and sys.argv[2]=='init':
 mm=np.memmap(mm_path,dtype='uint8',mode='w+',shape=(H,W,channels));mm[:]=0
 for p,x,y,w,h in rects:
  with Image.open(p)as im:
   for yy in range(0,h,256):mm[y+yy:y+min(h,yy+256),x:x+w]=np.asarray(im.crop((0,yy,w,min(h,yy+256))).convert(mode))
 mm.flush();print('init',mm_path);sys.exit()
mm=np.memmap(mm_path,dtype='uint8',mode='r',shape=(H,W,channels))
def render_source(box):
 x0,y0,x1,y1=box;return Image.fromarray(np.array(mm[y0:y1,x0:x1]))
def bounds(tx,ty,w,h):return(max(0,tx*512-1),max(0,ty*512-1),min(w,(tx+1)*512+1),min(h,(ty+1)*512+1))
for lev in ([int(sys.argv[2])]if len(sys.argv)>2 else range(L,-1,-1)):
 w=math.ceil(W/2**(L-lev));h=math.ceil(H/2**(L-lev));out=folder/str(lev);out.mkdir(parents=True,exist_ok=True)
 for ty in (range(int(sys.argv[3]),int(sys.argv[4]))if len(sys.argv)>4 else range(math.ceil(h/512))):
  for tx in range(math.ceil(w/512)):
   box=bounds(tx,ty,w,h)
   if lev==L:tile=render_source(box)
   else:
    pw=math.ceil(W/2**(L-lev-1));ph=math.ceil(H/2**(L-lev-1));x0,y0,x1,y1=box
    # An even context margin isolates the Lanczos support from tile boundaries.
    sx0=max(0,x0*2-8);sy0=max(0,y0*2-8);sx1=min(pw,x1*2+8);sy1=min(ph,y1*2+8);patch=Image.new(mode,(sx1-sx0,sy1-sy0))
    for yy in range(sy0//512,math.ceil(sy1/512)):
     for xx in range(sx0//512,math.ceil(sx1/512)):
      pb=bounds(xx,yy,pw,ph);a=max(sx0,pb[0]);c=min(sx1,pb[2]);bb=max(sy0,pb[1]);e=min(sy1,pb[3]);p=load(folder/str(lev+1)/f'{xx}_{yy}.webp');patch.paste(p.crop((a-pb[0],bb-pb[1],c-pb[0],e-pb[1])),(a-sx0,bb-sy0))
    reduced=patch.resize((math.ceil(patch.width/2),math.ceil(patch.height/2)),Image.Resampling.LANCZOS);tile=reduced.crop((x0-sx0//2,y0-sy0//2,x1-sx0//2,y1-sy0//2))
   tile.save(out/f'{tx}_{ty}.webp',lossless=lev==L,quality=88,method=4)
 load.cache_clear();gc.collect();print(name,lev,w,h,flush=True)
(r/(name+'.dzi')).write_text(f'<Image xmlns="http://schemas.microsoft.com/deepzoom/2008" Format="webp" Overlap="1" TileSize="512"><Size Width="{W}" Height="{H}"/></Image>\n')
print('complete',name,W,H)
