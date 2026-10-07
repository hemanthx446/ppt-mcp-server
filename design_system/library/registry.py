"""
Visual Primitive Registry & Dispatcher.

Provides a unified catalog, metadata, parameter schema, and execution
dispatcher for all 60 enterprise visual primitives.
"""

from typing import Dict, Any, List, Optional, Callable
from pptx.util import Inches
from ..color import ColorSystem, Theme, ExecutiveNavyTheme, ConsultingSlateTheme
from ..spacing import Margins, SpacingScale
import design_system.library as lib


PRIMITIVE_CATALOG: Dict[str, Dict[str, Any]] = {
    # -------------------------------------------------------------------------
    # ARCHITECTURE (1–9)
    # -------------------------------------------------------------------------
    "system_architecture": {
        "id": 1,
        "name": "System Architecture",
        "category": "ARCHITECTURE",
        "class": lib.SystemArchitecturePrimitive,
        "description": "Multi-tier decoupled system architecture with protocol connectors and boundaries.",
    },
    "layered_architecture": {
        "id": 2,
        "name": "Layered Architecture",
        "category": "ARCHITECTURE",
        "class": lib.LayeredArchitecturePrimitive,
        "description": "Horizontal architectural tiers (Presentation, Business Logic, Integration, Data).",
    },
    "enterprise_to_shopfloor": {
        "id": 3,
        "name": "Enterprise-to-Shopfloor Architecture",
        "category": "ARCHITECTURE",
        "class": lib.EnterpriseToShopfloorPrimitive,
        "description": "ISA-95 Level 4 (ERP) down to Level 1/0 (Sensors/Actuators) operational hierarchy.",
    },
    "application_landscape": {
        "id": 4,
        "name": "Application Landscape",
        "category": "ARCHITECTURE",
        "class": lib.ApplicationLandscapePrimitive,
        "description": "Multi-domain application portfolio across functional pillars.",
    },
    "integration_architecture": {
        "id": 5,
        "name": "Integration Architecture",
        "category": "ARCHITECTURE",
        "class": lib.IntegrationArchitecturePrimitive,
        "description": "Producer -> Message Broker / Queue -> Consumer event integration pipeline.",
    },
    "data_flow_architecture": {
        "id": 6,
        "name": "Data Flow Architecture",
        "category": "ARCHITECTURE",
        "class": lib.DataFlowArchitecturePrimitive,
        "description": "End-to-end data pipeline from ingestion to curation, semantic modeling, and consumption.",
    },
    "security_boundary": {
        "id": 7,
        "name": "Security Boundary",
        "category": "ARCHITECTURE",
        "class": lib.SecurityBoundaryPrimitive,
        "description": "Zoned network security perimeters (Internet, DMZ, Intranet, Air-Gapped OT).",
    },
    "deployment_architecture": {
        "id": 8,
        "name": "Deployment Architecture",
        "category": "ARCHITECTURE",
        "class": lib.DeploymentArchitecturePrimitive,
        "description": "Cloud hosting regions paired with on-premise edge appliance deployments.",
    },
    "cloud_edge_architecture": {
        "id": 9,
        "name": "Cloud / Edge Architecture",
        "category": "ARCHITECTURE",
        "class": lib.CloudEdgeArchitecturePrimitive,
        "description": "Cloud control plane coordination vs local disconnected edge runtime autonomy.",
    },

    # -------------------------------------------------------------------------
    # PROCESS (10–16)
    # -------------------------------------------------------------------------
    "horizontal_process_flow": {
        "id": 10,
        "name": "Horizontal Process Flow",
        "category": "PROCESS",
        "class": lib.HorizontalProcessFlowPrimitive,
        "description": "Sequential step-by-step horizontal progression with connecting chevrons.",
    },
    "vertical_process_flow": {
        "id": 11,
        "name": "Vertical Process Flow",
        "category": "PROCESS",
        "class": lib.VerticalProcessFlowPrimitive,
        "description": "Vertical cascading lifecycle steps with status checkpoints.",
    },
    "value_stream": {
        "id": 12,
        "name": "End-to-End Value Stream",
        "category": "PROCESS",
        "class": lib.ValueStreamPrimitive,
        "description": "Lean value stream mapping: Lead time, processing cycle time, and value-add ratios.",
    },
    "operational_workflow": {
        "id": 13,
        "name": "Operational Workflow",
        "category": "PROCESS",
        "class": lib.OperationalWorkflowPrimitive,
        "description": "Multi-role step workflow: Trigger, Actor, Action, Verification, and Next Stage.",
    },
    "swimlane_process": {
        "id": 14,
        "name": "Swimlane Process",
        "category": "PROCESS",
        "class": lib.SwimlaneProcessPrimitive,
        "description": "Cross-functional process flows separated across departmental swimlanes.",
    },
    "decision_flow": {
        "id": 15,
        "name": "Decision Flow",
        "category": "PROCESS",
        "class": lib.DecisionFlowPrimitive,
        "description": "Branching decision gate with evaluated criteria and pass/fail routes.",
    },
    "exception_rework_flow": {
        "id": 16,
        "name": "Exception / Rework Flow",
        "category": "PROCESS",
        "class": lib.ExceptionReworkFlowPrimitive,
        "description": "Happy path execution flow paired with NCR defect logging and loopback rework.",
    },

    # -------------------------------------------------------------------------
    # DATA (17–21)
    # -------------------------------------------------------------------------
    "data_lineage": {
        "id": 17,
        "name": "Data Lineage",
        "category": "DATA",
        "class": lib.DataLineagePrimitive,
        "description": "Lineage path from raw operational sources through Lakehouse to executive consumption.",
    },
    "entity_relationship": {
        "id": 18,
        "name": "Entity Relationship View",
        "category": "DATA",
        "class": lib.EntityRelationshipPrimitive,
        "description": "Relational entity schemas showing primary keys, attributes, and foreign connections.",
    },
    "genealogy_tree": {
        "id": 19,
        "name": "Genealogy Tree",
        "category": "DATA",
        "class": lib.GenealogyTreePrimitive,
        "description": "360-degree finished product serial number traceability down to component batches.",
    },
    "parent_child_relationship": {
        "id": 20,
        "name": "Parent-Child Relationship",
        "category": "DATA",
        "class": lib.ParentChildRelationshipPrimitive,
        "description": "Multi-tier indented bill-of-materials (BOM) hierarchy with quantities and revisions.",
    },
    "data_lifecycle": {
        "id": 21,
        "name": "Data Lifecycle",
        "category": "DATA",
        "class": lib.DataLifecyclePrimitive,
        "description": "Data governance lifecycle: Create/Ingest, Store, Process, Archive, and Purge.",
    },

    # -------------------------------------------------------------------------
    # ANALYTICS (22–34)
    # -------------------------------------------------------------------------
    "kpi_strip": {
        "id": 22,
        "name": "KPI Strip",
        "category": "ANALYTICS",
        "class": lib.KPIStripPrimitive,
        "description": "Horizontal executive metric strip with values, labels, context, and trend deltas.",
    },
    "executive_dashboard": {
        "id": 23,
        "name": "Executive Dashboard",
        "category": "ANALYTICS",
        "class": lib.ExecutiveDashboardPrimitive,
        "description": "Composite analytical cockpit pairing top KPIs with operational telemetry cards.",
    },
    "trend_chart": {
        "id": 24,
        "name": "Trend Chart",
        "category": "ANALYTICS",
        "class": lib.TrendChartPrimitive,
        "description": "Native, editable PowerPoint multi-series line trend chart.",
    },
    "bar_chart": {
        "id": 25,
        "name": "Bar Chart",
        "category": "ANALYTICS",
        "class": lib.BarChartPrimitive,
        "description": "Native, editable PowerPoint clustered bar/column comparison chart.",
    },
    "stacked_bar": {
        "id": 26,
        "name": "Stacked Bar",
        "category": "ANALYTICS",
        "class": lib.StackedBarPrimitive,
        "description": "Native, editable PowerPoint stacked bar chart for part-to-whole comparisons.",
    },
    "line_chart": {
        "id": 27,
        "name": "Line Chart",
        "category": "ANALYTICS",
        "class": lib.LineChartPrimitive,
        "description": "Native, editable PowerPoint time-series line chart.",
    },
    "waterfall": {
        "id": 28,
        "name": "Waterfall Chart",
        "category": "ANALYTICS",
        "class": lib.WaterfallPrimitive,
        "description": "Cumulative step variance waterfall (Initial Baseline -> Steps +/- -> Final Net).",
    },
    "pareto": {
        "id": 29,
        "name": "Pareto Analysis",
        "category": "ANALYTICS",
        "class": lib.ParetoPrimitive,
        "description": "80/20 root cause concentration ranking frequency and cumulative impact.",
    },
    "heatmap": {
        "id": 30,
        "name": "Heatmap",
        "category": "ANALYTICS",
        "class": lib.HeatmapPrimitive,
        "description": "2D matrix grid color-coded by intensity values (shifts vs hours vs defects).",
    },
    "variance_view": {
        "id": 31,
        "name": "Variance View",
        "category": "ANALYTICS",
        "class": lib.VarianceViewPrimitive,
        "description": "Actual vs Budget / Target operational performance with favorable/unfavorable deltas.",
    },
    "capacity_vs_demand": {
        "id": 32,
        "name": "Capacity vs Demand",
        "category": "ANALYTICS",
        "class": lib.CapacityVsDemandPrimitive,
        "description": "Machine/plant capacity limits plotted against forecasted production demand.",
    },
    "aging_analysis": {
        "id": 33,
        "name": "Aging Analysis",
        "category": "ANALYTICS",
        "class": lib.AgingAnalysisPrimitive,
        "description": "Bucketized aging distribution (0-30d, 31-60d, 61-90d, 90d+) for inventory or debt.",
    },
    "risk_matrix": {
        "id": 34,
        "name": "Risk Matrix",
        "category": "ANALYTICS",
        "class": lib.RiskMatrixPrimitive,
        "description": "Severity vs Likelihood 3x3 risk quadrant highlighting critical enterprise exposure.",
    },

    # -------------------------------------------------------------------------
    # BUSINESS (35–41)
    # -------------------------------------------------------------------------
    "capability_map": {
        "id": 35,
        "name": "Capability Map",
        "category": "BUSINESS",
        "class": lib.CapabilityMapPrimitive,
        "description": "Functional domain breakdown into core operational business capabilities.",
    },
    "operating_model": {
        "id": 36,
        "name": "Operating Model",
        "category": "BUSINESS",
        "class": lib.OperatingModelPrimitive,
        "description": "People, Process, Technology, and Governance target operating framework.",
    },
    "outcome_chain": {
        "id": 37,
        "name": "Outcome Chain",
        "category": "BUSINESS",
        "class": lib.OutcomeChainPrimitive,
        "description": "Strategic lever -> Operational mechanism -> Financial outcome causal chain.",
    },
    "value_driver_tree": {
        "id": 38,
        "name": "Value Driver Tree",
        "category": "BUSINESS",
        "class": lib.ValueDriverTreePrimitive,
        "description": "Top-line financial objective branching into operational sub-drivers and KPIs.",
    },
    "decision_matrix": {
        "id": 39,
        "name": "Decision Matrix",
        "category": "BUSINESS",
        "class": lib.DecisionMatrixPrimitive,
        "description": "Evaluation of strategic choices against weighted business decision criteria.",
    },
    "maturity_model": {
        "id": 40,
        "name": "Maturity Model",
        "category": "BUSINESS",
        "class": lib.MaturityModelPrimitive,
        "description": "5-stage staircase maturity progression (Ad-Hoc -> Managed -> Defined -> Measured -> Optimized).",
    },
    "current_vs_future_state": {
        "id": 41,
        "name": "Current vs Future State",
        "category": "BUSINESS",
        "class": lib.CurrentVsFutureStatePrimitive,
        "description": "As-Is operational friction side-by-side with To-Be architectural capabilities.",
    },

    # -------------------------------------------------------------------------
    # DELIVERY (42–46)
    # -------------------------------------------------------------------------
    "transformation_roadmap": {
        "id": 42,
        "name": "Transformation Roadmap",
        "category": "DELIVERY",
        "class": lib.TransformationRoadmapPrimitive,
        "description": "Phased implementation program over time with deliverables and sign-off gates.",
    },
    "timeline": {
        "id": 43,
        "name": "Timeline",
        "category": "DELIVERY",
        "class": lib.TimelinePrimitive,
        "description": "Chronological timeline track with date markers and deliverable flags.",
    },
    "milestone_gates": {
        "id": 44,
        "name": "Milestone Gates",
        "category": "DELIVERY",
        "class": lib.MilestoneGatesPrimitive,
        "description": "Stage-gate control framework (Gate 1 -> Gate 2 -> Gate 3) with entrance/exit criteria.",
    },
    "release_plan": {
        "id": 45,
        "name": "Release Plan",
        "category": "DELIVERY",
        "class": lib.ReleasePlanPrimitive,
        "description": "Quarterly release cadence and software deployment schedule.",
    },
    "workstream_view": {
        "id": 46,
        "name": "Workstream View",
        "category": "DELIVERY",
        "class": lib.WorkstreamViewPrimitive,
        "description": "Parallel track workstream schedule (Architecture, Build, Integration, Enablement).",
    },

    # -------------------------------------------------------------------------
    # GOVERNANCE (47–50)
    # -------------------------------------------------------------------------
    "approval_gates": {
        "id": 47,
        "name": "Approval Gates",
        "category": "GOVERNANCE",
        "class": lib.ApprovalGatesPrimitive,
        "description": "Multi-tier approval pipeline with sign-off authorities and audit slips.",
    },
    "raci_responsibility": {
        "id": 48,
        "name": "RACI Responsibility Matrix",
        "category": "GOVERNANCE",
        "class": lib.RACIResponsibilityPrimitive,
        "description": "Native PowerPoint RACI matrix mapping project deliverables against roles.",
    },
    "control_framework": {
        "id": 49,
        "name": "Control Framework",
        "category": "GOVERNANCE",
        "class": lib.ControlFrameworkPrimitive,
        "description": "Enterprise compliance framework: Preventive, Detective, and Corrective controls.",
    },
    "governance_model": {
        "id": 50,
        "name": "Governance Model",
        "category": "GOVERNANCE",
        "class": lib.GovernanceModelPrimitive,
        "description": "Multi-tier organizational governance: Steering Committee -> ARB -> Delivery Pods.",
    },

    # -------------------------------------------------------------------------
    # STRUCTURED INFORMATION (51–56)
    # -------------------------------------------------------------------------
    "professional_table": {
        "id": 51,
        "name": "Professional Table",
        "category": "STRUCTURED INFORMATION",
        "class": lib.ProfessionalTablePrimitive,
        "description": "Native PowerPoint enterprise table with column weighting, zebra fills, and typography tokens.",
    },
    "comparison_matrix": {
        "id": 52,
        "name": "Comparison Matrix",
        "category": "STRUCTURED INFORMATION",
        "class": lib.ComparisonMatrixPrimitive,
        "description": "Option comparison matrix across criteria with status pills and checkmarks.",
    },
    "commercial_table": {
        "id": 53,
        "name": "Commercial Table",
        "category": "STRUCTURED INFORMATION",
        "class": lib.CommercialTablePrimitive,
        "description": "Milestone investment schedule with fee percentages, payment terms, and totals.",
    },
    "kpi_table": {
        "id": 54,
        "name": "KPI Table",
        "category": "STRUCTURED INFORMATION",
        "class": lib.KPITablePrimitive,
        "description": "KPI tracking register with baselines, targets, measurement frequency, and status pills.",
    },
    "action_register": {
        "id": 55,
        "name": "Action Register",
        "category": "STRUCTURED INFORMATION",
        "class": lib.ActionRegisterPrimitive,
        "description": "Action item tracking register: Action ID, Workstream, Priority, Owner, and Status.",
    },
    "risk_register": {
        "id": 56,
        "name": "Risk Register",
        "category": "STRUCTURED INFORMATION",
        "class": lib.RiskRegisterPrimitive,
        "description": "Enterprise risk log: Risk ID, Vulnerability, Severity, Likelihood, Mitigation, and Owner.",
    },

    # -------------------------------------------------------------------------
    # NARRATIVE (57–60)
    # -------------------------------------------------------------------------
    "executive_statement": {
        "id": 57,
        "name": "Executive Statement",
        "category": "NARRATIVE",
        "class": lib.ExecutiveStatementPrimitive,
        "description": "Hero CXO quote thesis block, attribution pill, and supporting strategic pillars.",
    },
    "insight_and_evidence": {
        "id": 58,
        "name": "Insight + Evidence",
        "category": "NARRATIVE",
        "class": lib.InsightAndEvidencePrimitive,
        "description": "Analytical pairing: Left: Key Analytical Insight; Right: Quantitative Evidence metrics.",
    },
    "key_takeaway": {
        "id": 59,
        "name": "Key Takeaway",
        "category": "NARRATIVE",
        "class": lib.KeyTakeawayPrimitive,
        "description": "Executive conclusion summary with numbered strategic actions and call-to-action banner.",
    },
    "section_divider": {
        "id": 60,
        "name": "Section Divider",
        "category": "NARRATIVE",
        "class": lib.SectionDividerPrimitive,
        "description": "High-impact section transition slide with large section numbering and module agenda track.",
    },
}


def normalize_primitive_key(key: str) -> str:
    """Normalizes string or class name to standard registry key."""
    cleaned = key.strip().lower()
    cleaned = cleaned.replace("primitive", "").replace("-", "_").replace(" ", "_")
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    cleaned = cleaned.strip("_")
    return cleaned


def get_primitive_metadata(name_or_key: str) -> Optional[Dict[str, Any]]:
    """Retrieves metadata definition for a primitive."""
    norm_key = normalize_primitive_key(name_or_key)
    if norm_key in PRIMITIVE_CATALOG:
        res = dict(PRIMITIVE_CATALOG[norm_key])
        res["key"] = norm_key
        return res
    for k, v in PRIMITIVE_CATALOG.items():
        if str(v["id"]) == name_or_key.strip() or v["name"].lower() == name_or_key.strip().lower():
            res = dict(v)
            res["key"] = k
            return res
    return None


def list_primitives_catalog() -> List[Dict[str, Any]]:
    """Returns a serializable list of all 60 visual primitives."""
    items = []
    for k, v in sorted(PRIMITIVE_CATALOG.items(), key=lambda x: x[1]["id"]):
        items.append({
            "id": v["id"],
            "key": k,
            "name": v["name"],
            "category": v["category"],
            "description": v["description"]
        })
    return items
