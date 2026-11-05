import sys
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation

prs = Presentation('references/Data-Validation-and-ETL-Architecture-for-SAP-LTMC.pptx')
print(f'Total slides in LTMC: {len(prs.slides)}')

for idx, slide in enumerate(prs.slides):
    print(f'=== SLIDE {idx+1} ===')
    for shape in slide.shapes:
        if shape.has_text_frame:
            text = shape.text_frame.text.strip()
            if text:
                print('  - ' + '\n    '.join(text.splitlines()[:10]))
