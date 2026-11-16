from pathlib import Path
import osmium,json,collections
from shapely.geometry import LineString,box
r=Path('/tmp/fiel-albacete');bbox=box(-1.95,38.93,-1.75,39.09)
class H(osmium.SimpleHandler):
 def __init__(self):super().__init__();self.rows=[];self.rels=[];self.n=0
 def way(self,w):
  self.n+=1;t=dict(w.tags)
  if not(t.get('highway') or t.get('leisure')in ['park','garden','nature_reserve','sports_centre'] or t.get('landuse')in ['grass','forest','industrial','recreation_ground','residential']):return
  try:g=[{'lat':n.lat,'lon':n.lon}for n in w.nodes]
  except osmium.InvalidLocationError:return
  if len(g)<2 or not LineString([(p['lon'],p['lat'])for p in g]).intersects(bbox):return
  self.rows.append({'type':'way','id':str(w.id),'tags':t,'geometry':g,'version':w.version,'timestamp':str(w.timestamp)})
 def relation(self,rel):
  t=dict(rel.tags)
  if any(s in t.get('name','').lower() for s in ['pulgosa','botánico','campollano','romica']):self.rels.append({'id':rel.id,'tags':t,'members':[{'type':m.type,'ref':m.ref,'role':m.role}for m in rel.members]})
h=H();h.apply_file(str(r/'castilla-la-mancha-latest.osm.pbf'),locations=True);print('scannedways',h.n,'rows',len(h.rows),'relations',h.rels);(r/'geofabrik-albacete-source.json').write_text(json.dumps({'elements':h.rows,'relations':h.rels,'source':json.load(open(r/'geofabrik-source.json')),'selection_bbox':[-1.95,38.93,-1.75,39.09]},separators=(',',':')))
for p in h.rows:
 if any(s in p['tags'].get('name','').lower()for s in ['pulgosa','botánico']):print('MATCH',p['id'],p['tags'])
