"""
Business Transformation Maturity Assessment Engine.

Renders first-class maturity assessment visuals:
- 5-Level Maturity Staircase (1. Fragmented, 2. Standardized, 3. Integrated, 4. Intelligent, 5. Autonomous)
- Current vs. Target Level indicators and progression badges
- Score -> Gap -> Recommendation consulting layout
- Multi-dimensional assessment across Strategy, Process, Tech, Data, Quality, Governance

Strictly enforces:
- Inter-only typography
- Native PowerPoint shapes and progress bars
- Answers: "How good are you today, how much better could you be, and what should you do next?"
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Any
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

from .typography import TypographySystem, FONT_FAMILY
from .spacing import CanvasBounds, Margins, SpacingScale, GridCalculator
from .color import Theme
from .transformation_semantic import (
    MaturityAssessmentModel,
    MaturityDimensionScore,
    MaturityStaircaseLevel
)


class MaturityAssessmentComposer:
    """
    Renders enterprise maturity assessments including staircase models,
    gap scorecards, and prioritized transformation recommendations.
    """

    DEFAULT_STAIRCASE_LEVELS = [
        MaturityStaircaseLevel(1, "1. Fragmented", ["Manual paper logs", "Siloed machines", "Reactive firefighting"]),
        MaturityStaircaseLevel(2, "2. Standardized", ["Basic SOPs defined", "Disparate spreadsheets", "S/4HANA core entry"]),
        MaturityStaircaseLevel(3, "3. Integrated", ["S/4HANA + MES connected", "Automated genealogy", "Digital traveler"]),
        MaturityStaircaseLevel(4, "4. Intelligent", ["Closed-loop SPC", "Predictive maintenance", "Unified data fabric"]),
        MaturityStaircaseLevel(5, "5. Autonomous", ["Self-healing production", "Closed-loop AI control", "End-to-end digital twin"])
    ]

    @classmethod
    def render_staircase_scorecard(
        cls,
        slide,
        left: float,
        top: float,
        width: float,
        height: float,
        model: MaturityAssessmentModel,
        theme: Theme
    ):
        """
        Renders a comprehensive maturity assessment slide:
        - Top: Executive Score Banner (Current -> Target -> Net Lift)
        - Left 44%: 5-Step Ascending Maturity Staircase with Current/Target Markers
        - Right 54%: Dimension Score -> Gap -> Priority Recommendation Scorecard
        """
        # Outer container
        canvas_box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left), Inches(top), Inches(width), Inches(height)
        )
        canvas_box.fill.solid()
        canvas_box.fill.fore_color.rgb = theme.surface
        canvas_box.line.color.rgb = theme.border
        canvas_box.line.width = Pt(1.0)

        # 1. TOP EXECUTIVE SCORE BANNER
        hdr_h = 0.52
        hdr_box = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(left), Inches(top), Inches(width), Inches(hdr_h)
        )
        hdr_box.fill.solid()
        hdr_box.fill.fore_color.rgb = theme.surface_highlight
        hdr_box.line.fill.background()

        tf_h = hdr_box.text_frame
        tf_h.margin_left = Inches(0.20)
        tf_h.margin_top = Inches(0.08)
        p_h = tf_h.paragraphs[0]
        TypographySystem.apply_to_paragraph(
            p_h, TypographySystem.LABEL,
            f"DIGITAL TRANSFORMATION MATURITY ASSESSMENT: {model.title.upper()}",
            theme.text_accent
        )

        # Current vs Target metric chips on top right of banner
        cls._render_score_chips(
            slide=slide,
            right_x=left + width - 0.20,
            y=top + 0.08,
            current_score=model.overall_current_score,
            target_score=model.overall_target_score,
            theme=theme
        )

        content_top = top + hdr_h + 0.12
        content_h = height - hdr_h - 0.20

        stair_w = width * 0.44
        score_w = width * 0.53
        score_x = left + stair_w + 0.18

        # 2. LEFT: 5-STEP MATURITY STAIRCASE
        levels = model.staircase_levels or cls.DEFAULT_STAIRCASE_LEVELS
        cls._render_staircase(
            slide=slide,
            x=left + 0.14,
            y=content_top,
            w=stair_w,
            h=content_h,
            levels=levels,
            current_score=model.overall_current_score,
            target_score=model.overall_target_score,
            theme=theme
        )

        # 3. RIGHT: SCORE -> GAP -> RECOMMENDATION TABLE
        cls._render_dimension_scorecard(
            slide=slide,
            x=score_x,
            y=content_top,
            w=score_w,
            h=content_h,
            dimensions=model.dimensions,
            theme=theme
        )

    @classmethod
    def _render_score_chips(
        cls,
        slide,
        right_x: float,
        y: float,
        current_score: float,
        target_score: float,
        theme: Theme
    ):
        """Renders executive score progression chips in the header."""
        # Target chip
        target_chip = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(right_x - 1.80), Inches(y), Inches(1.80), Inches(0.36)
        )
        target_chip.fill.solid()
        target_chip.fill.fore_color.rgb = theme.status_success
        target_chip.line.fill.background()
        tf_t = target_chip.text_frame
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.alignment = PP_ALIGN.CENTER
        TypographySystem.apply_to_paragraph(
            p_t, TypographySystem.ANNOTATION,
            f"TARGET: {target_score:.1f} / 5.0",
            RGBColor(255, 255, 255)
        )

        # Arrow
        arr = slide.shapes.add_shape(
            MSO_SHAPE.RIGHT_ARROW,
            Inches(right_x - 2.15), Inches(y + 0.08), Inches(0.25), Inches(0.20)
        )
        arr.fill.solid()
        arr.fill.fore_color.rgb = theme.border_accent
        arr.line.fill.background()

        # Current chip
        cur_chip = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(right_x - 4.10), Inches(y), Inches(1.85), Inches(0.36)
        )
        cur_chip.fill.solid()
        cur_chip.fill.fore_color.rgb = theme.status_warning
        cur_chip.line.fill.background()
        tf_c = cur_chip.text_frame
        tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
        p_c = tf_c.paragraphs[0]
        p_c.alignment = PP_ALIGN.CENTER
        TypographySystem.apply_to_paragraph(
            p_c, TypographySystem.ANNOTATION,
            f"CURRENT: {current_score:.1f} / 5.0",
            RGBColor(255, 255, 255)
        )

    @classmethod
    def _render_staircase(
        cls,
        slide,
        x: float,
        y: float,
        w: float,
        h: float,
        levels: List[MaturityStaircaseLevel],
        current_score: float,
        target_score: float,
        theme: Theme
    ):
        """Renders 5 ascending staircase steps with current & target pins."""
        # Box container
        c_box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(h)
        )
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = theme.surface_alt
        c_box.line.color.rgb = theme.border
        c_box.line.width = Pt(1.0)

        # Header
        tb_h = slide.shapes.add_textbox(Inches(x + 0.12), Inches(y + 0.08), Inches(w - 0.24), Inches(0.32))
        tf_h = tb_h.text_frame
        tf_h.margin_left = tf_h.margin_top = 0
        TypographySystem.apply_to_paragraph(
            tf_h.paragraphs[0], TypographySystem.LABEL,
            "5-LEVEL DIGITAL MATURITY STAIRCASE",
            theme.text_accent
        )

        num_steps = len(levels)
        stair_bottom = y + h - 0.15
        step_h = (h - 0.65) / num_steps
        step_w_increment = (w - 0.28) / num_steps

        # Determine current and target integer steps
        cur_level_idx = min(max(int(round(current_score)) - 1, 0), num_steps - 1)
        tar_level_idx = min(max(int(round(target_score)) - 1, 0), num_steps - 1)

        for i, lvl in enumerate(levels):
            # Step ascends: Step 1 is at bottom left, Step 5 is at top right
            step_y = stair_bottom - ((i + 1) * step_h)
            step_x = x + 0.14
            step_cur_w = (i + 1) * step_w_increment

            is_current = (i == cur_level_idx)
            is_target = (i == tar_level_idx)

            fill_col = theme.surface
            border_col = theme.border
            if is_target:
                fill_col = theme.surface_highlight
                border_col = theme.status_success
            elif is_current:
                fill_col = theme.surface_highlight
                border_col = theme.status_warning

            step_box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(step_x), Inches(step_y), Inches(step_cur_w), Inches(step_h - 0.04)
            )
            step_box.fill.solid()
            step_box.fill.fore_color.rgb = fill_col
            step_box.line.color.rgb = border_col
            step_box.line.width = Pt(1.5 if (is_current or is_target) else 0.75)

            tf = step_box.text_frame
            tf.word_wrap = True
            tf.margin_left = Inches(0.10)
            tf.margin_top = Inches(0.04)

            # Step title
            p_st = tf.paragraphs[0]
            TypographySystem.apply_to_paragraph(
                p_st, TypographySystem.BODY_STRONG,
                lvl.level_name,
                theme.status_success if is_target else (theme.status_warning if is_current else theme.text_primary)
            )

            # Pin badge if current or target
            badge_text = ""
            if is_current:
                badge_text = " [CURRENT POSITION]"
            elif is_target:
                badge_text = " [TARGET HORIZON]"

            if badge_text:
                p_badge = tf.add_paragraph()
                TypographySystem.apply_to_paragraph(
                    p_badge, TypographySystem.ANNOTATION,
                    badge_text,
                    theme.status_success if is_target else theme.status_warning
                )

    @classmethod
    def _render_dimension_scorecard(
        cls,
        slide,
        x: float,
        y: float,
        w: float,
        h: float,
        dimensions: List[MaturityDimensionScore],
        theme: Theme
    ):
        """Renders dimension gap analysis: Score -> Identified Gap -> Priority Intervention."""
        c_box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(h)
        )
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = theme.surface
        c_box.line.color.rgb = theme.border
        c_box.line.width = Pt(1.0)

        # Header
        hdr_pill = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(0.36)
        )
        hdr_pill.fill.solid()
        hdr_pill.fill.fore_color.rgb = theme.surface_highlight
        hdr_pill.line.fill.background()
        tf_hp = hdr_pill.text_frame
        tf_hp.margin_left = Inches(0.12)
        tf_hp.margin_top = Inches(0.06)
        TypographySystem.apply_to_paragraph(
            tf_hp.paragraphs[0], TypographySystem.LABEL,
            "GAP AUDIT & PRIORITY INTERVENTIONS (SCORE -> GAP -> ACTION)",
            theme.text_accent
        )

        num_dims = min(len(dimensions), 5)
        if num_dims == 0:
            return

        row_y = y + 0.44
        row_h = (h - 0.52) / num_dims

        for k, dim in enumerate(dimensions[:5]):
            ry = row_y + (k * row_h)
            # Dimension card row
            d_box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(x + 0.10), Inches(ry + 0.04), Inches(w - 0.20), Inches(row_h - 0.08)
            )
            d_box.fill.solid()
            d_box.fill.fore_color.rgb = theme.surface_alt if (k % 2 == 1) else theme.surface
            d_box.line.color.rgb = theme.border_accent if dim.priority == "P1" else theme.border
            d_box.line.width = Pt(1.0 if dim.priority == "P1" else 0.5)

            tb = slide.shapes.add_textbox(
                Inches(x + 0.16), Inches(ry + 0.06), Inches(w - 0.32), Inches(row_h - 0.12)
            )
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

            # Line 1: Dimension Name + Score Progression + Priority Pill
            p_top = tf.paragraphs[0]
            gap_val = dim.target_score - dim.current_score
            TypographySystem.apply_to_paragraph(
                p_top, TypographySystem.BODY_STRONG,
                f"{dim.dimension_name}  [{dim.priority}]",
                theme.text_primary
            )

            # Score text
            p_sc = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(
                p_sc, TypographySystem.CAPTION,
                f"Current: {dim.current_score:.1f} / 5.0  ➔  Target: {dim.target_score:.1f} / 5.0 (Gap: +{gap_val:.1f})",
                theme.border_accent
            )

            # Line 2: Identified Gap
            p_gap = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(
                p_gap, TypographySystem.ANNOTATION,
                f"Gap: {dim.identified_gap}",
                theme.status_critical if dim.priority == "P1" else theme.text_muted
            )

            # Line 3: Priority Intervention
            p_int = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(
                p_int, TypographySystem.ANNOTATION,
                f"Intervention: {dim.priority_intervention}",
                theme.status_success
            )
