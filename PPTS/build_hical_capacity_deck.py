import os
# pyrefly: ignore [missing-import]
from pptx import Presentation
# pyrefly: ignore [missing-import]
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def build_presentation(output_path="HICAL_Capacity_Intelligence_Strategic_Roadmap.pptx"):
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
    
    TOTAL_SLIDES = 11

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
        # Category Tag Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.38), Inches(3.8), Inches(0.26))
        badge.fill.solid()
        badge.fill.fore_color.rgb = DARK_CARD if is_dark else RGBColor(238, 242, 255)
        badge.line.color.rgb = CYAN_ACCENT if is_dark else SAP_BLUE
        badge.line.width = Pt(1)
        tf_b = badge.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = Inches(0.1)
        tf_b.margin_top = Inches(0.02)
        p_b = tf_b.paragraphs[0]
        p_b.text = category_text.upper()
        p_b.font.name = "Arial"
        p_b.font.size = Pt(8.5)
        p_b.font.bold = True
        p_b.font.color.rgb = CYAN_ACCENT if is_dark else SAP_BLUE
        
        # Title
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
        
        # Subtitle
        if subtitle_text:
            tx_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.08), Inches(11.733), Inches(0.28))
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
        p.text = "Lumbini Elite Solutions  |  HICAL Technologies Strategic Roadmap  |  Confidential"
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

    def set_speaker_notes(slide, notes_text):
        try:
            notes_slide = slide.notes_slide
            tf = notes_slide.notes_text_frame
            tf.text = notes_text
        except Exception as e:
            print(f"Warning: Could not set notes: {e}")

    # =============================================================
    # SLIDE 1: Title & Executive Positioning (Dark Theme)
    # =============================================================
    s1 = add_base_slide(is_dark=True)
    
    # Top decorative cyan glow line
    top_glow = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    top_glow.fill.solid()
    top_glow.fill.fore_color.rgb = GOLD_ACCENT
    top_glow.line.fill.background()
    
    # Executive Tag Badge
    b1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.1), Inches(4.8), Inches(0.34))
    b1.fill.solid()
    b1.fill.fore_color.rgb = DARK_CARD
    b1.line.color.rgb = GOLD_ACCENT
    b1.line.width = Pt(1.2)
    tf1 = b1.text_frame
    tf1.margin_top = Inches(0.03)
    p = tf1.paragraphs[0]
    p.text = "AEROSPACE & DEFENSE MANUFACTURING EXCELLENCE"
    p.font.name = "Arial"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    
    # Main Title
    tx = s1.shapes.add_textbox(Inches(0.9), Inches(1.6), Inches(7.2), Inches(1.6))
    tf = tx.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "From Reactive Firefighting\nto Proactive Capacity\nIntelligence"
    p.font.name = "Arial"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT
    
    # Subtitle
    tx_sub = s1.shapes.add_textbox(Inches(0.9), Inches(3.45), Inches(7.2), Inches(0.8))
    tf_sub = tx_sub.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_left = tf_sub.margin_top = 0
    p = tf_sub.paragraphs[0]
    p.text = "A Strategic Roadmap to Transform Backlog & Costing Visibility into Real-Time Management Decisioning for HICAL Technologies"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.italic = True
    p.font.color.rgb = TEXT_LIGHT_MUTED
    
    # 4 Strategic Pillars Card on Left Bottom
    pillars_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(4.45), Inches(7.2), Inches(2.2))
    pillars_card.fill.solid()
    pillars_card.fill.fore_color.rgb = DARK_CARD
    pillars_card.line.color.rgb = DARK_BORDER
    pillars_card.line.width = Pt(1)
    
    tf_pc = pillars_card.text_frame
    tf_pc.word_wrap = True
    tf_pc.margin_left = Inches(0.2)
    tf_pc.margin_top = Inches(0.18)
    tf_pc.margin_right = Inches(0.2)
    
    bullets = [
        ("Challenge Reframed:", " HICAL's request for backlog & costing reports is a gateway to solving systemic operational constraints."),
        ("Opportunity Identified:", " Real-time visibility into order status, capacity bottlenecks, and financial exposure enables proactive control."),
        ("Our Approach:", " A phased, value-driven transformation delivering immediate MVP reporting while scaling into full SAP ePPDS/CRP."),
        ("Expected Outcome:", " Reduced backlog variance, 98%+ on-time delivery predictability, lower execution risk, and quantified margin recovery.")
    ]
    for i, (b_title, b_desc) in enumerate(bullets):
        p = tf_pc.paragraphs[0] if i == 0 else tf_pc.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = CYAN_ACCENT
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.bold = False
        r2.font.size = Pt(10)
        r2.font.color.rgb = TEXT_LIGHT
        
    # Right Side 3-Layer Visual Progression Stack (40% width)
    stack_bg = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.4), Inches(1.1), Inches(4.1), Inches(5.55))
    stack_bg.fill.solid()
    stack_bg.fill.fore_color.rgb = DARK_CARD
    stack_bg.line.color.rgb = DARK_BORDER
    stack_bg.line.width = Pt(1.2)
    
    # Header inside stack
    tx_st = s1.shapes.add_textbox(Inches(8.6), Inches(1.3), Inches(3.7), Inches(0.4))
    tf_st = tx_st.text_frame
    tf_st.word_wrap = True
    p = tf_st.paragraphs[0]
    p.text = "CAPABILITY MATURITY STACK"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    
    # Layer 3: Top - Gold
    l3 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.65), Inches(1.8), Inches(3.6), Inches(1.4))
    l3.fill.solid()
    l3.fill.fore_color.rgb = RGBColor(30, 27, 20)
    l3.line.color.rgb = GOLD_ACCENT
    l3.line.width = Pt(1.5)
    tf_l3 = l3.text_frame
    tf_l3.word_wrap = True
    tf_l3.margin_left = tf_l3.margin_top = Inches(0.12)
    p = tf_l3.paragraphs[0]
    p.text = "LAYER 3: PREDICTIVE & SIMULATION"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    p2 = tf_l3.add_paragraph()
    p2.text = "Capacity Intelligence & ePPDS"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_LIGHT
    p3 = tf_l3.add_paragraph()
    p3.text = "Finite capacity scheduling, ML bottleneck forecasting & automated what-if scenario engines."
    p3.font.size = Pt(9)
    p3.font.color.rgb = TEXT_LIGHT_MUTED
    
    # Layer 2: Middle - Blue
    l2 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.65), Inches(3.4), Inches(3.6), Inches(1.4))
    l2.fill.solid()
    l2.fill.fore_color.rgb = RGBColor(15, 30, 60)
    l2.line.color.rgb = CYAN_ACCENT
    l2.line.width = Pt(1.2)
    tf_l2 = l2.text_frame
    tf_l2.word_wrap = True
    tf_l2.margin_left = tf_l2.margin_top = Inches(0.12)
    p = tf_l2.paragraphs[0]
    p.text = "LAYER 2: DECISION COCKPIT"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p2 = tf_l2.add_paragraph()
    p2.text = "Real-Time Management Cockpit"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_LIGHT
    p3 = tf_l2.add_paragraph()
    p3.text = "Unified cross-functional risk scores, constraint heatmaps, and financial drag analysis."
    p3.font.size = Pt(9)
    p3.font.color.rgb = TEXT_LIGHT_MUTED
    
    # Layer 1: Base - Green
    l1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.65), Inches(5.0), Inches(3.6), Inches(1.4))
    l1.fill.solid()
    l1.fill.fore_color.rgb = RGBColor(16, 35, 28)
    l1.line.color.rgb = EMERALD_GREEN
    l1.line.width = Pt(1.2)
    tf_l1 = l1.text_frame
    tf_l1.word_wrap = True
    tf_l1.margin_left = tf_l1.margin_top = Inches(0.12)
    p = tf_l1.paragraphs[0]
    p.text = "LAYER 1: FOUNDATIONAL MVP"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = EMERALD_GREEN
    p2 = tf_l1.add_paragraph()
    p2.text = "Live Backlog & Costing Reports"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_LIGHT
    p3 = tf_l1.add_paragraph()
    p3.text = "Direct automated SAP HANA extracts retiring manual Excel tracker sheets in 8–12 weeks."
    p3.font.size = Pt(9)
    p3.font.color.rgb = TEXT_LIGHT_MUTED
    
    add_footer(s1, 1, is_dark=True)
    
    s1_notes = """SPEAKER NOTES:
"Good morning. Today, we're not just here to talk about building two reports. We're here to position HICAL for a transformation in how you manage one of the most critical operational challenges in aerospace/defense manufacturing: the tension between customer demand, production capacity, and execution cost.

Your request for a backlog report and a costing report is actually the entry point to something much bigger—a real-time management cockpit that connects order flow, capacity utilization, and financial exposure into a single decision-support system. Think of this like moving from a paper-based flight plan to a modern glass cockpit.

Over the next 45 minutes, we'll walk you through:
1. Why these two reports matter, and what they really represent
2. The hidden business logic that ties backlog, capacity, and cost together
3. A phased implementation roadmap that delivers value immediately while scaling toward a world-class ePPDS/CRP capability
4. The specific questions we need to answer to make this real in your environment

Let's start by grounding ourselves in your operational reality." """
    set_speaker_notes(s1, s1_notes)

    # =============================================================
    # SLIDE 2: Understanding HICAL's Operational Reality
    # =============================================================
    s2 = add_base_slide(is_dark=False)
    add_header(s2, "The Aerospace/Defense Manufacturing Complexity: Your Starting Point", "OPERATIONAL REALITY & CONTEXT")
    
    # Top 4-Stage Horizontal Flow Diagram
    flow_stages = [
        ("1. Customer Orders (SD)", "Firm MTO orders & forecast demand; strict contractual delivery dates & certifications.", SAP_BLUE),
        ("2. MTO/MTS Planning (PP)", "Multi-level routing, long-lead components, BOM explosion & capacity allocations.", GOLD_ACCENT),
        ("3. Multi-Facility Execution (EWM)", "Precision CNC, winding & sheet metal lines with setup constraints & QA gates.", PURPLE_ACCENT),
        ("4. Supplier Network (MM/SCP)", "Global high-reliability sourcing + local precision subcontracting with variable leads.", EMERALD_GREEN)
    ]
    
    w_box = 2.75
    h_box = 1.15
    for i, (title, desc, color_acc) in enumerate(flow_stages):
        x = 0.8 + i * (w_box + 0.24)
        box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.45), Inches(w_box), Inches(h_box))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = color_acc
        box.line.width = Pt(1.5)
        
        tf_b = box.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_top = Inches(0.1)
        p = tf_b.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = color_acc
        
        p2 = tf_b.add_paragraph()
        p2.text = desc
        p2.font.name = "Arial"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_DARK
        
        # Arrow connecting boxes (except last)
        if i < 3:
            arrow = s2.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + w_box + 0.05), Inches(1.9), Inches(0.14), Inches(0.25))
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = TEXT_MUTED
            arrow.line.fill.background()

    # Middle Left Card: Current State Pain Points (Red)
    cp_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.78), Inches(5.75), Inches(2.75))
    cp_card.fill.solid()
    cp_card.fill.fore_color.rgb = RED_LIGHT_BG
    cp_card.line.color.rgb = CRIMSON_RED
    cp_card.line.width = Pt(1.2)
    
    tf_cp = cp_card.text_frame
    tf_cp.word_wrap = True
    tf_cp.margin_left = tf_cp.margin_top = tf_cp.margin_right = Inches(0.18)
    p = tf_cp.paragraphs[0]
    p.text = "CURRENT STATE PAIN POINTS (REACTIVE MODE)"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = CRIMSON_RED
    
    pain_items = [
        ("Manual Excel Backlog Tracking:", "Planners burn 2+ hours/week reconciling orders, promises, and status across spreadsheets."),
        ("Siloed Departmental Visibility:", "Sales, Planning, Finance, and Operations manage divergent versions of truth."),
        ("Late Bottleneck Discovery:", "Capacity constraints are discovered only when a work center backs up, forcing crisis overtime."),
        ("Cost Variance Blind Spot:", "True backlog cost drag is hidden in lagging monthly CO variance reports long after execution.")
    ]
    for b_title, b_desc in pain_items:
        p = tf_cp.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = "• " + b_title + " "
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.bold = False
        r2.font.size = Pt(9)
        r2.font.color.rgb = TEXT_MUTED

    # Middle Right Card: Aerospace Operational Drivers (Blue)
    dr_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.78), Inches(2.78), Inches(5.75), Inches(2.75))
    dr_card.fill.solid()
    dr_card.fill.fore_color.rgb = CARD_BG
    dr_card.line.color.rgb = SAP_BLUE
    dr_card.line.width = Pt(1.2)
    
    tf_dr = dr_card.text_frame
    tf_dr.word_wrap = True
    tf_dr.margin_left = tf_dr.margin_top = tf_dr.margin_right = Inches(0.18)
    p = tf_dr.paragraphs[0]
    p.text = "AEROSPACE & DEFENSE OPERATIONAL DRIVERS"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = SAP_BLUE
    
    driver_items = [
        ("100% On-Time, Zero-Defect Mandate:", "Defense Tier-1 contracts carry heavy delay penalties, strict qualification audits, and zero tolerance."),
        ("Complex Hybrid Production Mix:", "Make-to-Order (MTO) customer builds combined with forecast-driven subassemblies (MTS)."),
        ("Multi-Tier BOM Dependencies:", "Sheet metal, precision winding, high-spec assembly, and subcontracts with distinct lead times."),
        ("Strict Quality Gate Hurdles:", "FAI (First Article Inspection) and SPC holds create execution delays that must be dynamically factored.")
    ]
    for b_title, b_desc in driver_items:
        p = tf_dr.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = "• " + b_title + " "
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.bold = False
        r2.font.size = Pt(9)
        r2.font.color.rgb = TEXT_MUTED

    # Bottom Banner: Data Landscape
    env_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.65), Inches(11.733), Inches(1.2))
    env_card.fill.solid()
    env_card.fill.fore_color.rgb = CARD_BG_MUTED
    env_card.line.color.rgb = CARD_BORDER
    env_card.line.width = Pt(1)
    
    tf_env = env_card.text_frame
    tf_env.word_wrap = True
    tf_env.margin_left = tf_env.margin_top = Inches(0.15)
    p = tf_env.paragraphs[0]
    p.text = "HICAL'S ENTERPRISE IT & DATA ASSETS: THE LEVERAGE POINT"
    p.font.name = "Arial"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = SAP_BLUE
    
    p2 = tf_env.add_paragraph()
    p2.space_before = Pt(3)
    p2.text = "• Core System: SAP HANA (MM, PP, PS, SD, EWM, CO/CA, BI) contains all operational data, but lacks a synthesized capacity-risk layer.\n• Advanced Planning: APO/ePPDS capable architecture exists within SAP, but is currently underutilized for finite constraint-based scheduling.\n• Analytics Layer: Tableau dashboards are already deployed across management, but are fed by manual Excel extracts rather than live SAP pipelines."
    p2.font.name = "Arial"
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = TEXT_DARK

    add_footer(s2, 2)
    
    s2_notes = """SPEAKER NOTES:
"Let's zoom into your world for a moment. HICAL operates in one of the most complex manufacturing verticals—aerospace and defense. Why does that matter? Because you're not just managing orders; you're managing a web of interdependencies:

First, you have demand complexity. You don't know if a customer order is going to be built from stock (MTS) or from scratch (MTO). Some components are long-lead supplier items bought months in advance. Others are made in-house with quality gates that add unpredictability.

Second, you have capacity constraints, and they're not always visible. You might have a precision CNC center, a sheet metal line, or a winding operation that becomes a bottleneck. You might not know it's constrained until an order hits it—at which point you're already late.

Third, you have cost exposure. When an order sits in backlog, it's tying up labor, consuming inventory holding cost, and potentially triggering supplier penalties. But where do you see that? You don't. It shows up in your monthly CO variance reports, weeks after the fact.

This is why your Excel backlog sheet exists. Planners maintain it because SAP doesn't answer their core question: 'Which orders are at-risk of missing their delivery date, what's the root cause, and what's it costing us?'

Your costing spreadsheet exists for the same reason: nobody has connected the dots between backlog depth -> capacity utilization -> execution cost.

So when you ask for a 'backlog report' and a 'costing report,' what you're really asking for is: 'Give me a system that tells me, in real-time, whether my operations are healthy.' That's what we are going to build." """
    set_speaker_notes(s2, s2_notes)

    # =============================================================
    # SLIDE 3: Deconstructing the Request
    # =============================================================
    s3 = add_base_slide(is_dark=False)
    add_header(s3, "From 'Two Reports' to 'One Integrated Management System'", "STRATEGIC REFRAMING")
    
    # Left Box (30% width): The Literal Request
    box_req = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(3.4), Inches(2.7))
    box_req.fill.solid()
    box_req.fill.fore_color.rgb = CARD_BG_MUTED
    box_req.line.color.rgb = CARD_BORDER
    box_req.line.width = Pt(1.2)
    
    tf_req = box_req.text_frame
    tf_req.word_wrap = True
    tf_req.margin_left = tf_req.margin_top = Inches(0.18)
    p = tf_req.paragraphs[0]
    p.text = "YOUR REQUEST (LITERAL VIEW)"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED
    
    req_bullets = [
        "Report 1: Backlog Report with open orders and current status.",
        "Report 2: Costing Report showing backlog cost figures.",
        "Approach: Flat tabular Excel or basic BI extract.",
        "Outcome: Static snapshots that freeze at demand spikes and trigger endless reconciliation meetings."
    ]
    for b in req_bullets:
        p = tf_req.add_paragraph()
        p.space_before = Pt(6)
        p.text = "• " + b
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_DARK

    # Center Transformation Badge
    arrow_t = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.35), Inches(2.3), Inches(0.9), Inches(0.9))
    arrow_t.fill.solid()
    arrow_t.fill.fore_color.rgb = GOLD_ACCENT
    arrow_t.line.fill.background()
    tf_at = arrow_t.text_frame
    tf_at.word_wrap = True
    p = tf_at.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "⟹\nVALUE"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = WHITE

    # Right Box (58% width): Strategic Systems View
    box_sys = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.4), Inches(1.4), Inches(7.133), Inches(2.7))
    box_sys.fill.solid()
    box_sys.fill.fore_color.rgb = CARD_BG
    box_sys.line.color.rgb = SAP_BLUE
    box_sys.line.width = Pt(1.5)
    
    tf_sys = box_sys.text_frame
    tf_sys.word_wrap = True
    tf_sys.margin_left = tf_sys.margin_top = Inches(0.18)
    p = tf_sys.paragraphs[0]
    p.text = "OUR INTERPRETATION (INTEGRATED SYSTEMS VIEW)"
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = SAP_BLUE
    
    sys_blocks = [
        ("1. Order Pipeline & Risk Management:", "Enriches backlog with buffer health, dynamic risk scoring (1-10), QA status, and material readiness."),
        ("2. Capacity-Finance Bridge:", "Links specific work center bottlenecks (CNC, sheet metal) directly to the financial cost of delayed orders."),
        ("3. Integrated Management Cockpit:", "Unifies order pipeline, capacity utilization, and what-if simulation (shift addition, expediting, sequencing) in live Tableau.")
    ]
    for b_title, b_desc in sys_blocks:
        p = tf_sys.add_paragraph()
        p.space_before = Pt(5)
        r1 = p.add_run()
        r1.text = "• " + b_title + " "
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.bold = False
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = TEXT_MUTED

    # Bottom Comparison Table
    table_shape = s3.shapes.add_table(7, 3, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.55))
    table = table_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(4.4)
    table.columns[2].width = Inches(5.133)
    
    headers = ["Dimension", "Report-Only Approach (Traditional)", "Integrated Cockpit Approach (Lumbini Proposal)"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = SAP_BLUE if col_idx == 2 else DARK_CARD
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(9)
        p.font.color.rgb = WHITE
        
    rows_data = [
        ("Scope & Horizon", "Static order listing + basic historical cost summaries", "Order pipeline + capacity load + financial drag + action engine"),
        ("Data Latency", "Daily or weekly manual Excel extracts", "Near real-time (4-hr live automated refresh directly from SAP)"),
        ("Depth of Insight", "Answers WHAT is late after it occurs", "Answers WHAT, WHY, WHICH constraints, and FINANCIAL IMPACT"),
        ("Operational Value", "Triggers meetings, debate, and firefighting", "Drives actionable decisions directly from exception dashboards"),
        ("Adaptability", "Breaks down during volume spikes or supply shocks", "Dynamically absorbs changes in priority, shifts, or vendor status"),
        ("Phase 1 Delivery", "6–8 weeks for basic reports", "8–12 weeks for automated reports AND integrated MVP dashboard")
    ]
    for row_idx, r in enumerate(rows_data):
        for col_idx, val in enumerate(r):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(240, 249, 255) if col_idx == 2 else (WHITE if row_idx % 2 == 0 else CARD_BG_MUTED)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.font.bold = (col_idx == 0 or col_idx == 2)
            p.font.color.rgb = SAP_BLUE if col_idx == 2 else TEXT_DARK
            
    add_footer(s3, 3)
    
    s3_notes = """SPEAKER NOTES:
"Let me be direct: if we just build you a backlog report and a costing report, you'll have better information than you have today. But you'll still be solving the problem the same way you're solving it now—manually, in spreadsheets and meetings.

Here's what's actually happening:
- Planners maintain a backlog spreadsheet to compensate for what SAP doesn't show them.
- Finance builds a separate costing model to understand the financial drag of backlog.
- Operations discovers bottlenecks when it's too late.
- Leadership makes decisions based on last week's data, not today's reality.

This is reactive firefighting, not proactive capacity management.

What if instead, we built you a system that:
1. Shows every open order, its promised date, its current status, and its risk score
2. Connects that backlog to your production capacity and shows you which work center is constraining which orders
3. Calculates the financial impact of that constraint in real-time (cost of delay, OT premiums, supplier penalties)
4. Lets you simulate what-if scenarios (add a shift, expedite a supplier, change production sequence) to see impact on delivery and margin
5. Sends exceptions to management when an order moves from 'manageable' to 'at-risk'

That's not a report. That's a management cockpit. It's what SAP's ePPDS and Capacity Requirement Planning (CRP) do in world-class enterprises. We deliver the foundational reports in Phase 1, and scale seamlessly into the cockpit." """
    set_speaker_notes(s3, s3_notes)

    # =============================================================
    # SLIDE 4: The Business Value Shift
    # =============================================================
    s4 = add_base_slide(is_dark=False)
    add_header(s4, "Moving from Reactive Crisis Management to Proactive Capacity Intelligence", "OPERATIONAL TRANSFORMATION & ROI")
    
    # Top Left: Reactive Cycle (Red)
    rc_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.35), Inches(5.75), Inches(2.25))
    rc_card.fill.solid()
    rc_card.fill.fore_color.rgb = RED_LIGHT_BG
    rc_card.line.color.rgb = CRIMSON_RED
    rc_card.line.width = Pt(1.2)
    
    tf_rc = rc_card.text_frame
    tf_rc.word_wrap = True
    tf_rc.margin_left = tf_rc.margin_top = Inches(0.15)
    p = tf_rc.paragraphs[0]
    p.text = "CURRENT: REACTIVE CYCLE (25+ DAY LAG TO CRISIS)"
    p.font.name = "Arial"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = CRIMSON_RED
    
    r_steps = [
        "Day 1: Order entered into SAP without forward capacity bottleneck check.",
        "Day 15: Planners spot backlog spike manually in Excel sheet during weekly review.",
        "Day 20: Work center bottleneck hit on shop floor; parts halted.",
        "Day 25: Customer escalates impending late delivery; emergency standup called.",
        "Day 28: Crisis firefighting: expensive weekend OT & airfreight premiums paid.",
        "Day 30: Delivery delayed by 3-5 days; contract penalties absorbed & margin eroded."
    ]
    for st in r_steps:
        p = tf_rc.add_paragraph()
        p.space_before = Pt(2)
        p.text = "• " + st
        p.font.size = Pt(8)
        p.font.color.rgb = TEXT_DARK

    # Top Right: Proactive Cycle (Green)
    pc_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.78), Inches(1.35), Inches(5.75), Inches(2.25))
    pc_card.fill.solid()
    pc_card.fill.fore_color.rgb = GREEN_LIGHT_BG
    pc_card.line.color.rgb = EMERALD_GREEN
    pc_card.line.width = Pt(1.2)
    
    tf_pc = pc_card.text_frame
    tf_pc.word_wrap = True
    tf_pc.margin_left = tf_pc.margin_top = Inches(0.15)
    p = tf_pc.paragraphs[0]
    p.text = "FUTURE: PROACTIVE CAPACITY INTELLIGENCE (1-2 DAY DETECTION)"
    p.font.name = "Arial"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_GREEN
    
    p_steps = [
        "Day 1: Order entered; automated logic evaluates buffer health & flags work center load.",
        "Day 2: Planner cockpit highlights yellow risk: CNC load at 115% in Week 4 ($45K risk).",
        "Day 3: Simulation engine compares 3 options (shift add vs vendor expedite vs sequence).",
        "Day 5: Cost-optimal decision approved (planned OT at $8.5K saves $17K execution drag).",
        "Day 15-20: Smooth shop execution without bottleneck surprises or rework chaos.",
        "Day 25: 100% on-time delivery achieved, full customer trust & target margin protected."
    ]
    for st in p_steps:
        p = tf_pc.add_paragraph()
        p.space_before = Pt(2)
        p.text = "• " + st
        p.font.size = Pt(8)
        p.font.color.rgb = TEXT_DARK

    # Bottom Split: KPI Table (Left 70%) & ROI Callout (Right 30%)
    table_kpi = s4.shapes.add_table(8, 4, Inches(0.8), Inches(3.75), Inches(8.3), Inches(3.1))
    tk = table_kpi.table
    tk.columns[0].width = Inches(2.2)
    tk.columns[1].width = Inches(1.8)
    tk.columns[2].width = Inches(1.8)
    tk.columns[3].width = Inches(2.5)
    
    k_headers = ["Metric / Dimension", "Current State", "Future Target", "Value Driver"]
    for col_idx, h in enumerate(k_headers):
        cell = tk.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_CARD
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(8.5)
        p.font.color.rgb = WHITE
        
    kpi_rows = [
        ("Backlog Detection Lag", "15–20 days", "1–2 days", "Automated SAP feed vs Excel"),
        ("On-Time Delivery Rate", "94–96%", "98%+", "Proactive buffer & capacity control"),
        ("Average Delay (Late Orders)", "3–5 days", "0–1 day", "Early resolution of bottlenecks"),
        ("Excess Overtime Spend", "$250K–$400K / yr", "$80K–$120K / yr", "Planned shifts vs reactive crisis OT"),
        ("Customer Escalations", "8–12 / month", "1–2 / month", "Predictable schedules & alerts"),
        ("Finance Variance Chasing", "40 hrs / month", "10 hrs / month", "Automated cost drag analytics"),
        ("Working Capital Freed", "Inflated inventory", "$100K–$300K freed", "Faster throughput & lower WIP")
    ]
    for r_idx, r in enumerate(kpi_rows):
        for c_idx, val in enumerate(r):
            cell = tk.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = GREEN_LIGHT_BG if c_idx == 2 else (WHITE if r_idx % 2 == 0 else CARD_BG_MUTED)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8)
            p.font.bold = (c_idx == 0 or c_idx == 2)
            p.font.color.rgb = EMERALD_GREEN if c_idx == 2 else TEXT_DARK

    # ROI Summary Card (Right 30%)
    roi_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.3), Inches(3.75), Inches(3.233), Inches(3.1))
    roi_card.fill.solid()
    roi_card.fill.fore_color.rgb = DARK_CARD
    roi_card.line.color.rgb = GOLD_ACCENT
    roi_card.line.width = Pt(1.5)
    
    tf_roi = roi_card.text_frame
    tf_roi.word_wrap = True
    tf_roi.margin_left = tf_roi.margin_top = Inches(0.18)
    p = tf_roi.paragraphs[0]
    p.text = "QUANTIFIED FIRST-YEAR BENEFIT"
    p.font.name = "Arial"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    
    p2 = tf_roi.add_paragraph()
    p2.space_before = Pt(6)
    p2.text = "$450K – $1.1M"
    p2.font.name = "Arial"
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_LIGHT
    
    roi_bullets = [
        "Overtime & Freight Recovery: $150K–$280K",
        "OTD Customer Retention: $200K–$500K",
        "Working Capital Release: $100K–$300K",
        "Planning Labor Reclaimed: 50–80 hrs/mo",
        "Expected Payback Period: 6–12 Months",
        "100% Founded on Existing SAP Data"
    ]
    for b in roi_bullets:
        p = tf_roi.add_paragraph()
        p.space_before = Pt(3)
        p.text = "✓ " + b
        p.font.size = Pt(8)
        p.font.color.rgb = CYAN_ACCENT

    add_footer(s4, 4)
    
    s4_notes = """SPEAKER NOTES:
"Let's talk about what this transformation is actually worth.

Today, your operation is optimized for reactive response. When a work center starts getting backed up, someone notices late—in a standup or an escalation call. Then costs spike: unplanned overtime, expedited freight, margin erosion.

Here is what's happening financially:
- You are spending $250K–$400K/year on unplanned overtime.
- Delayed orders erode 2–4% of gross margin through concessions and penalties.
- Your finance team spends 40+ hours/month chasing variance explanations instead of driving strategic decisions.

Now imagine the proactive world:
On Day 1, an order enters SAP. The system immediately checks current backlog and finite capacity load. If there is a bottleneck, it flags it within hours, not weeks.
The planner sees the root cause: CNC Work Center AB100 is at 115% in Week 4, threatening $45K of delay cost. They evaluate 3 clear options and make the economically optimal choice.

The result is $450K to $1.1M in first-year financial impact, with a 6 to 12 month payback period." """
    set_speaker_notes(s4, s4_notes)

    # =============================================================
    # SLIDE 5: Module 1 — Backlog Management Report
    # =============================================================
    s5 = add_base_slide(is_dark=False)
    add_header(s5, "Module 1: The 'Order Risk & Pipeline' Intelligence Layer", "MODULE 1: BACKLOG INTELLIGENCE", "Connecting Order Attributes, Aging Status, and Capacity Risk Flags to Drive Execution")
    
    # 3 Attribute Breakdown Columns
    attr_cols = [
        ("1. Order-Level Attributes (SD/PP)", SAP_BLUE, [
            "Order Number & Line Item (VBAK/VBAP)",
            "Customer Name & Strategic Tier (KNA1)",
            "Promised Delivery Date (VDDAT)",
            "Order Type: MTO, MTS, Subcontract",
            "Order Value & Standard Margin %",
            "Order State: Planned, Released, In-Progress"
        ]),
        ("2. Backlog-Level Attributes (Buffer & Aging)", GOLD_ACCENT, [
            "Days in Backlog (TODAY - ERDAT)",
            "Days Until Promise (VDDAT - TODAY)",
            "Buffer Health: Green (>5d), Yellow (2-5d), Red (<2d)",
            "Backlog Priority Sequence Rank",
            "Component Material Readiness (MSEG/MIGO)",
            "Quality Gate Status: FAI, SPC, Hold"
        ]),
        ("3. Production-Level Attributes (Capacity)", PURPLE_ACCENT, [
            "Operations Completed % (AUFM / AFVU)",
            "Identified Bottleneck Work Center (CRHD)",
            "Capacity Constraint Flag: YES / NO",
            "Supplier Dependency Flag (Open POs)",
            "Cumulative Setup & Rework Hours Absorbed",
            "Recommended Execution Action"
        ])
    ]
    
    w_c = 3.75
    for i, (title, color_b, items) in enumerate(attr_cols):
        x = 0.8 + i * (w_c + 0.24)
        c_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.45), Inches(w_c), Inches(1.85))
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = CARD_BG
        c_box.line.color.rgb = color_b
        c_box.line.width = Pt(1.2)
        
        tf_cb = c_box.text_frame
        tf_cb.word_wrap = True
        tf_cb.margin_left = tf_cb.margin_top = Inches(0.12)
        p = tf_cb.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = color_b
        
        for item in items:
            p = tf_cb.add_paragraph()
            p.space_before = Pt(2)
            p.text = "• " + item
            p.font.size = Pt(8)
            p.font.color.rgb = TEXT_DARK

    # Middle Banner: Risk Scoring Logic
    risk_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.4), Inches(11.733), Inches(0.85))
    risk_box.fill.solid()
    risk_box.fill.fore_color.rgb = CARD_BG_MUTED
    risk_box.line.color.rgb = CARD_BORDER
    risk_box.line.width = Pt(1)
    
    tf_rb = risk_box.text_frame
    tf_rb.word_wrap = True
    tf_rb.margin_left = tf_rb.margin_top = Inches(0.12)
    p = tf_rb.paragraphs[0]
    p.text = "DYNAMIC RISK SCORING ENGINE (1–10 INDEX)"
    p.font.name = "Arial"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = SAP_BLUE
    
    p2 = tf_rb.add_paragraph()
    p2.space_before = Pt(2)
    p2.text = "• GREEN (Score 1-4): Buffer >5 days AND No work center constraint AND 100% material ready → Action: Standard monitoring.\n• YELLOW (Score 5-7): Buffer 2-5 days OR capacity constraint active OR minor supplier delay → Action: Review sequence & buffer.\n• RED (Score 8-10): Buffer <2 days OR bottleneck load >100% OR QA hold → Action: Immediate escalation (add shift, expedite, negotiate)."
    p2.font.size = Pt(8)
    p2.font.color.rgb = TEXT_DARK

    # Bottom Sample Backlog Report Table
    tbl_s5 = s5.shapes.add_table(5, 9, Inches(0.8), Inches(4.35), Inches(11.733), Inches(2.55))
    t5 = tbl_s5.table
    widths = [Inches(0.6), Inches(1.1), Inches(1.5), Inches(1.1), Inches(0.9), Inches(1.5), Inches(1.1), Inches(1.2), Inches(2.733)]
    for i, w in enumerate(widths):
        t5.columns[i].width = w
        
    s5_headers = ["Risk", "Order #", "Customer", "Promised", "Days Left", "Constraint", "Material", "Cost Impact", "Recommended Action"]
    for col_idx, h in enumerate(s5_headers):
        cell = t5.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_CARD
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(8)
        p.font.color.rgb = WHITE
        
    s5_rows = [
        ("🔴 9", "SO-104921", "Acme Aerospace", "2026-03-02", "2 days", "CNC Work Center AB100", "✓ Ready (100%)", "$24,500", "Authorize Saturday shift to unblock 6 orders"),
        ("🟡 6", "SO-105014", "Boeing Defense", "2026-03-08", "8 days", "Supplier Delay (Part X)", "⚠ Delayed 4d", "$8,200", "Expedite shipment via airfreight ($1.8K cost)"),
        ("🟡 5", "SO-105188", "Hitachi Energy", "2026-03-12", "12 days", "Sheet Metal Line S2", "✓ Ready (100%)", "$4,100", "Re-sequence behind priority batch #4"),
        ("🟢 2", "SO-105340", "Pratt & Whitney", "2026-03-25", "25 days", "None (On Schedule)", "✓ Ready (100%)", "$0", "On track; standard production release")
    ]
    for r_idx, r in enumerate(s5_rows):
        for c_idx, val in enumerate(r):
            cell = t5.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            if "🔴" in r[0]:
                cell.fill.fore_color.rgb = RED_LIGHT_BG
            elif "🟡" in r[0]:
                cell.fill.fore_color.rgb = AMBER_LIGHT_BG
            else:
                cell.fill.fore_color.rgb = GREEN_LIGHT_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8)
            p.font.bold = (c_idx in [0, 1, 7])
            p.font.color.rgb = CRIMSON_RED if c_idx == 7 and "🔴" in r[0] else TEXT_DARK

    add_footer(s5, 5)
    
    s5_notes = """SPEAKER NOTES:
"Let's dive into Module 1: The Backlog Management Report. This is not just a spreadsheet list of orders; it is an order risk management engine.

Here is what we are solving:
Your planners spend hours every week asking: 'Which orders do I need to worry about, and why?' That question should be answered automatically by a system.

We organize the backlog into three layers:
Layer 1 is Order Identity: What is this order? Who is the customer? What did we promise?
Layer 2 is Backlog Aging and Buffer: How long has it been sitting? How much buffer remains?
Layer 3 is Constraint Visibility: What is actually blocking it? A CNC machine? A supplier delay? A quality inspection hold?

These layers feed our dynamic Risk Scoring Engine. Red orders don't just show a problem—they display a recommended action:
- 'Authorize Saturday shift to unblock CNC Work Center AB100'
- 'Expedite vendor shipment via airfreight'
- 'Negotiate 2-day customer extension'

The planner is no longer guessing. They are executing data-backed decisions." """
    set_speaker_notes(s5, s5_notes)

    # =============================================================
    # SLIDE 6: Module 2 — Costing Report & Backlog Financial Impact
    # =============================================================
    s6 = add_base_slide(is_dark=False)
    add_header(s6, "Module 2: The 'Capacity-Finance Bridge' Intelligence Layer", "MODULE 2: FINANCIAL IMPACT & COSTING", "Connecting Backlog Depth, Capacity Constraints, and Execution Cost to Drive Economic Decisions")
    
    # Top 3 Cost Anatomy Columns
    c_anatomy = [
        ("Column 1: Standard Cost (Quoted)", SAP_BLUE, [
            "Bill of Materials (BOM) Standard Material",
            "Direct Standard Labor Hours × Rate",
            "Standard Factory Burden / Overhead %",
            "Baseline Target: $1,000 / Unit",
            "Source: SAP COPC / Material Master"
        ]),
        ("Column 2: Execution Premiums (Actual)", GOLD_ACCENT, [
            "+ Unplanned Overtime & Shift Premiums",
            "+ Expedited Supplier Freight & Rush Fees",
            "+ Machine Setup Waste from Line Shuffling",
            "+ Rework & Quality Gate Absorption",
            "Execution Premium: +$190 / Unit"
        ]),
        ("Column 3: Backlog Drag Cost (Age)", CRIMSON_RED, [
            "+ Daily Holding & WIP Financing Cost",
            "+ Contractual Customer Delay Penalties",
            "+ Capacity Lockout (Opportunity Cost)",
            "Backlog Aging Drag: +$300 / Unit",
            "TRUE UNIT COST: $1,490 (49% Margin Erosion!)"
        ])
    ]
    w_a = 3.75
    for i, (title, color_c, items) in enumerate(c_anatomy):
        x = 0.8 + i * (w_a + 0.24)
        a_box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.45), Inches(w_a), Inches(1.6))
        a_box.fill.solid()
        a_box.fill.fore_color.rgb = CARD_BG
        a_box.line.color.rgb = color_c
        a_box.line.width = Pt(1.2)
        
        tf_ab = a_box.text_frame
        tf_ab.word_wrap = True
        tf_ab.margin_left = tf_ab.margin_top = Inches(0.12)
        p = tf_ab.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = color_c
        
        for item in items:
            p = tf_ab.add_paragraph()
            p.space_before = Pt(1.5)
            p.text = "• " + item
            p.font.size = Pt(7.5)
            p.font.bold = ("TRUE UNIT COST" in item)
            p.font.color.rgb = CRIMSON_RED if "TRUE UNIT COST" in item else TEXT_DARK

    # Middle Constraint Financial Exposure Table
    s6_mid_title = s6.shapes.add_textbox(Inches(0.8), Inches(3.1), Inches(11.733), Inches(0.25))
    tf_mt = s6_mid_title.text_frame
    tf_mt.margin_left = tf_mt.margin_top = 0
    p = tf_mt.paragraphs[0]
    p.text = "AGGREGATED FINANCIAL EXPOSURE BY CONSTRAINT TYPE"
    p.font.name = "Arial"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = SAP_BLUE
    
    t_fin = s6.shapes.add_table(4, 5, Inches(0.8), Inches(3.4), Inches(11.733), Inches(1.3))
    tf5 = t_fin.table
    w_tf = [Inches(3.3), Inches(1.8), Inches(2.2), Inches(2.2), Inches(2.233)]
    for idx, w in enumerate(w_tf):
        tf5.columns[idx].width = w
        
    f_headers = ["Bottleneck / Constraint Type", "Affected Orders", "Total Backlog Value", "Avg Delay Added", "Est. Execution Drag Cost"]
    for c_idx, h in enumerate(f_headers):
        cell = tf5.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_CARD
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(8)
        p.font.color.rgb = WHITE
        
    f_rows = [
        ("CNC Work Center AB100 Capacity", "15 orders", "$1,450,000", "+8.5 days", "$68,400 (48% of total drag)"),
        ("Supplier Component Delay (XYZ)", "8 orders", "$620,000", "+4.0 days", "$28,500 (20% of total drag)"),
        ("Quality Gate FAI Inspection Hold", "5 orders", "$380,000", "+3.2 days", "$15,200 (11% of total drag)")
    ]
    for r_idx, r in enumerate(f_rows):
        for c_idx, val in enumerate(r):
            cell = tf5.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else CARD_BG_MUTED
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8)
            p.font.bold = (c_idx in [0, 4])
            p.font.color.rgb = CRIMSON_RED if c_idx == 4 else TEXT_DARK

    # Bottom 3 Decision Support Scenario Cards (What-If Analysis)
    scenarios = [
        ("SCENARIO A: Add Saturday Shift (CNC AB100)", GREEN_LIGHT_BG, EMERALD_GREEN, [
            "Action: Schedule 8 hrs Saturday OT for CNC work center.",
            "Cost: $8,500 (OT wages, utilities, supervision).",
            "Impact: Clears 6 critical orders; unblocks $17,040 in delay penalties.",
            "NET FINANCIAL BENEFIT: +$8,540 | Delivery compressed 1.5 days",
            "Decision: HIGH ROI — AUTHORIZE IMMEDIATELY"
        ]),
        ("SCENARIO B: Expedite Supplier (Component XYZ)", RED_LIGHT_BG, CRIMSON_RED, [
            "Action: Pay rush airfreight surcharge on 400 subassemblies.",
            "Cost: $12,000 expedited logistics fees.",
            "Impact: Advances delivery 3 days, avoids $8,200 in holding cost.",
            "NET FINANCIAL BENEFIT: -$3,800 (Net Negative Trade-Off)",
            "Decision: REJECT — Cost exceeds delay penalty recovery"
        ]),
        ("SCENARIO C: Negotiate Customer Promise Extension", AMBER_LIGHT_BG, GOLD_ACCENT, [
            "Action: Proactively request 3-day extension with customer tier-2.",
            "Cost: $0 direct expenditure (relies on customer goodwill).",
            "Impact: Alleviates CNC crunch; eliminates need for Scenario A OT.",
            "NET FINANCIAL BENEFIT: +$8,500 (Overtime Avoided)",
            "Decision: FEASIBLE — Engage account manager for extension"
        ])
    ]
    w_sc = 3.75
    for i, (title, bg_col, border_col, bullets) in enumerate(scenarios):
        x = 0.8 + i * (w_sc + 0.24)
        sc_box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(4.8), Inches(w_sc), Inches(2.1))
        sc_box.fill.solid()
        sc_box.fill.fore_color.rgb = bg_col
        sc_box.line.color.rgb = border_col
        sc_box.line.width = Pt(1.2)
        
        tf_sc = sc_box.text_frame
        tf_sc.word_wrap = True
        tf_sc.margin_left = tf_sc.margin_top = Inches(0.12)
        p = tf_sc.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = border_col
        
        for b in bullets:
            p = tf_sc.add_paragraph()
            p.space_before = Pt(2)
            p.text = "• " + b
            p.font.size = Pt(7.5)
            p.font.bold = ("NET FINANCIAL BENEFIT" in b or "Decision:" in b)
            p.font.color.rgb = border_col if ("NET FINANCIAL BENEFIT" in b or "Decision:" in b) else TEXT_DARK

    add_footer(s6, 6)
    
    s6_notes = """SPEAKER NOTES:
"Now let's talk about money. A backlog report that doesn't connect to financial impact is interesting, but it's not actionable.

Here is the hidden cost structure:
When an order sits in backlog, it forces operational compromises. Standard quoted cost might be $1,000. But if we work emergency weekend shifts, add rush shipping, or shuffle machine setups, execution premiums add $190 per unit.
Add aging drag—working capital lockup, holding costs, customer penalties—and the actual cost climbs to $1,490. You just lost 49% of your gross margin!

The Costing Report aggregates this exposure by bottleneck work center:
- 48% of your current drag is concentrated on CNC Work Center AB100 ($68,400 exposure).

Even more powerful is the Decision Support Simulation:
- Scenario A: Add a Saturday shift. Costs $8,500, but recovers $17,040 in delay drag. Net benefit: +$8,540. A no-brainer.
- Scenario B: Expedite a supplier. Costs $12,000, recovers only $8,200. Net loss: -$3,800. The system tells you NOT to do this.
- Scenario C: Proactively negotiate a promise extension. Saves $8,500 in overtime with zero cash spent.

This shifts management from gut-feel crisis spending to economically optimal decisions." """
    set_speaker_notes(s6, s6_notes)

    # =============================================================
    # SLIDE 7: Conceptual Wireframe & UI Layout
    # =============================================================
    s7 = add_base_slide(is_dark=False)
    add_header(s7, "The Management Cockpit Interface: Where Reports Become Decisions", "CONCEPTUAL UI / UX WIREFRAME", "Phase 1 MVP Interactive Dashboard Mock-up Unifying Backlog, Capacity, and Costing")
    
    # Outer Dashboard Container Frame
    db_frame = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.5))
    db_frame.fill.solid()
    db_frame.fill.fore_color.rgb = CARD_BG
    db_frame.line.color.rgb = DARK_BORDER
    db_frame.line.width = Pt(1.5)
    
    # Dashboard Header Bar
    db_header = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(0.45))
    db_header.fill.solid()
    db_header.fill.fore_color.rgb = DARK_CARD
    db_header.line.fill.background()
    
    tf_dh = db_header.text_frame
    tf_dh.word_wrap = True
    tf_dh.margin_left = Inches(0.15)
    tf_dh.margin_top = Inches(0.08)
    p = tf_dh.paragraphs[0]
    p.text = "LUMBINI ELITE  |  HICAL CAPACITY INTELLIGENCE COCKPIT  •  LIVE SAP FEED (REFRESH: TODAY 14:32)  •  3 AT-RISK ORDERS FLAGGED"
    p.font.name = "Arial"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    # Left Mini Navigation Bar (1.6 inches width)
    nav_box = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.85), Inches(1.8), Inches(5.05))
    nav_box.fill.solid()
    nav_box.fill.fore_color.rgb = CARD_BG_MUTED
    nav_box.line.color.rgb = CARD_BORDER
    nav_box.line.width = Pt(1)
    
    tf_nav = nav_box.text_frame
    tf_nav.word_wrap = True
    tf_nav.margin_left = Inches(0.1)
    tf_nav.margin_top = Inches(0.12)
    nav_links = [
        ("📊 Executive Cockpit", True),
        ("📋 Backlog Pipeline", False),
        ("💰 Costing Drag Engine", False),
        ("⚙ Capacity & Work Centers", False),
        ("🔄 What-If Simulation", False),
        ("-------------------", False),
        ("FILTERS ACTIVE:", True),
        ("• Horizon: Next 30 Days", False),
        ("• Facility: CNC & Winding", False),
        ("• Status: Red & Yellow", False)
    ]
    for idx, (nl, is_b) in enumerate(nav_links):
        p = tf_nav.paragraphs[0] if idx == 0 else tf_nav.add_paragraph()
        p.space_before = Pt(3)
        p.text = nl
        p.font.size = Pt(7.5)
        p.font.bold = is_b
        p.font.color.rgb = SAP_BLUE if is_b else TEXT_DARK

    # Top Area: 4 Metric Cards (Horizontal row, width = 2.25 in each)
    kpis_cockpit = [
        ("Total Open Backlog", "47 Orders", "↑ +3 from yesterday", TEXT_DARK, CARD_BG),
        ("At-Risk Orders (Red)", "12 Orders", "Buffer <2d or Overload", CRIMSON_RED, RED_LIGHT_BG),
        ("Average Backlog Age", "8.3 Days", "↓ -0.5d improvement", GOLD_ACCENT, AMBER_LIGHT_BG),
        ("Financial Drag Exposure", "$1,240,000", "+$180K cost risk", SAP_BLUE, RGBColor(238, 242, 255))
    ]
    for i, (k_title, k_val, k_sub, col_t, bg_t) in enumerate(kpis_cockpit):
        x = 2.75 + i * (2.28 + 0.12)
        c_k = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.95), Inches(2.28), Inches(0.85))
        c_k.fill.solid()
        c_k.fill.fore_color.rgb = bg_t
        c_k.line.color.rgb = CARD_BORDER
        c_k.line.width = Pt(1)
        
        tf_ck = c_k.text_frame
        tf_ck.word_wrap = True
        tf_ck.margin_left = tf_ck.margin_top = Inches(0.08)
        p = tf_ck.paragraphs[0]
        p.text = k_title.upper()
        p.font.size = Pt(7)
        p.font.bold = True
        p.font.color.rgb = TEXT_MUTED
        
        p2 = tf_ck.add_paragraph()
        p2.text = k_val
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = col_t
        
        p3 = tf_ck.add_paragraph()
        p3.text = k_sub
        p3.font.size = Pt(6.5)
        p3.font.color.rgb = TEXT_MUTED

    # Middle Area Split:
    # Left: Constraint Heatmap Bar Chart Mockup (width = 4.2 in)
    ch_box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.75), Inches(2.9), Inches(4.5), Inches(1.8))
    ch_box.fill.solid()
    ch_box.fill.fore_color.rgb = CARD_BG
    ch_box.line.color.rgb = CARD_BORDER
    ch_box.line.width = Pt(1)
    
    tf_ch = ch_box.text_frame
    tf_ch.word_wrap = True
    tf_ch.margin_left = tf_ch.margin_top = Inches(0.1)
    p = tf_ch.paragraphs[0]
    p.text = "WORK CENTER CONSTRAINT HEATMAP"
    p.font.size = Pt(8)
    p.font.bold = True
    p.font.color.rgb = SAP_BLUE
    
    bars = [
        ("CNC Work Center AB100 (115% Load)", 15, "████████████████", CRIMSON_RED),
        ("Sequence & Setup Contention", 19, "████████████", GOLD_ACCENT),
        ("Supplier Part XYZ Shortage", 8, "██████", SAP_BLUE),
        ("Quality Gate FAI Inspection Hold", 5, "████", EMERALD_GREEN)
    ]
    for b_title, cnt, bar_str, col_bar in bars:
        p = tf_ch.add_paragraph()
        p.space_before = Pt(2)
        p.text = f"{b_title} ({cnt} orders)\n{bar_str}"
        p.font.size = Pt(7)
        p.font.color.rgb = col_bar

    # Right: Live Order Exception Stream (width = 4.8 in)
    oe_box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.35), Inches(2.9), Inches(5.083), Inches(1.8))
    oe_box.fill.solid()
    oe_box.fill.fore_color.rgb = CARD_BG
    oe_box.line.color.rgb = CARD_BORDER
    oe_box.line.width = Pt(1)
    
    tf_oe = oe_box.text_frame
    tf_oe.word_wrap = True
    tf_oe.margin_left = tf_oe.margin_top = Inches(0.1)
    p = tf_oe.paragraphs[0]
    p.text = "LIVE EXCEPTION QUEUE (TOP RED & YELLOW ORDERS)"
    p.font.size = Pt(8)
    p.font.bold = True
    p.font.color.rgb = SAP_BLUE
    
    ex_items = [
        "🔴 SO-104921 | Acme Corp | Due in 2d | Blocked: CNC AB100 ($24.5K Drag) [ACTION: Add Shift]",
        "🟡 SO-105014 | Boeing | Due in 8d | Blocked: Supplier XYZ ($8.2K Drag) [ACTION: Airfreight]",
        "🟡 SO-105188 | Hitachi | Due in 12d | Blocked: Sheet Metal Line ($4.1K Drag) [ACTION: Sequence]",
        "✓ SO-104880 | Pratt & Whitney | Completed 1d early | Cost Drag Saved: +$11,400"
    ]
    for ex in ex_items:
        p = tf_oe.add_paragraph()
        p.space_before = Pt(2)
        p.text = ex
        p.font.size = Pt(7)
        p.font.color.rgb = TEXT_DARK

    # Bottom Area: Interactive Simulation Engine Bar (width = 9.68 in)
    sim_bar = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.75), Inches(4.8), Inches(9.683), Inches(2.0))
    sim_bar.fill.solid()
    sim_bar.fill.fore_color.rgb = RGBColor(245, 243, 255)
    sim_bar.line.color.rgb = PURPLE_ACCENT
    sim_bar.line.width = Pt(1.2)
    
    tf_sb = sim_bar.text_frame
    tf_sb.word_wrap = True
    tf_sb.margin_left = tf_sb.margin_top = Inches(0.12)
    p = tf_sb.paragraphs[0]
    p.text = "WHAT-IF SIMULATION ENGINE (SCENARIO MODELING & ROI PREDICTION)"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = PURPLE_ACCENT
    
    p2 = tf_sb.add_paragraph()
    p2.space_before = Pt(3)
    p2.text = "• Scenario Selected: Schedule Saturday Shift (+8 hrs capacity on CNC AB100)\n  → Recalculation: Load drops from 115% to 88% | 6 Red orders unblocked | Net Savings: +$8,540 | Timeline compressed 1.5 days\n• One-Click Action: [EXECUTE SHIFT SCHEDULE]  [PUSH REVISED SAP ROUTING]  [NOTIFY PRODUCTION MANAGER]\n• Mobile Alert Rule: Push automated SMS/Email alert to VP Operations if any Tier-1 order hits Red buffer (<2 days)."
    p2.font.size = Pt(7.5)
    p2.font.color.rgb = TEXT_DARK

    add_footer(s7, 7)
    
    s7_notes = """SPEAKER NOTES:
"This is what the Phase 1 Management Cockpit looks like. It is built in Tableau, pulling live data from SAP HANA every 4 hours.

Let me walk you through the four key zones:
Zone 1 at the top gives leadership the pulse of operations in 3 seconds: total open orders, how many are at-risk, backlog aging, and total dollar exposure.
Zone 2 is the Constraint Heatmap. It shows exactly which work centers are choking production right now.
Zone 3 is the Live Exception Queue. It ranks every at-risk order, shows the root cause, and provides a direct recommended action.
Zone 4 is the What-If Simulation Engine. Planners can test operational adjustments—like scheduling a Saturday shift—and see immediate financial and timeline consequences before committing company capital.

Every element is clickable, fully drillable down to the underlying SAP production order, and accessible on desktop or mobile." """
    set_speaker_notes(s7, s7_notes)

    # =============================================================
    # SLIDE 8: Underlying Business Logic & SAP Data Mapping
    # =============================================================
    s8 = add_base_slide(is_dark=False)
    add_header(s8, "The Engine Behind the Cockpit: Business Rules & SAP Integration", "TECHNICAL ARCHITECTURE & DATA ENGINE", "Transparent Three-Tier Architecture Translating Raw SAP Tables into Calculated Executive Insights")
    
    # 3 Architectural Tier Rows
    # Tier 1: Business Questions & KPIs (Top)
    t1_box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(1.3))
    t1_box.fill.solid()
    t1_box.fill.fore_color.rgb = CARD_BG
    t1_box.line.color.rgb = SAP_BLUE
    t1_box.line.width = Pt(1.2)
    
    tf_t1 = t1_box.text_frame
    tf_t1.word_wrap = True
    tf_t1.margin_left = tf_t1.margin_top = Inches(0.12)
    p = tf_t1.paragraphs[0]
    p.text = "TIER 1: STRATEGIC BUSINESS QUESTIONS → MEASURABLE METRICS"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = SAP_BLUE
    
    t1_items = [
        ("Which orders are at-risk of late delivery?", "Risk Score (1-10) = Weighted formula of Buffer Days + Work Center Load + Material Ready."),
        ("Where are my critical bottlenecks?", "Constraint Flag = SUM(RESB Operation Hours) / CRHD Work Center Available Capacity > 100%."),
        ("What is backlog costing us financially?", "Total Drag = (Order Value × Margin Drag %) + (Backlog Age × Daily Holding Cost) + Premium OT."),
        ("What unblocks if we add capacity?", "Simulation Engine = Re-routes order sequence against +8 hrs CRHD capacity, recalculating margin.")
    ]
    for q, a in t1_items:
        p = tf_t1.add_paragraph()
        p.space_before = Pt(2)
        r1 = p.add_run()
        r1.text = "• " + q + " → "
        r1.font.bold = True
        r1.font.size = Pt(7.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = a
        r2.font.bold = False
        r2.font.size = Pt(7.5)
        r2.font.color.rgb = TEXT_MUTED

    # Tier 2: SAP Module & Table Mapping (Middle)
    t2_box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.8), Inches(11.733), Inches(2.3))
    t2_box.fill.solid()
    t2_box.fill.fore_color.rgb = CARD_BG
    t2_box.line.color.rgb = GOLD_ACCENT
    t2_box.line.width = Pt(1.2)
    
    tf_t2 = t2_box.text_frame
    tf_t2.word_wrap = True
    tf_t2.margin_left = tf_t2.margin_top = Inches(0.12)
    p = tf_t2.paragraphs[0]
    p.text = "TIER 2: SAP DATA OBJECT MAPPING & TRANSFORMATION PIPELINE"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    
    sap_mappings = [
        ("Sales & Demand (SD):", "VBAK (Order Header), VBAP (Line Items), VBEP (Delivery Schedule) → Pulls promised date (VDDAT), order net value (NETWR), and customer tier."),
        ("Production Planning (PP):", "AFPO / AFKO (Production Orders), AUFM (Operation Confirmations), RESB (Reservations) → Tracks % completion and material component allocation."),
        ("Capacity Management (CR):", "CRHD (Work Center Header), PLKO / PLKP (Routing Plans) → Extracts work center maximum daily hours vs scheduled load to pinpoint bottlenecks."),
        ("Materials Management (MM):", "MARA / MARC (Material Master), MSEG / MIGO (Goods Movements), EKKO / EKPO (Purchasing) → Detects part shortages and supplier receipt dates."),
        ("Costing & Finance (CO/FI):", "COPC (Cost Component Split), AFVC (Operation Costs), General Ledger → Computes baseline BOM standard cost vs overtime variance.")
    ]
    for mod, desc in sap_mappings:
        p = tf_t2.add_paragraph()
        p.space_before = Pt(2.5)
        r1 = p.add_run()
        r1.text = "• " + mod + " "
        r1.font.bold = True
        r1.font.size = Pt(7.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = desc
        r2.font.bold = False
        r2.font.size = Pt(7.5)
        r2.font.color.rgb = TEXT_MUTED

    # Tier 3: Technical Execution & Governance (Bottom)
    t3_box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.2), Inches(11.733), Inches(1.65))
    t3_box.fill.solid()
    t3_box.fill.fore_color.rgb = CARD_BG_MUTED
    t3_box.line.color.rgb = CARD_BORDER
    t3_box.line.width = Pt(1)
    
    tf_t3 = t3_box.text_frame
    tf_t3.word_wrap = True
    tf_t3.margin_left = tf_t3.margin_top = Inches(0.12)
    p = tf_t3.paragraphs[0]
    p.text = "TIER 3: DATA REFRESH, INTEGRITY & AUDIT GOVERNANCE"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = SAP_BLUE
    
    gov_items = [
        "Automated Refresh Cadence: Live data extracted from SAP HANA every 4 hours via read-only queries with zero operational slowdown.",
        "Full Traceability & Audit: Every KPI, risk score, and drag estimate is click-traceable back to individual SAP document numbers.",
        "Embedded Logic Transparency: Business calculation rules are documented in Tableau metadata and can be tuned dynamically by HICAL leadership.",
        "Data Quality Verification: Discovery phase includes automated pre-flight reconciliation against existing manual spreadsheets to guarantee 100% precision."
    ]
    for gi in gov_items:
        p = tf_t3.add_paragraph()
        p.space_before = Pt(2)
        p.text = "✓ " + gi
        p.font.size = Pt(7.5)
        p.font.color.rgb = TEXT_DARK

    add_footer(s8, 8)
    
    s8_notes = """SPEAKER NOTES:
"Let's look under the hood. The cockpit isn't magic; it is systematic and auditable. Every metric displayed comes from a transparent business rule grounded in active SAP tables.

In Tier 1, we translate leadership's core operational questions into strict mathematical formulas.
In Tier 2, we tap into your existing SAP HANA environment:
- Sales dates come directly from VBAK and VBAP.
- Routing and operation progress come from AFPO and AUFM.
- Work center capacity limits come from CRHD.
- Component availability is pulled live from MM and MSEG.
- Cost benchmarks come from COPC.

In Tier 3, we govern data integrity. The pipeline runs automated 4-hour extracts using read-only service accounts. Every number can be audited down to the specific SAP production order.

Most importantly, you validate these rules with us upfront during discovery. If your threshold for a constrained machine is 85% instead of 100%, we tune the logic accordingly." """
    set_speaker_notes(s8, s8_notes)

    # =============================================================
    # SLIDE 9: Phased Implementation Roadmap
    # =============================================================
    s9 = add_base_slide(is_dark=False)
    add_header(s9, "From MVP to World-Class ePPDS: A Phased Delivery Strategy", "DELIVERY STRATEGY & ROADMAP", "Low-Risk, Value-Driven Roadmap: Phase 1 MVP (Weeks 1–12) → Phase 2 Cockpit (Weeks 12–24) → Phase 3 ePPDS (Weeks 24+)")
    
    # 3 Phased Capability Columns
    phases = [
        ("PHASE 1: FOUNDATIONAL MVP", "WEEKS 1 – 12", EMERALD_GREEN, GREEN_LIGHT_BG, [
            "Live Backlog Report with risk scoring",
            "Costing Report with backlog drag metrics",
            "Initial Tableau Dashboard with KPI cards",
            "Automated 4-hour SAP HANA extraction",
            "Retires manual Excel tracking spreadsheets",
            "Delivers immediate $180K–$400K first-year ROI"
        ]),
        ("PHASE 2: MANAGEMENT COCKPIT", "WEEKS 12 – 24", SAP_BLUE, RGBColor(238, 242, 255), [
            "Integrated multi-constraint heatmap",
            "What-If Scenario Simulation engine",
            "Economic trade-off decision modeling",
            "Automated SMS/Email exception alerts",
            "Cross-facility load balancing (Plants A & B)",
            "Unlocks additional $100K–$200K annual value"
        ]),
        ("PHASE 3: SAP ePPDS / CRP", "WEEKS 24+", GOLD_ACCENT, GOLD_LIGHT_BG, [
            "Finite capacity automated scheduling",
            "Predictive ML bottleneck identification",
            "Dynamic automated sequence optimization",
            "Full SAP APO / ePPDS core integration",
            "Supply chain shock & demand sensing",
            "World-class aerospace manufacturing scale"
        ])
    ]
    w_ph = 3.75
    for i, (p_title, p_time, col_ph, bg_ph, bullets) in enumerate(phases):
        x = 0.8 + i * (w_ph + 0.24)
        box_p = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.45), Inches(w_ph), Inches(2.25))
        box_p.fill.solid()
        box_p.fill.fore_color.rgb = bg_ph
        box_p.line.color.rgb = col_ph
        box_p.line.width = Pt(1.5)
        
        tf_p = box_p.text_frame
        tf_p.word_wrap = True
        tf_p.margin_left = tf_p.margin_top = Inches(0.12)
        p = tf_p.paragraphs[0]
        p.text = p_title
        p.font.name = "Arial"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = col_ph
        
        p_sub = tf_p.add_paragraph()
        p_sub.text = p_time
        p_sub.font.size = Pt(8)
        p_sub.font.bold = True
        p_sub.font.color.rgb = TEXT_MUTED
        
        for b in bullets:
            p = tf_p.add_paragraph()
            p.space_before = Pt(2.5)
            p.text = "✓ " + b
            p.font.size = Pt(7.5)
            p.font.color.rgb = TEXT_DARK

    # Bottom Area Split:
    # Left: Phase 1 Detailed 12-Week Sprint Timeline (width = 7.5 in)
    s1_box = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.85), Inches(7.6), Inches(3.0))
    s1_box.fill.solid()
    s1_box.fill.fore_color.rgb = CARD_BG
    s1_box.line.color.rgb = CARD_BORDER
    s1_box.line.width = Pt(1)
    
    tf_s1 = s1_box.text_frame
    tf_s1.word_wrap = True
    tf_s1.margin_left = tf_s1.margin_top = Inches(0.15)
    p = tf_s1.paragraphs[0]
    p.text = "PHASE 1 DETAILED 12-WEEK SPRINT EXECUTION"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = SAP_BLUE
    
    sprints = [
        ("Weeks 1–2: Discovery & Requirements", "Conduct stakeholder workshops (Sales, Planning, Operations, Finance); audit SAP table access & data cleanliness; document custom business rules."),
        ("Weeks 3–4: Architecture & Design Sign-off", "Finalize Tableau UI wireframes, risk scoring formulas, and cost drag logic; obtain executive sign-off from CFO and VP Operations."),
        ("Weeks 5–7: SAP Integration & Data Pipeline Build", "Deploy automated read-only SQL/HANA queries; code data transformation models; build live Tableau data sources and calculations."),
        ("Weeks 8–10: User Acceptance Testing (UAT)", "Execute parallel test runs against manual spreadsheets; validate risk scores and financial estimates with shop floor planners; tune UI."),
        ("Weeks 11–12: Deployment, Training & Go-Live", "Production cutover; deliver role-based user training for 50+ staff; establish support SLAs; officially retire manual backlog spreadsheets.")
    ]
    for s_title, s_desc in sprints:
        p = tf_s1.add_paragraph()
        p.space_before = Pt(3)
        r1 = p.add_run()
        r1.text = "• " + s_title + ": "
        r1.font.bold = True
        r1.font.size = Pt(7.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = s_desc
        r2.font.bold = False
        r2.font.size = Pt(7)
        r2.font.color.rgb = TEXT_MUTED

    # Right: Investment, ROI & Risk Mitigation Box (width = 3.9 in)
    inv_box = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(3.85), Inches(3.933), Inches(3.0))
    inv_box.fill.solid()
    inv_box.fill.fore_color.rgb = DARK_CARD
    inv_box.line.color.rgb = GOLD_ACCENT
    inv_box.line.width = Pt(1.5)
    
    tf_inv = inv_box.text_frame
    tf_inv.word_wrap = True
    tf_inv.margin_left = tf_inv.margin_top = Inches(0.15)
    p = tf_inv.paragraphs[0]
    p.text = "INVESTMENT, GOVERNANCE & RISK MITIGATION"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    
    inv_items = [
        ("Project Investment:", " $60K–$85K (Fixed-scope delivery, consulting, configuration & enablement)."),
        ("Team Commitment:", " 3–4 HICAL champions allocated at 40% time for discovery and UAT."),
        ("First-Year Value:", " $180K–$400K direct net operational and overtime recovery."),
        ("Payback Horizon:", " 4–6 months from production go-live."),
        ("Data Quality Risk:", " Mitigated by automated pre-flight audit during Weeks 1-2."),
        ("Adoption Risk:", " Super-user champions trained per facility with daily usage metrics tracked.")
    ]
    for title, desc in inv_items:
        p = tf_inv.add_paragraph()
        p.space_before = Pt(3)
        r1 = p.add_run()
        r1.text = "• " + title
        r1.font.bold = True
        r1.font.size = Pt(7.5)
        r1.font.color.rgb = CYAN_ACCENT
        r2 = p.add_run()
        r2.text = desc
        r2.font.bold = False
        r2.font.size = Pt(7.5)
        r2.font.color.rgb = TEXT_LIGHT

    add_footer(s9, 9)
    
    s9_notes = """SPEAKER NOTES:
"Let's talk execution strategy. We don't try to boil the ocean on day one. We take a disciplined, phased approach that derisks delivery while generating immediate ROI.

Phase 1 is your 12-week MVP. It delivers the live Backlog Report, the Costing Report, and the foundational Tableau dashboard. It retires manual spreadsheets and delivers a proven $180K to $400K first-year benefit. That alone pays for the project within 4 to 6 months.

Phase 2 builds upon clean Phase 1 data, adding cross-facility load balancing, what-if scenario simulations, and automated mobile alerts.

Phase 3 is the long-term strategic vision: full finite capacity scheduling with SAP ePPDS and machine learning constraint forecasting.

Notice that each phase is self-funding and self-contained. Phase 1 delivers complete value even if you pause before Phase 2. To hit the 12-week Phase 1 target, we require 3 to 4 HICAL resources allocated at roughly 40% time during discovery and testing." """
    set_speaker_notes(s9, s9_notes)

    # =============================================================
    # SLIDE 10: Critical Discovery Questions for HICAL
    # =============================================================
    s10 = add_base_slide(is_dark=False)
    add_header(s10, "The Critical Discovery Questions: Inputs Required for Design", "STAKEHOLDER DISCOVERY FRAMEWORK", "30+ Operational, Financial, and Technical Clarifications to Tailor the Solution to HICAL's Reality")
    
    # 2 Wide Columns of Questions
    # Left Column: Operational & Manufacturing (width = 5.75 in)
    op_box = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.45), Inches(5.75), Inches(4.35))
    op_box.fill.solid()
    op_box.fill.fore_color.rgb = CARD_BG
    op_box.line.color.rgb = SAP_BLUE
    op_box.line.width = Pt(1.2)
    
    tf_op = op_box.text_frame
    tf_op.word_wrap = True
    tf_op.margin_left = tf_op.margin_top = Inches(0.15)
    p = tf_op.paragraphs[0]
    p.text = "OPERATIONAL & MANUFACTURING DISCOVERY"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = SAP_BLUE
    
    op_qs = [
        ("SECTION 1: ORDER & BACKLOG DEFINITION", [
            "Q1.1: What is HICAL's precise definition of backlog? (All open orders, released only, or <X days?)",
            "Q1.2: What is your current average backlog depth (# of orders and $ total exposure)?",
            "Q1.3: What is the split between Make-to-Order (MTO) and Make-to-Stock (MTS)?",
            "Q1.4: Are there contractual customer delivery penalty clauses in defense accounts?"
        ]),
        ("SECTION 2: CAPACITY & BOTTLENECK IDENTIFICATION", [
            "Q2.1: What are your top 3–5 recurring bottleneck work centers (e.g., CNC, winding, sheet metal)?",
            "Q2.2: How is machine capacity tracked today in SAP (CRHD shift-based or static)?",
            "Q2.3: What is your flexibility to schedule weekend overtime or second/third shifts?",
            "Q2.4: What % of precision fabrication is subcontracted, and what are vendor lead times?"
        ]),
        ("SECTION 3: QUALITY GATES & SUPPLY CHAIN RISK", [
            "Q3.1: Which specific quality gates delay release (First Article Inspection FAI, customer SPC)?",
            "Q3.2: How frequently do component supplier delivery delays cause shop floor rescheduling?"
        ])
    ]
    for sec_title, q_list in op_qs:
        p = tf_op.add_paragraph()
        p.space_before = Pt(4)
        p.text = sec_title
        p.font.size = Pt(7.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK
        for q in q_list:
            p2 = tf_op.add_paragraph()
            p2.space_before = Pt(1.5)
            p2.text = "☐ " + q
            p2.font.size = Pt(7)
            p2.font.color.rgb = TEXT_MUTED

    # Right Column: Financial, Technical & Governance (width = 5.75 in)
    fn_box = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.78), Inches(1.45), Inches(5.75), Inches(4.35))
    fn_box.fill.solid()
    fn_box.fill.fore_color.rgb = CARD_BG
    fn_box.line.color.rgb = GOLD_ACCENT
    fn_box.line.width = Pt(1.2)
    
    tf_fn = fn_box.text_frame
    tf_fn.word_wrap = True
    tf_fn.margin_left = tf_fn.margin_top = Inches(0.15)
    p = tf_fn.paragraphs[0]
    p.text = "FINANCIAL, TECHNICAL & GOVERNANCE DISCOVERY"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    
    fn_qs = [
        ("SECTION 4: COSTING & FINANCIAL DRAG", [
            "Q4.1: How is standard product cost calculated today (SAP COPC standard cost roll-up)?",
            "Q4.2: What is your effective overtime wage multiplier (1.5x, 2.0x, shift differentials)?",
            "Q4.3: What annual or daily holding cost rate % is applied to work-in-progress inventory?",
            "Q4.4: What is the estimated business cost of a 1-day delivery delay for a key tier-1 customer?"
        ]),
        ("SECTION 5: PROCESS & TECHNICAL ASSETS", [
            "Q5.1: Exactly who maintains the Excel backlog sheet today, and how many weekly hours are spent?",
            "Q5.2: Are routing plans (PLKO) and work center capacities (CRHD) updated and accurate in SAP?",
            "Q5.3: What is the preferred deployment format (Tableau Server, Cloud, or SAP Analytics Cloud)?"
        ]),
        ("SECTION 6: PROJECT GOVERNANCE & TIMELINE", [
            "Q6.1: Who will serve as executive sponsor and business system owner post go-live?",
            "Q6.2: Is leadership aligned on committing 3–4 staff champions at 40% time for 12 weeks?"
        ])
    ]
    for sec_title, q_list in fn_qs:
        p = tf_fn.add_paragraph()
        p.space_before = Pt(4)
        p.text = sec_title
        p.font.size = Pt(7.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK
        for q in q_list:
            p2 = tf_fn.add_paragraph()
            p2.space_before = Pt(1.5)
            p2.text = "☐ " + q
            p2.font.size = Pt(7)
            p2.font.color.rgb = TEXT_MUTED

    # Bottom Discovery Prioritization Matrix Bar
    m_bar = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.9), Inches(11.733), Inches(0.95))
    m_bar.fill.solid()
    m_bar.fill.fore_color.rgb = CARD_BG_MUTED
    m_bar.line.color.rgb = CARD_BORDER
    m_bar.line.width = Pt(1)
    
    tf_mb = m_bar.text_frame
    tf_mb.word_wrap = True
    tf_mb.margin_left = tf_mb.margin_top = Inches(0.1)
    p = tf_mb.paragraphs[0]
    p.text = "DISCOVERY PRIORITIZATION: TOP 3 QUESTIONS TO RESOLVE FIRST"
    p.font.size = Pt(8)
    p.font.bold = True
    p.font.color.rgb = SAP_BLUE
    
    p2 = tf_mb.add_paragraph()
    p2.space_before = Pt(2)
    p2.text = "1. Q1.1 (Backlog Definition): Directly determines data extraction scope and filter parameters for SAP HANA.\n2. Q2.1 (Bottleneck Work Centers): Identifies which shop floor machines require capacity modeling and alerting.\n3. Q4.4 (Cost of 1-Day Delay): Supplies the baseline economic equation that powers our ROI and what-if simulation engine."
    p2.font.size = Pt(7.5)
    p2.font.color.rgb = TEXT_DARK

    add_footer(s10, 10)
    
    s10_notes = """SPEAKER NOTES:
"Before we write a single line of code, we want to ensure complete alignment with your operational reality. These 30+ questions represent our discovery framework.

Let me highlight the top three that drive the entire system:
First is Q1.1: What is your exact definition of backlog? Some companies count all open sales orders; others only count orders within a 30-day window. This determines our query scope.
Second is Q2.1: What are your top 3 to 5 bottleneck machines? If precision CNC centers are the pinch point 80% of the time, we instrument them with specialized predictive alerts.
Third is Q4.4: What is the true cost of a one-day delay to your business? When we know the daily holding cost, contract penalty, and margin impact, our simulation engine can tell planners exactly whether spending $5K on overtime is economically sound.

We will provide this checklist as a structured discovery workbook for your team to complete." """
    set_speaker_notes(s10, s10_notes)

    # =============================================================
    # SLIDE 11: Summary & Next Steps (Dark Theme Closing)
    # =============================================================
    s11 = add_base_slide(is_dark=True)
    
    # Top decorative glow line
    top_glow11 = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    top_glow11.fill.solid()
    top_glow11.fill.fore_color.rgb = CYAN_ACCENT
    top_glow11.line.fill.background()
    
    add_header(s11, "Next Steps: Your Path to Capacity Intelligence", "EXECUTIVE CLOSING & ACTION PLAN", "Partnering with Lumbini Elite Solutions to Transform Aerospace Manufacturing Performance", is_dark=True)
    
    # 3 Summary Pillar Cards (Width = 3.75 in)
    # Pillar 1: Delivery Commitments
    p11_1 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(3.75), Inches(4.0))
    p11_1.fill.solid()
    p11_1.fill.fore_color.rgb = DARK_CARD
    p11_1.line.color.rgb = CYAN_ACCENT
    p11_1.line.width = Pt(1.2)
    
    tf_p11_1 = p11_1.text_frame
    tf_p11_1.word_wrap = True
    tf_p11_1.margin_left = tf_p11_1.margin_top = Inches(0.18)
    p = tf_p11_1.paragraphs[0]
    p.text = "PHASED DELIVERY MILESTONES"
    p.font.name = "Arial"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    
    m_items = [
        ("Weeks 1–2: Structured Discovery", "Execute 4–6 hrs of focused discovery workshops using our 30-question workbook."),
        ("Weeks 3–4: Architecture & UI Sign-off", "Review Tableau wireframes, SAP connection scripts, and risk scoring logic."),
        ("Weeks 5–7: Automated Pipeline Build", "Deploy SAP HANA queries and build the core Backlog & Costing reports."),
        ("Weeks 8–10: Rigorous UAT Testing", "Reconcile live data against legacy spreadsheets with shop planners."),
        ("Weeks 11–12: Production Go-Live", "Roll out Tableau cockpit across 50+ users and retire manual Excel spreadsheets.")
    ]
    for m_t, m_d in m_items:
        p = tf_p11_1.add_paragraph()
        p.space_before = Pt(5)
        r1 = p.add_run()
        r1.text = "• " + m_t + "\n"
        r1.font.bold = True
        r1.font.size = Pt(8)
        r1.font.color.rgb = TEXT_LIGHT
        r2 = p.add_run()
        r2.text = m_d
        r2.font.bold = False
        r2.font.size = Pt(7.5)
        r2.font.color.rgb = TEXT_LIGHT_MUTED

    # Pillar 2: Commercial & Resource Model
    p11_2 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.79), Inches(1.5), Inches(3.75), Inches(4.0))
    p11_2.fill.solid()
    p11_2.fill.fore_color.rgb = DARK_CARD
    p11_2.line.color.rgb = GOLD_ACCENT
    p11_2.line.width = Pt(1.2)
    
    tf_p11_2 = p11_2.text_frame
    tf_p11_2.word_wrap = True
    tf_p11_2.margin_left = tf_p11_2.margin_top = Inches(0.18)
    p = tf_p11_2.paragraphs[0]
    p.text = "COMMERCIALS & GOVERNANCE"
    p.font.name = "Arial"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    
    comm_items = [
        ("Phase 1 Investment: $60K–$85K", "Comprehensive fixed-scope delivery covering discovery, SAP integration, Tableau modeling, UAT, and enablement."),
        ("Expected First-Year ROI: $180K–$400K", "Recovers emergency overtime, minimizes delivery penalty drag, and reclaims planning hours."),
        ("Payback Period: 4–6 Months", "High-velocity return on investment that directly self-funds subsequent Phase 2 cockpit enhancements."),
        ("Team Commitment Required", "3–4 HICAL champions allocated at 40% time for 12 weeks to guide requirements, UAT, and adoption.")
    ]
    for c_t, c_d in comm_items:
        p = tf_p11_2.add_paragraph()
        p.space_before = Pt(5)
        r1 = p.add_run()
        r1.text = "• " + c_t + "\n"
        r1.font.bold = True
        r1.font.size = Pt(8)
        r1.font.color.rgb = TEXT_LIGHT
        r2 = p.add_run()
        r2.text = c_d
        r2.font.bold = False
        r2.font.size = Pt(7.5)
        r2.font.color.rgb = TEXT_LIGHT_MUTED

    # Pillar 3: Immediate Next Steps
    p11_3 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.78), Inches(1.5), Inches(3.75), Inches(4.0))
    p11_3.fill.solid()
    p11_3.fill.fore_color.rgb = DARK_CARD
    p11_3.line.color.rgb = EMERALD_GREEN
    p11_3.line.width = Pt(1.2)
    
    tf_p11_3 = p11_3.text_frame
    tf_p11_3.word_wrap = True
    tf_p11_3.margin_left = tf_p11_3.margin_top = Inches(0.18)
    p = tf_p11_3.paragraphs[0]
    p.text = "IMMEDIATE ACTION PLAN (NEXT 14 DAYS)"
    p.font.name = "Arial"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_GREEN
    
    act_items = [
        ("Step 1: Workbook Distribution", "Lumbini transmits the 30-question Discovery Workbook to HICAL project leads."),
        ("Step 2: Schedule Discovery Sessions", "Lock two 2-hour technical discovery workshops across Planning, SAP IT, and Finance."),
        ("Step 3: SAP Read Access Setup", "Coordinate IT provisioning of read-only access to VBAK, RESB, and CRHD."),
        ("Step 4: Scope & Statement of Work", "Lumbini submits the finalized Phase 1 Statement of Work for formal sign-off."),
        ("Target Go-Live: End of Q2 2026", "Positioning HICAL for measurable manufacturing excellence and capacity intelligence.")
    ]
    for a_t, a_d in act_items:
        p = tf_p11_3.add_paragraph()
        p.space_before = Pt(5)
        r1 = p.add_run()
        r1.text = "✓ " + a_t + "\n"
        r1.font.bold = True
        r1.font.size = Pt(8)
        r1.font.color.rgb = CYAN_ACCENT
        r2 = p.add_run()
        r2.text = a_d
        r2.font.bold = False
        r2.font.size = Pt(7.5)
        r2.font.color.rgb = TEXT_LIGHT_MUTED

    # Bottom Call-To-Action Banner
    cta_bar = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.65), Inches(11.733), Inches(1.15))
    cta_bar.fill.solid()
    cta_bar.fill.fore_color.rgb = RGBColor(15, 30, 60)
    cta_bar.line.color.rgb = CYAN_ACCENT
    cta_bar.line.width = Pt(1.5)
    
    tf_cta = cta_bar.text_frame
    tf_cta.word_wrap = True
    tf_cta.margin_left = tf_cta.margin_top = Inches(0.15)
    p = tf_cta.paragraphs[0]
    p.text = "EXECUTIVE SUMMARY STATEMENT"
    p.font.name = "Arial"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    
    p2 = tf_cta.add_paragraph()
    p2.space_before = Pt(3)
    p2.text = "\"HICAL has an immediate opportunity to move from reactive firefighting to proactive capacity intelligence. The technical foundation is already in place with SAP HANA and Tableau. The ROI is compelling with a 4–6 month payback. Lumbini Elite Solutions is ready to partner with you to turn this roadmap into reality. Are you ready to take the next step?\""
    p2.font.name = "Arial"
    p2.font.size = Pt(9)
    p2.font.italic = True
    p2.font.color.rgb = TEXT_LIGHT

    add_footer(s11, 11, is_dark=True)
    
    s11_notes = """SPEAKER NOTES:
"HICAL has an opportunity to move from reactive firefighting to proactive capacity intelligence. We've outlined a realistic, phased path to get there.

The foundation is strong: you already have SAP HANA data, Tableau infrastructure, and motivated teams.
The business case is compelling: a 4 to 6 month payback with $450K to $1.1M in value unlocked over 3 years.
The risk is low: Phase 1 delivers complete value in 12 weeks without requiring massive system overhauls.

What is required next is simple:
1. We transmit the discovery workbook.
2. We hold two 2-hour discovery workshops over the next two weeks.
3. We finalize the Statement of Work and launch Phase 1 for a target go-live by the end of Q2.

Thank you for your time, and we look forward to answering your questions." """
    set_speaker_notes(s11, s11_notes)

    # Save presentation
    prs.save(output_path)
    print(f"Presentation successfully created and saved to: {output_path}")

if __name__ == "__main__":
    build_presentation()
