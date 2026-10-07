"""
Current-to-Future State Transformation Engine.

Renders first-class transformation bridges and operating model evolutions:
- Current State (Baseline Friction, Manual Constraints, Baseline KPIs)
- Transformation Intervention (Strategic Enablers, S/4HANA & MES Integration, Governance)
- Future State (Target Operating Model, Transformed Capabilities, Measurable Outcomes)
- Value-Stream and Operating Model Dimension Comparisons

Strictly enforces:
- Inter-only typography
- Directional transformation bridge rather than 3 generic cards
- Clear visual contrast between baseline tension and target outcomes
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
    TransformationBridgeModel,
    CurrentStateSnapshot,
    TransformationIntervention,
    FutureStateVision
)


class TransformationBridgeComposer:
    """
    Renders enterprise transformation bridges connecting baseline reality
    to target operating model through strategic interventions.
    """

    @classmethod
    def render_bridge(
        cls,
        slide,
        left: float,
        top: float,
        width: float,
        height: float,
        model: TransformationBridgeModel,
        theme: Theme
    ):
        """
        Renders a 3-part transformation bridge: Current State -> Interventions -> Future State.
        """
        # Master diagram boundary
        canvas_box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left), Inches(top), Inches(width), Inches(height)
        )
        canvas_box.fill.solid()
        canvas_box.fill.fore_color.rgb = theme.surface
        canvas_box.line.color.rgb = theme.border
        canvas_box.line.width = Pt(1.0)

        # Header bar
        hdr_h = 0.38
        hdr_box = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(left), Inches(top), Inches(width), Inches(hdr_h)
        )
        hdr_box.fill.solid()
        hdr_box.fill.fore_color.rgb = theme.surface_highlight
        hdr_box.line.fill.background()
        tf_h = hdr_box.text_frame
        tf_h.margin_left = Inches(0.20)
        tf_h.margin_top = Inches(0.06)
        TypographySystem.apply_to_paragraph(
            tf_h.paragraphs[0], TypographySystem.LABEL,
            f"ENTERPRISE TRANSFORMATION BLUEPRINT: {model.title.upper()}",
            theme.text_accent
        )

        content_top = top + hdr_h + 0.10
        content_h = height - hdr_h - 0.70 # reserve 0.60 for bottom roadmap banner

        # Proportions: Current (32%), Bridge Arrows/Intervention (34%), Future (34%)
        cur_w = width * 0.30
        int_w = width * 0.34
        fut_w = width * 0.30
        gap = (width - (cur_w + int_w + fut_w)) / 2

        cur_x = left + 0.12
        int_x = cur_x + cur_w + gap
        fut_x = int_x + int_w + gap

        # 1. CURRENT STATE CONTAINER (Baseline Tension & Pain)
        cls._render_current_state(slide, cur_x, content_top, cur_w, content_h, model.current_state, theme)

        # Connector arrow from Current -> Intervention
        arr1_x = cur_x + cur_w + 0.04
        arr1_w = gap - 0.08
        arr1 = slide.shapes.add_shape(
            MSO_SHAPE.RIGHT_ARROW,
            Inches(arr1_x), Inches(content_top + (content_h / 2) - 0.15), Inches(arr1_w), Inches(0.30)
        )
        arr1.fill.solid()
        arr1.fill.fore_color.rgb = theme.status_warning
        arr1.line.fill.background()

        # 2. TRANSFORMATION INTERVENTIONS CONTAINER (Center Engine)
        cls._render_interventions(slide, int_x, content_top, int_w, content_h, model.intervention, theme)

        # Connector arrow from Intervention -> Future
        arr2_x = int_x + int_w + 0.04
        arr2_w = gap - 0.08
        arr2 = slide.shapes.add_shape(
            MSO_SHAPE.RIGHT_ARROW,
            Inches(arr2_x), Inches(content_top + (content_h / 2) - 0.15), Inches(arr2_w), Inches(0.30)
        )
        arr2.fill.solid()
        arr2.fill.fore_color.rgb = theme.status_success
        arr2.line.fill.background()

        # 3. FUTURE STATE CONTAINER (Target Operating Model & Value)
        cls._render_future_state(slide, fut_x, content_top, fut_w, content_h, model.future_state, theme)

        # 4. BOTTOM ROADMAP / HORIZON BANNER
        btm_y = top + height - 0.52
        btm_h = 0.44
        btm_box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left + 0.12), Inches(btm_y), Inches(width - 0.24), Inches(btm_h)
        )
        btm_box.fill.solid()
        btm_box.fill.fore_color.rgb = theme.surface_highlight
        btm_box.line.color.rgb = theme.border_accent
        btm_box.line.width = Pt(1.0)
        tf_b = btm_box.text_frame
        tf_b.margin_left = Inches(0.18)
        tf_b.margin_top = Inches(0.08)
        TypographySystem.apply_to_paragraph(
            tf_b.paragraphs[0], TypographySystem.LABEL,
            f"HORIZON: {model.timeframe.upper()}",
            theme.border_accent
        )
        p_sub = tf_b.add_paragraph()
        TypographySystem.apply_to_paragraph(
            p_sub, TypographySystem.ANNOTATION,
            "Phase 1: S/4HANA Core & Clean Master Data  ➔  Phase 2: MES MOM Dispatch & Traceability  ➔  Phase 3: Closed-Loop Analytics & Autonomous Control",
            theme.text_primary
        )

    @classmethod
    def _render_current_state(
        cls,
        slide,
        x: float,
        y: float,
        w: float,
        h: float,
        state: CurrentStateSnapshot,
        theme: Theme
    ):
        """Renders baseline current state container with red/warning accents."""
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(h)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = theme.surface
        box.line.color.rgb = theme.status_critical
        box.line.width = Pt(1.2)

        # Header pill
        pill = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(0.34)
        )
        pill.fill.solid()
        pill.fill.fore_color.rgb = theme.surface_alt
        pill.line.fill.background()
        tf_p = pill.text_frame
        tf_p.margin_left = Inches(0.12)
        tf_p.margin_top = Inches(0.06)
        TypographySystem.apply_to_paragraph(
            tf_p.paragraphs[0], TypographySystem.LABEL,
            state.title.upper(),
            theme.status_critical
        )

        # Top Zone: Pain Points & Constraints
        top_h = h - 1.55
        tb = slide.shapes.add_textbox(
            Inches(x + 0.12), Inches(y + 0.38), Inches(w - 0.24), Inches(top_h)
        )
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        TypographySystem.apply_to_paragraph(
            p1, TypographySystem.BODY_STRONG,
            "Operational Constraints & Friction",
            theme.text_primary
        )
        p1.space_after = Pt(4)

        for pt in state.pain_points[:4]:
            p = tf.add_paragraph()
            p.space_after = Pt(3)
            TypographySystem.apply_to_paragraph(
                p, TypographySystem.CAPTION,
                f"✗  {pt}",
                theme.status_critical
            )

        # Bottom Zone: Structured Baseline Metrics Container
        if state.baseline_metrics:
            panel_y = y + h - 1.45
            metric_panel = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(x + 0.10), Inches(panel_y), Inches(w - 0.20), Inches(1.35)
            )
            metric_panel.fill.solid()
            metric_panel.fill.fore_color.rgb = theme.surface_alt
            metric_panel.line.color.rgb = theme.border
            metric_panel.line.width = Pt(0.75)

            tb_m = slide.shapes.add_textbox(
                Inches(x + 0.16), Inches(panel_y + 0.06), Inches(w - 0.32), Inches(1.22)
            )
            tf_m = tb_m.text_frame
            tf_m.word_wrap = True
            tf_m.margin_left = tf_m.margin_top = tf_m.margin_right = tf_m.margin_bottom = 0

            p_m_hdr = tf_m.paragraphs[0]
            p_m_hdr.space_after = Pt(3)
            TypographySystem.apply_to_paragraph(
                p_m_hdr, TypographySystem.LABEL,
                "BASELINE FRICTION METRICS",
                theme.text_muted
            )
            for m_lbl, m_val in state.baseline_metrics[:3]:
                p_m = tf_m.add_paragraph()
                p_m.space_after = Pt(2)
                TypographySystem.apply_to_paragraph(
                    p_m, TypographySystem.ANNOTATION,
                    f"• {m_lbl}: {m_val}",
                    theme.status_critical
                )

    @classmethod
    def _render_interventions(
        cls,
        slide,
        x: float,
        y: float,
        w: float,
        h: float,
        intervention: TransformationIntervention,
        theme: Theme
    ):
        """Renders center transformation enablers and architectural changes."""
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(h)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = theme.surface_highlight
        box.line.color.rgb = theme.border_accent
        box.line.width = Pt(1.4)

        # Header pill
        pill = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(0.34)
        )
        pill.fill.solid()
        pill.fill.fore_color.rgb = theme.surface
        pill.line.fill.background()
        tf_p = pill.text_frame
        tf_p.margin_left = Inches(0.12)
        tf_p.margin_top = Inches(0.06)
        TypographySystem.apply_to_paragraph(
            tf_p.paragraphs[0], TypographySystem.LABEL,
            intervention.title.upper(),
            theme.border_accent
        )

        top_h = h - 1.55
        tb = slide.shapes.add_textbox(
            Inches(x + 0.12), Inches(y + 0.38), Inches(w - 0.24), Inches(top_h)
        )
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        TypographySystem.apply_to_paragraph(
            p1, TypographySystem.BODY_STRONG,
            "Strategic Initiatives & Technology",
            theme.text_primary
        )
        p1.space_after = Pt(4)

        for init in intervention.initiatives[:4]:
            p = tf.add_paragraph()
            p.space_after = Pt(3)
            TypographySystem.apply_to_paragraph(
                p, TypographySystem.CAPTION,
                f"⚙  {init}",
                theme.text_primary
            )

        # Bottom Zone: Architectural Enablers Container
        if intervention.enablers:
            panel_y = y + h - 1.45
            enabler_panel = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(x + 0.10), Inches(panel_y), Inches(w - 0.20), Inches(1.35)
            )
            enabler_panel.fill.solid()
            enabler_panel.fill.fore_color.rgb = theme.surface
            enabler_panel.line.color.rgb = theme.border_accent
            enabler_panel.line.width = Pt(0.75)

            tb_e = slide.shapes.add_textbox(
                Inches(x + 0.16), Inches(panel_y + 0.06), Inches(w - 0.32), Inches(1.22)
            )
            tf_e = tb_e.text_frame
            tf_e.word_wrap = True
            tf_e.margin_left = tf_e.margin_top = tf_e.margin_right = tf_e.margin_bottom = 0

            p_e_hdr = tf_e.paragraphs[0]
            p_e_hdr.space_after = Pt(3)
            TypographySystem.apply_to_paragraph(
                p_e_hdr, TypographySystem.LABEL,
                "CORE ARCHITECTURAL ENABLERS",
                theme.border_accent
            )
            for en in intervention.enablers[:3]:
                p_en = tf_e.add_paragraph()
                p_en.space_after = Pt(2)
                TypographySystem.apply_to_paragraph(
                    p_en, TypographySystem.ANNOTATION,
                    f"✔ {en}",
                    theme.text_primary
                )

    @classmethod
    def _render_future_state(
        cls,
        slide,
        x: float,
        y: float,
        w: float,
        h: float,
        future: FutureStateVision,
        theme: Theme
    ):
        """Renders target operating model container with success/green accents."""
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(h)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = theme.surface
        box.line.color.rgb = theme.status_success
        box.line.width = Pt(1.2)

        # Header pill
        pill = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(0.34)
        )
        pill.fill.solid()
        pill.fill.fore_color.rgb = theme.surface_alt
        pill.line.fill.background()
        tf_p = pill.text_frame
        tf_p.margin_left = Inches(0.12)
        tf_p.margin_top = Inches(0.06)
        TypographySystem.apply_to_paragraph(
            tf_p.paragraphs[0], TypographySystem.LABEL,
            future.title.upper(),
            theme.status_success
        )

        top_h = h - 1.55
        tb = slide.shapes.add_textbox(
            Inches(x + 0.12), Inches(y + 0.38), Inches(w - 0.24), Inches(top_h)
        )
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        TypographySystem.apply_to_paragraph(
            p1, TypographySystem.BODY_STRONG,
            "Transformed Capabilities",
            theme.text_primary
        )
        p1.space_after = Pt(4)

        for cap in future.transformed_capabilities[:4]:
            p = tf.add_paragraph()
            p.space_after = Pt(3)
            TypographySystem.apply_to_paragraph(
                p, TypographySystem.CAPTION,
                f"✔  {cap}",
                theme.status_success
            )

        # Bottom Zone: Target Audited Outcomes Container
        if future.target_outcomes:
            panel_y = y + h - 1.45
            outcome_panel = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(x + 0.10), Inches(panel_y), Inches(w - 0.20), Inches(1.35)
            )
            outcome_panel.fill.solid()
            outcome_panel.fill.fore_color.rgb = theme.surface_alt
            outcome_panel.line.color.rgb = theme.status_success
            outcome_panel.line.width = Pt(1.0)

            tb_o = slide.shapes.add_textbox(
                Inches(x + 0.16), Inches(panel_y + 0.06), Inches(w - 0.32), Inches(1.22)
            )
            tf_o = tb_o.text_frame
            tf_o.word_wrap = True
            tf_o.margin_left = tf_o.margin_top = tf_o.margin_right = tf_o.margin_bottom = 0

            p_o_hdr = tf_o.paragraphs[0]
            p_o_hdr.space_after = Pt(3)
            TypographySystem.apply_to_paragraph(
                p_o_hdr, TypographySystem.LABEL,
                "AUDITED VALUE OUTCOMES",
                theme.status_success
            )
            for o_lbl, o_val in future.target_outcomes[:3]:
                p_o = tf_o.add_paragraph()
                p_o.space_after = Pt(2)
                TypographySystem.apply_to_paragraph(
                    p_o, TypographySystem.ANNOTATION,
                    f"★ {o_lbl}: {o_val}",
                    theme.text_primary
                )
