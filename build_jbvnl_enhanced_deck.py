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

def build_jbvnl_enhanced_spec() -> dict:
    theme = get_lumbini_theme()

    slides = [
        # Slide 1: Cover (Dark Navy Hero)
        {
            "slide_number": 1,
            "content_shape": "cover",
            "dark_theme": True,
            "title": "JBVNL Has SAP. Is JBVNL Getting Its Money's Worth?",
            "subtitle": "From SAP Investment to Measurable Business Performance",
            "metadata": [
                ("Prepared for", "Jharkhand Bijli Vitran Nigam Limited (JBVNL)"),
                ("Strategic Partner", "Lumbini Elite Solutions & Services"),
                ("Focus Area", "SAP Adoption, DISCOM Benchmarking & Solution Proposal"),
                ("Date of Briefing", "November 2026")
            ],
            "pill_text": "Executive Briefing  |  JBVNL 2026",
            "layout_rationale": "Dark navy executive cover establishing an authoritative financial and operational advisory tone.",
            "notes": "What Management Should Understand: JBVNL does not necessarily need another ERP investment to begin its transformation. It needs to unlock the value of the enterprise system it already has.\nWhy It Matters Financially: Capital spent on unutilized software delivers zero return while manual workarounds continue to leak operating money.\nConclusion to Draw: Management should prioritize utilizing existing SAP investments through modern mobile and web interfaces.\nQuestion to Ask: 'Why should we procure another system when we haven't unlocked the value of what we already have?'"
        },

        # Slide 2: Why SAP Is Important for JBVNL (Levels x Dimensions Matrix)
        {
            "slide_number": 2,
            "content_shape": "levels_x_dimensions",
            "eyebrow": "Enterprise Process Integration",
            "title": "One Connected Enterprise System. Better Control Across Every Department.",
            "subtitle": "Connecting core utility functions to replace spreadsheets with disciplined enterprise execution",
            "col_headers": ["Control Domain", "Manual Gaps Today", "Connected Outcome"],
            "row_headers": [
                ("Finance & Spend", "Budgets & POs", theme.C_PRIMARY),
                ("Stores & Upkeep", "Materials & Assets", theme.C_NAVY),
                ("Works & Payroll", "CWIP & Staff", theme.C_MUTED)
            ],
            "cells": [
                [
                    "Finance & Spend: Accounts, receipts, and POs.",
                    "Spreadsheet tracking, approval delays, and late reconciliation.",
                    "Real-time budget checks, digital POs, and daily bank links."
                ],
                [
                    "Stores & Upkeep: Materials, stock, and repair orders.",
                    "Paper store chits, zero visibility, and unrecorded repairs.",
                    "Digital goods receipts (MIGO), central stock, and upkeep tracking."
                ],
                [
                    "Works & Payroll: Capital budgets, CWIP, and payroll.",
                    "Offline logs, delayed capitalization, and detached records.",
                    "WBS expenditure control, prompt handover, and auditable payroll."
                ]
            ],
            "caveat_text": "Note: Scope subject to verification against JBVNL existing SAP licenses.",
            "confirmed_title": "Core Value Levers",
            "confirmed_caps": [
                "Real-Time Budgets",
                "Stock Visibility",
                "Faster Approvals",
                "Audited Trails"
            ],
            "layout_rationale": "Chosen 'levels_x_dimensions' to map 6 core business functions directly against manual pain points and enterprise outcomes.",
            "notes": "What Management Should Understand: SAP is not an IT tool for reporting; it is an operating engine to control expenditure, inventory, and revenue across circles.\nWhy It Matters Financially: Fragmented working allows budgets to be bypassed and materials to be duplicated across circle store yards.\nConclusion to Draw: Connecting departments in SAP establishes single-point accountability and stops manual leakages.\nQuestion to Ask: 'Can our finance team see circle-level purchase commitments in real time today?'"
        },

        # Slide 3: Which Indian DISCOMs Are Using SAP? (Benchmark Comparison Table)
        {
            "slide_number": 3,
            "content_shape": "benchmark_table",
            "source_id": "PFC Ratings, CAG Reports, Official DISCOM Filings & World Bank Studies",
            "eyebrow": "Indian Power Sector Benchmarking",
            "title": "Indian Power Utilities Operate Core Workflows on SAP.",
            "subtitle": "Benchmarking confirmed state and private distribution utility SAP deployments",
            "headers": ["Utility & Jurisdiction", "SAP Solution", "Verified Version", "Core Processes & Capabilities"],
            "col_widths": [2.5, 2.3, 2.7, 4.53],
            "rows": [
                [
                    "Tata Power-DDL",
                    "SAP ERP & IS-U",
                    "Public filings",
                    "Meter-to-cash, FICO, MM, PS, PM; AT&C <6.8%"
                ],
                [
                    "APSPDCL",
                    "Suite on HANA",
                    "R/3 ➔ ECC ➔ HANA",
                    "FICO, MM, PS, PM; mobile DTR tracking & e-stores"
                ],
                [
                    "TSNPDCL",
                    "SAP ERP Core",
                    "R/3 ➔ ECC 6.0",
                    "FICO, MM, PS, PM across corporate & circles"
                ],
                [
                    "TP Ajmer",
                    "ECC on HANA",
                    "HANA 2.0 DB",
                    "Meter-to-cash, web portal, eMitra & Paytm"
                ],
                [
                    "Assam APDCL",
                    "SAP Billing App",
                    "Public filings",
                    "Billing app; CAG noted parallel manual registers"
                ]
            ],
            "callout_text": "Evidence: 5+ named utilities verified; nationwide count unconfirmed. Sources: PFC, CAG, filings.",
            "layout_rationale": "Chosen 'benchmark_table' to present an executive comparison table of confirmed Indian DISCOM SAP implementations and versions.",
            "notes": "What Management Should Understand: Indian power utilities of varying scale—both state-owned and private—have run SAP for over a decade.\nWhy It Matters Financially: Utilities like Tata Power-DDL and APSPDCL proved that integrating operational workflows into SAP cuts losses and enforces control.\nConclusion to Draw: JBVNL is not an experimental case; it is adopting established national utility best practices.\nQuestion to Ask: 'If state utilities like APSPDCL and TSNPDCL can operate on SAP, why is JBVNL still operating on spreadsheets?'"
        },

        # Slide 4: How Are Other DISCOMs Using SAP with Mobile and Web Applications? (Flow with Actions)
        {
            "slide_number": 4,
            "content_shape": "flow_with_actions",
            "source_id": "Tata Power-DDL, APSPDCL, and TPADL Public Disclosures",
            "eyebrow": "Digital Ecosystem & Field Mobility",
            "title": "SAP Extends Beyond Desktops to Field Teams and Consumers.",
            "subtitle": "Lightweight mobile and web applications connect edge operations directly to SAP",
            "flow_boxes": [
                ("Tata Power-DDL", "Consumer portal, spot billing, GIS & OMS", theme.C_PRIMARY),
                ("APSPDCL", "DTR mobile GPS tracking, photos & e-stores", theme.C_PRIMARY),
                ("TP Ajmer", "Customer portal, Paytm, eMitra & call centre", theme.C_NAVY)
            ],
            "actions": [
                "Consumers (Portal/App): Instant billing, payment gateways, and alerts.",
                "Field Engineers (Mobile): Transformer GPS tracking and repair sign-off.",
                "Store Keepers (Web): Central stock queries, paperless indents, and MIGO.",
                "Leadership (Cockpit): Daily revenue realization and bank reconciliation."
            ],
            "legend_items": [
                (theme.C_PRIMARY, "Field & Consumer Apps"),
                (theme.C_NAVY, "Commercial & Management Portals")
            ],
            "caveat_text": "Architecture: Mobile/web apps connect to SAP via standard APIs without altering core ERP.",
            "layout_rationale": "Chosen 'flow_with_actions' to show how DISCOMs connect consumers, field teams, stores, and leadership to SAP via mobile/web apps.",
            "notes": "What Management Should Understand: SAP does not force engineers to sit at desktop computers; lightweight mobile apps bring SAP to the field.\nWhy It Matters Financially: Mobile apps capture transformer failures and meter data instantly, eliminating clerical re-entry delays and paperwork losses.\nConclusion to Draw: Lumbini can deploy mobile and web applications on top of JBVNL's existing SAP system.\nQuestion to Ask: 'Can we give our field engineers mobile apps to track transformer replacements and store requests in SAP?'"
        },

        # Slide 5: Where Manual Processes Create Financial Exposure (Levels x Dimensions Matrix)
        {
            "slide_number": 5,
            "content_shape": "levels_x_dimensions",
            "eyebrow": "Operational Loss Diagnostics",
            "title": "Manual Workarounds Create Immediate Financial Exposure.",
            "subtitle": "Six priority operational leakage points where offline processes trap utility cash flow",
            "col_headers": ["Focus Area", "Manual Paperwork Gaps", "Balance Sheet Exposure"],
            "row_headers": [
                ("Meter-to-Cash", "Billing & Arrears", theme.C_NAVY),
                ("Supply Chain & CWIP", "Procurement & Works", theme.C_PRIMARY),
                ("Stores & Assets", "Inventory & Upkeep", theme.C_MUTED)
            ],
            "cells": [
                [
                    "Billing & Arrears: Delayed billing and unlinked receipts.",
                    "Depressed cash flow, arrears (>₹6,000 Cr), and interest cost.",
                    "Meter-to-cash tracking and daily reconciliation."
                ],
                [
                    "Procurement & CWIP: Offline approvals and late capitalization.",
                    "Purchase price variance and tariff pass-through disallowances.",
                    "Digital PO tracking and milestone asset capitalization."
                ],
                [
                    "Stores & Upkeep: Paper store chits and unrecorded repairs.",
                    "Locked working capital, duplicate buying, and asset burnouts.",
                    "Central stock balancing and scheduled maintenance logs."
                ]
            ],
            "caveat_text": "Baseline diagnostic focus areas to be verified during assessment.",
            "confirmed_title": "Target Diagnostic Levers",
            "confirmed_caps": [
                "Cash Collection",
                "Spend Governance",
                "Working Capital",
                "CWIP Capitalization"
            ],
            "layout_rationale": "Chosen 'levels_x_dimensions' to map the 6 operational loss areas directly across financial consequences and baseline focus.",
            "notes": "What Management Should Understand: Financial losses originate in daily field handovers, not in the accounting books.\nWhy It Matters Financially: When paperwork is slow, money gets trapped in arrears, idle stores, and uncapitalized projects.\nConclusion to Draw: A comprehensive baseline diagnostic will identify JBVNL's exact operational leakage points.\nQuestion to Ask: 'How much working capital is locked in circle stores because adjacent circles cannot see each other's stock?'"
        },

        # Slide 6: What Can SAP Improve in JBVNL's Day-to-Day Operations? (Requirement to Outcome)
        {
            "slide_number": 6,
            "content_shape": "requirement_to_outcome",
            "eyebrow": "Operational Workflows: Before vs. After",
            "title": "Standardizing Day-to-Day Operations Through Governed Workflows.",
            "subtitle": "Transforming disconnected manual tasks into auditable digital SAP transactions",
            "headers": ["Operational Stream", "Manual Working Today", "Target SAP-Driven Workflow"],
            "items": [
                {
                    "requirement": "Procurement",
                    "today": "Email ➔ Phone follow-up ➔ Manual register.",
                    "outcome": "Requisition ➔ Approval ➔ PO ➔ MIGO ➔ MIRO ➔ FI posting.",
                    "badge_color": theme.C_PRIMARY
                },
                {
                    "requirement": "Maintenance",
                    "today": "Fault call ➔ Paper chit ➔ Offline repair.",
                    "outcome": "Notification ➔ Work order ➔ Stock reservation ➔ Cost posting ➔ TECO.",
                    "badge_color": theme.C_NAVY
                },
                {
                    "requirement": "Inventory",
                    "today": "Manual bin card ➔ Phone check ➔ Paper issue.",
                    "outcome": "Material Master ➔ Digital MIGO ➔ Stock transfer ➔ Issue (261).",
                    "badge_color": theme.C_ACCENT
                },
                {
                    "requirement": "Projects",
                    "today": "Spreadsheet budget ➔ Delayed expense entry.",
                    "outcome": "WBS budget check ➔ Cost booking ➔ Asset capitalization.",
                    "badge_color": theme.C_MUTED
                }
            ],
            "caveat_text": "Workflows mapped to standard SAP best-practice utility modules.",
            "layout_rationale": "Chosen 'requirement_to_outcome' 4-row comparative layout contrasting manual workflows today with target SAP workflows.",
            "notes": "What Management Should Understand: SAP is not extra paperwork; it streamlines everyday tasks by removing repeated manual entries and phone follow-ups.\nWhy It Matters Financially: Digital workflows ensure that every expense has an approved budget and every material issue has an auditable reservation.\nConclusion to Draw: Standardized SAP workflows save hundreds of engineering hours while establishing financial discipline.\nQuestion to Ask: 'Why should our engineers waste days tracking files when SAP can route approvals automatically?'"
        },

        # Slide 7: What Solution Can Lumbini Propose to JBVNL? (Layered Architecture Stack)
        {
            "slide_number": 7,
            "content_shape": "layered_stack",
            "eyebrow": "Lumbini Solution Architecture",
            "title": "A Pragmatic 5-Layer Solution Connecting SAP Across JBVNL.",
            "subtitle": "Extending existing SAP with user-friendly web and mobile interfaces",
            "layers": [
                {
                    "tier": "Layer 1: Users",
                    "title": "Operational Personas",
                    "desc": "Leadership · Finance · Stores · Field Engineers",
                    "color": theme.C_NAVY
                },
                {
                    "tier": "Layer 2: Apps",
                    "title": "Mobile & Web Applications",
                    "desc": "Field app · Stock indenting · Purchase approvals · Executive dashboard",
                    "color": theme.C_PRIMARY
                },
                {
                    "tier": "Layer 3: Integration",
                    "title": "Integration Layer",
                    "desc": "REST/OData APIs · SAP Gateway · Validation rules",
                    "color": theme.C_PRIMARY
                },
                {
                    "tier": "Layer 4: Core ERP",
                    "title": "Existing SAP Environment",
                    "desc": "Core ERP (FICO, MM, PM, PS, HCM) · Database · Audit logs",
                    "color": theme.C_NAVY
                },
                {
                    "tier": "Layer 5: Insights",
                    "title": "Executive Cockpits",
                    "desc": "Real-time revenue, inventory, and capex KPIs",
                    "color": theme.C_MUTED
                }
            ],
            "callout_note": "Architecture Principle:\nEnhance existing SAP without costly replacements.\n\nLightweight apps connect field teams to core ERP via secure APIs.",
            "layout_rationale": "Chosen 'layered_stack' to present Lumbini's 5-layer solution architecture connecting users, apps, integration, SAP, and BI.",
            "notes": "What Management Should Understand: Lumbini is not selling new ERP software; we propose connecting your existing SAP to the people who run JBVNL through mobile apps and dashboards.\nWhy It Matters Financially: Layering lightweight apps on existing SAP avoids multimillion-rupee re-implementation costs while delivering immediate operational adoption.\nConclusion to Draw: Lumbini provides the end-to-end partner capability to assess, configure, integrate, and support this architecture.\nQuestion to Ask: 'Does this 5-layer approach give us the field connectivity we need without disrupting our core system?'"
        },

        # Slide 8: What Financial Value Can JBVNL Realize? (Tradeoff Matrix / Financial Value Bridge)
        {
            "slide_number": 8,
            "content_shape": "tradeoff_matrix",
            "source_id": "Illustrative Financial Sensitivity Model (JBVNL FY24 Baseline)",
            "eyebrow": "Financial Impact & Balance Sheet Realization",
            "title": "Better Operational Discipline Generates Substantial Financial Returns.",
            "subtitle": "Translating daily process compliance into measurable balance sheet and cash gains",
            "x_axis_title": "Operational Process Maturity (Manual ➔ Governed SAP)",
            "y_axis_title": "Balance Sheet Impact (Deficit ➔ Cash Flow)",
            "quadrants": [
                {
                    "name": "Billing & Collection Velocity",
                    "desc": "Closing billing delays directly accelerates cash into operating EBITDA."
                },
                {
                    "name": "Procurement Spend Control",
                    "desc": "Enforcing PO approvals cuts off-contract purchase variances by 8–12%."
                },
                {
                    "name": "Inventory Rationalization",
                    "desc": "Cross-circle stock visibility releases ₹45–60 Cr in locked working capital."
                },
                {
                    "name": "Capex Tariff Recovery",
                    "desc": "Prompt CWIP capitalization prevents regulatory tariff disallowances."
                }
            ],
            "callout_note": "Financial Sensitivities (JBVNL Base):\n• +1% Collection: ₹65–70 Cr cash recovered annually.\n• 15-Day Inventory Cut: ₹45–60 Cr working capital unlocked.\n• Timely CWIP Closure: ₹50+ Cr tariff disallowances prevented.",
            "layout_rationale": "Chosen 'tradeoff_matrix' 2x2 decision space to map operational transformation maturity directly against balance sheet realization levers.",
            "notes": "What Management Should Understand: In a utility with over ₹6,500 Cr in revenue, a single percentage point improvement generates ₹65+ Cr in hard cash.\nWhy It Matters Financially: Small process improvements generate substantial cash inflows that reduce expensive short-term borrowings.\nConclusion to Draw: Process optimization pays for itself many times over through working capital release and loss reduction.\nQuestion to Ask: 'Can we afford to leave ₹65–70 Cr on the table every year just because our collection reconciliation is delayed?'"
        },

        # Slide 9: How Do We Start? A 90-Day JBVNL Improvement Program (Roadmap Rows)
        {
            "slide_number": 9,
            "content_shape": "phases_over_time",
            "eyebrow": "Pragmatic Implementation Roadmap",
            "title": "A Disciplined 90-Day Sprint to Demonstrate Measurable Value.",
            "subtitle": "Phased implementation delivering early operational wins before broad rollout",
            "phases": [
                ("Days 1–30: Assessment", "Weeks 1–4 · Review SAP usage, processes, apps, data gaps, and baseline KPIs"),
                ("Days 31–60: Priority Improvements", "Weeks 5–8 · Clean master data, standardize approvals, configure pilot apps, train users"),
                ("Days 61–90: Pilot & Measurement", "Weeks 9–12 · Run pilot workflows, track compliance, demo mobile apps, present results")
            ],
            "future_readiness_title": "Pilot Deliverables",
            "future_readiness_desc": "Deliverables: SAP utilization audit · Process blueprint · API integration design · Priority pilot workflows · KPI scorecard.",
            "layout_rationale": "Chosen 'phases_over_time' 3-stage sequential timeline detailing the 90-day execution roadmap.",
            "notes": "What Management Should Understand: We are not proposing a multi-year disruption; we propose a structured 90-day pilot focused on high-impact areas.\nWhy It Matters Financially: A phased approach delivers measurable quick wins in 90 days without requiring capital investments in new software.\nConclusion to Draw: Starting with procurement and stores provides immediate expenditure control and working capital recovery.\nQuestion to Ask: 'Are we ready to pilot disciplined SAP usage in one or two circles over the next 90 days to prove the financial benefit?'"
        },

        # Slide 10: The Management Decision (Dark Hero Finale)
        {
            "slide_number": 10,
            "content_shape": "closing",
            "title": "JBVNL Already Has the Foundation. Let Us Help Unlock Its Value.",
            "subtitle": "Five decisive executive actions to transition from manual workarounds to governed enterprise operations",
            "core_message": "JBVNL does not need another ERP investment to begin its transformation. It needs to unlock the value of the enterprise system it already has.",
            "pillars": [
                ("Approve SAP Assessment", "Authorize a diagnostic team to inspect current transaction usage, approval logs, and system data."),
                ("Nominate Departmental Owners", "Designate accountable officers across Finance, Stores, Procurement, Projects, and Field Circles."),
                ("Provide System Access", "Authorize access to SAP configuration, database tables, and existing interface documentation."),
                ("Select Priority Processes", "Approve Procurement and Stores workflows for initial pilot implementation in selected circles."),
                ("Authorize Phased Initiative", "Establish 90-day pilot with fortnightly milestone reviews and quantifiable financial KPI targets.")
            ],
            "concluding_statement": "Every transaction accounted for. Every rupee tracked. Every process accountable.",
            "pill_text": "Lumbini Elite Solutions  |  Partner in Enterprise Value Realization",
            "layout_rationale": "Dark navy executive finale synthesizing required management decisions and delivering the decisive closing mandate.",
            "notes": "What Management Should Understand: The technology is in place; turning it into financial results requires five clear management decisions today.\nWhy It Matters Financially: Every month of delay preserves manual workarounds, unreconciled accounts, and commercial leakage.\nConclusion to Draw: Management should approve the diagnostic and the 90-day pilot initiative immediately.\nQuestion to Ask: 'Can we agree today to nominate our departmental owners and approve the 90-day pilot so we can start seeing results?'"
        }
    ]

    return {
        "theme": "lumbini",
        "client": "JBVNL",
        "meta": {
            "client": "JBVNL",
            "topic": "SAP Adoption, DISCOM Benchmarking & Solution Proposal",
            "confidentiality": "Executive Briefing",
            "doc_type": "Management Presentation"
        },
        "sections": [
            ("Business Justification & Need", 2),
            ("Indian DISCOM Benchmarks & Mobility", 2),
            ("Operational Diagnostics & Workflows", 2),
            ("Solution Proposal & Financial Value", 2),
            ("Action Plan & Management Decision", 2)
        ],
        "slides": slides
    }

if __name__ == "__main__":
    primary_out = os.path.abspath("JBVNL_Management_Presentation_Enhanced.pptx")
    fallback_out = os.path.abspath("JBVNL_Management_Presentation_Enhanced_Fixed.pptx")
    out_pptx = primary_out
    try:
        with open(primary_out, "a+b"): pass
    except Exception:
        print(f"[INFO] {primary_out} is locked by an open PowerPoint instance. Writing to {fallback_out}")
        out_pptx = fallback_out
    spec = build_jbvnl_enhanced_spec()

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
    preview_dir = os.path.abspath("previews_jbvnl_enhanced")
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

    qa_json_path = os.path.abspath("qa_jbvnl_enhanced_report.json")
    with open(qa_json_path, "w", encoding="utf-8") as f:
        json.dump(qa_report, f, indent=2)
    print(f"QA report written to: {qa_json_path}")
