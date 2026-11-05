import sys
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation

prs = Presentation('references/Supply_Chain_Resilience_A_Strategic_Advantage.pptx')
slide21 = prs.slides[20]
print('=== Slide 21 Shapes ===')
for s in slide21.shapes:
    if s.has_text_frame:
        print('Text:', s.text_frame.text)
