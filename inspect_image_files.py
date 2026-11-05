from PIL import Image
import os, glob

for p in sorted(glob.glob('assets/extracted_logos/*.*')):
    try:
        im = Image.open(p)
        print(f'{os.path.basename(p)}: size={im.size}, mode={im.mode}, format={im.format}')
    except Exception as e:
        print(f'{os.path.basename(p)}: error {e}')
