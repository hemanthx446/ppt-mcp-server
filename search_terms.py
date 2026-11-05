import sys, os, glob
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation

keywords = ['gcc', 'odc', 'usa', 'united states', 'middle east', 'qatar', 'dubai', '2013', '2026', 'safeexpress', 'safe express', 'sell partner', 'service partner', 'timeline']

files = glob.glob('references/*.pptx') + glob.glob('*.pptx')
for f in files:
    try:
        prs = Presentation(f)
        for idx, slide in enumerate(prs.slides):
            text_chunks = []
            for shape in slide.shapes:
                if shape.has_text_frame:
                    text_chunks.append(shape.text_frame.text)
            full_text = ' '.join(text_chunks).lower()
            found = [k for k in keywords if k in full_text]
            if found:
                print(f'[{os.path.basename(f)} - Slide {idx+1}] Found: {found}')
                # print snippet
                for p in full_text.split('\n'):
                    if any(k in p for k in found):
                        print('   --> ' + p.strip()[:100])
    except Exception as e:
        pass
