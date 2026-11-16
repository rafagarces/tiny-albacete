#!/usr/bin/env python3
"""Check the published atlas catalog independently of the browser. Requires Pillow."""
from pathlib import Path
import json,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[2]/'ilustrado'
d=json.loads((R/'tiles.json').read_text());b=d['bounds'];tiles=d['tiles'];names=set();area=0
assert b['maxX']>b['minX'] and b['maxY']>b['minY']
for i,t in enumerate(tiles):
 assert t['id'] not in names;names.add(t['id'])
 assert t['width']>0 and t['height']>0
 assert b['minX']<=t['x'] and b['minY']<=t['y'] and t['x']+t['width']<=b['maxX'] and t['y']+t['height']<=b['maxY']
 with Image.open(R/t['url']) as im:assert im.size==(round(t['width']*2048),round(t['height']*2048)),t['id']
 area+=t['width']*t['height']
 for u in tiles[:i]:
  dx=min(t['x']+t['width'],u['x']+u['width'])-max(t['x'],u['x']);dy=min(t['y']+t['height'],u['y']+u['height'])-max(t['y'],u['y'])
  assert dx<=0 or dy<=0,('overlap',t['id'],u['id'])
assert abs(area-(b['maxX']-b['minX'])*(b['maxY']-b['minY']))<1e-9,'gap in rectangular published atlas'
for entry in json.loads((R/'asset-manifest.json').read_text())['files']:
 data=(R/entry['name']).read_bytes();assert len(data)==entry['bytes'];assert hashlib.sha256(data).hexdigest()==entry['sha256'],entry['name']
print(f'PASS: {len(tiles)} non-overlapping tiles; exact rectangular coverage; dimensions and asset hashes valid.')
