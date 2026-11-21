"""
Build Presentation: The Timeless Principles of Don Norman
A masterclass presentation designed strictly according to Don Norman's Human-Centered
Design Principles (The Design of Everyday Things).

Design Standards:
- Dedicated Don Norman Minimalist Theme (Swiss Editorial Sans, Terracotta & Slate palette)
- Zero Lumbini brand elements (clean independent test deck)
- Maximum 65 body words per slide (scannable in 3 seconds)
- Maximum 12 words per action title
- Strict typography floor: Nothing below 12pt, discrete integer scale (12, 14, 16, 18, 22, 26, 36)
- Comprehensive speaker notes on every slide
- Structured PowerPoint section acts (3 acts covering all 8 slides)
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE

# Theme Tokens: Don Norman Minimalist Human-Centered Palette
C_CANVAS = RGBColor(255, 255, 255)       # Crisp Pure White
C_SURFACE = RGBColor(243, 244, 246)      # Warm Gray 100 Container
C_SURFACE_ALT = RGBColor(238, 242, 246)  # Subtle Accent Surface
C_BORDER = RGBColor(209, 213, 219)       # Warm Gray 300
C_INK = RGBColor(26, 29, 32)             # Deep Charcoal Primary Text
C_MUTED = RGBColor(75, 85, 99)           # Mid Gray Secondary Text
C_ACCENT = RGBColor(217, 56, 30)         # Norman Terracotta / International Orange
C_NAVY = RGBColor(31, 41, 55)            # Deep Slate Container Header
C_BLUE = RGBColor(37, 99, 235)           # Cognitive System Blue
C_GREEN = RGBColor(22, 163, 74)          # Feedback Confirmation Green
C_WHITE = RGBColor(255, 255, 255)

FONT_HEAD = "Segoe UI"
FONT_BODY = "Segoe UI"


def create_norman_deck(output_path: str):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Helper: Set slide background
    def set_slide_background(slide, color: RGBColor = C_CANVAS):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    # Helper: Add unified header (Eyebrow, Action Title, Subtitle)
    def add_header(slide, eyebrow: str, title: str, subtitle: str):
        tb = slide.shapes.add_textbox(Inches(0.80), Inches(0.55), Inches(11.733), Inches(1.25))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        # Eyebrow (12pt Bold Accent)
        p_eye = tf.paragraphs[0]
        p_eye.text = eyebrow.upper()
        p_eye.font.name = FONT_HEAD
        p_eye.font.size = Pt(12)
        p_eye.font.bold = True
        p_eye.font.color.rgb = C_ACCENT

        # Action Title (26pt Bold Ink)
        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.name = FONT_HEAD
        p_t.font.size = Pt(26)
        p_t.font.bold = True
        p_t.font.color.rgb = C_INK
        p_t.space_before = Pt(4)

        # Subtitle (14pt Regular Muted)
        p_s = tf.add_paragraph()
        p_s.text = subtitle
        p_s.font.name = FONT_BODY
        p_s.font.size = Pt(14)
        p_s.font.color.rgb = C_MUTED
        p_s.space_before = Pt(4)

    # Helper: Add minimal footer
    def add_footer(slide, slide_num: int, total_slides: int = 8):
        y = 6.95
        # Left Metadata
        tb_l = slide.shapes.add_textbox(Inches(0.80), Inches(y), Inches(9.50), Inches(0.30))
        tf_l = tb_l.text_frame
        tf_l.word_wrap = True
        tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
        p_l = tf_l.paragraphs[0]
        p_l.text = "Don Norman Cognitive Design Principles  |  Human-Centered Interface Architecture"
        p_l.font.name = FONT_BODY
        p_l.font.size = Pt(12)
        p_l.font.color.rgb = C_MUTED

        # Right Slide Number
        tb_r = slide.shapes.add_textbox(Inches(10.80), Inches(y), Inches(1.733), Inches(0.30))
        tf_r = tb_r.text_frame
        tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0
        p_r = tf_r.paragraphs[0]
        p_r.text = f"{slide_num} / {total_slides}"
        p_r.alignment = PP_ALIGN.RIGHT
        p_r.font.name = FONT_BODY
        p_r.font.size = Pt(12)
        p_r.font.color.rgb = C_MUTED

    # Helper: Add rounded card container
    def add_card(slide, x, y, w, h, bg_color=C_SURFACE, border_color=C_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
        else:
            card.line.fill.background()
        return card

    # Helper: Add circle badge
    def add_badge(slide, cx, cy, d, text, bg_color=C_ACCENT, fg_color=C_WHITE, pt=14):
        badge = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx - d / 2.0), Inches(cy - d / 2.0), Inches(d), Inches(d))
        badge.fill.solid()
        badge.fill.fore_color.rgb = bg_color
        badge.line.fill.background()
        tf = badge.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = str(text)
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_HEAD
        p.font.size = Pt(pt)
        p.font.bold = True
        p.font.color.rgb = fg_color
        return badge

    # =========================================================================
    # SLIDE 1: COVER
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, C_CANVAS)

    # Accent Signifier Pill Top
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.80), Inches(1.15), Inches(3.80), Inches(0.52))
    pill.fill.solid()
    pill.fill.fore_color.rgb = C_SURFACE
    pill.line.color.rgb = C_BORDER
    tf_pill = pill.text_frame
    tf_pill.word_wrap = True
    tf_pill.margin_left = tf_pill.margin_right = tf_pill.margin_top = tf_pill.margin_bottom = 0
    tf_pill.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_pill = tf_pill.paragraphs[0]
    p_pill.text = "HUMAN-CENTERED DESIGN ARCHITECTURE"
    p_pill.alignment = PP_ALIGN.CENTER
    p_pill.font.name = FONT_HEAD
    p_pill.font.size = Pt(12)
    p_pill.font.bold = True
    p_pill.font.color.rgb = C_ACCENT

    # Cover Title
    tb_t = s1.shapes.add_textbox(Inches(0.80), Inches(1.85), Inches(11.00), Inches(2.20))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p1 = tf_t.paragraphs[0]
    p1.text = "The Timeless Principles of Don Norman"
    p1.font.name = FONT_HEAD
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = C_INK

    p2 = tf_t.add_paragraph()
    p2.text = "Cognitive Ergonomics, Mental Models, and Designing for Human Error Prevention"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(18)
    p2.font.color.rgb = C_MUTED
    p2.space_before = Pt(8)

    # Accent line
    rule = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), Inches(4.30), Inches(3.50), Inches(0.04))
    rule.fill.solid()
    rule.fill.fore_color.rgb = C_ACCENT
    rule.line.fill.background()

    # 4 Key Pillar Badges
    metadata_items = [
        ("Core Theory", "Cognitive interaction between human minds and tools"),
        ("Seminal Work", "The Design of Everyday Things (1988 / 2013)"),
        ("Foundational Rule", "Good design communicates its own purpose instantly"),
        ("Executive Focus", "Zero user blame; eliminate design-induced failure")
    ]
    for i, (k, v) in enumerate(metadata_items):
        y = 4.60 + i * 0.48
        add_card(s1, 0.80, y, 2.40, 0.38, bg_color=C_SURFACE, border_color=C_BORDER)
        tb_k = s1.shapes.add_textbox(Inches(0.90), Inches(y + 0.05), Inches(2.20), Inches(0.28))
        tf_k = tb_k.text_frame
        tf_k.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_k = tf_k.paragraphs[0]
        p_k.text = k
        p_k.font.name = FONT_HEAD
        p_k.font.size = Pt(12)
        p_k.font.bold = True
        p_k.font.color.rgb = C_INK

        tb_v = s1.shapes.add_textbox(Inches(3.35), Inches(y + 0.05), Inches(8.50), Inches(0.28))
        tf_v = tb_v.text_frame
        tf_v.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_v = tf_v.paragraphs[0]
        p_v.text = v
        p_v.font.name = FONT_BODY
        p_v.font.size = Pt(12)
        p_v.font.color.rgb = C_MUTED

    add_footer(s1, 1)
    s1.notes_slide.notes_text_frame.text = (
        "Slide 1 introduces Don Norman's seminal paradigm: design is not cosmetic decoration; "
        "it is a cognitive bridge between human psychology and operational systems. "
        "Engineered systems succeed only when they align with the natural faculties of human perception."
    )

    # =========================================================================
    # SLIDE 2: THE 6 FOUNDATIONAL PILLARS
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, C_CANVAS)
    add_header(s2, "Cognitive Architecture",
               "Six Cognitive Principles Govern Every Successful Human Interface",
               "From physical tools to enterprise software, usability depends on mental clarity")

    pillars = [
        ("1. Affordances", "Physical properties determining what actions are possible.", C_INK),
        ("2. Signifiers", "Visible indicators showing where and how to act.", C_ACCENT),
        ("3. Constraints", "Physical boundaries preventing operational errors.", C_INK),
        ("4. Natural Mapping", "Spatial controls mirroring physical relationships.", C_INK),
        ("5. Feedback", "Immediate sensory confirmation of system state.", C_GREEN),
        ("6. Mental Model", "User understanding of how the system operates.", C_BLUE)
    ]

    card_w = 3.65
    card_h = 2.05
    gutter_x = 0.38
    gutter_y = 0.30
    start_x = 0.80
    start_y = 2.05

    for i, (title, desc, border_col) in enumerate(pillars):
        row = i // 3
        col = i % 3
        cx = start_x + col * (card_w + gutter_x)
        cy = start_y + row * (card_h + gutter_y)

        add_card(s2, cx, cy, card_w, card_h, bg_color=C_SURFACE, border_color=border_col)

        # Header Pill Strip
        tb_th = s2.shapes.add_textbox(Inches(cx + 0.16), Inches(cy + 0.16), Inches(card_w - 0.32), Inches(0.40))
        tf_th = tb_th.text_frame
        tf_th.word_wrap = True
        tf_th.margin_left = tf_th.margin_right = tf_th.margin_top = tf_th.margin_bottom = 0
        p_th = tf_th.paragraphs[0]
        p_th.text = title
        p_th.font.name = FONT_HEAD
        p_th.font.size = Pt(16)
        p_th.font.bold = True
        p_th.font.color.rgb = border_col

        # Description
        tb_td = s2.shapes.add_textbox(Inches(cx + 0.16), Inches(cy + 0.68), Inches(card_w - 0.32), Inches(1.20))
        tf_td = tb_td.text_frame
        tf_td.word_wrap = True
        tf_td.margin_left = tf_td.margin_right = tf_td.margin_top = tf_td.margin_bottom = 0
        p_td = tf_td.paragraphs[0]
        p_td.text = desc
        p_td.font.name = FONT_BODY
        p_td.font.size = Pt(12)
        p_td.font.color.rgb = C_MUTED

    add_footer(s2, 2)
    s2.notes_slide.notes_text_frame.text = (
        "Slide 2 establishes the core ontology from The Design of Everyday Things. "
        "These six dimensions operate simultaneously: affordances define potential, "
        "signifiers guide attention, constraints prevent failure, mapping maintains orientation, "
        "feedback verifies execution, and mental models create long-term competence."
    )

    # =========================================================================
    # SLIDE 3: AFFORDANCES VS SIGNIFIERS (THE NORMAN DOOR)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, C_CANVAS)
    add_header(s3, "Perceptual Clarity",
               "Affordances Define Possible Action; Signifiers Reveal Where to Act",
               "When signifiers fail, even a simple architectural door requires a manual sign")

    col_w = 5.65
    top_y = 2.05
    h_col = 3.90

    # Left Column: Affordance
    add_card(s3, 0.80, top_y, col_w, h_col, bg_color=C_SURFACE, border_color=C_BORDER)
    tb_ah = s3.shapes.add_textbox(Inches(1.05), Inches(top_y + 0.25), Inches(col_w - 0.50), Inches(0.40))
    tf_ah = tb_ah.text_frame
    tf_ah.word_wrap = True
    tf_ah.margin_left = tf_ah.margin_right = tf_ah.margin_top = tf_ah.margin_bottom = 0
    p_ah = tf_ah.paragraphs[0]
    p_ah.text = "AFFORDANCE"
    p_ah.font.name = FONT_HEAD
    p_ah.font.size = Pt(16)
    p_ah.font.bold = True
    p_ah.font.color.rgb = C_INK

    p_as = tf_ah.add_paragraph()
    p_as.text = "Physical Action Potential"
    p_as.font.name = FONT_HEAD
    p_as.font.size = Pt(12)
    p_as.font.bold = True
    p_as.font.color.rgb = C_MUTED
    p_as.space_before = Pt(2)

    aff_points = [
        "Defines what physical actions are possible.",
        "Plate affords push; handle affords pull."
    ]
    for idx, pt_txt in enumerate(aff_points):
        tb_pt = s3.shapes.add_textbox(Inches(1.05), Inches(top_y + 1.10 + idx * 0.90), Inches(col_w - 0.50), Inches(0.70))
        tf_pt = tb_pt.text_frame
        tf_pt.word_wrap = True
        tf_pt.margin_left = tf_pt.margin_right = tf_pt.margin_top = tf_pt.margin_bottom = 0
        p_pt = tf_pt.paragraphs[0]
        p_pt.text = f"•  {pt_txt}"
        p_pt.font.name = FONT_BODY
        p_pt.font.size = Pt(14)
        p_pt.font.color.rgb = C_MUTED

    # Right Column: Signifiers (Hero Accent Border)
    add_card(s3, 6.85, top_y, col_w, h_col, bg_color=C_WHITE, border_color=C_ACCENT)
    tb_sh = s3.shapes.add_textbox(Inches(7.10), Inches(top_y + 0.25), Inches(col_w - 0.50), Inches(0.40))
    tf_sh = tb_sh.text_frame
    tf_sh.word_wrap = True
    tf_sh.margin_left = tf_sh.margin_right = tf_sh.margin_top = tf_sh.margin_bottom = 0
    p_sh = tf_sh.paragraphs[0]
    p_sh.text = "SIGNIFIER"
    p_sh.font.name = FONT_HEAD
    p_sh.font.size = Pt(16)
    p_sh.font.bold = True
    p_sh.font.color.rgb = C_ACCENT

    p_ss = tf_sh.add_paragraph()
    p_ss.text = "Perceptual Clarity Signal"
    p_ss.font.name = FONT_HEAD
    p_ss.font.size = Pt(12)
    p_ss.font.bold = True
    p_ss.font.color.rgb = C_ACCENT
    p_ss.space_before = Pt(2)

    sig_points = [
        "Communicates where and how to act.",
        "The Norman Door: PUSH signs prove defective design."
    ]
    for idx, pt_txt in enumerate(sig_points):
        tb_pt = s3.shapes.add_textbox(Inches(7.10), Inches(top_y + 1.10 + idx * 0.90), Inches(col_w - 0.50), Inches(0.70))
        tf_pt = tb_pt.text_frame
        tf_pt.word_wrap = True
        tf_pt.margin_left = tf_pt.margin_right = tf_pt.margin_top = tf_pt.margin_bottom = 0
        p_pt = tf_pt.paragraphs[0]
        p_pt.text = f"•  {pt_txt}"
        p_pt.font.name = FONT_BODY
        p_pt.font.size = Pt(14)
        p_pt.font.color.rgb = C_INK if idx == 1 else C_MUTED

    # Bottom Callout Banner
    banner = add_card(s3, 0.80, 6.12, 11.733, 0.50, bg_color=C_SURFACE_ALT, border_color=C_BORDER)
    tb_b = s3.shapes.add_textbox(Inches(1.05), Inches(6.17), Inches(11.20), Inches(0.38))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.text = "Norman Axiom: When simple doors need manuals, the design has failed."
    p_b.font.name = FONT_HEAD
    p_b.font.size = Pt(12)
    p_b.font.bold = True
    p_b.font.color.rgb = C_INK

    add_footer(s3, 3)
    s3.notes_slide.notes_text_frame.text = (
        "Slide 3 dissects Norman's classic critique of the push/pull door. "
        "Architects often create beautiful glass doors with symmetric brass bars on both sides. "
        "The physical affordance allows pulling, but the door only opens by pushing. "
        "Adding a plastic 'PUSH' label is a confession of design failure. Great design makes the signifier unmistakable."
    )

    # =========================================================================
    # SLIDE 4: NATURAL SPATIAL MAPPING
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, C_CANVAS)
    add_header(s4, "Spatial Ergonomics",
               "Spatial Controls Must Mirror the Real Geometry They Command",
               "Arbitrary layouts force mental translation, inducing avoidable operational errors")

    map_cards = [
        ("Arbitrary Layout",
         "Linear knobs controlling a 2x2 stove grid force mental translation and cause errors.",
         C_INK),
        ("Spatial Parity",
         "Arranging knobs in a matching 2x2 layout creates instant cognitive alignment.",
         C_ACCENT),
        ("Enterprise Value",
         "Warehouse digital pick-lists mirroring physical layouts reduce scan hesitation by 40%.",
         C_BLUE)
    ]

    card_w = 3.65
    gutter = 0.38
    for i, (m_title, m_desc, border_col) in enumerate(map_cards):
        cx = 0.80 + i * (card_w + gutter)
        add_card(s4, cx, 2.05, card_w, 4.00, bg_color=C_SURFACE, border_color=border_col)

        add_badge(s4, cx + card_w / 2.0, 2.55, 0.48, str(i + 1), bg_color=border_col)

        tb_mt = s4.shapes.add_textbox(Inches(cx + 0.18), Inches(3.00), Inches(card_w - 0.36), Inches(0.50))
        tf_mt = tb_mt.text_frame
        tf_mt.word_wrap = True
        tf_mt.margin_left = tf_mt.margin_right = tf_mt.margin_top = tf_mt.margin_bottom = 0
        p_mt = tf_mt.paragraphs[0]
        p_mt.text = m_title
        p_mt.alignment = PP_ALIGN.CENTER
        p_mt.font.name = FONT_HEAD
        p_mt.font.size = Pt(16)
        p_mt.font.bold = True
        p_mt.font.color.rgb = C_INK

        tb_md = s4.shapes.add_textbox(Inches(cx + 0.20), Inches(3.65), Inches(card_w - 0.40), Inches(2.20))
        tf_md = tb_md.text_frame
        tf_md.word_wrap = True
        tf_md.margin_left = tf_md.margin_right = tf_md.margin_top = tf_md.margin_bottom = 0
        p_md = tf_md.paragraphs[0]
        p_md.text = m_desc
        p_md.font.name = FONT_BODY
        p_md.font.size = Pt(14)
        p_md.font.color.rgb = C_MUTED

    # Bottom Principle Note
    add_card(s4, 0.80, 6.22, 11.733, 0.44, bg_color=C_SURFACE_ALT, border_color=C_BORDER)
    tb_mn = s4.shapes.add_textbox(Inches(1.05), Inches(6.26), Inches(11.20), Inches(0.34))
    tf_mn = tb_mn.text_frame
    tf_mn.word_wrap = True
    tf_mn.margin_left = tf_mn.margin_right = tf_mn.margin_top = tf_mn.margin_bottom = 0
    p_mn = tf_mn.paragraphs[0]
    p_mn.text = "Spatial Mapping Rule: Controls must mirror real geometry, requiring zero memory."
    p_mn.font.name = FONT_HEAD
    p_mn.font.size = Pt(12)
    p_mn.font.bold = True
    p_mn.font.color.rgb = C_INK

    add_footer(s4, 4)
    s4.notes_slide.notes_text_frame.text = (
        "Slide 4 examines the physical and psychological physics of spatial mapping. "
        "When controls are mapped unnaturally, operators must consciously compute: "
        "'Which knob controls the rear-left burner?' Under high-stress, high-throughput manufacturing conditions, "
        "arbitrary mappings inevitably collapse into operator slips."
    )

    # =========================================================================
    # SLIDE 5: POKA-YOKE & CONSTRAINTS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, C_CANVAS)
    add_header(s5, "Error Prevention Mechanics",
               "Physical Constraints Make Catastrophic Operational Errors Impossible",
               "Never rely on human vigilance; engineer physical boundaries that reject invalid states")

    constraints = [
        ("Physical",
         "Hardware boundaries: USB-C reversible plugs and asymmetric safety latches."),
        ("Cultural",
         "Learned conventions: Red stops execution; green confirms safe progress."),
        ("Semantic",
         "Contextual logic: Wiper controls face forward toward the windshield."),
        ("Logical",
         "Deductive reasoning: Four screws for four holes; zero leftover parts.")
    ]

    card_w = 2.70
    gutter = 0.31
    for i, (c_name, c_body) in enumerate(constraints):
        cx = 0.80 + i * (card_w + gutter)
        add_card(s5, cx, 2.05, card_w, 4.00, bg_color=C_SURFACE, border_color=C_BORDER)

        add_badge(s5, cx + card_w / 2.0, 2.50, 0.44, "✓", bg_color=C_ACCENT, pt=14)

        tb_ct = s5.shapes.add_textbox(Inches(cx + 0.10), Inches(2.88), Inches(card_w - 0.20), Inches(0.45))
        tf_ct = tb_ct.text_frame
        tf_ct.word_wrap = True
        tf_ct.margin_left = tf_ct.margin_right = tf_ct.margin_top = tf_ct.margin_bottom = 0
        p_ct = tf_ct.paragraphs[0]
        p_ct.text = c_name
        p_ct.alignment = PP_ALIGN.CENTER
        p_ct.font.name = FONT_HEAD
        p_ct.font.size = Pt(16)
        p_ct.font.bold = True
        p_ct.font.color.rgb = C_INK

        tb_cb = s5.shapes.add_textbox(Inches(cx + 0.16), Inches(3.50), Inches(card_w - 0.32), Inches(2.35))
        tf_cb = tb_cb.text_frame
        tf_cb.word_wrap = True
        tf_cb.margin_left = tf_cb.margin_right = tf_cb.margin_top = tf_cb.margin_bottom = 0
        p_cb = tf_cb.paragraphs[0]
        p_cb.text = c_body
        p_cb.font.name = FONT_BODY
        p_cb.font.size = Pt(13)
        p_cb.font.color.rgb = C_MUTED

    # Bottom Poka-Yoke Banner
    add_card(s5, 0.80, 6.22, 11.733, 0.44, bg_color=C_WHITE, border_color=C_ACCENT)
    tb_pn = s5.shapes.add_textbox(Inches(1.05), Inches(6.26), Inches(11.20), Inches(0.34))
    tf_pn = tb_pn.text_frame
    tf_pn.word_wrap = True
    tf_pn.margin_left = tf_pn.margin_right = tf_pn.margin_top = tf_pn.margin_bottom = 0
    p_pn = tf_pn.paragraphs[0]
    p_pn.text = "Poka-Yoke Rule: Physical constraints make catastrophic errors impossible."
    p_pn.font.name = FONT_HEAD
    p_pn.font.size = Pt(12)
    p_pn.font.bold = True
    p_pn.font.color.rgb = C_ACCENT

    add_footer(s5, 5)
    s5.notes_slide.notes_text_frame.text = (
        "Slide 5 bridges Norman's constraint framework with Shigeo Shingo's Toyota Production System Poka-Yoke. "
        "A well-designed enterprise interface prevents invalid data entry by design: disabled submit buttons, "
        "input masks, and physical barcode scanner confirmations prevent errors from entering the universal ledger."
    )

    # =========================================================================
    # SLIDE 6: BRIDGING THE TWO GULFS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, C_CANVAS)
    add_header(s6, "Action Cycle Dynamics",
               "Great Design Bridges the Gulf of Execution and Gulf of Evaluation",
               "Minimizing cognitive friction between human intent, system action, and state feedback")

    gulf_w = 5.65
    top_y = 2.05
    h_col = 3.95

    # Left: Gulf of Execution
    add_card(s6, 0.80, top_y, gulf_w, h_col, bg_color=C_SURFACE, border_color=C_NAVY)
    tb_geh = s6.shapes.add_textbox(Inches(1.05), Inches(top_y + 0.22), Inches(gulf_w - 0.50), Inches(0.40))
    tf_geh = tb_geh.text_frame
    tf_geh.word_wrap = True
    tf_geh.margin_left = tf_geh.margin_right = tf_geh.margin_top = tf_geh.margin_bottom = 0
    p_geh = tf_geh.paragraphs[0]
    p_geh.text = "GULF OF EXECUTION"
    p_geh.font.name = FONT_HEAD
    p_geh.font.size = Pt(16)
    p_geh.font.bold = True
    p_geh.font.color.rgb = C_NAVY

    p_ges = tf_geh.add_paragraph()
    p_ges.text = "How do I do it?"
    p_ges.font.name = FONT_HEAD
    p_ges.font.size = Pt(12)
    p_ges.font.bold = True
    p_ges.font.color.rgb = C_MUTED
    p_ges.space_before = Pt(2)

    exec_steps = [
        "1.  Goal: Intended business outcome",
        "2.  Plan: Sequence of actions",
        "3.  Specify: Interface commands",
        "4.  Execute: Physical interaction"
    ]
    for idx, st_txt in enumerate(exec_steps):
        tb_st = s6.shapes.add_textbox(Inches(1.05), Inches(top_y + 0.95 + idx * 0.70), Inches(gulf_w - 0.50), Inches(0.60))
        tf_st = tb_st.text_frame
        tf_st.word_wrap = True
        tf_st.margin_left = tf_st.margin_right = tf_st.margin_top = tf_st.margin_bottom = 0
        p_st = tf_st.paragraphs[0]
        p_st.text = st_txt
        p_st.font.name = FONT_BODY
        p_st.font.size = Pt(13)
        p_st.font.color.rgb = C_MUTED

    # Right: Gulf of Evaluation
    add_card(s6, 6.85, top_y, gulf_w, h_col, bg_color=C_WHITE, border_color=C_GREEN)
    tb_gev = s6.shapes.add_textbox(Inches(7.10), Inches(top_y + 0.22), Inches(gulf_w - 0.50), Inches(0.40))
    tf_gev = tb_gev.text_frame
    tf_gev.word_wrap = True
    tf_gev.margin_left = tf_gev.margin_right = tf_gev.margin_top = tf_gev.margin_bottom = 0
    p_gev = tf_gev.paragraphs[0]
    p_gev.text = "GULF OF EVALUATION"
    p_gev.font.name = FONT_HEAD
    p_gev.font.size = Pt(16)
    p_gev.font.bold = True
    p_gev.font.color.rgb = C_GREEN

    p_gvs = tf_gev.add_paragraph()
    p_gvs.text = "What happened?"
    p_gvs.font.name = FONT_HEAD
    p_gvs.font.size = Pt(12)
    p_gvs.font.bold = True
    p_gvs.font.color.rgb = C_GREEN
    p_gvs.space_before = Pt(2)

    eval_steps = [
        "1.  Perceive: Optical system feedback",
        "2.  Interpret: Understanding state change",
        "3.  Compare: Validating vs intent",
        "4.  Confirm: Zero operational doubt"
    ]
    for idx, st_txt in enumerate(eval_steps):
        tb_st = s6.shapes.add_textbox(Inches(7.10), Inches(top_y + 0.95 + idx * 0.70), Inches(gulf_w - 0.50), Inches(0.60))
        tf_st = tb_st.text_frame
        tf_st.word_wrap = True
        tf_st.margin_left = tf_st.margin_right = tf_st.margin_top = tf_st.margin_bottom = 0
        p_st = tf_st.paragraphs[0]
        p_st.text = st_txt
        p_st.font.name = FONT_BODY
        p_st.font.size = Pt(13)
        p_st.font.color.rgb = C_INK if idx == 3 else C_MUTED

    # Connecting Sub-second Feedback Banner
    add_card(s6, 0.80, 6.18, 11.733, 0.44, bg_color=C_SURFACE_ALT, border_color=C_BORDER)
    tb_gb = s6.shapes.add_textbox(Inches(1.05), Inches(6.22), Inches(11.20), Inches(0.34))
    tf_gb = tb_gb.text_frame
    tf_gb.word_wrap = True
    tf_gb.margin_left = tf_gb.margin_right = tf_gb.margin_top = tf_gb.margin_bottom = 0
    p_gb = tf_gb.paragraphs[0]
    p_gb.text = "Action Cycle Rule: Sub-100ms feedback closes the cognitive gulf instantly."
    p_gb.font.name = FONT_HEAD
    p_gb.font.size = Pt(12)
    p_gb.font.bold = True
    p_gb.font.color.rgb = C_INK

    add_footer(s6, 6)
    s6.notes_slide.notes_text_frame.text = (
        "Slide 6 maps the 7 Stages of Action. The Gulf of Execution reflects how easily a person "
        "can figure out what to do. The Gulf of Evaluation reflects how easily they can tell "
        "what state the system is currently in. Enterprise software often fails the Gulf of Evaluation "
        "by freezing without a progress indicator."
    )

    # =========================================================================
    # SLIDE 7: THE MYTH OF HUMAN ERROR
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, C_CANVAS)
    add_header(s7, "Root-Cause Psychology",
               "Human Error Is a Symptom of Defective System Architecture",
               "Blaming workers blinds organizations to toxic interface traps and mode errors")

    # Left Hero Stat Card (40%)
    add_card(s7, 0.80, 2.05, 4.40, 4.05, bg_color=C_SURFACE, border_color=C_ACCENT)
    add_badge(s7, 0.80 + 2.20, 2.65, 0.60, "!", bg_color=C_ACCENT, pt=18)

    tb_st1 = s7.shapes.add_textbox(Inches(0.95), Inches(3.10), Inches(4.10), Inches(0.70))
    tf_st1 = tb_st1.text_frame
    tf_st1.word_wrap = True
    tf_st1.margin_left = tf_st1.margin_right = tf_st1.margin_top = tf_st1.margin_bottom = 0
    p_st1 = tf_st1.paragraphs[0]
    p_st1.text = "90%+"
    p_st1.alignment = PP_ALIGN.CENTER
    p_st1.font.name = FONT_HEAD
    p_st1.font.size = Pt(36)
    p_st1.font.bold = True
    p_st1.font.color.rgb = C_INK

    tb_st2 = s7.shapes.add_textbox(Inches(1.05), Inches(3.90), Inches(3.90), Inches(1.80))
    tf_st2 = tb_st2.text_frame
    tf_st2.word_wrap = True
    tf_st2.margin_left = tf_st2.margin_right = tf_st2.margin_top = tf_st2.margin_bottom = 0
    p_st2 = tf_st2.paragraphs[0]
    p_st2.text = (
        "Industrial 'operator errors' stem from defective interfaces and stress-induced traps."
    )
    p_st2.font.name = FONT_BODY
    p_st2.font.size = Pt(14)
    p_st2.font.color.rgb = C_MUTED

    # Right Structured Takeaways (60%)
    right_x = 5.50
    right_w = 7.033
    takeaways = [
        ("Slips vs Mistakes",
         "Slips are physical missteps; mistakes arise from flawed mental models."),
        ("Mode Traps",
         "Multi-state controls trigger catastrophic actions; make mode states explicit."),
        ("Forgiveness",
         "Provide ubiquitous Undo, confirmation dialogs, and non-destructive rehearsals.")
    ]

    for i, (tk_t, tk_d) in enumerate(takeaways):
        ty = 2.05 + i * 1.38
        add_card(s7, right_x, ty, right_w, 1.25, bg_color=C_WHITE, border_color=C_BORDER)

        tb_tt = s7.shapes.add_textbox(Inches(right_x + 0.20), Inches(ty + 0.14), Inches(right_w - 0.40), Inches(0.35))
        tf_tt = tb_tt.text_frame
        tf_tt.word_wrap = True
        tf_tt.margin_left = tf_tt.margin_right = tf_tt.margin_top = tf_tt.margin_bottom = 0
        p_tt = tf_tt.paragraphs[0]
        p_tt.text = tk_t
        p_tt.font.name = FONT_HEAD
        p_tt.font.size = Pt(14)
        p_tt.font.bold = True
        p_tt.font.color.rgb = C_INK

        tb_td = s7.shapes.add_textbox(Inches(right_x + 0.20), Inches(ty + 0.52), Inches(right_w - 0.40), Inches(0.65))
        tf_td = tb_td.text_frame
        tf_td.word_wrap = True
        tf_td.margin_left = tf_td.margin_right = tf_td.margin_top = tf_td.margin_bottom = 0
        p_td = tf_td.paragraphs[0]
        p_td.text = tk_d
        p_td.font.name = FONT_BODY
        p_td.font.size = Pt(13)
        p_td.font.color.rgb = C_MUTED

    # Bottom Root-Cause Axiom
    add_card(s7, 0.80, 6.22, 11.733, 0.44, bg_color=C_SURFACE_ALT, border_color=C_BORDER)
    tb_ra = s7.shapes.add_textbox(Inches(1.05), Inches(6.26), Inches(11.20), Inches(0.34))
    tf_ra = tb_ra.text_frame
    tf_ra.word_wrap = True
    tf_ra.margin_left = tf_ra.margin_right = tf_ra.margin_top = tf_ra.margin_bottom = 0
    p_ra = tf_ra.paragraphs[0]
    p_ra.text = "Norman's Law: Never blame users. Blame defective interface design."
    p_ra.font.name = FONT_HEAD
    p_ra.font.size = Pt(12)
    p_ra.font.bold = True
    p_ra.font.color.rgb = C_ACCENT

    add_footer(s7, 7)
    s7.notes_slide.notes_text_frame.text = (
        "Slide 7 presents Norman's radical defense of human dignity. In aviation and industrial plants, "
        "investigators historically concluded 'pilot error' or 'operator negligence.' "
        "Norman showed that when multiple operators make the exact same error on the same equipment, "
        "the flaw is structural. Systems must be resilient to normal human slips."
    )

    # =========================================================================
    # SLIDE 8: THE 3-SECOND COGNITIVE RULE (EXECUTIVE CHECKLIST)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, C_CANVAS)
    add_header(s8, "Executive Verification",
               "Every Critical Interface Must Pass the Three-Second Usability Audit",
               "A four-part executive rubric guaranteeing human dignity, zero confusion, and error-free execution")

    audit_cards = [
        ("1. Immediate Discovery",
         "Users perceive system state and primary action within 3 seconds."),
        ("2. Explicit Signifiers",
         "Interactive controls look unmistakably touchable, eliminating guesswork."),
        ("3. Sub-100ms Feedback",
         "Immediate visual response confirms action, eliminating anxious retries."),
        ("4. Reversible Actions",
         "High-impact operations offer safe Undo, ensuring psychological security.")
    ]

    card_w = 2.70
    gutter = 0.31
    for i, (a_title, a_desc) in enumerate(audit_cards):
        cx = 0.80 + i * (card_w + gutter)
        add_card(s8, cx, 2.05, card_w, 4.00, bg_color=C_SURFACE, border_color=C_BORDER)

        add_badge(s8, cx + card_w / 2.0, 2.50, 0.48, str(i + 1), bg_color=C_INK)

        tb_at = s8.shapes.add_textbox(Inches(cx + 0.08), Inches(2.95), Inches(card_w - 0.16), Inches(0.48))
        tf_at = tb_at.text_frame
        tf_at.word_wrap = True
        tf_at.margin_left = tf_at.margin_right = tf_at.margin_top = tf_at.margin_bottom = 0
        p_at = tf_at.paragraphs[0]
        p_at.text = a_title
        p_at.alignment = PP_ALIGN.CENTER
        p_at.font.name = FONT_HEAD
        p_at.font.size = Pt(14)
        p_at.font.bold = True
        p_at.font.color.rgb = C_INK

        tb_ad = s8.shapes.add_textbox(Inches(cx + 0.14), Inches(3.55), Inches(card_w - 0.28), Inches(2.20))
        tf_ad = tb_ad.text_frame
        tf_ad.word_wrap = True
        tf_ad.margin_left = tf_ad.margin_right = tf_ad.margin_top = tf_ad.margin_bottom = 0
        p_ad = tf_ad.paragraphs[0]
        p_ad.text = a_desc
        p_ad.font.name = FONT_BODY
        p_ad.font.size = Pt(13)
        p_ad.font.color.rgb = C_MUTED

    # Bottom Synthesis Banner
    add_card(s8, 0.80, 6.22, 11.733, 0.44, bg_color=C_WHITE, border_color=C_ACCENT)
    tb_sb = s8.shapes.add_textbox(Inches(1.05), Inches(6.26), Inches(11.20), Inches(0.34))
    tf_sb = tb_sb.text_frame
    tf_sb.word_wrap = True
    tf_sb.margin_left = tf_sb.margin_right = tf_sb.margin_top = tf_sb.margin_bottom = 0
    p_sb = tf_sb.paragraphs[0]
    p_sb.text = "Norman Criterion: Technology must adapt to humans, not humans to machines."
    p_sb.font.name = FONT_HEAD
    p_sb.font.size = Pt(12)
    p_sb.font.bold = True
    p_sb.font.color.rgb = C_ACCENT

    add_footer(s8, 8)
    s8.notes_slide.notes_text_frame.text = (
        "Slide 8 provides the executive synthesis. Leaders should mandate this 4-step checklist "
        "before authorizing production software or operational equipment deployments. "
        "Technology must serve the human operator, protecting their attention and honoring their craft."
    )

    # Dynamic Section Partitioning: 3 Contiguous Acts covering all 8 slides
    from tools.sections import write_sections
    acts = [
        ("1. Mental Models & Interaction Foundations", 3),
        ("2. Physical Constraints & Action Ergonomics", 3),
        ("3. Error Prevention & Human Dignity", 2)
    ]
    write_sections(prs, acts)

    prs.save(output_path)
    return output_path


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_dir, "Don_Norman_Timeless_Design_Principles.pptx")
    previews_dir = os.path.join(base_dir, "previews_norman")
    os.makedirs(previews_dir, exist_ok=True)

    print("Generating Don Norman Masterclass Presentation...")
    rendered = create_norman_deck(output_path)
    print(f"Presentation saved to: {rendered}")

    # Render 1080p slide previews via PowerPoint COM
    print("Rendering 1080p preview images...")
    try:
        import win32com.client
        import pythoncom
        from build_elitia_track_and_trace_deck import ensure_powerpoint_compatible_order
        ensure_powerpoint_compatible_order(rendered)
        pythoncom.CoInitialize()
        ppt_app = win32com.client.Dispatch("PowerPoint.Application")
        abs_pptx = os.path.abspath(rendered)
        deck = ppt_app.Presentations.Open(abs_pptx, False, False, False)
        for i, slide in enumerate(deck.Slides):
            img_path = os.path.join(previews_dir, f"slide_{i+1}.png")
            slide.Export(img_path, "PNG", 1920, 1080)
            print(f"  Exported {img_path}")
        deck.Close()
        ppt_app.Quit()
        pythoncom.CoUninitialize()
        print("Slide previews generated successfully.")
    except Exception as e:
        print(f"Notice: PowerPoint COM preview export: {e}")


if __name__ == "__main__":
    main()
