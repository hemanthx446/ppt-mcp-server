import sys
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation

def print_shapes(shapes, rels, depth=0):
    indent = '  ' * depth
    for s in shapes:
        text = s.text_frame.text.strip().replace('\n', ' ') if s.has_text_frame else ''
        target = ''
        if s.shape_type == 13:
            try:
                rId = s._element.blip_rId
                target = rels[rId].target_ref
            except:
                pass
        print(f'{indent}- {s.name} (type={s.shape_type}) text=\"{text[:60]}\" target={target}')
        if s.shape_type == 6: # Group
            print_shapes(s.shapes, rels, depth+1)

prs = Presentation('references/LumbiniEliteGroup_CompanyIntro.pptx')
slide8 = prs.slides[7]
print_shapes(slide8.shapes, slide8.part.rels)
