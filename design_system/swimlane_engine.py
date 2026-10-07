"""
Swimlane Process Diagram Engine.

Renders first-class cross-functional swimlane diagrams:
- Horizontal lane bands (Customer, SAP S/4HANA, MES, Shop Floor / OT, Quality, Management)
- Distinct actor/system header cards with role and scope badges
- Transactional handoffs crossing lane boundaries with protocol tags
- Poka-Yoke error-proofing rules and decision gates
- Loopback connectors for quality hold, rework, or release

Strictly enforces:
- Inter-only typography
- True geometric diagram flow rather than disconnected cards
- Clear cross-lane handoff arrows
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
from .primitives import SurfacePrimitive, ConnectorPrimitive
from .transformation_semantic import (
    SwimlaneDiagramModel,
    SwimlaneLane,
    SwimlaneStep,
    SwimlaneHandoff,
    ProcessNodeType
)


class SwimlaneDiagramComposer:
    """
    Renders enterprise cross-functional swimlane diagrams with multi-lane bands,
    step placements, and cross-lane handoff connectors.
    """

    @classmethod
    def render(
        cls,
        slide,
        left: float,
        top: float,
        width: float,
        height: float,
        model: SwimlaneDiagramModel,
        theme: Theme
    ):
        """
        Renders a full swimlane diagram into the specified slide bounding box.
        """
        lanes = model.lanes
        num_lanes = len(lanes)
        if num_lanes == 0:
            return

        # Overall diagram container
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
            f"CROSS-FUNCTIONAL OPERATIONAL SWIMLANE: {model.title.upper()}",
            theme.text_accent
        )

        # Usable diagram area below header
        diag_top = top + hdr_h
        diag_h = height - hdr_h
        lane_gap = 0.08
        lane_rows = GridCalculator.get_rows(num_lanes, top=diag_top + 0.05, total_height=diag_h - 0.10, gap=lane_gap)

        header_col_w = 2.10
        body_col_x = left + header_col_w + 0.12
        body_col_w = width - header_col_w - 0.24

        # Map lane_id to row index and y-position
        lane_coords: Dict[str, Tuple[float, float]] = {}  # lane_id -> (y, h)

        # 1. RENDER SWIMLANE BANDS & HEADERS
        for i, lane in enumerate(lanes):
            ly, lh = lane_rows[i]
            lane_coords[lane.lane_id] = (ly, lh)

            # Lane background band
            band = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(body_col_x), Inches(ly), Inches(body_col_w), Inches(lh)
            )
            band.fill.solid()
            # Alternate subtle tint
            band.fill.fore_color.rgb = theme.surface_alt if (i % 2 == 1) else theme.surface
            band.line.color.rgb = theme.border
            band.line.width = Pt(0.75)

            # Left Lane Header
            l_hdr = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(left + 0.08), Inches(ly), Inches(header_col_w), Inches(lh)
            )
            l_hdr.fill.solid()
            l_hdr.fill.fore_color.rgb = theme.surface_highlight
            l_hdr.line.color.rgb = theme.border_accent if (i == 1 or i == 2) else theme.border
            l_hdr.line.width = Pt(1.0)

            tf_lh = l_hdr.text_frame
            tf_lh.word_wrap = True
            tf_lh.margin_left = Inches(0.12)
            tf_lh.margin_right = Inches(0.08)
            tf_lh.margin_top = Inches(0.08)

            p_l = tf_lh.paragraphs[0]
            TypographySystem.apply_to_paragraph(
                p_l, TypographySystem.LABEL,
                lane.lane_name.upper(),
                theme.text_accent
            )

            if lane.system_tag:
                p_st = tf_lh.add_paragraph()
                TypographySystem.apply_to_paragraph(
                    p_st, TypographySystem.CAPTION,
                    lane.system_tag,
                    theme.text_muted
                )

        # 2. RENDER STEPS INSIDE LANES
        # Calculate maximum sequence order across steps
        max_seq = max((s.sequence_order for s in model.steps), default=6)
        col_w = (body_col_w - 0.30) / max(max_seq, 1)

        # Store step centers for handoff connectors
        step_centers: Dict[str, Tuple[float, float, float, float]] = {} # id -> (x, y, w, h)

        for step in model.steps:
            if step.lane_id not in lane_coords:
                continue

            ly, lh = lane_coords[step.lane_id]
            col_idx = step.sequence_order - 1
            sx = body_col_x + 0.15 + (col_idx * col_w)
            sw = col_w - 0.20
            sh = lh - 0.18
            sy = ly + 0.09

            step_centers[step.step_id] = (sx, sy, sw, sh)

            # Render Step Box
            shape_type = MSO_SHAPE.DIAMOND if step.is_decision else MSO_SHAPE.ROUNDED_RECTANGLE
            s_box = slide.shapes.add_shape(
                shape_type,
                Inches(sx), Inches(sy), Inches(sw), Inches(sh)
            )
            s_box.fill.solid()
            s_box.fill.fore_color.rgb = theme.surface
            s_box.line.color.rgb = theme.border_accent if step.is_decision else theme.border
            s_box.line.width = Pt(1.2 if step.is_decision else 1.0)

            tf_s = s_box.text_frame
            tf_s.word_wrap = True
            tf_s.margin_left = Inches(0.08)
            tf_s.margin_right = Inches(0.08)
            tf_s.margin_top = Inches(0.06)

            # Sequence tag
            p_seq = tf_s.paragraphs[0]
            TypographySystem.apply_to_paragraph(
                p_seq, TypographySystem.ANNOTATION,
                f"[{step.sequence_order}] {step.system_badge or ''}",
                theme.text_accent
            )

            p_title = tf_s.add_paragraph()
            TypographySystem.apply_to_paragraph(
                p_title, TypographySystem.BODY_STRONG,
                step.title,
                theme.text_primary
            )

            if step.subtitle:
                p_sub = tf_s.add_paragraph()
                TypographySystem.apply_to_paragraph(
                    p_sub, TypographySystem.ANNOTATION,
                    step.subtitle,
                    theme.text_muted
                )

            if step.kpi_annotation:
                p_kpi = tf_s.add_paragraph()
                TypographySystem.apply_to_paragraph(
                    p_kpi, TypographySystem.ANNOTATION,
                    step.kpi_annotation,
                    theme.status_info
                )

        # 3. RENDER CROSS-LANE & STEP HANDOFF CONNECTORS
        for handoff in model.handoffs:
            if handoff.from_step_id not in step_centers or handoff.to_step_id not in step_centers:
                continue

            fx, fy, fw, fh = step_centers[handoff.from_step_id]
            tx, ty, tw, th = step_centers[handoff.to_step_id]

            from_center_x = fx + (fw / 2)
            from_center_y = fy + (fh / 2)
            to_center_x = tx + (tw / 2)
            to_center_y = ty + (th / 2)

            # Determine relative direction: horizontal handoff vs vertical/cross-lane handoff
            if abs(to_center_y - from_center_y) < 0.20:
                # Same lane horizontal connector
                arr_x = fx + fw + 0.02
                arr_y = from_center_y - 0.08
                arr_w = max(tx - (fx + fw) - 0.04, 0.15)
                arr = slide.shapes.add_shape(
                    MSO_SHAPE.RIGHT_ARROW,
                    Inches(arr_x), Inches(arr_y), Inches(arr_w), Inches(0.16)
                )
                arr.fill.solid()
                arr.fill.fore_color.rgb = theme.border_accent
                arr.line.fill.background()

            elif to_center_y > from_center_y:
                # Downward cross-lane connector
                arr_x = from_center_x - 0.08
                arr_y = fy + fh + 0.02
                arr_h = max(ty - (fy + fh) - 0.04, 0.15)
                arr = slide.shapes.add_shape(
                    MSO_SHAPE.DOWN_ARROW,
                    Inches(arr_x), Inches(arr_y), Inches(0.16), Inches(arr_h)
                )
                arr.fill.solid()
                arr.fill.fore_color.rgb = theme.status_warning if handoff.is_feedback else theme.border_accent
                arr.line.fill.background()

                # Label tag
                if handoff.label:
                    cls._render_handoff_label(slide, arr_x + 0.20, arr_y + (arr_h / 2) - 0.10, handoff.label, theme)

            else:
                # Upward loop / feedback connector
                arr_x = from_center_x - 0.08
                arr_y = ty + th + 0.02
                arr_h = max(fy - (ty + th) - 0.04, 0.15)
                arr = slide.shapes.add_shape(
                    MSO_SHAPE.UP_ARROW,
                    Inches(arr_x), Inches(arr_y), Inches(0.16), Inches(arr_h)
                )
                arr.fill.solid()
                arr.fill.fore_color.rgb = theme.status_success if not handoff.is_feedback else theme.status_warning
                arr.line.fill.background()

                if handoff.label:
                    cls._render_handoff_label(slide, arr_x + 0.20, arr_y + (arr_h / 2) - 0.10, handoff.label, theme)

    @classmethod
    def _render_handoff_label(
        cls,
        slide,
        x: float,
        y: float,
        label_text: str,
        theme: Theme
    ):
        """Renders small informative pill badge beside cross-lane arrows."""
        badge = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(y), Inches(1.30), Inches(0.24)
        )
        badge.fill.solid()
        badge.fill.fore_color.rgb = theme.surface_highlight
        badge.line.color.rgb = theme.border
        badge.line.width = Pt(0.5)
        tf = badge.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        TypographySystem.apply_to_paragraph(
            p, TypographySystem.ANNOTATION,
            label_text,
            theme.text_accent
        )
