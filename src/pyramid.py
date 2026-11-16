#!/usr/bin/env python3
"""Build lower zoom levels from TOP tiles + emit tiles.json metadata."""
import os, math, json, sys
from PIL import Image, ImageEnhance
BASE='/tmp/tinyalba/site'
TOP=18; TS=1024
meta=json.load(open('/tmp/tinyalba/canvas.json'))
NTX=math.ceil(meta['W']/TS); NTY=math.ceil(meta['H']/TS)
def have(level):
    d=f'{BASE}/painted/{level}'
    if not os.path.isdir(d): return {}
    out={}
    for f in os.listdir(d):
        if f.endswith('.webp'):
            out[f[:-5]]=True
    return out
cur=have(TOP)
print('top tiles:',len(cur))
for level in range(TOP-1,TOP-9,-1):
    os.makedirs(f'{BASE}/painted/{level}',exist_ok=True)
    src=have(level+1)
    nxt={}
    for key in src:
        x,y=map(int,key.split('_'))
        nxt[(x//2,y//2)]=True
    n=0
    for (x,y) in sorted(nxt):
        out=f'{BASE}/painted/{level}/{x}_{y}.webp'
        if os.path.exists(out): continue
        im=Image.new('RGBA',(TS,TS),(0,0,0,0))
        any_tile=False
        for dx in (0,1):
            for dy in (0,1):
                p=f'{BASE}/painted/{level+1}/{x*2+dx}_{y*2+dy}.webp'
                if os.path.exists(p):
                    t=Image.open(p).resize((TS//2,TS//2),Image.BILINEAR)
                    t=ImageEnhance.Color(t).enhance(1.035)
                    t=ImageEnhance.Contrast(t).enhance(1.02)
                    im.paste(t,(dx*TS//2,dy*TS//2)); any_tile=True
        if any_tile:
            im.save(out,quality=80,method=4); n+=1
    print('level',level,'tiles',len(nxt),'new',n,flush=True)
# tiles.json: only mark non-black tiles as existing (approx: file size > 900B)
havemap={}
for level in range(TOP-8,TOP+1):
    d=f'{BASE}/painted/{level}'
    if not os.path.isdir(d): continue
    h={}
    for f in os.listdir(d):
        if f.endswith('.webp'):
            h[f[:-5]]='a'
    havemap[level]=h
json.dump({'w':meta['W'],'h':meta['H'],'top':TOP,'have':havemap},open(f'{BASE}/tiles.json','w'))
print('tiles.json written')
