import sys
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation

prs = Presentation('references/Lumbini_SAP_ME_DMC_AMS_Proposal.pptx')
for idx in range(10, len(prs.slides)):
    slide = prs.slides[idx]
    print(f'=== SLIDE {idx+1} ===')
    for shape in slide.shapes:
        if shape.has_text_frame:
            t = shape.text_frame.text.strip()
            if t:
                print('  - ' + '\n    '.join(t.splitlines()[:6]))
