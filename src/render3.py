#!/usr/bin/env python3
import json, math, os, sys, hashlib, collections
from PIL import Image, ImageDraw
import catparse

BASE='/tmp/tinyalba'
TS=1024
C=4.5                 # px per meter at TOP zoom
TOP=18
# urban crop (meters from cathedral)
MINE,MAXE,MINN,MAXN=-3100,3300,-2800,3200
LAT0,LON0=catparse.LAT0,catparse.LON0
h01=catparse.h01

def to_screen(e,n,z=0.0): return ((e+n)*C,(e-n)*0.5*C - z*C)

to_en=catparse.to_en
print('loading buildings (Catastro INSPIRE bulk 02900)...',flush=True)
def sane(b):
    xs=[p[0] for p in b['pts']]; ys=[p[1] for p in b['pts']]
    if max(xs)-min(xs)>300 or max(ys)-min(ys)>300: return False
    if b.get('area',100)<18: return False
    return True
_bu_parts=json.load(open('/tmp/tinyalba/bu_parts.json'))
_bu_blds=json.load(open('/tmp/tinyalba/bu_blds.json'))
use_map={b['id']:b['use'] for b in _bu_blds}
buildings=[]
for p in _bu_parts:
    if not any(MINE-80<e<MAXE+80 and MINN-80<n<MAXN+80 for e,n in p['pts']): continue
    fl=p['floors']
    h=fl*3.0+2.0 if fl>0 else 6.5+4.5*h01('h',p['id'])
    h=max(2.5,min(h,70))
    bid=p['id'].rsplit('_part',1)[0]
    b={'pts':p['pts'],'h':h,'use':use_map.get(bid,'1_residential'),'ref':p['id'],'area':p['area']}
    if sane(b): buildings.append(b)
print('buildings',len(buildings),'(catastro bulk, real floors)')

# landmark: Albacete cathedral is the (0,0)m origin - mark its footprint for special treatment
cath=None
for b in buildings:
    ce=sum(p[0] for p in b['pts'][:-1])/max(1,len(b['pts'])-1)
    cn=sum(p[1] for p in b['pts'][:-1])/max(1,len(b['pts'])-1)
    d=math.hypot(ce,cn)
    if d<90 and b['area']>700 and (cath is None or d<cath[0]): cath=(d,b)
if cath: cath[1]['cath']=True; cath[1]['h']=max(cath[1]['h'],17); print('cathedral part at',round(cath[0],1),'m area',cath[1]['area'])
# bell tower anchor: the cathedral is a multi-part building; its tower rises from the WEST end
# of the whole footprint (facade side), not from the largest part's roof vertex
if cath:
    cbid=cath[1]['ref'].rsplit('_part',1)[0]
    west=None
    for b in buildings:
        if b['ref'].rsplit('_part',1)[0]!=cbid: continue
        for (e,n) in b['pts'][:-1]:
            if west is None or e<west[0]: west=(e,n)
    cath[1]['tower_en']=(west[0]+5.0,west[1]-3.0)  # centred on the facade (footprint is ~10 m wide there)
    print('cathedral tower anchored west at',west)

# Teatro Circo (Catastro building 9472601WJ9197A): exterior is a curved metallic skin under a dark
# inclined roof (verified photos); the Catastro inner oval part is low, which opened a false arena.
for b in buildings:
    if b['ref'].startswith('9472601WJ9197A'):
        b['teatro']=True
        if b['ref'].endswith('_part6'): b['h']=max(b['h'],11.0)
        if b['ref'].endswith('_part12'):
            # Catastro stores the oval as a ring with a slit; keep only the outer outline so the exterior is closed
            ip=[i for i,p in enumerate(b['pts']) if (round(p[0]),round(p[1]))==(179,55)]
            if ip: b['pts']=b['pts'][:ip[0]+1]+[b['pts'][0]]
# Pasaje Lodares: OSM way (tunnel=building_passage, width 4.66) covered by a glazed roof with iron ribs
def _lodares():
    out=[]
    try:
        for el in json.load(open('/tmp/osm/roads.json'))['elements']:
            t=el.get('tags',{})
            if el.get('type')=='way' and t.get('name')=='Pasaje Lodares' and t.get('tunnel')=='building_passage':
                cl=[to_en(g['lat'],g['lon']) for g in el['geometry']]
                hw=float(t.get('width','4.66'))/2.0
                k=0
                for i in range(len(cl)-1):
                    (e0,n0),(e1,n1)=cl[i],cl[i+1]
                    L=math.hypot(e1-e0,n1-n0)
                    if L<4: continue
                    ux,uy=(e1-e0)/L,(n1-n0)/L; px_,py_=-uy*hw,ux*hw
                    q=[(e0+px_,n0+py_),(e1+px_,n1+py_),(e1-px_,n1-py_),(e0-px_,n0-py_)]
                    out.append({'pts':q+[q[0]],'h':15.0,'use':'glass','ref':'lodares_%d'%k,'area':L*hw*2,'glass':True,'cl':((e0,n0),(e1,n1))}); k+=1
    except Exception as ex: print('lodares fail',ex)
    return out
_lg=_lodares(); buildings.extend(_lg); print('lodares glass strips',len(_lg))

# OSM ground layers
def load(fn):
    with open(fn) as f: return json.load(f)['elements']
def to_en(lat,lon): return catparse.to_en(lat,lon)

roads=[];greens=[];waters=[];WK={};parkings=[];peds=[];rails=[];trees=[]
for el in load('/tmp/osm/green.json'):
    t=el.get('tags',{})
    if el['type']=='node' and t.get('natural')=='tree':
        e,n=to_en(el['lat'],el['lon'])
        if MINE-40<e<MAXE+40 and MINN-40<n<MAXN+40: trees.append((e,n))
        continue
    if el['type']!='way' or 'geometry' not in el: continue
    pts=[to_en(g['lat'],g['lon']) for g in el['geometry']]
    if not any(MINE-120<e<MAXE+120 and MINN-120<n<MAXN+120 for e,n in pts): continue
    if t.get('natural')=='water' or t.get('waterway') or t.get('water') or t.get('amenity')=='fountain':
        if t.get('waterway')=='lock_gate': continue
        wk='water'
        if t.get('amenity')=='fountain' or t.get('water')=='fountain': wk='fountain'
        elif t.get('waterway')=='canal': wk='canal'
        elif t.get('waterway') in ('stream','drain','ditch'): wk='ditch'
        elif t.get('water') in ('pond','lake','reservoir'): wk='pond'
        elif t.get('water')=='basin': wk='basin'
        elif t.get('water')=='well': wk='well'
        waters.append(pts); WK[(pts[0],len(pts))]=wk
    elif t.get('amenity')=='parking': parkings.append(pts)
    elif t.get('highway')=='pedestrian' or t.get('place')=='square': peds.append(pts)
    else: greens.append(pts)
for el in load('/tmp/osm/roads.json'):
    if el['type']!='way' or 'geometry' not in el: continue
    t=el.get('tags',{})
    pts=[to_en(g['lat'],g['lon']) for g in el['geometry']]
    if not any(MINE-150<e<MAXE+150 and MINN-150<n<MAXN+150 for e,n in pts): continue
    if 'railway' in t: rails.append(pts); continue
    hw=t.get('highway','')
    W_={'motorway':14,'trunk':12,'primary':11,'secondary':9,'tertiary':8,'unclassified':6,'residential':6,
       'living_street':5,'pedestrian':5,'service':4,'track':3,'footway':1.8,'path':1.8,'cycleway':2.2,'steps':1.8}.get(hw,5)
    roads.append({'w':W_,'hw':hw,'pts':pts})
print('roads',len(roads),'greens',len(greens),'waters',len(waters),'trees',len(trees),'rails',len(rails))

# junction detection for crosswalks: grid cells shared by 2+ paved roads
_ptc={}
for _r in roads:
    if _r['w']<6: continue
    for _p in _r['pts']:
        _ptc.setdefault((round(_p[0]/6),round(_p[1]/6)),set()).add(id(_r))
NJUNCT=sum(1 for v in _ptc.values() if len(v)>=2)
print('junctions',NJUNCT)

corn=[to_screen(e,n) for e in (MINE,MAXE) for n in (MINN,MAXN)]
sx0=min(p[0] for p in corn)-60; sx1=max(p[0] for p in corn)+60
sy0=min(p[1] for p in corn)-60-60*C; sy1=max(p[1] for p in corn)+60
W=int(sx1-sx0); H=int(sy1-sy0)
NTX=math.ceil(W/TS); NTY=math.ceil(H/TS)
print('canvas',W,H,'tiles',NTX*NTY)
def scr(e,n,z=0.0):
    x,y=to_screen(e,n,z); return (x-sx0,y-sy0)

GROUND=(216,199,163); PLAZA=(234,208,168); KERB=(238,232,216); ROAD=(124,123,120); PARK=(112,168,32)
WATER=(46,155,214); PARKING=(112,112,110); RAIL=(90,88,92); SHADOW=(24,28,54)
TREE_D=(54,104,16); TREE=(88,148,24); TREE_L=(116,176,40)
ROOFS=[(196,110,60),(206,124,70),(188,100,52),(214,134,80),(178,92,48),(200,118,66),(168,80,64),
       (216,140,88),(170,88,44),(222,150,100),(184,108,70),(164,74,58),(210,130,76),(192,120,84),(176,96,66)]
# wider Mediterranean palette: ~30% creams, rest saturated solid tones (salmon, terracotta,
# ochre, sage, grey-blue, dusty pink, pale yellow, tan) so each building gets its own identity
WALLS=[(236,224,200),(228,212,182),(240,232,212),(222,200,168),(232,218,196),
       (238,228,206),(244,236,216),(248,240,228),(234,220,190),
       (219,130,96),(206,110,78),(232,158,108),(190,100,70),(178,96,64),
       (222,166,96),(212,148,84),(236,190,120),
       (156,168,140),(170,182,152),
       (140,156,170),(158,172,186),(120,138,152),
       (228,176,162),(216,150,134),
       (240,222,172),(246,232,190),
       (198,176,150),(186,162,138)]
def roof_color(b):
    if b.get('teatro'): return (104,92,86)
    r=h01('r',b['ref'])
    if b['use'].startswith('3_industrial'): return (158,152,144) if r<0.5 else (146,140,134)
    if b['use'].startswith(('4_2','4_1')): return (188,120,78) if r<0.5 else (176,108,68)
    return ROOFS[int(r*len(ROOFS))]
def wall_color(b):
    if b.get('cath'): return (224,198,158)
    if b.get('teatro'): return (172,154,134)
    return WALLS[int(h01('w',b['ref'])*len(WALLS))]
def shade(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)

def _pip(poly,x,y):
    inside=False; j=len(poly)-1
    for i in range(len(poly)):
        xi,yi=poly[i]; xj,yj=poly[j]
        if (yi>y)!=(yj>y) and x<(xj-xi)*(y-yi)/((yj-yi) or 1e-9)+xi: inside=not inside
        j=i
    return inside

def dab_canopy(dr,x,y,s,seed,base=None,soft=False):
    # organic pixel canopy: many small jittered dabs inside an ellipse footprint
    # (reference look: noisy clusters, never smooth plastic ellipses)
    if base is None: base=(96,164,22)
    # calmer olive ramp with deep shadow (reference: large patches, deep shade)
    RAMP=[shade(base,0.55),shade(base,0.78),shade(base,0.94),shade(base,1.12)]
    if soft: RAMP=[shade(base,0.80),shade(base,0.95),shade(base,1.08),shade(base,1.22)]
    w=10*s; h=13.5*s
    # ground shadow
    dr.ellipse([x+2,y+2,x+(5 if soft else 7)*s,y+(3.5 if soft else 5.5)*s],fill=(88,92,76) if soft else (58,66,52))
    # wide canopy mass underlay (dabs break its edge, so it never reads as plastic)
    dr.ellipse([x-0.8*w,y-0.72*h,x+0.8*w,y+0.42*h],fill=shade(base,0.84))
    dr.ellipse([x-0.55*w,y-0.95*h,x+0.55*w,y+0.1*h],fill=shade(base,0.90))
    # clumped dabs: a few patch centers, each with its own tone, like the reference's
    # large grouped stains with deep shadows
    npatch=3+int(h01('dp',seed)*3)
    patches=[]
    for p in range(npatch):
        pu=h01('dpu',seed+str(p)); pv=h01('dpv',seed+str(p))
        patches.append(((pu-0.5)*1.1*w,(pv-0.5)*0.9*h-3.0*s,RAMP[p%4]))
    n=int(30*s*s)+12
    for k in range(n):
        pcx,pcy,ptone=patches[int(h01('dpk',seed+str(k))*npatch)%npatch]
        u=h01('du',seed+str(k)); v=h01('dv',seed+str(k))
        dx=pcx+(u-0.5)*0.62*w; dy=pcy+(v-0.5)*0.62*h
        # keep dabs inside the canopy footprint
        ex=dx/w; ey=(dy+3.5*s)/h
        if ex*ex+ey*ey>1.0: continue
        tone=ptone
        if dy>0.2*h: tone=shade(tone,0.88 if soft else 0.72)          # lower shade
        if dy<-0.55*h and dx<0: tone=shade(tone,1.15)  # lit crown
        d=1.8+s*1.1*(0.5+h01('ds',seed+str(k)))
        dr.ellipse([x+dx-d,y+dy-d,x+dx+d,y+dy+d],fill=tone)

def hatch_poly(dr,poly,step,col):
    # horizontal stripe rows clipped to a polygon via scanline intersection
    ys=[p[1] for p in poly]
    y=int(min(ys))+2
    while y<max(ys)-1:
        ints=[]
        for i in range(len(poly)-1):
            (xa,ya),(xb,yb)=poly[i],poly[i+1]
            if (ya<=y<yb) or (yb<=y<ya):
                ints.append(xa+(xb-xa)*(y-ya)/((yb-ya) or 1e-9))
        ints.sort()
        for j in range(0,len(ints)-1,2):
            dr.line([(ints[j],y),(ints[j+1],y)],fill=col,width=1)
        y+=step

def clip_segments(poly,o,d):
    # segments of the infinite line o+t*d clipped to the polygon
    ts=[]
    for i in range(len(poly)-1):
        (xa,ya),(xb,yb)=poly[i],poly[i+1]
        ex,ey=xb-xa,yb-ya
        den=d[0]*ey-d[1]*ex
        if abs(den)<1e-9: continue
        t=((xa-o[0])*ey-(ya-o[1])*ex)/den
        s=((xa-o[0])*d[1]-(ya-o[1])*d[0])/den
        if 0<=s<=1: ts.append(t)
    ts.sort()
    return [(ts[i],ts[i+1]) for i in range(0,len(ts)-1,2)]

def clip_half(poly,c,v,keep_pos):
    # Sutherland-Hodgman clip of polygon to one side of the ridge line through c along v-normal
    out=[]
    for i in range(len(poly)-1):
        pa,pb=poly[i],poly[i+1]
        da=(pa[0]-c[0])*v[0]+(pa[1]-c[1])*v[1]
        db=(pb[0]-c[0])*v[0]+(pb[1]-c[1])*v[1]
        ina=(da>=0) if keep_pos else (da<=0)
        inb=(db>=0) if keep_pos else (db<=0)
        if ina: out.append(pa)
        if ina!=inb:
            tt=da/((da-db) or 1e-9)
            out.append((pa[0]+(pb[0]-pa[0])*tt,pa[1]+(pb[1]-pa[1])*tt))
    if len(out)>2: out.append(out[0])
    return out if len(out)>2 else None

bindex=collections.defaultdict(list)
for b in buildings:
    g=[scr(e,n) for e,n in b['pts']]
    gx0=min(p[0] for p in g)-b['h']*C*1.1; gx1=max(p[0] for p in g)+b['h']*C*1.1
    gy0=min(p[1] for p in g)-b['h']*C*1.15; gy1=max(p[1] for p in g)+b['h']*C*0.7
    if b.get('cath'): gy0-=220  # bell tower rises well above the nave roof
    b['g']=g; b['key']=max(e-n for e,n in b['pts'])
    for tx in range(max(0,int(gx0//TS)),min(NTX-1,int(gx1//TS))+1):
        for ty in range(max(0,int(gy0//TS)),min(NTY-1,int(gy1//TS))+1):
            bindex[(tx,ty)].append(b)
tindex=collections.defaultdict(list)
for (e,n) in trees:
    x,y=scr(e,n); tindex[(int(x//TS),int(y//TS))].append((x,y,e-n))

def _bb_pts(pts):
    sp=[scr(e,n) for e,n in pts]
    xs=[p[0] for p in sp]; ys=[p[1] for p in sp]
    return min(xs),min(ys),max(xs),max(ys)
def _bucket(seq,bboxfn,margin):
    idx=collections.defaultdict(list)
    for it in seq:
        x0,y0,x1,y1=bboxfn(it)
        for tx in range(max(0,int((x0-margin)//TS)),min(NTX-1,int((x1+margin)//TS))+1):
            for ty in range(max(0,int((y0-margin)//TS)),min(NTY-1,int((y1+margin)//TS))+1):
                idx[(tx,ty)].append(it)
    return idx
gindex=_bucket(greens,_bb_pts,80)
pedindex=_bucket(peds,_bb_pts,80)
parkindex=_bucket(parkings,_bb_pts,80)
watindex=_bucket(waters,_bb_pts,80)
railindex=_bucket(rails,_bb_pts,80)
rindex=_bucket(roads,lambda r:_bb_pts(r['pts']),110)
print('bucketed ground layers')

def _convex(poly):
    s_=0
    for i in range(len(poly)-1):
        a=poly[i]; b_=poly[(i+1)%(len(poly)-1)]; c=poly[(i+2)%(len(poly)-1)]
        cr=(b_[0]-a[0])*(c[1]-b_[1])-(b_[1]-a[1])*(c[0]-b_[0])
        if abs(cr)>1e-6:
            if s_==0: s_=1 if cr>0 else -1
            elif (cr>0)!=(s_>0): return False
    return True

def render_tile(tx,ty):
    ox,oy=tx*TS,ty*TS
    im=Image.new('RGBA',(TS,TS),(0,0,0,0))
    dr=ImageDraw.Draw(im)
    K=C/4.5  # sprite/detail scale factor
    gp=[scr(MINE,MINN),scr(MAXE,MINN),scr(MAXE,MAXN),scr(MINE,MAXN)]
    dr.polygon([(x-ox,y-oy) for x,y in gp],fill=GROUND+(255,))
    for pts in gindex.get((tx,ty),[]):
        dr.polygon([(x-ox,y-oy) for x,y in (scr(e,n) for e,n in pts)],fill=PARK)
    for pts in pedindex.get((tx,ty),[]):
        sp=[(x-ox,y-oy) for x,y in (scr(e,n) for e,n in pts)]
        dr.polygon(sp,fill=PLAZA)
        dr.line(sp+[sp[0]],fill=shade(PLAZA,0.84),width=2)
        # warm paving, grid follows the street axes (isometric), masked to the plaza polygon
        m=Image.new('L',(TS,TS),0); ImageDraw.Draw(m).polygon(sp,fill=255)
        pg=Image.new('RGBA',(TS,TS),(0,0,0,0)); dg=ImageDraw.Draw(pg)
        pes=[p[0] for p in pts]; pns=[p[1] for p in pts]
        e0,e1,n0,n1=min(pes),max(pes),min(pns),max(pns)
        if (e1-e0)*(n1-n0)<400000:
            STEP=3.0
            ee=int(e0//STEP)*STEP
            while ee<=e1:
                a_=scr(ee,n0); b_=scr(ee,n1)
                dg.line([(a_[0]-ox,a_[1]-oy),(b_[0]-ox,b_[1]-oy)],fill=shade(PLAZA,0.80)+(255,),width=1); ee+=STEP
            nn=int(n0//STEP)*STEP
            while nn<=n1:
                a_=scr(e0,nn); b_=scr(e1,nn)
                dg.line([(a_[0]-ox,a_[1]-oy),(b_[0]-ox,b_[1]-oy)],fill=shade(PLAZA,0.80)+(255,),width=1); nn+=STEP
        pg.putalpha(m.point(lambda v:95 if v else 0))
        im=Image.alpha_composite(im,pg); dr=ImageDraw.Draw(im)
    for pts in parkindex.get((tx,ty),[]):
        dr.polygon([(x-ox,y-oy) for x,y in (scr(e,n) for e,n in pts)],fill=PARKING)
    # pale pavement strip on both sides of urban streets: separates footpath from carriageway
    for r in rindex.get((tx,ty),[]):
        if r['hw'] in ('residential','tertiary','unclassified','secondary','primary','living_street','service') and 4<=r['w']<=16:
            spk=[(x-ox,y-oy) for x,y in (scr(e,n) for e,n in r['pts'])]
            dr.line(spk,fill=KERB,width=max(2,int(r['w']*C*0.92+3.0*C)),joint='curve')
    for r in rindex.get((tx,ty),[]):
        sp=[(x-ox,y-oy) for x,y in (scr(e,n) for e,n in r['pts'])]
        soft=r['hw'] in ('footway','path','cycleway','steps','pedestrian','living_street')
        dr.line(sp,fill=PLAZA if soft else ROAD,width=max(1,int(r['w']*C*0.92)),joint='curve')
        # dashed centre line on wide roads
        if r['w']>=8 and not soft:
            period=3.0*C+4.0*C; acc=0.0
            for i in range(len(sp)-1):
                x1,y1=sp[i]; x2,y2=sp[i+1]
                seg=math.hypot(x2-x1,y2-y1)
                if seg<2: continue
                dx,dy=(x2-x1)/seg,(y2-y1)/seg
                s=(-acc)%period
                while s<seg:
                    e2=min(s+3.0*C,seg)
                    dr.line([(x1+dx*s,y1+dy*s),(x1+dx*e2,y1+dy*e2)],fill=(226,224,214),width=1)
                    s+=period
                acc=(acc+seg)%period
        # zebra crossings where this road meets others
        if r['w']>=6 and not soft:
            rpts=r['pts']
            for i,p in enumerate(rpts):
                if len(_ptc.get((round(p[0]/6),round(p[1]/6)),()))<2: continue
                q=rpts[i+1] if i<len(rpts)-1 else rpts[i-1]
                ddx,ddy=q[0]-p[0],q[1]-p[1]; dl=math.hypot(ddx,ddy)
                if dl<1: continue
                dx,dy=ddx/dl,ddy/dl
                if i==len(rpts)-1: dx,dy=-dx,-dy
                cx=p[0]+dx*5.0; cy=p[1]+dy*5.0
                scx,scy=scr(cx,cy); scx-=ox; scy-=oy
                sx,sy=to_screen(dx+100,dy+100); sx-=to_screen(100,100)[0]; sy-=to_screen(100,100)[1]
                sl=math.hypot(sx,sy); sx,sy=sx/sl,sy/sl
                px_,py_=-sy,sx
                halfW=r['w']*0.40*C
                for k in range(4):
                    off=(k-1.5)*2.0*C
                    cxk=scx+sx*off; cyk=scy+sy*off
                    wd=0.55*C
                    dr.polygon([(cxk-px_*halfW-sx*wd,cyk-py_*halfW-sy*wd),(cxk+px_*halfW-sx*wd,cyk+py_*halfW-sy*wd),
                                (cxk+px_*halfW+sx*wd,cyk+py_*halfW+sy*wd),(cxk-px_*halfW+sx*wd,cyk-py_*halfW+sy*wd)],fill=(238,236,230))
    CARS=[(196,68,62),(68,110,168),(238,238,238),(60,64,70),(232,196,60),(120,122,128)]
    for r in rindex.get((tx,ty),[]):
        if r['hw'] in ('footway','path','cycleway','steps','pedestrian','living_street'): continue
        sp=[scr(e,n) for e,n in r['pts']]
        acc=0.0
        for i in range(len(sp)-1):
            x1,y1=sp[i]; x2,y2=sp[i+1]
            seg=math.hypot(x2-x1,y2-y1); acc+=seg
            if seg<8: continue
            if acc>19*C and h01('car',str(r['pts'][0])+str(i))<0.60:
                acc=0.0
                tt=0.5
                px,py=(x1+x2)/2,(y1+y2)/2
                dx,dy=(x2-x1)/seg,(y2-y1)/seg
                L=4.2*C*0.5; Wd=1.9*C*0.5
                cc=CARS[int(h01('carc',str(r['pts'][0])+str(i))*len(CARS))]
                px-=ox; py-=oy
                dr.polygon([(px-dx*L-dy*Wd+2,py-dy*L+dx*Wd+2),(px+dx*L-dy*Wd+2,py+dy*L+dx*Wd+2),
                            (px+dx*L+dy*Wd+2,py+dy*L-dx*Wd+2),(px-dx*L+dy*Wd+2,py-dy*L-dx*Wd+2)],fill=(70,70,74))
                dr.polygon([(px-dx*L-dy*Wd,py-dy*L+dx*Wd),(px+dx*L-dy*Wd,py+dy*L+dx*Wd),
                            (px+dx*L+dy*Wd,py+dy*L-dx*Wd),(px-dx*L+dy*Wd,py-dy*L-dx*Wd)],fill=cc)
                L2=L*0.45
                dr.polygon([(px-dx*L2-dy*Wd*0.7,py-dy*L2+dx*Wd*0.7),(px+dx*L2-dy*Wd*0.7,py+dy*L2+dx*Wd*0.7),
                            (px+dx*L2+dy*Wd*0.7,py+dy*L2-dx*Wd*0.7),(px-dx*L2+dy*Wd*0.7,py-dy*L2-dx*Wd*0.7)],fill=shade(cc,1.25))
    # parked cars along kerbs on calm streets
    for r in rindex.get((tx,ty),[]):
        if r['hw'] not in ('residential','tertiary','unclassified','secondary'): continue
        sp=[scr(e,n) for e,n in r['pts']]
        for i in range(len(sp)-1):
            x1,y1=sp[i]; x2,y2=sp[i+1]
            seg=math.hypot(x2-x1,y2-y1)
            if seg<8: continue
            dx,dy=(x2-x1)/seg,(y2-y1)/seg
            nsteps=max(1,int(seg/(11*C)))
            for s_ in range(nsteps):
                if h01('pk',str(r['pts'][0])+str(i)+'_'+str(s_))>0.46: continue
                t0=(s_+0.5)/nsteps
                px,py=x1+(x2-x1)*t0,y1+(y2-y1)*t0
                side=1 if h01('pks',str(r['pts'][0])+str(i)+'_'+str(s_))<0.5 else -1
                off=(r['w']*0.5-1.6)*C*side*0.92
                px+=-dy*off; py+=dx*off
                L=4.2*C*0.5; Wd=1.9*C*0.5
                cc=CARS[int(h01('pkc',str(r['pts'][0])+str(i)+'_'+str(s_))*len(CARS))]
                px-=ox; py-=oy
                dr.polygon([(px-dx*L-dy*Wd+2,py-dy*L+dx*Wd+2),(px+dx*L-dy*Wd+2,py+dy*L+dx*Wd+2),
                            (px+dx*L+dy*Wd+2,py+dy*L-dx*Wd+2),(px-dx*L+dy*Wd+2,py-dy*L-dx*Wd+2)],fill=(70,70,74))
                dr.polygon([(px-dx*L-dy*Wd,py-dy*L+dx*Wd),(px+dx*L-dy*Wd,py+dy*L+dx*Wd),
                            (px+dx*L+dy*Wd,py+dy*L-dx*Wd),(px-dx*L+dy*Wd,py-dy*L-dx*Wd)],fill=cc)
                L2=L*0.45
                dr.polygon([(px-dx*L2-dy*Wd*0.7,py-dy*L2+dx*Wd*0.7),(px+dx*L2-dy*Wd*0.7,py+dy*L2+dx*Wd*0.7),
                            (px+dx*L2+dy*Wd*0.7,py+dy*L2-dx*Wd*0.7),(px-dx*L2+dy*Wd*0.7,py-dy*L2-dx*Wd*0.7)],fill=shade(cc,1.25))
    for pts in gindex.get((tx,ty),[]):
        gk='%.1f_%.1f'%(pts[0][0],pts[0][1])
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        area=abs(sum(pts[i][0]*pts[i+1][1]-pts[i+1][0]*pts[i][1] for i in range(len(pts)-1)))/2
        def _inside(e,n):
            inside=False; j=len(pts)-1
            for i in range(len(pts)):
                xi,yi=pts[i]; xj,yj=pts[j]
                if ((yi>n)!=(yj>n)) and (e<(xj-xi)*(n-yi)/(yj-yi+1e-9)+xi): inside=not inside
                j=i
            return inside
        # clustered canopy trees fill the park (reference look: overlapping multigreen blobs);
        # density per m2 constant across park sizes so big and small parks read equally wooded
        nt_=min(900,int(area/60))
        RAMP=[(66,124,24),(88,148,24),(54,104,16),(102,160,30)]
        for k in range(nt_):
            u=h01('tu',gk+'_'+str(k)); v=h01('tv',gk+'_'+str(k))
            e=min(xs)+(max(xs)-min(xs))*u; n=min(ys)+(max(ys)-min(ys))*v
            if not _inside(e,n): continue
            x,y=scr(e,n); x-=ox; y-=oy
            th=h01('tt',gk+'_'+str(k)); s=2.9+th*1.9
            dab_canopy(dr,x,y,s,'pk'+gk+'_'+str(k),RAMP[int(th*4)%4])
            if th>0.45:
                dr.ellipse([x-2*s,y-14*s,x+3*s,y-7*s],fill=(140,198,64))
        np_=min(14,int(area/900))
        for k in range(np_):
            u=h01('pu',gk+'_'+str(k)); v=h01('pv',gk+'_'+str(k))
            e=min(xs)+(max(xs)-min(xs))*u; n=min(ys)+(max(ys)-min(ys))*v
            if not _inside(e,n): continue
            x,y=scr(e,n); x-=ox; y-=oy
            if h01('ps',gk+'_'+str(k))<0.5:
                dr.ellipse([x-1.6,y-1.2,x+1.6,y+1.2],fill=(52,50,48))
                dr.ellipse([x-1.2,y-3.6,x+1.2,y-1.4],fill=(214,72,60) if k%3 else (236,236,232))
    # people: figures with shirt, trousers, head and cast shadow; on plazas, walking paths and pavements
    SHIRT=[(214,72,60),(236,236,232),(60,110,170),(240,196,60),(92,150,90),(190,90,150),(40,40,48),(230,130,60)]
    def person(x,y,seed):
        c=SHIRT[int(h01('pc',seed)*len(SHIRT))]
        dr.ellipse([x-6.5*K,y-0.8*K,x-0.5*K,y+1.4*K],fill=(120,112,96))
        dr.rectangle([x-1.1*K,y-3.2*K,x+1.1*K,y],fill=(48,46,56))
        dr.rectangle([x-1.4*K,y-6.2*K,x+1.4*K,y-3.0*K],fill=c)
        dr.rectangle([x-1.4*K,y-6.2*K,x-0.4*K,y-3.0*K],fill=shade(c,0.78))
        dr.ellipse([x-1.1*K,y-8.2*K,x+1.1*K,y-6.0*K],fill=(226,176,140))
    for pts in pedindex.get((tx,ty),[]):
        gk='pd%.1f_%.1f'%(pts[0][0],pts[0][1])
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        area=abs(sum(pts[i][0]*pts[i+1][1]-pts[i+1][0]*pts[i][1] for i in range(len(pts)-1)))/2
        np_=min(14,int(area/900))
        for k in range(np_):
            u=h01('pdu',gk+'_'+str(k)); v=h01('pdv',gk+'_'+str(k))
            e=min(xs)+(max(xs)-min(xs))*u; n=min(ys)+(max(ys)-min(ys))*v
            inside=False; j=len(pts)-1
            for i in range(len(pts)):
                xi,yi=pts[i]; xj,yj=pts[j]
                if ((yi>n)!=(yj>n)) and (e<(xj-xi)*(n-yi)/(yj-yi+1e-9)+xi): inside=not inside
                j=i
            if not inside: continue
            x,y=scr(e,n); x-=ox; y-=oy
            if not (-10<x<TS+10 and -10<y<TS+10): continue
            person(x,y,gk+'_'+str(k))
            if k%9==0:   # bench
                dr.rectangle([x+5*K,y-1.5*K,x+10*K,y+0.8*K],fill=(120,84,52)); dr.rectangle([x+5*K,y-3.2*K,x+10*K,y-1.5*K],fill=(150,106,66))
    for r in rindex.get((tx,ty),[]):
        soft=r['hw'] in ('footway','path','pedestrian','living_street','cycleway','steps')
        if not soft and not (r['hw'] in ('residential','tertiary','unclassified','secondary','primary') and r['w']<=16): continue
        sp=[scr(e,n) for e,n in r['pts']]
        wp=r['pts']
        rk=str(r['pts'][0])
        gapm=(26 if soft else 40)   # metres of path per walker, measured along the whole line
        acc=h01('wacc',rk)*gapm
        for i in range(len(sp)-1):
            x1,y1=sp[i]; x2,y2=sp[i+1]
            seg=math.hypot(x2-x1,y2-y1)
            if seg<1: continue
            dx,dy=(x2-x1)/seg,(y2-y1)/seg
            segm=math.hypot(wp[i+1][0]-wp[i][0],wp[i+1][1]-wp[i][1])
            pos=0.0
            while acc+(segm-pos)>=gapm:
                pos+=gapm-acc; acc=0.0
                t0=pos/max(segm,1e-6)
                sd=rk+'_'+str(i)+'_'+str(int(pos))
                ew=wp[i][0]+(wp[i+1][0]-wp[i][0])*t0; nw=wp[i][1]+(wp[i+1][1]-wp[i][1])*t0
                # thin walkers by 14 m cell so overlapping paths never pile people up
                ck=(int(ew//14),int(nw//14))
                if h01('wcell',str(ck))>0.45 or h01('wk',sd)>0.7: continue
                px,py=x1+(x2-x1)*t0,y1+(y2-y1)*t0
                if not soft:
                    side=1 if h01('wsd',sd)<0.5 else -1
                    off=(r['w']*0.5+1.0)*C*side
                    px+=-dy*off; py+=dx*off
                px-=ox; py-=oy
                if not (-10<px<TS+10 and -10<py<TS+10): continue
                person(px,py,sd)
            acc+=segm-pos
            if not soft and seg>20 and h01('lamp',rk+str(i))<0.35:
                side=1 if h01('lps',rk+str(i))<0.5 else -1
                off=(r['w']*0.5+1.2)*C*side
                px=(x1+x2)/2-dy*off-ox; py=(y1+y2)/2+dx*off-oy
                dr.line([(px,py),(px,py-11*K)],fill=(52,50,56),width=max(1,int(K)))
                dr.ellipse([px-1.6*K,py-13*K,px+1.6*K,py-10*K],fill=(250,226,150))
    for pts in railindex.get((tx,ty),[]):
        sp=[(x-ox,y-oy) for x,y in (scr(e,n) for e,n in pts)]
        dr.line(sp,fill=RAIL,width=max(2,int(2.6*C*0.9)),joint='curve')
        dr.line(sp,fill=(205,205,205),width=1)
    for pts in watindex.get((tx,ty),[]):
        sp=[(x-ox,y-oy) for x,y in (scr(e,n) for e,n in pts)]
        wk=WK.get((pts[0],len(pts)),'water')
        closed=pts[0]==pts[-1] and len(pts)>3
        if closed:
            base={'pond':(60,134,176),'water':(62,138,180),'basin':(74,150,190),'fountain':(96,170,204),'well':(96,170,204)}.get(wk,(62,138,180))
            wa=abs(sum(pts[i][0]*pts[i+1][1]-pts[i+1][0]*pts[i][1] for i in range(len(pts)-1)))/2
            if wk=='fountain':
                dr.polygon(sp,fill=(226,220,204)); dr.line(sp+[sp[0]],fill=(168,160,142),width=2)
                # inner water, inset toward the centroid so a stone rim reads around it
                cx_=sum(p[0] for p in sp[:-1])/(len(sp)-1); cy_=sum(p[1] for p in sp[:-1])/(len(sp)-1)
                f_=0.80
                dr.polygon([(cx_+(x-cx_)*f_,cy_+(y-cy_)*f_) for x,y in sp],fill=base)
            else:
                dr.polygon(sp,fill=shade(base,0.78)); dr.line(sp+[sp[0]],fill=(176,196,204),width=3)
                cx_=sum(p[0] for p in sp[:-1])/(len(sp)-1); cy_=sum(p[1] for p in sp[:-1])/(len(sp)-1)
                dr.polygon([(cx_+(x-cx_)*0.94,cy_+(y-cy_)*0.94) for x,y in sp],fill=base)
            # sparse deterministic ripples inside big surfaces
            if wa>150 and wk!='fountain':
                xs=[p[0] for p in sp]; ys=[p[1] for p in sp]
                gk='wt%.1f_%.1f'%(pts[0][0],pts[0][1])
                for k in range(min(36,int(wa/120))):
                    px=min(xs)+(max(xs)-min(xs))*h01('wru',gk+str(k)); py=min(ys)+(max(ys)-min(ys))*h01('wrv',gk+str(k))
                    if not _pip(sp,px,py) or not _pip(sp,px+6,py): continue
                    L_=3+h01('wrl',gk+str(k))*5
                    dr.line([(px,py),(px+L_,py)],fill=shade(base,1.28) if k%3 else shade(base,0.82),width=1)
        else:
            if wk=='canal':
                dr.line(sp,fill=(176,196,204),width=max(3,int(4*C*0.9)+3),joint='curve')
                dr.line(sp,fill=(66,140,184),width=max(2,int(4*C*0.9)),joint='curve')
            elif wk=='ditch':
                dr.line(sp,fill=(112,152,170),width=max(2,int(1.4*C)),joint='curve')
            else:
                dr.line(sp,fill=(66,140,184),width=max(2,int(3*C*0.9)),joint='curve')
    # shadows (binary mask -> constant alpha, no stacking)
    mask=Image.new('L',(TS,TS),0); dm=ImageDraw.Draw(mask)
    for b in bindex.get((tx,ty),[]):
        if b.get('glass'): continue
        hpx=b['h']*C
        sh=[(x-ox-hpx*1.05, y-oy+hpx*0.28) for x,y in b['g']]
        dm.polygon(sh,fill=255)
    ov=Image.new('RGBA',(TS,TS),(0,0,0,0))
    ov.paste(Image.new('RGBA',(TS,TS),SHADOW+(255,)),(0,0),mask.point(lambda v:110 if v else 0))
    im=Image.alpha_composite(im,ov)
    dr=ImageDraw.Draw(im)
    # painter order: buildings + trees
    items=[(b['key'],0,b) for b in bindex.get((tx,ty),[])]
    items+=[(k,1,(x,y)) for (x,y,k) in tindex.get((tx,ty),[])]
    items.sort(key=lambda t:(t[0],t[1]))
    for _,kind,obj in items:
        if kind==1:
            x,y=obj; x-=ox; y-=oy
            th=h01('tree',str(int(x*7))+str(int(y*7))); s=1.05+th*1.35
            _pal=[(112,160,44),(132,164,46),(152,168,56),(100,146,52),(140,172,64),(124,150,50),(160,172,70)]
            _bc=_pal[int(h01('tpal',str(int(x*7))+str(int(y*7)))*len(_pal))%len(_pal)]
            dab_canopy(dr,x,y,s,'st'+str(int(x*7))+str(int(y*7)),shade(_bc,0.86+th*0.22),soft=True)
            continue
        b=obj; hpx=b['h']*C
        g=[(x-ox,y-oy) for x,y in b['g']]
        t=[(x,y-hpx) for x,y in g]
        wall=wall_color(b); roof=roof_color(b)
        if b.get('glass'):
            A,B_,Cc,D=t[0],t[1],t[2],t[3]
            M1=((A[0]+D[0])/2,(A[1]+D[1])/2); M2=((B_[0]+Cc[0])/2,(B_[1]+Cc[1])/2)
            dr.polygon([A,B_,M2,M1],fill=(166,194,206)); dr.polygon([M1,M2,Cc,D],fill=(198,220,224))
            Ls=math.hypot(B_[0]-A[0],B_[1]-A[1]); nr=max(2,int(Ls/(2.4*C)))
            for k in range(1,nr):
                u=k/nr
                dr.line([(A[0]+(B_[0]-A[0])*u,A[1]+(B_[1]-A[1])*u),(M1[0]+(M2[0]-M1[0])*u,M1[1]+(M2[1]-M1[1])*u)],fill=(96,112,112),width=1)
                dr.line([(M1[0]+(M2[0]-M1[0])*u,M1[1]+(M2[1]-M1[1])*u),(D[0]+(Cc[0]-D[0])*u,D[1]+(Cc[1]-D[1])*u)],fill=(96,112,112),width=1)
            dr.line([M1,M2],fill=(84,98,98),width=2)
            dr.line([A,B_],fill=(84,98,98),width=1); dr.line([D,Cc],fill=(84,98,98),width=1)
            continue
        for i in range(len(g)-1):
            x1,y1=g[i]; x2,y2=g[i+1]
            de=b['pts'][i+1][0]-b['pts'][i][0]; dn=b['pts'][i+1][1]-b['pts'][i][1]
            nx,ny=dn,-de
            if nx-ny<=0: continue
            # wide value separation between orientations: readable 3D volume
            K=C/4.5  # detail scale factor: fixed-pixel features follow the map scale
            f=0.62+0.50*max(0.0,min(1.0,(nx*0.97+(-ny)*0.26)/max(1e-6,math.hypot(nx,ny))))
            col=shade(wall,f)
            dr.polygon([(x1,y1),(x2,y2),(x2,y2-hpx),(x1,y1-hpx)],fill=col)
            # wall texture: sparse tone dabs kill the flat fill, subtle vertical darkening to the base
            elen=math.hypot(x2-x1,y2-y1)
            ntex=min(26,int(elen*hpx/900))
            for k in range(ntex):
                u=h01('txu',b['ref']+f'{i}_{k}'); v=h01('txv',b['ref']+f'{i}_{k}')
                px=x1+(x2-x1)*u; py=(y1+(y2-y1)*u)-hpx*v
                tone=shade(col,0.94 if k%2 else 1.06)
                dr.rectangle([px-1.3*K,py-1.0*K,px+1.3*K,py+1.0*K],fill=tone)
            # ground-contact ambient occlusion
            dr.line([(x1,y1),(x2,y2)],fill=shade(col,0.58),width=2)
            # cornice: bright cap band with eave shadow under it
            dr.line([(x1,y1-hpx),(x2,y2-hpx)],fill=shade(col,1.20),width=3)
            dr.line([(x1,y1-hpx+3.2),(x2,y2-hpx+3.2)],fill=shade(col,0.70),width=2)
            # per-building facade rhythm from its seed: bay spacing + window proportion vary,
            # so the city never reads as one repeated grid; use type steers ground floor
            bay=2.7+1.5*h01('bay',b['ref'])
            winw=0.9+0.5*h01('ww',b['ref'])          # half-width factor
            winh=1.15+0.45*h01('wh',b['ref'])      # half-height factor
            pers=0.55+0.35*h01('pers',b['ref'])    # roller-shutter probability (very local)
            retail=b['use'].startswith(('4_2','4_1'))
            # ground floor: taller distinct base, arcade of bigger openings
            if hpx>20:
                gb=3.4*C
                dr.polygon([(x1,y1-gb),(x2,y2-gb),(x2,y2),(x1,y1)],fill=shade(col,0.80))
                dr.line([(x1,y1-gb),(x2,y2-gb)],fill=shade(col,0.58),width=2)
                el0=elen
                shop_p=0.85 if retail else 0.62
                if el0>14 and h01('shop',b['ref']+str(i))<shop_p:
                    nd=max(1,int(el0/(4.2*C)))
                    for dd_ in range(nd):
                        tt=(dd_+0.5)/nd
                        dxp=x1+(x2-x1)*tt; dyp=y1+(y2-y1)*tt
                        dr.rectangle([dxp-0.53*C,dyp-1.42*C,dxp+0.53*C,dyp-0.4],fill=shade(col,0.40))
                        dr.line([(dxp-0.53*C,dyp-1.42*C),(dxp+0.53*C,dyp-1.42*C)],fill=shade(col,1.12),width=1)
                        if retail:  # awning strip over retail fronts
                            AWN=[(214,90,60),(70,120,170),(238,238,230),(90,150,90)]
                            if h01('awn',b['ref']+str(i)+str(dd_))<0.5:
                                dr.rectangle([dxp-0.66*C,dyp-1.78*C,dxp+0.66*C,dyp-1.47*C],fill=AWN[int(h01('awnc',b['ref']+str(i)+str(dd_))*4)])
            if elen>18 and hpx>24:
                blind=h01('blind',b['ref'])<0.22
                cols=max(1,int(elen/(bay*C))); rows=int((b['h']-3.4)/3.0)
                # continuous balcony railing lines on some centre blocks (mirador/ironwork rows)
                rail_rows = h01('railr',b['ref'])<0.30 and not blind
                for r in range(min(rows,12)):
                    wy=y1-hpx+(r+0.8)*3*C; wy2=y2-hpx+(r+0.8)*3*C
                    if wy>y1-3.6*C: continue
                    dr.line([(x1,wy+3.1),(x2,wy2+3.1)],fill=shade(col,0.86),width=1)
                    if r%5==4 and rows>=6:
                        dr.line([(x1,wy+3.1+0.18*C),(x2,wy2+3.1+0.18*C)],fill=shade(col,0.78),width=max(1,int(0.35*K)))
                    if blind:
                        # party wall: few small openings + stains
                        for c in range(0,cols,2):
                            tt=(c+0.5)/cols
                            wx=x1+(x2-x1)*tt; wyy=wy+(wy2-wy)*tt
                            dr.rectangle([wx-0.24*C,wyy-0.38*C,wx+0.24*C,wyy+0.38*C],fill=shade(col,0.60))
                        continue
                    for c in range(cols):
                        tt=(c+0.5)/cols
                        wx=x1+(x2-x1)*tt; wyy=wy+(wy2-wy)*tt
                        hw=0.45*C*winw; hh=0.64*C*winh
                        dr.rectangle([wx-hw,wyy-hh,wx+hw,wyy+hh*0.9],fill=shade(col,1.16))
                        lit=h01('gl',b['ref']+f'{i}_{r}_{c}')>0.16
                        GLASS=shade((46,58,76),0.7+0.5*f) if lit else (104,130,158)
                        dr.rectangle([wx-hw*0.7,wyy-hh*0.8,wx+hw*0.7,wyy+hh*0.72],fill=GLASS)
                        dr.line([(wx-hw-0.05*C,wyy+hh*0.9+0.11*C),(wx+hw+0.05*C,wyy+hh*0.9+0.11*C)],fill=shade(col,0.50),width=max(1,int(0.3*K)))
                        # roller-shutter box above the window: the local signature
                        if h01('prs',b['ref']+f'{i}_{r}_{c}')<pers:
                            dr.rectangle([wx-hw-0.4*K,wyy-hh-0.4*K,wx+hw+0.4*K,wyy-hh-0.05*K],fill=shade(col,0.92))
                        hs=h01('sh',b['ref']+f'{i}_{r}_{c}')
                        if hs<0.30:
                            dr.line([(wx-hw-0.22*C,wyy-hh),(wx-hw-0.22*C,wyy+hh*0.8)],fill=shade(col,0.70),width=max(1,int(0.3*K)))
                            dr.line([(wx+hw+0.22*C,wyy-hh),(wx+hw+0.22*C,wyy+hh*0.8)],fill=shade(col,0.70),width=max(1,int(0.3*K)))
                        if r>0 and h01('bal',b['ref']+f'{i}_{r}_{c}')<0.38:
                            dr.polygon([(wx-0.66*C,wyy+hh*0.9+0.27*C),(wx+0.66*C,wyy+hh*0.9+0.27*C),(wx+0.8*C,wyy+hh*0.9+0.75*C),(wx-0.8*C,wyy+hh*0.9+0.75*C)],fill=shade(col,0.86))
                            dr.line([(wx-0.8*C,wyy+hh*0.9+0.75*C),(wx+0.8*C,wyy+hh*0.9+0.75*C)],fill=shade(col,0.50),width=1)
                            dr.line([(wx-0.8*C,wyy+hh*0.9+0.49*C),(wx+0.8*C,wyy+hh*0.9+0.49*C)],fill=shade(col,0.62),width=1)
                if rail_rows:
                    for r in range(min(rows,12)):
                        wy=y1-hpx+(r+0.8)*3*C; wy2=y2-hpx+(r+0.8)*3*C
                        if wy>y1-3.6*C: continue
                        dr.line([(x1,wy+4.6),(x2,wy2+4.6)],fill=shade(col,0.48),width=1)
        dr.polygon(t,fill=roof)
        dr.line(t+[t[0]],fill=shade(roof,0.7),width=max(1,int(K)))
        area_m=b.get('area',0)
        pitched=len(t)<=40 and area_m<4000 and not b['use'].startswith('3_industrial') and not b.get('cath') and not b.get('teatro')
        # hipped (4 aguas) for compact footprints: inset cap + hip lines, two-tone slopes
        if pitched and area_m>250:
            xs_=[p[0] for p in t]; ys_=[p[1] for p in t]
            aspect=(max(xs_)-min(xs_))/max(1e-6,max(ys_)-min(ys_))
            if 0.58<aspect<1.72 and len(t)<=8 and _convex(t[:-1]) and h01('hip',b['ref'])<0.75:
                pitched=False
                cxr=sum(p[0] for p in t[:-1])/(len(t)-1); cyr=sum(p[1] for p in t[:-1])/(len(t)-1)
                dr.polygon(t,fill=shade(roof,1.02))
                cap=[]
                for p in t[:-1]:
                    vx,vy=cxr-p[0],cyr-p[1]
                    dd=max(1e-6,math.hypot(vx,vy))
                    f=min(0.22,4.0*C/max(dd,1e-6))
                    cap.append((p[0]+vx*f,p[1]+vy*f))
                dr.polygon(cap,fill=shade(roof,1.14))
                for i in range(len(t)-1):
                    dr.line([t[i],cap[i]],fill=shade(roof,0.80),width=1)
                dr.line(cap+[cap[0]],fill=shade(roof,0.85),width=1)
                nsp=min(int(60*K),int(area_m*C*C*0.25/120))
                for k in range(nsp):
                    u=h01('hpu',b['ref']+str(k)); v=h01('hpv',b['ref']+str(k))
                    px=min(xs_)+(max(xs_)-min(xs_))*u; py=min(ys_)+(max(ys_)-min(ys_))*v
                    if not _pip(t,px,py): continue
                    tone=shade(roof,1.18 if k%3==0 else 0.84)
                    dr.rectangle([px-1.1*K,py-0.8*K,px+1.1*K,py+0.8*K],fill=tone)
        if b['use'].startswith('3_industrial') and area_m>300:
            # curved nave roof: sinusoidal light bands across the short axis
            xs_=[p[0] for p in t]; ys_=[p[1] for p in t]
            best=0; rdx,rdy=1,0
            for i in range(len(t)-1):
                ex,ey=t[i+1][0]-t[i][0],t[i+1][1]-t[i][1]
                el=math.hypot(ex,ey)
                if el>best: best=el; rdx,rdy=ex/el,ey/el
            pvx,pvy=-rdy,rdx
            cxr=sum(p[0] for p in t[:-1])/(len(t)-1); cyr=sum(p[1] for p in t[:-1])/(len(t)-1)
            for k in range(-20,21):
                oxk=cxr+pvx*k*1.1*C; oyk=cyr+pvy*k*1.1*C
                tonef=1.02+0.14*math.sin(k*1.9)
                for (t0,t1) in clip_segments(t,(oxk,oyk),(rdx,rdy)):
                    dr.line([(oxk+rdx*t0,oyk+rdy*t0),(oxk+rdx*t1,oyk+rdy*t1)],fill=shade(roof,tonef),width=max(1,int(0.9*C)))
        if pitched:
            # two-slope roof volume: split along the ridge (parallel to the longest edge);
            # slope facing the screen-space sun (down-right, matching wall light) reads lit,
            # the opposite one clearly shaded - orientation decides, not the half sign
            best=0; rdx,rdy=1,0
            for i in range(len(t)-1):
                ex,ey=t[i+1][0]-t[i][0],t[i+1][1]-t[i][1]
                el=math.hypot(ex,ey)
                if el>best: best=el; rdx,rdy=ex/el,ey/el
            cxr=sum(p[0] for p in t[:-1])/(len(t)-1); cyr=sum(p[1] for p in t[:-1])/(len(t)-1)
            pvx,pvy=-rdy,rdx
            neg=clip_half(t,(cxr,cyr),(pvx,pvy),False)
            pos=clip_half(t,(cxr,cyr),(pvx,pvy),True)
            def _facing(slope):
                if not slope: return 1
                mx=sum(p[0] for p in slope)/len(slope)-cxr
                my=sum(p[1] for p in slope)/len(slope)-cyr
                return 1 if (mx+0.7*my)>0 else -1
            fneg=_facing(neg); fpos=_facing(pos)
            if neg: dr.polygon(neg,fill=shade(roof,1.12 if fneg>0 else 0.74))
            if pos: dr.polygon(pos,fill=shade(roof,1.12 if fpos>0 else 0.74))
            # tile speckle on large slopes: tiny tone dabs, tone follows the slope's facing
            for si,(slope,face) in enumerate(((neg,fneg),(pos,fpos))):
                if not slope: continue
                xs=[p[0] for p in slope]; ys=[p[1] for p in slope]
                sx0,sx1,sy0,sy1=min(xs),max(xs),min(ys),max(ys)
                nsp=min(int(120*K),int((sx1-sx0)*(sy1-sy0)/120))
                for k in range(nsp):
                    u=h01('spu',b['ref']+f'{si}_{k}'); v=h01('spv',b['ref']+f'{si}_{k}')
                    px=sx0+(sx1-sx0)*u; py=sy0+(sy1-sy0)*v
                    if not _pip(slope,px,py): continue
                    tone=shade(roof,(1.17 if k%3==0 else 1.05) if face>0 else (0.66 if k%3==0 else 0.78))
                    dr.rectangle([px-1.1,py-0.8,px+1.1,py+0.8],fill=tone)
            for (t0,t1) in clip_segments(t,(cxr,cyr),(rdx,rdy)):
                dr.line([(cxr+rdx*t0,cyr+rdy*t0),(cxr+rdx*t1,cyr+rdy*t1)],fill=shade(roof,1.16),width=2)
            step=2.0*C
            for k in range(-14,15):
                if k==0: continue
                oxk=cxr+pvx*k*step; oyk=cyr+pvy*k*step
                for (t0,t1) in clip_segments(t,(oxk,oyk),(rdx,rdy)):
                    mx=oxk+rdx*(t0+t1)/2-cxr; my=oyk+rdy*(t0+t1)/2-cyr
                    side=mx+0.7*my
                    base=0.74 if side<0 else 1.12
                    dr.line([(oxk+rdx*t0,oyk+rdy*t0),(oxk+rdx*t1,oyk+rdy*t1)],fill=shade(roof,base*(0.80 if k%2 else 1.10)),width=1)
            # roof furniture on pitched roofs: chimneys, skylights
            if area_m>60:
                xs_=[p[0] for p in t]; ys_=[p[1] for p in t]
                for k in range(min(3,int(area_m/90)+1)):
                    u=0.2+0.6*h01('fu',b['ref']+str(k)); v=0.2+0.6*h01('fv',b['ref']+str(k))
                    px=min(xs_)+(max(xs_)-min(xs_))*u; py=min(ys_)+(max(ys_)-min(ys_))*v
                    if not _pip(t,px,py): continue
                    kd=h01('fk',b['ref']+str(k))
                    if kd<0.40:
                        dr.rectangle([px-1.5,py-6.0,px+1.5,py],fill=shade(roof,0.62))
                        dr.rectangle([px-1.5,py-6.0,px-0.2,py],fill=shade(roof,0.50))
                        dr.rectangle([px-2.0,py-7.2,px+2.0,py-6.0],fill=shade(roof,1.25))
                    elif kd<0.75:
                        dr.rectangle([px-2.6,py-1.8,px+2.6,py+1.8],fill=(118,150,170))
                        dr.line([(px-2.6,py-1.8),(px+2.6,py-1.8)],fill=(206,224,232),width=1)
                        dr.line([(px,py-1.8),(px,py+1.8)],fill=(80,104,122),width=1)
        else:
            # attic setback: tall blocks get a recessed top volume - stepped silhouette,
            # reads as the real penthouse level instead of one endless plane
            if b['h']>15 and area_m>200 and len(t)<=10 and _convex(t[:-1]) and not b.get('teatro') and h01('setb',b['ref'])<0.55:
                cxr=sum(p[0] for p in t[:-1])/(len(t)-1); cyr=sum(p[1] for p in t[:-1])/(len(t)-1)
                ins=[]
                for p in t[:-1]:
                    vx,vy=cxr-p[0],cyr-p[1]
                    dd=max(1e-6,math.hypot(vx,vy))
                    f=min(0.30,6.5*C/max(dd,1e-6))
                    ins.append((p[0]+vx*f,p[1]+vy*f))
                sh_=3.0*C*0.9
                twall=shade(wall,0.92); troof=shade(roof,1.06)
                for i in range(len(ins)-1):
                    x1,y1=ins[i]; x2,y2=ins[i+1]
                    de=b['pts'][min(i+1,len(b['pts'])-1)][0]-b['pts'][min(i,len(b['pts'])-1)][0] if False else None
                    # shade setback walls with the same orientation logic as main facades
                    dxn,dyn=-(y2-y1),(x2-x1)
                    if dxn-dyn<=0: continue
                    ff=0.62+0.50*max(0.0,min(1.0,(dxn*0.97+(-dyn)*0.26)/max(1e-6,math.hypot(dxn,dyn))))
                    sc=shade(twall,ff)
                    dr.polygon([(x1,y1),(x2,y2),(x2,y2-sh_),(x1,y1-sh_)],fill=sc)
                    dr.line([(x1,y1-sh_),(x2,y2-sh_)],fill=shade(sc,1.18),width=max(1,int(0.4*K)))
                ti=[(x,y-sh_) for x,y in ins]+[ins[0]]
                dr.polygon(ti[:-1],fill=troof)
                dr.line(ti,fill=shade(troof,0.75),width=1)
                # one clutter box on the penthouse roof
                if h01('setc',b['ref'])<0.7:
                    px=(ti[0][0]+ti[2][0])/2 if len(ti)>3 else cxr; py=(ti[0][1]+ti[2][1])/2 if len(ti)>3 else cyr-sh_
                    dr.rectangle([px-2.5*K,py-1.6*K,px+2.5*K,py+1.6*K],fill=shade(troof,0.80))
            # flat/complex roof: stripe rows + parapet + clutter
            if len(t)>5 and area_m>150:
                hatch_poly(dr,t,int(2.6*C),shade(roof,0.85))
                hatch_poly(dr,t,int(5.2*C),shade(roof,1.12))
            if area_m<2500 and len(t)<=8 and not b.get('teatro'):
                cxr=sum(p[0] for p in t[:-1])/(len(t)-1); cyr=sum(p[1] for p in t[:-1])/(len(t)-1)
                hip=shade(roof,0.84)
                for i in range(len(t)-1):
                    dr.line([t[i],(cxr,cyr-1)],fill=hip,width=1)
                dr.line([(cxr,cyr-2),(cxr+2,cyr)],fill=shade(roof,1.12),width=1)
            if len(t)==5 and area_m>90:
                (ax,ay),(bx,by),(cxq,cyq),(dxq,dyq)=t[0],t[1],t[2],t[3]
                lab=math.hypot(bx-ax,by-ay); lbc=math.hypot(cxq-bx,cyq-by)
                if lab>=lbc: p1,p2,q1,q2=(ax,ay),(bx,by),(dxq,dyq),(cxq,cyq); wid=lbc
                else: p1,p2,q1,q2=(bx,by),(cxq,cyq),(ax,ay),(dxq,dyq); wid=lab
                step=max(6.0,3.0*C)
                nh=int(wid/step)
                for k in range(1,nh+1):
                    u=k/(nh+1)
                    x1h=p1[0]+(q1[0]-p1[0])*u; y1h=p1[1]+(q1[1]-p1[1])*u
                    x2h=p2[0]+(q2[0]-p2[0])*u; y2h=p2[1]+(q2[1]-p2[1])*u
                    dr.line([(x1h,y1h),(x2h,y2h)],fill=shade(roof,0.88 if k%2 else 1.09),width=1)
            if area_m>150:
                cxr=sum(p[0] for p in t[:-1])/(len(t)-1); cyr=sum(p[1] for p in t[:-1])/(len(t)-1)
                ins=[]
                for p in t[:-1]:
                    vx,vy=cxr-p[0],cyr-p[1]
                    dd=max(1e-6,math.hypot(vx,vy))
                    f=min(0.12,3.2/dd)
                    ins.append((p[0]+vx*f,p[1]+vy*f))
                dr.line(ins+[ins[0]],fill=shade(roof,1.07),width=1)
            if area_m>120:
                hh=h01('cl',b['ref'])
                xs=[p[0] for p in t]; ys=[p[1] for p in t]
                rx0,rx1,ry0,ry1=min(xs),max(xs),min(ys),max(ys)
                ncl=min(5,int(area_m/120)+1)
                for k in range(ncl):
                    u=h01('clu',b['ref']+str(k)); v=h01('clv',b['ref']+str(k))
                    if u<0.15 or u>0.85 or v<0.15 or v>0.85: continue
                    px=rx0+(rx1-rx0)*u; py=ry0+(ry1-ry0)*v
                    w=2.2+h01('clw',b['ref']+str(k))*3.2
                    kind=h01('clk',b['ref']+str(k))
                    if kind<0.14:  # solar panel
                        dr.rectangle([px-w*1.4,py-w*0.55,px+w*1.4,py+w*0.55],fill=(58,84,110))
                        dr.line([(px-w*1.4,py),(px+w*1.4,py)],fill=(96,128,158),width=1)
                    elif kind<0.34:  # chimney
                        dr.rectangle([px-1.2,py-5.0,px+1.2,py],fill=shade(roof,0.72))
                        dr.line([(px-1.6,py-5.0),(px+1.6,py-5.0)],fill=shade(roof,1.12),width=1)
                    else:  # AC unit / bulkhead
                        dr.rectangle([px-w,py-w*0.6,px+w,py+w*0.6],fill=shade(roof,0.78))
                        dr.rectangle([px-w,py-w*0.6-1.2,px+w,py+w*0.6-1.2],fill=shade(roof,1.10))
        if b.get('cath'):
            # verified against es.wikipedia + Commons facade photo: warm sandstone exterior,
            # square bell tower with belfry arches dominating the main facade, balustraded
            # terrace; small stone dome only over the Virgen de los Llanos apse chapel.
            SAND=(224,198,158)
            cxr=sum(p[0] for p in t[:-1])/(len(t)-1); cyr=sum(p[1] for p in t[:-1])/(len(t)-1)
            # stone dome over the apse chapel (documented; NOT blue)
            dr.ellipse([cxr-12,cyr-7,cxr+12,cyr+7],fill=(188,158,118))
            dr.ellipse([cxr-10,cyr-16,cxr+10,cyr+4],fill=(206,176,136))
            dr.ellipse([cxr-6,cyr-17,cxr+1,cyr-8],fill=(226,198,158))
            dr.rectangle([cxr-1.6,cyr-20,cxr+1.6,cyr-15],fill=(188,158,118))
            # square bell tower, tall and dominant, rising from the WEST end of the
            # cathedral footprint (real tower stands by the west facade)
            gx,gy=scr(*b['tower_en']); gx-=ox; gy-=oy
            bx,by=gx,gy
            # proportions taken from the verified facade photo: stout square campanile integrated in the
            # main facade, about 1.7x the facade height, roughly facade-wide; one belfry arch with bell
            tw=20; th_=130
            dr.rectangle([bx-tw,by-th_,bx+tw,by],fill=SAND)
            dr.rectangle([bx-tw,by-th_,bx-tw+4,by],fill=shade(SAND,0.80))
            dr.rectangle([bx+tw-4,by-th_,bx+tw,by],fill=shade(SAND,1.06))
            for yy in (by-th_*0.30,by-th_*0.56):
                dr.line([(bx-tw,yy),(bx+tw,yy)],fill=shade(SAND,0.88),width=2)
            # rose window on the facade below the belfry
            dr.ellipse([bx-8,by-th_*0.46-8,bx+8,by-th_*0.46+8],fill=shade(SAND,0.80))
            dr.ellipse([bx-5,by-th_*0.46-5,bx+5,by-th_*0.46+5],fill=(120,150,176))
            # belfry: one arched opening with the bell, balcony balustrade below
            dr.rectangle([bx-5,by-th_+16,bx+5,by-th_+34],fill=(52,44,38))
            dr.ellipse([bx-5,by-th_+11,bx+5,by-th_+21],fill=(52,44,38))
            dr.rectangle([bx-3,by-th_+22,bx+3,by-th_+29],fill=(110,98,86))
            dr.rectangle([bx-8,by-th_+34,bx+8,by-th_+37],fill=shade(SAND,1.10))
            # cornice + two small corner pinnacles
            dr.rectangle([bx-tw-2.5,by-th_-3,bx+tw+2.5,by-th_],fill=shade(SAND,1.12))
            dr.line([(bx-tw-1,by-th_-9),(bx-tw-1,by-th_-3)],fill=shade(SAND,1.1),width=2)
            dr.line([(bx+tw+1,by-th_-9),(bx+tw+1,by-th_-3)],fill=shade(SAND,1.1),width=2)
    # clip everything to the ground diamond (no stray lines past the painting)
    cmask=Image.new('L',(TS,TS),0)
    ImageDraw.Draw(cmask).polygon([(x-ox,y-oy) for x,y in gp],fill=255)
    im.putalpha(Image.composite(im.getchannel('A'),Image.new('L',(TS,TS),0),cmask))
    return im

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='test':
        # tile containing the cathedral (0,0)m
        cx,cy=scr(0,0); ctx,cty=int(cx//TS),int(cy//TS)
        os.makedirs(f'{BASE}/test',exist_ok=True)
        for ty in range(cty-2,cty+2):
            for tx in range(ctx-1,ctx+2):
                render_tile(tx,ty).save(f'{BASE}/test/{tx}_{ty}.webp',quality=85)
        print('test tiles around',ctx,cty)
    else:
        os.makedirs(f'{BASE}/site/painted/{TOP}',exist_ok=True)
        tx0,ty0,tx1,ty1=map(int,sys.argv[2:6])
        n=0
        for ty in range(ty0,ty1):
            for tx in range(tx0,tx1):
                _p=f'{BASE}/site/painted/{TOP}/{tx}_{ty}.webp'
                if os.environ.get('SKIP') and os.path.exists(_p) and os.path.getmtime(_p)>os.path.getmtime(f'{BASE}/stamp'): continue
                im=render_tile(tx,ty)
                if im.getbbox() is None: continue
                im.save(f'{BASE}/site/painted/{TOP}/{tx}_{ty}.webp',quality=80,method=4)
                n+=1
                if n%25==0: print('tile',n,flush=True)
        print('done',n)
