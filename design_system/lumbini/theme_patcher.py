import os
import re
import zipfile
import shutil
import tempfile
from typing import Dict, Any

SLOTS = ["dk1", "lt1", "dk2", "lt2", "accent1", "accent2", "accent3", "accent4", "accent5", "accent6", "hlink", "folHlink"]

LUMBINI_THEME_COLORS = {
    "name": "Lumbini Elite",
    "dk1": "141E2D",
    "lt1": "FFFFFF",
    "dk2": "1F497D",
    "lt2": "EEF3F8",
    "accent1": "0070C0",
    "accent2": "F78B15",
    "accent3": "0066B4",
    "accent4": "646E78",
    "accent5": "DCE1E6",
    "accent6": "1F497D",
    "hlink": "0070C0",
    "folHlink": "646E78"
}

def patch_theme_xml(xml_content: str, theme_data: Dict[str, str] = None) -> str:
    if theme_data is None:
        theme_data = LUMBINI_THEME_COLORS
    theme_name = theme_data.get("name", "Lumbini Elite")
    
    scheme_parts = [f'<a:clrScheme name="{theme_name}">']
    for slot in SLOTS:
        val = theme_data.get(slot, "000000").upper().lstrip("#")
        scheme_parts.append(f'<a:{slot}><a:srgbClr val="{val}"/></a:{slot}>')
    scheme_parts.append('</a:clrScheme>')
    scheme_xml = "".join(scheme_parts)

    out = re.sub(r'<a:clrScheme\b[\s\S]*?<\/a:clrScheme>', scheme_xml, xml_content)
    out = re.sub(r'(<a:(?:theme|fontScheme)\b[^>]*?\bname=")[^"]*"', rf'\g<1>{theme_name}"', out)
    
    # Ensure Inter fonts in fontScheme
    font_scheme = (
        f'<a:fontScheme name="{theme_name}">'
        '<a:majorFont>'
        '<a:latin typeface="Inter"/>'
        '<a:ea typeface=""/>'
        '<a:cs typeface=""/>'
        '</a:majorFont>'
        '<a:minorFont>'
        '<a:latin typeface="Inter"/>'
        '<a:ea typeface=""/>'
        '<a:cs typeface=""/>'
        '</a:minorFont>'
        '</a:fontScheme>'
    )
    out = re.sub(r'<a:fontScheme\b[\s\S]*?<\/a:fontScheme>', font_scheme, out)
    return out

def patch_presentation_xml(xml_content: str) -> str:
    # Replace sldSz to 16:9 widescreen without type="screen4x3"
    widescreen_sz = '<p:sldSz cx="12192000" cy="6858000"/>'
    out = re.sub(r'<p:sldSz\b[^>]*?\/>', widescreen_sz, xml_content)
    
    # Enforce strict ECMA-376 schema sequence: notesMasterIdLst MUST precede sldIdLst
    # Schema: sldMasterIdLst -> notesMasterIdLst -> handoutMasterIdLst -> sldIdLst -> sldSz ...
    if '<p:notesMasterIdLst' in out and '<p:sldIdLst' in out:
        notes_m = re.search(r'<p:notesMasterIdLst\b[\s\S]*?<\/p:notesMasterIdLst>', out)
        sld_m = re.search(r'<p:sldIdLst\b[\s\S]*?<\/p:sldIdLst>|<p:sldIdLst\s*\/>', out)
        if notes_m and sld_m and notes_m.start() > sld_m.start():
            notes_str = notes_m.group(0)
            # Remove notesMasterIdLst from its current position
            out = out[:notes_m.start()] + out[notes_m.end():]
            # Find sldIdLst again in the updated string
            sld_m2 = re.search(r'<p:sldIdLst\b[\s\S]*?<\/p:sldIdLst>|<p:sldIdLst\s*\/>', out)
            if sld_m2:
                # Insert notesMasterIdLst before sldIdLst
                out = out[:sld_m2.start()] + notes_str + out[sld_m2.start():]
    return out

def apply_lumbini_theme_to_pptx(deck_path: str, out_path: str = None) -> str:
    if not out_path:
        out_path = deck_path
    deck_path = os.path.abspath(deck_path)
    out_path = os.path.abspath(out_path)

    temp_dir = tempfile.mkdtemp(prefix="pptx_theme_")
    try:
        with zipfile.ZipFile(deck_path, 'r') as zin:
            zin.extractall(temp_dir)

        theme_file = os.path.join(temp_dir, "ppt", "theme", "theme1.xml")
        if os.path.exists(theme_file):
            with open(theme_file, "r", encoding="utf-8") as f:
                theme_xml = f.read()
            patched_theme = patch_theme_xml(theme_xml)
            with open(theme_file, "w", encoding="utf-8") as f:
                f.write(patched_theme)

        pres_file = os.path.join(temp_dir, "ppt", "presentation.xml")
        if os.path.exists(pres_file):
            with open(pres_file, "r", encoding="utf-8") as f:
                pres_xml = f.read()
            patched_pres = patch_presentation_xml(pres_xml)
            with open(pres_file, "w", encoding="utf-8") as f:
                f.write(patched_pres)

        # Repack zip
        temp_zip = os.path.join(os.path.dirname(temp_dir), "repack.pptx")
        with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zout:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    full_p = os.path.join(root, file)
                    rel_p = os.path.relpath(full_p, temp_dir)
                    zout.write(full_p, rel_p)

        shutil.move(temp_zip, out_path)
        return out_path
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
