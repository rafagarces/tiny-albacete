"""Checks that sparse source coverage never includes the missing corner."""
import json
import numpy as np
from pathlib import Path
from coverage_geometry import source_coverage
catalog=json.load(open(Path(__file__).resolve().parents[2]/'ilustrado/tiles.json'))
actual=source_coverage(catalog,np.array([500000,4000000]));bounds=catalog['bounds'];rect={'tiles':[{'x':bounds['minX'],'y':bounds['minY'],'width':bounds['maxX']-bounds['minX'],'height':bounds['maxY']-bounds['minY']}]};envelope=source_coverage(rect,np.array([500000,4000000]));assert actual.is_valid and actual.geom_type=='Polygon'and not actual.interiors
assert abs(actual.area/envelope.area-555/560)<1e-10
old={'tiles':[t for t in catalog['tiles']if t['id']!='right16']};previous=source_coverage(old,np.array([500000,4000000]));assert previous.difference(actual).area<.0001
assert abs((actual.area-previous.area)/envelope.area-11/560)<1e-10
print('coverage: no holes, no previous loss, missing5cells not counted,11cells added')
