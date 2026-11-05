"""
Master Deck Generator for Lumbini Elite Group
Generates the 34-slide customer-grade executive presentation:
'Lumbini Elite Group | Product, Solutions & Services'

Built strictly to the master narrative:
'Lumbini Elite Group architects intelligent enterprises by connecting business strategy,
enterprise applications, operational systems, data, AI, governance, and industry platforms
into a unified operating model.'
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# -------------------------------------------------------------
# Premium Executive Color Tokens & Typography
# -------------------------------------------------------------
NAVY_CANVAS       = RGBColor(10, 22, 44)      # #0A162C Deep Executive Navy Canvas
NAVY_SURFACE      = RGBColor(19, 34, 64)      # #132240 Elevated Surface on Dark
NAVY_SURFACE_ALT  = RGBColor(22, 40, 75)      # #16284B Secondary Dark Surface
NAVY_BORDER       = RGBColor(38, 59, 99)      # #263B63 Restrained Dark Border
CYAN_ACCENT       = RGBColor(0, 180, 216)     # #00B4D8 Tech Cyan Accent
BLUE_SAP          = RGBColor(0, 102, 204)     # #0066CC Enterprise SAP Blue
SAP_DEEP          = RGBColor(10, 40, 95)      # #0A285F Sapphire Blue

LIGHT_CANVAS      = RGBColor(248, 250, 252)   # #F8FAFC Slate Ice Light Canvas
CARD_WHITE        = RGBColor(255, 255, 255)   # #FFFFFF Pure White Container
CARD_TINT         = RGBColor(241, 245, 249)   # #F1F5F9 Soft Slate Tint
CARD_BORDER       = RGBColor(226, 232, 240)   # #E2E8F0 Subtle Outline Border
BORDER_ACCENT     = RGBColor(186, 215, 245)   # #BAD7F5 Soft Blue Border
EMERALD_ACCENT    = RGBColor(16, 185, 129)    # #10B981 Verified Green
AMBER_ACCENT      = RGBColor(217, 119, 6)     # #D97706 Warm Warning Amber
CRIMSON_ACCENT    = RGBColor(220, 38, 38)     # #DC2626 Critical / Disconnect Red
PURPLE_ACCENT     = RGBColor(124, 58, 237)    # #7C3AED AI / Data Accent
TEAL              = RGBColor(27, 127, 121)    # #1B7F79 Industrial Teal Accent

TEXT_DARK         = RGBColor(15, 23, 42)      # #0F172A Deep Slate Charcoal
TEXT_SECONDARY    = RGBColor(51, 65, 85)      # #334155 Slate Secondary
TEXT_MUTED        = RGBColor(100, 116, 139)   # #64748B Cool Muted Slate
TEXT_LIGHT        = RGBColor(248, 250, 252)   # #F8FAFC High-Contrast Light
TEXT_LIGHT_MUTED  = RGBColor(148, 163, 184)   # #94A3B8 Soft Light Slate

FONT_FAMILY       = "Inter"
TOTAL_SLIDES      = 34


class DeckBuilder:
    def __init__(self, filename="Lumbini_Elite_Group_Product_Solutions_Services.pptx"):
        self.filename = filename
        self.prs = Presentation()
        self.prs.slide_width = Inches(13.333)
        self.prs.slide_height = Inches(7.500)
        self.blank_layout = self.prs.slide_layouts[6] if len(self.prs.slide_layouts) > 6 else self.prs.slide_layouts[0]
        
        # Clean package metadata
        core = self.prs.core_properties
        core.author = "Lumbini Elite Group"
        core.last_modified_by = "Lumbini Elite Group"
        core.title = "Lumbini Elite Group | Product, Solutions & Services"
        core.subject = "Enterprise Architecture, Products & Transformation Services"
        core.comments = "Unified Operating Model Capabilities Deck"

    # -------------------------------------------------------------
    # Slide Foundation Helpers
    # -------------------------------------------------------------
    def create_base_slide(self, is_dark=False):
        slide = self.prs.slides.add_slide(self.blank_layout)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.500))
        bg.fill.solid()
        bg.fill.fore_color.rgb = NAVY_CANVAS if is_dark else LIGHT_CANVAS
        bg.line.fill.background()
        return slide

    def add_header(self, slide, category_text, title_text, subtitle_text=None, is_dark=False):
        # 1. Category Eyebrow Badge
        badge_w = min(max(len(category_text) * 0.082 + 0.35, 2.0), 6.5)
        badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), Inches(0.36), Inches(badge_w), Inches(0.24))
        badge.fill.solid()
        badge.fill.fore_color.rgb = NAVY_SURFACE_ALT if is_dark else RGBColor(238, 242, 255)
        badge.line.color.rgb = CYAN_ACCENT if is_dark else BLUE_SAP
        badge.line.width = Pt(1.0)
        tf_b = badge.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = Inches(0.08)
        tf_b.margin_top = tf_b.margin_bottom = Inches(0.01)
        p_b = tf_b.paragraphs[0]
        p_b.text = category_text.upper()
        p_b.font.name = FONT_FAMILY
        p_b.font.size = Pt(8.5)
        p_b.font.bold = True
        p_b.font.color.rgb = CYAN_ACCENT if is_dark else BLUE_SAP

        # 2. Main Slide Title
        t_box = slide.shapes.add_textbox(Inches(0.80), Inches(0.66), Inches(11.733), Inches(0.44))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = FONT_FAMILY
        p_t.font.size = Pt(20)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_LIGHT if is_dark else TEXT_DARK

        # 3. Narrative Subheader (Action-oriented conversational thesis)
        if subtitle_text:
            s_box = slide.shapes.add_textbox(Inches(0.80), Inches(1.12), Inches(11.733), Inches(0.34))
            tf_s = s_box.text_frame
            tf_s.word_wrap = True
            tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
            p_s = tf_s.paragraphs[0]
            p_s.text = subtitle_text
            p_s.font.name = FONT_FAMILY
            p_s.font.size = Pt(11.5)
            p_s.font.bold = False
            p_s.font.color.rgb = CYAN_ACCENT if is_dark else BLUE_SAP

    def add_footer(self, slide, slide_num, is_dark=False):
        # Divider Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), Inches(6.92), Inches(11.733), Inches(0.01))
        line.fill.solid()
        line.fill.fore_color.rgb = NAVY_BORDER if is_dark else CARD_BORDER
        line.line.fill.background()

        # Metadata Left
        tb_l = slide.shapes.add_textbox(Inches(0.80), Inches(6.98), Inches(9.50), Inches(0.30))
        tf_l = tb_l.text_frame
        tf_l.margin_left = tf_l.margin_top = 0
        p_l = tf_l.paragraphs[0]
        p_l.text = "Lumbini Elite Group  |  Product, Solutions & Services  |  Executive Architecture Capabilities"
        p_l.font.name = FONT_FAMILY
        p_l.font.size = Pt(8.5)
        p_l.font.color.rgb = TEXT_LIGHT_MUTED if is_dark else TEXT_MUTED

        # Slide Number Right
        tb_r = slide.shapes.add_textbox(Inches(10.533), Inches(6.98), Inches(2.00), Inches(0.30))
        tf_r = tb_r.text_frame
        tf_r.margin_right = tf_r.margin_top = 0
        p_r = tf_r.paragraphs[0]
        p_r.alignment = PP_ALIGN.RIGHT
        p_r.text = f"{slide_num:02d} / {TOTAL_SLIDES:02d}"
        p_r.font.name = FONT_FAMILY
        p_r.font.size = Pt(8.5)
        p_r.font.bold = True
        p_r.font.color.rgb = CYAN_ACCENT if is_dark else BLUE_SAP

    # -------------------------------------------------------------
    # Visual Container & Card Factory Helpers
    # -------------------------------------------------------------
    def add_card(self, slide, x, y, w, h, bg_color=CARD_WHITE, border_color=CARD_BORDER, border_width=1.0):
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(border_width)
        else:
            shape.line.fill.background()
        return shape

    def add_text_block(self, slide, x, y, w, h, title=None, bullets=None, body=None, 
                       title_color=TEXT_DARK, body_color=TEXT_SECONDARY, title_size=13, body_size=10.5):
        box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.04)
        
        has_first = False
        if title:
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = FONT_FAMILY
            p.font.size = Pt(title_size)
            p.font.bold = True
            p.font.color.rgb = title_color
            p.space_after = Pt(4)
            has_first = True

        if body:
            p = tf.add_paragraph() if has_first else tf.paragraphs[0]
            p.text = body
            p.font.name = FONT_FAMILY
            p.font.size = Pt(body_size)
            p.font.color.rgb = body_color
            p.space_after = Pt(3)
            has_first = True

        if bullets:
            for b in bullets[:3]:  # Enforce 3-bullet maximum strictly
                p = tf.add_paragraph() if has_first else tf.paragraphs[0]
                p.text = f"•  {b}"
                p.font.name = FONT_FAMILY
                p.font.size = Pt(body_size)
                p.font.color.rgb = body_color
                p.space_after = Pt(3)
                has_first = True
        return box

    # -------------------------------------------------------------
    # SECTION I: THE ENTERPRISE PROBLEM (Slides 1 to 5)
    # -------------------------------------------------------------
    def build_slide_01(self):
        """Slide 1: Executive Title & Master Narrative (Dark)"""
        s = self.create_base_slide(is_dark=True)
        
        # Subtle decorative multi-tier architecture accent bars
        accent_y = 1.35
        for i, color in enumerate([CYAN_ACCENT, BLUE_SAP, PURPLE_ACCENT, EMERALD_ACCENT]):
            bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80 + i * 2.95), Inches(accent_y), Inches(2.80), Inches(0.06))
            bar.fill.solid()
            bar.fill.fore_color.rgb = color
            bar.line.fill.background()

        # Eyebrow
        tb_eye = s.shapes.add_textbox(Inches(0.80), Inches(1.70), Inches(11.733), Inches(0.40))
        tf_e = tb_eye.text_frame
        p_e = tf_e.paragraphs[0]
        p_e.text = "LUMBINI ELITE GROUP  ·  STRATEGIC CAPABILITIES OVERVIEW"
        p_e.font.name = FONT_FAMILY
        p_e.font.size = Pt(11)
        p_e.font.bold = True
        p_e.font.color.rgb = CYAN_ACCENT

        # Hero Presentation Title
        tb_title = s.shapes.add_textbox(Inches(0.80), Inches(2.15), Inches(11.733), Inches(1.10))
        tf_t = tb_title.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = "Lumbini Elite Group | Product, Solutions & Services"
        p_t.font.name = FONT_FAMILY
        p_t.font.size = Pt(34)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_LIGHT

        # Master Narrative Thesis Hero Container
        c_hero = self.add_card(s, 0.80, 3.45, 11.733, 1.65, bg_color=NAVY_SURFACE, border_color=CYAN_ACCENT, border_width=1.5)
        tb_m = s.shapes.add_textbox(Inches(1.10), Inches(3.60), Inches(11.133), Inches(1.35))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        
        p_lbl = tf_m.paragraphs[0]
        p_lbl.text = "THE CENTRAL NARRATIVE THESIS"
        p_lbl.font.name = FONT_FAMILY
        p_lbl.font.size = Pt(10)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = CYAN_ACCENT
        p_lbl.space_after = Pt(6)

        p_thesis = tf_m.add_paragraph()
        p_thesis.text = (
            "“Lumbini Elite Group architects intelligent enterprises by connecting business strategy, "
            "enterprise applications, operational systems, data, AI, governance, and industry platforms "
            "into a unified operating model.”"
        )
        p_thesis.font.name = FONT_FAMILY
        p_thesis.font.size = Pt(16)
        p_thesis.font.bold = True
        p_thesis.font.color.rgb = TEXT_LIGHT

        # Bottom 3 Contextual Overview Cards
        bottom_cards = [
            ("Two Complementary Entities", 
             ["Elitia Technologies delivers focused, productized software assets.",
              "Lumbini Elite Solutions & Services provides end-to-end consulting and engineering.",
              "Engaged individually or combined based on exact enterprise requirements."]),
            ("Intellectual & Editorial Rigor",
             ["Observe deeply: Uncover root constraints rather than treating symptoms.",
              "Question gently: Clarify process ownership, data lineage, and decision rights.",
              "Conclude structurally: Deliver measurable architectural and financial impact."]),
            ("Audience & Purpose",
             ["Built for enterprise decision-makers, CXOs, and solution architects.",
              "Not a generic brochure or vendor advertisement, but a strategic capabilities map.",
              "Demonstrates how to connect disparate systems into one coherent operating rhythm."])
        ]
        
        card_w = 3.75
        gap = 0.24
        for i, (head, bullets) in enumerate(bottom_cards):
            x = 0.80 + i * (card_w + gap)
            self.add_card(s, x, 5.30, card_w, 1.45, bg_color=NAVY_SURFACE_ALT, border_color=NAVY_BORDER)
            self.add_text_block(s, x + 0.15, 5.38, card_w - 0.30, 1.30,
                                title=head, bullets=bullets, title_color=CYAN_ACCENT, body_color=TEXT_LIGHT_MUTED,
                                title_size=11, body_size=9.2)

        self.add_footer(s, 1, is_dark=True)

    def build_slide_02(self):
        """Slide 2: The Enterprise Is More Than Its Systems"""
        s = self.create_base_slide(is_dark=False)
        self.add_header(s, "Section I: The Enterprise Problem", 
                        "The Enterprise Is More Than Its Systems",
                        "THE SYSTEM PARADOX: Enterprise performance emerges from process interaction, not isolated application silos")
        
        # 5-Column Conceptual Interaction Diagram
        dims = [
            ("1. Business Strategy", BLUE_SAP, 
             "Capital allocation, margin goals, delivery commitments, and market positioning.",
             ["Defines the target operating reality", "Establishes customer service-level mandates", "Sets capital and operational expenditure bounds"]),
            ("2. People & Roles", PURPLE_ACCENT, 
             "Shop-floor crews, plant planners, financial controllers, and executive decision-makers.",
             ["Execute physical and administrative actions", "Rely on timely operational context", "Require clear decision rights and ownership"]),
            ("3. Business Processes", BLUE_SAP, 
             "Plan-to-produce, order-to-cash, procure-to-pay, and record-to-report workflows.",
             ["Span multiple organizational handoffs", "Define standard operating sequencing", "Break down when exceptions lack owners"]),
            ("4. Systems & Tech", TEAL, 
             "SAP S/4HANA, MES, SCADA, edge PLCs, IoT meters, and cloud SaaS platforms.",
             ["Record transactions and machine states", "Store master data and operational logs", "Fail to coordinate when architectures diverge"]),
            ("5. Data & Governance", AMBER_ACCENT, 
             "Lineage definitions, validation rules, feedback loops, and audit checkpoints.",
             ["Validates information accuracy at entry", "Provides real-time observability across steps", "Ensures compliance and operational trust"])
        ]
        
        col_w = 2.15
        gap = 0.245
        for i, (title, color, desc, bullets) in enumerate(dims):
            x = 0.80 + i * (col_w + gap)
            # Header tab
            tab = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(1.60), Inches(col_w), Inches(0.36))
            tab.fill.solid()
            tab.fill.fore_color.rgb = color
            tab.line.fill.background()
            p = tab.text_frame.paragraphs[0]
            p.text = title
            p.alignment = PP_ALIGN.CENTER
            p.font.name = FONT_FAMILY
            p.font.size = Pt(10.5)
            p.font.bold = True
            p.font.color.rgb = TEXT_LIGHT

            # Content container
            self.add_card(s, x, 1.96, col_w, 3.45, bg_color=CARD_WHITE, border_color=CARD_BORDER)
            self.add_text_block(s, x + 0.12, 2.08, col_w - 0.24, 3.20,
                                title="Operational Role", body=desc, bullets=bullets,
                                title_color=color, body_color=TEXT_SECONDARY, title_size=11, body_size=9.2)

        # Horizontal Synthesis Box across the bottom
        c_syn = self.add_card(s, 0.80, 5.60, 11.733, 1.15, bg_color=CARD_TINT, border_color=BORDER_ACCENT)
        self.add_text_block(s, 0.95, 5.68, 11.433, 0.98,
                            title="THE ARCHITECTURAL IMPLICATION",
                            body="Evaluating applications in isolation hides the cross-dimensional dependencies that determine true operational throughput. A high-speed ERP transaction is rendered useless if physical shop-floor materials are misrouted, or if operators lack calibrated test data to clear a batch.",
                            bullets=["Point-solution optimization frequently pushes friction into adjacent business processes.",
                                     "True transformation requires harmonizing process design, human accountability, and data lineage."],
                            title_color=BLUE_SAP, body_color=TEXT_DARK, title_size=10.5, body_size=9.0)

        self.add_footer(s, 2)

    def build_slide_03(self):
        """Slide 3: Where Disconnection Becomes a Business Problem"""
        s = self.create_base_slide(is_dark=False)
        self.add_header(s, "Section I: The Enterprise Problem", 
                        "Where Disconnection Becomes a Business Problem",
                        "THE EXECUTION BREAKDOWN: Transactional completeness does not guarantee operational synchronization")
        
        # 6-Step Horizontal Value Sequence
        steps = [
            ("1. Business Intent", "Commercial order promise", 
             "Customer commits to precision shipment date with customized quality specifications.",
             "Disconnect: Commercial commitments made without real-time plant capacity verification.", CRIMSON_ACCENT),
            ("2. Enterprise Process", "ERP production order", 
             "Planning schedules MRP orders and generates shop-floor production batches in SAP.",
             "Disconnect: MRP schedule assumes theoretical machine uptime and static shift patterns.", AMBER_ACCENT),
            ("3. Application Trans.", "Materials release", 
             "Bill of materials (BOM) exploded and warehouse inventory reserved in digital ledger.",
             "Disconnect: Inventory records show stock present, but physical bin holds uninspected lots.", CRIMSON_ACCENT),
            ("4. Operational Exec.", "Shop-floor fabrication", 
             "Operators machine parts, capture torque curves, and assemble components on the line.",
             "Disconnect: Physical run deviates from plan; test data logged on manual paper run-sheets.", CRIMSON_ACCENT),
            ("5. Performance Info.", "Batch data capture", 
             "Quality results, machine scrap, cycle times, and energy consumption gathered.",
             "Disconnect: Telemetry trapped in isolated PLC logs; 48-hour delay before ERP confirmation.", AMBER_ACCENT),
            ("6. Management Dec.", "Executive evaluation", 
             "Leadership reviews monthly operational margins and customer delivery performance.",
             "Disconnect: Management acts on backward-looking averages, unaware of active line drift.", CRIMSON_ACCENT)
        ]
        
        box_w = 1.76
        gap = 0.234
        for i, (stitle, role, reality, friction, fcolor) in enumerate(steps):
            x = 0.80 + i * (box_w + gap)
            
            # Step sequence badge
            sbadge = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(1.60), Inches(box_w), Inches(0.32))
            sbadge.fill.solid()
            sbadge.fill.fore_color.rgb = BLUE_SAP
            sbadge.line.fill.background()
            p = sbadge.text_frame.paragraphs[0]
            p.text = stitle
            p.alignment = PP_ALIGN.CENTER
            p.font.name = FONT_FAMILY
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = TEXT_LIGHT

            # Step container
            self.add_card(s, x, 1.92, box_w, 4.60, bg_color=CARD_WHITE, border_color=CARD_BORDER)
            
            # Inner text blocks
            self.add_text_block(s, x + 0.10, 2.00, box_w - 0.20, 1.70,
                                title=role, body=reality,
                                title_color=TEXT_DARK, body_color=TEXT_SECONDARY, title_size=10, body_size=8.8)
            
            # Disconnect callout pill
            dpill = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x + 0.08), Inches(3.90), Inches(box_w - 0.16), Inches(2.50))
            dpill.fill.solid()
            dpill.fill.fore_color.rgb = RGBColor(254, 242, 242) if fcolor == CRIMSON_ACCENT else RGBColor(255, 251, 235)
            dpill.line.color.rgb = fcolor
            dpill.line.width = Pt(1.0)
            tf_d = dpill.text_frame
            tf_d.word_wrap = True
            tf_d.margin_left = tf_d.margin_right = Inches(0.08)
            tf_d.margin_top = Inches(0.08)
            p1 = tf_d.paragraphs[0]
            p1.text = "LATENT FRICTION POINT"
            p1.font.name = FONT_FAMILY
            p1.font.size = Pt(8.0)
            p1.font.bold = True
            p1.font.color.rgb = fcolor
            p1.space_after = Pt(4)
            p2 = tf_d.add_paragraph()
            p2.text = friction
            p2.font.name = FONT_FAMILY
            p2.font.size = Pt(8.5)
            p2.font.color.rgb = TEXT_DARK

            # Arrow connector to next
            if i < len(steps) - 1:
                arr = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + box_w + 0.05), Inches(1.68), Inches(0.14), Inches(0.16))
                arr.fill.solid()
                arr.fill.fore_color.rgb = BLUE_SAP
                arr.line.fill.background()

        # Synthesis Note
        sbar = self.add_card(s, 0.80, 6.60, 11.733, 0.26, bg_color=CARD_TINT, border_color=None)
        tb_sb = s.shapes.add_textbox(Inches(0.90), Inches(6.62), Inches(11.533), Inches(0.22))
        p_sb = tb_sb.text_frame.paragraphs[0]
        p_sb.text = "CORE INSIGHT: A system can record every ledger transaction perfectly while the underlying physical process remains fundamentally uncoordinated."
        p_sb.font.name = FONT_FAMILY
        p_sb.font.size = Pt(8.5)
        p_sb.font.bold = True
        p_sb.font.color.rgb = BLUE_SAP

        self.add_footer(s, 3)

    def build_slide_04(self):
        """Slide 4: Why Adding Another System May Not Solve the Problem"""
        s = self.create_base_slide(is_dark=False)
        self.add_header(s, "Section I: The Enterprise Problem", 
                        "Why Adding Another System May Not Solve the Problem",
                        "DIAGNOSTIC RIGOR: Sustainable interventions address underlying structural constraints, not software deficits")

        # 3x2 Comparative Diagnostic Matrix
        d_items = [
            ("1. Missing Tool vs. Disconnected Process",
             "Symptom: Operations requests a new tracking tool because work orders get delayed.",
             "Underlying Constraint: The handoff criteria between production planning and line supervisors is undefined.",
             "Intervention: Redesign the process boundary and handoff contract before configuring any software."),
            ("2. Data Volume vs. Information Quality",
             "Symptom: IT installs IoT sensors capturing millions of raw machine vibrations per minute.",
             "Underlying Constraint: Signals lack production batch context; nobody knows which customer lot was running.",
             "Intervention: Contextualize sensor telemetry with ERP work orders and material master definitions."),
            ("3. Missing Dashboard vs. Unclear Decision Rights",
             "Symptom: Quality requests an executive BI dashboard to visualize scrap spikes.",
             "Underlying Constraint: The dashboard shows scrap clearly, but no plant role has authority to pause the line.",
             "Intervention: Establish formal decision rights, escalation pathways, and operational intervention protocols."),
            ("4. Digitized Messages vs. Workflow Accountability",
             "Symptom: Procurement deploys a supplier messaging portal to eliminate email friction.",
             "Underlying Constraint: Messages arrive instantly, but nobody owns tracking unacknowledged delivery dates.",
             "Intervention: Implement automated task assignment, milestone approval gates, and SLA escalation rules."),
            ("5. AI Model Suggestion vs. Execution Authority",
             "Symptom: Data science deploys an AI model that predicts machine failures 4 hours in advance.",
             "Underlying Constraint: The model outputs an advisory ticket, but lacks permission to trigger maintenance in ERP.",
             "Intervention: Build deterministic governance boundaries and human-in-the-loop approval workflows."),
            ("6. Application Feature vs. Architecture Debt",
             "Symptom: Business units build ad-hoc custom web tools to fill local spreadsheet gaps.",
             "Underlying Constraint: Point tools create a fragile web of unmonitored point-to-point database syncs.",
             "Intervention: Integrate through an enterprise API fabric with unified data lineage and clean-core rules.")
        ]

        card_w = 3.75
        card_h = 2.45
        gap_x = 0.24
        gap_y = 0.20
        start_y = 1.60

        for idx, (title, symp, const, interv) in enumerate(d_items):
            row = idx // 3
            col = idx % 3
            x = 0.80 + col * (card_w + gap_x)
            y = start_y + row * (card_h + gap_y)

            self.add_card(s, x, y, card_w, card_h, bg_color=CARD_WHITE, border_color=CARD_BORDER)
            
            # Header strip
            hstrip = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(card_w), Inches(0.30))
            hstrip.fill.solid()
            hstrip.fill.fore_color.rgb = BLUE_SAP if row == 0 else SAP_DEEP
            hstrip.line.fill.background()
            p = hstrip.text_frame.paragraphs[0]
            p.text = title
            p.font.name = FONT_FAMILY
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = TEXT_LIGHT

            # Content inside card
            box = s.shapes.add_textbox(Inches(x + 0.12), Inches(y + 0.34), Inches(card_w - 0.24), Inches(card_h - 0.38))
            tf = box.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

            p1 = tf.paragraphs[0]
            p1.text = symp
            p1.font.name = FONT_FAMILY
            p1.font.size = Pt(8.5)
            p1.font.color.rgb = TEXT_MUTED
            p1.space_after = Pt(3)

            p2 = tf.add_paragraph()
            p2.text = const
            p2.font.name = FONT_FAMILY
            p2.font.size = Pt(9.0)
            p2.font.bold = True
            p2.font.color.rgb = CRIMSON_ACCENT
            p2.space_after = Pt(3)

            p3 = tf.add_paragraph()
            p3.text = interv
            p3.font.name = FONT_FAMILY
            p3.font.size = Pt(9.0)
            p3.font.bold = True
            p3.font.color.rgb = BLUE_SAP

        # Bottom synthesis banner
        self.add_card(s, 0.80, 6.55, 11.733, 0.28, bg_color=CARD_TINT, border_color=BORDER_ACCENT)
        tb_syn = s.shapes.add_textbox(Inches(0.90), Inches(6.57), Inches(11.533), Inches(0.24))
        p_s = tb_syn.text_frame.paragraphs[0]
        p_s.text = "CONCLUSION: Intervention must follow the actual constraint. We solve problems by identifying the disconnect, not by defaulting to software acquisition."
        p_s.font.name = FONT_FAMILY
        p_s.font.size = Pt(8.8)
        p_s.font.bold = True
        p_s.font.color.rgb = BLUE_SAP

        self.add_footer(s, 4)

    def build_slide_05(self):
        """Slide 5: Our Approach: Connect the Operating Model"""
        s = self.create_base_slide(is_dark=False)
        self.add_header(s, "Section I: The Enterprise Problem", 
                        "Our Approach: Connect the Operating Model",
                        "THE UNIFIED OPERATING MODEL: Synchronizing strategy, execution, data, and governance across continuous layers")

        # Left / Center: 6 Horizontal Stack Layers (7.80" wide)
        layers = [
            ("1. Business Strategy & Process Design", 
             "Strategic objectives, target operating models, cross-functional value streams, and decision rights.", BLUE_SAP),
            ("2. Enterprise Applications (ERP Core)", 
             "SAP S/4HANA, ECC, financial ledgers, procurement, and commercial supply chain backbones.", SAP_DEEP),
            ("3. Operational Systems & OT (Shop Floor)", 
             "Manufacturing Execution Systems (MES), SCADA, PLCs, testing stations, and digital energy meters.", TEAL),
            ("4. Data Foundations & Lineage Engineering", 
             "Ingestion pipelines, master data governance, automated data quality gates, and metric dictionaries.", PURPLE_ACCENT),
            ("5. AI-Enabled Workflows & Assistants", 
             "Grounded generative AI retrieval, autonomous agent task routing, and exception triage.", BLUE_SAP),
            ("6. Embedded Governance & Operational Controls", 
             "Role-based access, segregation of duties (SoD), audit logging, and human approval gates.", AMBER_ACCENT)
        ]

        stack_w = 7.70
        layer_h = 0.72
        layer_gap = 0.12
        stack_y = 1.60

        for i, (lname, ldesc, lcolor) in enumerate(layers):
            y = stack_y + i * (layer_h + layer_gap)
            
            # Layer bar
            self.add_card(s, 0.80, y, stack_w, layer_h, bg_color=CARD_WHITE, border_color=CARD_BORDER)
            
            # Left accent tag
            tag = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), Inches(y), Inches(0.18), Inches(layer_h))
            tag.fill.solid()
            tag.fill.fore_color.rgb = lcolor
            tag.line.fill.background()

            # Content
            self.add_text_block(s, 1.12, y + 0.08, stack_w - 0.40, layer_h - 0.16,
                                title=lname, body=ldesc,
                                title_color=lcolor, body_color=TEXT_SECONDARY, title_size=11, body_size=9.2)

        # Right: 3 Cross-Cutting Architecture Pillars (3.80" wide)
        pillars = [
            ("Cross-Cutting Integration", 
             "Bi-directional API management, event mesh, and edge protocol bridges connecting legacy and cloud.",
             ["Replaces fragile batch scripts with resilient APIs", "Enforces payload schema validation at boundaries", "Guarantees zero silent interface failures"],
             BLUE_SAP),
            ("Zero-Trust Security & Identity", 
             "Granular authorization, credential vaults, and encrypted operational telemetry.",
             ["Unifies corporate IT identity with OT plant access", "Protects operational technology from network threats", "Embeds compliance auditability across every tier"],
             SAP_DEEP),
            ("Closed-Loop Accountability", 
             "Human-in-the-loop validation, exception escalation, and audited ledger reconciliations.",
             ["Every automated action requires verified authority", "Exceptions route to defined role owners, not queues", "Ties operational changes directly to financial ledger"],
             EMERALD_ACCENT)
        ]

        pil_w = 3.80
        pil_h = 1.58
        pil_gap = 0.16
        pil_x = 8.733

        for i, (pname, pdesc, pbullets, pcolor) in enumerate(pillars):
            py = stack_y + i * (pil_h + pil_gap)
            self.add_card(s, pil_x, py, pil_w, pil_h, bg_color=CARD_WHITE, border_color=CARD_BORDER)
            
            # Header
            ph = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(pil_x), Inches(py), Inches(pil_w), Inches(0.28))
            ph.fill.solid()
            ph.fill.fore_color.rgb = pcolor
            ph.line.fill.background()
            p = ph.text_frame.paragraphs[0]
            p.text = pname
            p.font.name = FONT_FAMILY
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = TEXT_LIGHT

            # Bullets
            self.add_text_block(s, pil_x + 0.12, py + 0.32, pil_w - 0.24, pil_h - 0.36,
                                body=pdesc, bullets=pbullets,
                                body_color=TEXT_SECONDARY, body_size=8.5)

        # Bottom synthesis
        self.add_card(s, 0.80, 6.62, 11.733, 0.22, bg_color=CARD_TINT, border_color=None)
        tb_syn = s.shapes.add_textbox(Inches(0.90), Inches(6.63), Inches(11.533), Inches(0.20))
        p_syn = tb_syn.text_frame.paragraphs[0]
        p_syn.text = "NOT A SINGLE PRODUCT: These dimensions represent an integrated architecture methodology, not a claim that one software package solves everything."
        p_syn.font.name = FONT_FAMILY
        p_syn.font.size = Pt(8.5)
        p_syn.font.bold = True
        p_syn.font.color.rgb = BLUE_SAP

        self.add_footer(s, 5)

    # -------------------------------------------------------------
    # SECTION II: HOW THE CAPABILITIES FIT TOGETHER (Slides 6 to 8)
    # -------------------------------------------------------------
    def build_slide_06(self):
        """Slide 6: One Group, Two Complementary Capability Sets"""
        s = self.create_base_slide(is_dark=False)
        self.add_header(s, "Section II: How the Capabilities Fit Together", 
                        "One Group, Two Complementary Capability Sets",
                        "DUAL CAPABILITY MODEL: Productized software assets combined with end-to-end consulting, engineering, and support")

        # Two Distinct Primary Pillars
        col_w = 5.70
        
        # Left Pillar: Elitia Technologies (Products)
        self.add_card(s, 0.80, 1.60, col_w, 4.40, bg_color=CARD_WHITE, border_color=CARD_BORDER)
        hdr_l = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), Inches(1.60), Inches(col_w), Inches(0.48))
        hdr_l.fill.solid()
        hdr_l.fill.fore_color.rgb = BLUE_SAP
        hdr_l.line.fill.background()
        p = hdr_l.text_frame.paragraphs[0]
        p.text = "ELITIA TECHNOLOGIES  ·  SOFTWARE PRODUCTS"
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_FAMILY
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT

        self.add_text_block(s, 0.95, 2.15, col_w - 0.30, 0.70,
                            title="Purpose-Built Operational & Enterprise Software",
                            body="Responsible for engineering, packaging, and evolving the Elitia software product suite. Products address defined operational white spaces with rapid time-to-value.",
                            title_color=BLUE_SAP, body_color=TEXT_SECONDARY, title_size=11, body_size=9.2)

        p_items = [
            ("Manufacturing & Operations", "Elitia MES (Execution & Genealogy) · Elitia EMS (Energy Monitoring)"),
            ("Data & Analytics", "Elitia BI (Operational Analytics) · Elitia DGS (Data Governance Suite)"),
            ("Ecosystem & Migration", "Elitia Migration Cockpit (ECC to S/4HANA Validation) · Elitia Supplier Collaboration · Elitia Assessment Suite")
        ]
        for idx, (pcat, pnames) in enumerate(p_items):
            box_y = 2.90 + idx * 0.95
            self.add_card(s, 0.95, box_y, col_w - 0.30, 0.85, bg_color=CARD_TINT, border_color=BORDER_ACCENT)
            self.add_text_block(s, 1.05, box_y + 0.06, col_w - 0.50, 0.72,
                                title=pcat, body=pnames,
                                title_color=BLUE_SAP, body_color=TEXT_DARK, title_size=10, body_size=8.8)

        # Right Pillar: Lumbini Elite Solutions & Services
        rx = 6.833
        self.add_card(s, rx, 1.60, col_w, 4.40, bg_color=CARD_WHITE, border_color=CARD_BORDER)
        hdr_r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(rx), Inches(1.60), Inches(col_w), Inches(0.48))
        hdr_r.fill.solid()
        hdr_r.fill.fore_color.rgb = SAP_DEEP
        hdr_r.line.fill.background()
        p = hdr_r.text_frame.paragraphs[0]
        p.text = "LUMBINI ELITE SOLUTIONS & SERVICES  ·  CONSULTING & ENGINEERING"
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_FAMILY
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT

        self.add_text_block(s, rx + 0.15, 2.15, col_w - 0.30, 0.70,
                            title="End-to-End Enterprise Systems & Transformation Advisory",
                            body="Responsible for consulting, implementation, custom development, systems integration, data engineering, and support services across enterprise landscapes.",
                            title_color=SAP_DEEP, body_color=TEXT_SECONDARY, title_size=11, body_size=9.2)

        s_items = [
            ("Core Enterprise SAP Practice", "Implementation · Customization & BTP Extensions · AMS Support · System Integrations · Upgrades · S/4HANA System Conversion"),
            ("Data, AI & Analytics Practice", "Business Intelligence Services · Agentic AI Workflows · Generative AI Solutions · Data Engineering & Lakehouse Pipelines"),
            ("Digital Engineering & Edge", "Custom Enterprise Web Applications · Frontline Mobile Development · Industrial IoT Edge Solutions")
        ]
        for idx, (scat, snames) in enumerate(s_items):
            box_y = 2.90 + idx * 0.95
            self.add_card(s, rx + 0.15, box_y, col_w - 0.30, 0.85, bg_color=CARD_TINT, border_color=BORDER_ACCENT)
            self.add_text_block(s, rx + 0.25, box_y + 0.06, col_w - 0.50, 0.72,
                                title=scat, body=snames,
                                title_color=SAP_DEEP, body_color=TEXT_DARK, title_size=10, body_size=8.8)

        # Bottom Unifying Principle Box
        c_bridge = self.add_card(s, 0.80, 6.10, 11.733, 0.72, bg_color=CARD_TINT, border_color=BLUE_SAP, border_width=1.2)
        self.add_text_block(s, 0.95, 6.14, 11.433, 0.62,
                            title="HOW THEY OPERATE TOGETHER",
                            body="Products and services can be adopted independently or deployed as a synchronized solution. Products provide repeatable software capabilities; services ensure those capabilities are successfully integrated, governed, and adopted within each client's unique IT/OT landscape.",
                            bullets=["No pre-condition: Customers do not need to purchase Elitia software to engage Lumbini services, nor vice versa.",
                                     "When combined, they drastically reduce implementation friction and deliver end-to-end accountability."],
                            title_color=BLUE_SAP, body_color=TEXT_DARK, title_size=9.8, body_size=8.5)

        self.add_footer(s, 6)

    def build_slide_07(self):
        """Slide 7: The Enterprise Capability Map (Blueprint Canvas - Dark Navy)"""
        s = self.create_base_slide(is_dark=True)
        self.add_header(s, "Section II: How the Capabilities Fit Together", 
                        "The Enterprise Capability Map",
                        "REFERENCE ARCHITECTURE: Mapping group capabilities from corporate strategy to the physical shop-floor edge",
                        is_dark=True)

        # 5 Structured Horizontal Architecture Tiers
        tiers = [
            ("TIER 1: Strategy, Performance & Governance",
             "Executive Decisioning & Oversight",
             "Elitia BI · Enterprise BI Services (SAC / Power BI) · Elitia DGS · Data Governance Advisory · Master Data Stewardship",
             CYAN_ACCENT),
            ("TIER 2: Cognitive Augmentation & Workflows",
             "AI Agents & Ecosystem Collaboration",
             "Agentic AI Solutions (Deterministic Approval Gates) · Generative AI Assistants · Elitia Supplier Collaboration · Elitia Assessment Suite",
             PURPLE_ACCENT),
            ("TIER 3: Core Enterprise Applications",
             "Transactional Ledger & Clean Core",
             "SAP S/4HANA · SAP ECC · SAP BTP Extensions · Custom Enterprise Web Apps · Frontline Mobile Applications (iOS / Android)",
             BLUE_SAP),
            ("TIER 4: Integration Fabric & Data Foundations",
             "Semantic Data Highways & Governance",
             "SAP Integration Suite · API Management · Event Mesh · Elitia Migration Cockpit · Data Engineering (dbt / Spark / Lakehouse)",
             EMERALD_ACCENT),
            ("TIER 5: Manufacturing Operations & Edge OT",
             "Shop-Floor Execution & Physical Reality",
             "Elitia MES (Battery & Discrete Assembly) · Elitia EMS (Machine Energy Telemetry) · Industrial IoT Gateways (OPC UA / MQTT) · SCADA / PLCs",
             AMBER_ACCENT)
        ]

        ty_start = 1.60
        th = 0.88
        tgap = 0.14
        tw = 9.80

        for i, (thead, tsub, ttech, tcolor) in enumerate(tiers):
            y = ty_start + i * (th + tgap)
            self.add_card(s, 0.80, y, tw, th, bg_color=NAVY_SURFACE, border_color=NAVY_BORDER)
            
            # Left accent pill
            pill = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), Inches(y), Inches(0.18), Inches(th))
            pill.fill.solid()
            pill.fill.fore_color.rgb = tcolor
            pill.line.fill.background()

            # Text
            box = s.shapes.add_textbox(Inches(1.10), Inches(y + 0.08), Inches(tw - 0.40), Inches(th - 0.16))
            tf = box.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            
            p1 = tf.paragraphs[0]
            p1.text = f"{thead.upper()}  —  {tsub}"
            p1.font.name = FONT_FAMILY
            p1.font.size = Pt(10.5)
            p1.font.bold = True
            p1.font.color.rgb = tcolor
            p1.space_after = Pt(2)

            p2 = tf.add_paragraph()
            p2.text = ttech
            p2.font.name = FONT_FAMILY
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = TEXT_LIGHT

        # Right Flank: Cross-Cutting Architectural Controls
        cx = 10.75
        cw = 1.78
        ch = 4.96
        self.add_card(s, cx, ty_start, cw, ch, bg_color=NAVY_SURFACE_ALT, border_color=CYAN_ACCENT)
        
        # Header for flank
        fh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(ty_start), Inches(cw), Inches(0.35))
        fh.fill.solid()
        fh.fill.fore_color.rgb = CYAN_ACCENT
        fh.line.fill.background()
        p = fh.text_frame.paragraphs[0]
        p.text = "CROSS-CUTTING"
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_FAMILY
        p.font.size = Pt(9.0)
        p.font.bold = True
        p.font.color.rgb = NAVY_CANVAS

        self.add_text_block(s, cx + 0.08, ty_start + 0.40, cw - 0.16, ch - 0.45,
                            title="Security & ALM",
                            bullets=["Zero-Trust Role-Based Access (RBAC)",
                                     "End-to-end telemetry monitoring & audit logs",
                                     "Clean-Core compliance & upgrade protection"],
                            body="Operational controls wrap every layer to prevent unmonitored data drift.",
                            title_color=CYAN_ACCENT, body_color=TEXT_LIGHT_MUTED, title_size=10, body_size=8.2)

        # Bottom synthesis note
        sbox = self.add_card(s, 0.80, 6.64, 11.733, 0.22, bg_color=NAVY_SURFACE_ALT, border_color=None)
        tb_sn = s.shapes.add_textbox(Inches(0.90), Inches(6.65), Inches(11.533), Inches(0.20))
        p_sn = tb_sn.text_frame.paragraphs[0]
        p_sn.text = "ARCHITECTURAL REALITY: Not every integration is prebuilt or delivered out of the box. Capabilities are combined and mapped to client legacy systems via validated standards."
        p_sn.font.name = FONT_FAMILY
        p_sn.font.size = Pt(8.2)
        p_sn.font.bold = True
        p_sn.font.color.rgb = CYAN_ACCENT

        self.add_footer(s, 7, is_dark=True)

    def build_slide_08(self):
        """Slide 8: The Product and Service Portfolio"""
        s = self.create_base_slide(is_dark=False)
        self.add_header(s, "Section II: How the Capabilities Fit Together", 
                        "The Product and Service Portfolio",
                        "COMPLETE PORTFOLIO MAP: 7 purpose-built Elitia software products and 13 Lumbini Elite service practices")

        # Two Large Distinct Containers
        # Container Left: 7 Products (4.20" wide)
        pw = 4.20
        self.add_card(s, 0.80, 1.60, pw, 5.20, bg_color=CARD_WHITE, border_color=CARD_BORDER)
        
        ph = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), Inches(1.60), Inches(pw), Inches(0.38))
        ph.fill.solid()
        ph.fill.fore_color.rgb = BLUE_SAP
        ph.line.fill.background()
        p = ph.text_frame.paragraphs[0]
        p.text = "7 ELITIA SOFTWARE PRODUCTS"
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT

        prod_list = [
            ("1. Elitia MES", "Manufacturing Execution System connecting planning to shop-floor reality."),
            ("2. Elitia EMS", "Energy Monitoring System capturing machine-level utility consumption."),
            ("3. Elitia BI", "Decision-support analytics harmonizing cross-system operational KPIs."),
            ("4. Elitia Migration Cockpit", "Automated data validation engine for SAP ECC to S/4HANA migrations."),
            ("5. Elitia Supplier Collab.", "Supplier lifecycle collaboration, PO tracking, and milestone workflows."),
            ("6. Elitia Assessment Suite", "Calibrated technical candidate screening and interview workflow suite."),
            ("7. Elitia DGS", "Configurable Data Governance Suite for operational master data stewardship.")
        ]
        for i, (pname, pdesc) in enumerate(prod_list):
            py = 2.05 + i * 0.67
            self.add_card(s, 0.92, py, pw - 0.24, 0.60, bg_color=CARD_TINT, border_color=BORDER_ACCENT)
            self.add_text_block(s, 1.00, py + 0.04, pw - 0.40, 0.52,
                                title=pname, body=pdesc,
                                title_color=BLUE_SAP, body_color=TEXT_SECONDARY, title_size=9.5, body_size=8.0)

        # Container Right: 13 Services (7.30" wide)
        sw = 7.30
        sx = 5.233
        self.add_card(s, sx, 1.60, sw, 5.20, bg_color=CARD_WHITE, border_color=CARD_BORDER)
        
        sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(sx), Inches(1.60), Inches(sw), Inches(0.38))
        sh.fill.solid()
        sh.fill.fore_color.rgb = SAP_DEEP
        sh.line.fill.background()
        p = sh.text_frame.paragraphs[0]
        p.text = "13 LUMBINI ELITE SOLUTIONS & SERVICES PRACTICES"
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT

        # Sub-divide into 3 groups
        s_groups = [
            ("SAP Enterprise Practice (6 Categories)", SAP_DEEP, [
                ("1. SAP Implementation", "Full-lifecycle process design, fit-to-standard, and deployment."),
                ("2. SAP Customization", "Clean-core compliant BTP side-by-side & RAP/CAP extensions."),
                ("3. SAP Support & AMS", "L1-L3 ticket triage, root-cause problem reduction, and maintenance."),
                ("4. SAP Integrations", "API management, middleware integration, and event-driven fabric."),
                ("5. SAP System Upgrades", "Release lifecycle upgrades, SPDD/SPAU code remediation, and testing."),
                ("6. SAP System Conversion", "ECC to S/4HANA conversion, CVI integration, and ledger migration.")
            ]),
            ("Data & Applied AI Practice (4 Categories)", PURPLE_ACCENT, [
                ("7. BI & Analytics Services", "Semantic data modeling, KPI ontologies, and SAC/Power BI reporting."),
                ("8. Agentic AI Solutions", "Multi-agent autonomous task orchestration with human approval gates."),
                ("9. Generative AI Solutions", "Private domain RAG assistants, SOP search, and document summarization."),
                ("10. Data Engineering Services", "Scalable lakehouse pipelines, schema validation, and lineage modeling.")
            ]),
            ("Digital Engineering & Edge (3 Categories)", TEAL, [
                ("11. Custom App Development", "Modern web applications filling specialized operational white spaces."),
                ("12. Mobile App Development", "Offline-first native/hybrid mobile apps for field & shop-floor crews."),
                ("13. Custom IoT Solutions", "Industrial sensor connectivity, edge gateways, and protocol bridges.")
            ])
        ]

        cur_y = 2.05
        for gname, gcolor, items in s_groups:
            # Group header
            gh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(sx + 0.12), Inches(cur_y), Inches(sw - 0.24), Inches(0.24))
            gh.fill.solid()
            gh.fill.fore_color.rgb = gcolor
            gh.line.fill.background()
            p = gh.text_frame.paragraphs[0]
            p.text = gname
            p.font.name = FONT_FAMILY
            p.font.size = Pt(8.5)
            p.font.bold = True
            p.font.color.rgb = TEXT_LIGHT
            cur_y += 0.28

            # Items grid (2 columns)
            iw = (sw - 0.36) / 2
            for idx, (iname, idesc) in enumerate(items):
                r = idx // 2
                c = idx % 2
                ix = sx + 0.12 + c * (iw + 0.12)
                iy = cur_y + r * 0.48
                self.add_card(s, ix, iy, iw, 0.44, bg_color=CARD_TINT, border_color=CARD_BORDER)
                self.add_text_block(s, ix + 0.06, iy + 0.02, iw - 0.12, 0.40,
                                    title=iname, body=idesc,
                                    title_color=gcolor, body_color=TEXT_SECONDARY, title_size=8.5, body_size=7.5)
            rows = (len(items) + 1) // 2
            cur_y += rows * 0.48 + 0.06

        self.add_footer(s, 8)

    # -------------------------------------------------------------
    # SECTION III: ELITIA TECHNOLOGIES — PRODUCTS (Slides 9 to 15)
    # Standardized 7-question inquiry template for each product
    # -------------------------------------------------------------
    def render_product_slide(self, slide_num, prod_name, positioning, core_problem, 
                             hidden_truth, capabilities, enterprise_fit, stakeholders, 
                             discovery_q, complementary_services, visual_diagram_func):
        s = self.create_base_slide(is_dark=False)
        self.add_header(s, f"Section III: Elitia Technologies — Products", 
                        prod_name,
                        f"THE HIDDEN TRUTH: {hidden_truth}")

        # Top Information Strip: 3 Cards (Problem, Hidden Truth, Capabilities)
        top_cards = [
            ("1. Business Problem Addressed", core_problem, BLUE_SAP),
            ("2. The Less Obvious Reality", hidden_truth, AMBER_ACCENT),
            ("3. What the Product Delivers", capabilities, EMERALD_ACCENT)
        ]
        cw = 3.75
        gap = 0.24
        for i, (ctitle, cdesc, ccolor) in enumerate(top_cards):
            x = 0.80 + i * (cw + gap)
            self.add_card(s, x, 1.60, cw, 1.45, bg_color=CARD_WHITE, border_color=CARD_BORDER)
            # Header accent line
            top_line = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(1.60), Inches(cw), Inches(0.05))
            top_line.fill.solid()
            top_line.fill.fore_color.rgb = ccolor
            top_line.line.fill.background()

            if isinstance(cdesc, list):
                self.add_text_block(s, x + 0.12, 1.68, cw - 0.24, 1.30,
                                    title=ctitle, bullets=cdesc,
                                    title_color=ccolor, body_color=TEXT_SECONDARY, title_size=10.5, body_size=8.8)
            else:
                self.add_text_block(s, x + 0.12, 1.68, cw - 0.24, 1.30,
                                    title=ctitle, body=cdesc,
                                    title_color=ccolor, body_color=TEXT_SECONDARY, title_size=10.5, body_size=8.8)

        # Center Section: 50%+ Visual Diagram
        diag_card = self.add_card(s, 0.80, 3.15, 11.733, 2.05, bg_color=CARD_WHITE, border_color=CARD_BORDER)
        # Call specific diagram function
        visual_diagram_func(s, 0.80, 3.15, 11.733, 2.05)

        # Bottom Section: Stakeholders, Discovery Question & Complementary Services
        bot_cards = [
            ("4. Relevant Stakeholders", stakeholders, BLUE_SAP),
            ("5. Discovery Question for Clients", discovery_q, PURPLE_ACCENT),
            ("6. Complementary Group Capabilities", complementary_services, SAP_DEEP)
        ]
        for i, (btitle, bcontent, bcolor) in enumerate(bot_cards):
            x = 0.80 + i * (cw + gap)
            self.add_card(s, x, 5.30, cw, 1.45, bg_color=CARD_TINT, border_color=BORDER_ACCENT)
            if isinstance(bcontent, list):
                self.add_text_block(s, x + 0.12, 5.38, cw - 0.24, 1.30,
                                    title=btitle, bullets=bcontent,
                                    title_color=bcolor, body_color=TEXT_DARK, title_size=10, body_size=8.6)
            else:
                self.add_text_block(s, x + 0.12, 5.38, cw - 0.24, 1.30,
                                    title=btitle, body=bcontent,
                                    title_color=bcolor, body_color=TEXT_DARK, title_size=10, body_size=8.6)

        self.add_footer(s, slide_num)

    def build_slide_09(self):
        """Slide 9: Elitia MES"""
        def render_diagram(slide, x, y, w, h):
            # 4-stage horizontal manufacturing flow diagram
            stages = [
                ("SAP ERP Planning", "Production order dispatch, BOM explosion, and raw material allocations.", BLUE_SAP),
                ("Elitia MES Dispatch", "Work-order release, digital SOPs, operator sign-in, and tooling calibration.", TEAL),
                ("Shop-Floor Execution", "Battery cell-to-container genealogy, torque curves, and optical QA test logs.", PURPLE_ACCENT),
                ("ERP Confirmation", "Goods receipt, WIP balance clearing, scrap posting, and warranty genealogy.", EMERALD_ACCENT)
            ]
            sw = (w - 0.60 - 3 * 0.20) / 4
            for idx, (stitle, sdesc, scolor) in enumerate(stages):
                sx = x + 0.30 + idx * (sw + 0.20)
                # Stage box
                box = self.add_card(slide, sx, y + 0.30, sw, h - 0.60, bg_color=CARD_TINT, border_color=scolor)
                shdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(sx), Inches(y + 0.30), Inches(sw), Inches(0.28))
                shdr.fill.solid()
                shdr.fill.fore_color.rgb = scolor
                shdr.line.fill.background()
                p = shdr.text_frame.paragraphs[0]
                p.text = stitle
                p.font.name = FONT_FAMILY
                p.font.size = Pt(9.5)
                p.font.bold = True
                p.font.color.rgb = TEXT_LIGHT

                self.add_text_block(slide, sx + 0.08, y + 0.62, sw - 0.16, h - 0.96,
                                    body=sdesc, body_color=TEXT_DARK, body_size=8.5)
                
                # Connector arrow
                if idx < 3:
                    arr = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(sx + sw + 0.04), Inches(y + 0.95), Inches(0.12), Inches(0.18))
                    arr.fill.solid()
                    arr.fill.fore_color.rgb = scolor
                    arr.line.fill.background()

        self.render_product_slide(
            slide_num=9,
            prod_name="Elitia MES — Manufacturing Execution System",
            positioning="Manufacturing Execution System connecting production planning with shop-floor physical reality.",
            core_problem="Disconnect between scheduled ERP production orders and actual line execution, resulting in blind spots, unrecorded WIP, and manual QA paper logs.",
            hidden_truth="Knowing what production was planned is fundamentally different from knowing what actually happened on the shop floor.",
            capabilities=[
                "Real-time work-in-progress (WIP) tracking across discrete lines.",
                "High-precision battery cell-to-container genealogy and torque-tool data logging.",
                "Automated end-of-line (EOL) test data reconciliation with SAP production confirmations."
            ],
            enterprise_fit="Sits between SAP PP/MM and shop-floor PLCs/controllers to enforce execution rules.",
            stakeholders=[
                "Plant Managers & Operations Directors seeking scrap and throughput visibility.",
                "Quality Assurance Heads managing batch traceability and warranty liabilities.",
                "Manufacturing IT/OT leaders modernizing paper-based assembly lines."
            ],
            discovery_q="“When a quality deviation occurs on the assembly line, how many systems or shifts does it take to isolate the exact component batch, torque curve, and operator ID?”",
            complementary_services=[
                "SAP Integrations (Bi-directional PP/MM automated work-order confirmations).",
                "Custom IoT Solutions (Direct PLC, torque-tool, and test-bench connectivity).",
                "Mobile App Development (Frontline operator tablet interfaces and QA sign-offs)."
            ],
            visual_diagram_func=render_diagram
        )

    def build_slide_10(self):
        """Slide 10: Elitia EMS"""
        def render_diagram(slide, x, y, w, h):
            # Energy flow diagram
            stages = [
                ("Power Telemetry Capture", "Smart power meters, transformers, and gas flow sensors capture high-speed KW/KVA readings.", AMBER_ACCENT),
                ("Elitia EMS Aggregator", "Normalizes sensor telemetry, filters transient noise, and indexes by plant feeder.", TEAL),
                ("Operational Context", "Correlates utility spikes against active machine cycles, shift schedules, and idle states.", PURPLE_ACCENT),
                ("Targeted Intervention", "Dispatches peak demand alerts, optimizes load scheduling, and posts variance to SAP FI/CO.", EMERALD_ACCENT)
            ]
            sw = (w - 0.60 - 3 * 0.20) / 4
            for idx, (stitle, sdesc, scolor) in enumerate(stages):
                sx = x + 0.30 + idx * (sw + 0.20)
                box = self.add_card(slide, sx, y + 0.30, sw, h - 0.60, bg_color=CARD_TINT, border_color=scolor)
                shdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(sx), Inches(y + 0.30), Inches(sw), Inches(0.28))
                shdr.fill.solid()
                shdr.fill.fore_color.rgb = scolor
                shdr.line.fill.background()
                p = shdr.text_frame.paragraphs[0]
                p.text = stitle
                p.font.name = FONT_FAMILY
                p.font.size = Pt(9.5)
                p.font.bold = True
                p.font.color.rgb = TEXT_LIGHT

                self.add_text_block(slide, sx + 0.08, y + 0.62, sw - 0.16, h - 0.96,
                                    body=sdesc, body_color=TEXT_DARK, body_size=8.5)
                if idx < 3:
                    arr = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(sx + sw + 0.04), Inches(y + 0.95), Inches(0.12), Inches(0.18))
                    arr.fill.solid()
                    arr.fill.fore_color.rgb = scolor
                    arr.line.fill.background()

        self.render_product_slide(
            slide_num=10,
            prod_name="Elitia EMS — Energy Monitoring System",
            positioning="Energy Monitoring System providing granular visibility into consumption across equipment, utilities, and sites.",
            core_problem="Rising industrial utility costs and peak demand tariff penalties without visibility into which specific machines or shifts drive consumption spikes.",
            hidden_truth="An energy bill shows aggregate utility expenditure, but cannot explain where, when, or under what machine operating conditions that consumption occurred.",
            capabilities=[
                "High-frequency sub-meter and equipment-level electrical telemetry capture.",
                "Multi-site energy trend benchmarking and automated peak-demand penalty alerts.",
                "Correlation of utility draw against production order batches to calculate true unit cost."
            ],
            enterprise_fit="Ingests data via IoT gateways and feeds energy cost allocations directly to SAP CO.",
            stakeholders=[
                "Plant Directors & Operations Heads managing overall factory operating margins.",
                "Energy & Facilities Managers tasked with peak load shedding and tariff mitigation.",
                "Chief Sustainability Officers tracking carbon intensity and ESG audit disclosures."
            ],
            discovery_q="“Can your operations team correlate sudden utility demand charges to specific machine operating states, unoptimized idling, or off-shift HVAC schedules?”",
            complementary_services=[
                "Custom IoT Solutions (Industrial power sub-meter and PLC gateway connectivity).",
                "Data Engineering Services (Scalable time-series telemetry ingestion pipelines).",
                "BI & Analytics Services (Executive cross-plant sustainability dashboards)."
            ],
            visual_diagram_func=render_diagram
        )

    def build_slide_11(self):
        """Slide 11: Elitia BI"""
        def render_diagram(slide, x, y, w, h):
            stages = [
                ("Disparate Source Ingestion", "SAP S/4HANA, Elitia MES, legacy SQL databases, and machine spreadsheets.", BLUE_SAP),
                ("Semantic KPI Harmonization", "Unified metric ontology defining OEE, scrap percentage, and gross margins consistently.", PURPLE_ACCENT),
                ("Elitia BI Engine", "In-memory analytical caching, multi-dimensional drill-downs, and role-based views.", TEAL),
                ("Executive Decisioning", "CXO cockpits, plant supervisor tablets, and automated variance threshold alerts.", EMERALD_ACCENT)
            ]
            sw = (w - 0.60 - 3 * 0.20) / 4
            for idx, (stitle, sdesc, scolor) in enumerate(stages):
                sx = x + 0.30 + idx * (sw + 0.20)
                box = self.add_card(slide, sx, y + 0.30, sw, h - 0.60, bg_color=CARD_TINT, border_color=scolor)
                shdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(sx), Inches(y + 0.30), Inches(sw), Inches(0.28))
                shdr.fill.solid()
                shdr.fill.fore_color.rgb = scolor
                shdr.line.fill.background()
                p = shdr.text_frame.paragraphs[0]
                p.text = stitle
                p.font.name = FONT_FAMILY
                p.font.size = Pt(9.5)
                p.font.bold = True
                p.font.color.rgb = TEXT_LIGHT

                self.add_text_block(slide, sx + 0.08, y + 0.62, sw - 0.16, h - 0.96,
                                    body=sdesc, body_color=TEXT_DARK, body_size=8.5)
                if idx < 3:
                    arr = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(sx + sw + 0.04), Inches(y + 0.95), Inches(0.12), Inches(0.18))
                    arr.fill.solid()
                    arr.fill.fore_color.rgb = scolor
                    arr.line.fill.background()

        self.render_product_slide(
            slide_num=11,
            prod_name="Elitia BI — Business Intelligence & Operational Analytics",
            positioning="Business intelligence and operational analytics platform for enterprise decision-making.",
            core_problem="Fragmented reporting, conflicting departmental spreadsheets, and delayed executive visibility into plant-to-enterprise performance metrics.",
            hidden_truth="A dashboard creates business value only when it helps answer a specific operational decision, not simply because it displays more raw data.",
            capabilities=[
                "Role-based executive and operational KPI dashboards for manufacturing and enterprise.",
                "Cross-system reporting harmonizing shop-floor execution logs with SAP general ledgers.",
                "Automated operational variance tracking with drill-down to root-cause production batches."
            ],
            enterprise_fit="Acts as the presentation and semantic modeling layer across ERP, MES, and data marts.",
            stakeholders=[
                "Chief Executive & Operating Officers requiring daily operational clarity.",
                "Finance Directors analyzing plant-level manufacturing variances and gross margins.",
                "Operational Analytics Teams looking to replace brittle, manual spreadsheet compilation."
            ],
            discovery_q="“How much manual reconciliation happens in offline spreadsheets before your leadership team can agree on monthly manufacturing gross margins?”",
            complementary_services=[
                "Data Engineering Services (Data lakehouse pipelines and automated data quality).",
                "BI & Analytics Services (Customized Power BI, Tableau, or SAP Analytics Cloud builds).",
                "Elitia DGS (Ensuring underlying master data and KPI definitions remain governed)."
            ],
            visual_diagram_func=render_diagram
        )

    def build_slide_12(self):
        """Slide 12: Elitia Migration Cockpit"""
        def render_diagram(slide, x, y, w, h):
            stages = [
                ("Legacy ECC 6.0 Extraction", "Extracts master data, open transactions, GL balances, and historical records.", BLUE_SAP),
                ("Automated Profiling", "Runs schema rules, checks CVI customer-vendor mappings, and identifies orphan records.", PURPLE_ACCENT),
                ("Elitia Reconciliation Engine", "Executes 100% data comparison across source and target, flagging valuation discrepancies.", AMBER_ACCENT),
                ("Target S/4HANA Verification", "Validates clean migration cutover with auditable discrepancy logs and signed sign-offs.", EMERALD_ACCENT)
            ]
            sw = (w - 0.60 - 3 * 0.20) / 4
            for idx, (stitle, sdesc, scolor) in enumerate(stages):
                sx = x + 0.30 + idx * (sw + 0.20)
                box = self.add_card(slide, sx, y + 0.30, sw, h - 0.60, bg_color=CARD_TINT, border_color=scolor)
                shdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(sx), Inches(y + 0.30), Inches(sw), Inches(0.28))
                shdr.fill.solid()
                shdr.fill.fore_color.rgb = scolor
                shdr.line.fill.background()
                p = shdr.text_frame.paragraphs[0]
                p.text = stitle
                p.font.name = FONT_FAMILY
                p.font.size = Pt(9.5)
                p.font.bold = True
                p.font.color.rgb = TEXT_LIGHT

                self.add_text_block(slide, sx + 0.08, y + 0.62, sw - 0.16, h - 0.96,
                                    body=sdesc, body_color=TEXT_DARK, body_size=8.5)
                if idx < 3:
                    arr = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(sx + sw + 0.04), Inches(y + 0.95), Inches(0.12), Inches(0.18))
                    arr.fill.solid()
                    arr.fill.fore_color.rgb = scolor
                    arr.line.fill.background()

        self.render_product_slide(
            slide_num=12,
            prod_name="Elitia Migration Cockpit — SAP S/4HANA Data Validation",
            positioning="Data validation and reconciliation support platform for SAP ECC to SAP S/4HANA migration programs.",
            core_problem="High risk of financial ledger discrepancies, unmapped master data, and post-cutover operational disruption during S/4HANA conversions.",
            hidden_truth="A technically completed migration does not automatically establish that every critical business record and relational dependency is correct.",
            capabilities=[
                "Automated source-to-target field and relational data integrity comparisons.",
                "Pre-migration data quality profiling (identifying obsolete vendors and invalid tax codes).",
                "Reconciliation dashboards tracking financial balance carryforwards and open item clearing."
            ],
            enterprise_fit="Operates alongside standard SAP conversion tools as an independent, auditable validation gate.",
            stakeholders=[
                "SAP Program Leaders & Steering Committees managing cutover risk and project timelines.",
                "Enterprise Architects & Data Migration Leads responsible for data consistency.",
                "Business Data Owners and Corporate Controllers signing off on financial balance cutovers."
            ],
            discovery_q="“How will your program team verify that every relational balance—such as historical asset valuations and open purchase orders—transferred without silent corruption?”",
            complementary_services=[
                "SAP System Conversion Services (End-to-end technical conversion execution).",
                "Data Engineering Services (Data cleansing and legacy extraction scripting).",
                "Elitia DGS (Sustaining clean master data governance post-go-live)."
            ],
            visual_diagram_func=render_diagram
        )

    def build_slide_13(self):
        """Slide 13: Elitia Supplier Collaboration"""
        def render_diagram(slide, x, y, w, h):
            stages = [
                ("ERP Purchase Order Dispatch", "SAP MM/SRM automatically transmits POs, delivery schedules, and drawing specs.", BLUE_SAP),
                ("Supplier Portal Engagement", "Vendors receive notifications, confirm delivery milestones, and attach digital certs.", TEAL),
                ("Milestone Workflow Gate", "Automated escalation for overdue acknowledgments; exception routing for price/qty variances.", PURPLE_ACCENT),
                ("ERP Receipt & Inspection", "Advance shipping notices (ASN) feed warehouse docks; automated goods receipt matching.", EMERALD_ACCENT)
            ]
            sw = (w - 0.60 - 3 * 0.20) / 4
            for idx, (stitle, sdesc, scolor) in enumerate(stages):
                sx = x + 0.30 + idx * (sw + 0.20)
                box = self.add_card(slide, sx, y + 0.30, sw, h - 0.60, bg_color=CARD_TINT, border_color=scolor)
                shdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(sx), Inches(y + 0.30), Inches(sw), Inches(0.28))
                shdr.fill.solid()
                shdr.fill.fore_color.rgb = scolor
                shdr.line.fill.background()
                p = shdr.text_frame.paragraphs[0]
                p.text = stitle
                p.font.name = FONT_FAMILY
                p.font.size = Pt(9.5)
                p.font.bold = True
                p.font.color.rgb = TEXT_LIGHT

                self.add_text_block(slide, sx + 0.08, y + 0.62, sw - 0.16, h - 0.96,
                                    body=sdesc, body_color=TEXT_DARK, body_size=8.5)
                if idx < 3:
                    arr = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(sx + sw + 0.04), Inches(y + 0.95), Inches(0.12), Inches(0.18))
                    arr.fill.solid()
                    arr.fill.fore_color.rgb = scolor
                    arr.line.fill.background()

        self.render_product_slide(
            slide_num=13,
            prod_name="Elitia Supplier Collaboration — Supply Chain Lifecycle Platform",
            positioning="Supplier lifecycle collaboration and workflow platform connecting buyers with external supply ecosystems.",
            core_problem="Manual email/phone expediting, untracked delivery revisions, and supplier dispute delays causing production line stoppages.",
            hidden_truth="Digitizing supplier communication does not resolve who owns the next action, what is overdue, or which issue requires formal escalation.",
            capabilities=[
                "Centralized vendor workspace for real-time purchase order acknowledgment and milestone tracking.",
                "Digital document exchange (material test certificates, inspection sheets, commercial invoices).",
                "Automated SLA tracking with exception escalation for critical delivery and quality variances."
            ],
            enterprise_fit="Integrates with SAP MM and S/4HANA to keep purchasing records and logistics updated.",
            stakeholders=[
                "Chief Procurement Officers & Sourcing Heads managing supplier reliability.",
                "Supply Chain Planners & Expeditors seeking automated purchase order milestone visibility.",
                "Supplier Quality Directors requiring digital material certificates prior to shipping."
            ],
            discovery_q="“Where do your supplier commitments, delivery date revisions, and quality concession logs live today—in governed workflows or in personal inboxes?”",
            complementary_services=[
                "SAP Integrations (Automating bi-directional PO, ASN, and goods receipt flows).",
                "Agentic AI Solutions (Automated invoice and delivery discrepancy reconciliation).",
                "Custom Application Development (Tailored supplier onboarding and compliance portals)."
            ],
            visual_diagram_func=render_diagram
        )

    def build_slide_14(self):
        """Slide 14: Elitia Assessment Suite"""
        def render_diagram(slide, x, y, w, h):
            stages = [
                ("Role Specification", "Calibrated competencies defined for SAP consultants, data engineers, and AI developers.", BLUE_SAP),
                ("Automated Practical Screen", "Online coding, configuration scenarios, and architecture problem-solving challenges.", PURPLE_ACCENT),
                ("Panel Evaluation Rubric", "Structured evaluation scorecards standardizing technical depth and domain experience.", TEAL),
                ("Hiring Decision Audit", "Consolidated panel reviews, audit trail of scores, and automated ATS workflow integration.", EMERALD_ACCENT)
            ]
            sw = (w - 0.60 - 3 * 0.20) / 4
            for idx, (stitle, sdesc, scolor) in enumerate(stages):
                sx = x + 0.30 + idx * (sw + 0.20)
                box = self.add_card(slide, sx, y + 0.30, sw, h - 0.60, bg_color=CARD_TINT, border_color=scolor)
                shdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(sx), Inches(y + 0.30), Inches(sw), Inches(0.28))
                shdr.fill.solid()
                shdr.fill.fore_color.rgb = scolor
                shdr.line.fill.background()
                p = shdr.text_frame.paragraphs[0]
                p.text = stitle
                p.font.name = FONT_FAMILY
                p.font.size = Pt(9.5)
                p.font.bold = True
                p.font.color.rgb = TEXT_LIGHT

                self.add_text_block(slide, sx + 0.08, y + 0.62, sw - 0.16, h - 0.96,
                                    body=sdesc, body_color=TEXT_DARK, body_size=8.5)
                if idx < 3:
                    arr = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(sx + sw + 0.04), Inches(y + 0.95), Inches(0.12), Inches(0.18))
                    arr.fill.solid()
                    arr.fill.fore_color.rgb = scolor
                    arr.line.fill.background()

        self.render_product_slide(
            slide_num=14,
            prod_name="Elitia Assessment Suite — Technical Talent Evaluation Platform",
            positioning="Candidate assessment and recruitment workflow platform specialized for enterprise technology roles.",
            core_problem="High failure rate in technical hiring, inconsistent interviewer evaluation standards, and elongated recruitment cycle times for critical technology roles.",
            hidden_truth="Collecting subjective interview scores is not the same as conducting a consistent, role-relevant evaluation of technical capability.",
            capabilities=[
                "Role-specific assessment frameworks spanning SAP ERP, cloud engineering, data analytics, and AI/ML.",
                "Automated practical skill screening combined with structured offline interview rubrics.",
                "Collaborative panel approval workflows ensuring transparent, auditable hiring decisions."
            ],
            enterprise_fit="Integrates with corporate Applicant Tracking Systems (ATS) and HRIS platforms.",
            stakeholders=[
                "Talent Acquisition Leaders & Technical Recruiters screening high volumes of applicants.",
                "Engineering & Enterprise Practice Leads spending excessive billable hours on first-round interviews.",
                "Chief Human Resources Officers seeking objective benchmarks for technology talent."
            ],
            discovery_q="“How do your technical interviewers benchmark candidate capability objectively across specialized enterprise domains like SAP, Data, or AI?”",
            complementary_services=[
                "Generative AI Solutions (Automated candidate screening and job description harmonization).",
                "Custom Application Development (Integration with enterprise internal mobility portals).",
                "SAP Advisory Services (Domain expert vetting of enterprise solution architecture candidates)."
            ],
            visual_diagram_func=render_diagram
        )

    def build_slide_15(self):
        """Slide 15: Elitia DGS"""
        def render_diagram(slide, x, y, w, h):
            stages = [
                ("Master Data Ingestion", "Material masters, customer accounts, vendor records, and chart of accounts requests.", BLUE_SAP),
                ("Automated Rule Validation", "Runs deduplication algorithms, syntax verification, and mandatory business logic checks.", PURPLE_ACCENT),
                ("Stewardship Workflow", "Routes exceptions to designated business data stewards for review, adjustment, or sign-off.", AMBER_ACCENT),
                ("Governed ERP Publication", "Pushes approved, pristine master records directly into SAP MDG, S/4HANA, and data lakes.", EMERALD_ACCENT)
            ]
            sw = (w - 0.60 - 3 * 0.20) / 4
            for idx, (stitle, sdesc, scolor) in enumerate(stages):
                sx = x + 0.30 + idx * (sw + 0.20)
                box = self.add_card(slide, sx, y + 0.30, sw, h - 0.60, bg_color=CARD_TINT, border_color=scolor)
                shdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(sx), Inches(y + 0.30), Inches(sw), Inches(0.28))
                shdr.fill.solid()
                shdr.fill.fore_color.rgb = scolor
                shdr.line.fill.background()
                p = shdr.text_frame.paragraphs[0]
                p.text = stitle
                p.font.name = FONT_FAMILY
                p.font.size = Pt(9.5)
                p.font.bold = True
                p.font.color.rgb = TEXT_LIGHT

                self.add_text_block(slide, sx + 0.08, y + 0.62, sw - 0.16, h - 0.96,
                                    body=sdesc, body_color=TEXT_DARK, body_size=8.5)
                if idx < 3:
                    arr = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(sx + sw + 0.04), Inches(y + 0.95), Inches(0.12), Inches(0.18))
                    arr.fill.solid()
                    arr.fill.fore_color.rgb = scolor
                    arr.line.fill.background()

        self.render_product_slide(
            slide_num=15,
            prod_name="Elitia DGS — Configurable Data Governance Suite",
            positioning="Configurable Data Governance Suite for operational enterprise data governance, validation, and stewardship.",
            core_problem="Pervasive data decay, duplicate customer/vendor records, and unmonitored master data creation disrupting downstream billing and supply chains.",
            hidden_truth="Data governance becomes operational when ownership and validation rules influence daily work rather than existing only in policy documents.",
            capabilities=[
                "Configurable data stewardship workflows and role-based approval routing.",
                "Automated data-quality validation rules catching errors prior to ledger commit.",
                "Governance reporting and audit tracking for enterprise master and reference data."
            ],
            enterprise_fit="Complements or extends SAP MDG by providing lightweight, agile operational governance.",
            stakeholders=[
                "Chief Data Officers & Enterprise Data Governance Leaders driving data trust.",
                "Master Data Managers responsible for material, vendor, and customer data consistency.",
                "Business Process Owners tired of correcting invoice errors caused by flawed master data."
            ],
            discovery_q="“When an invalid vendor record or material master attribute enters your system, does a governance rule stop it, or does downstream invoicing fail first?”",
            complementary_services=[
                "Data Engineering Services (Data quality profiling and pipeline cleanup).",
                "SAP Implementation & Conversion (Establishing clean master data standards).",
                "Business Intelligence Services (Operational data-quality audit reporting)."
            ],
            visual_diagram_func=render_diagram
        )

    # -------------------------------------------------------------
    # SECTION IV: LUMBINI ELITE SOLUTIONS & SERVICES (Slides 16 to 28)
    # Standardized inquiry template for each of the 13 services
    # -------------------------------------------------------------
    def render_service_slide(self, slide_num, service_name, category_tag, subtitle_text,
                             problem_statement, underlying_challenge, what_we_do,
                             activities_deliverables, operating_model_role, 
                             relevant_tech, trigger_situations):
        s = self.create_base_slide(is_dark=False)
        self.add_header(s, f"Section IV: Lumbini Elite Solutions & Services  ·  {category_tag}", 
                        service_name,
                        subtitle_text)

        # 3 Top Columns: Problem, Underlying Challenge, What We Do
        cw = 3.75
        gap = 0.24
        
        top_cards = [
            ("1. Business Problem Addressed", problem_statement, BLUE_SAP),
            ("2. Underlying Challenge", underlying_challenge, AMBER_ACCENT),
            ("3. What Lumbini Elite Delivers", what_we_do, EMERALD_ACCENT)
        ]
        for i, (ctitle, ccontent, ccolor) in enumerate(top_cards):
            x = 0.80 + i * (cw + gap)
            self.add_card(s, x, 1.60, cw, 2.40, bg_color=CARD_WHITE, border_color=CARD_BORDER)
            top_line = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(1.60), Inches(cw), Inches(0.05))
            top_line.fill.solid()
            top_line.fill.fore_color.rgb = ccolor
            top_line.line.fill.background()

            if isinstance(ccontent, list):
                self.add_text_block(s, x + 0.12, 1.70, cw - 0.24, 2.20,
                                    title=ctitle, bullets=ccontent,
                                    title_color=ccolor, body_color=TEXT_SECONDARY, title_size=11, body_size=9.0)
            else:
                self.add_text_block(s, x + 0.12, 1.70, cw - 0.24, 2.20,
                                    title=ctitle, body=ccontent,
                                    title_color=ccolor, body_color=TEXT_SECONDARY, title_size=11, body_size=9.0)

        # 4 Bottom Columns: Deliverables, Operating Model Fit, Technologies, Trigger Situations
        bot_w = 2.75
        bot_gap = 0.244
        bot_cards = [
            ("Typical Deliverables", activities_deliverables, BLUE_SAP),
            ("Operating Model Role", operating_model_role, SAP_DEEP),
            ("Relevant Technologies", relevant_tech, PURPLE_ACCENT),
            ("When Clients Need This", trigger_situations, TEAL)
        ]
        for i, (btitle, bcontent, bcolor) in enumerate(bot_cards):
            x = 0.80 + i * (bot_w + bot_gap)
            self.add_card(s, x, 4.15, bot_w, 2.60, bg_color=CARD_TINT, border_color=BORDER_ACCENT)
            
            # Header strip
            bhdr = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(4.15), Inches(bot_w), Inches(0.28))
            bhdr.fill.solid()
            bhdr.fill.fore_color.rgb = bcolor
            bhdr.line.fill.background()
            p = bhdr.text_frame.paragraphs[0]
            p.text = btitle
            p.font.name = FONT_FAMILY
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = TEXT_LIGHT

            if isinstance(bcontent, list):
                self.add_text_block(s, x + 0.10, 4.48, bot_w - 0.20, 2.20,
                                    bullets=bcontent, body_color=TEXT_DARK, body_size=8.5)
            else:
                self.add_text_block(s, x + 0.10, 4.48, bot_w - 0.20, 2.20,
                                    body=bcontent, body_color=TEXT_DARK, body_size=8.5)

        self.add_footer(s, slide_num)

    def build_slide_16(self):
        """Slide 16: SAP Implementation"""
        self.render_service_slide(
            slide_num=16,
            service_name="SAP Implementation Services",
            category_tag="Enterprise SAP Practice",
            subtitle_text="PROCESS DESIGN OVER SOFTWARE: Establishing business capabilities, process contracts, and decision ownership",
            problem_statement="Organizations adopting modern ERP frequently struggle with misalignment between software capabilities, operating processes, and actual organizational readiness.",
            underlying_challenge="Treating SAP implementation as a software installation rather than the fundamental redesign of operating processes, data models, and business decision rights.",
            what_we_do=[
                "End-to-end implementation lifecycle from discovery to stabilization.",
                "Fit-to-standard process analysis aligned with industry best practices.",
                "Disciplined configuration, clean-core extensions, testing, and cutover."
            ],
            activities_deliverables=[
                "Enterprise Business Blueprint & Target Operating Model.",
                "SAP S/4HANA Configuration & Extension Rationale.",
                "End-to-End Integration Test Scenarios & Cutover Playbook."
            ],
            operating_model_role="Establishes the central transactional backbone, universal general ledger, and standardized business processes for the entire organization.",
            relevant_tech=[
                "SAP S/4HANA (Cloud / On-Premise)",
                "SAP Activate Methodology",
                "SAP Best Practice Process Frameworks"
            ],
            trigger_situations=[
                "Greenfield ERP implementations for scaling enterprises.",
                "Consolidation of disparate legacy accounting systems.",
                "Corporate restructuring, M&A integrations, or new entity launches."
            ]
        )

    def build_slide_17(self):
        """Slide 17: SAP Customization and Enhancements"""
        self.render_service_slide(
            slide_num=17,
            service_name="SAP Customization and Enhancements",
            category_tag="Enterprise SAP Practice",
            subtitle_text="CLEAN-CORE STRATEGY: Accommodating differentiated workflows while strictly ring-fencing the upgradeable core",
            problem_statement="Standard ERP functionality cannot accommodate unique competitive advantages or complex regulatory rules, leading to frustrated users.",
            underlying_challenge="Customizing standard ERP on-stack without architecture discipline creates crippling technical debt that makes future upgrades cost-prohibitive.",
            what_we_do=[
                "Engineers Clean-Core compliant side-by-side extensions on SAP BTP.",
                "Builds modern SAP Fiori user interfaces tailored to operational tasks.",
                "Refactors legacy on-stack modifications into loosely coupled microservices."
            ],
            activities_deliverables=[
                "Clean-Core Architecture Compliance Specifications.",
                "SAP BTP Extension Packages (Cloud Application Programming model).",
                "Automated ABAP Test Cockpit (ATC) Quality & Upgrade Gates."
            ],
            operating_model_role="Enables the business to execute proprietary, differentiated workflows without compromising the stability and upgradeability of standard ERP.",
            relevant_tech=[
                "SAP Business Technology Platform (BTP)",
                "ABAP RESTful Application Programming (RAP)",
                "SAP Fiori / UI5 & Cloud App Programming (CAP)"
            ],
            trigger_situations=[
                "Proprietary manufacturing dispatch or pricing algorithms.",
                "Complex regional statutory compliance or tax calculations.",
                "Prerequisite custom code cleanup for S/4HANA cloud upgrades."
            ]
        )

    def build_slide_18(self):
        """Slide 18: SAP Support and Application Maintenance"""
        self.render_service_slide(
            slide_num=18,
            service_name="SAP Support and Application Maintenance (AMS)",
            category_tag="Enterprise SAP Practice",
            subtitle_text="ROOT-CAUSE ELIMINATION: Transitioning from endless firefighting to structural stabilization and performance improvement",
            problem_statement="High recurring application support costs, repetitive ticket backlogs, and unplanned system downtime draining IT management bandwidth.",
            underlying_challenge="Repeatedly resolving visible incident symptoms without analyzing recurring process friction, user training deficits, or configuration drift.",
            what_we_do=[
                "L1-L3 SLA-governed functional and technical incident resolution.",
                "Proactive problem management and root-cause remediation programs.",
                "Managed change request execution, release coordination, and patch testing."
            ],
            activities_deliverables=[
                "24/7 Managed Support Desk & Incident SLA Reports.",
                "Root-Cause Analysis (RCA) & Defect Elimination Backlog.",
                "Monthly Performance Reviews & Continuous Improvement Plans."
            ],
            operating_model_role="Safeguards everyday business continuity, prevents operational disruption, and continually refines enterprise software performance.",
            relevant_tech=[
                "SAP Solution Manager & SAP Cloud ALM",
                "ServiceNow & Jira Service Management",
                "ITIL v4 Service Management Standards"
            ],
            trigger_situations=[
                "Post-go-live hypercare transition into steady-state operations.",
                "Internal IT teams overburdened with routine ticket management.",
                "Need for guaranteed 24/7 round-the-clock technical coverage."
            ]
        )

    def build_slide_19(self):
        """Slide 19: SAP Integrations"""
        self.render_service_slide(
            slide_num=19,
            service_name="SAP Integrations",
            category_tag="Enterprise SAP Practice",
            subtitle_text="SEMANTIC INTEGRATION: Systems must not only exchange raw data, but interpret and act upon it with business context",
            problem_statement="Isolated information silos, brittle point-to-point batch scripts, and data latency between SAP and shop-floor, logistics, or SaaS systems.",
            underlying_challenge="An integration is not complete simply because two systems exchange data packets; the receiving system must validate and interpret context correctly.",
            what_we_do=[
                "Architects event-driven and API-led integration architectures.",
                "Connects SAP with MES, CRM, e-commerce, banking, and 3PL partners.",
                "Implements centralized error-handling, payload validation, and replay queues."
            ],
            activities_deliverables=[
                "Enterprise Interface Catalog & API Mapping Matrix.",
                "SAP Integration Suite Pre-packaged Integration Flows.",
                "Automated Error Reconciliation & Alerting Dashboards."
            ],
            operating_model_role="Ensures coherent, real-time data flows between central business systems, customer touchpoints, and operational execution.",
            relevant_tech=[
                "SAP Integration Suite (Cloud Integration, API Management)",
                "SAP Event Mesh & Kafka Event Streams",
                "OData, REST, SOAP, and EDI Standards"
            ],
            trigger_situations=[
                "MES-to-ERP real-time shop-floor synchronization.",
                "Multi-cloud SaaS application integration (Salesforce, Workday).",
                "Supplier and 3PL logistics EDI automation."
            ]
        )

    def build_slide_20(self):
        """Slide 20: SAP System Upgrades"""
        self.render_service_slide(
            slide_num=20,
            service_name="SAP System Upgrades",
            category_tag="Enterprise SAP Practice",
            subtitle_text="LIFECYCLE CONTINUITY: Managing vendor release roadmaps and security mandates without operational downtime risk",
            problem_statement="Outdated software versions facing vendor end-of-maintenance, unpatched security vulnerabilities, and inability to run modern cloud features.",
            underlying_challenge="Managing complex cross-system dependencies, database sizing, and business continuity risks without prolonged production downtime.",
            what_we_do=[
                "Comprehensive upgrade technical readiness and compatibility assessments.",
                "SPDD/SPAU custom code adjustment and database remediation.",
                "Full sandbox rehearsals, minimal-downtime cutover, and post-upgrade testing."
            ],
            activities_deliverables=[
                "Upgrade Feasibility & Dependency Impact Report.",
                "Custom Code Remediation & Deprecation Analysis.",
                "Rehearsed Minimal-Downtime Cutover Playbook."
            ],
            operating_model_role="Keeps the enterprise digital core secure, supported, and positioned to take advantage of continuous vendor innovation.",
            relevant_tech=[
                "SAP Software Update Manager (SUM) with DMO",
                "SAP Maintenance Planner & Readiness Check",
                "SAP EarlyWatch Alert & Solution Manager"
            ],
            trigger_situations=[
                "Approaching vendor end-of-support deadlines for older releases.",
                "Prerequisite technical upgrade before S/4HANA migration.",
                "Mandatory database migrations to SAP HANA in-memory."
            ]
        )

    def build_slide_21(self):
        """Slide 21: SAP System Conversion"""
        self.render_service_slide(
            slide_num=21,
            service_name="SAP System Conversion",
            category_tag="Enterprise SAP Practice",
            subtitle_text="SYSTEM TRANSFORMATION: Converting legacy ECC systems into in-memory S/4HANA platforms while preserving data lineage",
            problem_statement="Organizations running legacy SAP ECC need to transition to SAP S/4HANA without losing historical financial and operational data.",
            underlying_challenge="Distinguishing a true business system conversion (CVI, New GL, Simplification Items) from a simple technical software upgrade.",
            what_we_do=[
                "Pre-conversion readiness assessments and Simplification Item reviews.",
                "Executes Customer-Vendor Integration (CVI) and Business Partner conversion.",
                "Manages financial ledger conversion, custom code adaptation, and cutover."
            ],
            activities_deliverables=[
                "S/4HANA Conversion Readiness & Simplification Analysis.",
                "CVI Business Partner Harmonization Strategy.",
                "Simulated Cutover Rehearsal Logs & Sign-Off Documentation."
            ],
            operating_model_role="Transforms legacy transactional engines into real-time, in-memory analytical and execution platforms for the intelligent enterprise.",
            relevant_tech=[
                "SAP S/4HANA Readiness Check 2.0",
                "ABAP Test Cockpit (ATC) with S/4HANA Checks",
                "Software Update Manager (SUM) Database Migration Option"
            ],
            trigger_situations=[
                "Corporate transition mandates from SAP ECC 6.0 to S/4HANA.",
                "Desire to preserve historical transactional data without greenfield rebuild.",
                "Consolidation onto modern in-memory data structures."
            ]
        )

    def build_slide_22(self):
        """Slide 22: Business Intelligence and Analytics Services"""
        self.render_service_slide(
            slide_num=22,
            service_name="Business Intelligence and Analytics Services",
            category_tag="Data & Applied AI Practice",
            subtitle_text="DECISION ARCHITECTURE: Establishing single-source metric definitions before deploying visualization dashboards",
            problem_statement="Fragmented executive reporting, contradictory spreadsheet numbers, and inability to correlate plant operational metrics with finance.",
            underlying_challenge="Reporting failures originate in inconsistent metric definitions and absent data ownership rather than a shortage of visualization tools.",
            what_we_do=[
                "Designs enterprise KPI ontologies and single-source-of-truth data models.",
                "Builds interactive executive, financial, and operational reporting dashboards.",
                "Implements self-service analytics frameworks with governed semantic layers."
            ],
            activities_deliverables=[
                "Enterprise Metric Dictionary & Governance Framework.",
                "Semantic Data Models & Dimensional Schemas.",
                "Executive CXO Dashboards & Automated Variance Reports."
            ],
            operating_model_role="Converts raw transactional and operational events into trustworthy, actionable intelligence for leadership decision-making.",
            relevant_tech=[
                "Power BI, Tableau & Apache Superset",
                "SAP Analytics Cloud (SAC) & SAP Datasphere",
                "SQL, Star-Schema Modeling & DAX"
            ],
            trigger_situations=[
                "Disjointed executive board and management reporting.",
                "Lack of visibility into real-time manufacturing and financial variances.",
                "Need to replace fragile, manual month-end spreadsheet compilation."
            ]
        )

    def build_slide_23(self):
        """Slide 23: Agentic AI Solutions"""
        self.render_service_slide(
            slide_num=23,
            service_name="Agentic AI Solutions",
            category_tag="Data & Applied AI Practice",
            subtitle_text="GOVERNED AUTONOMY: Autonomous AI agents require deterministic boundary constraints and explicit human-in-the-loop authorization gates",
            problem_statement="Complex, multi-step knowledge workflows that require employees to manually coordinate between multiple disconnected systems.",
            underlying_challenge="An AI system's ability to suggest an action is fundamentally different from its authority to execute that action in enterprise systems.",
            what_we_do=[
                "Designs multi-agent workflows with explicit deterministic boundary guardrails.",
                "Builds autonomous task execution for procurement, operations, and support.",
                "Integrates human-in-the-loop approval gates for high-value transactions."
            ],
            activities_deliverables=[
                "Multi-Agent Workflow Architecture & Action Permissions Matrix.",
                "Deterministic Business Rule & Policy Guardrails.",
                "Audit Trail & Telemetry Logging for Autonomous Operations."
            ],
            operating_model_role="Coordinates routine multi-system business actions autonomously while maintaining strict human governance and compliance.",
            relevant_tech=[
                "LangGraph, Semantic Kernel & FastMCP",
                "Enterprise Agent Orchestration Platforms",
                "Deterministic Business Rule Engines & OIDC Auth"
            ],
            trigger_situations=[
                "Automated triage and resolution of procurement discrepancies.",
                "Multi-step customer service inquiry and order modification routing.",
                "Automated invoice reconciliation across unstructured supplier documents."
            ]
        )

    def build_slide_24(self):
        """Slide 24: Generative AI Solutions"""
        self.render_service_slide(
            slide_num=24,
            service_name="Generative AI Solutions",
            category_tag="Data & Applied AI Practice",
            subtitle_text="GROUNDED INTELLIGENCE: Fluent answers are useless without verifiable source grounding, strict access control, and privacy protections",
            problem_statement="Knowledge workers spend hours searching scattered PDFs, technical documentation, and legacy wikis to answer operational questions.",
            underlying_challenge="A fluent answer is not necessarily a correct answer, and an ungrounded model will hallucinate with high confidence.",
            what_we_do=[
                "Deploys private, enterprise-grounded Retrieval-Augmented Generation (RAG).",
                "Builds domain-specific knowledge assistants for SOPs, engineering, and HR.",
                "Enforces strict role-based document access, redaction, and audit verification."
            ],
            activities_deliverables=[
                "Enterprise Grounded RAG Architecture & Vector Indexing.",
                "Domain-Specific Knowledge Assistant Applications.",
                "Hallucination Verification Benchmarks & Access Controls."
            ],
            operating_model_role="Augments workforce cognitive productivity by unlocking trapped institutional knowledge without compromising intellectual property.",
            relevant_tech=[
                "Enterprise LLMs (Gemini, Claude, GPT-4)",
                "Vector Databases (pgvector, ChromaDB, Qdrant)",
                "RAG Frameworks & Document Ingestion Pipelines"
            ],
            trigger_situations=[
                "Field service and plant technicians searching complex equipment SOPs.",
                "Accelerating technical bid, RFP, and commercial proposal drafting.",
                "Internal policy, IT helpdesk, and employee self-service query automation."
            ]
        )

    def build_slide_25(self):
        """Slide 25: Custom Application Development"""
        self.render_service_slide(
            slide_num=25,
            service_name="Custom Application Development",
            category_tag="Digital Engineering & Edge",
            subtitle_text="TARGETED EXTENSIONS: Engineering tailored applications that fit directly into enterprise architecture without creating unmaintainable silos",
            problem_statement="Commercial off-the-shelf software fails to address specialized operational processes, forcing teams into unmanaged spreadsheets.",
            underlying_challenge="Building point tools without enterprise architecture rigor results in fragile, unmaintainable shadow IT silos.",
            what_we_do=[
                "Full-lifecycle modern enterprise web application design and development.",
                "Engineers secure RESTful and GraphQL APIs linked to core systems.",
                "Builds responsive, accessible web portals for employees, clients, and partners."
            ],
            activities_deliverables=[
                "Enterprise Solution Architecture & Microservice Blueprints.",
                "Production-Grade Responsive Web Applications (React / TypeScript).",
                "Automated CI/CD Pipelines & Operational Handover Manuals."
            ],
            operating_model_role="Fills specialized operational white spaces with agile, modern digital interfaces connected directly to the enterprise core.",
            relevant_tech=[
                "React, TypeScript & Modern UI Frameworks",
                "Python (FastAPI / Django), Node.js & Go",
                "PostgreSQL, Redis, Docker & Kubernetes"
            ],
            trigger_situations=[
                "Specialized shop-floor tracking tools not covered by standard software.",
                "Custom customer-facing order tracking and service booking portals.",
                "Internal workflow automation replacing high-risk manual spreadsheets."
            ]
        )

    def build_slide_26(self):
        """Slide 26: Mobile Application Development"""
        self.render_service_slide(
            slide_num=26,
            service_name="Mobile Application Development",
            category_tag="Digital Engineering & Edge",
            subtitle_text="FRONTLINE EXECUTION: Purpose-built mobile experiences designed for shop-floor operators and field crews, not miniaturized desktop screens",
            problem_statement="Frontline field engineers, plant supervisors, and inspectors cannot access enterprise systems at the physical point of work.",
            underlying_challenge="Moving a desktop browser screen onto a mobile phone does not make the workflow usable in industrial field conditions.",
            what_we_do=[
                "Designs mobile-first applications optimized for touch, rugged devices, and gloves.",
                "Builds robust offline-first data caching and automatic background synchronization.",
                "Integrates mobile hardware features: barcode scanners, cameras, GPS, and RFID."
            ],
            activities_deliverables=[
                "Field UI/UX Journey Maps & Wireframe Design System.",
                "Production iOS & Android Enterprise Applications.",
                "Offline-First Synchronization Engine & Device Security Rules."
            ],
            operating_model_role="Extends enterprise transactional execution, inspections, and task sign-offs directly to frontline workers at the physical point of work.",
            relevant_tech=[
                "Flutter & React Native Cross-Platform",
                "Native iOS (Swift) & Android (Kotlin)",
                "SQLite Offline Sync & Mobile Device Management (MDM)"
            ],
            trigger_situations=[
                "Field service asset inspection and work-order management.",
                "Shop-floor supervisor quality audits and approval sign-offs.",
                "Warehouse inventory receiving, barcode scanning, and stock counts."
            ]
        )

    def build_slide_27(self):
        """Slide 27: Custom IoT Solutions"""
        self.render_service_slide(
            slide_num=27,
            service_name="Custom IoT Solutions",
            category_tag="Digital Engineering & Edge",
            subtitle_text="PHYSICAL-TO-DIGITAL BRIDGE: Machine telemetry generates value only when contextualized with production orders and operating states",
            problem_statement="Valuable operational machine data remains trapped inside legacy PLCs, sensors, and remote site equipment with zero enterprise visibility.",
            underlying_challenge="Collecting massive volumes of raw sensor data creates noise unless that data is contextualized with active production and maintenance records.",
            what_we_do=[
                "Deploys industrial edge gateways and protocol translation hardware.",
                "Connects legacy and modern PLCs using standard OPC UA, Modbus, and MQTT.",
                "Implements edge stream filtering and automated anomaly alert rules."
            ],
            activities_deliverables=[
                "Industrial Edge Architecture & Protocol Mapping Blueprint.",
                "Hardened Edge Gateway Deployments & Telemetry Pipelines.",
                "Real-Time Edge Health Monitoring & Maintenance Rules."
            ],
            operating_model_role="Bridges the physical-to-digital divide, feeding real-time operational truth into execution systems, analytics, and enterprise ledgers.",
            relevant_tech=[
                "OPC UA, MQTT, Modbus & Profinet",
                "Industrial Edge Gateways (Advantech, Siemens, Moxa)",
                "Time-Series Databases (TimescaleDB, InfluxDB, AWS IoT Core)"
            ],
            trigger_situations=[
                "Condition monitoring and predictive health on critical rotating assets.",
                "Connecting legacy manufacturing machines lacking native IT interfaces.",
                "Remote environmental, utility, and power generation monitoring."
            ]
        )

    def build_slide_28(self):
        """Slide 28: Data Engineering Services"""
        self.render_service_slide(
            slide_num=28,
            service_name="Data Engineering Services",
            category_tag="Data & Applied AI Practice",
            subtitle_text="FOUNDATIONAL INTEGRITY: Advanced analytics and AI initiatives remain brittle when underlying data pipelines lack lineage and validation",
            problem_statement="Fragmented data pipelines, unreliable batch updates, conflicting schemas, and poor data quality crippling analytics and AI programs.",
            underlying_challenge="An AI or analytics initiative cannot succeed when the underlying data foundation is inconsistent, unvalidated, or lacks clear lineage.",
            what_we_do=[
                "Architects resilient, scalable batch and streaming data lakehouse pipelines.",
                "Implements automated data quality testing, schema validation, and alerts.",
                "Establishes end-to-end data lineage tracking and semantic data modeling."
            ],
            activities_deliverables=[
                "Modern Data Lakehouse Architecture & Pipeline Blueprints.",
                "Automated Data Cleansing & Transformation Models (dbt / Spark).",
                "Automated Data Quality Monitoring & Lineage Catalog."
            ],
            operating_model_role="Builds the reliable, observable, and governed data foundation that powers enterprise reporting, AI algorithms, and operational systems.",
            relevant_tech=[
                "Apache Spark, Databricks, Snowflake & BigQuery",
                "dbt (data build tool) & Apache Airflow / Dagster",
                "Kafka, Iceberg, Delta Lake & Great Expectations"
            ],
            trigger_situations=[
                "High data pipeline failure rates and delayed month-end reporting.",
                "Preparation of enterprise data assets for generative AI or ML models.",
                "Migration from legacy on-premise data warehouses to modern lakehouses."
            ]
        )

    # -------------------------------------------------------------
    # SECTION V: BRINGING THE CAPABILITIES TOGETHER (Slides 29 to 34)
    # -------------------------------------------------------------
    def build_slide_29(self):
        """Slide 29: From Individual Capabilities to Connected Solutions"""
        s = self.create_base_slide(is_dark=False)
        self.add_header(s, "Section V: Bringing the Capabilities Together", 
                        "From Individual Capabilities to Connected Solutions",
                        "SYNERGISTIC SOLUTIONS: How targeted products and specialized services combine to solve multi-dimensional enterprise challenges")

        # 8 Solution Combinations (4x2 Grid)
        combos = [
            ("1. Production Visibility & Traceability",
             "Elitia MES  +  SAP Integrations  +  Manufacturing Analytics",
             "Connects ERP production orders directly to shop-floor lines, capturing cell-to-container genealogy and feeding automated confirmations to SAP."),
            ("2. Industrial Energy Management",
             "Elitia EMS  +  Custom IoT Solutions  +  Financial Analytics",
             "Deploys IoT power meters across plant feeders, captures machine-level demand telemetry, and attributes energy variance to specific production batches."),
            ("3. SAP S/4HANA Migration Validation",
             "Elitia Migration Cockpit  +  SAP System Conversion Services",
             "Executes end-to-end technical system conversion while providing automated source-to-target data reconciliation and financial sign-off audits."),
            ("4. Closed-Loop Supplier Coordination",
             "Elitia Supplier Collab.  +  SAP Integrations  +  Mobile Apps",
             "Provides vendors with real-time PO visibility, tracks delivery milestones, and enables warehouse dock receiving via frontline mobile barcode scanning."),
            ("5. Operational Data Governance",
             "Elitia DGS  +  Data Engineering Services  +  SAP Advisory",
             "Cleanses legacy master data assets, establishes automated validation rules at point of entry, and maintains data quality through active stewardship."),
            ("6. Executive Decision Intelligence",
             "Elitia BI  +  BI Services (SAC / Power BI)  +  Data Pipelines",
             "Harmonizes plant-level operational metrics with corporate financial ledgers, delivering unified executive cockpits with automated variance alerts."),
            ("7. Governed Enterprise AI Automation",
             "Agentic AI Solutions  +  Enterprise Integrations  +  Human Gates",
             "Automates multi-system procurement and service workflows with deterministic business boundary rules and mandatory human approval gateways."),
            ("8. Frontline Operations Digitization",
             "Custom Web & Mobile Apps  +  Custom IoT  +  Core SAP",
             "Replaces error-prone shop-floor spreadsheets with tailored operator tablets connected to machine PLCs and synchronized with ERP ledgers.")
        ]

        cw = 2.75
        ch = 2.38
        gx = 0.244
        gy = 0.20
        sy = 1.60

        for idx, (title, formula, impact) in enumerate(combos):
            r = idx // 4
            c = idx % 4
            x = 0.80 + c * (cw + gx)
            y = sy + r * (ch + gy)

            self.add_card(s, x, y, cw, ch, bg_color=CARD_WHITE, border_color=CARD_BORDER)
            
            # Header
            hdr = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(cw), Inches(0.28))
            hdr.fill.solid()
            hdr.fill.fore_color.rgb = BLUE_SAP if r == 0 else SAP_DEEP
            hdr.line.fill.background()
            p = hdr.text_frame.paragraphs[0]
            p.text = title
            p.font.name = FONT_FAMILY
            p.font.size = Pt(9.0)
            p.font.bold = True
            p.font.color.rgb = TEXT_LIGHT

            # Content
            box = s.shapes.add_textbox(Inches(x + 0.10), Inches(y + 0.32), Inches(cw - 0.20), Inches(ch - 0.36))
            tf = box.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

            p_f = tf.paragraphs[0]
            p_f.text = formula
            p_f.font.name = FONT_FAMILY
            p_f.font.size = Pt(8.5)
            p_f.font.bold = True
            p_f.font.color.rgb = BLUE_SAP
            p_f.space_after = Pt(4)

            p_i = tf.add_paragraph()
            p_i.text = impact
            p_i.font.name = FONT_FAMILY
            p_i.font.size = Pt(8.2)
            p_i.font.color.rgb = TEXT_SECONDARY

        # Bottom synthesis
        self.add_card(s, 0.80, 6.60, 11.733, 0.24, bg_color=CARD_TINT, border_color=None)
        tb_sn = s.shapes.add_textbox(Inches(0.90), Inches(6.62), Inches(11.533), Inches(0.22))
        p_sn = tb_sn.text_frame.paragraphs[0]
        p_sn.text = "MODULAR ARCHITECTURE: These combinations represent proven patterns. Capabilities are selected and integrated based on verified client constraints."
        p_sn.font.name = FONT_FAMILY
        p_sn.font.size = Pt(8.5)
        p_sn.font.bold = True
        p_sn.font.color.rgb = BLUE_SAP

        self.add_footer(s, 29)

    def build_slide_30(self):
        """Slide 30: The Industry 4.0 Connection"""
        s = self.create_base_slide(is_dark=False)
        self.add_header(s, "Section V: Bringing the Capabilities Together", 
                        "The Industry 4.0 Connection",
                        "THE ISA-95 CONTINUUM: Synchronizing physical plant assets with executive ledger systems across every operational layer")

        # 5-Level ISA-95 Stack Architecture Diagram
        levels = [
            ("LEVEL 4: Business Planning & Logistics", 
             "Enterprise ERP, Financials, Commercial Supply Chain & Sourcing",
             "SAP S/4HANA · SAP ECC · SAP BTP · Sourcing · Universal Ledger",
             "Group Role: Core SAP Implementation, BTP Extensions & Financial Integration", BLUE_SAP),
            ("LEVEL 3: Manufacturing Operations Management", 
             "Work-in-Progress, Quality Verification, Batch Traceability & Dispatch",
             "Elitia MES · Digital Work Instructions · Cell-to-Container Genealogy · EOL Testing",
             "Group Role: Elitia MES Deployment & Shop-Floor Operational Governance", TEAL),
            ("LEVEL 2: Supervisory & Cell Control", 
             "Supervisory Control, Line SCADA & Production Recipe Management",
             "SCADA Systems · Process Historians · Automated Line Interlocks · Shift Control",
             "Group Role: Custom IoT Edge Integration & Protocol Translation", PURPLE_ACCENT),
            ("LEVEL 1 & 0: Field Devices & Physical Machinery", 
             "Sensors, Actuators, PLCs, Electrical Feeder Meters & Physical Assembly",
             "Elitia EMS · Smart Power Meters · Modbus / OPC UA Gateways · Assembly Lines",
             "Group Role: Elitia EMS Sub-Metering & High-Frequency Telemetry Ingestion", AMBER_ACCENT)
        ]

        sw = 8.20
        sh = 1.05
        sgap = 0.16
        sy = 1.60

        for i, (lname, lscope, ltech, lrole, lcolor) in enumerate(levels):
            y = sy + i * (sh + sgap)
            self.add_card(s, 0.80, y, sw, sh, bg_color=CARD_WHITE, border_color=CARD_BORDER)
            
            # Left accent tag
            tag = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), Inches(y), Inches(0.20), Inches(sh))
            tag.fill.solid()
            tag.fill.fore_color.rgb = lcolor
            tag.line.fill.background()

            # Content
            box = s.shapes.add_textbox(Inches(1.12), Inches(y + 0.08), Inches(sw - 0.40), Inches(sh - 0.16))
            tf = box.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

            p1 = tf.paragraphs[0]
            p1.text = f"{lname.upper()}  —  {lscope}"
            p1.font.name = FONT_FAMILY
            p1.font.size = Pt(10)
            p1.font.bold = True
            p1.font.color.rgb = lcolor
            p1.space_after = Pt(2)

            p2 = tf.add_paragraph()
            p2.text = f"Technologies: {ltech}"
            p2.font.name = FONT_FAMILY
            p2.font.size = Pt(8.8)
            p2.font.color.rgb = TEXT_DARK
            p2.space_after = Pt(2)

            p3 = tf.add_paragraph()
            p3.text = f"Capabilities: {lrole}"
            p3.font.name = FONT_FAMILY
            p3.font.size = Pt(8.5)
            p3.font.bold = True
            p3.font.color.rgb = BLUE_SAP

        # Right Vertical Stack: End-to-End Vertical Enablers
        rw = 3.30
        rx = 9.233
        rh = 4.68
        self.add_card(s, rx, sy, rw, rh, bg_color=CARD_TINT, border_color=BORDER_ACCENT)
        
        rhdr = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(rx), Inches(sy), Inches(rw), Inches(0.35))
        rhdr.fill.solid()
        rhdr.fill.fore_color.rgb = SAP_DEEP
        rhdr.line.fill.background()
        p = rhdr.text_frame.paragraphs[0]
        p.text = "VERTICAL ENABLERS"
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT

        self.add_text_block(s, rx + 0.15, sy + 0.45, rw - 0.30, rh - 0.55,
                            title="Cross-Layer Intelligence",
                            bullets=[
                                "Data Engineering: Harmonizing time-series telemetry with transactional ledgers.",
                                "Agentic & Gen AI: Contextual assistants and automated multi-system routing.",
                                "Data Governance: Enforcing validation rules across the physical-to-digital bridge.",
                                "Zero-Trust Security: Protecting critical plant OT infrastructure from external threats."
                            ],
                            body="Industrial value depends on the seamless flow of verified information between layers, not the sheer count of deployed point technologies.",
                            title_color=SAP_DEEP, body_color=TEXT_DARK, title_size=10.5, body_size=8.6)

        # Bottom synthesis
        self.add_card(s, 0.80, 6.48, 11.733, 0.28, bg_color=CARD_TINT, border_color=BORDER_ACCENT)
        tb_sb = s.shapes.add_textbox(Inches(0.90), Inches(6.50), Inches(11.533), Inches(0.24))
        p_sb = tb_sb.text_frame.paragraphs[0]
        p_sb.text = "CORE ARCHITECTURAL INSIGHT: Industry 4.0 is achieved when shop-floor events automatically update the enterprise ledger, and business decisions immediately guide physical operations."
        p_sb.font.name = FONT_FAMILY
        p_sb.font.size = Pt(8.5)
        p_sb.font.bold = True
        p_sb.font.color.rgb = BLUE_SAP

        self.add_footer(s, 30)

    def build_slide_31(self):
        """Slide 31: Governance, Trust and Operational Control"""
        s = self.create_base_slide(is_dark=False)
        self.add_header(s, "Section V: Bringing the Capabilities Together", 
                        "Governance, Trust and Operational Control",
                        "BUILT-IN ASSURANCE: Embedding security, data integrity, access permissions, and auditability into daily operations")

        # 4 Governance Quadrants
        quads = [
            ("1. Identity & Role-Based Access Control",
             "Zero-Trust Architecture & Privilege Management",
             ["Enforces strict Segregation of Duties (SoD) across finance, procurement, and operations.",
              "Unifies corporate IT credentials with operational plant shop-floor authorization.",
              "Requires multi-factor authentication and role verification for sensitive transactional changes."],
             BLUE_SAP),
            ("2. Data Lineage & Integrity Validation",
             "Automated Quality Gates & Master Data Hygiene",
             ["Validates information accuracy at the point of entry before commits reach the ledger.",
              "Maintains end-to-end data lineage across extraction, transformation, and BI presentation.",
              "Prevents silent database corruption during migrations, system conversions, and batch syncs."],
             PURPLE_ACCENT),
            ("3. Workflow Accountability & Human Gates",
             "Deterministic Guardrails for AI & Automation",
             ["Every automated agent task operates within strict, deterministic policy boundaries.",
              "High-value transactions and exceptions require explicit human-in-the-loop authorization.",
              "Eliminates unmonitored shadow IT by channeling customizations through governed API fabrics."],
             EMERALD_ACCENT),
            ("4. Continuous Observability & Auditability",
             "Real-Time Telemetry, SLA Monitoring & Compliance",
             ["Provides real-time system health monitoring and proactive exception alert routing.",
              "Maintains immutable, time-stamped audit logs for all configuration and operational changes.",
              "Ensures full compliance readiness for ISO 9001, ISO 14001, CMMI, and statutory audits."],
             AMBER_ACCENT)
        ]

        qw = 5.70
        qh = 2.25
        gx = 0.333
        gy = 0.22
        sy = 1.60

        for idx, (qtitle, qsub, qbullets, qcolor) in enumerate(quads):
            r = idx // 2
            c = idx % 2
            x = 0.80 + c * (qw + gx)
            y = sy + r * (qh + gy)

            self.add_card(s, x, y, qw, qh, bg_color=CARD_WHITE, border_color=CARD_BORDER)
            
            # Header
            qhdr = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(qw), Inches(0.32))
            qhdr.fill.solid()
            qhdr.fill.fore_color.rgb = qcolor
            qhdr.line.fill.background()
            p = qhdr.text_frame.paragraphs[0]
            p.text = qtitle
            p.font.name = FONT_FAMILY
            p.font.size = Pt(10.5)
            p.font.bold = True
            p.font.color.rgb = TEXT_LIGHT

            self.add_text_block(s, x + 0.15, y + 0.38, qw - 0.30, qh - 0.42,
                                title=qsub, bullets=qbullets,
                                title_color=qcolor, body_color=TEXT_SECONDARY, title_size=10, body_size=8.8)

        # Bottom synthesis banner
        self.add_card(s, 0.80, 6.45, 11.733, 0.30, bg_color=CARD_TINT, border_color=BORDER_ACCENT)
        tb_sb = s.shapes.add_textbox(Inches(0.90), Inches(6.47), Inches(11.533), Inches(0.26))
        p_sb = tb_sb.text_frame.paragraphs[0]
        p_sb.text = "CROSS-CUTTING PRINCIPLE: Governance is not an administrative afterthought or a set of static policy PDFs. It is an active architectural design requirement embedded directly into enterprise software and workflows."
        p_sb.font.name = FONT_FAMILY
        p_sb.font.size = Pt(8.5)
        p_sb.font.bold = True
        p_sb.font.color.rgb = BLUE_SAP

        self.add_footer(s, 31)

    def build_slide_32(self):
        """Slide 32: A Practical Path from Problem to Solution"""
        s = self.create_base_slide(is_dark=False)
        self.add_header(s, "Section V: Bringing the Capabilities Together", 
                        "A Practical Path from Problem to Solution",
                        "DISCIPLINED ENGAGEMENT: A 7-step diagnostic methodology ensuring technology investments address verified business constraints")

        # 7-Step Process Pipeline
        steps = [
            ("1. Understand Problem", 
             "Deep discovery into operational symptoms, bottlenecks, and financial friction.",
             "Core Output: Business challenge definition."),
            ("2. Map Boundaries", 
             "Identify process handoffs, legacy system contracts, and organizational ownership.",
             "Core Output: Current-state process map."),
            ("3. Define Governance", 
             "Establish data quality rules, decision rights, access security, and audit needs.",
             "Core Output: Governance & lineage specification."),
            ("4. Determine Fit", 
             "Evaluate whether an existing product, service, custom build, or hybrid fits.",
             "Core Output: Architecture fit recommendation."),
            ("5. Validate Feasibility", 
             "Technical prototyping, sandbox validation, interface checks, and risk analysis.",
             "Core Output: Feasibility proof-of-concept."),
            ("6. Agree Scope & Roles", 
             "Define delivery milestones, success measures, accountability, and project governance.",
             "Core Output: Commercial statement of work."),
            ("7. Implement & Scale", 
             "Disciplined agile delivery, automated testing, change management, and hypercare.",
             "Core Output: Stabilized operational capability.")
        ]

        sw = 1.50
        sgap = 0.205
        sy = 1.60
        sh = 4.65

        for idx, (stitle, sdesc, soutput) in enumerate(steps):
            x = 0.80 + idx * (sw + sgap)
            self.add_card(s, x, sy, sw, sh, bg_color=CARD_WHITE, border_color=CARD_BORDER)
            
            # Step number badge
            snum = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(sy), Inches(sw), Inches(0.35))
            snum.fill.solid()
            snum.fill.fore_color.rgb = BLUE_SAP if idx < 4 else SAP_DEEP
            snum.line.fill.background()
            p = snum.text_frame.paragraphs[0]
            p.text = f"STAGE {idx + 1}"
            p.alignment = PP_ALIGN.CENTER
            p.font.name = FONT_FAMILY
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = TEXT_LIGHT

            # Content inside card
            self.add_text_block(s, x + 0.08, sy + 0.45, sw - 0.16, 2.50,
                                title=stitle, body=sdesc,
                                title_color=BLUE_SAP, body_color=TEXT_SECONDARY, title_size=10, body_size=8.5)

            # Output callout container at bottom of card
            ob = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x + 0.06), Inches(sy + 3.20), Inches(sw - 0.12), Inches(1.35))
            ob.fill.solid()
            ob.fill.fore_color.rgb = CARD_TINT
            ob.line.color.rgb = BORDER_ACCENT
            ob.line.width = Pt(1.0)
            tf_o = ob.text_frame
            tf_o.word_wrap = True
            tf_o.margin_left = tf_o.margin_right = Inches(0.06)
            tf_o.margin_top = Inches(0.06)
            p1 = tf_o.paragraphs[0]
            p1.text = "KEY DELIVERABLE"
            p1.font.name = FONT_FAMILY
            p1.font.size = Pt(7.5)
            p1.font.bold = True
            p1.font.color.rgb = BLUE_SAP
            p1.space_after = Pt(2)
            p2 = tf_o.add_paragraph()
            p2.text = soutput
            p2.font.name = FONT_FAMILY
            p2.font.size = Pt(8.2)
            p2.font.color.rgb = TEXT_DARK

            # Arrow connector to next
            if idx < len(steps) - 1:
                arr = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + sw + 0.04), Inches(sy + 1.80), Inches(0.12), Inches(0.18))
                arr.fill.solid()
                arr.fill.fore_color.rgb = BLUE_SAP
                arr.line.fill.background()

        # Bottom synthesis
        self.add_card(s, 0.80, 6.45, 11.733, 0.30, bg_color=CARD_TINT, border_color=BORDER_ACCENT)
        tb_sb = s.shapes.add_textbox(Inches(0.90), Inches(6.47), Inches(11.533), Inches(0.26))
        p_sb = tb_sb.text_frame.paragraphs[0]
        p_sb.text = "DELIVERY PHILOSOPHY: Solutions follow the verified problem. We never impose a predetermined software product or service package where simpler process adjustments or integration fixes suffice."
        p_sb.font.name = FONT_FAMILY
        p_sb.font.size = Pt(8.5)
        p_sb.font.bold = True
        p_sb.font.color.rgb = BLUE_SAP

        self.add_footer(s, 32)

    def build_slide_33(self):
        """Slide 33: Credentials and Delivery Discipline"""
        s = self.create_base_slide(is_dark=False)
        self.add_header(s, "Section V: Bringing the Capabilities Together", 
                        "Credentials and Delivery Discipline",
                        "VERIFIED STANDARDS: Enterprise delivery rigor backed by audited process maturity, quality frameworks, and partnerships")

        # 4 Credential Pillars
        creds = [
            ("SAP Service and Sell Partner",
             "Authorized Ecosystem Capability",
             ["Demonstrated technical delivery across the SAP ecosystem.",
              "Expertise spanning SAP S/4HANA, BTP, and enterprise integrations.",
              "Adherence to certified SAP implementation methodologies."],
             BLUE_SAP),
            ("CMMI Level 3 Appraised",
             "Defined Engineering & Process Rigor",
             ["Standardized, organization-wide software engineering processes.",
              "Disciplined requirements traceability, peer reviews, and QA testing.",
              "Predictable project delivery timelines and risk mitigation frameworks."],
             SAP_DEEP),
            ("ISO 9001:2015 Certified",
             "Quality Management System (QMS)",
             ["Audited quality governance across consulting and development.",
              "Systematic customer feedback and continuous service improvement.",
              "Transparent documentation and SLA-governed delivery oversight."],
             EMERALD_ACCENT),
            ("ISO 14001:2015 Certified",
             "Environmental Management System (EMS)",
             ["Audited environmental standards guiding enterprise operations.",
              "Commitment to sustainable software and industrial energy reduction.",
              "Embedding resource efficiency into enterprise transformation roadmaps."],
             TEAL)
        ]

        cw = 2.75
        ch = 4.40
        cg = 0.244
        sy = 1.60

        for idx, (ctitle, csub, cbullets, ccolor) in enumerate(creds):
            x = 0.80 + idx * (cw + cg)
            self.add_card(s, x, sy, cw, ch, bg_color=CARD_WHITE, border_color=CARD_BORDER)
            
            # Header
            chdr = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(sy), Inches(cw), Inches(0.40))
            chdr.fill.solid()
            chdr.fill.fore_color.rgb = ccolor
            chdr.line.fill.background()
            p = chdr.text_frame.paragraphs[0]
            p.text = ctitle
            p.alignment = PP_ALIGN.CENTER
            p.font.name = FONT_FAMILY
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = TEXT_LIGHT

            # Sub-badge
            sub_b = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x + 0.10), Inches(sy + 0.48), Inches(cw - 0.20), Inches(0.24))
            sub_b.fill.solid()
            sub_b.fill.fore_color.rgb = CARD_TINT
            sub_b.line.fill.background()
            p_s = sub_b.text_frame.paragraphs[0]
            p_s.text = csub
            p_s.alignment = PP_ALIGN.CENTER
            p_s.font.name = FONT_FAMILY
            p_s.font.size = Pt(8.2)
            p_s.font.bold = True
            p_s.font.color.rgb = ccolor

            # Content
            self.add_text_block(s, x + 0.12, sy + 0.80, cw - 0.24, 3.40,
                                title="Delivery Implications", bullets=cbullets,
                                title_color=TEXT_DARK, body_color=TEXT_SECONDARY, title_size=10, body_size=8.8)

        # Bottom synthesis box
        self.add_card(s, 0.80, 6.18, 11.733, 0.58, bg_color=CARD_TINT, border_color=BORDER_ACCENT)
        self.add_text_block(s, 0.95, 6.22, 11.433, 0.50,
                            title="HOW DISCIPLINED GOVERNANCE PROTECTS CLIENTS",
                            body="Certifications and partnerships are not decorative marketing badges; they represent audited organizational discipline. They guarantee that project milestones are governed by structured engineering processes, transparent risk management, and audited quality controls.",
                            bullets=["Reduces delivery variance, budget overruns, and unexpected post-go-live defects.",
                                     "Ensures technical claims remain grounded in verified partner authorizations and audited capabilities."],
                            title_color=BLUE_SAP, body_color=TEXT_DARK, title_size=9.5, body_size=8.2)

        self.add_footer(s, 33)

    def build_slide_34(self):
        """Slide 34: Engagement and Next Steps (Dark Canvas)"""
        s = self.create_base_slide(is_dark=True)
        self.add_header(s, "Lumbini Elite Group  ·  Strategic Engagement", 
                        "Engagement and Next Steps",
                        "COMMENCING THE CONVERSATION: A structured, non-disruptive path to evaluate operational challenges and explore solution fit",
                        is_dark=True)

        # 6-Step Discovery Roadmap
        stages = [
            ("1. Business Conversation", "Initial dialogue exploring operational challenges, process pain, and strategic goals."),
            ("2. Technical Discovery", "Lightweight review of current IT/OT architecture, system contracts, and data lineage."),
            ("3. Problem Definition", "Formal identification of underlying constraints vs. visible operational symptoms."),
            ("4. Solution Fit", "Evaluation of whether an Elitia product, Lumbini service, or hybrid fits best."),
            ("5. Feasibility Validation", "Targeted proof-of-concept, architectural sandbox verification, and risk review."),
            ("6. Proposed Roadmap", "Agreed scope, deliverables, governance milestones, and phased execution timeline.")
        ]

        sw = 1.76
        sgap = 0.234
        sy = 1.60

        for idx, (stitle, sdesc) in enumerate(stages):
            x = 0.80 + idx * (sw + sgap)
            self.add_card(s, x, sy, sw, 1.85, bg_color=NAVY_SURFACE, border_color=NAVY_BORDER)
            
            # Step header
            shdr = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(sy), Inches(sw), Inches(0.28))
            shdr.fill.solid()
            shdr.fill.fore_color.rgb = CYAN_ACCENT if idx < 3 else BLUE_SAP
            shdr.line.fill.background()
            p = shdr.text_frame.paragraphs[0]
            p.text = f"PHASE {idx + 1}"
            p.alignment = PP_ALIGN.CENTER
            p.font.name = FONT_FAMILY
            p.font.size = Pt(8.5)
            p.font.bold = True
            p.font.color.rgb = NAVY_CANVAS if idx < 3 else TEXT_LIGHT

            self.add_text_block(s, x + 0.08, sy + 0.36, sw - 0.16, 1.40,
                                title=stitle, body=sdesc,
                                title_color=CYAN_ACCENT, body_color=TEXT_LIGHT_MUTED, title_size=9.2, body_size=8.0)

            if idx < len(stages) - 1:
                arr = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + sw + 0.04), Inches(sy + 0.85), Inches(0.12), Inches(0.16))
                arr.fill.solid()
                arr.fill.fore_color.rgb = CYAN_ACCENT
                arr.line.fill.background()

        # Central Master Narrative Reinforcement Container
        self.add_card(s, 0.80, 3.65, 11.733, 1.60, bg_color=NAVY_SURFACE_ALT, border_color=CYAN_ACCENT, border_width=1.5)
        tb_mn = s.shapes.add_textbox(Inches(1.10), Inches(3.75), Inches(11.133), Inches(1.35))
        tf_mn = tb_mn.text_frame
        tf_mn.word_wrap = True

        p1 = tf_mn.paragraphs[0]
        p1.text = "THE GUIDING OBJECTIVE"
        p1.font.name = FONT_FAMILY
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = CYAN_ACCENT
        p1.space_after = Pt(4)

        p2 = tf_mn.add_paragraph()
        p2.text = (
            "“Lumbini Elite Group architects intelligent enterprises by connecting business strategy, "
            "enterprise applications, operational systems, data, AI, governance, and industry platforms "
            "into a unified operating model.”"
        )
        p2.font.name = FONT_FAMILY
        p2.font.size = Pt(15)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_after = Pt(4)

        p3 = tf_mn.add_paragraph()
        p3.text = "The objective is never to add technology for its own sake, but to establish a more connected, observable, controlled, and adaptable operating reality."
        p3.font.name = FONT_FAMILY
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = TEXT_LIGHT_MUTED

        # Bottom 2 Entity Recap Cards
        self.add_card(s, 0.80, 5.40, 5.70, 1.35, bg_color=NAVY_SURFACE, border_color=NAVY_BORDER)
        self.add_text_block(s, 0.95, 5.48, 5.40, 1.15,
                            title="Elitia Technologies — Software Products",
                            body="7 purpose-built operational software products: Elitia MES, EMS, BI, Migration Cockpit, Supplier Collaboration, Assessment Suite, and DGS.",
                            bullets=["Deployable independently or integrated into client enterprise landscapes.",
                                     "Delivers rapid time-to-value with packaged operational best practices."],
                            title_color=CYAN_ACCENT, body_color=TEXT_LIGHT_MUTED, title_size=10.5, body_size=8.5)

        self.add_card(s, 6.833, 5.40, 5.70, 1.35, bg_color=NAVY_SURFACE, border_color=NAVY_BORDER)
        self.add_text_block(s, 6.98, 5.48, 5.40, 1.15,
                            title="Lumbini Elite Solutions & Services — Advisory & Engineering",
                            body="13 specialized practices spanning Enterprise SAP, Data Engineering, Agentic AI, Generative AI, IoT, Web & Mobile development, and AMS support.",
                            bullets=["Deep advisory aligning operating processes, data lineage, and decision rights.",
                                     "End-to-end accountability backed by CMMI Level 3 and ISO 9001:2015 rigor."],
                            title_color=BLUE_SAP, body_color=TEXT_LIGHT_MUTED, title_size=10.5, body_size=8.5)

        self.add_footer(s, 34, is_dark=True)

    # -------------------------------------------------------------
    # Master Build Orchestrator
    # -------------------------------------------------------------
    def build_all(self):
        print(f"[*] Commencing master build for: {self.filename}")
        
        # Section I: The Enterprise Problem (Slides 1 to 5)
        print("[+] Building Section I: The Enterprise Problem (Slides 1-5)...")
        self.build_slide_01()
        self.build_slide_02()
        self.build_slide_03()
        self.build_slide_04()
        self.build_slide_05()

        # Section II: How Capabilities Fit Together (Slides 6 to 8)
        print("[+] Building Section II: How Capabilities Fit Together (Slides 6-8)...")
        self.build_slide_06()
        self.build_slide_07()
        self.build_slide_08()

        # Section III: Elitia Technologies Products (Slides 9 to 15)
        print("[+] Building Section III: Elitia Technologies Products (Slides 9-15)...")
        self.build_slide_09()
        self.build_slide_10()
        self.build_slide_11()
        self.build_slide_12()
        self.build_slide_13()
        self.build_slide_14()
        self.build_slide_15()

        # Section IV: Lumbini Elite Solutions & Services (Slides 16 to 28)
        print("[+] Building Section IV: Lumbini Elite Solutions & Services (Slides 16-28)...")
        self.build_slide_16()
        self.build_slide_17()
        self.build_slide_18()
        self.build_slide_19()
        self.build_slide_20()
        self.build_slide_21()
        self.build_slide_22()
        self.build_slide_23()
        self.build_slide_24()
        self.build_slide_25()
        self.build_slide_26()
        self.build_slide_27()
        self.build_slide_28()

        # Section V: Bringing Capabilities Together (Slides 29 to 34)
        print("[+] Building Section V: Bringing Capabilities Together (Slides 29-34)...")
        self.build_slide_29()
        self.build_slide_30()
        self.build_slide_31()
        self.build_slide_32()
        self.build_slide_33()
        self.build_slide_34()

        print(f"[*] Saving presentation ({len(self.prs.slides)} slides) to: {self.filename}...")
        self.prs.save(self.filename)
        print(f"[SUCCESS] Successfully generated: {self.filename} (Total Slides: {len(self.prs.slides)})")
        return self.filename


if __name__ == "__main__":
    builder = DeckBuilder()
    builder.build_all()
