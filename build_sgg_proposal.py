import os, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_sgg_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]

    # Executive Color Palette (Aligned with Elitia & Lumbini Enterprise Standards)
    NAVY_DARK = RGBColor(10, 25, 47)        # #0A192F Dark Hero Canvas
    NAVY_ACCENT = RGBColor(15, 35, 65)      # #0F2341 Header / Dark Cards
    NAVY_SURFACE = RGBColor(23, 42, 69)     # #172A45 Surface containers
    SLATE_900 = RGBColor(15, 23, 42)        # #0F172A Primary typography
    SLATE_700 = RGBColor(51, 65, 85)        # #334155 Body typography
    SLATE_500 = RGBColor(100, 116, 139)     # #64748B Secondary / Muted
    SLATE_200 = RGBColor(226, 232, 240)     # #E2E8F0 Subtle borders
    BG_LIGHT = RGBColor(248, 250, 252)      # #F8FAFC Clean slide canvas
    WHITE = RGBColor(255, 255, 255)
    ELITIA_BLUE = RGBColor(8, 88, 156)      # #08589C Primary Elitia Blue
    CYAN_ACCENT = RGBColor(2, 132, 199)     # #0284C7 Executive Blue
    BLUE_ACCENT = RGBColor(2, 132, 199)     # Alias for Executive Blue
    TEAL_ACCENT = RGBColor(27, 127, 121)    # #1B7F79 Operations & Data Teal
    AMBER_ACCENT = RGBColor(217, 119, 6)    # #D97706 Governance / Highlight

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, tracker, title, subtitle):
        # Tracker Category Pill
        tr_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.733), Inches(0.26))
        tf_tr = tr_box.text_frame
        tf_tr.word_wrap = True
        tf_tr.margin_left = tf_tr.margin_right = tf_tr.margin_top = tf_tr.margin_bottom = 0
        p_tr = tf_tr.paragraphs[0]
        p_tr.text = tracker.upper()
        p_tr.font.name = "Calibri"
        p_tr.font.size = Pt(9.5)
        p_tr.font.bold = True
        p_tr.font.color.rgb = CYAN_ACCENT

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
    # SLIDE 1: COVER (PREMIUM CXO DARK CONSULTING HERO)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, NAVY_DARK)

    # Lumbini Logo
    if os.path.exists("assets/lumbini_logo.png"):
        try:
            slide1.shapes.add_picture("assets/lumbini_logo.png", Inches(0.9), Inches(0.75), Inches(2.7), Inches(0.82))
        except:
            pass

    # Left Column: Strategic Title & Metadata
    # Category Pill / Kicker
    add_card(slide1, Inches(0.9), Inches(1.95), Inches(4.6), Inches(0.36), bg_color=NAVY_ACCENT, border_color=BLUE_ACCENT)
    tb_kicker = slide1.shapes.add_textbox(Inches(1.05), Inches(1.98), Inches(4.3), Inches(0.30))
    tf_k = tb_kicker.text_frame
    tf_k.word_wrap = True
    tf_k.margin_left = tf_k.margin_right = tf_k.margin_top = tf_k.margin_bottom = 0
    pk = tf_k.paragraphs[0]
    pk.text = "SAEED GODHARAN GROUP (SGG)  ·  EXECUTIVE PROPOSAL"
    pk.font.name = "Calibri"
    pk.font.size = Pt(9.5)
    pk.font.bold = True
    pk.font.color.rgb = RGBColor(56, 189, 248)

    # Main Proposal Title
    t_box1 = slide1.shapes.add_textbox(Inches(0.9), Inches(2.45), Inches(7.3), Inches(1.8))
    tf1 = t_box1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0

    p_main = tf1.paragraphs[0]
    p_main.text = "SGG – Enterprise Business Intelligence & Odoo Enhancement Proposal"
    p_main.font.name = "Calibri"
    p_main.font.size = Pt(30)
    p_main.font.bold = True
    p_main.font.color.rgb = WHITE
    p_main.space_before = Pt(2)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Centralized Insights  |  Improved ERP Experience  |  Connected Business Processes"
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(13.5)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_before = Pt(10)

    # Executive Context Container (Bottom Left)
    add_card(slide1, Inches(0.9), Inches(4.80), Inches(7.3), Inches(1.95), bg_color=NAVY_ACCENT, border_color=RGBColor(30, 58, 138))
    ctx_box = slide1.shapes.add_textbox(Inches(1.1), Inches(4.95), Inches(6.9), Inches(1.65))
    tf_ctx = ctx_box.text_frame
    tf_ctx.word_wrap = True
    tf_ctx.margin_left = tf_ctx.margin_right = tf_ctx.margin_top = tf_ctx.margin_bottom = 0

    pc1 = tf_ctx.paragraphs[0]
    pc1.text = "STRATEGIC ENTERPRISE TRANSFORMATION INITIATIVE"
    pc1.font.name = "Calibri"
    pc1.font.size = Pt(9.5)
    pc1.font.bold = True
    pc1.font.color.rgb = RGBColor(56, 189, 248)

    pc2 = tf_ctx.add_paragraph()
    pc2.text = "• Prepared for: Executive Leadership & Management  ·  Saeed Godharan Group (SGG)"
    pc2.font.name = "Calibri"
    pc2.font.size = Pt(10)
    pc2.font.bold = True
    pc2.font.color.rgb = WHITE
    pc2.space_before = Pt(4)

    pc3 = tf_ctx.add_paragraph()
    pc3.text = "• Prepared by: Lumbini Elite Solutions & Services Pvt. Ltd. (Lumbini Elite Group)"
    pc3.font.name = "Calibri"
    pc3.font.size = Pt(10)
    pc3.font.bold = True
    pc3.font.color.rgb = WHITE
    pc3.space_before = Pt(2)

    pc4 = tf_ctx.add_paragraph()
    pc4.text = "• Proposed Solution: ELITIA BI & Odoo Core Modernization Suite"
    pc4.font.name = "Calibri"
    pc4.font.size = Pt(9.5)
    pc4.font.color.rgb = RGBColor(203, 213, 225)
    pc4.space_before = Pt(2)

    pc5 = tf_ctx.add_paragraph()
    pc5.text = "• Proposal Date: November 2026  ·  Confidential Client Briefing"
    pc5.font.name = "Calibri"
    pc5.font.size = Pt(9.5)
    pc5.font.color.rgb = RGBColor(203, 213, 225)
    pc5.space_before = Pt(2)

    # Right Column: 4 Strategic Pillars Card
    add_card(slide1, Inches(8.5), Inches(1.0), Inches(4.0), Inches(5.75), bg_color=NAVY_ACCENT, border_color=RGBColor(30, 58, 138))
    tb_rp = slide1.shapes.add_textbox(Inches(8.75), Inches(1.2), Inches(3.5), Inches(5.35))
    tf_rp = tb_rp.text_frame
    tf_rp.word_wrap = True
    tf_rp.margin_left = tf_rp.margin_right = tf_rp.margin_top = tf_rp.margin_bottom = 0

    p_rp_k = tf_rp.paragraphs[0]
    p_rp_k.text = "TRANSFORMATION ARCHITECTURE"
    p_rp_k.font.name = "Calibri"
    p_rp_k.font.size = Pt(9.5)
    p_rp_k.font.bold = True
    p_rp_k.font.color.rgb = RGBColor(56, 189, 248)

    p_rp_t = tf_rp.add_paragraph()
    p_rp_t.text = "Four Integrated Workstreams"
    p_rp_t.font.name = "Calibri"
    p_rp_t.font.size = Pt(14)
    p_rp_t.font.bold = True
    p_rp_t.font.color.rgb = WHITE
    p_rp_t.space_before = Pt(2)
    p_rp_t.space_after = Pt(6)

    pillars = [
        ("A. ELITIA BI Platform", "Centralized executive cockpits, departmental views (Finance, HR, SCM) & transaction-level drill-through."),
        ("B. Odoo Health Check & UI/UX", "Comprehensive workflow audit, form simplification, and forward-readiness for Odoo v20 (2027)."),
        ("C. Resort ERP Data Migration", "6-stage structured extraction via Excel, profiling, automated cleansing, and balance reconciliation."),
        ("D. Payroll & WPS Integration", "Biometric terminal punch ingestion, timesheet validation rules, and automated regional bank WPS file generation.")
    ]

    for p_name, p_desc in pillars:
        p = tf_rp.add_paragraph()
        p.text = f"▸ {p_name}"
        p.font.name = "Calibri"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = RGBColor(56, 189, 248)
        p.space_before = Pt(6)

        p = tf_rp.add_paragraph()
        p.text = p_desc
        p.font.name = "Calibri"
        p.font.size = Pt(8.5)
        p.font.color.rgb = RGBColor(203, 213, 225)
        p.space_before = Pt(1)

    p_foot = tf_rp.add_paragraph()
    p_foot.text = "Positioning: End-to-End Transformation Partner"
    p_foot.font.name = "Calibri"
    p_foot.font.size = Pt(8.5)
    p_foot.font.italic = True
    p_foot.font.color.rgb = RGBColor(148, 163, 184)
    p_foot.space_before = Pt(8)

    slide1.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 1 (COVER):\n\n"
        "\"Good morning, esteemed leadership team of Saeed Godharan Group (SGG). On behalf of Lumbini Elite Solutions, we are pleased to present our comprehensive business and technology transformation proposal.\n\n"
        "Our objective today is to share an integrated roadmap combining ELITIA BI for centralized executive intelligence, an in-depth Odoo ERP Health Check and UI/UX audit, structured legacy Resort ERP data migration, and automated biometric payroll integration with compliant WPS file generation.\n\n"
        "We position ourselves not merely as software implementers or staffing providers, but as an end-to-end technology partner dedicated to unlocking full visibility and seamless operational performance across SGG's business units.\""
    )
    print("Slide 1: Cover generated.")

    # =========================================================================
    # SLIDE 2: UNDERSTANDING SGG'S BUSINESS REQUIREMENTS
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, BG_LIGHT)
    add_header(slide2, "Strategic Discovery & Business Context", "Understanding SGG's Core Business Requirements", "Connecting existing operational challenges to measurable enterprise transformation outcomes.")

    # 4 Key Pillars Side-by-Side (Challenges vs. Desired Outcomes)
    c2_w = Inches(2.78)
    c2_h = Inches(4.55)
    c2_x = [Inches(0.8), Inches(3.784), Inches(6.768), Inches(9.752)]

    req_data = [
        {
            "num": "REQUIREMENT 01",
            "title": "Centralized Business Intelligence",
            "color": ELITIA_BLUE,
            "challenges": [
                "Business information is fragmented across departments and entities.",
                "Management lacks single-pane consolidated visibility across business units.",
                "Reporting relies on manual spreadsheet extraction with delayed reporting cycles."
            ],
            "outcomes": [
                "Unified executive cockpits reading directly from the Odoo ERP core.",
                "Multi-entity drill-down from summary KPIs down to transaction records.",
                "Faster month-end financial and operational decision-making."
            ]
        },
        {
            "num": "REQUIREMENT 02",
            "title": "Odoo Health Check & UI/UX Audit",
            "color": TEAL_ACCENT,
            "challenges": [
                "End-users experience usability friction and complex screen layouts.",
                "Unoptimized navigation workflows slow down daily operational processing.",
                "Functional gaps and custom workarounds create user adoption hurdles."
            ],
            "outcomes": [
                "Comprehensive health check auditing workflows, database, and configurations.",
                "Streamlined screen layouts reducing user clicks and data entry errors.",
                "Prioritized enhancement roadmap preparing for future upgrade stability."
            ]
        },
        {
            "num": "REQUIREMENT 03",
            "title": "Resort ERP Data Migration",
            "color": CYAN_ACCENT,
            "challenges": [
                "Valuable historical operational data remains isolated in legacy Resort ERP.",
                "Missing data prevents historical trend analysis and unified record tracking.",
                "Risk of data duplication and inconsistent data structures between systems."
            ],
            "outcomes": [
                "Structured extraction of legacy historical data via standardized Excel files.",
                "Rigorous profiling, automated cleansing, and verified schema mapping.",
                "Reconciled loading into Odoo ensuring single-source-of-truth continuity."
            ]
        },
        {
            "num": "REQUIREMENT 04",
            "title": "Automated Payroll & Attendance",
            "color": AMBER_ACCENT,
            "challenges": [
                "Biometric device attendance data is disconnected from Odoo payroll.",
                "Manual compilation of timesheets, shift exceptions, and overtime hours.",
                "Administrative delays and compliance risks during monthly WPS bank file preparation."
            ],
            "outcomes": [
                "Automated ingestion pipeline from biometric devices to timesheet validation.",
                "Direct synchronization with Odoo payroll salary rules and deductions.",
                "Standardized, validated WPS salary file generation for bank upload."
            ]
        }
    ]

    for idx, r in enumerate(req_data):
        cx = c2_x[idx]
        add_card(slide2, cx, Inches(1.68), c2_w, c2_h)

        tb = slide2.shapes.add_textbox(cx + Inches(0.14), Inches(1.8), c2_w - Inches(0.28), c2_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = r["num"]
        p.font.name = "Calibri"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = r["color"]

        p = tf.add_paragraph()
        p.text = r["title"]
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = SLATE_900
        p.space_after = Pt(4)

        p = tf.add_paragraph()
        p.text = "CURRENT CHALLENGES:"
        p.font.name = "Calibri"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = SLATE_500
        p.space_before = Pt(2)

        for c in r["challenges"]:
            p = tf.add_paragraph()
            p.text = f"• {c}"
            p.font.name = "Calibri"
            p.font.size = Pt(8.2)
            p.font.color.rgb = SLATE_700
            p.space_before = Pt(1.5)

        p = tf.add_paragraph()
        p.text = "DESIRED OUTCOMES:"
        p.font.name = "Calibri"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_before = Pt(6)

        for o in r["outcomes"]:
            p = tf.add_paragraph()
            p.text = f"✓ {o}"
            p.font.name = "Calibri"
            p.font.size = Pt(8.2)
            p.font.color.rgb = SLATE_700
            p.space_before = Pt(1.5)

    # Bottom Summary
    add_card(slide2, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.78), bg_color=WHITE, border_color=SLATE_200)
    tb_bot = slide2.shapes.add_textbox(Inches(1.0), Inches(6.42), Inches(11.333), Inches(0.65))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = tf_bot.margin_bottom = 0

    p = tf_bot.paragraphs[0]
    p.text = "STRATEGIC IMPERATIVE FOR SAEED GODHARAN GROUP"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    p = tf_bot.add_paragraph()
    p.text = "SGG's requirements form an interconnected digital lifecycle: Cleansing legacy data and streamlining Odoo workflows creates trusted operational transactions, which in turn feed automated payroll processing and empower executive leadership with real-time, centralized ELITIA BI intelligence."
    p.font.name = "Calibri"
    p.font.size = Pt(9)
    p.font.color.rgb = SLATE_700
    p.space_before = Pt(2)

    slide2.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 2 (REQUIREMENTS):\n\n"
        "\"To architect the right solution, we began by analyzing SGG's current operating landscape across four vital dimensions.\n\n"
        "First, Business Intelligence: Leadership needs consolidated executive visibility across multiple business units without relying on tedious, error-prone manual spreadsheets.\n\n"
        "Second, Odoo Usability: End-users are experiencing friction with complex screens and navigation flows in the current Odoo deployment, which hinders adoption and speed.\n\n"
        "Third, Historical Data: Valuable operational history is still trapped inside legacy Resort ERP, leaving data gaps in Odoo.\n\n"
        "Fourth, Time-to-Pay: Biometric punch records and timesheets are not automated into Odoo payroll, creating end-of-month administrative pressure and manual WPS preparation.\n\n"
        "Our proposal directly addresses these challenges with four complementary, synchronized workstreams.\""
    )
    print("Slide 2: Requirements generated.")

    # =========================================================================
    # SLIDE 3: PROPOSED SOLUTION OVERVIEW
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, BG_LIGHT)
    add_header(slide3, "Integrated Transformation Architecture", "Proposed Solution Overview: Four Harmonized Workstreams", "A cohesive engagement model establishing a resilient ERP core and real-time executive visibility.")

    # 4 Workstream Cards (2x2 Grid)
    w3_w = Inches(5.7)
    w3_h = Inches(2.2)
    w3_x = [Inches(0.8), Inches(6.833)]
    w3_y = [Inches(1.68), Inches(4.02)]

    workstreams = [
        {
            "tag": "WORKSTREAM A · ANALYTICS & INSIGHTS",
            "title": "ELITIA BI Platform Deployment",
            "color": ELITIA_BLUE,
            "desc": "Centralized business intelligence layer reading directly from Odoo ERP and operational data stores.",
            "bullets": [
                "Executive Command Center: Multi-entity consolidated cockpits with high-level KPI strips.",
                "Departmental Dashboards: Dedicated views for Finance, HR, Supply Chain, and Operations.",
                "Depth on Demand: In-memory drill-through from summary KPIs to granular transaction documents.",
                "Audit-Ready Analytics: Transparent metric logic with automated Explain Change variance analysis."
            ]
        },
        {
            "tag": "WORKSTREAM B · CORE SYSTEM OPTIMIZATION",
            "title": "Odoo Health Check & UI/UX Audit",
            "color": TEAL_ACCENT,
            "desc": "Systematic diagnostic review of SGG's existing Odoo ERP environment, configurations, and workflows.",
            "bullets": [
                "Workflow Optimization: Removing navigation bottlenecks across core functional modules.",
                "UI/UX Simplification: Streamlining cluttered data-entry screens to improve user adoption.",
                "Technical Architecture Audit: Database index checks, module integrity, and custom code review.",
                "Prioritized Roadmap: Clear separation of immediate quick-wins versus strategic enhancements."
            ]
        },
        {
            "tag": "WORKSTREAM C · DATA CONTINUITY",
            "title": "Resort ERP to Odoo Data Migration",
            "color": CYAN_ACCENT,
            "desc": "Structured extraction, cleansing, mapping, and controlled loading of legacy historical data into Odoo.",
            "bullets": [
                "Excel-Based Ingestion: Standardized templates to safely extract data from Resort ERP.",
                "Automated Cleansing: Deduplication, missing field imputation, and data quality profiling.",
                "Field-to-Model Mapping: Aligning legacy resort records into Odoo partner, product, and GL schemas.",
                "Reconciliation Sign-Off: Audited control totals ensuring zero balance discrepancies."
            ]
        },
        {
            "tag": "WORKSTREAM D · OPERATIONAL AUTOMATION",
            "title": "Automated Payroll & Biometric Integration",
            "color": AMBER_ACCENT,
            "desc": "Seamless connectivity from frontline biometric attendance devices into Odoo payroll and WPS files.",
            "bullets": [
                "Biometric Telemetry Ingestion: Direct synchronization from fingerprint / facial recognition terminals.",
                "Timesheet Validation Engine: Automated shift allocation, overtime calculation, and leave reconciliation.",
                "Odoo Payroll Synchronization: Direct feeding into monthly salary rules and deduction structures.",
                "WPS File Generator: Validated electronic salary file creation compliant with regional bank formats."
            ]
        }
    ]

    for idx, w in enumerate(workstreams):
        rx = idx % 2
        ry = idx // 2
        cx = w3_x[rx]
        cy = w3_y[ry]

        add_card(slide3, cx, cy, w3_w, w3_h)

        tb = slide3.shapes.add_textbox(cx + Inches(0.2), cy + Inches(0.12), w3_w - Inches(0.4), w3_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = w["tag"]
        p.font.name = "Calibri"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = w["color"]

        p = tf.add_paragraph()
        p.text = w["title"]
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = SLATE_900

        p = tf.add_paragraph()
        p.text = w["desc"]
        p.font.name = "Calibri"
        p.font.size = Pt(8.8)
        p.font.color.rgb = SLATE_500
        p.space_after = Pt(2)

        for b in w["bullets"]:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.name = "Calibri"
            p.font.size = Pt(8.3)
            p.font.color.rgb = SLATE_700
            p.space_before = Pt(1)

    # Bottom Callout: Synergistic Architecture
    add_card(slide3, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.78), bg_color=WHITE, border_color=SLATE_200)
    tb_bot = slide3.shapes.add_textbox(Inches(1.0), Inches(6.42), Inches(11.333), Inches(0.65))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = tf_bot.margin_bottom = 0

    p = tf_bot.paragraphs[0]
    p.text = "HOW THE FOUR WORKSTREAMS REINFORCE EACH OTHER"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    p = tf_bot.add_paragraph()
    p.text = "Workstreams B & C establish a clean, complete, and user-friendly Odoo ERP transactional foundation. Workstream D automates high-volume frontline payroll data. Workstream A sits on top as the centralized intelligence layer, turning operational data into actionable executive decisions."
    p.font.name = "Calibri"
    p.font.size = Pt(9)
    p.font.color.rgb = SLATE_700
    p.space_before = Pt(2)

    slide3.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 3 (SOLUTION OVERVIEW):\n\n"
        "\"Slide 3 demonstrates how our proposed solution functions as an integrated ecosystem rather than isolated fixes.\n\n"
        "In Workstream B, we conduct an Odoo ERP Health Check to eliminate daily navigation bottlenecks and streamline UI/UX. In Workstream C, we extract and cleanse legacy data from Resort ERP, bringing missing history into Odoo.\n\n"
        "In Workstream D, we automate biometric punch capture and timesheet reconciliation directly into Odoo payroll, generating bank-ready WPS files.\n\n"
        "Finally, in Workstream A, ELITIA BI connects to this robust Odoo foundation, delivering centralized multi-entity dashboards and drill-down capability for executive management.\""
    )
    print("Slide 3: Solution Overview generated.")

    # =========================================================================
    # SLIDE 4: ELITIA BI: CENTRALIZED BUSINESS INTELLIGENCE
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, BG_LIGHT)
    add_header(slide4, "Primary Analytics Positioning", "ELITIA BI: Centralized Intelligence & Decision Cockpits", "Deploying a governed, source-agnostic semantic layer over Odoo ERP for end-to-end visibility.")

    # Top Conceptual Architecture Flow (Odoo -> Integration -> Semantic Layer -> Dashboards -> Insights)
    add_card(slide4, Inches(0.8), Inches(1.68), Inches(11.733), Inches(1.15), bg_color=WHITE, border_color=SLATE_200)
    tb_flow = slide4.shapes.add_textbox(Inches(1.0), Inches(1.78), Inches(11.333), Inches(0.95))
    tf_flow = tb_flow.text_frame
    tf_flow.word_wrap = True
    tf_flow.margin_left = tf_flow.margin_right = tf_flow.margin_top = tf_flow.margin_bottom = 0

    p = tf_flow.paragraphs[0]
    p.text = "CONCEPTUAL DATA FLOW: FROM ODOO TRANSACTIONS TO EXECUTIVE INSIGHT"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = ELITIA_BLUE

    p = tf_flow.add_paragraph()
    p.text = "Odoo ERP Core Data  ➔  Governed Data Extraction  ➔  ELITIA BI Semantic Layer  ➔  Departmental Cockpits  ➔  Executive Insights"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = SLATE_900
    p.space_before = Pt(3)

    p = tf_flow.add_paragraph()
    p.text = "Operational tables in Odoo (Invoices, Orders, Payroll, Inventory) are mapped into ELITIA BI's single semantic catalog, ensuring metrics are calculated identically everywhere without altering the ERP database."
    p.font.name = "Calibri"
    p.font.size = Pt(8.8)
    p.font.color.rgb = SLATE_700
    p.space_before = Pt(2)

    # 4 Product Capability Cards (Bottom Grid)
    c4_w = Inches(2.78)
    c4_h = Inches(3.35)
    c4_x = [Inches(0.8), Inches(3.784), Inches(6.768), Inches(9.752)]

    bi_caps = [
        {
            "title": "Finance & P&L Intelligence",
            "tag": "FINANCIAL VISIBILITY",
            "bullets": [
                "Net revenue, EBITDA, operating expenses, and gross margin trends.",
                "Accounts receivable aging, Days Sales Outstanding (DSO), and cash flow tracking.",
                "P&L waterfall bridge from gross billing to net operating margin.",
                "Departmental cost vs. budget variance heatmaps with anomaly detection."
            ]
        },
        {
            "title": "HR & Workforce Analytics",
            "tag": "PEOPLE & ATTENDANCE",
            "bullets": [
                "Total workforce headcount, turnover rates, and departmental distribution.",
                "Biometric attendance tracking, absenteeism, and shift coverage rates.",
                "Monthly overtime trends, cost distribution, and variance alerts.",
                "Departmental labor cost allocations tied directly to Odoo payroll."
            ]
        },
        {
            "title": "Supply Chain & Procurement",
            "tag": "OPERATIONS & INVENTORY",
            "bullets": [
                "Stock cover days, inventory valuation, and slow-moving stock aging.",
                "Purchase order cycle times, approval lag, and vendor spend Pareto.",
                "Supplier On-Time In-Full (OTIF) fulfillment and lead-time tracking.",
                "Procurement contract compliance and purchase price variance."
            ]
        },
        {
            "title": "Executive Depth on Demand",
            "tag": "MULTI-TIER DRILL-DOWN",
            "bullets": [
                "Multi-Entity Rollup: Consolidated performance across all SGG business units.",
                "Decomposition Tree: Drill into any KPI by division, department, or cost center.",
                "Underlying Records: Click any chart to view source Odoo document line items.",
                "Explain Change: Deterministic analysis answering why metrics moved."
            ]
        }
    ]

    for idx, c in enumerate(bi_caps):
        cx = c4_x[idx]
        add_card(slide4, cx, Inches(2.95), c4_w, c4_h)

        tb = slide4.shapes.add_textbox(cx + Inches(0.14), Inches(3.08), c4_w - Inches(0.28), c4_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = c["tag"]
        p.font.name = "Calibri"
        p.font.size = Pt(8)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT

        p = tf.add_paragraph()
        p.text = c["title"]
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = SLATE_900
        p.space_after = Pt(4)

        for b in c["bullets"]:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.name = "Calibri"
            p.font.size = Pt(8.2)
            p.font.color.rgb = SLATE_700
            p.space_before = Pt(2)

    # Bottom Architectural Guardrail
    add_card(slide4, Inches(0.8), Inches(6.42), Inches(11.733), Inches(0.72), bg_color=WHITE, border_color=SLATE_200)
    tb_bot = slide4.shapes.add_textbox(Inches(1.0), Inches(6.48), Inches(11.333), Inches(0.58))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = tf_bot.margin_bottom = 0

    p = tf_bot.paragraphs[0]
    p.text = "PRODUCT FIDELITY GUARANTEE: GROUNDED IN ACTUAL ELITIA BI CAPABILITIES"
    p.font.name = "Calibri"
    p.font.size = Pt(9.2)
    p.font.bold = True
    p.font.color.rgb = NAVY_ACCENT

    p = tf_bot.add_paragraph()
    p.text = "ELITIA BI utilizes a single governed semantic layer (Zod-validated SQL queries, role-based security, and in-memory caching) that separates data logic from UI rendering. It guarantees that numbers mean the same thing across every dashboard."
    p.font.name = "Calibri"
    p.font.size = Pt(8.8)
    p.font.color.rgb = SLATE_700
    p.space_before = Pt(2)

    slide4.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 4 (ELITIA BI POSITIONING):\n\n"
        "\"Slide 4 highlights our primary product offering: ELITIA BI.\n\n"
        "Rather than building brittle, disconnected reports, ELITIA BI connects to SGG's Odoo ERP via a governed semantic layer. This ensures that metrics like Net Revenue, Overtime, or Inventory Days have one unified, auditable calculation rule across the entire organization.\n\n"
        "Our product delivers 'Depth on Demand': An executive sees a high-level KPI card; clicking it opens a dimensional breakdown by business unit or department; clicking further displays the exact underlying Odoo transaction records.\n\n"
        "With dedicated modules for Finance, HR, Supply Chain, and multi-entity executive rollups, leadership gains real-time observability over business performance.\""
    )
    print("Slide 4: ELITIA BI generated.")

    # =========================================================================
    # SLIDE 5: EXECUTIVE REPORTING & BUSINESS VISIBILITY
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, BG_LIGHT)
    add_header(slide5, "Stakeholder Information Architecture", "Multi-Tier Executive Reporting & Visibility Framework", "Delivering tailored intelligence from board-level summaries down to frontline operational transactions.")

    # 3 Stakeholder Tier Columns (Executive Management, Department Heads, Operational Teams)
    c5_w = Inches(3.68)
    c5_h = Inches(4.55)
    c5_x = [Inches(0.8), Inches(4.82), Inches(8.84)]

    tiers = [
        {
            "level": "TIER 01 · STRATEGIC",
            "title": "Executive Management (C-Suite)",
            "focus": "Macro Business Health & Capital Visibility",
            "color": ELITIA_BLUE,
            "bullets": [
                "Consolidated Multi-Unit P&L: Consolidated revenue, EBITDA margin, and net profit across all SGG business divisions.",
                "Cash & Liquidity Monitor: Real-time cash balances, rolling cash runway, and working capital exposure.",
                "Strategic KPI Strip: High-level metric pulses (Revenue vs. Budget, Receivables, Headcount, Fulfillment SLA).",
                "Explain Change Variance: One-click contribution analysis identifying why margins or expenses moved across entities."
            ],
            "benefit": "Enables proactive strategic governance, capital allocation, and rapid board reporting."
        },
        {
            "level": "TIER 02 · TACTICAL",
            "title": "Department Heads & GMs",
            "focus": "Operational Performance & Exception Control",
            "color": TEAL_ACCENT,
            "bullets": [
                "Finance Controllers: Receivables aging (0-30, 31-60, 90+ days), payables schedule, and budget variance heatmaps.",
                "HR Directors: Departmental attendance rates, overtime budget burn, shift coverage, and turnover ratios.",
                "Supply Chain Managers: Inventory turnover, stock-out risk radar, purchase order cycle time, and vendor OTIF scorecards.",
                "Automated Anomaly Alerts: Pulsing alert indicators when metrics deviate more than 3% from operational plan."
            ],
            "benefit": "Accelerates operational problem-solving and cross-functional accountability."
        },
        {
            "level": "TIER 03 · OPERATIONAL",
            "title": "Operational Teams & Supervisors",
            "focus": "Actionable Registers & Detailed Transactions",
            "color": CYAN_ACCENT,
            "bullets": [
                "Accounting Staff: Actionable unpaid invoice registers, customer ledger reconciliation, and bank discrepancy logs.",
                "Payroll Officers: Daily biometric punch validation, unapproved overtime logs, and missing timesheet alerts.",
                "Warehouse Officers: Specific SKU stock replenishment alerts, pending delivery instructions, and gate-pass audits.",
                "Virtual Records Drill: Instant one-click copy of document numbers with direct drill into Odoo source screens."
            ],
            "benefit": "Eliminates daily spreadsheet chaos and automates administrative routines."
        }
    ]

    for idx, t in enumerate(tiers):
        cx = c5_x[idx]
        add_card(slide5, cx, Inches(1.68), c5_w, c5_h)

        tb = slide5.shapes.add_textbox(cx + Inches(0.18), Inches(1.8), c5_w - Inches(0.36), c5_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = t["level"]
        p.font.name = "Calibri"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = t["color"]

        p = tf.add_paragraph()
        p.text = t["title"]
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = SLATE_900

        p = tf.add_paragraph()
        p.text = t["focus"]
        p.font.name = "Calibri"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = SLATE_500
        p.space_after = Pt(4)

        for b in t["bullets"]:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.name = "Calibri"
            p.font.size = Pt(8.2)
            p.font.color.rgb = SLATE_700
            p.space_before = Pt(2)

        p = tf.add_paragraph()
        p.text = "Strategic Value:"
        p.font.name = "Calibri"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = t["benefit"]
        p.font.name = "Calibri"
        p.font.size = Pt(8.2)
        p.font.color.rgb = CYAN_ACCENT

    # Bottom Clarification Banner
    add_card(slide5, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.78), bg_color=WHITE, border_color=SLATE_200)
    tb_bot = slide5.shapes.add_textbox(Inches(1.0), Inches(6.42), Inches(11.333), Inches(0.65))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = tf_bot.margin_bottom = 0

    p = tf_bot.paragraphs[0]
    p.text = "GOVERNANCE NOTICE: ILLUSTRATIVE KPIS VS. CONFIRMED PLATFORM CAPABILITY"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT

    p = tf_bot.add_paragraph()
    p.text = "The reporting areas and KPIs listed above represent proven architectural patterns. Final metric formulas, dashboard wireframes, and authorization roles will be mapped and agreed during the Discovery Phase based on SGG's specific chart of accounts and operational hierarchy."
    p.font.name = "Calibri"
    p.font.size = Pt(9)
    p.font.color.rgb = SLATE_700
    p.space_before = Pt(2)

    slide5.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 5 (REPORTING TIERS):\n\n"
        "\"Slide 5 illustrates how different stakeholders across Saeed Godharan Group will interact with the new reporting environment.\n\n"
        "At the Executive Tier, the C-Suite and Board access consolidated business unit performance, cash flow trends, and high-level margin pulses.\n\n"
        "At the Departmental Tier, functional leaders in Finance, HR, and Supply Chain monitor budget variances, overtime trends, and vendor fulfillment scorecards with automated alert dots.\n\n"
        "At the Operational Tier, frontline supervisors receive actionable registers—such as unposted biometric punches or aging invoices—with direct links to the underlying Odoo transactions.\n\n"
        "We clearly distinguish confirmed platform capabilities from illustrative metrics, which we will tailor during discovery.\""
    )
    print("Slide 5: Reporting Tiers generated.")

    # =========================================================================
    # SLIDE 6: ODOO ERP HEALTH CHECK & UI/UX AUDIT
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, BG_LIGHT)
    add_header(slide6, "Core ERP Assessment & Optimization", "Odoo ERP Health Check & UI/UX Usability Audit", "A structured assessment approach to optimize workflows, resolve usability friction, and elevate adoption.")

    # 2 Main Columns: Left = Assessment Methodology; Right = Deliverables & Roadmapping
    col6_w = Inches(5.7)
    col6_h = Inches(4.55)
    col6_x = [Inches(0.8), Inches(6.833)]

    # Left: Audit Scope & Focus Areas
    add_card(slide6, col6_x[0], Inches(1.68), col6_w, col6_h)
    tb_a = slide6.shapes.add_textbox(col6_x[0] + Inches(0.22), Inches(1.8), col6_w - Inches(0.44), col6_h - Inches(0.24))
    tf_a = tb_a.text_frame
    tf_a.word_wrap = True
    tf_a.margin_left = tf_a.margin_right = tf_a.margin_top = tf_a.margin_bottom = 0

    p = tf_a.paragraphs[0]
    p.text = "PROPOSED ASSESSMENT METHODOLOGY"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SLATE_900

    p = tf_a.add_paragraph()
    p.text = "Thorough Evaluation Across 4 Core Technical Dimensions"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(4)

    audit_steps = [
        ("1. Environment & Architecture Review", "Inspect current Odoo deployment version, server sizing, database performance indexes, active modules, and installed third-party apps."),
        ("2. Workflow & Configuration Evaluation", "Audit critical operational workflows (Order-to-Cash, Procure-to-Pay, Inventory, General Ledger) against Odoo standard best practices."),
        ("3. UI/UX & User Pain Point Analysis", "Conduct structured walkthroughs with SGG department users to identify navigation bottlenecks, cluttered screen layouts, and redundant clicks."),
        ("4. Functional Gap & Customization Audit", "Review existing custom code and scripts to identify workarounds, data integrity risks, and unsupported configurations.")
    ]

    for title, desc in audit_steps:
        p = tf_a.add_paragraph()
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

    p_foc = tf_a.add_paragraph()
    p_foc.text = "Core Objective: Enhance user adoption, eliminate process friction, and improve transaction speed without destabilizing the live system."
    p_foc.font.name = "Calibri"
    p_foc.font.size = Pt(8.8)
    p_foc.font.bold = True
    p_foc.font.color.rgb = CYAN_ACCENT
    p_foc.space_before = Pt(4)

    # Right: Expected Tangible Deliverables
    add_card(slide6, col6_x[1], Inches(1.68), col6_w, col6_h)
    tb_b = slide6.shapes.add_textbox(col6_x[1] + Inches(0.22), Inches(1.8), col6_w - Inches(0.44), col6_h - Inches(0.24))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

    p = tf_b.paragraphs[0]
    p.text = "EXPECTED TANGIBLE DELIVERABLES"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SLATE_900

    p = tf_b.add_paragraph()
    p.text = "Actionable Documentation & Optimization Roadmap"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(4)

    deliverables = [
        ("Odoo Health Check Report", "Comprehensive technical assessment covering database health, server utilization, module dependencies, and system performance benchmarks."),
        ("UI/UX Assessment Findings", "Visual diagnostic identifying cluttered forms, navigation drop-offs, and redesigned screen wireframes for simplified data entry."),
        ("Functional Gap & Risk Register", "Detailed inventory of operational bottlenecks, manual spreadsheet dependencies, and process friction points across departments."),
        ("Prioritized Enhancement Roadmap", "Categorized action plan classifying fixes into Quick Wins (immediate UI tweaks) versus Strategic Improvements (workflow redesign).")
    ]

    for title, desc in deliverables:
        p = tf_b.add_paragraph()
        p.text = f"✓ {title}: "
        p.font.name = "Calibri"
        p.font.size = Pt(9.2)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_before = Pt(3)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = SLATE_700

    p_note = tf_b.add_paragraph()
    p_note.text = "Advisory Boundary: All recommendations will be objectively prioritized by business impact and complexity. Technical refactoring begins only after formal SGG sign-off."
    p_note.font.name = "Calibri"
    p_note.font.size = Pt(8.8)
    p_note.font.bold = True
    p_note.font.color.rgb = AMBER_ACCENT
    p_note.space_before = Pt(4)

    # Bottom Callout
    add_card(slide6, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.78), bg_color=WHITE, border_color=SLATE_200)
    tb_bot = slide6.shapes.add_textbox(Inches(1.0), Inches(6.42), Inches(11.333), Inches(0.65))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = tf_bot.margin_bottom = 0

    p = tf_bot.paragraphs[0]
    p.text = "OBJECTIVE AUDIT COMMITMENT: EVIDENCE BEFORE ACTION"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT

    p = tf_bot.add_paragraph()
    p.text = "Rather than applying unverified modifications, our consultants execute an objective diagnostic audit first. This ensures all UI/UX adjustments and configuration changes directly solve verified SGG user pain points while preserving system integrity."
    p.font.name = "Calibri"
    p.font.size = Pt(9)
    p.font.color.rgb = SLATE_700
    p.space_before = Pt(2)

    slide6.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 6 (ODOO HEALTH CHECK):\n\n"
        "\"Slide 6 details our approach to the Odoo ERP Health Check and UI/UX Audit.\n\n"
        "We understand that SGG's business users are experiencing friction with complex forms and confusing navigation layouts. Rather than making assumptions, we propose a structured diagnostic across four dimensions: technical environment, standard workflows, user UI/UX, and customization gaps.\n\n"
        "Our deliverables include an Odoo Health Check Report, UI/UX screen improvement wireframes, a Gap Register, and a Prioritized Roadmap separating immediate quick-wins from strategic improvements.\n\n"
        "We do not promise arbitrary fixes upfront; we audit first, present the findings, and agree on the prioritized fixes together with SGG leadership.\""
    )
    print("Slide 6: Odoo Health Check generated.")

    # =========================================================================
    # SLIDE 7: RESORT ERP TO ODOO DATA MIGRATION
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, BG_LIGHT)
    add_header(slide7, "Legacy Data Continuity", "Resort ERP to Odoo Data Migration Methodology", "A structured 6-step methodology ensuring complete, cleansed, and reconciled historical data transfer.")

    # 6 Step Sequential Process Cards across the slide
    s7_w = Inches(1.82)
    s7_h = Inches(4.35)
    s7_x = [Inches(0.8), Inches(2.78), Inches(4.76), Inches(6.74), Inches(8.72), Inches(10.70)]

    migration_steps = [
        {
            "step": "STEP 01",
            "title": "Extraction",
            "tag": "EXCEL EXTRACTS",
            "bullets": [
                "Obtain historical data extracts from legacy Resort ERP in Excel/CSV format.",
                "Extract chart of accounts, customers, vendors, and inventory master data.",
                "Capture historical operational transactions and opening balances."
            ],
            "output": "Raw Source Extract Inventory"
        },
        {
            "step": "STEP 02",
            "title": "Assessment",
            "tag": "DATA PROFILING",
            "bullets": [
                "Evaluate extract completeness, record volume, and date range coverage.",
                "Identify missing mandatory fields and corrupted character sets.",
                "Classify active master records versus obsolete legacy accounts."
            ],
            "output": "Data Assessment & Gap Report"
        },
        {
            "step": "STEP 03",
            "title": "Cleansing",
            "tag": "NORMALIZATION",
            "bullets": [
                "Automated deduplication of customer and vendor records.",
                "Standardize addresses, phone numbers, and regional tax identification codes.",
                "Rectify inconsistent units of measure (UOM) across inventory."
            ],
            "output": "Cleansed Staging Data Files"
        },
        {
            "step": "STEP 04",
            "title": "Mapping",
            "tag": "SCHEMA ALIGNMENT",
            "bullets": [
                "Field-by-field mapping aligning Resort ERP tables to target Odoo models.",
                "Map legacy chart of accounts to SGG's standard Odoo account codes.",
                "Define business partner CVI and payment term transformations."
            ],
            "output": "Data Mapping Specification Doc"
        },
        {
            "step": "STEP 05",
            "title": "Migration",
            "tag": "CONTROLLED LOAD",
            "bullets": [
                "Execute staging loads using validated Odoo import pipelines.",
                "Automate pre-posting validation to prevent rejected records.",
                "Conduct simulated cutover iterations to verify data dependencies."
            ],
            "output": "Migration Execution Logs"
        },
        {
            "step": "STEP 06",
            "title": "Sign-Off",
            "tag": "RECONCILIATION",
            "bullets": [
                "Perform debit/credit trial balance reconciliation with SGG Finance.",
                "Verify inventory valuations and open accounts receivable/payable.",
                "Formal stakeholder audit sign-off prior to production cutover."
            ],
            "output": "Reconciliation Sign-Off Certificate"
        }
    ]

    for idx, s in enumerate(migration_steps):
        cx = s7_x[idx]
        add_card(slide7, cx, Inches(1.68), s7_w, s7_h)

        tb = slide7.shapes.add_textbox(cx + Inches(0.1), Inches(1.8), s7_w - Inches(0.2), s7_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = s["step"]
        p.font.name = "Calibri"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT

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

        for b in s["bullets"]:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.name = "Calibri"
            p.font.size = Pt(8.2)
            p.font.color.rgb = SLATE_700
            p.space_before = Pt(2)

        p = tf.add_paragraph()
        p.text = "Deliverable:"
        p.font.name = "Calibri"
        p.font.size = Pt(8.2)
        p.font.bold = True
        p.font.color.rgb = SLATE_900
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = s["output"]
        p.font.name = "Calibri"
        p.font.size = Pt(8)
        p.font.color.rgb = CYAN_ACCENT

    # Bottom Scope Boundary Callout
    add_card(slide7, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.78), bg_color=WHITE, border_color=SLATE_200)
    tb_bot = slide7.shapes.add_textbox(Inches(1.0), Inches(6.42), Inches(11.333), Inches(0.65))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = tf_bot.margin_bottom = 0

    p = tf_bot.paragraphs[0]
    p.text = "DATA GOVERNANCE & BOUNDARY SAFEGUARD"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = NAVY_ACCENT

    p = tf_bot.add_paragraph()
    p.text = "Final migration scope, record volumes, and historical cutoff depth will depend on available Excel extracts provided from Resort ERP. SGG business owners maintain ownership of source record accuracy, while Lumbini governs technical cleansing, mapping integrity, and load verification."
    p.font.name = "Calibri"
    p.font.size = Pt(9)
    p.font.color.rgb = SLATE_700
    p.space_before = Pt(2)

    slide7.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 7 (DATA MIGRATION):\n\n"
        "\"Slide 7 presents our structured 6-step migration methodology to transition historical data from Resort ERP into Odoo.\n\n"
        "We recognize that legacy migrations fail when dirty data is loaded directly into a clean ERP. Our process enforces discipline:\n"
        "First, we obtain Excel extracts from Resort ERP. Second, we assess completeness and quality. Third, we cleanse duplicates and standardize formats. Fourth, we build an explicit mapping specification aligning legacy fields with Odoo models.\n\n"
        "Fifth, we execute controlled staging runs with automated pre-validation to eliminate upload errors. Sixth, and most importantly, we perform a strict financial and inventory reconciliation with SGG Finance before closing the migration.\n\n"
        "This ensures SGG gains complete historical continuity without contaminating the Odoo environment.\""
    )
    print("Slide 7: Data Migration generated.")

    # =========================================================================
    # SLIDE 8: AUTOMATED PAYROLL & TIME-TRACKING INTEGRATION
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, BG_LIGHT)
    add_header(slide8, "HR Operations Automation", "Automated Payroll, Biometric Attendance & WPS Integration", "Connecting frontline biometric punch capture directly to Odoo payroll processing and bank salary disbursement.")

    # Top Conceptual Architecture Flow Container
    add_card(slide8, Inches(0.8), Inches(1.68), Inches(11.733), Inches(1.15), bg_color=WHITE, border_color=SLATE_200)
    tb_flow8 = slide8.shapes.add_textbox(Inches(1.0), Inches(1.78), Inches(11.333), Inches(0.95))
    tf_flow8 = tb_flow8.text_frame
    tf_flow8.word_wrap = True
    tf_flow8.margin_left = tf_flow8.margin_right = tf_flow8.margin_top = tf_flow8.margin_bottom = 0

    p = tf_flow8.paragraphs[0]
    p.text = "END-TO-END PAYROLL AUTOMATION FLOW"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT

    p = tf_flow8.add_paragraph()
    p.text = "Biometric Devices (Fingerprint / Facial)  ➔  Attendance Ingestion  ➔  Timesheet Validation  ➔  Odoo Payroll Processing  ➔  WPS File Generation  ➔  Bank Upload"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = SLATE_900
    p.space_before = Pt(3)

    p = tf_flow8.add_paragraph()
    p.text = "Automates the entire payroll lifecycle from employee biometric terminal registration to automated salary rule calculations, statutory deductions, and electronic salary file formatting for corporate bank upload."
    p.font.name = "Calibri"
    p.font.size = Pt(8.8)
    p.font.color.rgb = SLATE_700
    p.space_before = Pt(2)

    # 4 Integration Pillar Cards (Bottom Grid)
    c8_w = Inches(2.78)
    c8_h = Inches(3.35)
    c8_x = [Inches(0.8), Inches(3.784), Inches(6.768), Inches(9.752)]

    payroll_caps = [
        {
            "title": "Biometric Hardware Ingestion",
            "tag": "TERMINAL CONNECTIVITY",
            "bullets": [
                "Integration assessment of existing fingerprint and facial recognition devices.",
                "Automated polling and push telemetry of raw employee punch timestamps.",
                "Edge buffering ensuring zero punch data loss during network interruptions.",
                "Standardized device communication (API, TCP/IP, or vendor middleware)."
            ]
        },
        {
            "title": "Timesheet & Rules Validation",
            "tag": "ATTENDANCE RECONCILIATION",
            "bullets": [
                "Automated mapping of raw punches to employee shifts and schedules.",
                "Rule-based calculation of regular hours, approved overtime, and tardiness.",
                "Automated synchronization with SGG approved leave and holiday rosters.",
                "Supervisor exception approval desk for missed punches and shift swaps."
            ]
        },
        {
            "title": "Odoo Payroll Synchronization",
            "tag": "SALARY CALCULATION",
            "bullets": [
                "Direct synchronization of validated hours into Odoo HR/Payroll module.",
                "Automated calculation of basic salary, housing, transport allowances, and deductions.",
                "Generation of digital employee salary payslips with self-service access.",
                "Automated general ledger payroll journal entry posting in Odoo Finance."
            ]
        },
        {
            "title": "Compliant WPS File Generation",
            "tag": "BANK SALARY DISBURSEMENT",
            "bullets": [
                "Automated generation of electronic Salary Information Files (SIF/WPS).",
                "Formatting aligned to regional Wages Protection System compliance.",
                "Validation of employee bank account numbers (IBAN), labor IDs, and totals.",
                "Ready-to-upload files formatted specifically for SGG's corporate bank."
            ]
        }
    ]

    for idx, c in enumerate(payroll_caps):
        cx = c8_x[idx]
        add_card(slide8, cx, Inches(2.95), c8_w, c8_h)

        tb = slide8.shapes.add_textbox(cx + Inches(0.14), Inches(3.08), c8_w - Inches(0.28), c8_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = c["tag"]
        p.font.name = "Calibri"
        p.font.size = Pt(8)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT

        p = tf.add_paragraph()
        p.text = c["title"]
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = SLATE_900
        p.space_after = Pt(4)

        for b in c["bullets"]:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.name = "Calibri"
            p.font.size = Pt(8.2)
            p.font.color.rgb = SLATE_700
            p.space_before = Pt(2)

    # Bottom Technical Qualification Box
    add_card(slide8, Inches(0.8), Inches(6.42), Inches(11.733), Inches(0.72), bg_color=WHITE, border_color=SLATE_200)
    tb_bot = slide8.shapes.add_textbox(Inches(1.0), Inches(6.48), Inches(11.333), Inches(0.58))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = tf_bot.margin_bottom = 0

    p = tf_bot.paragraphs[0]
    p.text = "TECHNICAL INTEGRATION DEPENDENCY & VALIDATION REQUIREMENT"
    p.font.name = "Calibri"
    p.font.size = Pt(9.2)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT

    p = tf_bot.add_paragraph()
    p.text = "Actual integration design and automation protocols depend on existing biometric device models, communication API readiness, SGG's specific Odoo payroll rule configurations, and technical validation of SGG's corporate bank WPS formatting specifications."
    p.font.name = "Calibri"
    p.font.size = Pt(8.8)
    p.font.color.rgb = SLATE_700
    p.space_before = Pt(2)

    slide8.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 8 (PAYROLL & BIOMETRIC INTEGRATION):\n\n"
        "\"Slide 8 addresses SGG's requirement to connect time-tracking and payroll into an automated, compliant process.\n\n"
        "Today, processing timesheets and payroll manually creates significant operational lag and risks human error. We propose an end-to-end automated flow:\n\n"
        "First, biometric devices capture employee punches. Second, our integration pipeline consolidates attendance and applies business rules for shifts, overtime, and leaves. Third, verified timesheet totals feed directly into Odoo's salary computation engine.\n\n"
        "Fourth, the system automatically generates standardized Wages Protection System (WPS) electronic salary files, formatted precisely for SGG's corporate bank upload.\n\n"
        "We note transparently that the final integration script will be validated against SGG's specific biometric terminal hardware and bank formatting rules.\""
    )
    print("Slide 8: Payroll Integration generated.")

    # =========================================================================
    # SLIDE 9: IMPLEMENTATION APPROACH & DELIVERY ROADMAP
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, BG_LIGHT)
    add_header(slide9, "Phased Program Execution", "Implementation Approach, Roadmap & Odoo v20 Readiness", "A structured 5-phase delivery model designed for rapid time-to-value and long-term upgrade compatibility.")

    # 5 Phase Sequential Cards
    ph_w = Inches(2.2)
    ph_h = Inches(3.55)
    ph_x = [Inches(0.8), Inches(3.18), Inches(5.56), Inches(7.94), Inches(10.32)]

    phases_data = [
        {
            "phase": "PHASE 01",
            "title": "Discovery & Audit",
            "tag": "ASSESSMENT GATE",
            "bullets": [
                "Conduct stakeholder requirement workshops across business units.",
                "Execute technical Odoo environment & workflow health check.",
                "Define ELITIA BI KPI catalog, formulas, and data sources.",
                "Audit biometric hardware APIs and Resort ERP data extracts."
            ],
            "milestone": "Signed Baseline & Architecture Spec"
        },
        {
            "phase": "PHASE 02",
            "title": "Design & Blueprint",
            "tag": "BLUEPRINT GATE",
            "bullets": [
                "Design ELITIA BI executive dashboards and wireframes.",
                "Author Odoo UI/UX optimization and workflow recommendations.",
                "Finalize Resort ERP to Odoo data mapping specifications.",
                "Design biometric punch ingestion and WPS file generator."
            ],
            "milestone": "Approved Functional Blueprint & UI Wireframes"
        },
        {
            "phase": "PHASE 03",
            "title": "Build & Migration",
            "tag": "CONFIGURATION",
            "bullets": [
                "Deploy ELITIA BI semantic models and dashboard cockpits.",
                "Implement approved Odoo UI/UX and workflow enhancements.",
                "Execute Resort ERP data cleansing, staging, and trial loads.",
                "Configure biometric attendance sync and Odoo payroll rules."
            ],
            "milestone": "System Configuration & Staging Complete"
        },
        {
            "phase": "PHASE 04",
            "title": "Testing & UAT",
            "tag": "VERIFICATION",
            "bullets": [
                "Conduct end-to-end integration and data pipeline testing.",
                "Perform trial balance and inventory migration reconciliation.",
                "Execute dual parallel payroll runs against legacy outputs.",
                "User acceptance testing (UAT) and super-user enablement."
            ],
            "milestone": "Formal Business UAT & Cutover Sign-Off"
        },
        {
            "phase": "PHASE 05",
            "title": "Go-Live & Support",
            "tag": "STABILISATION",
            "bullets": [
                "Execute production cutover and activate live ELITIA BI views.",
                "Initiate automated daily biometric attendance and payroll runs.",
                "Dedicated post-go-live hypercare and priority bug resolution.",
                "Comprehensive administrator and end-user knowledge transfer."
            ],
            "milestone": "Project Handover & SLA Support Transition"
        }
    ]

    for idx, ph in enumerate(phases_data):
        cx = ph_x[idx]
        add_card(slide9, cx, Inches(1.68), ph_w, ph_h)

        tb = slide9.shapes.add_textbox(cx + Inches(0.1), Inches(1.8), ph_w - Inches(0.2), ph_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = ph["phase"]
        p.font.name = "Calibri"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT

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
        p.space_after = Pt(3)

        for b in ph["bullets"]:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.name = "Calibri"
            p.font.size = Pt(8.2)
            p.font.color.rgb = SLATE_700
            p.space_before = Pt(1.5)

        p = tf.add_paragraph()
        p.text = "Key Deliverable:"
        p.font.name = "Calibri"
        p.font.size = Pt(8.2)
        p.font.bold = True
        p.font.color.rgb = SLATE_900
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = ph["milestone"]
        p.font.name = "Calibri"
        p.font.size = Pt(8)
        p.font.color.rgb = CYAN_ACCENT

    # Bottom Future-Readiness Container (Odoo v20 in 2027)
    add_card(slide9, Inches(0.8), Inches(5.35), Inches(11.733), Inches(1.78), bg_color=WHITE, border_color=SLATE_200)
    tb_fut = slide9.shapes.add_textbox(Inches(1.0), Inches(5.45), Inches(11.333), Inches(1.55))
    tf_fut = tb_fut.text_frame
    tf_fut.word_wrap = True
    tf_fut.margin_left = tf_fut.margin_right = tf_fut.margin_top = tf_fut.margin_bottom = 0

    p = tf_fut.paragraphs[0]
    p.text = "FUTURE-READINESS & COMPATIBILITY PLANNING FOR ODOO V20 (2027 UPGRADE)"
    p.font.name = "Calibri"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ELITIA_BLUE

    p = tf_fut.add_paragraph()
    p.text = "SGG plans to upgrade its core ERP to Odoo v20 in 2027. Lumbini incorporates forward-compatibility principles into every phase of the current engagement:"
    p.font.name = "Calibri"
    p.font.size = Pt(9)
    p.font.color.rgb = SLATE_700
    p.space_before = Pt(2)

    v20_points = [
        ("Decoupled Side-by-Side BI Architecture", "ELITIA BI interfaces with Odoo via non-invasive database views and governed APIs, ensuring the analytics layer remains entirely isolated from future ERP version upgrades."),
        ("Clean Core Customization Standard", "Odoo workflow optimizations and UI enhancements will adhere to Odoo standard extension frameworks, avoiding core modification and preventing future upgrade conflicts."),
        ("Forward Compatibility Governance", "While automatic compatibility cannot be guaranteed prior to Odoo v20 release notes, our design prioritizes maintainability and documented interface contracts to minimize future upgrade effort.")
    ]

    for title, desc in v20_points:
        p = tf_fut.add_paragraph()
        p.text = f"▸ {title}: "
        p.font.name = "Calibri"
        p.font.size = Pt(8.8)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_before = Pt(2)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = SLATE_700

    slide9.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 9 (ROADMAP & ODOO V20):\n\n"
        "\"Slide 9 lays out our 5-phase delivery framework, moving systematically from Discovery and Solution Design through to Build, Testing, and Post-Go-Live Support.\n\n"
        "Crucially, we incorporate SGG's planned 2027 upgrade to Odoo v20 into today's architecture.\n\n"
        "First, ELITIA BI is architected side-by-side using a decoupled semantic layer, meaning when Odoo upgrades to v20, the executive analytics layer does not break.\n\n"
        "Second, all Odoo enhancements adhere to standard modular practices rather than modifying the core code.\n\n"
        "We are transparent that automatic compatibility cannot be promised before Odoo v20's release specifications are published, but our clean-core approach ensures minimum friction and lowest upgrade cost in 2027.\""
    )
    print("Slide 9: Roadmap generated.")

    # =========================================================================
    # SLIDE 10: COMMERCIALS, RESOURCES & TERMS AND CONDITIONS
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, BG_LIGHT)
    add_header(slide10, "Commercial Proposal & Governance", "Commercial Framework, Proposed Resources & Terms", "Transparent investment schedule, dedicated consulting team, and standard engagement terms.")

    # 3 Distinct Columns: A. Commercial Proposal; B. Manpower Resources; C. Terms & Conditions
    c10_w = Inches(3.68)
    c10_h = Inches(5.35)
    c10_x = [Inches(0.8), Inches(4.82), Inches(8.84)]

    # Col A: Commercial Proposal
    add_card(slide10, c10_x[0], Inches(1.68), c10_w, c10_h)
    tb_c = slide10.shapes.add_textbox(c10_x[0] + Inches(0.18), Inches(1.8), c10_w - Inches(0.36), c10_h - Inches(0.24))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0

    p = tf_c.paragraphs[0]
    p.text = "SECTION A · COMMERCIAL PROPOSAL"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ELITIA_BLUE

    p = tf_c.add_paragraph()
    p.text = "Professional Services & Licensing"
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = SLATE_900
    p.space_after = Pt(4)

    comm_items = [
        ("Workstream A · ELITIA BI Implementation", "[Commercial Value / To be agreed]"),
        ("Workstream B · Odoo Health Check & UI/UX", "[Commercial Value / To be agreed]"),
        ("Workstream C · Resort ERP Data Migration", "[Commercial Value / To be agreed]"),
        ("Workstream D · Payroll & WPS Integration", "[Commercial Value / To be agreed]"),
        ("ELITIA BI Software Licensing / Subscription", "[Annual Tier / To be agreed]"),
        ("Third-Party & Hosting / Cloud Infrastructure", "Direct SGG / Vendor Billing"),
        ("Applicable Statutory Taxes", "Additional as per legal rate")
    ]

    for title, val in comm_items:
        p = tf_c.add_paragraph()
        p.text = f"• {title}: "
        p.font.name = "Calibri"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_before = Pt(2)
        run = p.add_run()
        run.text = val
        run.font.bold = False
        run.font.color.rgb = SLATE_700

    p = tf_c.add_paragraph()
    p.text = "Proposed Payment Milestones:"
    p.font.name = "Calibri"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = SLATE_900
    p.space_before = Pt(6)

    milestone_items = [
        ("M1 (20% Invoiced)", "Project Kick-off & Approved Discovery Baseline"),
        ("M2 (30% Invoiced)", "Approved Solution Design & Migration Mapping"),
        ("M3 (30% Invoiced)", "System Build, Cleansing & Business UAT Sign-off"),
        ("M4 (20% Invoiced)", "Production Go-Live & 30-Day Hypercare Handover")
    ]
    for m, d in milestone_items:
        p = tf_c.add_paragraph()
        p.text = f"▸ {m}: {d}"
        p.font.name = "Calibri"
        p.font.size = Pt(8)
        p.font.color.rgb = SLATE_700
        p.space_before = Pt(1.5)

    # Col B: Proposed Manpower Resources
    add_card(slide10, c10_x[1], Inches(1.68), c10_w, c10_h)
    tb_m = slide10.shapes.add_textbox(c10_x[1] + Inches(0.18), Inches(1.8), c10_w - Inches(0.36), c10_h - Inches(0.24))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = tf_m.margin_bottom = 0

    p = tf_m.paragraphs[0]
    p.text = "SECTION B · PROPOSED RESOURCES"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT

    p = tf_m.add_paragraph()
    p.text = "Dedicated Delivery Team Composition"
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = SLATE_900
    p.space_after = Pt(4)

    team_members = [
        ("Project Manager / Engagement Lead", "Program governance, schedule tracking, risk management, and stakeholder alignment.", "[Allocation Placeholder]"),
        ("ELITIA BI Solutions Consultant", "Semantic data modeling, KPI formula build, executive and departmental dashboard authoring.", "[Allocation Placeholder]"),
        ("Odoo Senior Functional Consultant", "Workflow health check, UI/UX screen simplification, and Odoo payroll configuration.", "[Allocation Placeholder]"),
        ("Data Migration Specialist", "Resort ERP data profiling, Excel cleansing, field mapping, staging validation, and reconciliation.", "[Allocation Placeholder]"),
        ("Integration Technical Consultant", "Biometric device connectivity, timesheet ingestion rules, and WPS file format generation.", "[Allocation Placeholder]"),
        ("QA & Testing Support Lead", "Test plan design, parallel payroll verification, UAT coordination, and defect tracking.", "[Allocation Placeholder]")
    ]

    for role, resp, alloc in team_members:
        p = tf_m.add_paragraph()
        p.text = f"▸ {role}"
        p.font.name = "Calibri"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_before = Pt(3)

        p = tf_m.add_paragraph()
        p.text = f"Responsibility: {resp}"
        p.font.name = "Calibri"
        p.font.size = Pt(8)
        p.font.color.rgb = SLATE_700
        p.space_before = Pt(1)

        p = tf_m.add_paragraph()
        p.text = f"Commitment: {alloc}"
        p.font.name = "Calibri"
        p.font.size = Pt(7.8)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
        p.space_before = Pt(1)

    # Col C: Terms & Conditions
    add_card(slide10, c10_x[2], Inches(1.68), c10_w, c10_h)
    tb_t = slide10.shapes.add_textbox(c10_x[2] + Inches(0.18), Inches(1.8), c10_w - Inches(0.36), c10_h - Inches(0.24))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0

    p = tf_t.paragraphs[0]
    p.text = "SECTION C · TERMS & CONDITIONS"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT

    p = tf_t.add_paragraph()
    p.text = "Commercial & Governance Safeguards"
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = SLATE_900
    p.space_after = Pt(4)

    terms = [
        ("Scope & Deliverables", "Scope is strictly governed by the mutually approved Functional Blueprint. Additional requirements handled via Change Order."),
        ("Timeline Dependencies", "Project duration depends on timely client access to Odoo environments, biometric terminals, and legacy Resort ERP data extracts."),
        ("Client Responsibilities", "SGG will nominate business module owners, provide clean Excel extracts, and facilitate bank WPS formatting specifications."),
        ("Third-Party Software", "Costs for Odoo licensing, server hosting, biometric device firmware/SDKs, or bank fees remain directly with SGG."),
        ("Payment & Invoicing", "Invoices payable within 30 days of submission against verified deliverable acceptance sign-off."),
        ("Acceptance & Sign-Off", "Deliverables deemed approved if formal feedback or objection is not submitted within 10 business days of submission."),
        ("Post-Go-Live Support", "Includes [30/60 Days] hypercare support covering defect resolution for implemented components.")
    ]

    for title, desc in terms:
        p = tf_t.add_paragraph()
        p.text = f"• {title}: "
        p.font.name = "Calibri"
        p.font.size = Pt(8.2)
        p.font.bold = True
        p.font.color.rgb = NAVY_ACCENT
        p.space_before = Pt(2.5)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = SLATE_700

    slide10.notes_slide.notes_text_frame.text = (
        "EXECUTIVE BRIEFING - SLIDE 10 (COMMERCIALS & GOVERNANCE):\n\n"
        "\"Slide 10 provides the commercial governance framework for the engagement.\n\n"
        "In Section A, we present the commercial structure across the four workstreams, licensing, and a milestone payment plan tied strictly to verified deliverables.\n\n"
        "In Section B, we outline our dedicated consulting team: Project Manager, ELITIA BI Consultant, Odoo Functional Consultant, Data Migration Specialist, Integration Consultant, and QA Lead—with flexible allocation placeholders for mutual agreement.\n\n"
        "In Section C, we define balanced engagement terms: scope boundaries, timely access to Resort ERP extracts, bank specifications, payment terms, and hypercare support.\n\n"
        "This transparent structure ensures clear accountability and mutual success from day one.\""
    )
    print("Slide 10: Commercials generated.")

    # Save Presentation
    output_path = "SGG_Enterprise_BI_and_Odoo_Enhancement_Proposal.pptx"
    prs.save(output_path)
    print(f"\nPresentation successfully generated and saved: {output_path}")
    print(f"Total slides count: {len(prs.slides)}")

if __name__ == "__main__":
    build_sgg_deck()
