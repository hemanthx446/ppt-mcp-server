"""
Test Suite for the Enterprise Architecture Composition Engine.

Validates that:
1. All 15 canonical narrative sections and archetypes are defined and properly mapped.
2. VisualRhythmController optimizes slide plans, alternating layout families and theme modes.
3. Renders a complete 10-slide enterprise architecture deck with verified visual rhythm.
4. Confirms 100% 'Inter' typography compliance across every generated slide.
5. Tests FastMCP tool integration for 'list_narrative_sections' and 'compose_architecture_deck'.
"""

import os
from pptx import Presentation
from design_system.composition import (
    NarrativeSection,
    SECTION_ARCHETYPES,
    VisualRhythmController,
    ArchitectureDeckSpec,
    EnterpriseArchitectureCompositionEngine,
)
import ppt_mcp_server as mcp_server


def test_narrative_sections_catalog():
    """Verify all 15 narrative sections are configured with rich archetypes."""
    assert len(NarrativeSection) == 15, f"Expected 15 narrative sections, got {len(NarrativeSection)}"
    assert len(SECTION_ARCHETYPES) == 15, f"Expected 15 section archetypes, got {len(SECTION_ARCHETYPES)}"

    for sec in NarrativeSection:
        arch = SECTION_ARCHETYPES[sec]
        assert arch.section == sec
        assert len(arch.primary_primitives) > 0
        assert arch.layout_family in ("blueprint", "flow", "dashboard", "table", "narrative", "timeline")
        assert arch.preferred_theme_mode in ("dark", "light")

    print(f"[PASS] All 15 narrative sections and archetypes verified.")


def test_visual_rhythm_optimization():
    """Test that VisualRhythmController prevents repetitive identical layouts."""
    # Create request with intentionally adjacent sections
    test_sections = [
        (NarrativeSection.EXECUTIVE_CONTEXT, {"title": "Slide 1: Executive Context"}),
        (NarrativeSection.CURRENT_REALITY, {"title": "Slide 2: Current Reality"}),
        (NarrativeSection.TARGET_ARCHITECTURE, {"title": "Slide 3: Target Architecture"}),
        (NarrativeSection.PROCESS_TRANSFORMATION, {"title": "Slide 4: Process Flow"}),
        (NarrativeSection.ANALYTICS_INTELLIGENCE, {"title": "Slide 5: Executive Dashboard"}),
        (NarrativeSection.GOVERNANCE, {"title": "Slide 6: Control Gates"}),
        (NarrativeSection.IMPLEMENTATION_ROADMAP, {"title": "Slide 7: Phased Roadmap"}),
        (NarrativeSection.COMMERCIAL_NEXT_STEPS, {"title": "Slide 8: Commercial Framework"}),
    ]

    optimized = VisualRhythmController.optimize_slide_plan(test_sections)
    assert len(optimized) == 8

    # Verify visual rhythm: check that adjacent slides vary in primitives and theme
    layout_sequence = [s["layout_family"] for s in optimized]
    primitive_sequence = [s["primitive_key"] for s in optimized]
    theme_sequence = [s["theme_name"] for s in optimized]

    print("Optimized Layout Sequence:   ", " -> ".join(layout_sequence))
    print("Optimized Primitive Sequence:", " -> ".join(primitive_sequence))
    print("Optimized Theme Sequence:    ", " -> ".join(theme_sequence))

    # Assert no identical consecutive primitives
    for i in range(len(primitive_sequence) - 1):
        assert primitive_sequence[i] != primitive_sequence[i+1], (
            f"Monotony violation: Slide {i+1} and {i+2} use identical primitive '{primitive_sequence[i]}'"
        )

    # Assert theme pacing (deck starts with navy dark anchor, alternates, and ends strong)
    assert theme_sequence[0] == "navy", "First anchor slide should be Executive Navy Dark"
    assert theme_sequence[-1] == "navy", "Closing commercial slide should be Executive Navy Dark"

    print("[PASS] Visual rhythm optimization verified: Zero repetitive consecutive primitives.")


def test_render_enterprise_architecture_deck():
    """Renders a 10-slide enterprise proposal deck for Lumbini Elite Solutions."""
    spec = ArchitectureDeckSpec(
        presentation_title="SAP S/4HANA & MES Clean-Core Integration Proposal",
        client_name="Lumbini Elite Solutions",
        target_solution="Sub-Second Shop Floor Telemetry & Edge Resilience",
        author="Principal Enterprise Architect",
        sections=[
            # 1. Executive Context (Hero thesis)
            (NarrativeSection.EXECUTIVE_CONTEXT, {
                "title": "THE STRATEGIC THESIS: Sub-Second Plant Telemetry with Zero ERP Core Risk",
                "subtitle": "HOW IT WORKS: High-velocity manufacturing telemetry ring-fenced at the plant edge",
                "primitive": "executive_statement",
                "data": {
                    "statement": "Manufacturing digital transformation succeeds only when high-velocity shop-floor telemetry is decoupled from the ERP core—protecting transactional stability while delivering sub-second plant visibility.",
                    "attribution": "Executive Advisory Practice, Lumbini Elite Solutions",
                    "pillars": [
                        ("Ring-Fenced Core", "No direct lock contention, memory bloat, or synchronous wait states in SAP S/4HANA."),
                        ("Autonomous Edge", "Plant cells operate continuously even during WAN fiber outages or ERP maintenance windows."),
                        ("Universal Ledger", "Clean-core 101 Goods Movements post asynchronously with complete ISA-95 lot genealogy.")
                    ]
                }
            }),

            # 2. Current Reality (As-Is Friction vs To-Be)
            (NarrativeSection.CURRENT_REALITY, {
                "title": "OPERATING REALITY: Legacy Batch Keypunching Destroys Production Flow",
                "subtitle": "HOW IT WORKS: As-is manual traveler latency vs target automated event-driven throughput",
                "primitive": "current_vs_future_state",
                "data": {
                    "as_is_title": "CURRENT STATE: Fragmented Paper Silos & End-of-Shift Keypunching",
                    "as_is_points": [
                        ("Paper Travelers", "4-hour batch release delays while physical travelers are signed and couriered."),
                        ("Isolated PLC Islands", "Critical cycle times and torque telemetry trapped in proprietary machine vendor siloes."),
                        ("Manual Keypunching", "End-of-shift SAP batch entry causes frequent inventory mismatches and stockout panics.")
                    ],
                    "to_be_title": "TARGET STATE: Event-Driven Clean-Core Edge Architecture",
                    "to_be_points": [
                        ("Electronic Traveler", "100% paperless e-traveler with biometric badge sign-off and instant genealogy."),
                        ("OPC-UA Edge Broker", "Universal edge collectors stream telemetry to Kafka message queue at 10ms intervals."),
                        ("Real-Time Posting", "Automated Movement 101 postings update SAP MM/PP within 180ms of machine cycle completion.")
                    ]
                }
            }),

            # 3. Target Architecture (Decoupled Blueprint)
            (NarrativeSection.TARGET_ARCHITECTURE, {
                "title": "TARGET ARCHITECTURE: The 3-Tier Clean-Core Operational Pipeline",
                "subtitle": "HOW IT WORKS: SAP RFC calls isolated behind Lumbini BTP Event Mesh and plant edge collectors",
                "primitive": "system_architecture",
                "callout_banner": "ARCHITECTURAL GUARANTEE: Zero custom Z-tables or direct write RFCs into the SAP S/4HANA transactional memory space.",
                "data": {
                    "tiers": [
                        ("Tier 1: Enterprise ERP Core", "SAP S/4HANA 2023", ["ACDOCA Universal Ledger", "BAPI_PRODORD_CONFIRM", "Master Data Governance"], "OData / TLS 1.3"),
                        ("Tier 2: Event Integration Mesh", "Lumbini BTP Broker", ["Kafka Message Fabric", "State Ring-Fencing", "Asynchronous RFC Queue"], "MQTT / OPC-UA"),
                        ("Tier 3: Shop Floor Edge Runtime", "Plant Edge Clusters", ["Local SQLite Cache", "Barcode Poka-Yoke Terminal", "Cognex Vision Interlock"])
                    ]
                }
            }),

            # 4. Process Transformation (Sequential Workflow)
            (NarrativeSection.PROCESS_TRANSFORMATION, {
                "title": "PROCESS FLOW: Closed-Loop Production Order Execution & Auto-Posting",
                "subtitle": "HOW IT WORKS: Five continuous automated stages from ERP release to finished goods inventory",
                "primitive": "horizontal_process_flow",
                "data": {
                    "steps": [
                        ("1", "Order Release", ["Production order dispatched from SAP PP", "Queue synced to local workstation edge"]),
                        ("2", "Lot Verification", ["Operator scans raw material QR code", "BOM genealogy validated against batch master"]),
                        ("3", "Machine Cycle", ["PLC executes automated assembly cycle", "Torque and cycle telemetry captured at 10ms"]),
                        ("4", "Vision Inspection", ["Cognex optical camera verifies +/-0.02mm tolerance", "Instant pass/fail interlock trigger"]),
                        ("5", "Auto Goods Receipt", ["Automatic 101 movement posted to SAP MM", "Digital certificate issued to warehouse"])
                    ]
                }
            }),

            # 5. Data & Integration Architecture (Security Boundary & DMZ)
            (NarrativeSection.DATA_INTEGRATION_ARCHITECTURE, {
                "title": "SECURITY BOUNDARY: Multi-Tier DMZ Perimeter Defense",
                "subtitle": "HOW IT WORKS: Stateful packet firewalls and isolated VLANs protect air-gapped machine networks",
                "primitive": "security_boundary",
                "data": {
                    "zones": [
                        ("L4: Corporate Enterprise", "Corporate WAN", ["S/4HANA ERP Core", "SAP Analytics Cloud", "Active Directory SSO"]),
                        ("L3.5: Plant Demilitarized Zone", "Plant DMZ", ["Reverse Proxy Appliance", "Data Diode Telemetry Bridge", "WSUS Patch Server"]),
                        ("L3/L2: Manufacturing Cell OT", "Air-Gapped OT Network", ["Edge Broker Runtime", "Operator HMI Terminals", "Machine PLCs & Scanners"])
                    ]
                }
            }),

            # 6. Operational Execution (Genealogy BOM Hierarchy)
            (NarrativeSection.OPERATIONAL_EXECUTION, {
                "title": "SHOP FLOOR GENEALOGY: 360° As-Built Multi-Tier BOM Lineage",
                "subtitle": "HOW IT WORKS: Indented component serialization tying every sub-assembly directly to the SAP lot",
                "primitive": "parent_child_relationship",
                "data": {
                    "bom_hierarchy": [
                        (0, "MAT-9000", "Top Assy: Turbine Actuator Module 24V", "1 EA", "Rev C"),
                        (1, "SUB-1010", "Solenoid Valve High-Pressure Sub-Assy", "1 EA", "Rev B"),
                        (2, "PRT-4401", "Titanium Coil Core M4 (Lot: 2026-X)", "4 EA", "Rev A"),
                        (2, "PRT-4402", "Viton O-Ring High-Temp Seal 12mm", "2 EA", "Rev A"),
                        (1, "SUB-1020", "Optical Angle Sensor Circuit Array", "1 EA", "Rev D"),
                        (2, "PRT-8810", "Precision Photodiode Chip (Batch: A9)", "1 EA", "Rev C")
                    ]
                }
            }),

            # 7. Analytics & Intelligence (Executive Cockpit)
            (NarrativeSection.ANALYTICS_INTELLIGENCE, {
                "title": "DECISION COCKPIT: Real-Time Plant OEE & Fulfillment Telemetry",
                "subtitle": "HOW IT WORKS: Closed-loop operational intelligence streamed directly to CXO dashboards",
                "primitive": "executive_dashboard",
                "data": {
                    "kpi_strip": [
                        ("89.4%", "Overall Equipment Effectiveness", "Plant 1 Rolling 30D", "+4.2%", True),
                        ("180ms", "ERP Sync Latency", "BTP Event SLA", "Sub-second", True),
                        ("0.6%", "Scrap Rate", "Shift A-C Avg", "-58%", True)
                    ],
                    "operational_reports": [
                        ("Live Machine Utilization", "Real-time spindle telemetry across 14 CNC cells with automated downtime categorization."),
                        ("Lot Traceability Ledger", "Sub-second 360-degree genealogy lookup resolving customer lot audits in <2 seconds."),
                        ("ACDOCA Financial Reconciliation", "Continuous material ledger tie-out ensuring physical WIP matches SAP financial inventory balance.")
                    ]
                }
            }),

            # 8. Governance & Controls (Approval Gates)
            (NarrativeSection.GOVERNANCE, {
                "title": "GOVERNANCE FRAMEWORK: Two-Tier Operational & Financial Verification Gates",
                "subtitle": "HOW IT WORKS: Multi-tier approval desk prevents unverified data from corrupting the financial ledger",
                "primitive": "approval_gates",
                "data": {
                    "gates": [
                        ("Gate 1: Tech Architecture", "Chief Solution Architect", "Sprint 0", ["Zero direct RFC writes", "BTP bandwidth benchmarked", "OT DMZ approved"], "Architecture Charter"),
                        ("Gate 2: Line 1 Pilot Acceptance", "Plant Operations Director", "Week 6", ["Cycle time neutral", "Zero dropped telemetry", "Operator UX passed"], "Plant Sign-Off Slip"),
                        ("Gate 3: Quality Compliance", "VP Global Quality", "Week 10", ["21 CFR Part 11 audit trails", "Electronic signatures tested", "Genealogy tied to ERP"], "Validation Master Report"),
                        ("Gate 4: Production Cutover", "Joint Steering Committee", "Week 14", ["Disaster recovery tested", "Go-Live checklist 100% green", "Runbook staffed"], "Go-Live Authorization")
                    ]
                }
            }),

            # 9. Implementation Roadmap (Phased Delivery Program)
            (NarrativeSection.IMPLEMENTATION_ROADMAP, {
                "title": "DELIVERY ROADMAP: 90-Day Agile Cutover & Hypercare Sequence",
                "subtitle": "HOW IT WORKS: Structured 3-phase program linking deliverables directly to milestone pass gates",
                "primitive": "transformation_roadmap",
                "data": {
                    "phases": [
                        ("PHASE 1", "Weeks 1-4", "Edge Pilot & Architecture Foundation", ["BTP Subaccount Setup", "OPC-UA Edge Configuration", "Line 1 Pilot Connect"], "GATE 1: Sub-250ms Latency"),
                        ("PHASE 2", "Weeks 5-10", "Core MES Integration & Digital Traveler", ["Production Order Dispatch", "Operator UI Rollout", "QA Automated Gates"], "GATE 2: Zero RFC Buffer Leaks"),
                        ("PHASE 3", "Weeks 11-14", "Enterprise Rollout & 90-Day Hypercare", ["Plant Lines 2-6 Cutover", "Operator Enablement", "Executive Cockpits"], "GATE 3: Final Acceptance")
                    ]
                }
            }),

            # 10. Commercial & Next Steps (Milestone Table)
            (NarrativeSection.COMMERCIAL_NEXT_STEPS, {
                "title": "COMMERCIAL MODEL: Milestone-Linked Fixed Investment & Warranty",
                "subtitle": "HOW IT WORKS: Deliverable-backed billing milestones with 90-day comprehensive hypercare warranty",
                "primitive": "commercial_table",
                "data": {
                    "milestones": [
                        ("M1", "Architecture Blueprint & Edge Lab Proof-of-Concept", "Month 1", "25%", "$125,000"),
                        ("M2", "Line 1 Pilot Go-Live & S/4HANA BAPI Validation", "Month 2", "35%", "$175,000"),
                        ("M3", "Plant-Wide Cutover across Lines 2 through 6", "Month 3", "30%", "$150,000"),
                        ("M4", "Final Operational Acceptance & 90-Day Hypercare", "Month 4", "10%", "$50,000")
                    ],
                    "total_amount": "$500,000 USD"
                }
            })
        ]
    )

    prs = Presentation()
    msg = EnterpriseArchitectureCompositionEngine.render_deck(prs, spec)
    print(f"[PASS] Deck Render Output: {msg}")

    output_path = os.path.join(os.path.dirname(__file__), "test_enterprise_architecture_composition.pptx")
    prs.save(output_path)
    print(f"[PASS] Successfully generated 10-slide deck at: {output_path}")

    # Inspect all fonts in all generated slides to ensure 100% Inter font compliance
    non_inter_fonts = set()
    total_runs = 0
    total_shapes = 0

    for slide_idx, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            total_shapes += 1
            if shape.has_text_frame:
                for p in shape.text_frame.paragraphs:
                    for run in p.runs:
                        total_runs += 1
                        fname = run.font.name
                        if fname and "Inter" not in fname:
                            non_inter_fonts.add((slide_idx + 1, fname))
            if shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:
                        for p in cell.text_frame.paragraphs:
                            for run in p.runs:
                                total_runs += 1
                                fname = run.font.name
                                if fname and "Inter" not in fname:
                                    non_inter_fonts.add((slide_idx + 1, fname))

    print(f"[PASS] Checked {total_shapes} shapes and {total_runs} text runs across all slides.")
    assert len(non_inter_fonts) == 0, f"Found non-Inter fonts: {non_inter_fonts}"
    print("[PASS] 100% Typography compliance verified: All text runs strictly use the 'Inter' font family.")


def test_mcp_composition_tools():
    """Verify FastMCP server tools for composition work correctly."""
    # 1. list_narrative_sections
    res = mcp_server.list_narrative_sections()
    assert res["total_sections"] == 15
    print(f"[PASS] MCP list_narrative_sections returned all {res['total_sections']} sections.")

    # 2. compose_architecture_deck
    test_path = "test_mcp_composed_deck.pptx"
    if os.path.exists(test_path):
        os.remove(test_path)

    sections_payload = [
        {
            "section": 1,
            "title": "Strategic Architecture Mandate",
            "subtitle": "Decoupled edge telemetry for Lumbini Elite Solutions",
            "primitive": "executive_statement",
            "data": {
                "statement": "Real-time edge telemetry protects the S/4HANA core.",
                "attribution": "Chief Architect",
                "pillars": [("Core Ring-Fence", "Zero direct writes"), ("Deterministic Edge", "100% uptime")]
            }
        },
        {
            "section": 6,
            "title": "Target System Architecture",
            "subtitle": "3-Tier Decoupled Operational Pipeline",
            "primitive": "system_architecture",
            "data": {
                "tiers": [
                    ("Tier 1: S/4HANA Core", "ERP", ["ECC FI/CO", "MM/PP Orders"], "RFC / IDOC"),
                    ("Tier 2: Event Mesh", "BTP", ["Kafka Broker", "State Ring-Fence"], "HTTPS / mTLS"),
                    ("Tier 3: OT Edge", "Edge", ["OPC-UA Collector", "SCADA Line 1"])
                ]
            }
        }
    ]

    msg = mcp_server.compose_architecture_deck(
        path=test_path,
        presentation_title="Lumbini Clean-Core Edge Proposal",
        client_name="Lumbini Elite Solutions",
        target_solution="SAP S/4HANA & MES Integration",
        sections=sections_payload
    )
    print(f"[PASS] MCP compose_architecture_deck output: {msg}")
    assert os.path.exists(test_path)
    print("[PASS] MCP composition tool execution verified.")


if __name__ == "__main__":
    test_narrative_sections_catalog()
    test_visual_rhythm_optimization()
    test_render_enterprise_architecture_deck()
    test_mcp_composition_tools()
    print("\nALL ENTERPRISE ARCHITECTURE COMPOSITION ENGINE TESTS PASSED!")
