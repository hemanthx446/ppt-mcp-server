import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def create_executive_deck(output_path="Lumbini_SAP_S4HANA_MES_Integration_Executive_Proposal.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # -------------------------------------------------------------
    # Design System Tokens
    # -------------------------------------------------------------
    NAVY_DARK = RGBColor(11, 19, 43)          # #0B132B Executive Deep Navy
    NAVY_CARD = RGBColor(21, 31, 60)         # #151F3C Navy Card
    NAVY_BORDER = RGBColor(40, 56, 95)       # Navy Outline
    
    SLATE_BG = RGBColor(248, 250, 252)       # #F8FAFC Crisp Slate Ice White
    CARD_BG = RGBColor(255, 255, 255)        # Pure White Card
    CARD_BORDER = RGBColor(226, 232, 240)    # Soft Slate Border
    CARD_BG_MUTED = RGBColor(241, 245, 249)  # Light Slate Pill
    
    SAP_BLUE = RGBColor(0, 102, 204)         # #0066CC Enterprise SAP Blue
    CYAN_ACCENT = RGBColor(0, 180, 216)      # #00B4D8 Tech Cyan Accent
    EMERALD_GREEN = RGBColor(16, 185, 129)   # #10B981 ROI / Success Green
    AMBER_ACCENT = RGBColor(217, 119, 6)     # #D97706 Operational Amber
    
    TEXT_DARK = RGBColor(15, 23, 42)         # #0F172A Primary Dark
    TEXT_MUTED = RGBColor(100, 116, 139)     # #64748B Secondary Slate
    TEXT_LIGHT = RGBColor(248, 250, 252)     # #F8FAFC Primary Light
    TEXT_LIGHT_MUTED = RGBColor(148, 163, 184) # Secondary Light

    # -------------------------------------------------------------
    # Slide Helper Functions
    # -------------------------------------------------------------
    def add_base_slide(is_dark=False):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = NAVY_DARK if is_dark else SLATE_BG
        bg.line.fill.background()
        return slide

    def add_header(slide, title_text, category_text, narrative_subtext, is_dark=False):
        # Category Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.42), Inches(3.8), Inches(0.28))
        badge.fill.solid()
        badge.fill.fore_color.rgb = NAVY_CARD if is_dark else RGBColor(238, 242, 255)
        badge.line.color.rgb = CYAN_ACCENT if is_dark else SAP_BLUE
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
        p_b.font.color.rgb = CYAN_ACCENT if is_dark else SAP_BLUE

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
        p_s.font.color.rgb = CYAN_ACCENT if is_dark else SAP_BLUE

        # Footer Branding
        ft_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(11.733), Inches(0.28))
        tf_f = ft_box.text_frame
        tf_f.margin_left = tf_f.margin_top = tf_f.margin_bottom = tf_f.margin_right = 0
        p_f = tf_f.paragraphs[0]
        p_f.text = "Lumbini Elite Solutions • Enterprise SAP & Smart Manufacturing Practice • Confidential"
        p_f.font.name = "Arial"
        p_f.font.size = Pt(8.5)
        p_f.font.color.rgb = TEXT_LIGHT_MUTED if is_dark else TEXT_MUTED

    # =============================================================
    # SLIDE 1: Executive Cover Slide
    # =============================================================
    slide1 = add_base_slide(is_dark=True)
    
    # Top Category Pill
    top_pill = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.9), Inches(4.5), Inches(0.32))
    top_pill.fill.solid()
    top_pill.fill.fore_color.rgb = NAVY_CARD
    top_pill.line.color.rgb = CYAN_ACCENT
    top_pill.line.width = Pt(1)
    tf1_p = top_pill.text_frame
    tf1_p.margin_left = Inches(0.15)
    tf1_p.margin_top = Inches(0.03)
    p1_p = tf1_p.paragraphs[0]
    p1_p.text = "LUMBINI ELITE SOLUTIONS • EXECUTIVE ARCHITECTURE PROPOSAL"
    p1_p.font.name = "Arial"
    p1_p.font.size = Pt(8.5)
    p1_p.font.bold = True
    p1_p.font.color.rgb = CYAN_ACCENT

    # Main Deck Title
    title_box = slide1.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.7), Inches(1.1))
    tf1_t = title_box.text_frame
    tf1_t.word_wrap = True
    tf1_t.margin_left = tf1_t.margin_top = tf1_t.margin_bottom = tf1_t.margin_right = 0
    p1_t = tf1_t.paragraphs[0]
    p1_t.text = "SAP S/4HANA & MES Real-Time\nShop Floor Integration"
    p1_t.font.name = "Arial"
    p1_t.font.size = Pt(32)
    p1_t.font.bold = True
    p1_t.font.color.rgb = TEXT_LIGHT

    # Narrative Subtitle
    narrative_box = slide1.shapes.add_textbox(Inches(0.8), Inches(2.65), Inches(11.7), Inches(0.55))
    tf1_n = narrative_box.text_frame
    tf1_n.word_wrap = True
    tf1_n.margin_left = tf1_n.margin_top = tf1_n.margin_bottom = tf1_n.margin_right = 0
    p1_n = tf1_n.paragraphs[0]
    p1_n.text = "BRIDGING THE CORE TO THE EDGE: Synchronizing plant-floor telemetry with enterprise ERP in sub-second cycles without compromising the clean core."
    p1_n.font.name = "Arial"
    p1_n.font.size = Pt(14)
    p1_n.font.bold = True
    p1_n.font.color.rgb = CYAN_ACCENT

    # 3 High-Impact Executive Pillar Cards (3-bullet maximum per card)
    pillar_data = [
        {
            "tag": "CLEAN CORE INTEGRITY",
            "title": "Zero ERP Modifications",
            "bullets": [
                "100% standard SAP OData & Event Mesh interfaces.",
                "Zero custom Z-tables or batch locks inside S/4HANA.",
                "Guaranteed future-proof SAP upgrade readiness."
            ],
            "accent": CYAN_ACCENT
        },
        {
            "tag": "REAL-TIME TELEMETRY",
            "title": "Sub-Second Edge Sync",
            "bullets": [
                "Live bi-directional MQTT & OPC-UA telemetry sync.",
                "Automated work-order and scrap confirmation.",
                "Immediate WIP variance visibility for plant controllers."
            ],
            "accent": SAP_BLUE
        },
        {
            "tag": "PROVEN TIMELINE",
            "title": "12-Week Rapid ROI",
            "bullets": [
                "Turnkey pre-built connectors for standard MES/SCADA.",
                "Store-and-forward edge buffer ensuring 99.99% uptime.",
                "14-month full capital payback via eliminated scrap."
            ],
            "accent": EMERALD_GREEN
        }
    ]

    card_w = Inches(3.75)
    card_gap = Inches(0.24)
    for i, col in enumerate(pillar_data):
        cx = Inches(0.8) + i * (card_w + card_gap)
        cbox = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, Inches(3.45), card_w, Inches(2.85))
        cbox.fill.solid()
        cbox.fill.fore_color.rgb = NAVY_CARD
        cbox.line.color.rgb = NAVY_BORDER
        cbox.line.width = Pt(1.2)
        
        # Pill Tag
        ptag = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.2), Inches(3.62), Inches(2.3), Inches(0.22))
        ptag.fill.solid()
        ptag.fill.fore_color.rgb = NAVY_DARK
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
        t_box = slide1.shapes.add_textbox(cx + Inches(0.2), Inches(3.92), card_w - Inches(0.4), Inches(0.35))
        tf_ct = t_box.text_frame
        tf_ct.margin_left = tf_ct.margin_top = tf_ct.margin_bottom = tf_ct.margin_right = 0
        pct = tf_ct.paragraphs[0]
        pct.text = col["title"]
        pct.font.name = "Arial"
        pct.font.size = Pt(15)
        pct.font.bold = True
        pct.font.color.rgb = TEXT_LIGHT

        # 3 Bullets Maximum
        b_box = slide1.shapes.add_textbox(cx + Inches(0.2), Inches(4.35), card_w - Inches(0.4), Inches(1.8))
        tf_cb = b_box.text_frame
        tf_cb.word_wrap = True
        tf_cb.margin_left = tf_cb.margin_top = tf_cb.margin_bottom = tf_cb.margin_right = 0
        
        for idx, bullet in enumerate(col["bullets"][:3]):
            p_bullet = tf_cb.paragraphs[0] if idx == 0 else tf_cb.add_paragraph()
            p_bullet.text = f"•  {bullet}"
            p_bullet.font.name = "Arial"
            p_bullet.font.size = Pt(11)
            p_bullet.font.color.rgb = TEXT_LIGHT_MUTED
            p_bullet.space_after = Pt(8)

    # Footer Metadata
    ft_box1 = slide1.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.733), Inches(0.3))
    tf_f1 = ft_box1.text_frame
    tf_f1.margin_left = tf_f1.margin_top = tf_f1.margin_bottom = tf_f1.margin_right = 0
    pf1 = tf_f1.paragraphs[0]
    pf1.text = "Lumbini Elite Solutions • Confidential Proposal • Target Delivery: 12 Weeks • Lead Architect: Enterprise SAP Practice"
    pf1.font.name = "Arial"
    pf1.font.size = Pt(9)
    pf1.font.color.rgb = TEXT_LIGHT_MUTED

    # =============================================================
    # SLIDE 2: Strategic Challenge & Operational Imperative
    # =============================================================
    slide2 = add_base_slide(is_dark=False)
    add_header(
        slide2,
        title_text="The Operational & Financial Disconnect",
        category_text="THE STRATEGIC CHALLENGE",
        narrative_subtext="THE BOTTLENECK: Batch-mode updates and siloed shop floors create critical blind spots between factory output and ERP financial books."
    )

    # 2-Column Split Cards (Enforcing 3-bullet max rule per card)
    left_x = Inches(0.8)
    right_x = Inches(6.8)
    card_width = Inches(5.7)
    card_y = Inches(1.75)
    card_h = Inches(4.8)

    # Left Card: Current State Bottlenecks
    l_box = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_x, card_y, card_width, card_h)
    l_box.fill.solid()
    l_box.fill.fore_color.rgb = RGBColor(254, 242, 242) # Soft Red/Amber Tint
    l_box.line.color.rgb = RGBColor(254, 202, 202)
    l_box.line.width = Pt(1.2)
    
    l_header = slide2.shapes.add_textbox(left_x + Inches(0.3), card_y + Inches(0.3), card_width - Inches(0.6), Inches(0.5))
    tf_lh = l_header.text_frame
    tf_lh.word_wrap = True
    tf_lh.margin_left = tf_lh.margin_top = tf_lh.margin_bottom = tf_lh.margin_right = 0
    plh = tf_lh.paragraphs[0]
    plh.text = "CURRENT STATE: SILOED BATCH FACTORY"
    plh.font.name = "Arial"
    plh.font.size = Pt(14)
    plh.font.bold = True
    plh.font.color.rgb = RGBColor(185, 28, 28) # Red Header

    l_body = slide2.shapes.add_textbox(left_x + Inches(0.3), card_y + Inches(0.85), card_width - Inches(0.6), Inches(3.6))
    tf_lb = l_body.text_frame
    tf_lb.word_wrap = True
    tf_lb.margin_left = tf_lb.margin_top = tf_lb.margin_bottom = tf_lb.margin_right = 0

    left_points = [
        ("Manual Shift Reconciliations (8-24h Lag)", "Floor supervisors key in paper production sheets at end-of-shift, leaving inventory ledgers blind during active runs."),
        ("Frequent Order Confirmation Mismatches", "Discrepancies between physical output and SAP confirmations trigger unplanned line halts and material shortages."),
        ("Ghost Scrap & Delayed Financial Costing", "Material scrap is recorded retrospectively, skewing standard costing models and preventing timely corrective action.")
    ]
    for idx, (head, desc) in enumerate(left_points[:3]):
        p_head = tf_lb.paragraphs[0] if idx == 0 else tf_lb.add_paragraph()
        p_head.text = f"•  {head}"
        p_head.font.name = "Arial"
        p_head.font.size = Pt(12)
        p_head.font.bold = True
        p_head.font.color.rgb = TEXT_DARK
        
        p_desc = tf_lb.add_paragraph()
        p_desc.text = f"    {desc}"
        p_desc.font.name = "Arial"
        p_desc.font.size = Pt(10.5)
        p_desc.font.color.rgb = TEXT_MUTED
        p_desc.space_after = Pt(14)

    # Right Card: Target Architecture
    r_box = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, card_y, card_width, card_h)
    r_box.fill.solid()
    r_box.fill.fore_color.rgb = RGBColor(240, 253, 244) # Soft Emerald Tint
    r_box.line.color.rgb = RGBColor(187, 247, 208)
    r_box.line.width = Pt(1.2)

    r_header = slide2.shapes.add_textbox(right_x + Inches(0.3), card_y + Inches(0.3), card_width - Inches(0.6), Inches(0.5))
    tf_rh = r_header.text_frame
    tf_rh.word_wrap = True
    tf_rh.margin_left = tf_rh.margin_top = tf_rh.margin_bottom = tf_rh.margin_right = 0
    prh = tf_rh.paragraphs[0]
    prh.text = "TARGET STATE: SYNCHRONIZED INTELLIGENT ENTERPRISE"
    prh.font.name = "Arial"
    prh.font.size = Pt(14)
    prh.font.bold = True
    prh.font.color.rgb = RGBColor(21, 128, 61) # Green Header

    r_body = slide2.shapes.add_textbox(right_x + Inches(0.3), card_y + Inches(0.85), card_width - Inches(0.6), Inches(3.6))
    tf_rb = r_body.text_frame
    tf_rb.word_wrap = True
    tf_rb.margin_left = tf_rb.margin_top = tf_rb.margin_bottom = tf_rb.margin_right = 0

    right_points = [
        ("Sub-Second Edge Telemetry & Event Streaming", "PLC and sensor signals stream directly through Lumbini BTP broker, updating production orders instantaneously."),
        ("Automated Routing & Work-Center Validation", "Operators confirm steps via rugged touch terminals, locking invalid job progression and enforcing zero defect gates."),
        ("Real-Time Variance Analytics & Cost Transparency", "Raw material consumption and yield post immediately to SAP Universal Journal (ACDOCA) for live margin control.")
    ]
    for idx, (head, desc) in enumerate(right_points[:3]):
        p_head = tf_rb.paragraphs[0] if idx == 0 else tf_rb.add_paragraph()
        p_head.text = f"•  {head}"
        p_head.font.name = "Arial"
        p_head.font.size = Pt(12)
        p_head.font.bold = True
        p_head.font.color.rgb = TEXT_DARK
        
        p_desc = tf_rb.add_paragraph()
        p_desc.text = f"    {desc}"
        p_desc.font.name = "Arial"
        p_desc.font.size = Pt(10.5)
        p_desc.font.color.rgb = TEXT_MUTED
        p_desc.space_after = Pt(14)

    # =============================================================
    # SLIDE 3: Technical Architecture & Edge Integration
    # =============================================================
    slide3 = add_base_slide(is_dark=False)
    add_header(
        slide3,
        title_text="Decoupled 3-Tier Enterprise Architecture",
        category_text="TECHNICAL ARCHITECTURE & INTEGRATION",
        narrative_subtext="HOW IT WORKS: Real-time telemetry out of the plant, event-brokered through BTP, zero risk to the ERP core."
    )

    # Visual 3-Box Horizontal Flow
    # [ SAP S/4HANA Core ] -> [ Lumbini BTP Middleware ] -> [ Shop Floor Edge Terminals ]
    box_w = Inches(3.45)
    box_h = Inches(3.4)
    box_y = Inches(1.7)
    
    tier_data = [
        {
            "tier": "ENTERPRISE CORE",
            "title": "SAP S/4HANA Cloud",
            "color": SAP_BLUE,
            "bullets": [
                "Standard OData APIs for Work Orders & BOMs.",
                "Universal Journal (ACDOCA) live cost updates.",
                "Zero custom code, keeping core 100% clean."
            ]
        },
        {
            "tier": "INTEGRATION BROKER",
            "title": "Lumbini BTP Middleware",
            "color": CYAN_ACCENT,
            "bullets": [
                "SAP Event Mesh with sub-second message queuing.",
                "Protocol translation: MQTT, OPC-UA to REST.",
                "Offline store-and-forward caching engine."
            ]
        },
        {
            "tier": "PHYSICAL FACTORY",
            "title": "Shop Floor Edge Terminals",
            "color": EMERALD_GREEN,
            "bullets": [
                "PLC & sensor IoT collectors at machine line.",
                "Rugged touch UI for instant operator confirmations.",
                "Automated barcode & RFID scrap tracking."
            ]
        }
    ]

    for i, tier in enumerate(tier_data):
        bx = Inches(0.8) + i * Inches(4.14)
        box = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, bx, box_y, box_w, box_h)
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = CARD_BORDER
        box.line.width = Pt(1.5)
        
        # Color Header Strip
        strip = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, bx, box_y, box_w, Inches(0.08))
        strip.fill.solid()
        strip.fill.fore_color.rgb = tier["color"]
        strip.line.fill.background()

        # Tier Tag
        ttag = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx + Inches(0.2), box_y + Inches(0.2), Inches(2.2), Inches(0.24))
        ttag.fill.solid()
        ttag.fill.fore_color.rgb = CARD_BG_MUTED
        ttag.line.fill.background()
        tf_tt = ttag.text_frame
        tf_tt.margin_left = Inches(0.08)
        tf_tt.margin_top = Inches(0.02)
        ptt = tf_tt.paragraphs[0]
        ptt.text = tier["tier"]
        ptt.font.name = "Arial"
        ptt.font.size = Pt(8)
        ptt.font.bold = True
        ptt.font.color.rgb = tier["color"]

        # Box Title
        tb_title = slide3.shapes.add_textbox(bx + Inches(0.2), box_y + Inches(0.55), box_w - Inches(0.4), Inches(0.4))
        tf_bt = tb_title.text_frame
        tf_bt.margin_left = tf_bt.margin_top = tf_bt.margin_bottom = tf_bt.margin_right = 0
        pbt = tf_bt.paragraphs[0]
        pbt.text = tier["title"]
        pbt.font.name = "Arial"
        pbt.font.size = Pt(14)
        pbt.font.bold = True
        pbt.font.color.rgb = TEXT_DARK

        # 3 Bullets Maximum
        tb_body = slide3.shapes.add_textbox(bx + Inches(0.2), box_y + Inches(1.05), box_w - Inches(0.4), Inches(2.1))
        tf_bb = tb_body.text_frame
        tf_bb.word_wrap = True
        tf_bb.margin_left = tf_bb.margin_top = tf_bb.margin_bottom = tf_bb.margin_right = 0
        
        for idx, bullet in enumerate(tier["bullets"][:3]):
            pb = tf_bb.paragraphs[0] if idx == 0 else tf_bb.add_paragraph()
            pb.text = f"•  {bullet}"
            pb.font.name = "Arial"
            pb.font.size = Pt(11)
            pb.font.color.rgb = TEXT_DARK
            pb.space_after = Pt(10)

        # Connector Arrow between Box 0->1 and 1->2
        if i < 2:
            arr_x = bx + box_w + Inches(0.12)
            arr = slide3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, arr_x, box_y + Inches(1.5), Inches(0.45), Inches(0.3))
            arr.fill.solid()
            arr.fill.fore_color.rgb = CYAN_ACCENT
            arr.line.fill.background()

    # Bottom Summary Callout Card for Security & Resilience
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
    pch.text = "SECURITY, RESILIENCE & ZERO-TRUST GOVERNANCE CALLOUT"
    pch.font.name = "Arial"
    pch.font.size = Pt(11)
    pch.font.bold = True
    pch.font.color.rgb = SAP_BLUE

    # 3 Bullets in Callout
    c_body = slide3.shapes.add_textbox(Inches(1.1), callout_y + Inches(0.48), Inches(11.1), Inches(0.8))
    tf_cb = c_body.text_frame
    tf_cb.word_wrap = True
    tf_cb.margin_left = tf_cb.margin_top = tf_cb.margin_bottom = tf_cb.margin_right = 0

    callout_bullets = [
        "Store-and-Forward Edge Resilience: Shop floor operates continuously even during wide-area network disconnects, queueing data locally and auto-syncing upon reconnection.",
        "Zero-Trust Edge Perimeter: Mutual TLS 1.3 encryption across all edge gateways with role-based JWT bearer authentication on SAP BTP endpoints.",
        "Certified Clean Core Alignment: Zero custom ABAP modifications ensure frictionless bi-annual SAP S/4HANA release upgrades."
    ]
    for idx, btext in enumerate(callout_bullets[:3]):
        pc = tf_cb.paragraphs[0] if idx == 0 else tf_cb.add_paragraph()
        pc.text = f"•  {btext}"
        pc.font.name = "Arial"
        pc.font.size = Pt(10)
        pc.font.color.rgb = TEXT_DARK
        pc.space_after = Pt(4)

    # =============================================================
    # SLIDE 4: Business Value & Quantified ROI
    # =============================================================
    slide4 = add_base_slide(is_dark=False)
    add_header(
        slide4,
        title_text="Quantified Financial & Operational Value",
        category_text="BUSINESS VALUE & ROI",
        narrative_subtext="MEASURABLE IMPACT: Transforming plant floor telemetry into 38% faster order turnaround and 14-month payback."
    )

    # 2-Column Side-by-Side Card Layout with Prominent Metric Callouts
    col4_w = Inches(5.7)
    col4_y = Inches(1.75)
    col4_h = Inches(4.8)

    # Left Column: Operational Excellence
    c_left = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), col4_y, col4_w, col4_h)
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = CARD_BG
    c_left.line.color.rgb = CARD_BORDER
    c_left.line.width = Pt(1.2)

    # Metric Banner Left
    m_left = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), col4_y, col4_w, Inches(1.05))
    m_left.fill.solid()
    m_left.fill.fore_color.rgb = RGBColor(238, 242, 255)
    m_left.line.fill.background()

    m_txt_l = slide4.shapes.add_textbox(Inches(1.1), col4_y + Inches(0.12), col4_w - Inches(0.6), Inches(0.8))
    tf_ml = m_txt_l.text_frame
    tf_ml.margin_left = tf_ml.margin_top = tf_ml.margin_bottom = tf_ml.margin_right = 0
    pml1 = tf_ml.paragraphs[0]
    pml1.text = "-65% WIP INVENTORY LATENCY"
    pml1.font.name = "Arial"
    pml1.font.size = Pt(20)
    pml1.font.bold = True
    pml1.font.color.rgb = SAP_BLUE
    
    pml2 = tf_ml.add_paragraph()
    pml2.text = "Operational Speed & Production Execution Gains"
    pml2.font.name = "Arial"
    pml2.font.size = Pt(10)
    pml2.font.color.rgb = TEXT_MUTED

    # Left 3 Bullets
    b_txt_l = slide4.shapes.add_textbox(Inches(1.1), col4_y + Inches(1.25), col4_w - Inches(0.6), Inches(3.2))
    tf_bl = b_txt_l.text_frame
    tf_bl.word_wrap = True
    tf_bl.margin_left = tf_bl.margin_top = tf_bl.margin_bottom = tf_bl.margin_right = 0

    left_val_bullets = [
        ("38% Faster Order-to-Cash Cycle", "Automated confirmation eliminates physical paper routing and manual approval delays across lines."),
        ("22% Reduction in Scrap & Defects", "In-line tolerance checks at operator terminals halt non-compliant assemblies before downstream processing."),
        ("100% Component Serialization Audit Trail", "Complete geneaology tracking ensures full compliance with ISO 9001 and IATF aerospace/automotive standards.")
    ]
    for idx, (title_b, desc_b) in enumerate(left_val_bullets[:3]):
        pb1 = tf_bl.paragraphs[0] if idx == 0 else tf_bl.add_paragraph()
        pb1.text = f"•  {title_b}"
        pb1.font.name = "Arial"
        pb1.font.size = Pt(12)
        pb1.font.bold = True
        pb1.font.color.rgb = TEXT_DARK
        
        pb2 = tf_bl.add_paragraph()
        pb2.text = f"    {desc_b}"
        pb2.font.name = "Arial"
        pb2.font.size = Pt(10.5)
        pb2.font.color.rgb = TEXT_MUTED
        pb2.space_after = Pt(12)

    # Right Column: Financial ROI
    c_right = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), col4_y, col4_w, col4_h)
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = CARD_BG
    c_right.line.color.rgb = CARD_BORDER
    c_right.line.width = Pt(1.2)

    # Metric Banner Right
    m_right = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), col4_y, col4_w, Inches(1.05))
    m_right.fill.solid()
    m_right.fill.fore_color.rgb = RGBColor(236, 253, 245)
    m_right.line.fill.background()

    m_txt_r = slide4.shapes.add_textbox(Inches(7.1), col4_y + Inches(0.12), col4_w - Inches(0.6), Inches(0.8))
    tf_mr = m_txt_r.text_frame
    tf_mr.margin_left = tf_mr.margin_top = tf_mr.margin_bottom = tf_mr.margin_right = 0
    pmr1 = tf_mr.paragraphs[0]
    pmr1.text = "14-MONTH CAPITAL PAYBACK"
    pmr1.font.name = "Arial"
    pmr1.font.size = Pt(20)
    pmr1.font.bold = True
    pmr1.font.color.rgb = EMERALD_GREEN

    pmr2 = tf_mr.add_paragraph()
    pmr2.text = "Direct Bottom-Line Cost Savings & Cash Flow Expansion"
    pmr2.font.name = "Arial"
    pmr2.font.size = Pt(10)
    pmr2.font.color.rgb = TEXT_MUTED

    # Right 3 Bullets
    b_txt_r = slide4.shapes.add_textbox(Inches(7.1), col4_y + Inches(1.25), col4_w - Inches(0.6), Inches(3.2))
    tf_br = b_txt_r.text_frame
    tf_br.word_wrap = True
    tf_br.margin_left = tf_br.margin_top = tf_br.margin_bottom = tf_br.margin_right = 0

    right_val_bullets = [
        ("$1.8M Recurring Annual Waste Reduction", "Prevented over-production and eliminated unrecorded material slippage across 3 target manufacturing plants."),
        ("85% Cut in Shift-End Administrative Overtime", "Supervisors save 90 minutes per shift previously spent manually auditing ERP batch discrepancies."),
        ("4.2x 3-Year Implementation IRR", "Turnkey architecture yields accelerated return on BTP licensing and deployment investment.")
    ]
    for idx, (title_b, desc_b) in enumerate(right_val_bullets[:3]):
        pb1 = tf_br.paragraphs[0] if idx == 0 else tf_br.add_paragraph()
        pb1.text = f"•  {title_b}"
        pb1.font.name = "Arial"
        pb1.font.size = Pt(12)
        pb1.font.bold = True
        pb1.font.color.rgb = TEXT_DARK
        
        pb2 = tf_br.add_paragraph()
        pb2.text = f"    {desc_b}"
        pb2.font.name = "Arial"
        pb2.font.size = Pt(10.5)
        pb2.font.color.rgb = TEXT_MUTED
        pb2.space_after = Pt(12)

    # =============================================================
    # SLIDE 5: 12-Week Implementation Roadmap & Next Steps
    # =============================================================
    slide5 = add_base_slide(is_dark=False)
    add_header(
        slide5,
        title_text="12-Week Rapid Production Roadmap",
        category_text="EXECUTION BLUEPRINT & MILESTONES",
        narrative_subtext="PHASED DEPLOYMENT: De-risked agile rollout from pilot work cell to plant-wide go-live in 90 days."
    )

    # 3-Phase Multi-Column Milestone Layout (Enforcing 3-bullet max rule per card)
    phase_cards = [
        {
            "tag": "PHASE 1 • WEEKS 1-3",
            "title": "Architecture & Edge Prototype",
            "accent": SAP_BLUE,
            "bullets": [
                "Establish S/4HANA OData and Event Mesh communication channels.",
                "Deploy edge collector in single pilot work cell for signal testing.",
                "Validate zero-trust network segregation and security policies."
            ]
        },
        {
            "tag": "PHASE 2 • WEEKS 4-8",
            "title": "Bi-Directional Pilot & Testing",
            "accent": CYAN_ACCENT,
            "bullets": [
                "Execute automated work-order dispatch to operator touchscreens.",
                "Simulate network drops to verify offline store-and-forward caching.",
                "Conduct live variance testing against SAP Universal Journal."
            ]
        },
        {
            "tag": "PHASE 3 • WEEKS 9-12",
            "title": "Plant Cutover & Scale-Out",
            "accent": EMERALD_GREEN,
            "bullets": [
                "Full plant-wide roll-out across all active work centers and lines.",
                "Complete supervisor SOP training and operator onboarding.",
                "Formal handover with 24/7 hypercare and scale-out playbook."
            ]
        }
    ]

    p_card_w = Inches(3.75)
    p_card_gap = Inches(0.24)
    p_card_y = Inches(1.75)
    p_card_h = Inches(3.4)

    for i, pcard in enumerate(phase_cards):
        pcx = Inches(0.8) + i * (p_card_w + p_card_gap)
        p_box = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, pcx, p_card_y, p_card_w, p_card_h)
        p_box.fill.solid()
        p_box.fill.fore_color.rgb = CARD_BG
        p_box.line.color.rgb = CARD_BORDER
        p_box.line.width = Pt(1.2)

        # Header Pill
        ppill = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, pcx + Inches(0.2), p_card_y + Inches(0.2), Inches(2.2), Inches(0.24))
        ppill.fill.solid()
        ppill.fill.fore_color.rgb = CARD_BG_MUTED
        ppill.line.fill.background()
        tf_pp = ppill.text_frame
        tf_pp.margin_left = Inches(0.08)
        tf_pp.margin_top = Inches(0.02)
        ppp = tf_pp.paragraphs[0]
        ppp.text = pcard["tag"]
        ppp.font.name = "Arial"
        ppp.font.size = Pt(8)
        ppp.font.bold = True
        ppp.font.color.rgb = pcard["accent"]

        # Phase Title
        pt_box = slide5.shapes.add_textbox(pcx + Inches(0.2), p_card_y + Inches(0.55), p_card_w - Inches(0.4), Inches(0.45))
        tf_pt = pt_box.text_frame
        tf_pt.margin_left = tf_pt.margin_top = tf_pt.margin_bottom = tf_pt.margin_right = 0
        ppt_txt = tf_pt.paragraphs[0]
        ppt_txt.text = pcard["title"]
        ppt_txt.font.name = "Arial"
        ppt_txt.font.size = Pt(14)
        ppt_txt.font.bold = True
        ppt_txt.font.color.rgb = TEXT_DARK

        # 3 Bullets Maximum
        pb_box = slide5.shapes.add_textbox(pcx + Inches(0.2), p_card_y + Inches(1.1), p_card_w - Inches(0.4), Inches(2.1))
        tf_pb = pb_box.text_frame
        tf_pb.word_wrap = True
        tf_pb.margin_left = tf_pb.margin_top = tf_pb.margin_bottom = tf_pb.margin_right = 0
        
        for idx, bullet in enumerate(pcard["bullets"][:3]):
            pb = tf_pb.paragraphs[0] if idx == 0 else tf_pb.add_paragraph()
            pb.text = f"•  {bullet}"
            pb.font.name = "Arial"
            pb.font.size = Pt(11)
            pb.font.color.rgb = TEXT_DARK
            pb.space_after = Pt(10)

    # Bottom Callout: Next Steps & Engagement Model
    b_callout_y = Inches(5.35)
    b_callout = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), b_callout_y, Inches(11.733), Inches(1.4))
    b_callout.fill.solid()
    b_callout.fill.fore_color.rgb = CARD_BG
    b_callout.line.color.rgb = SAP_BLUE
    b_callout.line.width = Pt(1.5)

    bc_hdr = slide5.shapes.add_textbox(Inches(1.1), b_callout_y + Inches(0.15), Inches(11.1), Inches(0.3))
    tf_bch = bc_hdr.text_frame
    tf_bch.margin_left = tf_bch.margin_top = tf_bch.margin_bottom = tf_bch.margin_right = 0
    pbch = tf_bch.paragraphs[0]
    pbch.text = "PROPOSED IMMEDIATE ACTION & NEXT STEPS"
    pbch.font.name = "Arial"
    pbch.font.size = Pt(11)
    pbch.font.bold = True
    pbch.font.color.rgb = SAP_BLUE

    bc_body = slide5.shapes.add_textbox(Inches(1.1), b_callout_y + Inches(0.48), Inches(11.1), Inches(0.8))
    tf_bcb = bc_body.text_frame
    tf_bcb.word_wrap = True
    tf_bcb.margin_left = tf_bcb.margin_top = tf_bcb.margin_bottom = tf_bcb.margin_right = 0

    next_steps = [
        "Architecture Discovery Workshop: Conduct a 1-day alignment session with SAP and plant engineering teams.",
        "Pilot Cell Selection: Identify target high-volume production line for initial Week 3 edge sensor hookup.",
        "Zero-Risk Pilot Approval: Authorize fixed-price Phase 1 proof-of-concept milestone with guaranteed SLA."
    ]
    for idx, step in enumerate(next_steps[:3]):
        ps = tf_bcb.paragraphs[0] if idx == 0 else tf_bcb.add_paragraph()
        ps.text = f"•  {step}"
        ps.font.name = "Arial"
        ps.font.size = Pt(10)
        ps.font.color.rgb = TEXT_DARK
        ps.space_after = Pt(4)

    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == "__main__":
    create_executive_deck()
