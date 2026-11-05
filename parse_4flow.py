import sys
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation

prs = Presentation('4Flow_SAP_IBP_Executive_Proposal.pptx')
print(f'Total slides in 4Flow: {len(prs.slides)}')
for idx, slide in enumerate(prs.slides):
    print(f'=== SLIDE {idx+1} ===')
    for shape in slide.shapes:
        if shape.has_text_frame:
            t = shape.text_frame.text.strip()
            if t:
                print('  ' + '\n  '.join(t.splitlines()[:6]))
