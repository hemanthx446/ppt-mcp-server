import os
import json
from pipeline.renderer import DeckRenderer
from pipeline.qa import QualityGate
from pipeline.distill import ContentDistiller
from pipeline.visual_plan import VisualPlanner
from pipeline.nexus_research import NexusResearchEngine
from pipeline.panel_review import PanelReviewEngine
from design_system.lumbini.tokens import get_lumbini_theme

def build_test_b_spec() -> dict:
    theme = get_lumbini_theme()

    platform_levels = ["Enterprise L4", "Plant MES L3", "Line L2", "Cell L1"]

    slides = [
        # Slide 1: Cover
        {
            "slide_number": 1,
            "content_shape": "cover",
            "title": "Deconstructing Discrete Plant Modernization",
            "subtitle": "Reconstructing the ISA-95 Shop-Floor to Cloud Ledger Integration  |  Apex Precision Machining",
            "metadata": [
                ("Enterprise Case", "Apex Precision Machining Corp. (Illustrative Reconstruction)"),
                ("Domain Context", "ISA-95 Discrete Manufacturing & S/4HANA Cloud"),
                ("Prepared by", "Lumbini Elite Solutions & Services"),
                ("Date", "November 2026")
            ],
            "pill_text": "Transformation Reconstruction  |  ISA-95",
            "layout_rationale": "Standard executive presentation cover layout with case metadata and category pill.",
            "notes": "Executive analysis reconstructing the organizational and technical mechanics of an ISA-95 shop-floor to S/4HANA transformation."
        },
        # Slide 2: The Fallacy of Machine Speed vs Binding Constraint (GRAMMAR: constraint_flow)
        {
            "slide_number": 2,
            "content_shape": "constraint_flow",
            "locator_level": "Line L2",
            "eyebrow": "Theory of Constraints",
            "title": "Machine speed fallacy versus the binding constraint",
            "subtitle": "Inspection queue forms the binding constraint across titanium production cells",
            "stages": [
                {"name": "Billet Prep", "desc": "Raw titanium sawing.", "rate": "42 units/hr"},
                {"name": "5-Axis Milling", "desc": "High-speed milling.", "rate": "38 units/hr"},
                {"name": "CMM QA (Bottleneck)", "desc": "Dimensional audit.", "rate": "14 units/hr"},
                {"name": "Deburr & Clean", "desc": "Rotary finishing.", "rate": "28 units/hr"},
                {"name": "Assembly", "desc": "Final unit assembly.", "rate": "32 units/hr"}
            ],
            "constraint_idx": 2,
            "buffer_desc": "WIP piled up before CMM inspection, creating batch congestion.",
            "impact_annotation": "Subordinating milling cadence to CMM buffers cut active WIP by 38% [SRC-MFG-01].",
            "source_id": "SRC-MFG-01",
            "illustrative": True,
            "layout_rationale": "Chosen 'constraint_flow' to expose the binding bottleneck at CMM inspection and demonstrate throughput subordination.",
            "notes": "Applies Goldratt Theory of Constraints to demonstrate that optimizing non-constraints worsened WIP batch queuing."
        },
        # Slide 3: What Was Really Broken Beneath the Surface (GRAMMAR: iceberg_shift)
        {
            "slide_number": 3,
            "content_shape": "iceberg_shift",
            "locator_level": "Plant MES L3",
            "eyebrow": "Root Cause Reconstruction",
            "title": "What was really broken beneath the scrap rate symptoms",
            "subtitle": "Split shift incentives and delayed accounting drove hidden defects",
            "visible_event": {
                "title": "Unplanned Rework & Late Deliveries",
                "desc": "Component rejection (8.4% scrap) and customer expediting surcharges."
            },
            "submerged_layers": [
                {
                    "layer_name": "Incentive Structures & Metrics",
                    "finding": "Machinists were evaluated solely on spindle uptime, encouraging cutting with worn inserts."
                },
                {
                    "layer_name": "Information Asymmetry",
                    "finding": "Handwritten paper travellers delayed defect discovery until quality control."
                },
                {
                    "layer_name": "Mental Models of Blame",
                    "finding": "Defects were treated as machinist errors rather than tool vibration drift."
                }
            ],
            "callout_text": "Transformation occurred only when real-time tool telemetry removed the conflict between shift speed and part precision.",
            "source_id": "SRC-MFG-02",
            "illustrative": True,
            "layout_rationale": "Chosen 'iceberg_shift' to separate visible scrap symptoms from deep misaligned incentives and information asymmetry.",
            "notes": "Reveals the organizational dynamics and perverse incentives underlying operational scrap rates."
        },
        # Slide 4: Target ISA-95 Platform Stack (GRAMMAR: layered_stack)
        {
            "slide_number": 4,
            "content_shape": "layered_stack",
            "locator_level": "Enterprise L4",
            "eyebrow": "Target Architecture",
            "title": "The four decoupled layers of the target manufacturing stack",
            "subtitle": "Isolating high-frequency machine telemetry from the universal cloud core",
            "layers": [
                {
                    "tier": "Level 4: Enterprise",
                    "title": "SAP S/4HANA Cloud (ACDOCA Core)",
                    "desc": "Universal Journal real-time financial posting and supplier orchestration.",
                    "color": theme.C_NAVY
                },
                {
                    "tier": "Level 3: Plant MES",
                    "title": "MES Execution Engine",
                    "desc": "Job order routing, serial genealogy tracking, and digital scrap sign-off.",
                    "color": theme.C_PRIMARY
                },
                {
                    "tier": "Level 2: Supervisory",
                    "title": "Line Edge Gateways (OPC-UA)",
                    "desc": "Machine state aggregation and automated tool offset feedback.",
                    "color": theme.C_PRIMARY
                },
                {
                    "tier": "Level 1/0: Machine Cells",
                    "title": "CNC PLCs & Vibration Probes",
                    "desc": "Spindle load cells and closed-loop CNC controller offsets.",
                    "color": theme.C_MUTED
                }
            ],
            "callout_note": "Rigorous ISA-95 boundary isolation guarantees shop-floor machine control continues buffering locally during cloud network outages.",
            "layout_rationale": "Chosen 'layered_stack' to formally map ISA-95 levels 0 to 4 with bidirectional data and control flow guarantees.",
            "notes": "Decoupled architecture preventing plant floor latencies from impacting enterprise financial transactions."
        },
        # Slide 5: Strategic Operating Model Alignment (GRAMMAR: tradeoff_matrix)
        {
            "slide_number": 5,
            "content_shape": "tradeoff_matrix",
            "locator_level": "Plant MES L3",
            "eyebrow": "Operating Model",
            "title": "Standardisation versus local agility quadrant",
            "subtitle": "Balancing universal ledger governance with plant-floor machining autonomy",
            "x_axis_title": "Process Standardisation",
            "y_axis_title": "System Integration",
            "quadrants": [
                {
                    "name": "Coordinated Digital Enterprise",
                    "desc": "Unified ACDOCA ledger with autonomous plant execution and shared telemetry.",
                    "is_target": True
                },
                {
                    "name": "Centralized Rigid Core",
                    "desc": "Top-down batch controls that strangle agility and delay tool adjustments.",
                    "is_target": False
                },
                {
                    "name": "Siloed Island Plants",
                    "desc": "Independent spreadsheets, disconnected MES servers, and month-end surprises.",
                    "is_target": False
                },
                {
                    "name": "Federated Loose Links",
                    "desc": "Lightweight API reporting without reconciled master data or synced lots.",
                    "is_target": False
                }
            ],
            "callout_note": "Standardized universal ledger and materials, while plant teams retain local machine tool autonomy.",
            "layout_rationale": "Chosen 'tradeoff_matrix' (Ross operating model framework) to define enterprise governance versus localized plant execution boundaries.",
            "notes": "Frames the strategic operating model decision governing standardisation and integration."
        },
        # Slide 6: Closed-Loop System Dynamics (GRAMMAR: causal_loop)
        {
            "slide_number": 6,
            "content_shape": "causal_loop",
            "locator_level": "Line L2",
            "eyebrow": "Systems Thinking",
            "title": "Reinforcing quality feedback loops and systemic stabilization delays",
            "subtitle": "How automated tool compensation triggered initial finishing delays before establishing equilibrium",
            "nodes": [
                {"label": "Tool Vibration Telemetry", "desc": "Sensors detect chatter before dimensional drift occurs."},
                {"label": "Automated Offset Correction", "desc": "Edge gateway pulses offset adjustments to CNC G-code."},
                {"label": "First-Pass Part Precision", "desc": "Machined tolerances remain locked within 5-micron bounds."},
                {"label": "Inspection Queue Cadence", "desc": "CMM sampling shifts from 100% sorting to statistical audit [SRC-MFG-03]."}
            ],
            "loops": [
                {"type": "Reinforcing Loop (R1)", "effect": "Accurate milling telemetry improves CMM clearance speed, accelerating shift throughput."},
                {"type": "Balancing Loop (B1)", "effect": "Initial sensor threshold tuning caused false alarms, temporarily pausing line spindle cycles."}
            ],
            "delay_annotation": "3-week stabilization delay required to train neural vibration filters against shop-floor thermal noise.",
            "source_id": "SRC-MFG-03",
            "illustrative": True,
            "layout_rationale": "Chosen 'causal_loop' (Senge systems framework) to map the dynamic feedback loops and delayed stabilization curve.",
            "notes": "Demonstrates systemic interactions where interventions initially increase friction before producing sustained compounding gains."
        },
        # Slide 7: Near-Misses, Failure Modes and Counterfactuals (GRAMMAR: requirement_to_outcome)
        {
            "slide_number": 7,
            "content_shape": "requirement_to_outcome",
            "locator_level": "Plant MES L3",
            "eyebrow": "Failure Mode Analysis",
            "title": "Three near-miss failure modes and engineered mitigations",
            "subtitle": "Points where the digital transformation nearly collapsed during factory cutover",
            "headers": ["CRITICAL RISK POINT", "NEAR-FAILURE MECHANISM", "ENGINEERED MITIGATION"],
            "items": [
                {
                    "title": "Shop-Floor Network Drops",
                    "today": "Factory Wi-Fi dead zones caused CNC controllers to freeze when buffering cloud REST payloads.",
                    "outcome": "Deployed localized edge MQTT brokers buffering up to 72 hours of telemetry completely offline.",
                    "badge_color": theme.C_ALERT
                },
                {
                    "title": "Operator Tool Override",
                    "today": "Machinists distrusted automated offset suggestions and reverted to manual override knobs.",
                    "outcome": "Paired shift leads with automation engineers, demonstrating tool life extension before locking G-code.",
                    "badge_color": theme.C_ACCENT
                },
                {
                    "title": "Month-End Ledger Lockout",
                    "today": "First mock cutover triggered 1,200 unresolved WIP cost variances in SAP universal journal.",
                    "outcome": "Automated sub-second settlement rules on MES job order completion, eliminating batch backlogs.",
                    "badge_color": theme.C_PRIMARY
                }
            ],
            "layout_rationale": "Chosen 'requirement_to_outcome' with customized risk headers to systematically analyze transformation failure modes.",
            "notes": "Analyzes real-world failure modes and architectural counterfactuals that nearly derailed deployment."
        },
        # Slide 8: Empirical Production Recovery (GRAMMAR: annotated_chart)
        {
            "slide_number": 8,
            "content_shape": "annotated_chart",
            "locator_level": "Enterprise L4",
            "eyebrow": "Productivity J-Curve",
            "title": "Empirical first-pass yield recovery through the transformation J-curve",
            "subtitle": "Production output experienced an 8-week dip during sensor calibration before surging to target levels",
            "chart_type": "line",
            "categories": ["M1 Pre-Cutover", "M2 Cutover Dip", "M3 Calibration", "M4 Equilibrium", "M5 Expansion"],
            "series_data": [
                {"name": "First-Pass Yield (%)", "values": [87.2, 83.4, 88.9, 94.8, 96.2]},
                {"name": "Target Plan (%)", "values": [90.0, 91.0, 92.0, 93.0, 94.0]}
            ],
            "chart_title": "Discrete Plant First-Pass Component Yield Trend (%)",
            "x_label": "Transformation Month",
            "y_label": "Yield (%)",
            "key_takeaway": "Yield declined 3.8% during Month 2 cutover due to operator learning curves and sensor tuning, validating Brynjolfsson's productivity J-curve hypothesis.",
            "callout_annotation": "Compounding returns manifested in Month 4, raising first-pass yield to 96.2% and reducing annual plant scrap cost by $1.42M across titanium milling lines.",
            "source_id": "SRC-MFG-02",
            "illustrative": True,
            "layout_rationale": "Chosen 'annotated_chart' to visualize the empirical J-curve recovery trajectory with verified source attribution.",
            "notes": "Proves the productivity J-curve with empirical production telemetry."
        },
        # Slide 9: Stakeholder Governance & Accountability (GRAMMAR: levels_x_dimensions)
        {
            "slide_number": 9,
            "content_shape": "levels_x_dimensions",
            "locator_level": "Enterprise L4",
            "eyebrow": "Operational Governance",
            "title": "Multi-tier operational governance and decision accountability",
            "subtitle": "Synchronizing shift leads with executive board capital oversight",
            "col_headers": ["Tooling Offsets", "Line Cadence (OEE)", "ACDOCA Financials"],
            "row_headers": [
                ("Executive Steering", "Plant capital return and scrap accruals", theme.C_NAVY),
                ("Plant Operations Lead", "Buffer health and tooling budget", theme.C_PRIMARY),
                ("Shift Cell Supervisor", "CNC spindle alarms and scrap sign-off", theme.C_MUTED)
            ],
            "cells": [
                [
                    "Capex allocation for machine fleet expansion",
                    "Plant OEE benchmark vs industry baseline",
                    "Consolidated gross margins and warranty reserves"
                ],
                [
                    "Tool wear budget and vendor rating",
                    "CMM inspection queue depth and shift logs",
                    "WIP variance in universal journal ledger"
                ],
                [
                    "Spindle alarm override authorizations",
                    "Hourly piece counts vs schedule target",
                    "Real-time digital scrap reason code sign-off"
                ]
            ],
            "caveat_text": "Shop supervisors control machine offsets; steering committees control capital sizing.",
            "confirmed_caps": [
                "ACDOCA settlement",
                "Edge MQTT buffering",
                "Tool offset feedback",
                "Scrap genealogy"
            ],
            "confirmed_title": "Verified Operational Control Gates",
            "layout_rationale": "Chosen 'levels_x_dimensions' to map stakeholder authority across operational, technical, and financial planes.",
            "notes": "Governance matrix defining operational rights and accountability."
        },
        # Slide 10: Scaling Horizons & Boundary Conditions (GRAMMAR: phases_over_time)
        {
            "slide_number": 10,
            "content_shape": "phases_over_time",
            "locator_level": "Enterprise L4",
            "eyebrow": "Strategic Outlook",
            "title": "Scaling roadmap and explicit boundary conditions",
            "subtitle": "Rollout sequence across remaining machining plants and replication criteria",
            "phases": [
                ("Stage 1: Plant #2 Baseline", "Freeze CNC milling telemetry · Calibrate thresholds · 95% yield [SRC-MFG-04]"),
                ("Stage 2: Tool Auto-Replenish", "Trigger supplier purchase orders when tool magazine drops below buffer"),
                ("Stage 3: Fleet Rollout", "Deploy validated ISA-95 edge containers to Plant #3 and #4 cells"),
                ("Stage 4: OEM Digital Thread", "Expose component genealogy travelers to aerospace OEM clients"),
                ("Stage 5: Autonomous Sched", "Dynamic job rescheduling based on predictive machine tool health")
            ],
            "future_readiness_title": "Boundary Condition for Replication",
            "future_readiness_desc": "Requires CNC machine controllers with open digital interfaces (OPC-UA / MTConnect). Legacy analog machines require gateway retrofits.",
            "source_id": "SRC-MFG-04",
            "illustrative": True,
            "layout_rationale": "Chosen 'phases_over_time' to articulate the multi-plant scaling sequence paired with explicit architectural boundary conditions.",
            "notes": "Final strategic decision slide outlining multi-plant expansion and non-applicability boundaries."
        }
    ]

    return {
        "meta": {
            "client": "Apex Precision Machining Corp.",
            "topic": "Discrete Manufacturing ISA-95 Transformation",
            "confidentiality": "Architectural Reconstruction",
            "doc_type": "Executive Transformation Analysis",
            "platform_levels": platform_levels,
            "illustrative": True
        },
        "theme": "lumbini",
        "slides": slides
    }

if __name__ == "__main__":
    out_dir = os.path.abspath("tests/out/test_b_manufacturing_v2")
    os.makedirs(out_dir, exist_ok=True)
    out_pptx = os.path.join(out_dir, "Apex_Manufacturing_Transformation_v2.pptx")

    glossary = {
        "ISA-95": "International standard defining boundaries between enterprise ERP (L4), plant MES (L3), line SCADA (L2), and machine control (L1/0).",
        "ACDOCA": "The Universal Journal single source of financial and controlling truth in SAP S/4HANA.",
        "MES": "Manufacturing Execution System managing shop-floor dispatching, work order tracking, and serial genealogy.",
        "CMM": "Coordinate Measuring Machine performing high-precision dimensional quality verification.",
        "OEE": "Overall Equipment Effectiveness evaluating machine Availability, Performance, and Quality yield."
    }
    with open(os.path.join(out_dir, "glossary.json"), "w", encoding="utf-8") as f:
        json.dump(glossary, f, indent=2)

    spec = build_test_b_spec()

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

    # 5. Panel Review Gate
    panel_results = PanelReviewEngine.review_deck(rendered_file, storyline=spec, output_report_path=os.path.join(out_dir, "panel-report.md"))
    print(f"Panel Review Gate: {panel_results['panel_gate_status']}, Mean Score: {panel_results['mean_score']}/5.0")
