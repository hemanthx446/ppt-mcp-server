from pptx import Presentation

prs = Presentation('references/The_Connected_Enterprise_TEPL_Lumbini.pptx')
print(f'Total slides in TEPL: {len(prs.slides)}')

for idx, slide in enumerate(prs.slides):
    print(f'=== SLIDE {idx+1} ===')
    for shape in slide.shapes:
        if shape.has_text_frame:
            text = shape.text_frame.text.strip()
            if text:
                print('  - ' + '\n    '.join(text.splitlines()[:10]))
