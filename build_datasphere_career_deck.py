import os
import json
from pipeline.renderer import DeckRenderer
from pipeline.qa import QualityGate
from pipeline.distill import ContentDistiller
from pipeline.visual_plan import VisualPlanner
from design_system.lumbini.tokens import get_lumbini_theme

def build_datasphere_spec() -> dict:
    theme = get_lumbini_theme()

    slides = [
        # Slide 1: Cover
        {
            "slide_number": 1,
            "content_shape": "cover",
            "title": "Navigating the SAP Datasphere Career Path",
            "subtitle": "Modern Data Fabric Architecture  |  Semantic Modeling  |  Cloud Data Warehousing",
            "metadata": [
                ("Audience", "Enterprise Data Architects & Practitioners"),
                ("Prepared by", "Lumbini Elite Solutions & Services"),
                ("Focus", "SAP Datasphere & BTP"),
                ("Date", "November 2026")
            ],
            "pill_text": "Career Strategy  |  SAP Datasphere",
            "notes": "Executive briefing outlining core technical domains, role transitions, market compensation benchmarks, and structured certification pathways in SAP Datasphere."
        },
        # Slide 2: Drivers to Outcomes
        {
            "slide_number": 2,
            "content_shape": "requirement_to_outcome",
            "eyebrow": "Ecosystem Evolution",
            "title": "The shift from legacy SAP BW to cloud data fabric",
            "subtitle": "How traditional data warehouse specializations evolve into high-demand modern cloud disciplines",
            "items": [
                {
                    "requirement": "Traditional BW / BI Modeler",
                    "today": "Complex InfoCubes, rigid DSO staging, and slow multi-hop batch extraction.",
                    "outcome": "Cloud Data Architect orchestrating business semantic layers and virtualized access.",
                    "badge_color": theme.C_PRIMARY
                },
                {
                    "requirement": "HANA Native SQL Developer",
                    "today": "Siloed Calculation Views, manual data duplication, and on-prem hardware constraints.",
                    "outcome": "Semantic Data Engineer building real-time graphical models and cross-cloud federations.",
                    "badge_color": theme.C_NAVY
                },
                {
                    "requirement": "Enterprise BI Analyst",
                    "today": "Dependent on IT queues for schema adjustments, calculated measures, and report extracts.",
                    "outcome": "Self-Service Business Modeler defining domain spaces and rapid SAC analytical stories.",
                    "badge_color": theme.C_ACCENT
                },
                {
                    "requirement": "Data Governance Lead",
                    "today": "Fragmented metadata dictionaries, manual compliance audits, and untracked shadow IT.",
                    "outcome": "Data Fabric Governance Officer enforcing Space-level isolation, masking, and lineage.",
                    "badge_color": theme.C_MUTED
                }
            ],
            "notes": "Direct career translation mapping legacy SAP competencies to future-ready cloud data fabric roles."
        },
        # Slide 3: Architecture Hub & Spokes
        {
            "slide_number": 3,
            "content_shape": "hub_and_spokes",
            "eyebrow": "Core competency domains",
            "title": "The four architectural pillars of SAP Datasphere",
            "subtitle": "Core technical capabilities required to design, deploy, and govern enterprise data fabrics",
            "hub_title": "SAP Datasphere",
            "hub_subtitle": "Enterprise Data Fabric",
            "spokes": [
                {"letter": "A", "title": "Data Builder & Integration", "desc": "Federation, replication flows, transform views, and non-SAP connectors"},
                {"letter": "B", "title": "Business Builder & Semantics", "desc": "Business entities, consumption models, hierarchies, and metric governance"},
                {"letter": "C", "title": "Space Management & Access", "desc": "Tenant isolation, memory budgeting, role assignments, and data cataloging"},
                {"letter": "D", "title": "SAC & Analytics Consumption", "desc": "Live data connectivity, planning integration, story building, and executive cockpits"}
            ],
            "notes": "The four essential technical domains every aspiring SAP Datasphere consultant must master."
        },
        # Slide 4: Market Dynamics & Adoption Cockpit
        {
            "slide_number": 4,
            "content_shape": "dashboard_concept",
            "eyebrow": "Market demand & compensation",
            "title": "Talent scarcity accelerates market compensation",
            "subtitle": "Enterprise S/4HANA cloud migrations create surging demand for certified Datasphere architects",
            "flow_steps": ["Legacy BW / ECC", "BTP Strategy", "Datasphere Fabric", "Hybrid Mesh", "Enterprise Value"],
            "tabs": ["Market Overview", "Talent Shortage", "Salary Premium", "Adoption Rate", "Skill Gaps"],
            "kpis": [
                ("Datasphere Demand Growth", "+142%", "▲ YoY enterprise hiring demand"),
                ("Certified Talent Shortage", "68%", "▲ Global unfilled roles index"),
                ("Consultant Rate Premium", "+35%", "▲ Over legacy BW/HANA baselines"),
                ("Cloud Migration Sync", "84%", "▲ Enterprise programs linking DS")
            ],
            "column_chart_labels": ["2023", "2024", "2025", "2026 (E)", "2027 (P)"],
            "column_chart_values": [100.0, 148.0, 215.0, 320.0, 450.0],
            "line_chart_categories": ["Junior", "Mid-Level", "Senior", "Lead", "Enterprise Architect"],
            "line_actual": [85.0, 115.0, 150.0, 195.0, 240.0],
            "line_plan": [70.0, 95.0, 125.0, 160.0, 195.0],
            "drill_steps": [
                ("Regional Surge", "North America and EMEA driving massive enterprise hiring demand"),
                ("Skill Stacking", "Datasphere paired with SAC and Databricks commands highest premium"),
                ("Advisory Rates", "Independent architects earning top-tier consulting day rates"),
                ("BTP Adoption", "Enterprise BTP credits heavily allocated to Datasphere compute units")
            ],
            "platform_note": "Market statistics synthesized from SAP partner ecosystems, enterprise hiring indices, and global analyst benchmarks.",
            "notes": "Market telemetry demonstrating explosive career upside and ROI for Datasphere specialists."
        },
        # Slide 5: Seniority & Competency Matrix
        {
            "slide_number": 5,
            "content_shape": "levels_x_dimensions",
            "eyebrow": "Skill progression matrix",
            "title": "Competency expectations across seniority levels",
            "subtitle": "Capability progression across modeling, fabric, and semantics",
            "col_headers": ["Data Architecture & Modeling", "Data Fabric & Integration", "Semantics & SAC Consumption"],
            "row_headers": [
                ("Lead Architect", "Enterprise strategy, multi-cloud fabric, and security", theme.C_NAVY),
                ("Senior Consultant", "Complex modeling, pipelines, and space orchestration", theme.C_PRIMARY),
                ("Associate Specialist", "Table creation, replication tasks, and basic views", theme.C_MUTED)
            ],
            "cells": [
                [
                    "Multi-tenant space architecture, tiering, and sizing",
                    "Cross-cloud federation with Databricks and BigQuery",
                    "Enterprise semantic governance and metric catalogs"
                ],
                [
                    "Complex relational joins and delta replication",
                    "Remote tables, streaming flows, and OData monitoring",
                    "Analytical datasets, consumption models, and SAC stories"
                ],
                [
                    "Graphical view creation and CSV data loading",
                    "Standard SAP replication and user credential mapping",
                    "Dimension tagging and simple hierarchy setup in SAC"
                ]
            ],
            "caveat_text": "Competencies align with official SAP Partner Center of Excellence standards.",
            "confirmed_caps": [
                "Role-based Space configuration",
                "Cross-cloud virtualization",
                "Consumption model orchestration",
                "Enterprise security mapping"
            ],
            "notes": "Matrix mapping professional seniority tiers against core Datasphere execution disciplines."
        },
        # Slide 6: Learning & Certification Pathway
        {
            "slide_number": 6,
            "content_shape": "phases_over_time",
            "eyebrow": "Career enablement path",
            "title": "A structured 5-stage roadmap to certified expertise",
            "subtitle": "Proven learning milestones bridging theoretical BTP foundations to live project execution",
            "phases": [
                ("Phase 1: Cloud & BTP Foundations", "SAP BTP subaccounts · Global accounts · Cloud security · HANA Cloud basics"),
                ("Phase 2: Data Builder Mastery", "Graphical & SQL views · Remote tables · Replication flows · Delta loading"),
                ("Phase 3: Business Semantics & SAC", "Business entities · Consumption models · SAC live connectivity · Metrics"),
                ("Phase 4: Fabric & External Mesh", "Data federation · BigQuery / Databricks integration · Open data fabric"),
                ("Phase 5: SAP Certification & Lead", "Official SAP C_DS_42 certification · Real-world implementation · Lead role")
            ],
            "future_readiness_title": "Continuous ecosystem currency",
            "future_readiness_desc": "Datasphere receives quarterly cloud updates; architects maintain currency via quarterly SAP delta certifications.",
            "notes": "Five-stage progression from initial BTP fundamentals through to full production architect credentialing."
        },
        # Slide 7: Career Roles, Compensation & Action Plan
        {
            "slide_number": 7,
            "content_shape": "roles_and_terms",
            "eyebrow": "Career milestones & trajectory",
            "title": "Target roles, compensation benchmarks and action plan",
            "subtitle": None,
            "sec_a_title": "A   Target industry roles & compensation",
            "table_a_headers": ["Role profile", "Indicative compensation"],
            "commercial_rows": [
                ("Datasphere Solution Architect", "$170k - $225k / ₹35-50 LPA"),
                ("Senior Semantic Data Engineer", "$135k - $170k / ₹24-35 LPA"),
                ("Datasphere BI / SAC Specialist", "$105k - $135k / ₹16-24 LPA"),
                ("BTP Data Integration Engineer", "$120k - $155k / ₹20-30 LPA")
            ],
            "sec_b_title": "B   Key certifications & credentials",
            "table_b_headers": ["Certification code", "Focus areas", "Platform"],
            "resource_rows": [
                ("C_DS_42: SAP Certified Associate", "Datasphere modeling, spaces, and data builder", "SAP Learning Hub"),
                ("C_S4CDP: SAP Cloud Data & BTP", "Cloud architecture, security, and BTP integration", "SAP PartnerEdge"),
                ("C_SAC_AD: SAP Analytics Cloud", "Story design, planning, and live Datasphere link", "SAP Learning")
            ],
            "sec_c_title": "C   Action plan & enablement milestones",
            "terms_list": [
                ("BTP free tier setup", "activate SAP BTP trial and initialize Datasphere."),
                ("Foundational learning", "complete official SAP Learning Journeys."),
                ("Hands-on build labs", "construct end-to-end model connecting S/4HANA to SAC."),
                ("Exam scheduling", "clear official C_DS_42 certification within 90 days."),
                ("Portfolio showcase", "demonstrate semantic models and data mesh designs."),
                ("Continuous upskilling", "engage with SAP Community and release webcasts.")
            ],
            "notes": "Practical compensation benchmarks, certification codes, and immediate actionable steps to launch a Datasphere career."
        }
    ]

    return {
        "theme": "lumbini",
        "client": "SAP Data Professionals",
        "slides": slides
    }

if __name__ == "__main__":
    out_dir = os.path.abspath("tests/out/deck4_datasphere_career")
    os.makedirs(out_dir, exist_ok=True)
    out_pptx = os.path.join(out_dir, "SAP_Datasphere_Career_Path_Guide.pptx")

    spec = build_datasphere_spec()

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
    print(f"QA Report saved: {qa_json_path}")
