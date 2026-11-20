"""
Build Smoke-Test Deck: Supplier Delivery Tracker: CIO briefing
Generates the fully refined, executive-ready 8-slide presentation in the Lumbini theme,
reflecting the 14 expert scrutiny perspectives (zero P1 blockers, closed-loop MES,
SAP S/4HANA single system of record, DBR constraint protection, and human dignity).
"""

import os
import sys
import shutil
import zipfile
import tempfile
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
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
# SLIDE BUILDERS (REFINED & WITHSTANDS SCRUTINY)
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

    top_band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.18))
    top_band.fill.solid()
    top_band.fill.fore_color.rgb = rgb(HEX_PRIMARY)
    top_band.line.fill.background()

    add_card(slide, 1.0, 1.6, 11.333, 4.4, fill=HEX_WHITE, border=HEX_BORDER_LIGHT, border_pt=1.5)

    add_badge(slide, 1.5, 2.1, 3.6, 0.36, "ENTERPRISE ARCHITECTURE & CIO REVIEW", bg_hex=HEX_PRIMARY_DEEP, text_hex=HEX_WHITE, pt=10.5)

    add_tb(slide, 1.5, 2.7, 10.3, 0.85, "Supplier Delivery Tracker: CIO Briefing",
           font=FONT_TITLE, pt=32.0, color=HEX_PRIMARY_DEEP, weight="bold")
    
    add_tb(slide, 1.5, 3.65, 10.3, 0.55, "Closed-Loop Inbound Execution, Constraint Protection & SAP S/4HANA Integration",
           font=FONT_BODY, pt=17.0, color=HEX_PRIMARY, weight="bold")

    add_tb(slide, 1.5, 4.45, 10.3, 0.45,
           "Prepared for: Chief Information Officer, Head of Supply Chain & Enterprise Architecture Board",
           font=FONT_BODY, pt=13.0, color=HEX_MUTED)
    add_tb(slide, 1.5, 4.95, 10.3, 0.40,
           "Presented by: Lumbini Elite Solutions & Services | Enterprise Solutions Practice",
           font=FONT_BODY, pt=12.0, color=HEX_MUTED)


def build_slide_2(prs):
    """Slide 2: Context & Friction (Grounded Operational Realities)"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    for ph in list(slide.placeholders):
        sp = ph._element
        sp.getparent().remove(sp)

    add_header(
        slide,
        title="Inbound Opacity Causes $2.4M Freight Expedites, Line Starvation, and Frontline Strain",
        subtitle="Fragmented plant receiving disconnects shopfloor assembly constraints from upstream enterprise visibility."
    )

    col_w = 3.8
    gap = 0.46
    start_x = 0.50

    cards_data = [
        ("YARD CONGESTION & DETENTION", "4.2 Hrs Avg Yard Dwell", HEX_PRIMARY,
         "Unscheduled truck arrivals cause yard gridlock. Independent long-haul drivers wait without staging countdowns or shelter. Gate security matches paper bills against stale ERP printouts with high friction."),
        ("CONSTRAINT LINE STARVATION", "18 Hrs/Mo Bottleneck Downtime", HEX_ACCENT,
         "Assembly lines suffer sudden critical part shortages. Plant supervisors learn about missing components mid-shift, triggering frantic emergency changeovers, idle operators, and lost throughput."),
        ("REACTIVE EXPEDITED FREIGHT", "$2.4M Annual Hot-Shot Waste", HEX_PRIMARY_DEEP,
         "Procurement lacks upstream transit visibility. When delays are discovered late, teams panic-expedite components via chartered air and spot-market couriers to avoid customer delivery breach penalties.")
    ]

    for idx, (title, stat, color, desc) in enumerate(cards_data):
        cx = start_x + idx * (col_w + gap)
        add_card(slide, cx, 1.5, col_w, 4.2, fill=HEX_WHITE, border=HEX_BORDER, border_pt=1.0)
        
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(1.5), Inches(col_w), Inches(0.1))
        bar.fill.solid()
        bar.fill.fore_color.rgb = rgb(color)
        bar.line.fill.background()

        add_badge(slide, cx + 0.3, 1.8, col_w - 0.6, 0.32, title, bg_hex=color, text_hex=HEX_WHITE, pt=10.0)
        add_tb(slide, cx + 0.3, 2.3, col_w - 0.6, 0.5, stat, font=FONT_TITLE, pt=20.0, color=HEX_PRIMARY_DEEP, weight="bold", align="center")
        add_tb(slide, cx + 0.3, 3.0, col_w - 0.6, 2.3, desc, font=FONT_BODY, pt=12.0, color=HEX_TEXT_MAIN)

    add_card(slide, 0.50, 6.0, 12.33, 0.85, fill=HEX_SURFACE, border=HEX_BORDER_LIGHT)
    add_tb(slide, 0.70, 6.15, 11.93, 0.55,
           "Key Takeaway: Disconnected point solutions cause reactive tampering and human stress. We must bridge suppliers, logistics carriers, and receiving docks directly into SAP S/4HANA and shopfloor MES.",
           font=FONT_BODY, pt=12.0, color=HEX_MUTED)


def build_slide_3(prs):
    """Slide 3: Proposed Architecture (Single System of Record & Edge Resiliency)"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    for ph in list(slide.placeholders):
        sp = ph._element
        sp.getparent().remove(sp)

    add_header(
        slide,
        title="Integrated Architecture: Resilient Edge Dock Execution with Event-Driven SAP Core",
        subtitle="Authoritative Single System of Record in SAP S/4HANA; local edge gateway ensures zero plant downtime."
    )

    blocks = [
        ("1. SUPPLIERS & CARRIERS", "Open Portal & Webhooks",
         "Suppliers submit digital ASNs with lot/batch details. Truck drivers receive automated SMS bay staging countdowns and self-service arrival check-in."),
        ("2. RESILIENT EDGE GATEWAY", "Plant L3 In-Memory Cache",
         "Local Docker edge gateway runs dock scanning offline. Sub-second barcode scans execute without WAN dependency; queues events during network drops."),
        ("3. EVENT-DRIVEN API SYNC", "Kafka / OData Integration",
         "Near-real-time event streaming reconciles dock events to SAP S/4HANA via secure REST/OData APIs (MIGO/BAPI) within 60 seconds of physical scan."),
        ("4. SAP CORE & MES BACKBONE", "Single System of Record",
         "SAP S/4HANA updates inventory goods receipts and invoice releases. Closed-loop events immediately update shopfloor MES finite line schedules.")
    ]

    bx_w = 2.85
    bx_gap = 0.31
    for idx, (b_title, b_sub, b_desc) in enumerate(blocks):
        bx = 0.50 + idx * (bx_w + bx_gap)
        add_card(slide, bx, 1.5, bx_w, 4.3, fill=HEX_WHITE, border=HEX_BORDER, border_pt=1.0)
        
        add_badge(slide, bx + 0.15, 1.7, bx_w - 0.3, 0.32, b_title, bg_hex=HEX_PRIMARY_DEEP if idx < 3 else HEX_PRIMARY, pt=10.0)
        add_tb(slide, bx + 0.15, 2.2, bx_w - 0.3, 0.35, b_sub, font=FONT_TITLE, pt=12.5, color=HEX_PRIMARY, weight="bold", align="center")
        add_tb(slide, bx + 0.15, 2.7, bx_w - 0.3, 2.8, b_desc, font=FONT_BODY, pt=11.5, color=HEX_TEXT_MAIN)

    add_card(slide, 0.50, 6.05, 12.33, 0.85, fill=HEX_BLUE_BG, border=HEX_PRIMARY)
    add_tb(slide, 0.70, 6.18, 11.93, 0.55,
           "Single System of Record Architecture: SAP S/4HANA remains the authoritative ERP core. Resilient Level 3 edge caching prevents plant outages without creating uncoordinated shadow master data stores.",
           font=FONT_BODY, pt=12.0, color=HEX_PRIMARY_DEEP, weight="bold")


def build_slide_4(prs):
    """Slide 4: Shopfloor Dock Receiving (ISA-95 Lots & Frontline Dignity)"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    for ph in list(slide.placeholders):
        sp = ph._element
        sp.getparent().remove(sp)

    add_header(
        slide,
        title="Shopfloor Dock Execution: Ergonomic Assistant with ISA-95 Lot Traceability & QA",
        subtitle="Ruggedized mobile tools with operator override rights, lot/batch tracking, and automated SAP QM inspection lots."
    )

    steps = [
        ("Step 1: Gate Check-In & Hospitality", "Driver checks in via mobile SMS or gate kiosk; assigned staging bay countdown; access to driver amenities lounge."),
        ("Step 2: Glove-Friendly Pallet Scan", "Dock coordinator scans 2D barcode using high-contrast rugged tablet (>48px targets); captures Vendor Lot, Internal Batch, and Expiry."),
        ("Step 3: ISA-95 QM Inspection Lot", "Automated SAP QM Inspection Lot generated; damaged cartons or label mismatches routed to designated physical Quarantine Bay."),
        ("Step 4: Constraint Staging Putaway", "Forklift operator transports pallets to staging bays prioritized by Drum-Buffer-Rope line starvation status in MES."),
        ("Step 5: Immediate SAP GR Posting", "Real-time MIGO Goods Receipt posted to SAP S/4HANA via OData API within 60 seconds; eliminates end-of-day batch bottlenecks.")
    ]

    sy = 1.55
    for idx, (st_name, st_desc) in enumerate(steps):
        add_card(slide, 0.50, sy, 12.33, 0.80, fill=HEX_WHITE, border=HEX_BORDER_LIGHT)
        add_badge(slide, 0.70, sy + 0.22, 2.6, 0.36, st_name, bg_hex=HEX_PRIMARY, pt=10.5)
        add_tb(slide, 3.40, sy + 0.18, 9.20, 0.48, st_desc, font=FONT_BODY, pt=12.0, color=HEX_TEXT_MAIN)
        sy += 0.88

    add_card(slide, 0.50, 6.10, 12.33, 0.80, fill=HEX_SURFACE, border=HEX_BORDER)
    add_tb(slide, 0.70, 6.22, 11.93, 0.55,
           "Human-Centered Design: Empowers dock specialists with situational override authority; ruggedized hardware adapts to cold weather and thick gloves while eliminating surveillance pacing.",
           font=FONT_BODY, pt=12.0, color=HEX_MUTED)


def build_slide_5(prs):
    """Slide 5: Statistical Process Control & AI Decision Copilot"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    for ph in list(slide.placeholders):
        sp = ph._element
        sp.getparent().remove(sp)

    add_header(
        slide,
        title="Statistical Process Control & AI Decision Copilot Replace Knee-Jerk Vendor Tampering",
        subtitle="Deming Shewhart charts separate systemic noise from special cause; central procurement retains commercial governance."
    )

    col_w = 3.8
    gap = 0.46
    kpis = [
        ("STATISTICAL OTIF (SPC)", "88.2% Stable", "UCL: 94% | LCL: 82%", HEX_PRIMARY,
         "Monitors vendor delivery variance using Shewhart control charts. Distinguishes common-cause traffic noise from genuine special-cause systemic supplier failure."),
        ("CONSTRAINT BUFFER HEALTH", "94.6%", "DBR Target: > 92.0%", HEX_ACCENT,
         "Tracks real-time component buffer penetration feeding bottleneck assembly lines, alerting line schedulers hours before physical starvation occurs."),
        ("DRIVER YARD EFFICIENCY", "42 Mins", "Target: < 45 Mins", HEX_PRIMARY_DEEP,
         "Measures total elapsed driver gate dwell; integrates automated SMS bay notifications and hospitality scoring to eliminate detention penalties.")
    ]

    for idx, (title, stat, target, color, desc) in enumerate(kpis):
        cx = 0.50 + idx * (col_w + gap)
        add_card(slide, cx, 1.5, col_w, 3.5, fill=HEX_WHITE, border=HEX_BORDER)
        add_badge(slide, cx + 0.2, 1.7, col_w - 0.4, 0.32, title, bg_hex=color, pt=10.0)
        add_tb(slide, cx + 0.2, 2.15, col_w - 0.4, 0.5, stat, font=FONT_TITLE, pt=24.0, color=HEX_PRIMARY_DEEP, weight="bold", align="center")
        add_tb(slide, cx + 0.2, 2.7, col_w - 0.4, 0.3, target, font=FONT_BODY, pt=11.5, color=color, weight="bold", align="center")
        add_tb(slide, cx + 0.2, 3.1, col_w - 0.4, 1.7, desc, font=FONT_BODY, pt=11.5, color=HEX_TEXT_MAIN)

    add_card(slide, 0.50, 5.25, 12.33, 1.65, fill=HEX_SURFACE_ALT, border=HEX_PRIMARY_DEEP, border_pt=1.5)
    add_badge(slide, 0.70, 5.42, 3.8, 0.34, "GOVERNED DECISION RIGHTS & AI COPILOT", bg_hex=HEX_PRIMARY_DEEP, pt=10.5)
    add_tb(slide, 0.70, 5.85, 11.93, 0.95,
           "Governed Enterprise Decision Rights: Dock supervisors annotate operational exceptions and capture context. Central category managers are assisted by an AI Decision Copilot that models supplier capacity and transit risk with confidence intervals. Eliminates unauthorized rogue PO rerouting.",
           font=FONT_BODY, pt=12.0, color=HEX_TEXT_MAIN)


def build_slide_6(prs):
    """Slide 6: Hybrid Cloud-Edge Architecture & Security"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    for ph in list(slide.placeholders):
        sp = ph._element
        sp.getparent().remove(sp)

    add_header(
        slide,
        title="Hybrid Cloud-Edge Architecture with Enterprise Security and Open Carrier APIs",
        subtitle="Modern containerized microservices integrated with corporate IAM, SAP S/4HANA, and plant MES."
    )

    layers = [
        ("EDGE PRESENTATION LAYER", "React PWA + Glove Mode",
         "Ruggedized, mobile-first responsive PWA deployed on plant edge gateways. Features high-contrast outdoor mode, large tap targets, and driver self-service web/SMS."),
        ("INTEGRATION & EVENT BUS", "Apache Kafka / EventBridge",
         "Near-real-time publish/subscribe event topics stream ISA-95 B2MML compliant messages: ASN received, gate arrived, lot inspected, and staged."),
        ("ENTERPRISE ERP & MES", "SAP OData & MES REST Connect",
         "Certified SAP S/4HANA OData connector executes synchronous Goods Receipts (MIGO). Bi-directional webhooks feed shopfloor MES line scheduling."),
        ("DATA ASSET & AI COPILOT", "Cloud Data Lakehouse + SML",
         "Curates structured inbound delivery event telemetry into an enduring enterprise asset to train predictive supplier transit risk machine learning models.")
    ]

    col_w = 2.85
    gap = 0.31
    for idx, (l_title, l_tech, l_desc) in enumerate(layers):
        cx = 0.50 + idx * (col_w + gap)
        add_card(slide, cx, 1.5, col_w, 4.3, fill=HEX_WHITE, border=HEX_BORDER)
        add_badge(slide, cx + 0.15, 1.7, col_w - 0.3, 0.32, l_title, bg_hex=HEX_PRIMARY_DEEP, pt=10.0)
        add_tb(slide, cx + 0.15, 2.2, col_w - 0.3, 0.45, l_tech, font=FONT_TITLE, pt=12.5, color=HEX_PRIMARY, weight="bold", align="center")
        add_tb(slide, cx + 0.15, 2.8, col_w - 0.3, 2.8, l_desc, font=FONT_BODY, pt=11.5, color=HEX_TEXT_MAIN)

    add_card(slide, 0.50, 6.05, 12.33, 0.85, fill=HEX_SURFACE, border=HEX_BORDER_LIGHT)
    add_tb(slide, 0.70, 6.20, 11.93, 0.55,
           "Enterprise Security & Governance: Fully integrated with corporate Azure AD / Okta SSO, end-to-end TLS encryption, and ISA-95 standard data definitions.",
           font=FONT_BODY, pt=12.0, color=HEX_MUTED)


def build_slide_7(prs):
    """Slide 7: 12-Week Vertical Delivery Slice & J-Curve Buffer"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    for ph in list(slide.placeholders):
        sp = ph._element
        sp.getparent().remove(sp)

    add_header(
        slide,
        title="12-Week Vertical Delivery Slice with 90-Day Productivity J-Curve Buffer",
        subtitle="Vertical end-to-end use-case deployment with frontline co-design clinics and assisted dual-running."
    )

    phases = [
        ("PHASE 1: CO-DESIGN SLICE", "Weeks 1 – 4", HEX_PRIMARY,
         "Conduct frontline dock co-design clinics. Build end-to-end vertical slice: Supplier ASN -> Edge Scan -> SAP OData Goods Receipt with quarantine exception handling."),
        ("PHASE 2: PILOT & J-CURVE BUFFER", "Weeks 5 – 12", HEX_PRIMARY_DEEP,
         "Plant 1 pilot go-live. Incorporate a formal 90-day Productivity J-Curve buffer; temporary dual-running coordinators support dock teams during digital cutover."),
        ("PHASE 3: MES & MULTI-PLANT", "Weeks 13 – 24", HEX_ACCENT,
         "Integrate closed-loop MES finite line scheduling. Roll out edge gateways and rugged tablets to Plants 2, 3, and 4; establish cross-plant DBR buffer visibility."),
        ("PHASE 4: PREDICTIVE ML COPILOT", "Weeks 25 – 36", "0F766E",
         "Deploy AI Decision Copilot to central category managers. Expand supplier self-service portal to automated Vendor-Managed Inventory (VMI) replenishment.")
    ]

    col_w = 2.85
    gap = 0.31
    for idx, (p_title, p_time, p_color, p_desc) in enumerate(phases):
        cx = 0.50 + idx * (col_w + gap)
        add_card(slide, cx, 1.5, col_w, 4.3, fill=HEX_WHITE, border=HEX_BORDER)
        add_badge(slide, cx + 0.15, 1.7, col_w - 0.3, 0.32, p_title, bg_hex=p_color, pt=10.0)
        add_tb(slide, cx + 0.15, 2.2, col_w - 0.3, 0.4, p_time, font=FONT_TITLE, pt=13.5, color=p_color, weight="bold", align="center")
        add_tb(slide, cx + 0.15, 2.8, col_w - 0.3, 2.8, p_desc, font=FONT_BODY, pt=11.5, color=HEX_TEXT_MAIN)

    add_card(slide, 0.50, 6.05, 12.33, 0.85, fill=HEX_SURFACE, border=HEX_BORDER_LIGHT)
    add_tb(slide, 0.70, 6.20, 11.93, 0.55,
           "Realistic Adoption Model: Frontline co-design and dual-running buffers ensure the project successfully navigates the initial learning curve without operational disruption.",
           font=FONT_BODY, pt=12.0, color=HEX_MUTED)


def build_slide_8(prs):
    """Slide 8: Financial Investment & Decision Requested"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    for ph in list(slide.placeholders):
        sp = ph._element
        sp.getparent().remove(sp)

    add_header(
        slide,
        title="Rebalanced Investment Prioritizes Complementary Intangibles for 14-Month Payback",
        subtitle="43% of funds allocated to organizational capital; protects $1.8M annual constraint throughput."
    )

    # Left: Commercial Breakdown Table Card
    add_card(slide, 0.50, 1.5, 7.5, 4.3, fill=HEX_WHITE, border=HEX_BORDER)
    add_badge(slide, 0.70, 1.7, 3.8, 0.32, "BALANCED INVESTMENT ALLOCATION (43% INTANGIBLES)", bg_hex=HEX_PRIMARY_DEEP, pt=10.0)

    rows = [
        ("Edge & Cloud Software Engineering (Enterprise APIs)", "$140,000"),
        ("Ruggedized Mobile Scanners & Driver Lounge Kiosks", "$50,000"),
        ("SAP S/4HANA & MES Closed-Loop Integration", "$50,000"),
        ("Frontline Co-Design, Job Redesign & Digital Training", "$80,000"),
        ("Supplier Onboarding Data Hygiene Clinics", "$60,000"),
        ("Executive Transformation Steering & Change Leadership", "$40,000"),
        ("Total Capital & Intangible Investment (100%)", "$420,000")
    ]

    ry = 2.15
    for r_idx, (item, cost) in enumerate(rows):
        is_total = (r_idx == len(rows) - 1)
        bg_col = HEX_BLUE_BG if is_total else (HEX_WHITE if r_idx % 2 == 0 else HEX_SURFACE)
        row_card = add_card(slide, 0.70, ry, 7.1, 0.44, fill=bg_col, border=HEX_BORDER_LIGHT if not is_total else HEX_PRIMARY)
        txt_col = HEX_PRIMARY_DEEP if is_total else HEX_TEXT_MAIN
        wt = "bold" if is_total else "regular"
        add_tb(slide, 0.85, ry + 0.08, 5.0, 0.28, item, font=FONT_BODY, pt=11.0, color=txt_col, weight=wt)
        add_tb(slide, 6.0, ry + 0.08, 1.6, 0.28, cost, font=FONT_TITLE if is_total else FONT_BODY, pt=12.0 if is_total else 11.0, color=txt_col, weight="bold", align="right")
        ry += 0.48

    # Right: Value Realization & ROI Card
    add_card(slide, 8.30, 1.5, 4.53, 4.3, fill=HEX_BLUE_BG, border=HEX_PRIMARY, border_pt=1.5)
    add_badge(slide, 8.55, 1.7, 3.4, 0.32, "VALUE REALIZATION & BUSINESS IMPACT", bg_hex=HEX_PRIMARY, pt=10.0)

    roi_points = [
        ("14 Months Realistic Payback", "Explicitly models the 90-day Productivity J-Curve transition dip, avoiding premature executive panic."),
        ("$1.8M Annual Net Savings", "Subordinates inbound buffer tracking to plant constraint assembly lines, preventing line stockouts."),
        ("Zero Plant Network Risk", "Level 3 edge gateway eliminates factory downtime during cloud or WAN connection blips."),
        ("Restored Frontline Dignity", "Eliminates panic expediting and stressful dock disputes; honors truck driver hospitality.")
    ]

    py = 2.20
    for r_title, r_desc in roi_points:
        add_tb(slide, 8.55, py, 4.0, 0.30, r_title, font=FONT_TITLE, pt=13.0, color=HEX_PRIMARY_DEEP, weight="bold")
        add_tb(slide, 8.55, py + 0.32, 4.0, 0.55, r_desc, font=FONT_BODY, pt=11.0, color=HEX_TEXT_MAIN)
        py += 0.88

    # Bottom Decision Requested Strip
    add_card(slide, 0.50, 6.05, 12.33, 0.85, fill=HEX_WHITE, border=HEX_ACCENT, border_pt=1.5)
    add_tb(slide, 0.70, 6.18, 11.93, 0.55,
           "Executive Decision Requested: Approve $420,000 investment to execute 12-week Phase 1 at Plant 1, establishing the closed-loop edge-to-core inbound architecture.",
           font=FONT_TITLE, pt=12.5, color=HEX_PRIMARY_DEEP, weight="bold")


# =============================================================================
# MAIN BUILD & PREVIEW PIPELINE
# =============================================================================
def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_dir, "Supplier_Delivery_Tracker_CIO_Briefing.pptx")
    previews_dir = os.path.join(base_dir, "previews_smoke")
    os.makedirs(previews_dir, exist_ok=True)

    print(f"Building Refined Smoke-Test Deck: {output_path}")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    build_slide_1(prs)
    build_slide_2(prs)
    build_slide_3(prs)
    build_slide_4(prs)
    build_slide_5(prs)
    build_slide_6(prs)
    build_slide_7(prs)
    build_slide_8(prs)

    prs.save(output_path)
    print("Base presentation saved.")

    # Patch Theme & XML Order
    print("Applying Lumbini theme patcher...")
    apply_lumbini_theme_to_pptx(output_path)
    ensure_powerpoint_compatible_order(output_path)
    print("Theme and XML order patched successfully.")

    # Render Preview Images via PowerPoint COM
    print("Rendering 1080p slide preview images...")
    try:
        import win32com.client
        import pythoncom
        pythoncom.CoInitialize()
        ppt_app = win32com.client.Dispatch("PowerPoint.Application")
        abs_pptx = os.path.abspath(output_path)
        deck = ppt_app.Presentations.Open(abs_pptx, False, False, False)
        for i, slide in enumerate(deck.Slides):
            img_path = os.path.join(previews_dir, f"slide_{i+1}.png")
            slide.Export(img_path, "PNG", 1920, 1080)
            print(f"  Exported {img_path}")
        deck.Close()
        ppt_app.Quit()
        pythoncom.CoUninitialize()
        print("Slide previews generated successfully.")
    except Exception as e:
        print(f"Warning: PowerPoint COM export failed: {e}")

    print("Build complete.")


if __name__ == "__main__":
    main()
