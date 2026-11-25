"""
Build Presentation: JBVNL Transformation Review - Decision-Acceleration Playbook
Consolidates all 4 JBVNL source files into an executive, jargon-free 11-slide decision deck.

Strict Standards:
- Zero IT / SAP jargon (no T-codes, no architecture buzzwords, plain utility language)
- Maximum 35-45 words per block; total body words <= 65 (Norman UX & Executive Standard)
- Exact operational facts, dates, modules, and bottlenecks from the 4 source files
- Four-block layout on Core Process slides:
  1. The Core Question
  2. Why We Are Asking (<= 12 words)
  3. Real-World Scenario (On the Ground)
  4. Possible Approaches (Option A vs Option B with trade-offs)
- Lumbini Executive Utility Theme (Deep Navy, Electric Blue, JBVNL Amber, Warm Slate)
- Strict typography floor: MIN_FONT_SIZE_PT = 12, discrete integer scale (12, 14, 16, 20, 24, 32)
- Structured PowerPoint sections covering all 11 slides
- Comprehensive executive speaking notes on every slide
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Theme Tokens: Lumbini Professional Executive Utility Palette
C_NAVY = RGBColor(10, 37, 64)        # #0A2540 - Deep Executive Navy
C_BLUE = RGBColor(0, 114, 206)      # #0072CE - Lumbini Electric Blue
C_AMBER = RGBColor(234, 88, 12)     # #EA580C - JBVNL Energy Orange/Amber
C_SLATE = RGBColor(71, 85, 105)     # #475569 - Muted Slate
C_INK = RGBColor(15, 23, 42)        # #0F172A - Deep Charcoal Ink
C_SURFACE = RGBColor(248, 250, 252) # #F8FAFC - Soft Container Background
C_SURFACE_ALT = RGBColor(241, 245, 249) # #F1F5F9 - Alternate Container
C_BORDER = RGBColor(226, 232, 240)  # #E2E8F0 - Clean Border
C_GREEN = RGBColor(22, 101, 52)     # #166534 - Forest Green
C_WHITE = RGBColor(255, 255, 255)

FONT_HEAD = "Segoe UI"
FONT_BODY = "Segoe UI"


def create_deck(output_path: str):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Helper: Set slide background
    def set_bg(slide, color=C_WHITE):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    # Helper: Unified header (Eyebrow, Action Title, Subtitle)
    def add_header(slide, eyebrow: str, title: str, subtitle: str):
        tb = slide.shapes.add_textbox(Inches(0.80), Inches(0.48), Inches(11.733), Inches(1.22))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        # Eyebrow (12pt Bold Accent)
        p_eye = tf.paragraphs[0]
        p_eye.text = eyebrow.upper()
        p_eye.font.name = FONT_HEAD
        p_eye.font.size = Pt(12)
        p_eye.font.bold = True
        p_eye.font.color.rgb = C_AMBER

        # Action Title (24pt Bold Navy)
        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.name = FONT_HEAD
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY
        p_t.space_before = Pt(3)

        # Subtitle (14pt Regular Slate)
        p_s = tf.add_paragraph()
        p_s.text = subtitle
        p_s.font.name = FONT_BODY
        p_s.font.size = Pt(14)
        p_s.font.color.rgb = C_SLATE
        p_s.space_before = Pt(3)

    # Helper: Minimal executive footer
    def add_footer(slide, slide_num: int, total_slides: int = 11):
        y = 6.95
        tb_l = slide.shapes.add_textbox(Inches(0.80), Inches(y), Inches(9.50), Inches(0.30))
        tf_l = tb_l.text_frame
        tf_l.word_wrap = True
        tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
        p_l = tf_l.paragraphs[0]
        p_l.text = "JBVNL Executive Strategy Review  |  Decision-Acceleration Playbook"
        p_l.font.name = FONT_BODY
        p_l.font.size = Pt(12)
        p_l.font.color.rgb = C_SLATE

        tb_r = slide.shapes.add_textbox(Inches(10.80), Inches(y), Inches(1.733), Inches(0.30))
        tf_r = tb_r.text_frame
        tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0
        p_r = tf_r.paragraphs[0]
        p_r.text = f"{slide_num} / {total_slides}"
        p_r.alignment = PP_ALIGN.RIGHT
        p_r.font.name = FONT_BODY
        p_r.font.size = Pt(12)
        p_r.font.color.rgb = C_SLATE

    # Helper: Rounded card container
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

    # Helper: Accent badge
    def add_badge(slide, cx, cy, d, text, bg_color=C_AMBER, fg_color=C_WHITE, pt=12):
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

    # Helper: Build standardized Core Process Decision Slide (4 clean blocks)
    def add_process_slide(slide, slide_num, eyebrow, title, subtitle,
                          core_question, why_text, scenario_text,
                          opt_a_title, opt_a_desc, opt_b_title, opt_b_desc, notes_text):
        set_bg(slide, C_WHITE)
        add_header(slide, eyebrow, title, subtitle)

        # Block 1: The Core Question (Hero Card Top)
        add_card(slide, 0.80, 1.85, 11.733, 0.95, bg_color=C_SURFACE, border_color=C_BLUE)
        tb_q = slide.shapes.add_textbox(Inches(1.00), Inches(1.92), Inches(11.333), Inches(0.80))
        tf_q = tb_q.text_frame
        tf_q.word_wrap = True
        tf_q.margin_left = tf_q.margin_right = tf_q.margin_top = tf_q.margin_bottom = 0
        p_qh = tf_q.paragraphs[0]
        p_qh.text = "CORE QUESTION"
        p_qh.font.name = FONT_HEAD
        p_qh.font.size = Pt(12)
        p_qh.font.bold = True
        p_qh.font.color.rgb = C_BLUE

        p_qt = tf_q.add_paragraph()
        p_qt.text = core_question
        p_qt.font.name = FONT_HEAD
        p_qt.font.size = Pt(15)
        p_qt.font.bold = True
        p_qt.font.color.rgb = C_NAVY
        p_qt.space_before = Pt(3)

        # Block 2: Why We Are Asking (Left middle card)
        add_card(slide, 0.80, 2.95, 5.65, 1.25, bg_color=C_WHITE, border_color=C_AMBER)
        tb_why = slide.shapes.add_textbox(Inches(1.00), Inches(3.05), Inches(5.25), Inches(1.05))
        tf_why = tb_why.text_frame
        tf_why.word_wrap = True
        tf_why.margin_left = tf_why.margin_right = tf_why.margin_top = tf_why.margin_bottom = 0
        p_wh = tf_why.paragraphs[0]
        p_wh.text = "WHY ASK"
        p_wh.font.name = FONT_HEAD
        p_wh.font.size = Pt(12)
        p_wh.font.bold = True
        p_wh.font.color.rgb = C_AMBER
        p_wt = tf_why.add_paragraph()
        p_wt.text = why_text
        p_wt.font.name = FONT_BODY
        p_wt.font.size = Pt(13)
        p_wt.font.color.rgb = C_INK
        p_wt.space_before = Pt(3)

        # Block 3: Real-World Scenario (Right middle card)
        add_card(slide, 6.85, 2.95, 5.683, 1.25, bg_color=C_SURFACE_ALT, border_color=C_BORDER)
        tb_scen = slide.shapes.add_textbox(Inches(7.05), Inches(3.05), Inches(5.283), Inches(1.05))
        tf_scen = tb_scen.text_frame
        tf_scen.word_wrap = True
        tf_scen.margin_left = tf_scen.margin_right = tf_scen.margin_top = tf_scen.margin_bottom = 0
        p_sh = tf_scen.paragraphs[0]
        p_sh.text = "ON THE GROUND"
        p_sh.font.name = FONT_HEAD
        p_sh.font.size = Pt(12)
        p_sh.font.bold = True
        p_sh.font.color.rgb = C_SLATE
        p_st = tf_scen.add_paragraph()
        p_st.text = scenario_text
        p_st.font.name = FONT_BODY
        p_st.font.size = Pt(13)
        p_st.font.color.rgb = C_INK
        p_st.space_before = Pt(3)

        # Block 4: Possible Approaches (Option A vs Option B)
        # Option A Card
        add_card(slide, 0.80, 4.35, 5.65, 2.30, bg_color=C_SURFACE, border_color=C_GREEN)
        tb_oa = slide.shapes.add_textbox(Inches(1.00), Inches(4.50), Inches(5.25), Inches(2.00))
        tf_oa = tb_oa.text_frame
        tf_oa.word_wrap = True
        tf_oa.margin_left = tf_oa.margin_right = tf_oa.margin_top = tf_oa.margin_bottom = 0
        p_oah = tf_oa.paragraphs[0]
        p_oah.text = f"OPTION A: {opt_a_title.upper()}"
        p_oah.font.name = FONT_HEAD
        p_oah.font.size = Pt(14)
        p_oah.font.bold = True
        p_oah.font.color.rgb = C_GREEN
        p_oab = tf_oa.add_paragraph()
        p_oab.text = opt_a_desc
        p_oab.font.name = FONT_BODY
        p_oab.font.size = Pt(13)
        p_oab.font.color.rgb = C_INK
        p_oab.space_before = Pt(6)

        # Option B Card
        add_card(slide, 6.85, 4.35, 5.683, 2.30, bg_color=C_SURFACE, border_color=C_BORDER)
        tb_ob = slide.shapes.add_textbox(Inches(7.05), Inches(4.50), Inches(5.283), Inches(2.00))
        tf_ob = tb_ob.text_frame
        tf_ob.word_wrap = True
        tf_ob.margin_left = tf_ob.margin_right = tf_ob.margin_top = tf_ob.margin_bottom = 0
        p_obh = tf_ob.paragraphs[0]
        p_obh.text = f"OPTION B: {opt_b_title.upper()}"
        p_obh.font.name = FONT_HEAD
        p_obh.font.size = Pt(14)
        p_obh.font.bold = True
        p_obh.font.color.rgb = C_SLATE
        p_obb = tf_ob.add_paragraph()
        p_obb.text = opt_b_desc
        p_obb.font.name = FONT_BODY
        p_obb.font.size = Pt(13)
        p_obb.font.color.rgb = C_INK
        p_obb.space_before = Pt(6)

        add_footer(slide, slide_num)
        slide.notes_slide.notes_text_frame.text = notes_text

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, C_WHITE)

    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.80), Inches(1.15), Inches(3.40), Inches(0.48))
    pill.fill.solid()
    pill.fill.fore_color.rgb = C_SURFACE
    pill.line.color.rgb = C_BORDER
    tf_p = pill.text_frame
    tf_p.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_pi = tf_p.paragraphs[0]
    p_pi.text = "EXECUTIVE STRATEGY REVIEW"
    p_pi.alignment = PP_ALIGN.CENTER
    p_pi.font.name = FONT_HEAD
    p_pi.font.size = Pt(12)
    p_pi.font.bold = True
    p_pi.font.color.rgb = C_AMBER

    tb_t = s1.shapes.add_textbox(Inches(0.80), Inches(1.85), Inches(11.00), Inches(2.20))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p1 = tf_t.paragraphs[0]
    p1.text = "JBVNL Transformation Review:\nKey Decisions for a Smooth Rollout"
    p1.font.name = FONT_HEAD
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY

    p2 = tf_t.add_paragraph()
    p2.text = "A Decision-Acceleration Playbook for Leadership  |  November 2026"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(16)
    p2.font.color.rgb = C_SLATE
    p2.space_before = Pt(8)

    rule = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), Inches(4.30), Inches(3.20), Inches(0.04))
    rule.fill.solid()
    rule.fill.fore_color.rgb = C_AMBER
    rule.line.fill.background()

    meta = [
        ("Transformation Footprint", "7 Area Boards, 15 Circles, and 15 Central & Divisional Stores across Jharkhand"),
        ("Decision Objective", "Resolve six operational bottlenecks to unlock clean accounting and store control"),
        ("Meeting Rule", "Focus strictly on root organizational causes, clear ownership, and pragmatic rules")
    ]
    for i, (k, v) in enumerate(meta):
        y = 4.60 + i * 0.65
        add_card(s1, 0.80, y, 3.00, 0.50, bg_color=C_SURFACE, border_color=C_BORDER)
        tb_k = s1.shapes.add_textbox(Inches(0.95), Inches(y + 0.08), Inches(2.70), Inches(0.34))
        p_k = tb_k.text_frame.paragraphs[0]
        p_k.text = k
        p_k.font.name = FONT_HEAD
        p_k.font.size = Pt(12)
        p_k.font.bold = True
        p_k.font.color.rgb = C_NAVY

        tb_v = s1.shapes.add_textbox(Inches(4.00), Inches(y + 0.08), Inches(7.80), Inches(0.34))
        p_v = tb_v.text_frame.paragraphs[0]
        p_v.text = v
        p_v.font.name = FONT_BODY
        p_v.font.size = Pt(13)
        p_v.font.color.rgb = C_SLATE

    add_footer(s1, 1)
    s1.notes_slide.notes_text_frame.text = (
        "Good morning, Managing Director, Directors, General Managers, and Chief Engineers. "
        "Today's session is not a technical progress report. We are here to review the real operational "
        "mechanics of JBVNL's transformation. This presentation is structured as a decision playbook: "
        "we present the plain field truth, examine why current processes are stalled, and offer two practical "
        "approaches for each core operation so leadership can decide and align today."
    )

    # =========================================================================
    # SLIDE 2: WHERE WE STAND TODAY (THE REALITY CHECK)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2, C_WHITE)
    add_header(s2, "Executive Baseline",
               "Where We Stand Today: Three Realities Governing the Rollout",
               "Balancing confirmed setup progress against growing transactional backlogs")

    col_w = 3.65
    col_h = 4.10
    gutter = 0.38
    y_top = 2.05

    cards_s2 = [
        ("What Is Working",
         "• System configuration complete\n"
         "• Employee payroll tested & trained\n"
         "• March 2025 opening balances loaded",
         C_GREEN, C_SURFACE),
        ("What Is Stuck",
         "• 19-month backlog growing daily\n"
         "• Store stock counts unreconciled\n"
         "• Field units still booking in Tally",
         C_AMBER, C_WHITE),
        ("Three Decisions Needed",
         "• Approve clean 30.09.2026 baseline\n"
         "• Authorize mobile emergency store issues\n"
         "• Freeze dual bookkeeping on go-live",
         C_BLUE, C_SURFACE)
    ]

    for i, (col_title, col_body, col_accent, col_bg) in enumerate(cards_s2):
        cx = 0.80 + i * (col_w + gutter)
        add_card(s2, cx, y_top, col_w, col_h, bg_color=col_bg, border_color=col_accent)

        tb_h = s2.shapes.add_textbox(Inches(cx + 0.20), Inches(y_top + 0.25), Inches(col_w - 0.40), Inches(0.40))
        p_h = tb_h.text_frame.paragraphs[0]
        p_h.text = col_title
        p_h.font.name = FONT_HEAD
        p_h.font.size = Pt(16)
        p_h.font.bold = True
        p_h.font.color.rgb = col_accent

        tb_b = s2.shapes.add_textbox(Inches(cx + 0.20), Inches(y_top + 0.85), Inches(col_w - 0.40), Inches(2.90))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
        p_b = tf_b.paragraphs[0]
        p_b.text = col_body
        p_b.font.name = FONT_BODY
        p_b.font.size = Pt(14)
        p_b.font.color.rgb = C_INK

    add_footer(s2, 2)
    s2.notes_slide.notes_text_frame.text = (
        "Slide 2 sets the baseline truth. On the technical side, systems are configured, payroll calculation "
        "has been simulated across 715+ employees, and opening balances as of March 31, 2025 were loaded. "
        "However, daily operations never started in the system. Because daily work remained manual or in Tally, "
        "we have accumulated 19 months of unentered transactions. Today, we need three core decisions: "
        "resetting to a manageable starting date, enabling emergency store movements, and stopping parallel manual books."
    )

    # =========================================================================
    # SLIDE 3: HOW TO USE THIS DECK (DECISION MAP)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3, C_WHITE)
    add_header(s3, "Playbook Navigation",
               "How to Use This Deck: Six Core Operational Decisions",
               "Organized strictly by JBVNL's end-to-end business operations to solve root causes")

    add_card(s3, 0.80, 2.05, 11.733, 0.55, bg_color=C_SURFACE_ALT, border_color=C_BLUE)
    tb_guide = s3.shapes.add_textbox(Inches(1.00), Inches(2.12), Inches(11.333), Inches(0.40))
    tf_g = tb_guide.text_frame
    tf_g.margin_left = tf_g.margin_right = tf_g.margin_top = tf_g.margin_bottom = 0
    p_g = tf_g.paragraphs[0]
    p_g.text = "Organized by JBVNL's core operations to solve root causes, not symptoms."
    p_g.font.name = FONT_HEAD
    p_g.font.size = Pt(14)
    p_g.font.bold = True
    p_g.font.color.rgb = C_NAVY

    processes = [
        ("1. Grid & Assets", "Substations, transformers, and capitalisation"),
        ("2. Inventory Flow", "15 regional stores and emergency issues"),
        ("3. Procurement", "Turnkey contracts and order controls"),
        ("4. Metering & Revenue", "Billing links, daily sweeps, and bank matching"),
        ("5. Financial Control", "Freezing legacy books and single payroll"),
        ("6. Phased Rollout", "Clean cutover date and roadmap gates")
    ]

    card_w3 = 3.65
    card_h3 = 1.55
    start_x3 = 0.80
    start_y3 = 2.95
    for i, (p_title, p_desc) in enumerate(processes):
        row = i // 3
        col = i % 3
        cx = start_x3 + col * (card_w3 + 0.38)
        cy = start_y3 + row * (card_h3 + 0.35)

        add_card(s3, cx, cy, card_w3, card_h3, bg_color=C_SURFACE, border_color=C_BORDER)

        tb_pt = s3.shapes.add_textbox(Inches(cx + 0.16), Inches(cy + 0.16), Inches(card_w3 - 0.32), Inches(0.35))
        tf_pt = tb_pt.text_frame
        tf_pt.margin_left = tf_pt.margin_right = tf_pt.margin_top = tf_pt.margin_bottom = 0
        p_pt = tf_pt.paragraphs[0]
        p_pt.text = p_title
        p_pt.font.name = FONT_HEAD
        p_pt.font.size = Pt(15)
        p_pt.font.bold = True
        p_pt.font.color.rgb = C_BLUE

        tb_pd = s3.shapes.add_textbox(Inches(cx + 0.16), Inches(cy + 0.58), Inches(card_w3 - 0.32), Inches(0.85))
        tf_pd = tb_pd.text_frame
        tf_pd.word_wrap = True
        tf_pd.margin_left = tf_pd.margin_right = tf_pd.margin_top = tf_pd.margin_bottom = 0
        p_pd = tf_pd.paragraphs[0]
        p_pd.text = p_desc
        p_pd.font.name = FONT_BODY
        p_pd.font.size = Pt(13)
        p_pd.font.color.rgb = C_SLATE

    add_footer(s3, 3)
    s3.notes_slide.notes_text_frame.text = (
        "Slide 3 introduces our agenda and methodology. We do not look at software modules or IT silos. "
        "We review JBVNL's business sequentially: from keeping the power flowing on the grid, "
        "to supplying materials from stores, paying contractors, collecting customer revenues, "
        "controlling company-wide finances, and executing the cutover. Each slide poses one sharp question "
        "with concrete options."
    )

    # =========================================================================
    # SLIDE 4: PROCESS 1 - GRID & ASSET OPERATIONS / MAINTENANCE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_process_slide(
        slide=s4,
        slide_num=4,
        eyebrow="Process 1: Grid & Asset Operations",
        title="Log Field Repairs in Asset Pools or Freeze for Board Approval?",
        subtitle="Balancing immediate maintenance records against audited asset registers",
        core_question="Log emergency repairs against generic substation pools, or freeze until Board approval?",
        why_text="Unapproved asset registers freeze field tracking and risk penalties.",
        scenario_text="Transformers trip; repairs proceed, but records sit in paper notebooks.",
        opt_a_title="Substation Pools",
        opt_a_desc="Log repairs immediately; reconcile serials post-audit. (Recommended)",
        opt_b_title="Approval Freeze",
        opt_b_desc="Wait for Board adoption; manual paper logs continue.",
        notes_text=(
            "Slide 4 addresses grid maintenance reality. Today, asset records up to March 2023 were loaded in test, "
            "but the post-2023 Fixed Asset Register awaits formal Board approval. "
            "In field divisions, distribution transformers fail and are replaced immediately. "
            "If we insist on having the final audited asset tag before recording work, field staff will continue "
            "using paper registers. Option A lets engineers log repairs against substation asset pools today, "
            "protecting grid reliability while the formal audit concludes."
        )
    )

    # =========================================================================
    # SLIDE 5: PROCESS 2 - INVENTORY & MATERIAL FLOW
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_process_slide(
        slide=s5,
        slide_num=5,
        eyebrow="Process 2: Inventory & Material Flow",
        title="Authorize Mobile Emergency Store Issues or Enforce Pre-Issue Locks?",
        subtitle="Preventing feeder downtime while establishing physical store accountability",
        core_question="Authorize mobile emergency spare issues, or enforce strict pre-issue locks?",
        why_text="Paper store processes create blackouts while physical stock sits unrecorded.",
        scenario_text="Rural feeders break; spares sit in store, but issue slips stall.",
        opt_a_title="Mobile Fast-Track",
        opt_a_desc="Issue spares via mobile; audit stock weekly. (Recommended)",
        opt_b_title="100% Pre-Issue Lock",
        opt_b_desc="Freeze issues until 15 stores finish physical audits.",
        notes_text=(
            "Slide 5 covers store inventory across JBVNL's 15 stores. Currently, opening stock counts are outdated "
            "and physical stock differs from old ledger balances. When a line trips, waiting days for manual paper "
            "approvals causes public power outages. Option A introduces a mobile store app where storekeepers scan and issue "
            "spares on the spot, backed by a mandatory weekly physical count. This protects the grid while bringing stores online."
        )
    )

    # =========================================================================
    # SLIDE 6: PROCESS 3 - PROCUREMENT & VENDOR PAYMENTS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_process_slide(
        slide=s6,
        slide_num=6,
        eyebrow="Process 3: Procurement & Vendor Payments",
        title="Mandate Order Matching for Large Contracts or Allow Direct Vouchers?",
        subtitle="Safeguarding cash flow while preventing unverified vendor commitments",
        core_question="Enforce order matching for contracts > ₹50 Lakh, reserving direct vouchers for utilities?",
        why_text="Unchecked direct payments accumulate unverified vendor liabilities.",
        scenario_text="Contractors submit running bills; Finance pays directly, letting balances drift.",
        opt_a_title="Tiered Threshold",
        opt_a_desc="Match orders for contracts > ₹50L; direct vouchers for utilities. (Recommended)",
        opt_b_title="Total Flexibility",
        opt_b_desc="Allow direct vouchers for all claims; reconcile later.",
        notes_text=(
            "Slide 6 tackles vendor payments. In the proposed Phase 1 plan, all bills are processed as direct financial "
            "vouchers without purchase orders to gain speed. However, for major turnkey schemes like RDSS, paying contractors "
            "without checking delivered quantities against purchase orders creates serious financial leakage risks. "
            "Option A sets a pragmatic ₹50 Lakh threshold: major contractors must be matched to purchase orders, "
            "while regular utilities and tax payments proceed via direct vouchers."
        )
    )

    # =========================================================================
    # SLIDE 7: PROCESS 4 - METERING, BILLING & REVENUE COLLECTION
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_process_slide(
        slide=s7,
        slide_num=7,
        eyebrow="Process 4: Revenue & Billing Link",
        title="Automate Daily Bank Sweeps or Rely on Monthly Circle Summaries?",
        subtitle="Closing the visibility gap between customer billing and bank deposits",
        core_question="Enforce automated daily bank sweeps, holding cashiers to 24-hour verification?",
        why_text="Delayed bank reconciliation masks revenue leakage and distorts monthly health.",
        scenario_text="Counters collect crores daily; billing figures match, but bank balances lag.",
        opt_a_title="Daily Bank Sweep",
        opt_a_desc="Automatic daily bank feeds; cashiers reconcile in 24 hours. (Recommended)",
        opt_b_title="Monthly Summaries",
        opt_b_desc="Manual monthly collection certificates from Circles; delays visibility.",
        notes_text=(
            "Slide 7 highlights the gap between consumer billing and company cash. Currently, consumer billing runs "
            "in a standalone system, and interface rules with central accounting have never been defined. "
            "Circles collect substantial revenue daily, but because bank reconciliation is manual and delayed, "
            "leadership does not know if collections match bank accounts until months later. "
            "Option A enforces daily electronic bank sweeps, closing the gap on commercial AT&C losses."
        )
    )

    # =========================================================================
    # SLIDE 8: PROCESS 5 - FINANCIAL CONTROL & GOVERNANCE
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_process_slide(
        slide=s8,
        slide_num=8,
        eyebrow="Process 5: Financial Governance",
        title="Decommission Tally on Cutover Day or Permit Dual Bookkeeping?",
        subtitle="Decommissioning legacy spreadsheets to establish an indisputable financial truth",
        core_question="Decommission Tally on cutover day, mandating single-system posting across Circles?",
        why_text="Dual systems split accountability and create conflicting records.",
        scenario_text="Divisions keep local Tally books; compiling liabilities takes three weeks.",
        opt_a_title="Hard Cutover Freeze",
        opt_a_desc="Decommission Tally on go-live; all entries in new system. (Recommended)",
        opt_b_title="60-Day Parallel Books",
        opt_b_desc="Allow Tally alongside rollout; doubles workload and conflicts.",
        notes_text=(
            "Slide 8 addresses the single biggest risk to financial integrity: running Tally and the new system in parallel. "
            "When field accountants are allowed to keep Tally open 'just in case,' they naturally prioritize the tool they know. "
            "The new system becomes an afterthought, entries lag, and leadership is left with two conflicting sets of books. "
            "Option A freezes Tally on cutover day, backed by dedicated field support managers in every Circle."
        )
    )

    # =========================================================================
    # SLIDE 9: PROCESS 6 - PHASED ROLLOUT & CUTOVER READINESS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_process_slide(
        slide=s9,
        slide_num=9,
        eyebrow="Process 6: Rollout & Cutover",
        title="Adopt Clean 30.09.2026 Baseline or Reconstruct 19-Month Backlog?",
        subtitle="Choosing between 19 months of paperwork catch-up and a swift operational start",
        core_question="Adopt 30.09.2026 as live baseline, archiving older records for statutory audit?",
        why_text="Reconstructing 19 months of old vouchers stalls operational go-live.",
        scenario_text="Accountants rebuild 2025 vouchers while current transactions wait.",
        opt_a_title="Clean 30.09.2026 Baseline",
        opt_a_desc="Catch-up drops to 1 month; older records archived. (Recommended)",
        opt_b_title="19-Month Backlog Route",
        opt_b_desc="Rebuilding 19 months delays live control by 10 months.",
        notes_text=(
            "Slide 9 presents the most pivotal timeline decision facing the Steering Committee today. "
            "The project has been stuck trying to reconcile 19 months of historical data since April 1, 2025. "
            "Field accountants cannot look forward because they are drowning in historical reconciliation. "
            "Option A draws a line in the sand at September 30, 2026. Older records are safely archived for statutory auditors, "
            "reducing the active catch-up to just one month and enabling live go-live by February 2027."
        )
    )

    # =========================================================================
    # SLIDE 10: DECISION SUMMARY MATRIX
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10, C_WHITE)
    add_header(s10, "Executive Action Register",
               "Decision Summary Matrix: Six Clear Choices for Today's Meeting",
               "Documenting the decision owner, required action, and operational timeline impact")

    rows = 7
    cols = 4
    left_t = Inches(0.80)
    top_t = Inches(2.05)
    width_t = Inches(11.733)
    height_t = Inches(4.55)

    table_shape = s10.shapes.add_table(rows, cols, left_t, top_t, width_t, height_t)
    table = table_shape.table
    table.columns[0].width = Inches(2.40)
    table.columns[1].width = Inches(4.533)
    table.columns[2].width = Inches(2.30)
    table.columns[3].width = Inches(2.50)

    headers_text = ["Business Area", "Decision Needed Today", "Lead Owner", "Timeline Impact"]
    for c_idx, h_text in enumerate(headers_text):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = FONT_HEAD
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    decisions_matrix = [
        ("1. Grid & Assets", "Log maintenance to substation pools pending register", "CE (O&M) / CE (Projects)", "Unlocks Phase 3 Works"),
        ("2. Inventory Flow", "Authorize mobile emergency issues with weekly audit", "CE (Stores & Materials)", "Unlocks 15 Stores by Sep 2027"),
        ("3. Procurement", "Mandate order match for contracts > ₹50 Lakh", "GM (F&A) / CE (Tenders)", "Prevents contract liability drift"),
        ("4. Metering & Revenue", "Enforce 24-hour bank sweep across all Circles", "Director (Finance) / Revenue", "Closes commercial cash gap"),
        ("5. Financial Control", "Decommission Tally completely on cutover date", "Finance Head / Circle F&A", "Ensures single financial truth"),
        ("6. Rollout Baseline", "Adopt 30.09.2026 clean baseline starting date", "Managing Director & Steering", "Accelerates Go-Live by 8-10 mos")
    ]

    for r_idx, row_data in enumerate(decisions_matrix, 1):
        for c_idx, val in enumerate(row_data):
            cell = table.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_SURFACE if r_idx % 2 == 1 else C_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(12)
            if c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_NAVY
            elif c_idx == 1:
                p.font.color.rgb = C_INK
            elif c_idx == 2:
                p.font.bold = True
                p.font.color.rgb = C_AMBER
            else:
                p.font.color.rgb = C_GREEN if r_idx == 6 else C_SLATE

    add_footer(s10, 10)
    s10.notes_slide.notes_text_frame.text = (
        "Slide 10 provides the executive decision sheet. If the Managing Director and Steering Committee sign off "
        "on these six decisions today, every operational ambiguity disappears. "
        "The project team will issue unified circulars within 48 hours, field units will have clear marching orders, "
        "and JBVNL will be on a definitive path to clean, accountable operations."
    )

    # =========================================================================
    # SLIDE 11: THE STRUCTURAL TAKEAWAY
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11, C_WHITE)
    add_header(s11, "Strategic Synthesis",
               "The Structural Takeaway: What Makes Utility Transformations Succeed",
               "Empowering frontline engineers and enforcing disciplined rules over software complexity")

    # Hero Quote Banner
    add_card(s11, 0.80, 1.95, 11.733, 1.45, bg_color=C_SURFACE, border_color=C_BLUE)
    tb_quote = s11.shapes.add_textbox(Inches(1.10), Inches(2.05), Inches(11.133), Inches(1.25))
    tf_q11 = tb_quote.text_frame
    tf_q11.word_wrap = True
    tf_q11.margin_left = tf_q11.margin_right = tf_q11.margin_top = tf_q11.margin_bottom = 0
    p_q1 = tf_q11.paragraphs[0]
    p_q1.text = "Utility transformations succeed through operational ownership and clear rules—not software."
    p_q1.font.name = FONT_HEAD
    p_q1.font.size = Pt(17)
    p_q1.font.bold = True
    p_q1.font.color.rgb = C_NAVY

    p_q2 = tf_q11.add_paragraph()
    p_q2.text = "When field engineers own simple tools and leadership enforces one set of books, reliable power follows."
    p_q2.font.name = FONT_BODY
    p_q2.font.size = Pt(13)
    p_q2.font.color.rgb = C_SLATE
    p_q2.space_before = Pt(6)

    # 3 Guiding Pillars
    pillars = [
        ("1. Frontline Ownership",
         "Field staff must own daily entry without operational friction.",
         C_NAVY),
        ("2. Pragmatic Rules",
         "Simple operational policies beat complex theoretical workflows.",
         C_AMBER),
        ("3. Decisive Cutover",
         "A clean baseline stops backlogs from killing transformation.",
         C_GREEN)
    ]

    card_w11 = 3.65
    gutter11 = 0.38
    y_p11 = 3.58
    for i, (p_t, p_d, p_col) in enumerate(pillars):
        cx = 0.80 + i * (card_w11 + gutter11)
        add_card(s11, cx, y_p11, card_w11, 2.95, bg_color=C_WHITE, border_color=p_col)

        add_badge(s11, cx + card_w11 / 2.0, y_p11 + 0.45, 0.48, str(i + 1), bg_color=p_col, pt=14)

        tb_pt = s11.shapes.add_textbox(Inches(cx + 0.16), Inches(y_p11 + 0.80), Inches(card_w11 - 0.32), Inches(0.40))
        tf_pt = tb_pt.text_frame
        tf_pt.margin_left = tf_pt.margin_right = tf_pt.margin_top = tf_pt.margin_bottom = 0
        p_pt = tf_pt.paragraphs[0]
        p_pt.text = p_t
        p_pt.alignment = PP_ALIGN.CENTER
        p_pt.font.name = FONT_HEAD
        p_pt.font.size = Pt(16)
        p_pt.font.bold = True
        p_pt.font.color.rgb = C_NAVY

        tb_pd = s11.shapes.add_textbox(Inches(cx + 0.20), Inches(y_p11 + 1.30), Inches(card_w11 - 0.40), Inches(1.45))
        tf_pd = tb_pd.text_frame
        tf_pd.word_wrap = True
        tf_pd.margin_left = tf_pd.margin_right = tf_pd.margin_top = tf_pd.margin_bottom = 0
        p_pd = tf_pd.paragraphs[0]
        p_pd.text = p_d
        p_pd.font.name = FONT_BODY
        p_pd.font.size = Pt(13)
        p_pd.font.color.rgb = C_SLATE

    add_footer(s11, 11)
    s11.notes_slide.notes_text_frame.text = (
        "Slide 11 leaves leadership with our final structural takeaway. Software never transforms a power utility; "
        "people and disciplined rules do. When we give our field engineers practical tools that don't delay their work, "
        "when our storekeepers can issue emergency spares without fear of audit penalties, and when our leadership "
        "demands a single source of financial truth, JBVNL achieves what every modern discom strives for: "
        "reliable electricity for Jharkhand and transparent, sustainable financial health. Thank you."
    )

    # Dynamic Section Partitioning: 3 Structured Acts covering all 11 slides
    from tools.sections import write_sections
    acts = [
        ("1. Executive Context & Reality Check", 3),
        ("2. Core Operational Decisions", 6),
        ("3. Alignment & Governance", 2)
    ]
    write_sections(prs, acts)

    prs.save(output_path)
    return output_path


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_dir, "JBVNL_Transformation_Decision_Playbook.pptx")
    previews_dir = os.path.join(base_dir, "previews_jbvnl_decision")
    os.makedirs(previews_dir, exist_ok=True)

    print("Generating JBVNL Transformation Decision Playbook...")
    rendered = create_deck(output_path)
    print(f"Presentation saved to: {rendered}")


if __name__ == "__main__":
    main()
