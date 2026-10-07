"""
Process Flow Composition Engine with Smart Connector Intelligence.

Renders first-class enterprise business and manufacturing process diagrams:
- Sequential flows with explicit system and role tags
- Decision points with genuine geometric diamonds (MSO_SHAPE.DIAMOND)
- Branching and converging paths (Happy Path vs Exception / Rework)
- Feedback loops returning to prior operations
- Closed-loop cyber-physical manufacturing architectures
- End-to-end genealogy and traceability flows

Strictly enforces:
- Inter-only typography
- No disconnected cards or equal container grids
- Clear directional flow and readable arrowheads
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
    ProcessFlowModel,
    ProcessNode,
    ProcessBranch,
    ProcessNodeType,
    ClosedLoopManufacturingModel
)


class ProcessFlowComposer:
    """
    Renders enterprise process flows with branching, decision diamonds,
    feedback loops, and system interaction overlays.
    """

    @classmethod
    def render_branching_process(
        cls,
        slide,
        left: float,
        top: float,
        width: float,
        height: float,
        flow_model: ProcessFlowModel,
        theme: Theme
    ):
        """
        Renders a complex process flow with linear steps, a decision diamond,
        and branching paths (Pass -> Confirm, Fail -> Rework -> Re-inspection loop).
        """
        # Outer diagram canvas boundary
        canvas_box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left), Inches(top), Inches(width), Inches(height)
        )
        canvas_box.fill.solid()
        canvas_box.fill.fore_color.rgb = theme.surface
        canvas_box.line.color.rgb = theme.border
        canvas_box.line.width = Pt(1.0)

        # Header banner inside diagram
        hdr_box = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(left), Inches(top), Inches(width), Inches(0.40)
        )
        hdr_box.fill.solid()
        hdr_box.fill.fore_color.rgb = theme.surface_highlight
        hdr_box.line.fill.background()
        tf_h = hdr_box.text_frame
        tf_h.margin_left = Inches(0.20)
        tf_h.margin_top = Inches(0.06)
        p_h = tf_h.paragraphs[0]
        TypographySystem.apply_to_paragraph(
            p_h, TypographySystem.LABEL,
            f"PROCESS ARCHITECTURE: {flow_model.title.upper()}",
            theme.text_accent
        )

        nodes = flow_model.nodes
        decision_node = next((n for n in nodes if n.is_decision or n.node_type == ProcessNodeType.DECISION), None)

        if decision_node:
            dec_idx = nodes.index(decision_node)
            pre_decision = nodes[:dec_idx]
            post_decision = nodes[dec_idx + 1:]
        else:
            pre_decision = nodes
            post_decision = []

        # Layout Geometry
        # Upper track: Pre-decision linear sequence -> Decision Diamond -> Pass Path
        # Lower track: Fail / Rework Exception path -> Re-inspection -> Loopback
        diagram_top = top + 0.55
        track_h = 1.30
        bottom_y = top + height - 1.45

        pre_count = len(pre_decision)
        post_nodes = post_decision[:2]
        post_count = len(post_nodes)
        total_units = pre_count + 1 + post_count

        # Dynamic sizing ensuring everything stays strictly inside [left, left + width]
        step_gap = 0.22
        avail_w = width - 0.50 - ((total_units - 1) * step_gap)
        step_w = max(min(avail_w / max(total_units, 1), 1.45), 1.05)
        diamond_w = max(step_w, 1.25)
        diamond_h = track_h

        cur_x = left + 0.25

        # 1. PRE-DECISION LINEAR NODES
        for i, node in enumerate(pre_decision):
            cls._render_process_step_node(
                slide=slide,
                x=cur_x,
                y=diagram_top,
                w=step_w,
                h=track_h,
                step_num=i + 1,
                node=node,
                theme=theme
            )

            # Connector arrow to next node
            arr_x = cur_x + step_w + 0.03
            arr_w = step_gap - 0.06
            arr_y = diagram_top + (track_h / 2) - 0.12
            cls._render_directional_arrow(slide, arr_x, arr_y, max(arr_w, 0.14), 0.24, "right", theme)

            cur_x += step_w + step_gap

        # 2. DECISION DIAMOND
        diamond_w = max(step_w * 1.15, 1.35)
        diamond_x = cur_x
        diamond_y = diagram_top

        cls._render_decision_diamond(
            slide=slide,
            x=diamond_x,
            y=diamond_y,
            w=diamond_w,
            h=diamond_h,
            node=decision_node or ProcessNode(id="dec", label="Quality Gate", is_decision=True),
            theme=theme
        )

        # 3. BRANCH A: PASS / CONFIRM (Continues horizontally on the main line)
        # Dedicated clearance for PASS badge so it never collides with Step 6
        pass_gap = max(step_gap + 0.40, 0.68)
        pass_arr_x = diamond_x + diamond_w + 0.04
        pass_arr_w = pass_gap - 0.08
        cls._render_directional_arrow(slide, pass_arr_x, diamond_y + (diamond_h / 2) - 0.12, pass_arr_w, 0.24, "right", theme)

        # "PASS" condition tag centered over the connector arrow
        pass_badge_w = 0.52
        pass_badge_h = 0.22
        pass_badge_x = pass_arr_x + (pass_arr_w - pass_badge_w) / 2
        cls._render_condition_badge(slide, pass_badge_x, diamond_y + (diamond_h / 2) - 0.30, pass_badge_w, pass_badge_h, "PASS", theme.status_success)

        # Render post-decision pass nodes
        cur_pass_x = diamond_x + diamond_w + pass_gap
        for j, p_node in enumerate(post_nodes):
            cls._render_process_step_node(
                slide=slide,
                x=cur_pass_x,
                y=diagram_top,
                w=step_w,
                h=track_h,
                step_num=pre_count + j + 2,
                node=p_node,
                theme=theme,
                is_terminal=(j == len(post_nodes) - 1)
            )
            if j < len(post_nodes) - 1:
                p_arr_x = cur_pass_x + step_w + 0.03
                p_arr_w = step_gap - 0.06
                cls._render_directional_arrow(slide, p_arr_x, diagram_top + (track_h / 2) - 0.12, max(p_arr_w, 0.14), 0.24, "right", theme)
                cur_pass_x += step_w + step_gap

        # 4. BRANCH B: FAIL / REWORK LOOP (Branches vertically downward from Diamond)
        down_arr_x = diamond_x + (diamond_w / 2) - 0.12
        down_arr_y = diamond_y + diamond_h + 0.05
        down_arr_h = bottom_y - (diamond_y + diamond_h) - 0.10
        cls._render_directional_arrow(slide, down_arr_x, down_arr_y, 0.24, max(down_arr_h, 0.25), "down", theme, fill_color=theme.status_critical)

        # "FAIL / REWORK" condition tag
        cls._render_condition_badge(slide, diamond_x + (diamond_w / 2) + 0.16, down_arr_y + 0.10, 1.10, 0.24, "REWORK", theme.status_critical)

        # Rework Operation Node
        rework_node = ProcessNode(
            id="rework_1",
            label="Rework Operation",
            role_lane="MES / Operator",
            system_tag="MES Non-Conformance",
            action_detail="Quarantine & Root Cause Correction",
            poka_yoke="Defect Logged in S/4HANA QM"
        )
        rework_w = max(step_w + 0.30, 1.40)
        rework_x = max(diamond_x - 0.40, left + 0.30)
        cls._render_process_step_node(
            slide=slide,
            x=rework_x,
            y=bottom_y,
            w=rework_w,
            h=track_h,
            step_num=0,
            node=rework_node,
            theme=theme,
            custom_badge="EXCEPTION PATH",
            is_warning=True
        )

        # Re-inspection Node
        reinspect_node = ProcessNode(
            id="reinspect_1",
            label="Re-Inspection & Verification",
            role_lane="Quality Assurance",
            system_tag="Digital Traveler",
            action_detail="Tolerance Validation & Clearance",
            poka_yoke="Serial Unlocked Only on Clearance"
        )
        rework_gap = 0.25
        reinspect_w = max(step_w + 0.35, 1.45)
        reinspect_x = rework_x + rework_w + rework_gap
        cls._render_process_step_node(
            slide=slide,
            x=reinspect_x,
            y=bottom_y,
            w=reinspect_w,
            h=track_h,
            step_num=0,
            node=reinspect_node,
            theme=theme,
            custom_badge="CLEARANCE GATE",
            is_info=True
        )

        # Arrow between Rework -> Re-inspection
        rework_arr_x = rework_x + rework_w + 0.04
        rework_arr_w = rework_gap - 0.08
        cls._render_directional_arrow(slide, rework_arr_x, bottom_y + (track_h / 2) - 0.12, max(rework_arr_w, 0.14), 0.24, "right", theme)

        # Re-inspection feedback loop up back to Confirmation & Ledger
        loop_arr_x = reinspect_x + reinspect_w + 0.08
        loop_arr_h = 0.55
        loop_arr_y = bottom_y - loop_arr_h
        up_arr = slide.shapes.add_shape(
            MSO_SHAPE.UP_ARROW,
            Inches(loop_arr_x), Inches(loop_arr_y), Inches(0.24), Inches(loop_arr_h)
        )
        up_arr.fill.solid()
        up_arr.fill.fore_color.rgb = theme.status_warning
        up_arr.line.fill.background()

        # Feedback loop banner cleanly routed above the clearance gate
        loop_badge_w = 1.35
        loop_badge_x = loop_arr_x + 0.28
        loop_badge = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(loop_badge_x), Inches(loop_arr_y + 0.08), Inches(loop_badge_w), Inches(0.42)
        )
        loop_badge.fill.solid()
        loop_badge.fill.fore_color.rgb = theme.surface_highlight
        loop_badge.line.color.rgb = theme.status_warning
        loop_badge.line.width = Pt(1.0)
        tf_lb = loop_badge.text_frame
        tf_lb.word_wrap = True
        tf_lb.margin_left = tf_lb.margin_right = tf_lb.margin_top = tf_lb.margin_bottom = Inches(0.04)
        TypographySystem.apply_to_paragraph(
            tf_lb.paragraphs[0], TypographySystem.ANNOTATION,
            "↺ RE-ENTRY LOOP\nCleared for Confirmation",
            theme.status_warning
        )

    @classmethod
    def render_closed_loop_manufacturing(
        cls,
        slide,
        left: float,
        top: float,
        width: float,
        height: float,
        model: ClosedLoopManufacturingModel,
        theme: Theme
    ):
        """
        Renders a circular, closed-loop cyber-physical manufacturing architecture:
        Physical World -> Digital Capture -> Contextualization -> Intelligence -> Decision -> Action -> Physical World.
        """
        # Outer boundary
        canvas_box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left), Inches(top), Inches(width), Inches(height)
        )
        canvas_box.fill.solid()
        canvas_box.fill.fore_color.rgb = theme.surface
        canvas_box.line.color.rgb = theme.border
        canvas_box.line.width = Pt(1.0)

        # Top banner
        hdr_box = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(left), Inches(top), Inches(width), Inches(0.42)
        )
        hdr_box.fill.solid()
        hdr_box.fill.fore_color.rgb = theme.surface_highlight
        hdr_box.line.fill.background()
        tf_h = hdr_box.text_frame
        tf_h.margin_left = Inches(0.20)
        tf_h.margin_top = Inches(0.06)
        TypographySystem.apply_to_paragraph(
            tf_h.paragraphs[0], TypographySystem.LABEL,
            f"CLOSED-LOOP CYBER-PHYSICAL ARCHITECTURE: {model.title.upper()}",
            theme.text_accent
        )

        stages = model.stages
        # Divide into top track (Left to Right: Physical -> Digital -> Context)
        # and bottom track (Right to Left: Intelligence -> Decision -> Action -> Return to Physical)
        half = (len(stages) + 1) // 2
        top_stages = stages[:half]
        bottom_stages = stages[half:]

        # Top Track
        top_y = top + 0.60
        stage_h = 1.35
        top_cols = GridCalculator.get_columns(len(top_stages), left=left + 0.35, total_width=width - 0.70, gap=0.35)

        for i, stg in enumerate(top_stages):
            cx, cw = top_cols[i]
            cls._render_closed_loop_card(slide, cx, top_y, cw, stage_h, stg, theme)

            # Connector arrow right
            if i < len(top_stages) - 1:
                arr_x = cx + cw + 0.05
                arr_w = 0.25
                cls._render_directional_arrow(slide, arr_x, top_y + stage_h/2 - 0.12, arr_w, 0.24, "right", theme)

        # Downward connector from last top stage to right bottom stage
        last_top_cx, last_top_cw = top_cols[-1]
        down_x = last_top_cx + last_top_cw / 2 - 0.12
        down_y = top_y + stage_h + 0.05
        down_h = height - (stage_h * 2) - 1.25
        cls._render_directional_arrow(slide, down_x, down_y, 0.24, max(down_h, 0.40), "down", theme, fill_color=theme.border_accent)

        # Bottom Track (Rendered right-to-left)
        bottom_y = top + height - stage_h - 0.45
        bottom_cols = GridCalculator.get_columns(len(bottom_stages), left=left + 0.35, total_width=width - 0.70, gap=0.35)
        # Reverse order so bottom flows from right to left
        rev_bottom_cols = list(reversed(bottom_cols))

        for j, stg in enumerate(bottom_stages):
            cx, cw = rev_bottom_cols[j]
            cls._render_closed_loop_card(slide, cx, bottom_y, cw, stage_h, stg, theme, is_feedback=(j == len(bottom_stages) - 1))

            # Connector arrow left
            if j < len(bottom_stages) - 1:
                arr_x = cx - 0.30
                arr_w = 0.25
                cls._render_directional_arrow(slide, arr_x, bottom_y + stage_h/2 - 0.12, arr_w, 0.24, "left", theme)

        # Upward Feedback Loop from first bottom stage back to Physical World
        first_bot_cx, first_bot_cw = rev_bottom_cols[-1]
        first_top_cx, first_top_cw = top_cols[0]
        up_x = first_bot_cx + first_bot_cw / 2 - 0.12
        up_y = top_y + stage_h + 0.05
        cls._render_directional_arrow(slide, up_x, up_y, 0.24, max(down_h, 0.40), "up", theme, fill_color=theme.status_success)

        # Central Loop Summary Callout
        mid_y = top_y + stage_h + 0.10
        mid_h = max(down_h - 0.10, 0.50)
        mid_box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left + 2.8), Inches(mid_y), Inches(width - 5.6), Inches(mid_h)
        )
        mid_box.fill.solid()
        mid_box.fill.fore_color.rgb = theme.surface_highlight
        mid_box.line.color.rgb = theme.border_accent
        tf_m = mid_box.text_frame
        tf_m.word_wrap = True
        TypographySystem.apply_to_paragraph(
            tf_m.paragraphs[0], TypographySystem.LABEL,
            "AUTONOMOUS FEEDBACK CONTROL LOOP",
            theme.border_accent
        )
        p_ms = tf_m.add_paragraph()
        TypographySystem.apply_to_paragraph(
            p_ms, TypographySystem.BODY,
            model.loop_closed_summary,
            theme.text_primary
        )

    # =========================================================================
    # Helpers & Primitive Renderers
    # =========================================================================

    @classmethod
    def _render_process_step_node(
        cls,
        slide,
        x: float,
        y: float,
        w: float,
        h: float,
        step_num: int,
        node: ProcessNode,
        theme: Theme,
        is_terminal: bool = False,
        custom_badge: Optional[str] = None,
        is_warning: bool = False,
        is_info: bool = False
    ):
        """Renders a single process step with system badge, role lane, and poka-yoke rule."""
        border_col = theme.border
        if is_terminal:
            border_col = theme.status_success
        elif is_warning:
            border_col = theme.status_critical
        elif is_info:
            border_col = theme.status_info

        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(h)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = theme.surface_alt if (is_warning or is_info) else theme.surface
        box.line.color.rgb = border_col
        box.line.width = Pt(1.2 if (is_terminal or is_warning) else 1.0)

        # Header Pill
        pill_h = 0.28
        pill = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(pill_h)
        )
        pill.fill.solid()
        pill.fill.fore_color.rgb = theme.surface_highlight
        pill.line.fill.background()
        tf_p = pill.text_frame
        tf_p.margin_left = Inches(0.08)
        tf_p.margin_top = Inches(0.04)
        tag_text = custom_badge or f"STEP {step_num}: {node.role_lane.upper()}"
        TypographySystem.apply_to_paragraph(
            tf_p.paragraphs[0], TypographySystem.ANNOTATION,
            tag_text,
            theme.text_accent
        )

        # Text Frame Body
        tb = slide.shapes.add_textbox(
            Inches(x + 0.08), Inches(y + pill_h + 0.04), Inches(w - 0.16), Inches(h - pill_h - 0.08)
        )
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Title
        p_title = tf.paragraphs[0]
        TypographySystem.apply_to_paragraph(
            p_title, TypographySystem.BODY_STRONG,
            node.label,
            theme.text_primary
        )
        p_title.space_after = Pt(2)

        # System Tag / Subtitle
        if node.system_tag:
            p_sys = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(
                p_sys, TypographySystem.CAPTION,
                f"[{node.system_tag}]",
                theme.border_accent
            )
            p_sys.space_after = Pt(2)

        # Action Detail
        if node.action_detail:
            p_act = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(
                p_act, TypographySystem.ANNOTATION,
                node.action_detail,
                theme.text_muted
            )

        # Poka-Yoke / Interlock
        if node.poka_yoke:
            p_py = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(
                p_py, TypographySystem.ANNOTATION,
                f"LOCK: {node.poka_yoke}",
                theme.status_warning
            )

    @classmethod
    def _render_decision_diamond(
        cls,
        slide,
        x: float,
        y: float,
        w: float,
        h: float,
        node: ProcessNode,
        theme: Theme
    ):
        """Renders an authentic MSO_SHAPE.DIAMOND for quality or control decision points."""
        diamond = slide.shapes.add_shape(
            MSO_SHAPE.DIAMOND,
            Inches(x), Inches(y), Inches(w), Inches(h)
        )
        diamond.fill.solid()
        diamond.fill.fore_color.rgb = theme.surface_highlight
        diamond.line.color.rgb = theme.border_accent
        diamond.line.width = Pt(1.5)

        tf = diamond.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.04)
        tf.margin_right = Inches(0.04)
        tf.margin_top = Inches(0.06)
        tf.margin_bottom = Inches(0.06)

        p1 = tf.paragraphs[0]
        p1.alignment = PP_ALIGN.CENTER
        TypographySystem.apply_to_paragraph(
            p1, TypographySystem.ANNOTATION,
            "GATE",
            theme.border_accent
        )
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        # Format concise label for diamond layout
        clean_label = node.label.replace(" & ", "\n& ") if len(node.label) > 16 else node.label
        TypographySystem.apply_to_paragraph(
            p2, TypographySystem.LABEL,
            clean_label,
            theme.text_primary
        )

    @classmethod
    def _render_condition_badge(
        cls,
        slide,
        x: float,
        y: float,
        w: float,
        h: float,
        text: str,
        color: RGBColor
    ):
        """Renders a small pill label over branch connectors."""
        badge = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(h)
        )
        badge.fill.solid()
        badge.fill.fore_color.rgb = color
        badge.line.fill.background()
        tf = badge.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        TypographySystem.apply_to_paragraph(
            p, TypographySystem.ANNOTATION,
            text,
            RGBColor(255, 255, 255)
        )

    @classmethod
    def _render_directional_arrow(
        cls,
        slide,
        x: float,
        y: float,
        w: float,
        h: float,
        direction: str,
        theme: Theme,
        fill_color: Optional[RGBColor] = None
    ):
        """Renders clear, native directional arrows (right, down, left, up)."""
        shape_type = MSO_SHAPE.RIGHT_ARROW
        if direction == "down":
            shape_type = MSO_SHAPE.DOWN_ARROW
        elif direction == "left":
            shape_type = MSO_SHAPE.LEFT_ARROW
        elif direction == "up":
            shape_type = MSO_SHAPE.UP_ARROW

        arr = slide.shapes.add_shape(
            shape_type,
            Inches(x), Inches(y), Inches(w), Inches(h)
        )
        arr.fill.solid()
        arr.fill.fore_color.rgb = fill_color or theme.border_accent
        arr.line.fill.background()

    @classmethod
    def _render_closed_loop_card(
        cls,
        slide,
        x: float,
        y: float,
        w: float,
        h: float,
        stage: Any,
        theme: Theme,
        is_feedback: bool = False
    ):
        """Renders a stage in the circular closed loop."""
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(h)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = theme.surface_highlight if is_feedback else theme.surface
        box.line.color.rgb = theme.status_success if is_feedback else theme.border
        box.line.width = Pt(1.2 if is_feedback else 1.0)

        # Header band
        pill = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(0.28)
        )
        pill.fill.solid()
        pill.fill.fore_color.rgb = theme.surface_alt
        pill.line.fill.background()
        tf_p = pill.text_frame
        tf_p.margin_left = Inches(0.08)
        tf_p.margin_top = Inches(0.04)
        TypographySystem.apply_to_paragraph(
            tf_p.paragraphs[0], TypographySystem.LABEL,
            f"STAGE {stage.stage_num}: {stage.stage_name.upper()}",
            theme.text_accent
        )

        tb = slide.shapes.add_textbox(
            Inches(x + 0.08), Inches(y + 0.32), Inches(w - 0.16), Inches(h - 0.36)
        )
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Subsystems
        if stage.subsystems:
            p_sub = tf.paragraphs[0]
            TypographySystem.apply_to_paragraph(
                p_sub, TypographySystem.BODY_STRONG,
                " • ".join(stage.subsystems[:2]),
                theme.text_primary
            )
            p_sub.space_after = Pt(2)

        # Data artifacts
        if stage.data_artifacts:
            p_art = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(
                p_art, TypographySystem.CAPTION,
                f"Data: {', '.join(stage.data_artifacts[:2])}",
                theme.text_muted
            )

        # Feedback signal
        if stage.feedback_signal:
            p_fb = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(
                p_fb, TypographySystem.ANNOTATION,
                f"Signal: {stage.feedback_signal}",
                theme.status_success
            )
