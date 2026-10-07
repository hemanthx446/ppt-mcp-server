"""
Semantic Visual Intelligence Engine.

Determines HOW information should be visualized before rendering the slide.
Answers the 6 foundational architectural questions:
  1. What is the audience?
  2. What is the business question?
  3. What is the decision being supported?
  4. What relationship exists between the information?
  5. What is the dominant message?
  6. What visual representation best communicates that relationship?

Strictly enforces visual-selection hierarchy:
Optimizes for "clarity of relationships" rather than "symmetry of boxes."
CARD_GRID is strictly reserved for independent peer concepts with no relational coupling.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Dict, Any, Tuple


class AudienceType(Enum):
    """Target persona receiving the presentation."""
    C_SUITE_CXO = auto()           # CEO, CFO, COO, Managing Director (Focus: Cash, EBITDA, Risk, Growth)
    ENTERPRISE_ARCHITECT = auto()  # Lead Architects, Security, Core IT (Focus: Clean core, Latency, WLM, APIs)
    PLANT_OPERATIONS = auto()      # Plant Directors, Quality Heads, Supervisors (Focus: OEE, Scrap, Poka-Yoke)
    SUPPLY_CHAIN_SOURCING = auto() # CPO, VP SCM, Commodity Buyers (Focus: Lead times, 52-wk pipeline, Stockouts)
    FINANCE_CONTROLLERS = auto()   # Cost Accounting, Treasury (Focus: ACDOCA, WIP aging, Cash covenants)
    PROJECT_STEERING = auto()      # Joint ARB, Steering Committee (Focus: Milestones, Gate criteria, SLAs)


class InformationRelationship(Enum):
    """The fundamental mathematical, spatial, or operational relationship within the data."""
    COMPONENT_STRUCTURE = auto()        # Systems, boundaries, containers, layers
    EXCHANGE_FLOW = auto()              # Data streaming, message broker, event exchange, APIs
    SEQUENTIAL_PROCESS = auto()         # Ordered business process flow
    OPERATIONAL_JOURNEY = auto()        # Step-by-step operator/workstation interaction with Poka-Yoke
    HIERARCHICAL_DECOMPOSITION = auto() # Tree structure, multi-level indented BOM, taxonomy
    GENEALOGICAL_LINEAGE = auto()       # Parent-child genealogy, trace-and-track, lot ancestry
    CONTRAST_TENSION = auto()           # As-Is vs. To-Be, Legacy Friction vs. Target Architecture
    TRANSFORMATION_STAGES = auto()      # Evolutionary maturity stages over time
    TEMPORAL_MILESTONES = auto()        # Project delivery timeline, duration, dates
    RESPONSIBILITY_ALLOCATION = auto()  # Ownership, cross-functional roles, RACI, swimlanes
    GOVERNANCE_CONTROL = auto()         # Review gates, approval desks, verification interlocks
    QUANTITATIVE_PERFORMANCE = auto()   # High-impact operational metrics, KPI cockpit
    QUANTITATIVE_COMPARISON = auto()    # Quantitative trends, ratios, distributions
    STRUCTURED_ATTRIBUTES = auto()      # Multi-dimensional evaluation matrix (e.g. 5 W's)
    FINANCIAL_COMMERCIAL = auto()       # Commercial pricing, unit economics, payback schedule
    DECISION_EVALUATION = auto()        # Criteria scoring, alternative trade-off analysis
    RISK_PROBABILITY_IMPACT = auto()    # Risk severity, probability, mitigation radar
    MATURITY_HORIZON = auto()           # Levels 1-5 evolutionary capability progression
    CAPABILITY_TAXONOMY = auto()        # Enterprise functional capability map
    CAUSE_AND_EFFECT = auto()           # Operational levers directly driving balance sheet outcomes
    NARRATIVE_EXPLANATION = auto()      # Strategic thesis, problem context, qualitative rationale
    INDEPENDENT_PEER_CONCEPTS = auto()  # Genuine independent parallel pillars (CARD_GRID allowed)


class VisualRepresentation(Enum):
    """The concrete visual archetype chosen to communicate the information relationship."""
    ARCHITECTURE_DIAGRAM = auto()       # 3-tier system stack, runtime boundaries, protocol arrows
    INTEGRATION_FLOW = auto()           # Directional data exchange pipeline (e.g. OData GET -> Queue -> HHT)
    PROCESS_FLOW = auto()               # End-to-end business process sequence
    JOURNEY_WORKFLOW = auto()           # Station-by-station operator journey with Poka-Yoke interlocks
    HIERARCHY_TREE = auto()             # Indented component / BOM hierarchy
    GENEALOGY_GRAPH = auto()            # Bi-directional component-to-finished-good trace tree
    AS_IS_TO_BE = auto()                # High-contrast 2-column tension (Red Friction vs. Green Target)
    TRANSFORMATION_ROADMAP = auto()     # Phased agile rollout with durations and gate criteria
    TIMELINE = auto()                   # Chronological schedule milestone track
    SWIMLANE = auto()                   # Horizontal actor lanes (Operator / Supervisor / ERP)
    CONTROL_GATES = auto()              # Multi-tier verification approval desk (Supervisor PIN + QC Stamp)
    EXECUTIVE_DASHBOARD = auto()        # Multi-metric operational cockpit & report catalog
    CHART = auto()                      # Quantitative data chart (bar, line, waterfall)
    TABLE_MATRIX = auto()               # 5 W's evaluation matrix with ERP table lineage
    COMMERCIAL_TABLE = auto()           # Milestone invoicing, unit cost, and payment triggers
    DECISION_MATRIX = auto()            # Multi-criteria scoring evaluation table
    RISK_MATRIX = auto()                # Risk probability vs. impact heat map / radar
    MATURITY_MODEL = auto()             # 5-level capability progression staircase
    CAPABILITY_MAP = auto()             # Categorized enterprise functional domain grid
    OUTCOME_CHAIN = auto()              # Operational metric levers connected to cash/EBITDA impact
    TYPOGRAPHIC_NARRATIVE = auto()      # Large hero statement with qualitative supporting proof
    CARD_GRID = auto()                  # Restricted multi-column layout for genuine peer concepts


@dataclass
class SlideContext:
    """The business context and decision environment for a slide."""
    audience: AudienceType
    business_question: str             # e.g., "How do we eliminate paper travelers without SAP licensing cost?"
    decision_supported: str            # e.g., "Authorize non-invasive shop-floor middleware architecture"
    dominant_message: str              # e.g., "Air-gapped edge layer guarantees zero live ERP write risk"
    information_relationship: InformationRelationship
    visual_representation: VisualRepresentation
    confidence_score: float = 1.0


@dataclass
class CompositeSlot:
    """A designated region on the slide assigned a specific visual primitive."""
    role: str                          # e.g., "MAIN_STAGE", "TOP_KPI_STRIP", "BOTTOM_GUARANTEE_BANNER"
    primitive_type: str                # e.g., "ARCHITECTURE_STACK", "DATA_TABLE", "METRIC_STRIP"
    width_ratio: float = 1.0           # Horizontal proportion of usable canvas
    height_ratio: float = 1.0          # Vertical proportion of usable canvas
    data: Any = None


@dataclass
class CompositeSlideSpec:
    """
    Complete composite layout specification for a slide.
    Enables asymmetrical, multi-primitive compositions (e.g. Title + Architecture + Guarantee Banner).
    """
    context: SlideContext
    title: str
    category_tag: str
    narrative_subtitle: str
    primary_representation: VisualRepresentation
    slots: List[CompositeSlot] = field(default_factory=list)
    is_dark: bool = False
    footer_metadata: str = "Confidential Advisory Proposal"


class VisualIntelligenceEngine:
    """
    Semantic Visual Intelligence & Intent Classifier.
    Analyzes content semantics, titles, and intent to select the optimal visual form.
    """

    # Keyword mappings for information relationship detection
    RELATIONSHIP_PATTERNS = [
        # Architecture & Integration
        (InformationRelationship.COMPONENT_STRUCTURE, [
            "architecture", "topology", "tiers", "layers", "stack", "decoupled", "core", "middleware", "edge", "database internals"
        ]),
        (InformationRelationship.EXCHANGE_FLOW, [
            "integration", "pipeline", "odata", "api", "broker", "event mesh", "mqtt", "rest", "telemetry", "streaming", "delta sync"
        ]),
        # Process & Journey
        (InformationRelationship.OPERATIONAL_JOURNEY, [
            "operator", "poka-yoke", "workstation", "traveler", "barcode", "hht", "scanner", "kitting", "assembly", "receiving dock"
        ]),
        (InformationRelationship.SEQUENTIAL_PROCESS, [
            "process", "workflow", "steps", "procedure", "stage", "routing", "order of operations"
        ]),
        (InformationRelationship.GENEALOGICAL_LINEAGE, [
            "genealogy", "traceability", "parent-child", "as-built", "bom traversal", "serial", "lot tracking", "audit trail"
        ]),
        # Contrast & State
        (InformationRelationship.CONTRAST_TENSION, [
            "current state", "target state", "as-is", "to-be", "disconnect", "friction", "bottleneck", "legacy", "before vs after"
        ]),
        # Roadmap & Timeline
        (InformationRelationship.TRANSFORMATION_STAGES, [
            "roadmap", "phases", "milestones", "rollout", "hypercare", "sprint", "deployment plan", "90-day", "12-week"
        ]),
        (InformationRelationship.TEMPORAL_MILESTONES, [
            "timeline", "schedule", "calendar", "duration", "weeks", "months", "days"
        ]),
        # Governance & Approval
        (InformationRelationship.GOVERNANCE_CONTROL, [
            "governance", "approval", "gate", "qc", "sign-off", "supervisor", "co11n", "inspection", "sla", "covenants"
        ]),
        # Metrics & Value
        (InformationRelationship.CAUSE_AND_EFFECT, [
            "ebitda", "cash flow", "free cash", "roi", "working capital", "payback", "irr", "cost avoidance", "margin impact", "p&l"
        ]),
        (InformationRelationship.QUANTITATIVE_PERFORMANCE, [
            "cockpit", "dashboard", "kpi", "metrics", "otif", "oee", "utilization", "scrap rate", "lead time"
        ]),
        # Structured Matrices
        (InformationRelationship.STRUCTURED_ATTRIBUTES, [
            "matrix", "5 w's", "persona", "inventory", "catalog", "specification", "table", "cross-functional"
        ]),
        (InformationRelationship.FINANCIAL_COMMERCIAL, [
            "commercial", "pricing", "investment", "fixed-price", "terms", "invoicing", "warranty", "lakhs", "contract"
        ]),
        (InformationRelationship.DECISION_EVALUATION, [
            "evaluation", "decision", "trade-off", "alternatives", "options", "comparison matrix", "selection"
        ]),
        (InformationRelationship.RISK_PROBABILITY_IMPACT, [
            "risk", "mitigation", "severity", "vulnerability", "exposure", "contingency"
        ]),
    ]

    # Deterministic mapping from Relationship to Visual Representation
    VISUAL_MAPPING = {
        InformationRelationship.COMPONENT_STRUCTURE: VisualRepresentation.ARCHITECTURE_DIAGRAM,
        InformationRelationship.EXCHANGE_FLOW: VisualRepresentation.INTEGRATION_FLOW,
        InformationRelationship.OPERATIONAL_JOURNEY: VisualRepresentation.JOURNEY_WORKFLOW,
        InformationRelationship.SEQUENTIAL_PROCESS: VisualRepresentation.PROCESS_FLOW,
        InformationRelationship.HIERARCHICAL_DECOMPOSITION: VisualRepresentation.HIERARCHY_TREE,
        InformationRelationship.GENEALOGICAL_LINEAGE: VisualRepresentation.GENEALOGY_GRAPH,
        InformationRelationship.CONTRAST_TENSION: VisualRepresentation.AS_IS_TO_BE,
        InformationRelationship.TRANSFORMATION_STAGES: VisualRepresentation.TRANSFORMATION_ROADMAP,
        InformationRelationship.TEMPORAL_MILESTONES: VisualRepresentation.TIMELINE,
        InformationRelationship.RESPONSIBILITY_ALLOCATION: VisualRepresentation.SWIMLANE,
        InformationRelationship.GOVERNANCE_CONTROL: VisualRepresentation.CONTROL_GATES,
        InformationRelationship.QUANTITATIVE_PERFORMANCE: VisualRepresentation.EXECUTIVE_DASHBOARD,
        InformationRelationship.QUANTITATIVE_COMPARISON: VisualRepresentation.CHART,
        InformationRelationship.STRUCTURED_ATTRIBUTES: VisualRepresentation.TABLE_MATRIX,
        InformationRelationship.FINANCIAL_COMMERCIAL: VisualRepresentation.COMMERCIAL_TABLE,
        InformationRelationship.DECISION_EVALUATION: VisualRepresentation.DECISION_MATRIX,
        InformationRelationship.RISK_PROBABILITY_IMPACT: VisualRepresentation.RISK_MATRIX,
        InformationRelationship.MATURITY_HORIZON: VisualRepresentation.MATURITY_MODEL,
        InformationRelationship.CAPABILITY_TAXONOMY: VisualRepresentation.CAPABILITY_MAP,
        InformationRelationship.CAUSE_AND_EFFECT: VisualRepresentation.OUTCOME_CHAIN,
        InformationRelationship.NARRATIVE_EXPLANATION: VisualRepresentation.TYPOGRAPHIC_NARRATIVE,
        InformationRelationship.INDEPENDENT_PEER_CONCEPTS: VisualRepresentation.CARD_GRID,
    }

    @classmethod
    def classify_intent(
        cls,
        title: str,
        category: str = "",
        narrative_subtitle: str = "",
        content_items: Optional[List[Any]] = None,
        explicit_audience: Optional[AudienceType] = None
    ) -> SlideContext:
        """
        Answers the 6 architectural questions and selects the visual representation.
        Guarantees that CARD_GRID is only selected if no stronger relationship exists.
        """
        body_text = ""
        if content_items:
            for item in content_items:
                if isinstance(item, str):
                    body_text += f" {item.lower()}"
                elif hasattr(item, "__dict__"):
                    body_text += f" {str(item.__dict__).lower()}"

        combined_text = f"{title} {category} {narrative_subtitle} {body_text}".lower()

        # 1. Determine Audience
        audience = explicit_audience or cls._infer_audience(combined_text)

        # 2. Detect Information Relationship with priority weighting
        detected_rel, confidence = cls._detect_relationship(
            title=title,
            category=category,
            subtitle=narrative_subtitle,
            body=body_text
        )

        # 3. Map to Visual Representation
        visual_rep = cls.VISUAL_MAPPING.get(detected_rel, VisualRepresentation.CARD_GRID)

        # 4. Formulate Business Question & Supported Decision
        b_question = cls._infer_business_question(detected_rel, title)
        decision = cls._infer_decision_supported(detected_rel, title)
        dominant_msg = narrative_subtitle if narrative_subtitle else f"Strategic alignment on {title}"

        return SlideContext(
            audience=audience,
            business_question=b_question,
            decision_supported=decision,
            dominant_message=dominant_msg,
            information_relationship=detected_rel,
            visual_representation=visual_rep,
            confidence_score=confidence
        )

    @classmethod
    def compose_slide_spec(
        cls,
        title: str,
        category_tag: str,
        narrative_subtitle: str,
        content_elements: List[Any],
        callout_banner: Optional[str] = None,
        is_dark: Optional[bool] = None,
        footer_metadata: str = "Confidential Advisory Proposal"
    ) -> CompositeSlideSpec:
        """
        Composes a multi-primitive slide specification optimizing for clarity of relationships.
        Never forces content into equal-sized symmetrical boxes when relationships dictate otherwise.
        """
        context = cls.classify_intent(title, category_tag, narrative_subtitle, content_elements)
        
        # Decide dark theme: Architecture and Title slides default to Executive Dark
        dark_flag = is_dark
        if dark_flag is None:
            dark_flag = context.visual_representation in (
                VisualRepresentation.ARCHITECTURE_DIAGRAM,
                VisualRepresentation.INTEGRATION_FLOW
            ) or "title" in title.lower() or "opening" in category_tag.lower()

        slots: List[CompositeSlot] = []

        # Multi-primitive slot assignment
        rep = context.visual_representation

        if rep in (VisualRepresentation.ARCHITECTURE_DIAGRAM, VisualRepresentation.INTEGRATION_FLOW):
            # Slot 1: Main Stage Architecture Pipeline (80% height)
            slots.append(CompositeSlot(
                role="MAIN_STAGE",
                primitive_type="ARCHITECTURE_STACK",
                width_ratio=1.0,
                height_ratio=0.75 if callout_banner else 1.0,
                data=content_elements
            ))
            # Slot 2: Enclosed Security / Architectural Guarantee Banner (20% height)
            if callout_banner:
                slots.append(CompositeSlot(
                    role="BOTTOM_CALLOUT",
                    primitive_type="GUARANTEE_BANNER",
                    width_ratio=1.0,
                    height_ratio=0.25,
                    data=callout_banner
                ))

        elif rep in (VisualRepresentation.TABLE_MATRIX, VisualRepresentation.COMMERCIAL_TABLE, VisualRepresentation.DECISION_MATRIX):
            # Slot 1: Large Enterprise Table (takes full stage)
            slots.append(CompositeSlot(
                role="MAIN_STAGE",
                primitive_type="DATA_TABLE",
                width_ratio=1.0,
                height_ratio=0.85 if callout_banner else 1.0,
                data=content_elements
            ))
            if callout_banner:
                slots.append(CompositeSlot(
                    role="BOTTOM_CALLOUT",
                    primitive_type="CONCLUSION_BANNER",
                    width_ratio=1.0,
                    height_ratio=0.15,
                    data=callout_banner
                ))

        elif rep == VisualRepresentation.OUTCOME_CHAIN or rep == VisualRepresentation.EXECUTIVE_DASHBOARD:
            # Slot 1: Top KPI Metric Strip
            # Slot 2: Operational Proof Points & Action Levers
            slots.append(CompositeSlot(
                role="TOP_METRIC_STRIP",
                primitive_type="HERO_METRIC_ROW",
                width_ratio=1.0,
                height_ratio=0.30,
                data=[e for e in content_elements if hasattr(e, "value")]
            ))
            slots.append(CompositeSlot(
                role="MAIN_STAGE",
                primitive_type="OPERATIONAL_PROOF_GRID",
                width_ratio=1.0,
                height_ratio=0.70,
                data=[e for e in content_elements if not hasattr(e, "value")]
            ))

        elif rep == VisualRepresentation.JOURNEY_WORKFLOW:
            # Slot 1: Station-by-station operational flow with Poka-Yoke interlocks
            slots.append(CompositeSlot(
                role="MAIN_STAGE",
                primitive_type="JOURNEY_STATIONS",
                width_ratio=1.0,
                height_ratio=0.78 if callout_banner else 1.0,
                data=content_elements
            ))
            if callout_banner:
                slots.append(CompositeSlot(
                    role="BOTTOM_CALLOUT",
                    primitive_type="POKA_YOKE_INTERLOCK_BANNER",
                    width_ratio=1.0,
                    height_ratio=0.22,
                    data=callout_banner
                ))

        elif rep == VisualRepresentation.AS_IS_TO_BE:
            # Slot: High-contrast 2-column tension
            slots.append(CompositeSlot(
                role="MAIN_STAGE",
                primitive_type="CONTRAST_SPLIT",
                width_ratio=1.0,
                height_ratio=1.0,
                data=content_elements
            ))

        elif rep == VisualRepresentation.TRANSFORMATION_ROADMAP:
            # Slot: Phased milestone blocks with duration spans and gate criteria
            slots.append(CompositeSlot(
                role="MAIN_STAGE",
                primitive_type="PHASED_TIMELINE_GRID",
                width_ratio=1.0,
                height_ratio=0.78 if callout_banner else 1.0,
                data=content_elements
            ))
            if callout_banner:
                slots.append(CompositeSlot(
                    role="BOTTOM_CALLOUT",
                    primitive_type="GOVERNANCE_GATE_BANNER",
                    width_ratio=1.0,
                    height_ratio=0.22,
                    data=callout_banner
                ))

        else:
            # Fallback for genuine peer concepts
            slots.append(CompositeSlot(
                role="MAIN_STAGE",
                primitive_type="STRUCTURED_CONTENT_GRID",
                width_ratio=1.0,
                height_ratio=1.0,
                data=content_elements
            ))

        return CompositeSlideSpec(
            context=context,
            title=title,
            category_tag=category_tag,
            narrative_subtitle=narrative_subtitle,
            primary_representation=rep,
            slots=slots,
            is_dark=dark_flag,
            footer_metadata=footer_metadata
        )

    # -------------------------------------------------------------
    # Internal Heuristic Classifiers
    # -------------------------------------------------------------

    @classmethod
    def _detect_relationship(
        cls,
        title: str,
        category: str = "",
        subtitle: str = "",
        body: str = ""
    ) -> Tuple[InformationRelationship, float]:
        """Scans title, category, subtitle, and body with hierarchical priority weighting."""
        best_rel = InformationRelationship.INDEPENDENT_PEER_CONCEPTS
        best_score = 0.0

        title_lower = title.lower()
        cat_lower = category.lower()
        sub_lower = subtitle.lower()
        body_lower = body.lower()

        for rel, keywords in cls.RELATIONSHIP_PATTERNS:
            score = 0.0
            for kw in keywords:
                weight = 2.5 if " " in kw else 1.0
                if kw in title_lower:
                    score += weight * 3.0   # Highest priority: title
                elif kw in cat_lower:
                    score += weight * 2.0   # High priority: category badge
                elif kw in sub_lower:
                    score += weight * 1.0   # Medium priority: subtitle
                elif kw in body_lower:
                    score += weight * 0.6   # Supporting: body content

            if score > best_score:
                best_score = score
                best_rel = rel

        # Domain Manufacturing Semantic Pattern Boost
        from .manufacturing_vocabulary import ManufacturingSemanticAnalyzer, SemanticPatternType
        domain_patterns = ManufacturingSemanticAnalyzer.detect_relational_patterns(f"{title} {category} {subtitle} {body}")
        if domain_patterns:
            top_pat = domain_patterns[0]
            pattern_rel_map = {
                SemanticPatternType.INTEGRATION_FLOW: InformationRelationship.EXCHANGE_FLOW,
                SemanticPatternType.MANUFACTURING_FLOW: InformationRelationship.SEQUENTIAL_PROCESS,
                SemanticPatternType.GENEALOGY_TRACEABILITY: InformationRelationship.GENEALOGICAL_LINEAGE,
                SemanticPatternType.OPERATIONAL_HIERARCHY: InformationRelationship.HIERARCHICAL_DECOMPOSITION,
                SemanticPatternType.DECISION_LOOP: InformationRelationship.DECISION_EVALUATION,
                SemanticPatternType.QUALITY_EXCEPTION: InformationRelationship.OPERATIONAL_JOURNEY,
            }
            mapped_rel = pattern_rel_map.get(top_pat.pattern_type)
            if mapped_rel:
                pat_score = top_pat.confidence * 4.5
                if pat_score > best_score or best_rel == InformationRelationship.INDEPENDENT_PEER_CONCEPTS:
                    best_score = pat_score
                    best_rel = mapped_rel

        confidence = min(1.0, best_score / 4.0) if best_score > 0 else 0.4
        return best_rel, confidence

    @classmethod
    def _infer_audience(cls, text: str) -> AudienceType:
        if any(k in text for k in ["cfo", "cash", "ebitda", "payback", "irr", "executive", "ceo", "board"]):
            return AudienceType.C_SUITE_CXO
        if any(k in text for k in ["architecture", "database", "odata", "api", "wlm", "push-down", "clean core", "hana"]):
            return AudienceType.ENTERPRISE_ARCHITECT
        if any(k in text for k in ["operator", "poka-yoke", "shop-floor", "hht", "scanner", "plant", "scrap", "co11n"]):
            return AudienceType.PLANT_OPERATIONS
        if any(k in text for k in ["buyer", "procurement", "cpo", "sourcing", "vendor", "52-week", "supplier"]):
            return AudienceType.SUPPLY_CHAIN_SOURCING
        if any(k in text for k in ["roadmap", "phase", "milestone", "hypercare", "timeline", "steering"]):
            return AudienceType.PROJECT_STEERING
        return AudienceType.C_SUITE_CXO

    @classmethod
    def _infer_business_question(cls, rel: InformationRelationship, title: str) -> str:
        questions = {
            InformationRelationship.COMPONENT_STRUCTURE: f"How are system boundaries and transactional safety decoupled in {title}?",
            InformationRelationship.EXCHANGE_FLOW: f"How does data flow in real time between tiers without point-to-point lockups?",
            InformationRelationship.OPERATIONAL_JOURNEY: f"How do shop-floor operators execute operations with zero assembly error?",
            InformationRelationship.CONTRAST_TENSION: f"What operational and financial friction separates our legacy state from target capability?",
            InformationRelationship.TRANSFORMATION_STAGES: f"What is the de-risked milestone sequence to deploy production capability?",
            InformationRelationship.GOVERNANCE_CONTROL: f"What verification gates prevent unverified data from polluting the financial ledger?",
            InformationRelationship.CAUSE_AND_EFFECT: f"What quantified EBITDA and working capital return does this transformation deliver?",
            InformationRelationship.STRUCTURED_ATTRIBUTES: f"How do personas, cadences, and ERP tables map to operational value in {title}?",
            InformationRelationship.FINANCIAL_COMMERCIAL: f"What is the fixed-price milestone investment and commercial warranty framework?",
        }
        return questions.get(rel, f"What strategic and operational capabilities are established by {title}?")

    @classmethod
    def _infer_decision_supported(cls, rel: InformationRelationship, title: str) -> str:
        decisions = {
            InformationRelationship.COMPONENT_STRUCTURE: "Approve decoupled target system architecture and clean-core integration strategy.",
            InformationRelationship.EXCHANGE_FLOW: "Authorize real-time OData / Event Mesh integration protocols.",
            InformationRelationship.OPERATIONAL_JOURNEY: "Mandate hardware-enforced barcode Poka-Yoke and digital traveler adoption.",
            InformationRelationship.CONTRAST_TENSION: "Prioritize elimination of high-friction legacy batch manual processes.",
            InformationRelationship.TRANSFORMATION_STAGES: "Commit to phased implementation roadmap and gate criteria sign-offs.",
            InformationRelationship.GOVERNANCE_CONTROL: "Establish two-tier approval desk and air-gapped posting governance.",
            InformationRelationship.CAUSE_AND_EFFECT: "Authorize capital budget based on validated 14-month payback model.",
            InformationRelationship.STRUCTURED_ATTRIBUTES: "Align departmental personas with core reporting cadences and ERP lineage.",
            InformationRelationship.FINANCIAL_COMMERCIAL: "Approve milestone-linked commercial proposal and engagement terms.",
        }
        return decisions.get(rel, f"Adopt strategic transformation proposal for {title}.")
