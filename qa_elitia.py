import os
import zipfile
import win32com.client
from pptx import Presentation

DECK_PATH = os.path.abspath("Elitia_Technology_Solutions_Capability_Overview.pptx")
IMG_DIR = os.path.abspath("audit_renderings/elitia")
os.makedirs(IMG_DIR, exist_ok=True)

# 1. Banned names scan
banned = ["lumbini", "aveva"]
found = []
with zipfile.ZipFile(DECK_PATH, "r") as z:
    for filename in z.namelist():
        content = z.read(filename).decode("utf-8", errors="ignore").lower()
        for b in banned:
            if b in content:
                found.append((filename, b))

print("=== 1. BANNED NAMES SCAN ===")
print(f"Scanned files inside PPTX zip: {len(z.namelist())}")
print(f"Banned occurrences found: {len(found)}")
if found:
    for f, b in found:
        print(f"  [VIOLATION] {f}: found '{b}'")
else:
    print("  [PASS] Zero occurrences of 'Lumbini' or 'AVEVA' anywhere in the package!")

# 2. Structure & Typography Validation
print("\n=== 2. STRUCTURAL & TYPOGRAPHY CHECK ===")
prs = Presentation(DECK_PATH)
print(f"Total slides: {len(prs.slides)}")
assert len(prs.slides) == 8, f"Expected 8 slides, found {len(prs.slides)}"

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

# 3. PowerPoint COM Native Rendering
print("\n=== 3. NATIVE POWERPOINT RENDERING ===")
ppt_app = win32com.client.Dispatch("PowerPoint.Application")
prs_com = ppt_app.Presentations.Open(DECK_PATH, WithWindow=False)

for i, slide in enumerate(prs_com.Slides, 1):
    out_img = os.path.join(IMG_DIR, f"slide_{i}.png")
    slide.Export(out_img, "PNG", 1920, 1080)
    print(f"  Exported Slide {i} -> {out_img}")

prs_com.Close()
ppt_app.Quit()
print("  [PASS] All slides successfully rendered to 1080p images!")
