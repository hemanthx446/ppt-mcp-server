"""
Process & Workflow Visual Primitives (Primitives 10–16).

Native, editable PowerPoint diagrams for business processes, manufacturing
workstation journeys, swimlanes, and exception/rework loops.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE

from ..typography import TypographySystem
from ..spacing import Margins, SpacingScale, GridCalculator
from ..color import Theme
from ..primitives import SurfacePrimitive, ConnectorPrimitive


class HorizontalProcessFlowPrimitive:
    """10. Horizontal sequential process flow with connecting arrows."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               steps: List[Tuple[str, str, List[str]]], # [(step_num, title, details)]
               theme: Theme):
        count = len(steps)
        cols = GridCalculator.get_columns(count, left=left, total_width=width, gap=0.35)

        for i, (num, title, details) in enumerate(steps):
            cx, cw = cols[i]
            SurfacePrimitive.render(slide, cx, top, cw, height, theme)

            # Header Step Tag
            tag = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(top), Inches(cw), Inches(0.36))
            tag.fill.solid()
            tag.fill.fore_color.rgb = theme.surface_highlight
            tag.line.color.rgb = theme.border
            tf_t = tag.text_frame
            tf_t.margin_left = Inches(0.12)
            p_t = tf_t.paragraphs[0]
            TypographySystem.apply_to_paragraph(p_t, TypographySystem.LABEL, f"STEP {num}", theme.text_accent)

            tb = slide.shapes.add_textbox(Inches(cx + 0.14), Inches(top + 0.44), Inches(cw - 0.28), Inches(height - 0.52))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = 0
            p_head = tf.paragraphs[0]
            TypographySystem.apply_to_paragraph(p_head, TypographySystem.BODY_STRONG, title, theme.text_primary)
            p_head.space_after = Pt(8)

            for d in details[:3]:
                p_d = tf.add_paragraph()
                p_d.space_after = Pt(4)
                TypographySystem.apply_to_paragraph(p_d, TypographySystem.BODY, f"•  {d}", theme.text_muted)

            if i < count - 1:
                ConnectorPrimitive.render_arrow(slide, cx + cw + 0.05, top + height/2 - 0.12, 0.25, 0.24, "right", theme)


class VerticalProcessFlowPrimitive:
    """11. Vertical cascading process flow with sequential phase checkpoints."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               stages: List[Tuple[str, str, str]], # [(phase_num, title, description)]
               theme: Theme):
        rows = GridCalculator.get_rows(len(stages), top=top, total_height=height, gap=0.18)
        for i, (p_num, title, desc) in enumerate(stages):
            ry, rh = rows[i]
            SurfacePrimitive.render(slide, left, ry, width, rh, theme)

            # Left number badge
            b_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(ry), Inches(1.2), Inches(rh))
            b_box.fill.solid()
            b_box.fill.fore_color.rgb = theme.surface_highlight
            b_box.line.color.rgb = theme.border
            tf_b = b_box.text_frame
            p_b = tf_b.paragraphs[0]
            TypographySystem.apply_to_paragraph(p_b, TypographySystem.LABEL, f"PHASE {p_num}", theme.text_accent)

            # Right content
            tb = slide.shapes.add_textbox(Inches(left + 1.35), Inches(ry + 0.08), Inches(width - 1.5), Inches(rh - 0.16))
            tf = tb.text_frame
            tf.word_wrap = True
            p1 = tf.paragraphs[0]
            TypographySystem.apply_to_paragraph(p1, TypographySystem.BODY_STRONG, title, theme.text_primary)
            p2 = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p2, TypographySystem.BODY, desc, theme.text_muted)


class ValueStreamPrimitive:
    """12. End-to-end Value Stream Map (Inbound -> WIP Assembly -> Inspection -> Dispatch) with Lead Times."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               stream_nodes: List[Tuple[str, str, str, str]], # [(stage, lead_time, value_add, cycle_time)]
               theme: Theme):
        cols = GridCalculator.get_columns(len(stream_nodes), left=left, total_width=width, gap=0.25)
        for i, (stage, lt, va, ct) in enumerate(stream_nodes):
            cx, cw = cols[i]
            SurfacePrimitive.render(slide, cx, top, cw, height - 0.70, theme)

            tb = slide.shapes.add_textbox(Inches(cx + 0.12), Inches(top + 0.12), Inches(cw - 0.24), Inches(height - 0.94))
            tf = tb.text_frame
            tf.word_wrap = True
            TypographySystem.apply_to_paragraph(tf.paragraphs[0], TypographySystem.LABEL, stage, theme.text_accent)
            p_va = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_va, TypographySystem.BODY_STRONG, f"Activity: {va}", theme.text_primary)
            p_va.space_after = Pt(6)
            p_ct = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_ct, TypographySystem.CAPTION, f"Cycle Time: {ct}", theme.text_muted)

            # Bottom lead-time pill
            lt_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(top + height - 0.60), Inches(cw), Inches(0.50))
            lt_box.fill.solid()
            lt_box.fill.fore_color.rgb = theme.surface_highlight
            lt_box.line.color.rgb = theme.border
            tf_lt = lt_box.text_frame
            TypographySystem.apply_to_paragraph(tf_lt.paragraphs[0], TypographySystem.ANNOTATION, f"LEAD TIME: {lt}", theme.status_info)


class OperationalWorkflowPrimitive:
    """13. Workstation operational flow with Poka-Yoke error-proofing checks."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               stations: List[Tuple[str, str, str, Optional[str]]], # [(station_num, name, action, poka_yoke)]
               theme: Theme):
        cols = GridCalculator.get_columns(len(stations), left=left, total_width=width, gap=0.30)
        for i, (s_num, s_name, s_action, py_rule) in enumerate(stations):
            cx, cw = cols[i]
            SurfacePrimitive.render(slide, cx, top, cw, height, theme)

            tb = slide.shapes.add_textbox(Inches(cx + 0.14), Inches(top + 0.14), Inches(cw - 0.28), Inches(height - 0.28))
            tf = tb.text_frame
            tf.word_wrap = True
            TypographySystem.apply_to_paragraph(tf.paragraphs[0], TypographySystem.LABEL, f"STATION {s_num}", theme.text_accent)

            p_nm = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_nm, TypographySystem.BODY_STRONG, s_name, theme.text_primary)
            p_nm.space_after = Pt(6)

            p_act = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_act, TypographySystem.BODY, s_action, theme.text_muted)
            p_act.space_after = Pt(10)

            if py_rule:
                p_py = tf.add_paragraph()
                TypographySystem.apply_to_paragraph(p_py, TypographySystem.ANNOTATION, f"POKA-YOKE: {py_rule}", theme.status_warning)

            if i < len(stations) - 1:
                ConnectorPrimitive.render_arrow(slide, cx + cw + 0.05, top + height/2 - 0.12, 0.20, 0.24, "right", theme)


class SwimlaneProcessPrimitive:
    """14. Cross-functional Swimlane process (Operator / Middleware / ERP Core)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               lanes: List[Tuple[str, List[Tuple[float, str]]]], # [(lane_actor, [(relative_x, task_name)])]
               theme: Theme):
        rows = GridCalculator.get_rows(len(lanes), top=top, total_height=height, gap=0.15)
        for i, (actor, tasks) in enumerate(lanes):
            ry, rh = rows[i]
            # Lane container
            SurfacePrimitive.render(slide, left, ry, width, rh, theme, fill_color=theme.surface_alt if i % 2 == 1 else theme.surface)

            # Actor header on left
            abox = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(ry), Inches(2.2), Inches(rh))
            abox.fill.solid()
            abox.fill.fore_color.rgb = theme.surface_highlight
            abox.line.color.rgb = theme.border
            tf_a = abox.text_frame
            TypographySystem.apply_to_paragraph(tf_a.paragraphs[0], TypographySystem.LABEL, actor, theme.text_accent)

            # Render tasks inside lane
            for rel_x, task_text in tasks:
                t_x = left + 2.4 + (rel_x * (width - 4.5))
                t_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(t_x), Inches(ry + 0.10), Inches(1.8), Inches(rh - 0.20))
                t_box.fill.solid()
                t_box.fill.fore_color.rgb = theme.surface
                t_box.line.color.rgb = theme.border_accent
                tf_t = t_box.text_frame
                tf_t.word_wrap = True
                TypographySystem.apply_to_paragraph(tf_t.paragraphs[0], TypographySystem.CAPTION, task_text, theme.text_primary)


class DecisionFlowPrimitive:
    """15. Decision flow with condition fork and conditional routing."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               init_step: str, condition: str,
               pass_path: Tuple[str, str], # (label, action)
               fail_path: Tuple[str, str],
               theme: Theme):
        # 3 horizontal columns
        cols = GridCalculator.get_columns(3, left=left, total_width=width, gap=0.50)

        # 1. Trigger
        SurfacePrimitive.render(slide, cols[0][0], top + height/2 - 0.6, cols[0][1], 1.2, theme)
        tb_i = slide.shapes.add_textbox(Inches(cols[0][0] + 0.1), Inches(top + height/2 - 0.5), Inches(cols[0][1] - 0.2), Inches(1.0))
        tf_i = tb_i.text_frame
        TypographySystem.apply_to_paragraph(tf_i.paragraphs[0], TypographySystem.LABEL, "TRIGGER STEP", theme.text_accent)
        p_it = tf_i.add_paragraph()
        TypographySystem.apply_to_paragraph(p_it, TypographySystem.BODY, init_step, theme.text_primary)

        # Arrow
        ConnectorPrimitive.render_arrow(slide, cols[0][0] + cols[0][1] + 0.05, top + height/2 - 0.12, 0.40, 0.24, "right", theme)

        # 2. Condition Diamond Container
        SurfacePrimitive.render(slide, cols[1][0], top + height/2 - 0.7, cols[1][1], 1.4, theme, border_color=theme.border_accent)
        tb_c = slide.shapes.add_textbox(Inches(cols[1][0] + 0.1), Inches(top + height/2 - 0.6), Inches(cols[1][1] - 0.2), Inches(1.2))
        tf_c = tb_c.text_frame
        TypographySystem.apply_to_paragraph(tf_c.paragraphs[0], TypographySystem.LABEL, "DECISION GATE", theme.border_accent)
        p_ct = tf_c.add_paragraph()
        TypographySystem.apply_to_paragraph(p_ct, TypographySystem.BODY_STRONG, condition, theme.text_primary)

        # 3. Branch Paths (Pass Top, Fail Bottom)
        # Pass
        pass_y = top + 0.2
        SurfacePrimitive.render(slide, cols[2][0], pass_y, cols[2][1], 1.0, theme, border_color=theme.status_success)
        tb_p = slide.shapes.add_textbox(Inches(cols[2][0] + 0.1), Inches(pass_y + 0.08), Inches(cols[2][1] - 0.2), Inches(0.84))
        tf_p = tb_p.text_frame
        TypographySystem.apply_to_paragraph(tf_p.paragraphs[0], TypographySystem.LABEL, f"PASS: {pass_path[0]}", theme.status_success)
        TypographySystem.apply_to_paragraph(tf_p.add_paragraph(), TypographySystem.CAPTION, pass_path[1], theme.text_primary)

        # Fail
        fail_y = top + height - 1.2
        SurfacePrimitive.render(slide, cols[2][0], fail_y, cols[2][1], 1.0, theme, border_color=theme.status_critical)
        tb_f = slide.shapes.add_textbox(Inches(cols[2][0] + 0.1), Inches(fail_y + 0.08), Inches(cols[2][1] - 0.2), Inches(0.84))
        tf_f = tb_f.text_frame
        TypographySystem.apply_to_paragraph(tf_f.paragraphs[0], TypographySystem.LABEL, f"REJECT: {fail_path[0]}", theme.status_critical)
        TypographySystem.apply_to_paragraph(tf_f.add_paragraph(), TypographySystem.CAPTION, fail_path[1], theme.text_primary)


class ExceptionReworkFlowPrimitive:
    """16. Happy Path with NCR exception logging and rework loop."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               standard_steps: List[str],
               exception_trigger: str,
               rework_steps: List[str],
               theme: Theme):
        # Top 60%: Standard Happy Path Flow
        happy_h = height * 0.52
        HorizontalProcessFlowPrimitive.render(
            slide, left, top, width, happy_h,
            [(str(i+1), s, ["Standard production routing"]) for i, s in enumerate(standard_steps)],
            theme
        )

        # Bottom 40%: Exception & Rework Loop
        rework_y = top + happy_h + 0.25
        rework_h = height - happy_h - 0.25
        SurfacePrimitive.render(slide, left, rework_y, width, rework_h, theme, fill_color=theme.surface_alt, border_color=theme.status_warning)

        tb = slide.shapes.add_textbox(Inches(left + 0.20), Inches(rework_y + 0.12), Inches(width - 0.40), Inches(rework_h - 0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        TypographySystem.apply_to_paragraph(tf.paragraphs[0], TypographySystem.LABEL, f"EXCEPTION LOOP: {exception_trigger}", theme.status_warning)
        p_rw = tf.add_paragraph()
        TypographySystem.apply_to_paragraph(p_rw, TypographySystem.BODY, "  ->  ".join(rework_steps), theme.text_primary)
