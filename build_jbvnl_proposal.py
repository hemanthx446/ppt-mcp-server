import os, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_jbvnl_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Executive Palette
    NAVY_DARK = RGBColor(10, 25, 47)       # #0A192F Dark Hero Background
    NAVY_ACCENT = RGBColor(15, 35, 65)     # #0F2341 Header / Dark Cards
    NAVY_SURFACE = RGBColor(23, 42, 69)    # #172A45
    SLATE_900 = RGBColor(15, 23, 42)       # #0F172A Primary text
    SLATE_700 = RGBColor(51, 65, 85)       # #334155 Body text
    SLATE_500 = RGBColor(100, 116, 139)    # #64748B Subtitle / Muted
    SLATE_200 = RGBColor(226, 232, 240)    # #E2E8F0 Borders / Lines
    BG_LIGHT = RGBColor(248, 250, 252)     # #F8FAFC Slide background
    WHITE = RGBColor(255, 255, 255)
    BLUE_ACCENT = RGBColor(2, 132, 199)    # #0284C7 Executive Cyan/Blue
    BLUE_LIGHT = RGBColor(224, 242, 254)   # #E0F2FE Subtle blue tag fill
    BLUE_DARK = RGBColor(30, 58, 138)      # #1E3A8A Deep accent
    GOLD_ACCENT = RGBColor(217, 119, 6)    # #D97706 Warning/Highlight
    GREEN_ACCENT = RGBColor(16, 185, 129)  # #10B981 Success / S/4HANA pill

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, tracker, title, subtitle):
        # Category tracker
        tr_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.733), Inches(0.26))
        tf_tr = tr_box.text_frame
        tf_tr.word_wrap = True
        tf_tr.margin_left = tf_tr.margin_right = tf_tr.margin_top = tf_tr.margin_bottom = 0
        p_tr = tf_tr.paragraphs[0]
        p_tr.text = tracker.upper()
        p_tr.font.name = "Calibri"
        p_tr.font.size = Pt(9.5)
        p_tr.font.bold = True
        p_tr.font.color.rgb = BLUE_ACCENT

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.64), Inches(11.733), Inches(0.52))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(20)
        p_t.font.bold = True
        p_t.font.color.rgb = SLATE_900

        # Subtitle
        s_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.18), Inches(11.733), Inches(0.32))
        tf_s = s_box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle
        p_s.font.name = "Calibri"
        p_s.font.size = Pt(11)
        p_s.font.color.rgb = SLATE_500

    def add_card(slide, left, top, width, height, bg_color=WHITE, border_color=SLATE_200):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
        else:
            card.line.fill.background()
        return card

    # =========================================================================
    # SLIDE 1: TITLE & STRATEGIC POSITIONING
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, NAVY_DARK)

    # Optional decorative graphic
    if os.path.exists("assets/title_bg_graphic.png"):
        try:
            slide1.shapes.add_picture("assets/title_bg_graphic.png", Inches(7.5), Inches(0), Inches(5.833), Inches(7.5))
        except:
            pass

    # Lumbini Logo
    if os.path.exists("assets/lumbini_logo.png"):
        try:
            slide1.shapes.add_picture("assets/lumbini_logo.png", Inches(0.9), Inches(0.8), Inches(2.7), Inches(0.82))
        except:
            pass

    t_box1 = slide1.shapes.add_textbox(Inches(0.9), Inches(2.2), Inches(10.5), Inches(2.5))
    tf1 = t_box1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0

    p_org = tf1.paragraphs[0]
    p_org.text = "JHARKHAND BIJLI VITRAN NIGAM LIMITED (JBVNL)"
    p_org.font.name = "Calibri"
    p_org.font.size = Pt(13)
    p_org.font.bold = True
    p_org.font.color.rgb = RGBColor(56, 189, 248)

    p_main = tf1.add_paragraph()
    p_main.text = "Strategic SAP Operationalisation & Modernisation Proposal"
    p_main.font.name = "Calibri"
    p_main.font.size = Pt(30)
    p_main.font.bold = True
    p_main.font.color.rgb = WHITE
    p_main.space_before = Pt(6)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Two-Option Delivery Architecture: Existing ECC Go-Live (5 Months) vs. Next-Gen S/4HANA Private Cloud Transformation (12 Months)"
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_before = Pt(10)

    # Context Card
    add_card(slide1, Inches(0.9), Inches(4.85), Inches(9.8), Inches(1.85), bg_color=NAVY_ACCENT, border_color=RGBColor(30, 58, 138))
    ctx_box = slide1.shapes.add_textbox(Inches(1.1), Inches(5.0), Inches(9.4), Inches(1.55))
    tf_ctx = ctx_box.text_frame
    tf_ctx.word_wrap = True
    tf_ctx.margin_left = tf_ctx.margin_right = tf_ctx.margin_top = tf_ctx.margin_bottom = 0

    pc1 = tf_ctx.paragraphs[0]
    pc1.text = "BUDGETARY COMMERCIAL PROPOSAL & DELIVERY BLUEPRINT FOR MANAGEMENT REVIEW"
    pc1.font.name = "Calibri"
    pc1.font.size = Pt(10)
    pc1.font.bold = True
    pc1.font.color.rgb = RGBColor(56, 189, 248)

    pc2 = tf_ctx.add_paragraph()
    pc2.text = "Prepared for: Executive Leadership & IT Steering Committee  ·  JBVNL\nProposed Delivery Partner: Lumbini Elite Solutions & Services Pvt. Ltd. (Lumbini Elite Group)"
    pc2.font.name = "Calibri"
    pc2.font.size = Pt(12)
    pc2.font.bold = True
    pc2.font.color.rgb = WHITE
    pc2.space_before = Pt(4)

    pc3 = tf_ctx.add_paragraph()
    pc3.text = "Coverage: Complete Services Commercials, 104-Person Field Deployment, SAP PCE Cloud BOM Alignment & 12 Months Post-Go-Live Support"
    pc3.font.name = "Calibri"
    pc3.font.size = Pt(10.5)
    pc3.font.color.rgb = RGBColor(203, 213, 225)
    pc3.space_before = Pt(4)

    slide1.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 1 (TITLE & STRATEGIC CONTEXT):\n\n"
        "\"Good morning, members of the Executive Committee. Today, Lumbini Elite Solutions presents a definitive, transparent architectural and commercial proposal for JBVNL's SAP enterprise landscape.\n\n"
        "We present two viable, fully budgeted paths: Option 1 operationalises and takes live JBVNL's existing ECC investment within 5 months, followed by 12 months of stabilization support at an indicative services budget of ₹6.90 crore. Option 2 establishes a future-proof S/4HANA Private Cloud transformation, targeting go-live in 12 months with 12 months of support at ₹11.69 crore, aligned with modern SAP Cloud ERP Bill of Materials (BOM).\n\n"
        "Crucially, our proposal includes complete central architecture oversight, 104 dedicated field deployment personnel across all JBVNL circles and stores, and clear acceptance criteria. Let us examine the executive comparison.\""
    )
    print("Slide 1 generated.")

    # =========================================================================
    # SLIDE 2: EXECUTIVE SUMMARY & TWO-OPTION DECISION MATRIX
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, BG_LIGHT)
    add_header(slide2, "Executive Decision Framework", "Strategic Comparison: Existing ECC vs. S/4HANA Transformation", "A balanced evaluation of timeline, budget, technical debt, and long-term viability for JBVNL leadership.")

    # Two Main Option Cards Side-by-Side
    card_w2 = Inches(5.7)
    card_h2 = Inches(4.55)
    opt_x = [Inches(0.8), Inches(6.833)]

    # Option 1 Card (ECC)
    add_card(slide2, opt_x[0], Inches(1.68), card_w2, card_h2)
    tb_o1 = slide2.shapes.add_textbox(opt_x[0] + Inches(0.25), Inches(1.82), card_w2 - Inches(0.5), card_h2 - Inches(0.28))
    tf_o1 = tb_o1.text_frame
    tf_o1.word_wrap = True
    tf_o1.margin_left = tf_o1.margin_right = tf_o1.margin_top = tf_o1.margin_bottom = 0

    p_t1 = tf_o1.paragraphs[0]
    p_t1.text = "OPTION 1: EXISTING ECC OPERATIONALISATION"
    p_t1.font.name = "Calibri"
    p_t1.font.size = Pt(13)
    p_t1.font.bold = True
    p_t1.font.color.rgb = SLATE_900

    p_b1 = tf_o1.add_paragraph()
    p_b1.text = "Target Go-Live: 5 Months  |  Indicative Services Budget: ₹6.90 Crore"
    p_b1.font.name = "Calibri"
    p_b1.font.size = Pt(11)
    p_b1.font.bold = True
    p_b1.font.color.rgb = BLUE_ACCENT
    p_b1.space_after = Pt(6)

    o1_points = [
        ("Core Objective", "Salvage past investments and achieve immediate transaction readiness across FICO, MM, PS, and HCM."),
        ("Backlog & Scope", "Remediate 16-month transaction backlog; reconcile opening balances to approved date; clean legacy master data."),
        ("Deployment Scale", "16.25 Central FTE (5 months) + 104 Field Operators across 7 Area Boards, 15 Circles, 15 Stores (4 months)."),
        ("Post-Go-Live Support", "12 Months dedicated SLA support pool (20.75 FTE) including 14 Area Coordinators (₹266.70L)."),
        ("Strategic Trade-off", "Provides rapid operational stability but leaves technical debt; SAP ECC mainstream maintenance ends by Dec 2027.")
    ]

    for title, desc in o1_points:
        pt = tf_o1.add_paragraph()
        pt.text = f"▸ {title}: "
        pt.font.name = "Calibri"
        pt.font.size = Pt(9.8)
        pt.font.bold = True
        pt.font.color.rgb = NAVY_ACCENT
        pt.space_before = Pt(4)
        run = pt.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = SLATE_700

    # Option 2 Card (S/4HANA)
    add_card(slide2, opt_x[1], Inches(1.68), card_w2, card_h2)
    tb_o2 = slide2.shapes.add_textbox(opt_x[1] + Inches(0.25), Inches(1.82), card_w2 - Inches(0.5), card_h2 - Inches(0.28))
    tf_o2 = tb_o2.text_frame
    tf_o2.word_wrap = True
    tf_o2.margin_left = tf_o2.margin_right = tf_o2.margin_top = tf_o2.margin_bottom = 0

    p_t2 = tf_o2.paragraphs[0]
    p_t2.text = "OPTION 2: NEXT-GEN S/4HANA TRANSFORMATION"
    p_t2.font.name = "Calibri"
    p_t2.font.size = Pt(13)
    p_t2.font.bold = True
    p_t2.font.color.rgb = SLATE_900

    p_b2 = tf_o2.add_paragraph()
    p_b2.text = "Target Go-Live: 12 Months  |  Indicative Services Budget: ₹11.69 Crore"
    p_b2.font.name = "Calibri"
    p_b2.font.size = Pt(11)
    p_b2.font.bold = True
    p_b2.font.color.rgb = GREEN_ACCENT
    p_b2.space_after = Pt(6)

    o2_points = [
        ("Core Objective", "Deploy modern SAP Cloud ERP Private Edition (PCE), eliminating legacy ECC technical debt permanently."),
        ("Modern Architecture", "Universal Journal (ACDOCA), Business Partner / CVI, Fiori mobile UX, and in-memory HANA analytics."),
        ("Deployment Scale", "19.25 Central FTE (12 months) + 104 Field Operators (6 months migration & rollout support)."),
        ("Post-Go-Live Support", "12 Months enterprise support pool (21.50 FTE) including Solution Architect & Fiori Lead (₹290.70L)."),
        ("Strategic Advantage", "Long-term vendor maintenance to 2040+; Clean-Core cloud extensibility via SAP BTP; avoided double-migration cost.")
    ]

    for title, desc in o2_points:
        pt = tf_o2.add_paragraph()
        pt.text = f"▸ {title}: "
        pt.font.name = "Calibri"
        pt.font.size = Pt(9.8)
        pt.font.bold = True
        pt.font.color.rgb = NAVY_ACCENT
        pt.space_before = Pt(4)
        run = pt.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = SLATE_700

    # Bottom Foundation Recommendation Banner
    add_card(slide2, Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.68), bg_color=WHITE, border_color=SLATE_200)
    tb_rec = slide2.shapes.add_textbox(Inches(1.0), Inches(6.52), Inches(11.333), Inches(0.55))
    tf_rec = tb_rec.text_frame
    tf_rec.word_wrap = True
    tf_rec.margin_left = tf_rec.margin_right = tf_rec.margin_top = tf_rec.margin_bottom = 0
    p_rec = tf_rec.paragraphs[0]
    p_rec.text = "EXECUTIVE RECOMMENDATION: 4-WEEK MOBILISATION ASSESSMENT FIRST (INCLUDED IN BOTH OPTIONS)"
    p_rec.font.name = "Calibri"
    p_rec.font.size = Pt(10)
    p_rec.font.bold = True
    p_rec.font.color.rgb = BLUE_DARK

    p_rec2 = tf_rec.add_paragraph()
    p_rec2.text = "Approve Month 1 assessment to audit database health, verify 16-month backlog volumes, reconcile JUSNL BOM entitlements, and freeze circle deployment locations. A sequential ECC-then-S/4 route requires a separate migration budget; option prices must not be combined."
    p_rec2.font.name = "Calibri"
    p_rec2.font.size = Pt(9.2)
    p_rec2.font.color.rgb = SLATE_700
    p_rec2.space_before = Pt(2)

    slide2.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 2 (DECISION MATRIX):\n\n"
        "\"To help the Board make an informed capital and operational decision, Slide 2 places the two options side by side.\n\n"
        "Option 1 focuses on speed and cost: Taking the existing ECC system live in 5 months for ₹6.90 crore. This solves immediate operational needs, clears the transaction backlog, and operationalises FICO, MM, PS, and Payroll. However, ECC reaches mainstream maintenance by end of 2027.\n\n"
        "Option 2 is a strategic transformation: Moving directly to S/4HANA Private Cloud over 12 months for ₹11.69 crore. This bypasses ECC technical debt, deploys modern Fiori interfaces, Universal Journal, and positions JBVNL on SAP's supported roadmap to 2040+.\n\n"
        "Our strong advice: Approve a 4-week assessment first—which is included in the implementation price of whichever option is selected—to establish the ground truth before capital commitment.\""
    )
    print("Slide 2 generated.")

    # =========================================================================
    # SLIDE 3: CURRENT STATE ASSESSMENT & OPERATIONAL SCOPE
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, BG_LIGHT)
    add_header(slide3, "Landscape & Operational Baseline", "Current State Baseline, Functional Scope & Boundaries", "Defining operational footprint, legacy remediation challenges, and explicit scope boundaries.")

    # 3 Cards Grid (Top) + 1 Full Width Card (Bottom)
    c3_w = Inches(3.68)
    c3_h = Inches(2.8)
    c3_x = [Inches(0.8), Inches(4.82), Inches(8.84)]

    # Col 1: JBVNL Footprint
    add_card(slide3, c3_x[0], Inches(1.68), c3_w, c3_h)
    tb_c1 = slide3.shapes.add_textbox(c3_x[0] + Inches(0.18), Inches(1.8), c3_w - Inches(0.36), c3_h - Inches(0.24))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_right = tf_c1.margin_top = tf_c1.margin_bottom = 0

    p = tf_c1.paragraphs[0]
    p.text = "OPERATIONAL FOOTPRINT"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT

    p = tf_c1.add_paragraph()
    p.text = "Geographic Distribution Baseline"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SLATE_900
    p.space_after = Pt(4)

    fp_points = [
        "1 Corporate Headquarters (Ranchi)",
        "7 Area Electricity Boards (Field Command)",
        "15 Electric Supply Circles (Operational hubs)",
        "15 Central & Divisional Stores (Material inventory)",
        "Multi-Division Sub-transmission Network across Jharkhand State"
    ]
    for pt in fp_points:
        p = tf_c1.add_paragraph()
        p.text = f"•  {pt}"
        p.font.name = "Calibri"
        p.font.size = Pt(9.5)
        p.font.color.rgb = SLATE_700
        p.space_before = Pt(2)

    # Col 2: Functional Scope
    add_card(slide3, c3_x[1], Inches(1.68), c3_w, c3_h)
    tb_c2 = slide3.shapes.add_textbox(c3_x[1] + Inches(0.18), Inches(1.8), c3_w - Inches(0.36), c3_h - Inches(0.24))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_right = tf_c2.margin_top = tf_c2.margin_bottom = 0

    p = tf_c2.paragraphs[0]
    p.text = "FUNCTIONAL MODULES"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT

    p = tf_c2.add_paragraph()
    p.text = "Core ERP Implementation Scope"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SLATE_900
    p.space_after = Pt(4)

    fn_points = [
        "FICO: General Ledger, AP, AR, Asset Accounting, Cost Centers",
        "MM: Procurement, Store Inventory, Purchase Orders, DI Tracking",
        "PS: Capital Works in Progress (CWIP), Project Budgets",
        "HCM: Personnel Admin, Organizational Mgmt, Payroll, ESS/MSS",
        "Reporting & Analytics: Operational MIS, Financial Statements"
    ]
    for pt in fn_points:
        p = tf_c2.add_paragraph()
        p.text = f"•  {pt}"
        p.font.name = "Calibri"
        p.font.size = Pt(9.5)
        p.font.color.rgb = SLATE_700
        p.space_before = Pt(2)

    # Col 3: Key Remediation Challenges
    add_card(slide3, c3_x[2], Inches(1.68), c3_w, c3_h)
    tb_c3 = slide3.shapes.add_textbox(c3_x[2] + Inches(0.18), Inches(1.8), c3_w - Inches(0.36), c3_h - Inches(0.24))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True
    tf_c3.margin_left = tf_c3.margin_right = tf_c3.margin_top = tf_c3.margin_bottom = 0

    p = tf_c3.paragraphs[0]
    p.text = "REMEDIATION CHALLENGES"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT

    p = tf_c3.add_paragraph()
    p.text = "Unblocking the Legacy System"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SLATE_900
    p.space_after = Pt(4)

    ch_points = [
        "16-Month Transaction Backlog across MM, FICO, and Stores",
        "Unreconciled opening cutover balances and physical stock drift",
        "Open Purchase Orders & Dispatch Instructions (DI) reconciliation",
        "Historical payroll discrepancy and policy rule sign-off",
        "Incomplete master data governance and role authorization gaps"
    ]
    for pt in ch_points:
        p = tf_c3.add_paragraph()
        p.text = f"•  {pt}"
        p.font.name = "Calibri"
        p.font.size = Pt(9.5)
        p.font.color.rgb = SLATE_700
        p.space_before = Pt(2)

    # Bottom Boundaries & Exclusions Card
    add_card(slide3, Inches(0.8), Inches(4.7), Inches(11.733), Inches(2.4), bg_color=WHITE, border_color=SLATE_200)
    tb_bnd = slide3.shapes.add_textbox(Inches(1.0), Inches(4.82), Inches(11.333), Inches(2.15))
    tf_bnd = tb_bnd.text_frame
    tf_bnd.word_wrap = True
    tf_bnd.margin_left = tf_bnd.margin_right = tf_bnd.margin_top = tf_bnd.margin_bottom = 0

    p = tf_bnd.paragraphs[0]
    p.text = "EXPLICIT SCOPE BOUNDARIES & INTEGRATION GOVERNANCE"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_ACCENT

    bnd_items = [
        ("CIS / Utility Billing Exclusion", "Replacement of Customer Information System (CIS), IS-U, or consumer revenue billing is explicitly excluded. Focus is enterprise resource planning (ERP). CIS interface assessment is included."),
        ("Backlog Data Ingestion Principle", "We do NOT recommend blindly re-entering 16 months of historical transactions line-by-line. JBVNL Finance must approve loading reconciled open items and balances to ensure audit integrity."),
        ("Licensing & Infrastructure Exclusions", "Services budgets exclude SAP software licences, annual maintenance (ATS), cloud subscriptions, server hardware, and taxes. These are subject to JUSNL BOM reconciliation."),
        ("Statutory & Ownership Boundaries", "Statutory audit, physical warehouse inventory counting, and policy definitions remain client-owned. Lumbini provides technical data migration, validation tooling, and system controls.")
    ]

    for title, desc in bnd_items:
        p = tf_bnd.add_paragraph()
        p.text = f"▸ {title}: "
        p.font.name = "Calibri"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = SLATE_900
        p.space_before = Pt(3)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = SLATE_700

    slide3.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 3 (CURRENT STATE & SCOPE):\n\n"
        "\"Slide 3 establishes the operational reality on the ground.\n\n"
        "JBVNL's deployment model covers 1 Corporate HQ, 7 Area Boards, 15 Circles, and 15 central/divisional stores. The functional footprint spans FICO, MM, PS, HCM, and reporting.\n\n"
        "Why has the system struggled to go live? Our diagnosis shows a 16-month operational backlog, unreconciled store stock, pending payroll rules, and missing master data governance.\n\n"
        "Crucially, we define clear scope boundaries: We are implementing enterprise ERP, not replacing consumer billing or CIS. We will interface with billing, but replacing it is out of scope. Furthermore, we advise against blindly re-entering 16 months of historical transactions. Instead, we propose loading verified opening balances and open items under strict Finance sign-off.\""
    )
    print("Slide 3 generated.")

    # =========================================================================
    # SLIDE 4: OPTION 1 — EXISTING ECC REMEDIATION (5 MONTHS)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, BG_LIGHT)
    add_header(slide4, "Option 1 Delivery Blueprint", "Existing ECC System Operationalisation & Go-Live (5 Months)", "A disciplined 5-month sprint plan to remediate data, fix defects, cut over, and support live operations.")

    # 5 Sequential Timeline Cards
    step_w = Inches(2.2)
    step_h = Inches(4.35)
    step_x = [Inches(0.8), Inches(3.18), Inches(5.56), Inches(7.94), Inches(10.32)]

    steps_ecc = [
        {
            "month": "MONTH 1",
            "title": "Inventory & Baseline",
            "tag": "ASSESSMENT GATE",
            "actions": [
                "Audit ECC release, EHP level, database, and system backups.",
                "Sizing 16-month backlog across FICO, MM, and Stores.",
                "Establish Central Command Centre at Ranchi HQ.",
                "Appoint functional unit owners across 7 Area Boards."
            ],
            "output": "Signed Readiness Report, Scope Baseline & Dependency Register."
        },
        {
            "month": "MONTHS 2–3",
            "title": "Remediation & Cleansing",
            "tag": "DATA & DEFECT FIXING",
            "actions": [
                "Cleanse vendor, material, customer, and GL master records.",
                "Reconcile opening balances, CWIP assets, and store stock.",
                "Reconcile open POs, pending DIs, and vendor advance ledgers.",
                "Finalize payroll policy rules and repair custom ABAP defects."
            ],
            "output": "Business-owned Reconciliation Sign-off & Master Data Freeze."
        },
        {
            "month": "MONTH 4",
            "title": "Integration & Mocks",
            "tag": "RIGOROUS REHEARSAL",
            "actions": [
                "Execute end-to-end integration and interface testing (CIS, Banks).",
                "Execute two complete payroll parallel runs against legacy outputs.",
                "Conduct user role verification and end-user training.",
                "Execute two simulated cutover rehearsals within outage windows."
            ],
            "output": "Formal UAT Sign-off & Mock Cutover Verification Report."
        },
        {
            "month": "MONTH 5",
            "title": "Cutover & Go-Live",
            "tag": "PRODUCTION ACTIVATION",
            "actions": [
                "Deploy 104 field operators to Circles and Stores across Jharkhand.",
                "Execute production cutover in approved unit waves.",
                "Reconcile uploaded opening balances against audited trial balances.",
                "Formally declare SAP ECC as the authoritative System of Record."
            ],
            "output": "Formal Go-Live Sign-off & Live Transaction Processing."
        },
        {
            "month": "MONTHS 6–17",
            "title": "12-Month Support",
            "tag": "STABILISATION & AMS",
            "actions": [
                "Deploy 20.75 FTE support pool including 14 Area Coordinators.",
                "Daily SLA incident resolution, defect bug-fixing, and patch monitoring.",
                "Continuous store inventory reconciliation and month-end close support.",
                "Structured knowledge transfer to JBVNL internal IT cadres."
            ],
            "output": "Monthly SLA Performance Reports & Final Transition Acceptance."
        }
    ]

    for idx, s in enumerate(steps_ecc):
        cx = step_x[idx]
        add_card(slide4, cx, Inches(1.68), step_w, step_h)

        tb = slide4.shapes.add_textbox(cx + Inches(0.12), Inches(1.8), step_w - Inches(0.24), step_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = s["month"]
        p.font.name = "Calibri"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = BLUE_ACCENT

        p = tf.add_paragraph()
        p.text = s["title"]
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = SLATE_900

        p = tf.add_paragraph()
        p.text = s["tag"]
        p.font.name = "Calibri"
        p.font.size = Pt(8)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_after = Pt(4)

        for a in s["actions"]:
            p = tf.add_paragraph()
            p.text = f"• {a}"
            p.font.name = "Calibri"
            p.font.size = Pt(8.5)
            p.font.color.rgb = SLATE_700
            p.space_before = Pt(2)

        p = tf.add_paragraph()
        p.text = "Deliverable Output:"
        p.font.name = "Calibri"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = SLATE_900
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = s["output"]
        p.font.name = "Calibri"
        p.font.size = Pt(8)
        p.font.color.rgb = BLUE_DARK

    # Bottom Callout
    add_card(slide4, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.78), bg_color=WHITE, border_color=SLATE_200)
    tb_bot = slide4.shapes.add_textbox(Inches(1.0), Inches(6.42), Inches(11.333), Inches(0.65))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = tf_bot.margin_bottom = 0

    p = tf_bot.paragraphs[0]
    p.text = "CRITICAL SUCCESS FACTOR FOR 5-MONTH ECC GO-LIVE"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT

    p = tf_bot.add_paragraph()
    p.text = "Strict adherence to the 5-month timeline requires prompt JBVNL nomination of 7 Area & 15 Circle unit owners, freezing master data changes by Month 3, and approving cutover opening balances without waiting for unresolved historical vendor audits."
    p.font.name = "Calibri"
    p.font.size = Pt(9)
    p.font.color.rgb = SLATE_700
    p.space_before = Pt(2)

    slide4.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 4 (OPTION 1: ECC ROADMAP):\n\n"
        "\"Slide 4 breaks down the 5-month execution sprint for Option 1.\n\n"
        "Month 1 is the assessment and command centre setup. We audit the database, backup integrity, and measure the exact backlog.\n\n"
        "Months 2 and 3 tackle data remediation: Master data cleansing, open purchase order reconciliation, and stock alignment across all 15 stores. Crucially, JBVNL Finance approves the cutover balances here.\n\n"
        "Month 4 is rigorous testing: Integration tests with banks and CIS, two payroll parallel runs, end-user training, and two simulated mock cutovers to ensure the team can execute within maintenance outage windows.\n\n"
        "Month 5 is deployment: 104 field operators go live across all circles and stores, activating SAP ECC as the single source of truth.\n\n"
        "Months 6 through 17 deliver 12 months of post-go-live stabilization, backed by 20.75 full-time support specialists.\""
    )
    print("Slide 4 generated.")

    # =========================================================================
    # SLIDE 5: OPTION 2 — S/4HANA PROGRAMME ROADMAP (12 MONTHS)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, BG_LIGHT)
    add_header(slide5, "Option 2 Transformation Blueprint", "S/4HANA Private Cloud Transformation Roadmap (12 Months)", "A modern, 12-month Clean-Core cloud transformation deploying SAP S/4HANA Private Cloud Edition (PCE).")

    # 6 Phase Cards across 12 Months
    ph_w = Inches(1.82)
    ph_h = Inches(4.35)
    ph_x = [Inches(0.8), Inches(2.78), Inches(4.76), Inches(6.74), Inches(8.72), Inches(10.70)]

    phases_s4 = [
        {
            "phase": "M 1",
            "title": "Assess & Baseline",
            "tag": "READINESS AUDIT",
            "bullets": [
                "Readiness check of current ECC system.",
                "Custom code & Z-table inventory analysis.",
                "PAM & add-on compatibility check.",
                "SAP PCE licence entitlement audit."
            ],
            "milestone": "Readiness Baseline & Target Architecture sign-off."
        },
        {
            "phase": "M 2–3",
            "title": "Design & Sizing",
            "tag": "BLUEPRINT GATE",
            "bullets": [
                "Select System Conversion vs. Greenfield implementation.",
                "HANA sizing, private cloud hosting & DR design.",
                "Reconcile JUSNL BOM to JBVNL FUE requirements.",
                "Finalize Clean-Core extension strategy (BTP)."
            ],
            "milestone": "Approved Solution Blueprint & Cloud BOM."
        },
        {
            "phase": "M 4–7",
            "title": "Build & Remediate",
            "tag": "CLEAN-CORE BUILD",
            "bullets": [
                "Configure Universal Journal (ACDOCA) & Asset Accounting.",
                "Execute Business Partner / CVI transformation.",
                "Remediate custom code to ABAP Cloud / RAP standards.",
                "Deploy Fiori UX and build BTP integration iFlows."
            ],
            "milestone": "Tested System Build & Migration Sandbox validation."
        },
        {
            "phase": "M 8–9",
            "title": "Mock Migrations",
            "tag": "DATA & INTEGRATION",
            "bullets": [
                "Execute 2 end-to-end mock data migrations.",
                "Reconcile balances & test Simplification Items.",
                "Validate CIS, SCADA, and banking interfaces.",
                "Defect resolution & performance tuning."
            ],
            "milestone": "Reconciled Data Results & Interface Sign-off."
        },
        {
            "phase": "M 10–11",
            "title": "UAT & Rehearsal",
            "tag": "OPERATIONAL READINESS",
            "bullets": [
                "Comprehensive business user acceptance testing (UAT).",
                "Execute 2 parallel payroll simulation runs.",
                "Train 104 field operators and circle champions.",
                "Dress rehearsal cutover within maintenance window."
            ],
            "milestone": "Signed Operational Readiness & Cutover Approval."
        },
        {
            "phase": "M 12–24",
            "title": "Go-Live & Support",
            "tag": "ACTIVATION & 12M AMS",
            "bullets": [
                "Production migration & live financial cutover.",
                "Deploy 104 field operators across circles/stores.",
                "12 Months Hypercare & Support (21.5 FTE).",
                "Continuous performance tuning & knowledge transfer."
            ],
            "milestone": "Go-Live Certificate & 12M Support SLA Acceptance."
        }
    ]

    for idx, ph in enumerate(phases_s4):
        cx = ph_x[idx]
        add_card(slide5, cx, Inches(1.68), ph_w, ph_h)

        tb = slide5.shapes.add_textbox(cx + Inches(0.1), Inches(1.8), ph_w - Inches(0.2), ph_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = ph["phase"]
        p.font.name = "Calibri"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = GREEN_ACCENT

        p = tf.add_paragraph()
        p.text = ph["title"]
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = SLATE_900

        p = tf.add_paragraph()
        p.text = ph["tag"]
        p.font.name = "Calibri"
        p.font.size = Pt(8)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_after = Pt(4)

        for b in ph["bullets"]:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.name = "Calibri"
            p.font.size = Pt(8.2)
            p.font.color.rgb = SLATE_700
            p.space_before = Pt(2)

        p = tf.add_paragraph()
        p.text = "Key Gate:"
        p.font.name = "Calibri"
        p.font.size = Pt(8.2)
        p.font.bold = True
        p.font.color.rgb = SLATE_900
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = ph["milestone"]
        p.font.name = "Calibri"
        p.font.size = Pt(8)
        p.font.color.rgb = BLUE_DARK

    # Bottom Architectural Guardrail
    add_card(slide5, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.78), bg_color=WHITE, border_color=SLATE_200)
    tb_bot = slide5.shapes.add_textbox(Inches(1.0), Inches(6.42), Inches(11.333), Inches(0.65))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = tf_bot.margin_bottom = 0

    p = tf_bot.paragraphs[0]
    p.text = "TARGET ARCHITECTURE SELECTION: CONVERSION VS. NEW IMPLEMENTATION"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK

    p = tf_bot.add_paragraph()
    p.text = "System conversion is preferred only if existing ECC configuration and data lineage justify retention. If legacy design carries excessive customization or structural defects, a fresh Clean-Core implementation is recommended to ensure long-term agility and avoid carrying historical flaws."
    p.font.name = "Calibri"
    p.font.size = Pt(9)
    p.font.color.rgb = SLATE_700
    p.space_before = Pt(2)

    slide5.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 5 (OPTION 2: S/4HANA ROADMAP):\n\n"
        "\"Slide 5 outlines the 12-month journey to SAP S/4HANA Private Cloud Edition.\n\n"
        "Months 1 through 3 establish the architectural foundation: Evaluating readiness, sizing HANA databases, deciding between system conversion versus new implementation, and freezing the Cloud BOM.\n\n"
        "Months 4 through 7 execute core configuration: Universal Journal (ACDOCA) for unified financials, Customer-Vendor Integration (CVI) to Business Partner, custom code refactoring to Clean Core standards, and Fiori UI setup.\n\n"
        "Months 8 through 11 ensure zero-defect migration: Executing two mock data cutovers, validating interfaces (SCADA, CIS), full business UAT, and payroll parallel testing.\n\n"
        "Month 12 is cutover and go-live, supported by 104 field operators, transitioning into a comprehensive 12-month post-go-live hypercare and support agreement.\""
    )
    print("Slide 5 generated.")

    # =========================================================================
    # SLIDE 6: TARGET S/4HANA ARCHITECTURE & SAP CLOUD BOM
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, BG_LIGHT)
    add_header(slide6, "Target Enterprise Architecture", "SAP Cloud ERP Bill of Materials (BOM) & BTP Innovations", "Harmonizing Private Cloud ERP subscriptions, BTP extensions, and user entitlements (JUSNL BOM alignment).")

    # 2 Main Columns: Left = Cloud ERP BOM (PCE); Right = BTP & Public Cloud Architecture
    col6_w = Inches(5.7)
    col6_h = Inches(4.55)
    col6_x = [Inches(0.8), Inches(6.833)]

    # Left: Private Cloud BOM
    add_card(slide6, col6_x[0], Inches(1.68), col6_w, col6_h)
    tb_pce = slide6.shapes.add_textbox(col6_x[0] + Inches(0.22), Inches(1.8), col6_w - Inches(0.44), col6_h - Inches(0.24))
    tf_pce = tb_pce.text_frame
    tf_pce.word_wrap = True
    tf_pce.margin_left = tf_pce.margin_right = tf_pce.margin_top = tf_pce.margin_bottom = 0

    p = tf_pce.paragraphs[0]
    p.text = "SAP CLOUD ERP PRIVATE EDITION (PCE) BOM"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SLATE_900

    p = tf_pce.add_paragraph()
    p.text = "S/4HANA Private Cloud Subscriptions (As per JUSNL Working)"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT
    p.space_after = Pt(4)

    pce_items = [
        ("8019361 · SAP Cloud ERP Private", "136 FUE (Full Use Equivalent) in 3-Tier Arch (Y1–Y3), scaling to 152 FUE in Y4."),
        ("User Breakdown (134 FUE)", "• Advanced Users: 32 (1:1 = 32 FUE)\n• Core Users: 425 (5:1 ratio = 85 FUE)\n• Developers: 4 (1:2 ratio = 8 FUE)\n• Self-Service: 270 (30:1 ratio = 9 FUE)"),
        ("8008910 · Core HCM Cloud, Private", "715 Users (Y1–Y3), scaling to 850 Users (Y4–Y5) for personnel management."),
        ("8008783 · SAP Payroll Processing", "715 Users (Y1–Y3), scaling to 850 Users (Y4–Y5) for compliant payroll."),
        ("8019271 · Business Data Cloud (BDC)", "640 Capacity Units (CU) Y2–Y3; doubled to 1,280 CU in Y4 for SAP Analytics Cloud."),
        ("8020297 · Digital Access & DR", "10,000 Documents for external interfaces + Disaster Recovery option from Year 2.")
    ]

    for title, desc in pce_items:
        p = tf_pce.add_paragraph()
        p.text = f"▸ {title}: "
        p.font.name = "Calibri"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_before = Pt(3)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = SLATE_700

    # Right: BTP & Digital Extensions
    add_card(slide6, col6_x[1], Inches(1.68), col6_w, col6_h)
    tb_btp = slide6.shapes.add_textbox(col6_x[1] + Inches(0.22), Inches(1.8), col6_w - Inches(0.44), col6_h - Inches(0.24))
    tf_btp = tb_btp.text_frame
    tf_btp.word_wrap = True
    tf_btp.margin_left = tf_btp.margin_right = tf_btp.margin_top = tf_btp.margin_bottom = 0

    p = tf_btp.paragraphs[0]
    p.text = "SAP BTP EXTENSIONS & INNOVATION FABRIC"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SLATE_900

    p = tf_btp.add_paragraph()
    p.text = "Cloud Credits, AI Units & Priority Use Cases"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT
    p.space_after = Pt(4)

    btp_items = [
        ("8016044 · BTP Enterprise Agreement", "Cloud Credits tier (₹10.93L – ₹65.60L) powering integrations and extensions."),
        ("8019544 / 8019164 · Joule Base & AI Units", "AI Capacity Units (25 ➔ 50 ➔ 100 ➔ 150) for Joule Premium AI in Finance and HCM."),
        ("8016701 · SAP Learning Hub", "2 User subscriptions from Year 2 for continuous internal capability enablement."),
        ("5 Critical BTP Extensions for JBVNL", "1. PF (Provident Fund) Extension — Custom trustee ledger & portal.\n2. SCADA Integration — Ingesting sub-station telemetry into SAP.\n3. Supplier Collaboration Portal — Vendor PO & DI tracking.\n4. Timesheet & Attendance — Frontline field operator recording.\n5. BTP Document Management — Digital archiving for bills & invoices.")
    ]

    for title, desc in btp_items:
        p = tf_btp.add_paragraph()
        p.text = f"▸ {title}: "
        p.font.name = "Calibri"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_before = Pt(3)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = SLATE_700

    # Bottom BOM Notice
    add_card(slide6, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.78), bg_color=WHITE, border_color=SLATE_200)
    tb_bot = slide6.shapes.add_textbox(Inches(1.0), Inches(6.42), Inches(11.333), Inches(0.65))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = tf_bot.margin_bottom = 0

    p = tf_bot.paragraphs[0]
    p.text = "JUSNL BOM RECONCILIATION REQUIREMENT"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK

    p = tf_bot.add_paragraph()
    p.text = "The Cloud ERP BOM above represents the reference architecture from JUSNL. For JBVNL, exact FUE counts, database tiering, and cloud subscription rates must be re-quoted by SAP India based on finalized active user counts and distribution transaction throughput."
    p.font.name = "Calibri"
    p.font.size = Pt(9)
    p.font.color.rgb = SLATE_700
    p.space_before = Pt(2)

    slide6.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 6 (S/4HANA ARCHITECTURE & BOM):\n\n"
        "\"Slide 6 provides complete architectural transparency into the SAP Cloud Bill of Materials (BOM), mapped directly from the JUSNL reference model.\n\n"
        "On the left is the Private Cloud ERP package: Sized at 136 Full Use Equivalents (FUE) across 32 Advance users, 425 Core operational users, 4 Developers, and 270 Self-service users. It includes Core HCM and Payroll for 715 employees, Business Data Cloud (BDC) with 640 capacity units, and digital access.\n\n"
        "On the right is SAP Business Technology Platform (BTP). Rather than writing heavy customizations inside the S/4HANA core, we build five targeted side-by-side extensions: A Provident Fund trustee extension, SCADA sub-station telemetry integration, Supplier Collaboration for purchase orders and delivery instructions, mobile timesheets for field operators, and cloud Document Management.\n\n"
        "This adheres strictly to SAP's Clean-Core architecture, ensuring zero upgrade disruption in the future.\""
    )
    print("Slide 6 generated.")

    # =========================================================================
    # SLIDE 7: COMPREHENSIVE MANPOWER DEPLOYMENT MODEL
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, BG_LIGHT)
    add_header(slide7, "Resource Architecture & Staffing", "Manpower Deployment Model: Central Specialists & 104 Field Staff", "Combining seasoned enterprise architects with massive on-ground field deployment across Jharkhand.")

    # 3 Structured Columns
    col7_w = Inches(3.68)
    col7_h = Inches(4.55)
    col7_x = [Inches(0.8), Inches(4.82), Inches(8.84)]

    # Col 1: Central Team
    add_card(slide7, col7_x[0], Inches(1.68), col7_w, col7_h)
    tb_m1 = slide7.shapes.add_textbox(col7_x[0] + Inches(0.18), Inches(1.8), col7_w - Inches(0.36), col7_h - Inches(0.24))
    tf_m1 = tb_m1.text_frame
    tf_m1.word_wrap = True
    tf_m1.margin_left = tf_m1.margin_right = tf_m1.margin_top = tf_m1.margin_bottom = 0

    p = tf_m1.paragraphs[0]
    p.text = "CENTRAL LEADERSHIP & SPECIALISTS"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT

    p = tf_m1.add_paragraph()
    p.text = "HQ Architecture & Delivery Team"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SLATE_900
    p.space_after = Pt(4)

    central_roles = [
        ("Programme Director", "0.25 FTE · ₹4.00L/mo (Executive Oversight)"),
        ("Project Manager & PMO", "2.00 FTE · ₹4.00L/mo (Delivery Governance)"),
        ("FICO Specialists", "2.00 FTE · ₹4.50L/mo (GL, AP, AR, Assets)"),
        ("MM Specialists", "2.00 FTE · ₹4.00L/mo (Procurement & Stores)"),
        ("PS & HCM Specialists", "2.00 FTE · ₹4.00L/mo (CWIP, Payroll, ESS)"),
        ("BASIS & ABAP/Interfaces", "2 to 3 FTE · ₹4.50L to ₹6.75L/mo"),
        ("Data Migration Leads", "4.00 FTE · ₹4.00L/mo (Cleansing & ETL)"),
        ("Training & QA Leads", "2.00 FTE · ₹3.00L/mo (Test & Adoption)"),
        ("S/4 Architect & Fiori Lead", "2.00 FTE · ₹5.75L/mo (S/4 Option Only)")
    ]
    for r, d in central_roles:
        p = tf_m1.add_paragraph()
        p.text = f"• {r}: "
        p.font.name = "Calibri"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_before = Pt(1.5)
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = SLATE_700

    p_tot1 = tf_m1.add_paragraph()
    p_tot1.text = "ECC: 16.25 FTE (₹29.00L/mo)  |  S/4: 19.25 FTE (₹37.00L/mo)"
    p_tot1.font.name = "Calibri"
    p_tot1.font.size = Pt(8.8)
    p_tot1.font.bold = True
    p_tot1.font.color.rgb = BLUE_DARK
    p_tot1.space_before = Pt(4)

    # Col 2: Field Staff (104 Personnel)
    add_card(slide7, col7_x[1], Inches(1.68), col7_w, col7_h)
    tb_m2 = slide7.shapes.add_textbox(col7_x[1] + Inches(0.18), Inches(1.8), col7_w - Inches(0.36), col7_h - Inches(0.24))
    tf_m2 = tb_m2.text_frame
    tf_m2.word_wrap = True
    tf_m2.margin_left = tf_m2.margin_right = tf_m2.margin_top = tf_m2.margin_bottom = 0

    p = tf_m2.paragraphs[0]
    p.text = "FIELD EXECUTION (104 PERSONNEL)"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT

    p = tf_m2.add_paragraph()
    p.text = "Statewide Ground Support Footprint"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SLATE_900
    p.space_after = Pt(4)

    field_roles = [
        ("14 Area Coordinators", "7 Area Boards (2 per Area)\nRate: ₹0.60L/mo · Total: ₹8.40L/mo\nRole: Regional governance, escalation & user hand-holding."),
        ("60 Circle Operators", "15 Electric Supply Circles (4 per Circle)\nRate: ₹0.45L/mo · Total: ₹27.00L/mo\nRole: Backlog voucher entry, DI reconciliation, user support."),
        ("30 Store Operators", "15 Central & Divisional Stores (2 per Store)\nRate: ₹0.45L/mo · Total: ₹13.50L/mo\nRole: GRN posting, material verification, gate pass audits.")
    ]
    for r, d in field_roles:
        p = tf_m2.add_paragraph()
        p.text = f"▸ {r}: "
        p.font.name = "Calibri"
        p.font.size = Pt(9.2)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_before = Pt(3)
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = SLATE_700

    p_tot2 = tf_m2.add_paragraph()
    p_tot2.text = "Total Field Strength: 104 Personnel · ₹48.90 Lakh / Month\nDuration: 4 Months (ECC: ₹195.60L)  |  6 Months (S/4: ₹293.40L)"
    p_tot2.font.name = "Calibri"
    p_tot2.font.size = Pt(8.8)
    p_tot2.font.bold = True
    p_tot2.font.color.rgb = BLUE_DARK
    p_tot2.space_before = Pt(4)

    # Col 3: Support Pool (12 Months)
    add_card(slide7, col7_x[2], Inches(1.68), col7_w, col7_h)
    tb_m3 = slide7.shapes.add_textbox(col7_x[2] + Inches(0.18), Inches(1.8), col7_w - Inches(0.36), col7_h - Inches(0.24))
    tf_m3 = tb_m3.text_frame
    tf_m3.word_wrap = True
    tf_m3.margin_left = tf_m3.margin_right = tf_m3.margin_top = tf_m3.margin_bottom = 0

    p = tf_m3.paragraphs[0]
    p.text = "12-MONTH POST-GO-LIVE SUPPORT"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT

    p = tf_m3.add_paragraph()
    p.text = "Stabilisation & Operational Retainer"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SLATE_900
    p.space_after = Pt(4)

    support_items = [
        ("Central Core Support Pool", "PM (0.5), FICO (1.0), MM (1.0), PS (0.5), HCM (0.5), BASIS (0.5), ABAP (0.5), Data (1.0), Training (0.5), QA (0.25)."),
        ("Regional Field Governance", "Retaining all 14 Area Coordinators across 7 Area Boards to handle regional circle escalations and user adoption."),
        ("ECC Support Commitment", "20.75 FTE Total · ₹22.225 Lakh / Month\nAnnual Support: ₹266.70 Lakh (Included in budget)"),
        ("S/4HANA Support Commitment", "Adds Solution Architect (0.25) & Fiori/Security (0.5).\n21.50 FTE Total · ₹24.225 Lakh / Month\nAnnual Support: ₹290.70 Lakh (Included in budget)"),
        ("Governance Window", "Coverage: 9 AM to 6 PM on business days with Severity-1 emergency on-call escalation.")
    ]
    for r, d in support_items:
        p = tf_m3.add_paragraph()
        p.text = f"▸ {r}: "
        p.font.name = "Calibri"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_before = Pt(2.5)
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = SLATE_700

    # Bottom Staffing Governance Note
    add_card(slide7, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.78), bg_color=WHITE, border_color=SLATE_200)
    tb_bot = slide7.shapes.add_textbox(Inches(1.0), Inches(6.42), Inches(11.333), Inches(0.65))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = tf_bot.margin_bottom = 0

    p = tf_bot.paragraphs[0]
    p.text = "FIELD OPERATOR GOVERNANCE & ACCOUNTABILITY SAFEGUARD"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK

    p = tf_bot.add_paragraph()
    p.text = "Peak staffing reaches 120.25 FTE (ECC) and 123.25 FTE (S/4HANA). Field operators support data entry, backlog clearance, and user guidance under explicit JBVNL authority; they do NOT independently approve financial accounting postings."
    p.font.name = "Calibri"
    p.font.size = Pt(9)
    p.font.color.rgb = SLATE_700
    p.space_before = Pt(2)

    slide7.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 7 (MANPOWER MODEL):\n\n"
        "\"Slide 7 details our manpower deployment model. Enterprise implementations succeed or fail on the ground in the field.\n\n"
        "Our model has two synchronized components:\n"
        "First, a Central Specialist Team of 16.25 to 19.25 FTE at Ranchi HQ, covering Project Management, Solution Architecture, FICO, MM, PS, HCM, BASIS, ABAP, and dedicated Data Leads.\n\n"
        "Second, a massive Field Execution Team of 104 personnel stationed across the state: 14 Area Coordinators (2 per Area Board), 60 Circle Operators (4 per Electric Supply Circle), and 30 Store Operators (2 per Central Store). They handle the heavy lifting of clearing the 16-month voucher backlog, verifying store inventory, and training end users.\n\n"
        "For post-go-live stabilization, we retain a 20.75 to 21.5 FTE support pool—including all 14 Area Coordinators—for 12 full months. Peak staffing is over 120 people, fully dedicated to JBVNL.\""
    )
    print("Slide 7 generated.")

    # =========================================================================
    # SLIDE 8: COMMERCIAL COMPARISON & FINANCIAL BREAKDOWN
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, BG_LIGHT)
    add_header(slide8, "Budgetary Analysis & Financial Summary", "Commercial Comparison: Services Budget & Cost Levers", "Detailed, transparent breakdown of implementation, field staffing, support, and contingency reserves.")

    # Table Card
    add_card(slide8, Inches(0.8), Inches(1.65), Inches(11.733), Inches(4.55))

    # Add Native PowerPoint Table
    rows = 11
    cols = 4
    left = Inches(1.0)
    top = Inches(1.8)
    width = Inches(11.333)
    height = Inches(4.25)

    table_shape = slide8.shapes.add_table(rows, cols, left, top, width, height)
    tbl = table_shape.table

    # Column widths
    tbl.columns[0].width = Inches(4.5)  # Component
    tbl.columns[1].width = Inches(2.2)  # ECC (₹ Lakh)
    tbl.columns[2].width = Inches(2.2)  # S/4HANA (₹ Lakh)
    tbl.columns[3].width = Inches(2.433) # Remarks / Basis

    table_data = [
        ("Cost Component / Work Package", "Option 1: Existing ECC", "Option 2: S/4HANA Cloud", "Budgeting Basis & Parameters"),
        ("1. Central Implementation Team", "₹145.00 Lakh", "₹444.00 Lakh", "ECC: 16.25 FTE x 5m | S/4: 19.25 FTE x 12m"),
        ("2. Field Execution Staff (104 Staff)", "₹195.60 Lakh", "₹293.40 Lakh", "ECC: 4 months deploy | S/4: 6 months deploy"),
        ("3. Travel & Field Deployment Allowance", "₹20.00 Lakh", "₹35.00 Lakh", "Provisional actuals ceiling (15 Circles/Stores)"),
        ("Implementation Subtotal (A)", "₹360.60 Lakh", "₹772.40 Lakh", "Deliverable milestone-linked payment base"),
        ("4. Twelve-Month Post-Go-Live Support Pool", "₹266.70 Lakh", "₹290.70 Lakh", "ECC: 20.75 FTE/mo | S/4: 21.50 FTE/mo (12 mos)"),
        ("Total Services Subtotal (A + 4)", "₹627.30 Lakh", "₹1,063.10 Lakh", "Base professional services value"),
        ("5. Client Contingency Reserve (10%)", "₹62.73 Lakh", "₹106.31 Lakh", "Client-controlled reserve for authorized CRs"),
        ("TOTAL INDICATIVE SERVICES BUDGET", "₹690.03 Lakh (~₹6.90 Cr)", "₹1,169.41 Lakh (~₹11.69 Cr)", "All inclusive of services, field staff & reserve"),
        ("SAP Software Licences & Subscriptions", "Existing Licences / Audit", "Vendor Quote Required", "PCE & BTP Cloud BOM (per JUSNL reference)"),
        ("Hardware, Hosting, HANA DB & DR", "Existing Infrastructure", "Vendor Quote Required", "Sizing & cloud subscription required")
    ]

    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Calibri"
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE

            if r_idx == 0:
                p.font.size = Pt(9.5)
                p.font.bold = True
                p.font.color.rgb = WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY_ACCENT
            elif r_idx in [4, 6, 8]:
                p.font.size = Pt(9.5)
                p.font.bold = True
                if r_idx == 8:
                    p.font.color.rgb = BLUE_DARK
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(224, 242, 254)
                else:
                    p.font.color.rgb = SLATE_900
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(241, 245, 249)
            else:
                p.font.size = Pt(8.8)
                p.font.color.rgb = SLATE_700
                if r_idx % 2 == 1:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = WHITE
                else:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(248, 250, 252)

    # Bottom Sensitivity Levers
    add_card(slide8, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.78), bg_color=WHITE, border_color=SLATE_200)
    tb_bot = slide8.shapes.add_textbox(Inches(1.0), Inches(6.42), Inches(11.333), Inches(0.65))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = tf_bot.margin_bottom = 0

    p = tf_bot.paragraphs[0]
    p.text = "BUDGET SENSITIVITY & COST REDUCTION LEVERS"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK

    p = tf_bot.add_paragraph()
    p.text = "• Schedule Sensitivity: 1 extra month of full team execution adds ₹77.90L (ECC) or ₹85.90L (S/4). 1 extra support month adds ₹22.23L or ₹24.23L.\n• Scope Reduction Lever: Removing dedicated field store operators for 4 ECC months saves ₹54.00L, subject to measured field workload."
    p.font.name = "Calibri"
    p.font.size = Pt(8.8)
    p.font.color.rgb = SLATE_700
    p.space_before = Pt(2)

    slide8.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 8 (COMMERCIALS):\n\n"
        "\"Slide 8 presents the complete commercial breakdown.\n\n"
        "For Option 1 (Existing ECC): Central team is ₹145 lakh, field deployment is ₹195.60 lakh, and travel allowance is ₹20 lakh, giving an implementation subtotal of ₹360.60 lakh. Adding 12 months of post-go-live support at ₹266.70 lakh and a 10% client-controlled contingency of ₹62.73 lakh yields exactly ₹690.03 lakh, or approximately ₹6.90 crore.\n\n"
        "For Option 2 (S/4HANA): Central team for 12 months is ₹444 lakh, 6 months of field deployment is ₹293.40 lakh, and travel is ₹35 lakh, bringing implementation to ₹772.40 lakh. With 12 months of support at ₹290.70 lakh and 10% contingency of ₹106.31 lakh, the total indicative services budget is ₹1,169.41 lakh, or ₹11.69 crore.\n\n"
        "Both budgets include 10% contingency and 12 months of full support. Software licences, hosting, and statutory taxes are additional.\""
    )
    print("Slide 8 generated.")

    # =========================================================================
    # SLIDE 9: GOVERNANCE, ACCEPTANCE CRITERIA & PAYMENT MILESTONES
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, BG_LIGHT)
    add_header(slide9, "Accountability & Commercial Governance", "Governance, Acceptance Criteria & Payment Milestones", "Deliverable-linked payment gates, rigorous acceptance criteria, and balanced joint accountability.")

    # Left: Payment Milestones (Implementation Subtotal)
    col9_w = Inches(5.7)
    col9_h = Inches(4.55)
    col9_x = [Inches(0.8), Inches(6.833)]

    add_card(slide9, col9_x[0], Inches(1.68), col9_w, col9_h)
    tb_pm = slide9.shapes.add_textbox(col9_x[0] + Inches(0.22), Inches(1.8), col9_w - Inches(0.44), col9_h - Inches(0.24))
    tf_pm = tb_pm.text_frame
    tf_pm.word_wrap = True
    tf_pm.margin_left = tf_pm.margin_right = tf_pm.margin_top = tf_pm.margin_bottom = 0

    p = tf_pm.paragraphs[0]
    p.text = "DELIVERABLE-LINKED PAYMENT GATES"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SLATE_900

    p = tf_pm.add_paragraph()
    p.text = "Implementation Subtotal Linked to Verified Deliverables"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT
    p.space_after = Pt(4)

    milestones = [
        ("M1 · 10% Invoiced", "Mobilisation & Baseline", "Upon approved Readiness Audit Report, scope freeze, data inventory, and dependency register."),
        ("M2 · 20% Invoiced", "Design & Data Cleansing", "Upon business sign-off on target architecture, master data freeze, and opening balance reconciliation strategy."),
        ("M3 · 25% Invoiced", "Build & Mock Cutover", "Upon completion of system configuration, interface builds, and successful mock cutover execution."),
        ("M4 · 20% Invoiced", "Business UAT Acceptance", "Upon signed UAT by participating business heads and successful parallel payroll simulation."),
        ("M5 · 15% Invoiced", "Production Go-Live", "Upon formal go-live sign-off, live transaction posting, and declaration of system of record."),
        ("M6 · 10% Invoiced", "Hypercare Exit & Handover", "Upon 60-day hypercare stabilization, closure of critical defects, and support transition.")
    ]

    for code, title, desc in milestones:
        p = tf_pm.add_paragraph()
        p.text = f"▸ {code} — {title}: "
        p.font.name = "Calibri"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_before = Pt(3)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = SLATE_700

    p_post = tf_pm.add_paragraph()
    p_post.text = "Post-Go-Live Support (Months 6–17 / 13–24): Invoiced monthly in arrears against accepted service reports and SLA metrics."
    p_post.font.name = "Calibri"
    p_post.font.size = Pt(8.5)
    p_post.font.bold = True
    p_post.font.color.rgb = BLUE_DARK
    p_post.space_before = Pt(4)

    # Right: Acceptance Criteria & Joint Governance
    add_card(slide9, col9_x[1], Inches(1.68), col9_w, col9_h)
    tb_gov = slide9.shapes.add_textbox(col9_x[1] + Inches(0.22), Inches(1.8), col9_w - Inches(0.44), col9_h - Inches(0.24))
    tf_gov = tb_gov.text_frame
    tf_gov.word_wrap = True
    tf_gov.margin_left = tf_gov.margin_right = tf_gov.margin_top = tf_gov.margin_bottom = 0

    p = tf_gov.paragraphs[0]
    p.text = "ACCEPTANCE GATES & ACCOUNTABILITY"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SLATE_900

    p = tf_gov.add_paragraph()
    p.text = "Strict Entrance & Exit Criteria for Production"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT
    p.space_after = Pt(4)

    gov_points = [
        ("Opening Balance Reconciliation", "General Ledger control totals, asset registers, and sub-ledgers must tie out with signed Finance approval before cutover."),
        ("Zero Severity-1 Defects", "Zero blocking or critical functional defects open in UAT prior to scheduling cutover weekend."),
        ("Dual Parallel Payroll Runs", "SAP Payroll must match legacy manual/Excel payroll calculations within agreed variance thresholds across two consecutive runs."),
        ("Disaster Recovery & Rollback", "Verified database backup, restore drill, and documented rollback criteria approved prior to production cutover."),
        ("Joint Governance Cadence", "• Daily Standup: Command Centre & Field Coordinators\n• Weekly Operational Review: Project Managers & Business Owners\n• Fortnightly Steering Committee: Executive Sponsors & Leadership")
    ]

    for title, desc in gov_points:
        p = tf_gov.add_paragraph()
        p.text = f"▸ {title}: "
        p.font.name = "Calibri"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_before = Pt(3)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = SLATE_700

    # Bottom Invoicing Terms
    add_card(slide9, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.78), bg_color=WHITE, border_color=SLATE_200)
    tb_bot = slide9.shapes.add_textbox(Inches(1.0), Inches(6.42), Inches(11.333), Inches(0.65))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = tf_bot.margin_bottom = 0

    p = tf_bot.paragraphs[0]
    p.text = "COMMERCIAL INVOICING & PAYMENT TERMS"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK

    p = tf_bot.add_paragraph()
    p.text = "Invoices payable within 30 days of submission upon accepted milestone deliverables. Client business owners review submissions within 10 working days. Unresolved objections escalate to the Steering Committee. Zero automatic billing for delay."
    p.font.name = "Calibri"
    p.font.size = Pt(9)
    p.font.color.rgb = SLATE_700
    p.space_before = Pt(2)

    slide9.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 9 (GOVERNANCE & MILESTONES):\n\n"
        "\"Slide 9 establishes how JBVNL's financial investment is protected through milestone gating.\n\n"
        "Nothing is invoiced against promises or elapsed time. 100% of the implementation subtotal is distributed across six concrete delivery milestones:\n"
        "10% on Assessment, 20% on Design, 25% on Build & Mock Cutover, 20% on Business UAT sign-off, 15% on Production Go-Live, and 10% on 60-day Hypercare exit. The subsequent 12-month support is invoiced monthly in arrears against verified service reports.\n\n"
        "Our acceptance gates are non-negotiable: All opening balances must reconcile, zero Severity-1 defects can remain, and payroll must successfully pass two consecutive parallel runs against legacy systems.\""
    )
    print("Slide 9 generated.")

    # =========================================================================
    # SLIDE 10: STRATEGIC RECOMMENDATION, JUSNL ALIGNMENT & IMMEDIATE ACTIONS
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, BG_LIGHT)
    add_header(slide10, "Executive Guidance & Next Steps", "Strategic Recommendation, JUSNL BOM Alignment & Immediate Actions", "Guiding JBVNL's decision between ECC and S/4HANA with a structured 4-week mobilization plan.")

    # 3 Strategic Columns
    col10_w = Inches(3.68)
    col10_h = Inches(4.55)
    col10_x = [Inches(0.8), Inches(4.82), Inches(8.84)]

    # Col 1: Strategic Recommendation
    add_card(slide10, col10_x[0], Inches(1.68), col10_w, col10_h)
    tb_s1 = slide10.shapes.add_textbox(col10_x[0] + Inches(0.18), Inches(1.8), col10_w - Inches(0.36), col10_h - Inches(0.24))
    tf_s1 = tb_s1.text_frame
    tf_s1.word_wrap = True
    tf_s1.margin_left = tf_s1.margin_right = tf_s1.margin_top = tf_s1.margin_bottom = 0

    p = tf_s1.paragraphs[0]
    p.text = "STRATEGIC RECOMMENDATION"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT

    p = tf_s1.add_paragraph()
    p.text = "How JBVNL Should Choose"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SLATE_900
    p.space_after = Pt(4)

    rec_items = [
        ("Choose Option 1 (ECC) If", "• Priority is immediate go-live within 5 months to stop operational drift.\n• Current capex budget is restricted to ₹6.90 Crore.\n• Business accepts performing a future S/4HANA migration before end of 2027."),
        ("Choose Option 2 (S/4HANA) If", "• JBVNL seeks a modern, permanent platform supported until 2040+.\n• Avoiding double-migration costs and duplicate effort is prioritized.\n• Cloud agility, mobile Fiori apps, and BTP extensions are needed for power distribution."),
        ("Modernisation Imperative", "Even if ECC is selected, S/4HANA planning must begin in parallel. ECC mainstream support ends Dec 2027.")
    ]
    for title, desc in rec_items:
        p = tf_s1.add_paragraph()
        p.text = f"▸ {title}: "
        p.font.name = "Calibri"
        p.font.size = Pt(9.2)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_before = Pt(3)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = SLATE_700

    # Col 2: JUSNL BOM Alignment Checklist
    add_card(slide10, col10_x[1], Inches(1.68), col10_w, col10_h)
    tb_s2 = slide10.shapes.add_textbox(col10_x[1] + Inches(0.18), Inches(1.8), col10_w - Inches(0.36), col10_h - Inches(0.24))
    tf_s2 = tb_s2.text_frame
    tf_s2.word_wrap = True
    tf_s2.margin_left = tf_s2.margin_right = tf_s2.margin_top = tf_s2.margin_bottom = 0

    p = tf_s2.paragraphs[0]
    p.text = "JUSNL BOM RECONCILIATION"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT

    p = tf_s2.add_paragraph()
    p.text = "7-Point Pre-Contract Checklist"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SLATE_900
    p.space_after = Pt(4)

    bom_check = [
        ("1. User & FUE Validation", "Reconcile 136 FUE against active JBVNL user directory across circles."),
        ("2. HCM & Payroll Users", "Validate 715 headcount against JBVNL permanent & contractual rolls."),
        ("3. S/4HANA Private Cloud Edition", "Verify exact SAP SKU, hosting region, and 3-tier system availability."),
        ("4. BTP Cloud Credits", "Confirm credit tier for SCADA, PF portal, and supplier collaboration."),
        ("5. Digital Access & Documents", "Confirm 10k documents cover external billing/metering interface calls."),
        ("6. Disaster Recovery (DR)", "Validate RPO/RTO parameters and standby cloud infrastructure from Y2."),
        ("7. Commercial Exclusions", "Ensure taxes, SAP licensing, and hardware are contracted cleanly.")
    ]
    for title, desc in bom_check:
        p = tf_s2.add_paragraph()
        p.text = f"• {title}: "
        p.font.name = "Calibri"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_before = Pt(1.5)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = SLATE_700

    # Col 3: Immediate Next Steps (4-Week Mobilization)
    add_card(slide10, col10_x[2], Inches(1.68), col10_w, col10_h)
    tb_s3 = slide10.shapes.add_textbox(col10_x[2] + Inches(0.18), Inches(1.8), col10_w - Inches(0.36), col10_h - Inches(0.24))
    tf_s3 = tb_s3.text_frame
    tf_s3.word_wrap = True
    tf_s3.margin_left = tf_s3.margin_right = tf_s3.margin_top = tf_s3.margin_bottom = 0

    p = tf_s3.paragraphs[0]
    p.text = "IMMEDIATE ACTIONS"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT

    p = tf_s3.add_paragraph()
    p.text = "4-Week Mobilisation Plan"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SLATE_900
    p.space_after = Pt(4)

    next_steps = [
        ("Week 1 · Mobilise & Appoint", "Issue LOI, establish Command Centre at Ranchi HQ, and notify 7 Area & 15 Circle unit owners."),
        ("Week 2 · System & Backlog Audit", "Inspect ECC database health, audit interface endpoints, and quantify exact 16-month backlog volume."),
        ("Week 3 · BOM & Vendor Quotes", "Obtain official SAP India quote for PCE Cloud BOM; validate hosting & sizing options."),
        ("Week 4 · Decision Gate Sign-Off", "Present findings to Steering Committee; formally select Option 1 or Option 2; release implementation baseline.")
    ]
    for title, desc in next_steps:
        p = tf_s3.add_paragraph()
        p.text = f"▸ {title}: "
        p.font.name = "Calibri"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_before = Pt(3)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = SLATE_700

    # Bottom Final Proposition Banner
    add_card(slide10, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.78), bg_color=NAVY_DARK, border_color=None)
    tb_close = slide10.shapes.add_textbox(Inches(1.0), Inches(6.42), Inches(11.333), Inches(0.65))
    tf_close = tb_close.text_frame
    tf_close.word_wrap = True
    tf_close.margin_left = tf_close.margin_right = tf_close.margin_top = tf_close.margin_bottom = 0

    p = tf_close.paragraphs[0]
    p.text = "LUMBINI ELITE SOLUTIONS — YOUR ENTERPRISE SAP TRANSFORMATION PARTNER"
    p.font.name = "Calibri"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = RGBColor(56, 189, 248)

    p = tf_close.add_paragraph()
    p.text = "Backed by 13+ years of SAP delivery, CMMI Level 3 appraised engineering rigor, and deep public utility experience (JBVNL, TVNL, MOIL, BHEL). We are ready to mobilise within 10 days of authorization."
    p.font.name = "Calibri"
    p.font.size = Pt(9.2)
    p.font.color.rgb = WHITE
    p.space_before = Pt(2)

    slide10.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 10 (RECOMMENDATIONS & NEXT STEPS):\n\n"
        "\"To conclude, JBVNL stands at an important strategic juncture.\n\n"
        "If immediate operational stabilization and capital containment are the top mandates, choose Option 1: Live ECC in 5 months for ₹6.90 crore.\n\n"
        "If building a modern, cloud-native digital utility supported to 2040+ is the mandate, choose Option 2: S/4HANA Private Cloud in 12 months for ₹11.69 crore.\n\n"
        "Regardless of the path chosen, our recommended immediate next step is identical: Authorize the 4-week mobilization assessment. We will audit the technical baseline, freeze circle locations, reconcile the JUSNL Cloud BOM, and present the Steering Committee with a zero-risk delivery baseline.\n\n"
        "Lumbini Elite Solutions brings over 13 years of SAP experience, CMMI Level 3 quality controls, and proven Jharkhand utility experience. We are ready to mobilize within 10 days. Thank you, and we welcome your questions.\""
    )
    print("Slide 10 generated.")

    output_path = "JBVNL_SAP_GoLive_and_Modernisation_Proposal.pptx"
    prs.save(output_path)
    print(f"\nSuccessfully generated and saved: {output_path}")
    print(f"Total slides count: {len(prs.slides)}")

if __name__ == "__main__":
    build_jbvnl_deck()
