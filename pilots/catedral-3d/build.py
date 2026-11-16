"""Original partial 3D study. Dimensions/relief placement ESTIMATED from open sources.
No Google data. Source dates and limits in README.md. Runs offline with Pillow/numpy.
"""
from pathlib import Path
import math,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).parent
faces=[]
stone='#cbb593';light='#dfc9a5';dark='#a68f70';trim='#e4ceb0';roof='#b36e50';glass='#304851';shadow='#3a3c38'
def face(v,c,kind='estimated'):
 faces.append({'v':[list(map(float,p)) for p in v],'c':c,'kind':kind})
def box(x0,x1,y0,y1,z0,z1,c=stone,kind='estimated'):
 a=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0)];b=[(x,y,z1) for x,y,z in a]
 face(b,c,kind)
 for i in range(4):face([a[i],a[(i+1)%4],b[(i+1)%4],b[i]],c,kind)
def plane(u,v,z,side):
 return (u,-18.42-v,z) if side=='south-low' else ((u,-14.12-v,z) if side=='south' else (-24.12-v,u,z))
def patch(pts,c,side,offset=0,kind='photo-feature-estimated-position'):
 face([plane(u,offset,z,side) for u,z in pts],c,kind)
def arch(u,z,w,h,side,c=glass,offset=.03):
 # Rounded arch opening, dimensions inferred from perspective photographs.
 r=w/2;spring=z+h-r
 pts=[(u-r,z),(u+r,z),(u+r,spring)]
 pts += [(u+r*math.cos(t),spring+r*math.sin(t)) for t in np.linspace(0,math.pi,17)]
 patch(pts,c,side,offset)
def ring(u,z,outer,inner,side,c=trim,offset=.1,n=40):
 for i in range(n):
  a,b=2*math.pi*i/n,2*math.pi*(i+1)/n
  patch([(u+outer*math.cos(a),z+outer*math.sin(a)),(u+outer*math.cos(b),z+outer*math.sin(b)),(u+inner*math.cos(b),z+inner*math.sin(b)),(u+inner*math.cos(a),z+inner*math.sin(a))],c,side,offset)
# Main nave. Eaves/ridge are rounded estimates informed by 2017 class6 heights.
box(-24,23,-14,14,0,24)
# Roof actual 3D pitched planes, not a photo or sprite.
face([(-24,-14,24),(23,-14,24),(23,0,32),(-24,0,32)],roof)
face([(-24,0,32),(23,0,32),(23,14,24),(-24,14,24)],'#945e4a')
face([(-24,-14,24),(-24,14,24),(-24,0,32)],stone)
face([(23,-14,24),(23,0,32),(23,14,24)],dark,'unknown-simplified')
# Stone courses are stylistic surface treatment, not an archaeological claim.
for z in np.arange(2,23,1.3):
 patch([(-23,z),(22,z),(22,z+.045),(-23,z+.045)],'#bea789','south',.02,'artistic-material')
# Documented south lower aisle and roof from lateral2026 photograph.
# Depth, heights and roof transitions are estimates, not a measured section.
box(-24,23,-18.3,-14.0,0,11.8)
face([(-24,-18.5,11.9),(23,-18.5,11.9),(23,-13.95,13.2),(-24,-13.95,13.2)],roof,'photo-feature-estimated-position')
face([(-24,-18.5,11.9),(-24,-13.95,13.2),(-24,-13.95,11.8)],stone,'photo-feature-estimated-position')
face([(23,-18.5,11.9),(23,-13.95,13.2),(23,-13.95,11.8)],stone,'photo-feature-estimated-position')
# Slightly raised south portal shed roof, dimensions inferred from the photo.
# The photo does not establish a separate gabled pediment: do not invent one.
face([(-4.8,-18.65,11.8),(4.8,-18.65,11.8),(4.8,-18.65,12.8),(-4.8,-18.65,12.8)],stone,'photo-feature-estimated-position')
face([(-4.8,-18.7,12.9),(4.8,-18.7,12.9),(4.8,-14,14.2),(-4.8,-14,14.2)],roof,'photo-feature-estimated-position')
for x in [-4.8,4.8]:
 face([(x,-18.7,11.8),(x,-18.7,12.9),(x,-14,14.2),(x,-14,11.8)],stone,'estimated-roof-junction')
# South face: three upper arched windows and doorway observed in2026 source.
for u in [-11,1,13]:
 arch(u,18.5,2.9,4.9,'south',trim,.08);arch(u,18.9,2.15,4.1,'south',glass,.1)
 patch([(u-.04,18.9),(u+.04,18.9),(u+.04,22.3),(u-.04,22.3)],'#9f9278','south',.13)
for u in [-18,-5,7,20]:
 box(u-.5,u+.5,-15.5,-13.9,0,24.4,dark)
 box(u-.76,u+.76,-15.72,-13.7,0,1.4,light)
 box(u-.65,u+.65,-15.7,-13.7,23.6,24.7,trim)
for w,h in [(7.6,10),(6.8,9.6),(6,9.1),(5.15,8.6)]:arch(0,0,w,h,'south-low',trim if w in [7.6,6] else dark,.22+(7.6-w)*.02)
arch(0,.2,4.4,7.8,'south-low',shadow,.4)
# Door slats are artistic material, not claims of exact board count.
for u in np.arange(-1.9,2,.4):patch([(u,.4),(u+.035,.4),(u+.035,5.6),(u,5.6)],'#736754','south-low',.42,kind='artistic-material')
for u in [-17,-9,9,18]:arch(u,5,1.1,2.3,'south-low',shadow,.2)
box(-24,23,-14.5,-13.8,23.4,24.3,trim)
# Stylised roof tile courses, visual material only. Not surveyed tile count.
for yy in np.arange(-13.5,0,.85):
 z=32+yy*(8/14)+.035
 face([(-24,yy,z),(23,yy,z),(23,yy+.045,z+.045*8/14),(-24,yy+.045,z+.045*8/14)],'#9d6049','artistic-material')
for xx in np.arange(-23.5,23,1.4):
 for yy in np.arange(-13,0,2.55):
  z=32+yy*(8/14)+.05
  face([(xx,yy,z),(xx+.045,yy,z),(xx+.045,yy+.55,z+.55*8/14),(xx,yy+.55,z+.55*8/14)],'#c4805c','artistic-material')
# West front: tower behind pediment with rose, Gothic entrance, flanking piers.
box(-24,-16,-4.5,4.5,24,38.5,light)
for z in [27,37.5,38.5]:box(-24.5,-15.5,-5,5,z,z+.65,trim)
# tower west-facing arch, on plane u=-24.
arch(0,29,3.4,6,'west',dark,.24);arch(0,29.4,2.6,5.1,'west',shadow,.29)
patch([(-2,28),(2,28),(2,28.65),(-2,28.65)],trim,'west',.34)
for y in [-3.7,3.7]:box(-24.7,-23.9,y-.28,y+.28,24.1,37.4,trim)
for y in [-11,11]:
 box(-25.4,-23.8,y-.55,y+.55,0,25,dark)
 box(-25.8,-23.5,y-.85,y+.85,24.4,25.3,trim)
# Rose: real source feature, tracery interpretation and dimensions estimated.
ring(0,20.6,3.15,2.65,'west',trim,.35)
patch([(3*math.cos(t),20.6+3*math.sin(t)) for t in np.linspace(0,2*math.pi,48)],glass,'west',.4)
ring(0,20.6,3.15,2.86,'west',trim,.44)
ring(0,20.6,1.8,1.56,'west',trim,.47)
for i in range(12):
 t=2*math.pi*i/12
 ring(2.25*math.cos(t),20.6+2.25*math.sin(t),.61,.4,'west',light,.48,n=12)
# Pointed Gothic portal, source geometry interpreted.
for width,top in [(11.5,15.4),(10.6,14.9),(9.7,14.4),(8.8,13.9),(7.9,13.4)]:
 h=width/2
 pts=[(-h,1),(h,1),(h,8.2),(h*.67,11.4),(0,top),(-h*.67,11.4),(-h,8.2)]
 patch(pts,trim if int(width*10)%2 else dark,'west',.6+(11.5-width)*.025)
patch([(-3.6,1),(3.6,1),(3.6,7),(2.8,9),(0,12.3),(-2.8,9),(-3.6,7)],shadow,'west',.8)
patch([(-2.9,1),(2.9,1),(2.9,5.6),(-2.9,5.6)],'#536363','west',.85)
# Front stair plinth, clear estimate of dimensions.
for i in range(6):box(-29+i*.7,-24,-10+i*.25,10-i*.25,i*.32,(i+1)*.32,light)
# Low semicircular side volumes visible west-front source, coarse estimated masses.
for sign in [-1,1]:
 cx=-24;cy=sign*10.5;r=4.5
 pts=[(cx+r*math.cos(a),cy+r*math.sin(a)) for a in np.linspace(math.pi/2,3*math.pi/2,15)]
 for k in range(len(pts)-1):
  a,b=pts[k],pts[k+1]
  face([(a[0],a[1],0),(b[0],b[1],0),(b[0],b[1],16),(a[0],a[1],16)],dark)
 face([(x,y,16.1) for x,y in pts],roof)
 for a in np.linspace(math.pi/2+.22,3*math.pi/2-.22,5):
  da=.105
  face([(cx+(r+.03)*math.cos(t),cy+(r+.03)*math.sin(t),z) for t,z in [(a-da,12),(a+da,12),(a+da,15.5),(a-da,15.5)]],shadow,'photo-feature-estimated-position')
# Cornice and tower decorative pinnacles, coarse not measured.
for x in [-24,-16]:
 for y in [-4.5,4.5]:box(x-.13,x+.13,y-.13,y+.13,39.1,39.7,trim)
# OBJ with per-material colours for ordinary 3D applications.
colors=list(dict.fromkeys(f['c'] for f in faces));mtl=[]
for i,c in enumerate(colors):
 rgb=[int(c[j:j+2],16)/255 for j in (1,3,5)];mtl += [f'newmtl m{i}', 'Kd '+' '.join(map(str,rgb))]
(P/'catedral.mtl').write_text('\n'.join(mtl))
obj=['# Estimated partial Cathedral model. See README.', 'mtllib catedral.mtl'];idx=1
for f in faces:
 obj.append('usemtl m'+str(colors.index(f['c'])))
 for v in f['v']:obj.append('v '+' '.join(map(str,v)))
 obj.append('f '+' '.join(str(idx+i) for i in range(len(f['v']))));idx+=len(f['v'])
(P/'catedral.obj').write_text('\n'.join(obj))
(P/'model.json').write_text(json.dumps(faces,separators=(',',':')))
# Shared deterministic orthographic renderer. Actual mesh polygons, depth-sorted.
def render(angle=-2.3,el=.55,size=(1400,1100),scale=15):
 W,H=size;im=Image.new('RGB',size,'#dce1d5');d=ImageDraw.Draw(im)
 ca,sa=math.cos(angle),math.sin(angle)
 def proj(v):
  x,y,z=v;return ((-sa*x+ca*y)*scale+W/2,(math.sin(el)*(ca*x+sa*y)-math.cos(el)*z)*scale+H*.77)
 # platform and ground shadow, no claim of surveyed plaza.
 ground=[(-38,-27,-.4),(35,-27,-.4),(35,29,-.4),(-38,29,-.4)]
 d.polygon([proj(p) for p in ground],fill='#b6bfad')
 d.polygon([proj((x+7,y+9,0)) for x,y,z in ground],fill='#c8d0c1')
 def depth(f):return sum(math.cos(el)*(ca*v[0]+sa*v[1])+math.sin(el)*v[2] for v in f['v'])/len(f['v'])
 pixels=np.array(im);zb=np.full((H,W),-1e9,dtype=float)
 for f in faces:
  v=np.array(f['v']);n=np.cross(v[1]-v[0],v[2]-v[0]);n=n/(np.linalg.norm(n) or 1)
  brightness=.78+.22*abs(n@np.array([-.6,-.45,.65]))
  rgb=tuple(min(255,int(int(f['c'][i:i+2],16)*brightness)) for i in (1,3,5))
  vv=np.array([[*proj(p),math.cos(el)*(ca*p[0]+sa*p[1])+math.sin(el)*p[2]] for p in v])
  for k in range(1,len(vv)-1):
   A,B,C=vv[[0,k,k+1]]
   xmin=max(0,int(min(A[0],B[0],C[0])));xmax=min(W-1,int(max(A[0],B[0],C[0]))+1)
   ymin=max(0,int(min(A[1],B[1],C[1])));ymax=min(H-1,int(max(A[1],B[1],C[1]))+1)
   den=(B[1]-C[1])*(A[0]-C[0])+(C[0]-B[0])*(A[1]-C[1])
   if abs(den)<.00001 or xmax<xmin or ymax<ymin:continue
   xx,yy=np.meshgrid(np.arange(xmin,xmax+1)+.5,np.arange(ymin,ymax+1)+.5)
   w0=((B[1]-C[1])*(xx-C[0])+(C[0]-B[0])*(yy-C[1]))/den
   w1=((C[1]-A[1])*(xx-C[0])+(A[0]-C[0])*(yy-C[1]))/den;w2=1-w0-w1
   zz=w0*A[2]+w1*B[2]+w2*C[2]
   zzb=zb[ymin:ymax+1,xmin:xmax+1];mask=(w0>=0)&(w1>=0)&(w2>=0)&(zz>zzb)
   zzb[mask]=zz[mask];pixels[ymin:ymax+1,xmin:xmax+1][mask]=rgb
 im=Image.fromarray(pixels)
 return im
im=render();im.save(P/'isometric.png')
# Pixel-art material study keeps mesh projection, not photo filtering.
px=render(size=(700,550),scale=7.5).resize((1400,1100),Image.Resampling.NEAREST);px.save(P/'isometric-pixel.png')
print(len(faces),'faces generated',P)
