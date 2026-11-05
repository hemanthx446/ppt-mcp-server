import zipfile
import re
import os
import tempfile
import shutil

template_path = 'themes/lumbini/template.pptx'
td = tempfile.mkdtemp()
with zipfile.ZipFile(template_path, 'r') as zin:
    zin.extractall(td)

# 1. Clean slideLayout2.xml: remove shape with id=8 (Text 5)
sl2_path = os.path.join(td, 'ppt', 'slideLayouts', 'slideLayout2.xml')
with open(sl2_path, 'r', encoding='utf-8') as f:
    xml = f.read()

# Replace the static footer shape containing SGG
pattern = r'<p:sp><p:nvSpPr><p:cNvPr id="8" name="Text 5">[\s\S]*?<\/p:sp>'
xml_cleaned = re.sub(pattern, '', xml)
with open(sl2_path, 'w', encoding='utf-8') as f:
    f.write(xml_cleaned)

# Also check all slideLayouts for any lingering SGG
for fname in os.listdir(os.path.join(td, 'ppt', 'slideLayouts')):
    if fname.endswith('.xml'):
        p = os.path.join(td, 'ppt', 'slideLayouts', fname)
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'SGG' in content:
            print(f'Warning: SGG found in {fname}, cleaning...')
            content = re.sub(r'Confidential proposal for SGG', 'Confidential', content)
            with open(p, 'w', encoding='utf-8') as f:
                f.write(content)

# 2. Clean docProps/core.xml
core_path = os.path.join(td, 'docProps', 'core.xml')
if os.path.exists(core_path):
    with open(core_path, 'r', encoding='utf-8') as f:
        cxml = f.read()
    cxml = re.sub(r'<dc:title>[\s\S]*?<\/dc:title>', '<dc:title>Lumbini Enterprise Presentation Template</dc:title>', cxml)
    with open(core_path, 'w', encoding='utf-8') as f:
        f.write(cxml)

# Repack template.pptx
if os.path.exists(template_path):
    os.remove(template_path)
with zipfile.ZipFile(template_path, 'w', zipfile.ZIP_DEFLATED) as zout:
    for root, _, files in os.walk(td):
        for file in files:
            full = os.path.join(root, file)
            rel = os.path.relpath(full, td)
            zout.write(full, rel)

shutil.rmtree(td)
print('Template successfully cleaned of SGG leaks!')
