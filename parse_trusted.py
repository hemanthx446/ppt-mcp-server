import sys
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation

prs = Presentation('references/LumbiniEliteGroup_CompanyIntro.pptx')
for idx in [6, 7, 8]:
    slide = prs.slides[idx]
    print(f'=== SLIDE {idx+1} ===')
    for shape in slide.shapes:
        if shape.has_text_frame:
            t = shape.text_frame.text.strip()
            if t:
                print('  - ' + t)

prs2 = Presentation('Lumbini_Elite_Group_Product_Solutions_Services.pptx')
print(f'Total slides in Master deck: {len(prs2.slides)}')
for idx, slide in enumerate(prs2.slides):
    t_list = [s.text_frame.text.strip().replace('\n', ' ') for s in slide.shapes if s.has_text_frame and s.text_frame.text.strip()]
    if t_list:
        print(f'Slide {idx+1}: {t_list[0][:80]}')
