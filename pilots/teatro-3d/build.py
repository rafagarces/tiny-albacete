"""Teatro Circo modern front: DnTrotaMundos2010 CC BY3.0.
Original estimated geometry, no photo textures or posters. See README.
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

W=math.hypot(30.4,17.9);grey='#a5aaa2';frame='#c8c6b5';metal='#8e9994';glass='#465a58'
# Modern concrete pylons and open ground-floor glazing, not historical printed facades.
for a,b in [(0,3.8),(W-3.8,W)]:box(a,b,0,9,0,13.6,frame)
box(3.8,W-3.8,.8,7.7,0,3.5,glass)
for x in [4+i*1.1 for i in range(int((W-8)/1.1)+1)]:box(x,x+.055,.65,.82,0,3.5,'#9aaba4')
box(3.7,W-3.7,.4,1,3.3,3.55,metal)
# Curved metal mesh curtain approximated with 18 horizontal bands.
# Count of seams not claimed as surveyed; no removed anniversary banners.
def yy(z):return -1.8*math.sin((z-3.5)/10.1*math.pi*.88)
for i in range(18):
 z=3.5+i*10.1/18;Z=3.5+(i+1)*10.1/18
 face([[3.9,yy(z),z],[W-3.9,yy(z),z],[W-3.9,yy(Z),Z],[3.9,yy(Z),Z]],metal)
# Large shallow sloping canopy observed in free photo, dimensions are estimates.
face([[-.8,-2.8,16.0],[W+.8,-2.8,16.0],[W+.8,11,14.8],[-.8,11,14.8]],'#a3aaa3')
face([[-.8,-2.8,15.82],[W+.8,-2.8,15.82],[W+.8,11,14.62],[-.8,11,14.62]],'#666f67')
face([[-.8,-2.8,15.82],[W+.8,-2.8,15.82],[W+.8,-2.8,16],[-.8,-2.8,16]],'#c0c7bd')
for x in [3.8,W-3.8]:
 face([[x,.6,13.4],[x,4.5,15.2],[x+.13,4.5,15.2],[x+.13,.6,13.4]],'#7d8881')
# Lettering is modelled as a simple line skeleton rather than a pasted image.
letters={
'T':[[(0,1),(1,1)],[(.5,1),(.5,0)]],
'E':[[(1,1),(0,1),(0,0),(1,0)],[(0,.5),(.8,.5)]],
'A':[[(0,0),(.5,1),(1,0)],[(.22,.4),(.78,.4)]],
'R':[[(0,0),(0,1),(.75,1),(1,.8),(1,.6),(.7,.5),(0,.5)],[(.5,.5),(1,0)]],
'O':[[(.2,0),(0,.2),(0,.8),(.2,1),(.8,1),(1,.8),(1,.2),(.8,0),(.2,0)]],
'C':[[(1,.9),(.8,1),(.2,1),(0,.8),(0,.2),(.2,0),(.8,0),(1,.1)]],
'I':[[(.5,0),(.5,1)]]}
text='TEATRO CIRCO';x=7.1
for ch in text:
 if ch!=' ':
  for line in letters[ch]:
   for (a,b),(A,B) in zip(line,line[1:]):
    xx=x+a*1.3;XX=x+A*1.3;z=4.25+b*1.1;Z=4.25+B*1.1
    L=math.hypot(XX-xx,Z-z) or 1;dx=-(Z-z)/L*.065;dz=(XX-xx)/L*.065
    face([[xx-dx,yy(z)-.3,z-dz],[XX-dx,yy(Z)-.3,Z-dz],[XX+dx,yy(Z)-.3,Z+dz],[xx+dx,yy(z)-.3,z+dz]],'#d9ddd2','photo-feature-estimated-lettering')
 x+=1.72
(P/'model.json').write_text(json.dumps(faces,separators=(',',':')))
print(len(faces),'faces')
