import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def build_trace_presentation(output_path="Hical_TRACE_n_TRACE_Executive_Proposal.pptx"):
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
    
    SAP_BLUE = RGBColor(0, 102, 204)         # #0066CC Enterprise SAP Blue
    CYAN_ACCENT = RGBColor(0, 180, 216)      # #00B4D8 Tech Cyan
    GOLD_ACCENT = RGBColor(217, 119, 6)      # #D97706 Lumbini Amber/Gold
    GOLD_LIGHT_BG = RGBColor(254, 243, 199)  # Gold Tint
    
    EMERALD_GREEN = RGBColor(16, 185, 129)   # #10B981 Success / Quality
    GREEN_LIGHT_BG = RGBColor(236, 253, 245) # Soft Green Tint
    AMBER_WARN = RGBColor(245, 158, 11)      # #F59E0B Warning
    AMBER_LIGHT_BG = RGBColor(255, 251, 235) # Soft Amber Tint
    CRIMSON_RED = RGBColor(239, 68, 68)      # #EF4444 Critical Alert
    RED_LIGHT_BG = RGBColor(254, 242, 242)   # Soft Red Tint
    
    PURPLE_ACCENT = RGBColor(124, 58, 237)   # Traceability Purple
    PURPLE_LIGHT_BG = RGBColor(245, 243, 255)
    
    TEXT_DARK = RGBColor(15, 23, 42)         # #0F172A Primary Dark
    TEXT_MUTED = RGBColor(100, 116, 139)     # #64748B Secondary Slate
    TEXT_LIGHT = RGBColor(248, 250, 252)     # #F8FAFC Off-White
    TEXT_LIGHT_MUTED = RGBColor(148, 163, 184)
    
    TOTAL_SLIDES = 12

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
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.38), Inches(4.8), Inches(0.26))
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
        p.text = "Lumbini Elite Solutions  |  Hical Technologies — TRACE n TRACE Proposal  |  Confidential"
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
    # SLIDE 1: Title & Strategic Context (Tell: Strategic Opening)
    # =============================================================
    s1 = add_base_slide(is_dark=True)
    
    top_glow = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    top_glow.fill.solid()
    top_glow.fill.fore_color.rgb = CYAN_ACCENT
    top_glow.line.fill.background()
    
    b1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.0), Inches(5.6), Inches(0.34))
    b1.fill.solid()
    b1.fill.fore_color.rgb = DARK_CARD
    b1.line.color.rgb = CYAN_ACCENT
    b1.line.width = Pt(1.2)
    tf1 = b1.text_frame
    tf1.margin_top = Inches(0.03)
    p = tf1.paragraphs[0]
    p.text = "AEROSPACE & DEFENCE SHOP-FLOOR DIGITALIZATION"
    p.font.name = "Arial"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    
    tx = s1.shapes.add_textbox(Inches(0.9), Inches(1.5), Inches(7.5), Inches(1.8))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "TRACE n TRACE\nDigital Execution & Genealogy"
    p.font.name = "Arial"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT
    
    tx_sub = s1.shapes.add_textbox(Inches(0.9), Inches(3.3), Inches(7.5), Inches(0.8))
    tf_sub = tx_sub.text_frame
    tf_sub.word_wrap = True
    p = tf_sub.paragraphs[0]
    p.text = "100% Non-Invasive, Read-Only SAP Integration & Air-Gapped Operational Approval Desk for Hical Technologies"
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
        ("Architecture Mandate:", " 100% Read-Only SAP Integration (Zero Write-Calls, Zero DB Table Locks)"),
        ("Commercial Advantage:", " Zero Added Named SAP Fiori/Professional User Licenses for Floor Operators"),
        ("Quality Framework:", " Hardware Barcode Poka-Yoke & AS9100D/MIL-STD 360° Full-Chain Genealogy"),
        ("Delivery Commitment:", " 90-Day Turnkey Agile Delivery + 60 Calendar Days Dedicated Hypercare")
    ]
    for i, (b_title, b_desc) in enumerate(ov_bullets):
        p = tf_ov.paragraphs[0] if i == 0 else tf_ov.add_paragraph()
        p.space_after = Pt(4)
        r1 = p.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = GOLD_ACCENT
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.bold = False
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_LIGHT

    # Right side 3 Strategic Pillars Card
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
    p.text = "THE THREE STRATEGIC PILLARS"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    
    pillars_data = [
        ("1. ZERO-RISK ARCHITECTURE", "100% Non-invasive OData GET requests. SAP remains untampered; zero table locking or data corruption risk.", SAP_BLUE),
        ("2. POKA-YOKE QUALITY GATE", "Hardware barcode scanning blocks incorrect lots, expired batches, and obsolete ECN drawing revisions instantly.", EMERALD_GREEN),
        ("3. AIR-GAPPED APPROVAL DESK", "Two-tier digital sign-off (Supervisor + QC) producing pre-verified Ready-to-Post slips for SAP GUI.", GOLD_ACCENT)
    ]
    
    top_pos = 2.1
    for title, desc, clr in pillars_data:
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
    # SLIDE 2: Problem Context (Tell: The Shop-Floor Bottleneck)
    # =============================================================
    s2 = add_base_slide(is_dark=False)
    add_header(s2, "The Aerospace Shop-Floor Disconnect: 4 Critical Pain Points", "PROBLEM CONTEXT & INDUSTRY CHALLENGES", "High-reliability MTO/ETO manufacturing constrained by manual processes and ERP licensing friction")
    
    pain_cards = [
        ("1. Paper Traveler Latency", [
            ("Laminated Paper Routing:", "Job instructions and inspection sheets travel physically through 8-15 assembly bays."),
            ("Shift-End Backlog:", "Manual clerical entry into SAP causes 24-48 hour delays in production visibility."),
            ("Lost Documentation:", "Damaged, stained, or misplaced paper cards threaten AS9100 customer audit compliance.")
        ], CRIMSON_RED),
        ("2. Heavy SAP Licensing Cost", [
            ("Named User Burden:", "Equipping 150-300 shop-floor operators with SAP Fiori or Professional licenses requires ₹80L–₹1.5Cr+ in OpEx."),
            ("High Administrative Drag:", "Managing SAP credentials, password resets, and user licenses for high-turnover assembly workers."),
            ("Infeasible ROI:", "Direct SAP licensing for assembly-line data capture is economically unviable.")
        ], AMBER_WARN),
        ("3. Human Assembly Errors", [
            ("Missing Hardware Poka-Yoke:", "Visual checks fail under production pressure, leading to wrong component batches mounted."),
            ("Expired Chemical Consumption:", "Potting resins, epoxies, or adhesives consumed past shelf life."),
            ("ECN Revision Mismatch:", "Parts assembled against outdated drawing revisions, triggering scrap and customer rejections.")
        ], PURPLE_ACCENT),
        ("4. ERP Database Risk", [
            ("Concurrent Write Lockups:", "Direct shop-floor write-calls into live SAP cause table contention in AUFM, AFRU, and MSEG."),
            ("System Outage Exposure:", "Shop-floor network dropouts cause uncommitted transactions, deadlocks, and corrupted ERP state."),
            ("Audit Exposure:", "Unfiltered operator entries into SAP core risk breaking financial and statutory reconciliation.")
        ], SAP_BLUE)
    ]
    
    col_w = 2.75
    spacing = 0.24
    for idx, (head, points, border_clr) in enumerate(pain_cards):
        c_left = 0.8 + idx * (col_w + spacing)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(col_w), Inches(5.1))
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
    # SLIDE 3: Strategic Value Proposition (Tell: The Solution)
    # =============================================================
    s3 = add_base_slide(is_dark=True)
    add_header(s3, "TRACE n TRACE Strategic Value Proposition & Win Themes", "EXECUTIVE VALUE FRAMEWORK", "Eliminating paper, guaranteeing zero-defect quality, and protecting the SAP core with zero licensing penalties", is_dark=True)
    
    val_cards = [
        ("1. 100% Non-Invasive Architecture", [
            ("Zero SAP Write-Calls:", "100% read-only OData data consumption. SAP core database tables remain untampered and completely safe."),
            ("Zero Table Locks:", "No deadlocks, no background process stalls, and zero performance impact on live S/4HANA operations."),
            ("Air-Gapped Decoupling:", "Shop floor operates independently on modern web and edge technology.")
        ], CYAN_ACCENT),
        ("2. Zero Added SAP Licensing Cost", [
            ("Massive OpEx Savings:", "Floor operators and inspectors access TRACE n TRACE without requiring Named SAP Fiori/Professional licenses."),
            ("Single System Interface:", "Only a single technical read-only user account is required to interface with SAP."),
            ("Immediate Payback:", "Saves ₹45L–₹75L in upfront and recurring annual software licensing fees.")
        ], GOLD_ACCENT),
        ("3. Aerospace Barcode Poka-Yoke", [
            ("Hardware Enforced:", "1D/2D barcode scanners immediately lock the terminal if an unreleased or incorrect component is scanned."),
            ("Drawing ECN Lockout:", "Prevents assembly of outdated revision materials against active production orders."),
            ("Direct Scrap Reduction:", "Recovers 2%–4% gross margin by stopping assembly defects before they happen.")
        ], EMERALD_GREEN),
        ("4. Two-Tier Approval & Staging", [
            ("Supervisor & QC Sign-off:", "Digital review gate requires Supervisor PIN and QC stamp before confirmations are finalized."),
            ("Ready-to-Post Slips:", "Automatically generates pre-verified slips indexed by SAP T-Code (CO11N, MIGO, QE51N)."),
            ("100% Accurate Inward Entry:", "Ensures flawless, audit-grade posting into SAP GUI with zero clerical error.")
        ], PURPLE_ACCENT)
    ]
    
    for idx, (title, points, border_c) in enumerate(val_cards):
        c_left = 0.8 + idx * (col_w + spacing)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(col_w), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = DARK_CARD
        card.line.color.rgb = border_c
        card.line.width = Pt(1.5)
        
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.18)
        tf_c.margin_top = Inches(0.18)
        
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
            r2.font.size = Pt(8.2)
            r2.font.color.rgb = TEXT_LIGHT_MUTED

    add_footer(s3, 3, is_dark=True)

    # =============================================================
    # SLIDE 4: Non-Invasive Architectural Blueprint (Show: The Architecture)
    # =============================================================
    s4 = add_base_slide(is_dark=True)
    add_header(s4, "Non-Invasive Architecture: The Air-Gapped Operational Pipeline", "TECHNICAL ARCHITECTURE", "Standard SAP Read-Only OData GET endpoints flowing to an air-gapped shop-floor execution and approval layer", is_dark=True)
    
    arch_tiers = [
        ("TIER 1: SAP S/4HANA / ECC CORE", "System of Record (Read-Only Exposure)", [
            ("Purchasing:", "API_PURCHASEORDER_PROCESS_SRV (PO, supplier lot, revision, quantities)."),
            ("Production:", "API_PRODUCTION_ORDER_2_SRV (Orders, routing sequence, cycle time, BOM reservations)."),
            ("Quality:", "API_INSPECTIONLOT_SRV (Inspection lots, tolerance limits, qualitative check flags)."),
            ("Inventory:", "I_MaterialStock CDS View (Unrestricted vs. quality inspection stock by bin)."),
            ("Security Profile:", "Dedicated technical user with strictly Authorization Activity 03 (Display only).")
        ], SAP_BLUE),
        ("TIER 2: TRACE n TRACE MIDDLE TIER", "Secure Enterprise Gateway & As-Built Graph", [
            ("API Gateway:", "Token authentication, rate-limiting, and TLS 1.3 encryption."),
            ("Delta Sync Engine:", "Timestamp polling ($filter=LastChangeDateTime ge ...) ensures near-zero SAP CPU load."),
            ("Operational Database:", "High-performance PostgreSQL relational store and As-Built graph database."),
            ("Two-Tier Approval Desk:", "Web-based supervisory and QC verification workbench."),
            ("Slip Compiler:", "Prepares pre-validated Ready-to-Post slips formatted for CO11N, MIGO, QE51N.")
        ], CYAN_ACCENT),
        ("TIER 3: OPERATIONAL EDGE LAYER", "Rugged Handheld Terminals (HHT) & Scanners", [
            ("Rugged Terminals:", "Optimized for Zebra TC26/TC57 and Honeywell ScanPal Android terminals."),
            ("Barcode Wedge Engine:", "Instant scanning of 1D, DataMatrix, and QR codes directly into traveler fields."),
            ("Local SQLite Buffer:", "Offline edge capability enabling uninterrupted work in cleanrooms and RF chambers."),
            ("Hardware Poka-Yoke:", "Immediate audible/visual lockout upon scanning incorrect or expired materials."),
            ("Operator Usability:", "Touch-friendly, high-contrast UI operable with manufacturing cleanroom gloves.")
        ], EMERALD_GREEN)
    ]
    
    col_w4 = 3.75
    spacing_c4 = 0.24
    for idx, (title, sub, items, border_c) in enumerate(arch_tiers):
        c_left = 0.8 + idx * (col_w4 + spacing_c4)
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(col_w4), Inches(5.1))
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

    add_footer(s4, 4, is_dark=True)

    # =============================================================
    # SLIDE 5: Read-Only SAP OData Specifications (Show: The Technical Engine)
    # =============================================================
    s5 = add_base_slide(is_dark=False)
    add_header(s5, "Read-Only SAP OData Specifications & Security Mechanics", "INTEGRATION SPECIFICATIONS", "Standard certified OData services, least-privilege security profiles, and offline edge resilience")
    
    # 4 Service Cards
    odata_services = [
        ("Procurement & Inbound", "API_PURCHASEORDER_PROCESS_SRV", [
            ("Entities Consumed:", "A_PurchaseOrder, A_PurchaseOrderItem"),
            ("Key Fields Extracted:", "PO Number, Line Item, Material, Vendor ID, Drawing Rev, Target Qty, Plant, Storage Location."),
            ("Shop-Floor Function:", "Validates incoming raw material and supplier hardware against active, approved PO lines.")
        ], SAP_BLUE),
        ("Production & Routing", "API_PRODUCTION_ORDER_2_SRV", [
            ("Entities Consumed:", "A_ProductionOrder_2, A_ProductionOrderOperation_2, A_ProductionOrderComponent_2"),
            ("Key Fields Extracted:", "Order ID, Operation #, Work Center, Setup/Machine Time, Material Reservations (RESB), ECN Revision."),
            ("Shop-Floor Function:", "Powers the Digital Traveler, routing sequences, required batch lists, and cycle time baselines.")
        ], CYAN_ACCENT),
        ("In-Process Quality", "API_INSPECTIONLOT_SRV", [
            ("Entities Consumed:", "A_InspectionLot, A_InspectionCharacteristic"),
            ("Key Fields Extracted:", "Inspection Lot ID, Char ID, Char Text, Upper/Lower Tolerance Limits, Qualitative Pass/Fail Flags."),
            ("Shop-Floor Function:", "Enforces digital inspection gates, requiring dimensional and electrical measurements before step completion.")
        ], EMERALD_GREEN),
        ("Inventory & Stock Status", "I_MaterialStock (CDS View)", [
            ("Entities Consumed:", "I_MaterialStock / API_PHYSICAL_INVENTORY"),
            ("Key Fields Extracted:", "Material Number, Batch Number, Storage Location, Unrestricted Stock, Quality Quarantine Stock."),
            ("Shop-Floor Function:", "Ensures unreleased or quarantined batches are immediately blocked from assembly picking.")
        ], PURPLE_ACCENT)
    ]
    
    top_c = 1.6
    w_c = 5.75
    h_c = 2.0
    for idx, (title, srv_name, bullets, border_c) in enumerate(odata_services):
        r_idx = idx // 2
        c_idx = idx % 2
        left_pos = 0.8 + c_idx * (w_c + 0.233)
        top_pos = top_c + r_idx * (h_c + 0.15)
        
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(top_pos), Inches(w_c), Inches(h_c))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_c
        card.line.width = Pt(1.5)
        
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.18)
        tf_c.margin_top = Inches(0.12)
        
        p = tf_c.paragraphs[0]
        p.text = title + "  (" + srv_name + ")"
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = border_c
        p.space_after = Pt(4)
        
        for b_title, b_desc in bullets:
            p_b = tf_c.add_paragraph()
            p_b.space_after = Pt(2)
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

    # Bottom Security Banner
    sec_banner = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.95), Inches(11.733), Inches(0.95))
    sec_banner.fill.solid()
    sec_banner.fill.fore_color.rgb = GREEN_LIGHT_BG
    sec_banner.line.color.rgb = EMERALD_GREEN
    sec_banner.line.width = Pt(1.2)
    
    tf_sb = sec_banner.text_frame
    tf_sb.word_wrap = True
    tf_sb.margin_left = tf_sb.margin_right = Inches(0.2)
    tf_sb.margin_top = Inches(0.1)
    
    p = tf_sb.paragraphs[0]
    p.text = "SECURITY & EDGE QUERY MECHANICS:"
    p.font.name = "Arial"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = EMERALD_GREEN
    p.space_after = Pt(2)
    
    p_desc = tf_sb.add_paragraph()
    r1 = p_desc.add_run()
    r1.text = "1. Least-Privilege Technical User: "
    r1.font.bold = True
    r1.font.size = Pt(8.5)
    r1.font.color.rgb = TEXT_DARK
    r2 = p_desc.add_run()
    r2.text = "Restricted strictly to Display Authorization (03). No create/change access (01/02) exists.  |  "
    r2.font.size = Pt(8.2)
    r2.font.color.rgb = TEXT_DARK
    
    r3 = p_desc.add_run()
    r3.text = "2. Delta Polling & Edge SQLite Buffer: "
    r3.font.bold = True
    r3.font.size = Pt(8.5)
    r3.font.color.rgb = TEXT_DARK
    r4 = p_desc.add_run()
    r4.text = "Timestamp filters ($filter=LastChangeDateTime ge ...) ensure minimal SAP CPU load, while local SQLite caches enable 100% offline scanning in RF cleanrooms."
    r4.font.size = Pt(8.2)
    r4.font.color.rgb = TEXT_DARK

    add_footer(s5, 5, is_dark=False)

    # =============================================================
    # SLIDE 6: Core Execution Modules (Show: The Software - Part 1)
    # =============================================================
    s6 = add_base_slide(is_dark=False)
    add_header(s6, "Core Modules: Digital Traveler, Kitting & Barcode Poka-Yoke", "FUNCTIONAL EXECUTION SUITE", "Step-by-step guidance, touchless labor capture, and real-time error prevention at the workstation")
    
    mod_cards = [
        ("MODULE A: DIGITAL INBOUND & KITTING", "PO & BOM Kitting Verification", [
            ("Barcode Goods Inward:", "Scans supplier 1D/2D barcodes on dock arrival, validating part numbers and purchase orders."),
            ("Kitting Cart Assembly:", "Verifies that picking carts contain the exact components and released batches for production."),
            ("Shortage & Substitution Alert:", "Instantly warns kitting coordinators of missing items before kits leave staging.")
        ], SAP_BLUE),
        ("MODULE B: OPERATOR DIGITAL TRAVELER", "Paperless Workstation Execution", [
            ("Touchless Clock-On/Off:", "Scans technician ID to track actual labor, setup, and run time per routing step."),
            ("Live Visual SOPs:", "Displays high-resolution assembly drawings, wiring schematics, and torque specs on terminal."),
            ("Dynamic Parameter Logging:", "Records resistance, torque, curing temperature, and pull-force directly into the digital record.")
        ], CYAN_ACCENT),
        ("MODULE C: AEROSPACE POKA-YOKE", "Real-Time Quality Enforcer", [
            ("Batch Release Sentinel:", "Blocks assembly if scanned components are unreleased or in Quality Quarantine."),
            ("ECN Revision Enforcer:", "Cross-references component drawing revision against the active production order BOM."),
            ("Potting & Chemical Expiry:", "Locks out resin, adhesive, or solder paste lots that have exceeded manufacturer shelf life.")
        ], CRIMSON_RED)
    ]
    
    for idx, (title, sub, items, border_c) in enumerate(mod_cards):
        c_left = 0.8 + idx * (col_w4 + spacing_c4)
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(col_w4), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
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
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_after = Pt(12)
        
        for item_h, item_d in items:
            p_it = tf_c.add_paragraph()
            p_it.space_after = Pt(8)
            r1 = p_it.add_run()
            r1.text = "• " + item_h + " "
            r1.font.bold = True
            r1.font.size = Pt(8.5)
            r1.font.color.rgb = TEXT_DARK
            r2 = p_it.add_run()
            r2.text = item_d
            r2.font.bold = False
            r2.font.size = Pt(8.2)
            r2.font.color.rgb = TEXT_MUTED

    add_footer(s6, 6, is_dark=False)

    # =============================================================
    # SLIDE 7: 360° Genealogy & Defect/Rework Routing (Show: Software - Part 2)
    # =============================================================
    s7 = add_base_slide(is_dark=False)
    add_header(s7, "360° Bi-Directional Genealogy & Defect/Rework Routing", "GENEALOGY & NON-CONFORMANCE", "Instant aerospace audit defense in <15 seconds and dynamic shop-floor rework branch control")
    
    gen_cards = [
        ("MODULE D: 360° BI-DIRECTIONAL GENEALOGY", "Complete Traceability in Seconds", [
            ("Top-Down FG Serialization:", "Enter a Finished Goods Serial ID to generate an As-Built tree showing all subassemblies, internal winding lots, raw wire batches, connectors, and technician logs."),
            ("Bottom-Up Raw Batch Trace:", "Enter a raw material batch (e.g., magnet wire spool) to pinpoint every FG serial unit containing that material across WIP, warehouse stock, and dispatches in 5 seconds."),
            ("AS9100 / Defense Audit Defense:", "Generates certified electronic Certificate of Conformance (CoC) and audit packages instantly, eliminating days of frantic paper searching.")
        ], PURPLE_ACCENT),
        ("MODULE E: DEFECT & REWORK ROUTING ENGINE", "Controlled Non-Conformance Loops", [
            ("Digital NCR Generation:", "Log non-conformances on the floor with photographic evidence and failure classification."),
            ("Rework Branching:", "Spawns authorized rework sub-operations (re-winding, de-potting, touch-up soldering) without corrupting or modifying the parent production order in SAP."),
            ("Re-Inspection Sign-Off:", "Enforces mandatory QC re-test and calibration before rework can merge back into main routing."),
            ("Scrap Disposition:", "Segregates scrapped parts physically and digitally with automated cost-center attribution.")
        ], GOLD_ACCENT)
    ]
    
    col_w7 = 5.75
    spacing_c7 = 0.233
    for idx, (title, sub, items, border_c) in enumerate(gen_cards):
        c_left = 0.8 + idx * (col_w7 + spacing_c7)
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(col_w7), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
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
        
        p_sub = tf_c.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(8.5)
        p_sub.font.italic = True
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_after = Pt(14)
        
        for item_h, item_d in items:
            p_it = tf_c.add_paragraph()
            p_it.space_after = Pt(10)
            r1 = p_it.add_run()
            r1.text = "• " + item_h + " "
            r1.font.bold = True
            r1.font.size = Pt(9)
            r1.font.color.rgb = TEXT_DARK
            r2 = p_it.add_run()
            r2.text = item_d
            r2.font.bold = False
            r2.font.size = Pt(8.5)
            r2.font.color.rgb = TEXT_MUTED

    add_footer(s7, 7, is_dark=False)

    # =============================================================
    # SLIDE 8: Two-Tier Approval Desk & Ready-to-Post Slips (Show: Operational Bridge)
    # =============================================================
    s8 = add_base_slide(is_dark=True)
    add_header(s8, "Two-Tier Operational Approval Desk & SAP Ready-to-Post Slips", "AIR-GAPPED OPERATIONAL GOVERNANCE", "Dual digital sign-off ensuring segregation of duties and error-free inward posting into SAP GUI", is_dark=True)
    
    wf_steps = [
        ("STEP 1: SHOP-FLOOR SUBMISSION", "Assembler Completes Step", [
            ("Operator Completion:", "Technician scans all component serials, logs parameters, finishes step, and hits 'Submit for Review'."),
            ("Terminal Lockout:", "Work traveler is placed into review queue, preventing unauthorized further modification."),
            ("Automated Audit Trail:", "System stamps time, terminal ID, and operator badge ID.")
        ], CYAN_ACCENT),
        ("STEP 2: TIER 1 - SUPERVISOR SIGN-OFF", "Production Verification", [
            ("Labor Actuals Validation:", "Shift supervisor inspects confirmed machine and setup hours."),
            ("Attendance & Output:", "Verifies yield quantities, operator assignment, and work center loading."),
            ("Digital Authorization:", "Supervisor validates the traveler via secure digital PIN or smart badge scan.")
        ], SAP_BLUE),
        ("STEP 3: TIER 2 - QC GATEKEEPER", "Quality Certification", [
            ("Inspection Parameter Review:", "QC inspector verifies recorded electrical readings, torque logs, and dimensions."),
            ("Calibration Check:", "Ensures testing instruments used were within valid calibration dates."),
            ("Cryptographic Stamp:", "QC applies digital sign-off, moving the traveler to 'Verified Staging'.")
        ], EMERALD_GREEN),
        ("STEP 4: READY-TO-POST SLIPS", "Error-Free SAP Inward", [
            ("Indexed by SAP T-Code:", "Auto-compiles verified actuals formatted for CO11N, MIGO (261/101), and QE51N."),
            ("Zero Typing Errors:", "Authorized clerk inputs verified values into SAP GUI in seconds with 100% accuracy."),
            ("Complete Air-Gap:", "Zero direct database connections to SAP; zero corruption risk.")
        ], GOLD_ACCENT)
    ]
    
    col_w8 = 2.75
    for idx, (title, sub, items, border_c) in enumerate(wf_steps):
        c_left = 0.8 + idx * (col_w8 + spacing)
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(col_w8), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = DARK_CARD
        card.line.color.rgb = border_c
        card.line.width = Pt(1.5)
        
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.18)
        tf_c.margin_top = Inches(0.18)
        
        p = tf_c.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(10)
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
            p_it.space_after = Pt(8)
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

    add_footer(s8, 8, is_dark=True)

    # =============================================================
    # SLIDE 9: 90-Day Implementation Methodology (Show: Execution Plan)
    # =============================================================
    s9 = add_base_slide(is_dark=False)
    add_header(s9, "90-Day Agile Implementation Roadmap & 60-Day Hypercare", "PROJECT PLAN & MILESTONES", "Five structured milestone stages ensuring rapid shop-floor deployment and comprehensive AS9100 validation")
    
    phases_s9 = [
        ("PHASE 1: BLUEPRINT", "Days 1–15", [
            ("Shop-Floor Walkthrough:", "Cell study across motors & harnesses."),
            ("OData Validation:", "Testing read endpoints in SAP Sandbox."),
            ("Architecture Sign-Off:", "Formal FRS and technical blueprint.")
        ], "Gate 1: Blueprint Sign-Off (20% Milestone)", SAP_BLUE),
        ("PHASE 2: CORE APP BUILD", "Days 16–45", [
            ("HHT Client Build:", "Zebra/Honeywell PWA & Android app."),
            ("Barcode Wedge Config:", "1D/2D DataMatrix scanning engine."),
            ("Poka-Yoke Engine:", "Offline SQLite edge caching & rules.")
        ], "Gate 2: App Alpha Complete (30% Milestone)", CYAN_ACCENT),
        ("PHASE 3: INTEGRATION", "Days 46–65", [
            ("OData Pipeline:", "Delta synchronization to PostgreSQL."),
            ("Approval Desk:", "Supervisor & QC review workbench."),
            ("Slip Compiler:", "Ready-to-Post engine (CO11N/MIGO).")
        ], "Review: System Integration Walkthrough", PURPLE_ACCENT),
        ("PHASE 4: DRY-RUNS & UAT", "Days 66–80", [
            ("Pilot Assembly Line:", "Dry-run on 2 active production cells."),
            ("Terminal Stress Test:", "15+ Zebra scanners concurrent run."),
            ("AS9100 Audit Dry-Run:", "Simulated 15-second genealogy audit.")
        ], "Gate 3: Formal Business UAT Sign-Off (30% Milestone)", AMBER_WARN),
        ("PHASE 5: CUTOVER & LIVE", "Days 81–90", [
            ("Production Rollout:", "Deployment to on-premise server."),
            ("Operator Training:", "Shift training for 50+ shop-floor users."),
            ("SOP & Handover:", "Commercial go-live transition.")
        ], "Gate 4: Production Go-Live (20% Milestone)", EMERALD_GREEN)
    ]
    
    p_w = 2.15
    p_spacing = 0.2
    for idx, (p_title, p_time, p_tasks, p_gate, p_clr) in enumerate(phases_s9):
        p_left = 0.8 + idx * (p_w + p_spacing)
        card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(p_left), Inches(1.6), Inches(p_w), Inches(5.1))
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

    add_footer(s9, 9, is_dark=False)

    # =============================================================
    # SLIDE 10: Commercial Proposal & Investment Framework (Tell: The Investment)
    # =============================================================
    s10 = add_base_slide(is_dark=True)
    add_header(s10, "Commercial Proposal, Milestone Payments & AMS Framework", "COMMERCIAL FRAMEWORK", "Turnkey Fixed-Price Implementation backed by 60 Days Hypercare and SLA-driven AMS", is_dark=True)
    
    comm_cards_s10 = [
        ("1. TURNKEY IMPLEMENTATION", "₹28,50,000 INR (Excl. Taxes)", [
            ("A. App & Platform Development:", "₹18,50,000\nEnd-to-end TRACE n TRACE software, Zebra/Honeywell scanner app, Two-Tier Approval Desk, SQLite edge cache, and PostgreSQL As-Built genealogy graph."),
            ("B. SAP Integration & Middleware:", "₹10,00,000\nRead-only SAP OData configuration, delta sync engine, Ready-to-Post Slip compiler (CO11N/MIGO/QE51N), AS9100 validation, and UAT.")
        ], CYAN_ACCENT),
        ("2. MILESTONE PAYMENT GATES", "Deliverable-Linked Billing", [
            ("Milestone 1 — 20% (₹5,70,000):", "Upon Kickoff and approved Architecture Blueprint (Day 15)."),
            ("Milestone 2 — 30% (₹8,55,000):", "Upon Core HHT Scanning App & Poka-Yoke Engine Complete (Day 45)."),
            ("Milestone 3 — 30% (₹8,55,000):", "Upon Middleware Integration & Shop-Floor UAT Sign-Off (Day 80)."),
            ("Milestone 4 — 20% (₹5,70,000):", "Upon Production Go-Live, Training & System Handover (Day 90).")
        ], GOLD_ACCENT),
        ("3. POST-GO-LIVE SUPPORT (AMS)", "Hypercare + Ongoing Retainer", [
            ("60-Day Dedicated Hypercare:", "INCLUDED at zero extra cost. On-site & remote stabilization, daily standups, and tuning."),
            ("Ongoing AMS Support:", "Time & Material (T&M) Retainer billed quarterly based on consumed effort hours."),
            ("Guaranteed SLA Tiers:", "• P1 (Production Halt): 2 Hr Response\n• P2 (Feature Degradation): 4 Hr Response\n• P3 (General Query): 8 Hr Response")
        ], EMERALD_GREEN)
    ]
    
    col_w10 = 3.75
    spacing_c10 = 0.24
    for idx, (title, sub, items, border_c) in enumerate(comm_cards_s10):
        c_left = 0.8 + idx * (col_w10 + spacing_c10)
        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(col_w10), Inches(5.1))
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
        
        p_sub = tf_c.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(9)
        p_sub.font.italic = True
        p_sub.font.color.rgb = TEXT_LIGHT_MUTED
        p_sub.space_after = Pt(12)
        
        for item_h, item_d in items:
            p_it = tf_c.add_paragraph()
            p_it.space_after = Pt(8)
            r1 = p_it.add_run()
            r1.text = item_h + "\n"
            r1.font.bold = True
            r1.font.size = Pt(8.5)
            r1.font.color.rgb = TEXT_LIGHT
            r2 = p_it.add_run()
            r2.text = item_d
            r2.font.bold = False
            r2.font.size = Pt(8.2)
            r2.font.color.rgb = TEXT_LIGHT_MUTED

    add_footer(s10, 10, is_dark=True)

    # =============================================================
    # SLIDE 11: Assumptions, Dependencies & Terms (Tell: Governance)
    # =============================================================
    s11 = add_base_slide(is_dark=False)
    add_header(s11, "Assumptions, Technical Dependencies & Commercial Terms", "GOVERNANCE & ENGAGEMENT TERMS", "Clear boundaries, client prerequisites, and contractual governance for predictable execution")
    
    terms_cards_s11 = [
        ("1. Client Dependencies (Hical)", [
            ("SAP OData Service Exposure:", "Hical IT to expose standard read-only OData endpoints with HTTPS network accessibility to middle tier."),
            ("Environment & Test Data:", "Provisioning of SAP Sandbox/Quality systems with active BOMs and discrete routing master data within 5 days of kickoff."),
            ("Rugged HHT Hardware:", "Hical to supply required Zebra/Honeywell handheld terminals with barcode wedge drivers and ensure floor Wi-Fi coverage.")
        ], SAP_BLUE),
        ("2. Key Architectural Assumptions", [
            ("Strictly Non-Invasive:", "SAP remains 100% read-only throughout. No custom ABAP write-back tables, direct RFC write destinations, or BAPIs."),
            ("Booking Authority Retained:", "Physical posting of production confirmations (CO11N) and goods receipts (MIGO) into SAP GUI remains under Hical's authorized personnel."),
            ("Source Master Data:", "Master data consistency in SAP (material numbers, BOM revisions, vendor info) is maintained by Hical internal teams.")
        ], CYAN_ACCENT),
        ("3. Commercial Terms & Conditions", [
            ("Proposal Validity:", "Commercial pricing of ₹28,50,000 INR is valid for 45 calendar days from formal presentation."),
            ("Taxation & Payments:", "GST @ 18% extra as applicable. Invoices payable within 15 business days of electronic milestone submission."),
            ("100% IP Transfer to Hical:", "Complete source code, configuration scripts, and documentation transfer exclusively to Hical upon final settlement."),
            ("Confidentiality & NDA:", "Strict mutual confidentiality protecting Hical's proprietary aerospace BOMs, pricing, and manufacturing parameters.")
        ], EMERALD_GREEN)
    ]
    
    col_w11 = 3.75
    for idx, (title, points, border_c) in enumerate(terms_cards_s11):
        c_left = 0.8 + idx * (col_w11 + spacing_c10)
        card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(col_w11), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
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
            r1.font.color.rgb = TEXT_DARK
            r2 = p_pt.add_run()
            r2.text = pt_body
            r2.font.bold = False
            r2.font.size = Pt(8.0)
            r2.font.color.rgb = TEXT_MUTED

    add_footer(s11, 11, is_dark=False)

    # =============================================================
    # SLIDE 12: Executive Value Recap & Strategic ROI (Tell: Closing Recap)
    # =============================================================
    s12 = add_base_slide(is_dark=True)
    add_header(s12, "Executive Value Recap: Why TRACE n TRACE for Hical", "CLOSING VALUE RECAP & ROI", "Recapping major value drivers and strategic win themes delivering 3.8x to 6.1x First-Year ROI", is_dark=True)
    
    # Left Side: Win Themes Recap Card
    recap_card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.75), Inches(5.1))
    recap_card.fill.solid()
    recap_card.fill.fore_color.rgb = DARK_CARD
    recap_card.line.color.rgb = CYAN_ACCENT
    recap_card.line.width = Pt(1.5)
    
    tf_rc = recap_card.text_frame
    tf_rc.word_wrap = True
    tf_rc.margin_left = tf_rc.margin_right = Inches(0.2)
    tf_rc.margin_top = Inches(0.2)
    
    p = tf_rc.paragraphs[0]
    p.text = "FOUR STRATEGIC WIN THEMES"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(10)
    
    recap_items = [
        ("1. Zero SAP Core Risk:", "100% read-only OData architecture ensures zero database deadlocks, table locks, or schema corruption."),
        ("2. Huge Licensing Savings:", "Floor operators use open-standard rugged handheld terminals without needing expensive Named SAP Fiori licenses."),
        ("3. AS9100 Zero-Defect Enforcement:", "Hardware barcode Poka-Yoke halts wrong component batches, unapproved ECN revisions, and expired resins instantly."),
        ("4. Two-Tier Air-Gapped Governance:", "Supervisor PIN + QC digital stamp generates pre-verified Ready-to-Post slips (CO11N, MIGO, QE51N), keeping ERP postings 100% error-free.")
    ]
    for r_head, r_body in recap_items:
        p_it = tf_rc.add_paragraph()
        p_it.space_after = Pt(8)
        r1 = p_it.add_run()
        r1.text = r_head + "\n"
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = TEXT_LIGHT
        r2 = p_it.add_run()
        r2.text = r_body
        r2.font.bold = False
        r2.font.size = Pt(8.2)
        r2.font.color.rgb = TEXT_LIGHT_MUTED

    # Right Side: Financial ROI Table Card
    roi_card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.783), Inches(1.6), Inches(5.75), Inches(5.1))
    roi_card.fill.solid()
    roi_card.fill.fore_color.rgb = DARK_CARD
    roi_card.line.color.rgb = GOLD_ACCENT
    roi_card.line.width = Pt(1.5)
    
    tf_roi = roi_card.text_frame
    tf_roi.word_wrap = True
    tf_roi.margin_left = tf_roi.margin_right = Inches(0.2)
    tf_roi.margin_top = Inches(0.2)
    
    p = tf_roi.paragraphs[0]
    p.text = "TANGIBLE ANNUAL VALUE CREATION FOR HICAL"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    p.space_after = Pt(10)
    
    roi_table_data = [
        ("SAP License Cost Avoidance (150 Floor Users):", "₹45,00,000 – ₹75,00,000"),
        ("Assembly Rework & Scrap Eradication (Poka-Yoke):", "₹28,00,000 – ₹42,00,000"),
        ("Paper Traveler Shift-End Labor Recovery:", "₹15,00,000 – ₹22,00,000"),
        ("AS9100 Audit Defense & Penalty Avoidance:", "₹20,00,000 – ₹35,00,000"),
        ("TOTAL ESTIMATED ANNUAL VALUE RELEASE:", "₹1,08,00,000 – ₹1,74,00,000"),
        ("PROJECT PAYBACK PERIOD:", "3.5 to 4.5 Months (ROI: 3.8x – 6.1x)")
    ]
    
    for r_lbl, r_val in roi_table_data:
        p_row = tf_roi.add_paragraph()
        p_row.space_after = Pt(7)
        r1 = p_row.add_run()
        r1.text = r_lbl + "\n"
        r1.font.bold = ("TOTAL" in r_lbl or "PAYBACK" in r_lbl)
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = GOLD_ACCENT if ("TOTAL" in r_lbl or "PAYBACK" in r_lbl) else TEXT_LIGHT
        
        r2 = p_row.add_run()
        r2.text = r_val
        r2.font.bold = True
        r2.font.size = Pt(9.5 if ("TOTAL" in r_lbl or "PAYBACK" in r_lbl) else 8.5)
        r2.font.color.rgb = EMERALD_GREEN if ("TOTAL" in r_lbl or "PAYBACK" in r_lbl) else CYAN_ACCENT

    add_footer(s12, 12, is_dark=True)

    # Save presentation
    prs.save(output_path)
    print(f"Successfully generated TRACE n TRACE presentation: {output_path}")

if __name__ == "__main__":
    build_trace_presentation()
