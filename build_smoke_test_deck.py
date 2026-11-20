"""
Build Smoke-Test Deck: Supplier Delivery Tracker: CIO briefing
Generates an authentic 8-slide first-draft executive presentation in the Lumbini theme,
patches fonts/XML schema, and renders 1080p preview images to previews_smoke/.
"""

import os
import sys
import shutil
import zipfile
import tempfile
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from lxml import etree

from design_system.lumbini.theme_patcher import apply_lumbini_theme_to_pptx

# =============================================================================
# CONSTANTS & THEME TOKENS
# =============================================================================
FONT_TITLE = "Inter"
FONT_BODY = "Inter"

HEX_PRIMARY = "0070C0"       # Lumbini Blue
HEX_PRIMARY_DEEP = "002060"  # Lumbini Navy
HEX_ACCENT = "ED7D31"        # Lumbini Orange
HEX_TEXT_MAIN = "1E293B"     # Slate 800
HEX_MUTED = "475569"         # Slate 600
HEX_SURFACE = "F8FAFC"       # Light Slate
HEX_SURFACE_ALT = "F1F5F9"   # Slate 100
HEX_BORDER = "CBD5E1"        # Slate 300
HEX_BORDER_LIGHT = "E2E8F0"  # Slate 200
HEX_WHITE = "FFFFFF"
HEX_BLUE_BG = "EBF5FB"


def rgb(hex_str: str) -> RGBColor:
    h = hex_str.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def ensure_powerpoint_compatible_order(abs_path: str):
    pns = "http://schemas.openxmlformats.org/presentationml/2006/main"
    tmp_dir = tempfile.mkdtemp(prefix="pptx_order_")
    try:
        tmp_out = os.path.join(tmp_dir, "fixed.pptx")
        with zipfile.ZipFile(abs_path, "r") as zin, zipfile.ZipFile(tmp_out, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "ppt/presentation.xml":
                    root = etree.fromstring(data)
                    nm = root.find(f"{{{pns}}}notesMasterIdLst")
                    sl = root.find(f"{{{pns}}}sldIdLst")
                    if nm is not None and sl is not None:
                        root.remove(nm)
                        idx = list(root).index(sl) + 1
                        root.insert(idx, nm)
                    data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
                zout.writestr(item, data)
        with open(tmp_out, "rb") as src, open(abs_path, "wb") as dst:
            shutil.copyfileobj(src, dst)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


# =============================================================================
# HELPER PRIMITIVES
# =============================================================================
def add_card(slide, x, y, w, h, fill=HEX_SURFACE, border=HEX_BORDER, border_pt=1.0, rounded=True):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(fill) if fill else rgb(HEX_WHITE)
    if border:
        shape.line.color.rgb = rgb(border)
        shape.line.width = Pt(border_pt)
    else:
        shape.line.fill.background()
    return shape


def add_tb(slide, x, y, w, h, text, font=FONT_BODY, pt=12.0, color=HEX_TEXT_MAIN, weight="regular", align="left"):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.0)
    tf.margin_right = Inches(0.0)
    tf.margin_top = Inches(0.0)
    tf.margin_bottom = Inches(0.0)
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = font
    p.font.size = Pt(pt)
    p.font.color.rgb = rgb(color)
    p.font.bold = (weight == "bold")
    if align == "center":
        p.alignment = PP_ALIGN.CENTER
    elif align == "right":
        p.alignment = PP_ALIGN.RIGHT
    else:
        p.alignment = PP_ALIGN.LEFT
    return tb


def add_badge(slide, x, y, w, h, text, bg_hex=HEX_PRIMARY, text_hex=HEX_WHITE, pt=10.0):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(bg_hex)
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = False
    tf.margin_left = Inches(0.05)
    tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = FONT_BODY
    p.font.size = Pt(pt)
    p.font.bold = True
    p.font.color.rgb = rgb(text_hex)
    p.alignment = PP_ALIGN.CENTER
    return shape


def add_header(slide, title, subtitle=None):
    add_tb(slide, 0.50, 0.40, 12.33, 0.45, title, font=FONT_TITLE, pt=20.0, color=HEX_PRIMARY_DEEP, weight="bold")
    if subtitle:
        add_tb(slide, 0.50, 0.88, 12.33, 0.35, subtitle, font=FONT_BODY, pt=12.5, color=HEX_MUTED)


# =============================================================================
# SLIDE BUILDERS
# =============================================================================
def build_slide_1(prs):
    """Slide 1: Title Slide"""
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    for ph in list(slide.placeholders):
        sp = ph._element
        sp.getparent().remove(sp)

    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = rgb("F4F7FB")
    bg.line.fill.background()

    # Blue top accent banner
    top_band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.18))
    top_band.fill.solid()
    top_band.fill.fore_color.rgb = rgb(HEX_PRIMARY)
    top_band.line.fill.background()

    # Title Card container
    add_card(slide, 1.0, 1.6, 11.333, 4.4, fill=HEX_WHITE, border=HEX_BORDER_LIGHT, border_pt=1.5)

    add_badge(slide, 1.5, 2.1, 3.2, 0.36, "EXECUTIVE BRIEFING & CIO REVIEW", bg_hex=HEX_PRIMARY_DEEP, text_hex=HEX_WHITE, pt=10.5)

    add_tb(slide, 1.5, 2.7, 10.3, 0.85, "Supplier Delivery Tracker: CIO Briefing",
           font=FONT_TITLE, pt=32.0, color=HEX_PRIMARY_DEEP, weight="bold")
    
    add_tb(slide, 1.5, 3.65, 10.3, 0.55, "Real-Time Inbound Supply Chain Visibility & Plant Execution Architecture",
           font=FONT_BODY, pt=17.0, color=HEX_PRIMARY, weight="bold")

    add_tb(slide, 1.5, 4.45, 10.3, 0.45,
           "Prepared for: Chief Information Officer, Head of Supply Chain & Enterprise Architecture Board",
           font=FONT_BODY, pt=13.0, color=HEX_MUTED)
    add_tb(slide, 1.5, 4.95, 10.3, 0.40,
           "Presented by: Lumbini Elite Solutions & Services | Enterprise Solutions Practice",
           font=FONT_BODY, pt=12.0, color=HEX_MUTED)


def build_slide_2(prs):
    """Slide 2: Context & Current Friction"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    for ph in list(slide.placeholders):
        sp = ph._element
        sp.getparent().remove(sp)

    add_header(
        slide,
        title="Inbound Visibility Blind Spots Cause $2.4M in Freight Expedites and Line Halts",
        subtitle="Four manufacturing plants operate disconnected receiving processes, relying on phone calls and local spreadsheets."
    )

    # 3 Column Cards
    col_w = 3.8
    gap = 0.46
    start_x = 0.50

    cards_data = [
        ("DOCK ARRIVAL CHAOS", "4.2 Hrs Avg Yard Dwell", HEX_PRIMARY,
         "Truck arrivals are unscheduled and unpredictable. Security gates cross-check paper bills of lading against disconnected ERP printouts, causing long queues, congested yards, and driver detention fees."),
        ("PRODUCTION STOPPAGES", "18 Hrs/Mo Line Downtime", HEX_ACCENT,
         "Assembly lines suffer sudden critical part shortages. Plant supervisors learn about missing components only after shifts begin, triggering emergency changeovers and unbudgeted machine downtime."),
        ("EXPEDITED FREIGHT PENALTIES", "$2.4M Annual Waste", HEX_PRIMARY_DEEP,
         "Procurement teams lack upstream shipment tracking. Inbound delays force expensive emergency hot-shot freight runs and chartered air shipments to prevent customer delivery breaches.")
    ]

    for idx, (title, stat, color, desc) in enumerate(cards_data):
        cx = start_x + idx * (col_w + gap)
        add_card(slide, cx, 1.5, col_w, 4.2, fill=HEX_WHITE, border=HEX_BORDER, border_pt=1.0)
        
        # Color bar top
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(1.5), Inches(col_w), Inches(0.1))
        bar.fill.solid()
        bar.fill.fore_color.rgb = rgb(color)
        bar.line.fill.background()

        add_badge(slide, cx + 0.3, 1.8, col_w - 0.6, 0.32, title, bg_hex=color, text_hex=HEX_WHITE, pt=10.0)
        add_tb(slide, cx + 0.3, 2.3, col_w - 0.6, 0.5, stat, font=FONT_TITLE, pt=20.0, color=HEX_PRIMARY_DEEP, weight="bold", align="center")
        add_tb(slide, cx + 0.3, 3.0, col_w - 0.6, 2.3, desc, font=FONT_BODY, pt=12.5, color=HEX_TEXT_MAIN)

    # Bottom summary strip
    add_card(slide, 0.50, 6.0, 12.33, 0.85, fill=HEX_SURFACE, border=HEX_BORDER_LIGHT)
    add_tb(slide, 0.70, 6.15, 11.93, 0.55,
           "Key Takeaway: Plant-level operational opacity forces reactive firefighting across all four facilities. An enterprise solution must connect suppliers, logistics carriers, and receiving docks directly into core planning.",
           font=FONT_BODY, pt=12.0, color=HEX_MUTED)


def build_slide_3(prs):
    """Slide 3: Proposed Architecture"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    for ph in list(slide.placeholders):
        sp = ph._element
        sp.getparent().remove(sp)

    add_header(
        slide,
        title="Proposed Architecture: Cloud Portal Captures Shipments with Nightly ERP Batch Sync",
        subtitle="Suppliers submit advance shipping notices into an isolated cloud database, synchronizing with SAP core overnight."
    )

    # 4 Flow Blocks
    blocks = [
        ("1. SUPPLIERS & CARRIERS", "External Portal Input", "Suppliers log into dedicated web portal to enter PO numbers, dispatched quantities, and carrier tracking IDs prior to departure."),
        ("2. CLOUD TRACKER DATABASE", "Isolated PostgreSQL Store", "A standalone cloud database stores active shipments, tracking milestones, and supplier compliance metrics independently from ERP."),
        ("3. NIGHTLY BATCH EXTRACT", "Scheduled Cron SFTP Job", "Every night at 02:00 AM, a scheduled ETL script extracts daily receiving events and pushes a consolidated flat CSV file to the corporate SFTP."),
        ("4. SAP ERP BACKBONE", "Central System of Record", "Corporate SAP S/4HANA core ingests the batch file the following morning to update PO line-item goods receipt records and release vendor invoices.")
    ]

    bx_w = 2.85
    bx_gap = 0.31
    for idx, (b_title, b_sub, b_desc) in enumerate(blocks):
        bx = 0.50 + idx * (bx_w + bx_gap)
        add_card(slide, bx, 1.5, bx_w, 4.3, fill=HEX_WHITE, border=HEX_BORDER, border_pt=1.0)
        
        add_badge(slide, bx + 0.15, 1.7, bx_w - 0.3, 0.32, b_title, bg_hex=HEX_PRIMARY_DEEP if idx < 3 else HEX_PRIMARY, pt=10.0)
        add_tb(slide, bx + 0.15, 2.2, bx_w - 0.3, 0.35, b_sub, font=FONT_TITLE, pt=12.5, color=HEX_PRIMARY, weight="bold", align="center")
        add_tb(slide, bx + 0.15, 2.7, bx_w - 0.3, 2.8, b_desc, font=FONT_BODY, pt=12.0, color=HEX_TEXT_MAIN)

    # Architecture Callout
    add_card(slide, 0.50, 6.05, 12.33, 0.85, fill=HEX_BLUE_BG, border=HEX_PRIMARY)
    add_tb(slide, 0.70, 6.18, 11.93, 0.55,
           "Architectural Characteristic: Direct supplier input into isolated database; batch sync to core ERP. Avoids direct ERP API calls to minimize initial integration complexity.",
           font=FONT_BODY, pt=12.0, color=HEX_PRIMARY_DEEP, weight="bold")


def build_slide_4(prs):
    """Slide 4: Shopfloor Dock Receiving"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    for ph in list(slide.placeholders):
        sp = ph._element
        sp.getparent().remove(sp)

    add_header(
        slide,
        title="Receiving Dock Teams Capture Physical Arrival and Quality on Mobile Tablets",
        subtitle="Material coordinators scan barcodes, log visual defects, and stage materials prior to ERP goods receipt."
    )

    steps = [
        ("Step 1: Gate Check-In", "Driver arrives at plant gate; security matches paper BOL to tracker portal records."),
        ("Step 2: Bay Offload & Scan", "Dock coordinator uses 10-inch Android tablet with Bluetooth ring scanner to scan pallet barcode."),
        ("Step 3: Visual QA Check", "Coordinator confirms packaging integrity, counts cartons, and logs any damage photos."),
        ("Step 4: Staging Bay Putaway", "Forklift operator transports accepted pallets to shopfloor raw material staging bays."),
        ("Step 5: Batch GR Posting", "ERP clerk manually keys bulk Goods Receipts into SAP ERP at end-of-day or relies on nightly batch.")
    ]

    sy = 1.55
    for idx, (st_name, st_desc) in enumerate(steps):
        add_card(slide, 0.50, sy, 12.33, 0.80, fill=HEX_WHITE, border=HEX_BORDER_LIGHT)
        add_badge(slide, 0.70, sy + 0.22, 2.2, 0.36, st_name, bg_hex=HEX_PRIMARY, pt=11.0)
        add_tb(slide, 3.10, sy + 0.18, 9.50, 0.48, st_desc, font=FONT_BODY, pt=12.5, color=HEX_TEXT_MAIN)
        sy += 0.88

    add_card(slide, 0.50, 6.10, 12.33, 0.80, fill=HEX_SURFACE, border=HEX_BORDER)
    add_tb(slide, 0.70, 6.22, 11.93, 0.55,
           "Operational Impact: Replaces clipboard spreadsheets on the dock with tablet entry, while maintaining separate end-of-day ERP transactional updates.",
           font=FONT_BODY, pt=12.0, color=HEX_MUTED)


def build_slide_5(prs):
    """Slide 5: Supplier OTIF & Scorecards"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    for ph in list(slide.placeholders):
        sp = ph._element
        sp.getparent().remove(sp)

    add_header(
        slide,
        title="On-Time In-Full Scorecards with Local Re-Rating and Redirection Rights",
        subtitle="Automated vendor ratings empower dock supervisors to immediately alter supplier tiers."
    )

    # 3 Scorecard Cards
    col_w = 3.8
    gap = 0.46
    kpis = [
        ("VENDOR OTIF COMPLIANCE", "78.4%", "Target: 95.0%", HEX_PRIMARY,
         "Calculates On-Time In-Full delivery rate based on supplier promised dispatch date vs physical plant gate arrival timestamp."),
        ("DOCK REJECTION RATE", "3.8%", "Target: < 1.0%", HEX_ACCENT,
         "Tracks percentage of inbound shipments quarantined or rejected due to physical carton damage, barcode errors, or wrong counts."),
        ("CARRIER YARD DWELL TIME", "252 Mins", "Target: 60 Mins", HEX_PRIMARY_DEEP,
         "Measures total elapsed time from truck arrival at security gate to complete pallet offload and gate checkout.")
    ]

    for idx, (title, stat, target, color, desc) in enumerate(kpis):
        cx = 0.50 + idx * (col_w + gap)
        add_card(slide, cx, 1.5, col_w, 3.5, fill=HEX_WHITE, border=HEX_BORDER)
        add_badge(slide, cx + 0.2, 1.7, col_w - 0.4, 0.32, title, bg_hex=color, pt=10.0)
        add_tb(slide, cx + 0.2, 2.15, col_w - 0.4, 0.5, stat, font=FONT_TITLE, pt=26.0, color=HEX_PRIMARY_DEEP, weight="bold", align="center")
        add_tb(slide, cx + 0.2, 2.7, col_w - 0.4, 0.3, target, font=FONT_BODY, pt=12.0, color=color, weight="bold", align="center")
        add_tb(slide, cx + 0.2, 3.1, col_w - 0.4, 1.7, desc, font=FONT_BODY, pt=11.5, color=HEX_TEXT_MAIN)

    # Policy Card: Decision Rights Red Flag
    add_card(slide, 0.50, 5.25, 12.33, 1.65, fill=HEX_SURFACE_ALT, border=HEX_ACCENT, border_pt=1.5)
    add_badge(slide, 0.70, 5.42, 3.2, 0.34, "OPERATIONAL GOVERNANCE & RIGHTS", bg_hex=HEX_ACCENT, pt=10.5)
    add_tb(slide, 0.70, 5.85, 11.93, 0.95,
           "Autonomous Dock Governance: When a supplier drops below 80% OTIF, dock supervisors have direct authority within the portal to downgrade supplier qualification tier and reroute upcoming purchase order shipments to secondary backup vendors without awaiting central procurement review.",
           font=FONT_BODY, pt=12.5, color=HEX_TEXT_MAIN)


def build_slide_6(prs):
    """Slide 6: Technology Stack & Microservices"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    for ph in list(slide.placeholders):
        sp = ph._element
        sp.getparent().remove(sp)

    add_header(
        slide,
        title="Custom React Frontend with Node.js Microservices and Isolated PostgreSQL Storage",
        subtitle="Modern lightweight microservices stack designed for rapid standalone deployment."
    )

    layers = [
        ("PRESENTATION LAYER", "React 18 SPA + TailwindCSS",
         "Mobile-first responsive web UI deployed on AWS CloudFront. Optimized for tablet touch interactions and handheld barcode scanner pairing."),
        ("APPLICATION SERVICES", "Node.js / Express Microservices",
         "Containerized REST API services running on Amazon ECS. Handles shipment tracking logic, notification dispatch, and OTIF calculations."),
        ("DATA STORAGE", "Dedicated PostgreSQL 15 Instance",
         "Isolated Amazon RDS PostgreSQL database storing supplier profiles, shipment records, dock timestamps, and user audit trails."),
        ("DOCUMENT STORAGE", "Amazon S3 Bucket Storage",
         "Secure cloud object repository storing high-resolution damage photos, scanned bills of lading, and signed delivery certificates.")
    ]

    col_w = 2.85
    gap = 0.31
    for idx, (l_title, l_tech, l_desc) in enumerate(layers):
        cx = 0.50 + idx * (col_w + gap)
        add_card(slide, cx, 1.5, col_w, 4.3, fill=HEX_WHITE, border=HEX_BORDER)
        add_badge(slide, cx + 0.15, 1.7, col_w - 0.3, 0.32, l_title, bg_hex=HEX_PRIMARY_DEEP, pt=10.0)
        add_tb(slide, cx + 0.15, 2.2, col_w - 0.3, 0.45, l_tech, font=FONT_TITLE, pt=13.0, color=HEX_PRIMARY, weight="bold", align="center")
        add_tb(slide, cx + 0.15, 2.8, col_w - 0.3, 2.8, l_desc, font=FONT_BODY, pt=12.0, color=HEX_TEXT_MAIN)

    add_card(slide, 0.50, 6.05, 12.33, 0.85, fill=HEX_SURFACE, border=HEX_BORDER_LIGHT)
    add_tb(slide, 0.70, 6.20, 11.93, 0.55,
           "Architectural Isolation: Completely decoupled cloud stack with no direct dependency on enterprise SAP middleware or central master data governance.",
           font=FONT_BODY, pt=12.0, color=HEX_MUTED)


def build_slide_7(prs):
    """Slide 7: Phased Implementation Roadmap"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    for ph in list(slide.placeholders):
        sp = ph._element
        sp.getparent().remove(sp)

    add_header(
        slide,
        title="Phase 1 Deploys Standalone Portal to Plant 1 in 8 Weeks; Other Plants Follow",
        subtitle="Single-plant pilot proves functionality before rolling out to remaining manufacturing facilities."
    )

    phases = [
        ("PHASE 1: PLANT 1 PILOT", "Weeks 1 – 8", HEX_PRIMARY,
         "Deploy portal for Plant 1 dock operations. Onboard top 20 component suppliers. Configure local PostgreSQL database and establish manual dock workflows."),
        ("PHASE 2: PLANT 2 EXPANSION", "Weeks 9 – 16", HEX_PRIMARY_DEEP,
         "Replicate standalone setup at Plant 2. Expand supplier onboarding to 50 vendors. Implement nightly batch SFTP CSV export to corporate ERP."),
        ("PHASE 3: PLANTS 3 & 4 ROLLOUT", "Weeks 17 – 24", HEX_ACCENT,
         "Standardize dock receiving across remaining regional plants. Roll out mobile tablets and establish cross-plant delivery benchmarking."),
        ("PHASE 4: ENTERPRISE EVALUATION", "Weeks 25 – 32", "0F766E",
         "Evaluate real-time SAP S/4HANA OData API integration to replace nightly batch script. Review enterprise master data governance alignment.")
    ]

    col_w = 2.85
    gap = 0.31
    for idx, (p_title, p_time, p_color, p_desc) in enumerate(phases):
        cx = 0.50 + idx * (col_w + gap)
        add_card(slide, cx, 1.5, col_w, 4.3, fill=HEX_WHITE, border=HEX_BORDER)
        add_badge(slide, cx + 0.15, 1.7, col_w - 0.3, 0.32, p_title, bg_hex=p_color, pt=10.0)
        add_tb(slide, cx + 0.15, 2.2, col_w - 0.3, 0.4, p_time, font=FONT_TITLE, pt=14.0, color=p_color, weight="bold", align="center")
        add_tb(slide, cx + 0.15, 2.8, col_w - 0.3, 2.8, p_desc, font=FONT_BODY, pt=12.0, color=HEX_TEXT_MAIN)

    add_card(slide, 0.50, 6.05, 12.33, 0.85, fill=HEX_SURFACE, border=HEX_BORDER_LIGHT)
    add_tb(slide, 0.70, 6.20, 11.93, 0.55,
           "Deployment Model: Sequential rollout by manufacturing site. Core enterprise ERP integration deferred to post-Phase 3 evaluation.",
           font=FONT_BODY, pt=12.0, color=HEX_MUTED)


def build_slide_8(prs):
    """Slide 8: Financial Investment & Decision Requested"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    for ph in list(slide.placeholders):
        sp = ph._element
        sp.getparent().remove(sp)

    add_header(
        slide,
        title="Approval Requested for $420,000 Implementation Budget to Launch Plant 1 Tracker",
        subtitle="Initial capital request funds software development, tablet hardware, and single-site deployment."
    )

    # Left: Commercial Breakdown Table Card
    add_card(slide, 0.50, 1.5, 7.5, 4.3, fill=HEX_WHITE, border=HEX_BORDER)
    add_badge(slide, 0.70, 1.7, 3.2, 0.32, "PHASE 1 INVESTMENT BREAKDOWN", bg_hex=HEX_PRIMARY_DEEP, pt=10.0)

    rows = [
        ("Custom React & Node.js Application Development", "$180,000"),
        ("Mobile Android Tablets & Rugged Scanners (20 units)", "$50,000"),
        ("Nightly Batch ETL & SFTP Interface Development", "$70,000"),
        ("Plant 1 Change Management, User Training & Go-Live", "$60,000"),
        ("Project Management, Cloud Hosting & Contingency", "$60,000"),
        ("Total Phase 1 Capital & Operational Expenditure", "$420,000")
    ]

    ry = 2.2
    for r_idx, (item, cost) in enumerate(rows):
        is_total = (r_idx == len(rows) - 1)
        bg_col = HEX_BLUE_BG if is_total else (HEX_WHITE if r_idx % 2 == 0 else HEX_SURFACE)
        row_card = add_card(slide, 0.70, ry, 7.1, 0.48, fill=bg_col, border=HEX_BORDER_LIGHT if not is_total else HEX_PRIMARY)
        txt_col = HEX_PRIMARY_DEEP if is_total else HEX_TEXT_MAIN
        wt = "bold" if is_total else "regular"
        add_tb(slide, 0.85, ry + 0.1, 5.0, 0.3, item, font=FONT_BODY, pt=11.5, color=txt_col, weight=wt)
        add_tb(slide, 6.0, ry + 0.1, 1.6, 0.3, cost, font=FONT_TITLE if is_total else FONT_BODY, pt=12.5 if is_total else 11.5, color=txt_col, weight="bold", align="right")
        ry += 0.55

    # Right: Decision Requested Card
    add_card(slide, 8.30, 1.5, 4.53, 4.3, fill=HEX_WHITE, border=HEX_ACCENT, border_pt=1.5)
    add_badge(slide, 8.60, 1.7, 3.2, 0.32, "DECISION REQUESTED TODAY", bg_hex=HEX_ACCENT, pt=10.0)

    add_tb(slide, 8.60, 2.3, 3.93, 0.35, "Action Required from CIO & Board:", font=FONT_TITLE, pt=13.0, color=HEX_PRIMARY_DEEP, weight="bold")
    add_tb(slide, 8.60, 2.75, 3.93, 2.8,
           "1. Authorize $420,000 budget allocation for Phase 1 development and Plant 1 pilot rollout.\n\n"
           "2. Approve procurement of 20 rugged Android warehouse tablets and ring scanners.\n\n"
           "3. Grant approval to establish nightly scheduled flat-file SFTP export with corporate SAP ERP team.\n\n"
           "4. Appoint Plant 1 Logistics Lead as Project Sponsor for the 8-week pilot.",
           font=FONT_BODY, pt=12.0, color=HEX_TEXT_MAIN)

    add_card(slide, 0.50, 6.05, 12.33, 0.85, fill=HEX_SURFACE, border=HEX_BORDER_LIGHT)
    add_tb(slide, 0.70, 6.20, 11.93, 0.55,
           "ROI Justification: Eliminating 25% of current $2.4M expedited freight ($600K/year) pays back the full Phase 1 investment in under 9 months.",
           font=FONT_BODY, pt=12.0, color=HEX_MUTED)


# =============================================================================
# EXPORT AND RENDERING
# =============================================================================
def main():
    template_path = os.path.abspath("themes/lumbini/template.pptx")
    out_pptx = os.path.abspath("Supplier_Delivery_Tracker_CIO_Briefing.pptx")
    img_dir = os.path.abspath("previews_smoke")

    print(f"Loading template: {template_path}")
    prs = Presentation(template_path)

    # Clear existing slides in template
    while len(prs.slides) > 0:
        sp = prs.slides[0]._element
        sp.getparent().remove(sp)

    print("Building 8 slides for Supplier Delivery Tracker...")
    build_slide_1(prs)
    build_slide_2(prs)
    build_slide_3(prs)
    build_slide_4(prs)
    build_slide_5(prs)
    build_slide_6(prs)
    build_slide_7(prs)
    build_slide_8(prs)

    tmp_dir = tempfile.mkdtemp(prefix="smoke_stage_")
    try:
        staged = os.path.join(tmp_dir, "staged.pptx")
        prs.save(staged)
        print("Applying Lumbini theme typography (Inter font)...")
        apply_lumbini_theme_to_pptx(staged)
        print("Ensuring PowerPoint schema-compatible order...")
        ensure_powerpoint_compatible_order(staged)
        with open(staged, "rb") as src, open(out_pptx, "wb") as dst:
            shutil.copyfileobj(src, dst)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    print(f"Generated PowerPoint: {out_pptx}")

    # Render slides to 1080p images using PowerPoint COM
    print("Rendering slides to 1080p PNG images in previews_smoke/...")
    import win32com.client
    ppt_app = win32com.client.Dispatch("PowerPoint.Application")
    try:
        prs_com = ppt_app.Presentations.Open(out_pptx, WithWindow=False)
        os.makedirs(img_dir, exist_ok=True)
        for i, slide in enumerate(prs_com.Slides, 1):
            out_img = os.path.join(img_dir, f"slide_{i}.png")
            slide.Export(out_img, "PNG", 1920, 1080)
            print(f"  Exported Slide {i} -> {out_img}")
        prs_com.Close()
        print("All 8 slides successfully exported!")
    finally:
        ppt_app.Quit()


if __name__ == "__main__":
    main()
