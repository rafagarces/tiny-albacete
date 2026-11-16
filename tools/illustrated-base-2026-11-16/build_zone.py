"""Build a bounded, original, attributed mesh from local Catastro/OSM and Cathedral pilot.
Context heights are estimates, with explicitly marked historical roof references.
Landmark meshes retain their own documented-vs-estimated feature provenance.
"""
import sys,json,math
from pathlib import Path
from shapely.geometry import Polygon,box
from shapely import constrained_delaunay_triangles
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'src'));import catparse
from local_frame import to_local
out=[]
def face(v,c,kind='context-estimated'):
 out.append({'v':v,'c':c,'kind':kind})
def flat(pts,z,col,kind='context-estimated',holes=None):
 p=Polygon(pts,holes)
 if not p.is_valid:p=p.buffer(0)
 if kind.startswith('osm'):p=p.intersection(box(-1060,-1090,630,510))
 if p.geom_type not in ('Polygon','MultiPolygon'):return
 # Constrain edges to polygon, including concave recesses and holes.
 # Centroid-filtered unconstrained triangles can bridge outside the footprint.
 for t in constrained_delaunay_triangles(p).geoms:
  face([[x,y,z]for x,y in list(t.exterior.coords)[:3]],col,kind)
# Bounded ground, street positions from OSM. No invented named features.
flat([[-1080,-1110],[650,-1110],[650,530],[-1080,530]],-.15,'#dce1d5','presentation-base')
osm=json.load(open(ROOT/'zona-catedral/osm-source.json'))
roads=0
for el in osm.get('elements',[]):
 tags=el.get('tags',{});g=el.get('geometry',[])
 if len(g)<2:continue
 pts=[to_local(p['lat'],p['lon'])for p in g]
 if tags.get('highway'):
  width={'primary':11,'secondary':9,'tertiary':8,'residential':6,'service':4,'pedestrian':6,'footway':2,'steps':2}.get(tags['highway'],5)
  col='#c8c5bb' if tags['highway'] in ['pedestrian','footway','steps'] else '#b0b3a9'
  for (x,y),(X,Y) in zip(pts,pts[1:]):
   L=math.hypot(X-x,Y-y)
   if not L:continue
   dx=-(Y-y)/L*(width/2+.7);dy=(X-x)/L*(width/2+.7)
   flat([(x+dx,y+dy),(X+dx,Y+dy),(X-dx,Y-dy),(x-dx,y-dy)],.01,'#e6e4d8','osm-road-width-estimated')
   dx*=width/(width+1.4);dy*=width/(width+1.4)
   flat([(x+dx,y+dy),(X+dx,Y+dy),(X-dx,Y-dy),(x-dx,y-dy)],.025,col,'osm-road-width-estimated')
  roads+=1
 elif len(pts)>3:flat(pts,.02,'#b8c6a2','osm-green')
parts=json.load(open(ROOT/'data/zone-building-parts.json'));count=0
palette=['#d6c9b1','#c9bea7','#d9cbb8','#c2baa8','#dfd4bd','#cbbbaa']
for b in parts:
 if b['id'].startswith(('9271101WJ9197A','9272019WJ9197S')):continue
 if b['id'] in ['9472601WJ9197A_part8','9472601WJ9197A_part9']:continue
 pts=b['pts'];cx=sum(p[0]for p in pts)/len(pts);cy=sum(p[1]for p in pts)/len(pts)
 if cx < -1050 or cx > 620 or cy < -1080 or cy > 500 or b['area']<18:continue
 col=palette[int(catparse.h01(b['id'])*len(palette))%len(palette)]
 h=min(50,max(3,b['floors']*3+2)) if b['floors']>0 else 9
 if b['id']=='9470007WJ9197A_part6':
  h=18.6
  pts=[q for p in pts for q in ([(176.1,-125.9),(171.6,-126.5)] if p==[173.6,-124.5] else [p])]
 if b['id'] in ['8971009WJ9187B_part2','8971009WJ9187B_part7','8971009WJ9187B_part4']:h=8.7
 # Front coarse mass adjusted to match documented facade proportions; still estimated.
 if b['id']=='9371110WJ9197A_part4':h=11.2
 if b['id'] in ['9472604WJ9197S_part5','9472604WJ9197S_part6','9472604WJ9197S_part7']:h=12.0
 if b['id']=='9472601WJ9197A_part12':h=12.0 # 2017 annular-roof median, not another cone.
 if b['id']=='9472601WJ9197A_part6':
  # Robust cone fitted to274PNOA2017 roof returns; not a current survey.
  # No fan across the non-star-shaped annular part12.
  def roofheight(p):return 21.2-.505*math.hypot(p[0]-163.45,p[1]-52.30)
  for a,B in zip(pts,pts[1:]+pts[:1]):
   if a!=B:
    ha,hb=roofheight(a),roofheight(B)
    face([[*a,ha],[*B,hb],[163.45,52.30,21.2]],'#9a9f89','pnoa2017-cone-fit')
    face([[*a,0],[*B,0],[*B,hb],[*a,ha]],col,'pnoa2017-roof-reference')
 else:
  flat(pts,h,'#c6b5a0',holes=b.get('holes'))
  for ring in [pts]+b.get('holes',[]):
   for a,B in zip(ring,ring[1:]+ring[:1]):
    if a==B:continue
    face([[*a,0],[*B,0],[*B,h],[*a,h]],col)
 # No invented windows/balconies/chimneys. Restrained cornice as artistic edge.
 count+=1
# Replace ALL cadastral Cathedral parts, not a duplicate overlay. Approximate registration.
ang=math.radians(-24);ca,sa=math.cos(ang),math.sin(ang)
for f in json.load(open(ROOT/'pilots/catedral-3d/model.json')):
 v=[[ca*x-sa*y-13.1,sa*x+ca*y+6.7,z]for x,y,z in f['v']]
 face(v,f['c'],f['kind'])
# CasaHortelano registered to cadastral front edge(-70.3,59.7)->(-54.6,62.4).
ang=math.atan2(2.7,15.7);ca,sa=math.cos(ang),math.sin(ang)
for f in json.load(open(ROOT/'pilots/hortelano-3d/model.json')):
 face([[ca*x-sa*y-70.3,sa*x+ca*y+59.7,z]for x,y,z in f['v']],f['c'],f['kind'])
# Antiguo Ayuntamiento front registered to cadastral edge; rear masses retained.
ang=math.atan2(-9.8,17.6);ca,sa=math.cos(ang),math.sin(ang)
for f in json.load(open(ROOT/'pilots/ayuntamiento-3d/model.json')):
 face([[ca*x-sa*y+161.2,sa*x+ca*y-60.6,z]for x,y,z in f['v']],f['c'],f['kind'])
# Modern Teatro Circo facade along Catastro front edge, not fictitious historical facade.
ang=math.atan2(-17.9,30.4);ca,sa=math.cos(ang),math.sin(ang)
for f in json.load(open(ROOT/'pilots/teatro-3d/model.json')):
 face([[ca*x-sa*y+130.7,sa*x+ca*y+31.7,z]for x,y,z in f['v']],f['c'],f['kind'])
# Palacio Provincial street facade; cadastral rear and courtyard retained.
ang=math.atan2(27.9,14.3);ca,sa=math.cos(ang),math.sin(ang)
for f in json.load(open(ROOT/'pilots/diputacion-3d/model.json')):
 face([[ca*x-sa*y+203.1,sa*x+ca*y-4.3,z]for x,y,z in f['v']],f['c'],f['kind'])
# Casa Perona north front and east return, registered to Catastro.
ang=math.atan2(.1,-24);ca,sa=math.cos(ang),math.sin(ang)
for f in json.load(open(ROOT/'pilots/perona-3d/model.json')):
 face([[ca*x-sa*y-239.5,sa*x+ca*y+11.2,z]for x,y,z in f['v']],f['c'],f['kind'])
# Gran Hotel uses global EN positions registered against its cadastral street edges.
for f in json.load(open(ROOT/'pilots/granhotel-3d/model.json')):face(f['v'],f['c'],f['kind'])
(ROOT/'zona-catedral/model.json').write_text(json.dumps(out,separators=(',',':')))
(ROOT/'zona-catedral/stats.json').write_text(json.dumps({'buildingParts':count,'roads':roads,'faces':len(out),'extentMeters':1670,'generated':'2026-11-16','cathedralRegistration':'approximate rotation-24deg, offset(-13.1,6.7)m; not a surveyed alignment'}))
print(count,'parts',roads,'roads',len(out),'faces')
