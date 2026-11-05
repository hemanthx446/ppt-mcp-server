import sys
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation

prs = Presentation('references/Lumbini_SAP_ME_DMC_AMS_Proposal.pptx')
for idx in [7, 8, 9, 10, 11]: # slides 8-12
    slide = prs.slides[idx]
    print(f'=== SLIDE {idx+1} ===')
    for s in slide.shapes:
        if s.has_text_frame:
            t = s.text_frame.text.strip()
            print('--- Text ---')
            print(t)
