"""Check source-union area, gaps and preservation independently of atlas bounds."""
import json
import numpy as np
from pathlib import Path
from coverage_geometry import source_coverage
catalog=json.load(open(Path(__file__).resolve().parents[2]/'ilustrado/tiles.json'))
origin=np.array([500000,4000000]);actual=source_coverage(catalog,origin);bounds=catalog['bounds'];rect={'tiles':[{'x':bounds['minX'],'y':bounds['minY'],'width':bounds['maxX']-bounds['minX'],'height':bounds['maxY']-bounds['minY']}]};envelope=source_coverage(rect,origin)
def cells(tiles):
 out=set()
 for t in tiles:
  q=[round(t[k]*4)for k in ['x','y','width','height']]
  assert all(abs(t[k]*4-v)<1e-8 for k,v in zip(['x','y','width','height'],q))
  x,y,w,h=q;out.update((i,j)for i in range(x,x+w)for j in range(y,y+h))
 return out
newcells=cells(catalog['tiles']);boundingcells=cells(rect['tiles']);previous_catalog={'tiles':catalog['tiles'][:-1]};oldcells=cells(previous_catalog['tiles']);previous=source_coverage(previous_catalog,origin)
assert actual.is_valid and actual.geom_type=='Polygon'and not actual.interiors
assert abs(actual.area/envelope.area-len(newcells)/len(boundingcells))<1e-10
assert previous.difference(actual).area<.0001
assert abs((actual.area-previous.area)/envelope.area-len(newcells-oldcells)/len(boundingcells))<1e-10
print('coverage: no holes or loss;',len(newcells),'real cells;',len(boundingcells-newcells),'exterior cells not counted;',len(newcells-oldcells),'new cells')
