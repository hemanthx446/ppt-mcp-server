import os
import json
from pipeline.renderer import DeckRenderer
from pipeline.qa import QualityGate
from pipeline.distill import ContentDistiller
from pipeline.visual_plan import VisualPlanner
from pipeline.panel_review import PanelReviewEngine
from design_system.lumbini.tokens import get_lumbini_theme

def build_test_c_spec() -> dict:
    theme = get_lumbini_theme()

    platform_levels = ["Global HQ", "Regional Hub", "Terminal Edge", "Fleet IoT"]

    slides = [
        # Slide 1: Cover
        {
            "slide_number": 1,
            "content_shape": "cover",
            "title": "Enterprise Digital Transformation Strategy",
            "subtitle": "Autonomous Supply Chain, Cloud Modernization & Operating Model 2027-2030  |  Meridian Logistics Global",
            "metadata": [
                ("Enterprise Client", "Meridian Logistics Global (Corporate Strategy)"),
                ("Strategic Focus", "Global TMS/WMS Unification & S/4HANA Cloud"),
                ("Advisory Practice", "Lumbini Strategy & Enterprise Practice"),
                ("Strategic Horizon", "2027 – 2030")
            ],
            "pill_text": "Corporate Strategy  |  Digital Logistics",
            "layout_rationale": "Standard executive presentation cover layout with corporate metadata and strategic pill.",
            "notes": "Comprehensive corporate strategy outlining cloud core modernization and autonomous logistics capabilities."
        },
        # Slide 2: Operational Bottleneck (GRAMMAR: constraint_flow)
        {
            "slide_number": 2,
            "content_shape": "constraint_flow",
            "locator_level": "Terminal Edge",
            "eyebrow": "Operational Constraints",
            "title": "Customs clearance bottleneck across multimodal corridors",
            "subtitle": "Manual tariff verification and yard dwell bind end-to-end container throughput",
            "stages": [
                {"name": "Vessel Discharge", "desc": "Crane container offload.", "rate": "45 boxes/hr"},
                {"name": "Terminal Staging", "desc": "Straddle carrier moves.", "rate": "40 boxes/hr"},
                {"name": "Customs QA (Bottleneck)", "desc": "Document & tariff audit.", "rate": "14 boxes/hr"},
                {"name": "Intermodal Rail", "desc": "Wagon train loading.", "rate": "32 boxes/hr"},
                {"name": "Depot Ingestion", "desc": "Final cross-dock intake.", "rate": "38 boxes/hr"}
            ],
            "constraint_idx": 2,
            "buffer_desc": "Containers piled up before customs clearance, causing severe yard dwell congestion.",
            "impact_annotation": "Subordinating depot dispatch to pre-cleared electronic manifests cuts dwell by 32% [SRC-STRAT-01].",
            "source_id": "SRC-STRAT-01",
            "illustrative": True,
            "layout_rationale": "Chosen 'constraint_flow' to expose the binding bottleneck at customs verification and illustrate buffer subordination.",
            "notes": "Applies Goldratt Theory of Constraints to show that accelerating vessel cranes without customs automation worsens yard gridlock."
        },
        # Slide 3: Submerged Systemic Drivers (GRAMMAR: iceberg_shift)
        {
            "slide_number": 3,
            "content_shape": "iceberg_shift",
            "locator_level": "Regional Hub",
            "eyebrow": "Root Cause Anatomy",
            "title": "Underlying structural drivers beneath demurrage penalties",
            "subtitle": "Fragmented regional operating cultures and disconnected master data create visible losses",
            "visible_event": {
                "title": "Port Demurrage & Customer Churn",
                "desc": "$24.6M annual demurrage fines and corporate customer SLA contract penalties."
            },
            "submerged_layers": [
                {
                    "layer_name": "System Fragmentation",
                    "finding": "14 regional legacy WMS instances operating independent, incompatible product master schemas."
                },
                {
                    "layer_name": "Misaligned Performance Metrics",
                    "finding": "Terminal managers were evaluated solely on berth crane moves rather than end-to-end cycle velocity."
                },
                {
                    "layer_name": "Entrenched Risk Avoidance",
                    "finding": "Customs handlers manually re-verified electronic manifests in spreadsheets to dodge compliance audits."
                }
            ],
            "callout_text": "Transformation occurs only when cloud master data harmonization removes the friction between terminal speed and regulatory accuracy.",
            "source_id": "SRC-STRAT-02",
            "illustrative": True,
            "layout_rationale": "Chosen 'iceberg_shift' to separate visible demurrage losses from deep system fragmentation and behavioral incentives.",
            "notes": "Identifies cultural and architectural root causes behind operational delays."
        },
        # Slide 4: Target Operating Model (GRAMMAR: tradeoff_matrix)
        {
            "slide_number": 4,
            "content_shape": "tradeoff_matrix",
            "locator_level": "Global HQ",
            "eyebrow": "Operating Model",
            "title": "Standardisation versus local terminal agility quadrant",
            "subtitle": "Positioning Meridian as a Coordinated Global Network across Ross operating quadrants",
            "x_axis_title": "Process Standardisation",
            "y_axis_title": "System Integration",
            "quadrants": [
                {
                    "name": "Coordinated Global Network",
                    "desc": "Unified cloud core with automated tariffs, coupled with autonomous regional terminal dispatch.",
                    "is_target": True
                },
                {
                    "name": "Centralized Rigid Command",
                    "desc": "Monolithic headquarter scheduling that strangles local berth adjustments during weather delays.",
                    "is_target": False
                },
                {
                    "name": "Fragmented Island Hubs",
                    "desc": "Legacy baseline: 14 disconnected terminals with monthly spreadsheet reconciliation surprises.",
                    "is_target": False
                },
                {
                    "name": "Loose Regional Alliances",
                    "desc": "Uncoordinated point-to-point APIs without harmonized billing rules or container tracking.",
                    "is_target": False
                }
            ],
            "callout_note": "Global standards govern financial ledgers and customer contracts, while terminal heads retain berth tactical dispatch autonomy.",
            "layout_rationale": "Chosen 'tradeoff_matrix' (Ross Operating Model) to articulate governance boundaries between global standards and local operations.",
            "notes": "Defines strategic operating model alignment across international logistics nodes."
        },
        # Slide 5: Platform Architecture Stack (GRAMMAR: layered_stack)
        {
            "slide_number": 5,
            "content_shape": "layered_stack",
            "locator_level": "Global HQ",
            "eyebrow": "Platform Architecture",
            "title": "Four decoupled tiers of the modern logistics cloud platform",
            "subtitle": "Decoupling high-frequency telematics streams from core financial transaction systems",
            "layers": [
                {
                    "tier": "Tier 4: Enterprise Core",
                    "title": "SAP S/4HANA Cloud (Universal Ledger)",
                    "desc": "Single-source financial billing, automated customs revenue accrual, and global tax compliance.",
                    "color": theme.C_NAVY
                },
                {
                    "tier": "Tier 3: Digital Orchestration",
                    "title": "Logistics Event Streaming Platform",
                    "desc": "Dynamic order booking, multimodal freight TMS, predictive vessel arrival, and carrier dispatch.",
                    "color": theme.C_PRIMARY
                },
                {
                    "tier": "Tier 2: Terminal Edge",
                    "title": "Edge Terminal Controllers & Gateways",
                    "desc": "Automated OCR container gate lanes, crane management telemetry, and local buffer management.",
                    "color": theme.C_PRIMARY
                },
                {
                    "tier": "Tier 1: Telematics & IoT",
                    "title": "Fleet Telemetry & Reefer Sensors",
                    "desc": "Real-time vessel GPS transponders, reefer temperature probes, and smart container seals.",
                    "color": theme.C_MUTED
                }
            ],
            "callout_note": "Decoupled edge architecture guarantees regional container terminals continue operating offline even during global cloud network outages.",
            "layout_rationale": "Chosen 'layered_stack' to demonstrate hierarchical platform tiering with clear transaction and data boundaries.",
            "notes": "Ensures terminal continuity and shields enterprise financial systems from edge event floods."
        },
        # Slide 6: Financial Strategy & Trajectory (GRAMMAR: annotated_chart)
        {
            "slide_number": 6,
            "content_shape": "annotated_chart",
            "locator_level": "Global HQ",
            "eyebrow": "Value Realization",
            "title": "EBITDA margin expansion and unit economics through the transformation",
            "subtitle": "Productivity J-curve dip during cutover precedes sustained 720 bps margin expansion",
            "chart_type": "line",
            "categories": ["2024A Baseline", "2025A Pilot", "2026E Cutover", "2027P Scaling", "2028P Target"],
            "series_data": [
                {"name": "EBITDA Margin (%)", "values": [11.2, 11.8, 10.4, 15.6, 18.4]},
                {"name": "Target Benchmark (%)", "values": [11.5, 12.0, 13.0, 15.0, 17.0]}
            ],
            "chart_title": "Meridian Global EBITDA Margin Trajectory 2024-2028 (%)",
            "x_label": "Fiscal Year",
            "y_label": "EBITDA Margin (%)",
            "key_takeaway": "Planned margin dip in 2026 cutover reflects system cutover stabilization, validating Brynjolfsson's productivity J-curve model before accelerating to 18.4%.",
            "callout_annotation": "Automated customs straight-through processing unlocks $68M net recurring EBITDA uplift and 28% lower unit cost-to-serve [SRC-STRAT-01].",
            "source_id": "SRC-STRAT-01",
            "illustrative": True,
            "layout_rationale": "Chosen 'annotated_chart' to visualize the multi-year financial trajectory from supplied planning data with strict source attribution.",
            "notes": "Demonstrates clear financial ROI and realistic productivity J-curve trajectory."
        },
        # Slide 7: Closed-Loop Network Dynamics (GRAMMAR: causal_loop)
        {
            "slide_number": 7,
            "content_shape": "causal_loop",
            "locator_level": "Terminal Edge",
            "eyebrow": "Systems Dynamics",
            "title": "Reinforcing carrier booking loops and terminal capacity equilibrium",
            "subtitle": "How predictive gate throughput triggers self-reinforcing shipping volume expansion",
            "nodes": [
                {"label": "Dynamic Berth Allocation", "desc": "AI schedules vessel berths based on real-time crane throughput."},
                {"label": "Automated Gate Clearance", "desc": "Optical character recognition clears drayage trucks in 45 seconds."},
                {"label": "Yard Dwell Stabilization", "desc": "Mean container dwell time falls from 5.4 days to 1.8 days [SRC-STRAT-02]."},
                {"label": "Carrier Loyalty Index", "desc": "Tier-1 shipping lines commit long-term guaranteed container volume."}
            ],
            "loops": [
                {"type": "Reinforcing Loop (R1)", "effect": "Faster terminal gate turns attract premier ocean carriers, driving freight booking density."},
                {"type": "Balancing Loop (B1)", "effect": "Peak container surges temporarily strain yard stackers, triggering dynamic congestion surcharges."}
            ],
            "delay_annotation": "4-week algorithmic stabilization delay required to calibrate predictive berth allocation against adverse weather patterns.",
            "source_id": "SRC-STRAT-02",
            "illustrative": True,
            "layout_rationale": "Chosen 'causal_loop' (Senge Systems Thinking) to reveal the self-reinforcing dynamics and capacity balancing mechanisms.",
            "notes": "Explains how operational velocity drives customer retention and commercial pricing power."
        },
        # Slide 8: Governance Matrix & Decision Rights (GRAMMAR: levels_x_dimensions)
        {
            "slide_number": 8,
            "content_shape": "levels_x_dimensions",
            "locator_level": "Global HQ",
            "eyebrow": "Operational Governance",
            "title": "Multi-tier transformation governance and capital decision rights",
            "subtitle": "Synchronizing executive board capital allocation with frontline terminal modernization squads",
            "col_headers": ["Capital Allocation", "Process Harmonization", "Digital Platform SLA"],
            "row_headers": [
                ("Executive Steering", "Digital capital allocation and cross-border M&A technology integration", theme.C_NAVY),
                ("Global Process Owners", "Universal freight tariffs, straight-through customs, and SLA metrics", theme.C_PRIMARY),
                ("Terminal Sprint Squads", "Edge OCR gate deployment, crane dispatch, and trucker mobile apps", theme.C_MUTED)
            ],
            "cells": [
                [
                    "Tranche sign-off for global cloud rollout",
                    "Global hub SLA compliance and margin review",
                    "Consolidated unit cost-to-serve metrics"
                ],
                [
                    "Tariff rule harmonization across 14 hubs",
                    "Customs straight-through processing rates",
                    "Cloud TMS API latency and platform uptime"
                ],
                [
                    "Local gate lane hardware and sensor capex",
                    "Yard crane dispatch sequence adherence",
                    "Edge message broker buffer redundancy"
                ]
            ],
            "caveat_text": "Terminal leads retain berth tactical scheduling; global council governs universal tariff rules.",
            "confirmed_caps": [
                "Universal Ledger Core",
                "Straight-Through Customs",
                "Edge Gate Buffering",
                "Predictive Slotting"
            ],
            "confirmed_title": "Verified Capability Gates",
            "layout_rationale": "Chosen 'levels_x_dimensions' to map cross-tier decision rights and operational responsibilities without ambiguity.",
            "notes": "Establishes institutional accountability across governance layers."
        },
        # Slide 9: Multi-Horizon Roadmap & Boundaries (GRAMMAR: phases_over_time)
        {
            "slide_number": 9,
            "content_shape": "phases_over_time",
            "locator_level": "Global HQ",
            "eyebrow": "Strategic Roadmap",
            "title": "Three-horizon digital transformation roadmap and architectural boundaries",
            "subtitle": "Balancing near-term financial payback with long-term predictive platform capability",
            "phases": [
                ("Horizon 1: Core Unification (M1-12)", "Deploy unified S/4HANA cloud ledger · Harmonize customer & tariff data · Pilot OCR gates"),
                ("Horizon 2: Dynamic Routing (M13-24)", "Roll out enterprise cloud TMS · Straight-through customs filing · Real-time reefer IoT"),
                ("Horizon 3: Ecosystem Platform (M25-36)", "Predictive intermodal dispatch · Carrier self-service booking portal · Carbon API")
            ],
            "future_readiness_title": "Architectural Boundary Conditions",
            "future_readiness_desc": "Requires microservices-compatible Terminal Operating Systems (TOS). Legacy proprietary terminal databases require edge adapters.",
            "source_id": "SRC-STRAT-03",
            "illustrative": True,
            "layout_rationale": "Chosen 'phases_over_time' to define clear execution horizons and prerequisites for ecosystem intelligence.",
            "notes": "Strategic sequencing ensuring self-funding milestone delivery."
        }
    ]

    return {
        "meta": {
            "client": "Meridian Logistics Global",
            "topic": "Corporate Digital Transformation Strategy",
            "confidentiality": "Strategic & Confidential",
            "doc_type": "Executive Strategy Deck",
            "platform_levels": platform_levels,
            "illustrative": True
        },
        "theme": "lumbini",
        "slides": slides
    }

if __name__ == "__main__":
    out_dir = os.path.abspath("tests/out/test_c_strategy_v2")
    os.makedirs(out_dir, exist_ok=True)
    out_pptx = os.path.join(out_dir, "Meridian_Digital_Strategy_v2.pptx")

    glossary = {
        "TMS": "Transportation Management System orchestrating multimodal carrier routing, rating, and load tracking.",
        "WMS": "Warehouse Management System controlling inventory receiving, slotting, and distribution cross-docking.",
        "STP": "Straight-Through Processing enabling touchless electronic customs declarations without human intervention.",
        "TEU": "Twenty-foot Equivalent Unit, standard maritime measure for cargo container capacity.",
        "EBITDA": "Earnings Before Interest, Taxes, Depreciation, and Amortization measuring operational profitability."
    }
    with open(os.path.join(out_dir, "glossary.json"), "w", encoding="utf-8") as f:
        json.dump(glossary, f, indent=2)

    spec = build_test_c_spec()

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

    # 4. Automated Pre-Flight QA Audit
    qa_report = QualityGate.audit_deck(rendered_file, spec, render_images=True, preview_dir=os.path.join(out_dir, "previews"))
    qa_json_path = os.path.join(out_dir, "qa-report.json")
    with open(qa_json_path, "w", encoding="utf-8") as f:
        json.dump(qa_report, f, indent=2)
    print(f"QA Status: {qa_report['status']}, Blocking: {qa_report['blocking_count']}, Warnings: {qa_report['warning_count']}")
    print(f"Anti-Copy Audit: {qa_report['anti_copy_audit']}")

    # 5. Panel Review Gate
    panel_results = PanelReviewEngine.review_deck(rendered_file, storyline=spec, output_report_path=os.path.join(out_dir, "panel-report.md"))
    print(f"Panel Review Gate: {panel_results['panel_gate_status']}, Mean Score: {panel_results['mean_score']}/5.0")
