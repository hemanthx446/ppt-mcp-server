import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def build_4flow_deck(output_path="4Flow_SAP_IBP_Executive_Proposal.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # -------------------------------------------------------------
    # Executive Design Tokens & Harmonized Palette
    # -------------------------------------------------------------
    DARK_NAVY = RGBColor(10, 22, 44)         # #0A162C Deep Executive Navy
    NAVY_CARD = RGBColor(19, 34, 64)         # #132240 Elevated Navy Card
    NAVY_BORDER = RGBColor(38, 59, 99)       # Navy Card Outline
    
    SLATE_BG = RGBColor(248, 250, 252)       # #F8FAFC Clean Slate Canvas
    CARD_BG = RGBColor(255, 255, 255)        # Pure White Card
    CARD_BORDER = RGBColor(226, 232, 240)    # Soft Slate Card Outline
    CARD_BG_MUTED = RGBColor(241, 245, 249)  # Light Slate Pill
    
    FLOW_BLUE = RGBColor(0, 102, 204)        # #0066CC Enterprise 4Flow / SAP Blue
    CYAN_ACCENT = RGBColor(0, 180, 216)      # #00B4D8 Tech Cyan Accent
    EMERALD_GREEN = RGBColor(16, 185, 129)   # #10B981 ROI / Success Green
    AMBER_ACCENT = RGBColor(217, 119, 6)     # #D97706 Constraint / Alert Amber
    
    TEXT_DARK = RGBColor(15, 23, 42)         # #0F172A Primary Dark Text
    TEXT_MUTED = RGBColor(100, 116, 139)     # #64748B Secondary Slate Text
    TEXT_LIGHT = RGBColor(248, 250, 252)     # #F8FAFC Primary Light Text
    TEXT_LIGHT_MUTED = RGBColor(148, 163, 184) # Secondary Light Text

    # -------------------------------------------------------------
    # Base Slide & Header Helpers
    # -------------------------------------------------------------
    def add_base_slide(is_dark=False):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = DARK_NAVY if is_dark else SLATE_BG
        bg.line.fill.background()
        return slide

    def add_header(slide, title_text, category_text, narrative_subtext, is_dark=False):
        # Category Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.42), Inches(4.2), Inches(0.28))
        badge.fill.solid()
        badge.fill.fore_color.rgb = NAVY_CARD if is_dark else RGBColor(238, 242, 255)
        badge.line.color.rgb = CYAN_ACCENT if is_dark else FLOW_BLUE
        badge.line.width = Pt(1)
        tf_b = badge.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = Inches(0.12)
        tf_b.margin_top = Inches(0.02)
        p_b = tf_b.paragraphs[0]
        p_b.text = category_text.upper()
        p_b.font.name = "Arial"
        p_b.font.size = Pt(8.5)
        p_b.font.bold = True
        p_b.font.color.rgb = CYAN_ACCENT if is_dark else FLOW_BLUE

        # Slide Main Title
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.44))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_bottom = tf.margin_right = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(21)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT if is_dark else TEXT_DARK

        # Action-oriented Narrative Subheader
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.18), Inches(11.733), Inches(0.36))
        tf_s = sub_box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_top = tf_s.margin_bottom = tf_s.margin_right = 0
        p_s = tf_s.paragraphs[0]
        p_s.text = narrative_subtext
        p_s.font.name = "Arial"
        p_s.font.size = Pt(12)
        p_s.font.bold = True
        p_s.font.color.rgb = CYAN_ACCENT if is_dark else FLOW_BLUE

        # Footer Branding
        ft_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(11.733), Inches(0.28))
        tf_f = ft_box.text_frame
        tf_f.margin_left = tf_f.margin_top = tf_f.margin_bottom = tf_f.margin_right = 0
        p_f = tf_f.paragraphs[0]
        p_f.text = "4Flow Strategic Advisory • Enterprise Supply Chain & SAP IBP Practice • Confidential"
        p_f.font.name = "Arial"
        p_f.font.size = Pt(8.5)
        p_f.font.color.rgb = TEXT_LIGHT_MUTED if is_dark else TEXT_MUTED

    # =============================================================
    # SLIDE 1: Executive Cover Slide
    # =============================================================
    slide1 = add_base_slide(is_dark=True)

    # Top Tag Pill
    c_pill = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.9), Inches(4.8), Inches(0.32))
    c_pill.fill.solid()
    c_pill.fill.fore_color.rgb = NAVY_CARD
    c_pill.line.color.rgb = CYAN_ACCENT
    c_pill.line.width = Pt(1)
    tf1_p = c_pill.text_frame
    tf1_p.margin_left = Inches(0.15)
    tf1_p.margin_top = Inches(0.03)
    p1_p = tf1_p.paragraphs[0]
    p1_p.text = "4FLOW STRATEGIC ADVISORY • ENTERPRISE SUPPLY CHAIN PRACTICE"
    p1_p.font.name = "Arial"
    p1_p.font.size = Pt(8.5)
    p1_p.font.bold = True
    p1_p.font.color.rgb = CYAN_ACCENT

    # Main Title
    t_box1 = slide1.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.7), Inches(1.15))
    tf1_t = t_box1.text_frame
    tf1_t.word_wrap = True
    tf1_t.margin_left = tf1_t.margin_top = tf1_t.margin_bottom = tf1_t.margin_right = 0
    p1_t = tf1_t.paragraphs[0]
    p1_t.text = "SAP IBP Next-Generation\nSupply Chain Transformation"
    p1_t.font.name = "Arial"
    p1_t.font.size = Pt(32)
    p1_t.font.bold = True
    p1_t.font.color.rgb = TEXT_LIGHT

    # Narrative Subtitle
    n_box1 = slide1.shapes.add_textbox(Inches(0.8), Inches(2.65), Inches(11.7), Inches(0.55))
    tf1_n = n_box1.text_frame
    tf1_n.word_wrap = True
    tf1_n.margin_left = tf1_n.margin_top = tf1_n.margin_bottom = tf1_n.margin_right = 0
    p1_n = tf1_n.paragraphs[0]
    p1_n.text = "SYNCHRONIZING ENTERPRISE PLANNING WITH SHOP-FLOOR REALITY: Closed-loop demand sensing, bottleneck-aware supply optimization, and automated financial tie-outs."
    p1_n.font.name = "Arial"
    p1_n.font.size = Pt(14)
    p1_n.font.bold = True
    p1_n.font.color.rgb = CYAN_ACCENT

    # 3 Executive Pillar Cards (3-bullet max rule strictly enforced)
    pillar_cards = [
        {
            "tag": "FOUNDATION & FEDERATION",
            "title": "Zero-Replication Core Topology",
            "bullets": [
                "Bypasses fragile CIF batches via real-time HANA direct federation.",
                "Zero redundant data lakes or uncoordinated planning silos.",
                "Ring-fenced memory partitions shield transactional S/4HANA core."
            ],
            "accent": CYAN_ACCENT
        },
        {
            "tag": "SYSTEMS THINKING (GOLDRATT)",
            "title": "Constraint-Synchronized Supply",
            "bullets": [
                "Translates Theory of Constraints into dynamic drum-buffer-rope heuristics.",
                "Mathematically protects physical bottleneck work centers from starving.",
                "Eliminates phantom capacity schedules across plant networks."
            ],
            "accent": FLOW_BLUE
        },
        {
            "tag": "ENTERPRISE ONTOLOGY (ROSS/ZACHMAN)",
            "title": "Universal Financial Tie-Out",
            "bullets": [
                "Every operational planning scenario reconciles to SAP Universal Journal.",
                "Working capital decisions dynamically linked to corporate cash covenants.",
                "Deming closed-loop variance feedback continuously tunes forecast safety stocks."
            ],
            "accent": EMERALD_GREEN
        }
    ]

    card_w = Inches(3.75)
    card_gap = Inches(0.24)
    for i, col in enumerate(pillar_cards):
        cx = Inches(0.8) + i * (card_w + card_gap)
        cbox = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, Inches(3.45), card_w, Inches(2.85))
        cbox.fill.solid()
        cbox.fill.fore_color.rgb = NAVY_CARD
        cbox.line.color.rgb = NAVY_BORDER
        cbox.line.width = Pt(1.2)
        
        # Pill Tag
        ptag = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.2), Inches(3.62), Inches(3.2), Inches(0.22))
        ptag.fill.solid()
        ptag.fill.fore_color.rgb = DARK_NAVY
        ptag.line.fill.background()
        tf_pt = ptag.text_frame
        tf_pt.margin_left = Inches(0.08)
        tf_pt.margin_top = Inches(0.01)
        ppt = tf_pt.paragraphs[0]
        ppt.text = col["tag"]
        ppt.font.name = "Arial"
        ppt.font.size = Pt(7.5)
        ppt.font.bold = True
        ppt.font.color.rgb = col["accent"]

        # Card Title
        tb_t = slide1.shapes.add_textbox(cx + Inches(0.2), Inches(3.92), card_w - Inches(0.4), Inches(0.35))
        tf_ct = tb_t.text_frame
        tf_ct.margin_left = tf_ct.margin_top = tf_ct.margin_bottom = tf_ct.margin_right = 0
        pct = tf_ct.paragraphs[0]
        pct.text = col["title"]
        pct.font.name = "Arial"
        pct.font.size = Pt(14)
        pct.font.bold = True
        pct.font.color.rgb = TEXT_LIGHT

        # 3 Bullets Maximum
        tb_b = slide1.shapes.add_textbox(cx + Inches(0.2), Inches(4.35), card_w - Inches(0.4), Inches(1.8))
        tf_cb = tb_b.text_frame
        tf_cb.word_wrap = True
        tf_cb.margin_left = tf_cb.margin_top = tf_cb.margin_bottom = tf_cb.margin_right = 0
        
        for idx, bullet in enumerate(col["bullets"][:3]):
            pb = tf_cb.paragraphs[0] if idx == 0 else tf_cb.add_paragraph()
            pb.text = f"•  {bullet}"
            pb.font.name = "Arial"
            pb.font.size = Pt(11)
            pb.font.color.rgb = TEXT_LIGHT_MUTED
            pb.space_after = Pt(8)

    # Footer Metadata
    ft_box1 = slide1.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.733), Inches(0.3))
    tf_f1 = ft_box1.text_frame
    tf_f1.margin_left = tf_f1.margin_top = tf_f1.margin_bottom = tf_f1.margin_right = 0
    pf1 = tf_f1.paragraphs[0]
    pf1.text = "Prepared by 4Flow Supply Chain Architects for Executive Committee • Systems Thinking & Clean Core Blueprint"
    pf1.font.name = "Arial"
    pf1.font.size = Pt(9)
    pf1.font.color.rgb = TEXT_LIGHT_MUTED

    # =============================================================
    # SLIDE 2: Strategic Supply Chain Disconnect & Systems Dynamics
    # =============================================================
    slide2 = add_base_slide(is_dark=False)
    add_header(
        slide2,
        title_text="The Supply Chain Disconnect & Constraint Dynamics",
        category_text="SYSTEM DYNAMICS & CONSTRAINT REALITY (SENGE / GOLDRATT)",
        narrative_subtext="WHERE CONVENTIONAL PLANNING FAILS: Periodic batch ETL decouples S&OP from physical shop-floor bottlenecks, inflating working capital by 24%."
    )

    # 2-Column Multi-Card Split (Enforcing 3-bullet max rule per card)
    col_w = Inches(5.7)
    card_y = Inches(1.75)
    card_h = Inches(4.8)

    # Left Column: Conventional Legacy Traps
    c_left = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), card_y, col_w, card_h)
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = RGBColor(254, 242, 242)
    c_left.line.color.rgb = RGBColor(254, 202, 202)
    c_left.line.width = Pt(1.2)

    l_head = slide2.shapes.add_textbox(Inches(1.1), card_y + Inches(0.28), col_w - Inches(0.6), Inches(0.45))
    tf_lh = l_head.text_frame
    tf_lh.margin_left = tf_lh.margin_top = tf_lh.margin_bottom = tf_lh.margin_right = 0
    plh = tf_lh.paragraphs[0]
    plh.text = "LEGACY STATE: BATCH SILOS & CONSTRAINT VIOLATIONS"
    plh.font.name = "Arial"
    plh.font.size = Pt(13.5)
    plh.font.bold = True
    plh.font.color.rgb = RGBColor(185, 28, 28)

    l_body = slide2.shapes.add_textbox(Inches(1.1), card_y + Inches(0.85), col_w - Inches(0.6), Inches(3.7))
    tf_lb = l_body.text_frame
    tf_lb.word_wrap = True
    tf_lb.margin_left = tf_lb.margin_top = tf_lb.margin_bottom = tf_lb.margin_right = 0

    legacy_points = [
        ("Stale 48-Hour Batch CIF Interfaces", "Uncoordinated ETL pipelines create blind spots where sudden demand spikes or supplier stockouts are discovered days after occurrence."),
        ("Unconstrained S&OP Schedules (Phantom Capacity)", "Master schedules assume infinite plant capacity, overloading physical bottleneck machines and creating massive shop-floor WIP queues."),
        ("Decoupled P&L & Balance Sheet Drift", "Supply planners optimize unit costs in isolation, inadvertently ballooning raw material inventory while missing corporate cash targets.")
    ]
    for idx, (title, desc) in enumerate(legacy_points[:3]):
        pt = tf_lb.paragraphs[0] if idx == 0 else tf_lb.add_paragraph()
        pt.text = f"•  {title}"
        pt.font.name = "Arial"
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = TEXT_DARK
        
        pd = tf_lb.add_paragraph()
        pd.text = f"    {desc}"
        pd.font.name = "Arial"
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = TEXT_MUTED
        pd.space_after = Pt(14)

    # Right Column: 4Flow Systems Architecture
    c_right = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), card_y, col_w, card_h)
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = RGBColor(240, 253, 244)
    c_right.line.color.rgb = RGBColor(187, 247, 208)
    c_right.line.width = Pt(1.2)

    r_head = slide2.shapes.add_textbox(Inches(7.1), card_y + Inches(0.28), col_w - Inches(0.6), Inches(0.45))
    tf_rh = r_head.text_frame
    tf_rh.margin_left = tf_rh.margin_top = tf_rh.margin_bottom = tf_rh.margin_right = 0
    prh = tf_rh.paragraphs[0]
    prh.text = "TARGET ARCHITECTURE: 4FLOW CLOSED-LOOP IBP ENGINE"
    prh.font.name = "Arial"
    prh.font.size = Pt(13.5)
    prh.font.bold = True
    prh.font.color.rgb = RGBColor(21, 128, 61)

    r_body = slide2.shapes.add_textbox(Inches(7.1), card_y + Inches(0.85), col_w - Inches(0.6), Inches(3.7))
    tf_rb = r_body.text_frame
    tf_rb.word_wrap = True
    tf_rb.margin_left = tf_rb.margin_top = tf_rb.margin_bottom = tf_rb.margin_right = 0

    target_points = [
        ("Sub-Second Demand Sensing & Channel Ingestion", "Pattern recognition algorithms dynamically capture point-of-sale telemetry, smoothing bullwhip ripples before they amplify upstream."),
        ("Bottleneck-Governed Supply (Theory of Constraints)", "Heuristic solvers anchor entire plant throughput around physical constraint work centers, preventing WIP accumulation."),
        ("Real-Time ACDOCA Working Capital Feedback", "Every S&OP scenario dynamically quantifies inventory carry costs and gross margin impact against SAP Universal Journal ledgers.")
    ]
    for idx, (title, desc) in enumerate(target_points[:3]):
        pt = tf_rb.paragraphs[0] if idx == 0 else tf_rb.add_paragraph()
        pt.text = f"•  {title}"
        pt.font.name = "Arial"
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = TEXT_DARK
        
        pd = tf_rb.add_paragraph()
        pd.text = f"    {desc}"
        pd.font.name = "Arial"
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = TEXT_MUTED
        pd.space_after = Pt(14)

    # =============================================================
    # SLIDE 3: Foundation & Architectural Mechanics
    # =============================================================
    slide3 = add_base_slide(is_dark=False)
    add_header(
        slide3,
        title_text="Zero-Replication Core-to-Cloud Topology",
        category_text="FOUNDATION & INTEGRATION MECHANICS (CLEAN CORE)",
        narrative_subtext="HOW IT WORKS: The calculation happens in memory on SAP HANA Cloud, bypassing traditional batch ETL and fragile staging data lakes."
    )

    # 3-Box Horizontal Architectural Flow
    # [ SAP S/4HANA Enterprise Core ] -> [ SAP IBP In-Memory Engine ] -> [ Shop Floor MES (ISA-95 L3) ]
    box_w = Inches(3.45)
    box_h = Inches(3.4)
    box_y = Inches(1.7)

    topo_nodes = [
        {
            "tag": "TRANSACTIONAL CORE",
            "title": "SAP S/4HANA Core",
            "color": FLOW_BLUE,
            "bullets": [
                "Universal Journal (ACDOCA) single source of financial truth.",
                "Master data governance: BOMs, routings & factory calendars.",
                "Clean-core standard OData CDS views with zero custom Z-tables."
            ]
        },
        {
            "tag": "CALCULATION ENGINE",
            "title": "SAP IBP (HANA Cloud)",
            "color": CYAN_ACCENT,
            "bullets": [
                "In-memory columnar computation without data duplication.",
                "Ring-fenced memory partitions prevent noisy-neighbor contention.",
                "Zero-CIF real-time Smart Data Integration (SDI) pipelines."
            ]
        },
        {
            "tag": "PHYSICAL DISPATCH",
            "title": "Shop Floor & MES (ISA-95 L3)",
            "color": EMERALD_GREEN,
            "bullets": [
                "Synchronized dispatch lists direct to work center terminals.",
                "Live scrap and actual yield feedback auto-adjust safety stocks.",
                "Sub-second constraint validation prevents unverified job releases."
            ]
        }
    ]

    for i, node in enumerate(topo_nodes):
        bx = Inches(0.8) + i * Inches(4.14)
        box = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, bx, box_y, box_w, box_h)
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = CARD_BORDER
        box.line.width = Pt(1.5)

        # Header Accent Strip
        strip = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, bx, box_y, box_w, Inches(0.08))
        strip.fill.solid()
        strip.fill.fore_color.rgb = node["color"]
        strip.line.fill.background()

        # Tag
        ntag = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx + Inches(0.2), box_y + Inches(0.2), Inches(2.4), Inches(0.24))
        ntag.fill.solid()
        ntag.fill.fore_color.rgb = CARD_BG_MUTED
        ntag.line.fill.background()
        tf_nt = ntag.text_frame
        tf_nt.margin_left = Inches(0.08)
        tf_nt.margin_top = Inches(0.02)
        pnt = tf_nt.paragraphs[0]
        pnt.text = node["tag"]
        pnt.font.name = "Arial"
        pnt.font.size = Pt(8)
        pnt.font.bold = True
        pnt.font.color.rgb = node["color"]

        # Box Title
        tb_t = slide3.shapes.add_textbox(bx + Inches(0.2), box_y + Inches(0.55), box_w - Inches(0.4), Inches(0.4))
        tf_bt = tb_t.text_frame
        tf_bt.margin_left = tf_bt.margin_top = tf_bt.margin_bottom = tf_bt.margin_right = 0
        pbt = tf_bt.paragraphs[0]
        pbt.text = node["title"]
        pbt.font.name = "Arial"
        pbt.font.size = Pt(14)
        pbt.font.bold = True
        pbt.font.color.rgb = TEXT_DARK

        # 3 Bullets Maximum
        tb_b = slide3.shapes.add_textbox(bx + Inches(0.2), box_y + Inches(1.05), box_w - Inches(0.4), Inches(2.1))
        tf_bb = tb_b.text_frame
        tf_bb.word_wrap = True
        tf_bb.margin_left = tf_bb.margin_top = tf_bb.margin_bottom = tf_bb.margin_right = 0
        
        for idx, bullet in enumerate(node["bullets"][:3]):
            pb = tf_bb.paragraphs[0] if idx == 0 else tf_bb.add_paragraph()
            pb.text = f"•  {bullet}"
            pb.font.name = "Arial"
            pb.font.size = Pt(11)
            pb.font.color.rgb = TEXT_DARK
            pb.space_after = Pt(10)

        # Connector Arrows
        if i < 2:
            arr_x = bx + box_w + Inches(0.12)
            arr = slide3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, arr_x, box_y + Inches(1.5), Inches(0.45), Inches(0.3))
            arr.fill.solid()
            arr.fill.fore_color.rgb = CYAN_ACCENT
            arr.line.fill.background()

    # Bottom Callout Card: System Performance & Memory Ring-Fencing
    callout_y = Inches(5.35)
    callout = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), callout_y, Inches(11.733), Inches(1.4))
    callout.fill.solid()
    callout.fill.fore_color.rgb = CARD_BG
    callout.line.color.rgb = CYAN_ACCENT
    callout.line.width = Pt(1.5)

    c_hdr = slide3.shapes.add_textbox(Inches(1.1), callout_y + Inches(0.15), Inches(11.1), Inches(0.3))
    tf_ch = c_hdr.text_frame
    tf_ch.margin_left = tf_ch.margin_top = tf_ch.margin_bottom = tf_ch.margin_right = 0
    pch = tf_ch.paragraphs[0]
    pch.text = "SYSTEM PERFORMANCE LIMITS & MEMORY RING-FENCING GOVERNANCE"
    pch.font.name = "Arial"
    pch.font.size = Pt(11)
    pch.font.bold = True
    pch.font.color.rgb = FLOW_BLUE

    c_body = slide3.shapes.add_textbox(Inches(1.1), callout_y + Inches(0.48), Inches(11.1), Inches(0.8))
    tf_cb = c_body.text_frame
    tf_cb.word_wrap = True
    tf_cb.margin_left = tf_cb.margin_top = tf_cb.margin_bottom = tf_cb.margin_right = 0

    callout_bullets = [
        "Memory Ring-Fencing: Computationally heavy Monte Carlo simulations execute in dedicated cloud memory containers, guaranteeing zero slowdown on S/4HANA transaction processing.",
        "Delta-Only Change Data Capture: Real-time event triggers stream strictly changed records, cutting network overhead by 88% and eliminating batch database lock contention.",
        "Zero-Data-Duplication Principle: Calculation models reference S/4HANA virtual data tables in-place without generating shadow operational copies."
    ]
    for idx, btext in enumerate(callout_bullets[:3]):
        pc = tf_cb.paragraphs[0] if idx == 0 else tf_cb.add_paragraph()
        pc.text = f"•  {btext}"
        pc.font.name = "Arial"
        pc.font.size = Pt(10)
        pc.font.color.rgb = TEXT_DARK
        pc.space_after = Pt(4)

    # =============================================================
    # SLIDE 4: Operational Cockpits & ISA-95 Alignment
    # =============================================================
    slide4 = add_base_slide(is_dark=False)
    add_header(
        slide4,
        title_text="Operational Cockpits Across ISA-95 Hierarchy",
        category_text="DECISION ARCHITECTURE & OPERATIONAL COCKPITS (BRANDL / ISA-95)",
        narrative_subtext="DECISION ARCHITECTURE: Translating executive S&OP strategy into automated dispatch decisions across ISA-95 enterprise tiers."
    )

    # 3 Multi-Column Cockpit Cards
    cockpit_cards = [
        {
            "tier": "ISA-95 LEVEL 4 • EXECUTIVE S&OP",
            "title": "Margin & Revenue at Risk Cockpit",
            "color": FLOW_BLUE,
            "bullets": [
                "Live P&L simulations projecting gross margin impact across constrained demand scenarios.",
                "Automated working capital exposure monitors tied directly to treasury debt covenants.",
                "Unconstrained vs. constrained demand gap visibility with dynamic price elasticity modeling."
            ]
        },
        {
            "tier": "ISA-95 LEVEL 3 • PLANT BOTTLENECK",
            "title": "Constraint & Drum-Buffer Tower",
            "color": AMBER_ACCENT,
            "bullets": [
                "Real-time buffer saturation tracking preventing starvation at critical bottleneck cells.",
                "Automated multi-plant load balancing dynamically re-routing over-capacity production orders.",
                "Predictive On-Time In-Full (OTIF) radar identifying at-risk sales orders 14 days in advance."
            ]
        },
        {
            "tier": "ENTERPRISE FINANCE • LEDGER AUDIT",
            "title": "ACDOCA Financial Tie-Out Cockpit",
            "color": EMERALD_GREEN,
            "bullets": [
                "Sub-second variance reconciliation comparing IBP planned cost absorption with live S/4HANA actuals.",
                "Automated cross-border transfer pricing compliance adhering to OECD and corporate tax rules.",
                "Immutable scenario version lineage providing complete audit trails for internal & external auditors."
            ]
        }
    ]

    p_card_w = Inches(3.75)
    p_card_gap = Inches(0.24)
    p_card_y = Inches(1.75)
    p_card_h = Inches(4.8)

    for i, ccard in enumerate(cockpit_cards):
        pcx = Inches(0.8) + i * (p_card_w + p_card_gap)
        p_box = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, pcx, p_card_y, p_card_w, p_card_h)
        p_box.fill.solid()
        p_box.fill.fore_color.rgb = CARD_BG
        p_box.line.color.rgb = CARD_BORDER
        p_box.line.width = Pt(1.2)

        # Header Pill
        ppill = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, pcx + Inches(0.2), p_card_y + Inches(0.25), Inches(3.2), Inches(0.24))
        ppill.fill.solid()
        ppill.fill.fore_color.rgb = CARD_BG_MUTED
        ppill.line.fill.background()
        tf_pp = ppill.text_frame
        tf_pp.margin_left = Inches(0.08)
        tf_pp.margin_top = Inches(0.02)
        ppp = tf_pp.paragraphs[0]
        ppp.text = ccard["tier"]
        ppp.font.name = "Arial"
        ppp.font.size = Pt(7.5)
        ppp.font.bold = True
        ppp.font.color.rgb = ccard["color"]

        # Card Title
        pt_box = slide4.shapes.add_textbox(pcx + Inches(0.2), p_card_y + Inches(0.65), p_card_w - Inches(0.4), Inches(0.55))
        tf_pt = pt_box.text_frame
        tf_pt.word_wrap = True
        tf_pt.margin_left = tf_pt.margin_top = tf_pt.margin_bottom = tf_pt.margin_right = 0
        ppt_txt = tf_pt.paragraphs[0]
        ppt_txt.text = ccard["title"]
        ppt_txt.font.name = "Arial"
        ppt_txt.font.size = Pt(14)
        ppt_txt.font.bold = True
        ppt_txt.font.color.rgb = TEXT_DARK

        # 3 Bullets Maximum
        pb_box = slide4.shapes.add_textbox(pcx + Inches(0.2), p_card_y + Inches(1.3), p_card_w - Inches(0.4), Inches(3.2))
        tf_pb = pb_box.text_frame
        tf_pb.word_wrap = True
        tf_pb.margin_left = tf_pb.margin_top = tf_pb.margin_bottom = tf_pb.margin_right = 0
        
        for idx, bullet in enumerate(ccard["bullets"][:3]):
            pb = tf_pb.paragraphs[0] if idx == 0 else tf_pb.add_paragraph()
            pb.text = f"•  {bullet}"
            pb.font.name = "Arial"
            pb.font.size = Pt(11)
            pb.font.color.rgb = TEXT_DARK
            pb.space_after = Pt(14)

    # =============================================================
    # SLIDE 5: Value Realization & Quantified Business Impact
    # =============================================================
    slide5 = add_base_slide(is_dark=False)
    add_header(
        slide5,
        title_text="Quantified Working Capital & Operational ROI",
        category_text="VALUE REALIZATION & MEASURABLE IMPACT (4FLOW BENCHMARK)",
        narrative_subtext="MEASURABLE IMPACT: 4Flow's blueprint delivers 28% working capital reduction and an 11-month capital payback."
    )

    # 2-Column Split Cards with Bold Metric Headers
    c5_w = Inches(5.7)
    c5_y = Inches(1.75)
    c5_h = Inches(4.8)

    # Left Column: Operational Agility & Fulfillment
    left_c5 = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), c5_y, c5_w, c5_h)
    left_c5.fill.solid()
    left_c5.fill.fore_color.rgb = CARD_BG
    left_c5.line.color.rgb = CARD_BORDER
    left_c5.line.width = Pt(1.2)

    # Metric Banner Left
    m_left = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), c5_y, c5_w, Inches(1.1))
    m_left.fill.solid()
    m_left.fill.fore_color.rgb = RGBColor(238, 242, 255)
    m_left.line.fill.background()

    m_txt_l = slide5.shapes.add_textbox(Inches(1.1), c5_y + Inches(0.12), c5_w - Inches(0.6), Inches(0.85))
    tf_ml = m_txt_l.text_frame
    tf_ml.margin_left = tf_ml.margin_top = tf_ml.margin_bottom = tf_ml.margin_right = 0
    pml1 = tf_ml.paragraphs[0]
    pml1.text = "+14 PTS ON-TIME IN-FULL (OTIF)"
    pml1.font.name = "Arial"
    pml1.font.size = Pt(20)
    pml1.font.bold = True
    pml1.font.color.rgb = FLOW_BLUE
    
    pml2 = tf_ml.add_paragraph()
    pml2.text = "Operational Responsiveness & Customer Service Excellence"
    pml2.font.name = "Arial"
    pml2.font.size = Pt(10)
    pml2.font.color.rgb = TEXT_MUTED

    # 3 Proof Bullets Left
    b_txt_l = slide5.shapes.add_textbox(Inches(1.1), c5_y + Inches(1.3), c5_w - Inches(0.6), Inches(3.2))
    tf_bl = b_txt_l.text_frame
    tf_bl.word_wrap = True
    tf_bl.margin_left = tf_bl.margin_top = tf_bl.margin_bottom = tf_bl.margin_right = 0

    left_roi = [
        ("98.5% Sustained Order Fulfillment", "Algorithmic safety stock sizing absorbs supply volatility without requiring excess buffer stock."),
        ("35% Reduction in Factory Stockouts", "Multi-echelon inventory optimization (MEIO) synchronizes raw material intake with finished goods demand."),
        ("45% Faster S&OP Planning Iteration Cycles", "Replaces multi-day spreadsheet assembly with continuous real-time scenario modeling.")
    ]
    for idx, (title, desc) in enumerate(left_roi[:3]):
        pb1 = tf_bl.paragraphs[0] if idx == 0 else tf_bl.add_paragraph()
        pb1.text = f"•  {title}"
        pb1.font.name = "Arial"
        pb1.font.size = Pt(12)
        pb1.font.bold = True
        pb1.font.color.rgb = TEXT_DARK
        
        pb2 = tf_bl.add_paragraph()
        pb2.text = f"    {desc}"
        pb2.font.name = "Arial"
        pb2.font.size = Pt(10.5)
        pb2.font.color.rgb = TEXT_MUTED
        pb2.space_after = Pt(12)

    # Right Column: Financial ROI
    right_c5 = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), c5_y, c5_w, c5_h)
    right_c5.fill.solid()
    right_c5.fill.fore_color.rgb = CARD_BG
    right_c5.line.color.rgb = CARD_BORDER
    right_c5.line.width = Pt(1.2)

    # Metric Banner Right
    m_right = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), c5_y, c5_w, Inches(1.1))
    m_right.fill.solid()
    m_right.fill.fore_color.rgb = RGBColor(236, 253, 244)
    m_right.line.fill.background()

    m_txt_r = slide5.shapes.add_textbox(Inches(7.1), c5_y + Inches(0.12), c5_w - Inches(0.6), Inches(0.85))
    tf_mr = m_txt_r.text_frame
    tf_mr.margin_left = tf_mr.margin_top = tf_mr.margin_bottom = tf_mr.margin_right = 0
    pmr1 = tf_mr.paragraphs[0]
    pmr1.text = "$14.2M WORKING CAPITAL RELEASE"
    pmr1.font.name = "Arial"
    pmr1.font.size = Pt(20)
    pmr1.font.bold = True
    pmr1.font.color.rgb = EMERALD_GREEN
    
    pmr2 = tf_mr.add_paragraph()
    pmr2.text = "11-Month Capital Payback & Direct P&L Free Cash Flow Acceleration"
    pmr2.font.name = "Arial"
    pmr2.font.size = Pt(10)
    pmr2.font.color.rgb = TEXT_MUTED

    # 3 Proof Bullets Right
    b_txt_r = slide5.shapes.add_textbox(Inches(7.1), c5_y + Inches(1.3), c5_w - Inches(0.6), Inches(3.2))
    tf_br = b_txt_r.text_frame
    tf_br.word_wrap = True
    tf_br.margin_left = tf_br.margin_top = tf_br.margin_bottom = tf_br.margin_right = 0

    right_roi = [
        ("28% Reduction in Holding Inventory Costs", "Eliminates dead stock and optimizes WIP buffers across warehouse distribution networks."),
        ("$3.6M Annual Freight Surcharge Avoidance", "Predictive load-building prevents emergency expedited air shipping and premium expediting."),
        ("4.8x Program ROI Across 3 Years", "De-risked architecture provides self-funding cash flow starting in Month 6 of deployment.")
    ]
    for idx, (title, desc) in enumerate(right_roi[:3]):
        pb1 = tf_br.paragraphs[0] if idx == 0 else tf_br.add_paragraph()
        pb1.text = f"•  {title}"
        pb1.font.name = "Arial"
        pb1.font.size = Pt(12)
        pb1.font.bold = True
        pb1.font.color.rgb = TEXT_DARK
        
        pb2 = tf_br.add_paragraph()
        pb2.text = f"    {desc}"
        pb2.font.name = "Arial"
        pb2.font.size = Pt(10.5)
        pb2.font.color.rgb = TEXT_MUTED
        pb2.space_after = Pt(12)

    # =============================================================
    # SLIDE 6: Value Realization & Phased Delivery Blueprint
    # =============================================================
    slide6 = add_base_slide(is_dark=False)
    add_header(
        slide6,
        title_text="Phased Delivery Blueprint & Milestone Gates",
        category_text="DELIVERY BLUEPRINT & GOVERNANCE GATES",
        narrative_subtext="PHASED GOVERNANCE: De-risked milestone gates ensuring architectural integrity and early business value realization."
    )

    # 3 Milestone Phase Cards
    milestone_cards = [
        {
            "tag": "GATE 1 • WEEKS 1-6",
            "title": "Clean-Core Data & Demand Sensing",
            "accent": FLOW_BLUE,
            "bullets": [
                "Establish zero-duplication S/4HANA CDS views & real-time SDI integration pipelines.",
                "Deploy statistical forecasting algorithms and demand sensing pattern models.",
                "Gate Criteria: Baseline forecast error reduced by at least 12% across pilot product families."
            ]
        },
        {
            "tag": "GATE 2 • WEEKS 7-14",
            "title": "Constrained Supply & S&OP Cockpits",
            "accent": CYAN_ACCENT,
            "bullets": [
                "Configure Goldratt bottleneck constraint optimizer and drum-buffer-rope heuristics.",
                "Deploy Executive S&OP and Plant Bottleneck real-time decision cockpits.",
                "Gate Criteria: Multi-site capacity simulations reconcile with physical shop-floor production limits."
            ]
        },
        {
            "tag": "GATE 3 • WEEKS 15-20",
            "title": "MEIO Scaling & ACDOCA Tie-Out",
            "accent": EMERALD_GREEN,
            "bullets": [
                "Activate multi-echelon inventory optimization across finished goods and supplier tiers.",
                "Automate live financial variance tie-outs against SAP Universal Journal ledgers.",
                "Gate Criteria: Production go-live with 4Flow hypercare and formal executive value audit sign-off."
            ]
        }
    ]

    m_card_w = Inches(3.75)
    m_card_gap = Inches(0.24)
    m_card_y = Inches(1.75)
    m_card_h = Inches(3.4)

    for i, mcard in enumerate(milestone_cards):
        mcx = Inches(0.8) + i * (m_card_w + m_card_gap)
        m_box = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, mcx, m_card_y, m_card_w, m_card_h)
        m_box.fill.solid()
        m_box.fill.fore_color.rgb = CARD_BG
        m_box.line.color.rgb = CARD_BORDER
        m_box.line.width = Pt(1.2)

        # Tag
        mpill = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, mcx + Inches(0.2), m_card_y + Inches(0.2), Inches(2.2), Inches(0.24))
        mpill.fill.solid()
        mpill.fill.fore_color.rgb = CARD_BG_MUTED
        mpill.line.fill.background()
        tf_mp = mpill.text_frame
        tf_mp.margin_left = Inches(0.08)
        tf_mp.margin_top = Inches(0.02)
        pmp = tf_mp.paragraphs[0]
        pmp.text = mcard["tag"]
        pmp.font.name = "Arial"
        pmp.font.size = Pt(8)
        pmp.font.bold = True
        pmp.font.color.rgb = mcard["accent"]

        # Title
        mt_box = slide6.shapes.add_textbox(mcx + Inches(0.2), m_card_y + Inches(0.55), m_card_w - Inches(0.4), Inches(0.45))
        tf_mt = mt_box.text_frame
        tf_mt.margin_left = tf_mt.margin_top = tf_mt.margin_bottom = tf_mt.margin_right = 0
        pmt = tf_mt.paragraphs[0]
        pmt.text = mcard["title"]
        pmt.font.name = "Arial"
        pmt.font.size = Pt(14)
        pmt.font.bold = True
        pmt.font.color.rgb = TEXT_DARK

        # 3 Bullets Maximum
        mb_box = slide6.shapes.add_textbox(mcx + Inches(0.2), m_card_y + Inches(1.1), m_card_w - Inches(0.4), Inches(2.1))
        tf_mb = mb_box.text_frame
        tf_mb.word_wrap = True
        tf_mb.margin_left = tf_mb.margin_top = tf_mb.margin_bottom = tf_mb.margin_right = 0
        
        for idx, bullet in enumerate(mcard["bullets"][:3]):
            pb = tf_mb.paragraphs[0] if idx == 0 else tf_mb.add_paragraph()
            pb.text = f"•  {bullet}"
            pb.font.name = "Arial"
            pb.font.size = Pt(11)
            pb.font.color.rgb = TEXT_DARK
            pb.space_after = Pt(10)

    # Bottom Governance Callout: Deming PDCA Closed Loop
    b_callout_y = Inches(5.35)
    b_callout = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), b_callout_y, Inches(11.733), Inches(1.4))
    b_callout.fill.solid()
    b_callout.fill.fore_color.rgb = CARD_BG
    b_callout.line.color.rgb = FLOW_BLUE
    b_callout.line.width = Pt(1.5)

    bc_hdr = slide6.shapes.add_textbox(Inches(1.1), b_callout_y + Inches(0.15), Inches(11.1), Inches(0.3))
    tf_bch = bc_hdr.text_frame
    tf_bch.margin_left = tf_bch.margin_top = tf_bch.margin_bottom = tf_bch.margin_right = 0
    pbch = tf_bch.paragraphs[0]
    pbch.text = "4FLOW GOVERNANCE & DEMING CLOSED-LOOP QUALITY ASSURANCE"
    pbch.font.name = "Arial"
    pbch.font.size = Pt(11)
    pbch.font.bold = True
    pbch.font.color.rgb = FLOW_BLUE

    bc_body = slide6.shapes.add_textbox(Inches(1.1), b_callout_y + Inches(0.48), Inches(11.1), Inches(0.8))
    tf_bcb = bc_body.text_frame
    tf_bcb.word_wrap = True
    tf_bcb.margin_left = tf_bcb.margin_top = tf_bcb.margin_bottom = tf_bcb.margin_right = 0

    gov_steps = [
        "Deming Plan-Do-Check-Act (PDCA) Assurance: Weekly tuning cycles continuously adjust algorithmic safety stocks based on live plant variance data.",
        "Joint Architecture Review Board (ARB): Strict clean-core gating ensures zero custom code touches the SAP S/4HANA transactional ledger.",
        "4Flow Supply Chain Co-Piloting: Dedicated senior supply chain architects guarantee knowledge transfer and change enablement across plant teams."
    ]
    for idx, step in enumerate(gov_steps[:3]):
        ps = tf_bcb.paragraphs[0] if idx == 0 else tf_bcb.add_paragraph()
        ps.text = f"•  {step}"
        ps.font.name = "Arial"
        ps.font.size = Pt(10)
        ps.font.color.rgb = TEXT_DARK
        ps.space_after = Pt(4)

    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == "__main__":
    build_4flow_deck()
