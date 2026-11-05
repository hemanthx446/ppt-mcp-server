import os, glob
from PIL import Image

for f in sorted(glob.glob('assets/company_logos/*.*')):
    try:
        im = Image.open(f)
        info = im.info
        print(f'{os.path.basename(f)}: size={im.size}, info_keys={list(info.keys())}')
        if 'title' in info or 'description' in info:
            print('  title/desc:', info.get('title'), info.get('description'))
    except Exception as e:
        pass
