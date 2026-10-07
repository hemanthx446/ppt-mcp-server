"""
Business & Strategy Visual Primitives (Primitives 35–41).

Native, editable PowerPoint diagrams for capability maps, operating models,
outcome chains, value driver trees, decision matrices, maturity models, and as-is/to-be.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE

from ..typography import TypographySystem
from ..spacing import Margins, SpacingScale, GridCalculator
from ..color import Theme
from ..primitives import SurfacePrimitive, ConnectorPrimitive


class CapabilityMapPrimitive:
    """35. Capability Map (Functional Domains broken into core business capabilities)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               domains: List[Tuple[str, List[str]]], # [(domain_name, [capabilities])]
               theme: Theme):
        cols = GridCalculator.get_columns(len(domains), left=left, total_width=width, gap=0.22)
        for i, (d_name, caps) in enumerate(domains):
            cx, cw = cols[i]
            SurfacePrimitive.render(slide, cx, top, cw, height, theme)

            # Domain Header
            h_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(top), Inches(cw), Inches(0.44))
            h_box.fill.solid()
            h_box.fill.fore_color.rgb = theme.surface_highlight
            h_box.line.color.rgb = theme.border
            tf_h = h_box.text_frame
            TypographySystem.apply_to_paragraph(tf_h.paragraphs[0], TypographySystem.LABEL, d_name, theme.text_accent)

            # Capability Boxes
            cap_y = top + 0.54
            box_h = (height - 0.70) / max(len(caps[:5]), 1) - 0.08
            for c_title in caps[:5]:
                cb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx + 0.10), Inches(cap_y), Inches(cw - 0.20), Inches(box_h))
                cb.fill.solid()
                cb.fill.fore_color.rgb = theme.surface_alt
                cb.line.color.rgb = theme.border
                tf_c = cb.text_frame
                tf_c.word_wrap = True
                TypographySystem.apply_to_paragraph(tf_c.paragraphs[0], TypographySystem.BODY, c_title, theme.text_primary)
                cap_y += box_h + 0.08


class OperatingModelPrimitive:
    """36. Operating Model 4-Quadrant Framework (People, Process, Technology, Governance)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               quadrants: List[Tuple[str, List[str]]], # exactly 4 quadrants
               theme: Theme):
        qw = (width - 0.25) / 2.0
        qh = (height - 0.25) / 2.0
        positions = [
            (left, top),                  # Top-Left: People
            (left + qw + 0.25, top),      # Top-Right: Process
            (left, top + qh + 0.25),      # Bottom-Left: Technology
            (left + qw + 0.25, top + qh + 0.25) # Bottom-Right: Governance
        ]
        for i, (title, points) in enumerate(quadrants[:4]):
            qx, qy = positions[i]
            SurfacePrimitive.render(slide, qx, qy, qw, qh, theme)

            tb = slide.shapes.add_textbox(Inches(qx + 0.16), Inches(qy + 0.14), Inches(qw - 0.32), Inches(qh - 0.28))
            tf = tb.text_frame
            tf.word_wrap = True
            TypographySystem.apply_to_paragraph(tf.paragraphs[0], TypographySystem.LABEL, title, theme.text_accent)
            for p in points[:3]:
                p_it = tf.add_paragraph()
                p_it.space_after = Pt(4)
                TypographySystem.apply_to_paragraph(p_it, TypographySystem.BODY, f"•  {p}", theme.text_muted)


class OutcomeChainPrimitive:
    """37. Outcome Chain (Strategic Objective -> Operational Lever -> Enabler -> Financial Outcome)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               chain_steps: List[Tuple[str, str, str]], # [(stage_name, core_action, measurable_result)]
               theme: Theme):
        cols = GridCalculator.get_columns(len(chain_steps), left=left, total_width=width, gap=0.35)
        for i, (stage, action, result) in enumerate(chain_steps):
            cx, cw = cols[i]
            border_c = theme.status_success if i == len(chain_steps) - 1 else theme.border
            SurfacePrimitive.render(slide, cx, top, cw, height, theme, border_color=border_c)

            tb = slide.shapes.add_textbox(Inches(cx + 0.14), Inches(top + 0.14), Inches(cw - 0.28), Inches(height - 0.28))
            tf = tb.text_frame
            tf.word_wrap = True
            TypographySystem.apply_to_paragraph(tf.paragraphs[0], TypographySystem.LABEL, stage, theme.text_accent)
            p_a = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_a, TypographySystem.BODY_STRONG, action, theme.text_primary)
            p_a.space_after = Pt(8)
            p_r = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_r, TypographySystem.ANNOTATION, f"OUTCOME: {result}", border_c)

            if i < len(chain_steps) - 1:
                ConnectorPrimitive.render_arrow(slide, cx + cw + 0.05, top + height/2 - 0.12, 0.25, 0.24, "right", theme)


class ValueDriverTreePrimitive:
    """38. Value Driver Tree (EBITDA -> Revenue, Margin, Working Capital Levers)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               root_metric: str,
               level1_branches: List[Tuple[str, List[str]]], # [(branch_name, [sub_levers])]
               theme: Theme):
        # 30% Left (Root EBITDA) + 70% Right (Branches)
        (lx, lw), (rx, rw) = GridCalculator.get_split(left_ratio=0.30, left=left, total_width=width, gap=0.35)

        # Root Box
        SurfacePrimitive.render(slide, lx, top + height/2 - 0.8, lw, 1.6, theme, border_color=theme.status_success)
        tb_r = slide.shapes.add_textbox(Inches(lx + 0.15), Inches(top + height/2 - 0.65), Inches(lw - 0.3), Inches(1.3))
        tf_r = tb_r.text_frame
        TypographySystem.apply_to_paragraph(tf_r.paragraphs[0], TypographySystem.LABEL, "ENTERPRISE VALUE GOAL", theme.status_success)
        TypographySystem.apply_to_paragraph(tf_r.add_paragraph(), TypographySystem.KPI_NUMBER, root_metric, theme.text_primary)

        # Connector
        ConnectorPrimitive.render_arrow(slide, lx + lw + 0.05, top + height/2 - 0.15, 0.25, 0.28, "right", theme)

        # Branches
        rows = GridCalculator.get_rows(len(level1_branches), top=top, total_height=height, gap=0.15)
        for i, (b_title, sub_levers) in enumerate(level1_branches):
            by, bh = rows[i]
            SurfacePrimitive.render(slide, rx, by, rw, bh, theme)
            tb = slide.shapes.add_textbox(Inches(rx + 0.16), Inches(by + 0.10), Inches(rw - 0.32), Inches(bh - 0.20))
            tf = tb.text_frame
            TypographySystem.apply_to_paragraph(tf.paragraphs[0], TypographySystem.LABEL, b_title, theme.text_accent)
            p_subs = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_subs, TypographySystem.BODY, " • ".join(sub_levers[:3]), theme.text_primary)


class DecisionMatrixPrimitive:
    """39. Decision Matrix (Comparing multiple options against weighted criteria)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               criteria: List[Tuple[str, float]], # [(criterion_name, weight)]
               options: List[Tuple[str, List[int]]], # [(option_name, scores_1_to_5)]
               theme: Theme):
        # Rendered as an enterprise scoring matrix table
        headers = ["EVALUATION CRITERIA", "WEIGHT"] + [opt[0] for opt in options]
        rows = []
        for c_idx, (c_name, weight) in enumerate(criteria):
            row = [c_name, f"{weight:.0%}"]
            for opt_name, scores in options:
                s = scores[c_idx] if c_idx < len(scores) else 3
                row.append(f"{s}/5 ({s*weight:.1f})")
            rows.append(row)

        from ..primitives import TablePrimitive
        TablePrimitive.render(slide, left, top, width, height, headers, rows, theme)


class MaturityModelPrimitive:
    """40. Maturity Model Staircase (Levels 1–5: Ad-Hoc -> Managed -> Defined -> Measured -> Autonomous)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               levels: List[Tuple[int, str, List[str]]], # [(level_num, title, capabilities)]
               theme: Theme):
        count = len(levels)
        cols = GridCalculator.get_columns(count, left=left, total_width=width, gap=0.15)
        base_h = height / count

        for i, (lvl_num, title, caps) in enumerate(levels):
            cx, cw = cols[i]
            # Staircase height grows with maturity
            stair_h = base_h * (i + 1)
            stair_y = top + height - stair_h

            SurfacePrimitive.render(slide, cx, stair_y, cw, stair_h, theme, fill_color=theme.surface_highlight if i == count - 1 else theme.surface)

            tb = slide.shapes.add_textbox(Inches(cx + 0.10), Inches(stair_y + 0.10), Inches(cw - 0.20), Inches(stair_h - 0.20))
            tf = tb.text_frame
            tf.word_wrap = True
            TypographySystem.apply_to_paragraph(tf.paragraphs[0], TypographySystem.LABEL, f"LEVEL {lvl_num}", theme.text_accent)
            p_t = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_t, TypographySystem.BODY_STRONG, title, theme.text_primary)
            p_t.space_after = Pt(4)
            for c in caps[:2]:
                p_c = tf.add_paragraph()
                TypographySystem.apply_to_paragraph(p_c, TypographySystem.CAPTION, f"• {c}", theme.text_muted)


class CurrentVsFutureStatePrimitive:
    """41. Current vs Future State (As-Is Friction vs To-Be Capabilities)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               as_is_title: str, as_is_points: List[Tuple[str, str]],
               to_be_title: str, to_be_points: List[Tuple[str, str]],
               theme: Theme):
        from ..primitives import TextPrimitive
        (lx, lw), (rx, rw) = GridCalculator.get_split(left_ratio=0.50, left=left, total_width=width, gap=0.30)

        # As-Is Left (Warning / Red Tint)
        SurfacePrimitive.render(slide, lx, top, lw, height, theme, fill_color=theme.surface_alt, border_color=theme.status_warning)
        tb_l = slide.shapes.add_textbox(Inches(lx + 0.20), Inches(top + 0.20), Inches(lw - 0.40), Inches(height - 0.40))
        tf_l = tb_l.text_frame
        TypographySystem.apply_to_paragraph(tf_l.paragraphs[0], TypographySystem.LABEL, as_is_title, theme.status_warning)
        tf_l.paragraphs[0].space_after = Pt(12)
        TextPrimitive.render_lead_in_list(tf_l, as_is_points, theme, max_items=4)

        # To-Be Right (Success / Green Tint)
        SurfacePrimitive.render(slide, rx, top, rw, height, theme, fill_color=theme.surface, border_color=theme.status_success)
        tb_r = slide.shapes.add_textbox(Inches(rx + 0.20), Inches(top + 0.20), Inches(rw - 0.40), Inches(height - 0.40))
        tf_r = tb_r.text_frame
        TypographySystem.apply_to_paragraph(tf_r.paragraphs[0], TypographySystem.LABEL, to_be_title, theme.status_success)
        tf_r.paragraphs[0].space_after = Pt(12)
        TextPrimitive.render_lead_in_list(tf_r, to_be_points, theme, max_items=4)
