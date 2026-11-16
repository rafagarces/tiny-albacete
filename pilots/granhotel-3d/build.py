"""Gran Hotel: partial street elevations from free photos and official description.
See README for evidence and limits. Dimensions/details are estimates.
"""
import math,json
from pathlib import Path
P=Path(__file__).parent
faces=[]
stone='#c5beaa';trim='#e4dfcb';green='#9fb96e';glass='#405354';wood='#795a3c';dark='#857e6d'
def face(v,c,kind='photo-feature-estimated-geometry'):faces.append({'v':v,'c':c,'kind':kind})
def box(a,b,c,d,z,Z,col,kind='photo-feature-estimated-geometry'):
 q=[(a,c,z),(b,c,z),(b,d,z),(a,d,z)];Q=[(x,y,Z)for x,y,_ in q]
 face(Q,col,kind)
 for i in range(4):face([q[i],q[(i+1)%4],Q[(i+1)%4],Q[i]],col,kind)
def patch(pts,col,y=-.03,kind='photo-feature-estimated-geometry'):face([[x,y,z]for x,z in pts],col,kind)
def arch(x,z,w,h,col,y=-.05):
 r=w/2;s=z+h-r;pts=[(x-r,z),(x+r,z),(x+r,s)]+[(x+r*math.cos(t*math.pi/18),s+r*math.sin(t*math.pi/18))for t in range(19)]
 patch(pts,col,y)
def circle(x,z,r,col,y=-.06):patch([(x+r*math.cos(i*math.tau/24),z+r*math.sin(i*math.tau/24))for i in range(24)],col,y)
def ring(x,z,r,R,col,y):
 for i in range(20):
  a=i*math.tau/20;b=(i+1)*math.tau/20
  patch([(x+r*math.cos(a),z+r*math.sin(a)),(x+r*math.cos(b),z+r*math.sin(b)),(x+R*math.cos(b),z+R*math.sin(b)),(x+R*math.cos(a),z+R*math.sin(a))],col,y)
def spire(x,z,h=1.6,y=-.3):
 box(x-.12,x+.12,y-.12,y+.12,z,z+h*.72,trim)
 face([(x-.2,y-.2,z+h*.65),(x+.2,y-.2,z+h*.65),(x,y,z+h)],trim)
 face([(x+.2,y-.2,z+h*.65),(x+.2,y+.2,z+h*.65),(x,y,z+h)],stone)
 box(x-.23,x+.23,y-.17,y+.17,z+.15,z+.28,trim)


cream='#dfd2b1';trim='#eaddbd';pane='#748b8d';iron='#575d55'
# Two street faces only. Measured lengths follow Catastro, heights are estimates.
def elevation(W,ends):
 box(0,W,-.1,.15,0,18.6,cream)
 for z,Z in [(0,.45),(4.1,4.35),(8,8.2),(11.7,11.9),(15.4,15.65),(18.5,18.85)]:box(-.15,W+.15,-.32,.1,z,Z,trim)
 # Three central single balcony bays observed on the Altozano front;
 # same organization described in the official heritage inventory.
 for x in [W*.28,W*.50,W*.72]:
  for z in [4.5,8.4,12.1]:
   box(x-.74,x+.74,-.2,-.1,z,z+2.65,trim);box(x-.57,x+.57,-.24,-.2,z+.1,z+2.5,pane)
   box(x-.025,x+.025,-.28,-.24,z+.1,z+2.5,trim)
   box(x-.95,x+.95,-.43,-.08,z+2.7,z+2.88,trim)
   if z==12.1:
    box(x-.9,x+.9,-.75,.1,z-.12,z,trim)
    for i in range(8):box(x-.85+i*.24,x-.82+i*.24,-.8,-.73,z,z+.8,iron)
    box(x-.9,x+.9,-.81,-.73,z+.78,z+.84,iron)
 # First/second continuous balconies, masonry then iron; no copied small ornament.
 for z in [4.4,8.3]:
  box(2,W-2,-.75,.15,z-.15,z,trim)
  for i in range(int((W-4)/.32)):
   x=2+i*.32;box(x,x+.055,-.81,-.73,z,z+.82,trim if z==4.4 else iron)
  box(2,W-2,-.83,-.73,z+.8,z+.9,trim if z==4.4 else iron)
 # Three paired attic openings between entrance axes, explicitly visible in photos.
 for x in [W*.28,W*.50,W*.72]:
  arch(x,16.0,3.0,2.55,trim,-.20)
  for X in [x-.65,x+.65]:
   arch(X,16.1,1.12,2.16,pane,-.25)
   box(X-.025,X+.025,-.3,-.25,16.2,17.6,trim)
  box(x-.08,x+.08,-.32,-.22,16.0,17.8,trim)
  # Original smooth crest silhouette; exact foliage and heads deliberately omitted.
  pts=[(x-1.9,18.7),(x-1.9,19.0),(x-1.1,19.5),(x,19.9),(x+1.1,19.5),(x+1.9,19.0),(x+1.9,18.7)]
  patch(pts,trim,-.14)
 # Narrow entrance axes at the ends. Visible paired attic and lower balcony forms.
 for x in ends:
  for z in [4.5,8.4,12.1]:
   box(x-.9,x+.9,-.28,-.1,z,z+2.8,trim)
   box(x-.65,x+.65,-.32,-.28,z+.15,z+2.6,pane)
  arch(x,15.9,2.85,2.8,trim,-.32)
  for X in [x-.6,x+.6]:arch(X,16.05,1.0,2.15,pane,-.37)
  patch([(x-2,18.6),(x-1.8,19.5),(x-1.1,19.8),(x,21.0),(x+1.1,19.8),(x+1.8,19.5),(x+2,18.6)],trim,-.31)
  arch(x,.3,2.25,3.6,'#686955',-.34)

def register(A,B,ends):
 W=math.dist(A,B);start=len(faces);elevation(W,ends);a=math.atan2(B[1]-A[1],B[0]-A[0]);c,s=math.cos(a),math.sin(a)
 for f in faces[start:]:f['v']=[[A[0]+c*x-s*y,A[1]+s*x+c*y,z]for x,y,z in f['v']]
register((194.4,-136.3),(176.1,-125.9),[1.8])
register((171.6,-126.5),(155.5,-142.6),[math.dist((171.6,-126.5),(155.5,-142.6))-1.8])
# Estimated short chamfer, documented in the official inventory but absent from
# the generalized cadastral corner. Its exact width is not a measured claim.
start=len(faces);W=math.dist((176.1,-125.9),(171.6,-126.5));x=W/2
box(0,W,-.1,.15,0,19,cream)
for z in [4.5,8.4,12.1]:
 box(.7,W-.7,-.25,-.1,z,z+2.8,trim)
 box(.9,W-.9,-.3,-.25,z+.1,z+2.6,pane)
 box(x-.04,x+.04,-.34,-.30,z+.1,z+2.6,trim)
 box(.5,W-.5,-.7,.1,z-.15,z,trim)
 for i in range(10):box(.5+i*(W-1)/9,.55+i*(W-1)/9,-.75,-.68,z,z+.85,trim if z==4.5 else iron)
 box(.5,W-.5,-.76,-.68,z+.8,z+.9,trim if z==4.5 else iron)
arch(x,15.9,3.2,3.0,trim,-.32)
for X in [x-.65,x+.65]:arch(X,16.1,1.08,2.3,pane,-.37)
patch([(0,18.8),(.35,19.6),(1.0,19.8),(x,21.1),(W-1,19.8),(W-.35,19.6),(W,18.8)],trim,-.31)
arch(x,.3,2.25,3.6,'#686955',-.34)
a=math.atan2(-.6,-4.5);c,s=math.cos(a),math.sin(a)
for f in faces[start:]:f['v']=[[176.1+c*x-s*y,-125.9+s*x+c*y,z]for x,y,z in f['v']]

# Three documented blue cupulillas and lanterns. Placement/size are estimated;
# rear rooftop and glazed courtyard hall are NOT reconstructed.
for cx,cy,R,h in [(191.0,-136.4,1.75,4.3),(173.8,-128.0,2.35,5.5),(158.1,-142.2,1.75,4.3)]:
 z0=19.0;N=24;M=8
 for j in range(M):
  t=j/M;T=(j+1)/M
  def v(t,a):
   r=R*(1-.65*t*t);return [cx+r*math.cos(a),cy+r*math.sin(a),z0+h*t]
  for i in range(N):
   a=i*math.tau/N;b=(i+1)*math.tau/N
   face([v(t,a),v(t,b),v(T,b),v(T,a)],'#738b9d' if j<6 else trim,'documented-cupola-estimated-geometry')
 z=z0+h;r=R*.40
 box(cx-r,cx+r,cy-r,cy+r,z,z+.3,trim)
 box(cx-r*.68,cx+r*.68,cy-r*.68,cy+r*.68,z+.3,z+1.8,pane)
 for X in [-r,r]:
  for Y in [-r,r]:box(cx+X-.10,cx+X+.10,cy+Y-.10,cy+Y+.10,z+.3,z+1.9,trim)
 box(cx-r*1.25,cx+r*1.25,cy-r*1.25,cy+r*1.25,z+1.85,z+2.1,trim)
 for i in range(4):
  a=i*math.pi/2;b=(i+1)*math.pi/2
  face([[cx+r*1.3*math.cos(a),cy+r*1.3*math.sin(a),z+2.1],[cx+r*1.3*math.cos(b),cy+r*1.3*math.sin(b),z+2.1],[cx,cy,z+2.8]],trim)
 box(cx-.10,cx+.10,cy-.1,cy+.1,z+2.7,z+3.7,trim)
(P/'model.json').write_text(json.dumps(faces,separators=(',',':')))
print(len(faces),'faces')
