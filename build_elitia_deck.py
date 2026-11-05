"""
Build the 8-slide customer-grade executive capability presentation for Elitia Technology Solutions.
All dimension math done with pure float inches, converting via Inches() only when passing to PowerPoint.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Core Color Palette
NAVY = RGBColor(0x0A, 0x25, 0x40)        # #0A2540 - Dark canvas & title text
ELITIA_BLUE = RGBColor(0x08, 0x58, 0x9C) # #08589C - Dominant Elitia accent
TEAL = RGBColor(0x1B, 0x7F, 0x79)        # #1B7F79 - Plant platform
SLATE = RGBColor(0x44, 0x54, 0x6A)       # #44546A - SAP & muted text
ORANGE = RGBColor(0xF2, 0x8C, 0x28)      # #F28C28 - Sharp loop & scale accent
BG_LIGHT = RGBColor(0xF8, 0xFA, 0xFC)    # #F8FAFC - Content canvas
SURFACE_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SURFACE_CARD = RGBColor(0xF1, 0xF5, 0xF9) # Light grey fill
BORDER_LIGHT = RGBColor(0xCB, 0xD5, 0xE1) # Light slate border
TEXT_MUTED = RGBColor(0x64, 0x74, 0x8B)   # Slate 500
TEXT_DARK = RGBColor(0x0F, 0x17, 0x2A)    # Deep slate for primary text
DOT_FILLED = "\u25CF"  # ●
DOT_HOLLOW = "\u25CB"  # ○

def create_deck(filename="Elitia_Technology_Solutions_Capability_Overview.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.50)
    blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]

    # Clean package core properties to guarantee no banned metadata
    core = prs.core_properties
    core.author = "Elitia Technology Solutions"
    core.last_modified_by = "Elitia Technology Solutions"
    core.title = "Elitia Technology Solutions Capability Overview"
    core.subject = "Industrial Intelligence and Enterprise Integration"
    core.comments = "Capability Overview for Industrial Digital Transformation"

    # Helper: add standard header and footer for content slides
    def add_chrome(slide, slide_num, title_text):
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.50))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_LIGHT
        bg.line.fill.background()
        bg.name = f"Background_Slide_{slide_num}"

        # Title Box (Calibri 32pt bold, Navy, left-aligned, max 55 chars)
        tb_title = slide.shapes.add_textbox(Inches(0.60), Inches(0.48), Inches(12.133), Inches(0.70))
        tb_title.name = f"Title_Slide_{slide_num}"
        tf = tb_title.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Calibri"
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = NAVY

        # Footer Left
        tb_fl = slide.shapes.add_textbox(Inches(0.60), Inches(7.05), Inches(6.0), Inches(0.30))
        tb_fl.name = f"Footer_Left_Slide_{slide_num}"
        tfl = tb_fl.text_frame
        tfl.margin_left = tfl.margin_right = tfl.margin_top = tfl.margin_bottom = 0
        pl = tfl.paragraphs[0]
        pl.text = "Elitia Technology Solutions"
        pl.font.name = "Calibri"
        pl.font.size = Pt(11)
        pl.font.color.rgb = TEXT_MUTED

        # Footer Right (Slide Number)
        tb_fr = slide.shapes.add_textbox(Inches(10.733), Inches(7.05), Inches(2.0), Inches(0.30))
        tb_fr.name = f"Footer_Right_Slide_{slide_num}"
        tfr = tb_fr.text_frame
        tfr.margin_left = tfr.margin_right = tfr.margin_top = tfr.margin_bottom = 0
        pr = tfr.paragraphs[0]
        pr.alignment = PP_ALIGN.RIGHT
        pr.text = f"{slide_num:02d} / 08"
        pr.font.name = "Calibri"
        pr.font.size = Pt(11)
        pr.font.color.rgb = TEXT_MUTED

        return bg

    # ==========================================
    # SLIDE 1: Title (Dark)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.50))
    bg1.name = "Background_Title_Slide"
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    # Four stacked bars motif echoing the 4-layer reference architecture
    bar_x = 0.80
    bar_y_start = 1.50
    bar_colors = [SLATE, ELITIA_BLUE, TEAL, BORDER_LIGHT]
    for i, col in enumerate(bar_colors):
        bar = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(bar_x), Inches(bar_y_start + i * 0.16), Inches(0.40), Inches(0.09))
        bar.name = f"Motif_Layer_Bar_{i+1}"
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()

    # Company Title
    tb_t = s1.shapes.add_textbox(Inches(0.80), Inches(2.40), Inches(11.50), Inches(1.00))
    tb_t.name = "Company_Title"
    tft = tb_t.text_frame
    tft.word_wrap = True
    tft.margin_left = tft.margin_top = tft.margin_right = tft.margin_bottom = 0
    pt = tft.paragraphs[0]
    pt.text = "Elitia Technology Solutions"
    pt.font.name = "Calibri"
    pt.font.size = Pt(46)
    pt.font.bold = True
    pt.font.color.rgb = SURFACE_WHITE

    # Subtitle
    tb_sub = s1.shapes.add_textbox(Inches(0.80), Inches(3.55), Inches(11.00), Inches(0.80))
    tb_sub.name = "Title_Subtitle"
    tfsub = tb_sub.text_frame
    tfsub.word_wrap = True
    tfsub.margin_left = tfsub.margin_top = tfsub.margin_right = tfsub.margin_bottom = 0
    psub = tfsub.paragraphs[0]
    psub.text = "Industrial intelligence for plants, grids and remote assets, connected to SAP and the shop floor"
    psub.font.name = "Calibri"
    psub.font.size = Pt(20)
    psub.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8) # Slate 400

    # Thin separator line
    sep = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), Inches(4.70), Inches(11.733), Inches(0.02))
    sep.name = "Title_Separator"
    sep.fill.solid()
    sep.fill.fore_color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    sep.line.fill.background()

    # Eight Target Industries Line
    tb_ind = s1.shapes.add_textbox(Inches(0.80), Inches(5.10), Inches(11.733), Inches(0.60))
    tb_ind.name = "Target_Industries_Line"
    tfind = tb_ind.text_frame
    tfind.word_wrap = True
    tfind.margin_left = tfind.margin_top = tfind.margin_right = tfind.margin_bottom = 0
    pind_lbl = tfind.paragraphs[0]
    pind_lbl.text = "TARGET INDUSTRIES"
    pind_lbl.font.name = "Calibri"
    pind_lbl.font.size = Pt(11)
    pind_lbl.font.bold = True
    pind_lbl.font.color.rgb = ORANGE
    pind_lbl.space_after = Pt(4)

    pind = tfind.add_paragraph()
    pind.text = "Manufacturing  ·  Energy  ·  Utilities  ·  Automotive  ·  Telecom  ·  Oil & Gas  ·  Mining  ·  Renewable Energy"
    pind.font.name = "Calibri"
    pind.font.size = Pt(15)
    pind.font.color.rgb = SURFACE_WHITE

    # Title slide footer
    tb_f1 = s1.shapes.add_textbox(Inches(0.80), Inches(6.80), Inches(11.733), Inches(0.30))
    tb_f1.name = "Title_Footer"
    tff1 = tb_f1.text_frame
    pf1 = tff1.paragraphs[0]
    pf1.text = "Enterprise Architecture & Capability Overview  ·  Pre-Read"
    pf1.font.name = "Calibri"
    pf1.font.size = Pt(11)
    pf1.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # ==========================================
    # SLIDE 2: Disconnect & Bridging Threads
    # "Plant data and enterprise decisions still don't meet"
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_chrome(s2, 2, "Plant data and enterprise decisions still don't meet")

    tb_s2_sub = s2.shapes.add_textbox(Inches(0.60), Inches(1.22), Inches(12.133), Inches(0.40))
    tb_s2_sub.name = "Slide_2_Thesis"
    tfs2 = tb_s2_sub.text_frame
    tfs2.margin_left = tfs2.margin_top = tfs2.margin_right = tfs2.margin_bottom = 0
    ps2 = tfs2.paragraphs[0]
    ps2.text = "Industrial plants generate millions of operational signals, yet enterprise decisions remain delayed in disconnected silos."
    ps2.font.name = "Calibri"
    ps2.font.size = Pt(15)
    ps2.font.color.rgb = SLATE

    col_left_x = 0.60
    col_left_w = 3.50

    col_center_x = 4.35
    col_center_w = 4.60

    col_right_x = 9.20
    col_right_w = 3.533

    def render_zone_hdr(slide, x, w, title, color, name):
        h_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(1.75), Inches(w), Inches(0.36))
        h_box.name = name
        h_box.fill.solid()
        h_box.fill.fore_color.rgb = color
        h_box.line.fill.background()
        tf = h_box.text_frame
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        p = tf.paragraphs[0]
        p.text = title
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = SURFACE_WHITE

    render_zone_hdr(s2, col_left_x, col_left_w, "PLANT DATA & SIGNALS", TEAL, "Header_Plant_Data")
    render_zone_hdr(s2, col_center_x, col_center_w, "ELITIA BRIDGING INTELLIGENCE", ELITIA_BLUE, "Header_Elitia_Bridge")
    render_zone_hdr(s2, col_right_x, col_right_w, "ENTERPRISE DECISIONS (SAP)", SLATE, "Header_SAP_Decisions")

    threads = [
        {
            "num": "01",
            "plant_title": "Asset & Machine Condition",
            "plant_sub": "Vibration, thermal telemetry, cycle counts and PLC run-hours at the machine.",
            "elitia_tag": "APM  ·  FOS",
            "elitia_role": "Predictive Health & Field Work Orders",
            "elitia_desc": "Calculates Remaining Useful Life (RUL) and dispatches digital SOP work orders to field crews.",
            "sap_title": "Maintenance Work Orders",
            "sap_sub": "Automated maintenance notifications and confirmed work orders in SAP PM.",
        },
        {
            "num": "02",
            "plant_title": "Production & Process Results",
            "plant_sub": "Shop-floor piece counts, quality scrap logs, heating curves and line cycle times.",
            "elitia_tag": "MES  ·  RSM  ·  CX",
            "elitia_role": "Execution Tracking & Customer Dispatch",
            "elitia_desc": "Correlates process heat maps, reconciles QA tolerances, and generates digital material certs.",
            "sap_title": "Orders & Dispatch",
            "sap_sub": "Production order confirmation, batch goods receipt, and dispatch in SAP SD & MM.",
        },
        {
            "num": "03",
            "plant_title": "Energy & Asset Usage",
            "plant_sub": "Smart meter telemetry, peak substation demand, fuel usage and grid feeder loads.",
            "elitia_tag": "EMS  ·  BI",
            "elitia_role": "Energy Optimization & Governance",
            "elitia_desc": "Aggregates multi-site utility consumption, baseline tariffs, and carbon emissions.",
            "sap_title": "Cost & Sustainability Reporting",
            "sap_sub": "Accurate ledger postings, utility variance allocations, and ESG disclosures in SAP FI.",
        }
    ]

    t_top_start = 2.25
    t_height = 1.38
    t_gap = 0.18

    for i, t in enumerate(threads):
        y = t_top_start + (i * (t_height + t_gap))

        row_bg = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.60), Inches(y), Inches(12.133), Inches(t_height))
        row_bg.name = f"Thread_Row_BG_{i+1}"
        row_bg.fill.solid()
        row_bg.fill.fore_color.rgb = SURFACE_WHITE
        row_bg.line.color.rgb = BORDER_LIGHT
        row_bg.line.width = Pt(1.0)

        # Left Box (Plant)
        b_pl = s2.shapes.add_textbox(Inches(col_left_x + 0.15), Inches(y + 0.12), Inches(col_left_w - 0.30), Inches(t_height - 0.24))
        b_pl.name = f"Plant_Box_{i+1}"
        tf_pl = b_pl.text_frame
        tf_pl.word_wrap = True
        tf_pl.margin_left = tf_pl.margin_right = tf_pl.margin_top = tf_pl.margin_bottom = 0
        p_pt = tf_pl.paragraphs[0]
        p_pt.text = t["plant_title"]
        p_pt.font.name = "Calibri"
        p_pt.font.size = Pt(14)
        p_pt.font.bold = True
        p_pt.font.color.rgb = TEAL

        p_ps = tf_pl.add_paragraph()
        p_ps.text = t["plant_sub"]
        p_ps.font.name = "Calibri"
        p_ps.font.size = Pt(12)
        p_ps.font.color.rgb = TEXT_DARK
        p_ps.space_before = Pt(4)

        # Connector arrow: Left -> Center
        arr1 = s2.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(col_left_x + col_left_w + 0.04), Inches(y + 0.55), Inches(0.17), Inches(0.22))
        arr1.name = f"Arrow_L_to_C_{i+1}"
        arr1.fill.solid()
        arr1.fill.fore_color.rgb = ELITIA_BLUE
        arr1.line.fill.background()

        # Center Box (Elitia Bridge)
        b_el = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(col_center_x), Inches(y + 0.08), Inches(col_center_w), Inches(t_height - 0.16))
        b_el.name = f"Elitia_Box_{i+1}"
        b_el.fill.solid()
        b_el.fill.fore_color.rgb = RGBColor(0xEA, 0xEE, 0xF4)
        b_el.line.color.rgb = ELITIA_BLUE
        b_el.line.width = Pt(1.25)
        tf_el = b_el.text_frame
        tf_el.word_wrap = True
        tf_el.margin_left = Inches(0.15)
        tf_el.margin_right = Inches(0.15)
        tf_el.margin_top = Inches(0.08)
        tf_el.margin_bottom = Inches(0.06)

        p_elt = tf_el.paragraphs[0]
        p_elt.text = f"{t['elitia_role']}   [{t['elitia_tag']}]"
        p_elt.font.name = "Calibri"
        p_elt.font.size = Pt(13)
        p_elt.font.bold = True
        p_elt.font.color.rgb = ELITIA_BLUE

        p_eld = tf_el.add_paragraph()
        p_eld.text = t["elitia_desc"]
        p_eld.font.name = "Calibri"
        p_eld.font.size = Pt(12)
        p_eld.font.color.rgb = TEXT_DARK
        p_eld.space_before = Pt(3)

        # Connector arrow: Center -> Right
        arr2 = s2.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(col_center_x + col_center_w + 0.04), Inches(y + 0.55), Inches(0.17), Inches(0.22))
        arr2.name = f"Arrow_C_to_R_{i+1}"
        arr2.fill.solid()
        arr2.fill.fore_color.rgb = SLATE
        arr2.line.fill.background()

        # Right Box (SAP)
        b_sap = s2.shapes.add_textbox(Inches(col_right_x + 0.15), Inches(y + 0.12), Inches(col_right_w - 0.30), Inches(t_height - 0.24))
        b_sap.name = f"SAP_Box_{i+1}"
        tf_sap = b_sap.text_frame
        tf_sap.word_wrap = True
        tf_sap.margin_left = tf_sap.margin_right = tf_sap.margin_top = tf_sap.margin_bottom = 0
        p_st = tf_sap.paragraphs[0]
        p_st.text = t["sap_title"]
        p_st.font.name = "Calibri"
        p_st.font.size = Pt(14)
        p_st.font.bold = True
        p_st.font.color.rgb = SLATE

        p_ss = tf_sap.add_paragraph()
        p_ss.text = t["sap_sub"]
        p_ss.font.name = "Calibri"
        p_ss.font.size = Pt(12)
        p_ss.font.color.rgb = TEXT_DARK
        p_ss.space_before = Pt(4)

    tb_c2 = s2.shapes.add_textbox(Inches(0.60), Inches(6.52), Inches(12.133), Inches(0.35))
    tb_c2.name = "Slide_2_Takeaway"
    tfc2 = tb_c2.text_frame
    tfc2.margin_left = tfc2.margin_top = tfc2.margin_right = tfc2.margin_bottom = 0
    pc2 = tfc2.paragraphs[0]
    pc2.text = "Key takeaway: Elitia synchronizes machine physics with financial and operational ledgers without manual intervention."
    pc2.font.name = "Calibri"
    pc2.font.size = Pt(13)
    pc2.font.bold = True
    pc2.font.color.rgb = NAVY

    # ==========================================
    # SLIDE 3: Reference Architecture
    # "Elitia sits between the plant platform and SAP"
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_chrome(s3, 3, "Elitia sits between the plant platform and SAP")

    leg_x = 8.30
    leg_y = 1.22
    leg_items = [
        ("SAP (Slate)", SLATE),
        ("Elitia (Blue)", ELITIA_BLUE),
        ("Your Platform (Teal)", TEAL)
    ]
    for idx, (lbl, col) in enumerate(leg_items):
        pill = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(leg_x + idx * 1.50), Inches(leg_y), Inches(1.40), Inches(0.24))
        pill.name = f"Legend_Pill_{idx+1}"
        pill.fill.solid()
        pill.fill.fore_color.rgb = col
        pill.line.fill.background()
        tf = pill.text_frame
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = lbl
        p.font.name = "Calibri"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = SURFACE_WHITE

    band_x = 0.60
    band_w = 12.133
    band_h = 0.92

    bands = [
        {
            "level": "L4 ENTERPRISE",
            "owner": "SAP & Elitia",
            "color": SLATE,
            "y": 1.58,
            "left_title": "SAP S/4HANA Core",
            "left_desc": "Modules: SD (Sales), MM (Materials), PM (Plant Maintenance), FI (Finance & Costing)",
            "left_owner": "SAP S/4HANA",
            "left_color": SLATE,
            "right_title": "Enterprise Intelligence & Data Governance",
            "right_desc": "Elitia BI (Executive Analytics)  ·  Elitia DGS (Industrial Data Governance)  ·  Elitia CX (B2B Portal)",
            "right_owner": "Elitia",
            "right_color": ELITIA_BLUE,
            "connector_below": "Work orders, orders and postings via SAP APIs"
        },
        {
            "level": "L3 OPERATIONS INTELLIGENCE",
            "owner": "Elitia",
            "color": ELITIA_BLUE,
            "y": 2.80,
            "left_title": "Predictive Operations & Asset Reliability",
            "left_desc": "Elitia APM (Machine Diagnostics & RUL)  ·  Elitia RSM (Mill Quality)  ·  Elitia FOS (Field SOPs)",
            "left_owner": "Elitia",
            "left_color": ELITIA_BLUE,
            "right_title": "Safety Intelligence & Energy Optimization",
            "right_desc": "Elitia WSM (Geofencing)  ·  Elitia Vision AI (PPE Compliance)  ·  Elitia EMS (Energy Management)",
            "right_owner": "Elitia",
            "right_color": ELITIA_BLUE,
            "connector_below": "Platform data access"
        },
        {
            "level": "L2 DATA & OPERATIONS PLATFORM",
            "owner": "Your Platform",
            "color": TEAL,
            "y": 4.02,
            "left_title": "\"Your Platform\" (Existing Infrastructure)",
            "left_desc": "Site SCADA, Process Historian, Plant MES, IoT Data Services, and Time-Series Repositories",
            "left_owner": "Your Platform",
            "left_color": TEAL,
            "right_title": "Alternative Native Options (Where None Exists)",
            "right_desc": "Elitia MES (Lightweight Shop-Floor Execution)  ·  Elitia Grid-X (Substation SCADA)",
            "right_owner": "Elitia Optional",
            "right_color": ELITIA_BLUE,
            "connector_below": "OPC-UA  ·  MQTT"
        },
        {
            "level": "L0-1 FIELD & EDGE",
            "owner": "Shop Floor & Grid",
            "color": SLATE,
            "y": 5.24,
            "left_title": "Industrial Control & Physical Assets",
            "left_desc": "PLCs, DCS Controllers, Field Sensors, Vibration Transmitters, Optical Gauges, and CNC Tooling",
            "left_owner": "Plant / Grid",
            "left_color": SLATE,
            "right_title": "Distributed Generation & Edge Gateways",
            "right_desc": "Smart Energy Meters, Solar Inverters, Wind Converters, Battery BMS, and Industrial IoT Gateways",
            "right_owner": "Remote Assets",
            "right_color": SLATE,
            "connector_below": None
        }
    ]

    for b in bands:
        box = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(band_x), Inches(b["y"]), Inches(band_w), Inches(band_h))
        box.name = f"Band_{b['level'].replace(' ', '_')}"
        box.fill.solid()
        box.fill.fore_color.rgb = SURFACE_WHITE
        box.line.color.rgb = b["color"]
        box.line.width = Pt(1.5)

        tab = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(band_x), Inches(b["y"]), Inches(2.20), Inches(band_h))
        tab.name = f"Tab_{b['level'].replace(' ', '_')}"
        tab.fill.solid()
        tab.fill.fore_color.rgb = b["color"]
        tab.line.fill.background()
        tf_t = tab.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = Inches(0.10)
        tf_t.margin_top = Inches(0.20)
        p1 = tf_t.paragraphs[0]
        p1.text = b["level"]
        p1.font.name = "Calibri"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = SURFACE_WHITE

        p2 = tf_t.add_paragraph()
        p2.text = f"Owner: {b['owner']}"
        p2.font.name = "Calibri"
        p2.font.size = Pt(10)
        p2.font.color.rgb = RGBColor(0xE2, 0xE8, 0xF0)

        cz1 = s3.shapes.add_textbox(Inches(band_x + 2.35), Inches(b["y"] + 0.10), Inches(4.70), Inches(band_h - 0.20))
        cz1.name = f"Content_Left_{b['level'].replace(' ', '_')}"
        tf_c1 = cz1.text_frame
        tf_c1.word_wrap = True
        tf_c1.margin_left = tf_c1.margin_right = tf_c1.margin_top = tf_c1.margin_bottom = 0
        pc1_t = tf_c1.paragraphs[0]
        pc1_t.text = b["left_title"]
        pc1_t.font.name = "Calibri"
        pc1_t.font.size = Pt(13)
        pc1_t.font.bold = True
        pc1_t.font.color.rgb = b["left_color"]

        pc1_d = tf_c1.add_paragraph()
        pc1_d.text = b["left_desc"]
        pc1_d.font.name = "Calibri"
        pc1_d.font.size = Pt(11)
        pc1_d.font.color.rgb = TEXT_DARK
        pc1_d.space_before = Pt(3)

        vdiv = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(band_x + 7.15), Inches(b["y"] + 0.12), Inches(0.02), Inches(band_h - 0.24))
        vdiv.name = f"Divider_{b['level'].replace(' ', '_')}"
        vdiv.fill.solid()
        vdiv.fill.fore_color.rgb = BORDER_LIGHT
        vdiv.line.fill.background()

        cz2 = s3.shapes.add_textbox(Inches(band_x + 7.30), Inches(b["y"] + 0.10), Inches(4.70), Inches(band_h - 0.20))
        cz2.name = f"Content_Right_{b['level'].replace(' ', '_')}"
        tf_c2 = cz2.text_frame
        tf_c2.word_wrap = True
        tf_c2.margin_left = tf_c2.margin_right = tf_c2.margin_top = tf_c2.margin_bottom = 0
        pc2_t = tf_c2.paragraphs[0]
        pc2_t.text = b["right_title"]
        pc2_t.font.name = "Calibri"
        pc2_t.font.size = Pt(13)
        pc2_t.font.bold = True
        pc2_t.font.color.rgb = b["right_color"]

        pc2_d = tf_c2.add_paragraph()
        pc2_d.text = b["right_desc"]
        pc2_d.font.name = "Calibri"
        pc2_d.font.size = Pt(11)
        pc2_d.font.color.rgb = TEXT_DARK
        pc2_d.space_before = Pt(3)

        if b["connector_below"]:
            conn_y = b["y"] + band_h + 0.04
            conn_pill = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.20), Inches(conn_y), Inches(4.933), Inches(0.22))
            conn_pill.name = f"Connector_{b['level'].replace(' ', '_')}"
            conn_pill.fill.solid()
            conn_pill.fill.fore_color.rgb = SURFACE_CARD
            conn_pill.line.color.rgb = BORDER_LIGHT
            conn_pill.line.width = Pt(0.75)
            tf_cn = conn_pill.text_frame
            tf_cn.margin_top = tf_cn.margin_bottom = tf_cn.margin_left = tf_cn.margin_right = 0
            p_cn = tf_cn.paragraphs[0]
            p_cn.alignment = PP_ALIGN.CENTER
            p_cn.text = f"↕  {b['connector_below']}  ↕"
            p_cn.font.name = "Calibri"
            p_cn.font.size = Pt(10)
            p_cn.font.bold = True
            p_cn.font.color.rgb = SLATE

    tb_fn = s3.shapes.add_textbox(Inches(0.60), Inches(6.32), Inches(12.133), Inches(0.40))
    tb_fn.name = "Slide_3_Footnote"
    tffn = tb_fn.text_frame
    tffn.margin_left = tffn.margin_top = tffn.margin_right = tffn.margin_bottom = 0
    pfn = tffn.paragraphs[0]
    pfn.text = "* Footnote: Elitia works with the plant platform you already run; Elitia MES and Grid-X SCADA are available where none exists."
    pfn.font.name = "Calibri"
    pfn.font.size = Pt(12)
    pfn.font.italic = True
    pfn.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 4: Portfolio (Five Chevron Columns)
    # "One portfolio, built from the same few building blocks"
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_chrome(s4, 4, "One portfolio, built from the same few building blocks")

    col_w = 2.32
    col_gap = 0.13
    start_x = 0.60
    top_y = 1.35
    header_h = 0.45
    body_h = 4.75

    categories = [
        {
            "name": "OPERATIONS",
            "color": ELITIA_BLUE,
            "items": [
                ("Elitia MES", "Traditional production control, work order tracking & traceability"),
                ("Elitia RSM", "Rail & mill intelligence, predictive heating & QA parameter correlation"),
                ("Elitia APM", "Machine diagnostics, Remaining Useful Life (RUL) & automated SAP PM integration")
            ]
        },
        {
            "name": "SAFETY",
            "color": TEAL,
            "items": [
                ("Elitia FOS", "Voice-assist field execution, digital audit logs & dynamic SOP builder"),
                ("Elitia WSM", "Workforce spatial tracking, geofence breach alerting & emergency muster"),
                ("Elitia Vision AI", "Real-time PPE compliance monitoring, violation snapshots & safety heatmaps")
            ]
        },
        {
            "name": "ENERGY",
            "color": SLATE,
            "items": [
                ("Elitia EMS", "Real-time energy monitoring, multi-site analytics & sustainability reporting"),
                ("Elitia Grid-X", "Grid visibility for substations, feeders & distributed utility infrastructure"),
                ("Elitia Meter-X", "Smart metering, remote tariff logging & consumption analytics")
            ]
        },
        {
            "name": "REMOTE ASSETS",
            "color": ELITIA_BLUE,
            "items": [
                ("Solar-X & Wind-X", "Performance analytics for solar inverters & turbine diagnostics"),
                ("Tower-X & Battery", "Remote monitoring for telecom towers & Battery SoC/SoH tracking"),
                ("PIDS & LDS", "Pipeline Intrusion Detection & Leak Detection sensor integrity systems")
            ]
        },
        {
            "name": "INSIGHT",
            "color": NAVY,
            "items": [
                ("Elitia BI", "AI-based data analytics, executive dashboards & cross-plant KPI insights"),
                ("Elitia DGS", "Industrial data governance framework, master data consistency & lineage"),
                ("Elitia CX", "B2B customer portal, order tracking, digital MTCs & logistics status")
            ]
        }
    ]

    for c_idx, cat in enumerate(categories):
        x = start_x + (c_idx * (col_w + col_gap))

        chv = s4.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(x), Inches(top_y), Inches(col_w), Inches(header_h))
        chv.name = f"Chevron_{cat['name']}"
        chv.fill.solid()
        chv.fill.fore_color.rgb = cat["color"]
        chv.line.fill.background()
        tf_h = chv.text_frame
        tf_h.margin_left = tf_h.margin_right = tf_h.margin_top = tf_h.margin_bottom = 0
        p_h = tf_h.paragraphs[0]
        p_h.text = cat["name"]
        p_h.alignment = PP_ALIGN.CENTER
        p_h.font.name = "Calibri"
        p_h.font.size = Pt(13)
        p_h.font.bold = True
        p_h.font.color.rgb = SURFACE_WHITE

        c_body = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(top_y + header_h + 0.08), Inches(col_w), Inches(body_h))
        c_body.name = f"Body_{cat['name']}"
        c_body.fill.solid()
        c_body.fill.fore_color.rgb = SURFACE_WHITE
        c_body.line.color.rgb = BORDER_LIGHT
        c_body.line.width = Pt(1.0)

        item_h = 1.45
        item_gap = 0.10
        for i_idx, (m_name, m_desc) in enumerate(cat["items"]):
            iy = top_y + header_h + 0.16 + (i_idx * (item_h + item_gap))

            ibox = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.08), Inches(iy), Inches(col_w - 0.16), Inches(item_h))
            ibox.name = f"Tile_{cat['name']}_{i_idx+1}"
            ibox.fill.solid()
            ibox.fill.fore_color.rgb = SURFACE_CARD
            ibox.line.color.rgb = cat["color"] if i_idx == 0 else BORDER_LIGHT
            ibox.line.width = Pt(1.0 if i_idx == 0 else 0.75)

            tf_i = ibox.text_frame
            tf_i.word_wrap = True
            tf_i.margin_left = Inches(0.10)
            tf_i.margin_right = Inches(0.10)
            tf_i.margin_top = Inches(0.10)
            tf_i.margin_bottom = Inches(0.08)

            p_in = tf_i.paragraphs[0]
            p_in.text = m_name
            p_in.font.name = "Calibri"
            p_in.font.size = Pt(13)
            p_in.font.bold = True
            p_in.font.color.rgb = cat["color"]

            p_id = tf_i.add_paragraph()
            p_id.text = m_desc
            p_id.font.name = "Calibri"
            p_id.font.size = Pt(11)
            p_id.font.color.rgb = TEXT_DARK
            p_id.space_before = Pt(4)

    tb_fn4 = s4.shapes.add_textbox(Inches(0.60), Inches(6.70), Inches(12.133), Inches(0.28))
    tb_fn4.name = "Slide_4_Footnote"
    tffn4 = tb_fn4.text_frame
    tffn4.margin_left = tffn4.margin_top = tffn4.margin_right = tffn4.margin_bottom = 0
    pfn4 = tffn4.paragraphs[0]
    pfn4.text = "* Footnote: 19 modules in the full portfolio. The core of the offer is shown."
    pfn4.font.name = "Calibri"
    pfn4.font.size = Pt(12)
    pfn4.font.italic = True
    pfn4.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 5: Industry Capability Matrix
    # "One capability set, eight industries"
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_chrome(s5, 5, "One capability set, eight industries")

    tb_leg5 = s5.shapes.add_textbox(Inches(7.50), Inches(1.15), Inches(5.233), Inches(0.35))
    tb_leg5.name = "Legend_Slide_5"
    tf_leg5 = tb_leg5.text_frame
    tf_leg5.margin_top = tf_leg5.margin_bottom = tf_leg5.margin_left = tf_leg5.margin_right = 0
    p_l5 = tf_leg5.paragraphs[0]
    p_l5.alignment = PP_ALIGN.RIGHT
    p_l5.text = f"{DOT_FILLED} Core Fit   |   {DOT_HOLLOW} Supporting Fit   |   Ratings reflect architect solution fit"
    p_l5.font.name = "Calibri"
    p_l5.font.size = Pt(11)
    p_l5.font.bold = True
    p_l5.font.color.rgb = SLATE

    tbl_shape = s5.shapes.add_table(9, 7, Inches(0.60), Inches(1.55), Inches(12.133), Inches(4.85))
    tbl_shape.name = "Industry_Matrix_Table"
    tbl = tbl_shape.table

    tbl.columns[0].width = Inches(2.20)
    tbl.columns[1].width = Inches(1.30)
    tbl.columns[2].width = Inches(1.30)
    tbl.columns[3].width = Inches(1.30)
    tbl.columns[4].width = Inches(1.30)
    tbl.columns[5].width = Inches(1.30)
    tbl.columns[6].width = Inches(3.433)

    headers = ["INDUSTRY", "OPERATIONS", "SAFETY", "ENERGY", "REMOTE ASSETS", "INSIGHT", "WHERE TO START"]
    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.alignment = PP_ALIGN.CENTER if 1 <= j <= 5 else PP_ALIGN.LEFT
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = SURFACE_WHITE

    matrix_data = [
        ("Manufacturing", DOT_FILLED, DOT_FILLED, DOT_HOLLOW, DOT_HOLLOW, DOT_FILLED, "Start with APM machine reliability & automated SAP PM work orders"),
        ("Energy", DOT_HOLLOW, DOT_FILLED, DOT_FILLED, DOT_FILLED, DOT_FILLED, "Substation telemetry & Grid-X real-time visibility"),
        ("Utilities", DOT_HOLLOW, DOT_FILLED, DOT_FILLED, DOT_HOLLOW, DOT_FILLED, "Meter-X distributed smart metering & customer billing sync"),
        ("Automotive", DOT_FILLED, DOT_FILLED, DOT_HOLLOW, DOT_HOLLOW, DOT_FILLED, "MES assembly line execution & Vision AI quality/safety"),
        ("Telecom", DOT_HOLLOW, DOT_FILLED, DOT_HOLLOW, DOT_FILLED, DOT_FILLED, "Tower-X remote power tracking & battery bank health"),
        ("Oil & Gas", DOT_HOLLOW, DOT_FILLED, DOT_HOLLOW, DOT_FILLED, DOT_FILLED, "Pipeline PIDS intrusion & LDS leak integrity monitoring"),
        ("Mining", DOT_FILLED, DOT_FILLED, DOT_HOLLOW, DOT_FILLED, DOT_FILLED, "Workforce WSM geofencing, muster alerts & haul fleet APM"),
        ("Renewable Energy", DOT_HOLLOW, DOT_HOLLOW, DOT_FILLED, DOT_FILLED, DOT_FILLED, "Solar-X & Wind-X inverter telemetry & battery SoC tracking")
    ]

    for i, row in enumerate(matrix_data):
        row_idx = i + 1
        bg_color = SURFACE_WHITE if (i % 2 == 0) else SURFACE_CARD
        for j, val in enumerate(row):
            cell = tbl.cell(row_idx, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_color
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Calibri"

            if j == 0:
                p.alignment = PP_ALIGN.LEFT
                p.font.size = Pt(13)
                p.font.bold = True
                p.font.color.rgb = NAVY
            elif 1 <= j <= 5:
                p.alignment = PP_ALIGN.CENTER
                p.font.size = Pt(16)
                p.font.bold = True
                p.font.color.rgb = ELITIA_BLUE if val == DOT_FILLED else SLATE
            else:
                p.alignment = PP_ALIGN.LEFT
                p.font.size = Pt(12)
                p.font.color.rgb = TEXT_DARK

    tb_c5 = s5.shapes.add_textbox(Inches(0.60), Inches(6.55), Inches(12.133), Inches(0.30))
    tb_c5.name = "Slide_5_Footnote"
    tfc5 = tb_c5.text_frame
    tfc5.margin_left = tfc5.margin_top = tfc5.margin_right = tfc5.margin_bottom = 0
    pc5 = tfc5.paragraphs[0]
    pc5.text = "* Solution note: Industry capability ratings and recommended starting points represent architect assessment based on cross-industry deployments."
    pc5.font.name = "Calibri"
    pc5.font.size = Pt(11)
    pc5.font.italic = True
    pc5.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 6: Five-Step Flow with Return Loop
    # "From machine signal to closed work order, no re-keying"
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_chrome(s6, 6, "From machine signal to closed work order, no re-keying")

    steps = [
        {
            "num": "1",
            "name": "Sense",
            "owner": "Your Platform",
            "owner_color": TEAL,
            "system_pill": "SCADA  ·  Historian  ·  PLC",
            "action": "Ingests continuous sensor telemetry, temperature, vibration, and machine cycle metrics."
        },
        {
            "num": "2",
            "name": "Predict",
            "owner": "Elitia APM",
            "owner_color": ELITIA_BLUE,
            "system_pill": "Machine Diagnostics & RUL",
            "action": "Detects early degradation patterns, forecasts Remaining Useful Life, and triggers maintenance rules."
        },
        {
            "num": "3",
            "name": "Plan",
            "owner": "SAP PM",
            "owner_color": SLATE,
            "system_pill": "Plant Maintenance API",
            "action": "Generates maintenance notification, schedules skilled crew, reserves spare parts, and creates work order."
        },
        {
            "num": "4",
            "name": "Execute",
            "owner": "Elitia FOS",
            "owner_color": ELITIA_BLUE,
            "system_pill": "Digital Field SOPs",
            "action": "Guides field technician with voice assist, step-by-step checklists, digital sign-off, and photo proof."
        },
        {
            "num": "5",
            "name": "Learn",
            "owner": "Elitia BI · APM",
            "owner_color": ELITIA_BLUE,
            "system_pill": "Closed-Loop Analytics",
            "action": "Posts completion to SAP, correlates repair duration, updates failure curves, and refines predictive models."
        }
    ]

    card_w = 2.20
    card_gap = 0.28
    flow_x = 0.60
    flow_y = 1.50
    card_h = 3.60

    for idx, st in enumerate(steps):
        cx = flow_x + (idx * (card_w + card_gap))

        cbox = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cx), Inches(flow_y), Inches(card_w), Inches(card_h))
        cbox.name = f"Step_Card_{st['num']}"
        cbox.fill.solid()
        cbox.fill.fore_color.rgb = SURFACE_WHITE
        cbox.line.color.rgb = st["owner_color"]
        cbox.line.width = Pt(1.5)

        cir = s6.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx + 0.80), Inches(flow_y + 0.18), Inches(0.60), Inches(0.60))
        cir.name = f"Step_Circle_{st['num']}"
        cir.fill.solid()
        cir.fill.fore_color.rgb = st["owner_color"]
        cir.line.fill.background()
        tf_cir = cir.text_frame
        tf_cir.margin_top = tf_cir.margin_bottom = tf_cir.margin_left = tf_cir.margin_right = 0
        p_c = tf_cir.paragraphs[0]
        p_c.alignment = PP_ALIGN.CENTER
        p_c.text = st["num"]
        p_c.font.name = "Calibri"
        p_c.font.size = Pt(18)
        p_c.font.bold = True
        p_c.font.color.rgb = SURFACE_WHITE

        tb_sn = s6.shapes.add_textbox(Inches(cx + 0.10), Inches(flow_y + 0.85), Inches(card_w - 0.20), Inches(0.40))
        tb_sn.name = f"Step_Name_{st['num']}"
        tf_sn = tb_sn.text_frame
        tf_sn.margin_top = tf_sn.margin_bottom = tf_sn.margin_left = tf_sn.margin_right = 0
        psn = tf_sn.paragraphs[0]
        psn.alignment = PP_ALIGN.CENTER
        psn.text = st["name"]
        psn.font.name = "Calibri"
        psn.font.size = Pt(16)
        psn.font.bold = True
        psn.font.color.rgb = NAVY

        opill = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cx + 0.20), Inches(flow_y + 1.30), Inches(card_w - 0.40), Inches(0.32))
        opill.name = f"Owner_Pill_{st['num']}"
        opill.fill.solid()
        opill.fill.fore_color.rgb = st["owner_color"]
        opill.line.fill.background()
        tf_op = opill.text_frame
        tf_op.margin_top = tf_op.margin_bottom = tf_op.margin_left = tf_op.margin_right = 0
        pop = tf_op.paragraphs[0]
        pop.alignment = PP_ALIGN.CENTER
        pop.text = st["owner"]
        pop.font.name = "Calibri"
        pop.font.size = Pt(11)
        pop.font.bold = True
        pop.font.color.rgb = SURFACE_WHITE

        tb_sys = s6.shapes.add_textbox(Inches(cx + 0.10), Inches(flow_y + 1.70), Inches(card_w - 0.20), Inches(0.35))
        tb_sys.name = f"System_Subtitle_{st['num']}"
        tf_sys = tb_sys.text_frame
        tf_sys.word_wrap = True
        tf_sys.margin_top = tf_sys.margin_bottom = tf_sys.margin_left = tf_sys.margin_right = 0
        psys = tf_sys.paragraphs[0]
        psys.alignment = PP_ALIGN.CENTER
        psys.text = st["system_pill"]
        psys.font.name = "Calibri"
        psys.font.size = Pt(10)
        psys.font.bold = True
        psys.font.color.rgb = TEXT_MUTED

        sdiv = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx + 0.20), Inches(flow_y + 2.10), Inches(card_w - 0.40), Inches(0.015))
        sdiv.name = f"Step_Divider_{st['num']}"
        sdiv.fill.solid()
        sdiv.fill.fore_color.rgb = BORDER_LIGHT
        sdiv.line.fill.background()

        tb_act = s6.shapes.add_textbox(Inches(cx + 0.12), Inches(flow_y + 2.20), Inches(card_w - 0.24), Inches(1.25))
        tb_act.name = f"Step_Action_{st['num']}"
        tf_act = tb_act.text_frame
        tf_act.word_wrap = True
        tf_act.margin_top = tf_act.margin_bottom = tf_act.margin_left = tf_act.margin_right = 0
        pact = tf_act.paragraphs[0]
        pact.text = st["action"]
        pact.font.name = "Calibri"
        pact.font.size = Pt(11.5)
        pact.font.color.rgb = TEXT_DARK

        if idx < 4:
            arr_x = cx + card_w + 0.04
            arr = s6.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(arr_x), Inches(flow_y + 1.65), Inches(0.20), Inches(0.26))
            arr.name = f"Forward_Arrow_{idx+1}_to_{idx+2}"
            arr.fill.solid()
            arr.fill.fore_color.rgb = ELITIA_BLUE
            arr.line.fill.background()

    # Orange Return Loop Arrow (Step 5 -> Step 2)
    x_step2_mid = flow_x + (1 * (card_w + card_gap)) + (card_w / 2.0)
    x_step5_mid = flow_x + (4 * (card_w + card_gap)) + (card_w / 2.0)
    ret_y = flow_y + card_h + 0.18

    loop_band = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x_step2_mid - 0.20), Inches(ret_y), Inches((x_step5_mid - x_step2_mid) + 0.40), Inches(0.46))
    loop_band.name = "Return_Loop_Banner"
    loop_band.fill.solid()
    loop_band.fill.fore_color.rgb = RGBColor(0xFE, 0xED, 0xD5)
    loop_band.line.color.rgb = ORANGE
    loop_band.line.width = Pt(1.5)
    tf_lb = loop_band.text_frame
    tf_lb.margin_top = tf_lb.margin_bottom = tf_lb.margin_left = tf_lb.margin_right = 0
    plb = tf_lb.paragraphs[0]
    plb.alignment = PP_ALIGN.CENTER
    plb.text = "↺  CONTINUOUS LEARNING LOOP: Field repair evidence & run-hours update Step 2 predictive failure models  ↺"
    plb.font.name = "Calibri"
    plb.font.size = Pt(11)
    plb.font.bold = True
    plb.font.color.rgb = RGBColor(0xC2, 0x41, 0x0C)

    tb_t6 = s6.shapes.add_textbox(Inches(0.60), Inches(6.05), Inches(12.133), Inches(0.45))
    tb_t6.name = "Slide_6_Takeaway"
    tf_t6 = tb_t6.text_frame
    tf_t6.word_wrap = True
    tf_t6.margin_top = tf_t6.margin_bottom = tf_t6.margin_left = tf_t6.margin_right = 0
    pt6 = tf_t6.paragraphs[0]
    pt6.text = "Key Takeaway: \"Nothing is re-keyed between the plant, Elitia and SAP.\""
    pt6.font.name = "Calibri"
    pt6.font.size = Pt(16)
    pt6.font.bold = True
    pt6.font.color.rgb = NAVY

    pt6_sub = tf_t6.add_paragraph()
    pt6_sub.text = "From raw sensor anomaly to closed maintenance ledger, data traverses pre-built SAP APIs and Elitia intelligence automatically."
    pt6_sub.font.name = "Calibri"
    pt6_sub.font.size = Pt(12)
    pt6_sub.font.color.rgb = SLATE
    pt6_sub.space_before = Pt(2)

    # ==========================================
    # SLIDE 7: Deployed Environments & Reference Table
    # "Deployed across plants, grids and remote sites"
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_chrome(s7, 7, "Deployed across plants, grids and remote sites")

    t7_shape = s7.shapes.add_table(6, 3, Inches(0.60), Inches(1.45), Inches(12.133), Inches(4.75))
    t7_shape.name = "Customer_Reference_Table"
    t7 = t7_shape.table

    t7.columns[0].width = Inches(3.20)
    t7.columns[1].width = Inches(5.933)
    t7.columns[2].width = Inches(3.00)

    t7_headers = ["ENVIRONMENT", "WHAT WAS DELIVERED", "CONFIRMED CUSTOMER REFERENCE"]
    for j, h in enumerate(t7_headers):
        cell = t7.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.alignment = PP_ALIGN.LEFT
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = SURFACE_WHITE

    references_data = [
        (
            "Energy & Utilities Distribution\nPower grid substations and transmission networks",
            "Full SAP ERP rollout across utility distribution, revenue cycles, and billing channels. Standardized operational asset schemas across millions of smart metering points.",
            "JBVNL & TVNL"
        ),
        (
            "Distributed Renewables & Storage\nWind and solar generation plants & BESS assets",
            "Deployed Remote Monitoring Systems (RMS) for power conversion devices. Secure SCADA setups deployed for distributed wind and solar generation plants.",
            "Lineage Power & Windcare"
        ),
        (
            "Industrial Manufacturing\nHigh-volume shop-floor discrete assembly lines",
            "Engineered custom Manufacturing Execution (MES) modules for shop-floor assembly lines. Implemented Energy Management Systems (EMS) to balance plant power loads.",
            "Midwest Energy & HSA"
        ),
        (
            "Energy Infrastructure & Telemetry\nCross-border pipeline and industrial asset telemetry",
            "Developed cross-border industrial telemetry platforms for distributed energy assets. Delivered digital twin dashboards showing real-time utility parameters.",
            "Qatar Energy & Acelion Energy"
        ),
        (
            "Regulated Manufacturing & Supply Chain\nMedical device manufacturing and enterprise ERP",
            "Deployed Elitia DGS (Data Governance Suite) to centralize customer, vendor, and material master data catalogs with workflow validation before SAP S/4HANA execution.",
            "Healthium Medtech"
        )
    ]

    for i, (env, deliv, cust) in enumerate(references_data):
        row_idx = i + 1
        bg_col = SURFACE_WHITE if (i % 2 == 0) else SURFACE_CARD

        c0 = t7.cell(row_idx, 0)
        c0.fill.solid()
        c0.fill.fore_color.rgb = bg_col
        c0.vertical_anchor = MSO_ANCHOR.MIDDLE
        p0 = c0.text_frame.paragraphs[0]
        p0.text = env
        p0.font.name = "Calibri"
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = NAVY

        c1 = t7.cell(row_idx, 1)
        c1.fill.solid()
        c1.fill.fore_color.rgb = bg_col
        c1.vertical_anchor = MSO_ANCHOR.MIDDLE
        p1 = c1.text_frame.paragraphs[0]
        p1.text = deliv
        p1.font.name = "Calibri"
        p1.font.size = Pt(11.5)
        p1.font.color.rgb = TEXT_DARK

        c2 = t7.cell(row_idx, 2)
        c2.fill.solid()
        c2.fill.fore_color.rgb = bg_col
        c2.vertical_anchor = MSO_ANCHOR.MIDDLE
        p2 = c2.text_frame.paragraphs[0]
        p2.text = cust
        p2.font.name = "Calibri"
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = ELITIA_BLUE

    tb_fn7 = s7.shapes.add_textbox(Inches(0.60), Inches(6.35), Inches(12.133), Inches(0.40))
    tb_fn7.name = "Slide_7_Footnote"
    tffn7 = tb_fn7.text_frame
    tffn7.margin_left = tffn7.margin_top = tffn7.margin_right = tffn7.margin_bottom = 0
    pfn7 = tffn7.paragraphs[0]
    pfn7.text = "* Customer note: References shown were delivered using Elitia-type product suites and architectures. Confirm permission prior to external distribution."
    pfn7.font.name = "Calibri"
    pfn7.font.size = Pt(11)
    pfn7.font.italic = True
    pfn7.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 8: Phased Scaling & Commercial Engagement
    # "Start with one use case, then scale across sites"
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_chrome(s8, 8, "Start with one use case, then scale across sites")

    phases = [
        {
            "num": "PHASE 01",
            "name": "Pilot",
            "accent": ELITIA_BLUE,
            "theme": "Single Unit / Line Proof of Value",
            "action_1_title": "Isolate high-impact asset or bottleneck line",
            "action_1_desc": "Deploy targeted module (e.g., APM on critical motor, or Vision AI on safety cell) on existing platform data.",
            "action_2_title": "Validate predictive anomaly detection & ROI",
            "action_2_desc": "Confirm baseline failure detection accuracy, operator adoption, and quantified uptime gain with plant engineers."
        },
        {
            "num": "PHASE 02",
            "name": "Integrate",
            "accent": SLATE,
            "theme": "Enterprise Core & Closed-Loop Workflows",
            "action_1_title": "Bind automated bi-directional SAP APIs",
            "action_1_desc": "Connect predictive alerts directly to SAP PM notifications, material reservations, and finance cost ledgers.",
            "action_2_title": "Standardize master data governance via DGS",
            "action_2_desc": "Enforce unified asset catalogs, BOM schemas, and maintenance hierarchy rules across operational domains."
        },
        {
            "num": "PHASE 03",
            "name": "Scale",
            "accent": ORANGE,
            "theme": "Multi-Site Industrial Rollout",
            "action_1_title": "Replicate modular stack across all facilities",
            "action_1_desc": "Roll out unified Operations Intelligence templates across regional plants, distributed grids, and field sites.",
            "action_2_title": "Establish cross-plant executive visibility",
            "action_2_desc": "Deploy Elitia BI cross-plant cockpits to track global OEE, fleet reliability, energy benchmarks, and carbon metrics."
        }
    ]

    p_w = 3.78
    p_gap = 0.39
    p_x_start = 0.60
    p_y = 1.45
    p_h = 3.60

    for p_idx, ph in enumerate(phases):
        px = p_x_start + (p_idx * (p_w + p_gap))

        pbox = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(px), Inches(p_y), Inches(p_w), Inches(p_h))
        pbox.name = f"Phase_Card_{p_idx+1}"
        pbox.fill.solid()
        pbox.fill.fore_color.rgb = SURFACE_WHITE
        pbox.line.color.rgb = ph["accent"]
        pbox.line.width = Pt(1.5 if ph["accent"] == ORANGE else 1.0)

        htag = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(px), Inches(p_y), Inches(p_w), Inches(0.70))
        htag.name = f"Phase_Header_{p_idx+1}"
        htag.fill.solid()
        htag.fill.fore_color.rgb = ph["accent"]
        htag.line.fill.background()
        tf_ht = htag.text_frame
        tf_ht.margin_left = tf_ht.margin_right = Inches(0.15)
        tf_ht.margin_top = Inches(0.10)
        p_num = tf_ht.paragraphs[0]
        p_num.text = ph["num"]
        p_num.font.name = "Calibri"
        p_num.font.size = Pt(11)
        p_num.font.bold = True
        p_num.font.color.rgb = RGBColor(0xFE, 0xED, 0xD5) if ph["accent"] == ORANGE else RGBColor(0xE2, 0xE8, 0xF0)

        p_name = tf_ht.add_paragraph()
        p_name.text = ph["name"]
        p_name.font.name = "Calibri"
        p_name.font.size = Pt(16)
        p_name.font.bold = True
        p_name.font.color.rgb = SURFACE_WHITE

        tb_thm = s8.shapes.add_textbox(Inches(px + 0.15), Inches(p_y + 0.80), Inches(p_w - 0.30), Inches(0.35))
        tb_thm.name = f"Phase_Theme_{p_idx+1}"
        tf_thm = tb_thm.text_frame
        tf_thm.margin_top = tf_thm.margin_bottom = tf_thm.margin_left = tf_thm.margin_right = 0
        pthm = tf_thm.paragraphs[0]
        pthm.text = ph["theme"]
        pthm.font.name = "Calibri"
        pthm.font.size = Pt(11)
        pthm.font.bold = True
        pthm.font.color.rgb = TEXT_MUTED

        a1_box = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(px + 0.12), Inches(p_y + 1.22), Inches(p_w - 0.24), Inches(1.05))
        a1_box.name = f"Action_1_{p_idx+1}"
        a1_box.fill.solid()
        a1_box.fill.fore_color.rgb = SURFACE_CARD
        a1_box.line.color.rgb = BORDER_LIGHT
        a1_box.line.width = Pt(0.75)
        tf_a1 = a1_box.text_frame
        tf_a1.word_wrap = True
        tf_a1.margin_left = tf_a1.margin_right = Inches(0.10)
        tf_a1.margin_top = Inches(0.08)
        p_a1t = tf_a1.paragraphs[0]
        p_a1t.text = f"1. {ph['action_1_title']}"
        p_a1t.font.name = "Calibri"
        p_a1t.font.size = Pt(12)
        p_a1t.font.bold = True
        p_a1t.font.color.rgb = NAVY

        p_a1d = tf_a1.add_paragraph()
        p_a1d.text = ph["action_1_desc"]
        p_a1d.font.name = "Calibri"
        p_a1d.font.size = Pt(10.5)
        p_a1d.font.color.rgb = TEXT_DARK
        p_a1d.space_before = Pt(3)

        a2_box = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(px + 0.12), Inches(p_y + 2.38), Inches(p_w - 0.24), Inches(1.05))
        a2_box.name = f"Action_2_{p_idx+1}"
        a2_box.fill.solid()
        a2_box.fill.fore_color.rgb = SURFACE_CARD
        a2_box.line.color.rgb = BORDER_LIGHT
        a2_box.line.width = Pt(0.75)
        tf_a2 = a2_box.text_frame
        tf_a2.word_wrap = True
        tf_a2.margin_left = tf_a2.margin_right = Inches(0.10)
        tf_a2.margin_top = Inches(0.08)
        p_a2t = tf_a2.paragraphs[0]
        p_a2t.text = f"2. {ph['action_2_title']}"
        p_a2t.font.name = "Calibri"
        p_a2t.font.size = Pt(12)
        p_a2t.font.bold = True
        p_a2t.font.color.rgb = NAVY

        p_a2d = tf_a2.add_paragraph()
        p_a2d.text = ph["action_2_desc"]
        p_a2d.font.name = "Calibri"
        p_a2d.font.size = Pt(10.5)
        p_a2d.font.color.rgb = TEXT_DARK
        p_a2d.space_before = Pt(3)

        if p_idx < 2:
            parr_x = px + p_w + 0.08
            parr = s8.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(parr_x), Inches(p_y + 1.60), Inches(0.23), Inches(0.32))
            parr.name = f"Phase_Arrow_{p_idx+1}_to_{p_idx+2}"
            parr.fill.solid()
            parr.fill.fore_color.rgb = ELITIA_BLUE
            parr.line.fill.background()

    eng_y = 5.30
    eng_box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.60), Inches(eng_y), Inches(12.133), Inches(1.15))
    eng_box.name = "Closing_Engagement_Band"
    eng_box.fill.solid()
    eng_box.fill.fore_color.rgb = NAVY
    eng_box.line.color.rgb = ELITIA_BLUE
    eng_box.line.width = Pt(1.5)

    tf_eng = eng_box.text_frame
    tf_eng.word_wrap = True
    tf_eng.margin_left = Inches(0.30)
    tf_eng.margin_right = Inches(0.30)
    tf_eng.margin_top = Inches(0.14)
    tf_eng.margin_bottom = Inches(0.10)

    p_eh = tf_eng.paragraphs[0]
    p_eh.text = "How we engage: Modular licensing  ·  Co-development with your engineers  ·  Specialist staff augmentation"
    p_eh.font.name = "Calibri"
    p_eh.font.size = Pt(15)
    p_eh.font.bold = True
    p_eh.font.color.rgb = SURFACE_WHITE

    p_eb = tf_eng.add_paragraph()
    p_eb.text = "Flexible collaboration models tailored to customer governance: license individual proprietary modules, co-innovate on complex plant-specific integrations, or augment internal engineering teams with deep SAP & OT specialists."
    p_eb.font.name = "Calibri"
    p_eb.font.size = Pt(12)
    p_eb.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)
    p_eb.space_before = Pt(4)

    prs.save(filename)
    print(f"[SUCCESS] Clean presentation generated: {filename}")
    return filename

if __name__ == "__main__":
    create_deck()
