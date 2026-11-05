from pptx import Presentation
prs = Presentation('themes/lumbini/template.pptx')
for i, l in enumerate(prs.slide_layouts):
    print(f"--- Layout {i}: {l.name} ---")
    for s in l.shapes:
        ph_type = s.placeholder_format.type if s.is_placeholder else "Not PH"
        text = s.text if s.has_text_frame else "No Text"
        print(f"  Shape: {s.name}, is_ph: {s.is_placeholder}, ph_type: {ph_type}, text: {repr(text)}")
