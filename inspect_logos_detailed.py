import os, glob
from PIL import Image

# Let's inspect images in assets/extracted_logos
# Notice that earlier in parse_slide14.py from TEPL:
# Shape Picture 3 -> image8.png (top left on TEPL slide 14, left=1.26, top=1.58, w=2.92, h=1.43)
# Let's check image8.png
print('Checking specific logo candidates...')
for img in ['image8.png', 'image45.png', 'image46.png', 'image47.png', 'image48.png', 'image50.png', 'image55.png', 'image60.png', 'image67.png']:
    p = os.path.join('assets/extracted_logos', img)
    if os.path.exists(p):
        im = Image.open(p)
        print(f'{img}: {im.size}, {im.mode}')
