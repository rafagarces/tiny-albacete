"""Fit historic roof samples; does not certify present-day geometry."""
import json,numpy as np
from pathlib import Path
from scipy.optimize import least_squares
P=Path(__file__).parent
X,Y,H=np.array(json.loads((P/'roof-samples-2017.json').read_text())).T
def residual(a):
 cx,cy,top,slope=a
 return top-slope*np.hypot(X-cx,Y-cy)-H
fit=least_squares(residual,[163,51,22,.45],bounds=([157,46,18,.1],[170,58,28,1.5]),loss='soft_l1',f_scale=.3)
print('n',len(H),'cx,cy,apex,slope',fit.x,'median absolute residual',np.median(abs(residual(fit.x))))
