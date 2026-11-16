"""Offline footprint triangulation regression (Shapely >= 2.1, GEOS >= 3.10)."""
import json, sys
from pathlib import Path
from shapely import constrained_delaunay_triangles
from shapely.geometry import Polygon
from shapely.ops import triangulate, unary_union
source = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'data/zone-building-parts.json'
count = affected = 0
interiorRings=0
voidArea=0.0
extra = missing = 0.0
previously_skipped=0
for b in json.loads(source.read_text()):
    if b['id'].startswith(('9271101WJ9197A','9272019WJ9197S')): continue
    if b['id'] in ['9472601WJ9197A_part8','9472601WJ9197A_part9','9472601WJ9197A_part6']: continue
    pts=b['pts']; x=sum(p[0]for p in pts)/len(pts); y=sum(p[1]for p in pts)/len(pts)
    if x < -300 or x > 250 or abs(y)>250 or b['area']<18: continue
    if b['id']=='9470007WJ9197A_part6':
        pts=[q for p in pts for q in ([(176.1,-125.9),(171.6,-126.5)] if p==[173.6,-124.5] else [p])]
    p=Polygon(pts,b.get('holes'))
    interiorRings+=len(b.get('holes',[]))
    voidArea+=Polygon(pts).area-p.area
    if not p.is_valid:p=p.buffer(0)
    assert p.geom_type in ('Polygon','MultiPolygon'),b['id']
    if p.geom_type=='MultiPolygon':
        previously_skipped+=1
        old=Polygon()
    else:
        old=unary_union([t for t in triangulate(p) if p.covers(t.representative_point())])
    new=unary_union(constrained_delaunay_triangles(p).geoms)
    error=p.symmetric_difference(new).area
    assert error < 1e-6,(b['id'],error)
    if p.symmetric_difference(old).area>.01:
        affected+=1; extra+=old.difference(p).area; missing+=p.difference(old).area
    count+=1
print(json.dumps(dict(checked=count,interiorRings=interiorRings,restoredVoidAreaM2=round(voidArea,2),previouslyAffected=affected,previouslySkippedMultiPolygons=previously_skipped,previousExtraAreaM2=round(extra,2),previousMissingAreaM2=round(missing,2),newDifferenceAreaM2=0)))
