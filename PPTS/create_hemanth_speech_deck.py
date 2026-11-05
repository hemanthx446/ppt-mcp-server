import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def build_presentation(output_path="Swetha_GRC_Meeting_Speech_Deck.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # -------------------------------------------------------------
    # Palette & Design Tokens
    # -------------------------------------------------------------
    DARK_BG = RGBColor(18, 18, 18)           # #121212 Dark Charcoal
    DARK_CARD = RGBColor(28, 28, 30)         # #1C1C1E
    DARK_BORDER = RGBColor(48, 48, 52)       # Subtle slate border
    
    LIGHT_BG = RGBColor(248, 249, 250)       # #F8F9FA Ice White
    CARD_BG = RGBColor(255, 255, 255)        # Crisp White
    BORDER_GRAY = RGBColor(226, 232, 240)    # Soft slate border
    
    PRIMARY_RED = RGBColor(227, 6, 19)       # #E30613 Brand Accent Red
    ACCENT_RED_BG = RGBColor(254, 242, 242)  # Subtle Red Tint for key pills
    
    TEXT_DARK = RGBColor(26, 32, 44)         # #1A202C High contrast dark
    TEXT_MUTED = RGBColor(100, 116, 139)     # Slate Muted
    TEXT_LIGHT = RGBColor(248, 250, 252)     # Off-white
    TEXT_LIGHT_MUTED = RGBColor(148, 163, 184)
    
    TOTAL_SLIDES = 4

    def create_base_slide(is_dark=False):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = DARK_BG if is_dark else LIGHT_BG
        bg.line.fill.background()
        return slide

    def add_header(slide, title_text, subtitle_text):
        # Red Accent Bar
        stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.55), Inches(0.08), Inches(0.55))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = PRIMARY_RED
        stripe.line.fill.background()
        
        # Title
        tx_box = slide.shapes.add_textbox(Inches(1.05), Inches(0.48), Inches(11.4), Inches(0.45))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK
        
        # Subtitle
        tx_sub = slide.shapes.add_textbox(Inches(1.05), Inches(0.98), Inches(11.4), Inches(0.35))
        tf_sub = tx_sub.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle_text
        p_sub.font.name = "Calibri"
        p_sub.font.size = Pt(12)
        p_sub.font.italic = True
        p_sub.font.color.rgb = TEXT_MUTED

    def add_footer(slide, slide_num):
        # Footer Divider Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = BORDER_GRAY
        line.line.fill.background()
        
        # Left Text
        tx_l = slide.shapes.add_textbox(Inches(0.8), Inches(6.95), Inches(8.5), Inches(0.3))
        tf_l = tx_l.text_frame
        tf_l.margin_left = tf_l.margin_top = tf_l.margin_bottom = tf_l.margin_right = 0
        p_l = tf_l.paragraphs[0]
        p_l.text = "Lumbini Elite Solutions  |  Executive Follow-Up with Swetha, CPO of SAP GRC"
        p_l.font.name = "Calibri"
        p_l.font.size = Pt(9)
        p_l.font.color.rgb = TEXT_MUTED
        
        # Right Page Number
        tx_r = slide.shapes.add_textbox(Inches(11.033), Inches(6.95), Inches(1.5), Inches(0.3))
        tf_r = tx_r.text_frame
        tf_r.margin_left = tf_r.margin_top = tf_r.margin_bottom = tf_r.margin_right = 0
        p_r = tf_r.paragraphs[0]
        p_r.text = f"Slide {slide_num} of {TOTAL_SLIDES}"
        p_r.font.name = "Calibri"
        p_r.font.size = Pt(9)
        p_r.font.color.rgb = TEXT_MUTED
        p_r.alignment = PP_ALIGN.RIGHT

    # =========================================================================
    # SLIDE 1: Title & Vision Alignment (Dark Theme)
    # =========================================================================
    s1 = create_base_slide(is_dark=True)
    
    # Top Tag Pill
    tag_bg = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.15), Inches(3.6), Inches(0.38))
    tag_bg.fill.solid()
    tag_bg.fill.fore_color.rgb = DARK_CARD
    tag_bg.line.color.rgb = PRIMARY_RED
    tag_bg.line.width = Pt(1)
    
    tx_tag = s1.shapes.add_textbox(Inches(1.1), Inches(1.22), Inches(3.4), Inches(0.3))
    tf_tag = tx_tag.text_frame
    tf_tag.margin_top = tf_tag.margin_left = tf_tag.margin_bottom = tf_tag.margin_right = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = "EXECUTIVE FOLLOW-UP DIALOGUE"
    p_tag.font.name = "Arial"
    p_tag.font.size = Pt(10)
    p_tag.font.bold = True
    p_tag.font.color.rgb = PRIMARY_RED
    
    # Main Title
    tx_title = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(1.6))
    tf_title = tx_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_top = tf_title.margin_left = tf_title.margin_bottom = tf_title.margin_right = 0
    p1 = tf_title.paragraphs[0]
    p1.text = "The Next-Gen SAP GRC Paradigm"
    p1.font.name = "Arial"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT
    p1.space_after = Pt(8)
    
    p2 = tf_title.add_paragraph()
    p2.text = "Governance, Risk, and Control as the Architectural Backbone of Enterprise Integration"
    p2.font.name = "Arial"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = PRIMARY_RED
    
    # Red Horizontal Accent Line
    div_line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(3.65), Inches(2.2), Inches(0.04))
    div_line.fill.solid()
    div_line.fill.fore_color.rgb = PRIMARY_RED
    div_line.line.fill.background()
    
    # Speaker & Meeting Info Card
    spk_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.9), Inches(11.3), Inches(0.95))
    spk_card.fill.solid()
    spk_card.fill.fore_color.rgb = DARK_CARD
    spk_card.line.color.rgb = DARK_BORDER
    spk_card.line.width = Pt(1)
    
    tx_spk = s1.shapes.add_textbox(Inches(1.25), Inches(4.02), Inches(10.8), Inches(0.75))
    tf_spk = tx_spk.text_frame
    tf_spk.word_wrap = True
    tf_spk.margin_top = tf_spk.margin_left = tf_spk.margin_bottom = tf_spk.margin_right = 0
    
    p_spk1 = tf_spk.paragraphs[0]
    p_spk1.text = "Presented by Hemanth Kumar, Principal Consultant  |  Lumbini Elite Solutions"
    p_spk1.font.name = "Arial"
    p_spk1.font.size = Pt(13)
    p_spk1.font.bold = True
    p_spk1.font.color.rgb = TEXT_LIGHT
    p_spk1.space_after = Pt(4)
    
    p_spk2 = tf_spk.add_paragraph()
    p_spk2.text = "Strategic Discussion with Swetha, Chief Product Officer (CPO), SAP GRC  |  Focus: Clean Core, IAG/Joule AI Readiness & Scale"
    p_spk2.font.name = "Calibri"
    p_spk2.font.size = Pt(11)
    p_spk2.font.color.rgb = TEXT_LIGHT_MUTED
    
    # Bottom 3 Context Highlights
    pills = [
        ("Clean Core Alignment", "Eliminating custom ABAP to safeguard S/4HANA upgrade cycles."),
        ("Joule AI Readiness", "Structuring role semantics & authorization metadata for autonomous agent governance."),
        ("Field-Validated Scale", "Proven operational impact across 20k+ users and automated 2-hour SLAs.")
    ]
    card_w = 3.55
    gap = 0.32
    start_x = 1.0
    for i, (p_title, p_desc) in enumerate(pills):
        x = start_x + i * (card_w + gap)
        c_shape = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(5.2), Inches(card_w), Inches(1.4))
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = DARK_CARD
        c_shape.line.color.rgb = DARK_BORDER
        c_shape.line.width = Pt(1)
        
        tx_c = s1.shapes.add_textbox(Inches(x + 0.2), Inches(5.35), Inches(card_w - 0.4), Inches(1.1))
        tf_c = tx_c.text_frame
        tf_c.word_wrap = True
        tf_c.margin_top = tf_c.margin_left = tf_c.margin_bottom = tf_c.margin_right = 0
        
        pc1 = tf_c.paragraphs[0]
        pc1.text = p_title
        pc1.font.name = "Arial"
        pc1.font.size = Pt(12.5)
        pc1.font.bold = True
        pc1.font.color.rgb = PRIMARY_RED
        pc1.space_after = Pt(4)
        
        pc2 = tf_c.add_paragraph()
        pc2.text = p_desc
        pc2.font.name = "Calibri"
        pc2.font.size = Pt(10.5)
        pc2.font.color.rgb = TEXT_LIGHT_MUTED
        
    s1.notes_slide.notes_text_frame.text = (
        "TOPIC 1: OPENING & VISION ALIGNMENT (Slide 1)\n\n"
        "Key Bullet Points to Mention:\n"
        "- Zero-Modification Standard: Protecting S/4HANA core by avoiding custom ABAP code and decoupling custom workflows onto SAP BTP.\n"
        "- Upgrade Safety: Automated SU24/SU25 delta analysis to pre-empt authorization breaks and eliminate post-upgrade downtime.\n\n"
        "Spoken Script (Hemanth Kumar):\n"
        "\"Hi Swetha, thank you for your time today. As a Principal Consultant at Lumbini Elite, my focus is bridging high-level SAP roadmaps with enterprise-grade system plumbing. When we speak with enterprise clients moving to S/4HANA Cloud, their primary fear is custom code bloat. Our approach is absolute: zero core modifications, enforcing standard SAP APIs, and leveraging BTP so their baseline remains pristine and upgrade-ready.\""
    )

    # =========================================================================
    # SLIDE 2: Ecosystem & AI Readiness (Light Theme)
    # =========================================================================
    s2 = create_base_slide(is_dark=False)
    add_header(
        s2,
        "Ecosystem & AI Readiness",
        "Protecting the Clean Core while architecting role metadata for SAP Joule AI-driven governance."
    )
    
    pillars_s2 = [
        {
            "tag": "CLEAN CORE",
            "title": "Clean Core Alignment",
            "sub": "Zero-Modification Standard",
            "bullets": [
                "Zero core modifications in S/4HANA transformations.",
                "Enforce standard SAP APIs for user lifecycle events.",
                "Decouple custom workflows onto SAP BTP to preserve baseline."
            ]
        },
        {
            "tag": "S/4HANA SAFETY",
            "title": "Upgrade Safety",
            "sub": "Risk-Free Release Cycles",
            "bullets": [
                "Automated SU24/SU25 delta analysis across releases.",
                "Pre-empt authorization breaks and SoD conflicts before cutover.",
                "Eliminate post-upgrade emergency patching and downtime."
            ]
        },
        {
            "tag": "BTP SECURITY",
            "title": "BTP-Driven Security",
            "sub": "Enterprise Identity Fabric",
            "bullets": [
                "Native integration with SAP Cloud Identity Services (IAS/IPS).",
                "Centralized identity federation across hybrid cloud/on-prem.",
                "SCIM-based provisioning connectors across all cloud tenants."
            ]
        },
        {
            "tag": "JOULE AI READY",
            "title": "SAP Joule AI Readiness",
            "sub": "Clean Role Metadata Layer",
            "bullets": [
                "Standardized role taxonomies and semantic metadata models.",
                "Enables Joule AI natural language access queries & approvals.",
                "Contextual simulation & intelligent role recommendation."
            ]
        }
    ]
    
    col4_w = 2.7
    col4_gap = 0.31
    left4_start = 0.8
    card2_y = 1.55
    card2_h = 4.2
    
    for i, p_info in enumerate(pillars_s2):
        x = left4_start + i * (col4_w + col4_gap)
        
        c_shape = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(card2_y), Inches(col4_w), Inches(card2_h))
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = CARD_BG
        c_shape.line.color.rgb = BORDER_GRAY
        c_shape.line.width = Pt(1)
        
        # Red Header Bar
        top_bar = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(card2_y), Inches(col4_w), Inches(0.08))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = PRIMARY_RED
        top_bar.line.fill.background()
        
        tx_box = s2.shapes.add_textbox(Inches(x + 0.2), Inches(card2_y + 0.22), Inches(col4_w - 0.4), Inches(card2_h - 0.44))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_bottom = tf.margin_right = 0
        
        # Tag
        p_tag = tf.paragraphs[0]
        p_tag.text = p_info["tag"]
        p_tag.font.name = "Arial"
        p_tag.font.size = Pt(9.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = PRIMARY_RED
        p_tag.space_after = Pt(3)
        
        # Title
        p_title = tf.add_paragraph()
        p_title.text = p_info["title"]
        p_title.font.name = "Arial"
        p_title.font.size = Pt(13)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_DARK
        p_title.space_after = Pt(2)
        
        # Subtitle
        p_subt = tf.add_paragraph()
        p_subt.text = p_info["sub"]
        p_subt.font.name = "Calibri"
        p_subt.font.size = Pt(10)
        p_subt.font.bold = True
        p_subt.font.color.rgb = TEXT_MUTED
        p_subt.space_after = Pt(12)
        
        for b_text in p_info["bullets"]:
            pb = tf.add_paragraph()
            pb.text = "-  " + b_text
            pb.font.name = "Calibri"
            pb.font.size = Pt(10)
            pb.font.color.rgb = TEXT_DARK
            pb.space_after = Pt(8)
            
    # Bottom Callout Card
    takeaway_shape = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.95), Inches(11.733), Inches(0.75))
    takeaway_shape.fill.solid()
    takeaway_shape.fill.fore_color.rgb = ACCENT_RED_BG
    takeaway_shape.line.color.rgb = PRIMARY_RED
    takeaway_shape.line.width = Pt(1)
    
    tx_tk = s2.shapes.add_textbox(Inches(1.0), Inches(6.05), Inches(11.3), Inches(0.55))
    tf_tk = tx_tk.text_frame
    tf_tk.word_wrap = True
    tf_tk.margin_top = tf_tk.margin_left = tf_tk.margin_bottom = tf_tk.margin_right = 0
    ptk = tf_tk.paragraphs[0]
    ptk.text = "Key Dialogue Takeaway for CPO: "
    ptk.font.name = "Arial"
    ptk.font.size = Pt(11)
    ptk.font.bold = True
    ptk.font.color.rgb = PRIMARY_RED
    
    run_tk = ptk.add_run()
    run_tk.text = "Lumbini Elite cleanses enterprise authorization data and enforces BTP standards today, creating the prerequisite semantic foundation for SAP Joule AI to govern tomorrow."
    run_tk.font.name = "Calibri"
    run_tk.font.size = Pt(10.5)
    run_tk.font.bold = False
    run_tk.font.color.rgb = TEXT_DARK
    
    add_footer(s2, 2)
    
    s2.notes_slide.notes_text_frame.text = (
        "TOPIC 2: AI & JOULE READINESS (Slide 2)\n\n"
        "Key Bullet Points to Mention:\n"
        "- BTP-Driven Identity Fabric: Native integration with SAP Cloud Identity Services (IAS/IPS) and SCIM-based provisioning connectors across tenants.\n"
        "- Clean Role Metadata Layer: Standardizing role taxonomies so SAP Joule can execute natural-language access queries, approvals, and contextual simulations.\n\n"
        "Spoken Script (Hemanth Kumar):\n"
        "\"Everyone wants to adopt AI and SAP Joule, but customers hit a wall because their underlying role metadata and legacy PFCG structures are chaotic. At Lumbini, we cleanse and structure that metadata today—establishing the exact semantic foundation required for SAP Joule and Cloud IAG to govern autonomously tomorrow.\""
    )

    # =========================================================================
    # SLIDE 3: Proven Field Scale & Metrics (Light Theme)
    # =========================================================================
    s3 = create_base_slide(is_dark=False)
    add_header(
        s3,
        "Proven Field Scale & Operational Metrics",
        "Demonstrated enterprise reliability, maintenance efficiency, and SLA compliance at scale."
    )
    
    stats_s3 = [
        {
            "val": "90%",
            "label": "Provisioning Time Reduction",
            "ctx": "Global Analytics & Cloud Estates",
            "desc": "Transformed 5-day manual ticketing bottlenecks into automated, policy-compliant 4-hour approvals."
        },
        {
            "val": "60%",
            "label": "Maintenance Overhead Drop",
            "ctx": "20,000+ Global Users Scaled",
            "desc": "Slashed recurring administrative effort via role rationalization, composite pruning, and automated re-certification."
        },
        {
            "val": "< 2 Hours",
            "label": "IP Access SLAs",
            "ctx": "GRC CUP / ARM Automation",
            "desc": "Guaranteed firefighter emergency role elevation with zero-touch provisioning and continuous audit logging."
        }
    ]
    
    stat_w = 3.65
    stat_gap = 0.39
    stat_y = 1.55
    stat_h = 2.1
    left_start = 0.8
    
    for i, s_item in enumerate(stats_s3):
        x = left_start + i * (stat_w + stat_gap)
        
        c_shape = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(stat_y), Inches(stat_w), Inches(stat_h))
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = CARD_BG
        c_shape.line.color.rgb = BORDER_GRAY
        c_shape.line.width = Pt(1)
        
        tx_box = s3.shapes.add_textbox(Inches(x + 0.25), Inches(stat_y + 0.18), Inches(stat_w - 0.5), Inches(stat_h - 0.36))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_bottom = tf.margin_right = 0
        
        p_val = tf.paragraphs[0]
        p_val.text = s_item["val"]
        p_val.font.name = "Arial"
        p_val.font.size = Pt(28)
        p_val.font.bold = True
        p_val.font.color.rgb = PRIMARY_RED
        p_val.space_after = Pt(2)
        
        p_lbl = tf.add_paragraph()
        p_lbl.text = s_item["label"]
        p_lbl.font.name = "Arial"
        p_lbl.font.size = Pt(11)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = TEXT_DARK
        
        p_ctx = tf.add_paragraph()
        p_ctx.text = s_item["ctx"]
        p_ctx.font.name = "Calibri"
        p_ctx.font.size = Pt(9.5)
        p_ctx.font.bold = True
        p_ctx.font.color.rgb = PRIMARY_RED
        p_ctx.space_after = Pt(5)
        
        p_desc = tf.add_paragraph()
        p_desc.text = s_item["desc"]
        p_desc.font.name = "Calibri"
        p_desc.font.size = Pt(9.5)
        p_desc.font.color.rgb = TEXT_MUTED
        
    # Bottom Containers: Operational Blueprint & Strategic Impact
    bot_y = 3.9
    bot_h = 2.8
    bot_w = 5.67
    bot_gap = 0.39
    
    # Left Box
    c_left = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(bot_y), Inches(bot_w), Inches(bot_h))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = CARD_BG
    c_left.line.color.rgb = BORDER_GRAY
    c_left.line.width = Pt(1)
    
    tx_bl = s3.shapes.add_textbox(Inches(1.05), Inches(bot_y + 0.2), Inches(bot_w - 0.5), Inches(bot_h - 0.4))
    tf_bl = tx_bl.text_frame
    tf_bl.word_wrap = True
    tf_bl.margin_top = tf_bl.margin_left = tf_bl.margin_bottom = tf_bl.margin_right = 0
    
    p_bl_t = tf_bl.paragraphs[0]
    p_bl_t.text = "Operational Field Rigor (Validated Architecture)"
    p_bl_t.font.name = "Arial"
    p_bl_t.font.size = Pt(13)
    p_bl_t.font.bold = True
    p_bl_t.font.color.rgb = TEXT_DARK
    p_bl_t.space_after = Pt(8)
    
    points_left = [
        "Complex Multi-Instance Support: Flawless governance orchestration across on-prem ECC 6.0, S/4HANA, and BTP.",
        "Zero-Defect Audit Performance: 100% pass rate under SOX-404, ISO-27001, and global data privacy audits.",
        "Automated ARM/CUP Routing: 99.9% automated routing accuracy, eliminating manual helpdesk escalation."
    ]
    for pt in points_left:
        p_pt = tf_bl.add_paragraph()
        p_pt.text = "-  " + pt
        p_pt.font.name = "Calibri"
        p_pt.font.size = Pt(10)
        p_pt.font.color.rgb = TEXT_DARK
        p_pt.space_after = Pt(6)
        
    # Right Box
    c_right = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + bot_w + bot_gap), Inches(bot_y), Inches(bot_w), Inches(bot_h))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = CARD_BG
    c_right.line.color.rgb = BORDER_GRAY
    c_right.line.width = Pt(1)
    
    tx_br = s3.shapes.add_textbox(Inches(0.8 + bot_w + bot_gap + 0.25), Inches(bot_y + 0.2), Inches(bot_w - 0.5), Inches(bot_h - 0.4))
    tf_br = tx_br.text_frame
    tf_br.word_wrap = True
    tf_br.margin_top = tf_br.margin_left = tf_br.margin_bottom = tf_br.margin_right = 0
    
    p_br_t = tf_br.paragraphs[0]
    p_br_t.text = "Direct Value for the SAP CPO Roadmap"
    p_br_t.font.name = "Arial"
    p_br_t.font.size = Pt(13)
    p_br_t.font.bold = True
    p_br_t.font.color.rgb = TEXT_DARK
    p_br_t.space_after = Pt(8)
    
    points_right = [
        "De-risks Cloud Migrations: Eliminates customer hesitation by proving seamless coexistence of on-prem GRC and IAG.",
        "Reduces Post-Go-Live Churn: Clean authorization design cuts customer governance support tickets by over 70%.",
        "Field Telemetry Loop: Provides real-world connector benchmarks and edge-case telemetry directly to SAP engineering."
    ]
    for pr in points_right:
        p_pr = tf_br.add_paragraph()
        p_pr.text = "-  " + pr
        p_pr.font.name = "Calibri"
        p_pr.font.size = Pt(10)
        p_pr.font.color.rgb = TEXT_DARK
        p_pr.space_after = Pt(6)

    add_footer(s3, 3)
    
    s3.notes_slide.notes_text_frame.text = (
        "TOPIC 3: PROVEN FIELD SCALE & METRICS (Slide 3)\n\n"
        "Key Bullet Points to Mention:\n"
        "- 90% Provisioning Reduction: Transforming 5-day manual bottlenecks into automated 4-hour approvals for global analytics estates.\n"
        "- 20,000+ Global Users Scaled: Dropping recurring maintenance overhead by 60% through role rationalization and automated re-certification.\n"
        "- Under 2-Hour IP SLAs: GRC CUP and ARM automation guaranteeing secure, zero-touch emergency access for development teams.\n\n"
        "Spoken Script (Hemanth Kumar):\n"
        "\"We don't just talk theory; we bring battle-tested execution. For complex global landscapes supporting over 20,000 users, our role rationalization frameworks have dropped maintenance overhead by 60%. Furthermore, by combining GRC CUP and ARM automation, we’ve slashed secure IP access provisioning SLAs from 5 days down to under 2 hours.\""
    )

    # =========================================================================
    # SLIDE 4: Partnership Proposal & Next Steps (Light Theme)
    # =========================================================================
    s4 = create_base_slide(is_dark=False)
    add_header(
        s4,
        "Partnership Proposal & Next Steps",
        "Positioning Lumbini Elite as an agile extension of the SAP GRC CPO Office."
    )
    
    proposals = [
        {
            "tag": "PILLAR 1",
            "title": "Extension of CPO Office",
            "sub": "Agile Field Delivery Partner",
            "items": [
                "Serve as a specialized strike team for strategic SAP accounts undergoing complex GRC modernization.",
                "Provide rapid technical validation on new Cloud IAG API capabilities and hybrid deployment topologies.",
                "Funnel structured enterprise feedback and customer challenges directly to SAP product management."
            ]
        },
        {
            "tag": "PILLAR 2",
            "title": "Pre-Cloud Remediation Accelerators",
            "sub": "De-Risking Customer Onboarding",
            "items": [
                "Offer proven toolkits that scrub legacy custom ABAP code and obsolete t-codes before cloud migration.",
                "Automate SoD rule-set rationalization, cutting pre-migration readiness time by over 40%.",
                "Ensure clean, standard-compliant role catalogs for friction-free Cloud IAG adoption."
            ]
        },
        {
            "tag": "PILLAR 3",
            "title": "Joint Technical Workshop Pilot",
            "sub": "30-Day Co-Innovation Sprint",
            "items": [
                "Conduct a 2-week joint working session with SAP GRC engineering on Joule AI role metadata templates.",
                "Deploy a joint prototype on a nominated lighthouse enterprise client to validate real-world impact.",
                "Co-author an executive case study and co-present outcomes at SAP Sapphire."
            ]
        }
    ]
    
    ws_w = 3.65
    ws_gap = 0.39
    ws_y = 1.55
    ws_h = 3.7
    
    for i, prop in enumerate(proposals):
        x = left_start + i * (ws_w + ws_gap)
        
        c_shape = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(ws_y), Inches(ws_w), Inches(ws_h))
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = CARD_BG
        c_shape.line.color.rgb = BORDER_GRAY
        c_shape.line.width = Pt(1)
        
        # Pill for Pillar Tag
        pill = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.25), Inches(ws_y + 0.25), Inches(1.2), Inches(0.3))
        pill.fill.solid()
        pill.fill.fore_color.rgb = ACCENT_RED_BG
        pill.line.color.rgb = PRIMARY_RED
        pill.line.width = Pt(1)
        
        tx_pill = s4.shapes.add_textbox(Inches(x + 0.25), Inches(ws_y + 0.28), Inches(1.2), Inches(0.25))
        tf_pill = tx_pill.text_frame
        tf_pill.margin_top = tf_pill.margin_left = tf_pill.margin_bottom = tf_pill.margin_right = 0
        p_p = tf_pill.paragraphs[0]
        p_p.text = prop["tag"]
        p_p.font.name = "Arial"
        p_p.font.size = Pt(9)
        p_p.font.bold = True
        p_p.font.color.rgb = PRIMARY_RED
        p_p.alignment = PP_ALIGN.CENTER
        
        # Card Body
        tx_box = s4.shapes.add_textbox(Inches(x + 0.25), Inches(ws_y + 0.72), Inches(ws_w - 0.5), Inches(ws_h - 0.85))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_bottom = tf.margin_right = 0
        
        p_title = tf.paragraphs[0]
        p_title.text = prop["title"]
        p_title.font.name = "Arial"
        p_title.font.size = Pt(13)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_DARK
        p_title.space_after = Pt(2)
        
        p_sub = tf.add_paragraph()
        p_sub.text = prop["sub"]
        p_sub.font.name = "Calibri"
        p_sub.font.size = Pt(10)
        p_sub.font.bold = True
        p_sub.font.color.rgb = PRIMARY_RED
        p_sub.space_after = Pt(12)
        
        for item in prop["items"]:
            pi = tf.add_paragraph()
            pi.text = "-  " + item
            pi.font.name = "Calibri"
            pi.font.size = Pt(10)
            pi.font.color.rgb = TEXT_DARK
            pi.space_after = Pt(7)
            
    # Bottom Action Callout
    act_shape = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.5), Inches(11.733), Inches(1.15))
    act_shape.fill.solid()
    act_shape.fill.fore_color.rgb = CARD_BG
    act_shape.line.color.rgb = PRIMARY_RED
    act_shape.line.width = Pt(1.5)
    
    tx_act = s4.shapes.add_textbox(Inches(1.1), Inches(5.62), Inches(11.1), Inches(0.9))
    tf_act = tx_act.text_frame
    tf_act.word_wrap = True
    tf_act.margin_top = tf_act.margin_left = tf_act.margin_bottom = tf_act.margin_right = 0
    
    p_act1 = tf_act.paragraphs[0]
    p_act1.text = "Proposed Immediate Next Step: 45-Minute Working Session"
    p_act1.font.name = "Arial"
    p_act1.font.size = Pt(12)
    p_act1.font.bold = True
    p_act1.font.color.rgb = PRIMARY_RED
    p_act1.space_after = Pt(3)
    
    p_act2 = tf_act.add_paragraph()
    p_act2.text = "Schedule a 45-minute technical alignment between Hemanth Kumar (Lumbini Elite) and the SAP GRC Product Architecture Lead to define the Phase 1 workshop agenda and establish criteria for a lighthouse pilot."
    p_act2.font.name = "Calibri"
    p_act2.font.size = Pt(11)
    p_act2.font.color.rgb = TEXT_DARK
    
    add_footer(s4, 4)
    
    s4.notes_slide.notes_text_frame.text = (
        "TOPIC 4: PARTNERSHIP & PROPOSED NEXT STEPS (Slide 4)\n\n"
        "Key Bullet Points to Mention:\n"
        "- Extension of CPO Office: Acting as a specialized field strike team for strategic SAP accounts undergoing complex GRC modernization.\n"
        "- Pre-Cloud Remediation: Utilizing proprietary toolkits to scrub custom ABAP code and rationalize SoD rule-sets before cloud onboarding.\n"
        "- 30-Day Co-Innovation Sprint: Conducting a joint working session on Joule AI role metadata templates and launching a lighthouse client pilot.\n\n"
        "Spoken Script (Hemanth Kumar):\n"
        "\"Our goal is to act as an agile extension of your CPO office—helping de-risk customer onboarding and accelerating Cloud IAG adoption. I’d love to propose a brief 45-minute technical working session between our engineering team and your product architecture leads next week to define a Phase 1 workshop agenda and a lighthouse pilot. How does that sound?\""
    )

    # Save presentation
    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == "__main__":
    build_presentation()
