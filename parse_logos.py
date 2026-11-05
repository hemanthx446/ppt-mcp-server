import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation

prs = Presentation('references/Lumbini_SAP_ME_DMC_AMS_Proposal.pptx')
slide16 = prs.slides[15] # 0-indexed 15 = slide 16
print('=== Slide 16 Shapes ===')
for shape in slide16.shapes:
    if shape.has_text_frame:
        print('Text:', shape.text_frame.text.strip())
    elif shape.shape_type == 13: # picture
        print('Picture name:', shape.name)

# Also check The_Connected_Enterprise_TEPL_Lumbini.pptx Slide 14
prs_tepl = Presentation('references/The_Connected_Enterprise_TEPL_Lumbini.pptx')
slide14 = prs_tepl.slides[13]
print('=== TEPL Slide 14 Shapes ===')
for shape in slide14.shapes:
    if shape.has_text_frame:
        print('Text:', shape.text_frame.text.strip())
    elif shape.shape_type == 13:
        print('Picture name:', shape.name)
