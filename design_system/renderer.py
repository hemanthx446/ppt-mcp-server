"""
PowerPoint Renderer Engine.

Translates SemanticSlide models into PowerPoint shapes using strictly defined
Visual Primitives, Typography tokens, Spacing scale, and Color themes.
"""

from typing import List, Tuple
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

from .typography import TypographySystem
from .spacing import CanvasBounds, Margins, SpacingScale, GridCalculator
from .color import ColorSystem, Theme
from .semantic import (
    SemanticSlide,
    VisualIntent,
    ContentBlock,
    KeyMetric,
    TableData,
    ProcessStep,
    ArchitectureTier,
    RoadmapPhase
)
from .primitives import (
    HeaderPrimitive,
    FooterPrimitive,
    SurfacePrimitive,
    TextPrimitive,
    MetricPrimitive,
    TablePrimitive,
    ConnectorPrimitive,
    CalloutBannerPrimitive
)


class PPTXRenderer:
    """Renderer orchestrator translating SemanticSlide instances into PowerPoint slides."""

    @staticmethod
    def initialize_presentation(prs: Presentation):
        """Ensures the presentation adheres to the 16:9 widescreen standard."""
        prs.slide_width = Inches(CanvasBounds.width)
        prs.slide_height = Inches(CanvasBounds.height)

    @staticmethod
    def create_base_slide(prs: Presentation, theme: Theme):
        """Creates a blank slide with the themed canvas background."""
        PPTXRenderer.initialize_presentation(prs)
        blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
        slide = prs.slides.add_slide(blank_layout)

        # Full canvas background shape
        bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0), Inches(0),
            Inches(CanvasBounds.width), Inches(CanvasBounds.height)
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = theme.canvas
        bg.line.fill.background()
        return slide

    @classmethod
    def render(cls, prs: Presentation, model: SemanticSlide):
        """Main rendering entry point for a semantic slide."""
        theme = ColorSystem.resolve_theme(model.is_dark)
        slide = cls.create_base_slide(prs, theme)

        # 1. Render Header
        HeaderPrimitive.render(
            slide=slide,
            category_text=model.category_tag,
            title_text=model.title,
            subtitle_text=model.narrative_subtitle,
            theme=theme
        )

        # 2. Render Footer
        FooterPrimitive.render(
            slide=slide,
            slide_num=model.slide_number,
            total_slides=model.total_slides,
            metadata_text=model.footer_metadata,
            theme=theme
        )

        # 3. Dispatch Content Based on Visual Intent
        if model.visual_intent == VisualIntent.SYSTEM_ARCHITECTURE:
            cls._render_architecture(slide, model, theme)
        elif model.visual_intent == VisualIntent.GOVERNANCE_MATRIX:
            cls._render_governance_matrix(slide, model, theme)
        elif model.visual_intent == VisualIntent.VALUE_REALIZATION:
            cls._render_value_realization(slide, model, theme)
        elif model.visual_intent in (VisualIntent.PROBLEM_FRICTION, VisualIntent.GENERIC_COMPARISON):
            cls._render_comparison(slide, model, theme)
        elif model.visual_intent == VisualIntent.EXECUTIVE_OPENING:
            cls._render_executive_opening(slide, model, theme)
        elif model.visual_intent == VisualIntent.PROCESS_JOURNEY:
            cls._render_process_journey(slide, model, theme)
        elif model.visual_intent == VisualIntent.PHASED_ROADMAP:
            cls._render_phased_roadmap(slide, model, theme)
        elif model.visual_intent == VisualIntent.OPERATIONAL_COCKPIT:
            cls._render_cockpit(slide, model, theme)
        else:
            cls._render_default_grid(slide, model, theme)

        # 4. Optional Callout Banner
        if model.callout_banner:
            banner_y = SpacingScale.CONTENT_TOP + SpacingScale.CONTENT_HEIGHT - 1.25
            CalloutBannerPrimitive.render(
                slide=slide,
                left=Margins.left,
                top=banner_y,
                width=Margins().usable_width,
                height=1.20,
                headline="ARCHITECTURAL GUARANTEE & GOVERNANCE COMMITMENT",
                body_bullets=[model.callout_banner],
                theme=theme
            )

        return slide

    # -------------------------------------------------------------
    # Visual Intent Renderers
    # -------------------------------------------------------------

    @classmethod
    def _render_architecture(cls, slide, model: SemanticSlide, theme: Theme):
        """Renders 3-tier architecture with protocol flow connectors."""
        tiers: List[ArchitectureTier] = [e for e in model.elements if isinstance(e, ArchitectureTier)]
        if not tiers:
            return

        has_callout = bool(model.callout_banner)
        avail_h = SpacingScale.CONTENT_HEIGHT - (1.35 if has_callout else 0.0)
        
        # Determine orientation: 3 horizontal columns or 3 vertical stacked layers
        col_count = len(tiers)
        cols = GridCalculator.get_columns(col_count, left=Margins.left, total_width=Margins().usable_width, gap=0.55)

        for i, tier in enumerate(tiers):
            col_x, col_w = cols[i]
            box = SurfacePrimitive.render(slide, col_x, SpacingScale.CONTENT_TOP, col_w, avail_h, theme)

            # Top accent strip
            strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(col_x), Inches(SpacingScale.CONTENT_TOP), Inches(col_w), Inches(0.06))
            strip.fill.solid()
            strip.fill.fore_color.rgb = theme.border_accent
            strip.line.fill.background()

            # Content inside box
            tb = slide.shapes.add_textbox(Inches(col_x + 0.16), Inches(SpacingScale.CONTENT_TOP + 0.18), Inches(col_w - 0.32), Inches(avail_h - 0.36))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

            # Tier Name
            p_tn = tf.paragraphs[0]
            TypographySystem.apply_to_paragraph(p_tn, TypographySystem.LABEL, tier.tier_name, theme.text_accent)

            # Subtitle
            p_sub = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_sub, TypographySystem.BODY_STRONG, tier.subtitle, theme.text_primary)
            p_sub.space_after = Pt(10.0)

            # Subsystem Components
            for comp in tier.components[:3]:
                p_c = tf.add_paragraph()
                p_c.space_after = Pt(6.0)
                TypographySystem.apply_to_paragraph(p_c, TypographySystem.BODY, f"•  {comp}", theme.text_muted)

            # Optional Guarantee Badge
            if tier.guarantee_badge:
                p_gb = tf.add_paragraph()
                p_gb.space_after = Pt(4.0)
                TypographySystem.apply_to_paragraph(p_gb, TypographySystem.ANNOTATION, tier.guarantee_badge, theme.status_success)

            # Connector Arrow to next tier
            if i < col_count - 1:
                arr_x = col_x + col_w + 0.10
                arr_y = SpacingScale.CONTENT_TOP + (avail_h / 2.0) - 0.15
                proto_label = tier.protocol_to_next if tier.protocol_to_next else "SYNC"
                ConnectorPrimitive.render_arrow(slide, arr_x, arr_y, 0.35, 0.28, "right", theme, label=proto_label)

    @classmethod
    def _render_governance_matrix(cls, slide, model: SemanticSlide, theme: Theme):
        """Renders enterprise data table (e.g., 5 W's matrix)."""
        table_data: TableData = next((e for e in model.elements if isinstance(e, TableData)), None)
        if not table_data:
            return

        TablePrimitive.render(
            slide=slide,
            left=Margins.left,
            top=SpacingScale.CONTENT_TOP,
            width=Margins().usable_width,
            height=SpacingScale.CONTENT_HEIGHT - 0.1,
            headers=table_data.headers,
            rows=table_data.rows,
            theme=theme,
            col_weights=table_data.column_weights
        )

    @classmethod
    def _render_value_realization(cls, slide, model: SemanticSlide, theme: Theme):
        """Renders 2-column side-by-side metric hero cards with operational proof points."""
        splits = GridCalculator.get_columns(2, left=Margins.left, total_width=Margins().usable_width, gap=SpacingScale.STANDARD)
        
        metrics = [e for e in model.elements if isinstance(e, KeyMetric)]
        content_blocks = [e for e in model.elements if isinstance(e, ContentBlock)]

        for i in range(min(2, len(splits))):
            col_x, col_w = splits[i]
            
            # Metric Hero Banner on top
            if i < len(metrics):
                m = metrics[i]
                MetricPrimitive.render(
                    slide=slide,
                    left=col_x,
                    top=SpacingScale.CONTENT_TOP,
                    width=col_w,
                    height=1.20,
                    value_str=m.value,
                    label_str=m.label,
                    context_str=m.context,
                    theme=theme,
                    accent_color=theme.status_success if m.is_positive else theme.status_warning
                )

            # Detail container below
            body_top = SpacingScale.CONTENT_TOP + 1.35
            body_h = SpacingScale.CONTENT_HEIGHT - 1.35
            SurfacePrimitive.render(slide, col_x, body_top, col_w, body_h, theme)

            if i < len(content_blocks):
                cb = content_blocks[i]
                tb = slide.shapes.add_textbox(Inches(col_x + 0.2), Inches(body_top + 0.2), Inches(col_w - 0.4), Inches(body_h - 0.4))
                tf = tb.text_frame
                tf.word_wrap = True
                tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

                p_t = tf.paragraphs[0]
                TypographySystem.apply_to_paragraph(p_t, TypographySystem.LABEL, cb.title, theme.text_accent)
                p_t.space_after = Pt(12.0)

                TextPrimitive.render_lead_in_list(tf, cb.bullets, theme, max_items=3)

    @classmethod
    def _render_comparison(cls, slide, model: SemanticSlide, theme: Theme):
        """Renders 2-column contrast (e.g. Current vs Target State)."""
        splits = GridCalculator.get_columns(2, left=Margins.left, total_width=Margins().usable_width, gap=SpacingScale.STANDARD)
        blocks: List[ContentBlock] = [e for e in model.elements if isinstance(e, ContentBlock)]

        for i in range(min(2, len(blocks))):
            col_x, col_w = splits[i]
            cb = blocks[i]
            
            # Left = warning/friction tint, Right = success/target tint
            fill_c = theme.surface_alt if i == 0 else theme.surface
            border_c = theme.status_warning if (i == 0 and not theme.is_dark) else (theme.status_success if i == 1 else theme.border)

            SurfacePrimitive.render(slide, col_x, SpacingScale.CONTENT_TOP, col_w, SpacingScale.CONTENT_HEIGHT, theme, fill_color=fill_c, border_color=border_c)

            tb = slide.shapes.add_textbox(Inches(col_x + 0.25), Inches(SpacingScale.CONTENT_TOP + 0.25), Inches(col_w - 0.5), Inches(SpacingScale.CONTENT_HEIGHT - 0.5))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

            p_h = tf.paragraphs[0]
            TypographySystem.apply_to_paragraph(p_h, TypographySystem.LABEL, cb.title, border_c)
            p_h.space_after = Pt(12.0)

            TextPrimitive.render_lead_in_list(tf, cb.bullets, theme, max_items=3)

    @classmethod
    def _render_executive_opening(cls, slide, model: SemanticSlide, theme: Theme):
        """Renders title / executive opening slide with 3 strategic pillars."""
        cols = GridCalculator.get_columns(3, left=Margins.left, total_width=Margins().usable_width, gap=SpacingScale.STANDARD)
        blocks = [e for e in model.elements if isinstance(e, ContentBlock)]
        
        # 3 Pillar Surfaces across bottom
        card_y = SpacingScale.CONTENT_TOP + 1.2
        card_h = SpacingScale.CONTENT_HEIGHT - 1.2

        for i, col in enumerate(cols):
            if i >= len(blocks):
                break
            cx, cw = col
            cb = blocks[i]
            SurfacePrimitive.render(slide, cx, card_y, cw, card_h, theme)

            tb = slide.shapes.add_textbox(Inches(cx + 0.18), Inches(card_y + 0.18), Inches(cw - 0.36), Inches(card_h - 0.36))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

            p_t = tf.paragraphs[0]
            TypographySystem.apply_to_paragraph(p_t, TypographySystem.LABEL, cb.title, theme.text_accent)
            p_t.space_after = Pt(10.0)

            if cb.subtitle:
                p_sub = tf.add_paragraph()
                TypographySystem.apply_to_paragraph(p_sub, TypographySystem.BODY_STRONG, cb.subtitle, theme.text_primary)
                p_sub.space_after = Pt(8.0)

            TextPrimitive.render_lead_in_list(tf, cb.bullets, theme, max_items=3)

    @classmethod
    def _render_process_journey(cls, slide, model: SemanticSlide, theme: Theme):
        """Renders step-by-step physical-to-digital execution steps."""
        steps: List[ProcessStep] = [e for e in model.elements if isinstance(e, ProcessStep)]
        if not steps:
            return
        
        count = len(steps)
        cols = GridCalculator.get_columns(count, left=Margins.left, total_width=Margins().usable_width, gap=0.3)

        for i, step in enumerate(steps):
            cx, cw = cols[i]
            SurfacePrimitive.render(slide, cx, SpacingScale.CONTENT_TOP, cw, SpacingScale.CONTENT_HEIGHT, theme)

            tb = slide.shapes.add_textbox(Inches(cx + 0.16), Inches(SpacingScale.CONTENT_TOP + 0.18), Inches(cw - 0.32), Inches(SpacingScale.CONTENT_HEIGHT - 0.36))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

            # Step Number
            p_sn = tf.paragraphs[0]
            TypographySystem.apply_to_paragraph(p_sn, TypographySystem.LABEL, f"STATION 0{step.step_num}", theme.text_accent)

            # Station Name
            p_nm = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_nm, TypographySystem.BODY_STRONG, step.station_name, theme.text_primary)
            p_nm.space_after = Pt(8.0)

            # Action
            p_act = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_act, TypographySystem.BODY, step.action, theme.text_muted)
            p_act.space_after = Pt(12.0)

            # Poka-Yoke Rule
            if step.poka_yoke_rule:
                p_py = tf.add_paragraph()
                TypographySystem.apply_to_paragraph(p_py, TypographySystem.ANNOTATION, f"INTERLOCK: {step.poka_yoke_rule}", theme.status_warning)

            # Connector to next station
            if i < count - 1:
                arr_x = cx + cw + 0.05
                arr_y = SpacingScale.CONTENT_TOP + (SpacingScale.CONTENT_HEIGHT / 2.0) - 0.12
                ConnectorPrimitive.render_arrow(slide, arr_x, arr_y, 0.20, 0.24, "right", theme)

    @classmethod
    def _render_phased_roadmap(cls, slide, model: SemanticSlide, theme: Theme):
        """Renders phased milestone delivery roadmap with explicit gate criteria."""
        phases: List[RoadmapPhase] = [e for e in model.elements if isinstance(e, RoadmapPhase)]
        if not phases:
            return

        cols = GridCalculator.get_columns(len(phases), left=Margins.left, total_width=Margins().usable_width, gap=SpacingScale.STANDARD)

        for i, phase in enumerate(phases):
            cx, cw = cols[i]
            SurfacePrimitive.render(slide, cx, SpacingScale.CONTENT_TOP, cw, SpacingScale.CONTENT_HEIGHT, theme)

            tb = slide.shapes.add_textbox(Inches(cx + 0.18), Inches(SpacingScale.CONTENT_TOP + 0.18), Inches(cw - 0.36), Inches(SpacingScale.CONTENT_HEIGHT - 0.36))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

            # Phase ID & Duration
            p_tag = tf.paragraphs[0]
            TypographySystem.apply_to_paragraph(p_tag, TypographySystem.LABEL, f"{phase.phase_id} • {phase.duration.upper()}", theme.text_accent)

            # Title
            p_t = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_t, TypographySystem.BODY_STRONG, phase.title, theme.text_primary)
            p_t.space_after = Pt(10.0)

            # Workstreams
            for ws in phase.workstreams[:3]:
                p_ws = tf.add_paragraph()
                p_ws.space_after = Pt(6.0)
                TypographySystem.apply_to_paragraph(p_ws, TypographySystem.BODY, f"•  {ws}", theme.text_muted)

            # Gate Criteria
            if phase.gate_criteria:
                p_gate = tf.add_paragraph()
                p_gate.space_after = Pt(4.0)
                TypographySystem.apply_to_paragraph(p_gate, TypographySystem.ANNOTATION, f"GATE CRITERIA: {phase.gate_criteria}", theme.status_success)

    @classmethod
    def _render_cockpit(cls, slide, model: SemanticSlide, theme: Theme):
        """Renders executive cockpit columns with report inventory and KPI cards."""
        blocks: List[ContentBlock] = [e for e in model.elements if isinstance(e, ContentBlock)]
        if not blocks:
            return

        cols = GridCalculator.get_columns(len(blocks), left=Margins.left, total_width=Margins().usable_width, gap=SpacingScale.STANDARD)

        for i, cb in enumerate(blocks):
            cx, cw = cols[i]
            SurfacePrimitive.render(slide, cx, SpacingScale.CONTENT_TOP, cw, SpacingScale.CONTENT_HEIGHT, theme)

            tb = slide.shapes.add_textbox(Inches(cx + 0.18), Inches(SpacingScale.CONTENT_TOP + 0.18), Inches(cw - 0.36), Inches(SpacingScale.CONTENT_HEIGHT - 0.36))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

            p_h = tf.paragraphs[0]
            TypographySystem.apply_to_paragraph(p_h, TypographySystem.LABEL, cb.title, theme.text_accent)
            p_h.space_after = Pt(8.0)

            if cb.subtitle:
                p_sub = tf.add_paragraph()
                TypographySystem.apply_to_paragraph(p_sub, TypographySystem.BODY_STRONG, cb.subtitle, theme.text_primary)
                p_sub.space_after = Pt(10.0)

            TextPrimitive.render_lead_in_list(tf, cb.bullets, theme, max_items=4)

    @classmethod
    def _render_default_grid(cls, slide, model: SemanticSlide, theme: Theme):
        """Fallback clean grid renderer for unspecified element lists."""
        blocks: List[ContentBlock] = [e for e in model.elements if isinstance(e, ContentBlock)]
        col_count = max(1, min(len(blocks), 4))
        cols = GridCalculator.get_columns(col_count, left=Margins.left, total_width=Margins().usable_width, gap=SpacingScale.STANDARD)

        for i, cb in enumerate(blocks[:col_count]):
            cx, cw = cols[i]
            SurfacePrimitive.render(slide, cx, SpacingScale.CONTENT_TOP, cw, SpacingScale.CONTENT_HEIGHT, theme)

            tb = slide.shapes.add_textbox(Inches(cx + 0.18), Inches(SpacingScale.CONTENT_TOP + 0.18), Inches(cw - 0.36), Inches(SpacingScale.CONTENT_HEIGHT - 0.36))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

            p_h = tf.paragraphs[0]
            TypographySystem.apply_to_paragraph(p_h, TypographySystem.LABEL, cb.title, theme.text_accent)
            p_h.space_after = Pt(10.0)

            TextPrimitive.render_lead_in_list(tf, cb.bullets, theme, max_items=3)
