import os
import json
from pipeline.renderer import DeckRenderer
from pipeline.qa import QualityGate
from pipeline.distill import ContentDistiller
from pipeline.visual_plan import VisualPlanner
from design_system.lumbini.tokens import get_lumbini_theme

def build_test_a_spec() -> dict:
    theme = get_lumbini_theme()

    slides = [
        # Slide 1: Cover
        {
            "slide_number": 1,
            "content_shape": "cover",
            "title": "Navigating the SAP Datasphere Career Path",
            "subtitle": "Modern Data Fabric Architecture  |  Semantic Modeling  |  Cloud Warehousing",
            "metadata": [
                ("Audience", "Enterprise Data Architects & Practitioners"),
                ("Prepared by", "Lumbini Elite Solutions & Services"),
                ("Focus", "SAP Datasphere & BTP"),
                ("Date", "November 2026")
            ],
            "pill_text": "Career Architecture  |  SAP Datasphere",
            "layout_rationale": "Standard executive presentation cover layout with metadata and category pill.",
            "notes": "Executive briefing outlining core technical domains, role transitions, market compensation benchmarks, and structured certification pathways in SAP Datasphere."
        },
        # Slide 2: The Architectural Iceberg of Data Warehousing (NEW GRAMMAR: iceberg_shift)
        {
            "slide_number": 2,
            "content_shape": "iceberg_shift",
            "eyebrow": "Ecosystem Transformation",
            "title": "The architectural iceberg of enterprise data warehousing",
            "subtitle": "Distinguishing visible reporting symptoms from deep structural shifts in cloud data fabric",
            "visible_event": {
                "title": "Legacy BW / Reporting Bottlenecks",
                "desc": "Rigid InfoCubes, delayed batch extraction queues, and siloed calculation views."
            },
            "submerged_layers": [
                {
                    "layer_name": "Data Virtualization & Federation",
                    "finding": "Zero-copy virtualization connecting SAP HANA Cloud to hyperscalers without duplication."
                },
                {
                    "layer_name": "Decentralized Space Governance",
                    "finding": "Domain Spaces enforcing tenant isolation, memory budgeting, and role access control."
                },
                {
                    "layer_name": "Business Semantic Modeling",
                    "finding": "Decoupling database schemas from analytical consumption via governed business entities."
                }
            ],
            "callout_text": "The transition from SAP BW to Datasphere is an architectural shift from batch staging to decentralized data fabric with self-service semantic consumption.",
            "layout_rationale": "Chosen 'iceberg_shift' because the transformation requires separating visible SQL/reporting symptoms above the waterline from deep structural governance and semantic mesh layers beneath.",
            "notes": "Contrasts legacy BW operational bottlenecks with deep Datasphere fabric architecture."
        },
        # Slide 3: Four-Tier Enterprise Data Fabric Stack (NEW GRAMMAR: layered_stack)
        {
            "slide_number": 3,
            "content_shape": "layered_stack",
            "eyebrow": "Architectural Hierarchy",
            "title": "The four foundational tiers of modern SAP data fabric",
            "subtitle": "Structural layers bridging physical data storage to executive consumption",
            "layers": [
                {
                    "tier": "Tier 4: Analytics Consumption",
                    "title": "SAP Analytics Cloud (SAC) & Executive Cockpits",
                    "desc": "Live analytical connections, predictive planning models, and unified board cockpits.",
                    "color": theme.C_NAVY
                },
                {
                    "tier": "Tier 3: Business Semantics",
                    "title": "Business Builder & Governed Metrics",
                    "desc": "Business entities, consumption models, dimension hierarchies, and governed metric definitions.",
                    "color": theme.C_PRIMARY
                },
                {
                    "tier": "Tier 2: Space Governance",
                    "title": "Multi-Tenant Spaces & Access Boundaries",
                    "desc": "Logical tenant isolation, memory quota allocation, and cross-space data sharing.",
                    "color": theme.C_PRIMARY
                },
                {
                    "tier": "Tier 1: Data Virtualization",
                    "title": "Data Builder, Replication & Hyperscalers",
                    "desc": "Remote tables, replication flows, delta transform views, and connectors to BigQuery and Databricks.",
                    "color": theme.C_MUTED
                }
            ],
            "callout_note": "Datasphere establishes an open data fabric, virtualizing structured SAP business context alongside multi-cloud lakehouse storage without vendor lock-in.",
            "layout_rationale": "Chosen 'layered_stack' because Datasphere is an architectural platform stack where higher analytical consumption strictly depends on foundational virtualization and governance tiers.",
            "notes": "Four-tier architectural breakdown of Datasphere technical components."
        },
        # Slide 4: Market Scarcity & Demand Acceleration (NEW GRAMMAR: annotated_chart)
        {
            "slide_number": 4,
            "content_shape": "annotated_chart",
            "eyebrow": "Market Telemetry",
            "title": "Talent scarcity accelerates market compensation",
            "subtitle": "Enterprise S/4HANA migrations create intense industry demand for certified Datasphere architects",
            "chart_type": "column",
            "categories": ["2023 Base", "2024 Actual", "2025 Actual", "2026 Forecast", "2027 Projected"],
            "series_data": [
                {"name": "Hiring Demand Index", "values": [100.0, 148.0, 215.0, 320.0, 450.0]}
            ],
            "chart_title": "Enterprise Datasphere Talent Demand Index (Base 100)",
            "x_label": "Timeline Year",
            "y_label": "Demand Index",
            "key_takeaway": "Surging S/4HANA cloud transitions drive a 142% annual growth in certified Datasphere openings, creating acute talent shortages across global enterprises.",
            "callout_annotation": "Consultants combining Datasphere certification with SAP Analytics Cloud (SAC) and cross-cloud lakehouse experience command a 35% salary premium over traditional legacy developers.",
            "source_id": "SRC-DS-01",
            "layout_rationale": "Chosen 'annotated_chart' to display quantitative hiring growth metrics paired with an executive interpretation panel and verified source provenance.",
            "notes": "Empirical proof of career ROI and market momentum driving Datasphere specialization."
        },
        # Slide 5: Capability Maturity & Career Progression (NEW GRAMMAR: capability_maturity_staircase)
        {
            "slide_number": 5,
            "content_shape": "capability_maturity_staircase",
            "eyebrow": "Career Progression Matrix",
            "title": "Ascending competency expectations across career stages",
            "subtitle": "Clear capability progression from associate modeler to enterprise data architect",
            "steps": [
                {
                    "level_name": "Associate",
                    "role_title": "Data Builder Specialist",
                    "competencies": ["Graphical view modeling", "CSV & remote tables", "Local data flows"],
                    "gate_criterion": "Foundational Learning Journey"
                },
                {
                    "level_name": "Consultant",
                    "role_title": "Senior Semantic Engineer",
                    "competencies": ["Relational joins & SQL", "Delta replication tasks", "Consumption models & SAC"],
                    "gate_criterion": "C_DS_42 Certified Associate"
                },
                {
                    "level_name": "Architect",
                    "role_title": "Lead Data Fabric Architect",
                    "competencies": ["Multi-tenant Space sizing", "Databricks & BigQuery mesh", "Semantic catalog governance"],
                    "gate_criterion": "Production cutover lead"
                },
                {
                    "level_name": "Fellow",
                    "role_title": "Enterprise Chief Architect",
                    "competencies": ["Multi-cloud fabric strategy", "SAP BTP clean-core architecture", "Enterprise data governance"],
                    "gate_criterion": "Enterprise blueprint sign-off"
                }
            ],
            "caveat_text": "Competencies align with official SAP Partner Center of Excellence standards.",
            "layout_rationale": "Chosen 'capability_maturity_staircase' because career growth follows a discrete, ascending staircase of responsibilities and gate criteria.",
            "notes": "Granular capability roadmap from associate developer to enterprise fellow."
        },
        # Slide 6: Phased Roadmap to Certified Expertise
        {
            "slide_number": 6,
            "content_shape": "phases_over_time",
            "eyebrow": "Enablement Pathway",
            "title": "A structured 5-stage roadmap to certified expertise",
            "subtitle": "Proven learning milestones bridging theoretical foundations to live cloud implementation",
            "phases": [
                ("Phase 1: BTP Foundations", "SAP BTP subaccounts · Global accounts · Cloud security · HANA Cloud basics"),
                ("Phase 2: Data Builder", "Graphical & SQL views · Remote tables · Replication flows · Delta loading"),
                ("Phase 3: Business Semantics", "Business entities · Consumption models · SAC live connectivity · Metrics"),
                ("Phase 4: Fabric & Mesh", "Data federation · BigQuery / Databricks integration · Open data fabric"),
                ("Phase 5: SAP Certification", "Official SAP C_DS_42 certification · Real-world implementation · Lead role")
            ],
            "future_readiness_title": "Continuous ecosystem currency",
            "future_readiness_desc": "Datasphere receives quarterly cloud updates; architects maintain currency via quarterly SAP delta certifications.",
            "layout_rationale": "Chosen 'phases_over_time' to present chronological 5-stage learning progression from fundamentals to official certification.",
            "notes": "Five-stage progression from initial BTP fundamentals through to full production credentialing."
        },
        # Slide 7: Target Roles, Compensation & Action Plan (NEW GRAMMAR: career_trajectory_roadmap)
        {
            "slide_number": 7,
            "content_shape": "career_trajectory_roadmap",
            "eyebrow": "Career Trajectory",
            "title": "Target roles, compensation benchmarks and action plan",
            "subtitle": None,
            "roles": [
                ("Datasphere Solution Architect", "$170k - $225k"),
                ("Senior Semantic Data Engineer", "$135k - $170k"),
                ("Datasphere BI / SAC Specialist", "$105k - $135k"),
                ("BTP Integration Engineer", "$120k - $155k")
            ],
            "certifications": [
                ("C_DS_42", "SAP Certified Associate - Datasphere", "SAP Learning Hub"),
                ("C_S4CDP", "Cloud Architecture & BTP Integration", "SAP PartnerEdge"),
                ("C_SAC_AD", "SAP Analytics Cloud Story Design", "SAP Learning")
            ],
            "action_plan": [
                ("Days 1–15", "Initialize BTP trial tenant and provision Datasphere space."),
                ("Days 16–45", "Complete official Learning Journeys and graphical modeling labs."),
                ("Days 46–75", "Construct end-to-end data federation lab linking S/4HANA to SAC."),
                ("Days 76–90", "Schedule and pass official C_DS_42 associate certification.")
            ],
            "caveat_text": "Compensation ranges based on 2026 global enterprise consulting benchmarks.",
            "layout_rationale": "Chosen 'career_trajectory_roadmap' 3-zone layout to align role profiles, certification credentials, and a focused 90-day execution roadmap.",
            "notes": "Target roles, compensation benchmarks, core certifications, and 90-day enablement timeline."
        }
    ]

    return {
        "meta": {
            "client": "SAP Data Practitioners",
            "topic": "SAP Datasphere Career Architecture",
            "confidentiality": "Professional Development",
            "doc_type": "Career Guide"
        },
        "theme": "lumbini",
        "slides": slides
    }

if __name__ == "__main__":
    out_dir = os.path.abspath("tests/out/test_a_datasphere_v2")
    os.makedirs(out_dir, exist_ok=True)
    out_pptx = os.path.join(out_dir, "SAP_Datasphere_Career_Path_v2.pptx")

    spec = build_test_a_spec()

    # 1. Audit content & word budgets
    distiller = ContentDistiller()
    total_words = 0
    for s in spec["slides"]:
        valid, w, viols = distiller.audit_slide_content(s)
        total_words += w
        print(f"Slide {s['slide_number']} ({s['content_shape']}): {w} words. Valid: {valid}")
        if viols:
            print("  Violations:", viols)
    print(f"Total Words: {total_words}, Avg words/slide: {total_words / len(spec['slides']):.1f}")

    # 2. Audit visual layout diversity
    valid_layouts, l_viols = VisualPlanner.validate_layout_rules(spec["slides"])
    print(f"Layout diversity valid: {valid_layouts}, violations: {l_viols}")

    # 3. Render presentation
    renderer = DeckRenderer(theme_name="lumbini")
    rendered_file = renderer.render(spec, out_pptx)
    print(f"Rendered presentation: {rendered_file}")

    # 4. Automated Pre-Flight QA Audit with PowerPoint COM 1080p slide export
    qa_report = QualityGate.audit_deck(rendered_file, spec, render_images=True, preview_dir=os.path.join(out_dir, "previews"))
    qa_json_path = os.path.join(out_dir, "qa-report.json")
    with open(qa_json_path, "w", encoding="utf-8") as f:
        json.dump(qa_report, f, indent=2)
    print(f"QA Status: {qa_report['status']}, Blocking: {qa_report['blocking_count']}, Warnings: {qa_report['warning_count']}")
    print(f"Anti-Copy Audit: {qa_report['anti_copy_audit']}")
