from PIL import Image
import os
for f in os.listdir('site/painted/18'):
    try: Image.open('site/painted/18/'+f).load()
    except Exception: print('bad',f); os.remove('site/painted/18/'+f)
