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

    # 7. TRANSFORMATION NARRATIVE DECK
    prs_trans = Presentation()
    prs_trans.slide_width = Inches(CanvasBounds.width)
    prs_trans.slide_height = Inches(CanvasBounds.height)
    from design_system.narrative_intelligence import NarrativeFramework, NarrativeIntelligenceEngine
    NarrativeIntelligenceEngine.render_narrative_deck(
        prs=prs_trans,
        framework=NarrativeFramework.TRANSFORMATION_JOURNEY,
        topic="Autonomous Manufacturing Execution",
        client_name="Lockheed Martin Aerospace"
    )
    rep_trans = PresentationQualityGate.audit_and_remediate(prs_trans, auto_remediate=True)
    prs_trans.save("representative_transformation.pptx")
    print(f"[GENERATED] representative_transformation.pptx: {len(prs_trans.slides)} slides | Quality Score: {rep_trans.overall_quality_score}/100 | Status: {rep_trans.status.name}")

    # 8. PROCESS FLOW DECK
    from design_system.transformation_semantic import ProcessFlowModel, ProcessNode, ProcessNodeType
    from design_system.process_flow_engine import ProcessFlowComposer
    prs_proc = Presentation()
    prs_proc.slide_width = Inches(CanvasBounds.width)
    prs_proc.slide_height = Inches(CanvasBounds.height)
    blank_layout = prs_proc.slide_layouts[6] if len(prs_proc.slide_layouts) > 6 else prs_proc.slide_layouts[0]

    # Slide 1: SAP to MES Branching Process
    s1 = prs_proc.slides.add_slide(blank_layout)
    HeaderPrimitive.render(s1, "1. PROCESS ARCHITECTURE", "SAP S/4HANA to MES Production Execution & Quality Clearance", "Sequential order dispatch with automated Poka-Yoke decision gate and rework loopback.", ConsultingSlateTheme)
    FooterPrimitive.render(s1, 1, 2, "Boeing Commercial Airplanes • Process Architecture Advisory", ConsultingSlateTheme)
    flow_model_1 = ProcessFlowModel(
        title="Production Execution & Quality Clearance",
        nodes=[
            ProcessNode("n1", "Demand & Sales Order", role_lane="Customer Demand", system_tag="SAP SD"),
            ProcessNode("n2", "Production Order & MRP", role_lane="SAP Core", system_tag="PP Order 100482"),
            ProcessNode("n3", "MES Dispatch & Setup", role_lane="MES Operations", system_tag="Digital Dispatch"),
            ProcessNode("n4", "Machine Execution", role_lane="Shop Floor OT", system_tag="CNC Work Center"),
            ProcessNode("n5", "Quality Gate & SPC", role_lane="Quality Assurance", system_tag="Vision / CMM", is_decision=True),
            ProcessNode("n6", "Confirmation & Ledger", role_lane="SAP Finance", system_tag="CO11N / 101 GR"),
            ProcessNode("n7", "Finished Goods Dispatch", role_lane="Logistics", system_tag="Outbound Delivery")
        ],
        branches=[]
    )
    ProcessFlowComposer.render_branching_process(s1, Margins.left, SpacingScale.CONTENT_TOP, Margins().usable_width, SpacingScale.CONTENT_HEIGHT, flow_model_1, ConsultingSlateTheme)

    # Slide 2: Frontline Operator Journey
    s2 = prs_proc.slides.add_slide(blank_layout)
    HeaderPrimitive.render(s2, "2. OPERATOR EXECUTION", "Frontline Operator Workflow with Poka-Yoke Interlocks", "Deterministic digital work instructions eliminate human assembly errors.", ExecutiveNavyTheme)
    FooterPrimitive.render(s2, 2, 2, "Boeing Commercial Airplanes • Operator Workflow Advisory", ExecutiveNavyTheme)
    lib.OperationalWorkflowPrimitive.render(
        slide=s2, left=Margins.left, top=SpacingScale.CONTENT_TOP, width=Margins().usable_width, height=SpacingScale.CONTENT_HEIGHT,
        stations=[
            ("10", "Inbound Kit Verification", "Operator scans component traveler barcode against ERP BOM", "Barcode mismatch interlock halts carrier"),
            ("20", "Robotic Cell Assembly", "Automated cell executes precision torque sequence with telemetry", "Temperature parameter drift triggers alert"),
            ("30", "Laser Direct Part Marking", "Permanent 2D DataMatrix serial UID etched onto titanium chassis", "High-res optical camera verifies scan contrast"),
            ("40", "End-of-Line Quality Gate", "Automated electrical resistance and pneumatic leak testing", "Defect failure locks output nest and posts NCR")
        ],
        theme=ExecutiveNavyTheme
    )
    rep_proc = PresentationQualityGate.audit_and_remediate(prs_proc, auto_remediate=True)
    prs_proc.save("representative_process_flow.pptx")
    print(f"[GENERATED] representative_process_flow.pptx: {len(prs_proc.slides)} slides | Quality Score: {rep_proc.overall_quality_score}/100 | Status: {rep_proc.status.name}")

    # 9. SWIMLANE DECK
    from design_system.transformation_semantic import SwimlaneDiagramModel, SwimlaneLane, SwimlaneStep, SwimlaneHandoff
    from design_system.swimlane_engine import SwimlaneDiagramComposer
    prs_swim = Presentation()
    prs_swim.slide_width = Inches(CanvasBounds.width)
    prs_swim.slide_height = Inches(CanvasBounds.height)

    s_sw1 = prs_swim.slides.add_slide(blank_layout)
    HeaderPrimitive.render(s_sw1, "1. CROSS-FUNCTIONAL SWIMLANE", "End-to-End Enterprise Order-to-Confirmation Swimlane", "Multi-tier transactional handoffs and Poka-Yoke interlocks across 5 enterprise lanes.", ConsultingSlateTheme)
    FooterPrimitive.render(s_sw1, 1, 1, "Siemens Industrial • Cross-Functional Swimlane Advisory", ConsultingSlateTheme)

    swim_model = SwimlaneDiagramModel(
        title="Order-to-Confirmation Operational Swimlane",
        lanes=[
            SwimlaneLane("l_cust", "Customer Demand", "External Partner", 1),
            SwimlaneLane("l_sap", "SAP S/4HANA", "System of Record", 2),
            SwimlaneLane("l_mes", "MES MOM Core", "Execution", 3),
            SwimlaneLane("l_shop", "Shop Floor / OT", "Edge Physical Layer", 4),
            SwimlaneLane("l_qm", "Quality Assurance", "Compliance Interlock", 5)
        ],
        steps=[
            SwimlaneStep("s1", "l_cust", "Demand Forecast / EDI", 1, "Sales Demand Signal", system_badge="EDI 850"),
            SwimlaneStep("s2", "l_sap", "Sales & Production Order", 2, "MRP Planning Run", system_badge="S/4HANA PP"),
            SwimlaneStep("s3", "l_mes", "Dispatch & Work Queue", 3, "Operation Scheduling", system_badge="MES MOM"),
            SwimlaneStep("s4", "l_shop", "CNC Machining & Setup", 4, "Physical Execution", system_badge="PLC / OPC UA"),
            SwimlaneStep("s5", "l_shop", "Material Consumption", 5, "Batch Component Binding", system_badge="261 Movement"),
            SwimlaneStep("s6", "l_qm", "Optical Inspection Gate", 6, "SPC Tolerance Validation", is_decision=True, system_badge="CMM Gauge"),
            SwimlaneStep("s7", "l_sap", "Confirmation & Ledger", 7, "CO11N & 101 Goods Receipt", system_badge="ACDOCA Post")
        ],
        handoffs=[
            SwimlaneHandoff("s1", "s2", "Sales Order", "B2B EDI"),
            SwimlaneHandoff("s2", "s3", "Production Order", "BAPI / OData"),
            SwimlaneHandoff("s3", "s4", "Dispatch Job", "OPC-UA / MQTT"),
            SwimlaneHandoff("s4", "s5", "As-Built Log", "Unit Traveler"),
            SwimlaneHandoff("s5", "s6", "Inspection Trigger", "Quality Call"),
            SwimlaneHandoff("s6", "s7", "Clearance GR", "101 Receipt")
        ]
    )
    SwimlaneDiagramComposer.render(s_sw1, Margins.left, SpacingScale.CONTENT_TOP, Margins().usable_width, SpacingScale.CONTENT_HEIGHT, swim_model, ConsultingSlateTheme)
    rep_swim = PresentationQualityGate.audit_and_remediate(prs_swim, auto_remediate=True)
    prs_swim.save("representative_swimlane.pptx")
    print(f"[GENERATED] representative_swimlane.pptx: {len(prs_swim.slides)} slides | Quality Score: {rep_swim.overall_quality_score}/100 | Status: {rep_swim.status.name}")

    # 10. MATURITY ASSESSMENT DECK
    from design_system.transformation_semantic import MaturityAssessmentModel, MaturityDimensionScore
    from design_system.maturity_engine import MaturityAssessmentComposer
    prs_mat = Presentation()
    prs_mat.slide_width = Inches(CanvasBounds.width)
    prs_mat.slide_height = Inches(CanvasBounds.height)

    s_m1 = prs_mat.slides.add_slide(blank_layout)
    HeaderPrimitive.render(s_m1, "1. MATURITY ASSESSMENT", "Digital Transformation Maturity Staircase & Gap Scorecard", "5-Level capability staircase and prioritized dimension gap scorecard.", ConsultingSlateTheme)
    FooterPrimitive.render(s_m1, 1, 1, "Caterpillar Manufacturing • Digital Maturity Audit", ConsultingSlateTheme)

    mat_model = MaturityAssessmentModel(
        title="Manufacturing Digital Transformation Maturity",
        overall_current_score=2.4,
        overall_target_score=4.2,
        dimensions=[
            MaturityDimensionScore("Process & Execution", 2.1, 4.3, "P1", "Paper travel cards & manual dispatch", "Deploy MES automated dispatch & digital traveler"),
            MaturityDimensionScore("Data & Genealogy", 2.3, 4.5, "P1", "Missing component-to-serial batch linkage", "Automated barcode & OPC-UA genealogy binding"),
            MaturityDimensionScore("SAP Clean Core", 2.6, 4.2, "P2", "Excess custom Z-tables blocking cloud upgrade", "Migrate custom code to BTP event mesh"),
            MaturityDimensionScore("Quality & Rework", 2.2, 4.0, "P1", "Delayed defect logging & missing CAPA loops", "Closed-loop digital inspection interlocks"),
            MaturityDimensionScore("Governance & RACI", 2.8, 4.0, "P2", "Ambiguous IT/OT boundary ownership", "Formalize unified IT/OT operating charter")
        ]
    )
    MaturityAssessmentComposer.render_staircase_scorecard(s_m1, Margins.left, SpacingScale.CONTENT_TOP, Margins().usable_width, SpacingScale.CONTENT_HEIGHT, mat_model, ConsultingSlateTheme)
    rep_mat = PresentationQualityGate.audit_and_remediate(prs_mat, auto_remediate=True)
    prs_mat.save("representative_maturity_assessment.pptx")
    print(f"[GENERATED] representative_maturity_assessment.pptx: {len(prs_mat.slides)} slides | Quality Score: {rep_mat.overall_quality_score}/100 | Status: {rep_mat.status.name}")

    # 11. CLOSED-LOOP MANUFACTURING DECK
    from design_system.transformation_semantic import ClosedLoopManufacturingModel, ClosedLoopStage
    prs_cl = Presentation()
    prs_cl.slide_width = Inches(CanvasBounds.width)
    prs_cl.slide_height = Inches(CanvasBounds.height)

    s_cl1 = prs_cl.slides.add_slide(blank_layout)
    HeaderPrimitive.render(s_cl1, "1. CLOSED-LOOP ARCHITECTURE", "Physical-to-Digital Closed-Loop Cyber-Physical Architecture", "Continuous cyber-physical feedback from machine sensors through S/4HANA intelligence.", ExecutiveNavyTheme)
    FooterPrimitive.render(s_cl1, 1, 1, "Honeywell Aerospace • Closed-Loop Manufacturing Advisory", ExecutiveNavyTheme)

    cl_model = ClosedLoopManufacturingModel(
        title="Autonomous Cyber-Physical Production Loop",
        stages=[
            ClosedLoopStage(1, "Physical World", ["CNC Machine", "Operator Tooling", "Physical Sensors"], ["Vibration & Current", "Spindle Speed"]),
            ClosedLoopStage(2, "Digital Capture", ["Edge Industrial Gateway", "OPC UA Collector"], ["Raw Telemetry Stream", "Time-Series Logs"]),
            ClosedLoopStage(3, "Contextualization", ["MES MOM Engine", "Unit Genealogy Traveler"], ["Order #100482 Context", "Lot & Serial Binding"]),
            ClosedLoopStage(4, "Enterprise Intelligence", ["SAP S/4HANA", "Predictive AI / SPC"], ["ACDOCA Ledger Postings", "Deviation Anomaly"]),
            ClosedLoopStage(5, "Decision Engine", ["Autonomous Control Logic", "Supervisor Approval"], ["Tool Offset Adjustment", "Hold/Release Clearance"]),
            ClosedLoopStage(6, "Directed Action", ["PLC Actuator", "Operator Terminal"], ["Automated Parameter Update", "Closed-Loop Physical Execution"])
        ],
        loop_closed_summary="Sub-second closed-loop telemetry updates machine tool offsets directly before tolerance drift causes non-conformance."
    )
    ProcessFlowComposer.render_closed_loop_manufacturing(s_cl1, Margins.left, SpacingScale.CONTENT_TOP, Margins().usable_width, SpacingScale.CONTENT_HEIGHT, cl_model, ExecutiveNavyTheme)
    rep_cl = PresentationQualityGate.audit_and_remediate(prs_cl, auto_remediate=True)
    prs_cl.save("representative_closed_loop_manufacturing.pptx")
    print(f"[GENERATED] representative_closed_loop_manufacturing.pptx: {len(prs_cl.slides)} slides | Quality Score: {rep_cl.overall_quality_score}/100 | Status: {rep_cl.status.name}")

    # 12. SAP + MES TRANSFORMATION DECK
    from design_system.transformation_semantic import (
        TransformationBridgeModel, CurrentStateSnapshot, TransformationIntervention, FutureStateVision
    )
    from design_system.transformation_engine import TransformationBridgeComposer
    from design_system.table_engine import EnterpriseTableFactory, EnterpriseTableComposer, TableArchetype
    from design_system.architecture_engine import ArchitectureBlueprintFactory, EnterpriseArchitectureComposer

    prs_sap_mes = Presentation()
    prs_sap_mes.slide_width = Inches(CanvasBounds.width)
    prs_sap_mes.slide_height = Inches(CanvasBounds.height)

    # Slide 1: Clean-Core Architecture Blueprint
    arch_spec = ArchitectureBlueprintFactory.clean_core_sap_to_shopfloor(client_name="General Electric")
    arch_spec.category_tag = "1. ENTERPRISE ARCHITECTURE"
    arch_spec.title = "SAP S/4HANA & MES Clean-Core Decoupled Architecture"
    arch_spec.subtitle = "Preserving ERP financial ledger integrity via event-driven edge execution."
    EnterpriseArchitectureComposer.compose_and_render(prs_sap_mes, arch_spec)

    # Slide 2: Cross-Functional Swimlane
    s_sm2 = prs_sap_mes.slides.add_slide(blank_layout)
    HeaderPrimitive.render(s_sm2, "2. OPERATIONAL SWIMLANE", "Cross-Functional SAP, MES & Shop Floor Handoff Architecture", "End-to-end transactional handoffs with Poka-Yoke error-proofing interlocks.", ConsultingSlateTheme)
    FooterPrimitive.render(s_sm2, 2, 5, "General Electric • Operational Swimlane Advisory", ConsultingSlateTheme)
    SwimlaneDiagramComposer.render(s_sm2, Margins.left, SpacingScale.CONTENT_TOP, Margins().usable_width, SpacingScale.CONTENT_HEIGHT, swim_model, ConsultingSlateTheme)

    # Slide 3: Branching Production Execution Flow
    s_sm3 = prs_sap_mes.slides.add_slide(blank_layout)
    HeaderPrimitive.render(s_sm3, "3. PROCESS EXECUTION", "Production Execution, Quality Clearance & Rework Loopback", "Sequential order dispatch with automated Poka-Yoke decision gate and rework loopback.", ConsultingSlateTheme)
    FooterPrimitive.render(s_sm3, 3, 5, "General Electric • Production Execution Flow", ConsultingSlateTheme)
    ProcessFlowComposer.render_branching_process(s_sm3, Margins.left, SpacingScale.CONTENT_TOP, Margins().usable_width, SpacingScale.CONTENT_HEIGHT, flow_model_1, ConsultingSlateTheme)

    # Slide 4: Transformation Intervention Bridge
    s_sm4 = prs_sap_mes.slides.add_slide(blank_layout)
    HeaderPrimitive.render(s_sm4, "4. TRANSFORMATION BLUEPRINT", "Current State to Future Operating Model Transformation Bridge", "Bridging legacy operational friction through S/4HANA clean-core and MES execution enablers.", ConsultingSlateTheme)
    FooterPrimitive.render(s_sm4, 4, 5, "General Electric • Transformation Bridge", ConsultingSlateTheme)
    trans_model = TransformationBridgeModel(
        title="SAP to MES Digital Transformation Blueprint",
        current_state=CurrentStateSnapshot(
            title="CURRENT STATE (Baseline)",
            pain_points=["Fragmented master data & BOM mismatches", "Manual paper travelers & dispatch clipboards", "Disconnected quality logs in Excel", "Delayed inventory confirmation (2-3 day lag)"],
            baseline_metrics=[("WIP Latency", "4.8 Days"), ("Scrap Rate", "4.2%"), ("OTIF Delivery", "81.4%")]
        ),
        intervention=TransformationIntervention(
            title="TRANSFORMATION ENABLERS",
            initiatives=["SAP S/4HANA Clean-Core Integration", "MES Digital Dispatch & Real-Time Tracking", "Automated Closed-Loop Quality Interlocks", "Unified Industrial Data Fabric & BTP Mesh"],
            enablers=["Air-gapped edge buffering", "Deterministic PLC connectors", "Zero custom Z-tables in ERP"]
        ),
        future_state=FutureStateVision(
            title="FUTURE OPERATING MODEL",
            transformed_capabilities=["Synchronized MRP-to-machine dispatch", "Full serial & batch genealogy trace", "Predictive quality interlocks at station", "Sub-second financial ledger postings"],
            target_outcomes=[("WIP Latency", "1.2 Days (-75%)"), ("Scrap Rate", "0.8% (-81%)"), ("OTIF Delivery", "97.5% (+16 pts)")]
        ),
        timeframe="12–18 Month Execution Horizon"
    )
    TransformationBridgeComposer.render_bridge(s_sm4, Margins.left, SpacingScale.CONTENT_TOP, Margins().usable_width, SpacingScale.CONTENT_HEIGHT, trans_model, ConsultingSlateTheme)

    # Slide 5: Digital Maturity Staircase & Scorecard
    s_sm5 = prs_sap_mes.slides.add_slide(blank_layout)
    HeaderPrimitive.render(s_sm5, "5. MATURITY ASSESSMENT", "Digital Transformation Maturity Staircase & Gap Scorecard", "5-Level capability staircase and prioritized dimension gap scorecard.", ConsultingSlateTheme)
    FooterPrimitive.render(s_sm5, 5, 5, "General Electric • Maturity Assessment", ConsultingSlateTheme)
    MaturityAssessmentComposer.render_staircase_scorecard(s_sm5, Margins.left, SpacingScale.CONTENT_TOP, Margins().usable_width, SpacingScale.CONTENT_HEIGHT, mat_model, ConsultingSlateTheme)

    rep_sap_mes = PresentationQualityGate.audit_and_remediate(prs_sap_mes, auto_remediate=True)
    prs_sap_mes.save("representative_sap_mes_transformation.pptx")
    print(f"[GENERATED] representative_sap_mes_transformation.pptx: {len(prs_sap_mes.slides)} slides | Quality Score: {rep_sap_mes.overall_quality_score}/100 | Status: {rep_sap_mes.status.name}")

    # 13. COMPLETE ENTERPRISE SOLUTION PROPOSAL (Regenerated with genuine process/transformation diagrams)
    prs_full = Presentation()
    prs_full.slide_width = Inches(CanvasBounds.width)
    prs_full.slide_height = Inches(CanvasBounds.height)

    # Slide 1: Executive Opening Tell
    from design_system.density_intelligence import LowDensitySlideRenderer
    LowDensitySlideRenderer.render_executive_statement(
        prs=prs_full,
        statement="Zero latency between the machine spindle and the balance sheet.",
        supporting_thesis="Preserving ERP ledger integrity while synchronizing sub-second plant floor execution.",
        author_or_source="Global Enterprise Solutions Architecture",
        category_tag="1. EXECUTIVE MANDATE • STRATEGIC THESIS",
        client_name="Global Aerospace & Defense",
        is_dark=True
    )

    # Slide 2: Transformation Bridge
    s_f2 = prs_full.slides.add_slide(blank_layout)
    HeaderPrimitive.render(s_f2, "2. TRANSFORMATION BLUEPRINT", "Current State to Future Operating Model Transformation Bridge", "Bridging legacy operational friction through S/4HANA clean-core and MES execution enablers.", ConsultingSlateTheme)
    FooterPrimitive.render(s_f2, 2, 7, "Global Aerospace & Defense • Transformation Blueprint", ConsultingSlateTheme)
    TransformationBridgeComposer.render_bridge(s_f2, Margins.left, SpacingScale.CONTENT_TOP, Margins().usable_width, SpacingScale.CONTENT_HEIGHT, trans_model, ConsultingSlateTheme)

    # Slide 3: Clean-Core System Architecture
    arch_spec_full = ArchitectureBlueprintFactory.clean_core_sap_to_shopfloor(client_name="Global Aerospace & Defense")
    arch_spec_full.category_tag = "3. SYSTEM ARCHITECTURE • CLEAN CORE"
    EnterpriseArchitectureComposer.compose_and_render(prs_full, arch_spec_full)

    # Slide 4: Cross-Functional Operational Swimlane
    s_f4 = prs_full.slides.add_slide(blank_layout)
    HeaderPrimitive.render(s_f4, "4. OPERATIONAL SWIMLANE", "Cross-Functional SAP, MES & Shop Floor Handoff Architecture", "End-to-end transactional handoffs with Poka-Yoke error-proofing interlocks.", ConsultingSlateTheme)
    FooterPrimitive.render(s_f4, 4, 7, "Global Aerospace & Defense • Operational Swimlane", ConsultingSlateTheme)
    SwimlaneDiagramComposer.render(s_f4, Margins.left, SpacingScale.CONTENT_TOP, Margins().usable_width, SpacingScale.CONTENT_HEIGHT, swim_model, ConsultingSlateTheme)

    # Slide 5: Branching Production Execution Process Flow
    s_f5 = prs_full.slides.add_slide(blank_layout)
    HeaderPrimitive.render(s_f5, "5. PROCESS ARCHITECTURE", "Production Execution, Quality Clearance & Rework Loopback", "Sequential order dispatch with automated Poka-Yoke decision gate and rework loopback.", ConsultingSlateTheme)
    FooterPrimitive.render(s_f5, 5, 7, "Global Aerospace & Defense • Process Architecture", ConsultingSlateTheme)
    ProcessFlowComposer.render_branching_process(s_f5, Margins.left, SpacingScale.CONTENT_TOP, Margins().usable_width, SpacingScale.CONTENT_HEIGHT, flow_model_1, ConsultingSlateTheme)

    # Slide 6: Digital Maturity Staircase
    s_f6 = prs_full.slides.add_slide(blank_layout)
    HeaderPrimitive.render(s_f6, "6. MATURITY ASSESSMENT", "Digital Transformation Maturity Staircase & Gap Scorecard", "5-Level capability staircase and prioritized dimension gap scorecard.", ConsultingSlateTheme)
    FooterPrimitive.render(s_f6, 6, 7, "Global Aerospace & Defense • Maturity Assessment", ConsultingSlateTheme)
    MaturityAssessmentComposer.render_staircase_scorecard(s_f6, Margins.left, SpacingScale.CONTENT_TOP, Margins().usable_width, SpacingScale.CONTENT_HEIGHT, mat_model, ConsultingSlateTheme)

    # Slide 7: Closed-Loop Manufacturing Architecture
    s_f7 = prs_full.slides.add_slide(blank_layout)
    HeaderPrimitive.render(s_f7, "7. CLOSED-LOOP ARCHITECTURE", "Physical-to-Digital Closed-Loop Cyber-Physical Architecture", "Continuous cyber-physical feedback from machine sensors through S/4HANA intelligence.", ExecutiveNavyTheme)
    FooterPrimitive.render(s_f7, 7, 7, "Global Aerospace & Defense • Closed-Loop Architecture", ExecutiveNavyTheme)
    ProcessFlowComposer.render_closed_loop_manufacturing(s_f7, Margins.left, SpacingScale.CONTENT_TOP, Margins().usable_width, SpacingScale.CONTENT_HEIGHT, cl_model, ExecutiveNavyTheme)

    # Slide 8: Commercial Benefits Table
    table_spec = EnterpriseTableFactory.get_table_spec(TableArchetype.BUSINESS_BENEFITS, client_name="Global Aerospace & Defense")
    table_spec.category_tag = "8. VALUE REALIZATION • AUDITED ROI"
    EnterpriseTableComposer.compose_and_render(prs_full, table_spec)

    rep_full = PresentationQualityGate.audit_and_remediate(prs_full, auto_remediate=True)
    prs_full.save("representative_complete_enterprise_solution.pptx")
    print(f"[GENERATED] representative_complete_enterprise_solution.pptx: {len(prs_full.slides)} slides | Quality Score: {rep_full.overall_quality_score}/100 | Status: {rep_full.status.name}")


if __name__ == "__main__":
    generate_all_representative_decks()
