import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def build_proposal_presentation(output_path="Hical_Technologies_Strategic_CXO_Dashboards_Executive_Proposal.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # -------------------------------------------------------------
    # Palette & Design Tokens
    # -------------------------------------------------------------
    DARK_BG = RGBColor(11, 19, 43)           # #0B132B Deep Executive Navy
    DARK_CARD = RGBColor(21, 31, 60)         # #151F3C Navy Card
    DARK_BORDER = RGBColor(40, 56, 95)       # Navy Outline
    
    LIGHT_BG = RGBColor(248, 250, 252)       # #F8FAFC Slate Ice White
    CARD_BG = RGBColor(255, 255, 255)        # Pure White
    CARD_BORDER = RGBColor(226, 232, 240)    # Soft slate border
    CARD_BG_MUTED = RGBColor(241, 245, 249)  # Light Slate Pill
    WHITE = RGBColor(255, 255, 255)          # White
    
    SAP_BLUE = RGBColor(0, 102, 204)         # #0066CC Enterprise SAP Blue
    CYAN_ACCENT = RGBColor(0, 180, 216)      # #00B4D8 Tech Cyan
    GOLD_ACCENT = RGBColor(217, 119, 6)      # #D97706 Lumbini Amber/Gold
    GOLD_LIGHT_BG = RGBColor(254, 243, 199)  # Gold Tint
    
    EMERALD_GREEN = RGBColor(16, 185, 129)   # #10B981 Success / On-Track
    GREEN_LIGHT_BG = RGBColor(236, 253, 245) # Soft Green Tint
    AMBER_WARN = RGBColor(245, 158, 11)      # #F59E0B Warning
    AMBER_LIGHT_BG = RGBColor(255, 251, 235) # Soft Amber Tint
    CRIMSON_RED = RGBColor(239, 68, 68)      # #EF4444 Critical At-Risk
    RED_LIGHT_BG = RGBColor(254, 242, 242)   # Soft Red Tint
    
    PURPLE_ACCENT = RGBColor(124, 58, 237)   # AI / Simulation Purple
    PURPLE_LIGHT_BG = RGBColor(245, 243, 255)
    
    TEXT_DARK = RGBColor(15, 23, 42)         # #0F172A Primary Dark
    TEXT_MUTED = RGBColor(100, 116, 139)     # #64748B Secondary Slate
    TEXT_LIGHT = RGBColor(248, 250, 252)     # #F8FAFC Off-White
    TEXT_LIGHT_MUTED = RGBColor(148, 163, 184)
    
    TOTAL_SLIDES = 13

    # -------------------------------------------------------------
    # Helper Functions
    # -------------------------------------------------------------
    def add_base_slide(is_dark=False):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = DARK_BG if is_dark else LIGHT_BG
        bg.line.fill.background()
        return slide

    def add_header(slide, title_text, category_text, subtitle_text=None, is_dark=False):
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.38), Inches(4.5), Inches(0.26))
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
        
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.66), Inches(11.733), Inches(0.42))
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
            tx_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.08), Inches(11.733), Inches(0.28))
            tf_sub = tx_sub.text_frame
            tf_sub.word_wrap = True
            tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = tf_sub.margin_bottom = 0
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
        p.text = "Lumbini Elite Solutions  |  Hical Technologies Strategic CXO Dashboards Proposal  |  Confidential"
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
    # SLIDE 1: Title & Executive Positioning (Dark Theme)
    # =============================================================
    s1 = add_base_slide(is_dark=True)
    
    top_glow = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    top_glow.fill.solid()
    top_glow.fill.fore_color.rgb = GOLD_ACCENT
    top_glow.line.fill.background()
    
    b1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.0), Inches(5.2), Inches(0.34))
    b1.fill.solid()
    b1.fill.fore_color.rgb = DARK_CARD
    b1.line.color.rgb = GOLD_ACCENT
    b1.line.width = Pt(1.2)
    tf1 = b1.text_frame
    tf1.margin_top = Inches(0.03)
    p = tf1.paragraphs[0]
    p.text = "AEROSPACE & DEFENCE ENTERPRISE PROPOSAL"
    p.font.name = "Arial"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    
    tx = s1.shapes.add_textbox(Inches(0.9), Inches(1.5), Inches(7.5), Inches(1.8))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Strategic CXO Dashboards\nfor Hical Technologies"
    p.font.name = "Arial"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT
    
    tx_sub = s1.shapes.add_textbox(Inches(0.9), Inches(3.3), Inches(7.5), Inches(0.8))
    tf_sub = tx_sub.text_frame
    tf_sub.word_wrap = True
    p = tf_sub.paragraphs[0]
    p.text = "Unlocking S/4HANA Dormant Data: 3 High-Velocity Executive Cockpits Powered by Native SAP HANA Calculation Views & Microsoft Power BI"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.italic = True
    p.font.color.rgb = TEXT_LIGHT_MUTED
    
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
        ("Technology Stack:", " SAP S/4HANA In-Memory Calculation Views + Microsoft Power BI DirectQuery"),
        ("Commercial Model:", " Fixed-Price Per-Report Commercials @ ₹10,00,000 INR each (₹30,00,000 INR Total)"),
        ("Project Duration:", " 10-Week Agile Execution across 5 Structured Milestone Gates"),
        ("Core Objectives:", " Cash Flow Acceleration, 52-Week Sourcing Pipeline, Real-Time Batch Costing & COPQ")
    ]
    for i, (b_title, b_desc) in enumerate(ov_bullets):
        p = tf_ov.paragraphs[0] if i == 0 else tf_ov.add_paragraph()
        p.space_after = Pt(4)
        r1 = p.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = CYAN_ACCENT
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.bold = False
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_LIGHT

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
    p.text = "THE 3 STRATEGIC COCKPITS"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    
    cockpit_cards_data = [
        ("COCKPIT 1: CASH FLOW & FULFILLMENT", "Dispatch SLAs, Expected Inbound Materials, AR/AP Liquidity Runway, Liquidated Damages Risk Tracker.", SAP_BLUE),
        ("COCKPIT 2: 52-WEEK SOURCING PIPELINE", "52-Week Horizon, Part Traceability, Subcontractor Special Stock 'O', Critical Component Predictor.", CYAN_ACCENT),
        ("COCKPIT 3: MANUFACTURING & BATCH COST", "Full-Kitting Verification, Batch Costing (Standard vs. Actual), COPQ Scrap Engine, WIP Aging Matrix.", PURPLE_ACCENT)
    ]
    
    top_pos = 2.1
    for title, desc, clr in cockpit_cards_data:
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
    # SLIDE 2: Operational Complexity & The Dormant Data Challenge (Light)
    # =============================================================
    s2 = add_base_slide(is_dark=False)
    add_header(s2, "Aerospace Manufacturing Reality: The Dormant Data Bottleneck", "CONTEXT & PROBLEM FRAMING", "Why transactional depth inside S/4HANA without high-velocity analytics leads to trapped working capital and reactive decisions")
    
    cards_data_s2 = [
        ("Precision Aerospace Constraints", [
            ("AS9100D & NADCAP:", "Zero-defect mandates where component deviation halts entire assemblies."),
            ("Multi-Level Indented BOMs:", "Complex assemblies (actuators, motors, cable harnesses) spanning 6-10 tiers."),
            ("Long-Lead Buffers:", "Raw material cycles of 26 to 52 weeks requiring tight procurement coordination."),
            ("Subcontractor Job-Work:", "Specialized plating, heat-treatment, and winding dependencies.")
        ], SAP_BLUE),
        ("The 'Dormant Data' Paradox", [
            ("Transactional Silos:", "S/4HANA records millions of rows, but insights remain locked in deep tables."),
            ("Spreadsheet Dependency:", "Planners stitch together manual weekly Excel exports with high latency."),
            ("Lagging Month-End Signals:", "Cost variances, scrap leakage, and overtime appear weeks after occurrence."),
            ("No Unified Visibility:", "Absence of real-time bridge linking finance with factory-floor execution.")
        ], CRIMSON_RED),
        ("Financial & Business Bleed", [
            ("Trapped Working Capital:", "Buffer stock and unmonitored WIP accumulate across machine stations."),
            ("Liquidated Damages Risk:", "Late delivery penalties (0.5%-1% per week) threaten defense contract margins."),
            ("Job-Work Leakage:", "Material issued to external subcontractors lacks real-time yield/scrap tracking."),
            ("Unplanned Expediting:", "Emergency weekend overtime and spot-freight erode gross profit.")
        ], AMBER_WARN),
        ("The Strategic Imperative", [
            ("In-Memory Push-Down:", "Leverage native SAP HANA Calculation Views to eliminate batch ETL lag."),
            ("Sub-Second Power BI Cockpits:", "Deliver live executive direct-query without burdening live OLTP."),
            ("Proactive Early Warnings:", "Anticipate shortages 60-90 days early and protect project EBITDA."),
            ("Audit-Grade Reconciliation:", "Guarantee mathematical harmony with General Ledger (ACDOCA).")
        ], EMERALD_GREEN)
    ]
    
    left_start = 0.8
    card_w = 2.75
    spacing = 0.24
    for idx, (head, points, border_clr) in enumerate(cards_data_s2):
        c_left = left_start + idx * (card_w + spacing)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(card_w), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_clr
        card.line.width = Pt(1.5)
        
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.18)
        tf_c.margin_top = Inches(0.18)
        
        p = tf_c.paragraphs[0]
        p.text = head
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = border_clr
        p.space_after = Pt(10)
        
        for p_title, p_desc in points:
            p_pt = tf_c.add_paragraph()
            p_pt.space_after = Pt(8)
            r1 = p_pt.add_run()
            r1.text = "• " + p_title + " "
            r1.font.bold = True
            r1.font.size = Pt(8.5)
            r1.font.color.rgb = TEXT_DARK
            r2 = p_pt.add_run()
            r2.text = p_desc
            r2.font.bold = False
            r2.font.size = Pt(8.2)
            r2.font.color.rgb = TEXT_MUTED

    add_footer(s2, 2, is_dark=False)

    # =============================================================
    # SLIDE 3: Enterprise Solution Architecture (Dark)
    # =============================================================
    s3 = add_base_slide(is_dark=True)
    add_header(s3, "Enterprise Solution Architecture: Zero-ETL In-Memory Push-Down", "TECHNICAL ARCHITECTURE", "Connecting SAP S/4HANA Database Internals natively to Microsoft Power BI via DirectQuery", is_dark=True)
    
    arch_cols = [
        ("LAYER 1: S/4HANA DATABASE TABLES", "Transactional Core (Single Source of Truth)", [
            ("Financial Universal Journal:", "ACDOCA, BSID, BSIK, BKPF (Open items, AP/AR liabilities, GL entries)"),
            ("Inventory & Movements:", "MATDOC / MSEG, MARC, MARD (Real-time stock, movement types 101, 541, 551)"),
            ("Production & Costing:", "AFKO, AFPO, AFRU, RESB, AUFM, CKIS, KEPH (Work orders, confirmations, standard BOM)"),
            ("Purchasing & Logistics:", "EKKO, EKPO, EKET, EKKN, VBAK, VBAP, LIKP, LIPS (PO lines, sales schedule lines)"),
            ("Quality & Subcontracting:", "QALS, QMEL, Special Stock 'O' (Inspection lots, defects, vendor balances)")
        ], SAP_BLUE),
        ("LAYER 2: SAP HANA CALCULATION VIEWS", "In-Memory Engine & Push-Down Logic", [
            ("Star-Join Architecture:", "High-speed dimensional joins between facts and master data without Cartesian drag."),
            ("Recursive BOM Procedures:", "In-engine recursive traversal of 6-10 level indented BOM hierarchies in milliseconds."),
            ("Workload Management (WLM):", "Resource-group bounding ensuring zero CPU starvation for transactional users."),
            ("Material Movement Unions:", "Partition-aware projection filters consolidating production and inventory movements."),
            ("Data Pruning & Optimization:", "Push-down SQL hints and temporal windows reducing query load by 85%.")
        ], CYAN_ACCENT),
        ("LAYER 3: POWER BI EXECUTIVE COCKPIT", "DirectQuery / Dual-Storage Semantic Layer", [
            ("DirectQuery Connectivity:", "Direct sub-second query execution against HANA DB Server layer (ODBC/HDB)."),
            ("Advanced DAX Calculations:", "Dynamic Net Liquidity Runway, Contract LD Exposure, COPQ Leakage, WIP Aging."),
            ("Executive UI/UX Design:", "Board-ready dark/light themes, executive summary KPI cards, and drill-throughs."),
            ("Row-Level Security (RLS):", "Role-based authorization mirroring SAP user profiles across plants and functions."),
            ("On-Premise Gateway Clustering:", "High-availability gateway cluster ensuring seamless, secure data traversal.")
        ], EMERALD_GREEN)
    ]
    
    col_w = 3.75
    spacing_c = 0.24
    for idx, (title, sub, items, border_c) in enumerate(arch_cols):
        c_left = 0.8 + idx * (col_w + spacing_c)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(col_w), Inches(5.1))
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
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = border_c
        
        p_sub = tf_c.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(8.5)
        p_sub.font.italic = True
        p_sub.font.color.rgb = TEXT_LIGHT_MUTED
        p_sub.space_after = Pt(12)
        
        for item_h, item_d in items:
            p_it = tf_c.add_paragraph()
            p_it.space_after = Pt(6)
            r1 = p_it.add_run()
            r1.text = "• " + item_h + " "
            r1.font.bold = True
            r1.font.size = Pt(8.5)
            r1.font.color.rgb = TEXT_LIGHT
            r2 = p_it.add_run()
            r2.text = item_d
            r2.font.bold = False
            r2.font.size = Pt(8.2)
            r2.font.color.rgb = TEXT_LIGHT_MUTED

    add_footer(s3, 3, is_dark=True)

    # =============================================================
    # SLIDE 4: Cockpit 1 - Executive Cash Flow & Operational Fulfillment
    # =============================================================
    s4 = add_base_slide(is_dark=False)
    add_header(s4, "Cockpit 1: Executive Cash Flow & Operational Fulfillment", "EXECUTIVE DASHBOARD 1 | DAILY - WEEKLY - MONTHLY", "Synchronizing Customer SLAs, Inbound Supply, Supplier Payables, and Predictive Liquidity Runway")
    
    core_cards_s4 = [
        ("Scheduled Shipments & Pipeline", [
            ("Committed vs. Actual Dispatch:", "Track sales line delivery dates vs. current shipping status."),
            ("OTIF Performance:", "On-Time In-Full metrics segmented by customer program and division."),
            ("Revenue Pipeline:", "Confirmed orders ready for invoicing across daily and weekly horizons.")
        ]),
        ("Expected Inbound Raw Materials", [
            ("Open Vendor PO Lines:", "Scheduled dock deliveries cross-referenced with vendor commitments."),
            ("In-Transit ASN Visibility:", "Early notice of incoming raw materials to stage receiving bays."),
            ("Supply Reliability Score:", "Vendor delivery date adherence tracking to isolate unreliable suppliers.")
        ]),
        ("Supplier Payments Due (AP)", [
            ("AP Liability Aging:", "Payables grouped into 30/60/90-day buckets based on credit terms."),
            ("Cash Discount Capture:", "Identification of early-settlement discounts to optimize treasury outflow."),
            ("Critical Vendor Exposure:", "Payables prioritization for single-source aerospace suppliers.")
        ]),
        ("Customer Payments Incoming (AR)", [
            ("AR Collection Aging:", "Open receivables tracking by customer tier and defense agency."),
            ("Milestone Billing Realization:", "Unbilled milestone tracking tied to engineering and FAT sign-offs."),
            ("DSO Optimization:", "Real-time Days Sales Outstanding telemetry to accelerate collections.")
        ])
    ]
    
    top_c = 1.6
    w_c = 5.75
    h_c = 2.0
    for idx, (title, bullets) in enumerate(core_cards_s4):
        r_idx = idx // 2
        c_idx = idx % 2
        left_pos = 0.8 + c_idx * (w_c + 0.233)
        top_pos = top_c + r_idx * (h_c + 0.15)
        
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(top_pos), Inches(w_c), Inches(h_c))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.2)
        
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.18)
        tf_c.margin_top = Inches(0.12)
        
        p = tf_c.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = SAP_BLUE
        p.space_after = Pt(4)
        
        for b_title, b_desc in bullets:
            p_b = tf_c.add_paragraph()
            p_b.space_after = Pt(3)
            r1 = p_b.add_run()
            r1.text = "• " + b_title + " "
            r1.font.bold = True
            r1.font.size = Pt(8.5)
            r1.font.color.rgb = TEXT_DARK
            r2 = p_b.add_run()
            r2.text = b_desc
            r2.font.bold = False
            r2.font.size = Pt(8.2)
            r2.font.color.rgb = TEXT_MUTED

    enh_banner_s4 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.95), Inches(11.733), Inches(0.95))
    enh_banner_s4.fill.solid()
    enh_banner_s4.fill.fore_color.rgb = GOLD_LIGHT_BG
    enh_banner_s4.line.color.rgb = GOLD_ACCENT
    enh_banner_s4.line.width = Pt(1.2)
    
    tf_eb = enh_banner_s4.text_frame
    tf_eb.word_wrap = True
    tf_eb.margin_left = tf_eb.margin_right = Inches(0.2)
    tf_eb.margin_top = Inches(0.1)
    
    p = tf_eb.paragraphs[0]
    p.text = "STRATEGIC ENHANCEMENTS BY LUMBINI ELITE:"
    p.font.name = "Arial"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    p.space_after = Pt(2)
    
    p_desc = tf_eb.add_paragraph()
    r1 = p_desc.add_run()
    r1.text = "1. Net Liquidity Runway Simulator: "
    r1.font.bold = True
    r1.font.size = Pt(8.5)
    r1.font.color.rgb = TEXT_DARK
    r2 = p_desc.add_run()
    r2.text = "Predictive cash flow modeling simulating AR inflow vs. AP outflow under 30/60/90-day stress scenarios to protect bank covenants.  |  "
    r2.font.size = Pt(8.2)
    r2.font.color.rgb = TEXT_DARK
    
    r3 = p_desc.add_run()
    r3.text = "2. Late Delivery Risk & Liquidated Damages (LD) Tracker: "
    r3.font.bold = True
    r3.font.size = Pt(8.5)
    r3.font.color.rgb = TEXT_DARK
    r4 = p_desc.add_run()
    r4.text = "Algorithmic penalty calculation correlating routing delays with defense contract penalty clauses, protecting 1–3% of top-line revenue."
    r4.font.size = Pt(8.2)
    r4.font.color.rgb = TEXT_DARK

    add_footer(s4, 4, is_dark=False)

    # =============================================================
    # SLIDE 5: Cockpit 2 - Procurement & Subcontracting 52-Week Pipeline
    # =============================================================
    s5 = add_base_slide(is_dark=False)
    add_header(s5, "Cockpit 2: Procurement & Subcontracting 52-Week Pipeline", "EXECUTIVE DASHBOARD 2 | ROLLING 52-WEEK VIEW", "Forward Sourcing Visibility, Component-to-Part Traceability, and Subcontractor Special Stock Control")
    
    core_cards_s5 = [
        ("Scheduled vs. Confirmed PO Releases", [
            ("52-Week Sourcing Pipeline:", "Continuous forward visibility comparing MRP requisition demand with actual PO releases."),
            ("Uncommitted Demand Identification:", "Highlighting open requirements lacking supplier contracts."),
            ("Purchase Budget Adherence:", "Monitoring committed capital against approved procurement budgets.")
        ]),
        ("Component-to-Part Traceability", [
            ("Parent-Child Lineage:", "Direct linkage mapping open purchase order line items to SFG and FG assemblies."),
            ("Customer Program Allocation:", "Visibility into which defense programs are impacted by specific delayed lines."),
            ("Engineering Revision Tracking:", "Verifying mil-spec component drawing revisions before PO issuance.")
        ]),
        ("Vendor Performance & Concentration", [
            ("Spend Concentration (HHI):", "Identifying dangerous single-source vendor vulnerabilities on critical commodities."),
            ("Quoted vs. Actual Lead Time:", "Tracking supplier lead-time drift across precision alloys and electronic parts."),
            ("Supplier On-Time Delivery:", "Objective scorecard to strengthen quarterly vendor negotiations.")
        ]),
        ("Subcontractor Job-Work Operations", [
            ("Special Stock 'O' Tracking:", "Full visibility into material issued to external vendors (541/542 movements)."),
            ("Aging of Material with Vendors:", "Highlighting raw materials held at job-workers beyond acceptable cycle times."),
            ("Outside Processing Balance:", "Real-time valuation of inventory residing outside plant premises.")
        ])
    ]
    
    for idx, (title, bullets) in enumerate(core_cards_s5):
        r_idx = idx // 2
        c_idx = idx % 2
        left_pos = 0.8 + c_idx * (w_c + 0.233)
        top_pos = top_c + r_idx * (h_c + 0.15)
        
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(top_pos), Inches(w_c), Inches(h_c))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.2)
        
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.18)
        tf_c.margin_top = Inches(0.12)
        
        p = tf_c.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
        p.space_after = Pt(4)
        
        for b_title, b_desc in bullets:
            p_b = tf_c.add_paragraph()
            p_b.space_after = Pt(3)
            r1 = p_b.add_run()
            r1.text = "• " + b_title + " "
            r1.font.bold = True
            r1.font.size = Pt(8.5)
            r1.font.color.rgb = TEXT_DARK
            r2 = p_b.add_run()
            r2.text = b_desc
            r2.font.bold = False
            r2.font.size = Pt(8.2)
            r2.font.color.rgb = TEXT_MUTED

    enh_banner_s5 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.95), Inches(11.733), Inches(0.95))
    enh_banner_s5.fill.solid()
    enh_banner_s5.fill.fore_color.rgb = GREEN_LIGHT_BG
    enh_banner_s5.line.color.rgb = EMERALD_GREEN
    enh_banner_s5.line.width = Pt(1.2)
    
    tf_eb5 = enh_banner_s5.text_frame
    tf_eb5.word_wrap = True
    tf_eb5.margin_left = tf_eb5.margin_right = Inches(0.2)
    tf_eb5.margin_top = Inches(0.1)
    
    p = tf_eb5.paragraphs[0]
    p.text = "STRATEGIC ENHANCEMENTS BY LUMBINI ELITE:"
    p.font.name = "Arial"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = EMERALD_GREEN
    p.space_after = Pt(2)
    
    p_desc = tf_eb5.add_paragraph()
    r1 = p_desc.add_run()
    r1.text = "1. Subcontractor TAT & Stage Yield/Scrap Tracker: "
    r1.font.bold = True
    r1.font.size = Pt(8.5)
    r1.font.color.rgb = TEXT_DARK
    r2 = p_desc.add_run()
    r2.text = "Monitors exact turnaround cycle times and scrap/yield discrepancies across external processors, recovering lost material.  |  "
    r2.font.size = Pt(8.2)
    r2.font.color.rgb = TEXT_DARK
    
    r3 = p_desc.add_run()
    r3.text = "2. Critical Path Component Shortage Predictor: "
    r3.font.bold = True
    r3.font.size = Pt(8.5)
    r3.font.color.rgb = TEXT_DARK
    r4 = p_desc.add_run()
    r4.text = "Predictive heuristic flagging components with Lead Time > 16 weeks where projected stock breaches safety levels, warning buyers 60–90 days ahead."
    r4.font.size = Pt(8.2)
    r4.font.color.rgb = TEXT_DARK

    add_footer(s5, 5, is_dark=False)

    # =============================================================
    # SLIDE 6: Cockpit 3 - Manufacturing Operations & Batch Cost Intelligence
    # =============================================================
    s6 = add_base_slide(is_dark=False)
    add_header(s6, "Cockpit 3: Manufacturing Operations & Batch Cost Intelligence", "EXECUTIVE DASHBOARD 3 | SHIFT & BATCH COSTING", "MRP Readiness, Real-Time Batch Cost Variances, Work-in-Progress (WIP) Aging, and COPQ")
    
    core_cards_s6 = [
        ("MRP Readiness & Kitting Operations", [
            ("Pre-Release Kitting Checks:", "Verification of 100% component availability prior to releasing production orders."),
            ("Short-Supply Alerts:", "Instant notification of missing hardware or fasteners to halt premature staging."),
            ("Staging Bay Velocity:", "Tracking kit movement from raw stock picking to work-center delivery.")
        ]),
        ("Batch Costing Variance Engine", [
            ("Material Actual vs. Standard:", "Real-time detection of component substitution or excessive material consumption."),
            ("Machine & Labor Hour Variances:", "Comparison of confirmed operation hours (AFRU) against standard routing."),
            ("Job-Order Profitability:", "Live gross margin calculation per batch before goods receipt to finished stock.")
        ]),
        ("Cross-Functional Decision Engine", [
            ("Work-Center Utilization:", "Overall Equipment Effectiveness (OEE) and capacity loading on critical CNC machines."),
            ("Line Throughput Velocity:", "Cycle time tracking across winding, machining, assembly, and testing bays."),
            ("Capacity Bottleneck Isolation:", "Early warning when station queues exceed rated capacity limits.")
        ]),
        ("Shift Performance & Operations Control", [
            ("Operator & Shift Efficiency:", "Hourly confirmation output tracking across production shifts."),
            ("Setup vs. Run Time Ratios:", "Highlighting excessive machine setup and changeover times."),
            ("Dispatch Readiness:", "Finished batch certification status for final QA and shipping handover.")
        ])
    ]
    
    for idx, (title, bullets) in enumerate(core_cards_s6):
        r_idx = idx // 2
        c_idx = idx % 2
        left_pos = 0.8 + c_idx * (w_c + 0.233)
        top_pos = top_c + r_idx * (h_c + 0.15)
        
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(top_pos), Inches(w_c), Inches(h_c))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.2)
        
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.18)
        tf_c.margin_top = Inches(0.12)
        
        p = tf_c.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = PURPLE_ACCENT
        p.space_after = Pt(4)
        
        for b_title, b_desc in bullets:
            p_b = tf_c.add_paragraph()
            p_b.space_after = Pt(3)
            r1 = p_b.add_run()
            r1.text = "• " + b_title + " "
            r1.font.bold = True
            r1.font.size = Pt(8.5)
            r1.font.color.rgb = TEXT_DARK
            r2 = p_b.add_run()
            r2.text = b_desc
            r2.font.bold = False
            r2.font.size = Pt(8.2)
            r2.font.color.rgb = TEXT_MUTED

    enh_banner_s6 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.95), Inches(11.733), Inches(0.95))
    enh_banner_s6.fill.solid()
    enh_banner_s6.fill.fore_color.rgb = PURPLE_LIGHT_BG
    enh_banner_s6.line.color.rgb = PURPLE_ACCENT
    enh_banner_s6.line.width = Pt(1.2)
    
    tf_eb6 = enh_banner_s6.text_frame
    tf_eb6.word_wrap = True
    tf_eb6.margin_left = tf_eb6.margin_right = Inches(0.2)
    tf_eb6.margin_top = Inches(0.1)
    
    p = tf_eb6.paragraphs[0]
    p.text = "STRATEGIC ENHANCEMENTS BY LUMBINI ELITE:"
    p.font.name = "Arial"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = PURPLE_ACCENT
    p.space_after = Pt(2)
    
    p_desc = tf_eb6.add_paragraph()
    r1 = p_desc.add_run()
    r1.text = "1. Cost of Poor Quality (COPQ) & Scrap Leakage Engine: "
    r1.font.bold = True
    r1.font.size = Pt(8.5)
    r1.font.color.rgb = TEXT_DARK
    r2 = p_desc.add_run()
    r2.text = "Drills down scrap costs (551/552) to work centers, tool sets, and shifts, identifying root causes to preserve 2-4% gross margin.  |  "
    r2.font.size = Pt(8.2)
    r2.font.color.rgb = TEXT_DARK
    
    r3 = p_desc.add_run()
    r3.text = "2. WIP Valuation & In-Process Ageing Matrix: "
    r3.font.bold = True
    r3.font.size = Pt(8.5)
    r3.font.color.rgb = TEXT_DARK
    r4 = p_desc.add_run()
    r4.text = "Real-time valuation of semi-finished stock categorized by dwelling age (<15, 16-30, 31-60, >60 days), releasing trapped working capital."
    r4.font.size = Pt(8.2)
    r4.font.color.rgb = TEXT_DARK

    add_footer(s6, 6, is_dark=False)

    # =============================================================
    # SLIDE 7: Cockpit Report Inventory & Deliverable Count (Light)
    # =============================================================
    s7 = add_base_slide(is_dark=False)
    add_header(s7, "Cockpit Report Inventory: Itemized Deliverables by Cockpit", "DELIVERABLE MANIFEST | 18 TOTAL EXECUTIVE REPORTS", "Itemized Architecture: Exactly 6 Dedicated Production Reports Per Cockpit Across Finance, Sourcing, and Manufacturing")
    
    # 4 Quick Metric Summary Badges (Top Row)
    kpis_s7 = [
        ("TOTAL COCKPIT SUITES", "3 Executive Suites", SAP_BLUE, RGBColor(238, 242, 255)),
        ("TOTAL DELIVERABLE REPORTS", "18 Production Reports", GOLD_ACCENT, GOLD_LIGHT_BG),
        ("REPORTS PER COCKPIT", "6 Reports Each (4 Core + 2 Strategic)", EMERALD_GREEN, GREEN_LIGHT_BG),
        ("UNIT COMMERCIAL ALIGNMENT", "~₹1.67L / Report (₹10.0L / Suite)", PURPLE_ACCENT, PURPLE_LIGHT_BG),
    ]
    
    kpi_w7 = 2.75
    kpi_gap7 = 0.244
    for i, (k_lbl, k_val, k_clr, k_bg) in enumerate(kpis_s7):
        k_left = 0.8 + i * (kpi_w7 + kpi_gap7)
        card_k = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(k_left), Inches(1.36), Inches(kpi_w7), Inches(0.56))
        card_k.fill.solid()
        card_k.fill.fore_color.rgb = k_bg
        card_k.line.color.rgb = k_clr
        card_k.line.width = Pt(1)
        tf_k = card_k.text_frame
        tf_k.word_wrap = True
        tf_k.margin_left = tf_k.margin_right = Inches(0.12)
        tf_k.margin_top = Inches(0.04)
        
        p1 = tf_k.paragraphs[0]
        p1.text = k_lbl
        p1.font.name = "Arial"
        p1.font.size = Pt(7.2)
        p1.font.bold = True
        p1.font.color.rgb = k_clr
        
        p2 = tf_k.add_paragraph()
        p2.text = k_val
        p2.font.name = "Arial"
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_DARK

    # 3 Main Cockpit Columns (6 Reports each)
    cockpits_catalog = [
        {
            "header": "COCKPIT 1: CASH FLOW & FULFILLMENT",
            "badge": "6 Dedicated Reports (4 Core + 2 Strategic) | Finance & SCM",
            "border": SAP_BLUE,
            "header_bg": RGBColor(238, 245, 255),
            "reports": [
                ("1.1 Scheduled Shipments & Dispatch Pipeline", "Line-item tracking of customer orders vs. dispatch dates, OTIF %, and backlog velocity."),
                ("1.2 Expected Inbound Materials & Bay Staging", "Open vendor PO lines, in-transit ASN visibility, and dock arrival staging readiness."),
                ("1.3 Supplier Payables (AP Due) & Liability Aging", "Payables aging (30/60/90 days), cash discount capture, and vendor credit exposure."),
                ("1.4 Customer Receivables (AR Due) & Cash Realization", "Open AR aging, customer tier DSO optimization, and unbilled defense milestone claims."),
                ("1.5 [Strategic] Net Liquidity Runway Simulator", "Multi-scenario cash burn forecasting (AR vs. AP) under 30/60/90-day stress to safeguard covenants."),
                ("1.6 [Strategic] Late Delivery Risk & LD Penalty Tracker", "Algorithmic penalty scoring correlating routing delays with contract LD clauses (protecting 1–3% margin).")
            ]
        },
        {
            "header": "COCKPIT 2: PROCUREMENT 52-WEEK PIPELINE",
            "badge": "6 Dedicated Reports (4 Core + 2 Strategic) | Sourcing & Job-Work",
            "border": CYAN_ACCENT,
            "header_bg": RGBColor(235, 251, 255),
            "reports": [
                ("2.1 52-Week Sourcing Pipeline & PO Releases", "Forward rolling demand vs. confirmed POs, uncommitted PR gaps, and purchase budget adherence."),
                ("2.2 Component-to-Part Traceability & Program Lineage", "Multi-tier BOM lineage mapping open PO lines directly to SFG/FG and end-customer defense programs."),
                ("2.3 Vendor Concentration & Lead-Time Volatility", "Herfindahl spend concentration (HHI), quoted vs. actual lead-time drift, and supplier scorecards."),
                ("2.4 Subcontractor Job-Work & Special Stock 'O'", "Materials issued to platers/heattreaters (541/542), vendor possession aging, outside processing valuation."),
                ("2.5 [Strategic] Subcontractor TAT & Stage Yield/Scrap", "Outside cycle times (TAT) and stage yield loss at external job-workers to stop untracked material bleed."),
                ("2.6 [Strategic] Critical Path Component Shortage Predictor", "Predictive heuristic flagging items with lead times >16 wks before buffer stock breaches safety thresholds.")
            ]
        },
        {
            "header": "COCKPIT 3: MANUFACTURING & BATCH COSTING",
            "badge": "6 Dedicated Reports (4 Core + 2 Strategic) | Operations & Quality",
            "border": PURPLE_ACCENT,
            "header_bg": RGBColor(248, 244, 255),
            "reports": [
                ("3.1 Pre-Release MRP Kitting Readiness Gate", "Automated 100% component availability validation prior to releasing production orders (RESB/AFPO)."),
                ("3.2 Batch Costing Variance Engine (Actual vs. Std BOM)", "Material price/usage variance, confirmed machine/labor hours (AFRU) vs. standard routing."),
                ("3.3 Work-Center Utilization (OEE) & Line Throughput", "CNC machine capacity loading, queue bottleneck telemetry across winding, machining, and testing."),
                ("3.4 Shift Operations & Daily Floor Telemetry", "Hourly operator confirmation velocity, machine setup vs. run ratios, and QA dispatch readiness."),
                ("3.5 [Strategic] Cost of Poor Quality (COPQ) Scrap Leakage", "Inspection defect logging (551/552) attributed to work centers, tool sets, and shifts (2–4% margin recovery)."),
                ("3.6 [Strategic] WIP Valuation & In-Process Ageing Matrix", "Financial valuation of stalled semi-finished stock categorized by dwelling age (<15, 16–30, 31–60, >60 days).")
            ]
        }
    ]

    col_w7 = 3.75
    col_gap7 = 0.24
    col_top7 = 2.02
    col_h7 = 4.45

    for c_idx, data in enumerate(cockpits_catalog):
        c_left = 0.8 + c_idx * (col_w7 + col_gap7)
        
        # Outer Card Container
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(col_top7), Inches(col_w7), Inches(col_h7))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = data["border"]
        card.line.width = Pt(1.5)
        
        # Header banner inside column
        hb = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left + 0.06), Inches(col_top7 + 0.06), Inches(col_w7 - 0.12), Inches(0.52))
        hb.fill.solid()
        hb.fill.fore_color.rgb = data["header_bg"]
        hb.line.color.rgb = data["border"]
        hb.line.width = Pt(1)
        tf_hb = hb.text_frame
        tf_hb.word_wrap = True
        tf_hb.margin_left = tf_hb.margin_right = Inches(0.06)
        tf_hb.margin_top = Inches(0.03)
        
        p_h1 = tf_hb.paragraphs[0]
        p_h1.text = data["header"]
        p_h1.font.name = "Arial"
        p_h1.font.size = Pt(8.2)
        p_h1.font.bold = True
        p_h1.font.color.rgb = data["border"]
        
        p_h2 = tf_hb.add_paragraph()
        p_h2.text = data["badge"]
        p_h2.font.name = "Arial"
        p_h2.font.size = Pt(7.0)
        p_h2.font.bold = True
        p_h2.font.color.rgb = TEXT_DARK

        # Report Items Box
        rep_box = s7.shapes.add_textbox(Inches(c_left + 0.05), Inches(col_top7 + 0.64), Inches(col_w7 - 0.10), Inches(3.80))
        tf_rep = rep_box.text_frame
        tf_rep.word_wrap = True
        tf_rep.margin_left = tf_rep.margin_right = tf_rep.margin_top = tf_rep.margin_bottom = 0

        for r_num, (r_name, r_desc) in enumerate(data["reports"]):
            p_r = tf_rep.paragraphs[0] if r_num == 0 else tf_rep.add_paragraph()
            p_r.space_before = Pt(3) if r_num > 0 else Pt(0)
            p_r.space_after = Pt(2)
            
            is_strat = "[Strategic]" in r_name
            
            run_title = p_r.add_run()
            run_title.text = "• " + r_name + "\n"
            run_title.font.name = "Arial"
            run_title.font.size = Pt(7.3)
            run_title.font.bold = True
            run_title.font.color.rgb = data["border"] if not is_strat else GOLD_ACCENT
            
            run_desc = p_r.add_run()
            run_desc.text = "   " + r_desc
            run_desc.font.name = "Arial"
            run_desc.font.size = Pt(6.8)
            run_desc.font.bold = False
            run_desc.font.color.rgb = TEXT_MUTED if not is_strat else TEXT_DARK

    # Bottom Architecture & SLA Guarantee Banner
    banner_b7 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.56), Inches(11.733), Inches(0.38))
    banner_b7.fill.solid()
    banner_b7.fill.fore_color.rgb = RGBColor(241, 245, 249)
    banner_b7.line.color.rgb = SAP_BLUE
    banner_b7.line.width = Pt(1)
    
    tf_bb7 = banner_b7.text_frame
    tf_bb7.word_wrap = True
    tf_bb7.margin_left = tf_bb7.margin_right = Inches(0.15)
    tf_bb7.margin_top = Inches(0.04)
    p_bb7 = tf_bb7.paragraphs[0]
    
    r_b1 = p_bb7.add_run()
    r_b1.text = "COMPLETE 4-LAYER TURNKEY STACK PER REPORT: "
    r_b1.font.bold = True
    r_b1.font.size = Pt(7.5)
    r_b1.font.color.rgb = SAP_BLUE
    
    r_b2 = p_bb7.add_run()
    r_b2.text = "All 18 reports include: ① SAP HANA Push-Down Calculation Views  |  ② Power BI DirectQuery Interactive Semantic Models  |  ③ ACDOCA / MATDOC GL Reconciliation  |  ④ Dynamic Role-Based Security (RLS) & UAT Sign-Off"
    r_b2.font.bold = False
    r_b2.font.size = Pt(7.2)
    r_b2.font.color.rgb = TEXT_DARK

    add_footer(s7, 7, is_dark=False)

    # =============================================================
    # SLIDE 8: The 5 W's Strategic Evaluation Matrix
    # =============================================================
    s8 = add_base_slide(is_dark=False)
    add_header(s8, "The 5 W’s Strategic Evaluation Matrix", "GOVERNANCE & IMPACT MATRIX", "Mapping Organizational Personas, Data Entities, Cadences, and P&L/EBITDA Drivers across Cockpits")
    
    rows = 4
    cols = 6
    tbl_shape = s8.shapes.add_table(rows, cols, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1))
    tbl = tbl_shape.table
    
    tbl.columns[0].width = Inches(1.8)
    tbl.columns[1].width = Inches(1.8)
    tbl.columns[2].width = Inches(2.5)
    tbl.columns[3].width = Inches(1.6)
    tbl.columns[4].width = Inches(2.0)
    tbl.columns[5].width = Inches(2.033)
    
    headers = ["COCKPIT / MODULE", "WHO (Personas)", "WHAT (Core Metrics & Scope)", "WHEN (Cadence)", "WHERE (S/4HANA Tables)", "WHY (EBITDA & Cash Impact)"]
    for c_idx, h_text in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_CARD
        tf_c = cell.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.08)
        p = tf_c.paragraphs[0]
        p.text = h_text
        p.font.name = "Arial"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
    
    matrix_rows = [
        ("Dashboard 1: Cash Flow & Fulfillment",
         "CFO, VP Finance, Commercial Director, CEO",
         "Scheduled dispatches vs. SLAs, Inbound materials, AP/AR aging, Liquidity Runway simulation, LD penalty exposure.",
         "Daily 06:00 AM & Intraday on-demand before bank clearing runs.",
         "ACDOCA, BSID, BSIK, VBAK, VBAP, LIKP, LIPS.\nDirectQuery View.",
         "Accelerates Free Cash Flow; captures cash discounts; eliminates 1-3% revenue loss from liquidated damages."),
        ("Dashboard 2: 52-Week Sourcing Pipeline",
         "CPO, VP Supply Chain, Lead Commodity Buyers",
         "52-week PO releases vs. demand, Component-to-part traceability, Vendor concentration, Subcontractor TAT/Yield, Shortage predictor.",
         "Daily morning refresh; Weekly rolling 52-week planning cycle.",
         "EKKO, EKPO, EKET, EKKN, EBAN, LFA1, MSEG (541/542).\nStar-Join Cube.",
         "Prevents spot freight premiums; mitigates single-source supplier risks; recovers lost job-work material."),
        ("Dashboard 3: Manufacturing & Batch Cost",
         "COO, VP Operations, Plant Directors, Cost Controller",
         "Full-kitting readiness %, Batch actual vs. standard cost variance, Line utilization (OEE), COPQ scrap drill-down, WIP aging.",
         "Shift-wise (3x daily) for kitting; Daily for batch cost & scrap review.",
         "AFKO, AFPO, AFRU, RESB, AUFM, CKIS, KEPH, QALS.\nIn-memory Cube.",
         "Releases 10-18% trapped WIP; prevents missing-part line halts; recovers 2-4% gross margin leakage from scrap.")
    ]
    
    for r_idx, row_data in enumerate(matrix_rows, start=1):
        for c_idx, val in enumerate(row_data):
            cell = tbl.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if r_idx % 2 == 1 else CARD_BG_MUTED
            tf_c = cell.text_frame
            tf_c.word_wrap = True
            tf_c.margin_left = tf_c.margin_right = Inches(0.08)
            p = tf_c.paragraphs[0]
            p.text = val
            p.font.name = "Arial"
            p.font.size = Pt(8)
            p.font.color.rgb = TEXT_DARK
            if c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = SAP_BLUE

    add_footer(s8, 8, is_dark=False)

    # =============================================================
    # SLIDE 9: Technical Complexity & Engineering Justification (Dark)
    # =============================================================
    s9 = add_base_slide(is_dark=True)
    add_header(s9, "Deep Database Internals: The Engineering Rigor Behind the Value", "TECHNICAL JUSTIFICATION", "Establishing why enterprise-grade S/4HANA analytics demands specialized database in-memory engineering", is_dark=True)
    
    tech_cards = [
        ("In-Memory Star-Joins & Recursive BOMs", [
            ("Multi-Tier BOM Traversal:", "Hical's electromechanical assemblies feature 6-10 level indented BOMs. Recursive calculation views process parent-child links in milliseconds, avoiding memory overflow."),
            ("Cartesian Elimination:", "Joining material movements (MATDOC/MSEG/AUFM) with confirmations (AFRU) creates millions of records. Push-down projection filters isolate relevant subsets prior to joining."),
            ("Columnar Store Pruning:", "Leveraging SAP HANA's columnar dictionary and partition pruning to achieve sub-second execution across dense manufacturing tables.")
        ], SAP_BLUE),
        ("S/4HANA Production Safety & Isolation", [
            ("Zero OLTP Degradation:", "Analytical queries generated by Power BI must never cause row locks, table locks, or CPU starvation for live transactional users on the factory floor."),
            ("Workload Management (WLM):", "Configuring dedicated HANA DB user classes and resource limits to cap memory allocation and thread execution for analytics."),
            ("Dual-Mode Aggregations:", "Power BI composite models cache summarized metrics in memory while routing granular drill-through queries via DirectQuery only when filtered.")
        ], CYAN_ACCENT),
        ("Audit-Grade Financial & Operational Harmony", [
            ("The 'Two-Book' Problem:", "Factory floor logs frequently diverge from financial ledgers due to timing delays, scrap accruals, and manual journal postings."),
            ("Harmonization with ACDOCA:", "Every rupee reported in cash flow, inventory valuation, and batch costing is programmatically reconciled against the Universal Journal (ACDOCA)."),
            ("Subledger Alignment:", "Automated cross-checking between vendor balances (BSIK), customer receivables (BSID), and costing sheets (CKIS/KEPH) guarantees audit sign-off.")
        ], GOLD_ACCENT)
    ]
    
    col_w9 = 3.75
    spacing_c9 = 0.24
    for idx, (title, points, border_c) in enumerate(tech_cards):
        c_left = 0.8 + idx * (col_w9 + spacing_c9)
        card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(col_w9), Inches(5.1))
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
        p.space_after = Pt(12)
        
        for pt_head, pt_body in points:
            p_pt = tf_c.add_paragraph()
            p_pt.space_after = Pt(8)
            r1 = p_pt.add_run()
            r1.text = "• " + pt_head + " "
            r1.font.bold = True
            r1.font.size = Pt(8.5)
            r1.font.color.rgb = TEXT_LIGHT
            r2 = p_pt.add_run()
            r2.text = pt_body
            r2.font.bold = False
            r2.font.size = Pt(8.2)
            r2.font.color.rgb = TEXT_LIGHT_MUTED

    add_footer(s9, 9, is_dark=True)

    # =============================================================
    # SLIDE 10: 10-Week Agile Implementation Roadmap & Governance
    # =============================================================
    s10 = add_base_slide(is_dark=False)
    add_header(s10, "10-Week Agile Implementation Roadmap & Governance", "PROJECT TIMELINE & PHASING", "Disciplined 5-phase delivery framework ensuring rapid time-to-value, rigorous validation, and zero production risk")
    
    phases_s10 = [
        ("PHASE 1: BLUEPRINT", "Weeks 1–2", [
            ("KPI Workshops:", "Alignment with CFO, COO, CPO & Plant Heads on formulas."),
            ("Calculation Blueprint:", "Documenting field-level logic and transformation rules."),
            ("Environment Verification:", "HANA DB user permissions & Power BI gateway checks.")
        ], "Gate 1: Metric Blueprint Sign-Off (25% Milestone)", SAP_BLUE),
        ("PHASE 2: HANA VIEWS", "Weeks 3–5", [
            ("Star-Join Modeling:", "Building Calculation Views in SAP HANA Studio/Web IDE."),
            ("Recursive BOM Logic:", "Implementing multi-level indented BOM SQLScript logic."),
            ("WLM & Performance:", "Workload management configuration and query tuning.")
        ], "Gate 2: Calculation Views Validated (35% Milestone)", CYAN_ACCENT),
        ("PHASE 3: POWER BI MODELING", "Weeks 5–7", [
            ("Semantic Model Design:", "Building DirectQuery/dual-mode relationships in Power BI."),
            ("Advanced DAX Layer:", "Implementing Liquidity Runway, LD risk, and COPQ logic."),
            ("Executive UI/UX Design:", "Crafting intuitive, board-ready dark/light interfaces.")
        ], "Review: Interactive Alpha/Beta Dashboard Walkthrough", PURPLE_ACCENT),
        ("PHASE 4: RECONCILIATION & UAT", "Weeks 7–8", [
            ("Financial Reconciliation:", "3-way tie-out between shop floor (MSEG) and GL (ACDOCA)."),
            ("User Acceptance Testing:", "Rigorous validation with Finance & Operations teams."),
            ("Concurrency Stress Test:", "Validating sub-second response times under peak load.")
        ], "Gate 3: Formal Business UAT Sign-Off (25% Milestone)", AMBER_WARN),
        ("PHASE 5: CUTOVER & GO-LIVE", "Weeks 9–10", [
            ("Gateway Deployment:", "Publishing semantic models to Power BI Service."),
            ("Security & RLS Rollout:", "Dynamic role-based security mapped to SAP authorizations."),
            ("CXO Handover & Training:", "Executive enablement workshops, SOPs, and project closure.")
        ], "Gate 4: Production Go-Live & Handover (15% Milestone)", EMERALD_GREEN)
    ]
    
    p_w10 = 2.15
    p_spacing10 = 0.2
    for idx, (p_title, p_time, p_tasks, p_gate, p_clr) in enumerate(phases_s10):
        p_left = 0.8 + idx * (p_w10 + p_spacing10)
        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(p_left), Inches(1.6), Inches(p_w10), Inches(5.1))
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

    add_footer(s10, 10, is_dark=False)

    # =============================================================
    # SLIDE 11: Sequential Cockpit Commercial Framework & Sprint Rollout (Dark)
    # =============================================================
    s11 = add_base_slide(is_dark=True)
    add_header(s11, "Sequential Cockpit Commercial Framework & Sprint Rollout", "AGILE SPRINT DELIVERY | ₹10,00,000 PER COCKPIT SUITE", "Developing One Cockpit After Another — and Within Each Cockpit, One Report After Another", is_dark=True)
    
    sequential_cards = [
        ("SPRINT 1: COCKPIT 1", "Cash Flow & Fulfillment (₹10.0L | W1–W4)", [
            ("Sequential Report Build:", "1. Scheduled Dispatches → 2. Inbound Logistics → 3. AP Liability Aging → 4. AR Collection Inflows."),
            ("Embedded Enhancements:", "Net Liquidity Runway Simulator + Late Delivery LD Penalty Tracker embedded on same screens."),
            ("Full SOW Layers Included:", "HANA Views (₹4.5L) + Power BI & DAX (₹3.5L) + Financial Reconciliation (₹1.2L) + UAT/RLS (₹0.8L)."),
            ("Sprint 1 Milestone Gate:", "Complete functional sign-off & production cutover of Cockpit 1 before Sprint 2 commences.")
        ], SAP_BLUE),
        ("SPRINT 2: COCKPIT 2", "52-Week Procurement Pipeline (₹10.0L | W4–W7)", [
            ("Sequential Report Build:", "1. Planned PO Releases → 2. Confirmed POs → 3. Part Traceability → 4. Vendor Load → 5. Subcontractor Special Stock 'O'."),
            ("Embedded Enhancements:", "Subcontractor TAT/Yield Loss Tracker + Critical Component Shortage Predictor."),
            ("Full SOW Layers Included:", "HANA Views (₹4.5L) + Power BI & DAX (₹3.5L) + PO Commitment Reconciliation (₹1.2L) + UAT/RLS (₹0.8L)."),
            ("Sprint 2 Milestone Gate:", "Complete procurement sign-off & production cutover of Cockpit 2 before Sprint 3 commences.")
        ], CYAN_ACCENT),
        ("SPRINT 3: COCKPIT 3", "Manufacturing & Batch Costing (₹10.0L | W7–W10)", [
            ("Sequential Report Build:", "1. MRP Kitting Readiness → 2. Batch Cost Actual vs. Standard → 3. Work-Center OEE & Line Throughput."),
            ("Embedded Enhancements:", "Cost of Poor Quality (COPQ) Scrap Leakage Engine + WIP Valuation & Ageing Matrix."),
            ("Full SOW Layers Included:", "HANA Recursive BOM Views (₹4.5L) + Power BI & DAX (₹3.5L) + Cost Reconciliation (₹1.2L) + UAT/RLS (₹0.8L)."),
            ("Sprint 3 Milestone Gate:", "Complete operations UAT sign-off, dynamic RLS rollout, executive training, and final handover.")
        ], PURPLE_ACCENT)
    ]
    
    col_w11 = 3.75
    spacing_c11 = 0.24
    for idx, (title, sub, items, border_c) in enumerate(sequential_cards):
        c_left = 0.8 + idx * (col_w11 + spacing_c11)
        card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.55), Inches(col_w11), Inches(4.35))
        card.fill.solid()
        card.fill.fore_color.rgb = DARK_CARD
        card.line.color.rgb = border_c
        card.line.width = Pt(1.5)
        
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.18)
        tf_c.margin_top = Inches(0.15)
        
        p = tf_c.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = border_c
        
        p_sub = tf_c.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(8.5)
        p_sub.font.bold = True
        p_sub.font.color.rgb = TEXT_LIGHT
        p_sub.space_after = Pt(8)
        
        for item_h, item_d in items:
            p_it = tf_c.add_paragraph()
            p_it.space_after = Pt(5)
            r1 = p_it.add_run()
            r1.text = item_h + " "
            r1.font.bold = True
            r1.font.size = Pt(8.2)
            r1.font.color.rgb = CYAN_ACCENT if border_c != CYAN_ACCENT else GOLD_ACCENT
            r2 = p_it.add_run()
            r2.text = item_d
            r2.font.bold = False
            r2.font.size = Pt(7.8)
            r2.font.color.rgb = TEXT_LIGHT_MUTED

    # Bottom Sequential Milestone Banner on Slide 11
    banner_s11 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.0), Inches(11.733), Inches(0.9))
    banner_s11.fill.solid()
    banner_s11.fill.fore_color.rgb = DARK_CARD
    banner_s11.line.color.rgb = GOLD_ACCENT
    banner_s11.line.width = Pt(1.2)
    
    tf_b11 = banner_s11.text_frame
    tf_b11.word_wrap = True
    tf_b11.margin_left = tf_b11.margin_right = Inches(0.2)
    tf_b11.margin_top = Inches(0.08)
    
    p = tf_b11.paragraphs[0]
    p.text = "SEQUENTIAL SPRINT DELIVERY & BILLING: ₹10,00,000 PER COCKPIT SUITE (₹30,00,000 TOTAL)"
    p.font.name = "Arial"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    p.space_after = Pt(2)
    
    p_desc = tf_b11.add_paragraph()
    r1 = p_desc.add_run()
    r1.text = "• Sprint 1 (Weeks 1–4): "
    r1.font.bold = True
    r1.font.size = Pt(8.2)
    r1.font.color.rgb = TEXT_LIGHT
    r1_d = p_desc.add_run()
    r1_d.text = "Cockpit 1 Delivered Report-by-Report → UAT & Live (₹10.0L)  |  "
    r1_d.font.size = Pt(8.0)
    r1_d.font.color.rgb = TEXT_LIGHT_MUTED
    
    r2 = p_desc.add_run()
    r2.text = "• Sprint 2 (Weeks 4–7): "
    r2.font.bold = True
    r2.font.size = Pt(8.2)
    r2.font.color.rgb = TEXT_LIGHT
    r2_d = p_desc.add_run()
    r2_d.text = "Cockpit 2 Delivered Report-by-Report → UAT & Live (₹10.0L)  |  "
    r2_d.font.size = Pt(8.0)
    r2_d.font.color.rgb = TEXT_LIGHT_MUTED
    
    r3 = p_desc.add_run()
    r3.text = "• Sprint 3 (Weeks 7–10): "
    r3.font.bold = True
    r3.font.size = Pt(8.2)
    r3.font.color.rgb = TEXT_LIGHT
    r3_d = p_desc.add_run()
    r3_d.text = "Cockpit 3 Delivered Report-by-Report → Final Handover (₹10.0L)"
    r3_d.font.size = Pt(8.0)
    r3_d.font.color.rgb = TEXT_LIGHT_MUTED

    p_subtranche = tf_b11.add_paragraph()
    p_subtranche.space_before = Pt(2)
    r_tr = p_subtranche.add_run()
    r_tr.text = "Sprint Milestone Tranches (per Cockpit): 25% Sprint Blueprint & Scope | 50% HANA Views & Reports Built | 25% Sprint UAT & Go-Live"
    r_tr.font.size = Pt(7.8)
    r_tr.font.italic = True
    r_tr.font.color.rgb = CYAN_ACCENT

    add_footer(s11, 11, is_dark=True)

    # =============================================================
    # SLIDE 12: Commercial Terms & Conditions (Light)
    # =============================================================
    s12 = add_base_slide(is_dark=False)
    add_header(s12, "Commercial Terms & Conditions of Engagement", "CONTRACTUAL GOVERNANCE", "Formal commercial, delivery, intellectual property, and warranty parameters")
    
    terms_cards = [
        ("1. Commercial Pricing & Taxes", [
            ("Proposal Validity:", "Commercial pricing of ₹10,00,000 INR per report (₹30,00,000 INR total) is valid for 30 calendar days from presentation."),
            ("Tax Treatment:", "All professional fees are quoted exclusive of statutory levies. Goods & Services Tax (GST @ 18%) applies extra on all invoices."),
            ("Fixed-Price Commitment:", "Turnkey professional services delivery guarantees zero billing escalation for the agreed scope of work."),
            ("Out-of-Pocket Expenses:", "Client visits within Bengaluru are included. Any specialized outstation travel, if requested, billed on actuals with prior approval.")
        ], SAP_BLUE),
        ("2. Milestone Invoicing & Payment Terms", [
            ("Invoicing Triggers:", "Invoices raised strictly upon written sign-off of defined milestone deliverables (Blueprint, Views, UAT, Go-Live)."),
            ("Credit Period:", "All approved milestone invoices payable within 15 business days from the date of formal electronic submission."),
            ("Independent Report Billing:", "Reports can progress and be invoiced modularly, allowing rapid deployment of completed cockpits."),
            ("Mobilization Advance:", "Milestone 1 invoice (25%) payable upon project agreement execution prior to Week 1 workshop kickoff.")
        ], CYAN_ACCENT),
        ("3. Scope Boundaries & Change Requests", [
            ("Scope Baseline:", "Strictly bounded to the 3 named CXO cockpits and S/4HANA tables specified in the Metric Calculation Blueprint."),
            ("Out-of-Scope Items:", "Upstream ERP data entry cleanup, custom ABAP transaction creation, or OS-level server upgrades are outside scope."),
            ("Change Management (CR):", "Substantial additions of new tables, custom data flows, or new reports managed via formal Change Request at agreed daily rates."),
            ("Schedule Adjustment:", "CR evaluations will define associated timeline impact prior to initiating additional work.")
        ], AMBER_WARN),
        ("4. Intellectual Property, Warranty & Hypercare", [
            ("Full IP Ownership Transfer:", "Complete ownership of custom Calculation Views, Power BI .pbix models, and DAX IP vests with Hical upon final settlement."),
            ("Complimentary Hypercare:", "Includes 30 calendar days of post-go-live hypercare support covering defect fixes and query performance stabilization."),
            ("NDA & Confidentiality:", "Strict mutual confidentiality protecting Hical's proprietary BOMs, pricing sheets, cost rates, and strategic customer data."),
            ("Long-Term Support (AMC):", "Optional annual maintenance contract (AMC) available post-hypercare for ongoing model extensions.")
        ], EMERALD_GREEN)
    ]
    
    w12 = 5.75
    h12 = 2.45
    for idx, (title, points, border_clr) in enumerate(terms_cards):
        r_idx = idx // 2
        c_idx = idx % 2
        left_pos = 0.8 + c_idx * (w12 + 0.233)
        top_pos = 1.6 + r_idx * (h12 + 0.2)
        
        card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(top_pos), Inches(w12), Inches(h12))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_clr
        card.line.width = Pt(1.5)
        
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.18)
        tf_c.margin_top = Inches(0.12)
        
        p = tf_c.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = border_clr
        p.space_after = Pt(4)
        
        for p_head, p_desc in points:
            p_pt = tf_c.add_paragraph()
            p_pt.space_after = Pt(3)
            r1 = p_pt.add_run()
            r1.text = "• " + p_head + " "
            r1.font.bold = True
            r1.font.size = Pt(8.2)
            r1.font.color.rgb = TEXT_DARK
            r2 = p_pt.add_run()
            r2.text = p_desc
            r2.font.bold = False
            r2.font.size = Pt(8.0)
            r2.font.color.rgb = TEXT_MUTED

    add_footer(s12, 12, is_dark=False)

    # =============================================================
    # SLIDE 13: Project Assumptions & Technical Dependencies (Dark)
    # =============================================================
    s13 = add_base_slide(is_dark=True)
    add_header(s13, "Project Assumptions & Technical Prerequisites", "DELIVERY PREREQUISITES & CLIENT DEPENDENCIES", "Key environment access, software licensing, and stakeholder availability essential for 10-week delivery", is_dark=True)
    
    dep_cards = [
        ("1. SAP S/4HANA Environment & Access", [
            ("Dedicated Database User:", "Hical IT to provision a dedicated read-only analytical database user on SAP HANA DB with authorization to build calculation views in an agreed analytics package (e.g. Z_HICAL_ANALYTICS)."),
            ("Modeling Tool Access:", "Access to SAP HANA Studio, SAP Web IDE, or Business Application Studio with developer rights to deploy views to the HANA repository (_SYS_BIC)."),
            ("Data Availability & Consistency:", "Standard S/4HANA tables (ACDOCA, MATDOC, EKPO, AFPO, RESB) are actively populated with consistent transactional records; upstream master data correction remains with Hical.")
        ], SAP_BLUE),
        ("2. Power BI Platform & Gateway Infrastructure", [
            ("Power BI Workspace & Licensing:", "Hical to provision required Power BI Pro, Premium Per User (PPU), or Microsoft Fabric capacity licenses for development, publishing, and executive consumption."),
            ("On-Premises Gateway VM:", "Hical IT to provide a dedicated Windows Server VM meeting Microsoft specifications for hosting the clustered On-Premises Data Gateway."),
            ("Network & Firewall Clearance:", "Unrestricted, low-latency network and firewall connectivity between the Data Gateway, SAP HANA DB server (ports 30015/39015), and the Power BI Cloud Service.")
        ], CYAN_ACCENT),
        ("3. Business SME Availability & Governance", [
            ("Single Point of Contact (SPOC):", "Hical to designate an internal Project Manager / SPOC to facilitate cross-functional scheduling, technical coordination, and milestone sign-offs."),
            ("Functional Stakeholder Time:", "Finance (CFO/Controller), Supply Chain (CPO/Buyers), and Operations (Plant Heads) teams available for Phase 1 metric discovery (4-6 hours total) and Phase 4 UAT sessions."),
            ("Timely Sign-Off Turnaround:", "Formal milestone deliverable reviews and feedback turnaround completed within 5 business days to maintain the 10-week agile project schedule.")
        ], GOLD_ACCENT)
    ]
    
    col_w13 = 3.75
    spacing_c13 = 0.24
    for idx, (title, points, border_c) in enumerate(dep_cards):
        c_left = 0.8 + idx * (col_w13 + spacing_c13)
        card = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(col_w13), Inches(5.1))
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
        p.font.size = Pt(10.5)
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
            r1.font.color.rgb = TEXT_LIGHT
            r2 = p_pt.add_run()
            r2.text = pt_body
            r2.font.bold = False
            r2.font.size = Pt(8.0)
            r2.font.color.rgb = TEXT_LIGHT_MUTED

    add_footer(s13, 13, is_dark=True)

    # Save presentation
    prs.save(output_path)
    print(f"Successfully generated proposal presentation: {output_path}")
    try:
        prs.save("Hical_Technologies_Strategic_CXO_Dashboards_Proposal.pptx")
    except Exception as e:
        print(f"Note: Hical_Technologies_Strategic_CXO_Dashboards_Proposal.pptx is open/locked ({e}), saved to {output_path}")

if __name__ == "__main__":
    build_proposal_presentation()
