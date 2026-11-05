import sys
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation

for f in ['references/Hical_Strategic_CXO_Dashboards_Proposal_v2.pptx', 'references/Hical_TRACE_n_TRACE_Executive_Proposal_v2.pptx']:
    prs = Presentation(f)
    print(f'=== {f} ({len(prs.slides)} slides) ===')
    for idx, slide in enumerate(prs.slides):
        print(f'-- Slide {idx+1} --')
        for shape in slide.shapes:
            if shape.has_text_frame:
                t = shape.text_frame.text.strip()
                if t:
                    print('  ' + '\n  '.join(t.splitlines()[:6]))
