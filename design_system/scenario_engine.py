"""
Generic Semantic Scenario Presentation Engine.

Dynamically maps business scenarios and semantic requirements into distinct,
first-class visual representations, without hardcoding static templates.

Core Principles:
1. Pure Semantic Intent Mapping: Evaluates requirements against ontology & information relationships.
2. Form-Follows-Function: Selects the visual primitive that best communicates the underlying data relationship.
3. Visual Rhythm & Anti-Monotony: Avoids consecutive identical layouts and prevents card-grid overuse.
4. Native PPTX Construction: Uses native editable PowerPoint shapes, tables, and charts.
5. Presentation Quality Gate: Automatically validates and certifies presentations prior to export.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Any, Optional, Tuple, Set
import re
import os

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE

from .typography import TypographySystem, FONT_FAMILY
from .spacing import CanvasBounds, Margins, SpacingScale, GridCalculator
from .color import Theme, ExecutiveNavyTheme, ConsultingSlateTheme
from .primitives import HeaderPrimitive, FooterPrimitive, SurfacePrimitive, CalloutBannerPrimitive
from .density_intelligence import VisualDensity
from .quality_gate import PresentationQualityGate, QualityGateReport, QualityStatus
from .intelligence import InformationRelationship, VisualRepresentation
from .manufacturing_vocabulary import MANUFACTURING_VOCABULARY, EntityCategory
import design_system.library as lib


# =============================================================================
# 1. Semantic Visual Form Mapping
# =============================================================================

@dataclass
class VisualFormDescriptor:
    """Descriptor defining a visual form and its associated primitive key."""
    form_key: str                         # Unique key for the form
    display_name: str                     # Human-readable title
    primitive_key: str                    # Key in PRIMITIVE_CATALOG
    relationship: InformationRelationship
    layout_family: str                    # 'blueprint', 'flow', 'dashboard', 'hierarchy', 'table', 'timeline', 'matrix'
    preferred_theme: str                  # 'navy' or 'slate'
    default_density: VisualDensity
    category_tag: str                     # Category header text


SEMANTIC_FORM_RULES: List[Tuple[List[str], VisualFormDescriptor]] = [
    # -------------------------------------------------------------------------
    # ARCHITECTURE & SYSTEMS
    # -------------------------------------------------------------------------
    (
        ["enterprise architecture", "system architecture", "target architecture", "solution architecture", "multi-tier architecture"],
        VisualFormDescriptor(
            form_key="enterprise_architecture",
            display_name="Enterprise Architecture Diagram",
            primitive_key="system_architecture",
            relationship=InformationRelationship.COMPONENT_STRUCTURE,
            layout_family="blueprint",
            preferred_theme="navy",
            default_density=VisualDensity.MEDIUM_DENSITY,
            category_tag="ENTERPRISE ARCHITECTURE"
        )
    ),
    (
        ["integration", "data flow", "data pipeline", "event mesh", "interface architecture", "integration architecture"],
        VisualFormDescriptor(
            form_key="integration_data_flow",
            display_name="Integration & Data Flow Architecture",
            primitive_key="integration_architecture",
            relationship=InformationRelationship.EXCHANGE_FLOW,
            layout_family="blueprint",
            preferred_theme="navy",
            default_density=VisualDensity.HIGH_DENSITY,
            category_tag="INTEGRATION FABRIC"
        )
    ),
    (
        ["manufacturing hierarchy", "isa-95", "shop-floor hierarchy", "enterprise-to-shopfloor", "plant hierarchy"],
        VisualFormDescriptor(
            form_key="manufacturing_hierarchy",
            display_name="ISA-95 Manufacturing Hierarchy",
            primitive_key="enterprise_to_shopfloor",
            relationship=InformationRelationship.HIERARCHICAL_DECOMPOSITION,
            layout_family="blueprint",
            preferred_theme="slate",
            default_density=VisualDensity.HIGH_DENSITY,
            category_tag="OPERATIONAL TOPOLOGY"
        )
    ),
    (
        ["scope architecture", "application landscape", "solution scope", "systems landscape"],
        VisualFormDescriptor(
            form_key="application_landscape",
            display_name="Application Scope Landscape",
            primitive_key="application_landscape",
            relationship=InformationRelationship.COMPONENT_STRUCTURE,
            layout_family="blueprint",
            preferred_theme="navy",
            default_density=VisualDensity.HIGH_DENSITY,
            category_tag="APPLICATION PORTFOLIO"
        )
    ),
    # -------------------------------------------------------------------------
    # PROCESS & WORKFLOW
    # -------------------------------------------------------------------------
    (
        ["process flow", "operational process", "value stream", "order flow", "execution sequence"],
        VisualFormDescriptor(
            form_key="process_flow",
            display_name="End-to-End Process Flow",
            primitive_key="horizontal_process_flow",
            relationship=InformationRelationship.SEQUENTIAL_PROCESS,
            layout_family="flow",
            preferred_theme="slate",
            default_density=VisualDensity.MEDIUM_DENSITY,
            category_tag="PROCESS ARCHITECTURE"
        )
    ),
    (
        ["shop-floor workflow", "operator workflow", "workstation workflow", "poka-yoke workflow"],
        VisualFormDescriptor(
            form_key="shopfloor_workflow",
            display_name="Shop-Floor Operator Workflow",
            primitive_key="operational_workflow",
            relationship=InformationRelationship.OPERATIONAL_JOURNEY,
            layout_family="flow",
            preferred_theme="slate",
            default_density=VisualDensity.HIGH_DENSITY,
            category_tag="OPERATOR EXECUTION"
        )
    ),
    (
        ["exception/rework flow", "rework flow", "ncr flow", "exception flow", "quarantine loop"],
        VisualFormDescriptor(
            form_key="exception_rework_flow",
            display_name="Non-Conformance & Rework Loop",
            primitive_key="exception_rework_flow",
            relationship=InformationRelationship.SEQUENTIAL_PROCESS,
            layout_family="flow",
            preferred_theme="navy",
            default_density=VisualDensity.MEDIUM_DENSITY,
            category_tag="QUALITY CONTROL & REWORK"
        )
    ),
    # -------------------------------------------------------------------------
    # TRACEABILITY & DATA RELATIONSHIPS
    # -------------------------------------------------------------------------
    (
        ["genealogy visualization", "genealogy", "as-built genealogy", "component genealogy"],
        VisualFormDescriptor(
            form_key="genealogy_tree",
            display_name="Unit & Lot Genealogy Tree",
            primitive_key="genealogy_tree",
            relationship=InformationRelationship.GENEALOGICAL_LINEAGE,
            layout_family="hierarchy",
            preferred_theme="navy",
            default_density=VisualDensity.HIGH_DENSITY,
            category_tag="AS-BUILT TRACEABILITY"
        )
    ),
    (
        ["serial/batch relationships", "serial relationships", "batch relationships", "parent-child", "bom relationship"],
        VisualFormDescriptor(
            form_key="serial_batch_relationship",
            display_name="Serial & Batch BOM Ancestry",
            primitive_key="parent_child_relationship",
            relationship=InformationRelationship.HIERARCHICAL_DECOMPOSITION,
            layout_family="hierarchy",
            preferred_theme="slate",
            default_density=VisualDensity.HIGH_DENSITY,
            category_tag="GENEALOGY RELATIONSHIPS"
        )
    ),
    (
        ["process history", "data lifecycle", "lot history", "audit lifecycle"],
        VisualFormDescriptor(
            form_key="process_history",
            display_name="Process History & Data Lifecycle",
            primitive_key="data_lifecycle",
            relationship=InformationRelationship.SEQUENTIAL_PROCESS,
            layout_family="flow",
            preferred_theme="slate",
            default_density=VisualDensity.MEDIUM_DENSITY,
            category_tag="TRACEABILITY LIFECYCLE"
        )
    ),
    (
        ["quality relationship", "quality matrix", "quality inspection", "inspection relationship"],
        VisualFormDescriptor(
            form_key="quality_relationship",
            display_name="Quality & Compliance Architecture",
            primitive_key="control_framework",
            relationship=InformationRelationship.GOVERNANCE_CONTROL,
            layout_family="table",
            preferred_theme="slate",
            default_density=VisualDensity.HIGH_DENSITY,
            category_tag="QUALITY COMPLIANCE"
        )
    ),
    # -------------------------------------------------------------------------
    # ANALYTICS & EXECUTIVE COCKPITS
    # -------------------------------------------------------------------------
    (
        ["kpi strip", "executive kpi", "metric strip", "headline kpis"],
        VisualFormDescriptor(
            form_key="kpi_strip",
            display_name="Executive KPI Metric Strip",
            primitive_key="kpi_strip",
            relationship=InformationRelationship.QUANTITATIVE_PERFORMANCE,
            layout_family="dashboard",
            preferred_theme="navy",
            default_density=VisualDensity.LOW_DENSITY,
            category_tag="EXECUTIVE SCORECARD"
        )
    ),
    (
        ["trend analysis", "trend chart", "performance trend", "run rate trend"],
        VisualFormDescriptor(
            form_key="trend_analysis",
            display_name="Operational Performance Trend Chart",
            primitive_key="trend_chart",
            relationship=InformationRelationship.QUANTITATIVE_COMPARISON,
            layout_family="dashboard",
            preferred_theme="navy",
            default_density=VisualDensity.MEDIUM_DENSITY,
            category_tag="PERFORMANCE TRAJECTORY"
        )
    ),
    (
        ["bottleneck visualization", "bottleneck", "capacity vs demand", "constraint analysis"],
        VisualFormDescriptor(
            form_key="bottleneck_analysis",
            display_name="Work-Center Bottleneck & Capacity Loading",
            primitive_key="capacity_vs_demand",
            relationship=InformationRelationship.QUANTITATIVE_COMPARISON,
            layout_family="dashboard",
            preferred_theme="slate",
            default_density=VisualDensity.HIGH_DENSITY,
            category_tag="BOTTLENECK ANALYSIS"
        )
    ),
    (
        ["quality/pareto visualization", "pareto", "quality pareto", "root cause pareto", "80/20"],
        VisualFormDescriptor(
            form_key="pareto_analysis",
            display_name="Pareto 80/20 Root-Cause Defect Concentration",
            primitive_key="pareto",
            relationship=InformationRelationship.QUANTITATIVE_COMPARISON,
            layout_family="dashboard",
            preferred_theme="navy",
            default_density=VisualDensity.MEDIUM_DENSITY,
            category_tag="QUALITY CONCENTRATION"
        )
    ),
    (
        ["action-oriented table", "action table", "action register", "exception table", "mitigation table"],
        VisualFormDescriptor(
            form_key="action_table",
            display_name="Action-Oriented Exception Register",
            primitive_key="action_register",
            relationship=InformationRelationship.STRUCTURED_ATTRIBUTES,
            layout_family="table",
            preferred_theme="slate",
            default_density=VisualDensity.HIGH_DENSITY,
            category_tag="CORRECTIVE ACTIONS"
        )
    ),
    # -------------------------------------------------------------------------
    # STRATEGY & TRANSFORMATION
    # -------------------------------------------------------------------------
    (
        ["current-state", "current state", "baseline", "as-is", "operating baseline"],
        VisualFormDescriptor(
            form_key="current_state",
            display_name="Current Operating Reality vs. Target State",
            primitive_key="current_vs_future_state",
            relationship=InformationRelationship.CONTRAST_TENSION,
            layout_family="flow",
            preferred_theme="slate",
            default_density=VisualDensity.MEDIUM_DENSITY,
            category_tag="OPERATING REALITY"
        )
    ),
    (
        ["structural problem", "root cause", "core constraint", "problem diagnosis"],
        VisualFormDescriptor(
            form_key="structural_problem",
            display_name="Structural Constraints & Insight Evidence",
            primitive_key="insight_and_evidence",
            relationship=InformationRelationship.NARRATIVE_EXPLANATION,
            layout_family="narrative",
            preferred_theme="navy",
            default_density=VisualDensity.MEDIUM_DENSITY,
            category_tag="PROBLEM MECHANICS"
        )
    ),
    (
        ["transformation journey", "journey", "outcome chain", "capability maturity"],
        VisualFormDescriptor(
            form_key="transformation_journey",
            display_name="Strategic Transformation Outcome Chain",
            primitive_key="outcome_chain",
            relationship=InformationRelationship.CAUSE_AND_EFFECT,
            layout_family="flow",
            preferred_theme="slate",
            default_density=VisualDensity.MEDIUM_DENSITY,
            category_tag="STRATEGIC JOURNEY"
        )
    ),
    (
        ["operating model", "target operating model", "org model"],
        VisualFormDescriptor(
            form_key="operating_model",
            display_name="Target Operating Model & Governance Tiers",
            primitive_key="operating_model",
            relationship=InformationRelationship.RESPONSIBILITY_ALLOCATION,
            layout_family="table",
            preferred_theme="slate",
            default_density=VisualDensity.HIGH_DENSITY,
            category_tag="OPERATING MODEL"
        )
    ),
    (
        ["modules/capabilities", "modules", "capabilities", "capability map", "functional modules"],
        VisualFormDescriptor(
            form_key="capability_modules",
            display_name="Modular Functional Capability Map",
            primitive_key="capability_map",
            relationship=InformationRelationship.CAPABILITY_TAXONOMY,
            layout_family="blueprint",
            preferred_theme="navy",
            default_density=VisualDensity.HIGH_DENSITY,
            category_tag="CAPABILITY ARCHITECTURE"
        )
    ),
    (
        ["business outcomes", "outcomes", "roi", "value realization", "cost benefit"],
        VisualFormDescriptor(
            form_key="business_outcomes",
            display_name="Business Outcomes & Value Realization",
            primitive_key="cost_benefit_summary",
            relationship=InformationRelationship.CAUSE_AND_EFFECT,
            layout_family="table",
            preferred_theme="slate",
            default_density=VisualDensity.MEDIUM_DENSITY,
            category_tag="VALUE REALIZATION"
        )
    ),
    # -------------------------------------------------------------------------
    # GOVERNANCE & DELIVERY
    # -------------------------------------------------------------------------
    (
        ["governance", "governance/control points", "control points", "governance model"],
        VisualFormDescriptor(
            form_key="governance_controls",
            display_name="Multi-Tier Governance & Control Gates",
            primitive_key="approval_gates",
            relationship=InformationRelationship.GOVERNANCE_CONTROL,
            layout_family="table",
            preferred_theme="slate",
            default_density=VisualDensity.HIGH_DENSITY,
            category_tag="GOVERNANCE & CONTROLS"
        )
    ),
    (
        ["delivery roadmap", "roadmap", "implementation roadmap", "phased rollout"],
        VisualFormDescriptor(
            form_key="delivery_roadmap",
            display_name="Phased Transformation Delivery Roadmap",
            primitive_key="transformation_roadmap",
            relationship=InformationRelationship.TRANSFORMATION_STAGES,
            layout_family="timeline",
            preferred_theme="slate",
            default_density=VisualDensity.HIGH_DENSITY,
            category_tag="DELIVERY ROADMAP"
        )
    ),
    (
        ["milestone structure", "milestones", "milestone gates"],
        VisualFormDescriptor(
            form_key="milestone_structure",
            display_name="Milestone Gates & Quality Criteria",
            primitive_key="milestone_gates",
            relationship=InformationRelationship.TRANSFORMATION_STAGES,
            layout_family="timeline",
            preferred_theme="slate",
            default_density=VisualDensity.MEDIUM_DENSITY,
            category_tag="MILESTONE GATES"
        )
    ),
    (
        ["timeline", "schedule", "chronology"],
        VisualFormDescriptor(
            form_key="timeline",
            display_name="Execution Timeline & Deliverable Milestones",
            primitive_key="timeline",
            relationship=InformationRelationship.TEMPORAL_MILESTONES,
            layout_family="timeline",
            preferred_theme="slate",
            default_density=VisualDensity.MEDIUM_DENSITY,
            category_tag="PROGRAM SCHEDULE"
        )
    ),
    # -------------------------------------------------------------------------
    # COMMERCIAL & ENGAGEMENT
    # -------------------------------------------------------------------------
    (
        ["scope table", "scope", "solution scope", "scope matrix"],
        VisualFormDescriptor(
            form_key="scope_table",
            display_name="Commercial Scope & Boundary Matrix",
            primitive_key="comparison_matrix",
            relationship=InformationRelationship.STRUCTURED_ATTRIBUTES,
            layout_family="table",
            preferred_theme="slate",
            default_density=VisualDensity.HIGH_DENSITY,
            category_tag="SCOPE MATRIX"
        )
    ),
    (
        ["payment gates", "commercial proposal", "commercial terms", "pricing model"],
        VisualFormDescriptor(
            form_key="payment_gates",
            display_name="Commercial Model & Milestone Payment Gates",
            primitive_key="commercial_table",
            relationship=InformationRelationship.FINANCIAL_COMMERCIAL,
            layout_family="table",
            preferred_theme="navy",
            default_density=VisualDensity.HIGH_DENSITY,
            category_tag="COMMERCIAL TERMS"
        )
    ),
    (
        ["assumptions", "assumptions register", "action items"],
        VisualFormDescriptor(
            form_key="assumptions",
            display_name="Operational Assumptions & Commitments",
            primitive_key="action_register",
            relationship=InformationRelationship.STRUCTURED_ATTRIBUTES,
            layout_family="table",
            preferred_theme="slate",
            default_density=VisualDensity.HIGH_DENSITY,
            category_tag="ASSUMPTIONS REGISTER"
        )
    ),
    (
        ["dependencies", "raci", "dependencies/raci", "responsibility matrix"],
        VisualFormDescriptor(
            form_key="dependencies",
            display_name="Program Dependencies & RACI Alignment",
            primitive_key="raci_responsibility",
            relationship=InformationRelationship.RESPONSIBILITY_ALLOCATION,
            layout_family="table",
            preferred_theme="slate",
            default_density=VisualDensity.HIGH_DENSITY,
            category_tag="RACI ALIGNMENT"
        )
    ),
]


class SemanticVisualFormResolver:
    """Resolves natural language or semantic tokens into concrete visual forms and primitives."""

    @classmethod
    def resolve_requirement(cls, req_text: str) -> VisualFormDescriptor:
        req_clean = req_text.lower().strip()

        # 1. Exact or substring match in rules
        for keywords, descriptor in SEMANTIC_FORM_RULES:
            for kw in keywords:
                if kw in req_clean or req_clean in kw:
                    return descriptor

        # 2. Token overlap fallback
        req_tokens = set(re.findall(r"\w+", req_clean))
        best_match = None
        best_score = 0

        for keywords, descriptor in SEMANTIC_FORM_RULES:
            for kw in keywords:
                kw_tokens = set(re.findall(r"\w+", kw))
                overlap = len(req_tokens & kw_tokens)
                if overlap > best_score:
                    best_score = overlap
                    best_match = descriptor

        if best_match:
            return best_match

        # 3. Default structured fallback
        return VisualFormDescriptor(
            form_key="structured_table",
            display_name="Structured Enterprise Analysis",
            primitive_key="comparison_matrix",
            relationship=InformationRelationship.STRUCTURED_ATTRIBUTES,
            layout_family="table",
            preferred_theme="slate",
            default_density=VisualDensity.HIGH_DENSITY,
            category_tag="ANALYSIS & DATA"
        )


# =============================================================================
# 2. Contextual Domain Payload Synthesizer
# =============================================================================

class DomainPayloadSynthesizer:
    """Generates realistic, domain-accurate payload data for any resolved primitive."""

    @classmethod
    def synthesize_payload(
        cls,
        primitive_key: str,
        topic: str,
        client_name: str,
        slide_title: str
    ) -> Dict[str, Any]:
        from .library.architecture import ArchTierData

        # 1. SYSTEM ARCHITECTURE
        if primitive_key == "system_architecture":
            return {
                "tiers": [
                    ArchTierData(
                        tier_name="Tier 1: Enterprise ERP Core",
                        subtitle="SAP S/4HANA Cloud (Clean Core Architecture)",
                        subsystems=["Production Orders (PP)", "Material Master (MM)", "Inventory Management (IM)", "Ledger (ACDOCA)"],
                        protocol_to_next="OData APIs / Business Event Mesh"
                    ),
                    ArchTierData(
                        tier_name="Tier 2: Integration & Orchestration",
                        subtitle="SAP BTP & Hybrid Middleware Fabric",
                        subsystems=["Event Mesh Broker", "Integration Suite", "API Management Gateway", "Dead-Letter Queue Buffer"],
                        protocol_to_next="TLS 1.3 / OPC-UA / MQTT"
                    ),
                    ArchTierData(
                        tier_name="Tier 3: Manufacturing Execution & Edge",
                        subtitle="Digital Manufacturing (MES/MOM) & OT Edge",
                        subsystems=["Shopfloor Dispatcher", "Unit Genealogy Engine", "Line SCADA Collector", "PLC Machine Sensors"],
                        protocol_to_next=None
                    )
                ]
            }

        # 2. INTEGRATION ARCHITECTURE
        if primitive_key == "integration_architecture":
            return {
                "producer_info": ("Event Producers (Shopfloor & ERP)", ["SAP S/4HANA Order Events", "Barcode Scanners (HHT)", "Inline Vision Cameras", "OPC-UA Edge Daemons"]),
                "broker_info": ("SAP BTP Event Mesh & Broker", ["Kafka Message Fabric", "API Management Gateway", "Dead-Letter Buffer"], "Pub/Sub Event Streaming"),
                "consumer_info": ("Subscribers & Consumers", ["Digital Manufacturing MES", "Quality Historian DB", "SAP S/4HANA (101 Postings)", "CXO Control Tower"])
            }

        # 3. ENTERPRISE TO SHOPFLOOR (ISA-95)
        if primitive_key == "enterprise_to_shopfloor":
            return {
                "isa_levels": [
                    ("Level 4: Business Logistics", "Enterprise Core", ["ERP Financials", "Master Planning (PP)", "Material Master (MM)"], "OData / BAPI"),
                    ("Level 3: Operations (MOM/MES)", "Plant Execution", ["Work Order Dispatch", "Real-Time Genealogy", "Non-Conformance Tracking"], "REST / WebSockets"),
                    ("Level 2: Supervisory Control", "Line Control", ["SCADA Systems", "Cell Controllers", "Batch Engine"], "OPC-UA / Modbus"),
                    ("Level 1: Sensing & Manipulation", "Machine OT", ["PLC Controllers", "Robotics Actuators", "Torque Drivers"], "Fieldbus / I/O"),
                ]
            }

        # 4. HORIZONTAL PROCESS FLOW
        if primitive_key == "horizontal_process_flow":
            return {
                "steps": [
                    ("1", "Order Release", ["Confirmed in SAP S/4HANA", "Dispatched to plant queue"]),
                    ("2", "Kitting & Scan", ["Serial barcode verified", "Validated against BOM"]),
                    ("3", "Assembly Run", ["Torque telemetry tracked", "Real-time cycle time log"]),
                    ("4", "Quality Gate", ["Vision system inspection", "Automated tolerance check"]),
                    ("5", "Goods Receipt", ["Auto 101 movement posted", "Ledger tie-out in ERP"]),
                ]
            }

        # 5. OPERATIONAL WORKFLOW
        if primitive_key == "operational_workflow":
            return {
                "stations": [
                    ("10", "Inbound Kit Verification", "Operator scans component traveler barcode against ERP BOM", "Barcode mismatch interlock halts carrier"),
                    ("20", "Robotic Cell Assembly", "Automated cell executes precision torque sequence with telemetry", "Temperature parameter drift triggers alert"),
                    ("30", "Laser Direct Part Marking", "Permanent 2D DataMatrix serial UID etched onto titanium chassis", "High-res optical camera verifies scan contrast"),
                    ("40", "End-of-Line Quality Gate", "Automated electrical resistance and pneumatic leak testing", "Defect failure locks output nest and posts NCR"),
                ]
            }

        # 6. EXCEPTION REWORK FLOW
        if primitive_key == "exception_rework_flow":
            return {
                "standard_steps": ["Component Kitting", "Torque Assembly", "Automated QC Test", "Packaging & Dispatch"],
                "exception_trigger": "Torque angle out of specification (+/- 3.5 deg tolerance breach)",
                "rework_steps": ["Quarantine Unit to MRB Nest", "Scan Technician Badge", "Disassemble Fasteners", "Re-Torque & Re-Test"]
            }

        # 7. GENEALOGY TREE
        if primitive_key == "genealogy_tree":
            return {
                "finished_good": ("SN-994820-A", "Titanium Actuator Module 24V", "Customer Delivery PO-88319"),
                "sub_assemblies": [
                    ("Valve Body Sub-Assy", "LOT-VB-4401", ["Casting Lot #8821", "O-Ring Seal #1094"]),
                    ("Stator Coil Module", "LOT-SC-2041", ["Copper Wire #5502", "Epoxy Core #9914"]),
                    ("Digital Controller PCB", "LOT-PCB-7712", ["Microcontroller #441", "Firmware Rev 4.2"]),
                ]
            }

        # 8. PARENT CHILD RELATIONSHIP
        if primitive_key == "parent_child_relationship":
            return {
                "bom_hierarchy": [
                    (0, "MAT-9000", "Top Assembly: Actuator Module 24V", "1 EA", "Rev C"),
                    (1, "SUB-1010", "Solenoid Valve Body Sub-Assembly", "1 EA", "Rev B"),
                    (2, "PRT-4401", "Titanium Fastener M4 x 20mm", "4 EA", "Rev A"),
                    (2, "PRT-4405", "Viton Flange Seal Ring 18mm", "1 EA", "Rev A"),
                    (1, "SUB-1020", "Digital Controller Board Assembly", "1 EA", "Rev D"),
                    (2, "PRT-8802", "Optical Shaft Encoder Sensor", "1 EA", "Rev B"),
                ]
            }

        # 9. DATA LIFECYCLE
        if primitive_key == "data_lifecycle":
            return {
                "stages": [
                    ("1. Ingestion", "Sub-second", "OPC-UA and barcode scans stream to edge cache"),
                    ("2. Processing", "5 seconds", "Validates serial genealogy and ERP work order"),
                    ("3. Execution", "Shift Real-Time", "Real-time MES traveler execution and sign-off"),
                    ("4. Archival", "10 Years SLA", "WORM storage compliance for 21 CFR Part 11 audit"),
                ]
            }

        # 10. KPI STRIP
        if primitive_key == "kpi_strip":
            return {
                "kpis": [
                    ("91.4%", "Overall Equipment Effectiveness (OEE)", "Plant Benchmark", "+4.8% vs Target", True),
                    ("99.4%", "On-Time In-Full Delivery (OTIF)", "Customer SLA", "+1.2% Improvement", True),
                    ("1.4%", "Scrap & Non-Conformance Rate", "Quality Gate", "-42% Reduction", True),
                    ("240ms", "Shop-Floor to ERP Sync Latency", "BTP SLA", "Sub-Second Verified", True),
                ]
            }

        # 11. TREND CHART
        if primitive_key == "trend_chart":
            return {
                "periods": ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026"],
                "series_data": [
                    ("Actual Performance", [81.2, 83.5, 86.1, 88.4, 90.2, 91.4]),
                    ("Target Benchmark", [85.0, 85.0, 88.0, 88.0, 90.0, 90.0]),
                ]
            }

        # 12. CAPACITY VS DEMAND
        if primitive_key == "capacity_vs_demand":
            return {
                "work_centers": [
                    ("WC-101 CNC Machining", 450.0, 520.0),      # Bottleneck (>100%)
                    ("WC-204 Robotic Welding", 400.0, 370.0),    # Balanced
                    ("WC-305 Final Assembly", 500.0, 440.0),     # Balanced
                    ("WC-408 Quality Inspection", 300.0, 360.0), # Bottleneck
                ]
            }

        # 13. PARETO ANALYSIS
        if primitive_key == "pareto":
            return {
                "items": [
                    ("Torque Calibration Drift", 54.0),
                    ("Material Kitting Shortage", 26.0),
                    ("Barcode Read Error", 12.0),
                    ("Operator Travel Delay", 5.0),
                    ("Other Minor Exceptions", 3.0),
                ]
            }

        # 14. ACTION REGISTER
        if primitive_key == "action_register":
            return {
                "actions": [
                    ("ACT-01", "Recalibrate torque load cells on Station 20", "Maintenance", "HIGH", "Lead Tech", "Week 2", "IN PROGRESS"),
                    ("ACT-02", "Implement automated ASN barcode validation in ERP", "Integration", "HIGH", "BTP Lead", "Week 3", "OPEN"),
                    ("ACT-03", "Conduct operator Poka-Yoke ergonomics review", "Plant Ops", "MED", "Supervisor", "Week 4", "OPEN"),
                    ("ACT-04", "Publish updated First Pass Yield dashboard to CXO", "Analytics", "MED", "Data Arch", "Week 1", "COMPLETED"),
                ]
            }

        # 15. CURRENT VS FUTURE STATE
        if primitive_key == "current_vs_future_state":
            return {
                "as_is_title": "Current State: Fragmented Legacy Islands",
                "as_is_points": [
                    ("Paper Travelers", "Physical paper sheets create 4-hour batch release latency"),
                    ("Siloed PLC Controllers", "Isolated machine data with no automated ERP tie-out"),
                    ("Batch Scrap Discovery", "Quality defects discovered only at end-of-line test"),
                ],
                "to_be_title": "Target State: Connected Digital Manufacturing",
                "to_be_points": [
                    ("Digital Work Instructions", "100% paperless e-traveler with biometric operator sign-off"),
                    ("Sub-Second Telemetry", "OPC-UA edge brokers stream telemetry straight into BTP"),
                    ("Closed-Loop Poka-Yoke", "Automated machine interlock halts defective assemblies instantly"),
                ]
            }

        # 16. INSIGHT AND EVIDENCE
        if primitive_key == "insight_and_evidence":
            return {
                "insight_headline": "Root cause of variance is disconnected execution, not operator capability.",
                "evidence_points": [
                    ("82% of batch release delays stem from manual paper traveler transcription into SAP."),
                    ("Machine calibration drifts 3.5 hours before supervisors receive shift variance notifications."),
                    ("Single-piece electronic genealogy eliminates 94% of containment search hours during customer audits."),
                ]
            }

        # 17. OUTCOME CHAIN
        if primitive_key == "outcome_chain":
            return {
                "chains": [
                    ("Standardized BTP Integration", "Sub-second event dispatch", "Zero ERP buffer backlog", "+$1.8M Working Capital"),
                    ("Electronic Lot Genealogy", "Real-time Poka-Yoke interlocking", "99.4% First Pass Yield", "+420 bps Gross Margin"),
                    ("Automated Goods Receipt", "Real-time 101 ledger tie-out", "Zero inventory reconciliation delay", "+3.3 Mo Cash Acceleration"),
                ]
            }

        # 18. OPERATING MODEL
        if primitive_key == "operating_model":
            return {
                "layers": [
                    ("Corporate Steering", "Monthly", ["Capital allocation", "Architecture principles", "Program KPIs"]),
                    ("Architecture Review Board", "Bi-Weekly", ["Clean-core compliance", "Interface standards", "Security approvals"]),
                    ("Plant Execution Teams", "Daily Agile", ["Work-center enablement", "Shift OEE reviews", "Continuous improvement"]),
                ]
            }

        # 19. CAPABILITY MAP
        if primitive_key == "capability_map":
            return {
                "domains": [
                    ("Production Execution", ["Digital Work Instructions", "Work Order Dispatch", "Electronic Batch Records"]),
                    ("Quality & Genealogy", ["Component Lot Tracing", "In-Line SPC Alerts", "Non-Conformance Quarantine"]),
                    ("Enterprise Integration", ["SAP PP Order Sync", "BOM Consumption", "Automated Goods Receipt"]),
                ]
            }

        # 20. COST BENEFIT SUMMARY
        if primitive_key == "cost_benefit_summary":
            return {
                "benefits": [
                    ("Scrap & Non-Conformance Reduction", "$1,450,000", "58% reduction in machining rework"),
                    ("Working Capital & WIP Acceleration", "$1,820,000", "4-day reduction in cycle time"),
                    ("Paperless Compliance & Audit Hours", "$620,000", "Elimination of paper traveler handling"),
                ],
                "total_value": "$3,890,000 Annualized Net EBITDA Impact",
                "payback_period": "5.4 Months Post Go-Live"
            }

        # 21. APPROVAL GATES
        if primitive_key == "approval_gates":
            return {
                "gates": [
                    ("Gate 1: Architecture Sign-Off", "Chief Enterprise Architect", "Sprint 0", ["Clean-core rules validated", "OT firewall verified", "Data models approved"], "Signed Architecture Charter"),
                    ("Gate 2: Pilot Plant Acceptance", "Plant Operations Director", "Sprint 4", ["Pilot line latency <200ms", "Zero dropped telemetry events", "Operator ergonomics passed"], "Pilot Sign-Off Slip"),
                    ("Gate 3: Quality Compliance", "Global VP of Quality", "Sprint 8", ["21 CFR Part 11 audit trails", "Electronic signatures tested", "Lot genealogy tied to ERP"], "Validation Master Report"),
                    ("Gate 4: Production Cutover", "Executive Steering Comm", "Sprint 12", ["Go-live checklist 100% green", "Disaster recovery tested", "24/7 hypercare staffed"], "Production Go-Live Permit"),
                ]
            }

        # 22. TRANSFORMATION ROADMAP
        if primitive_key == "transformation_roadmap":
            return {
                "phases": [
                    ("PHASE 1", "Weeks 1-4", "Blueprint & Edge Setup", ["OPC-UA Edge Config", "SAP BTP Subaccount Setup", "Pilot Line Connect"], "GATE 1: Latency <250ms"),
                    ("PHASE 2", "Weeks 5-10", "Core MES Integration", ["Production Order Dispatch", "Electronic Traveler UI", "QA Inspection Gates"], "GATE 2: Zero RFC Buffer Leaks"),
                    ("PHASE 3", "Weeks 11-16", "Enterprise Rollout", ["Lines 2-6 Cutover", "Operator Enablement", "Hypercare Support"], "GATE 3: Final Acceptance"),
                ]
            }

        # 23. MILESTONE GATES
        if primitive_key == "milestone_gates":
            return {
                "gates": [
                    ("1", "Architecture Blueprint", ["BTP event mesh sized", "Clean-core APIs catalogued", "Security boundaries approved"], "Chief Architect"),
                    ("2", "Pilot Line Deployment", ["Work-center dispatch live", "Inline vision cameras tested", "Zero dropped telemetry"], "Plant Director"),
                    ("3", "Quality Certification", ["21 CFR Part 11 signed", "Genealogy tree validated", "Audit trail verified"], "VP Quality"),
                    ("4", "Enterprise Go-Live", ["Multi-plant cutover completed", "Real-time 101 posting live", "Hypercare SLA active"], "Steering Committee"),
                ]
            }

        # 24. TIMELINE
        if primitive_key == "timeline":
            return {
                "milestones": [
                    ("Month 1", "Sprint 0: Architecture Blueprint", "BTP subaccounts & OT edge configuration"),
                    ("Month 2", "Sprint 1-2: Pilot Line Deployment", "CNC machining cell connected & telemetry live"),
                    ("Month 3", "Sprint 3-4: Quality & Genealogy", "Electronic batch record & camera inspection live"),
                    ("Month 4", "Sprint 5-6: Enterprise Cutover", "Full plant rollout & 24/7 hypercare transition"),
                ]
            }

        # 25. COMPARISON MATRIX (Scope Table)
        if primitive_key == "comparison_matrix":
            return {
                "options": ["In-Scope (Turnkey)", "Customer Responsibility", "Out-of-Scope (Phase 2)"],
                "criteria": [
                    ("SAP BTP Event Mesh Setup", ["FULL (Turnkey)", "PARTIAL (Access)", "NO"]),
                    ("OPC-UA Machine Telemetry", ["FULL (Turnkey)", "PARTIAL (Network)", "NO"]),
                    ("Electronic Batch Records", ["FULL (Turnkey)", "PARTIAL (SOP Sign-off)", "NO"]),
                    ("Multi-Site Cloud Rollout", ["NO", "NO", "RECOMMENDED"]),
                ]
            }

        # 26. COMMERCIAL TABLE
        if primitive_key == "commercial_table":
            return {
                "milestones": [
                    ("Phase 1: Architecture Blueprint", "Architecture blueprint & security sign-off", "Weeks 1-3", "25%", "$85,000"),
                    ("Phase 2: Pilot Implementation", "Pilot line integration & telemetry validation", "Weeks 4-8", "35%", "$119,000"),
                    ("Phase 3: Plant Rollout", "Full plant cutover & operator enablement", "Weeks 9-14", "30%", "$102,000"),
                    ("Phase 4: Final Acceptance", "30-day hypercare completion & ledger audit", "Weeks 15-16", "10%", "$34,000"),
                ],
                "total_amount": "$340,000 Turnkey Fixed Investment"
            }

        # 27. RACI RESPONSIBILITY (Dependencies)
        if primitive_key == "raci_responsibility":
            return {
                "roles": ["Advisory Architect", "Client IT Lead", "Plant Operations Lead", "Steering Committee"],
                "deliverables": [
                    ("System Architecture & BTP Sizing", ["A", "R", "C", "I"]),
                    ("OT Network & Firewall Exceptions", ["C", "A", "R", "I"]),
                    ("Operator Enablement & SOP Sign-off", ["R", "C", "A", "I"]),
                    ("Milestone Gate Sign-off & Invoicing", ["C", "C", "C", "A"]),
                ]
            }

        # 28. APPLICATION LANDSCAPE
        if primitive_key == "application_landscape":
            return {
                "domains": [
                    ("Enterprise ERP Core", ["SAP S/4HANA (PP/MM)", "SAP S/4HANA (FI/CO)", "Master Data Governance"]),
                    ("Integration & Middleware", ["SAP BTP Integration Suite", "BTP Event Mesh", "API Management Gateway"]),
                    ("Operations & Execution", ["SAP Digital Manufacturing", "Plant SCADA Suite", "Electronic Traveler UI"]),
                ]
            }

        # Fallback default
        return {
            "title": slide_title,
            "topic": topic,
            "client": client_name
        }


# =============================================================================
# 3. Scenario Deck Result & Presentation Engine
# =============================================================================

@dataclass
class ScenarioDeckResult:
    """Complete diagnostic and execution result for an automated scenario deck."""
    scenario_id: str
    scenario_title: str
    output_path: str
    slide_count: int
    visual_forms_chosen: List[str]
    primitives_used: List[str]
    quality_report: QualityGateReport
    is_export_authorized: bool
    diversity_score: int


class ScenarioPresentationEngine:
    """
    Automated presentation generator for complex business scenarios.
    
    Dynamically maps requested semantic requirements to distinct visual forms,
    enforces anti-monotony visual rhythm, renders native PPTX shapes,
    and runs the Presentation Quality Gate before export.
    """

    @classmethod
    def build_scenario_presentation(
        cls,
        scenario_id: str,
        title: str,
        topic: str,
        client_name: str,
        requirements: List[str],
        output_path: Optional[str] = None
    ) -> ScenarioDeckResult:
        """
        Builds, validates, and exports an automated presentation for a scenario.
        """
        prs = Presentation()
        prs.slide_width = Inches(CanvasBounds.width)
        prs.slide_height = Inches(CanvasBounds.height)
        blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]

        total_slides = len(requirements)
        visual_forms_chosen: List[str] = []
        primitives_used: List[str] = []

        last_theme = "slate"
        last_primitive = ""

        for slide_idx, req in enumerate(requirements, start=1):
            # 1. Semantic Form Resolution
            desc = SemanticVisualFormResolver.resolve_requirement(req)
            visual_forms_chosen.append(desc.display_name)
            primitives_used.append(desc.primitive_key)

            # 2. Theme & Visual Rhythm (alternate dark / light for visual breathing room)
            if slide_idx == 1 or slide_idx == total_slides:
                cur_theme_mode = "navy"
            elif desc.primitive_key == last_primitive:
                cur_theme_mode = "slate" if last_theme == "navy" else "navy"
            else:
                cur_theme_mode = desc.preferred_theme

            theme = ExecutiveNavyTheme if cur_theme_mode == "navy" else ConsultingSlateTheme
            last_theme = cur_theme_mode
            last_primitive = desc.primitive_key

            # 3. Add Slide & Themed Canvas
            slide = prs.slides.add_slide(blank_layout)
            bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(CanvasBounds.width), Inches(CanvasBounds.height))
            bg.fill.solid()
            bg.fill.fore_color.rgb = theme.canvas
            bg.line.fill.background()

            # 4. Universal Header
            slide_action_title = f"{desc.display_name}: {topic}"
            slide_subtitle = f"DECISION INTENT: {desc.category_tag} mapped for {client_name} operational architecture."
            HeaderPrimitive.render(
                slide=slide,
                category_text=f"{slide_idx}. {desc.category_tag}",
                title_text=slide_action_title,
                subtitle_text=slide_subtitle,
                theme=theme
            )

            # 5. Universal Footer
            FooterPrimitive.render(
                slide=slide,
                slide_num=slide_idx,
                total_slides=total_slides,
                metadata_text=f"{client_name} • {title} • Enterprise Architecture Advisory",
                theme=theme
            )

            # 6. Render Native Visual Primitive
            meta = lib.get_primitive_metadata(desc.primitive_key)
            if meta:
                prim_cls = meta["class"]
                payload = DomainPayloadSynthesizer.synthesize_payload(desc.primitive_key, topic, client_name, desc.display_name)
                
                left = Margins.left
                top = SpacingScale.CONTENT_TOP
                width = Margins().usable_width
                height = SpacingScale.CONTENT_HEIGHT

                # Dispatch primitive
                cls._dispatch_primitive(slide, prim_cls, desc.primitive_key, left, top, width, height, payload, theme)

        # 7. Quality Gate Audit & Auto-Remediation
        report = PresentationQualityGate.audit_and_remediate(prs, auto_remediate=True)

        # 8. Save Presentation
        dest_path = output_path or f"{scenario_id}.pptx"
        prs.save(dest_path)

        diversity_count = len(set(primitives_used))
        diversity_score = int((diversity_count / max(1, total_slides)) * 100)

        return ScenarioDeckResult(
            scenario_id=scenario_id,
            scenario_title=title,
            output_path=dest_path,
            slide_count=total_slides,
            visual_forms_chosen=visual_forms_chosen,
            primitives_used=primitives_used,
            quality_report=report,
            is_export_authorized=report.is_export_authorized,
            diversity_score=diversity_score
        )

    @staticmethod
    def _dispatch_primitive(slide, prim_cls, prim_key: str, left: float, top: float, width: float, height: float, data: Dict[str, Any], theme: Theme):
        """Safely dispatches keyword payload into primitive class render method."""
        import inspect
        sig = inspect.signature(prim_cls.render)
        all_param_names = [p.name for p in sig.parameters.values()]
        custom_params = [name for name in all_param_names if name not in ("slide", "left", "top", "width", "height", "theme")]

        kwargs = {
            "slide": slide,
            "left": left,
            "top": top,
            "width": width,
            "height": height,
            "theme": theme,
        }

        for k, v in data.items():
            if k in custom_params:
                kwargs[k] = v

        try:
            prim_cls.render(**kwargs)
        except Exception as e:
            tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
            tf = tb.text_frame
            TypographySystem.apply_to_paragraph(tf.paragraphs[0], TypographySystem.BODY_STRONG, f"Primitive Dispatch: {str(e)}", theme.status_critical)
