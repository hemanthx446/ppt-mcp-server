import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def build_refined_trace_deck(output_path="Hical_TRACE_n_TRACE_Executive_Proposal.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # -------------------------------------------------------------
    # Palette & Design Tokens (Executive Palette)
    # -------------------------------------------------------------
    DARK_BG = RGBColor(11, 19, 43)           # #0B132B Deep Executive Navy
    DARK_CARD = RGBColor(21, 31, 60)         # #151F3C Navy Card
    DARK_CARD_ALT = RGBColor(16, 26, 52)     # Alternating Card
    DARK_BORDER = RGBColor(40, 56, 95)       # Navy Outline
    
    LIGHT_BG = RGBColor(248, 250, 252)       # #F8FAFC Slate Ice White
    CARD_BG = RGBColor(255, 255, 255)        # Pure White
    CARD_BORDER = RGBColor(226, 232, 240)    # Soft slate border
    CARD_BG_MUTED = RGBColor(241, 245, 249)  # Light Slate Pill
    
    SAP_BLUE = RGBColor(0, 102, 204)         # #0066CC Enterprise SAP Blue
    CYAN_ACCENT = RGBColor(0, 180, 216)      # #00B4D8 Tech Cyan
    GOLD_ACCENT = RGBColor(217, 119, 6)      # #D97706 Lumbini Amber/Gold
    GOLD_LIGHT_BG = RGBColor(254, 243, 199)  # Gold Tint
    
    EMERALD_GREEN = RGBColor(16, 185, 129)   # #10B981 Success / Quality
    GREEN_LIGHT_BG = RGBColor(236, 253, 245) # Soft Green Tint
    AMBER_WARN = RGBColor(245, 158, 11)      # #F59E0B Warning
    AMBER_LIGHT_BG = RGBColor(255, 251, 235) # Soft Amber Tint
    CRIMSON_RED = RGBColor(239, 68, 68)      # #EF4444 Critical Alert
    RED_LIGHT_BG = RGBColor(254, 242, 242)   # Soft Red Tint
    
    PURPLE_ACCENT = RGBColor(124, 58, 237)   # Traceability Purple
    PURPLE_LIGHT_BG = RGBColor(245, 243, 255)
    
    TEXT_DARK = RGBColor(15, 23, 42)         # #0F172A Primary Dark
    TEXT_MUTED = RGBColor(100, 116, 139)     # #64748B Secondary Slate
    TEXT_LIGHT = RGBColor(248, 250, 252)     # #F8FAFC Off-White
    TEXT_LIGHT_MUTED = RGBColor(148, 163, 184)
    
    TOTAL_SLIDES = 12

    # -------------------------------------------------------------
    # Slide Building Helpers
    # -------------------------------------------------------------
    def add_base_slide(is_dark=False):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = DARK_BG if is_dark else LIGHT_BG
        bg.line.fill.background()
        return slide

    def add_header(slide, title_text, category_text, subtitle_text=None, is_dark=False):
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.36), Inches(4.8), Inches(0.26))
        badge.fill.solid()
        badge.fill.fore_color.rgb = DARK_CARD if is_dark else RGBColor(238, 242, 255)
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
        
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.64), Inches(11.733), Inches(0.42))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(19)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT if is_dark else TEXT_DARK
        
        if subtitle_text:
            tx_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.06), Inches(11.733), Inches(0.28))
            tf_sub = tx_sub.text_frame
            tf_sub.word_wrap = True
            tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
            ps = tf_sub.paragraphs[0]
            ps.text = subtitle_text
            ps.font.name = "Arial"
            ps.font.size = Pt(10.5)
            ps.font.italic = True
            ps.font.color.rgb = TEXT_LIGHT_MUTED if is_dark else TEXT_MUTED

    def add_footer(slide, slide_num, is_dark=False):
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.01))
        line.fill.solid()
        line.fill.fore_color.rgb = DARK_BORDER if is_dark else CARD_BORDER
        line.line.fill.background()
        
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(8.5), Inches(0.3))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = "Lumbini Elite Solutions  |  Hical Technologies — TRACE n TRACE  |  Confidential"
        p.font.name = "Arial"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_LIGHT_MUTED if is_dark else TEXT_MUTED
        
        tx_num = slide.shapes.add_textbox(Inches(11.533), Inches(7.05), Inches(1.0), Inches(0.3))
        tf_num = tx_num.text_frame
        tf_num.word_wrap = True
        tf_num.margin_right = tf_num.margin_top = 0
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"{slide_num:02d} / {TOTAL_SLIDES:02d}"
        p_num.font.name = "Arial"
        p_num.font.size = Pt(8.5)
        p_num.font.bold = True
        p_num.font.color.rgb = CYAN_ACCENT if is_dark else SAP_BLUE

    # =============================================================
    # SLIDE 1: Title & Strategic Context (Tell: Strategic Opening)
    # =============================================================
    s1 = add_base_slide(is_dark=True)
    
    top_glow = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    top_glow.fill.solid()
    top_glow.fill.fore_color.rgb = CYAN_ACCENT
    top_glow.line.fill.background()
    
    b1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.0), Inches(5.6), Inches(0.34))
    b1.fill.solid()
    b1.fill.fore_color.rgb = DARK_CARD
    b1.line.color.rgb = CYAN_ACCENT
    b1.line.width = Pt(1.2)
    tf1 = b1.text_frame
    tf1.margin_top = Inches(0.03)
    p = tf1.paragraphs[0]
    p.text = "AEROSPACE & DEFENCE SHOP-FLOOR DIGITALIZATION"
    p.font.name = "Arial"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    
    tx = s1.shapes.add_textbox(Inches(0.9), Inches(1.5), Inches(7.5), Inches(1.8))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "TRACE n TRACE\nDigital Execution & Genealogy"
    p.font.name = "Arial"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT
    
    tx_sub = s1.shapes.add_textbox(Inches(0.9), Inches(3.3), Inches(7.5), Inches(0.8))
    tf_sub = tx_sub.text_frame
    tf_sub.word_wrap = True
    p = tf_sub.paragraphs[0]
    p.text = "Non-Invasive Shop-Floor Execution, Hardware Poka-Yoke & End-to-End Traceability without SAP Licensing Overheads"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.italic = True
    p.font.color.rgb = TEXT_LIGHT_MUTED
    
    # Left Executive Context Card
    ov_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(4.3), Inches(7.5), Inches(2.4))
    ov_card.fill.solid()
    ov_card.fill.fore_color.rgb = DARK_CARD
    ov_card.line.color.rgb = DARK_BORDER
    ov_card.line.width = Pt(1)
    tf_ov = ov_card.text_frame
    tf_ov.word_wrap = True
    tf_ov.margin_left = tf_ov.margin_right = Inches(0.25)
    tf_ov.margin_top = Inches(0.18)
    
    ov_bullets = [
        ("Client:", " Hical Technologies Private Limited (Aerospace, Defence & Electromechanical)"),
        ("Strategic Objective:", " Digitize physical shop-floor travelers and enforce zero-defect quality gates."),
        ("Architecture Integrity:", " 100% Non-Invasive Read-Only Interface — Zero database write risks to SAP."),
        ("Licensing Advantage:", " Zero Named SAP Fiori/Professional User Licenses required for shop-floor operators."),
        ("Turnkey Commitment:", " 90-Day Production Go-Live backed by 60 Days of Dedicated Hypercare.")
    ]
    for i, (b_title, b_desc) in enumerate(ov_bullets):
        p = tf_ov.paragraphs[0] if i == 0 else tf_ov.add_paragraph()
        p.space_after = Pt(4)
        r1 = p.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = GOLD_ACCENT
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.bold = False
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_LIGHT

    # Right side 3 Strategic Pillars Card
    right_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.7), Inches(1.5), Inches(3.8), Inches(5.2))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = DARK_CARD
    right_card.line.color.rgb = DARK_BORDER
    right_card.line.width = Pt(1)
    
    tf_rc = right_card.text_frame
    tf_rc.word_wrap = True
    tf_rc.margin_left = tf_rc.margin_right = Inches(0.2)
    tf_rc.margin_top = Inches(0.2)
    p = tf_rc.paragraphs[0]
    p.text = "THE THREE STRATEGIC PILLARS"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    
    pillars_data = [
        ("1. ZERO-RISK ARCHITECTURE", "100% Read-Only data extraction. Live SAP database remains completely untampered, with zero table locks.", SAP_BLUE),
        ("2. HARDWARE POKA-YOKE", "Zebra/Honeywell barcode scanning stops incorrect lots, expired batches, and outdated drawings instantly.", EMERALD_GREEN),
        ("3. AIR-GAPPED APPROVAL", "Two-tier digital sign-off (Supervisor + QC) producing pre-verified Ready-to-Post slips for SAP GUI entry.", GOLD_ACCENT)
    ]
    
    top_pos = 2.1
    for title, desc, clr in pillars_data:
        box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.9), Inches(top_pos), Inches(3.4), Inches(1.3))
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(15, 23, 42)
        box.line.color.rgb = clr
        box.line.width = Pt(1)
        tf_b = box.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = Inches(0.15)
        tf_b.margin_top = Inches(0.12)
        p1 = tf_b.paragraphs[0]
        p1.text = title
        p1.font.bold = True
        p1.font.size = Pt(9)
        p1.font.color.rgb = clr
        p2 = tf_b.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(8)
        p2.font.color.rgb = TEXT_LIGHT_MUTED
        top_pos += 1.45

    add_footer(s1, 1, is_dark=True)

    # =============================================================
    # SLIDE 2: Problem Context (Tell: The Shop-Floor Bottleneck)
    # =============================================================
    s2 = add_base_slide(is_dark=False)
    add_header(s2, "The Aerospace Shop-Floor Reality: 3 Operating Disconnects", "PROBLEM CONTEXT & OPERATIONAL PAIN", "Why high-reliability discrete manufacturing struggles with paper job cards and conventional ERP extensions")
    
    clean_pains = [
        ("1. Paper Traveler Friction & Data Latency", [
            ("Laminated Paper Routing:", "Job cards physically wander through 8 to 15 manufacturing and testing bays."),
            ("Shift-End Backlog:", "Actual labor hours, batch consumption, and inspection results are logged into SAP 24–48 hours late."),
            ("Audit Exposure:", "Lost, stained, or illegible paper signatures create severe AS9100 customer audit risks.")
        ], CRIMSON_RED),
        ("2. The SAP Licensing Cost Barrier", [
            ("Named User Overhead:", "Extending SAP Fiori to 150–300 shop-floor operators costs ₹80L–₹1.5Cr+ in recurring software licensing."),
            ("Administrative Complexity:", "Managing ERP credentials and access profiles for shop-floor operators is impractical."),
            ("Infeasible Business Case:", "Direct SAP licensing for assembly-line data capture is economically unviable.")
        ], AMBER_WARN),
        ("3. Human Error & Live ERP Risk", [
            ("Missing Physical Poka-Yoke:", "Visual checks under pressure fail to block assembling incorrect component batches or expired resins."),
            ("Drawing Revision Mismatches:", "Components assembled against obsolete engineering revisions trigger costly scrap."),
            ("Database Lock Concerns:", "Direct concurrent write-calls from hundreds of devices threaten SAP database performance.")
        ], SAP_BLUE)
    ]
    
    col_w2 = 3.75
    spacing_c2 = 0.24
    for idx, (head, points, border_clr) in enumerate(clean_pains):
        c_left = 0.8 + idx * (col_w2 + spacing_c2)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(col_w2), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_clr
        card.line.width = Pt(1.5)
        
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.2)
        tf_c.margin_top = Inches(0.2)
        
        p = tf_c.paragraphs[0]
        p.text = head
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = border_clr
        p.space_after = Pt(14)
        
        for p_title, p_desc in points:
            p_pt = tf_c.add_paragraph()
            p_pt.space_after = Pt(10)
            r1 = p_pt.add_run()
            r1.text = p_title + "\n"
            r1.font.bold = True
            r1.font.size = Pt(9.5)
            r1.font.color.rgb = TEXT_DARK
            r2 = p_pt.add_run()
            r2.text = p_desc
            r2.font.bold = False
            r2.font.size = Pt(8.5)
            r2.font.color.rgb = TEXT_MUTED

    add_footer(s2, 2, is_dark=False)

    # =============================================================
    # SLIDE 3: Strategic Value Proposition (Tell: The Solution)
    # =============================================================
    s3 = add_base_slide(is_dark=True)
    add_header(s3, "TRACE n TRACE Strategic Solution Overview", "VALUE PROPOSITION", "Delivering shop-floor digital execution and error-proofing while keeping the SAP core completely untouched", is_dark=True)
    
    clean_sol_cards = [
        ("1. Non-Invasive by Design", "Protecting the SAP Core", [
            ("Zero Direct Write Calls:", "Standard read-only OData communication. Your live SAP database remains untampered."),
            ("Zero Table Lock Risk:", "No database deadlocks or performance degradation for enterprise users."),
            ("Air-Gapped Execution:", "Shop floor operates on high-speed modern web and edge technology.")
        ], CYAN_ACCENT),
        ("2. Zero Added SAP Licenses", "Massive OpEx Cost Avoidance", [
            ("No Named Fiori Licenses:", "Operators use open-standard rugged handheld terminals without SAP user accounts."),
            ("Single Interface User:", "Requires only a single technical communication account to read master and order data."),
            ("Immediate Payback:", "Saves ₹45L–₹75L in software fees, delivering complete payback in 3.5 to 4.5 months.")
        ], GOLD_ACCENT),
        ("3. Digital Poka-Yoke & Quality", "Zero-Defect Aerospace Manufacturing", [
            ("Hardware Barcode Enforced:", "Scanners immediately lock the terminal if an incorrect or expired component is scanned."),
            ("Drawing ECN Enforcer:", "Prevents assembly of outdated revision materials against active production orders."),
            ("15-Second Traceability:", "Generates complete 360° genealogy trees for AS9100 customer audits in seconds.")
        ], EMERALD_GREEN)
    ]
    
    for idx, (title, sub, points, border_c) in enumerate(clean_sol_cards):
        c_left = 0.8 + idx * (col_w2 + spacing_c2)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(col_w2), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = DARK_CARD
        card.line.color.rgb = border_c
        card.line.width = Pt(1.5)
        
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.2)
        tf_c.margin_top = Inches(0.2)
        
        p = tf_c.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = border_c
        
        p_sub = tf_c.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(8.5)
        p_sub.font.italic = True
        p_sub.font.color.rgb = TEXT_LIGHT_MUTED
        p_sub.space_after = Pt(14)
        
        for pt_head, pt_body in points:
            p_pt = tf_c.add_paragraph()
            p_pt.space_after = Pt(10)
            r1 = p_pt.add_run()
            r1.text = pt_head + "\n"
            r1.font.bold = True
            r1.font.size = Pt(9.5)
            r1.font.color.rgb = TEXT_LIGHT
            r2 = p_pt.add_run()
            r2.text = pt_body
            r2.font.bold = False
            r2.font.size = Pt(8.5)
            r2.font.color.rgb = TEXT_LIGHT_MUTED

    add_footer(s3, 3, is_dark=True)

    # =============================================================
    # SLIDE 4: THE ARCHITECTURE DIAGRAM (Show: Actual Visual Blueprint)
    # =============================================================
    s4 = add_base_slide(is_dark=True)
    add_header(s4, "Enterprise Architecture Diagram: The Air-Gapped Operational Pipeline", "TECHNICAL ARCHITECTURE BLUEPRINT", "Decoupled multi-tier flow isolating SAP from shop-floor transactions while ensuring 100% operational fidelity", is_dark=True)
    
    # 1. TOP TIER: SAP S/4HANA Core
    sap_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(1.1))
    sap_box.fill.solid()
    sap_box.fill.fore_color.rgb = DARK_CARD
    sap_box.line.color.rgb = SAP_BLUE
    sap_box.line.width = Pt(1.5)
    
    tf_sap = sap_box.text_frame
    tf_sap.word_wrap = True
    tf_sap.margin_left = Inches(0.2)
    tf_sap.margin_top = Inches(0.12)
    p = tf_sap.paragraphs[0]
    p.text = "TIER 1: SAP S/4HANA ENTERPRISE SYSTEM OF RECORD"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = SAP_BLUE
    
    p2 = tf_sap.add_paragraph()
    r = p2.add_run()
    r.text = "Exposes standard, certified Read-Only OData Endpoints (Work Orders, BOM Component Reservations, Quality Inspection Plans, Stock Status).\n"
    r.font.size = Pt(8.5)
    r.font.color.rgb = TEXT_LIGHT_MUTED
    r_badge = p2.add_run()
    r_badge.text = "[ ARCHITECTURAL GUARANTEE: 100% READ-ONLY | ZERO WRITE-CALLS | ZERO DATABASE LOCKS | 100% UNHARMED ]"
    r_badge.font.size = Pt(8.2)
    r_badge.font.bold = True
    r_badge.font.color.rgb = EMERALD_GREEN

    # Arrow Down from SAP to Middle Tier
    arr1 = s4.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(6.3), Inches(2.75), Inches(0.7), Inches(0.28))
    arr1.fill.solid()
    arr1.fill.fore_color.rgb = CYAN_ACCENT
    arr1.line.fill.background()

    # 2. MIDDLE TIER: TRACE n TRACE Enterprise Middleware
    mid_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.08), Inches(6.5), Inches(1.5))
    mid_box.fill.solid()
    mid_box.fill.fore_color.rgb = DARK_CARD
    mid_box.line.color.rgb = CYAN_ACCENT
    mid_box.line.width = Pt(1.5)
    
    tf_mid = mid_box.text_frame
    tf_mid.word_wrap = True
    tf_mid.margin_left = Inches(0.2)
    tf_mid.margin_top = Inches(0.12)
    p = tf_mid.paragraphs[0]
    p.text = "TIER 2: TRACE n TRACE ENTERPRISE MIDDLEWARE"
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    
    mid_items = [
        "• Secure API Gateway with encrypted communication and token rate-limiting.",
        "• Periodic delta synchronization: near-zero CPU load on SAP application server.",
        "• Operational PostgreSQL database storing As-Built Genealogy graph and active shop-floor state."
    ]
    for it in mid_items:
        p_it = tf_mid.add_paragraph()
        p_it.text = it
        p_it.font.size = Pt(8.2)
        p_it.font.color.rgb = TEXT_LIGHT_MUTED

    # Arrow Down to Shop Floor
    arr2 = s4.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(4.0), Inches(4.62), Inches(0.6), Inches(0.25))
    arr2.fill.solid()
    arr2.fill.fore_color.rgb = EMERALD_GREEN
    arr2.line.fill.background()

    # 3. BOTTOM TIER: Digital Shop Floor
    floor_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.92), Inches(6.5), Inches(1.85))
    floor_box.fill.solid()
    floor_box.fill.fore_color.rgb = DARK_CARD
    floor_box.line.color.rgb = EMERALD_GREEN
    floor_box.line.width = Pt(1.5)
    
    tf_fl = floor_box.text_frame
    tf_fl.word_wrap = True
    tf_fl.margin_left = Inches(0.2)
    tf_fl.margin_top = Inches(0.12)
    p = tf_fl.paragraphs[0]
    p.text = "TIER 3: DIGITAL SHOP-FLOOR EXECUTION (ZEBRA / HONEYWELL HHTs)"
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_GREEN
    
    floor_items = [
        "• Rugged Handheld Scanners & Tablets: Gloved operation, touchless badge labor clocking.",
        "• Barcode Poka-Yoke: Instant hardware lockout upon scanning wrong lots or obsolete ECNs.",
        "• Offline Edge Buffer: SQLite cache enables 100% uninterrupted scanning in RF-shielded cleanrooms.",
        "• Digital Travelers: Step-by-step SOPs, wiring schematics, and live parameter logging."
    ]
    for it in floor_items:
        p_it = tf_fl.add_paragraph()
        p_it.text = it
        p_it.font.size = Pt(8.2)
        p_it.font.color.rgb = TEXT_LIGHT_MUTED

    # Arrow Right to Approval Desk
    arr3 = s4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(7.35), Inches(5.6), Inches(0.55), Inches(0.4))
    arr3.fill.solid()
    arr3.fill.fore_color.rgb = GOLD_ACCENT
    arr3.line.fill.background()

    # 4. RIGHT CONTAINER: Two-Tier Approval Desk & Slips
    appr_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.95), Inches(3.08), Inches(4.583), Inches(3.69))
    appr_box.fill.solid()
    appr_box.fill.fore_color.rgb = DARK_CARD
    appr_box.line.color.rgb = GOLD_ACCENT
    appr_box.line.width = Pt(1.5)
    
    tf_ap = appr_box.text_frame
    tf_ap.word_wrap = True
    tf_ap.margin_left = Inches(0.2)
    tf_ap.margin_top = Inches(0.15)
    p = tf_ap.paragraphs[0]
    p.text = "TWO-TIER OPERATIONAL APPROVAL DESK"
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    
    ap_items = [
        ("Step 1. Supervisor Review:", "Shift supervisor validates confirmed labor actuals, cycle times, and operator hours using secure PIN."),
        ("Step 2. QC Inspector Stamp:", "QC gatekeeper validates electrical readings, dimensional tolerances, and affixes digital stamp."),
        ("Step 3. 'Ready-to-Post' Slip:", "Auto-compiles verified operational summaries indexed by SAP Transaction Code:"),
        ("   • CO11N:", "Confirmed Order Operations, Scrap & Actual Hours"),
        ("   • MIGO:", "Backflush Component Consumption & FG Goods Receipt"),
        ("   • QE51N:", "Inspection Lot Results & Qualitative Parameters"),
        ("Step 4. Controlled ERP Inward:", "Authorized clerk reviews slip and posts to SAP GUI with 100% first-pass accuracy.")
    ]
    for h_txt, b_txt in ap_items:
        p_it = tf_ap.add_paragraph()
        p_it.space_after = Pt(2)
        r1 = p_it.add_run()
        r1.text = h_txt + " "
        r1.font.bold = True
        r1.font.size = Pt(8.2)
        r1.font.color.rgb = TEXT_LIGHT
        r2 = p_it.add_run()
        r2.text = b_txt
        r2.font.bold = False
        r2.font.size = Pt(8.0)
        r2.font.color.rgb = TEXT_LIGHT_MUTED

    add_footer(s4, 4, is_dark=True)

    # =============================================================
    # SLIDE 5: Functional Journey 1 — Digital Inbound & Kitting
    # =============================================================
    s5 = add_base_slide(is_dark=False)
    add_header(s5, "Functional Journey 1: Digital Inbound & Kitting Verification", "SHOP-FLOOR FUNCTIONAL SUITE", "Eliminating missing-part line halts and ensuring 100% verified material staging for production orders")
    
    kitting_steps = [
        ("1. Receiving Dock Verification", [
            ("Supplier Barcode Scanning:", "Scans 1D/2D barcodes upon arrival, automatically verifying material codes and vendor purchase orders."),
            ("Approved Manufacturer Check:", "Validates parts against approved vendor lists and active revision drawings."),
            ("Quarantine Segregation:", "Instantly flags lots requiring mandatory first-article or laboratory inspection.")
        ], SAP_BLUE),
        ("2. BOM Kitting Cart Validation", [
            ("Picking Cart Verification:", "Scanners cross-reference picking bins against the active production order component reservation list."),
            ("Batch Integrity Check:", "Ensures only released, fully tested component batches are placed into assembly kits."),
            ("Quantity Control:", "Enforces exact pick counts, preventing over-issues and inventory shrinkage.")
        ], CYAN_ACCENT),
        ("3. Staging & Shortage Prevention", [
            ("Shortage Alerts:", "Instantly alerts kitting leads if high-lead aerospace fasteners or connectors are missing."),
            ("Zero Line Starvation:", "Kits are released to assembly bays only after 100% completeness certification."),
            ("Staging Cart Tracking:", "Tracks kit cart location as it moves from the warehouse to the assembly workstation.")
        ], EMERALD_GREEN)
    ]
    
    for idx, (title, points, border_c) in enumerate(kitting_steps):
        c_left = 0.8 + idx * (col_w2 + spacing_c2)
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(col_w2), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_c
        card.line.width = Pt(1.5)
        
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.2)
        tf_c.margin_top = Inches(0.2)
        
        p = tf_c.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = border_c
        p.space_after = Pt(14)
        
        for p_head, p_desc in points:
            p_pt = tf_c.add_paragraph()
            p_pt.space_after = Pt(10)
            r1 = p_pt.add_run()
            r1.text = p_head + "\n"
            r1.font.bold = True
            r1.font.size = Pt(9.5)
            r1.font.color.rgb = TEXT_DARK
            r2 = p_pt.add_run()
            r2.text = p_desc
            r2.font.bold = False
            r2.font.size = Pt(8.5)
            r2.font.color.rgb = TEXT_MUTED

    add_footer(s5, 5, is_dark=False)

    # =============================================================
    # SLIDE 6: Functional Journey 2 — Digital Traveler & Hardware Poka-Yoke
    # =============================================================
    s6 = add_base_slide(is_dark=False)
    add_header(s6, "Functional Journey 2: Operator Digital Traveler & Hardware Poka-Yoke", "WORKSTATION QUALITY ENFORCEMENT", "Replacing paper job cards with touchless digital guidance and automated hardware-level error proofing")
    
    # Left Card: Digital Traveler
    card_l6 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.75), Inches(5.1))
    card_l6.fill.solid()
    card_l6.fill.fore_color.rgb = CARD_BG
    card_l6.line.color.rgb = SAP_BLUE
    card_l6.line.width = Pt(1.5)
    
    tf_l6 = card_l6.text_frame
    tf_l6.word_wrap = True
    tf_l6.margin_left = tf_l6.margin_right = Inches(0.25)
    tf_l6.margin_top = Inches(0.2)
    p = tf_l6.paragraphs[0]
    p.text = "OPERATOR DIGITAL TRAVELER"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = SAP_BLUE
    p.space_after = Pt(12)
    
    trav_items = [
        ("Touchless Labor Tracking:", "Assemblers scan their badge to clock setup and run times, capturing exact labor actuals without clerical overhead."),
        ("Visual Work Instructions:", "Renders high-resolution assembly drawings, wiring schematics, and torque specifications on rugged tablets."),
        ("Dynamic Parameter Capture:", "Technicians record critical values (winding resistance, curing temperatures, crimp pull-force) with instant tolerance checks."),
        ("Paperless Operation:", "Eliminates stained, lost, or illegible paper traveler sheets across all manufacturing bays.")
    ]
    for h, b in trav_items:
        p_pt = tf_l6.add_paragraph()
        p_pt.space_after = Pt(8)
        r1 = p_pt.add_run()
        r1.text = h + "\n"
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p_pt.add_run()
        r2.text = b
        r2.font.bold = False
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = TEXT_MUTED

    # Right Card: Hardware Barcode Poka-Yoke
    card_r6 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.783), Inches(1.6), Inches(5.75), Inches(5.1))
    card_r6.fill.solid()
    card_r6.fill.fore_color.rgb = CARD_BG
    card_r6.line.color.rgb = CRIMSON_RED
    card_r6.line.width = Pt(1.5)
    
    tf_r6 = card_r6.text_frame
    tf_r6.word_wrap = True
    tf_r6.margin_left = tf_r6.margin_right = Inches(0.25)
    tf_r6.margin_top = Inches(0.2)
    p = tf_r6.paragraphs[0]
    p.text = "AEROSPACE HARDWARE BARCODE POKA-YOKE"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CRIMSON_RED
    p.space_after = Pt(12)
    
    poka_items = [
        ("Batch Release Sentinel:", "Scanning an unreleased or quarantined component lot immediately locks the screen with an audible alarm."),
        ("ECN Drawing Revision Lockout:", "Compares component drawing revision against the active production order, preventing obsolete parts usage."),
        ("Chemical Shelf-Life Enforcer:", "Validates expiration dates on potting resins, epoxies, adhesives, and solder pastes prior to application."),
        ("Zero-Defect Quality Gate:", "Assembly step cannot proceed until the correct physical barcode is scanned and validated.")
    ]
    for h, b in poka_items:
        p_pt = tf_r6.add_paragraph()
        p_pt.space_after = Pt(8)
        r1 = p_pt.add_run()
        r1.text = h + "\n"
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p_pt.add_run()
        r2.text = b
        r2.font.bold = False
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = TEXT_MUTED

    add_footer(s6, 6, is_dark=False)

    # =============================================================
    # SLIDE 7: Functional Journey 3 — Two-Tier Approval Desk
    # =============================================================
    s7 = add_base_slide(is_dark=False)
    add_header(s7, "Functional Journey 3: Two-Tier Operational Approval Desk", "OPERATIONAL GOVERNANCE & CONTROL", "Air-gapped dual digital review generating pre-verified Ready-to-Post slips for error-free SAP inward booking")
    
    approval_cards = [
        ("1. Supervisor Verification", "Tier 1: Labor & Output Check", [
            ("Operational Review:", "Shift supervisor inspects confirmed machine times, labor hours, and piece counts."),
            ("Discrepancy Flags:", "System automatically highlights cycle times that deviate significantly from routing standards."),
            ("Digital Sign-Off:", "Supervisor authorizes the traveler package via secure digital PIN or smart badge scan.")
        ], SAP_BLUE),
        ("2. Quality Gatekeeper (QC)", "Tier 2: Engineering Tolerances", [
            ("Measurement Audit:", "QC inspector verifies recorded electrical readings, dimensional tolerances, and visual logs."),
            ("Instrument Calibration:", "Verifies that testing devices used were within valid calibration periods."),
            ("Cryptographic Stamp:", "QC applies digital sign-off, locking the operational record into 'Verified' status.")
        ], CYAN_ACCENT),
        ("3. Ready-to-Post Slips", "Air-Gapped ERP Inward Entry", [
            ("CO11N Confirmation Slip:", "Pre-formats actual setup, machine hours, and confirmed yields for production orders."),
            ("MIGO Goods Movement Slip:", "Pre-verified material backflush (261) and finished assembly receipt (101)."),
            ("QE51N Quality Slip:", "Compiles inspection lot results for instant first-pass entry into SAP GUI with zero typing errors.")
        ], EMERALD_GREEN)
    ]
    
    for idx, (title, sub, items, border_c) in enumerate(approval_cards):
        c_left = 0.8 + idx * (col_w2 + spacing_c2)
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(col_w2), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_c
        card.line.width = Pt(1.5)
        
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.2)
        tf_c.margin_top = Inches(0.2)
        
        p = tf_c.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = border_c
        
        p_sub = tf_c.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(8.5)
        p_sub.font.italic = True
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_after = Pt(14)
        
        for item_h, item_d in items:
            p_it = tf_c.add_paragraph()
            p_it.space_after = Pt(10)
            r1 = p_it.add_run()
            r1.text = item_h + "\n"
            r1.font.bold = True
            r1.font.size = Pt(9.5)
            r1.font.color.rgb = TEXT_DARK
            r2 = p_it.add_run()
            r2.text = item_d
            r2.font.bold = False
            r2.font.size = Pt(8.5)
            r2.font.color.rgb = TEXT_MUTED

    add_footer(s7, 7, is_dark=False)

    # =============================================================
    # SLIDE 8: Functional Journey 4 — 360° Genealogy & Defect Routing
    # =============================================================
    s8 = add_base_slide(is_dark=False)
    add_header(s8, "Functional Journey 4: 360° As-Built Genealogy & Defect Routing", "TRACEABILITY & NON-CONFORMANCE", "Instant aerospace audit defense in <15 seconds and dynamic shop-floor rework branch control")
    
    # Left: 360 Genealogy
    card_l8 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.75), Inches(5.1))
    card_l8.fill.solid()
    card_l8.fill.fore_color.rgb = CARD_BG
    card_l8.line.color.rgb = PURPLE_ACCENT
    card_l8.line.width = Pt(1.5)
    
    tf_l8 = card_l8.text_frame
    tf_l8.word_wrap = True
    tf_l8.margin_left = tf_l8.margin_right = Inches(0.25)
    tf_l8.margin_top = Inches(0.2)
    p = tf_l8.paragraphs[0]
    p.text = "360° BI-DIRECTIONAL GENEALOGY"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PURPLE_ACCENT
    p.space_after = Pt(12)
    
    gen_items = [
        ("Top-Down Finished Good Search:", "Enter an actuator or motor serial number to instantly generate the complete As-Built hierarchy: every subassembly, internal winding lot, raw wire spool, connector, and operator stamp."),
        ("Bottom-Up Raw Batch Traceability:", "Enter a suspect vendor raw material lot (e.g., magnet wire spool) to pinpoint every finished assembly containing that material across active WIP, storage, and customer dispatches in 5 seconds."),
        ("AS9100 Audit Defense in <15 Seconds:", "Transforms customer and regulatory traceability audits from days of frantic paper-chasing into a single-click demonstration.")
    ]
    for h, b in gen_items:
        p_pt = tf_l8.add_paragraph()
        p_pt.space_after = Pt(10)
        r1 = p_pt.add_run()
        r1.text = h + "\n"
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p_pt.add_run()
        r2.text = b
        r2.font.bold = False
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = TEXT_MUTED

    # Right: Defect & Rework Routing
    card_r8 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.783), Inches(1.6), Inches(5.75), Inches(5.1))
    card_r8.fill.solid()
    card_r8.fill.fore_color.rgb = CARD_BG
    card_r8.line.color.rgb = GOLD_ACCENT
    card_r8.line.width = Pt(1.5)
    
    tf_r8 = card_r8.text_frame
    tf_r8.word_wrap = True
    tf_r8.margin_left = tf_r8.margin_right = Inches(0.25)
    tf_r8.margin_top = Inches(0.2)
    p = tf_r8.paragraphs[0]
    p.text = "DEFECT & REWORK ROUTING ENGINE"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    p.space_after = Pt(12)
    
    rework_items = [
        ("Digital NCR Logging:", "Operators log non-conformance reports on handhelds with photographic evidence and failure category codes."),
        ("Dynamic Rework Branching:", "Spawns authorized rework sub-operations (re-winding, touch-up soldering, re-curing) without corrupting the parent production order in SAP."),
        ("Mandatory Re-Inspection:", "Enforces mandatory QC re-test and calibration before reworked parts can merge back into the main assembly routing."),
        ("Scrap Segregation & Attribution:", "Segregates scrapped parts physically and digitally with automated cost-center and root-cause attribution.")
    ]
    for h, b in rework_items:
        p_pt = tf_r8.add_paragraph()
        p_pt.space_after = Pt(10)
        r1 = p_pt.add_run()
        r1.text = h + "\n"
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p_pt.add_run()
        r2.text = b
        r2.font.bold = False
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = TEXT_MUTED

    add_footer(s8, 8, is_dark=False)

    # =============================================================
    # SLIDE 9: 90-Day Implementation Plan & 60-Day Hypercare
    # =============================================================
    s9 = add_base_slide(is_dark=False)
    add_header(s9, "90-Day Agile Implementation Roadmap & 60-Day Hypercare", "PROJECT PLAN & MILESTONES", "Five structured milestone stages ensuring rapid shop-floor deployment and comprehensive AS9100 validation")
    
    phases_s9 = [
        ("PHASE 1: BLUEPRINT", "Days 1–15", [
            ("Shop-Floor Study:", "Cell walkthrough across motors & cable assembly bays."),
            ("OData Validation:", "Testing read endpoints in SAP Sandbox."),
            ("Architecture Sign-Off:", "Approved FRS & technical blueprint.")
        ], "Gate 1: Blueprint Sign-Off (20% Milestone)", SAP_BLUE),
        ("PHASE 2: CORE APP BUILD", "Days 16–45", [
            ("HHT Client Build:", "Zebra/Honeywell scanner application."),
            ("Poka-Yoke Rules:", "Barcode verification engine."),
            ("Edge Offline Cache:", "Local SQLite edge buffering.")
        ], "Gate 2: App Alpha Complete (30% Milestone)", CYAN_ACCENT),
        ("PHASE 3: INTEGRATION", "Days 46–65", [
            ("OData Pipeline:", "Delta synchronization to middleware."),
            ("Approval Workbench:", "Supervisor & QC review desk."),
            ("Slip Compiler:", "Ready-to-Post engine (CO11N/MIGO).")
        ], "Review: System Integration Walkthrough", PURPLE_ACCENT),
        ("PHASE 4: DRY-RUNS & UAT", "Days 66–80", [
            ("Pilot Assembly Line:", "Dry-run on 2 active production cells."),
            ("Scanner Stress Test:", "15+ Zebra scanners concurrent run."),
            ("AS9100 Audit Dry-Run:", "Simulated 15-second genealogy audit.")
        ], "Gate 3: Formal Business UAT Sign-Off (30% Milestone)", AMBER_WARN),
        ("PHASE 5: CUTOVER & LIVE", "Days 81–90", [
            ("Production Rollout:", "Deployment to on-premise server."),
            ("Operator Training:", "Shift training for 50+ shop-floor users."),
            ("SOP & Handover:", "Commercial go-live transition.")
        ], "Gate 4: Production Go-Live (20% Milestone)", EMERALD_GREEN)
    ]
    
    p_w = 2.15
    p_spacing = 0.2
    for idx, (p_title, p_time, p_tasks, p_gate, p_clr) in enumerate(phases_s9):
        p_left = 0.8 + idx * (p_w + p_spacing)
        card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(p_left), Inches(1.6), Inches(p_w), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = p_clr
        card.line.width = Pt(1.5)
        
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.12)
        tf_c.margin_top = Inches(0.15)
        
        p = tf_c.paragraphs[0]
        p.text = p_title
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = p_clr
        
        p_sub = tf_c.add_paragraph()
        p_sub.text = p_time
        p_sub.font.size = Pt(8.5)
        p_sub.font.bold = True
        p_sub.font.color.rgb = TEXT_DARK
        p_sub.space_after = Pt(8)
        
        for t_h, t_d in p_tasks:
            p_t = tf_c.add_paragraph()
            p_t.space_after = Pt(5)
            r1 = p_t.add_run()
            r1.text = "• " + t_h + " "
            r1.font.bold = True
            r1.font.size = Pt(8)
            r1.font.color.rgb = TEXT_DARK
            r2 = p_t.add_run()
            r2.text = t_d
            r2.font.bold = False
            r2.font.size = Pt(7.8)
            r2.font.color.rgb = TEXT_MUTED
            
        p_g = tf_c.add_paragraph()
        p_g.space_before = Pt(12)
        r_g = p_g.add_run()
        r_g.text = p_gate
        r_g.font.bold = True
        r_g.font.size = Pt(7.8)
        r_g.font.color.rgb = p_clr

    add_footer(s9, 9, is_dark=False)

    # =============================================================
    # SLIDE 10: Turnkey Commercial Investment Framework (Tell: The Investment)
    # =============================================================
    s10 = add_base_slide(is_dark=True)
    add_header(s10, "Turnkey Commercial Investment & Milestone Framework", "COMMERCIAL PROPOSAL", "Turnkey Fixed-Price Implementation backed by 60 Days Hypercare and SLA-driven AMS", is_dark=True)
    
    comm_cards_s10 = [
        ("1. TURNKEY IMPLEMENTATION", "₹28,50,000 INR (Excl. Taxes)", [
            ("A. App & Platform Development:", "₹18,50,000\nEnd-to-end TRACE n TRACE software, Zebra/Honeywell scanner app, Two-Tier Approval Desk, SQLite edge cache, and As-Built genealogy engine."),
            ("B. SAP Integration & Middleware:", "₹10,00,000\nRead-only SAP OData configuration, delta sync middleware, Ready-to-Post Slip compiler (CO11N/MIGO/QE51N), AS9100 validation, and UAT.")
        ], CYAN_ACCENT),
        ("2. MILESTONE PAYMENT GATES", "Deliverable-Linked Billing", [
            ("Milestone 1 — 20% (₹5,70,000):", "Upon Kickoff and approved Architecture Blueprint (Day 15)."),
            ("Milestone 2 — 30% (₹8,55,000):", "Upon Core HHT Scanning App & Poka-Yoke Engine Complete (Day 45)."),
            ("Milestone 3 — 30% (₹8,55,000):", "Upon Middleware Integration & Shop-Floor UAT Sign-Off (Day 80)."),
            ("Milestone 4 — 20% (₹5,70,000):", "Upon Production Go-Live, Training & System Handover (Day 90).")
        ], GOLD_ACCENT),
        ("3. POST-GO-LIVE SUPPORT (AMS)", "Hypercare + Ongoing Retainer", [
            ("60-Day Dedicated Hypercare:", "INCLUDED at zero extra cost. On-site & remote stabilization, daily standups, and tuning."),
            ("Ongoing AMS Support:", "Time & Material (T&M) Retainer billed quarterly based on consumed effort hours."),
            ("Guaranteed SLA Tiers:", "• P1 (Production Halt): 2 Hr Response\n• P2 (Feature Degradation): 4 Hr Response\n• P3 (General Query): 8 Hr Response")
        ], EMERALD_GREEN)
    ]
    
    col_w10 = 3.75
    spacing_c10 = 0.24
    for idx, (title, sub, items, border_c) in enumerate(comm_cards_s10):
        c_left = 0.8 + idx * (col_w10 + spacing_c10)
        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(col_w10), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = DARK_CARD
        card.line.color.rgb = border_c
        card.line.width = Pt(1.5)
        
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.2)
        tf_c.margin_top = Inches(0.2)
        
        p = tf_c.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = border_c
        
        p_sub = tf_c.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(9)
        p_sub.font.italic = True
        p_sub.font.color.rgb = TEXT_LIGHT_MUTED
        p_sub.space_after = Pt(12)
        
        for item_h, item_d in items:
            p_it = tf_c.add_paragraph()
            p_it.space_after = Pt(8)
            r1 = p_it.add_run()
            r1.text = item_h + "\n"
            r1.font.bold = True
            r1.font.size = Pt(8.5)
            r1.font.color.rgb = TEXT_LIGHT
            r2 = p_it.add_run()
            r2.text = item_d
            r2.font.bold = False
            r2.font.size = Pt(8.2)
            r2.font.color.rgb = TEXT_LIGHT_MUTED

    add_footer(s10, 10, is_dark=True)

    # =============================================================
    # SLIDE 11: Governance, Dependencies & Terms (Tell: Governance)
    # =============================================================
    s11 = add_base_slide(is_dark=False)
    add_header(s11, "Assumptions, Technical Dependencies & Commercial Terms", "GOVERNANCE & ENGAGEMENT TERMS", "Clear boundaries, client prerequisites, and contractual governance for predictable execution")
    
    terms_cards_s11 = [
        ("1. Client Dependencies (Hical)", [
            ("SAP OData Service Exposure:", "Hical IT to expose standard read-only OData endpoints with HTTPS network accessibility to middle tier."),
            ("Environment & Test Data:", "Provisioning of SAP Sandbox/Quality systems with active BOMs and discrete routing master data within 5 days of kickoff."),
            ("Rugged HHT Hardware:", "Hical to supply required Zebra/Honeywell handheld terminals with barcode wedge drivers and ensure floor Wi-Fi coverage.")
        ], SAP_BLUE),
        ("2. Key Architectural Assumptions", [
            ("Strictly Non-Invasive:", "SAP remains 100% read-only throughout. No custom ABAP write-back tables, direct RFC write destinations, or BAPIs."),
            ("Booking Authority Retained:", "Physical posting of production confirmations (CO11N) and goods receipts (MIGO) into SAP GUI remains under Hical's authorized personnel."),
            ("Source Master Data:", "Master data consistency in SAP (material numbers, BOM revisions, vendor info) is maintained by Hical internal teams.")
        ], CYAN_ACCENT),
        ("3. Commercial Terms & Conditions", [
            ("Proposal Validity:", "Commercial pricing of ₹28,50,000 INR is valid for 45 calendar days from formal presentation."),
            ("Taxation & Payments:", "GST @ 18% extra as applicable. Invoices payable within 15 business days of electronic milestone submission."),
            ("100% IP Transfer to Hical:", "Complete source code, configuration scripts, and documentation transfer exclusively to Hical upon final settlement."),
            ("Confidentiality & NDA:", "Strict mutual confidentiality protecting Hical's proprietary aerospace BOMs, pricing, and manufacturing parameters.")
        ], EMERALD_GREEN)
    ]
    
    col_w11 = 3.75
    for idx, (title, points, border_c) in enumerate(terms_cards_s11):
        c_left = 0.8 + idx * (col_w11 + spacing_c10)
        card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(col_w11), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_c
        card.line.width = Pt(1.5)
        
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.2)
        tf_c.margin_top = Inches(0.2)
        
        p = tf_c.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = border_c
        p.space_after = Pt(12)
        
        for pt_head, pt_body in points:
            p_pt = tf_c.add_paragraph()
            p_pt.space_after = Pt(8)
            r1 = p_pt.add_run()
            r1.text = "• " + pt_head + " "
            r1.font.bold = True
            r1.font.size = Pt(8.5)
            r1.font.color.rgb = TEXT_DARK
            r2 = p_pt.add_run()
            r2.text = pt_body
            r2.font.bold = False
            r2.font.size = Pt(8.0)
            r2.font.color.rgb = TEXT_MUTED

    add_footer(s11, 11, is_dark=False)

    # =============================================================
    # SLIDE 12: Business Value Recap & ROI (Tell: Closing Recap)
    # =============================================================
    s12 = add_base_slide(is_dark=True)
    add_header(s12, "Executive Value Recap: Why TRACE n TRACE for Hical", "CLOSING VALUE RECAP & ROI", "Recapping major value drivers and strategic win themes delivering 3.8x to 6.1x First-Year ROI", is_dark=True)
    
    # Left Side: Win Themes Recap Card
    recap_card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.75), Inches(5.1))
    recap_card.fill.solid()
    recap_card.fill.fore_color.rgb = DARK_CARD
    recap_card.line.color.rgb = CYAN_ACCENT
    recap_card.line.width = Pt(1.5)
    
    tf_rc = recap_card.text_frame
    tf_rc.word_wrap = True
    tf_rc.margin_left = tf_rc.margin_right = Inches(0.2)
    tf_rc.margin_top = Inches(0.2)
    
    p = tf_rc.paragraphs[0]
    p.text = "FOUR STRATEGIC WIN THEMES"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(10)
    
    recap_items = [
        ("1. Zero SAP Core Risk:", "100% read-only OData architecture ensures zero database deadlocks, table locks, or schema corruption."),
        ("2. Huge Licensing Savings:", "Floor operators use open-standard rugged handheld terminals without needing expensive Named SAP Fiori licenses."),
        ("3. AS9100 Zero-Defect Enforcement:", "Hardware barcode Poka-Yoke halts wrong component batches, unapproved ECN revisions, and expired resins instantly."),
        ("4. Two-Tier Air-Gapped Governance:", "Supervisor PIN + QC digital stamp generates pre-verified Ready-to-Post slips (CO11N, MIGO, QE51N), keeping ERP postings 100% error-free.")
    ]
    for r_head, r_body in recap_items:
        p_it = tf_rc.add_paragraph()
        p_it.space_after = Pt(8)
        r1 = p_it.add_run()
        r1.text = r_head + "\n"
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = TEXT_LIGHT
        r2 = p_it.add_run()
        r2.text = r_body
        r2.font.bold = False
        r2.font.size = Pt(8.2)
        r2.font.color.rgb = TEXT_LIGHT_MUTED

    # Right Side: Financial ROI Table Card
    roi_card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.783), Inches(1.6), Inches(5.75), Inches(5.1))
    roi_card.fill.solid()
    roi_card.fill.fore_color.rgb = DARK_CARD
    roi_card.line.color.rgb = GOLD_ACCENT
    roi_card.line.width = Pt(1.5)
    
    tf_roi = roi_card.text_frame
    tf_roi.word_wrap = True
    tf_roi.margin_left = tf_roi.margin_right = Inches(0.2)
    tf_roi.margin_top = Inches(0.2)
    
    p = tf_roi.paragraphs[0]
    p.text = "TANGIBLE ANNUAL VALUE CREATION FOR HICAL"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    p.space_after = Pt(10)
    
    roi_table_data = [
        ("SAP License Cost Avoidance (150 Floor Users):", "₹45,00,000 – ₹75,00,000"),
        ("Assembly Rework & Scrap Eradication (Poka-Yoke):", "₹28,00,000 – ₹42,00,000"),
        ("Paper Traveler Shift-End Labor Recovery:", "₹15,00,000 – ₹22,00,000"),
        ("AS9100 Audit Defense & Penalty Avoidance:", "₹20,00,000 – ₹35,00,000"),
        ("TOTAL ESTIMATED ANNUAL VALUE RELEASE:", "₹1,08,00,000 – ₹1,74,00,000"),
        ("PROJECT PAYBACK PERIOD:", "3.5 to 4.5 Months (ROI: 3.8x – 6.1x)")
    ]
    
    for r_lbl, r_val in roi_table_data:
        p_row = tf_roi.add_paragraph()
        p_row.space_after = Pt(7)
        r1 = p_row.add_run()
        r1.text = r_lbl + "\n"
        r1.font.bold = ("TOTAL" in r_lbl or "PAYBACK" in r_lbl)
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = GOLD_ACCENT if ("TOTAL" in r_lbl or "PAYBACK" in r_lbl) else TEXT_LIGHT
        
        r2 = p_row.add_run()
        r2.text = r_val
        r2.font.bold = True
        r2.font.size = Pt(9.5 if ("TOTAL" in r_lbl or "PAYBACK" in r_lbl) else 8.5)
        r2.font.color.rgb = EMERALD_GREEN if ("TOTAL" in r_lbl or "PAYBACK" in r_lbl) else CYAN_ACCENT

    add_footer(s12, 12, is_dark=True)

    # Save presentation
    prs.save(output_path)
    print(f"Successfully generated refined TRACE n TRACE presentation: {output_path}")

if __name__ == "__main__":
    build_refined_trace_deck()
