import json,sys,math,numpy as np
from pathlib import Path
from shapely.geometry import shape,mapping,Polygon
from shapely.ops import unary_union,transform
from pyproj import Transformer
from PIL import Image,ImageDraw
r=Path('/tmp/fiel-albacete');out=r/'art-release/ilustrado';raw=json.loads(json.loads(Path('/tmp/albacete-barrios-live.json').read_text())['content']);clean=json.load(open(r/'coverage-research/barrios-official.geojson'));tr=Transformer.from_crs(4326,25830,always_xy=True).transform;hp=unary_union([transform(tr,shape(f['geometry']))for f in clean['features']]);hist=shape(json.load(open(r/'coverage-research/barrios2016-outer-manual.geojson'))['geometry']);siu=unary_union([shape(f['geometry'])for f in json.load(open(r/'albacete-siu-urban.geojson'))['features']]);main=max(siu.geoms,key=lambda p:p.area);u=hp.union(main)
sys.path.insert(0,str(r/'art-layout-build/src'));from parse_bu import E0,N0
A=np.array([[-math.sin(math.radians(-154)),math.cos(math.radians(-154))],[math.sin(.6)*math.cos(math.radians(-154)),math.sin(.6)*math.sin(math.radians(-154))]]);focus=np.array([-123.2408167310922,-243.6981380554508]);m=472/2048
def cell(c,row):return Polygon([np.linalg.solve(A,[(x-1536)*m,(y-1024)*m-9])+focus+[E0,N0]for x,y in [(c*512,row*512),((c+1)*512,row*512),((c+1)*512,(row+1)*512),(c*512,(row+1)*512)]])
b=json.load(open(out/'tiles.json'))['bounds'];art=unary_union([cell(c,row)for c in range(round(b['minX']*4),round(b['maxX']*4))for row in range(round(b['minY']*4),round(b['maxY']*4))]);cells=[]
for row in range(-35,36):
 for c in range(-35,36):
  p=cell(c,row);area=p.intersection(u).area
  if area>1:cells.append({'column':c,'row':row,'id':f'c{c}r{row}','candidate_fraction':round(area/p.area,6),'art_status':'published'if p.difference(art).area<1 else 'not-started'})
props={'status':'official-neighborhood-union-principal-SIU-candidate-not-final-city-mask','crs':'EPSG:25830','method':'Union of25live municipal neighborhood vector polygons and largest SIU urban planning component. Replaces the manual outer approximation for this candidate, retaining the earlier trace only as an audit artifact.','neighborhoods_source_url':raw['url'],'neighborhoods_boundary_approval':'2016-06-29, as stated in live municipal viewer','retrieved':'2026-11-16','official_neighborhoods_km2':hp.area/1e6,'union_km2':u.area/1e6,'manual_trace_symmetric_difference_km2':hp.symmetric_difference(hist).area/1e6,'limitations':['An administrative boundary and planning classes, not a2026built-edge survey.','Some source rows carry2022-2023record dates; these do not establish source imagery freshness.','External industrial sectors and separate settlements remain explicitly unresolved, not silently excluded.','Current facade/reference review remains pending.']}
(out/'principal-extent-candidate.geojson').write_text(json.dumps({'type':'Feature','properties':props,'geometry':mapping(u)},indent=2));(out/'neighborhoods-official.geojson').write_text(json.dumps(clean,indent=2))
rows=[]
for f in clean['features']:
 p=transform(tr,shape(f['geometry']));rows.append({'name':f['properties']['name'],'source_id':f['properties']['source_id'],'administrative_area_km2':p.area/1e6,'published_ground_envelope_intersection_km2':p.intersection(art).area/1e6,'meaning':'ground-plane envelope only, not verified artwork/facades or a completion percentage'})
eraw=json.loads(json.loads(Path('/tmp/albacete-entidades-live.json').read_text())['content']);entities=[{**f['properties'],'status':'scope-unresolved-not-completed-not-excluded','note':'Administrative statistical entity; its polygon is not a built-up footprint.'}for f in eraw['data']['features']]
p=out/'coverage-ledger.json';d=json.load(open(p));d['expanded_principal_candidate']={**props,'cells_count':len(cells),'cells':cells,'completion_percentage':None};d['official_neighborhood_inventory']={'source_url':raw['url'],'features_count':25,'rows':rows};d['singular_entity_inventory']={'source_url':eraw['url'],'features_count':len(entities),'rows':entities};
for x in d['neighborhood_inventory']:
 x['boundary_status']='official vector geometry retrieved; see official_neighborhood_inventory';x['coverage_status']='ground envelope measured; artwork/facade completion not certified'
d['limitations']=[x.replace('PNOAdateJuly2024was checked at one point only, not across the city.','PNOA July2024 checked at five sample points only, not every pixel or current2026facades.')for x in d['limitations']]
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
im=Image.open('/downloads/albacete-pnoa-territory.jpg').convert('RGB');draw=ImageDraw.Draw(im)
def xy(c):return [(round((e-594500)/6500*1600),round((4320500-n)/6500*1600))for e,n in c]
for p in siu.geoms:draw.line(xy(p.exterior.coords),fill='#c747ed',width=2)
for f in clean['features']:
 p=transform(tr,shape(f['geometry']));parts=[p]if p.geom_type=='Polygon'else p.geoms
 for q in parts:draw.line(xy(q.exterior.coords),fill='#00ffff',width=2)
for p in [art]if art.geom_type=='Polygon'else art.geoms:draw.line(xy(p.exterior.coords),fill='#ffff00',width=4)
draw.rectangle((8,8,1050,66),fill='white');draw.text((18,17),'CYAN: 25 official neighborhoods, approval2016. MAGENTA: SIU planning. YELLOW: atlas envelope.',fill='black');draw.text((18,38),'Background PNOA July2024 at5samplepoints. Candidate only, not a2026built-edge survey.',fill='black');im.save('/downloads/territorial-official-neighborhoods.png');print('official',hp.area/1e6,'union',u.area/1e6,'manual_symdiff',hp.symmetric_difference(hist).area/1e6,'cells',len(cells),'neighborhoods intersected',sum(x['published_ground_envelope_intersection_km2']>0 for x in rows))
