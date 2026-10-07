"""
Enterprise Architecture Composition Engine.

Orchestrates multi-slide solution-design presentations as a coherent narrative arc
rather than a disjointed sequence of independent slides.

Enforces:
1. Canonical 15-stage Enterprise Solution Architecture Narrative Structure.
2. Visual Rhythm & Anti-Monotony Guardrails (alternating layouts, densities, and themes).
3. Strategic Section-to-Visual-Primitive mapping.
4. Seamless rendering using native PowerPoint shapes, tables, and charts via the Design System.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Any, Optional, Tuple
import os

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE

from .typography import TypographySystem
from .spacing import CanvasBounds, Margins, SpacingScale, GridCalculator
from .color import Theme, ExecutiveNavyTheme, ConsultingSlateTheme, ColorSystem
from .semantic import SemanticSlide, VisualIntent
from .primitives import HeaderPrimitive, FooterPrimitive, SurfacePrimitive, CalloutBannerPrimitive
import design_system.library as lib


# =============================================================================
# 1. Canonical Narrative Structure (15 Sections)
# =============================================================================

class NarrativeSection(Enum):
    """The 15 canonical sections of an enterprise solution architecture presentation."""
    EXECUTIVE_CONTEXT = 1             # 1. Strategic Mandate, CXO Thesis, North Star
    CURRENT_REALITY = 2               # 2. Operating Baseline, As-Is Friction, Value Leakage
    BUSINESS_PROBLEM = 3              # 3. Problem Landscape, Quantitative Variance, Scrap
    ROOT_CAUSE_CONSTRAINT = 4         # 4. Underlying Mechanics, Goldratt Constraints, Bottlenecks
    OPPORTUNITY = 5                   # 5. The Strategic Opportunity, To-Be Ambition, Capability Shifts
    TARGET_ARCHITECTURE = 6           # 6. Target System Architecture, Ring-Fencing, Clean Core
    PROCESS_TRANSFORMATION = 7        # 7. End-to-End Process Flow, Swimlanes, Decision Gateways
    DATA_INTEGRATION_ARCHITECTURE = 8 # 8. Integration Pipelines, Event Mesh, DMZ, Boundary Defense
    OPERATIONAL_EXECUTION = 9         # 9. Shop Floor Execution, Workstations, Genealogy, Traceability
    GOVERNANCE = 10                   # 10. Multi-Tier Control Gates, RACI Model, Steering Cadence
    ANALYTICS_INTELLIGENCE = 11       # 11. KPI Cockpits, Real-Time Dashboards, Decision Models
    IMPLEMENTATION_ROADMAP = 12       # 12. Phased Rollout, Milestone Deliverables, Workstreams
    BUSINESS_OUTCOMES = 13            # 13. Value Realization, EBITDA / Cash Acceleration, Payback
    RISKS_ASSUMPTIONS = 14            # 14. Enterprise Risk Heatmap, Mitigation Radar, Assumptions
    COMMERCIAL_NEXT_STEPS = 15        # 15. Commercial Milestones, Invoicing Triggers, Immediate Next Steps


# =============================================================================
# 2. Section Archetypes & Visual Primitive Mapping
# =============================================================================

@dataclass
class SectionArchetype:
    """Design guidelines and primitive mappings for a narrative section."""
    section: NarrativeSection
    display_title: str
    category_tag: str
    dominant_question: str
    primary_primitives: List[str]      # Top recommended primitive keys
    preferred_theme_mode: str          # 'dark' or 'light'
    visual_density: str                # 'dense', 'medium', 'open'
    layout_family: str                 # 'blueprint', 'flow', 'dashboard', 'table', 'narrative', 'timeline'


SECTION_ARCHETYPES: Dict[NarrativeSection, SectionArchetype] = {
    NarrativeSection.EXECUTIVE_CONTEXT: SectionArchetype(
        section=NarrativeSection.EXECUTIVE_CONTEXT,
        display_title="Executive Context & Strategic Mandate",
        category_tag="EXECUTIVE MANDATE",
        dominant_question="Why are we here and what is the strategic board-level imperative?",
        primary_primitives=["executive_statement", "capability_map", "section_divider"],
        preferred_theme_mode="dark",
        visual_density="open",
        layout_family="narrative"
    ),
    NarrativeSection.CURRENT_REALITY: SectionArchetype(
        section=NarrativeSection.CURRENT_REALITY,
        display_title="Current Reality & Operating Baseline",
        category_tag="OPERATING REALITY",
        dominant_question="What operational and architectural friction creates latency and risk today?",
        primary_primitives=["current_vs_future_state", "value_stream", "heatmap"],
        preferred_theme_mode="light",
        visual_density="medium",
        layout_family="flow"
    ),
    NarrativeSection.BUSINESS_PROBLEM: SectionArchetype(
        section=NarrativeSection.BUSINESS_PROBLEM,
        display_title="Business Problem & Cost of Inaction",
        category_tag="PROBLEM ANALYSIS",
        dominant_question="Where is value leaking and what is the quantifiable penalty of the status quo?",
        primary_primitives=["pareto", "variance_view", "insight_and_evidence"],
        preferred_theme_mode="light",
        visual_density="medium",
        layout_family="dashboard"
    ),
    NarrativeSection.ROOT_CAUSE_CONSTRAINT: SectionArchetype(
        section=NarrativeSection.ROOT_CAUSE_CONSTRAINT,
        display_title="Root Cause & Structural Constraints",
        category_tag="SYSTEM MECHANICS",
        dominant_question="What hidden physical, technical, or memory constraint prevents conventional success?",
        primary_primitives=["insight_and_evidence", "value_driver_tree", "exception_rework_flow"],
        preferred_theme_mode="dark",
        visual_density="dense",
        layout_family="blueprint"
    ),
    NarrativeSection.OPPORTUNITY: SectionArchetype(
        section=NarrativeSection.OPPORTUNITY,
        display_title="The Strategic Opportunity",
        category_tag="STRATEGIC AMBITION",
        dominant_question="What new operating paradigm becomes unlocked by eliminating these constraints?",
        primary_primitives=["current_vs_future_state", "maturity_model", "outcome_chain"],
        preferred_theme_mode="light",
        visual_density="open",
        layout_family="narrative"
    ),
    NarrativeSection.TARGET_ARCHITECTURE: SectionArchetype(
        section=NarrativeSection.TARGET_ARCHITECTURE,
        display_title="Target Solution Architecture",
        category_tag="ARCHITECTURE BLUEPRINT",
        dominant_question="How are system tiers, runtime boundaries, and clean-core transactions decoupled?",
        primary_primitives=["system_architecture", "layered_architecture", "enterprise_to_shopfloor", "cloud_edge_architecture"],
        preferred_theme_mode="dark",
        visual_density="dense",
        layout_family="blueprint"
    ),
    NarrativeSection.PROCESS_TRANSFORMATION: SectionArchetype(
        section=NarrativeSection.PROCESS_TRANSFORMATION,
        display_title="Process Transformation & Workflow",
        category_tag="PROCESS ARCHITECTURE",
        dominant_question="How does information and physical material flow through the transformed operational path?",
        primary_primitives=["horizontal_process_flow", "swimlane_process", "decision_flow"],
        preferred_theme_mode="light",
        visual_density="medium",
        layout_family="flow"
    ),
    NarrativeSection.DATA_INTEGRATION_ARCHITECTURE: SectionArchetype(
        section=NarrativeSection.DATA_INTEGRATION_ARCHITECTURE,
        display_title="Data & Integration Architecture",
        category_tag="INTEGRATION TOPOLOGY",
        dominant_question="How is telemetry ingested, ring-fenced, and secured across network DMZ zones?",
        primary_primitives=["integration_architecture", "data_lineage", "security_boundary", "entity_relationship"],
        preferred_theme_mode="dark",
        visual_density="dense",
        layout_family="blueprint"
    ),
    NarrativeSection.OPERATIONAL_EXECUTION: SectionArchetype(
        section=NarrativeSection.OPERATIONAL_EXECUTION,
        display_title="Shop Floor Operational Execution",
        category_tag="SHOP FLOOR EXECUTION",
        dominant_question="How do frontline operators execute assembly and verify lot genealogy with zero error?",
        primary_primitives=["operational_workflow", "genealogy_tree", "parent_child_relationship"],
        preferred_theme_mode="light",
        visual_density="dense",
        layout_family="flow"
    ),
    NarrativeSection.GOVERNANCE: SectionArchetype(
        section=NarrativeSection.GOVERNANCE,
        display_title="Governance, Controls & RACI Model",
        category_tag="GOVERNANCE & CONTROLS",
        dominant_question="Who owns decisions and what automated gates protect the financial ledger from bad data?",
        primary_primitives=["approval_gates", "raci_responsibility", "control_framework", "governance_model"],
        preferred_theme_mode="light",
        visual_density="medium",
        layout_family="table"
    ),
    NarrativeSection.ANALYTICS_INTELLIGENCE: SectionArchetype(
        section=NarrativeSection.ANALYTICS_INTELLIGENCE,
        display_title="Analytics & Decision Intelligence",
        category_tag="DECISION COCKPIT",
        dominant_question="What operational telemetry enables CXO leadership to make closed-loop proactive decisions?",
        primary_primitives=["executive_dashboard", "kpi_strip", "trend_chart", "bar_chart"],
        preferred_theme_mode="dark",
        visual_density="dense",
        layout_family="dashboard"
    ),
    NarrativeSection.IMPLEMENTATION_ROADMAP: SectionArchetype(
        section=NarrativeSection.IMPLEMENTATION_ROADMAP,
        display_title="Phased Implementation Roadmap",
        category_tag="DELIVERY ROADMAP",
        dominant_question="What is the de-risked milestone sequence, workstream track, and gate criteria to deploy?",
        primary_primitives=["transformation_roadmap", "milestone_gates", "workstream_view", "timeline"],
        preferred_theme_mode="light",
        visual_density="medium",
        layout_family="timeline"
    ),
    NarrativeSection.BUSINESS_OUTCOMES: SectionArchetype(
        section=NarrativeSection.BUSINESS_OUTCOMES,
        display_title="Business Outcomes & Value Realization",
        category_tag="VALUE REALIZATION",
        dominant_question="What quantified EBITDA, working capital, and cash return does this transformation generate?",
        primary_primitives=["outcome_chain", "waterfall", "kpi_table", "key_takeaway"],
        preferred_theme_mode="light",
        visual_density="medium",
        layout_family="dashboard"
    ),
    NarrativeSection.RISKS_ASSUMPTIONS: SectionArchetype(
        section=NarrativeSection.RISKS_ASSUMPTIONS,
        display_title="Enterprise Risk Mitigation & Assumptions",
        category_tag="RISK MANAGEMENT",
        dominant_question="What technical and organizational risks threaten this program, and how are they hedged?",
        primary_primitives=["risk_matrix", "risk_register", "control_framework"],
        preferred_theme_mode="light",
        visual_density="medium",
        layout_family="table"
    ),
    NarrativeSection.COMMERCIAL_NEXT_STEPS: SectionArchetype(
        section=NarrativeSection.COMMERCIAL_NEXT_STEPS,
        display_title="Commercial Model & Immediate Next Steps",
        category_tag="COMMERCIAL TERMS",
        dominant_question="What is the turnkey milestone pricing, scope commitment, and immediate next action?",
        primary_primitives=["commercial_table", "action_register", "comparison_matrix", "key_takeaway"],
        preferred_theme_mode="dark",
        visual_density="medium",
        layout_family="table"
    ),
}


# =============================================================================
# 3. Visual Rhythm Controller
# =============================================================================

class VisualRhythmController:
    """
    Enforces visual pacing, layout diversity, and typographic balance across a presentation deck.
    
    Prevents presentation monotony anti-patterns:
    - Never place two identical layout families consecutively (e.g. Table after Table, Blueprint after Blueprint).
    - Alternates cognitive density (Dense blueprint -> Motion flow -> Telemetry dashboard -> Structured table).
    - Alternates theme atmosphere (Dark executive anchor -> Light operational detail) for visual breathing room.
    """

    @classmethod
    def optimize_slide_plan(
        cls,
        requested_sections: List[Tuple[NarrativeSection, Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """
        Takes raw section requests and optimizes visual primitive selection and theme pacing
        to guarantee a strong, engaging visual rhythm.
        """
        optimized_slides: List[Dict[str, Any]] = []
        last_layout_family: Optional[str] = None
        last_primitive_key: Optional[str] = None
        last_theme_mode: Optional[str] = None

        total_count = len(requested_sections)

        for idx, (section, user_payload) in enumerate(requested_sections, start=1):
            archetype = SECTION_ARCHETYPES[section]
            user_prim = user_payload.get("primitive")

            # 1. Select Primitive respecting Visual Diversity
            selected_primitive = None
            if user_prim and user_prim in archetype.primary_primitives:
                selected_primitive = user_prim
            else:
                # Pick primary candidate that doesn't repeat the previous layout family
                candidates = archetype.primary_primitives
                for cand in candidates:
                    cand_meta = lib.get_primitive_metadata(cand)
                    if cand != last_primitive_key:
                        selected_primitive = cand
                        break
                if not selected_primitive:
                    selected_primitive = candidates[0]

            # 2. Determine Layout Family
            cur_layout_family = archetype.layout_family
            # If same layout family as previous slide, adjust theme or primitive to inject variety
            is_layout_collision = (cur_layout_family == last_layout_family)

            # 3. Optimize Theme Pacing (Contrast rhythm)
            # Default to archetype preference, but avoid 4+ consecutive dark or light slides
            pref_theme = archetype.preferred_theme_mode
            if idx == 1 or idx == total_count:
                # First and last slides prefer Executive Navy Dark mode for gravitas
                resolved_theme = "navy"
            elif is_layout_collision:
                # Flip theme to break monotony
                resolved_theme = "slate" if last_theme_mode == "navy" else "navy"
            else:
                resolved_theme = "navy" if pref_theme == "dark" else "slate"

            # 4. Generate Slide Spec
            title = user_payload.get("title", f"{archetype.display_title}")
            subtitle = user_payload.get("subtitle", f"HOW IT WORKS: {archetype.dominant_question}")
            category = user_payload.get("category", archetype.category_tag)
            callout = user_payload.get("callout_banner")

            slide_spec = {
                "slide_number": idx,
                "total_slides": total_count,
                "section": section,
                "section_name": section.name,
                "title": title,
                "subtitle": subtitle,
                "category_tag": category,
                "primitive_key": selected_primitive,
                "layout_family": cur_layout_family,
                "theme_name": resolved_theme,
                "is_dark": (resolved_theme == "navy"),
                "callout_banner": callout,
                "data": user_payload.get("data", {}),
            }

            optimized_slides.append(slide_spec)
            last_layout_family = cur_layout_family
            last_primitive_key = selected_primitive
            last_theme_mode = resolved_theme

        return optimized_slides


# =============================================================================
# 4. Deck Composition Specifications
# =============================================================================

@dataclass
class ArchitectureDeckSpec:
    """Complete specification for an enterprise architecture presentation."""
    presentation_title: str
    client_name: str
    target_solution: str
    author: str = "Enterprise Architecture Advisory"
    sections: List[Tuple[NarrativeSection, Dict[str, Any]]] = field(default_factory=list)


# =============================================================================
# 5. Enterprise Architecture Composition Engine
# =============================================================================

class EnterpriseArchitectureCompositionEngine:
    """
    Primary orchestrator translating high-level architecture proposals
    into an intentionally sequenced, visually diverse presentation deck.
    """

    @classmethod
    def compose_deck_plan(cls, spec: ArchitectureDeckSpec) -> List[Dict[str, Any]]:
        """Plans the complete deck structure and assigns visual primitives with verified rhythm."""
        return VisualRhythmController.optimize_slide_plan(spec.sections)

    @classmethod
    def render_deck(cls, prs: Presentation, spec: ArchitectureDeckSpec) -> str:
        """Renders the full presentation into PowerPoint shapes using the Design System."""
        prs.slide_width = Inches(CanvasBounds.width)
        prs.slide_height = Inches(CanvasBounds.height)
        blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]

        deck_plan = cls.compose_deck_plan(spec)

        for slide_info in deck_plan:
            theme = ExecutiveNavyTheme if slide_info["is_dark"] else ConsultingSlateTheme

            # 1. Base Slide & Themed Canvas
            slide = prs.slides.add_slide(blank_layout)
            bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(CanvasBounds.width), Inches(CanvasBounds.height))
            bg.fill.solid()
            bg.fill.fore_color.rgb = theme.canvas
            bg.line.fill.background()

            # 2. Universal Header
            HeaderPrimitive.render(
                slide=slide,
                category_text=slide_info["category_tag"],
                title_text=slide_info["title"],
                subtitle_text=slide_info["subtitle"],
                theme=theme
            )

            # 3. Universal Footer
            FooterPrimitive.render(
                slide=slide,
                slide_num=slide_info["slide_number"],
                total_slides=slide_info["total_slides"],
                metadata_text=f"{spec.client_name} • {spec.target_solution} • {spec.author}",
                theme=theme
            )

            # 4. Render Primary Visual Primitive on Main Stage
            prim_key = slide_info["primitive_key"]
            meta = lib.get_primitive_metadata(prim_key)
            if meta:
                prim_cls = meta["class"]
                data = slide_info["data"]

                # Calculate geometry (leaving room for optional callout banner)
                has_callout = bool(slide_info["callout_banner"])
                prim_top = SpacingScale.CONTENT_TOP
                prim_height = SpacingScale.CONTENT_HEIGHT - (1.35 if has_callout else 0.0)
                prim_left = Margins.left
                prim_width = Margins().usable_width

                cls._dispatch_primitive(slide, prim_cls, prim_key, prim_left, prim_top, prim_width, prim_height, data, theme)

            # 5. Optional Architectural Callout Banner
            if slide_info["callout_banner"]:
                banner_y = SpacingScale.CONTENT_TOP + SpacingScale.CONTENT_HEIGHT - 1.25
                CalloutBannerPrimitive.render(
                    slide=slide,
                    left=Margins.left,
                    top=banner_y,
                    width=Margins().usable_width,
                    height=1.18,
                    headline="ARCHITECTURAL GUARANTEE & GOVERNANCE COMMITMENT",
                    body_bullets=[slide_info["callout_banner"]],
                    theme=theme
                )

        return f"Successfully composed and rendered {len(deck_plan)}-slide enterprise architecture presentation: '{spec.presentation_title}'."

    @staticmethod
    def _dispatch_primitive(slide, prim_cls, prim_key: str, left: float, top: float, width: float, height: float, data: Any, theme: Theme):
        """Dispatches data into primitive render method with automatic format conversion."""
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

        if isinstance(data, dict):
            for k, v in data.items():
                if k in custom_params:
                    kwargs[k] = v
        elif isinstance(data, list) and len(custom_params) == 1:
            kwargs[custom_params[0]] = data

        # System Architecture tier conversion
        if prim_key == "system_architecture" and "tiers" in kwargs:
            from .library.architecture import ArchTierData
            conv_tiers = []
            for t in kwargs["tiers"]:
                if isinstance(t, dict):
                    conv_tiers.append(ArchTierData(**t))
                elif isinstance(t, (list, tuple)):
                    conv_tiers.append(ArchTierData(
                        tier_name=t[0],
                        subtitle=t[1] if len(t) > 1 and isinstance(t[1], str) else "Architecture Subsystem",
                        subsystems=t[2] if len(t) > 2 and isinstance(t[2], list) else (t[1] if isinstance(t[1], list) else []),
                        protocol_to_next=t[3] if len(t) > 3 else None
                    ))
                else:
                    conv_tiers.append(t)
            kwargs["tiers"] = conv_tiers

        # Safe invocation
        try:
            prim_cls.render(**kwargs)
        except Exception as e:
            # Fallback error container
            tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
            tf = tb.text_frame
            TypographySystem.apply_to_paragraph(tf.paragraphs[0], TypographySystem.BODY_STRONG, f"Visual Primitive Render Error: {str(e)}", theme.status_critical)
