"""Refresh derived source-union measurements after inventory imports and scope notices.
Source geometry dates stay unchanged. Intersection is not artwork/currentness verification.
"""
from pathlib import Path
import json,sys,numpy as np
from shapely.geometry import shape,Point
from shapely.ops import transform
from pyproj import Transformer
r=Path('/tmp/fiel-albacete');o=r/'art-release';ill=o/'ilustrado';sys.path.insert(0,str(o/'tools/illustrated-atlas'));from coverage_geometry import source_coverage
sys.path.insert(0,str(r/'art-layout-build/src'));from parse_bu import E0,N0
cat=json.load(open(ill/'tiles.json'));art=source_coverage(cat,np.array([E0,N0]));to=Transformer.from_crs(4326,25830,always_xy=True).transform;d=json.load(open(ill/'coverage-ledger.json'));rev=cat['asset_revision'];stamp={'measurement_basis':'actual current source-rectangle union, not atlas bounds or source-era extent','measurement_revision':rev,'measurement_date':'2026-11-17','meaning':'geometry overlap only, not verified architecture, current facade or completion'}
for row in d.get('southern_science_botanic_inventory',{}).get('rows',[]):
 pt=row['point'];p=Point(to(pt['lng'],pt['lat']));row['in_art_ground_envelope']=art.covers(p);row['point_distance_to_art_m']=art.distance(p);row.update(stamp);row['geometry_status']='Point alone does not certify whole-site coverage. See current polygon overlap where available.'
row=d.get('southern_pulgosa_inventory',{})
if row:
 p=Point(to(*row['point_lonlat']));row['point_in_art']=art.covers(p);row['point_distance_to_art_m']=art.distance(p);row.update(stamp)
for name,key in [('exterior-park-candidates.geojson','exterior_park_geometry_candidates'),('exterior-industrial-candidates.geojson','exterior_industrial_geometry_inventory')]:
 p=ill/name;j=json.load(open(p));measure={}
 for f in j['features']:
  g=transform(to,shape(f['geometry']));a=g.intersection(art).area;pr=f['properties'];pr['published_source_union_intersection_km2']=a/1e6;pr['outside_source_union_km2']=g.difference(art).area/1e6;pr['distance_to_source_union_m']=g.distance(art);pr.update(stamp)
  if 'published_ground_envelope_intersection_km2'in pr:pr['published_ground_envelope_intersection_km2']=a/1e6
  measure[str(pr['osm_way'])]=pr
 for row in d.get(key,{}).get('rows',[]):
  fresh=measure.get(str(row['osm_way']))
  if fresh:row.update(fresh)
 p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
for row in d.get('official_neighborhood_inventory',{}).get('rows',[]):
 fs=[f for f in json.load(open(r/'coverage-research/barrios-official.geojson'))['features']if f['properties'].get('name')==row['name']]
 if fs:
  g=transform(to,shape(fs[0]['geometry']));row['published_ground_envelope_intersection_km2']=g.intersection(art).area/1e6;row['outside_source_union_km2']=g.difference(art).area/1e6;row.update(stamp)
d['inventory_measurement_refresh']=stamp
(ill/'coverage-ledger.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n');print('refreshed',rev)
for row in d['southern_science_botanic_inventory']['rows']:print(row['name'],row['in_art_ground_envelope'],row['point_distance_to_art_m'])
for row in d['exterior_park_geometry_candidates']['rows']:print(row['name'],row['published_source_union_intersection_km2'],row['outside_source_union_km2'],row['distance_to_source_union_m'])
