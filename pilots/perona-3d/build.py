"""Casa Perona: original partial front and east side from free photos.
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

salmon='#ca9170';cream='#e7dfc4';pane='#71817b';iron='#4c5650'
W=24.0;D=19.1
# Thin front/side facades, cadastral interior masses retained behind.
box(0,W,-.09,.12,0,8.7,salmon)
start=len(faces);box(-.1,.1,0,D,0,8.7,salmon)
for f in faces[start:]:f['v']=[[X-Y*.058,Y,Z]for X,Y,Z in f['v']]
for z,Z in [(0,.4),(8.25,8.45),(8.6,8.9),(9.0,9.17)]:
 box(-.15,W+.15,-.3,.16,z,Z,cream);start=len(faces);box(-.3,.16,0,D,z,Z,cream)
 for f in faces[start:]:f['v']=[[X-Y*.058,Y,Z]for X,Y,Z in f['v']]
def bay(x,door=False):
 # Two photos show five front bays and three along the east return.
 box(x-.87,x+.87,-.2,-.1,4.65,7.95,cream)
 box(x-.65,x+.65,-.23,-.2,4.85,7.75,pane)
 for X in [x-.65,x,x+.65]:box(X-.035,X+.035,-.28,-.23,4.85,7.75,cream)
 for z in [5.3,6.0,6.7,7.4]:box(x-.65,x+.65,-.28,-.23,z,z+.045,cream)
 box(x-1.03,x+1.03,-.3,-.1,7.96,8.1,cream)
 box(x-.95,x+.95,-.5,.1,4.45,4.62,cream)
 for z in [4.75,5.65]:box(x-.9,x+.9,-.6,-.5,z,z+.065,iron)
 for i in range(8):
  X=x-.85+i*1.7/7;box(X-.025,X+.025,-.6,-.5,4.7,5.65,iron)
 box(x-1.08,x+1.08,-.23,-.1,.3,4.3,cream)
 box(x-.8,x+.8,-.27,-.23,.4,3.85,pane if not door else '#514d40')
 if not door:
  for i in range(8):
   X=x-.76+i*1.52/7;box(X-.025,X+.025,-.39,-.28,.45,3.8,iron)
  for z in [.8,1.6,2.4,3.2,3.7]:box(x-.8,x+.8,-.4,-.28,z,z+.04,iron)
 # Plain stone lintel substitutes for exact small carvings.
 box(x-1.15,x+1.15,-.31,-.1,4.0,4.22,cream)
for x in [2.4,7.2,12,16.8,21.6]:bay(x,x==12)
# The short east return has three observed bays, including lower iron grilles.
for y in [3.3,9.55,15.8]:
 start=len(faces);bay(y)
 for f in faces[start:]:f['v']=[[Y-X*.058,X,Z]for X,Y,Z in f['v']]
# Broad stone entrance and two plain shield silhouettes; no invented heraldic arms.
for x in [10.6,13.4]:box(x-.2,x+.2,-.35,-.09,.15,4.5,cream)
box(10.2,13.8,-.42,-.08,4.2,4.5,cream)
for x in [10.65,13.35]:
 box(x-.38,x+.38,-.46,-.15,4.6,5.1,cream)
 patch([(x-.36,5.1),(x+.36,5.1),(x+.46,5.8),(x+.25,6.2),(x-.25,6.2),(x-.46,5.8)],cream,-.45)
# Dome over the stair core. Form documented; diameter, height, ribs and registration estimated.
cx,cy=14,14.5;R=2.7;z0=9.0
box(cx-2.9,cx+2.9,cy-2.9,cy+2.9,8.7,9.2,cream)
N=40;M=10
for j in range(M):
 t=j*math.pi/2/M;T=(j+1)*math.pi/2/M
 for i in range(N):
  a=i*math.tau/N;b=(i+1)*math.tau/N
  def v(t,a):return [cx+R*math.cos(t)*math.cos(a),cy+R*math.cos(t)*math.sin(a),z0+3.2*math.sin(t)]
  face([v(t,a),v(t,b),v(T,b),v(T,a)],cream if i%5==0 else '#708d9c','documented-dome-estimated-geometry')
box(cx-.34,cx+.34,cy-.34,cy+.34,12.15,12.9,cream)
for i in range(4):
 a=i*math.pi/2;b=(i+1)*math.pi/2
 face([[cx+.4*math.cos(a),cy+.4*math.sin(a),12.9],[cx+.4*math.cos(b),cy+.4*math.sin(b),12.9],[cx,cy,15.8]],'#68746c','documented-dome-estimated-geometry')
assert len(faces)>900
(P/'model.json').write_text(json.dumps(faces,separators=(',',':')))
print(len(faces),'faces')
