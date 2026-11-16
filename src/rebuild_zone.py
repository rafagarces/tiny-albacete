"""Offline bounded-zone rebuild; never rebuilds or removes the general map."""
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for name in ['catedral','hortelano','ayuntamiento','teatro','diputacion','perona','granhotel']:
 subprocess.run([sys.executable,str(ROOT/'pilots'/f'{name}-3d'/'build.py')],cwd=ROOT,check=True)
subprocess.run([sys.executable,str(ROOT/'src/build_zone.py')],cwd=ROOT,check=True)
subprocess.run([sys.executable,str(ROOT/'tests/check_roof_triangulation.py')],cwd=ROOT,check=True)
subprocess.run([sys.executable,str(ROOT/'tests/check_local_frame.py')],cwd=ROOT,check=True)
