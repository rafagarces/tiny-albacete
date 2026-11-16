import re, glob, math, hashlib
LAT0, LON0 = 38.9956, -1.8558
MLAT = 111132.954 - 559.822*math.cos(math.radians(2*LAT0)) + 1.175*math.cos(math.radians(4*LAT0))
MLON = 111320*math.cos(math.radians(LAT0))
def to_en(lat,lon): return ((lon-LON0)*MLON,(lat-LAT0)*MLAT)
def h01(*a):
    return int(hashlib.md5('|'.join(map(str,a)).encode()).hexdigest()[:8],16)/0xffffffff

FM = re.compile(r'<gml:featureMember>(.*?)</gml:featureMember>', re.S)
POS = re.compile(r'<gml:posList[^>]*>(.*?)</gml:posList>', re.S)
GID = re.compile(r'<bu-ext2d:Building gml:id="([^"]+)"')
FLOORS = re.compile(r'<bu-ext2d:numberOfFloorsAboveGround>(\d+)<')
USE = re.compile(r'<bu-ext2d:currentUse>([^<]+)<')

def height_for(use, area, e, n, ref):
    # distance-based center factor (city core taller)
    d = math.hypot(e+300, n-100)
    central = max(0.0, 1.0 - d/3200.0)
    r = h01('h', ref)
    if use.startswith('3_industrial'): return 6.5 + 2*r
    if use.startswith('4_2_retail'): return 8 + 3*r
    if use.startswith('4_3_publicServices'): return 9 + 4*r
    if use.startswith('2_agriculture'): return 4 + 1.5*r
    # residential / other
    base = 7.5 + 10.5*central
    return base + r*4.0

def load_buildings():
    out=[]; seen=set()
    for fn in glob.glob('/tmp/cat/c_*.xml'):
        txt=open(fn,encoding='iso-8859-1',errors='replace').read()
        for m in FM.finditer(txt):
            chunk=m.group(1)
            gm=GID.search(chunk)
            ref=gm.group(1) if gm else None
            if ref:
                if ref in seen: continue
                seen.add(ref)
            pm=POS.search(chunk)
            if not pm: continue
            nums=pm.group(1).split()
            pts=[]
            for i in range(0,len(nums)-1,2):
                try: lat=float(nums[i]); lon=float(nums[i+1])
                except ValueError: break
                pts.append(to_en(lat,lon))
            if len(pts)<4: continue
            if pts[0]!=pts[-1]: pts.append(pts[0])
            sa=sum(pts[i][0]*pts[i+1][1]-pts[i+1][0]*pts[i][1] for i in range(len(pts)-1))
            if sa<0: pts=[pts[0]]+pts[1:][::-1]
            fm=FLOORS.search(chunk)
            floors=int(fm.group(1)) if fm else 0
            um=USE.search(chunk); use=um.group(1) if um else '1_residential'
            xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
            area=abs(sum(pts[i][0]*pts[i+1][1]-pts[i+1][0]*pts[i][1] for i in range(len(pts)-1)))/2
            e=(min(xs)+max(xs))/2; n=(min(ys)+max(ys))/2
            h=(floors*3.0+2.0) if floors>0 else height_for(use,area,e,n,ref or fn+str(len(out)))
            h=max(3.0,min(h,60.0))
            out.append({'pts':pts,'h':h,'use':use,'ref':ref or str(len(out)),'area':area})
    return out

if __name__=='__main__':
    b=load_buildings()
    import collections
    print('buildings:',len(b))
    print(collections.Counter(x['use'] for x in b).most_common())
    hs=[x['h'] for x in b]; print('avg h:',round(sum(hs)/len(hs),1),'max',max(hs))
