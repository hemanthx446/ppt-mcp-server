import os, sys
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation

prs = Presentation('references/The_Connected_Enterprise_TEPL_Lumbini.pptx')
slide14 = prs.slides[13]

for idx, shape in enumerate(slide14.shapes):
    if shape.has_text_frame:
        print(f'Text: {shape.text_frame.text}')
    if shape.shape_type == 13:
        rId = shape._element.blip_rId
        target = slide14.part.rels[rId].target_ref
        print(f'Shape {shape.name}: target={target}, left={shape.left/914400:.2f}, top={shape.top/914400:.2f}, w={shape.width/914400:.2f}, h={shape.height/914400:.2f}')
