"""
Transformation & Process Semantic Layer.

Defines formal semantic relationship types, process nodes, decision branches,
swimlanes, transformation bridges, maturity models, and relationship inference
for enterprise and manufacturing digital transformations.

Core Design Principle:
"Never choose a visual because it is easy to render. Choose a visual because
it best expresses the underlying relationship, decision, process, architecture, or evidence."
"Cards are a component, not a presentation architecture."
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Set, Tuple, Optional, Any
import re


# =============================================================================
# 1. Transformation Relationship Types
# =============================================================================

class TransformationRelationType(Enum):
    """Strongly typed semantic vocabulary for enterprise transformation relationships."""
    # CURRENT_STATE -> PAIN / GAP -> INTERVENTION -> FUTURE_STATE -> BUSINESS_OUTCOME
    TRANSFORMATION_BRIDGE = auto()

    # TRIGGER -> PROCESS STEP -> DECISION -> ACTION -> OUTCOME -> FEEDBACK
    PROCESS_EXECUTION = auto()

    # SOURCE -> INTEGRATION -> TRANSFORMATION / CONTEXT -> CONSUMER -> DECISION / ACTION
    SYSTEM_DATA_FLOW = auto()

    # DEMAND -> PLAN -> PRODUCTION ORDER -> DISPATCH -> EXECUTE -> CONSUME -> QUALITY -> CONFIRM -> INVENTORY / COST
    MANUFACTURING_EXECUTION = auto()

    # PHYSICAL WORLD -> DIGITAL CAPTURE -> CONTEXTUALIZATION -> INTELLIGENCE -> DECISION -> ACTION -> PHYSICAL
    CLOSED_LOOP_FEEDBACK = auto()

    # ASSESS -> SCORE -> IDENTIFY GAP -> PRIORITIZE -> TARGET STATE -> ROADMAP -> MEASURE
    MATURITY_PROGRESSION = auto()

    # REQUEST -> VALIDATION -> CONTROL GATE -> APPROVAL -> EXECUTION -> EVIDENCE -> AUDIT
    GOVERNANCE_GATEWAY = auto()

    # SIGNAL -> DETECTION -> ASSESSMENT -> DECISION -> MITIGATION -> VALIDATION
    RISK_CHAIN = auto()

    # GENEALOGY / TRACEABILITY (Finished Unit -> Serial -> Order -> Lot -> Machine -> Quality)
    GENEALOGY_TRACEABILITY = auto()

    # CROSS_FUNCTIONAL_SWIMLANE (Customer -> ERP -> MES -> Shop Floor -> Quality -> Confirmation)
    CROSS_FUNCTIONAL_SWIMLANE = auto()


# =============================================================================
# 2. Process Flow Node & Branch Models
# =============================================================================

class ProcessNodeType(Enum):
    """Semantic classification of a process node."""
    TRIGGER = auto()           # Start or external demand trigger
    STEP = auto()              # Standard operational or transactional activity
    DECISION = auto()          # Branching decision gate (e.g. Quality Pass/Fail)
    ACTION = auto()            # Directed action or operational execution
    QUALITY_GATE = auto()      # Inspection, compliance, or validation interlock
    SYSTEM_HANDOFF = auto()    # Transaction handoff across system boundary
    REWORK_LOOP = auto()       # Corrective exception or rework path
    OUTCOME = auto()           # Terminal business or operational deliverable


@dataclass
class ProcessNode:
    """A semantic node in a business or manufacturing process."""
    id: str
    label: str
    node_type: ProcessNodeType = ProcessNodeType.STEP
    role_lane: str = "Enterprise"          # Assigned swimlane actor/system
    system_tag: Optional[str] = None       # e.g., "SAP S/4HANA", "MES", "PLC"
    action_detail: Optional[str] = None    # Descriptive action
    poka_yoke: Optional[str] = None        # Error-proofing or interlock rule
    metric_kpi: Optional[str] = None       # SLA, cycle time, or lead time
    is_decision: bool = False              # Renders as diamond


@dataclass
class ProcessBranch:
    """A directed relationship or handoff between two process nodes."""
    source_id: str
    target_id: str
    condition_label: Optional[str] = None  # e.g., "PASS", "FAIL", "REWORK", "CONFIRM"
    is_feedback_loop: bool = False         # Returns to prior stage
    is_exception_path: bool = False        # Deviates from happy path
    protocol: Optional[str] = None         # e.g., "OData", "OPC UA", "RFC"


@dataclass
class ProcessFlowModel:
    """Complete semantic model of a process flow."""
    title: str
    nodes: List[ProcessNode]
    branches: List[ProcessBranch]
    subtitle: Optional[str] = None
    relation_type: TransformationRelationType = TransformationRelationType.PROCESS_EXECUTION


# =============================================================================
# 3. Swimlane Model
# =============================================================================

@dataclass
class SwimlaneLane:
    """A distinct functional or system swimlane band."""
    lane_id: str
    lane_name: str                         # e.g., "CUSTOMER", "SAP S/4HANA", "MES", "SHOP FLOOR / OT", "QUALITY"
    system_tag: Optional[str] = None       # e.g., "System of Record", "Execution Core", "Physical Layer"
    order: int = 0


@dataclass
class SwimlaneStep:
    """A step placed inside a specific swimlane."""
    step_id: str
    lane_id: str
    title: str
    sequence_order: int                    # Horizontal sequence 1..N
    subtitle: Optional[str] = None
    node_type: ProcessNodeType = ProcessNodeType.STEP
    is_decision: bool = False
    system_badge: Optional[str] = None
    kpi_annotation: Optional[str] = None


@dataclass
class SwimlaneHandoff:
    """A transactional connector crossing or linking swimlane steps."""
    from_step_id: str
    to_step_id: str
    label: Optional[str] = None            # e.g., "Production Order", "Dispatch", "Confirmation"
    protocol: Optional[str] = None         # e.g., "BAPI", "OData", "OPC UA"
    is_feedback: bool = False


@dataclass
class SwimlaneDiagramModel:
    """Complete semantic model of a cross-functional swimlane diagram."""
    title: str
    lanes: List[SwimlaneLane]
    steps: List[SwimlaneStep]
    handoffs: List[SwimlaneHandoff]
    subtitle: Optional[str] = None


# =============================================================================
# 4. Transformation Bridge Model
# =============================================================================

@dataclass
class CurrentStateSnapshot:
    """Baseline reality, friction, and pain points."""
    title: str = "CURRENT STATE (Baseline)"
    pain_points: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    baseline_metrics: List[Tuple[str, str]] = field(default_factory=list)  # [(label, value)]


@dataclass
class TransformationIntervention:
    """Strategic and technical interventions bridging to target state."""
    title: str = "TRANSFORMATION INTERVENTIONS"
    initiatives: List[str] = field(default_factory=list)
    enablers: List[str] = field(default_factory=list)
    governance_gates: List[str] = field(default_factory=list)


@dataclass
class FutureStateVision:
    """Target operating model and measurable business outcomes."""
    title: str = "FUTURE STATE (Target Operating Model)"
    transformed_capabilities: List[str] = field(default_factory=list)
    operating_model_shifts: List[str] = field(default_factory=list)
    target_outcomes: List[Tuple[str, str]] = field(default_factory=list)  # [(metric, value)]


@dataclass
class TransformationBridgeModel:
    """Complete semantic model of a Current -> Intervention -> Future transformation bridge."""
    title: str
    current_state: CurrentStateSnapshot
    intervention: TransformationIntervention
    future_state: FutureStateVision
    subtitle: Optional[str] = None
    timeframe: str = "12–18 Month Execution Horizon"


# =============================================================================
# 5. Maturity Assessment Model
# =============================================================================

@dataclass
class MaturityDimensionScore:
    """Score and gap audit for a single operational dimension."""
    dimension_name: str                   # e.g., "Process & Execution", "Technology & SAP", "Data & Genealogy"
    current_score: float                  # e.g., 2.1 (out of 5.0)
    target_score: float                   # e.g., 4.2 (out of 5.0)
    priority: str = "P1"                  # "P1", "P2", "P3"
    identified_gap: str = ""              # Core constraint
    priority_intervention: str = ""       # Required action


@dataclass
class MaturityStaircaseLevel:
    """A stage in a 5-level maturity staircase."""
    level_num: int                        # 1..5
    level_name: str                       # e.g., "1. Fragmented", "2. Standardized", "3. Integrated", "4. Intelligent", "5. Autonomous"
    characteristics: List[str]
    is_current_level: bool = False
    is_target_level: bool = False


@dataclass
class MaturityAssessmentModel:
    """Complete semantic model of an enterprise maturity assessment."""
    title: str
    overall_current_score: float          # e.g., 2.6
    overall_target_score: float           # e.g., 4.3
    dimensions: List[MaturityDimensionScore]
    staircase_levels: List[MaturityStaircaseLevel] = field(default_factory=list)
    roadmap_summary: Optional[str] = None
    subtitle: Optional[str] = None


# =============================================================================
# 6. Closed-Loop Manufacturing Model
# =============================================================================

@dataclass
class ClosedLoopStage:
    """A stage in a circular physical-digital-intelligence loop."""
    stage_num: int
    stage_name: str                       # e.g., "1. Physical World", "2. Digital Capture", "3. Contextualization", etc.
    subsystems: List[str]                 # Actors or systems
    data_artifacts: List[str]             # Information produced
    feedback_signal: Optional[str] = None # Control adjustment to physical world


@dataclass
class ClosedLoopManufacturingModel:
    """Complete model of a closed-loop Physical -> Digital -> Intelligence -> Action cycle."""
    title: str
    stages: List[ClosedLoopStage]
    loop_closed_summary: str              # How the loop drives autonomous or continuous optimization
    subtitle: Optional[str] = None


# =============================================================================
# 7. Semantic Transformation Inferrer
# =============================================================================

class TransformationSemanticInferrer:
    """
    Infers transformation relationships and selects the appropriate visual intent.
    Never chooses a visual because it is easy to render; chooses the visual that
    best expresses the underlying relationship, decision, process, or architecture.
    """

    TRANSFORMATION_PATTERNS = {
        TransformationRelationType.CROSS_FUNCTIONAL_SWIMLANE: [
            r"swimlane", r"cross-functional", r"customer.*sap.*mes", r"hand-off", r"handoff",
            r"multi-role", r"actor interaction", r"departmental flow"
        ],
        TransformationRelationType.CLOSED_LOOP_FEEDBACK: [
            r"closed[- ]loop", r"physical.*digital.*intelligence", r"feedback loop",
            r"cyber[- ]physical", r"circular", r"re-inspection", r"root cause.*corrective"
        ],
        TransformationRelationType.MATURITY_PROGRESSION: [
            r"maturity", r"assessment", r"staircase", r"radar", r"heatmap",
            r"current vs target", r"gap analysis", r"score progression", r"level 1.*level 5"
        ],
        TransformationRelationType.TRANSFORMATION_BRIDGE: [
            r"current[- ]state.*future[- ]state", r"before.*after", r"transformation journey",
            r"bridge", r"operating model shift", r"intervention", r"modernization path"
        ],
        TransformationRelationType.MANUFACTURING_EXECUTION: [
            r"sap.*mes", r"production order.*dispatch", r"routing.*operation",
            r"material consumption", r"confirmation.*inventory", r"shop floor execution",
            r"demand.*plan.*execute"
        ],
        TransformationRelationType.GENEALOGY_TRACEABILITY: [
            r"genealogy", r"traceability", r"as-built", r"serial.*batch", r"parent.*child",
            r"lot tracking", r"component consumption"
        ],
        TransformationRelationType.GOVERNANCE_GATEWAY: [
            r"governance", r"control gate", r"approval gate", r"audit", r"compliance gate",
            r"stage-gate", r"poka-yoke"
        ],
        TransformationRelationType.RISK_CHAIN: [
            r"risk mitigation", r"signal.*detection.*assessment", r"failure mode", r"fmea",
            r"risk chain"
        ],
        TransformationRelationType.PROCESS_EXECUTION: [
            r"process flow", r"workflow", r"branching", r"decision point", r"sequential flow",
            r"pass.*fail", r"rework path", r"order-to-cash", r"procure-to-pay"
        ]
    }

    @classmethod
    def infer_relationship(cls, text: str, context: Optional[Dict[str, Any]] = None) -> TransformationRelationType:
        """Analyzes text to classify the primary transformation relationship."""
        cleaned = text.lower()

        # Check matched patterns with priority scoring
        best_match = TransformationRelationType.PROCESS_EXECUTION
        highest_score = 0

        for rel_type, patterns in cls.TRANSFORMATION_PATTERNS.items():
            score = 0
            for pat in patterns:
                if re.search(pat, cleaned):
                    score += 2
            if score > highest_score:
                highest_score = score
                best_match = rel_type

        # Context overrides if supplied
        if context and "explicit_type" in context:
            return context["explicit_type"]

        return best_match

    @classmethod
    def infer_visual_intent(cls, rel_type: TransformationRelationType) -> str:
        """
        Maps a transformation relationship type to the primary visual representation
        that must be rendered according to the Step 15 decision tree.
        """
        mapping = {
            TransformationRelationType.CROSS_FUNCTIONAL_SWIMLANE: "SWIMLANE_DIAGRAM",
            TransformationRelationType.PROCESS_EXECUTION: "PROCESS_FLOW_DIAGRAM",
            TransformationRelationType.CLOSED_LOOP_FEEDBACK: "CLOSED_LOOP_DIAGRAM",
            TransformationRelationType.TRANSFORMATION_BRIDGE: "TRANSFORMATION_BRIDGE_DIAGRAM",
            TransformationRelationType.MATURITY_PROGRESSION: "MATURITY_STAIRCASE_SCORECARD",
            TransformationRelationType.MANUFACTURING_EXECUTION: "MANUFACTURING_VALUE_STREAM_FLOW",
            TransformationRelationType.GENEALOGY_TRACEABILITY: "GENEALOGY_TREE_DIAGRAM",
            TransformationRelationType.GOVERNANCE_GATEWAY: "STAGE_GATE_LIFECYCLE_DIAGRAM",
            TransformationRelationType.RISK_CHAIN: "RISK_DECISION_CHAIN_DIAGRAM",
            TransformationRelationType.SYSTEM_DATA_FLOW: "SYSTEM_INTEGRATION_FLOW_DIAGRAM"
        }
        return mapping.get(rel_type, "PROCESS_FLOW_DIAGRAM")
