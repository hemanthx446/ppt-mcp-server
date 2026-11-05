import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

# Initialize presentation
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Constants
DARK_CHARCOAL = RGBColor(18, 18, 18)
LIGHT_BG = RGBColor(248, 249, 250)
HITACHI_RED = RGBColor(227, 6, 19)
TEXT_DARK = RGBColor(26, 32, 44)
TEXT_MUTED = RGBColor(113, 128, 150)
WHITE = RGBColor(255, 255, 255)
BORDER_GRAY = RGBColor(226, 232, 240)
CARD_BG = RGBColor(255, 255, 255)
CARD_BG_MUTED = RGBColor(247, 250, 252)

TOTAL_SLIDES = 10

# Helper function to create blank slide and set background
def create_base_slide(prs, is_dark=False):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    if is_dark:
        bg.fill.fore_color.rgb = DARK_CHARCOAL
    else:
        bg.fill.fore_color.rgb = LIGHT_BG
    bg.line.fill.background()
    return slide

# Helper function to add headers on content slides
def add_slide_header(slide, title_text, is_dark=False):
    # Red stripe
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.5), Inches(0.08), Inches(0.45))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = HITACHI_RED
    stripe.line.fill.background()
    
    # Title Text
    tx_box = slide.shapes.add_textbox(Inches(1.0), Inches(0.45), Inches(11.0), Inches(0.6))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0)
    tf.margin_top = Inches(0)
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Arial"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = WHITE if is_dark else TEXT_DARK

# Helper function to add subtitle on content slides
def add_slide_subtitle(slide, subtitle_text):
    tx_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.0), Inches(11.5), Inches(0.4))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0)
    tf.margin_top = Inches(0)
    p = tf.paragraphs[0]
    p.text = subtitle_text
    p.font.name = "Calibri"
    p.font.size = Pt(13)
    p.font.italic = True
    p.font.color.rgb = TEXT_MUTED

# Helper function to add footer on content slides
def add_slide_footer(slide, slide_num, total_slides=TOTAL_SLIDES):
    # Divider
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.01))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER_GRAY
    line.line.fill.background()
    
    # Footer Text
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.92), Inches(8.0), Inches(0.3))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0)
    p = tf.paragraphs[0]
    p.text = "Lumbini Elitia Enterprise Suite  |  Strategic Pitch for Hitachi Energy"
    p.font.name = "Calibri"
    p.font.size = Pt(9)
    p.font.color.rgb = TEXT_MUTED
    
    # Page Number
    tx_box_num = slide.shapes.add_textbox(Inches(11.533), Inches(6.92), Inches(1.0), Inches(0.3))
    tf_num = tx_box_num.text_frame
    tf_num.word_wrap = True
    tf_num.margin_right = Inches(0)
    p_num = tf_num.paragraphs[0]
    p_num.text = f"Slide {slide_num} of {total_slides}"
    p_num.font.name = "Calibri"
    p_num.font.size = Pt(9)
    p_num.font.color.rgb = TEXT_MUTED
    p_num.alignment = PP_ALIGN.RIGHT

# Helper function to create clean container cards
def add_card(slide, left, top, width, height, title, subtitle=None, bullets=None, bg_color=CARD_BG, border_color=BORDER_GRAY):
    # Card shape
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
        
    # Text Box
    tx_box = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.2), Inches(width - 0.4), Inches(height - 0.4))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0)
    tf.margin_top = Inches(0)
    tf.margin_right = Inches(0)
    
    # Card Title
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = HITACHI_RED
    p.space_after = Pt(6)
    
    if subtitle:
        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.name = "Calibri"
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_DARK
        p2.space_after = Pt(8)
        
    if bullets:
        for bullet in bullets:
            p_b = tf.add_paragraph()
            p_b.text = "•  " + bullet.replace("**", "")
            p_b.font.name = "Calibri"
            p_b.font.size = Pt(10.5)
            p_b.font.color.rgb = TEXT_DARK
            p_b.space_after = Pt(4)

# Helper function to add vertical architecture layer card
def add_layer_card(slide, left, top, width, height, title, content, bg_color=CARD_BG, border_color=BORDER_GRAY):
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
        
    tx_box = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.15), Inches(width - 0.4), Inches(height - 0.3))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0)
    tf.margin_top = Inches(0)
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = HITACHI_RED
    p.space_after = Pt(2)
    
    p2 = tf.add_paragraph()
    p2.text = content
    p2.font.name = "Calibri"
    p2.font.size = Pt(11)
    p2.font.color.rgb = TEXT_DARK

# Helper function to format tables
def format_table(table, header_bg=HITACHI_RED, header_fg=WHITE, row_bg_even=CARD_BG, row_bg_odd=CARD_BG_MUTED):
    for c in range(len(table.columns)):
        cell = table.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_bg
        p = cell.text_frame.paragraphs[0]
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = header_fg
        
    for r in range(1, len(table.rows)):
        bg_color = row_bg_even if r % 2 == 0 else row_bg_odd
        for c in range(len(table.columns)):
            cell = table.cell(r, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_color
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Calibri"
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_DARK
            p.font.bold = (c == 0)

# ----------------- SLIDE BUILDERS -----------------

# Slide 1: Title Slide (Dark Theme)
def build_slide_1(prs):
    slide = create_base_slide(prs, is_dark=True)
    
    # Left Red Stripe
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.12), Inches(3.8))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = HITACHI_RED
    stripe.line.fill.background()
    
    # Title & Subtitle
    tx_box = slide.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(2.2))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p_title = tf.paragraphs[0]
    p_title.text = "Empowering Hitachi Energy's Next-Gen Infrastructure:"
    p_title.font.name = "Arial"
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = WHITE
    
    p_title2 = tf.add_paragraph()
    p_title2.text = "Lumbini Elitia Enterprise Suite & Co-Innovation Services"
    p_title2.font.name = "Arial"
    p_title2.font.size = Pt(36)
    p_title2.font.bold = True
    p_title2.font.color.rgb = HITACHI_RED
    p_title2.space_after = Pt(20)
    
    # Subtitle
    tx_sub = slide.shapes.add_textbox(Inches(1.2), Inches(4.2), Inches(11.0), Inches(1.0))
    tf_sub = tx_sub.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "A Deep-Domain Digital Transformation Suite Bridging Design, Shop-Floor Operations, and Enterprise IT/OT Convergence"
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(17)
    p_sub.font.italic = True
    p_sub.font.color.rgb = RGBColor(180, 187, 195)
    
    # Partnership Details Footer
    tx_foot = slide.shapes.add_textbox(Inches(1.2), Inches(5.8), Inches(8.0), Inches(1.0))
    tf_foot = tx_foot.text_frame
    tf_foot.word_wrap = True
    p_foot = tf_foot.paragraphs[0]
    p_foot.text = "Lumbini Elitia × Hitachi Energy Partnership Proposal"
    p_foot.font.name = "Arial"
    p_foot.font.size = Pt(12)
    p_foot.font.bold = True
    p_foot.font.color.rgb = HITACHI_RED
    p_foot.space_after = Pt(2)
    
    p_foot2 = tf_foot.add_paragraph()
    p_foot2.text = "August 2026  |  GTIC Porur & Chengalpattu Advanced Manufacturing Facility"
    p_foot2.font.name = "Calibri"
    p_foot2.font.size = Pt(11)
    p_foot2.font.color.rgb = TEXT_MUTED

# Slide 2: Executive Summary & Local Footprint (Light Theme)
def build_slide_2(prs):
    slide = create_base_slide(prs, is_dark=False)
    add_slide_header(slide, "Executive Summary & Local Footprint")
    add_slide_subtitle(slide, "Strategic alignment with Hitachi Energy's Chennai engineering design and manufacturing footprint.")
    
    # Left Column: Executive Summary Card
    summary_bullets = [
        "Power & Energy DNA: Deep experience in utility networks and heavy manufacturing infrastructure.",
        "Hybrid Capability Model: Joint product co-development and staff augmentation services alongside the Elitia software suite.",
        "Local Footprint Alignment: Direct support for Porur GTIC engineering teams and Chengalpattu factory workloads.",
        "System Lifespan Mindset: Software and engineering designed for 30-40 years of high-availability utility operation."
    ]
    add_card(slide, 0.8, 1.5, 5.5, 5.0, "Executive Summary", "Strategic Positioning & Domain DNA", summary_bullets)
    
    # Right Column Top: Porur GTIC
    porur_bullets = [
        "Engineering R&D and Power Electronics Simulation.",
        "Elitia Integration: Configuration release control, CAD/BOM sync, and data profiling.",
        "Co-Development: Direct API integration co-development with GTIC system engineers."
    ]
    add_card(slide, 6.7, 1.5, 5.8, 2.3, "Global Technology & Innovation Centre (GTIC) - Porur", "Engineering Focus", porur_bullets)
    
    # Right Column Bottom: Chengalpattu
    chengalpattu_bullets = [
        "Advanced HVDC systems and Power Quality manufacturing (₹2,000 crore expansion).",
        "Elitia Integration: Shop-floor MES quality gates, predictive APM, and migration validations.",
        "Augmentation: On-demand squads of utility and data engineers to accelerate continuous upgrades."
    ]
    add_card(slide, 6.7, 4.1, 5.8, 2.4, "Advanced Manufacturing Facility - Chengalpattu", "Operations Focus", chengalpattu_bullets)
    
    add_slide_footer(slide, 2)

# Slide 3: Power Domain DNA & Core Capabilities (Light Theme)
def build_slide_3(prs):
    slide = create_base_slide(prs, is_dark=False)
    add_slide_header(slide, "Power Domain DNA & Core Capabilities")
    add_slide_subtitle(slide, "Lumbini has over 12 years of utility software heritage with a core philosophy of building for 30-40 years of service life.")
    
    # Top Highlight Bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(0.6))
    bar.fill.solid()
    bar.fill.fore_color.rgb = CARD_BG_MUTED
    bar.line.color.rgb = BORDER_GRAY
    
    tx_bar = slide.shapes.add_textbox(Inches(1.0), Inches(1.45), Inches(11.3), Inches(0.5))
    tf_bar = tx_bar.text_frame
    tf_bar.word_wrap = True
    p_bar = tf_bar.paragraphs[0]
    p_bar.text = "12+ Years Heritage  |  ISO 9001 & 27001 Certified  |  Active Siemens & SAP Global Partner Ecosystem"
    p_bar.font.name = "Arial"
    p_bar.font.size = Pt(12)
    p_bar.font.bold = True
    p_bar.font.color.rgb = HITACHI_RED
    p_bar.alignment = PP_ALIGN.CENTER
    
    # 4-Quadrant Card Grid
    add_card(slide, 0.8, 2.2, 5.6, 2.1, "Generation Systems", "Telemetry & Asset Monitoring", [
        "Grid integration portals for Hydro, Thermal, and Solar setups.",
        "Real-time boiler telemetry and generation dispatch optimization."
    ])
    
    add_card(slide, 6.9, 2.2, 5.6, 2.1, "Transmission & Substation", "IEC 61850 & HVDC Focus", [
        "Substation automation software configurations and RTU mapping.",
        "Transformer diagnostics and high-voltage line monitoring."
    ])
    
    add_card(slide, 0.8, 4.5, 5.6, 2.2, "Grid Distribution", "Smart Metering & Billing", [
        "Orchestration layers for smart meters handling millions of endpoints.",
        "Outage management system (OMS) billing validation loops."
    ])
    
    add_card(slide, 6.9, 4.5, 5.6, 2.2, "Renewables & Microgrids", "BESS & Distributed Energy", [
        "Secure SCADA telemetry interfaces for wind/solar remote platforms.",
        "Battery Bank (BESS) charge control and battery pack diagnostics."
    ])
    
    add_slide_footer(slide, 3)

# Slide 4: Elitia Industrial Suite & EMS Architecture (Light Theme)
def build_slide_4(prs):
    slide = create_base_slide(prs, is_dark=False)
    add_slide_header(slide, "Elitia Suite: L0-L4 IT/OT Convergence")
    add_slide_subtitle(slide, "Our proprietary product suite bridges shop-floor operations with enterprise analytics in a standard layered model.")
    
    # Layer 4 (Top)
    add_layer_card(slide, 0.8, 1.5, 11.733, 1.15, 
                   "Layer 4: Business Enterprise Level (SAP ERP, Siemens PLM, Elitia BI)",
                   "Aggregated cross-plant OEE dashboards, supply chain demand forecasting, and central master data governance via Elitia DGS.")
                   
    # Layer 3
    add_layer_card(slide, 0.8, 2.8, 11.733, 1.15,
                   "Layer 3: Operations Management Level (Elitia APM & Scheduling)",
                   "Predictive maintenance models, asset remaining useful life (RUL) forecasting, and engineering change order (ECO) release flows.")
                   
    # Layer 2
    add_layer_card(slide, 0.8, 4.1, 11.733, 1.15,
                   "Layer 2: Supervisory Control Level (Elitia MES, SCADA, Grid-X)",
                   "Local shop-floor execution tracking, paperless operator instructions, closed-loop quality gates, and remote monitoring systems (RMS).")
                   
    # Layer 0-1 (Bottom)
    add_layer_card(slide, 0.8, 5.4, 11.733, 1.15,
                   "Layer 0-1: Field Control & Physical Level (PLCs, Remote I/O, BESS Banks)",
                   "High-frequency sensor telemetry (thermal, vibration, voltage), battery cell controllers, and edge communication gateways.")
                   
    add_slide_footer(slide, 4)

# Slide 5: Smart Manufacturing & HVDC Shop-Floor Optimization (Light Theme)
def build_slide_5(prs):
    slide = create_base_slide(prs, is_dark=False)
    add_slide_header(slide, "Smart Manufacturing & HVDC Shop-Floor Optimization")
    add_slide_subtitle(slide, "Empowering shop-floor operators with predictive asset health, MES, and Vision AI.")
    
    # Left Column: APM/MES
    mes_bullets = [
        "Remaining Useful Life (RUL): Predicts optimal maintenance windows for critical curing ovens and winding machines.",
        "High-Frequency Edge Telemetry: Dynamic processing of vibration, thermal, and acoustic sensors on testing bays.",
        "Traceability: Serialization and history tracking for complex HVDC transformer parts.",
        "Defect Reduction: Reduces unscheduled line stoppages, securing high plant yield."
    ]
    add_card(slide, 0.8, 1.6, 5.6, 5.0, "Elitia MES & APM: Predictive Asset Performance", "HVDC Curing & Winding Control", mes_bullets)
    
    # Right Column: Vision AI
    vision_bullets = [
        "Vision AI Inspection: High-speed camera arrays check welds, alignment, and components on automated assembly lines.",
        "Closed-Loop Quality reconciliation: Real-time visual defect detection automatically links back to PLM CAD records.",
        "Automatic Alerts: Instantly flags assembly line deviations to operators before damage occurs.",
        "Partner Case Study: Deployed Vision QA at Midwest Energy plants with a 24% reduction in manual inspection requirements."
    ]
    add_card(slide, 6.9, 1.6, 5.6, 5.0, "Vision AI & Closed-Loop Quality Inspection", "Automated QA & Defect Tracking", vision_bullets)
    
    add_slide_footer(slide, 5)

# Slide 6: Grid Management & Energy Storage Systems (BESS) (Light Theme)
def build_slide_6(prs):
    slide = create_base_slide(prs, is_dark=False)
    add_slide_header(slide, "Grid Management & Energy Storage Systems (BESS)")
    add_slide_subtitle(slide, "Real-time distribution SCADA portals and sensor-driven battery health monitoring.")
    
    # Left Column: EMS / SCADA
    ems_bullets = [
        "EMS Integration: Real-time load balancing, substation monitoring, and active dispatch telemetry.",
        "Grid-X SCADA: Supports standard industrial protocols (IEC 60870-5, DNP3, Modbus) for legacy grids.",
        "Smart Meter Orchestration: Links dispatch telemetry to billing engines and smart meter endpoints."
    ]
    add_card(slide, 0.8, 1.6, 5.6, 5.0, "Elitia EMS & Grid-X SCADA", "Utility Grid Control", ems_bullets)
    
    # Right Column: BESS
    bess_bullets = [
        "Cell-Level Diagnostics: Continuous logs of cell thermal parameters, voltage, and vibration cycles.",
        "Early Fault Detection: Custom algorithms predict thermal runaway risks, automatically isolating faulty battery cells.",
        "Optimized C-Rating: Programmatically manages battery charge/discharge loops to extend battery life cycles by 20%."
    ]
    add_card(slide, 6.9, 1.6, 5.6, 5.0, "Battery Bank (BESS) Telemetry", "Thermal & Charge Diagnostics", bess_bullets)
    
    add_slide_footer(slide, 6)

# Slide 7: Enterprise Data Governance & Migrations (Light Theme)
def build_slide_7(prs):
    slide = create_base_slide(prs, is_dark=False)
    add_slide_header(slide, "Enterprise Data Governance & Migrations")
    add_slide_subtitle(slide, "Elitia DGS acts as an SAP MDG equivalent, ensuring master data consistency and lineage.")
    
    # Left Column: DGS
    dgs_bullets = [
        "SAP MDG Equivalent: Centralizes asset and material master catalogs across multiple manufacturing locations.",
        "Schema Cleansing: Automatically checks syntax and profile completeness before records are committed.",
        "Audit-Ready Lineage: Generates visual lineage maps showing asset changes and historical data modifications."
    ]
    add_card(slide, 0.8, 1.6, 5.6, 5.0, "Elitia DGS: Master Data Governance", "Data Consistency & Lineage", dgs_bullets)
    
    # Right Column: DVE
    dve_bullets = [
        "DVE validation framework: Designed for major utility database upgrades and legacy-to-modern ERP migrations.",
        "150+ Custom Rules: Automated business checks target electrical engineering schemas and substation structures.",
        "Zero-Loss Reconciliation: Performs pre- and post-migration validation checks to guarantee zero data loss."
    ]
    add_card(slide, 6.9, 1.6, 5.6, 5.0, "Data Validation Engine (DVE)", "Frictionless Migration Pipeline", dve_bullets)
    
    add_slide_footer(slide, 7)

# Slide 8: Proven Customer Success & Track Record (Light Theme)
def build_slide_8(prs):
    slide = create_base_slide(prs, is_dark=False)
    add_slide_header(slide, "Proven Customer Success & Track Record")
    add_slide_subtitle(slide, "Delivering digital transformation and engineering excellence across global utility networks.")
    
    # 4-Quadrant Case Studies Grid
    add_card(slide, 0.8, 1.6, 5.6, 2.4, "JBVNL & TVNL", "SAP ERP & Grid Distribution", [
        "Full SAP ERP rollout across utility distribution and billing channels.",
        "Standardized asset schemas for millions of smart metering points."
    ])
    
    add_card(slide, 6.9, 1.6, 5.6, 2.4, "Lineage Power & Windcare", "RMS & SCADA gateways", [
        "Deployed Remote Monitoring Systems (RMS) for power conversion devices.",
        "Secure SCADA setups deployed for distributed wind and solar generation plants."
    ])
    
    add_card(slide, 0.8, 4.2, 5.6, 2.4, "Midwest Energy & HSA", "Plant MES & EMS Deployments", [
        "Engineered custom MES modules for shop-floor assembly lines.",
        "Implemented Energy Management Systems (EMS) to balance plant power loads."
    ])
    
    add_card(slide, 6.9, 4.2, 5.6, 2.4, "Qatar Energy & Aceleon", "Industrial Digital Solutions", [
        "Developed cross-border industrial telemetry platforms for energy assets.",
        "Digital twin dashboards showing real-time utility parameters."
    ])
    
    add_slide_footer(slide, 8)

# Slide 9: Flexible Engagement & Staff Augmentation Model (Light Theme)
def build_slide_9(prs):
    slide = create_base_slide(prs, is_dark=False)
    add_slide_header(slide, "Flexible Engagement & Co-Innovation")
    add_slide_subtitle(slide, "Supporting Hitachi's continuous local/global projects with adaptive resource and co-development models.")
    
    # 3 Column Cards
    col1_bullets = [
        "Modular licensing of the proprietary Elitia suite (MES, APM, DGS, BI, EMS).",
        "Includes standard APIs for fast integration with SAP ERP and Siemens PLM."
    ]
    add_card(slide, 0.8, 1.6, 3.6, 5.0, "Software Licensing", "Elitia Product Suite", col1_bullets)
    
    col2_bullets = [
        "Dedicated engineering squads work side-by-side with GTIC Porur design teams.",
        "Shared codebase ownership and custom feature extension development.",
        "Experienced in standard enterprise product development lifecycle."
    ]
    add_card(slide, 4.8, 1.6, 3.6, 5.0, "Expert Co-Development", "Shared Engineering Model", col2_bullets)
    
    col3_bullets = [
        "Access to certified utility engineers, power electronics, and data experts.",
        "Resource squads ready to scale up within 2-4 weeks to hit critical deadlines.",
        "Flexible staffing structure aligning with local operations and global headquarters."
    ]
    add_card(slide, 8.8, 1.6, 3.7, 5.0, "Staff Augmentation", "On-Demand Resource Delivery", col3_bullets)
    
    add_slide_footer(slide, 9)

# Slide 10: Partnership Call to Action (Dark Theme)
def build_slide_10(prs):
    slide = create_base_slide(prs, is_dark=True)
    
    # Left Red Stripe
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.12), Inches(3.8))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = HITACHI_RED
    stripe.line.fill.background()
    
    # Text box containing title and bullets
    tx_box = slide.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(4.8))
    tf = tx_box.text_frame
    tf.word_wrap = True
    
    # Title
    p_title = tf.paragraphs[0]
    p_title.text = "Partnering for the Future of Energy Infrastructure"
    p_title.font.name = "Arial"
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = WHITE
    p_title.space_after = Pt(20)
    
    # Next Steps Bullet points
    next_steps = [
        "Proposing an immediate Architecture Workshop at GTIC Porur to map integration points.",
        "Initiating a 30-Day Proof of Value (PoV) on a selected HVDC winding line at Chengalpattu.",
        "Establishing an Agile Delivery & Augmentation SLA to support your ₹2,000 Cr facility expansion."
    ]
    
    for i, step in enumerate(next_steps):
        p_step = tf.add_paragraph()
        p_step.text = f"{i+1}.  {step}"
        p_step.font.name = "Calibri"
        p_step.font.size = Pt(14)
        p_step.font.color.rgb = RGBColor(220, 225, 230)
        p_step.space_after = Pt(12)
        
    p_spacer = tf.add_paragraph()
    p_spacer.space_after = Pt(24)
    
    # Offices metadata
    p_contact_title = tf.add_paragraph()
    p_contact_title.text = "LUMBINI ELITIA GLOBAL OFFICES"
    p_contact_title.font.name = "Arial"
    p_contact_title.font.size = Pt(12)
    p_contact_title.font.bold = True
    p_contact_title.font.color.rgb = HITACHI_RED
    
    p_contact = tf.add_paragraph()
    p_contact.text = "Locations: Bangalore  |  Noida  |  Ranchi  |  Doha, Qatar  |  Chennai (Local Support Office)"
    p_contact.font.name = "Calibri"
    p_contact.font.size = Pt(11)
    p_contact.font.color.rgb = TEXT_MUTED

# Build all slides
build_slide_1(prs)
build_slide_2(prs)
build_slide_3(prs)
build_slide_4(prs)
build_slide_5(prs)
build_slide_6(prs)
build_slide_7(prs)
build_slide_8(prs)
build_slide_9(prs)
build_slide_10(prs)

# Save presentation
output_path = "Hitachi_Energy_Elitia_Enterprise_Pitch.pptx"
prs.save(output_path)
print(f"Presentation successfully created at: {output_path}")
