import math, os, subprocess, numpy as np, urllib.request, json, io
from PIL import Image, ImageFilter
from scipy import ndimage
REPO='/tmp/tiny-albacete'
DONOR='f7651d32da064384ee3d1ad740cdab6ab38c4c39'
PAD=24
REGIONS={33:(13831,5662,1552,401),35:(10247,5715,528,348),40:(12295,6227,1040,348),42:(14859,6231,520,340),44:(10247,6739,528,348),45:(5607,6747,964,348)}
angle=math.radians(-154)
A=np.array([[-math.sin(angle),math.cos(angle)],[math.sin(.6)*math.cos(angle),math.sin(.6)*math.sin(angle)]])
focus=np.array([-123.2408167310922,-243.6981380554508]);m=472/2048
B=np.linalg.inv(A)*472
offset=np.linalg.solve(A,[-1536*m,-1024*m-9])+focus
MINX,MINY=-4.5,-1.25
E0,N0=599085.806441913,4316910.931406423
M=B/2048.0
off2=offset+np.array([E0,N0])+B@np.array([MINX,MINY])
def tile(c,r,donor=False):
    p=f'ilustrado/atlas_files/15/{c}_{r}.webp'
    if donor:
        cp=subprocess.run(['git','-C',REPO,'show',f'{DONOR}:{p}'],capture_output=True)
        if cp.returncode!=0: return None
        return Image.open(io.BytesIO(cp.stdout)).convert('RGB')
    fp=f'{REPO}/{p}'
    return Image.open(fp).convert('RGB') if os.path.exists(fp) else None
def assemble(box,donor=False):
    x,y,w,h=box
    im=Image.new('RGB',(w,h),(255,255,255))
    for c in range(x//512,(x+w-1)//512+1):
        for r in range(y//512,(y+h-1)//512+1):
            t=tile(c,r,donor)
            if t is None: continue
            sx=int(c>0);sy=int(r>0)
            im.paste(t.crop((sx,sy,sx+512,sy+512)),(c*512-x,r*512-y))
    return im
def pnoa(box):
    x,y,w,h=box
    corners=[M@np.array([px,py])+off2 for px in (x,x+w) for py in (y,y+h)]
    le=min(c[0] for c in corners);he=max(c[0] for c in corners);ln=min(c[1] for c in corners);hn=max(c[1] for c in corners)
    Wp,Hp=int((he-le)/0.25),int((hn-ln)/0.25)
    url=f"https://www.ign.es/wms-inspire/pnoa-ma?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&LAYERS=OI.OrthoimageCoverage&STYLES=&CRS=EPSG:25830&BBOX={le},{ln},{he},{hn}&WIDTH={Wp}&HEIGHT={Hp}&FORMAT=image/jpeg"
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    raw=Image.open(urllib.request.urlopen(req,timeout=90)).convert('RGB')
    base=M@np.array([x,y])+off2
    a=M[0,0]/0.25;b=M[0,1]/0.25;c=(base[0]-le)/0.25
    d=-M[1,0]/0.25;e=-M[1,1]/0.25;f=(hn-base[1])/0.25
    return raw.transform((w,h),Image.AFFINE,(a,b,c,d,e,f),Image.BICUBIC)
stats={}
for rid,box0 in REGIONS.items():
    x,y,w,h=box0; box=(x-PAD,y-PAD,w+2*PAD,h+2*PAD)
    cur=assemble(box); don=assemble(box,donor=True)
    ca=np.array(cur).astype(np.int16); da=np.array(don).astype(np.int16)
    diff=(np.abs(ca-da).max(axis=2)>12)
    dil=ndimage.binary_dilation(diff,iterations=3)
    lab,n=ndimage.label(dil)
    # keep components that intersect the inner box (the audit rectangle)
    inner=np.zeros(dil.shape,bool); inner[PAD:PAD+h,PAD:PAD+w]=True
    keep=set(np.unique(lab[inner&dil]))-{0}
    support=np.isin(lab,list(keep))
    # feather 1.5px
    mask=Image.fromarray((support*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))
    cand=Image.composite(don,cur,mask)
    os.makedirs(f'r{rid}',exist_ok=True)
    cand.save(f'r{rid}/candidate.png'); mask.save(f'{rid if False else ""}r{rid}/mask.png')
    cur.save(f'r{rid}/current.png'); don.save(f'r{rid}/donor.png')
    pn=pnoa(box)
    W,H=box[2],box[3]
    tri=Image.new('RGB',(W*3+20,H),(255,255,255))
    tri.paste(cur,(0,0));tri.paste(cand,(W+10,0));tri.paste(pn,(2*W+20,0))
    tri.save(f'r{rid}/tri.png')
    stats[rid]={'box':box,'diff_px':int(diff.sum()),'support_px':int(support.sum()),'components':len(keep)}
    print(rid,stats[rid])
json.dump(stats,open('stats.json','w'),indent=1)
