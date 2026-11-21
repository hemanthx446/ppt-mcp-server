#!/usr/bin/env python3
"""Deck QA: sections, text fit (real Inter metrics), bounds, leaks, density.
Usage: python3 -I qa_pptx.py deck.pptx [--min-pt 10] [--slack 1.06] [--reference ref.pptx [--brief brief.txt]] [--json out.json]
Exit code 1 if any BLOCKING finding. Limitations: top-level shapes only (group transforms ignored); table cells are not measured."""
import zipfile, re, sys, os, json, argparse, html
if hasattr(sys.stdout, "reconfigure"):
    try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from textfit import measure
EMU = 914400.0
ap = argparse.ArgumentParser(); ap.add_argument("deck"); ap.add_argument("--min-pt", type=float, default=12)
ap.add_argument("--slack", type=float, default=1.06); ap.add_argument("--reference", action="append", default=[])
ap.add_argument("--brief"); ap.add_argument("--json"); ap.add_argument("--min-slides-for-sections", type=int, default=8)
a = ap.parse_args()
F = []  # (level, slide, code, msg)
def add(lv, s, c, m): F.append((lv, s, c, m))
z = zipfile.ZipFile(a.deck)
pres = z.read("ppt/presentation.xml").decode()
SW = int(re.search(r'<p:sldSz cx="(\d+)"', pres).group(1)) / EMU; SH = int(re.search(r'<p:sldSz cx="\d+" cy="(\d+)"', pres).group(1)) / EMU
live = re.findall(r'<p:sldId id="(\d+)"', pres)
# ---- sections
secs = [(m.group(1), re.findall(r'<p14:sldId id="(\d+)"', m.group(2))) for m in re.finditer(r'<p14:section name="([^"]*)"[^>]*>(.*?)</p14:section>', pres, re.S)]
if secs:
    seen = set()
    for i, (nm, ids) in enumerate(secs):
        dang = [x for x in ids if x not in live]; real = [x for x in ids if x in live]; seen.update(real)
        if dang: add("BLOCK", 0, "SEC_DANGLING", f"section '{nm}' references {len(dang)} slide id(s) that do not exist")
        if not real: add("BLOCK", 0, "SEC_EMPTY", f"section '{nm}' has no slides")
        elif len(real) == 1 and i != len(secs) - 1: add("WARN", 0, "SEC_SINGLE", f"section '{nm}' has a single slide")
    un = [x for x in live if x not in seen]
    if un: add("BLOCK", 0, "SEC_UNASSIGNED", f"{len(un)} slide(s) are outside every section")
    if len(live) < a.min_slides_for_sections: add("WARN", 0, "SEC_NOT_NEEDED", f"{len(live)} slides: sections add no value below {a.min_slides_for_sections}")
    if len(secs) > 5: add("WARN", 0, "SEC_TOO_MANY", f"{len(secs)} sections")
# ---- slides
names = sorted([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)], key=lambda n: int(re.findall(r"\d+", n)[0]))
def ngrams(txt, n=4):
    w = re.findall(r"[a-z0-9\-']+", html.unescape(txt).lower()); return {" ".join(w[i:i+n]) for i in range(len(w) - n + 1)}
deck_text = ""
for idx, n in enumerate(names, 1):
    x = z.read(n).decode(); alltxt = " ".join(re.findall(r"<a:t>([^<]*)</a:t>", x)); deck_text += " " + alltxt
    words = len(alltxt.split())
    if words > 160 and idx != 1: add("WARN", idx, "WORDS", f"{words} words (target <=120, hard 160)")
    for m in re.finditer(r"\[SRC-[^\]]*\]|lorem ipsum|\bTODO\b|\[insert", alltxt, re.I): add("BLOCK", idx, "LEAK_TOKEN", f"unresolved token '{m.group(0)}'")
    for sp in re.findall(r"<p:sp>.*?</p:sp>", x, re.S):
        o = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/><a:ext cx="(\d+)" cy="(\d+)"', sp)
        txts = re.findall(r"<a:t>([^<]*)</a:t>", sp)
        if not o or "<p:ph " in sp or "slidenum" in sp: continue
        ox, oy, cx, cy = [int(v) / EMU for v in o.groups()]
        if txts and (ox < -0.01 or oy < -0.01 or ox + cx > SW + 0.01 or oy + cy > SH + 0.01):
            add("BLOCK", idx, "TEXT_OUT_OF_SLIDE", f"text box '{' '.join(txts)[:30]}' spans x {ox:.2f}-{ox+cx:.2f} (slide {SW:.2f}x{SH:.2f})")
        if not txts: continue
        bp = re.search(r"<a:bodyPr([^>]*)", sp).group(1)
        g = lambda k, d: int(re.search(k + r'="(\d+)"', bp).group(1)) / EMU if k + "=" in bp else d
        iw = cx - g("lIns", .1) - g("rIns", .1); ih = cy - g("tIns", .05) - g("bIns", .05)
        nowrap = 'wrap="none"' in bp; need = 0
        for para in re.findall(r"<a:p>.*?</a:p>", sp, re.S):
            t = "".join(re.findall(r"<a:t>([^<]*)</a:t>", para)).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
            if not t.strip(): continue
            szs = [int(s) / 100 for s in re.findall(r' sz="(\d+)"', para)]
            if not szs: continue  # size inherited from layout: cannot measure here
            sz = max(szs); b = 'b="1"' in para or "Bold" in para or "SemiBold" in para
            if min(szs) < a.min_pt and not (idx > 0 and min(szs) >= 9 and ox > -1 and (oy > SH - 0.6)):
                add("BLOCK" if min(szs) < 8 else "WARN", idx, "FONT_SMALL", f"{min(szs)}pt in '{t[:28]}'")
            lines, cur = 1, 0.0; sp_ = measure(" ", b, sz) * a.slack
            for w in t.split():
                ww = measure(w, b, sz) * a.slack
                if ww > iw + .01: add("BLOCK", idx, "WORD_WIDER_THAN_BOX", f"'{w}' needs {ww:.2f}in, box inner width {iw:.2f}in")
                if cur and cur + sp_ + ww > iw: lines += 1; cur = ww
                else: cur += (sp_ if cur else 0) + ww
            if nowrap and measure(t, b, sz) * a.slack > iw + .01: add("BLOCK", idx, "NOWRAP_OVERFLOW", f"'{t[:34]}' needs {measure(t,b,sz)*a.slack:.2f}in in {iw:.2f}in with wrap=none (neighbour will hide it)")
            need += lines * sz * 1.2 / 72
        if ih > .05 and need > ih + .08: add("BLOCK", idx, "TEXT_TALLER_THAN_BOX", f"'{' '.join(txts)[:32]}' needs {need:.2f}in, has {ih:.2f}in")
# ---- leakage vs reference decks
if a.reference:
    ref = set()
    for r in a.reference:
        rz = zipfile.ZipFile(r)
        for n in rz.namelist():
            if re.match(r"ppt/slides/slide\d+\.xml$", n): ref |= ngrams(" ".join(re.findall(r"<a:t>([^<]*)</a:t>", rz.read(n).decode())))
    allowed = ngrams(open(a.brief, encoding="utf-8", errors="ignore").read()) if a.brief else set()
    leak = sorted(g for g in (ngrams(deck_text) & ref) - allowed if not any(k in g for k in ("lumbini","elite solutions","solutions services")))
    if leak: add("BLOCK" if len(leak) > 3 else "WARN", 0, "REFERENCE_LEAK", f"{len(leak)} 4-gram(s) shared with reference decks and absent from the brief, e.g. {leak[:4]}")
B = [f for f in F if f[0] == "BLOCK"]; W = [f for f in F if f[0] == "WARN"]
print(f"{a.deck}: {len(live)} slides, {len(secs)} section(s) -> {len(B)} blocking, {len(W)} warning")
for lv, s, c, m in sorted(F, key=lambda f: (f[0] != "BLOCK", f[1])): print(f"  [{lv}] slide {s or '-'} {c}: {m}")
if a.json: json.dump([dict(level=l, slide=s, code=c, message=m) for l, s, c, m in F], open(a.json, "w"), indent=1)
sys.exit(1 if B else 0)
