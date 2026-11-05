import os
import sys
import json
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from pipeline.renderer import DeckRenderer
from pipeline.qa import QualityGate
from pipeline.distill import ContentDistiller
from pipeline.visual_plan import VisualPlanner
from design_system.lumbini.tokens import get_lumbini_theme

def build_jbvnl_10slide_spec() -> dict:
    theme = get_lumbini_theme()

    slides = [
        # Slide 1: Title & Opening Challenge (Dark Hero Canvas)
        {
            "slide_number": 1,
            "content_shape": "cover",
            "dark_theme": True,
            "title": "JBVNL Has SAP. Is JBVNL Getting Its Money's Worth?",
            "subtitle": "Turning Existing Technology Investment into Better Financial and Operational Performance",
            "metadata": [
                ("Prepared for", "JBVNL Leadership"),
                ("Strategic Advisor", "Lumbini Elite Solutions"),
                ("Focus Area", "SAP Financial Value Realization"),
                ("Date", "November 2026")
            ],
            "pill_text": "Executive Briefing  |  JBVNL Strategy",
            "layout_rationale": "Dark navy executive cover establishing an authoritative financial advisory tone.",
            "notes": "What Management Should Understand: JBVNL has already paid for an enterprise platform, but parallel manual processes prevent realization of that investment.\nWhy It Matters Financially: Technology that is not utilized effectively delivers zero financial return while manual workarounds continue to leak operating money.\nConclusion to Draw: Management should explore unlocking value from its existing system rather than considering new technology.\nQuestion to Ask: 'If we already have SAP, why are we still spending so much time and effort managing business operations manually?'"
        },

        # Slide 2: Where Is JBVNL's Money Getting Stuck? (Levels x Dimensions Matrix)
        {
            "slide_number": 2,
            "content_shape": "levels_x_dimensions",
            "eyebrow": "Operational Loss Diagnostics",
            "title": "Financial losses do not always begin in finance; they begin in business processes",
            "subtitle": "Six operational areas where disconnected workflows create revenue leakages and cost inflation",
            "col_headers": ["Operational Process Gaps", "Financial Consequences", "Management Attention Levers"],
            "row_headers": [
                ("Commercial Operations", "Billing & Collections", theme.C_NAVY),
                ("Supply Chain & Projects", "Procurement & Schemes", theme.C_PRIMARY),
                ("Asset Management", "Inventory & Maintenance", theme.C_MUTED)
            ],
            "cells": [
                [
                    "Delayed meter readings, unmetered supply, unlinked receipts.",
                    "Depressed cash inflows, rising arrears, elevated short-term debt.",
                    "Automated meter-to-cash tracking and daily reconciliation."
                ],
                [
                    "Offline purchase approvals, rate bypass, slow capitalization.",
                    "Uncontrolled procurement costs, trapped store capital, idle CWIP.",
                    "Enforced digital purchase orders and milestone accounting."
                ],
                [
                    "Paper store chits, excess safety buffers, breakdown logs.",
                    "Capital locked in slow inventory, high equipment repair opex.",
                    "Centralized reorder rules and systematic preventive upkeep."
                ]
            ],
            "caveat_text": "Takeaway: Disconnected processes create delays, cost inflation, and loss of control.",
            "confirmed_title": "Core Value Levers",
            "confirmed_caps": [
                "Billing Realization",
                "Procurement Control",
                "Inventory Optimization",
                "Capex Protection"
            ],
            "layout_rationale": "Chosen 'levels_x_dimensions' to map the 6 operational bottleneck areas directly across financial consequences and management action levers.",
            "notes": "What Management Should Understand: Revenue and working capital problems originate in operational disconnects across billing, stores, and maintenance.\nWhy It Matters Financially: Fixing financial statements requires fixing the underlying operational workflows that feed those numbers.\nConclusion to Draw: Disconnected workflows are actively trapping money across circles and departments.\nQuestion to Ask: 'How much of our cash delay is caused by slow paperwork between field offices, stores, and finance?'"
        },

        # Slide 3: Electricity Supplied Is Not Money Collected (Step-Line Pipeline)
        {
            "slide_number": 3,
            "content_shape": "step_line",
            "source_id": "PFC 12th/13th Integrated Rating (FY23/24)",
            "eyebrow": "Commercial Value Stream",
            "title": "The business must track every step from power purchase to payment collection",
            "subtitle": "Closing operational disconnects across the commercial chain to protect revenues and eliminate leakages",
            "steps": [
                ("Power Purchase", "What are we paying for input power?"),
                ("Grid Distribution", "How much energy enters the network?"),
                ("Energy Accounting", "How much energy is consumed and verified?"),
                ("Consumer Billing", "How much revenue is accurately billed?"),
                ("Payment Collection", "How much cash has actually been collected?"),
                ("Reconciliation", "Does collected money match bank and ledger?")
            ],
            "deliverables": [
                "AT&C Loss: 30.28% (PFC FY23)",
                "Billing Gap: 93.85% efficiency",
                "Collection Gap: 95.46% efficiency",
                "Reconciliation: Bank & consumer ledger"
            ],
            "caveat_text": "Source: PFC Report FY23/24: SAP provides commercial and financial governance, integrating with specialized MDMS, HES, AMR, and SCADA.",
            "layout_rationale": "Chosen 'step_line' 6-step sequential pipeline with aligned operational leakage risks directly mapped below each commercial stage.",
            "notes": "What Management Should Understand: Money collection is the final step of a continuous 6-stage chain; a breakdown at any earlier stage destroys revenue.\nWhy It Matters Financially: High AT&C losses (30.28%) are driven by gaps in energy accounting and delayed billing, not merely collection drives.\nConclusion to Draw: Managing meter-to-cash as an integrated enterprise flow in SAP protects cash at every handover.\nQuestion to Ask: 'Do we have a single system view showing energy sent, energy billed, and cash banked by feeder every month?'"
        },

        # Slide 4: Manual Working vs. SAP-Driven Working (Requirement to Outcome)
        {
            "slide_number": 4,
            "content_shape": "requirement_to_outcome",
            "eyebrow": "Operational Comparison",
            "title": "The same business process can be managed with more control and less manual effort",
            "subtitle": "Eliminating spreadsheet follow-ups and paper chits through standardized, auditable digital workflows",
            "headers": ["Business Dimension", "Manual Working Today", "SAP-Driven Working"],
            "items": [
                {
                    "requirement": "Transaction Recording",
                    "today": "Entered multiple times across spreadsheets; adoption remains low.",
                    "outcome": "Single digital entry in SAP establishing immediate operational ownership.",
                    "badge_color": theme.C_PRIMARY
                },
                {
                    "requirement": "Approval Authority",
                    "today": "Chasing physical files and emails; decisions lack audit trails.",
                    "outcome": "Standardized multi-level digital workflows with complete transparency.",
                    "badge_color": theme.C_NAVY
                },
                {
                    "requirement": "Expenditure Control",
                    "today": "Spending reconciled weeks late; budget limits bypassed offline.",
                    "outcome": "Real-time budget availability checks preventing unapproved commitments.",
                    "badge_color": theme.C_ACCENT
                },
                {
                    "requirement": "Management Oversight",
                    "today": "Reports compiled manually after problems occur; delayed visibility.",
                    "outcome": "Automated exception cockpits alerting leadership to operational delays.",
                    "badge_color": theme.C_MUTED
                }
            ],
            "layout_rationale": "Chosen 'requirement_to_outcome' 4-row comparative structure to sharply contrast current manual bottlenecks with target enterprise outcomes.",
            "notes": "What Management Should Understand: SAP is not extra paperwork; it replaces duplicate spreadsheets and offline registers with a single auditable entry.\nWhy It Matters Financially: Manual approvals and paper chits obscure budget overruns and delay vendor settlements.\nConclusion to Draw: Transitioning to SAP saves employee hours and establishes executive accountability.\nQuestion to Ask: 'Why should an engineer spend hours reconciling spreadsheets when SAP can track store issues and work orders automatically?'"
        },

        # Slide 5: Five Ways SAP Improves Financial Performance (Flow with Actions)
        {
            "slide_number": 5,
            "content_shape": "flow_with_actions",
            "eyebrow": "Financial Value Levers",
            "title": "Better process control can protect revenue and reduce unnecessary expenditure",
            "subtitle": "Five concrete operational levers to expand EBITDA, release working capital, and enforce discipline",
            "flow_boxes": [
                ("Revenue Realization", "Track billing & collections", theme.C_PRIMARY),
                ("Procurement Control", "Standardize purchase orders", theme.C_PRIMARY),
                ("Inventory Optimization", "Real-time stock visibility", theme.C_PRIMARY),
                ("Capex Governance", "Track project milestones", theme.C_PRIMARY),
                ("Asset Upkeep", "Schedule preventive repair", theme.C_NAVY)
            ],
            "actions": [
                "Revenue Protection: Early billing exception alerts and targeted commercial recovery.",
                "Purchase Savings: Rate contract enforcement preventing off-contract emergency buying.",
                "Working Capital: Real-time stock visibility avoiding duplicate purchases across circles.",
                "Capex Protection: Milestone project accounting ensuring prompt CWIP capitalization."
            ],
            "legend_items": [
                (theme.C_PRIMARY, "Revenue Protection & Cost Reduction"),
                (theme.C_NAVY, "Working Capital & Asset Governance")
            ],
            "caveat_text": "Core Levers: Revenue Protection | Cost Reduction | Working Capital | Financial Control.",
            "layout_rationale": "Chosen 'flow_with_actions' to show the 5 functional value levers supported by actionable enterprise initiatives.",
            "notes": "What Management Should Understand: SAP improves financial performance across five distinct operational areas, from stores to capital projects.\nWhy It Matters Financially: These 5 levers directly impact EBITDA, operating cash flow, and debt-servicing capacity.\nConclusion to Draw: Financial turnaround requires coordinated discipline across procurement, stores, billing, and projects.\nQuestion to Ask: 'Which of these five areas currently causes our biggest monthly cash drain?'"
        },

        # Slide 6: JBVNL's Financial Performance: What Needs to Improve? (Annotated Chart)
        {
            "slide_number": 6,
            "content_shape": "annotated_chart",
            "source_id": "PFC 12th/13th Integrated Rating (FY23/24) · MoP PIB (FY25) · JSERC Tariff Orders",
            "eyebrow": "Verified Financial Baseline",
            "title": "The numbers tell management where immediate operational attention is required",
            "subtitle": "Verified performance indicators from official regulatory and statutory filings establishing baseline priorities",
            "chart_type": "column",
            "categories": ["FY21 Base", "FY22 Actual", "FY23 Actual", "FY24 Actual", "FY25 Benchmark"],
            "series_data": [
                {"name": "DISCOM Aggregate Net Profit / Loss", "values": [-50281.0, -31025.0, -28200.0, -25553.0, 2701.0]}
            ],
            "chart_title": "All-India DISCOMs Aggregate Net Profit / Loss (₹ Crore)",
            "x_label": "Financial Year",
            "y_label": "Net Profit / Loss (₹ Cr)",
            "key_takeaway": "All-India DISCOMs achieved a historic turnaround from a loss of ₹25,553 Cr (FY24) to a profit of ₹2,701 Cr (FY25) via operational discipline (MoP / PFC data).",
            "callout_annotation": "JBVNL Official Baseline: AT&C Loss 30.28% (Rank 52, PFC FY23) | Billing Efficiency 93.85% | Collection Efficiency 95.46% (PFC FY24) | ACS-ARR Gap ₹1.12/kWh (JSERC True-up). Consumer receivables exceed ₹6,000 Cr, locking up critical operating cash.",
            "layout_rationale": "Chosen 'annotated_chart' to display national utility turnaround trajectory paired with an authoritative JBVNL baseline panel.",
            "notes": "What Management Should Understand: JBVNL's 30.28% AT&C loss and ₹1.12/kWh ACS-ARR gap represent substantial financial leakage that operational discipline can narrow.\nWhy It Matters Financially: National data proves utilities are turning profitable by tightening billing and collection processes under RDSS.\nConclusion to Draw: JBVNL has the operational headroom to convert commercial losses into cash inflows.\nQuestion to Ask: 'If other state utilities can turnaround their balance sheets through process discipline, why can't JBVNL?'"
        },

        # Slide 7: Indian Power Utilities Are Moving Ahead (Iceberg Shift)
        {
            "slide_number": 7,
            "content_shape": "iceberg_shift",
            "source_id": "World Bank, TPDDL Reports, and CAG Assam SPSE Audit",
            "eyebrow": "Utility Transformation Benchmarks",
            "title": "Power utilities are turning losses into cash through process control",
            "subtitle": "Empirical evidence from Indian power distribution turnarounds",
            "visible_event": {
                "title": "Visible Benchmark: Utilities Achieving Operational Turnaround",
                "desc": "Utilities prove that process discipline and system integration convert losses into viability."
            },
            "submerged_layers": [
                {
                    "layer_name": "Tata Power-DDL (North Delhi)",
                    "finding": "Integrated SAP IS-U with GIS and AMR; cut AT&C losses from 53.1% to <6.8% with >99.5% collection."
                },
                {
                    "layer_name": "Goa Electricity Department",
                    "finding": "Rolled out SAP IS-U to 600,000 consumers in 6 months via standardized utility workflows."
                },
                {
                    "layer_name": "Assam APDCL (CAG Warning)",
                    "finding": "CAG audit found that deploying SAP without training preserved manual registers and arrears."
                }
            ],
            "callout_text": "Source: World Bank, TPDDL, and CAG Audit Report (Assam SPSEs).",
            "layout_rationale": "Chosen 'iceberg_shift' to contrast visible turnaround milestones with deep operational discipline and governance lessons.",
            "notes": "What Management Should Understand: Technology alone does not guarantee results; adoption, training, and governance are the real drivers of turnaround.\nWhy It Matters Financially: TPDDL proved that eliminating parallel registers cuts AT&C losses dramatically; Assam APDCL showed that ignoring training preserves manual workarounds.\nConclusion to Draw: JBVNL must combine its existing SAP platform with strict process governance and user enablement.\nQuestion to Ask: 'Are we managing JBVNL like Assam APDCL before its audit, or are we building the governance of Tata Power-DDL?'"
        },

        # Slide 8: What If JBVNL Improves Its Processes? (Tradeoff Matrix / Financial Value Bridge)
        {
            "slide_number": 8,
            "content_shape": "tradeoff_matrix",
            "source_id": "Illustrative Financial Scenario (JBVNL FY24 Baseline)",
            "eyebrow": "Financial Impact Modeling",
            "title": "Even small process improvements create significant financial value",
            "subtitle": "Financial impact matrix and illustrative scenarios based on JBVNL's operating baseline",
            "x_axis_title": "Operational Process Maturity (Manual Workarounds ➔ Governed SAP Processes)",
            "y_axis_title": "Financial Balance Sheet Impact (Operating Deficit ➔ Sustainable Cash Flow)",
            "quadrants": [
                {
                    "name": "Billing & Collection Velocity",
                    "desc": "Closing commercial billing gaps directly expands revenues, adding ₹300–600 Cr into operating EBITDA."
                },
                {
                    "name": "Procurement Spend Control",
                    "desc": "Standardized purchase approvals and contract enforcement reduce off-contract purchase variances by 8–12%."
                },
                {
                    "name": "Inventory Rationalization",
                    "desc": "Stock visibility across circles prevents duplicate buying, releasing ₹45–60 Cr in locked working capital."
                },
                {
                    "name": "Capex Tariff Recovery",
                    "desc": "Prompt CWIP capitalization ensures full capex pass-through in JSERC petitions, avoiding disallowances."
                }
            ],
            "callout_note": "Illustrative Scenarios (JBVNL Base):\n• +1% Collection: ₹65–70 Cr cash recovered annually (₹6,800 Cr base).\n• 15-Day Inventory Drop: ₹45–60 Cr working capital unlocked.\n• Timely CWIP Closure: ₹50+ Cr tariff disallowances avoided.\n\nTakeaway: Process visibility drives financial control and cash results.",
            "layout_rationale": "Chosen 'tradeoff_matrix' 2x2 decision space to map operational transformation maturity directly against balance sheet realization levers.",
            "notes": "What Management Should Understand: In a utility with over ₹6,500 Cr in revenue, a single percentage point improvement generates ₹65+ Cr in hard cash.\nWhy It Matters Financially: Small process improvements generate substantial cash inflows that reduce expensive short-term borrowings.\nConclusion to Draw: Process optimization pays for itself many times over through working capital release and loss reduction.\nQuestion to Ask: 'Can we afford to leave ₹65–70 Cr on the table every year just because our collection reconciliation is delayed?'"
        },

        # Slide 9: A Practical 90-Day Plan to Start Getting Results (Roadmap Rows)
        {
            "slide_number": 9,
            "content_shape": "phases_over_time",
            "eyebrow": "Pragmatic Implementation Roadmap",
            "title": "Start with existing SAP; fix the most important business processes first",
            "subtitle": "A pragmatic 90-day plan focused on high-impact quick wins before broader enterprise optimization",
            "phases": [
                ("Days 1–30: Assess & Audit", "Weeks 1–4 · SAP utilization audit · Process gap mapping · Master data checks · Leadership workshops"),
                ("Days 31–60: Standardize", "Weeks 5–8 · Select priority circles · Clean master data · Standardize workflows · Role-based training"),
                ("Days 61–90: Pilot & Measure", "Weeks 9–12 · Deploy in pilot circles · Track live transactions · Measure KPI gains · Executive dashboards")
            ],
            "future_readiness_title": "Target Pilot Focus Streams",
            "future_readiness_desc": "Focused on 2 high-impact streams: Procurement (stopping offline approvals) and Stores (eliminating paper chits).",
            "layout_rationale": "Chosen 'phases_over_time' 3-stage sequential timeline detailing the 90-day execution roadmap.",
            "notes": "What Management Should Understand: We are not proposing a multi-year disruption; we propose a structured 90-day pilot focused on high-impact areas.\nWhy It Matters Financially: A phased approach delivers measurable quick wins in 90 days without requiring capital investments in new software.\nConclusion to Draw: Starting with procurement and stores provides immediate expenditure control and working capital recovery.\nQuestion to Ask: 'Are we ready to pilot disciplined SAP usage in one or two circles over the next 90 days to prove the financial benefit?'"
        },

        # Slide 10: The Decision: Start Using What JBVNL Already Has (Dark Hero Finale)
        {
            "slide_number": 10,
            "content_shape": "closing",
            "title": "The Opportunity Is Already Within JBVNL; Next Step Is Action",
            "subtitle": "Four decisive executive actions to transition from manual workarounds to governed enterprise operations",
            "core_message": "JBVNL does not necessarily need another system to begin improving its business performance. It needs to unlock the value of the system it already owns.",
            "pillars": [
                ("Executive Sponsorship", "Nominate a leadership sponsor to champion SAP process adoption and eliminate parallel registers."),
                ("Departmental Ownership", "Designate accountable officers across Finance, Stores, Procurement, Projects, and Field Circles."),
                ("Process & Data Access", "Authorize a rapid diagnostics team to inspect current transaction usage, approval logs, and system data."),
                ("90-Day Pilot Approval", "Approve a focused 90-day pilot with fortnightly milestone reviews and quantifiable financial KPI targets.")
            ],
            "concluding_statement": "Every transaction accounted for. Every rupee tracked. Every process accountable.",
            "pill_text": "Executive Decision  |  JBVNL 2026",
            "layout_rationale": "Dark navy executive finale synthesizing required management decisions and delivering the decisive closing mandate.",
            "notes": "What Management Should Understand: The technology is in place; turning it into financial results requires four clear management decisions today.\nWhy It Matters Financially: Every month of delay preserves manual workarounds, unreconciled accounts, and commercial leakage.\nConclusion to Draw: Management should approve the executive sponsor and the 90-day pilot initiative immediately.\nQuestion to Ask: 'Can we agree today to nominate our executive sponsor and approve the 90-day pilot so we can start seeing results?'"
        }
    ]

    return {
        "theme": "lumbini",
        "client": "JBVNL",
        "meta": {
            "client": "JBVNL",
            "topic": "Turning SAP Investment into Financial Results",
            "confidentiality": "Executive Briefing",
            "doc_type": "Management Presentation"
        },
        "sections": [
            ("The Financial Reality", 3),
            ("Process Control & Capabilities", 2),
            ("Empirical Evidence & Financial Impact", 3),
            ("Action Plan & Management Decisions", 2)
        ],
        "slides": slides
    }

if __name__ == "__main__":
    out_pptx = os.path.abspath("JBVNL_10_Slide_Executive_Presentation.pptx")
    spec = build_jbvnl_10slide_spec()

    # 1. Distillation and Word Budget Audit
    print("=" * 70)
    print("STAGE 1: CONTENT DISTILLATION & WORD BUDGET AUDIT")
    print("=" * 70)
    distiller = ContentDistiller()
    total_words = 0
    all_valid = True
    for s in spec["slides"]:
        valid, w, viols = distiller.audit_slide_content(s)
        total_words += w
        if not valid:
            all_valid = False
        print(f"Slide {s['slide_number']:02d} ({s['content_shape']:<28}): {w:3d} words | Valid: {valid}")
        if viols:
            for v in viols:
                print(f"   [VIOLATION] {v}")
    print(f"Total Deck Words: {total_words} | Average words/slide: {total_words / len(spec['slides']):.1f}")
    assert all_valid, "Word budget violations detected!"

    # 2. Visual Layout Rules Validation
    print("\n" + "=" * 70)
    print("STAGE 2: VISUAL LAYOUT DIVERSITY AUDIT")
    print("=" * 70)
    valid_layouts, l_viols = VisualPlanner.validate_layout_rules(spec["slides"])
    print(f"Layout diversity valid: {valid_layouts}")
    if l_viols:
        for v in l_viols:
            print(f"   [LAYOUT VIOLATION] {v}")
    assert valid_layouts, f"Layout diversity violations: {l_viols}"

    # 3. Render Deck via DeckRenderer
    print("\n" + "=" * 70)
    print("STAGE 3: POWERPOINT RENDERING (LEVEL B PRIMITIVES)")
    print("=" * 70)
    renderer = DeckRenderer(theme_name="lumbini")
    rendered_file = renderer.render(spec, out_pptx)
    print(f"Rendered presentation successfully: {rendered_file}")

    # 4. Strict Quality Gate Pre-Flight Audit
    print("\n" + "=" * 70)
    print("STAGE 4: PRE-FLIGHT QUALITY GATE & AUDIT REPORT")
    print("=" * 70)
    preview_dir = os.path.abspath("previews_jbvnl_10slide")
    os.makedirs(preview_dir, exist_ok=True)
    qa_report = QualityGate.audit_deck(rendered_file, spec, render_images=False, preview_dir=preview_dir)
    print(f"QA Status: {qa_report['status']}")
    print(f"Blocking Count: {qa_report['blocking_count']}")
    print(f"Warning Count:  {qa_report['warning_count']}")
    if qa_report['blocking_findings']:
        print("Blocking Findings:")
        for b in qa_report['blocking_findings']:
            print(f"   [BLOCKING] {b}")
    if qa_report['warning_findings']:
        print("Warning Findings:")
        for w in qa_report['warning_findings']:
            print(f"   [WARNING] {w}")

    qa_json_path = os.path.abspath("qa_jbvnl_10slide_report.json")
    with open(qa_json_path, "w", encoding="utf-8") as f:
        json.dump(qa_report, f, indent=2)
    print(f"QA report written to: {qa_json_path}")
