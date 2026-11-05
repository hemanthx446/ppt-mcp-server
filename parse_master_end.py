import sys
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation

prs = Presentation('Lumbini_Elite_Group_Product_Solutions_Services.pptx')
for idx in range(28, len(prs.slides)):
    slide = prs.slides[idx]
    print(f'=== SLIDE {idx+1} ===')
    for shape in slide.shapes:
        if shape.has_text_frame:
            t = shape.text_frame.text.strip()
            if t:
                print('  - ' + '\n    '.join(t.splitlines()[:10]))
