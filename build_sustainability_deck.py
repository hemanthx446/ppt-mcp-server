import os
import copy
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

def build_sustainability_extension():
    deck_path = "Elitia Enterprise Suite for Energy's Next-Gen Infrastructure.pptx"
    prs = Presentation(deck_path)
    
    print(f"Initial slide count: {len(prs.slides)}")
    
    # -------------------------------------------------------------
    # Palette & Design Tokens (Matched to existing deck)
    # -------------------------------------------------------------
    PRIMARY_RED = RGBColor(227, 6, 19)         # #E30613 Brand Red
    DARK_TITLE = RGBColor(20, 30, 45)          # #141E2D Executive Navy/Charcoal
    TEXT_BODY = RGBColor(30, 41, 59)           # #1E293B Deep Slate
    TEXT_MUTED = RGBColor(100, 116, 139)       # #64748B Subtitle/Footer Slate
    BLUE_ACCENT = RGBColor(0, 102, 180)        # #0066B4 Technical Blue
    NAVY_DARK = RGBColor(10, 37, 64)           # #0A2540 Container Header Navy
    
    WHITE = RGBColor(255, 255, 255)
    CARD_BG = RGBColor(255, 255, 255)
    CARD_BG_MUTED = RGBColor(248, 250, 252)    # #F8FAFC Subtle Gray Wash
    CARD_BG_LIGHT_BLUE = RGBColor(240, 246, 252) # #F0F6FC Technical Callout Wash
    CARD_BG_LIGHT_RED = RGBColor(254, 242, 242)  # #FEF2F2 Accent Red Wash
    
    BORDER_GRAY = RGBColor(226, 232, 240)      # #E2E8F0 Soft Card Outline
    BORDER_BLUE = RGBColor(186, 215, 240)      # #BAD7F0
    BORDER_RED = RGBColor(252, 165, 165)       # #FCA5A5
    
    slide4 = prs.slides[3] # Reference slide for layout & decorative elements
    blank_layout = slide4.slide_layout
    
    # Helper to add standard slide template with header and footer
    def create_content_slide(title_text, subtitle_text):
        new_slide = prs.slides.add_slide(blank_layout)
        
        # Copy decorative shapes from slide 4
        # Group 16: top-right blue accent, Rectangle 19: bottom-left blue accent,
        # Rectangle 2: red stripe, Rectangle 13: footer divider,
        # TextBox 14: footer left text
        for sh_name in ['Group 16', 'Rectangle: Rounded Corners 19', 'Rectangle 2', 'Rectangle 13', 'TextBox 14']:
            for sh in slide4.shapes:
                if sh.name == sh_name:
                    new_slide.shapes._spTree.append(copy.deepcopy(sh._element))
                    break
                    
        # Red Stripe at top-left
        # (already cloned via Rectangle 2)
        
        # Title
        tx_box = new_slide.shapes.add_textbox(Inches(1.5), Inches(0.64), Inches(15.64), Inches(0.72))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Segoe UI"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = DARK_TITLE
        
        # Subtitle
        tx_sub = new_slide.shapes.add_textbox(Inches(1.5), Inches(1.42), Inches(16.36), Inches(0.36))
        tf_sub = tx_sub.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle_text
        p_sub.font.name = "Calibri"
        p_sub.font.size = Pt(13)
        p_sub.font.italic = True
        p_sub.font.color.rgb = TEXT_MUTED
        
        # Page Number placeholder (will be set accurately later)
        tx_num = new_slide.shapes.add_textbox(Inches(16.48), Inches(9.84), Inches(1.42), Inches(0.32))
        tf_num = tx_num.text_frame
        tf_num.word_wrap = True
        tf_num.margin_right = 0
        p_num = tf_num.paragraphs[0]
        p_num.font.name = "Calibri"
        p_num.font.size = Pt(9)
        p_num.font.color.rgb = TEXT_MUTED
        p_num.alignment = PP_ALIGN.RIGHT
        
        return new_slide

    # =========================================================================
    # SLIDE 1 (New Slide 5): "From Sustainable Material Innovation to Industrialization"
    # =========================================================================
    slide_s1 = create_content_slide(
        "From Sustainable Material Innovation to Industrialization",
        "Connecting engineering, manufacturing, quality and lifecycle data across the high-voltage product journey"
    )
    
    # Horizontal Digital Thread Indicator Banner (Top of lifecycle flow)
    thread_banner = slide_s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.21), Inches(1.95), Inches(16.69), Inches(0.40))
    thread_banner.fill.solid()
    thread_banner.fill.fore_color.rgb = NAVY_DARK
    thread_banner.line.color.rgb = BLUE_ACCENT
    thread_banner.line.width = Pt(1)
    
    tf_tb = thread_banner.text_frame
    tf_tb.word_wrap = True
    tf_tb.margin_left = Inches(0.2)
    tf_tb.margin_top = Inches(0.08)
    p_tb = tf_tb.paragraphs[0]
    p_tb.text = "HIGH-VOLTAGE SUSTAINABILITY DIGITAL THREAD  |  UNIFIED END-TO-END DATA CONTINUITY"
    p_tb.font.name = "Arial"
    p_tb.font.size = Pt(11)
    p_tb.font.bold = True
    p_tb.font.color.rgb = WHITE
    p_tb.alignment = PP_ALIGN.CENTER
    
    # 7 Lifecycle Stages
    stages = [
        {
            "num": "01",
            "title": "MATERIAL / DESIGN",
            "points": [
                "Alternative material evaluation",
                "Material properties & sustainability attributes",
                "AI-assisted discovery & decision support"
            ]
        },
        {
            "num": "02",
            "title": "ENGINEERING",
            "points": [
                "CAD / BOM integration",
                "Engineering Change Management",
                "Product configuration & release control"
            ]
        },
        {
            "num": "03",
            "title": "SUPPLIER",
            "points": [
                "Material traceability",
                "Supplier qualification",
                "Sustainability attributes"
            ]
        },
        {
            "num": "04",
            "title": "MANUFACTURING",
            "points": [
                "Elitia MES",
                "Process monitoring",
                "Digital work instructions & traceability"
            ]
        },
        {
            "num": "05",
            "title": "QUALITY & TEST",
            "points": [
                "Quality gates",
                "Vision AI",
                "Test-result correlation"
            ]
        },
        {
            "num": "06",
            "title": "FIELD PERFORMANCE",
            "points": [
                "SCADA / IoT",
                "Asset monitoring",
                "Predictive APM / RUL"
            ]
        },
        {
            "num": "07",
            "title": "LIFECYCLE",
            "points": [
                "Maintenance intelligence",
                "Reuse / refurbishment data",
                "End-of-life / lifecycle analytics"
            ]
        }
    ]
    
    card_width = 2.24
    gap = 0.17
    start_left = 1.21
    card_top = 2.50
    card_height = 4.85
    
    for i, st in enumerate(stages):
        cur_left = start_left + i * (card_width + gap)
        
        # Outer Card Container
        card = slide_s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cur_left), Inches(card_top), Inches(card_width), Inches(card_height))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_GRAY
        card.line.width = Pt(1)
        
        # Card Header Tab
        header_tab = slide_s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cur_left), Inches(card_top), Inches(card_width), Inches(0.82))
        header_tab.fill.solid()
        header_tab.fill.fore_color.rgb = NAVY_DARK if i % 2 == 0 else BLUE_ACCENT
        header_tab.line.fill.background()
        
        tf_ht = header_tab.text_frame
        tf_ht.word_wrap = True
        tf_ht.margin_left = Inches(0.1)
        tf_ht.margin_top = Inches(0.1)
        tf_ht.margin_right = Inches(0.1)
        
        p_st_num = tf_ht.paragraphs[0]
        p_st_num.text = f"STAGE {st['num']}"
        p_st_num.font.name = "Arial"
        p_st_num.font.size = Pt(8.5)
        p_st_num.font.bold = True
        p_st_num.font.color.rgb = RGBColor(200, 225, 255)
        p_st_num.alignment = PP_ALIGN.CENTER
        
        p_st_title = tf_ht.add_paragraph()
        p_st_title.text = st['title']
        p_st_title.font.name = "Arial"
        p_st_title.font.size = Pt(9.5)
        p_st_title.font.bold = True
        p_st_title.font.color.rgb = WHITE
        p_st_title.alignment = PP_ALIGN.CENTER
        
        # Text box for bullet capabilities
        tx_box = slide_s1.shapes.add_textbox(Inches(cur_left + 0.12), Inches(card_top + 0.95), Inches(card_width - 0.24), Inches(card_height - 1.05))
        tf_card = tx_box.text_frame
        tf_card.word_wrap = True
        tf_card.margin_left = tf_card.margin_top = tf_card.margin_right = tf_card.margin_bottom = 0
        
        for p_idx, pt in enumerate(st['points']):
            p_b = tf_card.paragraphs[0] if p_idx == 0 else tf_card.add_paragraph()
            p_b.text = "•  " + pt
            p_b.font.name = "Calibri"
            p_b.font.size = Pt(10.0)
            p_b.font.color.rgb = TEXT_BODY
            p_b.space_after = Pt(8)
            
        # Subtle Chevron / Arrow indicator between cards (for stages 0-5)
        if i < 6:
            arrow = slide_s1.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(cur_left + card_width + 0.03), Inches(card_top + 0.30), Inches(0.11), Inches(0.20))
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = PRIMARY_RED
            arrow.line.fill.background()

    # Bottom Full-Width Highlight Statement Card
    stmt_top = 7.55
    stmt_height = 1.95
    stmt_card = slide_s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.21), Inches(stmt_top), Inches(16.69), Inches(stmt_height))
    stmt_card.fill.solid()
    stmt_card.fill.fore_color.rgb = CARD_BG_LIGHT_BLUE
    stmt_card.line.color.rgb = BORDER_BLUE
    stmt_card.line.width = Pt(1)
    
    # Left Red Accent Stripe on Statement Card
    stmt_stripe = slide_s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.21), Inches(stmt_top), Inches(0.12), Inches(stmt_height))
    stmt_stripe.fill.solid()
    stmt_stripe.fill.fore_color.rgb = PRIMARY_RED
    stmt_stripe.line.fill.background()
    
    # Statement Card Content
    tx_stmt = slide_s1.shapes.add_textbox(Inches(1.50), Inches(stmt_top + 0.18), Inches(16.15), Inches(stmt_height - 0.36))
    tf_stmt = tx_stmt.text_frame
    tf_stmt.word_wrap = True
    tf_stmt.margin_left = tf_stmt.margin_top = tf_stmt.margin_right = tf_stmt.margin_bottom = 0
    
    p_s1 = tf_stmt.paragraphs[0]
    p_s1.text = "THE INDUSTRIAL SUSTAINABILITY DIGITAL THREAD"
    p_s1.font.name = "Arial"
    p_s1.font.size = Pt(10.5)
    p_s1.font.bold = True
    p_s1.font.color.rgb = BLUE_ACCENT
    p_s1.space_after = Pt(4)
    
    p_s2 = tf_stmt.add_paragraph()
    p_s2.text = "“Elitia provides the digital thread that connects sustainable product decisions with engineering validation, manufacturing execution and lifecycle performance.”"
    p_s2.font.name = "Segoe UI"
    p_s2.font.size = Pt(13.5)
    p_s2.font.bold = True
    p_s2.font.color.rgb = DARK_TITLE
    p_s2.space_after = Pt(8)
    
    p_s3 = tf_stmt.add_paragraph()
    p_s3.text = "High-Voltage Rigor: Designed specifically to validate alternative dielectric fluids, sustainable insulation materials, and circular metallurgy without compromising electrical insulation, thermal limits, pressure boundaries, or 30–40 year utility lifespan."
    p_s3.font.name = "Calibri"
    p_s3.font.size = Pt(11.0)
    p_s3.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 2 (New Slide 6): "AI-Enabled Material, Engineering & Manufacturing Intelligence"
    # =========================================================================
    slide_s2 = create_content_slide(
        "AI-Enabled Material, Engineering & Manufacturing Intelligence",
        "Turning engineering and operational data into evidence-based sustainability decisions"
    )
    
    col_top = 2.05
    col_height = 5.65
    
    # LEFT COLUMN: 5 Connected Data Domains
    left_w = 4.85
    card_left = 1.21
    
    left_header = slide_s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(card_left), Inches(col_top), Inches(left_w), Inches(0.42))
    left_header.fill.solid()
    left_header.fill.fore_color.rgb = NAVY_DARK
    left_header.line.fill.background()
    p_lh = left_header.text_frame.paragraphs[0]
    p_lh.text = "CONNECTED DATA DOMAINS (INPUTS)"
    p_lh.font.name = "Arial"
    p_lh.font.size = Pt(10.5)
    p_lh.font.bold = True
    p_lh.font.color.rgb = WHITE
    p_lh.alignment = PP_ALIGN.CENTER
    
    domains = [
        ("1. ENGINEERING DATA", "CAD | BOM | Specifications | ECO", "Captures native 3D geometry, component hierarchies, tolerance limits, and approved design revisions."),
        ("2. MATERIAL DATA", "Material Properties | Compliance | Environmental Attributes", "Standardizes dielectric ratings, conductivity, flammability classes, RoHS/REACH compliance & embodied CO2."),
        ("3. SUPPLIER DATA", "Supplier Qualification | Source | Sustainability Data", "Tracks supplier ESG scoring, Tier-1/2 provenance, transport footprint, and batch material certificates."),
        ("4. MANUFACTURING DATA", "MES | Process Parameters | Quality | Traceability", "Streams real-time curing temperatures, winding tension, resin impregnation metrics & serial genealogy."),
        ("5. FIELD / ASSET DATA", "SCADA | Sensors | APM | Maintenance | Failure History", "Collects transformer acoustic/thermal logs, DGA oil telemetry, breaker cycles & partial discharge data.")
    ]
    
    d_card_h = 0.96
    d_gap = 0.09
    d_start_top = col_top + 0.48
    
    for d_idx, (d_title, d_tags, d_desc) in enumerate(domains):
        cur_d_top = d_start_top + d_idx * (d_card_h + d_gap)
        d_card = slide_s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(card_left), Inches(cur_d_top), Inches(left_w), Inches(d_card_h))
        d_card.fill.solid()
        d_card.fill.fore_color.rgb = CARD_BG
        d_card.line.color.rgb = BORDER_GRAY
        d_card.line.width = Pt(1)
        
        tx_d = slide_s2.shapes.add_textbox(Inches(card_left + 0.15), Inches(cur_d_top + 0.08), Inches(left_w - 0.30), Inches(d_card_h - 0.16))
        tf_d = tx_d.text_frame
        tf_d.word_wrap = True
        tf_d.margin_left = tf_d.margin_top = tf_d.margin_right = tf_d.margin_bottom = 0
        
        p1 = tf_d.paragraphs[0]
        p1.text = d_title
        p1.font.name = "Arial"
        p1.font.size = Pt(10.5)
        p1.font.bold = True
        p1.font.color.rgb = PRIMARY_RED
        
        p2 = tf_d.add_paragraph()
        p2.text = d_tags
        p2.font.name = "Calibri"
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = BLUE_ACCENT
        p2.space_after = Pt(2)
        
        p3 = tf_d.add_paragraph()
        p3.text = d_desc
        p3.font.name = "Calibri"
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = TEXT_MUTED

    # MIDDLE COLUMN: Central Elitia Intelligence Layer
    mid_left = 6.30
    mid_w = 6.45
    
    mid_container = slide_s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(mid_left), Inches(col_top), Inches(mid_w), Inches(col_height))
    mid_container.fill.solid()
    mid_container.fill.fore_color.rgb = CARD_BG_LIGHT_BLUE
    mid_container.line.color.rgb = BORDER_BLUE
    mid_container.line.width = Pt(1.5)
    
    mid_header = slide_s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(mid_left), Inches(col_top), Inches(mid_w), Inches(0.42))
    mid_header.fill.solid()
    mid_header.fill.fore_color.rgb = NAVY_DARK
    mid_header.line.fill.background()
    p_mh = mid_header.text_frame.paragraphs[0]
    p_mh.text = "CENTRAL INTELLIGENCE & ORCHESTRATION ENGINE"
    p_mh.font.name = "Arial"
    p_mh.font.size = Pt(10.5)
    p_mh.font.bold = True
    p_mh.font.color.rgb = WHITE
    p_mh.alignment = PP_ALIGN.CENTER
    
    # Core Intelligence Title & Explanatory text inside Middle Container
    tx_mid = slide_s2.shapes.add_textbox(Inches(mid_left + 0.25), Inches(col_top + 0.55), Inches(mid_w - 0.50), Inches(col_height - 0.70))
    tf_mid = tx_mid.text_frame
    tf_mid.word_wrap = True
    tf_mid.margin_left = tf_mid.margin_top = tf_mid.margin_right = tf_mid.margin_bottom = 0
    
    p_mt1 = tf_mid.paragraphs[0]
    p_mt1.text = "Elitia Intelligence Layer"
    p_mt1.font.name = "Arial"
    p_mt1.font.size = Pt(18)
    p_mt1.font.bold = True
    p_mt1.font.color.rgb = DARK_TITLE
    p_mt1.space_after = Pt(2)
    
    p_mt2 = tf_mid.add_paragraph()
    p_mt2.text = "AI-assisted material discovery and qualification orchestration"
    p_mt2.font.name = "Arial"
    p_mt2.font.size = Pt(12)
    p_mt2.font.bold = True
    p_mt2.font.color.rgb = PRIMARY_RED
    p_mt2.space_after = Pt(8)
    
    # Explanatory quote box
    p_mt3 = tf_mid.add_paragraph()
    p_mt3.text = "“Elitia can provide the data, integration and analytics layer connecting material databases, engineering systems, test results and manufacturing evidence to support sustainable product innovation.”"
    p_mt3.font.name = "Calibri"
    p_mt3.font.size = Pt(11)
    p_mt3.font.italic = True
    p_mt3.font.color.rgb = DARK_TITLE
    p_mt3.space_after = Pt(14)
    
    # Architecture highlights
    p_arch_title = tf_mid.add_paragraph()
    p_arch_title.text = "CORE ARCHITECTURAL CAPABILITIES:"
    p_arch_title.font.name = "Arial"
    p_arch_title.font.size = Pt(10.5)
    p_arch_title.font.bold = True
    p_arch_title.font.color.rgb = BLUE_ACCENT
    p_arch_title.space_after = Pt(4)
    
    arch_bullets = [
        "Multi-Domain Semantic Fusion: Ingests CAD, BOM, MES, test benches, and sensor feeds into a unified graph schema.",
        "Physics & Constraints Validation: Cross-verifies candidate materials against dielectric margins, thermal boundaries & mechanical stress.",
        "Qualification Workflow Orchestration: Automates the progression of new formulations from virtual simulation to shop-floor pilot.",
        "Continuous Feedback Reconciliation: Closes the loop between post-qualification field performance and upstream design models."
    ]
    for ab in arch_bullets:
        p_ab = tf_mid.add_paragraph()
        p_ab.text = "•  " + ab
        p_ab.font.name = "Calibri"
        p_ab.font.size = Pt(10)
        p_ab.font.color.rgb = TEXT_BODY
        p_ab.space_after = Pt(6)

    # RIGHT COLUMN: 7 AI/Analytics Use Cases
    right_left = 13.05
    right_w = 4.85
    
    right_header = slide_s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(right_left), Inches(col_top), Inches(right_w), Inches(0.42))
    right_header.fill.solid()
    right_header.fill.fore_color.rgb = NAVY_DARK
    right_header.line.fill.background()
    p_rh = right_header.text_frame.paragraphs[0]
    p_rh.text = "AI & ANALYTICS USE CASES (OUTCOMES)"
    p_rh.font.name = "Arial"
    p_rh.font.size = Pt(10.5)
    p_rh.font.bold = True
    p_rh.font.color.rgb = WHITE
    p_rh.alignment = PP_ALIGN.CENTER
    
    use_cases = [
        ("Alternative Material Decision Support", "Ranks sustainable substitutes based on electrical, thermal & cost KPIs."),
        ("Process Optimization", "Calibrates curing and winding parameters for lower energy and cycle time."),
        ("Defect Prediction", "Anticipates micro-voids and insulation cracks using inline machine telemetry."),
        ("Quality Correlation", "Correlates batch test results directly with raw material supplier properties."),
        ("Asset Performance Prediction", "Models Remaining Useful Life (RUL) under actual grid harmonic loads."),
        ("Sustainability KPI Analytics", "Tracks real-time Scope 1-3 carbon, scrap rates & circularity index."),
        ("Lifecycle Decision Support", "Identifies components suitable for second-life reuse vs. refurbishment.")
    ]
    
    u_card_h = 0.66
    u_gap = 0.08
    u_start_top = col_top + 0.48
    
    for u_idx, (u_title, u_desc) in enumerate(use_cases):
        cur_u_top = u_start_top + u_idx * (u_card_h + u_gap)
        u_card = slide_s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(right_left), Inches(cur_u_top), Inches(right_w), Inches(u_card_h))
        u_card.fill.solid()
        u_card.fill.fore_color.rgb = CARD_BG
        u_card.line.color.rgb = BORDER_GRAY
        u_card.line.width = Pt(1)
        
        tx_u = slide_s2.shapes.add_textbox(Inches(right_left + 0.15), Inches(cur_u_top + 0.05), Inches(right_w - 0.30), Inches(u_card_h - 0.10))
        tf_u = tx_u.text_frame
        tf_u.word_wrap = True
        tf_u.margin_left = tf_u.margin_top = tf_u.margin_right = tf_u.margin_bottom = 0
        
        p1 = tf_u.paragraphs[0]
        p1.text = u_title
        p1.font.name = "Arial"
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = PRIMARY_RED
        
        p2 = tf_u.add_paragraph()
        p2.text = u_desc
        p2.font.name = "Calibri"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_BODY

    # Flow arrows from Left to Middle and Middle to Right
    arr_l2m = slide_s2.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(6.08), Inches(4.70), Inches(0.18), Inches(0.35))
    arr_l2m.fill.solid()
    arr_l2m.fill.fore_color.rgb = BLUE_ACCENT
    arr_l2m.line.fill.background()
    
    arr_m2r = slide_s2.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(12.78), Inches(4.70), Inches(0.18), Inches(0.35))
    arr_m2r.fill.solid()
    arr_m2r.fill.fore_color.rgb = BLUE_ACCENT
    arr_m2r.line.fill.background()

    # BOTTOM KPI STRIP: Sustainability & Technical Metrics
    kpi_top = 7.85
    kpi_height = 1.65
    
    # Left KPI Box: Sustainability Metrics
    kpi_s_box = slide_s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.21), Inches(kpi_top), Inches(8.15), Inches(kpi_height))
    kpi_s_box.fill.solid()
    kpi_s_box.fill.fore_color.rgb = CARD_BG_LIGHT_BLUE
    kpi_s_box.line.color.rgb = BORDER_BLUE
    kpi_s_box.line.width = Pt(1)
    
    tx_ks = slide_s2.shapes.add_textbox(Inches(1.40), Inches(kpi_top + 0.12), Inches(7.75), Inches(kpi_height - 0.24))
    tf_ks = tx_ks.text_frame
    tf_ks.word_wrap = True
    tf_ks.margin_left = tf_ks.margin_top = tf_ks.margin_right = tf_ks.margin_bottom = 0
    
    p_ks_title = tf_ks.paragraphs[0]
    p_ks_title.text = "SUSTAINABILITY KPI TARGETS"
    p_ks_title.font.name = "Arial"
    p_ks_title.font.size = Pt(11)
    p_ks_title.font.bold = True
    p_ks_title.font.color.rgb = BLUE_ACCENT
    p_ks_title.space_after = Pt(4)
    
    s_kpis = [
        "Material Footprint: Quantified reduction in embodied carbon, virgin resins & scarce alloys.",
        "Energy / Process Efficiency: Reduced curing oven cycle times & shop-floor heating kilowatt-hours.",
        "Scrap & Yield Optimization: Early visual AI gating securing near-zero high-value winding scrap.",
        "Reuse & Circularity Potential: Standardized product passports ready for second-life redeployment."
    ]
    for sk in s_kpis:
        p_sk = tf_ks.add_paragraph()
        p_sk.text = "•  " + sk
        p_sk.font.name = "Calibri"
        p_sk.font.size = Pt(9.5)
        p_sk.font.color.rgb = TEXT_BODY
        p_sk.space_after = Pt(2)

    # Right KPI Box: Technical Performance Metrics
    kpi_t_box = slide_s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.75), Inches(kpi_top), Inches(8.15), Inches(kpi_height))
    kpi_t_box.fill.solid()
    kpi_t_box.fill.fore_color.rgb = CARD_BG_LIGHT_RED
    kpi_t_box.line.color.rgb = BORDER_RED
    kpi_t_box.line.width = Pt(1)
    
    tx_kt = slide_s2.shapes.add_textbox(Inches(9.95), Inches(kpi_top + 0.12), Inches(7.75), Inches(kpi_height - 0.24))
    tf_kt = tx_kt.text_frame
    tf_kt.word_wrap = True
    tf_kt.margin_left = tf_kt.margin_top = tf_kt.margin_right = tf_kt.margin_bottom = 0
    
    p_kt_title = tf_kt.paragraphs[0]
    p_kt_title.text = "TECHNICAL VALIDATION RIGOR"
    p_kt_title.font.name = "Arial"
    p_kt_title.font.size = Pt(11)
    p_kt_title.font.bold = True
    p_kt_title.font.color.rgb = PRIMARY_RED
    p_kt_title.space_after = Pt(4)
    
    t_kpis = [
        "Electrical Performance: Dielectric breakdown strength, insulation resistance & partial discharge limits.",
        "Thermal Endurance: Continuous heat dissipation ratings, glass transition temp & hot-spot limits.",
        "Pressure & Mechanical Integrity: High burst-pressure safety factors, tensile strength & vibration limits.",
        "Product Lifetime: Accelerated aging models validating 30–40 year utility service life and low flammability."
    ]
    for tk in t_kpis:
        p_tk = tf_kt.add_paragraph()
        p_tk.text = "•  " + tk
        p_tk.font.name = "Calibri"
        p_tk.font.size = Pt(9.5)
        p_tk.font.color.rgb = TEXT_BODY
        p_tk.space_after = Pt(2)

    # =========================================================================
    # SLIDE 3 (New Slide 7): "Co-Innovation Pathway for Sustainable High-Voltage Solutions"
    # =========================================================================
    slide_s3 = create_content_slide(
        "Co-Innovation Pathway for Sustainable High-Voltage Solutions",
        "From challenge identification to validated industrial deployment"
    )
    
    # 6-Step Maturity / Pilot Journey (Horizontal Top Section)
    steps = [
        ("01", "IDENTIFY", "Select a high-impact material, process or lifecycle sustainability opportunity."),
        ("02", "CONNECT", "Integrate engineering, material, supplier, manufacturing and asset data."),
        ("03", "MODEL", "Apply analytics / AI to evaluate alternatives and identify candidate solutions."),
        ("04", "VALIDATE", "Connect simulations, laboratory/test results and manufacturing quality evidence."),
        ("05", "PILOT", "Run a controlled manufacturing or customer test-case with traceability and measurable KPIs."),
        ("06", "INDUSTRIALIZE", "Integrate with PLM, MES, ERP and enterprise architecture and scale across product families/sites.")
    ]
    
    st_w = 2.64
    st_gap = 0.17
    st_left_start = 1.21
    st_top = 2.05
    st_h = 2.45
    
    for idx, (num, title, desc) in enumerate(steps):
        cur_left = st_left_start + idx * (st_w + st_gap)
        
        # Step Container Card
        s_card = slide_s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cur_left), Inches(st_top), Inches(st_w), Inches(st_h))
        s_card.fill.solid()
        s_card.fill.fore_color.rgb = CARD_BG
        s_card.line.color.rgb = BORDER_GRAY
        s_card.line.width = Pt(1)
        
        # Step Number Badge
        badge = slide_s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cur_left + 0.15), Inches(st_top + 0.15), Inches(st_w - 0.30), Inches(0.40))
        badge.fill.solid()
        badge.fill.fore_color.rgb = NAVY_DARK if idx < 3 else BLUE_ACCENT
        badge.line.fill.background()
        
        p_b = badge.text_frame.paragraphs[0]
        p_b.text = f"{num} — {title}"
        p_b.font.name = "Arial"
        p_b.font.size = Pt(10.5)
        p_b.font.bold = True
        p_b.font.color.rgb = WHITE
        p_b.alignment = PP_ALIGN.CENTER
        
        # Step Description
        tx_sd = slide_s3.shapes.add_textbox(Inches(cur_left + 0.15), Inches(st_top + 0.65), Inches(st_w - 0.30), Inches(st_h - 0.75))
        tf_sd = tx_sd.text_frame
        tf_sd.word_wrap = True
        tf_sd.margin_left = tf_sd.margin_top = tf_sd.margin_right = tf_sd.margin_bottom = 0
        
        p_desc = tf_sd.paragraphs[0]
        p_desc.text = desc
        p_desc.font.name = "Calibri"
        p_desc.font.size = Pt(10.5)
        p_desc.font.color.rgb = TEXT_BODY
        
        # Chevron Arrow to next step
        if idx < 5:
            c_arrow = slide_s3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(cur_left + st_w + 0.03), Inches(st_top + 0.25), Inches(0.11), Inches(0.20))
            c_arrow.fill.solid()
            c_arrow.fill.fore_color.rgb = PRIMARY_RED
            c_arrow.line.fill.background()

    # Middle Section: 3 Collaboration Models (Left) + Potential Pilot Areas (Right)
    mid_sec_top = 4.75
    mid_sec_h = 3.25
    
    # Left: Three Collaboration Models
    collab_left = 1.21
    collab_total_w = 10.60
    
    collab_container = slide_s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(collab_left), Inches(mid_sec_top), Inches(collab_total_w), Inches(mid_sec_h))
    collab_container.fill.solid()
    collab_container.fill.fore_color.rgb = CARD_BG_LIGHT_BLUE
    collab_container.line.color.rgb = BORDER_BLUE
    collab_container.line.width = Pt(1)
    
    collab_header = slide_s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(collab_left), Inches(mid_sec_top), Inches(collab_total_w), Inches(0.40))
    collab_header.fill.solid()
    collab_header.fill.fore_color.rgb = NAVY_DARK
    collab_header.line.fill.background()
    p_ch = collab_header.text_frame.paragraphs[0]
    p_ch.text = "FLEXIBLE CO-INNOVATION ENGAGEMENT MODELS (CONSISTENT WITH LUMBINI SUITE)"
    p_ch.font.name = "Arial"
    p_ch.font.size = Pt(10.5)
    p_ch.font.bold = True
    p_ch.font.color.rgb = WHITE
    p_ch.alignment = PP_ALIGN.CENTER
    
    models = [
        ("PRODUCT / PLATFORM", "Elitia Modular Software Capabilities", [
            "Modular licensing of proprietary Elitia MES, APM, DGS & BI engines.",
            "Pre-configured REST/MQTT APIs for seamless SAP ERP & Siemens PLM sync.",
            "Rapid deployment of digital thread and traceability templates."
        ]),
        ("CO-DEVELOPMENT", "Joint Engineering & Solution Development", [
            "Dedicated engineering squads co-authoring specialized test connectors.",
            "Shared IP & codebase ownership for custom high-voltage analytical algorithms.",
            "Agile co-innovation cycles aligned directly with local & global R&D sprints."
        ]),
        ("EXPERT AUGMENTATION", "Utility, Manufacturing & Data Specialists", [
            "On-demand squads of power electronics, utility and material data experts.",
            "Rapid scale-up within 2-4 weeks to accelerate validation milestones.",
            "Embedded specialists bridging laboratory testing with shop-floor operations."
        ])
    ]
    
    m_w = 3.25
    m_gap = 0.20
    m_start_l = collab_left + 0.20
    m_top = mid_sec_top + 0.55
    m_h = mid_sec_h - 0.70
    
    for m_idx, (m_title, m_sub, m_bullets) in enumerate(models):
        cur_m_l = m_start_l + m_idx * (m_w + m_gap)
        m_box = slide_s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cur_m_l), Inches(m_top), Inches(m_w), Inches(m_h))
        m_box.fill.solid()
        m_box.fill.fore_color.rgb = CARD_BG
        m_box.line.color.rgb = BORDER_GRAY
        m_box.line.width = Pt(1)
        
        tx_m = slide_s3.shapes.add_textbox(Inches(cur_m_l + 0.15), Inches(m_top + 0.12), Inches(m_w - 0.30), Inches(m_h - 0.24))
        tf_m = tx_m.text_frame
        tf_m.word_wrap = True
        tf_m.margin_left = tf_m.margin_top = tf_m.margin_right = tf_m.margin_bottom = 0
        
        p1 = tf_m.paragraphs[0]
        p1.text = m_title
        p1.font.name = "Arial"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = PRIMARY_RED
        
        p2 = tf_m.add_paragraph()
        p2.text = m_sub
        p2.font.name = "Calibri"
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = BLUE_ACCENT
        p2.space_after = Pt(6)
        
        for mb in m_bullets:
            p_mb = tf_m.add_paragraph()
            p_mb.text = "•  " + mb
            p_mb.font.name = "Calibri"
            p_mb.font.size = Pt(9)
            p_mb.font.color.rgb = TEXT_BODY
            p_mb.space_after = Pt(3)

    # Right: Potential Pilot Areas Box
    pilot_left = 12.10
    pilot_w = 5.80
    
    pilot_container = slide_s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(pilot_left), Inches(mid_sec_top), Inches(pilot_w), Inches(mid_sec_h))
    pilot_container.fill.solid()
    pilot_container.fill.fore_color.rgb = CARD_BG_LIGHT_RED
    pilot_container.line.color.rgb = BORDER_RED
    pilot_container.line.width = Pt(1)
    
    pilot_header = slide_s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(pilot_left), Inches(mid_sec_top), Inches(pilot_w), Inches(0.40))
    pilot_header.fill.solid()
    pilot_header.fill.fore_color.rgb = PRIMARY_RED
    pilot_header.line.fill.background()
    p_ph = pilot_header.text_frame.paragraphs[0]
    p_ph.text = "POTENTIAL CO-INNOVATION & PILOT FOCUS AREAS"
    p_ph.font.name = "Arial"
    p_ph.font.size = Pt(10.5)
    p_ph.font.bold = True
    p_ph.font.color.rgb = WHITE
    p_ph.alignment = PP_ALIGN.CENTER
    
    tx_pilot = slide_s3.shapes.add_textbox(Inches(pilot_left + 0.20), Inches(mid_sec_top + 0.50), Inches(pilot_w - 0.40), Inches(mid_sec_h - 0.60))
    tf_pilot = tx_pilot.text_frame
    tf_pilot.word_wrap = True
    tf_pilot.margin_left = tf_pilot.margin_top = tf_pilot.margin_right = tf_pilot.margin_bottom = 0
    
    p_pi = tf_pilot.paragraphs[0]
    p_pi.text = "Candidate domains for joint proof-of-value validation:"
    p_pi.font.name = "Calibri"
    p_pi.font.size = Pt(10)
    p_pi.font.italic = True
    p_pi.font.color.rgb = TEXT_MUTED
    p_pi.space_after = Pt(4)
    
    pilots = [
        "High-voltage cooling systems (alternative fluids, coatings & thermal simulations)",
        "Sustainable material alternatives (bio-based resins, low-carbon conductors)",
        "Manufacturing process optimization (curing oven energy, winding tension yield)",
        "Product traceability (cradle-to-grave digital component passports)",
        "Engineering-to-shop-floor digital thread (automated CAD/BOM-to-MES routing)",
        "Lifecycle / reuse intelligence (refurbishment assessment & second-life grading)"
    ]
    for pl in pilots:
        p_pl = tf_pilot.add_paragraph()
        p_pl.text = "✔  " + pl
        p_pl.font.name = "Calibri"
        p_pl.font.size = Pt(9.5)
        p_pl.font.color.rgb = DARK_TITLE
        p_pl.space_after = Pt(3)

    # Bottom Highlighted Objective Box
    obj_top = 8.20
    obj_h = 1.30
    obj_card = slide_s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.21), Inches(obj_top), Inches(16.69), Inches(obj_h))
    obj_card.fill.solid()
    obj_card.fill.fore_color.rgb = CARD_BG
    obj_card.line.color.rgb = PRIMARY_RED
    obj_card.line.width = Pt(1.5)
    
    obj_stripe = slide_s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.21), Inches(obj_top), Inches(0.12), Inches(obj_h))
    obj_stripe.fill.solid()
    obj_stripe.fill.fore_color.rgb = PRIMARY_RED
    obj_stripe.line.fill.background()
    
    tx_obj = slide_s3.shapes.add_textbox(Inches(1.50), Inches(obj_top + 0.12), Inches(16.15), Inches(obj_h - 0.24))
    tf_obj = tx_obj.text_frame
    tf_obj.word_wrap = True
    tf_obj.margin_left = tf_obj.margin_top = tf_obj.margin_right = tf_obj.margin_bottom = 0
    
    p_o1 = tf_obj.paragraphs[0]
    p_o1.text = "CORE CO-INNOVATION OBJECTIVE"
    p_o1.font.name = "Arial"
    p_o1.font.size = Pt(10)
    p_o1.font.bold = True
    p_o1.font.color.rgb = PRIMARY_RED
    p_o1.space_after = Pt(2)
    
    p_o2 = tf_obj.add_paragraph()
    p_o2.text = "“Objective: reduce the time and uncertainty between a sustainable product idea and a technically validated, manufacturable and scalable solution.”"
    p_o2.font.name = "Segoe UI"
    p_o2.font.size = Pt(13)
    p_o2.font.bold = True
    p_o2.font.color.rgb = DARK_TITLE
    p_o2.space_after = Pt(2)
    
    p_o3 = tf_obj.add_paragraph()
    p_o3.text = "De-risking industrial scale-up: Combining digital simulation, shop-floor sensor telemetry, and automated quality gating to achieve first-time-right manufacturing without impacting production line commitments."
    p_o3.font.name = "Calibri"
    p_o3.font.size = Pt(10.5)
    p_o3.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # REORDER SLIDES IN PRESENTATION
    # =========================================================================
    # Currently, new slides are appended at indices 13, 14, 15 (0-indexed).
    # We want them at positions 5, 6, 7 (which correspond to 0-indices 4, 5, 6).
    # In prs.slides._sldIdLst, we move the last 3 slides to indices 4, 5, 6.
    sldIdLst = prs.slides._sldIdLst
    
    slide_s3_id = sldIdLst[len(sldIdLst) - 1]
    slide_s2_id = sldIdLst[len(sldIdLst) - 2]
    slide_s1_id = sldIdLst[len(sldIdLst) - 3]
    
    # Remove from end
    sldIdLst.remove(slide_s1_id)
    sldIdLst.remove(slide_s2_id)
    sldIdLst.remove(slide_s3_id)
    
    # Insert right after slide 4 (which is at index 3)
    sldIdLst.insert(4, slide_s1_id)
    sldIdLst.insert(5, slide_s2_id)
    sldIdLst.insert(6, slide_s3_id)
    
    print(f"Total slides after insertion: {len(prs.slides)}")

    # =========================================================================
    # ENHANCE SLIDE 11 (was Slide 8): "Proven Customer Success & Track Record"
    # =========================================================================
    slide_cust = prs.slides[10] # Now at index 10 (Slide 11)
    
    # Add prominent domain breadth banner right under the subtitle
    banner = slide_cust.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.21), Inches(1.82), Inches(16.69), Inches(0.38))
    banner.fill.solid()
    banner.fill.fore_color.rgb = CARD_BG_LIGHT_BLUE
    banner.line.color.rgb = BORDER_BLUE
    banner.line.width = Pt(1)
    
    tf_ban = banner.text_frame
    tf_ban.word_wrap = True
    tf_ban.margin_left = Inches(0.2)
    tf_ban.margin_top = Inches(0.06)
    p_ban = tf_ban.paragraphs[0]
    p_ban.text = "PROVEN TRACK RECORD ACROSS:   ENERGY & UTILITIES   |   INDUSTRIAL MANUFACTURING   |   ENTERPRISE DIGITAL TRANSFORMATION"
    p_ban.font.name = "Arial"
    p_ban.font.size = Pt(10)
    p_ban.font.bold = True
    p_ban.font.color.rgb = BLUE_ACCENT
    p_ban.alignment = PP_ALIGN.CENTER

    # Update category tags inside the 4 customer cards on Slide 11
    # Card 1: JBVNL & TVNL (TextBox 6)
    for sh in slide_cust.shapes:
        if sh.name == 'TextBox 6':
            sh.text_frame.paragraphs[0].text = "JBVNL & TVNL  [ENERGY & UTILITIES DISTRIBUTION]"
            sh.text_frame.paragraphs[0].font.size = Pt(13)
        elif sh.name == 'TextBox 8':
            sh.text_frame.paragraphs[0].text = "Lineage Power & Windcare  [RENEWABLES & BESS]"
            sh.text_frame.paragraphs[0].font.size = Pt(13)
        elif sh.name == 'TextBox 10':
            sh.text_frame.paragraphs[0].text = "Midwest Energy & HSA  [INDUSTRIAL MANUFACTURING & MES]"
            sh.text_frame.paragraphs[0].font.size = Pt(13)
        elif sh.name == 'TextBox 12':
            sh.text_frame.paragraphs[0].text = "Qatar Energy & Acelion Energy  [DIGITAL TRANSFORMATION]"
            sh.text_frame.paragraphs[0].font.size = Pt(13)

    # =========================================================================
    # UPDATE SLIDE NUMBERING FOOTERS CONSISTENTLY ACROSS ALL NUMBERED SLIDES
    # =========================================================================
    # The numbered sequence has 12 content slides (Slide 2 through Slide 12).
    # Slide 13 is Partnering for the Future (Closing, unnumbered).
    # Slide 14 is Industries We Serve.
    # Slide 15 is Trusted By.
    # Slide 16 is Get in Touch.
    # Total numbered sequence denominator: 13 (matching the original 'Slide X of 10' convention for the core deck + 3 new slides = 13).
    TOTAL_NUMBERED = 13
    
    for s_idx in range(1, 12): # slides 2 to 12 (0-indexed 1 to 11)
        cur_slide = prs.slides[s_idx]
        display_num = s_idx + 1
        
        # Look for footer text box containing 'Slide '
        found_footer = False
        for sh in cur_slide.shapes:
            if sh.has_text_frame and 'Slide ' in sh.text_frame.text:
                for p in sh.text_frame.paragraphs:
                    p.text = f"Slide {display_num} of {TOTAL_NUMBERED}"
                    p.font.name = "Calibri"
                    p.font.size = Pt(9)
                    p.font.color.rgb = TEXT_MUTED
                    p.alignment = PP_ALIGN.RIGHT
                found_footer = True
                break
                
        # If not found (like in new slides if not caught), add it
        if not found_footer:
            tx_num = cur_slide.shapes.add_textbox(Inches(16.48), Inches(9.84), Inches(1.42), Inches(0.32))
            tf_num = tx_num.text_frame
            tf_num.word_wrap = True
            tf_num.margin_right = 0
            p_num = tf_num.paragraphs[0]
            p_num.text = f"Slide {display_num} of {TOTAL_NUMBERED}"
            p_num.font.name = "Calibri"
            p_num.font.size = Pt(9)
            p_num.font.color.rgb = TEXT_MUTED
            p_num.alignment = PP_ALIGN.RIGHT

    # Save to local workspace presentation file
    prs.save(deck_path)
    print(f"Successfully saved enhanced presentation to: {deck_path}")
    
    # Also save to D: drive path so the source location remains updated
    d_path = "D:/Lumbini Elite Group/New Decks Lumbini/Elitia Enterprise Suite for Energy's Next-Gen Infrastructure.pptx"
    try:
        prs.save(d_path)
        print(f"Successfully synchronized to D: drive: {d_path}")
    except Exception as e:
        print(f"Warning: Could not save to D: drive directly ({e}), copying file instead...")
        shutil.copy2(deck_path, d_path)

if __name__ == "__main__":
    build_sustainability_extension()
