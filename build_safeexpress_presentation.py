import os, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Executive Palette
    NAVY_DARK = RGBColor(10, 25, 47)      # #0A192F Title / Dark Cards
    NAVY_ACCENT = RGBColor(15, 35, 65)    # #0F2341
    SLATE_900 = RGBColor(15, 23, 42)      # #0F172A Primary text
    SLATE_700 = RGBColor(51, 65, 85)      # #334155 Body text
    SLATE_500 = RGBColor(100, 116, 139)   # #64748B Subtitle / Muted
    SLATE_200 = RGBColor(226, 232, 240)   # #E2E8F0 Borders
    BG_LIGHT = RGBColor(248, 250, 252)    # #F8FAFC Slide background
    WHITE = RGBColor(255, 255, 255)
    BLUE_ACCENT = RGBColor(2, 132, 199)   # #0284C7 Executive Cyan/Blue
    BLUE_DARK = RGBColor(30, 58, 138)     # #1E3A8A Deep accent

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, tracker, title, subtitle):
        tracker_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.28))
        tf_tr = tracker_box.text_frame
        tf_tr.word_wrap = True
        tf_tr.margin_left = tf_tr.margin_right = tf_tr.margin_top = tf_tr.margin_bottom = 0
        p_tr = tf_tr.paragraphs[0]
        p_tr.text = tracker.upper()
        p_tr.font.name = "Calibri"
        p_tr.font.size = Pt(10)
        p_tr.font.bold = True
        p_tr.font.color.rgb = BLUE_ACCENT

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.733), Inches(0.55))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = SLATE_900

        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.22), Inches(11.733), Inches(0.35))
        tf_s = sub_box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle
        p_s.font.name = "Calibri"
        p_s.font.size = Pt(12)
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
    # SLIDE 1: TITLE & EXECUTIVE POSITIONING
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, NAVY_DARK)

    if os.path.exists("assets/title_bg_graphic.png"):
        try:
            slide1.shapes.add_picture("assets/title_bg_graphic.png", Inches(7.5), Inches(0), Inches(5.833), Inches(7.5))
        except:
            pass

    if os.path.exists("assets/lumbini_logo.png"):
        try:
            slide1.shapes.add_picture("assets/lumbini_logo.png", Inches(1.0), Inches(0.8), Inches(2.8), Inches(0.85))
        except:
            pass

    title_box1 = slide1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(10.5), Inches(2.4))
    tf1 = title_box1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0

    p_org = tf1.paragraphs[0]
    p_org.text = "LUMBINI ELITE GROUP"
    p_org.font.name = "Calibri"
    p_org.font.size = Pt(14)
    p_org.font.bold = True
    p_org.font.color.rgb = RGBColor(56, 189, 248)

    p_main = tf1.add_paragraph()
    p_main.text = "Enterprise Technology & Transformation Capabilities"
    p_main.font.name = "Calibri"
    p_main.font.size = Pt(32)
    p_main.font.bold = True
    p_main.font.color.rgb = WHITE
    p_main.space_before = Pt(8)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Connecting enterprise systems, operational data, integration, and AI-ready business transformation."
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_before = Pt(12)

    add_card(slide1, Inches(1.0), Inches(4.8), Inches(9.5), Inches(1.8), bg_color=NAVY_ACCENT, border_color=RGBColor(30, 58, 138))
    ctx_box = slide1.shapes.add_textbox(Inches(1.2), Inches(4.95), Inches(9.1), Inches(1.5))
    tf_ctx = ctx_box.text_frame
    tf_ctx.word_wrap = True
    tf_ctx.margin_left = tf_ctx.margin_right = tf_ctx.margin_top = tf_ctx.margin_bottom = 0

    p_c1 = tf_ctx.paragraphs[0]
    p_c1.text = "EXECUTIVE CAPABILITY & STRATEGIC ROADMAP DIALOGUE"
    p_c1.font.name = "Calibri"
    p_c1.font.size = Pt(11)
    p_c1.font.bold = True
    p_c1.font.color.rgb = RGBColor(56, 189, 248)

    p_c2 = tf_ctx.add_paragraph()
    p_c2.text = "Prepared for: General Manager, Information Technology  ·  SafeExpress"
    p_c2.font.name = "Calibri"
    p_c2.font.size = Pt(13)
    p_c2.font.bold = True
    p_c2.font.color.rgb = WHITE
    p_c2.space_before = Pt(4)

    p_c3 = tf_ctx.add_paragraph()
    p_c3.text = "Presenter: Senior Enterprise Technology & SAP Solutions Architecture Practice\nLumbini Elite Solutions & Services Pvt. Ltd. (Lumbini Elite Group)"
    p_c3.font.name = "Calibri"
    p_c3.font.size = Pt(11)
    p_c3.font.color.rgb = RGBColor(203, 213, 225)
    p_c3.space_before = Pt(4)

    slide1.notes_slide.notes_text_frame.text = (
        "KEY MESSAGE: Establish Lumbini immediately as a strategic technology and transformation partner capable of architecting, integrating, and sustaining enterprise solutions—not merely a staffing vendor.\n\n"
        "TALK TRACK (30 seconds):\n"
        "\"Good morning. Over the past three years, SafeExpress has been a valued customer for Lumbini Elite Solutions. As your leadership team takes on the next horizon of digital modernization, ERP excellence, and AI-enabled transformation, we wanted to take ten minutes to share who Lumbini is today.\n\n"
        "We are an accredited enterprise technology partner combining deep SAP and multi-ERP architecture, mission-critical systems integration, data trust engineering, and scalable global delivery. Today, we want to move beyond personnel and demonstrate our real delivery architectures, proven integration track record, and how our engineering discipline can complement SafeExpress's technology roadmap.\"\n\n"
        "TRANSITION: \"To begin, let us look at the complete breadth of our end-to-end technology services portfolio.\""
    )
    print("Slide 1 configured.")

    # =========================================================================
    # SLIDE 2: OUR END-TO-END SERVICES
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, BG_LIGHT)
    add_header(slide2, "Comprehensive Capabilities Portfolio", "Our End-to-End Enterprise Services", "Architecting, integrating, and sustaining mission-critical enterprise solutions across the entire lifecycle.")

    card_w = Inches(3.68)
    card_h = Inches(2.25)
    cols_x = [Inches(0.8), Inches(4.82), Inches(8.84)]
    rows_y = [Inches(1.75), Inches(4.25)]

    services_data = [
        {
            "num": "01",
            "title": "Enterprise Applications & Core ERP",
            "tag": "SAP S/4HANA · ECC · RISE · CLEAN CORE",
            "bullets": [
                "End-to-end ERP implementation, greenfield deployments, and S/4HANA conversions.",
                "Clean-Core advisory and BTP side-by-side extensibility (RAP / CAP frameworks).",
                "Fit-to-standard process design, cutover governance, and post-go-live stabilization."
            ]
        },
        {
            "num": "02",
            "title": "Enterprise Systems & 3PL Integration",
            "tag": "SAP INTEGRATION SUITE · APIS · SFTP · EDI",
            "bullets": [
                "Bi-directional middleware connecting core ERP with 3PL logistics, WMS, and MES.",
                "Real-time event streaming, queue monitoring, and automated exception routing.",
                "High-throughput transactional interfaces (PO, ASN, GRN, PGI, and billing synchronization)."
            ]
        },
        {
            "num": "03",
            "title": "Data Platforms, Analytics & AI Readiness",
            "tag": "DATASPERE · HANA CLOUD · SAC · POWER BI",
            "bullets": [
                "In-memory calculation views resolving complex logic directly where operational data lives.",
                "Automated ETL pipelines, master data governance (MDG), and schema reconciliation.",
                "Enterprise AI grounding: private vector knowledge bases, RAG, and agentic guardrails."
            ]
        },
        {
            "num": "04",
            "title": "Operational Tech & Smart Operations",
            "tag": "ELITIA SUITE · IOT · EDGE TELEMETRY · OPC UA",
            "bullets": [
                "Decoupled manufacturing & logistics microservices (Elitia MES, EMS, and Gateways).",
                "High-frequency sensor and scanner telemetry ingestion without core database locks.",
                "End-to-end operational traceability, automated poka-yoke, and digital thread tracking."
            ]
        },
        {
            "num": "05",
            "title": "Cloud Applications & Managed Services",
            "tag": "REACT · .NET · PYTHON · 24/7 SLA AMS",
            "bullets": [
                "Custom web and mobile frontends engineered for frontline warehouse and plant personnel.",
                "24/7 SLA-governed L1–L3 technical and functional support with automated runbooks.",
                "Proactive Root Cause Analysis (RCA) eliminating repeat operational incidents."
            ]
        },
        {
            "num": "06",
            "title": "Architecture & Delivery Governance",
            "tag": "CMMI LEVEL 3 · ISO 9001:2015 · ISO 14001",
            "bullets": [
                "Appraised CMMI Level 3 engineering rigor ensuring repeatable, audited sprint delivery.",
                "Deliverable-linked milestone gates, automated testing, and stringent UAT sign-offs.",
                "Disciplined scope management, transparent burn-downs, and executive steering oversight."
            ]
        }
    ]

    for idx, s in enumerate(services_data):
        r = idx // 3
        c = idx % 3
        cx = cols_x[c]
        cy = rows_y[r]

        add_card(slide2, cx, cy, card_w, card_h)

        tb = slide2.shapes.add_textbox(cx + Inches(0.18), cy + Inches(0.12), card_w - Inches(0.36), card_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = f"{s['num']}  |  {s['title']}"
        p0.font.name = "Calibri"
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = SLATE_900

        p_tag = tf.add_paragraph()
        p_tag.text = s["tag"]
        p_tag.font.name = "Calibri"
        p_tag.font.size = Pt(8.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = BLUE_ACCENT
        p_tag.space_after = Pt(4)

        for b in s["bullets"]:
            pb = tf.add_paragraph()
            pb.text = f"•  {b}"
            pb.font.name = "Calibri"
            pb.font.size = Pt(10)
            pb.font.color.rgb = SLATE_700
            pb.space_before = Pt(2)

    add_card(slide2, Inches(0.8), Inches(6.65), Inches(11.733), Inches(0.52), bg_color=WHITE, border_color=SLATE_200)
    tb_b = slide2.shapes.add_textbox(Inches(1.0), Inches(6.72), Inches(11.333), Inches(0.38))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
    pb = tf_b.paragraphs[0]
    pb.text = "LIFECYCLE PARTNERSHIP: We contribute across the entire delivery continuum—from initial architectural discovery and solution design to hybrid integration, automated data validation, and 24/7 managed support."
    pb.font.name = "Calibri"
    pb.font.size = Pt(10.5)
    pb.font.bold = True
    pb.font.color.rgb = BLUE_DARK

    slide2.notes_slide.notes_text_frame.text = (
        "KEY MESSAGE: Demonstrate the breadth and architectural maturity of Lumbini's services across 6 cohesive capability groups, addressing delivery governance and sprint accountability head-on.\n\n"
        "TALK TRACK (1 minute):\n"
        "\"This slide represents the complete scope of what Lumbini delivers across enterprise ecosystems. Rather than thinking of us as individual contractors, we operate across six integrated disciplines.\n\n"
        "First, core enterprise applications—delivering S/4HANA, ECC, and clean-core private cloud systems. Second, systems and logistics integration—connecting ERP backbones to 3PL logistics, warehouse management systems, and partner portals through robust APIs and event streaming.\n\n"
        "Third, data platforms and analytics—resolving business logic where data lives, enabling real-time operational visibility and building the governed data foundations that enterprise AI models require. Fourth, operational technology through our Elitia microservices suite. Fifth, custom cloud applications and 24/7 SLA-governed support.\n\n"
        "Crucially, the sixth pillar is Delivery Governance. We are appraised at CMMI Level 3 and certified in ISO 9001:2015. We govern our engagements through deliverable-linked milestone gates and automated test acceptance—ensuring predictable sprint closure and transparent accountability.\"\n\n"
        "TRANSITION: \"Now let us look at how these capabilities translate into actual implemented solutions and global delivery engagements.\""
    )
    print("Slide 2 configured.")

    # =========================================================================
    # SLIDE 3: OUR CUSTOMER SOLUTIONS AND GLOBAL DELIVERY EXPERIENCE
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, BG_LIGHT)
    add_header(slide3, "Proven Delivery Footprint", "Customer Solutions & Global Delivery Experience", "Real-world solution architectures delivering measurable operational control across distributed enterprise landscapes.")

    card3_w = Inches(3.68)
    card3_h = Inches(2.28)
    card3_w_large = Inches(5.7)

    solutions_top = [
        {
            "client": "ALGHANIM INDUSTRIES & DSV",
            "type": "IMPLEMENTED SOLUTION",
            "title": "3PL Logistics & WMS Integration",
            "desc": "Architected end-to-end integration between SAP and 3PL warehouse management systems (DSV & Agility WMS).",
            "points": [
                "Automated Inbound (PO/ASN -> GRN) and Outbound (Delivery Orders -> PGI).",
                "Synchronized SKU masters, batch expiration, and storage location states.",
                "Automated midnight inventory reconciliation eliminating stock write-offs."
            ]
        },
        {
            "client": "TATA ELECTRONICS (TEPL & TSAT)",
            "type": "IMPLEMENTED SOLUTION",
            "title": "Connected Enterprise & Shop Floor",
            "desc": "Unified SAP S/4HANA with Siemens/Cantier MES and APS across multiple high-tech manufacturing plants.",
            "points": [
                "Engineered 3 'Super-Interfaces' replacing 6 complex point-to-point flows.",
                "Production reporting lag compressed from 1–2 shifts down to real-time.",
                "Manual manufacturing confirmations reduced by 70%; month-end close by 60%."
            ]
        },
        {
            "client": "HEALTHIUM MEDTECH",
            "type": "IMPLEMENTED SOLUTION",
            "title": "Pre-SAP Migration Data Trust Tool",
            "desc": "Engineered standalone automated ETL & validation engine complementing SAP LTMC during S/4HANA migration.",
            "points": [
                "Automated cross-object dependency validation (Material, BOM, Routing, QC).",
                "100% elimination of LTMC upload rejections and manual Excel rework cycles.",
                "Secured FDA / ISO audit compliance for regulated healthcare operations."
            ]
        }
    ]

    for idx, s in enumerate(solutions_top):
        cx = cols_x[idx]
        cy = Inches(1.75)
        add_card(slide3, cx, cy, card3_w, card3_h)

        tb = slide3.shapes.add_textbox(cx + Inches(0.18), cy + Inches(0.12), card3_w - Inches(0.36), card3_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p_t = tf.paragraphs[0]
        p_t.text = s["type"]
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(8.5)
        p_t.font.bold = True
        p_t.font.color.rgb = BLUE_ACCENT

        p_cl = tf.add_paragraph()
        p_cl.text = s["client"]
        p_cl.font.name = "Calibri"
        p_cl.font.size = Pt(11)
        p_cl.font.bold = True
        p_cl.font.color.rgb = SLATE_900

        p_name = tf.add_paragraph()
        p_name.text = s["title"]
        p_name.font.name = "Calibri"
        p_name.font.size = Pt(12)
        p_name.font.bold = True
        p_name.font.color.rgb = NAVY_ACCENT
        p_name.space_after = Pt(2)

        p_d = tf.add_paragraph()
        p_d.text = s["desc"]
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = SLATE_700
        p_d.space_after = Pt(3)

        for pt in s["points"]:
            ppt = tf.add_paragraph()
            ppt.text = f"✓  {pt}"
            ppt.font.name = "Calibri"
            ppt.font.size = Pt(9)
            ppt.font.color.rgb = SLATE_700
            ppt.space_before = Pt(1)

    solutions_bot = [
        {
            "client": "L&T CONSTRUCTION & MINING MACHINERY",
            "type": "IMPLEMENTED SOLUTION",
            "title": "Custom B2B Enterprise Portal (DEMANS)",
            "desc": "Architected and delivered custom Dealer Management System (DEMANS) extending SAP S/4HANA core.",
            "points": [
                "Provided seamless dealer ordering, machine telemetry, and warranty registration without core ERP bloat.",
                "Real-time bidirectional synchronization with SAP Sales & Distribution (SD) and Materials Management (MM).",
                "Streamlined dealer lead-to-fulfillment cycle and eliminated manual processing backlogs."
            ]
        },
        {
            "client": "GLOBAL DELIVERY & GCC CAPABILITY",
            "type": "GCC & GLOBAL ENGAGEMENTS",
            "title": "Delivery Centers: USA  ·  Middle East (Qatar)  ·  India",
            "desc": "Operating scalable Offshore Development Centers (ODC) and follow-the-sun global delivery capability.",
            "points": [
                "USA: Enterprise GRC access governance and high-volume financial invoice automation (VS&Co, Prometheus).",
                "Middle East (Qatar / Kuwait): Omnichannel retail logistics and 3PL supply chain integration (Alghanim).",
                "India Delivery Hubs (Bangalore, Noida, Ranchi): CMMI Level 3 appraised engineering centers sustaining global enterprise SLAs."
            ]
        }
    ]

    bot_x = [Inches(0.8), Inches(6.833)]
    for idx, s in enumerate(solutions_bot):
        cx = bot_x[idx]
        cy = Inches(4.25)
        add_card(slide3, cx, cy, card3_w_large, card3_h)

        tb = slide3.shapes.add_textbox(cx + Inches(0.22), cy + Inches(0.12), card3_w_large - Inches(0.44), card3_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p_t = tf.paragraphs[0]
        p_t.text = s["type"]
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(8.5)
        p_t.font.bold = True
        p_t.font.color.rgb = BLUE_ACCENT

        p_cl = tf.add_paragraph()
        p_cl.text = s["client"]
        p_cl.font.name = "Calibri"
        p_cl.font.size = Pt(11)
        p_cl.font.bold = True
        p_cl.font.color.rgb = SLATE_900

        p_name = tf.add_paragraph()
        p_name.text = s["title"]
        p_name.font.name = "Calibri"
        p_name.font.size = Pt(12)
        p_name.font.bold = True
        p_name.font.color.rgb = NAVY_ACCENT
        p_name.space_after = Pt(2)

        p_d = tf.add_paragraph()
        p_d.text = s["desc"]
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = SLATE_700
        p_d.space_after = Pt(3)

        for pt in s["points"]:
            ppt = tf.add_paragraph()
            ppt.text = f"✓  {pt}"
            ppt.font.name = "Calibri"
            ppt.font.size = Pt(9)
            ppt.font.color.rgb = SLATE_700
            ppt.space_before = Pt(1)

    add_card(slide3, Inches(0.8), Inches(6.65), Inches(11.733), Inches(0.52), bg_color=WHITE, border_color=SLATE_200)
    tb_b3 = slide3.shapes.add_textbox(Inches(1.0), Inches(6.72), Inches(11.333), Inches(0.38))
    tf_b3 = tb_b3.text_frame
    tf_b3.word_wrap = True
    tf_b3.margin_left = tf_b3.margin_right = tf_b3.margin_top = tf_b3.margin_bottom = 0
    pb3 = tf_b3.paragraphs[0]
    pb3.text = "SOLUTION PORTFOLIO GROUNDING: Every reference represents delivered architectures across logistics, manufacturing, and data migration—governed by defined SLAs, zero-defect quality thresholds, and documented client ROI."
    pb3.font.name = "Calibri"
    pb3.font.size = Pt(10.5)
    pb3.font.bold = True
    pb3.font.color.rgb = BLUE_DARK

    slide3.notes_slide.notes_text_frame.text = (
        "KEY MESSAGE: Provide concrete, verifiable delivery proof points across logistics integration, high-tech discrete manufacturing, migration data trust, and global delivery centers in the USA, Middle East, and India.\n\n"
        "TALK TRACK (1 minute):\n"
        "\"To understand Lumbini's capability, look at what we have actually delivered for enterprise clients.\n\n"
        "In supply chain logistics, we architected the SAP-to-3PL integration for Alghanim Industries and DSV WMS—automating purchase orders, ASN receipts, goods issues, and nightly stock reconciliation across multi-facility operations. In high-tech manufacturing, we partnered with Tata Electronics and TSAT to build the 'Connected Enterprise', creating 3 super-interfaces that reduced shift reporting lag to real-time and slashed manual confirmations by 70%.\n\n"
        "At Healthium Medtech, we engineered a pre-migration data validation engine that eliminated 100% of upload rejections during their S/4HANA migration. For L&T, we built their dealer management portal, DEMANS, handling equipment configuration without modifying core ERP.\n\n"
        "Furthermore, our delivery capacity is truly global—with offshore and nearshore delivery centers supporting clients across the USA, the Middle East, and India under unified CMMI Level 3 quality controls.\"\n\n"
        "TRANSITION: \"Underpinning this delivery is our 13-year journey and strategic partnership within the SAP ecosystem.\""
    )
    print("Slide 3 configured.")

    # =========================================================================
    # SLIDE 4: OUR SAP JOURNEY AND STRATEGIC COMPETENCIES
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, BG_LIGHT)
    add_header(slide4, "Ecosystem Evolution & Strategic Pillars", "Our SAP Journey (2013–2026) & Competency Pillars", "From specialized SAP services to an accredited SAP Sell & Service Partner delivering Clean-Core innovation.")

    add_card(slide4, Inches(0.8), Inches(1.75), Inches(11.733), Inches(1.05), bg_color=WHITE, border_color=SLATE_200)
    time_box = slide4.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(11.333), Inches(0.85))
    tf_time = time_box.text_frame
    tf_time.word_wrap = True
    tf_time.margin_left = tf_time.margin_right = tf_time.margin_top = tf_time.margin_bottom = 0

    p_th = tf_time.paragraphs[0]
    p_th.text = "PARTNERSHIP EVOLUTION (2013 – 2026)"
    p_th.font.name = "Calibri"
    p_th.font.size = Pt(9.5)
    p_th.font.bold = True
    p_th.font.color.rgb = BLUE_ACCENT

    p_tm = tf_time.add_paragraph()
    p_tm.text = "2013: SAP Service Partner  ▸  2017: Enterprise Integrations & S/4HANA Advisory  ▸  2021: Cloud Extensions & BTP  ▸  2024: Supply Chain Advisory with 4flow  ▸  2026: Official SAP Sell & Service Partner"
    p_tm.font.name = "Calibri"
    p_tm.font.size = Pt(11)
    p_tm.font.bold = True
    p_tm.font.color.rgb = SLATE_900
    p_tm.space_before = Pt(3)

    p_td = tf_time.add_paragraph()
    p_td.text = "Over 13 years of continuous engineering maturity—from core ABAP/RICEF support to authorized SAP Sell & Service status, Clean-Core cloud extensions, and enterprise AI enablement."
    p_td.font.name = "Calibri"
    p_td.font.size = Pt(9.5)
    p_td.font.color.rgb = SLATE_700
    p_td.space_before = Pt(2)

    col4_w = Inches(2.78)
    col4_h = Inches(3.55)
    col4_x = [Inches(0.8), Inches(3.784), Inches(6.768), Inches(9.752)]

    pillars_data = [
        {
            "code": "PILLAR A",
            "title": "RISE with SAP",
            "sub": "S/4HANA Cloud Private Edition",
            "bullets": [
                "Clean-Core Architecture: Keeping standard transactional ledgers pristine by decoupling extensions.",
                "Custom Code Modernization: Auditing SPDD/SPAU, deprecating legacy modifications, and migrating to ABAP Cloud.",
                "Readiness & Cutover Assurance: End-to-end rehearsal migrations and minimum-downtime cutover governance."
            ]
        },
        {
            "code": "PILLAR B",
            "title": "SAP Business AI & BTP",
            "sub": "Intelligent Technology Fabric",
            "bullets": [
                "App Development & Automation: SAP Build, Build Process Automation, and central task routing.",
                "Database & Data Management: SAP HANA Cloud & Datasphere real-time data federation.",
                "Integration Suite (CPI): Enterprise API mediation, B2B/EDI trading partner flows, and Event Mesh.",
                "AI Foundation: Joule assistants, generative RAG on private data, and deterministic agentic gates."
            ]
        },
        {
            "code": "PILLAR C",
            "title": "SAP Business Data Cloud",
            "sub": "Unified Data & Semantics",
            "bullets": [
                "SAP Analytics Cloud (SAC): Live executive dashboards, predictive forecasting, and planning.",
                "SAP Datasphere & BW/4HANA: Business data fabric harmonizing distributed enterprise data.",
                "SAP Databricks & HANA Cloud: High-throughput lakehouse engineering with sub-second queries.",
                "Master Data Governance (MDG) & Reltio: Single source of truth for materials, customers, and suppliers."
            ]
        },
        {
            "code": "PILLAR D",
            "title": "SAP Human Capital Mgmt",
            "sub": "End-to-End Talent Solutions",
            "bullets": [
                "Core HR & Payroll: Compliant localization, multi-country payroll, and benefits administration.",
                "Workforce Management: Shift scheduling, time recording, and operational attendance tracking.",
                "Talent & Learning: Role-tailored learning management, performance tracking, and recruiting.",
                "Employee Experience: Modern Fiori / UI5 self-service portals (ESS/MSS) on mobile and web."
            ]
        }
    ]

    for idx, p in enumerate(pillars_data):
        cx = col4_x[idx]
        cy = Inches(2.95)
        add_card(slide4, cx, cy, col4_w, col4_h)

        tb = slide4.shapes.add_textbox(cx + Inches(0.15), cy + Inches(0.12), col4_w - Inches(0.3), col4_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = p["code"]
        p0.font.name = "Calibri"
        p0.font.size = Pt(8.5)
        p0.font.bold = True
        p0.font.color.rgb = BLUE_ACCENT

        p1 = tf.add_paragraph()
        p1.text = p["title"]
        p1.font.name = "Calibri"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = SLATE_900

        p2 = tf.add_paragraph()
        p2.text = p["sub"]
        p2.font.name = "Calibri"
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = SLATE_500
        p2.space_after = Pt(4)

        for b in p["bullets"]:
            pb = tf.add_paragraph()
            pb.text = f"•  {b}"
            pb.font.name = "Calibri"
            pb.font.size = Pt(9.2)
            pb.font.color.rgb = SLATE_700
            pb.space_before = Pt(2)

    add_card(slide4, Inches(0.8), Inches(6.62), Inches(11.733), Inches(0.55), bg_color=WHITE, border_color=SLATE_200)
    tb_b4 = slide4.shapes.add_textbox(Inches(1.0), Inches(6.68), Inches(11.333), Inches(0.42))
    tf_b4 = tb_b4.text_frame
    tf_b4.word_wrap = True
    tf_b4.margin_left = tf_b4.margin_right = tf_b4.margin_top = tf_b4.margin_bottom = 0
    pb4 = tf_b4.paragraphs[0]
    pb4.text = "STRATEGIC SUPPLY CHAIN COLLABORATION: Joint solution advisory with German consulting leader 4flow on closed-loop SAP Integrated Business Planning (SAP IBP)—connecting demand sensing and finite bottleneck optimization with SAP ACDOCA financial tie-outs."
    pb4.font.name = "Calibri"
    pb4.font.size = Pt(9.8)
    pb4.font.bold = True
    pb4.font.color.rgb = BLUE_DARK

    slide4.notes_slide.notes_text_frame.text = (
        "KEY MESSAGE: Walk through the evolution of Lumbini's SAP ecosystem journey from 2013 to 2026, presenting our 4 core competencies and strategic collaboration with 4flow.\n\n"
        "TALK TRACK (1 minute 45 seconds):\n"
        "\"Lumbini's SAP relationship is grounded in a 13-year trajectory. We began in 2013 as an SAP Service Partner, advanced into S/4HANA migrations and hybrid integrations by 2017, expanded into SAP BTP and cloud extensions in 2021, and in 2026 reached accredited SAP Sell & Service Partner status.\n\n"
        "Our capabilities are anchored around four strategic pillars:\n"
        "Pillar A is RISE with SAP—supporting private cloud enterprise transformations while enforcing the Clean-Core paradigm, ensuring customizations live outside the core.\n"
        "Pillar B is SAP Business AI and BTP—spanning application development, automation, database management, and the AI Foundation where Joule and agentic workflows are safely grounded in enterprise truth.\n"
        "Pillar C is SAP Business Data Cloud—unifying analytics across SAC, Datasphere, BW/4HANA, Databricks, and Master Data Governance so leadership has a single version of the truth.\n"
        "Pillar D is SAP HCM—covering core HR, payroll, workforce management, and mobile employee experiences.\n\n"
        "Additionally, we collaborate with German supply chain consulting leader 4flow on SAP IBP—connecting multi-tier demand sensing with physical plant capacity and live balance sheet reconciliations.\"\n\n"
        "TRANSITION: \"Next, let us dive into two specific enterprise integration case studies directly relevant to complex logistics landscapes.\""
    )
    print("Slide 4 configured.")

    # =========================================================================
    # SLIDE 5: CASE STUDY: ENTERPRISE AND LOGISTICS SYSTEMS INTEGRATION
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, BG_LIGHT)
    add_header(slide5, "Deep Integration Architecture", "Enterprise & Logistics Systems Integration", "Connecting ERP backbones with operational execution, third-party logistics (3PL), and shop-floor systems.")

    col5_w = Inches(5.7)
    col5_h = Inches(4.75)
    col5_x = [Inches(0.8), Inches(6.833)]

    # Case A: TEPL
    add_card(slide5, col5_x[0], Inches(1.75), col5_w, col5_h)
    tb_tepl = slide5.shapes.add_textbox(col5_x[0] + Inches(0.25), Inches(1.88), col5_w - Inches(0.5), col5_h - Inches(0.26))
    tf_tepl = tb_tepl.text_frame
    tf_tepl.word_wrap = True
    tf_tepl.margin_left = tf_tepl.margin_right = tf_tepl.margin_top = tf_tepl.margin_bottom = 0

    p_a0 = tf_tepl.paragraphs[0]
    p_a0.text = "CASE STUDY A: HIGH-PRECISION MANUFACTURING"
    p_a0.font.name = "Calibri"
    p_a0.font.size = Pt(9)
    p_a0.font.bold = True
    p_a0.font.color.rgb = BLUE_ACCENT

    p_a1 = tf_tepl.add_paragraph()
    p_a1.text = "Tata Electronics (TEPL & TSAT) — Connected Enterprise"
    p_a1.font.name = "Calibri"
    p_a1.font.size = Pt(14)
    p_a1.font.bold = True
    p_a1.font.color.rgb = SLATE_900

    sections_tepl = [
        ("Business Context", "High-precision electronics & semiconductor operations across corporate headquarters and multiple plants (Marigold & Jasmine plants)."),
        ("Integration Challenge", "Disconnected planning (SAP S/4HANA) and execution (Siemens/Cantier MES, APS) caused 1–2 shift reporting delays, manual PR creation, and lack of component traceability."),
        ("Architecture & Solution", "Consolidated 6 complex point-to-point concepts into 3 optimized 'Super-Interfaces' via SAP PI/PO & webMethods:\n  1. Outbound Material Master (Basic, Plant & Scheduling views)\n  2. Production Orders & Batch Routing synchronization\n  3. Inbound Confirmations & Goods Movements (MFBF automation)\nPlus Streamlit GRN Variance Management System for Jasmine plant."),
        ("Documented Results", "• Production reporting lag compressed from 1–2 shifts to near real-time.\n• Manual manufacturing confirmations reduced by ~70%.\n• Month-end financial close accelerated from 10 to 4 days.\n• Near-zero inventory variance on critical high-value materials.")
    ]

    for title, desc in sections_tepl:
        p_sec = tf_tepl.add_paragraph()
        p_sec.text = title.upper()
        p_sec.font.name = "Calibri"
        p_sec.font.size = Pt(9.5)
        p_sec.font.bold = True
        p_sec.font.color.rgb = NAVY_ACCENT
        p_sec.space_before = Pt(4)

        p_desc = tf_tepl.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = "Calibri"
        p_desc.font.size = Pt(9.5)
        p_desc.font.color.rgb = SLATE_700
        p_desc.space_before = Pt(1)

    # Case B: Alghanim
    add_card(slide5, col5_x[1], Inches(1.75), col5_w, col5_h)
    tb_alg = slide5.shapes.add_textbox(col5_x[1] + Inches(0.25), Inches(1.88), col5_w - Inches(0.5), col5_h - Inches(0.26))
    tf_alg = tb_alg.text_frame
    tf_alg.word_wrap = True
    tf_alg.margin_left = tf_alg.margin_right = tf_alg.margin_top = tf_alg.margin_bottom = 0

    p_b0 = tf_alg.paragraphs[0]
    p_b0.text = "CASE STUDY B: LOGISTICS & SUPPLY CHAIN INTEGRATION"
    p_b0.font.name = "Calibri"
    p_b0.font.size = Pt(9)
    p_b0.font.bold = True
    p_b0.font.color.rgb = BLUE_ACCENT

    p_b1 = tf_alg.add_paragraph()
    p_b1.text = "Alghanim Industries — SAP-to-3PL Logistics Integration"
    p_b1.font.name = "Calibri"
    p_b1.font.size = Pt(14)
    p_b1.font.bold = True
    p_b1.font.color.rgb = SLATE_900

    sections_alg = [
        ("Business Context", "Major commercial enterprise in Kuwait/Middle East managing high-volume distribution through external 3PL logistics partners (DSV WMS & Agility WMS)."),
        ("Integration Challenge", "Bridging enterprise sales & procurement in SAP with physical 3PL warehouse operations without manual handoffs, data loss, or inventory mismatch."),
        ("Architecture & Solution", "End-to-end bi-directional integration via REST APIs, SQL Server staging, and secure SFTP file drop automation:\n  • Inbound Flow: SAP PO/ASN generation -> 3PL receiving & QC -> automated GRN posting back to SAP.\n  • Outbound Flow: Store Delivery orders -> 3PL picking & packing -> automated PGI posting and ledger update.\n  • Master Data: SKU extension, batch expiry sync, and Sloc movements."),
        ("Documented Results", "• Daily midnight automated balance-in-hand reconciliation (RAP).\n• 100% elimination of manual re-keying across 3PL warehouse docks.\n• Zero discrepancy write-offs between 3PL storage and SAP core ledgers.")
    ]

    for title, desc in sections_alg:
        p_sec = tf_alg.add_paragraph()
        p_sec.text = title.upper()
        p_sec.font.name = "Calibri"
        p_sec.font.size = Pt(9.5)
        p_sec.font.bold = True
        p_sec.font.color.rgb = NAVY_ACCENT
        p_sec.space_before = Pt(4)

        p_desc = tf_alg.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = "Calibri"
        p_desc.font.size = Pt(9.5)
        p_desc.font.color.rgb = SLATE_700
        p_desc.space_before = Pt(1)

    add_card(slide5, Inches(0.8), Inches(6.62), Inches(11.733), Inches(0.55), bg_color=WHITE, border_color=SLATE_200)
    tb_b5 = slide5.shapes.add_textbox(Inches(1.0), Inches(6.68), Inches(11.333), Inches(0.42))
    tf_b5 = tb_b5.text_frame
    tf_b5.word_wrap = True
    tf_b5.margin_left = tf_b5.margin_right = tf_b5.margin_top = tf_b5.margin_bottom = 0
    pb5 = tf_b5.paragraphs[0]
    pb5.text = "STRATEGIC RELEVANCE TO SAFEXPRESS: Demonstrates proven capability in connecting heterogeneous enterprise cores (whether SAP or Oracle) with specialized logistics execution engines (such as PROPEL-i and 3PL hubs), guaranteeing sub-second synchronization and audited financial reconciliation."
    pb5.font.name = "Calibri"
    pb5.font.size = Pt(9.8)
    pb5.font.bold = True
    pb5.font.color.rgb = BLUE_DARK

    slide5.notes_slide.notes_text_frame.text = (
        "KEY MESSAGE: Prove deep, real-world capability in designing and implementing complex enterprise integrations connecting ERP backbones with logistics execution (3PL) and shop-floor operations.\n\n"
        "TALK TRACK (2 minutes):\n"
        "\"Here are two detailed architectural case studies demonstrating our integration capabilities.\n\n"
        "Case A is Tata Electronics. In a complex high-precision environment, TEPL faced significant lag between planning in SAP S/4HANA and execution on the shop floor. We re-engineered six point-to-point connections into three robust 'super-interfaces'—handling material master syndication, production orders, and automated confirmation backflushing. This eliminated shift reporting lag entirely and cut manual confirmations by 70%.\n\n"
        "Case B is especially relevant to logistics: Alghanim Industries' integration with DSV and Agility WMS. Alghanim needed seamless coordination between enterprise orders and external third-party logistics providers. We designed a bi-directional integration layer using APIs, SQL Server staging, and secure SFTP. When a PO or ASN is generated in SAP, it drops directly to 3PL queues; when items are received, inspected, and put away, GRNs post back automatically. Similarly, outbound delivery orders trigger picking and packing, returning PGI files to decrement inventory in SAP, with an automated midnight reconciliation engine auditing balance-in-hand.\n\n"
        "For SafeExpress, this proves our ability to connect core systems with specialized logistics platforms—whether connecting your Oracle enterprise core to PROPEL-i, hub scanners, or external partner networks—with complete data integrity.\"\n\n"
        "TRANSITION: \"In addition to integration, enterprise success requires data trust and structured transformation governance, as shown in our next case studies.\""
    )
    print("Slide 5 configured.")

    # =========================================================================
    # SLIDE 6: CASE STUDY: DATA TRUST, TRANSFORMATION AND INDUSTRY SOLUTIONS
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, BG_LIGHT)
    add_header(slide6, "Data Governance & Transformation", "Data Trust, Migration Assurance & Precision Transformation", "Establishing verifiable data foundations and disciplined engineering frameworks for complex enterprise programs.")

    col6_w = Inches(5.7)
    col6_h = Inches(4.75)
    col6_x = [Inches(0.8), Inches(6.833)]

    # Case A: Healthium Medtech
    add_card(slide6, col6_x[0], Inches(1.75), col6_w, col6_h)
    tb_hlt = slide6.shapes.add_textbox(col6_x[0] + Inches(0.25), Inches(1.88), col6_w - Inches(0.5), col6_h - Inches(0.26))
    tf_hlt = tb_hlt.text_frame
    tf_hlt.word_wrap = True
    tf_hlt.margin_left = tf_hlt.margin_right = tf_hlt.margin_top = tf_hlt.margin_bottom = 0

    p_h0 = tf_hlt.paragraphs[0]
    p_h0.text = "CASE STUDY A: REGULATED LIFE SCIENCES & HEALTHCARE"
    p_h0.font.name = "Calibri"
    p_h0.font.size = Pt(9)
    p_h0.font.bold = True
    p_h0.font.color.rgb = BLUE_ACCENT

    p_h1 = tf_hlt.add_paragraph()
    p_h1.text = "Healthium Medtech — Pre-SAP Migration Data Trust Tool"
    p_h1.font.name = "Calibri"
    p_h1.font.size = Pt(14)
    p_h1.font.bold = True
    p_h1.font.color.rgb = SLATE_900

    sections_hlt = [
        ("Business Context", "Global medical device manufacturer migrating complex enterprise data from SAP ECC to S/4HANA under strict FDA and ISO regulatory compliance standards."),
        ("Data Migration Challenge", "Uploading data directly via SAP LTMC repeatedly failed due to cross-object dependency mismatches (Material, BOM, Routing, Quality), UOM inconsistencies, and missing configuration keys."),
        ("Architecture & Solution", "Engineered a custom, standalone Pre-SAP Validation & ETL Framework complementing SAP LTMC:\n  • Automated validation engine checking cross-sheet dependencies before upload.\n  • Automated UOM standardization, duplicate detection, and mandatory config verification.\n  • Interactive SME exception dashboard with controlled inline editing."),
        ("Documented Results", "• 100% elimination of LTMC upload rejections across master data waves.\n• Drastically reduced manual Excel reconciliation and rehearsal cycles.\n• Established an immutable, audit-ready data lineage for regulatory sign-off.")
    ]

    for title, desc in sections_hlt:
        p_sec = tf_hlt.add_paragraph()
        p_sec.text = title.upper()
        p_sec.font.name = "Calibri"
        p_sec.font.size = Pt(9.5)
        p_sec.font.bold = True
        p_sec.font.color.rgb = NAVY_ACCENT
        p_sec.space_before = Pt(4)

        p_desc = tf_hlt.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = "Calibri"
        p_desc.font.size = Pt(9.5)
        p_desc.font.color.rgb = SLATE_700
        p_desc.space_before = Pt(1)

    # Case B: Hical Technologies
    add_card(slide6, col6_x[1], Inches(1.75), col6_w, col6_h)
    tb_hic = slide6.shapes.add_textbox(col6_x[1] + Inches(0.25), Inches(1.88), col6_w - Inches(0.5), col6_h - Inches(0.26))
    tf_hic = tb_hic.text_frame
    tf_hic.word_wrap = True
    tf_hic.margin_left = tf_hic.margin_right = tf_hic.margin_top = tf_hic.margin_bottom = 0

    p_c0 = tf_hic.paragraphs[0]
    p_c0.text = "CASE STUDY B: AEROSPACE & DEFENSE TRANSFORMATION (STRATEGIC PROPOSAL)"
    p_c0.font.name = "Calibri"
    p_c0.font.size = Pt(9)
    p_c0.font.bold = True
    p_c0.font.color.rgb = BLUE_ACCENT

    p_c1 = tf_hic.add_paragraph()
    p_c1.text = "Hical Technologies — Live CXO Cockpits & Traceability Blueprint"
    p_c1.font.name = "Calibri"
    p_c1.font.size = Pt(14)
    p_c1.font.bold = True
    p_c1.font.color.rgb = SLATE_900

    sections_hic = [
        ("Business Context", "AS9100-certified aerospace & defense component manufacturer requiring real-time executive visibility and foolproof shop-floor traceability."),
        ("Transformation Scope", "1. Strategic CXO Dashboards: Live financial, supply, and manufacturing cockpits reading live S/4HANA tables without overnight ETL or data lake delay.\n2. TRACE n TRACE: Poka-yoke shop-floor execution using handheld terminals with offline edge caching and two-tier digital approval desks."),
        ("Proposed Architecture", "• In-memory HANA calculation views resolving deep multi-level BOMs in milliseconds.\n• Workload management limits ring-fencing live transactional performance.\n• Fixed-price phased delivery with 4 milestone payment gates tied to verified working deliverables."),
        ("Demonstrated Capability", "Proves architectural mastery in zero-copy analytics, shop-floor error prevention, and deliverable-linked governance without risking core ERP ledger integrity.")
    ]

    for title, desc in sections_hic:
        p_sec = tf_hic.add_paragraph()
        p_sec.text = title.upper()
        p_sec.font.name = "Calibri"
        p_sec.font.size = Pt(9.5)
        p_sec.font.bold = True
        p_sec.font.color.rgb = NAVY_ACCENT
        p_sec.space_before = Pt(4)

        p_desc = tf_hic.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = "Calibri"
        p_desc.font.size = Pt(9.5)
        p_desc.font.color.rgb = SLATE_700
        p_desc.space_before = Pt(1)

    add_card(slide6, Inches(0.8), Inches(6.62), Inches(11.733), Inches(0.55), bg_color=WHITE, border_color=SLATE_200)
    tb_b6 = slide6.shapes.add_textbox(Inches(1.0), Inches(6.68), Inches(11.333), Inches(0.42))
    tf_b6 = tb_b6.text_frame
    tf_b6.word_wrap = True
    tf_b6.margin_left = tf_b6.margin_right = tf_b6.margin_top = tf_b6.margin_bottom = 0
    pb6 = tf_b6.paragraphs[0]
    pb6.text = "AI-READY DATA FOUNDATIONS: 1. Data Integrity Before AI (models are only as good as the underlying data)  ·  2. Disciplined Milestone Delivery (payment & sprint acceptance tied to verified working software)  ·  3. Zero-Copy Architecture (computing where data lives)."
    pb6.font.name = "Calibri"
    pb6.font.size = Pt(9.8)
    pb6.font.bold = True
    pb6.font.color.rgb = BLUE_DARK

    slide6.notes_slide.notes_text_frame.text = (
        "KEY MESSAGE: Demonstrate capability in solving complex data trust, migration validation, and industry transformation challenges—connecting data quality directly to AI readiness and disciplined delivery.\n\n"
        "TALK TRACK (2 minutes):\n"
        "\"A critical lesson from our enterprise engagements is that technology transformation—and especially AI transformation—fails without data trust.\n\n"
        "At Healthium Medtech, standard migration tools repeatedly failed because underlying master data had cross-sheet dependency errors, unit-of-measure discrepancies, and missing configuration objects. We engineered a dedicated pre-SAP ETL and validation engine that intercepted data, ran automated business rule validations, surfaced exceptions on an interactive dashboard, and produced 100% clean upload templates. This eliminated LTMC upload failures entirely.\n\n"
        "In our aerospace transformation architecture for Hical Technologies, we proposed two high-impact solutions: live CXO cockpits powered by native in-memory HANA calculation views—calculating directly where the data already lives without overnight ETL batch latency—and shop-floor barcode poka-yoke tracking with offline edge caching and two-tier digital approval gates.\n\n"
        "Notice the delivery approach we designed for Hical: an 18-week phased timeline with four milestone payment gates tied strictly to verified working deliverables. This reflects our core philosophy: we hold ourselves accountable to working software, not just hours worked.\n\n"
        "For an enterprise pursuing AI initiatives, clean data, governed pipelines, and disciplined milestone execution are non-negotiable foundations.\"\n\n"
        "TRANSITION: \"Finally, let us review our broader enterprise ecosystem of clients, partners, and our vision for collaborating with SafeExpress.\""
    )
    print("Slide 6 configured.")

    # =========================================================================
    # SLIDE 7: CLIENTS, PARTNERS AND CLOSING (DEDICATED ECOSYSTEM SLIDE)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, BG_LIGHT)
    add_header(slide7, "Our Enterprise Ecosystem & Strategic Alliances", "Trusted by Global Leaders, Public Sector Giants & Strategic Partners", "Delivering scalable engineering, mission-critical integration, and enterprise governance across diverse industries.")

    quad_w = Inches(2.78)
    quad_h = Inches(4.75)
    quad_x = [Inches(0.8), Inches(3.784), Inches(6.768), Inches(9.752)]

    ecosystem_data = [
        {
            "category": "GLOBAL CLIENTS",
            "tag": "INTERNATIONAL ENTERPRISES",
            "items": [
                ("VS&Co (Victoria's Secret)", "Scaled AI-driven financial invoice processing and SAP GRC compliant access management across 15+ business divisions."),
                ("Prometheus Group", "Integrated global plant maintenance and operational asset reliability workflows directly with SAP PM/MM enterprise cores."),
                ("Elior (Elior India)", "Automated SAP S/4HANA e-invoicing (IRN digital signing / ZEINVOICE dispatch) and enterprise billing reconciliation."),
                ("Alghanim Industries", "Deployed end-to-end SAP-to-3PL logistics integration (DSV & Agility WMS) automating PO, ASN, GRN, PGI, and stock audits."),
                ("4flow", "Co-architected next-generation SAP IBP supply chain planning, freight order RAP services, and closed-loop demand sensing.")
            ]
        },
        {
            "category": "DOMESTIC CLIENTS",
            "tag": "INDIAN INDUSTRIAL LEADERS",
            "items": [
                ("Tata Electronics (TEPL)", "Delivered 3 'Super-Interfaces' between SAP S/4HANA and MES/APS, cutting shift reporting lag to real-time."),
                ("Tata Semiconductors (TSAT)", "Architected high-precision semiconductor shopfloor execution and wafer-level batch traceability workflows."),
                ("L&T Construction & Mining", "Built custom Dealer Management System (DEMANS) web platform integrated seamlessly with SAP S/4HANA core."),
                ("Hical Technologies", "Formulated strategic architecture for live in-memory HANA calculation views and shopfloor poka-yoke batch traceability."),
                ("Healthium Medtech", "Engineered pre-SAP automated ETL & validation engine for 100% error-free ECC to S/4HANA data migration.")
            ]
        },
        {
            "category": "PSU ENTERPRISE CLIENTS",
            "tag": "PUBLIC SECTOR & UTILITIES",
            "items": [
                ("MOIL Limited", "Delivered end-to-end SAP ERP support and seamless Government e-Marketplace (GeM) integration via PI/PO."),
                ("NMDC", "Supported large-scale mining enterprise ERP operations, materials governance, and heavy supply chain logistics."),
                ("Petronet MHB", "Engineered cross-country hydrocarbon pipeline logistics, plant maintenance, and financial controlling ERP support."),
                ("TVNL (Tenughat Vidyut)", "Implemented end-to-end generation utility SAP ERP and executed complex SRM technical upgrade."),
                ("JBVNL (Jharkhand Bijli)", "Executed state-wide power distribution ERP rollout across FICO, MM, PS, and HCM managing complex billing cutovers."),
                ("BHEL", "Heavy electrical manufacturing SAP consulting, plant asset management, and shopfloor systems support.")
            ]
        },
        {
            "category": "STRATEGIC PARTNERS",
            "tag": "ECOSYSTEM & ALLIANCES",
            "items": [
                ("Gyansis", "Enterprise SAP consulting and digital transformation co-delivery alliance for complex cloud migrations."),
                ("Inchure", "Strategic technology partner collaborating on enterprise digital systems integration and specialized workflow digitization."),
                ("Stellium", "Supply chain and digital manufacturing consulting partner co-architecting integrated logistics, SAP IBP, and warehouse operations."),
                ("SAP (Sell & Service)", "Accredited dual-status official SAP partner driving RISE with SAP, Clean Core, and BTP innovations."),
                ("SafeExpress", "Valued customer for 3+ years; collaborating on enterprise operations, system stability, and future digital modernization.")
            ]
        }
    ]

    for idx, quad in enumerate(ecosystem_data):
        cx = quad_x[idx]
        cy = Inches(1.75)
        add_card(slide7, cx, cy, quad_w, quad_h)

        tb = slide7.shapes.add_textbox(cx + Inches(0.14), cy + Inches(0.12), quad_w - Inches(0.28), quad_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p_t = tf.paragraphs[0]
        p_t.text = quad["tag"]
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(8)
        p_t.font.bold = True
        p_t.font.color.rgb = BLUE_ACCENT

        p_cat = tf.add_paragraph()
        p_cat.text = quad["category"]
        p_cat.font.name = "Calibri"
        p_cat.font.size = Pt(12)
        p_cat.font.bold = True
        p_cat.font.color.rgb = SLATE_900
        p_cat.space_after = Pt(4)

        for name, story in quad["items"]:
            pn = tf.add_paragraph()
            pn.text = f"▸ {name}"
            pn.font.name = "Calibri"
            pn.font.size = Pt(9.5)
            pn.font.bold = True
            pn.font.color.rgb = NAVY_ACCENT
            pn.space_before = Pt(3)

            ps = tf.add_paragraph()
            ps.text = story
            ps.font.name = "Calibri"
            ps.font.size = Pt(8.2)
            ps.font.color.rgb = SLATE_700
            ps.space_before = Pt(1)

    # Executive Closing Callout Banner (Base of Slide 7)
    add_card(slide7, Inches(0.8), Inches(6.6), Inches(11.733), Inches(0.65), bg_color=NAVY_DARK, border_color=None)
    tb_b7 = slide7.shapes.add_textbox(Inches(1.0), Inches(6.64), Inches(11.333), Inches(0.55))
    tf_b7 = tb_b7.text_frame
    tf_b7.word_wrap = True
    tf_b7.margin_left = tf_b7.margin_right = tf_b7.margin_top = tf_b7.margin_bottom = 0

    p_close = tf_b7.paragraphs[0]
    p_close.text = "BEYOND RESOURCES. BUILT AROUND SOLUTIONS, INTEGRATION, AND BUSINESS OUTCOMES."
    p_close.font.name = "Calibri"
    p_close.font.size = Pt(11)
    p_close.font.bold = True
    p_close.font.color.rgb = RGBColor(56, 189, 248)

    p_inv = tf_b7.add_paragraph()
    p_inv.text = "Discussion Invitation: Explore where Lumbini's enterprise integration, data readiness, and transformation capabilities can complement SafeExpress's technology roadmap."
    p_inv.font.name = "Calibri"
    p_inv.font.size = Pt(9.8)
    p_inv.font.color.rgb = WHITE
    p_inv.space_before = Pt(2)

    slide7.notes_slide.notes_text_frame.text = (
        "KEY MESSAGE: Conclude with a strong, credible ecosystem view spanning global enterprises, domestic industrial leaders, public sector giants, and strategic alliances—ending on a collaborative, solution-oriented closing message.\n\n"
        "TALK TRACK (45 seconds):\n"
        "\"To conclude, Lumbini is privileged to serve an extraordinary ecosystem of enterprise clients and partners.\n\n"
        "Globally, we work with Victoria's Secret, Prometheus Group, Elior, Alghanim Industries, and 4flow. In the Indian domestic market, we support leaders like Tata Electronics, Tata Semiconductor, L&T, Hical Technologies, and Healthium Medtech. In the public sector, we sustain mission-critical ERP landscapes for MOIL, NMDC, Petronet MHB, TVNL, JBVNL, and BHEL. And we co-innovate alongside strategic partners such as Gyansis, Inchure, Stellium, and SAP.\n\n"
        "SafeExpress has been a cornerstone partner for Lumbini over the past three years. Our positioning today is clear: we are beyond resources. We are built around solutions, integration, and business outcomes.\n\n"
        "We welcome the opportunity to discuss where our integration engineering, data readiness frameworks, and delivery governance can best complement your internal technology and AI transformation roadmap.\n\n"
        "Thank you, and we look forward to the discussion.\""
    )
    print("Slide 7 configured.")

    # Save presentation
    output_path = "Lumbini_SafeExpress_Executive_Capabilities.pptx"
    prs.save(output_path)
    print(f"\nSuccessfully generated and saved presentation: {output_path}")
    print(f"Total slides: {len(prs.slides)}")

if __name__ == "__main__":
    create_deck()

