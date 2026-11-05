import sys
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation

prs = Presentation('references/LumbiniEliteGroup_CompanyIntro.pptx')
slide8 = prs.slides[7]
for s in slide8.shapes:
    if s.shape_type == 6: # Group shape
        print(f'Group shape {s.name} has {len(s.shapes)} sub-shapes:')
        for sub in s.shapes:
            text = sub.text_frame.text if sub.has_text_frame else ''
            target = ''
            if sub.shape_type == 13:
                rId = sub._element.blip_rId
                target = slide8.part.rels[rId].target_ref
            print(f'  - Sub: {sub.name}, type={sub.shape_type}, text="{text}", target={target}')
