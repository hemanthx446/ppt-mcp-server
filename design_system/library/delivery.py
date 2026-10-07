"""
Delivery & Execution Visual Primitives (Primitives 42–46).

Native, editable PowerPoint diagrams for agile rollouts, transformation roadmaps,
chronological timelines, milestone control gates, and parallel workstream tracks.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE

from ..typography import TypographySystem
from ..spacing import Margins, SpacingScale, GridCalculator
from ..color import Theme
from ..primitives import SurfacePrimitive, ConnectorPrimitive


class TransformationRoadmapPrimitive:
    """42. Transformation Roadmap (Phases over time with workstreams, deliverables, and pass gates)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               phases: List[Tuple[str, str, str, List[str], Optional[str]]], # [(phase_id, duration, title, deliverables, gate)]
               theme: Theme):
        cols = GridCalculator.get_columns(len(phases), left=left, total_width=width, gap=0.25)
        for i, (p_id, dur, title, deliverables, gate) in enumerate(phases):
            cx, cw = cols[i]
            SurfacePrimitive.render(slide, cx, top, cw, height, theme)

            # Phase Pill Tag
            ptag = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(top), Inches(cw), Inches(0.40))
            ptag.fill.solid()
            ptag.fill.fore_color.rgb = theme.surface_highlight
            ptag.line.color.rgb = theme.border
            tf_p = ptag.text_frame
            tf_p.margin_left = Inches(0.12)
            TypographySystem.apply_to_paragraph(tf_p.paragraphs[0], TypographySystem.LABEL, f"{p_id} • {dur.upper()}", theme.text_accent)

            tb = slide.shapes.add_textbox(Inches(cx + 0.16), Inches(top + 0.48), Inches(cw - 0.32), Inches(height - 0.58))
            tf = tb.text_frame
            tf.word_wrap = True
            p_t = tf.paragraphs[0]
            TypographySystem.apply_to_paragraph(p_t, TypographySystem.BODY_STRONG, title, theme.text_primary)
            p_t.space_after = Pt(10)

            for deliv in deliverables[:3]:
                p_d = tf.add_paragraph()
                p_d.space_after = Pt(6)
                TypographySystem.apply_to_paragraph(p_d, TypographySystem.BODY, f"•  {deliv}", theme.text_muted)

            if gate:
                p_g = tf.add_paragraph()
                p_g.space_after = Pt(4)
                TypographySystem.apply_to_paragraph(p_g, TypographySystem.ANNOTATION, f"GATE: {gate}", theme.status_success)


class TimelinePrimitive:
    """43. Chronological timeline track with date markers and deliverable flags."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               milestones: List[Tuple[str, str, str]], # [(date_label, milestone_title, summary)]
               theme: Theme):
        SurfacePrimitive.render(slide, left, top, width, height, theme)

        # Center timeline rail
        rail_y = top + height / 2.0
        rail = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left + 0.4), Inches(rail_y - 0.02), Inches(width - 0.8), Inches(0.04))
        rail.fill.solid()
        rail.fill.fore_color.rgb = theme.border_accent
        rail.line.fill.background()

        cols = GridCalculator.get_columns(len(milestones), left=left + 0.4, total_width=width - 0.8, gap=0.20)
        for i, (date_lbl, m_title, summary) in enumerate(milestones):
            cx, cw = cols[i]
            # Marker node
            node = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx + cw/2 - 0.12), Inches(rail_y - 0.12), Inches(0.24), Inches(0.24))
            node.fill.solid()
            node.fill.fore_color.rgb = theme.border_accent
            node.line.fill.background()

            # Date box above or below rail alternately
            is_above = (i % 2 == 0)
            t_y = top + 0.30 if is_above else rail_y + 0.25
            tb = slide.shapes.add_textbox(Inches(cx), Inches(t_y), Inches(cw), Inches(height/2 - 0.5))
            tf = tb.text_frame
            tf.word_wrap = True
            TypographySystem.apply_to_paragraph(tf.paragraphs[0], TypographySystem.LABEL, date_lbl, theme.text_accent)
            p_t = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_t, TypographySystem.BODY_STRONG, m_title, theme.text_primary)
            TypographySystem.apply_to_paragraph(tf.add_paragraph(), TypographySystem.CAPTION, summary, theme.text_muted)


class MilestoneGatesPrimitive:
    """44. Milestone Control Gates (Gate 1 -> Gate 2 -> Gate 3 with exit pass criteria)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               gates: List[Tuple[str, str, List[str], str]], # [(gate_num, gate_title, checklist, owner)]
               theme: Theme):
        cols = GridCalculator.get_columns(len(gates), left=left, total_width=width, gap=0.35)
        for i, (g_num, g_title, checklist, owner) in enumerate(gates):
            cx, cw = cols[i]
            SurfacePrimitive.render(slide, cx, top, cw, height, theme, border_color=theme.status_success)

            tb = slide.shapes.add_textbox(Inches(cx + 0.16), Inches(top + 0.16), Inches(cw - 0.32), Inches(height - 0.32))
            tf = tb.text_frame
            tf.word_wrap = True
            TypographySystem.apply_to_paragraph(tf.paragraphs[0], TypographySystem.LABEL, f"GATE 0{g_num}", theme.status_success)
            p_t = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_t, TypographySystem.BODY_STRONG, g_title, theme.text_primary)
            p_t.space_after = Pt(10)

            for chk in checklist[:4]:
                p_c = tf.add_paragraph()
                p_c.space_after = Pt(4)
                TypographySystem.apply_to_paragraph(p_c, TypographySystem.BODY, f"[✓] {chk}", theme.text_muted)

            p_own = tf.add_paragraph()
            p_own.space_after = Pt(4)
            TypographySystem.apply_to_paragraph(p_own, TypographySystem.ANNOTATION, f"OWNER: {owner}", theme.text_accent)

            if i < len(gates) - 1:
                ConnectorPrimitive.render_arrow(slide, cx + cw + 0.05, top + height/2 - 0.12, 0.25, 0.24, "right", theme)


class ReleasePlanPrimitive:
    """45. Multi-Release cadence schedule (Release 1.0, 2.0, 3.0 across quarters)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               releases: List[Tuple[str, str, List[str]]], # [(release_id, target_quarter, features)]
               theme: Theme):
        cols = GridCalculator.get_columns(len(releases), left=left, total_width=width, gap=0.25)
        for i, (rel_id, qtr, feats) in enumerate(releases):
            cx, cw = cols[i]
            SurfacePrimitive.render(slide, cx, top, cw, height, theme)

            hb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(top), Inches(cw), Inches(0.42))
            hb.fill.solid()
            hb.fill.fore_color.rgb = theme.surface_highlight
            hb.line.color.rgb = theme.border
            tf_h = hb.text_frame
            TypographySystem.apply_to_paragraph(tf_h.paragraphs[0], TypographySystem.LABEL, f"{rel_id} ({qtr})", theme.text_accent)

            tb = slide.shapes.add_textbox(Inches(cx + 0.16), Inches(top + 0.50), Inches(cw - 0.32), Inches(height - 0.60))
            tf = tb.text_frame
            tf.word_wrap = True
            for f in feats[:5]:
                p = tf.add_paragraph()
                p.space_after = Pt(6)
                TypographySystem.apply_to_paragraph(p, TypographySystem.BODY, f"•  {f}", theme.text_primary)


class WorkstreamViewPrimitive:
    """46. Parallel Workstream Tracks (Architecture, Core Build, Integration, Change Enablement)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               workstreams: List[Tuple[str, str, List[Tuple[float, float, str]]]], # [(ws_name, lead, [(start_pct, width_pct, task)])]
               theme: Theme):
        rows = GridCalculator.get_rows(len(workstreams), top=top, total_height=height, gap=0.15)
        for i, (ws_name, lead, bars) in enumerate(workstreams):
            ry, rh = rows[i]
            SurfacePrimitive.render(slide, left, ry, width, rh, theme)

            # Left Workstream Label
            l_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(ry), Inches(2.2), Inches(rh))
            l_box.fill.solid()
            l_box.fill.fore_color.rgb = theme.surface_highlight
            l_box.line.color.rgb = theme.border
            tf_l = l_box.text_frame
            TypographySystem.apply_to_paragraph(tf_l.paragraphs[0], TypographySystem.LABEL, ws_name, theme.text_accent)
            TypographySystem.apply_to_paragraph(tf_l.add_paragraph(), TypographySystem.CAPTION, f"Lead: {lead}", theme.text_muted)

            # Schedule bars
            track_w = width - 2.5
            for start_p, width_p, task_lbl in bars:
                bx = left + 2.3 + (start_p * track_w)
                bw = width_p * track_w
                bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(bx), Inches(ry + 0.12), Inches(bw), Inches(rh - 0.24))
                bar.fill.solid()
                bar.fill.fore_color.rgb = theme.border_accent
                bar.line.fill.background()
                tf_b = bar.text_frame
                TypographySystem.apply_to_paragraph(tf_b.paragraphs[0], TypographySystem.CAPTION, task_lbl, theme.text_primary)
