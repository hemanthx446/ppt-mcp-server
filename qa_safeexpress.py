import os, sys
import zipfile
import win32com.client
from pptx import Presentation

DECK_PATH = os.path.abspath("Lumbini_SafeExpress_Executive_Capabilities.pptx")
IMG_DIR = os.path.abspath("audit_renderings/safeexpress")
os.makedirs(IMG_DIR, exist_ok=True)

print("=== 1. STRUCTURAL & TYPOGRAPHY CHECK ===")
prs = Presentation(DECK_PATH)
print(f"Total slides: {len(prs.slides)}")
assert len(prs.slides) == 7, f"Expected 7 slides, found {len(prs.slides)}"

font_violations = []
for idx, slide in enumerate(prs.slides, 1):
    for shape in slide.shapes:
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                if p.font and p.font.name and p.font.name.lower() != "calibri":
                    font_violations.append((idx, p.font.name, p.text[:30]))
                for r in p.runs:
                    if r.font and r.font.name and r.font.name.lower() != "calibri":
                        font_violations.append((idx, r.font.name, r.text[:30]))

print(f"Font violations (non-Calibri): {len(font_violations)}")
if font_violations:
    print("Violations:", font_violations[:5])
else:
    print("  [PASS] 100% Calibri compliance!")

print("\n=== 2. NATIVE POWERPOINT RENDERING TO 1080P ===")
ppt_app = win32com.client.Dispatch("PowerPoint.Application")
prs_com = ppt_app.Presentations.Open(DECK_PATH, WithWindow=False)

for i, slide in enumerate(prs_com.Slides, 1):
    out_img = os.path.join(IMG_DIR, f"slide_{i}.png")
    slide.Export(out_img, "PNG", 1920, 1080)
    print(f"  Exported Slide {i} -> {out_img}")

prs_com.Close()
ppt_app.Quit()
print("  [PASS] All 7 slides successfully rendered to 1080p images!")

