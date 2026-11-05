"""
python-pptx helpers that make text clipping structurally impossible.

Why this exists: python-pptx's add_textbox() writes <a:bodyPr wrap="none"> plus <a:spAutoFit/>.
Text then never wraps, runs past its container, and is cut off by the shape next to it.
Formatting set through paragraph.font lands on <a:pPr><a:defRPr>, which some viewers ignore.

Rules enforced here:
  1. Label text lives INSIDE its shape's own text frame (node, pill, chevron, card), so the
     container and the text can never drift apart.
  2. wrap is always "square", auto-size is always NONE, margins are explicit.
  3. Font, size, bold and colour are written on every run (<a:rPr>), never only on the paragraph.
  4. Size comes from a measure-then-fit step using the real Inter files; if text does not fit,
     shorten the text or widen/split the layout. Never shrink below the token floor (10pt body).
"""
from pptx.util import Pt, Inches, Emu
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN, MSO_AUTO_SIZE
from pptx.dml.color import RGBColor
from PIL import ImageFont

FONTS_DIR = "themes/lumbini/fonts"
_FILES = {"regular": "Inter-Regular.otf", "semibold": "Inter-SemiBold.otf", "bold": "Inter-Bold.otf"}
_cache = {}


def _font(weight, pt):
    k = (weight, pt)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(f"{FONTS_DIR}/{_FILES[weight]}", int(pt * 10))
    return _cache[k]


def width_in(text, weight="regular", pt=12):
    return _font(weight, pt).getlength(text) / 10.0 / 72.0


def lines_needed(text, weight, pt, inner_w_in):
    n = 0
    for para in text.split("\n"):
        cur, k = "", 1
        for w in para.split(" "):
            trial = (cur + " " + w).strip()
            if width_in(trial, weight, pt) <= inner_w_in or not cur:
                cur = trial
            else:
                k, cur = k + 1, w
        n += k
    return n


def fit_pt(text, weight, box_w_in, box_h_in, start_pt, min_pt=10, pad_in=0.08, safety=1.12):
    """Largest size in [min_pt, start_pt] that fits with a safety factor for font fallback.
    Returns None when even min_pt does not fit: caller must shorten the text or enlarge the box."""
    inner_w = (box_w_in - 2 * pad_in) / safety
    inner_h = box_h_in - 2 * 0.04
    pt = start_pt
    while pt >= min_pt:
        longest = max(width_in(w, weight, pt) for w in text.replace("\n", " ").split(" "))
        if longest <= inner_w and lines_needed(text, weight, pt, inner_w) * pt * 1.2 / 72.0 <= inner_h:
            return pt
        pt -= 0.5
    return None


def set_text(shape, text, *, face="Inter", weight="regular", pt=12, color="141E2D",
             align="left", anchor="middle", pad_in=0.08, italic=False):
    """Write text into an existing shape/textbox safely. Supports '\n' for paragraphs."""
    tf = shape.text_frame
    tf.word_wrap = True                       # wrap="square"
    tf.auto_size = MSO_AUTO_SIZE.NONE         # no spAutoFit / shrink surprises
    tf.margin_left = tf.margin_right = Inches(pad_in)
    tf.margin_top = tf.margin_bottom = Inches(0.04)
    tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}[anchor]
    typeface = {"regular": face, "semibold": f"{face} SemiBold", "bold": face}[weight]
    for i, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}[align]
        r = p.add_run()
        r.text = line
        f = r.font                            # run-level <a:rPr>
        f.name, f.size, f.bold, f.italic = typeface, Pt(pt), weight == "bold", italic
        f.color.rgb = RGBColor.from_string(color)
    return shape


def label_in_shape(shape, text, *, weight="semibold", start_pt=13, min_pt=10, **kw):
    """Fit then write. Raises ValueError so the pipeline shortens text instead of clipping it."""
    w, h = shape.width / 914400.0, shape.height / 914400.0
    pt = fit_pt(text, weight, w, h, start_pt, min_pt)
    if pt is None:
        raise ValueError(f"'{text}' does not fit {w:.2f}x{h:.2f}in at >= {min_pt}pt: shorten, widen, or re-layout.")
    return set_text(shape, text, weight=weight, pt=pt, **kw)
