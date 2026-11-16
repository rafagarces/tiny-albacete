#!/usr/bin/env python3
"""Parse Catastro INSPIRE bulk GML (building + buildingpart) -> compact jsonl."""
import re, json, math, sys
LAT0, LON0 = 38.9956, -1.8558
MLAT = 111132.954 - 559.822*math.cos(math.radians(2*LAT0)) + 1.175*math.cos(math.radians(4*LAT0))
MLON = 111320*math.cos(math.radians(LAT0))
def to_en(lat,lon): return ((lon-LON0)*MLON,(lat-LAT0)*MLAT)

# UTM 30N (WGS84) -> relative meters from cathedral
def latlon_to_utm30(lat,lon):
    a=6378137.0; f=1/298.257223563; e2=f*(2-f); ep2=e2/(1-e2)
    k0=0.9996; lon0=math.radians(-3.0)
    la=math.radians(lat); lo=math.radians(lon)
    N=a/math.sqrt(1-e2*math.sin(la)**2); T=math.tan(la)**2; C=ep2*math.cos(la)**2; A=math.cos(la)*(lo-lon0)
    M=a*((1-e2/4-3*e2**2/64-5*e2**3/256)*la-(3*e2/8+3*e2**2/32+45*e2**3/1024)*math.sin(2*la)+(15*e2**2/256+45*e2**3/1024)*math.sin(4*la)-(35*e2**3/3072)*math.sin(6*la))
    E=k0*N*(A+(1-T+C)*A**3/6+(5-18*T+T*T+72*C-58*ep2)*A**5/120)+500000
    NN=k0*(M+N*math.tan(la)*(A*A/2+(5-T+9*C+4*C*C)*A**4/24+(61-58*T+T*T+600*C-330*ep2)*A**6/720))
    return E,NN
E0,N0=latlon_to_utm30(LAT0,LON0)
def utm_to_en(north,east): return (east-E0, north-N0)

FM=re.compile(r'<gml:featureMember>(.*?)</gml:featureMember>',re.S)
POS=re.compile(r'<gml:posList[^>]*>([^<]+)</gml:posList>')
LID=re.compile(r'<base:localId>([^<]+)</base:localId>')
FLOORS=re.compile(r'<bu-ext2d:numberOfFloorsAboveGround>(\d+)<')
USE=re.compile(r'<bu-ext2d:currentUse>([^<]+)<')

def stream_members(path):
    buf=''
    with open(path,encoding='utf-8',errors='replace') as f:
        while True:
            chunk=f.read(1<<23)
            if not chunk: break
            buf+=chunk
            parts=buf.split('</gml:featureMember>')
            buf=parts.pop()
            for p in parts:
                yield p+ '</gml:featureMember>'
    if buf.strip(): yield buf

def parse(path,want_use):
    out=[]
    for m in stream_members(path):
        lid=LID.search(m); pm=POS.search(m)
        if not lid or not pm: continue
        nums=pm.group(1).split()
        pts=[]
        ok=True
        for i in range(0,len(nums)-1,2):
            try: lat=float(nums[i]); lon=float(nums[i+1])
            except ValueError: ok=False; break
            if abs(lat)>10000:  # UTM 25830: (northing, easting)
                pts.append(utm_to_en(lon,lat))  # raw pair is (easting, northing)
            else:
                pts.append(to_en(lat,lon))
        if not ok or len(pts)<4: continue
        if pts[0]!=pts[-1]: pts.append(pts[0])
        sa=sum(pts[i][0]*pts[i+1][1]-pts[i+1][0]*pts[i][1] for i in range(len(pts)-1))
        if sa<0: pts=[pts[0]]+pts[1:][::-1]
        area=abs(sa)/2
        fm=FLOORS.search(m); floors=int(fm.group(1)) if fm else 0
        use=''
        if want_use:
            um=USE.search(m); use=um.group(1) if um else ''
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        out.append({'id':lid.group(1),'pts':[[round(x,1),round(y,1)] for x,y in pts],
                    'floors':floors,'use':use,'area':round(area,1)})
    return out

if __name__=='__main__':
    parts=parse('/tmp/bu_gml/A.ES.SDGC.BU.02900.buildingpart.gml',False)
    print('parts',len(parts))
    with open('bu_parts.json','w') as f: json.dump(parts,f)
    blds=parse('/tmp/bu_gml/A.ES.SDGC.BU.02900.building.gml',True)
    print('buildings',len(blds))
    with open('bu_blds.json','w') as f: json.dump(blds,f)
