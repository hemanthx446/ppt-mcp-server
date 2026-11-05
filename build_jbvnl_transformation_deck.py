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

def build_jbvnl_spec() -> dict:
    theme = get_lumbini_theme()

    slides = [
        # Slide 1: Title & Strategic Positioning (Dark Hero Canvas)
        {
            "slide_number": 1,
            "content_shape": "cover",
            "dark_theme": True,
            "title": "Unlocking JBVNL's Enterprise Potential",
            "subtitle": "From SAP Implementation to Business Intelligence, Governance and Autonomous Operations",
            "metadata": [
                ("Prepared for", "Jharkhand Bijli Vitran Nigam Limited (JBVNL)"),
                ("Strategic Advisor", "Lumbini Elite Solutions & Services"),
                ("Focus Area", "Enterprise Architecture & SAP Value Realization"),
                ("Proposal Date", "November 2026")
            ],
            "pill_text": "Executive Briefing  |  JBVNL Strategy",
            "layout_rationale": "Dark navy executive cover setting an authoritative strategic consulting tone.",
            "notes": "Executive briefing prepared for the Board of Directors, Managing Director, and senior leadership of Jharkhand Bijli Vitran Nigam Limited (JBVNL). Establishes the business case for closing the gap between capital technology investment in SAP and day-to-day organizational adoption."
        },

        # Slide 2: The JBVNL Reality Check (Comparative Rows)
        {
            "slide_number": 2,
            "content_shape": "requirement_to_outcome",
            "eyebrow": "Current Operating Challenge",
            "title": "Having SAP and operating through SAP are two different things",
            "subtitle": "Closing the gap between technology investment and day-to-day organizational adoption",
            "headers": ["Operational Dimension", "Traditional Operating Environment", "Connected Enterprise Outcome"],
            "items": [
                {
                    "requirement": "Transaction Execution",
                    "today": "Manual registers and repeated spreadsheet entries; reported utilization remains below potential.",
                    "outcome": "Single digital entry directly in SAP, establishing enforceable transaction integrity and ownership.",
                    "badge_color": theme.C_PRIMARY
                },
                {
                    "requirement": "Approvals & Governance",
                    "today": "Offline notes and email approvals bypass controls, obscuring accountability and decision trails.",
                    "outcome": "Standardized multi-level digital workflows in SAP, providing verifiable and auditable approval trails.",
                    "badge_color": theme.C_NAVY
                },
                {
                    "requirement": "Operational Visibility",
                    "today": "Departmental silos reconciled weeks late; leadership lacks unified operational visibility.",
                    "outcome": "One integrated view connecting metering, billing, inventory, and finance in real time.",
                    "badge_color": theme.C_ACCENT
                },
                {
                    "requirement": "Management Decisions",
                    "today": "Management relies on lagging spreadsheet extracts with conflicting operational figures.",
                    "outcome": "Real-time exception cockpits delivering decision-ready intelligence and circle accountability.",
                    "badge_color": theme.C_MUTED
                }
            ],
            "layout_rationale": "Chosen 'requirement_to_outcome' 4-row comparative structure to sharply contrast current manual bottlenecks with target enterprise outcomes.",
            "notes": "Highlights the central paradox: JBVNL has invested in SAP, yet operations continue in parallel offline registers. Crucially, notes that reported sub-10% adoption is a working hypothesis, not an audited fact. Emphasizes that this gap stems from process design, workflow adoption, and governance, not employee limitation."
        },

        # Slide 3: The Hidden Cost of Parallel Processes (Constraint Flow)
        {
            "slide_number": 3,
            "content_shape": "constraint_flow",
            "eyebrow": "Process Vulnerability Analysis",
            "title": "Every manual workaround creates an additional business risk",
            "subtitle": "How offline registers and parallel spreadsheets compromise auditability, working capital, and speed",
            "stages": [
                {
                    "name": "Procurement & Indenting",
                    "desc": "Material indents tracked in spreadsheets; rate contracts and budget limits bypassed.",
                    "rate": "14-21 Day Cycle"
                },
                {
                    "name": "Inventory & Issue",
                    "desc": "Transformers and cables issued on paper chits without real-time SAP reservation.",
                    "rate": "Binding Bottleneck"
                },
                {
                    "name": "Asset Maintenance",
                    "desc": "Breakdowns logged in paper logs; repair costs disconnected from plant maintenance history.",
                    "rate": "Unvouched Capex"
                },
                {
                    "name": "Financial Settlement",
                    "desc": "Vendor invoices manually matched against physical files, creating reconciliation delays.",
                    "rate": "Cash Lockup"
                }
            ],
            "constraint_idx": 1,
            "buffer_desc": "Paper chits and manual store registers sever audit trails, masking stockouts and prompting spot buys.",
            "impact_annotation": "Operational Consequence: Disconnected parallel workflows generate unreconciled liabilities, tariff true-up delays, and cash lockup.",
            "layout_rationale": "Chosen 'constraint_flow' to pinpoint how offline store issues form a binding operational bottleneck that cascades into financial deficits.",
            "notes": "Illustrates how disconnected workflows across procurement, inventory, maintenance, and finance multiply operational risk. Every spreadsheet workaround destroys transaction integrity, prevents real-time budget control, and exposes the utility to regulatory disallowance."
        },

        # Slide 4: Metadata vs. Business Context (Two-Column Comparison)
        {
            "slide_number": 4,
            "content_shape": "metadata_vs_context",
            "eyebrow": "Enterprise Conceptual Framework",
            "title": "Data describes the enterprise; context helps manage it",
            "subtitle": "Connecting system records with operational rules, relationships, and financial accountability",
            "metadata_items": [
                ("Consumer Master", "Tariff slab, sanctioned load, meter number."),
                ("Asset Master", "100 kVA rating, GIS coordinates, feeder."),
                ("Material Master", "11kV cable code, bin location, unit cost."),
                ("Vendor Master", "PO terms, milestone schedule, GSTIN.")
            ],
            "context_items": [
                ("Revenue Protection", "Does billed energy match feeder export?"),
                ("Asset Health", "Is oil temperature rising? Outage risk?"),
                ("Budget Control", "Is requisition within approved circle capex?"),
                ("Action Trigger", "Who is accountable? What action follows?")
            ],
            "example_box": {
                "title": "DTR Operational Case (Illustrative)",
                "metadata_text": "100kVA DTR #4029, Kanke Feeder.",
                "context_text": "88% peak load. Overhaul avoids ₹4.5L opex."
            },
            "layout_rationale": "Chosen 'metadata_vs_context' 2-column comparative layout with bottom practical DTR case strip to establish the core intellectual premise.",
            "notes": "Establishes the foundational intellectual framework of the presentation. Explains that collecting more data or deploying AI models without context fails because raw data only describes what exists. Value emerges when data is connected to business rules, accountability, and financial consequences."
        },

        # Slide 5: The Meter-to-Cash Value Chain (Step-Line Pipeline)
        {
            "slide_number": 5,
            "content_shape": "step_line",
            "eyebrow": "Commercial Value Stream",
            "title": "Revenue realization begins long before payment collection",
            "subtitle": "End-to-end integration across metering, billing, and accounting closes commercial revenue leakages",
            "steps": [
                ("Consumer Onboarding", "KYC verification, load sanction, GPS feeder indexing, and master setup."),
                ("Meter Installation", "Physical meter pairing, seal logging, and test reading synchronization."),
                ("Meter Reading & HES", "Automated AMR/AMI polling, optical scan capture, and boundary energy accounting."),
                ("Billing & Tariff Engine", "Slab tariff calculation, rebate/surcharge processing, and bill generation."),
                ("Collection & Cash Flow", "Multi-channel payment gateway realization, RTGS, and direct consumer deposits."),
                ("Reconciliation & Ledger", "Daily bank reconciliation, ledger matching, aging analysis, and disconnection triggers.")
            ],
            "deliverables": [
                "Gap: Unindexed consumers",
                "Gap: Defective / bypassed meters",
                "Gap: Unmetered estimated billing",
                "Gap: Delayed bill dispatch",
                "Gap: Unreconciled bank deposits",
                "Gap: Unenforced arrears recovery"
            ],
            "caveat_text": "System Integration: SAP IS-U / ERP provides the commercial and financial backbone; it integrates with specialized MDMS, HES, AMR, and GIS.",
            "layout_rationale": "Chosen 'step_line' 6-step sequential pipeline with aligned operational leakage risks directly mapped below each commercial stage.",
            "notes": "Maps the 6-stage Meter-to-Cash value chain. Proves that revenue leakage is not just an issue of collection drives; it starts with unindexed meters, delayed readings, and disconnected ledgers. Explains the critical distinction between specialized OT systems and the ERP financial backbone."
        },

        # Slide 6: Where Business Value Leaks (Levels x Dimensions Matrix)
        {
            "slide_number": 6,
            "content_shape": "levels_x_dimensions",
            "source_id": "PFC Integrated Rating Report (FY23/24)",
            "eyebrow": "Value Leakage Diagnostics",
            "title": "Operational gaps eventually become financial balance sheet deficits",
            "subtitle": "How unaligned workflows compound into commercial losses, cash lockup, and disallowances",
            "col_headers": ["Operational Process Gaps", "Balance Sheet Consequences", "Measurable DISCOM KPIs"],
            "row_headers": [
                ("Commercial Operations", "Metering & Collections", theme.C_NAVY),
                ("Supply Chain & Capex", "Stores & Schemes", theme.C_PRIMARY),
                ("Asset Maintenance", "Substation & Feeder O&M", theme.C_MUTED)
            ],
            "cells": [
                [
                    "Billing delays, estimates, unlinked receipts.",
                    "Depressed cash flow, higher arrears, elevated debt.",
                    "AT&C: 30.28% | Billing: 93.85% | Collection: 95.46% (PFC FY23)."
                ],
                [
                    "Spot buys, unrecorded issues, slow capitalization.",
                    "Trapped store capital, stockouts, idle CWIP.",
                    "Inventory holding >120 days | Idle CWIP | Rate variance."
                ],
                [
                    "Reactive repairs, offline logs, unmonitored assets.",
                    "DTR burnouts, high repair costs, unserved energy.",
                    "DTR failure >10% | High O&M cost | Elevated SAIFI."
                ]
            ],
            "caveat_text": "Source: PFC Report FY23/24: JBVNL AT&C loss was 30.28% (Rank 52) vs national RDSS target 12-15%.",
            "confirmed_title": "Core Strategic Value Levers",
            "confirmed_caps": [
                "AT&C Loss Reduction",
                "Billing Cycle Speed",
                "Working Capital Release",
                "CWIP Capitalization"
            ],
            "layout_rationale": "Chosen 'levels_x_dimensions' matrix to systematically demonstrate how operational deficiencies across 3 streams convert directly into financial metrics.",
            "notes": "Directly connects operational flaws to financial balance sheet distress. Categorizes losses into technical dissipation, commercial theft/underbilling, and administrative/process inefficiency. Demonstrates that JBVNL's 30.28% AT&C loss is heavily driven by process leakages that SAP was designed to eliminate."
        },

        # Slide 7: Why SAP Matters (Hub and Spokes Core Architecture)
        {
            "slide_number": 7,
            "content_shape": "hub_and_spokes",
            "eyebrow": "Enterprise Backbone Architecture",
            "title": "SAP is an enterprise process backbone, not a transaction ledger",
            "subtitle": "Orchestrating cross-functional workflows so a single operational event updates the entire organization",
            "hub_title": "Unified SAP Backbone",
            "hub_subtitle": "Single Source of Truth",
            "spokes": [
                {"letter": "A", "title": "Finance & Controlling (FICO)", "desc": "Real-time cost centre accounting, budget availability control, general ledger integrity, and financial transparency."},
                {"letter": "B", "title": "Materials Management (MM)", "desc": "Centralized procurement, automated inventory reorder points, three-way invoice matching, and stores governance."},
                {"letter": "C", "title": "Plant Maintenance (PM)", "desc": "Asset master tracking, scheduled preventive maintenance work orders, breakdown root-cause analysis, and equipment history."},
                {"letter": "D", "title": "Project Systems (PS)", "desc": "Capital electrification scheme tracking, milestone-based contractor billing, CWIP capitalization, and grant auditability."}
            ],
            "layout_rationale": "Chosen 'hub_and_spokes' to show the central enterprise core unifying Finance, Procurement, Plant Maintenance, and Capital Projects.",
            "notes": "Explains the functional core of SAP (FICO, MM, PM, PS, SD, HCM). Uses a practical discom example: a DTR breakdown triggers a PM notification, which auto-reserves material in MM, logs labour in HCM, posts costs in FICO, and capitalizes assets in PS—eliminating multi-department spreadsheet reconciliation. Notes that specific active modules at JBVNL will be confirmed during discovery."
        },

        # Slide 8: Connecting the Enterprise (6-Tier Layered Stack)
        {
            "slide_number": 8,
            "content_shape": "layered_stack",
            "eyebrow": "Target Operating Topology",
            "title": "From departmental silos to one unified enterprise architecture",
            "subtitle": "Positioning SAP as the transactional backbone connecting field operational systems to executive intelligence",
            "layers": [
                {
                    "tier": "Tier 6: Executive Governance",
                    "title": "Management Cockpits & Regulatory Reporting",
                    "desc": "Board decision cockpits, JSERC petitions, and circle accountability.",
                    "color": theme.C_NAVY
                },
                {
                    "tier": "Tier 5: Business Intelligence",
                    "title": "Enterprise BI & Cross-Functional Analytics",
                    "desc": "Feeder energy audits, consumer aging analysis, and loss heatmaps.",
                    "color": theme.C_PRIMARY
                },
                {
                    "tier": "Tier 4: Enterprise Integration",
                    "title": "Integration & Master Data Management",
                    "desc": "Clean master data, automated interfaces, and IT/OT data connectors.",
                    "color": theme.C_PRIMARY
                },
                {
                    "tier": "Tier 3: Enterprise Backbone",
                    "title": "SAP ERP Core (FICO, MM, PM, PS, HCM)",
                    "desc": "System of record enforcing business rules, budget checks, and accounting.",
                    "color": theme.C_PRIMARY
                },
                {
                    "tier": "Tier 2: Operational Systems",
                    "title": "Operational Systems (OT Landscape)",
                    "desc": "MDMS, Smart Meter HES, GIS network mapping, and SCADA telemetry.",
                    "color": theme.C_MUTED
                },
                {
                    "tier": "Tier 1: Physical Infrastructure",
                    "title": "Grid Infrastructure & Endpoints",
                    "desc": "Substations, distribution transformers, smart meters, and line networks.",
                    "color": theme.C_MUTED
                }
            ],
            "callout_note": "Integration Rule: SAP does not replace OT systems. It unifies them into one financial backbone.",
            "layout_rationale": "Chosen 'layered_stack' 6-tier architectural hierarchy bridging physical electrical assets up to executive governance cockpits.",
            "notes": "Presents the comprehensive 6-layer enterprise architecture. Resolves the critical consulting question: SAP is not an island, nor is it a replacement for SCADA or smart meters; it is the transactional orchestrator that links technical operations to balance sheet realization."
        },

        # Slide 9: Indian DISCOM Case Study: Tata Power-DDL (Iceberg Shift)
        {
            "slide_number": 9,
            "content_shape": "iceberg_shift",
            "source_id": "World Bank & TPDDL Case Study (2002-2023)",
            "eyebrow": "Transformation Benchmark",
            "title": "Integrated business processes can transform utility operations",
            "subtitle": "How North Delhi's distribution utility engineered a benchmark turnaround through IT/OT convergence and process discipline",
            "visible_event": {
                "title": "Historic AT&C Loss Reduction (Tata Power-DDL)",
                "desc": "AT&C losses slashed from 53.1% (July 2002) to <6.8% (FY23), with >99.5% collection efficiency."
            },
            "submerged_layers": [
                {
                    "layer_name": "IT/OT Convergence Architecture",
                    "finding": "Integrated SAP IS-U with GIS mapping, SCADA, and AMR into a single operational fabric."
                },
                {
                    "layer_name": "Process Re-engineering",
                    "finding": "Eliminated manual registers; mandated all meter issues and maintenance actions execute in SAP."
                },
                {
                    "layer_name": "Governance & Accountability",
                    "finding": "Tied circle performance and engineer incentives directly to feeder loss reduction."
                }
            ],
            "callout_text": "Source: World Bank Case Study: Technology deployment was merely an enabler. The driver was process redesign, system adoption, and cultural accountability.",
            "layout_rationale": "Chosen 'iceberg_shift' to contrast visible loss reduction achievements with deep operational and architectural changes below the waterline.",
            "notes": "Examines the transformation of Tata Power-DDL (TPDDL). Emphasizes that when TPDDL took over DVB in 2002, losses were 53.1%. The turnaround was achieved by integrating SAP ERP/IS-U with field GIS, SCADA, and AMR, enforcing single-system entry, and holding circle managers accountable. Cites World Bank published documentation."
        },

        # Slide 10: Indian Utility Experiences & Sector Turnaround (Annotated Chart)
        {
            "slide_number": 10,
            "content_shape": "annotated_chart",
            "eyebrow": "Sector Empirical Evidence",
            "title": "The Indian power distribution sector is executing a measurable financial pivot",
            "subtitle": "National financial turnaround proves that operational governance and digital discipline convert losses into operating profit",
            "chart_type": "column",
            "categories": ["FY21 Base", "FY22 Actual", "FY23 Actual", "FY24 Actual", "FY25 Benchmark"],
            "series_data": [
                {"name": "DISCOM Aggregate Net Profit / Loss", "values": [-50281.0, -31025.0, -28200.0, -25553.0, 2701.0]}
            ],
            "chart_title": "All-India DISCOMs Aggregate Net Profit / Loss (₹ Crore)",
            "x_label": "Financial Year",
            "y_label": "Net Profit / Loss (₹ Cr)",
            "key_takeaway": "All-India DISCOMs achieved a historic aggregate turnaround from a net loss of ₹25,553 Cr in FY24 to a net profit of ₹2,701 Cr in FY25 (MoP / PFC Official Data), driven by RDSS discipline and loss reduction.",
            "callout_annotation": "State Utility Evidence: Goa Electricity Dept achieved rapid 6-month SAP IS-U go-live across 600k consumers with TPDDL/Fujitsu; conversely, Assam APDCL's CAG Performance Audit proved that deploying SAP without adequate training and migration controls leads to unverified manual billing and unrecovered arrears.",
            "source_id": "Source: PFC Utility Report (FY24) · MoP PIB (FY25) · CAG Assam SPSE Audit",
            "layout_rationale": "Chosen 'annotated_chart' to display quantitative national turnaround trajectory paired with an executive dual-utility case analysis panel.",
            "notes": "Combines quantitative national turnaround data with two qualitative case studies. Goa ED proves that rapid implementation with utility-specific processes is feasible; Assam APDCL serves as a vital counterexample showing that technology without training and governance leads to parallel manual records. Sector-wide turnaround reflects multiple reforms, not SAP alone."
        },

        # Slide 11: Connecting Process Performance to Financial Outcomes (Tradeoff Matrix)
        {
            "slide_number": 11,
            "content_shape": "tradeoff_matrix",
            "eyebrow": "Financial Value Realization",
            "title": "Better process control creates the conditions for financial turnaround",
            "subtitle": "How operational discipline across JBVNL's core workflows directly influences EBITDA, working capital, and debt servicing",
            "x_axis_title": "Operational Process Maturity (Manual Spreadsheets ➔ Governed SAP Workflows)",
            "y_axis_title": "Financial Balance Sheet Impact (Operating Deficit ➔ Sustainable EBITDA)",
            "quadrants": [
                {
                    "name": "Revenue Protection & Loss Reduction",
                    "desc": "Closing energy accounting gaps directly expands billed sales, adding ₹300–600 Cr in gross margin into Operating EBITDA."
                },
                {
                    "name": "Cash Flow Velocity & Working Capital",
                    "desc": "Accelerating meter-to-cash cycles compresses DSO, releasing ₹150–250 Cr tied-up cash and lowering short-term debt borrowings."
                },
                {
                    "name": "Supply Chain & O&M Discipline",
                    "desc": "Consolidated rate contracts and inventory reorder controls prevent emergency spot purchases, cutting carrying costs by 15–20%."
                },
                {
                    "name": "Capital Efficiency & Tariff Recovery",
                    "desc": "Timely CWIP capitalization into Fixed Assets ensures full capex admissibility during JSERC true-up petitions, safeguarding RoE."
                }
            ],
            "callout_note": "Regulatory Bridge (Illustrative Scenario): SAP provides transaction integrity and audit trails required for regulatory pass-through, converting operational losses into recoverable assets.",
            "layout_rationale": "Chosen 'tradeoff_matrix' 2x2 decision space to map operational transformation maturity directly against balance sheet realization levers.",
            "notes": "Details the exact business value chain: Process discipline -> Transaction integrity -> Operational control -> Revenue protection -> PAT, EBITDA, and debt-servicing capacity. Includes clear disclaimer that financial scenarios are illustrative potential outcomes, not contractually guaranteed figures."
        },

        # Slide 12: From Data to Enterprise Intelligence (Maturity Staircase)
        {
            "slide_number": 12,
            "content_shape": "capability_maturity_staircase",
            "eyebrow": "Enterprise Maturity Model",
            "title": "The next advantage is not more data, but richer business context",
            "subtitle": "Ascending the capability curve from raw meter readings to context-aware operational decisions",
            "steps": [
                {
                    "level_name": "Capture",
                    "role_title": "Raw Data Ingestion",
                    "competencies": ["Smart meter AMR", "Substation SCADA logs", "Store receipt records"],
                    "gate_criterion": "Automated ingestion"
                },
                {
                    "level_name": "Record",
                    "role_title": "Transaction Discipline",
                    "competencies": ["Direct SAP postings", "Standard workflows", "Standard master data"],
                    "gate_criterion": "Register elimination"
                },
                {
                    "level_name": "Integrate",
                    "role_title": "Process Convergence",
                    "competencies": ["PM linked to MM", "PS auto-capitalization", "FICO budget control"],
                    "gate_criterion": "Zero offline reconciliations"
                },
                {
                    "level_name": "Intelligence",
                    "role_title": "Contextual Operations",
                    "competencies": ["Feeder energy audits", "Predictive DTR health", "Revenue risk alerts"],
                    "gate_criterion": "Context-aware action"
                }
            ],
            "caveat_text": "Feeder Diagnostic (Illustrative Case): Raw data flags 14% drop; Metadata flags Feeder Kanke; Context directs field inspection.",
            "layout_rationale": "Chosen 'capability_maturity_staircase' to depict ascending capability stages with discrete competencies and stage-gate criteria.",
            "notes": "Explains the 5-stage progression (Capture -> Record -> Integrate -> Intelligence -> Contextual Action). Uses the feeder anomaly case: raw data only reveals an energy drop; metadata identifies the feeder; business context synthesizes weather, billing, and commercial mix to prescribe immediate intervention."
        },

        # Slide 13: Preparing JBVNL for AI & Autonomous Operations (Flow with Actions)
        {
            "slide_number": 13,
            "content_shape": "flow_with_actions",
            "eyebrow": "Autonomous Utility Architecture",
            "title": "Autonomous utility operations require governed business processes",
            "subtitle": "Artificial intelligence models cannot deliver value over unvouched transactions or conflicting offline spreadsheets",
            "flow_boxes": [
                ("Reliable Transactions", "SAP Audit Trails", theme.C_MUTED),
                ("Connected Processes", "IT/OT Convergence", theme.C_PRIMARY),
                ("Governed Master Data", "Semantic Entities", theme.C_PRIMARY),
                ("AI-Assisted Decisions", "Pattern Analytics", theme.C_PRIMARY),
                ("Controlled Automation", "Human Governance", theme.C_NAVY)
            ],
            "actions": [
                "Billing Anomaly Detection: Pattern recognition spotting meter tampering and sudden zero-consumption accounts.",
                "Receivables Priority Scoring: Dynamic collection scoring ranking high-default commercial consumers for recovery.",
                "Predictive Asset Maintenance: Health-indexing transformers based on load cycles and ambient thermal stress.",
                "Working Capital Forecasting: Predictive modeling of daily power purchase liabilities against collection inflows."
            ],
            "legend_items": [
                (theme.C_MUTED, "Foundational Process Discipline"),
                (theme.C_PRIMARY, "Enterprise Context & AI Analytics"),
                (theme.C_NAVY, "Governed Operational Autonomy")
            ],
            "caveat_text": "Governance Mandate: AI assists and recommends, but human accountability and authorization thresholds remain non-negotiable for regulatory and financial decisions.",
            "layout_rationale": "Chosen 'flow_with_actions' to show the sequential progression toward autonomy backed by practical utility AI use case cards.",
            "notes": "Details JBVNL's path toward intelligent and autonomous operations. Emphasizes that AI models amplify whatever data they receive: bad data and chaotic manual processes produce flawed AI decisions. Controlled automation requires governed transactions as an absolute precondition."
        },

        # Slide 14: The Roadmap to Value Realization (Roadmap Rows)
        {
            "slide_number": 14,
            "content_shape": "phases_over_time",
            "eyebrow": "Transformation Execution Plan",
            "title": "A practical four-phase journey from underutilized ERP to intelligent utility",
            "subtitle": "Prioritizing high-impact quick wins and operational stabilization before advanced automated intelligence",
            "phases": [
                ("Phase 1: Discover & Assess", "Weeks 1–8 · SAP audit · Process gap mapping · Master data checks · KPI alignment · Leadership workshops"),
                ("Phase 2: Stabilize & Standardize", "Weeks 9–20 · Master data cleansing · Mandatory workflows · Retraining · Register elimination"),
                ("Phase 3: Integrate & Optimize", "Weeks 21–36 · Meter-to-cash integration · PM-MM-FICO links · Exception dashboards · Bank reconciliation"),
                ("Phase 4: Intelligent Operations", "Weeks 37–52 · Predictive asset analytics · Revenue protection · AI forecasting · Circle governance")
            ],
            "future_readiness_title": "Continuous Value Architecture",
            "future_readiness_desc": "Establishes self-sustaining process ownership across JBVNL circles, preparing the utility for future S/4HANA migration.",
            "layout_rationale": "Chosen 'phases_over_time' 4-phase sequential timeline with future architecture readiness callout card.",
            "notes": "Outlines a pragmatic, non-disruptive 52-week transformation roadmap. Rejects big-bang risks in favor of quick wins in Phase 1 and stabilization in Phase 2, followed by cross-system integration and intelligent operations."
        },

        # Slide 15: Closing Strategic Mandate (Dark Hero Finale)
        {
            "slide_number": 15,
            "content_shape": "closing",
            "title": "From Systems of Record to an Intelligent Power Distribution Enterprise",
            "subtitle": "JBVNL's transformation begins by unlocking the value of its existing enterprise systems and operational data",
            "core_message": "JBVNL does not necessarily need another system to begin its transformation. It needs to unlock the business value of the systems, processes and information it already possesses.",
            "pillars": [
                ("Meter-to-Cash Integrity", "End-to-end integration from smart meters to bank reconciliation, eliminating commercial revenue leakages."),
                ("Asset & O&M Governance", "Lifecycle maintenance tracking linking distribution transformers to inventory and cost centres."),
                ("Unified Financial Backbone", "Transaction integrity enforcing budget control, clean audit trails, and unified regulatory true-ups."),
                ("Contextual Utility Intelligence", "Connecting operational signals with business reality to enable predictive and autonomous decisions.")
            ],
            "concluding_statement": "What matters is not how much information the enterprise holds, but how effectively it turns that information into action.",
            "pill_text": "Strategic Mandate  |  JBVNL 2026",
            "layout_rationale": "Dark navy executive finale synthesizing core transformation pillars and delivering the decisive concluding message.",
            "notes": "Concluding executive address to the Board of Directors of JBVNL. Reasserts that enterprise transformation is about operational adoption, governance, and business context—positioning Lumbini as JBVNL's long-term transformation partner."
        }
    ]

    return {
        "theme": "lumbini",
        "client": "Jharkhand Bijli Vitran Nigam Limited (JBVNL)",
        "meta": {
            "client": "Jharkhand Bijli Vitran Nigam Limited (JBVNL)",
            "topic": "Enterprise Transformation & SAP Value Realization",
            "confidentiality": "Executive Strategy Briefing",
            "doc_type": "Strategy Presentation"
        },
        "sections": [
            ("The Operational Reality", 4),
            ("Value Chain & Architecture", 4),
            ("Empirical Benchmarks & Financial Impact", 3),
            ("Intelligent Operations & Roadmap", 4)
        ],
        "slides": slides
    }

if __name__ == "__main__":
    out_pptx = os.path.abspath("JBVNL_Enterprise_Transformation_Strategy.pptx")
    spec = build_jbvnl_spec()

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
    print("STAGE 4: PRE-FLIGHT QUALITY GATE & PREVIEW EXPORT")
    print("=" * 70)
    preview_dir = os.path.abspath("previews_jbvnl")
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

    qa_json_path = os.path.abspath("qa_jbvnl_report.json")
    with open(qa_json_path, "w", encoding="utf-8") as f:
        json.dump(qa_report, f, indent=2)
    print(f"QA report written to: {qa_json_path}")
