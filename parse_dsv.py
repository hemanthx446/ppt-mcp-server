import xml.etree.ElementTree as ET
import re

tree = ET.parse('dsv_stream_11.bin')
root = tree.getroot()

print('=== PARSED CELLS FROM DRAW.IO DIAGRAM ===')
for cell in root.iter('mxCell'):
    val = cell.attrib.get('value', '').replace('&nbsp;', ' ').replace('&amp;', '&')
    if val:
        clean = re.sub(r'<[^>]+>', '', val).strip()
        if len(clean) > 2:
            print(f"- {clean}")
