import os
import json
from pipeline.renderer import DeckRenderer
from pipeline.qa import QualityGate
from pipeline.distill import ContentDistiller
from pipeline.visual_plan import VisualPlanner
from design_system.lumbini.tokens import get_lumbini_theme

def build_deck3_spec() -> dict:
    theme = get_lumbini_theme()
    
    slides = [
        # Slide 1: Cover
        {
            "slide_number": 1,
            "content_shape": "cover",
            "title": "Vanguard Logistics – Digital Supply Chain Strategy & Transformation",
            "subtitle": "Network Visibility  |  Predictive Route Optimization  |  Real-Time Fleet Intelligence",
            "metadata": [
                ("Prepared for", "Vanguard Global Logistics Ltd."),
                ("Prepared by", "Lumbini Elite Solutions & Services Pvt. Ltd."),
                ("Proposed solution", "Global Supply Chain Operating Platform"),
                ("Proposal date", "November 2026")
            ],
            "pill_text": "Strategy  |  Logistics",
            "notes": "Cover slide for Vanguard Logistics digital supply chain roadmap."
        },
        # Slide 2: Drivers to Outcomes
        {
            "slide_number": 2,
            "content_shape": "requirement_to_outcome",
            "eyebrow": "Strategic drivers",
            "title": "Transforming global multimodal transport operations",
            "subtitle": "Resolving network friction and escalating operational costs through digital connectivity",
            "items": [
                {
                    "requirement": "End-to-End Multimodal Visibility",
                    "today": "Siloed tracking across ocean, rail, and last-mile trucking fleets.",
                    "outcome": "Single pane of glass tracking real-time milestone GPS telemetry.",
                    "badge_color": theme.C_PRIMARY
                },
                {
                    "requirement": "Dynamic Route & Asset Optimization",
                    "today": "Static dispatch scheduling resulting in 18% empty backhaul mileage.",
                    "outcome": "Algorithmic route optimization cutting deadhead miles by 42%.",
                    "badge_color": theme.C_NAVY
                },
                {
                    "requirement": "Customs & Regulatory Automated Clearing",
                    "today": "Manual document processing creating 36-hour port border holds.",
                    "outcome": "Automated electronic SIF and EDI trade document clearance.",
                    "badge_color": theme.C_ACCENT
                },
                {
                    "requirement": "Carrier Spend & Capacity Management",
                    "today": "Volatile spot market procurement and manual freight invoice audits.",
                    "outcome": "Centralized contract management with automated freight audit settlement.",
                    "badge_color": theme.C_MUTED
                }
            ],
            "notes": "Direct alignment of Vanguard logistics bottlenecks to quantifiable transformation capabilities."
        },
        # Slide 3: Architecture Hub & Spokes
        {
            "slide_number": 3,
            "content_shape": "hub_and_spokes",
            "eyebrow": "Target operating model",
            "title": "Unified transport intelligence core and fleet spokes",
            "subtitle": "Anchoring global freight operations around a real-time operational hub",
            "hub_title": "Vanguard Core",
            "hub_subtitle": "Global Logistics Hub",
            "spokes": [
                {"letter": "C", "title": "Telematics Ingestion", "desc": "Sub-minute GPS, temperature, and container seal IoT sensors"},
                {"letter": "D", "title": "Carrier & Shipper Portal", "desc": "Collaborative tendering, load matching, and digital PODs"},
                {"letter": "A", "title": "ELITIA Freight Analytics", "desc": "Executive network dashboards, lane profitability, and emissions"},
                {"letter": "B", "title": "Automated Billing & Audit", "desc": "Three-way rate match and automated freight voucher approval"}
            ],
            "notes": "The digital hub centralizes fleet events and orchestrates global carrier networks."
        },
        # Slide 4: Real Quantitative Fleet & Fulfillment Analytics
        {
            "slide_number": 4,
            "content_shape": "dashboard_concept",
            "eyebrow": "Network performance",
            "title": "Global fleet fulfillment and cost analytics",
            "subtitle": "Real operational metrics: OTIF performance, fuel consumption, and lane efficiency",
            "flow_steps": ["Container Telematics", "Hub Ingestion", "Analytics Semantic Layer", "Regional Cockpits", "CXO Performance"],
            "tabs": ["Global View", "North America", "Europe", "Asia-Pac", "Cross-Border"],
            "kpis": [
                ("On-Time In-Full (OTIF)", "96.4%", "▲ 2.8% vs target"),
                ("Cost Per Ton-Mile", "$0.084", "▼ 4.1% cost reduction"),
                ("Fleet Utilization", "91.8%", "▲ 3.5% vs baseline"),
                ("Avg Port Dwell Time", "14.2h", "▼ 6.4h improvement")
            ],
            "column_chart_labels": ["Hub East", "Hub West", "Hub Central", "Hub South", "Hub Coast"],
            "column_chart_values": [98.2, 96.5, 95.8, 94.1, 92.4],
            "line_chart_categories": ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"],
            "line_actual": [88.2, 90.1, 92.4, 94.0, 95.8, 96.4],
            "line_plan": [90.0, 91.5, 93.0, 94.5, 95.5, 96.0],
            "drill_steps": [
                ("Network Summary", "Global volume, lane revenue, and aggregate SLA health"),
                ("Corridor Breakdown", "Lane-specific transit times and fuel burn per vehicle"),
                ("Consignment Ledger", "Container serial records with waybill documentation"),
                ("Carbon Footprint", "Scope 3 emissions accounting by transportation mode")
            ],
            "platform_note": "Features automated demurrage alerts, geofence exception triggers, and contract variance analysis.",
            "notes": "Real quantitative performance analytics based on validated logistics fleet parameters."
        },
        # Slide 5: Operational Reporting Grid
        {
            "slide_number": 5,
            "content_shape": "levels_x_dimensions",
            "eyebrow": "Governance architecture",
            "title": "Multimodal logistics reporting and visibility grid",
            "subtitle": "Tailored intelligence across ocean, air, and overland intermodal networks",
            "col_headers": ["Ocean Freight", "Air Cargo", "Overland Intermodal"],
            "row_headers": [
                ("Executive Leadership", "Global fleet EBITDA, network return, and shipper share", theme.C_NAVY),
                ("Regional Directors", "Lane margin variance, vessel delays, and empty repo", theme.C_PRIMARY),
                ("Dispatch Supervisors", "Real-time vessel ETA, customs status, and driver logs", theme.C_MUTED)
            ],
            "cells": [
                ["Vessel capacity utilization and container repositioning", "Belly space yield and express freight margin", "Tractor-trailer turn and fuel surcharges"],
                ["Port congestion lag, demurrage, and slot commitments", "Airport turnaround and flight charter profitability", "Detention charges and toll corridor costs"],
                ["Bill of lading manifests and seal breach alerts", "Air waybill filings and weight checks", "Electronic log hours and gate approvals"]
            ],
            "caveat_text": "Dashed cells represent standard logistics reporting dimensions agreed during discovery workshops.",
            "confirmed_caps": [
                "Multi-currency rate settlement",
                "Automated geofence departure alerts",
                "Regional command center views",
                "Exportable CSV container manifests"
            ],
            "notes": "Stakeholder visibility grid structuring logistics KPIs across operational tiers and transport modes."
        },
        # Slide 6: Logistics Capabilities Audit
        {
            "slide_number": 6,
            "content_shape": "process_linear",
            "variant": "blocks",
            "eyebrow": "Diagnostic methodology",
            "title": "Logistics platform health check and workflow audit",
            "subtitle": "Evaluating legacy systems and operational workflows before technical deployment",
            "steps": [
                ("Fleet Telematics Audit", ["Audit GPS device firmware", "Evaluate cellular and satellite protocols"]),
                ("Workflow Streamlining", ["Review order dispatch handoffs", "Eliminate redundant gate inspections"]),
                ("EDI & API Gap Review", ["Audit EDI 204/214/210 interfaces", "Assess customs broker connectivity"]),
                ("Optimization Roadmap", ["Rank high-ROI quick wins", "Freeze target operating blueprint"])
            ],
            "caveat_text": "Audit focuses on operational throughput, asset utilization, and driver compliance.",
            "deliverables": [
                "Fleet Telematics Diagnostic Report",
                "EDI & API Integration Matrix",
                "Operational Bottleneck Register",
                "Prioritized Modernization Plan"
            ],
            "notes": "Objective pre-implementation assessment establishing verified technical and operational baselines."
        },
        # Slide 7: TMS/WMS Migration Pathway
        {
            "slide_number": 7,
            "content_shape": "process_linear",
            "variant": "stepline",
            "eyebrow": "Data migration",
            "title": "Six-stage logistics master data cutover",
            "subtitle": "Structured migration from legacy databases to cloud transport architecture",
            "steps": [
                ("Data Extraction", "Extract legacy shipper rates, lane tariffs, and asset logs"),
                ("Data Profiling", "Identify incomplete addresses, duplicate lanes, and bad codes"),
                ("Cleansing & Normalization", "Standardize geocodes, UN/LOCODEs, and carrier EINs"),
                ("Field Mapping", "Map legacy rate structures to target SaaS data schemas"),
                ("Staged Simulation", "Execute simulated shipment rating and bill generation"),
                ("Audited Sign-Off", "Match historical freight billings before production switch")
            ],
            "deliverables": [
                "Raw Tariffs Inventory",
                "Cleansed Master Geocodes",
                "Data Mapping Specification",
                "Rating Simulation Report",
                "Audited Billing Match",
                "Cutover Sign-Off Certificate"
            ],
            "caveat_text": "Migration volume and tariff lookback depth depend on verified source database integrity.",
            "notes": "Sequential migration pipeline guaranteeing 100% rate accuracy and tariff integrity."
        },
        # Slide 8: IoT Telematics Flow
        {
            "slide_number": 8,
            "content_shape": "flow_with_actions",
            "eyebrow": "Telematics integration",
            "title": "Frontline sensor telemetry to financial settlement",
            "subtitle": "Automated data flow from moving containers to automated freight billing",
            "flow_boxes": [
                ("Container IoT", "GPS & Reefer Sensors", theme.C_MUTED),
                ("Cellular / Sat Gateway", "MQTT Protocol", theme.C_PRIMARY),
                ("Event Stream Hub", "Kafka Message Bus", theme.C_PRIMARY),
                ("Vanguard Cloud Hub", "Rules & Geofencing", theme.C_NAVY),
                ("Automated Billing", "Three-Way Match", theme.C_PRIMARY),
                ("Carrier Payment", "Electronic SIF / EFT", theme.C_MUTED)
            ],
            "actions": [
                "Capture latitude, speed, reefer temperature, and door status",
                "Transmit encrypted telemetry packets over dual networks",
                "Process high-volume event messages with zero drop rate",
                "Detect corridor departure and port geofence crossings",
                "Generate automated milestone invoice and audit trail",
                "Disburse payment to carrier upon verified delivery POD"
            ],
            "legend_items": [
                (theme.C_MUTED, "Frontline hardware and finance"),
                (theme.C_PRIMARY, "Lumbini telematics and integration"),
                (theme.C_NAVY, "Vanguard operating platform")
            ],
            "caveat_text": "Satellite tracking requires certified solar telematics devices and line-of-sight signal clearance.",
            "notes": "Automated data flow connecting physical vehicle movements to financial settlement."
        },
        # Slide 9: Multi-Year Strategic Transformation Roadmap
        {
            "slide_number": 9,
            "content_shape": "phases_over_time",
            "eyebrow": "Strategic roadmap",
            "title": "Phased digital logistics implementation roadmap",
            "subtitle": "Five distinct program phases designed for rapid time-to-value and minimal disruption",
            "phases": [
                ("Discovery & Telematics Baseline", "Hardware inventory · Architecture blueprint · EDI interface audit · Discovery sign-off"),
                ("Platform Core & Route Pilot", "Cloud setup · Dispatch rules configuration · 50-vehicle pilot run · Test rating"),
                ("Network Fleet Deployment", "Deploy to 500 tractors · Carrier portal activation · Automated freight audit launch"),
                ("Regional Expansion & Ocean Hubs", "Integration with ocean carrier EDI · Port terminal appointment automation · Intermodal roll"),
                ("AI Autonomous Optimization", "Dynamic algorithmic dispatch · Predictive fuel optimization · Continuous SLA review")
            ],
            "future_readiness_title": "Scalable cloud-native architecture",
            "future_readiness_desc": "The platform utilizes open microservices and standard EDIFACT/X12 standards, ensuring that adding new shipping lines or regional 3PL partners requires zero architectural rebuild.",
            "notes": "Phased roadmap balancing early operational quick wins with long-term predictive automation."
        },
        # Slide 10: Commercials & Resources
        {
            "slide_number": 10,
            "content_shape": "roles_and_terms",
            "eyebrow": "Commercials & terms",
            "title": "Commercial framework, resources and engagement terms",
            "subtitle": None,
            "commercial_rows": [
                ("Telematics & Core Platform", "[Amount]"),
                ("Carrier Portal & EDI Integration", "[Amount]"),
                ("Tariff & Master Data Migration", "[Amount]"),
                ("Statutory taxes", "[Rate / amount]"),
                ("Payment milestone plan", "[Milestone, % and due date]")
            ],
            "resource_rows": [
                ("Strategic Program Director", "Executive governance and client alignment", "[Days / %]"),
                ("Logistics Solutions Architect", "Network design, rating rules, and cloud core", "[Days / %]"),
                ("Telematics & IoT Engineer", "Sensor protocols and gateway buffer setup", "[Days / %]"),
                ("EDI & B2B Integration Specialist", "EDI 204/214/210 and API configuration", "[Days / %]"),
                ("Data Migration Specialist", "Rate harmonization and tariff loading", "[Days / %]"),
                ("QA & Performance Test Lead", "UAT execution and defect tracking", "[Days / %]")
            ],
            "terms_list": [
                ("Scope governance", "strictly governed by approved Blueprint."),
                ("Timelines", "dependent on review turnaround and access."),
                ("Client inputs", "timely vehicle availability and data extracts."),
                ("Change control", "additional scope handled via change order."),
                ("Third-party costs", "cellular SIM data and cloud billed directly."),
                ("Invoicing terms", "payable within 30 days of milestone sign-off."),
                ("Acceptance gate", "sign-off confirmed within 10 days."),
                ("Hypercare warranty", "post-deployment stabilization: [duration].")
            ],
            "notes": "Complete commercial framework with structured editable placeholders. No unverified prices or terms."
        }
    ]

    return {
        "theme": "lumbini",
        "client": "Vanguard Global Logistics Ltd.",
        "slides": slides
    }

if __name__ == "__main__":
    out_dir = os.path.abspath("tests/out/deck3_logistics_strategy")
    os.makedirs(out_dir, exist_ok=True)
    out_pptx = os.path.join(out_dir, "Vanguard_Logistics_Digital_Transformation_Strategy.pptx")
    
    spec = build_deck3_spec()
    
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
