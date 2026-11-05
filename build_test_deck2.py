import os
import json
from pipeline.renderer import DeckRenderer
from pipeline.qa import QualityGate
from pipeline.distill import ContentDistiller
from pipeline.visual_plan import VisualPlanner
from design_system.lumbini.tokens import get_lumbini_theme

def build_deck2_spec() -> dict:
    theme = get_lumbini_theme()
    
    slides = [
        # Slide 1: Cover
        {
            "slide_number": 1,
            "content_shape": "cover",
            "title": "Industrial Precision – SAP S/4HANA Manufacturing Transformation",
            "subtitle": "Clean Core Architecture  |  Shop-Floor Connectivity  |  Real-Time ACDOCA Lineage",
            "metadata": [
                ("Prepared for", "Apex Industrial Manufacturing Corp."),
                ("Prepared by", "Lumbini Elite Solutions & Services Pvt. Ltd."),
                ("Proposed solution", "SAP S/4HANA Private Cloud & MES"),
                ("Proposal date", "November 2026")
            ],
            "pill_text": "Transformation  |  S/4HANA",
            "notes": "Cover slide for Apex Industrial Manufacturing SAP S/4HANA transformation proposal."
        },
        # Slide 2: Drivers to Outcomes
        {
            "slide_number": 2,
            "content_shape": "requirement_to_outcome",
            "eyebrow": "Strategic drivers",
            "title": "Modernizing discrete plant operations on S/4HANA",
            "subtitle": "Connecting shop-floor execution constraints to enterprise financial outcomes",
            "items": [
                {
                    "requirement": "Real-Time Plant Financials",
                    "today": "Batch costing and delayed month-end WIP reconciliation across 4 manufacturing plants.",
                    "outcome": "Instantaneous margin visibility via universal journal ledger (ACDOCA).",
                    "badge_color": theme.C_PRIMARY
                },
                {
                    "requirement": "Shop-Floor Execution & MES Sync",
                    "today": "Isolated paper travellers, manual shift handovers, and untracked scrap rates.",
                    "outcome": "Closed-loop MES telemetry updating machine tool offsets and job orders.",
                    "badge_color": theme.C_NAVY
                },
                {
                    "requirement": "Legacy ECC Custom Code Debt",
                    "today": "Over 450 custom Z-reports and modifications delaying system upgrades.",
                    "outcome": "Clean-core extension architecture utilizing SAP BTP side-by-side apps.",
                    "badge_color": theme.C_ACCENT
                },
                {
                    "requirement": "Supply Chain & Material Visibility",
                    "today": "Stockouts and buffer inventory inflation due to batch MRP cycles.",
                    "outcome": "Predictive MRP Live running in seconds for automated supplier replenishment.",
                    "badge_color": theme.C_MUTED
                }
            ],
            "notes": "Direct alignment between Apex plant challenges and target S/4HANA business capabilities."
        },
        # Slide 3: Architecture Hub & Spokes
        {
            "slide_number": 3,
            "content_shape": "hub_and_spokes",
            "eyebrow": "Target architecture",
            "title": "Connected digital core anchored by S/4HANA",
            "subtitle": "Direct integration linking shop-floor PLCs to executive board reporting",
            "hub_title": "SAP S/4HANA",
            "hub_subtitle": "Digital Enterprise Core",
            "spokes": [
                {"letter": "C", "title": "BTP Integration Suite", "desc": "API management, supplier portal, and cloud microservices"},
                {"letter": "D", "title": "Shop-Floor MES & OT", "desc": "Sub-second PLC machine telemetry and unit genealogy"},
                {"letter": "A", "title": "ELITIA Plant Intelligence", "desc": "Centralized executive cockpits, OEE metrics, and yield analysis"},
                {"letter": "B", "title": "Extended Warehouse (EWM)", "desc": "Automated guided vehicles and bin-level serialization"}
            ],
            "notes": "S/4HANA core orchestrates plant execution, supplier logistics, and operational intelligence."
        },
        # Slide 4: Plant Intelligence Dashboard
        {
            "slide_number": 4,
            "content_shape": "dashboard_concept",
            "eyebrow": "Manufacturing intelligence",
            "title": "Shop-floor telemetry and executive cockpit",
            "subtitle": "Real-time visibility across lines, machine work centers, and shift performance",
            "flow_steps": ["Plant Sensors", "Edge Gateway", "SAP BTP Core", "Plant Cockpits", "CXO Analytics"],
            "tabs": ["Plant Overview", "Machining Lines", "Assembly", "Quality & Scrap", "Maintenance"],
            "kpis": [
                ("Overall OEE", "87.4%", "▲ 3.2% vs baseline"),
                ("Schedule Adherence", "98.1%", "▲ 1.5% vs target"),
                ("First-Pass Yield", "99.4%", "▲ 0.4% vs last qtr"),
                ("Scrap Reduction", "1.2%", "▼ 0.8% reduction")
            ],
            "column_chart_labels": ["Plant 1", "Plant 2", "Plant 3", "Plant 4", "Plant 5"],
            "column_chart_values": [91.2, 88.5, 86.4, 84.1, 82.0],
            "line_chart_categories": ["W1", "W2", "W3", "W4", "W5", "W6"],
            "line_actual": [84.0, 85.2, 86.1, 86.8, 87.1, 87.4],
            "line_plan": [85.0, 85.5, 86.0, 86.5, 87.0, 87.5],
            "drill_steps": [
                ("Fleet Summary", "Global plant OEE, downtime, and commitment rates"),
                ("Work Center Drill", "Machine-level cycle times and operator performance"),
                ("Genealogy Traveler", "Serial-tracked component lot and heat numbers"),
                ("Financial Impact", "Real-time cost variance posted to universal ledger")
            ],
            "platform_note": "Includes automated anomaly threshold alerts, maintenance telemetry, and shift handovers.",
            "notes": "Primary operational analytics slide. Illustrative layout representing plant telemetry feeds."
        },
        # Slide 5: Operational Reporting Grid
        {
            "slide_number": 5,
            "content_shape": "levels_x_dimensions",
            "eyebrow": "Operational governance",
            "title": "Multi-tier manufacturing governance framework",
            "subtitle": "Targeted visibility from plant floor supervisors to executive steering committee",
            "col_headers": ["Plant Finance", "Shop-Floor Ops", "Supply Chain"],
            "row_headers": [
                ("Executive Steering", "Total plant margin, return on capital, and capex", theme.C_NAVY),
                ("Plant Managers", "OEE bottlenecks, labor variance, and tooling spend", theme.C_PRIMARY),
                ("Line Supervisors", "Job order progress, scrap counts, and shift logs", theme.C_MUTED)
            ],
            "cells": [
                ["Unit manufacturing cost and inventory capital exposure", "Plant capacity utilization and equipment yield", "Supplier OTIF adherence and material cost variance"],
                ["Standard vs actual production cost variances", "Unplanned machine downtime and maintenance lag", "Raw material buffer stock and lead-time tracking"],
                ["Active job routing times and rework labor tracking", "Immediate machine alarm logs and operator shift notes", "Warehouse bin replenishment and picking queues"]
            ],
            "caveat_text": "Dashed cells represent agreed reporting lenses. Final KPIs will be approved during Explore workshops.",
            "confirmed_caps": [
                "Real-time ACDOCA ledger settlement",
                "Machine-level drill down to batch travelers",
                "Role-based plant floor dashboards",
                "Automated scrap exception alerts"
            ],
            "notes": "Structured matrix mapping stakeholder tiers against core manufacturing operational domains."
        },
        # Slide 6: Custom Code Remediation
        {
            "slide_number": 6,
            "content_shape": "process_linear",
            "variant": "blocks",
            "eyebrow": "Clean core methodology",
            "title": "Technical code remediation and migration audit",
            "subtitle": "Systematic assessment retiring technical debt before production migration",
            "steps": [
                ("Custom Code Audit", ["Scan 450+ legacy Z-objects", "Classify usage via SAP UPL"]),
                ("Clean Core Review", ["Map custom logic to standard S/4", "Retire obsolete modifications"]),
                ("BTP Decoupling", ["Author side-by-side extensions", "Expose secure OData REST APIs"]),
                ("Readiness Baseline", ["Execute readiness check tool", "Sign off target landscape"])
            ],
            "caveat_text": "Assessment methodology adheres strictly to SAP Clean Core guidelines to ensure future release stability.",
            "deliverables": [
                "Custom Code Assessment Report",
                "Clean Core Architecture Blueprint",
                "Remediation Work Breakdown",
                "Target Cloud Landscape Baseline"
            ],
            "notes": "Methodology focuses on reducing technical debt and moving custom enhancements to SAP BTP."
        },
        # Slide 7: Data Migration Pathway
        {
            "slide_number": 7,
            "content_shape": "process_linear",
            "variant": "stepline",
            "eyebrow": "Migration methodology",
            "title": "Structured six-stage manufacturing data cutover",
            "subtitle": "From legacy ECC extraction to fully reconciled production balance sheets",
            "steps": [
                ("Extract & Scope", "Extract plant master data, open orders, and balance sheets"),
                ("Data Cleansing", "Deduplicate vendor records and harmonize material masters"),
                ("Field Mapping", "Map legacy tables to target S/4 business partner structures"),
                ("Staging Load", "Execute automated load cycles using SAP Migration Cockpit"),
                ("Dry-Run Cutover", "Conduct mock cutover over a simulated production weekend"),
                ("Sign-Off & Go-Live", "Audited financial trial balance matching before go-live")
            ],
            "deliverables": [
                "Raw Extract Inventory",
                "Cleansed Material Master",
                "Migration Mapping Spec",
                "Cockpit Execution Logs",
                "Mock Cutover Sign-Off",
                "Production Go-Live Certificate"
            ],
            "caveat_text": "Cutover timing and blackout windows will be finalized during the Realize phase based on mock timings.",
            "notes": "Six-stage migration pipeline ensuring zero data loss and complete financial reconciliation."
        },
        # Slide 8: Shop-Floor OT-IT Flow
        {
            "slide_number": 8,
            "content_shape": "flow_with_actions",
            "eyebrow": "Shop-floor integration",
            "title": "Real-time machine telemetry to enterprise ledger",
            "subtitle": "Connecting frontline shop-floor PLCs to SAP production order settlement",
            "flow_boxes": [
                ("Machine Sensors", "CNC / PLC Telemetry", theme.C_MUTED),
                ("Edge Gateway", "OPC-UA Protocol", theme.C_PRIMARY),
                ("MES MOM Server", "Genealogy Tracking", theme.C_PRIMARY),
                ("SAP BTP Bridge", "REST OData APIs", theme.C_NAVY),
                ("S/4HANA Core", "Production Settlement", theme.C_PRIMARY),
                ("Executive Ledgers", "Real-Time ACDOCA", theme.C_MUTED)
            ],
            "actions": [
                "Ingest high-frequency vibration and cycle telemetry",
                "Buffer readings locally to prevent loss during drops",
                "Bind component serial numbers to lot orders",
                "Validate API payload schema and authentication",
                "Trigger automated confirmation of production orders",
                "Settle labor and variance directly to P&L"
            ],
            "legend_items": [
                (theme.C_MUTED, "Frontline shop-floor and finance"),
                (theme.C_PRIMARY, "Lumbini integration and MES engine"),
                (theme.C_NAVY, "SAP S/4HANA core")
            ],
            "caveat_text": "PLC communications depend on plant OPC-UA server readiness and network firewall isolation rules.",
            "notes": "End-to-end integration architecture demonstrating sub-second OT-to-IT data lineage."
        },
        # Slide 9: 5-Phase Implementation Roadmap
        {
            "slide_number": 9,
            "content_shape": "phases_over_time",
            "eyebrow": "Implementation roadmap",
            "title": "Phased SAP Activate delivery roadmap",
            "subtitle": "Structured delivery model with formal quality gates across all phases",
            "phases": [
                ("Discover & Prepare", "Project governance setup · Technical readiness check · Scope baseline · Architecture freeze"),
                ("Explore & Design", "Standard process workshops · Delta design · Clean core mapping · Integration specs"),
                ("Realize & Build", "S/4HANA configuration · MES interface build · Mock cutovers · Migration staging"),
                ("Deploy & Cutover", "User acceptance testing · Key user training · Final cutover weekend · Production go-live"),
                ("Run & Hypercare", "Dedicated post-go-live hypercare · SLA support · Knowledge transfer · Continuous improvement")
            ],
            "future_readiness_title": "Clean-core upgrade safety",
            "future_readiness_desc": "All extensions are developed on SAP BTP using approved APIs, ensuring that bi-annual S/4HANA cloud upgrades execute smoothly without regression risks.",
            "notes": "Roadmap aligned with SAP Activate methodology. Sequence bars indicate relative phasing without fixed dates."
        },
        # Slide 10: Commercials & Resources
        {
            "slide_number": 10,
            "content_shape": "roles_and_terms",
            "eyebrow": "Commercials & governance",
            "title": "Commercial framework, resources and engagement terms",
            "subtitle": None,
            "commercial_rows": [
                ("S/4HANA Core Implementation", "[Amount]"),
                ("MES & Shop-Floor Integration", "[Amount]"),
                ("Data Migration & Cleansing", "[Amount]"),
                ("Statutory taxes", "[Rate / amount]"),
                ("Payment milestone schedule", "[Milestone, % and due date]")
            ],
            "resource_rows": [
                ("Project Director / Enterprise Lead", "Program governance, risk management, and steerco", "[Days / %]"),
                ("SAP Solution Architect (S/4HANA)", "Core functional blueprint, ACDOCA design, and integration", "[Days / %]"),
                ("Manufacturing & MES Specialist", "PP/QM/MES shop-floor telemetry and machine bindings", "[Days / %]"),
                ("Clean Core & BTP Consultant", "Side-by-side app architecture and REST API services", "[Days / %]"),
                ("Data Migration Lead", "SAP Migration Cockpit staging, profiling, and validation", "[Days / %]"),
                ("QA & Performance Test Lead", "Integration test design, UAT coordination, and defect resolution", "[Days / %]")
            ],
            "terms_list": [
                ("Scope governance", "governed by approved Functional Blueprint."),
                ("Timelines", "dependent on workshop cadence and stage sign-offs."),
                ("Client inputs", "timely machine access and data extracts."),
                ("Change control", "scope adjustments managed via change order."),
                ("Third-party software", "SAP software contracted directly with vendor."),
                ("Invoicing terms", "payable within 30 days against signed milestones."),
                ("Acceptance gate", "sign-off within 10 days of submission."),
                ("Hypercare warranty", "post-cutover stabilization support: [duration].")
            ],
            "notes": "Commercial proposal with structured placeholders. All amounts, roles, and duration placeholders are editable."
        }
    ]

    return {
        "theme": "lumbini",
        "client": "Apex Industrial Manufacturing Corp.",
        "slides": slides
    }

if __name__ == "__main__":
    out_dir = os.path.abspath("tests/out/deck2_sap_manufacturing")
    os.makedirs(out_dir, exist_ok=True)
    out_pptx = os.path.join(out_dir, "Apex_SAP_S4HANA_Manufacturing_Transformation.pptx")
    
    spec = build_deck2_spec()
    
    # Audit
    distiller = ContentDistiller()
    total_words = 0
    for s in spec["slides"]:
        valid, w, viols = distiller.audit_slide_content(s)
        total_words += w
        print(f"Slide {s['slide_number']} ({s['content_shape']}): {w} words. Valid: {valid}")
        if viols:
            print("  Violations:", viols)
    print(f"Total Words: {total_words}, Avg words/slide: {total_words / len(spec['slides']):.1f}")
    
    # Layout diversity
    valid_layouts, l_viols = VisualPlanner.validate_layout_rules(spec["slides"])
    print(f"Layout diversity valid: {valid_layouts}, violations: {l_viols}")
    
    # Render
    renderer = DeckRenderer(theme_name="lumbini")
    rendered_file = renderer.render(spec, out_pptx)
    print(f"Rendered presentation: {rendered_file}")
    
    # QA
    qa_report = QualityGate.audit_deck(rendered_file, spec, render_images=True, preview_dir=os.path.join(out_dir, "previews"))
    qa_json_path = os.path.join(out_dir, "qa-report.json")
    with open(qa_json_path, "w", encoding="utf-8") as f:
        json.dump(qa_report, f, indent=2)
    print(f"QA Status: {qa_report['status']}, Blocking: {qa_report['blocking_count']}, Warnings: {qa_report['warning_count']}")
    print(f"QA Report saved: {qa_json_path}")
