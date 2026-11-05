import sys
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation

prs = Presentation('references/LumbiniEliteGroup_CompanyIntro.pptx')
print(f'Total slides in CompanyIntro: {len(prs.slides)}')
for idx, slide in enumerate(prs.slides):
    print(f'=== SLIDE {idx+1} ===')
    for shape in slide.shapes:
        if shape.has_text_frame:
            t = shape.text_frame.text.strip()
            if t:
                print('  - ' + '\n    '.join(t.splitlines()[:6]))
