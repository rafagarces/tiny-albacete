"""Independent frame consistency and transformed footprint regression."""
import sys,json,hashlib
from pathlib import Path
import numpy as np
from pyproj import Transformer
from shapely.geometry import Polygon,Point
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from local_frame import to_local
from parse_bu import E0,N0
inverse=Transformer.from_crs(25830,4326,always_xy=True)
for x,y in [(0,0),(164.1,50.2),(180,-135),(-250,0)]:
 lon,lat=inverse.transform(E0+x,N0+y);a,b=to_local(lat,lon)
 assert abs(a-x)<1e-5 and abs(b-y)<1e-5,(x,y,a,b)
parts=json.loads((ROOT/'data/zone-building-parts.json').read_text())
p=Polygon(next(b['pts']for b in parts if b['id']=='9472601WJ9197A_part6'))
assert p.contains(Point(163.45,52.30))
samples=np.array(json.loads((ROOT/'pilots/teatro-3d/roof-samples-2017.json').read_text()))
assert len(samples)==274 and all(p.buffer(-.999).covers(Point(x,y))for x,y in samples[:,:2])
res=21.18969574-.5046525*np.hypot(samples[:,0]-163.45082123,samples[:,1]-52.29728775)-samples[:,2]
assert abs(np.median(abs(res))-.26748575)<1e-5
print('Shared-frame roundtrip and274roof sample checks passed')

assert sum(len(b.get('holes',[]))for b in parts)==119
assert sum(bool(b.get('holes'))for b in parts)==85
manifest=json.loads((ROOT/'data/source-manifest.json').read_text())
assert hashlib.sha256((ROOT/'data/zone-building-parts.json').read_bytes()).hexdigest()==manifest['normalizedInputSha256']
for b in parts:
 if b.get('holes'):assert Polygon(b['pts'],b['holes']).is_valid,b['id']
print('Source snapshot checksum and119interior rings passed')
