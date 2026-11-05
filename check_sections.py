import zipfile
import re

for path in ['themes/lumbini/template.pptx', 'reference/negative_example_datasphere_after_v2.pptx', 'SAP_Datasphere_Career_Path.pptx', 'tests/out/deck1_sgg/SGG_ELITIA_BI_Odoo_Proposal.pptx']:
    try:
        with zipfile.ZipFile(path, 'r') as z:
            if 'ppt/presentation.xml' in z.namelist():
                xml = z.read('ppt/presentation.xml').decode('utf-8')
                has_sec = 'sectionLst' in xml
                secs = re.findall(r'<p14:section\b[^>]*\bname="([^"]+)"', xml)
                print(f"{path}: has_sectionLst={has_sec}, sections={secs}")
    except Exception as e:
        print(f"{path}: error {e}")
