import sys
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation

prs = Presentation('references/LumbiniEliteGroup_CompanyIntro.pptx')
slide8 = prs.slides[7]

def dump_shapes(shapes, rels, parent_name=''):
    for s in shapes:
        name = f'{parent_name}/{s.name}' if parent_name else s.name
        if s.shape_type == 13: # picture
            try:
                target = rels[s._element.blip_rId].target_ref
                print(f'{name}: {target} left={s.left/914400:.2f}, top={s.top/914400:.2f}, w={s.width/914400:.2f}, h={s.height/914400:.2f}')
            except Exception as e:
                pass
        elif s.shape_type == 6: # group
            dump_shapes(s.shapes, rels, name)

dump_shapes(slide8.shapes, slide8.part.rels)
