import sys
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation

prs = Presentation('references/The_Connected_Enterprise_TEPL_Lumbini.pptx')
slide14 = prs.slides[13]

for shape in slide14.shapes:
    if shape.shape_type == 13: # picture
        rId = shape._element.blip_rId
        target = slide14.part.rels[rId].target_ref
        print(f'Shape {shape.name} -> {target} (pos: left={shape.left/914400:.2f}, top={shape.top/914400:.2f})')
