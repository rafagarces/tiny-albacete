"""Palacio Provincial: partial original frontage from free photos 2017.
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

W=math.hypot(14.3,27.9);C=W/2
red='#c18d7c';cream='#e9e2c9';pane='#435051';iron='#555a54'
box(0,W,-.08,.15,0,12.1,red)
for z,Z in [(0,.7),(4.5,4.8),(5.1,5.35),(11,11.35),(11.75,12.1)]:box(-.15,W+.15,-.4,.17,z,Z,cream)
# Three central upper openings and one visible opening on either flank.
for x in [3.5,C-4,C,C+4,W-3.5]:
 box(x-1.18,x+1.18,-.24,-.09,5.2,10.3,cream)
 box(x-.93,x+.93,-.28,-.24,5.42,10,pane)
 box(x-.035,x+.035,-.33,-.28,5.42,10,'#9b805b')
 box(x-.92,x+.92,-.34,-.28,9.1,9.18,cream)
 box(x-1.35,x+1.35,-.4,-.08,10.38,10.6,cream)
 patch([(x-1.3,10.6),(x,10.9),(x+1.3,10.6)],cream,-.35)
# Lower facade obscured in references: plain central entry only, no invented grilles.
box(C-1,C+1,-.3,-.12,0,3.5,pane)
for x in [C-6.35,C-5.8,C+5.8,C+6.35]:
 box(x-.19,x+.19,-.68,-.3,4.8,10.9,cream)
 box(x-.32,x+.32,-.8,-.22,10.7,11,cream)
 box(x-.28,x+.28,-.8,-.2,4.8,5,cream)
box(C-6.5,C+6.5,-1.35,.18,4.55,4.8,cream)
for z in [4.95,5.8]:box(C-6.5,C+6.5,-1.42,-1.28,z,z+.09,iron)
for i in range(45):
 x=C-6.45+i*12.9/44;box(x-.025,x+.025,-1.42,-1.28,4.9,5.85,iron)
for i in range(47):
 x=.25+i*(W-.5)/46;box(x-.12,x+.12,-.58,-.12,11.3,11.73,cream,'artistic-material')
box(C-6.7,C+6.7,-.05,2.2,12.1,14.8,red)
for x in [C-6.7,C+5.7]:box(x,x+1,-.24,2.3,12.1,15.3,red)
for z in [12.35,13.8,14.6]:box(C-6.8,C+6.8,-.4,2.35,z,z+.2,cream)
# Plain tablet instead of unsupported lettering or carved municipal shields.
box(C-5.1,C+5.1,-.31,-.07,12.65,13.7,cream)
arch(C,14.4,5.8,3.5,cream,-.19);arch(C,14.45,5.3,3.25,red,-.23)
circle(C,15.5,1.05,cream,-.26);circle(C,15.5,.83,'#c6d0c9',-.3)
for i in range(12):
 a=i*math.tau/12;x=C+.65*math.sin(a);z=15.5+.65*math.cos(a)
 patch([(x-.025,z-.05),(x+.025,z-.05),(x+.025,z+.05),(x-.025,z+.05)],iron,-.32)
patch([(C-.03,15.5),(C+.03,15.5),(C+.03,16),(C-.03,16)],iron,-.35,'artistic-clock-pose')
patch([(C,15.47),(C+.45,15.7),(C+.49,15.76),(C,15.55)],iron,-.35,'artistic-clock-pose')
for x in [C-6.2,C+6.2,C]:
 z=15.3 if x!=C else 17.9
 box(x-.5,x+.5,-.2,.6,z,z+.6,cream)
 patch([(x-.4,z+.6),(x+.4,z+.6),(x+.3,z+1),(x-.3,z+1)],cream,-.21)
# Low attic masses simplified, no inventory of partly cropped openings.
for a,b in [(0,C-7),(C+7,W)]:
 box(a,b,0,3.5,12.1,14.8,red)
 box(a-.1,b+.1,-.24,3.6,14.8,15.03,cream)
assert len(faces)>700, 'Unexpectedly empty/incomplete model'
(P/'model.json').write_text(json.dumps(faces,separators=(',',':')))
print(len(faces),'faces')
