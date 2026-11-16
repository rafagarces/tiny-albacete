from PIL import Image
from pathlib import Path
import numpy as np,json,math,hashlib
r=Path(__file__).resolve().parents[2]/'ilustrado';d=json.load(open(r/'tiles.json'));b=d['bounds'];W=round((b['maxX']-b['minX'])*2048);H=round((b['maxY']-b['minY'])*2048);full=Image.new('RGB',(W,H))
for t in d['tiles']:full.paste(Image.open(r/t['url']).convert('RGB'),(round((t['x']-b['minX'])*2048),round((t['y']-b['minY'])*2048)))
for name,ref in [('atlas',full),('comparison',Image.open(r/d['comparison']['url']).convert('RGB'))]:
 maxL=math.ceil(math.log2(max(ref.size)));out=Image.new('RGB',ref.size)
 for y in range(math.ceil(H/512)):
  for x in range(math.ceil(W/512)):
   im=Image.open(r/(name+'_files')/str(maxL)/f'{x}_{y}.webp');ox=1 if x else 0;oy=1 if y else 0;out.paste(im.crop((ox,oy,ox+min(512,W-x*512),oy+min(512,H-y*512))),(x*512,y*512))
 assert np.array_equal(np.array(out),np.array(ref)),name;print(name,'top-level exact pixel identity')
