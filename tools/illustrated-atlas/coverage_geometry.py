"""Ground coverage from actual source rectangles, never their bounding box.
Union in exact atlas coordinates first, then project the merged geometry.
This avoids false sliver holes caused by projecting adjacent polygons separately.
It describes supplied art, not city completion or verified current facades.
"""
import math
import numpy as np
from shapely.geometry import box
from shapely.ops import unary_union
from shapely.affinity import affine_transform

def source_coverage(catalog, origin_utm):
 angle=math.radians(-154)
 A=np.array([[-math.sin(angle),math.cos(angle)],[math.sin(.6)*math.cos(angle),math.sin(.6)*math.sin(angle)]])
 focus=np.array([-123.2408167310922,-243.6981380554508]);m=472/2048
 rectangles=[box(t['x'],t['y'],t['x']+t['width'],t['y']+t['height'])for t in catalog['tiles']]
 coverage=unary_union(rectangles);B=np.linalg.inv(A)*472
 offset=np.linalg.solve(A,[-1536*m,-1024*m-9])+focus+origin_utm
 return affine_transform(coverage,[B[0,0],B[0,1],B[1,0],B[1,1],offset[0],offset[1]])
