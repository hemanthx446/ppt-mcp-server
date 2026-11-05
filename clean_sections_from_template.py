import zipfile
import re
import tempfile
import os
import shutil

template_path = os.path.abspath('themes/lumbini/template.pptx')
temp_dir = tempfile.mkdtemp(prefix='tmpl_clean_')

try:
    with zipfile.ZipFile(template_path, 'r') as zin:
        zin.extractall(temp_dir)

    pres_xml_path = os.path.join(temp_dir, 'ppt', 'presentation.xml')
    with open(pres_xml_path, 'r', encoding='utf-8') as f:
        xml = f.read()

    # Remove p14:sectionLst extension
    xml = re.sub(r'<p:ext uri="\{521415D9-36F7-43E2-AB2F-B90AF26B5E84\}">.*?</p:ext>', '', xml, flags=re.S)
    xml = re.sub(r'<p:extLst>\s*</p:extLst>', '', xml)

    with open(pres_xml_path, 'w', encoding='utf-8') as f:
        f.write(xml)

    # Repack zip
    temp_zip = os.path.join(os.path.dirname(temp_dir), 'cleaned_template.pptx')
    with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zout:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                full_p = os.path.join(root, file)
                rel_p = os.path.relpath(full_p, temp_dir)
                zout.write(full_p, rel_p)

    shutil.copy2(temp_zip, template_path)
    os.remove(temp_zip)
    print("Cleaned template.pptx successfully!")
finally:
    shutil.rmtree(temp_dir, ignore_errors=True)
