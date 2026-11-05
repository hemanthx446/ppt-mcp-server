"""
Write PowerPoint sections (the collapsible groups in the slide navigator) with python-pptx.

Rules (see UPDATE_v3 §2):
  - Sections are the acts of THIS deck's storyline, named in the topic's own language.
  - Decide them after the slide plan exists. Never copy names from another deck.
  - No deck under 8 slides gets sections. 2 to 5 sections otherwise. Each has >= 2 slides.
  - Every slide belongs to exactly one section; sections are contiguous.
"""
import uuid
from lxml import etree

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"
URI = "{521415D9-36F7-43E2-AB2F-B90AF26B5E84}"


def plan_ok(n_slides, acts):
    """acts: list of (name, n_slides_in_act). Returns (ok, reason)."""
    if n_slides < 8:
        return False, "deck under 8 slides: no sections"
    if not 2 <= len(acts) <= 5:
        return False, "use 2 to 5 sections"
    if sum(n for _, n in acts) != n_slides:
        return False, "sections must cover every slide exactly once"
    if any(n < 2 for _, n in acts):
        return False, "each section needs at least 2 slides"
    return True, "ok"


def remove_sections(prs):
    """Remove any sectionLst from the presentation."""
    pres = prs.part._element
    ext_lst = pres.find(f"{{{P}}}extLst")
    if ext_lst is not None:
        for e in list(ext_lst):
            if e.get("uri") == URI:
                ext_lst.remove(e)
        if len(ext_lst) == 0:
            pres.remove(ext_lst)


def write_sections(prs, acts):
    """acts: list of (section_name, number_of_slides). Replaces any existing sections.
    Call only when plan_ok(...) is True; otherwise leave the deck without sections."""
    pres = prs.part._element
    ids = [s.get("id") for s in pres.find(f"{{{P}}}sldIdLst")]
    ok, why = plan_ok(len(ids), acts)
    if not ok:
        raise ValueError(f"no sections written: {why}")
    ext_lst = pres.find(f"{{{P}}}extLst")
    if ext_lst is None:
        ext_lst = etree.SubElement(pres, f"{{{P}}}extLst")      # must be the last child
    for e in list(ext_lst):
        if e.get("uri") == URI:
            ext_lst.remove(e)
    ext = etree.SubElement(ext_lst, f"{{{P}}}ext", uri=URI)
    sl = etree.SubElement(ext, f"{{{P14}}}sectionLst", nsmap={"p14": P14})
    i = 0
    for name, n in acts:
        sec = etree.SubElement(sl, f"{{{P14}}}section", name=name, id="{" + str(uuid.uuid4()).upper() + "}")
        lst = etree.SubElement(sec, f"{{{P14}}}sldIdLst")
        for sid in ids[i:i + n]:
            etree.SubElement(lst, f"{{{P14}}}sldId", id=sid)
        i += n
