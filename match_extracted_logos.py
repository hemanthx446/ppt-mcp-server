import os, glob
from PIL import Image

# Let's inspect images in assets/extracted_logos
# We have image8, image45 to image69
images = glob.glob('assets/extracted_logos/image*.*')
print(f'Total image files: {len(images)}')
for im in sorted(images):
    print(os.path.basename(im), os.path.getsize(im))
