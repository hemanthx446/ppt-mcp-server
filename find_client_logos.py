import os, glob, zipfile
from pptx import Presentation

# Check slides named 'Trusted By' or 'OUR CLIENTS & PARTNERS' across all decks
for f in glob.glob('references/*.pptx') + glob.glob('*.pptx'):
    try:
        prs = Presentation(f)
        for idx, slide in enumerate(prs.slides):
            t = ' '.join([s.text_frame.text.lower() for s in slide.shapes if s.has_text_frame])
            if any(k in t for k in ['trusted by', 'our clients', 'clients & partners', 'ecosystem', 'industries we serve']):
                print(f'{f} - Slide {idx+1}: {t[:100]}')
                # inspect shapes
                pic_count = sum(1 for s in slide.shapes if s.shape_type == 13)
                print(f'   -> Pictures count: {pic_count}')
    except Exception as e:
        pass
