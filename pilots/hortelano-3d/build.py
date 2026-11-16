"""Casa de Hortelano: original partial front, positions/reliefs estimated.
Reference existence verified in Rodelar2024/User0412026; see README.
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
# Approximate registration to exact cadastral corner, not separate ground survey.
box(0,15.93,0,14,0,8.0,stone,'unknown-simplified')
box(0,2.65,0,5.5,0,9.0,stone)
box(11.75,15.93,0,5.5,0,11.0,stone)
# Actual green tile fields on the front, with ornamental stone edges.
patch([(0.65,1.4),(2.4,1.4),(2.4,8.8),(.65,8.8)],green,-.04)
patch([(2.65,1.4),(11.75,1.4),(11.75,8.0),(2.65,8)],green,-.04)
patch([(12.3,1.4),(15.25,1.4),(15.25,10.8),(12.3,10.8)],green,-.04)
# Rusticated base/corner courses, artistic material pattern not exact stone inventory.
for z in [0.4,.8,1.2]:
 patch([(0,z),(15.93,z),(15.93,z+.04),(0,z+.04)],dark,-.08,'artistic-material')
for z in [1.7+i*.55 for i in range(16)]:
 for a,b in [(0,.65),(15.25,15.93)]:patch([(a,z),(b,z),(b,z+.03),(a,z+.03)],dark,-.08,'artistic-material')
# Five upper central Gothic windows: count comes from both photographs.
# The trifoliate upper shape/tracery is simplified, no exact carving claim.
for x in [3.55,5.32,7.1,8.87,10.64]:
 arch(x,4.1,1.68,3.15,trim,-.67);arch(x,4.28,1.32,2.77,glass,-.70)
 for X in [x-.34,x+.34]:box(X-.035,X+.035,-.76,-.70,4.28,6.55,wood)
 box(x-.66,x+.66,-.76,-.70,6.36,6.43,wood)
 circle(x,6.76,.28,trim,-.73);circle(x,6.77,.21,glass,-.75)
 for X in [x-.74,x+.74]:box(X-.065,X+.065,-.78,-.62,4.05,7.15,trim)
 # Pale Gothic cap rising over each arch.
 patch([(x-.83,6.8),(x,7.8),(x+.83,6.8),(x+.65,6.9),(x,7.5),(x-.65,6.9)],trim,-.8)
# Projecting gallery sill and ornamental rail are actual visible forms.
box(2.65,11.75,-.86,0,3.5,3.8,trim)
box(2.65,11.75,-.8,-.56,4.0,4.15,trim)
for x in [3.3+i*.48 for i in range(18)]:ring(x,3.97,.19,.12,trim,-.84)
# Three lower grilled windows documented front; grills interpreted coarsely.
for x in [3.9,7.2,10.5]:
 arch(x,1.4,1.25,2.05,dark,-.10);arch(x,1.5,1.0,1.83,glass,-.13)
 for X in [x-.36,x-.18,x,x+.18,x+.36]:box(X-.018,X+.018,-.19,-.13,1.5,3.15,'#393f37')
# Right entrance and separate projecting bay. Lobes deliberately simplified.
for w,h,col,y in [(3.4,3.5,trim,-.14),(3.0,3.22,dark,-.17),(2.65,3.0,trim,-.2),(2.32,2.8,'#353c32',-.23)]:arch(13.82,.08,w,h,col,y)
box(12.7,14.95,-.25,-.22,.1,2.0,wood)
box(13.79,13.85,-.28,-.24,.1,2.,dark)
arch(13.82,4.12,2.38,3.1,trim,-.57);arch(13.82,4.34,1.8,2.65,glass,-.61)
for X in [13.3,13.82,14.34]:box(X-.04,X+.04,-.67,-.61,4.34,6.68,wood)
box(12.45,15.2,-.83,0,3.5,3.8,trim)
for x in [12.8+i*.4 for i in range(6)]:ring(x,3.97,.18,.115,trim,-.84)
for x in [2.75+i*1.8 for i in range(6)]:spire(x,7.6,1.8,-.5)
for x in [12.55,15.08]:spire(x,7.15,2.1,-.45)
# Asymmetric stepped tower crowns, observed silhouettes. Floral carving omitted.
for a,b,z in [(0,2.65,9),(11.75,15.93,11)]:
 cx=(a+b)/2
 box(a-.15,b+.15,-.2,1,z,z+.22,trim)
 box(a+.5,b-.5,-.08,.6,z+.22,z+1.0,stone)
 box(a+.35,b-.35,-.22,.75,z+1.0,z+1.18,trim)
 box(cx-.3,cx+.3,-.08,.6,z+1.18,z+1.85,stone)
 box(cx-.52,cx+.52,-.2,.75,z+1.85,z+2.0,trim)
 spire(cx,z+2.0,.9,-.1)
 for x in [a+.14,b-.14]:spire(x,z+.2,.8,-.1)
# Flat closure behind decorative front, not a surveyed roof topology.
box(2.7,11.7,.3,13.8,8,8.12,'#967e65','unknown-simplified')
(P/'model.json').write_text(json.dumps(faces,separators=(',',':')))
print(len(faces),'faces',P)
