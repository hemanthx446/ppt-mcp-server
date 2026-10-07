"""
Narrative Intelligence Engine: Multi-Slide Storytelling & Cognitive Intent.

Implements macro-level narrative frameworks:
1. TELL -> SHOW -> TELL
   - OPENING TELL: Why does this matter? (Low density executive mandate / strategic thesis)
   - SHOW: What is actually happening? (Architecture blueprint, process flow, operational cockpit)
   - CLOSING TELL: What does this mean for the customer? (Decision request, quantified ROI, commitment)

2. PRIDE & PURPOSE -> DESTINATION (6 Stages)
   - Pride & Purpose -> Current Reality -> Opportunity -> Journey -> Changes -> Destination

3. SOLUTION SELLING (4 Stages)
   - WHY -> WHAT -> HOW -> BUSINESS VALUE

4. EXECUTIVE DEMONSTRATION (6 Stages)
   - Opening -> Business Outcomes -> Challenges -> Opportunities -> Demonstration -> Close

Every slide has an internal reason for existing:
"What does the audience need to understand, believe, decide or do after seeing this slide?"

Internal reasoning governs visual selection and density without being exposed in presentation content.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Any, Optional, Tuple

from pptx import Presentation
from pptx.util import Inches

from .typography import TypographySystem
from .color import Theme, ExecutiveNavyTheme, ConsultingSlateTheme
from .spacing import CanvasBounds, Margins
from .density_intelligence import (
    VisualDensity,
    VisualDensityClassifier,
    LowDensitySlideRenderer,
    WhitespaceIntelligenceEngine
)
from .architecture_engine import (
    ArchitectureBlueprintFactory,
    EnterpriseArchitectureComposer
)
from .dashboard import (
    ExecutiveDashboardComposer,
    DashboardQuestionClassifier
)
from .table_engine import (
    EnterpriseTableFactory,
    EnterpriseTableComposer,
    TableArchetype
)
import design_system.library as lib


# =============================================================================
# 1. Macro Narrative Frameworks
# =============================================================================

class NarrativeFramework(Enum):
    TELL_SHOW_TELL = auto()               # 3 slides: Why it matters -> What happens -> What to decide
    PRIDE_PURPOSE_DESTINATION = auto()    # 6 slides: Purpose -> Reality -> Opportunity -> Journey -> Changes -> Destination
    WHY_WHAT_HOW_VALUE = auto()           # 4 slides: Why -> What -> How -> Business Value
    EXECUTIVE_DEMONSTRATION = auto()      # 6 slides: Opening -> Outcomes -> Challenges -> Opportunities -> Demo -> Close


@dataclass
class AudienceCognitiveObjective:
    """Internal reasoning determining why the slide exists (never exposed on slide)."""
    understand: str                       # Technical or operational truth audience must grasp
    believe: str                          # Core belief or confidence shift required
    decide: str                           # Decision or tradeoff audience must validate
    do: str                               # Direct operational or governance action to trigger


@dataclass
class NarrativeSlideIntent:
    """Design and content intent for a single slide within a narrative arc."""
    stage_id: str                         # e.g., "OPENING_TELL", "SHOW", "CLOSING_TELL"
    slide_title: str                      # Audience-facing action title
    slide_subtitle: str                   # Audience-facing takeaway
    category_tag: str                     # Banner tag
    cognitive_objective: AudienceCognitiveObjective
    recommended_density: VisualDensity
    recommended_primitive: str            # e.g., 'executive_statement', 'architecture_diagram', 'table'
    is_dark: bool
    data_payload: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# 2. Narrative Arc Generator
# =============================================================================

class NarrativeIntelligenceEngine:
    """Synthesizes narrative arcs and renders presentations mapped to cognitive intent."""

    @classmethod
    def plan_narrative_deck(
        cls,
        framework: NarrativeFramework,
        topic: str,
        client_name: str = "Executive Leadership",
        custom_data: Optional[Dict[str, Any]] = None
    ) -> List[NarrativeSlideIntent]:
        """Plans the sequence of slides with internal cognitive reasoning and visual choices."""
        cdata = custom_data or {}

        # ---------------------------------------------------------------------
        # FRAMEWORK 1: TELL -> SHOW -> TELL
        # ---------------------------------------------------------------------
        if framework == NarrativeFramework.TELL_SHOW_TELL:
            return [
                NarrativeSlideIntent(
                    stage_id="OPENING_TELL",
                    slide_title=cdata.get("tell_1_title", f"The Strategic Mandate for {topic}"),
                    slide_subtitle=cdata.get("tell_1_subtitle", "Legacy data replication creates financial reconciliation risk; execution must move to the edge."),
                    category_tag="1. OPENING TELL • WHY THIS MATTERS",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="Why the current legacy architecture is structurally unsustainable.",
                        believe="That decoupling execution from the financial core is the only viable path.",
                        decide="Acknowledge the strategic imperative to transform.",
                        do="Commit attention to the underlying system mechanics."
                    ),
                    recommended_density=VisualDensity.LOW_DENSITY,
                    recommended_primitive="executive_statement",
                    is_dark=True,
                    data_payload={
                        "statement": cdata.get("statement", f"The maths must happen where the data already lives."),
                        "thesis": cdata.get("thesis", f"Preserving ERP financial ledger integrity requires air-gapped manufacturing execution."),
                        "source": "Enterprise Solutions Architecture"
                    }
                ),
                NarrativeSlideIntent(
                    stage_id="SHOW",
                    slide_title=cdata.get("show_title", f"Clean-Core Architecture & Event Topology"),
                    slide_subtitle=cdata.get("show_subtitle", "Sub-second event dispatch from S/4HANA to edge PLCs with zero ACDOCA replication."),
                    category_tag="2. SHOW • WHAT IS ACTUALLY HAPPENING",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="The exact technical flow of orders, telemetry, and ledger postings.",
                        believe="The solution is technically de-risked and protects against network outages.",
                        decide="Validate the clean-core integration boundary.",
                        do="Authorize engineering deployment to pilot lines."
                    ),
                    recommended_density=VisualDensity.MEDIUM_DENSITY,
                    recommended_primitive="architecture_diagram",
                    is_dark=True,
                    data_payload={
                        "template_id": "CLEAN_CORE_SAP_TO_SHOPFLOOR"
                    }
                ),
                NarrativeSlideIntent(
                    stage_id="CLOSING_TELL",
                    slide_title=cdata.get("tell_2_title", f"Customer Impact & Immediate Action Plan"),
                    slide_subtitle=cdata.get("tell_2_subtitle", "Turnkey milestone governance delivering 3.3-month payback and audited ledger tie-out."),
                    category_tag="3. CLOSING TELL • WHAT THIS MEANS FOR YOU",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="The financial return, milestone timeline, and commercial warranty.",
                        believe="That the investment carries bounded risk and delivers immediate EBITDA impact.",
                        decide="Approve the fixed-price milestone engagement terms.",
                        do="Sign off on Gate 1 mobilization and schedule the kick-off review."
                    ),
                    recommended_density=VisualDensity.HIGH_DENSITY,
                    recommended_primitive="table",
                    is_dark=False,
                    data_payload={
                        "table_archetype": TableArchetype.COMMERCIAL_PROPOSAL
                    }
                )
            ]

        # ---------------------------------------------------------------------
        # FRAMEWORK 2: PRIDE & PURPOSE -> DESTINATION
        # ---------------------------------------------------------------------
        elif framework == NarrativeFramework.PRIDE_PURPOSE_DESTINATION:
            return [
                NarrativeSlideIntent(
                    stage_id="PRIDE_PURPOSE",
                    slide_title="Our Identity & Manufacturing Heritage",
                    slide_subtitle="Delivering mission-critical precision engineering across global aerospace and defense programs.",
                    category_tag="1. PRIDE & PURPOSE",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="The foundational strengths and operational heritage of the organization.",
                        believe="That transformation builds upon our core competitive strengths rather than discarding them.",
                        decide="Reaffirm organizational pride and engineering excellence.",
                        do="Align leadership around a unified modernization ambition."
                    ),
                    recommended_density=VisualDensity.LOW_DENSITY,
                    recommended_primitive="executive_statement",
                    is_dark=True,
                    data_payload={"statement": "Engineering excellence is built on uncompromising precision.", "thesis": "Modernizing our digital infrastructure safeguards fifty years of trusted manufacturing heritage."}
                ),
                NarrativeSlideIntent(
                    stage_id="CURRENT_REALITY",
                    slide_title="Current Operating Baseline & Structural Constraints",
                    slide_subtitle="Manual traveler reconciliation and shop floor batch synch starves downstream packaging cells.",
                    category_tag="2. CURRENT REALITY",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="Where working capital is trapped and where scrap originates.",
                        believe="That localized heroics cannot overcome architectural bottlenecks.",
                        decide="Acknowledge the need for systemic process redesign.",
                        do="Target root constraints rather than symptoms."
                    ),
                    recommended_density=VisualDensity.HIGH_DENSITY,
                    recommended_primitive="dashboard",
                    is_dark=False,
                    data_payload={"question": "Where is production constrained?"}
                ),
                NarrativeSlideIntent(
                    stage_id="OPPORTUNITY",
                    slide_title="The Strategic Leap: Autonomous Shop Floor Intelligence",
                    slide_subtitle="Transitioning from paper-driven batch tracking to real-time closed-loop execution.",
                    category_tag="3. OPPORTUNITY",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="The operational and financial prize of full IT/OT convergence.",
                        believe="That 14% OEE acceleration and 60% scrap reduction are realistically attainable.",
                        decide="Endorse the target transformation goals.",
                        do="Mobilize cross-functional sponsorship across IT and Operations."
                    ),
                    recommended_density=VisualDensity.LOW_DENSITY,
                    recommended_primitive="hero_kpi",
                    is_dark=True,
                    data_payload={"metric_value": "$3.11M", "metric_label": "Annualized EBITDA Acceleration", "conclusion": "Eliminating paper travelers and manual quality audits unlocks 3.3-month capital payback."}
                ),
                NarrativeSlideIntent(
                    stage_id="JOURNEY",
                    slide_title="Phased Implementation Roadmap & Milestone Gating",
                    slide_subtitle="Four deliverable-linked milestone gates ensuring zero disruption to live customer shipments.",
                    category_tag="4. JOURNEY",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="The sequence of sprints and validation gates across the 16-week timeline.",
                        believe="That the rollout is de-risked and will not halt active plant lines.",
                        decide="Approve the phased deployment gate sequence.",
                        do="Schedule joint ARB governance checkpoints."
                    ),
                    recommended_density=VisualDensity.HIGH_DENSITY,
                    recommended_primitive="table",
                    is_dark=False,
                    data_payload={"table_archetype": TableArchetype.ROADMAP}
                ),
                NarrativeSlideIntent(
                    stage_id="CHANGES",
                    slide_title="System Architecture & Integration Topology",
                    slide_subtitle="Clean-core S/4HANA decoupling with air-gapped industrial edge resilience.",
                    category_tag="5. CHANGES",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="What changes under the hood in systems, networks, and operator PODs.",
                        believe="That SAP core stability and cybersecurity perimeters are preserved.",
                        decide="Validate the clean-core boundary architecture.",
                        do="Authorize edge hardware gateway installation."
                    ),
                    recommended_density=VisualDensity.MEDIUM_DENSITY,
                    recommended_primitive="architecture_diagram",
                    is_dark=True,
                    data_payload={"template_id": "CLEAN_CORE_SAP_TO_SHOPFLOOR"}
                ),
                NarrativeSlideIntent(
                    stage_id="DESTINATION",
                    slide_title="The Target Operating Model & Sustainable Advantage",
                    slide_subtitle="Fully auditable closed-loop manufacturing execution integrated with financial ledgers.",
                    category_tag="6. DESTINATION",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="The final operating reality and lasting capabilities established.",
                        believe="That our manufacturing posture is now best-in-class across the industry.",
                        decide="Sign off on transformation governance and operational charter.",
                        do="Commence Day 1 execution."
                    ),
                    recommended_density=VisualDensity.LOW_DENSITY,
                    recommended_primitive="architectural_principle",
                    is_dark=True,
                    data_payload={"headline": "Autonomous Operational Control", "core_rule": "Every physical movement on the plant floor is reflected in the enterprise ledger in real time.", "rationale": "Complete digital genealogy and sub-second execution deliver unbreakable customer trust."}
                )
            ]

        # ---------------------------------------------------------------------
        # FRAMEWORK 3: SOLUTION SELLING (WHY -> WHAT -> HOW -> VALUE)
        # ---------------------------------------------------------------------
        elif framework == NarrativeFramework.WHY_WHAT_HOW_VALUE:
            return [
                NarrativeSlideIntent(
                    stage_id="WHY",
                    slide_title=f"Why Change Now: The Cost of Inaction in {topic}",
                    slide_subtitle="Customer OTIF penalties and scrap rates erode operating margins by $3.4M annually.",
                    category_tag="1. WHY • COMPELLING REASON TO ACT",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="The compounding financial loss and delivery penalties under legacy processes.",
                        believe="Doing nothing is significantly more costly than transforming.",
                        decide="Prioritize immediate capital allocation.",
                        do="Authorize solution evaluation."
                    ),
                    recommended_density=VisualDensity.HIGH_DENSITY,
                    recommended_primitive="dashboard",
                    is_dark=False,
                    data_payload={"question": "How much is quality costing us?"}
                ),
                NarrativeSlideIntent(
                    stage_id="WHAT",
                    slide_title="Target Solution Architecture & Clean Core",
                    slide_subtitle="Decoupled ISA-95 execution stack preserving SAP S/4HANA ledger purity.",
                    category_tag="2. WHAT • THE TARGET SOLUTION",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="The target technical components, interfaces, and persistence layers.",
                        believe="The solution is modern, standards-based, and future-proof.",
                        decide="Adopt the proposed target architecture as the enterprise blueprint.",
                        do="Freeze legacy customization requests."
                    ),
                    recommended_density=VisualDensity.MEDIUM_DENSITY,
                    recommended_primitive="architecture_diagram",
                    is_dark=True,
                    data_payload={"template_id": "CLEAN_CORE_SAP_TO_SHOPFLOOR"}
                ),
                NarrativeSlideIntent(
                    stage_id="HOW",
                    slide_title="Execution Mechanics & Governance RACI",
                    slide_subtitle="Air-gapped edge buffering, deterministic machine interlocks, and RACI governance.",
                    category_tag="3. HOW • OPERATIONAL EXECUTION",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="How systems interact on the plant floor without interrupting live lines.",
                        believe="The deployment methodology is realistic and governance is unambiguous.",
                        decide="Approve the governance and responsibility allocation.",
                        do="Charter the joint program steering committee."
                    ),
                    recommended_density=VisualDensity.HIGH_DENSITY,
                    recommended_primitive="table",
                    is_dark=False,
                    data_payload={"table_archetype": TableArchetype.RESPONSIBILITY_MATRIX}
                ),
                NarrativeSlideIntent(
                    stage_id="BUSINESS_VALUE",
                    slide_title="Quantified Business Case & Commercial Payback",
                    slide_subtitle="$3.11M audited annual EBITDA impact delivering a 3.3-month payback horizon.",
                    category_tag="4. BUSINESS VALUE • COMMERCIAL TERMS",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="The return on investment, milestone deliverables, and fixed-price fee structure.",
                        believe="The business case provides extraordinary risk-adjusted return.",
                        decide="Approve the fixed-price commercial proposal.",
                        do="Execute contract engagement agreement."
                    ),
                    recommended_density=VisualDensity.HIGH_DENSITY,
                    recommended_primitive="table",
                    is_dark=False,
                    data_payload={"table_archetype": TableArchetype.BUSINESS_BENEFITS}
                )
            ]

        # ---------------------------------------------------------------------
        # FRAMEWORK 4: EXECUTIVE DEMONSTRATION
        # ---------------------------------------------------------------------
        else: # EXECUTIVE_DEMONSTRATION
            return [
                NarrativeSlideIntent(
                    stage_id="OPENING",
                    slide_title="Executive Context & Operational Mission",
                    slide_subtitle="Demonstrating closed-loop manufacturing execution integrated with SAP S/4HANA.",
                    category_tag="1. OPENING • EXECUTIVE CONTEXT",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="The exact operational challenge being solved today.",
                        believe="This session demonstrates real, working enterprise mechanics.",
                        decide="Engage actively in evaluating the technical workflow.",
                        do="Set expectations for the live operational walkthrough."
                    ),
                    recommended_density=VisualDensity.LOW_DENSITY,
                    recommended_primitive="executive_statement",
                    is_dark=True,
                    data_payload={"statement": "Zero latency between the machine spindle and the balance sheet.", "thesis": "Demonstrating how edge telemetry updates SAP financials without human delay."}
                ),
                NarrativeSlideIntent(
                    stage_id="BUSINESS_OUTCOMES",
                    slide_title="Target Operational Telemetry & KPI Benchmark",
                    slide_subtitle="95% Customer OTIF, 96.5% First Pass Yield, and 28-day inventory turns.",
                    category_tag="2. OUTCOMES • STRATEGIC TELEMETRY",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="The quantitative metrics the solution is designed to optimize.",
                        believe="These outcomes solve our primary board-level bottlenecks.",
                        decide="Agree that these four metrics define transformation success.",
                        do="Hold delivery teams accountable to these target SLAs."
                    ),
                    recommended_density=VisualDensity.HIGH_DENSITY,
                    recommended_primitive="dashboard",
                    is_dark=False,
                    data_payload={"question": "Are we shipping what we promised?"}
                ),
                NarrativeSlideIntent(
                    stage_id="CHALLENGES",
                    slide_title="Current System Friction & Latency Bottlenecks",
                    slide_subtitle="Point-to-point batch replication delays order visibility by up to four hours.",
                    category_tag="3. CHALLENGES • SYSTEM FRICTION",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="Why existing legacy tools fail to achieve the required latency.",
                        believe="Incremental patches to ECC cannot fix structural batch latency.",
                        decide="Reject superficial workarounds.",
                        do="Demand an event-driven architecture."
                    ),
                    recommended_density=VisualDensity.HIGH_DENSITY,
                    recommended_primitive="table",
                    is_dark=False,
                    data_payload={"table_archetype": TableArchetype.ARCHITECTURE_COMPARISON}
                ),
                NarrativeSlideIntent(
                    stage_id="OPPORTUNITIES",
                    slide_title="Clean-Core Decoupling & Edge Buffering",
                    slide_subtitle="Event-driven architecture separating shopfloor execution from financial ledgers.",
                    category_tag="4. OPPORTUNITIES • ARCHITECTURAL LEAP",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="The core innovations making this breakthrough possible.",
                        believe="Air-gapped edge buffering guarantees uninterrupted plant operation.",
                        decide="Endorse the clean-core decoupling strategy.",
                        do="Review the technical demonstration."
                    ),
                    recommended_density=VisualDensity.LOW_DENSITY,
                    recommended_primitive="architectural_principle",
                    is_dark=True,
                    data_payload={"headline": "Air-Gapped Plant Resilience", "core_rule": "The factory must never stop when the enterprise network disconnects.", "rationale": "Edge gateways sustain 48 hours of autonomous production, synching on reconnect."}
                ),
                NarrativeSlideIntent(
                    stage_id="DEMONSTRATION",
                    slide_title="Live Architecture Topology & Data Movement",
                    slide_subtitle="End-to-end trace: S/4HANA Order -> BTP Mesh -> DMC Execution -> Edge IPC -> Machine PLC.",
                    category_tag="5. DEMO • LIVE ARCHITECTURE MECHANICS",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="How orders, tool parameters, and confirmations flow in real time.",
                        believe="The solution is robust, deterministic, and enterprise-grade.",
                        decide="Confirm technical feasibility and compliance with plant security.",
                        do="Proceed to pilot deployment planning."
                    ),
                    recommended_density=VisualDensity.MEDIUM_DENSITY,
                    recommended_primitive="architecture_diagram",
                    is_dark=True,
                    data_payload={"template_id": "CLEAN_CORE_SAP_TO_SHOPFLOOR"}
                ),
                NarrativeSlideIntent(
                    stage_id="CLOSE",
                    slide_title="Commercial Proposal & Next Steps",
                    slide_subtitle="Milestone-linked fixed investment delivering production capability in 90 days.",
                    category_tag="6. CLOSE • DECISION & ACTION",
                    cognitive_objective=AudienceCognitiveObjective(
                        understand="The commercial terms, warranty scope, and immediate Day 1 actions.",
                        believe="The risk is fully mitigated by deliverable-linked acceptance gates.",
                        decide="Approve engagement and launch Gate 1 discovery.",
                        do="Sign milestone agreement."
                    ),
                    recommended_density=VisualDensity.HIGH_DENSITY,
                    recommended_primitive="table",
                    is_dark=False,
                    data_payload={"table_archetype": TableArchetype.COMMERCIAL_PROPOSAL}
                )
            ]

    # =========================================================================
    # 3. Slide Rendering Dispatcher
    # =========================================================================

    @classmethod
    def render_narrative_deck(
        cls,
        prs: Presentation,
        framework: NarrativeFramework,
        topic: str,
        client_name: str = "Executive Leadership",
        custom_data: Optional[Dict[str, Any]] = None
    ) -> List[NarrativeSlideIntent]:
        """
        Renders the complete narrative deck without exposing internal cognitive reasoning.
        """
        intents = cls.plan_narrative_deck(framework, topic, client_name, custom_data)

        for intent in intents:
            prim = intent.recommended_primitive
            payload = intent.data_payload

            # 1. Executive Statement (Low Density)
            if prim == "executive_statement":
                LowDensitySlideRenderer.render_executive_statement(
                    prs=prs,
                    statement=payload.get("statement", intent.slide_title),
                    supporting_thesis=payload.get("thesis", intent.slide_subtitle),
                    author_or_source=payload.get("source"),
                    category_tag=intent.category_tag,
                    client_name=client_name,
                    is_dark=intent.is_dark
                )

            # 2. Architectural Principle (Low Density)
            elif prim == "architectural_principle":
                LowDensitySlideRenderer.render_architectural_principle(
                    prs=prs,
                    principle_title=intent.slide_title,
                    core_rule=payload.get("core_rule", intent.slide_subtitle),
                    architectural_rationale=payload.get("rationale", "Underlying architectural constraint."),
                    category_tag=intent.category_tag,
                    client_name=client_name,
                    is_dark=intent.is_dark
                )

            # 3. Hero KPI (Low Density)
            elif prim == "hero_kpi":
                LowDensitySlideRenderer.render_hero_kpi_with_conclusion(
                    prs=prs,
                    metric_value=payload.get("metric_value", "$3.11M"),
                    metric_label=payload.get("metric_label", intent.slide_title),
                    conclusion_statement=payload.get("conclusion", intent.slide_subtitle),
                    category_tag=intent.category_tag,
                    client_name=client_name,
                    is_dark=intent.is_dark
                )

            # 4. Architecture Diagram (Medium Density)
            elif prim == "architecture_diagram":
                template_id = payload.get("template_id", "CLEAN_CORE_SAP_TO_SHOPFLOOR")
                if template_id == "ZERO_TRUST_OT_PERIMETER":
                    spec = ArchitectureBlueprintFactory.zero_trust_ot_security_perimeter(client_name=client_name)
                else:
                    spec = ArchitectureBlueprintFactory.clean_core_sap_to_shopfloor(client_name=client_name)
                spec.title = intent.slide_title
                spec.subtitle = intent.slide_subtitle
                spec.category_tag = intent.category_tag
                spec.is_dark = intent.is_dark
                EnterpriseArchitectureComposer.compose_and_render(prs, spec)

            # 5. Executive Dashboard (High Density)
            elif prim == "dashboard":
                q = payload.get("question", intent.slide_title)
                dspec = ExecutiveDashboardComposer.build_from_question(q, client_name=client_name)
                dspec.business_question = intent.slide_title
                dspec.key_takeaway = intent.slide_subtitle
                dspec.category_tag = intent.category_tag
                dspec.is_dark = intent.is_dark
                ExecutiveDashboardComposer.compose_and_render(prs, dspec)

            # 6. Structured Table (High Density)
            elif prim == "table":
                t_arch = payload.get("table_archetype", TableArchetype.COMMERCIAL_PROPOSAL)
                tspec = EnterpriseTableFactory.get_table_spec(t_arch, client_name=client_name)
                tspec.title = intent.slide_title
                tspec.subtitle = intent.slide_subtitle
                tspec.category_tag = intent.category_tag
                tspec.is_dark = intent.is_dark
                EnterpriseTableComposer.compose_and_render(prs, tspec)

            # Fallback
            else:
                LowDensitySlideRenderer.render_executive_statement(
                    prs=prs,
                    statement=intent.slide_title,
                    supporting_thesis=intent.slide_subtitle,
                    category_tag=intent.category_tag,
                    client_name=client_name,
                    is_dark=intent.is_dark
                )

        return intents
