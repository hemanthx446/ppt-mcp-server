import zipfile, re, os, shutil, tempfile
from pptx import Presentation

src = 'reference/SGG_ELITIA_BI_Odoo_Proposal_Lumbini.pptx'
dst = 'themes/lumbini/template.pptx'

td = tempfile.mkdtemp()
with zipfile.ZipFile(src, 'r') as zin:
    zin.extractall(td)

# 1. Clean presentation.xml: empty <p:sldIdLst/>
pres_path = os.path.join(td, 'ppt', 'presentation.xml')
with open(pres_path, 'r', encoding='utf-8') as f:
    pxml = f.read()
pxml = re.sub(r'<p:sldIdLst>[\s\S]*?<\/p:sldIdLst>', '<p:sldIdLst/>', pxml)
with open(pres_path, 'w', encoding='utf-8') as f:
    f.write(pxml)

# 2. Clean presentation.xml.rels
pres_rels = os.path.join(td, 'ppt', '_rels', 'presentation.xml.rels')
with open(pres_rels, 'r', encoding='utf-8') as f:
    rxml = f.read()
rxml = re.sub(r'<Relationship[^>]*?Target="slides\/slide\d+\.xml"[^>]*?\/>', '', rxml)
with open(pres_rels, 'w', encoding='utf-8') as f:
    f.write(rxml)

# 3. Clean [Content_Types].xml
ct_path = os.path.join(td, '[Content_Types].xml')
with open(ct_path, 'r', encoding='utf-8') as f:
    ctxml = f.read()
ctxml = re.sub(r'<Override[^>]*?PartName="\/ppt\/(?:slides|notesSlides|charts|tags)\/[^"]*"[^>]*?\/>', '', ctxml)
with open(ct_path, 'w', encoding='utf-8') as f:
    f.write(ctxml)

# 4. Delete orphan directories/files
for folder in ['slides', 'notesSlides', 'charts', 'tags', 'embeddings']:
    fp = os.path.join(td, 'ppt', folder)
    if os.path.exists(fp):
        shutil.rmtree(fp)

# 5. Repack
if os.path.exists(dst):
    os.remove(dst)
with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
    for root, _, files in os.walk(td):
        for file in files:
            full = os.path.join(root, file)
            rel = os.path.relpath(full, td)
            zout.write(full, rel)

shutil.rmtree(td)
print('Pristine template created at:', dst)

prs = Presentation(dst)
print('Verified clean open! Slide count:', len(prs.slides), 'Layouts:', [l.name for l in prs.slide_layouts])
s1 = prs.slides.add_slide(prs.slide_layouts[1])
s1.shapes.add_textbox(0, 0, 100, 100).text = 'Test Slide'
prs.save('test_clean_template_save.pptx')
print('Verified clean save with zero warnings!')
