import os
import win32com.client

PPTX_PATH = os.path.abspath("JBVNL_Transformation_Decision_Playbook.pptx")
PDF_PATH = os.path.abspath("JBVNL_Transformation_Decision_Playbook.pdf")
IMG_DIR = os.path.abspath("previews_jbvnl_decision")

os.makedirs(IMG_DIR, exist_ok=True)

print(f"Opening: {PPTX_PATH}")
ppt_app = win32com.client.Dispatch("PowerPoint.Application")
try:
    prs_com = ppt_app.Presentations.Open(PPTX_PATH, WithWindow=False)

    print(f"Exporting PDF -> {PDF_PATH}")
    prs_com.SaveAs(PDF_PATH, 32) # 32 = ppSaveAsPDF

    print(f"Exporting slide PNGs -> {IMG_DIR}")
    for i, slide in enumerate(prs_com.Slides, 1):
        out_img = os.path.join(IMG_DIR, f"slide_{i}.png")
        slide.Export(out_img, "PNG", 1920, 1080)
        print(f"  Exported Slide {i} -> {out_img}")

    prs_com.Close()
finally:
    ppt_app.Quit()

print("Export completed successfully!")
