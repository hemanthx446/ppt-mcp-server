"""
Visual-Density and Whitespace Intelligence Engine.

Whitespace is an intentional architectural design choice, not empty space to be filled.
A slide does NOT need to be completely filled with boxes and cards.

Implements three distinct density tiers:

1. LOW DENSITY (50% - 70% intentional whitespace)
   - Executive statement
   - Architectural principle / North Star
   - Key strategic insight / conclusion
   - Section divider / transition
   - Hero KPI + single definitive conclusion
   * Rule: Minimalist, generous whitespace, large typography, zero filler cards.

2. MEDIUM DENSITY (30% - 45% intentional whitespace)
   - Architecture diagram
   - Process flow
   - Transformation roadmap
   - Governance model
   - Current vs Future comparison
   * Rule: Single focal visual primitive is 100% complete on its own.
     Do NOT add side banners, bottom summaries, or decorative icons simply to fill space.

3. HIGH DENSITY (15% - 25% structured whitespace)
   - Executive analytical dashboard
   - Structured enterprise table
   - Interface catalogue
   - Detailed operating model
   * Rule: High informational bandwidth, compact margins, structured grid, maximized scanability.

Optimizes:
   CONTENT IMPORTANCE  vs  VISUAL COMPLEXITY  vs  READABILITY.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Any, Optional, Tuple

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

from .typography import TypographySystem
from .spacing import CanvasBounds, Margins, SpacingScale, GridCalculator
from .color import Theme, ExecutiveNavyTheme, ConsultingSlateTheme, RGB
from .primitives import HeaderPrimitive, FooterPrimitive, SurfacePrimitive


# =============================================================================
# 1. Visual Density Classification
# =============================================================================

class VisualDensity(Enum):
    LOW_DENSITY = auto()      # Executive statement, principle, key insight, divider
    MEDIUM_DENSITY = auto()   # Architecture diagram, process flow, roadmap, governance
    HIGH_DENSITY = auto()     # Dashboard, analytical table, interface catalogue


class VisualDensityClassifier:
    """Classifies slides and visual primitives into density tiers."""

    LOW_DENSITY_KEYWORDS = [
        "executive statement", "statement", "architectural principle", "principle",
        "key insight", "insight", "section divider", "divider", "north star",
        "mandate", "strategic thesis", "takeaway", "hero kpi", "quote"
    ]

    MEDIUM_DENSITY_KEYWORDS = [
        "architecture diagram", "architecture", "system architecture", "process flow",
        "process", "value stream", "workflow", "journey", "roadmap", "timeline",
        "governance", "governance model", "operating model", "comparison", "as-is vs to-be",
        "swimlane", "control gates", "decision flow", "outcome chain"
    ]

    HIGH_DENSITY_KEYWORDS = [
        "dashboard", "cockpit", "analytical table", "table", "interface catalogue",
        "catalogue", "kpi definitions", "data mapping", "matrix", "raci", "risks",
        "assumptions", "commercial proposal", "detailed operating model", "heatmap"
    ]

    @classmethod
    def classify(
        cls,
        title_or_topic: str,
        primitive_hint: Optional[str] = None
    ) -> VisualDensity:
        """Determines the appropriate visual density tier."""
        combined = f"{title_or_topic} {primitive_hint or ''}".lower()

        # Check high density first
        if any(k in combined for k in cls.HIGH_DENSITY_KEYWORDS):
            return VisualDensity.HIGH_DENSITY

        # Check low density
        if any(k in combined for k in cls.LOW_DENSITY_KEYWORDS):
            return VisualDensity.LOW_DENSITY

        # Check medium density
        if any(k in combined for k in cls.MEDIUM_DENSITY_KEYWORDS):
            return VisualDensity.MEDIUM_DENSITY

        # Default to medium density (balanced)
        return VisualDensity.MEDIUM_DENSITY


# =============================================================================
# 2. Whitespace & Readability Intelligence
# =============================================================================

@dataclass
class DensityEvaluation:
    """Evaluation of visual density, whitespace budget, and anti-filler guardrails."""
    density_class: VisualDensity
    target_whitespace_ratio: float     # e.g., 0.60 for 60% whitespace
    content_importance: float          # 0.0 to 1.0
    visual_complexity: float           # 0.0 to 1.0
    readability_score: float           # 0.0 to 1.0
    is_self_sufficient: bool           # True if single primary component is complete
    allow_auxiliary_cards: bool        # False prevents adding filler cards
    layout_recommendation: str
    anti_filler_rules: List[str] = field(default_factory=list)


class WhitespaceIntelligenceEngine:
    """
    Optimizes Content Importance vs Visual Complexity vs Readability.
    Enforces anti-filler guardrails so slides with a single strong primitive are complete.
    """

    @classmethod
    def evaluate(
        cls,
        slide_title: str,
        primary_primitive: str,
        component_count: int = 1,
        text_volume_words: int = 25
    ) -> DensityEvaluation:
        density = VisualDensityClassifier.classify(slide_title, primary_primitive)

        if density == VisualDensity.LOW_DENSITY:
            return DensityEvaluation(
                density_class=VisualDensity.LOW_DENSITY,
                target_whitespace_ratio=0.65,
                content_importance=0.95,
                visual_complexity=0.15,
                readability_score=0.98,
                is_self_sufficient=True,
                allow_auxiliary_cards=False,
                layout_recommendation="Generous whitespace, large typography scale (24-32pt), centered/asymmetric hero layout.",
                anti_filler_rules=[
                    "DO NOT add satellite cards or container boxes.",
                    "DO NOT add generic summaries or decorative icons.",
                    "Let the core executive statement or architectural principle command the canvas."
                ]
            )

        elif density == VisualDensity.MEDIUM_DENSITY:
            return DensityEvaluation(
                density_class=VisualDensity.MEDIUM_DENSITY,
                target_whitespace_ratio=0.38,
                content_importance=0.85,
                visual_complexity=0.55,
                readability_score=0.90,
                is_self_sufficient=True,
                allow_auxiliary_cards=False,
                layout_recommendation="Single focal visual primitive occupying the main canvas with comfortable margins (0.80\" margins).",
                anti_filler_rules=[
                    "A slide with one strong architecture diagram is COMPLETE on its own.",
                    "A slide with one clear process flow or roadmap is COMPLETE on its own.",
                    "DO NOT add redundant bullet points or bottom callout cards simply because vertical space exists."
                ]
            )

        else: # HIGH_DENSITY
            return DensityEvaluation(
                density_class=VisualDensity.HIGH_DENSITY,
                target_whitespace_ratio=0.20,
                content_importance=0.90,
                visual_complexity=0.85,
                readability_score=0.82,
                is_self_sufficient=True,
                allow_auxiliary_cards=True,
                layout_recommendation="Structured grid, compact margins (0.08\" cell padding), max scanability.",
                anti_filler_rules=[
                    "A slide with an executive dashboard or structured table is COMPLETE.",
                    "Maintain strong typographic hierarchy and data alignment without decorative chrome."
                ]
            )


# =============================================================================
# 3. Dedicated Low-Density Visual Renderers
# =============================================================================

class LowDensitySlideRenderer:
    """
    Renders high-impact low-density slides with intentional, majestic whitespace.
    Zero decorative boxes, zero filler cards.
    """

    @classmethod
    def render_executive_statement(
        cls,
        prs: Presentation,
        statement: str,
        supporting_thesis: Optional[str] = None,
        author_or_source: Optional[str] = None,
        category_tag: str = "STRATEGIC IMPERATIVE",
        client_name: str = "Executive Leadership",
        is_dark: bool = True
    ):
        """
        Renders a minimalist, powerful executive statement slide.
        Whitespace ratio: ~65%. Zero filler boxes.
        """
        theme = ExecutiveNavyTheme if is_dark else ConsultingSlateTheme
        blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
        slide = prs.slides.add_slide(blank_layout)

        # 1. Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(CanvasBounds.width), Inches(CanvasBounds.height))
        bg.fill.solid()
        bg.fill.fore_color.rgb = theme.canvas
        bg.line.fill.background()

        # 2. Header Category Pill
        HeaderPrimitive.render(
            slide=slide,
            category_text=f"{category_tag} • {client_name.upper()}",
            title_text="",  # No duplicate title; statement IS the hero
            subtitle_text="",
            theme=theme
        )

        # 3. Universal Footer
        FooterPrimitive.render(
            slide=slide,
            slide_num=1,
            total_slides=1,
            metadata_text=f"{client_name} • Strategic Mandate • Intentional Whitespace",
            theme=theme
        )

        # 4. Hero Statement Canvas (Generous margins, vertically centered)
        # Left = 1.60", Width = 10.133", Top = 2.40", Height = 3.60"
        tb = slide.shapes.add_textbox(Inches(1.60), Inches(2.30), Inches(10.133), Inches(3.60))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Hero Statement
        p1 = tf.paragraphs[0]
        p1.space_after = Pt(24.0)
        TypographySystem.apply_to_paragraph(p1, TypographySystem.PRESENTATION_TITLE, f'"{statement}"', theme.text_primary)

        # Supporting Thesis
        if supporting_thesis:
            p2 = tf.add_paragraph()
            p2.space_after = Pt(14.0)
            TypographySystem.apply_to_paragraph(p2, TypographySystem.BODY_STRONG, supporting_thesis, theme.text_secondary)

        # Author / Attribution
        if author_or_source:
            p3 = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p3, TypographySystem.LABEL, f"— {author_or_source.upper()}", theme.border_accent)

        return slide

    @classmethod
    def render_architectural_principle(
        cls,
        prs: Presentation,
        principle_title: str,
        core_rule: str,
        architectural_rationale: str,
        category_tag: str = "ARCHITECTURAL PRINCIPLE",
        client_name: str = "Enterprise Architecture",
        is_dark: bool = True
    ):
        """
        Renders a definitive architectural rule or system constraint.
        Whitespace ratio: ~60%.
        """
        theme = ExecutiveNavyTheme if is_dark else ConsultingSlateTheme
        blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
        slide = prs.slides.add_slide(blank_layout)

        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(CanvasBounds.width), Inches(CanvasBounds.height))
        bg.fill.solid()
        bg.fill.fore_color.rgb = theme.canvas
        bg.line.fill.background()

        # Header
        HeaderPrimitive.render(
            slide=slide,
            category_text=f"{category_tag} • {principle_title.upper()}",
            title_text=principle_title,
            subtitle_text="",
            theme=theme
        )

        FooterPrimitive.render(
            slide=slide,
            slide_num=1,
            total_slides=1,
            metadata_text=f"{client_name} • Architecture Decision Standard",
            theme=theme
        )

        # Architectural Accent Bar (Vertical left indicator)
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.20), Inches(2.40), Inches(0.08), Inches(3.20))
        bar.fill.solid()
        bar.fill.fore_color.rgb = theme.border_accent
        bar.line.fill.background()

        # Principle Text Box
        tb = slide.shapes.add_textbox(Inches(1.50), Inches(2.35), Inches(10.20), Inches(3.40))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Core Rule
        p1 = tf.paragraphs[0]
        p1.space_after = Pt(20.0)
        TypographySystem.apply_to_paragraph(p1, TypographySystem.SECTION_TITLE, core_rule, theme.text_primary)

        # Rationale
        p2 = tf.add_paragraph()
        p2.space_after = Pt(12.0)
        TypographySystem.apply_to_paragraph(p2, TypographySystem.BODY, architectural_rationale, theme.text_secondary)

        return slide

    @classmethod
    def render_hero_kpi_with_conclusion(
        cls,
        prs: Presentation,
        metric_value: str,
        metric_label: str,
        conclusion_statement: str,
        context_detail: Optional[str] = None,
        category_tag: str = "STRATEGIC OUTCOME",
        client_name: str = "Executive Leadership",
        is_dark: bool = False
    ):
        """
        Renders a single monumental metric with a definitive takeaway.
        A complete slide in itself. Zero satellite cards.
        """
        theme = ExecutiveNavyTheme if is_dark else ConsultingSlateTheme
        blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
        slide = prs.slides.add_slide(blank_layout)

        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(CanvasBounds.width), Inches(CanvasBounds.height))
        bg.fill.solid()
        bg.fill.fore_color.rgb = theme.canvas
        bg.line.fill.background()

        HeaderPrimitive.render(
            slide=slide,
            category_text=f"{category_tag} • {client_name.upper()}",
            title_text=metric_label,
            subtitle_text="",
            theme=theme
        )

        FooterPrimitive.render(
            slide=slide,
            slide_num=1,
            total_slides=1,
            metadata_text=f"{client_name} • Key Impact Telemetry",
            theme=theme
        )

        # Split: Monumental Hero Number (Left 45%) vs Conclusion Statement (Right 55%)
        # Left Metric
        tb_num = slide.shapes.add_textbox(Inches(1.20), Inches(2.20), Inches(4.50), Inches(3.50))
        tf_num = tb_num.text_frame
        tf_num.word_wrap = True
        tf_num.margin_left = tf_num.margin_top = tf_num.margin_right = tf_num.margin_bottom = 0

        p_num = tf_num.paragraphs[0]
        p_num.space_after = Pt(12.0)
        # Monumental typography: 64pt
        TypographySystem.apply_to_paragraph(p_num, TypographySystem.PRESENTATION_TITLE, metric_value, theme.accent_primary)
        p_num.runs[0].font.size = Pt(64.0)
        p_num.runs[0].font.bold = True

        p_lbl = tf_num.add_paragraph()
        TypographySystem.apply_to_paragraph(p_lbl, TypographySystem.LABEL, metric_label.upper(), theme.text_accent)

        if context_detail:
            p_ctx = tf_num.add_paragraph()
            p_ctx.space_before = Pt(6.0)
            TypographySystem.apply_to_paragraph(p_ctx, TypographySystem.CAPTION, context_detail, theme.text_muted)

        # Right Conclusion Text
        tb_con = slide.shapes.add_textbox(Inches(6.20), Inches(2.40), Inches(6.00), Inches(3.20))
        tf_con = tb_con.text_frame
        tf_con.word_wrap = True
        tf_con.margin_left = tf_con.margin_top = tf_con.margin_right = tf_con.margin_bottom = 0

        p_take = tf_con.paragraphs[0]
        p_take.space_after = Pt(14.0)
        TypographySystem.apply_to_paragraph(p_take, TypographySystem.SLIDE_TITLE, conclusion_statement, theme.text_primary)

        return slide
