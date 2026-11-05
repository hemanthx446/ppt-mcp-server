from pptx import Presentation

prs = Presentation('SAP_Datasphere_Career_Path.pptx')
for idx, s in enumerate(prs.slides):
    if idx >= 3:
        break
    print(f"\n--- Slide {idx+1} ---")
    for shp in s.shapes:
        txt = repr(shp.text[:35]) if shp.has_text_frame else "None"
        ph = shp.is_placeholder
        print(f"  Shape '{shp.name}' (is_ph={ph}): {txt}")
