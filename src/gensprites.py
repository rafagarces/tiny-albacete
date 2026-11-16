#!/usr/bin/env python3
"""Sprites pixel-art de los monstruos, dibujados por código. Escala 1:1, se agrandan en el cliente."""
from PIL import Image, ImageDraw

def img(w,h):
    im=Image.new('RGBA',(w,h),(0,0,0,0))
    return im,ImageDraw.Draw(im)

# ---------- Godzilla (vista lateral, mira a la izquierda) ----------
im,d=img(56,64)
DARK=(46,84,40,255); MID=(63,110,50,255); BELLY=(150,196,120,255); PLATE=(222,238,200,255); EYE=(220,60,50,255); MOUTH=(30,50,26,255)
# cola
d.polygon([(54,46),(56,60),(46,58),(40,50)],fill=DARK)
# piernas
d.rectangle([16,50,24,62],fill=DARK); d.rectangle([30,50,38,62],fill=DARK)
d.rectangle([14,60,25,63],fill=MID); d.rectangle([29,60,40,63],fill=MID)
# cuerpo
d.ellipse([12,26,42,56],fill=DARK)
d.ellipse([18,30,38,54],fill=BELLY)
# espinas dorsales
for i,(x,y,s) in enumerate([(40,26,7),(43,33,8),(45,41,7),(47,48,6)]):
    d.polygon([(x,y),(x+s,y+s),(x-2,y+s)],fill=PLATE)
# brazo
d.rectangle([12,34,18,44],fill=MID)
# cuello+cabeza (hacia la izquierda)
d.rectangle([8,18,22,32],fill=DARK)
d.rectangle([2,12,16,26],fill=DARK)      # cráneo
d.rectangle([0,20,10,26],fill=DARK)      # hocico
d.rectangle([0,24,9,27],fill=MOUTH)      # boca
d.polygon([(4,26),(8,26),(5,29)],fill=(240,240,230,255))  # diente
d.rectangle([5,15,8,18],fill=EYE)        # ojo
d.rectangle([10,12,14,15],fill=PLATE)    # ceja/placa
im.save('site/monsters/godzilla.png')

# ---------- Robot gigante (frontal) ----------
im,d=img(48,64)
METAL=(150,158,168,255); DARKM=(88,96,106,255); LIGHT=(190,198,208,255); VISOR=(216,60,60,255); CORE=(60,200,220,255)
# piernas
d.rectangle([12,44,20,60],fill=DARKM); d.rectangle([28,44,36,60],fill=DARKM)
d.rectangle([10,58,22,63],fill=METAL); d.rectangle([26,58,38,63],fill=METAL)
# cadera
d.rectangle([14,38,34,46],fill=METAL)
# torso
d.rectangle([8,18,40,40],fill=METAL)
d.rectangle([10,20,38,26],fill=LIGHT)
d.rectangle([20,28,28,36],fill=DARKM); d.rectangle([22,30,26,34],fill=CORE)  # núcleo
# brazos
d.rectangle([2,20,8,38],fill=DARKM); d.rectangle([40,20,46,38],fill=DARKM)
d.rectangle([1,36,9,44],fill=METAL); d.rectangle([39,36,47,44],fill=METAL)
# hombros
d.rectangle([2,16,10,22],fill=LIGHT); d.rectangle([38,16,46,22],fill=LIGHT)
# cabeza
d.rectangle([14,4,34,18],fill=METAL)
d.rectangle([16,8,32,13],fill=VISOR)   # visor
d.rectangle([23,0,25,5],fill=DARKM); d.point((24,0),fill=VISOR)  # antena
im.save('site/monsters/robot.png')

# ---------- Manchega gigante ----------
im,d=img(44,64)
SKIN=(240,205,170,255); HAIR=(40,30,28,255); BLOUSE=(245,240,230,255); SKIRT=(146,32,44,255); SKIRT_D=(110,22,32,255); APRON=(250,248,240,255); SHAWL=(60,80,46,255); GOLD=(226,180,60,255)
# falda amplia (campana)
d.polygon([(22,30),(6,62),(38,62)],fill=SKIRT)
d.polygon([(22,30),(6,62),(14,62)],fill=SKIRT_D)
d.polygon([(22,30),(30,62),(38,62)],fill=SKIRT_D)
# delantal
d.polygon([(22,34),(16,58),(28,58)],fill=APRON)
d.line([(16,58),(28,58)],fill=(220,120,120,255),width=1)
# blouse torso
d.rectangle([16,18,28,32],fill=BLOUSE)
# mantón verde cruzado
d.polygon([(16,18),(28,18),(24,30),(20,30)],fill=SHAWL)
d.polygon([(20,30),(24,30),(26,44),(18,44)],fill=SHAWL)
# brazos
d.rectangle([10,20,16,32],fill=BLOUSE); d.rectangle([28,20,34,32],fill=BLOUSE)
d.rectangle([11,30,15,36],fill=SKIN); d.rectangle([29,30,33,36],fill=SKIN)
# cuello y cabeza
d.rectangle([20,14,24,19],fill=SKIN)
d.ellipse([15,4,29,17],fill=SKIN)
# pelo: moño alto con peineta
d.pieslice([14,2,30,18],180,360,fill=HAIR)
d.ellipse([18,-2,26,6],fill=HAIR)          # moño
d.rectangle([17,-4,27,-1],fill=GOLD)       # peineta
# pendientes
d.point((16,12),fill=GOLD); d.point((28,12),fill=GOLD)
# cara
d.point((19,9),fill=(30,30,30,255)); d.point((25,9),fill=(30,30,30,255))
d.point((22,13),fill=(190,90,90,255))
im.save('site/monsters/manchega.png')
print('sprites ok')
