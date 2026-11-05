from pptx import Presentation

prs = Presentation('references/LumbiniEliteGroup_CompanyIntro.pptx')
slide8 = prs.slides[7]
print('=== Slide 8 Shapes in CompanyIntro ===')
for s in slide8.shapes:
    print(s.name, s.shape_type)
    if s.shape_type == 13:
        rId = s._element.blip_rId
        target = slide8.part.rels[rId].target_ref
        print('  target:', target)
    if s.has_text_frame:
        print('  text:', s.text_frame.text)
