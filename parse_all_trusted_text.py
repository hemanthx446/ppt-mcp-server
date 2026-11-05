import glob, sys
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation

for f in glob.glob('references/*.pptx'):
    try:
        prs = Presentation(f)
        for idx, s in enumerate(prs.slides):
            for sh in s.shapes:
                if sh.has_text_frame:
                    t = sh.text_frame.text.strip()
                    for name in ['moil', 'nmdc', 'petronet', 'tvnl', 'jbvnl', 'bhel', 'vs&co', 'prometheus', 'elior', 'alghanim', 'gyansis', 'inchure', 'stellium', 'tata', 'hical', 'healthium']:
                        if name in t.lower():
                            print(f'[{f} Slide {idx+1}] Matched {name}: {t[:120]}')
    except:
        pass
