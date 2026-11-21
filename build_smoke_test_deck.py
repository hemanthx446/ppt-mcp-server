"""
Build Smoke-Test Deck: Supplier Delivery Tracker: CIO briefing
Generates the authentic executive-ready 8-slide presentation using the Lumbini Presentation Pipeline
(DeckRenderer, themes/lumbini/template.pptx, native charts, dashboard concept, benchmark tables,
and Inter typography), embodying the 14 Scrutiny Perspectives for content and context.
"""

import os
import sys
import glob
from pipeline.renderer import DeckRenderer
from design_system.lumbini.tokens import get_lumbini_theme


def build_deck_spec() -> dict:
    theme = get_lumbini_theme()
    
    spec = {
        "meta": {
            "client": "CIO & Supply Chain Board",
            "confidentiality": "Confidential",
            "doc_type": "Architecture Briefing",
            "platform_levels": ["L4 Enterprise ERP", "L3 MOM / Dock Execution", "L2 Automation / Scanners"]
        },
        "slides": [
            # Slide 1: Cover (Lumbini Master Template Layout)
            {
                "slide_number": 1,
                "content_shape": "cover",
                "title": "Supplier Delivery Tracker: CIO Briefing",
                "subtitle": "Closed-Loop Inbound Execution, Constraint Protection & SAP S/4HANA Integration",
                "pill_text": "Executive Briefing  |  Inbound Supply Chain",
                "metadata": [
                    ("Prepared for", "Chief Information Officer & Enterprise Architecture Board"),
                    ("Prepared by", "Lumbini Elite Solutions & Services | Enterprise Solutions Practice"),
                    ("Core ERP Core", "SAP S/4HANA (Single System of Record)"),
                    ("Date", "November 2026")
                ],
                "notes": "Executive briefing for CIO and Supply Chain Board. Establishes the integrated inbound visibility and execution architecture."
            },

            # Slide 2: Context & Operational Friction (Requirement to Outcome Layout)
            {
                "slide_number": 2,
                "content_shape": "requirement_to_outcome",
                "eyebrow": "Operational Reality & Business Friction",
                "title": "Inbound Opacity Causes $2.4M Freight Waste and Constraint Starvation",
                "subtitle": "From disconnected plant dock firefighting to synchronized enterprise material flow",
                "items": [
                    {
                        "requirement": "Yard Congestion & Driver Detention",
                        "today": "Trucks arrive unscheduled; 4.2h avg yard dwell; drivers idle without bay countdowns or basic amenities.",
                        "outcome": "Automated SMS driver staging, scheduled bay allocations, and <45 min yard turnaround.",
                        "badge_color": theme.C_PRIMARY
                    },
                    {
                        "requirement": "Bottleneck Assembly Line Starvation",
                        "today": "18 hrs/month line downtime; supervisors learn of part stockouts mid-shift, halting high-value production.",
                        "outcome": "Drum-Buffer-Rope line buffer tracking; assembly schedulers alerted hours before starvation.",
                        "badge_color": theme.C_ACCENT
                    },
                    {
                        "requirement": "Emergency Expedited Freight Penalties",
                        "today": "$2.4M wasted annually in emergency chartered air shipments and hot-shot couriers due to upstream transit blind spots.",
                        "outcome": "Predictive carrier milestone tracking cuts expedited freight by $1.8M annually.",
                        "badge_color": theme.C_NAVY
                    },
                    {
                        "requirement": "ERP Goods Receipt Lag & Data Silos",
                        "today": "Dock receipts keyed manually into spreadsheets; SAP core lags physical arrival by 24 to 48 hours.",
                        "outcome": "Sub-minute event sync into SAP S/4HANA; single authoritative System of Record.",
                        "badge_color": theme.C_MUTED
                    }
                ],
                "notes": "Slide 2 establishes the human and business problem: plant-level opacity forces expensive expediting and line halts."
            },

            # Slide 3: Flow with Actions (Inbound Edge Dock to SAP S/4HANA Core)
            {
                "slide_number": 3,
                "content_shape": "flow_with_actions",
                "eyebrow": "System Architecture & Integration",
                "title": "Edge Dock Resiliency Coupled to Event-Driven SAP S/4HANA Core",
                "subtitle": "Authoritative Single System of Record in SAP; local edge gateway ensures zero plant downtime",
                "flow_boxes": [
                    ("1. SUPPLIERS & CARRIERS", "Open ASN Web Portal\nCarrier SMS Check-In\nGPS Milestones", theme.C_PRIMARY),
                    ("2. RESILIENT EDGE GATEWAY", "Plant L3 Edge Gateway\nIn-Memory B2MML Cache\nOffline Queueing", theme.C_NAVY),
                    ("3. EVENT STREAMING BUS", "Kafka / EventBridge\nISA-95 B2MML Topics\nSub-Minute Ingestion", theme.C_PRIMARY),
                    ("4. SAP CORE & MES", "SAP S/4HANA (System of Record)\nSynchronous MIGO GR\nMES Finite Schedule Feed", theme.C_NAVY)
                ],
                "actions": [
                    "Supplier issues ASN with lot/batch data; driver receives gate appointment.",
                    "Dock clerks scan pallets offline; sub-second validation even if WAN drops.",
                    "Events stream to cloud bus; reconciles edge transactions within 60 seconds.",
                    "SAP executes automated Goods Receipt; MES reprioritizes assembly line runs."
                ],
                "legend_items": [
                    (theme.C_NAVY, "Level 4 Enterprise Core"),
                    (theme.C_PRIMARY, "Level 3 Plant Edge"),
                    (theme.C_ACCENT, "Physical Execution")
                ],
                "caveat_text": "Architectural Principle: SAP S/4HANA remains the single authoritative System of Record. Resilient edge caching prevents factory downtime.",
                "notes": "Slide 3 illustrates the edge-to-core architecture. Emphasizes Ross single system of record and Brandl L3 decoupling."
            },

            # Slide 4: Step Line (Shopfloor Dock Receiving & ISA-95 Traceability)
            {
                "slide_number": 4,
                "content_shape": "step_line",
                "eyebrow": "Shopfloor Execution & Quality Operations",
                "title": "Shopfloor Dock Execution: Ergonomic Assistant with Lot Traceability",
                "subtitle": "Ruggedized mobile tools with operator override rights, lot/batch tracking, and automated SAP QM",
                "steps": [
                    ("Gate Arrival & Hospitality", "Driver check-in via SMS; automated bay countdown; driver lounge staging."),
                    ("Glove-Friendly Scan", "Rugged tablet barcode scan (>48px targets); captures Vendor Lot, Internal Batch, Expiry."),
                    ("SAP QM Inspection Lot", "Automated SAP QM inspection lot triggered; damaged goods routed to Quarantine Bay."),
                    ("Constraint Staging Putaway", "Forklift operator transports pallets to staging bays prioritized by assembly line DBR urgency."),
                    ("Instant SAP GR Posting", "Synchronous MIGO goods receipt posted to SAP S/4HANA via OData API within 60 seconds.")
                ],
                "deliverables": [
                    "Bay ETA SMS",
                    "Batch Genealogy",
                    "QM Lot / Hold",
                    "DBR Priority Tag",
                    "MIGO Doc #"
                ],
                "caveat_text": "Human-Centered Design: Empowers dock specialists with situational override authority; eliminates surveillance pacing.",
                "notes": "Slide 4 shows the physical dock receiving sequence with ISA-95 lot tracking and frontline dignity safeguards."
            },

            # Slide 5: Executive Dashboard Concept (Real Native Charts & KPI Tiles)
            {
                "slide_number": 5,
                "content_shape": "dashboard_concept",
                "eyebrow": "Performance Cockpit & Statistical Governance",
                "title": "Statistical Process Control & AI Decision Copilot Drive Inbound Calm",
                "subtitle": "Shewhart SPC charts separate systemic transit noise from true supplier performance breakdown",
                "flow_steps": ["Inbound Transit Tracking", "Statistical SPC Control", "Constraint Buffer Management", "Governed AI Copilot"],
                "tabs": ["Strategic Suppliers", "Constraint Part Buffers", "Carrier Yard Velocity", "Quality Exceptions"],
                "kpis": [
                    ("STATISTICAL OTIF", "88.4%", "+6.2% vs Q2"),
                    ("CONSTRAINT BUFFER", "94.6%", "+12.4% MoM"),
                    ("CARRIER YARD DWELL", "42 Mins", "-210 Mins Saved"),
                    ("FRONT-LINE USABILITY", "86/100", "+24 pts SUS")
                ],
                "chart1_title": "CARRIER YARD DWELL TIME REDUCTION (MINS)",
                "column_chart_labels": ["Plant 1 (Baseline)", "Plant 1 (Post-Pilot)", "Plant 2 (Target)", "Plant 3 (Target)", "Plant 4 (Target)"],
                "column_chart_values": [252, 42, 45, 45, 40],
                "chart2_title": "VENDOR DELIVERY ON-TIME RATE VS STATISTICAL LIMITS",
                "line_chart_categories": ["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"],
                "line_actual": [76.5, 79.2, 82.0, 85.4, 84.1, 87.8, 88.4, 89.1],
                "line_plan": [82.0, 82.0, 82.0, 82.0, 82.0, 82.0, 82.0, 82.0],
                "drill_title": "AI DECISION COPILOT",
                "drill_steps": [
                    ("SPC Noise Filtering", "Distinguishes normal highway transit noise from special-cause vendor failure."),
                    ("AI Risk Copilot", "Predicts supplier delay probabilities with transparent confidence intervals."),
                    ("Central Procurement Rights", "Commercial tier adjustments governed by buyers; eliminates rogue dock rerouting."),
                    ("Driver Hospitality Index", "Tracks driver wait times and lounge amenities to maintain carrier loyalty.")
                ],
                "platform_title": "ELITIA LOGISTICS INTELLIGENCE",
                "platform_note": "Governed Decision Rights: Dock supervisors annotate exception context; central category managers retain commercial authority.",
                "platform_disclaimer": "SAP S/4HANA verified metrics",
                "notes": "Slide 5 features an executive dashboard mockup with real native column and line charts demonstrating statistical quality control."
            },

            # Slide 6: Layered Architecture Stack (Enterprise Security & Edge Microservices)
            {
                "slide_number": 6,
                "content_shape": "layered_stack",
                "eyebrow": "Technology Physics & Enterprise Integration",
                "title": "Hybrid Cloud-Edge Architecture with Enterprise Security Standards",
                "subtitle": "Modern containerized microservices integrated with corporate IAM, SAP S/4HANA, and plant MES",
                "layers": [
                    {
                        "tier": "LEVEL 4: ENTERPRISE CORE",
                        "title": "SAP S/4HANA (Single System of Record) & Enterprise Data Lakehouse",
                        "desc": "Certified OData/REST APIs execute synchronous MIGO Goods Receipts; curates structured logistics telemetry.",
                        "color": theme.C_NAVY
                    },
                    {
                        "tier": "LEVEL 3: EVENT BUS & MES",
                        "title": "Apache Kafka / EventBridge & Shopfloor MES Finite Line Connector",
                        "desc": "High-throughput asynchronous pub/sub messaging decoupling plant edge; sub-minute feeds to MES line schedules.",
                        "color": theme.C_PRIMARY
                    },
                    {
                        "tier": "LEVEL 2: PLANT EDGE GATEWAY",
                        "title": "Local Docker Edge Gateway with In-Memory B2MML Transactional Cache",
                        "desc": "Runs autonomous plant dock operations; sub-second barcode scans execute offline during network drops.",
                        "color": theme.C_PRIMARY
                    },
                    {
                        "tier": "LEVEL 1: FRONTLINE ECOSYSTEM",
                        "title": "Frontline Dock Assistant PWA & Carrier Driver Self-Service Mobile Web",
                        "desc": "Rugged glove-friendly UI (>48px targets) with operator override rights, plus automated SMS driver countdowns.",
                        "color": theme.C_MUTED
                    }
                ],
                "callout_note": "Security & Architecture: Fully integrated with corporate Azure AD / Okta SSO, end-to-end TLS 1.3 encryption, and ISA-95 standard data definitions.",
                "notes": "Slide 6 outlines the 4-layer technical stack showing clear physical network topology and edge resilience."
            },

            # Slide 7: Phases Over Time (12-Week Vertical Delivery Roadmap)
            {
                "slide_number": 7,
                "content_shape": "phases_over_time",
                "eyebrow": "Implementation Strategy & Transition Governance",
                "title": "12-Week Vertical Delivery Slice with 90-Day Productivity J-Curve Buffer",
                "subtitle": "Vertical end-to-end use-case deployment with frontline co-design clinics and assisted dual-running",
                "phases": [
                    ("Phase 1: Co-Design Slice (W1–4)", "Frontline dock worker clinics; deliver vertical slice: ASN -> Edge Scan -> SAP GR -> Quarantine Bay."),
                    ("Phase 2: Pilot & J-Curve Buffer (W5–12)", "Plant 1 pilot go-live; 90-day Productivity J-Curve buffer; assisted dual-running support for dock teams."),
                    ("Phase 3: MES & Multi-Plant (W13–24)", "Closed-loop MES finite line scheduling integration; rollout to Plants 2, 3, and 4; cross-plant buffer visibility."),
                    ("Phase 4: Predictive ML Platform (W25–36)", "AI Decision Copilot deployment for category managers; automated VMI supplier replenishment onboarding.")
                ],
                "future_readiness_title": "Productivity J-Curve Realism",
                "future_readiness_desc": "Explicitly plans for the initial 60-day operational learning curve, ensuring executive confidence and sustained adoption.",
                "notes": "Slide 7 presents a phased implementation roadmap structured around vertical use cases and J-Curve transition management."
            },

            # Slide 8: Benchmark Table (Commercial Investment Breakdown & Throughput ROI)
            {
                "slide_number": 8,
                "content_shape": "benchmark_table",
                "eyebrow": "Business Case & Decision Requested",
                "title": "Rebalanced Investment Prioritizes Intangibles for 14-Month Payback",
                "subtitle": "43% of funds allocated to organizational capital; protects $1.8M annual constraint throughput",
                "headers": ["Investment Workstream", "Capital Allocation", "Asset Classification", "Core Deliverable & Strategic Value"],
                "col_widths": [3.6, 1.8, 2.6, 4.3],
                "rows": [
                    ["Edge & Cloud Software Engineering", "$140,000", "Tangible Software", "Plant edge gateway, Kafka event broker, and mobile PWA build."],
                    ["Rugged Mobile Scanners & Lounge Kiosks", "$50,000", "Tangible Hardware", "20 rugged Android tablets, ring scanners, and driver gate kiosks."],
                    ["SAP S/4HANA & MES Integration", "$50,000", "Tangible Integration", "Certified OData/REST APIs for synchronous MIGO & MES line feeds."],
                    ["Frontline Co-Design & Digital Upskilling", "$80,000", "Complementary Intangible", "Worker co-design workshops, ergonomics testing, and role redesign."],
                    ["Supplier Data Hygiene & Onboarding Clinics", "$60,000", "Complementary Intangible", "Top 50 component vendor ASN clinics and EDI mapping validation."],
                    ["Transformation Steering & Change Leadership", "$40,000", "Complementary Intangible", "Cross-functional governance board, SOP rewrites, and executive steering."],
                    ["Total Capital & Intangible Investment", "$420,000", "100% Balanced Program", "14-Month Payback | $1.8M Annual Net Freight & Throughput Savings"]
                ],
                "callout_text": "Executive Decision Requested: Approve $420,000 investment to execute 12-week Phase 1 at Plant 1, establishing closed-loop inbound architecture.",
                "notes": "Slide 8 details the investment breakdown. Highlights 43% allocation to complementary intangibles (Brynjolfsson) and $1.8M constraint ROI (Goldratt)."
            }
        ]
    }
    return spec


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_dir, "Supplier_Delivery_Tracker_CIO_Briefing.pptx")
    previews_dir = os.path.join(base_dir, "previews_smoke")
    os.makedirs(previews_dir, exist_ok=True)

    print("Building Authentic Lumbini Presentation via DeckRenderer...")
    spec = build_deck_spec()
    renderer = DeckRenderer(theme_name="lumbini")
    rendered_path = renderer.render(spec, output_path)
    print(f"Presentation generated at: {rendered_path}")

    # Render Preview Images via PowerPoint COM
    print("Rendering 1080p slide preview images...")
    try:
        import win32com.client
        import pythoncom
        from build_elitia_track_and_trace_deck import ensure_powerpoint_compatible_order
        ensure_powerpoint_compatible_order(rendered_path)
        pythoncom.CoInitialize()
        ppt_app = win32com.client.Dispatch("PowerPoint.Application")
        abs_pptx = os.path.abspath(rendered_path)
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
