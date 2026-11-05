import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

def build_presentation(output_path="Lumbini_SAP_ME_DMC_AMS_Proposal.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # -------------------------------------------------------------
    # Brand Design Tokens (Matching Template.pptx & Brand Guidelines)
    # -------------------------------------------------------------
    BRAND_NAVY = RGBColor(20, 30, 45)         # #141E2D Deep Charcoal / Title Dark
    DEEP_BLUE = RGBColor(30, 97, 187)         # #1E61BB Brand Deep Blue
    PRIMARY_BLUE = RGBColor(0, 102, 180)      # #0066B4 / #006FC9 Lumbini Blue
    SKY_BLUE = RGBColor(0, 129, 226)          # #0081E2 Tech Cyan / Highlight Blue
    ACCENT_ORANGE = RGBColor(247, 150, 70)    # #F79646 Accent Warm Amber
    AMBER_DARK = RGBColor(230, 115, 0)        # #E67300 Warm Orange Divider
    
    SURFACE_WHITE = RGBColor(255, 255, 255)   # #FFFFFF Card Surface
    BG_LIGHT = RGBColor(248, 250, 252)        # #F8FAFC Subtle background tint
    BORDER_SLATE = RGBColor(226, 232, 240)    # #E2E8F0 Card Stroke
    BORDER_BLUE = RGBColor(190, 215, 245)     # Soft blue highlight border
    
    TEXT_DARK = RGBColor(20, 30, 45)          # #141E2D Primary Heading
    TEXT_BODY = RGBColor(45, 64, 80)          # #2D4050 High contrast body text
    TEXT_MUTED = RGBColor(100, 116, 139)      # #64748B Secondary / Footer text
    TEXT_LIGHT = RGBColor(255, 255, 255)      # White
    
    TAG_BG_BLUE = RGBColor(238, 246, 255)     # Pill badge background
    TAG_BG_ORANGE = RGBColor(255, 247, 237)   # Pill badge orange background
    
    LOGO_PATH = os.path.join("assets", "lumbini_logo.png")
    BG_GRAPHIC_PATH = os.path.join("assets", "title_bg_graphic.png")
    TOTAL_SLIDES = 7

    # -------------------------------------------------------------
    # Layout Helpers
    # -------------------------------------------------------------
    def add_base_slide():
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_LIGHT
        bg.line.fill.background()
        
        # Subtle top brand accent line
        top_accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.04))
        top_accent.fill.solid()
        top_accent.fill.fore_color.rgb = PRIMARY_BLUE
        top_accent.line.fill.background()
        
        return slide

    def add_header(slide, heading_text, sub_tagline):
        # Vertical Orange Accent Bar (exact signature element from Template.pptx)
        v_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.55), Inches(0.09), Inches(0.65))
        v_bar.fill.solid()
        v_bar.fill.fore_color.rgb = ACCENT_ORANGE
        v_bar.line.fill.background()
        
        # Heading
        h_box = slide.shapes.add_textbox(Inches(1.02), Inches(0.48), Inches(9.8), Inches(0.48))
        tf_h = h_box.text_frame
        tf_h.word_wrap = True
        tf_h.margin_left = tf_h.margin_top = tf_h.margin_right = tf_h.margin_bottom = 0
        p_h = tf_h.paragraphs[0]
        p_h.text = heading_text
        p_h.font.name = "Inter"
        p_h.font.size = Pt(22)
        p_h.font.bold = True
        p_h.font.color.rgb = TEXT_DARK
        
        # Sub tagline
        s_box = slide.shapes.add_textbox(Inches(1.02), Inches(0.98), Inches(9.8), Inches(0.28))
        tf_s = s_box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
        p_s = tf_s.paragraphs[0]
        p_s.text = sub_tagline
        p_s.font.name = "Inter"
        p_s.font.size = Pt(11)
        p_s.font.bold = True
        p_s.font.color.rgb = PRIMARY_BLUE
        
        # Top-right Lumbini Elite Logo
        if os.path.exists(LOGO_PATH):
            slide.shapes.add_picture(LOGO_PATH, Inches(11.1), Inches(0.45), width=Inches(1.5))

    def add_footer(slide, slide_num):
        # Divider Line
        div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.01))
        div.fill.solid()
        div.fill.fore_color.rgb = BORDER_SLATE
        div.line.fill.background()
        
        # Left Text
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.06), Inches(9.0), Inches(0.26))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = "Lumbini Elite Solutions & Services | Elitia Enterprise Suite | Confidential"
        p.font.name = "Inter"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MUTED
        
        # Right Slide Number
        tx_num = slide.shapes.add_textbox(Inches(10.5), Inches(7.06), Inches(2.033), Inches(0.26))
        tf_n = tx_num.text_frame
        tf_n.word_wrap = True
        tf_n.margin_right = tf_n.margin_top = 0
        p_n = tf_n.paragraphs[0]
        p_n.alignment = PP_ALIGN.RIGHT
        p_n.text = f"Slide {slide_num} of {TOTAL_SLIDES}"
        p_n.font.name = "Inter"
        p_n.font.size = Pt(8.5)
        p_n.font.color.rgb = TEXT_MUTED

    def create_card(slide, left, top, width, height, border_color=BORDER_SLATE, bg_color=SURFACE_WHITE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # =============================================================
    # SLIDE 1: Title Slide & Partnership Positioning
    # =============================================================
    s1 = prs.slides.add_slide(prs.slide_layouts[6])
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = SURFACE_WHITE
    bg1.line.fill.background()
    
    # Background architectural isometric graphic on left
    if os.path.exists(BG_GRAPHIC_PATH):
        s1.shapes.add_picture(BG_GRAPHIC_PATH, Inches(-0.2), Inches(0.2), width=Inches(6.8))
        
    # Top Right Logo
    if os.path.exists(LOGO_PATH):
        s1.shapes.add_picture(LOGO_PATH, Inches(10.3), Inches(0.65), width=Inches(2.2))
        
    # Title Category Pill
    cat_badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.85), Inches(4.3), Inches(0.35))
    cat_badge.fill.solid()
    cat_badge.fill.fore_color.rgb = TAG_BG_BLUE
    cat_badge.line.color.rgb = BORDER_BLUE
    cat_badge.line.width = Pt(1)
    tf_cb = cat_badge.text_frame
    tf_cb.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_cb.margin_left = Inches(0.15)
    p_cb = tf_cb.paragraphs[0]
    p_cb.text = "ENTERPRISE AMS STRATEGIC PROPOSAL"
    p_cb.font.name = "Inter"
    p_cb.font.size = Pt(9.5)
    p_cb.font.bold = True
    p_cb.font.color.rgb = PRIMARY_BLUE

    # Main Title
    t_box = s1.shapes.add_textbox(Inches(0.9), Inches(2.35), Inches(10.5), Inches(1.5))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = "SAP Manufacturing Execution (SAP ME) &\nSAP Digital Manufacturing (SAP DMC)"
    p_t.font.name = "Poppins"
    p_t.font.size = Pt(28)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_DARK
    
    # Orange Accent Divider Line (matching Template.pptx Freeform 4912)
    div1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(4.05), Inches(5.8), Inches(0.05))
    div1.fill.solid()
    div1.fill.fore_color.rgb = AMBER_DARK
    div1.line.fill.background()
    
    # Tagline / Subtitle
    sub_box = s1.shapes.add_textbox(Inches(0.9), Inches(4.25), Inches(10.5), Inches(0.7))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_left = tf_sub.margin_top = 0
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "Driving Resilient Shop-Floor Operations through Expert L1/L2 Support and End-to-End Enterprise Integration"
    p_sub.font.name = "Poppins"
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = PRIMARY_BLUE
    
    # Credential Callout Card (Bottom Left / Center)
    cred_card = create_card(s1, 0.9, 5.25, 8.2, 1.45, border_color=BORDER_BLUE, bg_color=TAG_BG_BLUE)
    tf_cc = cred_card.text_frame
    tf_cc.word_wrap = True
    tf_cc.margin_left = Inches(0.2)
    tf_cc.margin_top = Inches(0.15)
    
    p_cc1 = tf_cc.paragraphs[0]
    p_cc1.text = "OFFICIAL SAP TRUSTED PARTNER | SELL & SERVICE PARTNER"
    p_cc1.font.name = "Inter"
    p_cc1.font.size = Pt(9.5)
    p_cc1.font.bold = True
    p_cc1.font.color.rgb = DEEP_BLUE
    
    p_cc2 = tf_cc.add_paragraph()
    p_cc2.text = "Actively delivering end-to-end RISE with SAP and GROW with SAP enterprise transformations across hybrid onsite/offshore delivery models. Tailored to meet Panasonic global manufacturing standards with 24/7 mission-critical operational resilience."
    p_cc2.font.name = "Inter"
    p_cc2.font.size = Pt(9)
    p_cc2.font.color.rgb = TEXT_BODY
    
    # Bottom Right Pill Badge (matching Template.pptx 'Company Profile' pill)
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.6), Inches(5.95), Inches(3.2), Inches(0.75))
    pill.fill.solid()
    pill.fill.fore_color.rgb = DEEP_BLUE
    pill.line.fill.background()
    tf_p = pill.text_frame
    tf_p.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_p = tf_p.paragraphs[0]
    p_p.alignment = PP_ALIGN.CENTER
    p_p.text = "Enterprise AMS Proposal"
    p_p.font.name = "Calibri Light"
    p_p.font.size = Pt(15)
    p_p.font.bold = True
    p_p.font.color.rgb = TEXT_LIGHT

    # =============================================================
    # SLIDE 2: Core Capabilities & Ecosystem
    # =============================================================
    s2 = add_base_slide()
    add_header(s2, "Lumbini Elite Solutions – Core Capabilities & Ecosystem", 
               "Technological Breadth Beyond Standard ERP | Advanced Manufacturing & Cloud Extensions")
    add_footer(s2, 2)
    
    # Top Summary Card
    top_c2 = create_card(s2, 0.8, 1.4, 11.733, 0.95, border_color=BORDER_BLUE, bg_color=TAG_BG_BLUE)
    tf_t2 = top_c2.text_frame
    tf_t2.word_wrap = True
    tf_t2.margin_left = Inches(0.2)
    tf_t2.margin_top = Inches(0.12)
    p_t2_1 = tf_t2.paragraphs[0]
    p_t2_1.text = "ENTERPRISE MANUFACTURING EXCELLENCE & DUAL ECOSYSTEM ADVANTAGE"
    p_t2_1.font.name = "Inter"
    p_t2_1.font.size = Pt(9.5)
    p_t2_1.font.bold = True
    p_t2_1.font.color.rgb = PRIMARY_BLUE
    p_t2_2 = tf_t2.add_paragraph()
    p_t2_2.text = "Lumbini Elite combines official SAP Sell & Service partner status with deep shop-floor MES engineering and proprietary microservices innovation via Elitia Technologies to ensure continuous manufacturing availability."
    p_t2_2.font.name = "Inter"
    p_t2_2.font.size = Pt(9)
    p_t2_2.font.color.rgb = TEXT_BODY

    # 4 Pillar Cards
    pillars = [
        ("Official SAP Partner", "Sell & Service Dual Status", [
            "Accredited SAP Sell & Service Partner.",
            "Proven delivery across global transformation mandates.",
            "Active RISE with SAP and GROW with SAP rollouts.",
            "Bilingual, follow-the-sun global support capacity."
        ]),
        ("Digital Manufacturing", "SAP ME & SAP DMC Mastery", [
            "Deep expertise in SAP ME 15.x and Cloud DMC.",
            "Shop-floor execution, POD configuration & SFC tracking.",
            "Resource tracking, OEE, and scrap recording.",
            "PLC/SCADA, PCo, and machine-level telemetry integration."
        ]),
        ("Enterprise Platforms", "SAP BTP, SBPA & MDG", [
            "SAP Business Technology Platform (BTP) integration.",
            "Automated workflows with Build Process Automation.",
            "Master Data Governance (MDG) for clean routing & BOMs.",
            "Cloud Integration (CPI) for real-time plant syncing."
        ]),
        ("Custom Microservices", "Elitia Technologies Suite", [
            "Bespoke manufacturing extensions outside core ERP.",
            "Modern decoupled microservices & reactive APIs.",
            "High-throughput edge computing for high-volume lines.",
            "Zero core modification preserving clean ERP core."
        ])
    ]
    
    col_w = 2.78
    gap = 0.2
    for i, (title, sub, bullets) in enumerate(pillars):
        cx = 0.8 + i * (col_w + gap)
        card = create_card(s2, cx, 2.5, col_w, 4.3)
        
        # Header Accent Strip
        hdr_bar = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cx + 0.15), Inches(2.65), Inches(col_w - 0.3), Inches(0.65))
        hdr_bar.fill.solid()
        hdr_bar.fill.fore_color.rgb = TAG_BG_BLUE if i < 3 else TAG_BG_ORANGE
        hdr_bar.line.fill.background()
        tf_hb = hdr_bar.text_frame
        tf_hb.word_wrap = True
        tf_hb.margin_left = Inches(0.1)
        tf_hb.margin_top = Inches(0.08)
        p_hbt = tf_hb.paragraphs[0]
        p_hbt.text = title
        p_hbt.font.name = "Inter"
        p_hbt.font.size = Pt(10.5)
        p_hbt.font.bold = True
        p_hbt.font.color.rgb = PRIMARY_BLUE if i < 3 else AMBER_DARK
        p_hbs = tf_hb.add_paragraph()
        p_hbs.text = sub
        p_hbs.font.name = "Inter"
        p_hbs.font.size = Pt(8.5)
        p_hbs.font.color.rgb = TEXT_MUTED

        # Bullets
        tx = s2.shapes.add_textbox(Inches(cx + 0.15), Inches(3.45), Inches(col_w - 0.3), Inches(3.2))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        for b_idx, bullet in enumerate(bullets):
            p = tf.paragraphs[0] if b_idx == 0 else tf.add_paragraph()
            p.text = f"• {bullet}"
            p.font.name = "Inter"
            p.font.size = Pt(9)
            p.font.color.rgb = TEXT_BODY
            p.space_after = Pt(6)

    # =============================================================
    # SLIDE 3: Manufacturing Digital Thread
    # =============================================================
    s3 = add_base_slide()
    add_header(s3, "Understanding the Manufacturing Digital Thread", 
               "Connecting Business Intent to Plant-Floor Execution | End-to-End Operational Integrity")
    add_footer(s3, 3)
    
    # Left Hero Card (Concept & Context)
    left_c3 = create_card(s3, 0.8, 1.4, 3.8, 5.4, border_color=BORDER_BLUE, bg_color=SURFACE_WHITE)
    tf_l3 = left_c3.text_frame
    tf_l3.word_wrap = True
    tf_l3.margin_left = Inches(0.25)
    tf_l3.margin_top = Inches(0.2)
    
    p_l3_0 = tf_l3.paragraphs[0]
    p_l3_0.text = "THE STRATEGIC CHALLENGE"
    p_l3_0.font.name = "Inter"
    p_l3_0.font.size = Pt(10)
    p_l3_0.font.bold = True
    p_l3_0.font.color.rgb = ACCENT_ORANGE
    
    p_l3_1 = tf_l3.add_paragraph()
    p_l3_1.text = "How does the business connect to the shop floor?"
    p_l3_1.font.name = "Inter"
    p_l3_1.font.size = Pt(14)
    p_l3_1.font.bold = True
    p_l3_1.font.color.rgb = TEXT_DARK
    p_l3_1.space_after = Pt(8)
    
    p_l3_2 = tf_l3.add_paragraph()
    p_l3_2.text = "In high-throughput enterprise manufacturing (such as Panasonic's electronics and battery operations), commercial planning in SAP ERP must translate flawlessly into millisecond-accurate production execution."
    p_l3_2.font.name = "Inter"
    p_l3_2.font.size = Pt(9.5)
    p_l3_2.font.color.rgb = TEXT_BODY
    p_l3_2.space_after = Pt(8)
    
    p_l3_3 = tf_l3.add_paragraph()
    p_l3_3.text = "Lumbini Elite eliminates the critical friction points where ERP schedules disconnect from plant reality, guaranteeing data fidelity, synchronizing work orders, and stabilizing MES pipelines."
    p_l3_3.font.name = "Inter"
    p_l3_3.font.size = Pt(9.5)
    p_l3_3.font.color.rgb = TEXT_BODY
    p_l3_3.space_after = Pt(12)
    
    # Highlight Box inside Left Card
    p_l3_4 = tf_l3.add_paragraph()
    p_l3_4.text = "LUMBINI THREAD VALUE:\n✓ Zero Latency Order Release\n✓ 100% Component Traceability\n✓ Automated Confirmation & Goods Issue"
    p_l3_4.font.name = "Inter"
    p_l3_4.font.size = Pt(9)
    p_l3_4.font.bold = True
    p_l3_4.font.color.rgb = PRIMARY_BLUE

    # 5 Process Horizontal/Vertical Flow Cards on the Right
    processes = [
        ("1. Work Order & Production Version", "Synchronization of LOIPRO & Production Versions", 
         "Validating BOM explosion, recipe/routing alignment, and release triggers between ERP/S4 and SAP ME/DMC without batch lag."),
        ("2. Materials Movement & Inventory Control", "Real-Time Staging & Consumption Tracking", 
         "Synchronizing MATMAS master records, line-side replenishment, kanban triggers, and automated Goods Issue (261) movements."),
        ("3. Shop-Floor Controlling & Routing Execution", "Granular Operation Dispatching & POD Control", 
         "Live SFC (Shop Floor Control) progression, work-center routing enforcement, operator validations, and automated cycle-time capture."),
        ("4. Bill of Materials & Production Execution", "Component Consumption & Scrap Accounting", 
         "Multi-level assembly verification, alternate component management, immediate scrap recording, and yield reconciliation."),
        ("5. Traceability, Quality & Logistics Integration", "Serialized Tracking & 3PL Integration", 
         "Full genealogy tracking, in-process non-conformance (NC) recording, and seamless handoff to automated warehousing & 3PL logistics.")
    ]
    
    card_top = 1.4
    card_h = 0.98
    card_gap = 0.12
    for p_i, (p_title, p_sub, p_desc) in enumerate(processes):
        py = card_top + p_i * (card_h + card_gap)
        p_card = create_card(s3, 4.8, py, 7.733, card_h)
        tf_pc = p_card.text_frame
        tf_pc.word_wrap = True
        tf_pc.margin_left = Inches(0.2)
        tf_pc.margin_top = Inches(0.08)
        
        p1 = tf_pc.paragraphs[0]
        p1.text = p_title
        p1.font.name = "Inter"
        p1.font.size = Pt(10.5)
        p1.font.bold = True
        p1.font.color.rgb = DEEP_BLUE
        
        p2 = tf_pc.add_paragraph()
        p2.text = f"{p_sub} — {p_desc}"
        p2.font.name = "Inter"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_BODY

    # =============================================================
    # SLIDE 4: Strategic Approach – Beyond Siloed Support
    # =============================================================
    s4 = add_base_slide()
    add_header(s4, "Strategic Approach – Beyond Siloed Support", 
               "Solving the Business, Architecture & Transformation Problem | Advisory-Led AMS Model")
    add_footer(s4, 4)
    
    # 3 Strategic Dimension Cards
    dimensions = [
        ("1. Cross-System Orchestration", "How do these systems work together?",
         "Traditional AMS vendors treat ERP, MES, and WMS as isolated silos. Lumbini analyzes the macro ecosystem architecture:\n\n"
         "• Real-time queue monitoring across LOIPRO, LOIWCS, and MATMAS interfaces.\n"
         "• Rapid resolution of IDoc bottlenecks, web-service time-outs, and PCo communication drops.\n"
         "• Alignment of plant-floor events with corporate financial and controlling ledgers.",
         TAG_BG_BLUE, PRIMARY_BLUE),
        
        ("2. Operating Model Transformation", "How should the enterprise transform its model?",
         "Support is a catalyst for continuous modernization, not just firefighting. Our senior consultants continuously evaluate:\n\n"
         "• Identifying repetitive incident root causes and automating corrective runbooks.\n"
         "• Refactoring manual plant supervisor overrides into automated standard system workflows.\n"
         "• Accelerating the transitional path from on-premise SAP ME to SAP Digital Manufacturing (DMC).",
         TAG_BG_BLUE, PRIMARY_BLUE),
        
        ("3. Flexible Architecture Execution", "Seamlessly within SAP or outside via Elitia",
         "Enterprise agility demands practical technical pragmatism without bloating core systems:\n\n"
         "• In-SAP Solutions: Standard configurations, BAdIs, and SAP BTP extensions adhering to the Clean Core paradigm.\n"
         "• Outside-SAP Extensions: Leveraging Elitia Technologies' high-performance microservices when custom edge logic or sub-millisecond line speeds are required.\n"
         "• No vendor lock-in with open, API-driven architectures.",
         TAG_BG_ORANGE, AMBER_DARK)
    ]
    
    dim_w = 3.75
    dim_gap = 0.24
    for d_i, (d_title, d_question, d_body, bg_c, title_c) in enumerate(dimensions):
        dx = 0.8 + d_i * (dim_w + dim_gap)
        d_card = create_card(s4, dx, 1.45, dim_w, 4.35)
        
        # Pill top
        d_badge = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(dx + 0.15), Inches(1.6), Inches(dim_w - 0.3), Inches(0.65))
        d_badge.fill.solid()
        d_badge.fill.fore_color.rgb = bg_c
        d_badge.line.fill.background()
        tf_db = d_badge.text_frame
        tf_db.word_wrap = True
        tf_db.margin_left = Inches(0.12)
        tf_db.margin_top = Inches(0.08)
        p_dbt = tf_db.paragraphs[0]
        p_dbt.text = d_title
        p_dbt.font.name = "Inter"
        p_dbt.font.size = Pt(10)
        p_dbt.font.bold = True
        p_dbt.font.color.rgb = title_c
        p_dbq = tf_db.add_paragraph()
        p_dbq.text = d_question
        p_dbq.font.name = "Inter"
        p_dbq.font.size = Pt(8.5)
        p_dbq.font.italic = True
        p_dbq.font.color.rgb = TEXT_DARK
        
        # Content
        d_tx = s4.shapes.add_textbox(Inches(dx + 0.15), Inches(2.35), Inches(dim_w - 0.3), Inches(3.3))
        tf_dt = d_tx.text_frame
        tf_dt.word_wrap = True
        tf_dt.margin_left = tf_dt.margin_top = 0
        p_d1 = tf_dt.paragraphs[0]
        p_d1.text = d_body
        p_d1.font.name = "Inter"
        p_d1.font.size = Pt(8.8)
        p_d1.font.color.rgb = TEXT_BODY

    # Bottom Callout Banner
    bot_c4 = create_card(s4, 0.8, 5.95, 11.733, 0.85, border_color=BORDER_BLUE, bg_color=TAG_BG_BLUE)
    tf_b4 = bot_c4.text_frame
    tf_b4.word_wrap = True
    tf_b4.margin_left = Inches(0.2)
    tf_b4.margin_top = Inches(0.1)
    p_b4_1 = tf_b4.paragraphs[0]
    p_b4_1.text = "THE LUMBINI DIFFERENCE: ADVISORY-LED STABILIZATION"
    p_b4_1.font.name = "Inter"
    p_b4_1.font.size = Pt(9.5)
    p_b4_1.font.bold = True
    p_b4_1.font.color.rgb = PRIMARY_BLUE
    p_b4_2 = tf_b4.add_paragraph()
    p_b4_2.text = "We transform ticket-handling into proactive technical health checks, eliminating recurring defects and providing architectural roadmaps that safeguard high-volume manufacturing throughput."
    p_b4_2.font.name = "Inter"
    p_b4_2.font.size = Pt(8.8)
    p_b4_2.font.color.rgb = TEXT_BODY

    # =============================================================
    # SLIDE 5: Proposed AMS Scope & Delivery Model
    # =============================================================
    s5 = add_base_slide()
    add_header(s5, "Proposed AMS Support Scope & Delivery Model", 
               "L1/L2 Technical & Functional Support | SLA-Driven Governance & Integration Monitoring")
    add_footer(s5, 5)
    
    # 3 Scope Columns
    scopes = [
        ("L1/L2 Incident Triage & Resolution", [
            ("24/5 - 24/7 Coverage Window", "Rapid response for shift handovers and critical production interruptions."),
            ("SFC & Routing Exceptions", "Immediate troubleshooting of blocked SFCs, routing deviations, and POD error messages."),
            ("Order Release & Staging", "Verifying production order statuses, resolving hold flags, and unlocking line execution."),
            ("User Access & POD Privileges", "Managing user provisioning, plant role assignments, and operator profile configurations.")
        ]),
        ("Interface & Integration Monitoring", [
            ("LOIPRO / LOIWCS Interfaces", "Proactive queue monitoring and re-triggering of failed work order transfers."),
            ("MATMAS & BOM Synchronization", "Auditing material master updates, component changes, and production version alignment."),
            ("3PL & Warehouse Integration", "Resolving inventory synchronization drops between shop-floor buffers and warehouse systems."),
            ("PCo / Edge Device Heartbeats", "Diagnostic monitoring of plant connectivity, barcode scanners, and printer integrations.")
        ]),
        ("Continuous Stabilization & Maintenance", [
            ("Root Cause Analysis (RCA)", "Weekly Pareto trend analysis on recurring failure codes to implement permanent systemic fixes."),
            ("Recipe & Version Governance", "Regular audits of production version validity dates and routing task lists."),
            ("SOP & Knowledge Base Updates", "Continuous documentation of plant-floor resolutions in client-accessible runbooks."),
            ("Release & Patch Validation", "Support testing for SAP ME service packs, DMC updates, and cloud connector patches.")
        ])
    ]
    
    sc_w = 3.75
    sc_gap = 0.24
    for s_i, (s_title, items) in enumerate(scopes):
        sx = 0.8 + s_i * (sc_w + sc_gap)
        sc_card = create_card(s5, sx, 1.45, sc_w, 4.35)
        
        # Header Badge
        sc_hdr = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(sx + 0.15), Inches(1.6), Inches(sc_w - 0.3), Inches(0.48))
        sc_hdr.fill.solid()
        sc_hdr.fill.fore_color.rgb = TAG_BG_BLUE
        sc_hdr.line.fill.background()
        tf_sh = sc_hdr.text_frame
        tf_sh.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_sh = tf_sh.paragraphs[0]
        p_sh.text = s_title
        p_sh.font.name = "Inter"
        p_sh.font.size = Pt(9.8)
        p_sh.font.bold = True
        p_sh.font.color.rgb = DEEP_BLUE
        
        # Items
        sc_tx = s5.shapes.add_textbox(Inches(sx + 0.15), Inches(2.2), Inches(sc_w - 0.3), Inches(3.4))
        tf_sc = sc_tx.text_frame
        tf_sc.word_wrap = True
        tf_sc.margin_left = tf_sc.margin_top = 0
        for it_idx, (it_title, it_desc) in enumerate(items):
            p_it = tf_sc.paragraphs[0] if it_idx == 0 else tf_sc.add_paragraph()
            p_it.text = f"• {it_title}"
            p_it.font.name = "Inter"
            p_it.font.size = Pt(9)
            p_it.font.bold = True
            p_it.font.color.rgb = TEXT_DARK
            p_it.space_after = Pt(2)
            
            p_desc_txt = tf_sc.add_paragraph()
            p_desc_txt.text = f"  {it_desc}"
            p_desc_txt.font.name = "Inter"
            p_desc_txt.font.size = Pt(8.2)
            p_desc_txt.font.color.rgb = TEXT_BODY
            p_desc_txt.space_after = Pt(6)

    # SLA Metrics Footer Banner
    sla_c5 = create_card(s5, 0.8, 5.95, 11.733, 0.85, border_color=BORDER_BLUE, bg_color=TAG_BG_BLUE)
    tf_sla = sla_c5.text_frame
    tf_sla.word_wrap = True
    tf_sla.margin_left = Inches(0.2)
    tf_sla.margin_top = Inches(0.1)
    p_sla1 = tf_sla.paragraphs[0]
    p_sla1.text = "OFFSHORE DELIVERY EXCELLENCE | RIGOROUS ENTERPRISE SLAs"
    p_sla1.font.name = "Inter"
    p_sla1.font.size = Pt(9.5)
    p_sla1.font.bold = True
    p_sla1.font.color.rgb = PRIMARY_BLUE
    p_sla2 = tf_sla.add_paragraph()
    p_sla2.text = "• P1 Critical (Plant Down): < 15 Min Response | 2 Hr Workaround   • P2 High (Degraded Line): < 30 Min Response | 4 Hr Target   • P3/P4 Routine: < 2 Hr Response | SLA-Governed"
    p_sla2.font.name = "Inter"
    p_sla2.font.size = Pt(8.8)
    p_sla2.font.color.rgb = TEXT_BODY

    # =============================================================
    # SLIDE 6: Team Profiles & Governance Structure
    # =============================================================
    s6 = add_base_slide()
    add_header(s6, "Team Profiles & Governance Structure", 
               "Offshore Delivery Excellence | India-Based MES Leads with Direct Global Stakeholder Alignment")
    add_footer(s6, 6)
    
    # Left Box: Governance Framework
    gov_card = create_card(s6, 0.8, 1.45, 5.7, 4.35)
    tf_gv = gov_card.text_frame
    tf_gv.word_wrap = True
    tf_gv.margin_left = Inches(0.25)
    tf_gv.margin_top = Inches(0.18)
    
    p_gv0 = tf_gv.paragraphs[0]
    p_gv0.text = "GOVERNANCE & ENGAGEMENT MODEL"
    p_gv0.font.name = "Inter"
    p_gv0.font.size = Pt(10)
    p_gv0.font.bold = True
    p_gv0.font.color.rgb = PRIMARY_BLUE
    p_gv0.space_after = Pt(6)
    
    gv_bullets = [
        ("India Project Delivery Manager (Lead SPOC)", 
         "Acts as the dedicated interface for client IT leadership, managing resource allocation, SLA compliance, escalation resolution, and steering committee cadence."),
        ("Senior MES Functional & Technical Leads", 
         "Experienced practitioners specializing in SAP ME core, DMC cloud extensions, PCo integration, and S/4HANA PP/MM alignment."),
        ("L1/L2 Incident Analysts & Interface Engineers", 
         "Dedicated shift engineers handling real-time ticket triage, queue clearance, user authorizations, and operational execution assistance."),
        ("Global Coordination & Shift Overlap", 
         "Designed with purposeful operating overlap with US and global manufacturing shifts to ensure seamless handovers and live plant support.")
    ]
    for g_title, g_desc in gv_bullets:
        p_gt = tf_gv.add_paragraph()
        p_gt.text = f"• {g_title}"
        p_gt.font.name = "Inter"
        p_gt.font.size = Pt(9.5)
        p_gt.font.bold = True
        p_gt.font.color.rgb = TEXT_DARK
        
        p_gd = tf_gv.add_paragraph()
        p_gd.text = f"  {g_desc}"
        p_gd.font.name = "Inter"
        p_gd.font.size = Pt(8.5)
        p_gd.font.color.rgb = TEXT_BODY
        p_gd.space_after = Pt(6)

    # Right Box: Cadence & Communications
    cad_card = create_card(s6, 6.75, 1.45, 5.78, 4.35)
    tf_cd = cad_card.text_frame
    tf_cd.word_wrap = True
    tf_cd.margin_left = Inches(0.25)
    tf_cd.margin_top = Inches(0.18)
    
    p_cd0 = tf_cd.paragraphs[0]
    p_cd0.text = "COLLABORATIVE GOVERNANCE CADENCE"
    p_cd0.font.name = "Inter"
    p_cd0.font.size = Pt(10)
    p_cd0.font.bold = True
    p_cd0.font.color.rgb = PRIMARY_BLUE
    p_cd0.space_after = Pt(6)
    
    cad_items = [
        ("Daily Standups (15 Mins)", "Review open tickets, shift handover items, critical interface queue backlog, and urgent line priorities."),
        ("Weekly Operations Review", "Ticket Pareto analysis, SLA compliance metrics, recurring defect evaluation, and staffing review."),
        ("Monthly Technical Steering", "Root cause review, preventive recommendations, system upgrade impact, and architecture roadmapping."),
        ("Quarterly Executive Review (QBR)", "Strategic roadmap assessment, capacity optimization, ROI reporting, and digital manufacturing evolution.")
    ]
    for c_title, c_desc in cad_items:
        p_ct = tf_cd.add_paragraph()
        p_ct.text = f"✓ {c_title}"
        p_ct.font.name = "Inter"
        p_ct.font.size = Pt(9.5)
        p_ct.font.bold = True
        p_ct.font.color.rgb = DEEP_BLUE
        
        p_cd = tf_cd.add_paragraph()
        p_cd.text = f"  {c_desc}"
        p_cd.font.name = "Inter"
        p_cd.font.size = Pt(8.5)
        p_cd.font.color.rgb = TEXT_BODY
        p_cd.space_after = Pt(6)

    # Callout Placeholder Note at Bottom
    note_card = create_card(s6, 0.8, 5.95, 11.733, 0.85, border_color=AMBER_DARK, bg_color=TAG_BG_ORANGE)
    tf_nt = note_card.text_frame
    tf_nt.word_wrap = True
    tf_nt.margin_left = Inches(0.25)
    tf_nt.margin_top = Inches(0.14)
    p_nt1 = tf_nt.paragraphs[0]
    p_nt1.text = "RESOURCE PROFILES & QUALIFICATION NOTE"
    p_nt1.font.name = "Inter"
    p_nt1.font.size = Pt(9)
    p_nt1.font.bold = True
    p_nt1.font.color.rgb = AMBER_DARK
    p_nt2 = tf_nt.add_paragraph()
    p_nt2.text = "* Detailed resource profiles and resumes attached in the subsequent slides."
    p_nt2.font.name = "Inter"
    p_nt2.font.size = Pt(10)
    p_nt2.font.italic = True
    p_nt2.font.bold = True
    p_nt2.font.color.rgb = TEXT_DARK

    # =============================================================
    # SLIDE 7: Commercial & Costing Structure
    # =============================================================
    s7 = add_base_slide()
    add_header(s7, "Commercial & Costing Structure (Offshore AMS Model)", 
               "Transparent, Highly Competitive Pricing | Enterprise-Grade MES Support with Predictable Economics")
    add_footer(s7, 7)
    
    # Left Card: Commercial Table
    tbl_card = create_card(s7, 0.8, 1.45, 6.8, 4.35)
    
    # Table inside Left Card
    t_shape = s7.shapes.add_table(5, 2, Inches(1.0), Inches(1.65), Inches(6.4), Inches(2.7))
    tbl = t_shape.table
    tbl.columns[0].width = Inches(2.6)
    tbl.columns[1].width = Inches(3.8)
    
    pricing_data = [
        ("Engagement Model", "100% Offshore Delivery (India Center of Excellence)"),
        ("Support Tier", "L1 Support (SAP ME / SAP DMC / Interface Monitoring)"),
        ("Hourly Billing Rate", "$10.00 to $12.00 USD per hour per resource"),
        ("Standard Time Commitment", "8 Hours / Day — 40 Hours / Week per Resource"),
        ("Estimated Monthly Cost", "~$1,600 to $1,920 USD per Resource / Month (160 Hrs)")
    ]
    
    for row_i, (k, v) in enumerate(pricing_data):
        cell_k = tbl.cell(row_i, 0)
        cell_v = tbl.cell(row_i, 1)
        
        cell_k.text = k
        cell_v.text = v
        
        for cell, is_val in [(cell_k, False), (cell_v, True)]:
            cell.margin_left = Inches(0.12)
            cell.margin_right = Inches(0.12)
            cell.margin_top = Inches(0.08)
            cell.margin_bottom = Inches(0.08)
            cell.fill.solid()
            cell.fill.fore_color.rgb = TAG_BG_BLUE if row_i % 2 == 0 else SURFACE_WHITE
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Inter"
            p.font.size = Pt(9.5)
            p.font.bold = not is_val or row_i == 2
            p.font.color.rgb = PRIMARY_BLUE if (is_val and row_i == 2) else (TEXT_DARK if not is_val else TEXT_BODY)
            
    # Small note under table
    tbl_note = s7.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(6.4), Inches(1.1))
    tf_tn = tbl_note.text_frame
    tf_tn.word_wrap = True
    tf_tn.margin_left = tf_tn.margin_top = 0
    p_tn1 = tf_tn.paragraphs[0]
    p_tn1.text = "Commercial Notes & Terms:"
    p_tn1.font.name = "Inter"
    p_tn1.font.size = Pt(9)
    p_tn1.font.bold = True
    p_tn1.font.color.rgb = TEXT_DARK
    
    p_tn2 = tf_tn.add_paragraph()
    p_tn2.text = "• Invoicing on actual hours delivered with monthly automated timesheet reconciliation.\n• Flexibility to scale resource count up or down with a standard 30-day notice period.\n• Optional L2/L3 senior escalation pool accessible on a blended advisory rate card."
    p_tn2.font.name = "Inter"
    p_tn2.font.size = Pt(8.2)
    p_tn2.font.color.rgb = TEXT_MUTED

    # Right Card: Value Proposition
    vp_card = create_card(s7, 7.85, 1.45, 4.683, 4.35, border_color=BORDER_BLUE, bg_color=TAG_BG_BLUE)
    tf_vp = vp_card.text_frame
    tf_vp.word_wrap = True
    tf_vp.margin_left = Inches(0.25)
    tf_vp.margin_top = Inches(0.2)
    
    p_vp0 = tf_vp.paragraphs[0]
    p_vp0.text = "THE CLIENT VALUE PROPOSITION"
    p_vp0.font.name = "Inter"
    p_vp0.font.size = Pt(10)
    p_vp0.font.bold = True
    p_vp0.font.color.rgb = PRIMARY_BLUE
    p_vp0.space_after = Pt(6)
    
    val_points = [
        ("Maximum Operational Availability", 
         "Continuous shop-floor vigilance prevents costly line stoppages and minimizes unplanned downtime."),
        ("Enterprise-Grade Governance", 
         "Certified SAP Partner governance frameworks aligned with Panasonic's strict quality, compliance, and security standards."),
        ("Senior Functional Oversight", 
         "Every offshore engineer is backed by experienced India Project Delivery Managers and MES solution architects."),
        ("Unmatched Cost Optimization", 
         "Deliver 60-70% operational savings compared to traditional onsite or blended tier-1 vendor support models.")
    ]
    for v_title, v_desc in val_points:
        p_vt = tf_vp.add_paragraph()
        p_vt.text = f"✓ {v_title}"
        p_vt.font.name = "Inter"
        p_vt.font.size = Pt(9.5)
        p_vt.font.bold = True
        p_vt.font.color.rgb = DEEP_BLUE
        
        p_vd = tf_vp.add_paragraph()
        p_vd.text = f"  {v_desc}"
        p_vd.font.name = "Inter"
        p_vd.font.size = Pt(8.5)
        p_vd.font.color.rgb = TEXT_BODY
        p_vd.space_after = Pt(6)

    # Bottom Contact Bar
    bot_c7 = create_card(s7, 0.8, 5.95, 11.733, 0.85, border_color=BORDER_BLUE, bg_color=SURFACE_WHITE)
    tf_b7 = bot_c7.text_frame
    tf_b7.word_wrap = True
    tf_b7.margin_left = Inches(0.25)
    tf_b7.margin_top = Inches(0.12)
    p_b7_1 = tf_b7.paragraphs[0]
    p_b7_1.text = "LUMBINI ELITE SOLUTIONS — YOUR STRATEGIC SAP MANUFACTURING AMS PARTNER"
    p_b7_1.font.name = "Inter"
    p_b7_1.font.size = Pt(9.5)
    p_b7_1.font.bold = True
    p_b7_1.font.color.rgb = PRIMARY_BLUE
    p_b7_2 = tf_b7.add_paragraph()
    p_b7_2.text = "Corporate Office: #7, SJR Eternity, Phase 1, Kodigehalli Road, Hoodi, Bangalore - 560048 | Web: www.lumbinielite.com | Email: info@lumbinielite.com"
    p_b7_2.font.name = "Inter"
    p_b7_2.font.size = Pt(8.5)
    p_b7_2.font.color.rgb = TEXT_BODY

    # Save presentation
    prs.save(output_path)
    print(f"Presentation successfully generated at: {output_path}")

if __name__ == "__main__":
    build_presentation()
