"""Text measurement and fitting with REAL Inter metrics (no substitute fonts).
API:
  measure(text, bold, pt) -> inches wide (single line)
  wrap(text, bold, pt, inner_w) -> list of lines (words never split; a too-long word is returned as its own line)
  fit_label(text, box_w, box_h, pt=12, min_pt=10, max_lines=2, bold=False, slack=1.06, ins=(0.1,0.05))
      -> {"status": "ok"|"shrunk"|"needs_shorter_label"|"needs_wider_box", "pt": float, "lines": [...], "need_w": float, "need_h": float}
Rules enforced: never go below min_pt; never allow a word wider than the inner width; width is multiplied by `slack`
(default 6%) to cover renderer differences and machines where Inter is missing.
Font files: ../themes/lumbini/fonts/Inter-Regular.otf and Inter-Bold.otf (override with INTER_DIR env var)."""
import os
from PIL import ImageFont
_D = os.environ.get("INTER_DIR") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "themes", "lumbini", "fonts")
_C = {}
def _font(bold):
    if bold not in _C:
        for base in (_D, "/usr/share/fonts/opentype/inter"):
            p = os.path.join(base, "Inter-%s.otf" % ("Bold" if bold else "Regular"))
            if os.path.exists(p):
                _C[bold] = ImageFont.truetype(p, 1000); break
        else:
            raise FileNotFoundError("Inter font files not found; set INTER_DIR")
    return _C[bold]
def measure(text, bold, pt):
    return _font(bold).getlength(text) / 1000.0 * pt / 72.0
def wrap(text, bold, pt, inner_w, slack=1.06):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if measure(t, bold, pt) * slack <= inner_w or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines
def fit_label(text, box_w, box_h, pt=12, min_pt=10, max_lines=2, bold=False, slack=1.06, ins=(0.1, 0.05)):
    iw, ih = box_w - 2 * ins[0], box_h - 2 * ins[1]
    size = float(pt)
    while size >= min_pt - 1e-9:
        lines = wrap(text, bold, size, iw, slack)
        longest = max(measure(l, bold, size) * slack for l in lines) if lines else 0
        need_h = len(lines) * size * 1.2 / 72
        if longest <= iw + 1e-6 and len(lines) <= max_lines and need_h <= ih + 1e-6:
            return {"status": "ok" if size == pt else "shrunk", "pt": size, "lines": lines, "need_w": round(longest, 2), "need_h": round(need_h, 2)}
        size -= 0.5
    lines = wrap(text, bold, min_pt, iw, slack)
    longest = max(measure(l, bold, min_pt) * slack for l in lines) if lines else 0
    st = "needs_wider_box" if longest > iw else "needs_shorter_label"
    return {"status": st, "pt": min_pt, "lines": lines, "need_w": round(longest, 2), "need_h": round(len(lines) * min_pt * 1.2 / 72, 2)}
if __name__ == "__main__":
    for t, w, h in [("Tier 4: Analytics Consumption", 1.8, 0.7), ("Tier 4: Analytics Consumption", 2.9, 0.7), ("Space Governance", 1.8, 0.7)]:
        print(t, w, h, fit_label(t, w, h, pt=13, bold=True))
