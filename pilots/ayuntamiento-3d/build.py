"""Antiguo Ayuntamiento: partial original facade, JPOK CC0 10 Nov2016.
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

# Front of Catastro 9371110WJ9197A: 20.14 m. Facade-only overlay;
# Catastro masses behind it remain, not an invented full rectangular building.
W=math.hypot(17.6,9.8);C=W/2
cream='#eee8d8';red='#be8e80';pane='#3c4c4c';iron='#535752'
box(0,W,-.08,.18,0,11.2,cream)
# Four red strips and long vertical corner/pier decoration visible in JPOK2016.
for x in [.25,7.3,12.0,W-.7]:
 box(x,x+.45,-.13,-.08,.6,10.6,red)
 for z in [i*.4+.7 for i in range(24)]:
  box(x-.12,x+.57,-.18,-.13,z,z+.11,cream,'artistic-material')
# Strong shallow pilasters, square capitals and frieze below the cornice.
for x in [.7,6.8,12.95,19.45]:
 box(x-.13,x+.13,-.42,-.18,5.9,10.5,cream)
 box(x-.3,x+.3,-.5,-.14,9.93,10.18,cream)
 box(x-.25,x+.25,-.47,-.15,5.84,6.08,cream)
for x in [1.8,3.5,5.2,14.9,16.6,18.3]:
 box(x-.35,x+.35,-.35,-.11,10.22,10.46,'#d7d0bd')
# Main door, four lower grilles and four upper windows. Avoid ephemeral signs/flags.
for x in [1.95,5.1,15.05,18.2]:
 box(x-1.03,x+1.03,-.22,-.08,1.0,4.4,cream)
 box(x-.81,x+.81,-.25,-.22,1.25,4.18,pane)
 for X in [x-.65+i*.22 for i in range(7)]:box(X-.025,X+.025,-.31,-.25,1.25,4.18,iron)
 for z in [1.7,2.5,3.3,4.0]:box(x-.8,x+.8,-.31,-.25,z,z+.04,iron)
 box(x-1.07,x+1.07,-.22,-.08,6.0,9.8,cream)
 box(x-.8,x+.8,-.26,-.22,6.2,9.5,pane)
 box(x-.03,x+.03,-.32,-.26,6.2,9.5,iron)
 box(x-.8,x+.8,-.32,-.26,8.9,8.96,iron)
 box(x-1.2,x+1.2,-.4,-.08,9.85,10.03,cream)
 # Shallow decorative pediment, not an exact floral carving.
 patch([(x-1.05,10.05),(x,10.35),(x+1.05,10.05)],cream,-.31)
# Center entrance and balcony door.
box(C-1.1,C+1.1,-.3,-.1,0,4.3,'#775e43')
box(C-.03,C+.03,-.34,-.3,.05,4.25,'#534836')
for x in [C-1.55,C+1.35]:box(x,x+.2,-.4,-.08,.3,9.9,cream)
box(C-1.04,C+1.04,-.3,-.09,6.15,9.55,pane)
box(C-.035,C+.035,-.37,-.3,6.2,9.5,iron)
box(C-2.1,C+2.1,-1.15,.2,5.65,5.9,cream)
box(C-2.1,C+2.1,-1.18,-1.02,6.65,6.83,cream)
for x in [C-1.95+i*.3 for i in range(14)]:box(x-.04,x+.04,-1.18,-1.02,5.92,6.65,iron)
for z in [5.1,10.6,11.05]:box(-.18,W+.18,-.42,.24,z,z+.22,cream)
# Balustrade and stepped parapets, simplified silhouette from the photo.
for a,b in [(0,C-2.4),(C+2.4,W)]:
 box(a,b,-.17,.12,11.4,11.55,cream);box(a,b,-.17,.12,12.1,12.25,cream)
 for x in [a+i*.48 for i in range(int((b-a)/.48)+1)]:box(x,x+.065,-.17,.12,11.55,12.1,cream)
for x in [2.6,W-2.6]:
 box(x-1.55,x+1.55,-.12,.18,11.5,12.35,cream)
 box(x-1.2,x+1.2,-.15,.18,12.35,12.6,cream)
 box(x-.8,x+.8,-.15,.18,12.6,12.85,cream)
 patch([(x-1.3,11.7),(x+1.3,11.7),(x+1.3,12.1),(x+.6,12.1),(x+.6,12.4),(x-.6,12.4),(x-.6,12.1),(x-1.3,12.1)],red,-.19)
# Square clock tower, front and visible right face. Face/clock geometry estimated.
box(C-2.35,C+2.35,0,3.8,11.1,18.0,red)
for x in [C-2.35,C+1.95]:
 box(x,x+.4,-.22,.16,11.1,18.2,cream)
 box(x-.13,x+.53,-.35,.23,17.9,18.2,cream)
# Simplified shield below front clock, no invented heraldic details.
patch([(C-.9,12),(C+.9,12),(C+.85,13.45),(C,13.95),(C-.85,13.45)],cream,-.29)
patch([(C-.64,12.27),(C+.64,12.27),(C+.58,13.3),(C,13.68),(C-.58,13.3)],'#bab8a8',-.33)
circle(C,16.05,1.37,cream,-.3);circle(C,16.05,1.11,pane,-.34)
for i in range(12):
 a=i*math.tau/12
 x=C+.89*math.sin(a);z=16.05+.89*math.cos(a)
 patch([(x-.035,z-.06),(x+.035,z-.06),(x+.035,z+.06),(x-.035,z+.06)],cream,-.36)
# Neutral clock hands are a static artistic pose, not live time.
patch([(C-.04,16.05),(C+.04,16.05),(C+.04,16.75),(C-.04,16.75)],cream,-.38,'artistic-clock-pose')
patch([(C,16.0),(C+.61,16.35),(C+.65,16.42),(C,16.1)],cream,-.38,'artistic-clock-pose')
# Side clock, visible in the free photo, without adding hidden faces.
for r,col,x in [(1.25,cream,C+2.38),(1.01,pane,C+2.4)]:
 face([[x,1.9+r*math.cos(i*math.tau/28),16.05+r*math.sin(i*math.tau/28)]for i in range(28)],col)
box(C-2.5,C+2.5,-.3,.2,18.2,18.42,cream)
box(C-2.5,C-2.22,0,3.8,18.2,18.42,cream)
box(C+2.22,C+2.5,0,3.8,18.2,18.42,cream)
# Curved open parapet on the visible front, simplified from the CC0 photo.
for i in range(16):
 x=C-2.25+i*4.5/16;X=x+4.5/16
 z=18.6+.55*(1-((x-C)/2.25)**2);Z=18.6+.55*(1-((X-C)/2.25)**2)
 patch([(x,z),(X,Z),(X,Z+.16),(x,z+.16)],cream,-.41)
for i in range(11):
 x=C-2.2+i*.44;z=18.6+.55*(1-((x-C)/2.25)**2)
 box(x-.035,x+.035,-.4,-.17,18.42,z,cream)
for x in [C-2.25,C-1.45,C+1.45,C+2.25]:spire(x,18.4,.8,0)
box(C-.8,C+.8,-.1,.35,18.42,18.85,cream)
spire(C,18.85,1.4,.1)
(P/'model.json').write_text(json.dumps(faces,separators=(',',':')))
print(len(faces),'faces')
