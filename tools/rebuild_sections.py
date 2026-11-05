#!/usr/bin/env python3
"""Rewrite (or remove) the section list of a .pptx from a mapping, discarding whatever sections it carried.
Usage: python3 -I rebuild_sections.py in.pptx out.pptx sections.json
sections.json: [{"name":"Context","slides":[1,2]},{"name":"Architecture","slides":[3,4]}]  (1-based slide numbers in presentation order)
       or []  -> remove all sections.
Rules enforced: every slide in exactly one section; no empty section."""
import sys, re, json, uuid, zipfile
src, dst, mp = sys.argv[1:4]; secs = json.load(open(mp))
z = zipfile.ZipFile(src); pres = z.read("ppt/presentation.xml").decode()
ids = re.findall(r'<p:sldId id="(\d+)"', pres); n = len(ids)
if secs:
    flat = [s for sec in secs for s in sec["slides"]]
    assert sorted(flat) == list(range(1, n + 1)), f"sections must cover slides 1..{n} exactly once; got {sorted(flat)}"
    assert all(sec["slides"] for sec in secs), "empty section"
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")
pres = re.sub(r'<p:ext uri="\{521415D9-36F7-43E2-AB2F-B90AF26B5E84\}">.*?</p:ext>', "", pres, flags=re.S)
if secs:
    body = "".join('<p14:section name="%s" id="{%s}"><p14:sldIdLst>%s</p14:sldIdLst></p14:section>' % (esc(s["name"]), str(uuid.uuid4()).upper(), "".join('<p14:sldId id="%s"/>' % ids[i - 1] for i in s["slides"])) for s in secs)
    ext = '<p:ext uri="{521415D9-36F7-43E2-AB2F-B90AF26B5E84}"><p14:sectionLst xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main">%s</p14:sectionLst></p:ext>' % body
    if "<p:extLst>" in pres: pres = pres.replace("<p:extLst>", "<p:extLst>" + ext, 1)
    else: pres = pres.replace("</p:presentation>", "<p:extLst>" + ext + "</p:extLst></p:presentation>")
pres = re.sub(r"<p:extLst>\s*</p:extLst>", "", pres)
with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as out:
    for it in z.infolist(): out.writestr(it, pres.encode() if it.filename == "ppt/presentation.xml" else z.read(it.filename))
print("wrote", dst, "sections:", [s["name"] for s in secs] or "none")
