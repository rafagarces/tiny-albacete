from pathlib import Path
from PIL import Image
import json,math,hashlib
r=Path(__file__).resolve().parents[2]/'ilustrado';d=json.load(open(r/'tiles.json'));b=d['bounds'];U=2048;W=round((b['maxX']-b['minX'])*U);H=round((b['maxY']-b['minY'])*U)
def pyramid(name,im):
 w,h=im.size;levels=math.ceil(math.log2(max(w,h)));folder=r/(name+'_files');count=0
 for level in range(levels+1):
  f=2**(levels-level);sw=math.ceil(w/f);sh=math.ceil(h/f);small=im if f==1 else im.resize((sw,sh),Image.Resampling.LANCZOS);p=folder/str(level);p.mkdir(parents=True,exist_ok=True)
  for y in range(math.ceil(sh/512)):
   for x in range(math.ceil(sw/512)):
    tile=small.crop((max(0,x*512-1),max(0,y*512-1),min(sw,(x+1)*512+1),min(sh,(y+1)*512+1)));tile.save(p/f'{x}_{y}.webp',lossless=level==levels,quality=88,method=6);count+=1
 (r/(name+'.dzi')).write_text(f'<Image xmlns="http://schemas.microsoft.com/deepzoom/2008" Format="webp" Overlap="1" TileSize="512"><Size Width="{w}" Height="{h}"/></Image>\n');print(name,w,h,'files',count,'bytes',sum(p.stat().st_size for p in folder.rglob('*.webp')))
full=Image.new('RGB',(W,H))
for t in d['tiles']:full.paste(Image.open(r/t['url']).convert('RGB'),(round((t['x']-b['minX'])*U),round((t['y']-b['minY'])*U)))
pyramid('atlas',full);pyramid('comparison',Image.open(r/d['comparison']['url']).convert('RGB'))
