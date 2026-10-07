"""
Generate Representative PPTX Decks for Production-Readiness Review.

Generates 7 representative presentations:
1. representative_architecture.pptx
2. representative_process.pptx
3. representative_dashboard.pptx
4. representative_table.pptx
5. representative_roadmap.pptx
6. representative_governance.pptx
7. representative_complete_enterprise_solution.pptx
"""

import os
from pptx import Presentation
from pptx.util import Inches

from design_system.spacing import CanvasBounds, Margins, SpacingScale
from design_system.color import ExecutiveNavyTheme, ConsultingSlateTheme
from design_system.primitives import HeaderPrimitive, FooterPrimitive
from design_system.quality_gate import PresentationQualityGate
from design_system.scenario_engine import ScenarioPresentationEngine
import design_system.library as lib


def build_deck(filename, title, client, slides_data):
    prs = Presentation()
    prs.slide_width = Inches(CanvasBounds.width)
    prs.slide_height = Inches(CanvasBounds.height)
    blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]

    total_slides = len(slides_data)
    for idx, (cat_tag, slide_title, subtitle, is_dark, prim_cls, kwargs) in enumerate(slides_data, start=1):
        theme = ExecutiveNavyTheme if is_dark else ConsultingSlateTheme
        slide = prs.slides.add_slide(blank_layout)

        # Background
        from pptx.enum.shapes import MSO_SHAPE
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(CanvasBounds.width), Inches(CanvasBounds.height))
        bg.fill.solid()
        bg.fill.fore_color.rgb = theme.canvas
        bg.line.fill.background()

        # Header
        HeaderPrimitive.render(
            slide=slide,
            category_text=f"{idx}. {cat_tag}",
            title_text=slide_title,
            subtitle_text=subtitle,
            theme=theme
        )

        # Footer
        FooterPrimitive.render(
            slide=slide,
            slide_num=idx,
            total_slides=total_slides,
            metadata_text=f"{client} • {title} • Enterprise Architecture Advisory",
            theme=theme
        )

        # Primitive
        left = Margins.left
        top = SpacingScale.CONTENT_TOP
        width = Margins().usable_width
        height = SpacingScale.CONTENT_HEIGHT

        call_kwargs = dict(kwargs)
        call_kwargs["slide"] = slide
        call_kwargs["left"] = left
        call_kwargs["top"] = top
        call_kwargs["width"] = width
        call_kwargs["height"] = height
        call_kwargs["theme"] = theme

        prim_cls.render(**call_kwargs)

    report = PresentationQualityGate.audit_and_remediate(prs, auto_remediate=True)
    prs.save(filename)
    print(f"[GENERATED] {filename}: {total_slides} slides | Quality Score: {report.overall_quality_score}/100 | Status: {report.status.name}")
    return report


def generate_all_representative_decks():
    from design_system.library.architecture import ArchTierData

    # 1. ARCHITECTURE
    arch_slides = [
        (
            "SYSTEM ARCHITECTURE",
            "Multi-Tier Decoupled Clean-Core Architecture",
            "Preserving S/4HANA financial core integrity via event-driven edge decoupling.",
            True,
            lib.SystemArchitecturePrimitive,
            {
                "tiers": [
                    ArchTierData(tier_name="Tier 1: Enterprise ERP Core", subtitle="SAP S/4HANA Cloud (Clean Core)", subsystems=["PP Production Orders", "MM Material Master", "ACDOCA Financial Ledger"], protocol_to_next="Business Event Mesh / OData"),
                    ArchTierData(tier_name="Tier 2: Event Mesh & Integration", subtitle="SAP BTP Middleware Fabric", subsystems=["Kafka Message Broker", "API Gateway", "Dead-Letter Buffer"], protocol_to_next="mTLS / OPC-UA / REST"),
                    ArchTierData(tier_name="Tier 3: Manufacturing Operations", subtitle="Digital Manufacturing (MES) & Edge", subsystems=["Shopfloor Dispatcher", "Unit Genealogy Engine", "Line SCADA Collector"])
                ]
            }
        ),
        (
            "INTEGRATION TOPOLOGY",
            "Event-Driven Telemetry Ingestion Pipeline",
            "Sub-second event dispatch from machine sensors to ERP with zero ledger polling.",
            False,
            lib.IntegrationArchitecturePrimitive,
            {
                "producer_info": ("Event Producers (Shopfloor & ERP)", ["CNC Machine PLCs", "Inline Vision Cameras", "Operator Barcode Scanners", "Automated Guided Vehicles"]),
                "broker_info": ("SAP BTP Event Mesh & Kafka Fabric", ["Kafka Message Fabric", "API Management Gateway", "Dead-Letter Buffer"], "Pub/Sub Event Streaming"),
                "consumer_info": ("Subscribers & Consumers", ["Digital Manufacturing MES", "Quality Historian DB", "SAP S/4HANA (101 Postings)", "CXO Control Tower"])
            }
        ),
        (
            "SECURITY BOUNDARIES",
            "Zoned Defense-in-Depth & Air-Gapped OT Perimeters",
            "Strict network segmentation isolates plant floor execution from public cyber perimeters.",
            True,
            lib.SecurityBoundaryPrimitive,
            {
                "zones": [
                    ("Zone 1: Corporate Enterprise", "Corporate WAN", ["S/4HANA ERP", "Azure AD Identity", "Corporate Analytics"]),
                    ("Zone 2: Industrial DMZ", "Perimeter Defense", ["Reverse Proxy Gateway", "Patch Staging Server", "Data Diode Collector"]),
                    ("Zone 3: Manufacturing Operations", "Air-Gapped OT", ["MES Execution Node", "SCADA Historian", "Batch Manager"]),
                ]
            }
        )
    ]
    build_deck("representative_architecture.pptx", "Enterprise Architecture Specification", "Lockheed Martin", arch_slides)

    # 2. PROCESS
    process_slides = [
        (
            "VALUE STREAM",
            "Closed-Loop Production Execution Flow",
            "Eliminating paper traveler latency from production release to goods receipt.",
            False,
            lib.HorizontalProcessFlowPrimitive,
            {
                "steps": [
                    ("1", "Order Release", ["Production order released in S/4HANA", "Dispatched to plant queue"]),
                    ("2", "Component Kitting", ["Barcode verified against BOM", "Serialized lot confirmation"]),
                    ("3", "Assembly Run", ["Torque telemetry tracked live", "Cycle time logged at edge"]),
                    ("4", "Automated QA", ["Inline vision camera inspection", "Dimensional tolerance verified"]),
                    ("5", "Goods Receipt", ["Auto 101 posting in S/4HANA", "Finished goods inventory ready"]),
                ]
            }
        ),
        (
            "SHOP-FLOOR WORKFLOW",
            "Frontline Operator Journey with Poka-Yoke Interlocks",
            "Deterministic digital work instructions eliminate human assembly errors.",
            True,
            lib.OperationalWorkflowPrimitive,
            {
                "stations": [
                    ("10", "Inbound Kit Verification", "Operator scans component traveler barcode against ERP BOM", "Barcode mismatch interlock halts carrier"),
                    ("20", "Robotic Cell Assembly", "Automated cell executes precision torque sequence with telemetry", "Temperature parameter drift triggers alert"),
                    ("30", "Laser Direct Part Marking", "Permanent 2D DataMatrix serial UID etched onto titanium chassis", "High-res optical camera verifies scan contrast"),
                    ("40", "End-of-Line Quality Gate", "Automated electrical resistance and pneumatic leak testing", "Defect failure locks output nest and posts NCR"),
                ]
            }
        ),
        (
            "EXCEPTION & REWORK",
            "Automated NCR Logging & Non-Conformance Quarantine",
            "Defective components are automatically locked and rerouted to authorized rework bays.",
            False,
            lib.ExceptionReworkFlowPrimitive,
            {
                "standard_steps": ["Component Kitting", "Torque Assembly", "Automated QC Test", "Packaging & Dispatch"],
                "exception_trigger": "Torque angle out of specification (+/- 3.5 deg tolerance breach)",
                "rework_steps": ["Quarantine Unit to MRB Nest", "Scan Technician Badge", "Disassemble Fasteners", "Re-Torque & Re-Test"]
            }
        )
    ]
    build_deck("representative_process.pptx", "Manufacturing Process Architecture", "Boeing Commercial Airplanes", process_slides)

    # 3. DASHBOARD
    dashboard_slides = [
        (
            "EXECUTIVE COCKPIT",
            "Plant Performance & Operational KPI Strip",
            "Real-time operational telemetry across OEE, quality yield, and inventory latency.",
            True,
            lib.KPIStripPrimitive,
            {
                "kpis": [
                    ("92.4%", "Overall Equipment Effectiveness", "Plant Target: 90.0%", "+2.4% vs Benchmark", True),
                    ("99.2%", "First Pass Quality Yield", "Inline Vision Gates", "+1.8% Improvement", True),
                    ("1.2%", "Unplanned Machine Downtime", "Monthly Rolling Avg", "-48% Reduction", True),
                    ("220ms", "Shop-Floor ERP Sync Latency", "BTP Event SLA", "Sub-Second Verified", True),
                ]
            }
        ),
        (
            "BOTTLENECK ANALYSIS",
            "Work-Center Capacity Loading vs. Production Demand",
            "Identifying binding operational constraints before work order release.",
            False,
            lib.CapacityVsDemandPrimitive,
            {
                "work_centers": [
                    ("WC-101 CNC Machining", 450.0, 530.0),
                    ("WC-204 Robotic Welding", 400.0, 360.0),
                    ("WC-305 Final Assembly", 500.0, 440.0),
                    ("WC-408 Quality Inspection", 300.0, 380.0),
                ]
            }
        ),
        (
            "PARETO ANALYSIS",
            "Pareto 80/20 Root-Cause Defect Concentration",
            "Targeting the top two failure modes eliminates 80% of manufacturing rework.",
            True,
            lib.ParetoPrimitive,
            {
                "items": [
                    ("Torque Calibration Drift", 52.0),
                    ("Component Kitting Mismatch", 28.0),
                    ("Barcode Camera Read Error", 11.0),
                    ("Operator Delay", 6.0),
                    ("Other Minor Exceptions", 3.0),
                ]
            }
        ),
        (
            "EXCEPTION REGISTER",
            "Action-Oriented Plant Floor Corrective Actions",
            "Assigned mitigation owners, priority ratings, and due dates.",
            False,
            lib.ActionRegisterPrimitive,
            {
                "actions": [
                    ("ACT-01", "Recalibrate torque load cells on Station 20", "Maintenance", "HIGH", "Lead Tech", "Week 2", "IN PROGRESS"),
                    ("ACT-02", "Implement automated ASN barcode validation in ERP", "Integration", "HIGH", "BTP Lead", "Week 3", "OPEN"),
                    ("ACT-03", "Conduct operator Poka-Yoke ergonomics review", "Plant Ops", "MED", "Supervisor", "Week 4", "OPEN"),
                    ("ACT-04", "Publish updated First Pass Yield dashboard to CXO", "Analytics", "MED", "Data Arch", "Week 1", "COMPLETED"),
                ]
            }
        )
    ]
    build_deck("representative_dashboard.pptx", "CXO Manufacturing Control Tower", "Hitachi Energy", dashboard_slides)

    # 4. TABLE
    table_slides = [
        (
            "SCOPE MATRIX",
            "Turnkey Implementation Scope & Boundary Matrix",
            "Clear demarcations of advisory deliverables vs. client prerequisites.",
            False,
            lib.ComparisonMatrixPrimitive,
            {
                "options": ["In-Scope (Turnkey)", "Client Responsibility", "Out-of-Scope (Phase 2)"],
                "criteria": [
                    ("SAP BTP Event Mesh Setup", ["FULL (Turnkey)", "PARTIAL (Access)", "NO"]),
                    ("OPC-UA Machine Telemetry", ["FULL (Turnkey)", "PARTIAL (Network)", "NO"]),
                    ("Electronic Batch Records", ["FULL (Turnkey)", "PARTIAL (SOP Sign-off)", "NO"]),
                    ("Multi-Site Cloud Rollout", ["NO", "NO", "RECOMMENDED"]),
                ]
            }
        ),
        (
            "COMMERCIAL MODEL",
            "Milestone Invoicing Schedule & Payment Gates",
            "Fixed-price engagement with payments tied strictly to certified deliverables.",
            True,
            lib.CommercialTablePrimitive,
            {
                "milestones": [
                    ("Phase 1: Architecture Blueprint", "Architecture blueprint & security sign-off", "Weeks 1-3", "25%", "$85,000"),
                    ("Phase 2: Pilot Implementation", "Pilot line integration & telemetry validation", "Weeks 4-8", "35%", "$119,000"),
                    ("Phase 3: Plant Rollout", "Full plant cutover & operator enablement", "Weeks 9-14", "30%", "$102,000"),
                    ("Phase 4: Final Acceptance", "30-day hypercare completion & ledger audit", "Weeks 15-16", "10%", "$34,000"),
                ],
                "total_amount": "$340,000 Turnkey Fixed Investment"
            }
        ),
        (
            "RISK REGISTER",
            "Enterprise Risk Mitigation & Contingency Radar",
            "Quantified severity and pre-engineered hedging strategies.",
            False,
            lib.RiskRegisterPrimitive,
            {
                "risks": [
                    ("RSK-01", "OT firewall change freeze delays pilot line connect", "HIGH", "MED", "CRITICAL", "Pre-authorize security exceptions via ARB charter", "CISO"),
                    ("RSK-02", "Legacy PLC firmware incompatible with OPC-UA daemon", "MED", "LOW", "MODERATE", "Deploy industrial edge protocol translation gateway", "OT Lead"),
                    ("RSK-03", "Operator pushback against biometric sign-off", "LOW", "MED", "LOW", "Provide RFID badge tap alternative with supervisor PIN", "HR Lead"),
                ]
            }
        )
    ]
    build_deck("representative_table.pptx", "Enterprise Structured Tables", "Siemens Energy", table_slides)

    # 5. ROADMAP
    roadmap_slides = [
        (
            "TRANSFORMATION ROADMAP",
            "Phased Agile Rollout & Milestone Gate Schedule",
            "De-risking enterprise cutover through incremental multi-plant waves.",
            False,
            lib.TransformationRoadmapPrimitive,
            {
                "phases": [
                    ("PHASE 1", "Weeks 1-4", "Blueprint & Edge Setup", ["OPC-UA Edge Config", "SAP BTP Subaccount Setup", "Pilot Line Connect"], "GATE 1: Latency <250ms"),
                    ("PHASE 2", "Weeks 5-10", "Core MES Integration", ["Production Order Dispatch", "Electronic Traveler UI", "QA Inspection Gates"], "GATE 2: Zero RFC Buffer Leaks"),
                    ("PHASE 3", "Weeks 11-16", "Enterprise Rollout", ["Lines 2-6 Cutover", "Operator Enablement", "Hypercare Support"], "GATE 3: Final Acceptance"),
                ]
            }
        ),
        (
            "CONTROL GATES",
            "Milestone Quality & Acceptance Gates",
            "Formal criteria required before transitioning between project phases.",
            True,
            lib.MilestoneGatesPrimitive,
            {
                "gates": [
                    ("1", "Architecture Blueprint", ["BTP event mesh sized", "Clean-core APIs catalogued", "Security boundaries approved"], "Chief Architect"),
                    ("2", "Pilot Line Deployment", ["Work-center dispatch live", "Inline vision cameras tested", "Zero dropped telemetry"], "Plant Director"),
                    ("3", "Quality Certification", ["21 CFR Part 11 signed", "Genealogy tree validated", "Audit trail verified"], "VP Quality"),
                    ("4", "Enterprise Go-Live", ["Multi-plant cutover completed", "Real-time 101 posting live", "Hypercare SLA active"], "Steering Committee"),
                ]
            }
        ),
        (
            "TIMELINE TRACK",
            "Program Delivery Schedule & Major Workstreams",
            "Chronological milestone progression across four delivery months.",
            False,
            lib.TimelinePrimitive,
            {
                "milestones": [
                    ("Month 1", "Sprint 0: Architecture Blueprint", "BTP subaccounts & OT edge configuration"),
                    ("Month 2", "Sprint 1-2: Pilot Line Deployment", "CNC machining cell connected & telemetry live"),
                    ("Month 3", "Sprint 3-4: Quality & Genealogy", "Electronic batch record & camera inspection live"),
                    ("Month 4", "Sprint 5-6: Enterprise Cutover", "Full plant rollout & 24/7 hypercare transition"),
                ]
            }
        )
    ]
    build_deck("representative_roadmap.pptx", "Enterprise Delivery Roadmap", "Schneider Electric", roadmap_slides)

    # 6. GOVERNANCE
    gov_slides = [
        (
            "GOVERNANCE MODEL",
            "Multi-Level Program Governance & Cadence",
            "Clear escalation channels connecting plant floor execution to the C-suite.",
            True,
            lib.GovernanceModelPrimitive,
            {
                "layers": [
                    ("Executive Steering Committee", "Monthly", "Managing Director", ["Budget allocation", "Strategic scope", "Executive escalations"], "Board of Directors"),
                    ("Architecture Review Board", "Bi-Weekly", "Chief Architect", ["Clean-core compliance", "Interface standards", "Security sign-off"], "Steering Committee"),
                    ("Plant Working Teams", "Daily Standup", "Plant Operations Lead", ["Line-level sprint backlog", "Operator enablement", "Defect remediation"], "Architecture Board"),
                ]
            }
        ),
        (
            "APPROVAL GATES",
            "Multi-Tier Stage-Gate Sign-Off Criteria",
            "Formally designated stakeholders certifying technical and operational readiness.",
            False,
            lib.ApprovalGatesPrimitive,
            {
                "gates": [
                    ("Gate 1: Architecture Sign-Off", "Chief Enterprise Architect", "Sprint 0", ["Clean-core rules validated", "OT firewall verified", "Data models approved"], "Signed Architecture Charter"),
                    ("Gate 2: Pilot Plant Acceptance", "Plant Operations Director", "Sprint 4", ["Pilot line latency <200ms", "Zero dropped telemetry events", "Operator ergonomics passed"], "Pilot Sign-Off Slip"),
                    ("Gate 3: Quality Compliance", "Global VP of Quality", "Sprint 8", ["21 CFR Part 11 audit trails", "Electronic signatures tested", "Lot genealogy tied to ERP"], "Validation Master Report"),
                    ("Gate 4: Production Cutover", "Executive Steering Comm", "Sprint 12", ["Go-live checklist 100% green", "Disaster recovery tested", "24/7 hypercare staffed"], "Production Go-Live Permit"),
                ]
            }
        ),
        (
            "RACI ALIGNMENT",
            "Program RACI Responsibility Matrix",
            "Accountability matrix preventing organizational confusion during deployment.",
            True,
            lib.RACIResponsibilityPrimitive,
            {
                "roles": ["Advisory Architect", "Client IT Lead", "Plant Operations Lead", "Steering Committee"],
                "deliverables": [
                    ("System Architecture & BTP Sizing", ["A", "R", "C", "I"]),
                    ("OT Network & Firewall Exceptions", ["C", "A", "R", "I"]),
                    ("Operator Enablement & SOP Sign-off", ["R", "C", "A", "I"]),
                    ("Milestone Gate Sign-off & Invoicing", ["C", "C", "C", "A"]),
                ]
            }
        )
    ]
    build_deck("representative_governance.pptx", "Enterprise Program Governance", "ABB Robotics", gov_slides)

    # 7. COMPLETE ENTERPRISE SOLUTION PROPOSAL
    solution_reqs = [
        "current-state",
        "structural problem",
        "target architecture",
        "integration/data flow",
        "shop-floor workflow",
        "genealogy visualization",
        "KPI strip",
        "delivery roadmap",
        "commercial proposal"
    ]
    res = ScenarioPresentationEngine.build_scenario_presentation(
        scenario_id="representative_complete_enterprise_solution",
        title="Autonomous Manufacturing Execution & Clean-Core ERP Architecture",
        topic="Enterprise Digital Transformation Proposal",
        client_name="Global Aerospace & Defense Conglomerate",
        requirements=solution_reqs,
        output_path="representative_complete_enterprise_solution.pptx"
    )
    print(f"[GENERATED] representative_complete_enterprise_solution.pptx: {res.slide_count} slides | Quality Score: {res.quality_report.overall_quality_score}/100 | Status: {res.quality_report.status.name} | Diversity: {res.diversity_score}%")


if __name__ == "__main__":
    generate_all_representative_decks()
