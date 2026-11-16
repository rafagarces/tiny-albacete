#!/usr/bin/env python3
"""Append one spatial source tile. No deployment or generation. Requires Pillow, numpy, pyproj."""
import argparse,json,hashlib,gzip,shutil,math,re,sys
from pathlib import Path
from PIL import Image
import numpy as np
from pyproj import Transformer
p=argparse.ArgumentParser();p.add_argument('--id',required=True);p.add_argument('--x',type=float,required=True);p.add_argument('--y',type=float,required=True);p.add_argument('--width',type=float,required=True);p.add_argument('--height',type=float,required=True);p.add_argument('--base',required=True);p.add_argument('--build',required=True);p.add_argument('--osm-addition',required=True);p.add_argument('--note',required=True);a=p.parse_args()
r=Path(__file__).resolve().parents[2];ill=r/'ilustrado';build=Path(a.build);cat=json.loads((ill/'tiles.json').read_text());assert a.id not in [t['id']for t in cat['tiles']]
tile={'id':a.id,'url':a.id+'.webp','x':a.x,'y':a.y,'width':a.width,'height':a.height};assert Image.open(ill/tile['url']).size==(round(a.width*2048),round(a.height*2048))
cat['tiles'].append(tile);cat['asset_revision']=hashlib.sha256(b''.join((ill/t['url']).read_bytes()for t in cat['tiles'])).hexdigest()[:16];b=cat['bounds'];b.update(minX=min(b['minX'],a.x),minY=min(b['minY'],a.y),maxX=max(b['maxX'],a.x+a.width),maxY=max(b['maxY'],a.y+a.height));W=round((b['maxX']-b['minX'])*2048);H=round((b['maxY']-b['minY'])*2048)
assert Image.open(a.base).size==(W,H)
# Validate proposed coverage before writing metadata.
area=0
for i,t in enumerate(cat['tiles']):
 area+=t['width']*t['height']
 for u in cat['tiles'][:i]:assert min(t['x']+t['width'],u['x']+u['width'])<=max(t['x'],u['x'])or min(t['y']+t['height'],u['y']+u['height'])<=max(t['y'],u['y'])
assert abs(area-(b['maxX']-b['minX'])*(b['maxY']-b['minY']))<1e-8
base='base-'+a.id+'.webp';Image.open(a.base).convert('RGB').save(ill/base,quality=88,method=6);cat['comparison'].update(url=base,x=b['minX'],y=b['minY'],width=b['maxX']-b['minX'],height=b['maxY']-b['minY']);cat['display'].update(x=b['minX'],y=b['minY'],width=b['maxX']-b['minX'],height=b['maxY']-b['minY']);(ill/'tiles.json').write_text(json.dumps(cat,indent=2)+'\n')
p=ill/'art.js';s=p.read_text();i=s.index('const fallback=');j=s.index('\nlet atlas=',i);p.write_text(s[:i]+'const fallback='+json.dumps(cat,separators=(',',':'))+';'+s[j:]);p=ill/'asset-manifest.json';m=json.loads(p.read_text());m['atlas'].update(width=W,height=H,world_bounds=[b['minX'],b['minY'],b['maxX'],b['maxY']])
for n in[tile['url'],base]:
 raw=(ill/n).read_bytes();m['files'].append({'name':n,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
p.write_text(json.dumps(m,indent=2)+'\n');p=ill/'sources.html';s=p.read_text();s=re.sub(r'(?:Trece|Catorce|Quince|Diecisé?s|\d+) imágenes WebP locales \([^<]+?\) y una captura',str(len(cat['tiles'])+1)+' imágenes WebP locales ('+str(len(cat['tiles']))+' fragmentos fuente del entorno y una vista de detalle separada) y una captura',s);s=re.sub(r'El atlas actual mide \d+ × \d+ píxeles',f'El atlas actual mide {W} × {H} píxeles',s);p.write_text(s)
arc=r/'tools/illustrated-base-2026-11-16'
for n in['build_zone.py','parse_bu.py']:shutil.copyfile(build/'src'/n,arc/n)
for src,dst in[('data/zone-building-parts.json','zone-building-parts.json.gz'),('zona-catedral/osm-source.json','osm-source.json.gz')]:
 with gzip.open(arc/dst,'wb',compresslevel=9)as f:f.write((build/src).read_bytes())
shutil.copyfile(a.osm_addition,arc/(a.id+'-osm-addition.json'));stats=json.loads((build/'zona-catedral/stats.json').read_text());records=len(json.loads((build/'data/zone-building-parts.json').read_text()));sourcecount=len(json.loads((build/'zona-catedral/osm-source.json').read_text())['elements'])
p=arc/'README.md';p.write_text(p.read_text()+f'\n\n## {a.id}\n\n{W}x{H}px, bounds{m["atlas"]["world_bounds"]}. Source records{records}, renderedparts{stats["buildingParts"]}, roadways{stats["roads"]}, faces{stats["faces"]}, OSMelements{sourcecount}. {a.note}\n')
sys.path.insert(0,str(build/'src'));from parse_bu import E0,N0
ang=math.radians(-154);A=np.array([[-math.sin(ang),math.cos(ang)],[math.sin(.6)*math.cos(ang),math.sin(.6)*math.sin(ang)]]);focus=np.array([-123.2408167310922,-243.6981380554508]);to=Transformer.from_crs(25830,4326,always_xy=True);corn=[]
for x,y in[(b['minX'],b['minY']),(b['maxX'],b['minY']),(b['maxX'],b['maxY']),(b['minX'],b['maxY']),(b['minX'],b['minY'])]:
 xy=np.linalg.solve(A,[(x*2048-1536)*472/2048,(y*2048-1024)*472/2048-9])+focus;corn.append(list(to.transform(E0+xy[0],N0+xy[1])))
p=ill/'coverage.geojson';c=json.loads(p.read_text());c['geometry']['coordinates']=[corn];area=W*H*(472/2048)**2/math.sin(.6)/1e6;c['properties']['area_km2']=area;p.write_text(json.dumps(c,indent=2)+'\n');p=r/'DECISIONS.md';p.write_text(p.read_text()+f'\n\n## 2026-11-16 {a.id}\n\nAppend tile at({a.x},{a.y}),size({a.width},{a.height}),total{W}x{H},approx{area:.3f}km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. {a.note}\n');p=r/'tools/illustrated-atlas/README.md';s=p.read_text();s=re.sub(r'approximately[\d.]+km2',f'approximately{area:.3f}km2',s);s=re.sub(r'\d+published cells',f'{round(W/512)*round(H/512)}published cells',s);level=math.ceil(math.log2(max(W,H)));count=sum(math.ceil(math.ceil(W/2**(level-l))/512)*math.ceil(math.ceil(H/2**(level-l))/512) for l in range(level+1));s=re.sub(r'\d+display tiles',f'{count}display tiles',s);p.write_text(s);print('appended',a.id,'atlas',W,H,'envelope',area,'displaytiles',count)
