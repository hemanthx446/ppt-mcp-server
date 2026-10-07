"""
Narrative & Executive Visual Primitives (Primitives 57–60).

Native, editable PowerPoint layouts for CXO executive statements,
insight + quantitative evidence pairings, strategic key takeaways, and section transition dividers.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

from ..typography import TypographySystem
from ..spacing import Margins, SpacingScale, GridCalculator
from ..color import Theme
from ..primitives import SurfacePrimitive, MetricPrimitive


class ExecutiveStatementPrimitive:
    """57. Executive Statement (High-impact CXO thesis quote block, attribution, and strategic pillars)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               statement: str, # Strategic thesis quote
               attribution: str, # E.g. "Vice President, Global Manufacturing Operations"
               pillars: List[Tuple[str, str]], # [(pillar_title, description)]
               theme: Theme):
        # Background container surface
        SurfacePrimitive.render(slide, left, top, width, height, theme)

        # Left vertical accent line
        acc = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left + 0.35), Inches(top + 0.35), Inches(0.06), Inches(1.8))
        acc.fill.solid()
        acc.fill.fore_color.rgb = theme.border_accent
        acc.line.fill.background()

        # Statement Textbox
        tb = slide.shapes.add_textbox(Inches(left + 0.60), Inches(top + 0.35), Inches(width - 1.0), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p_q = tf.paragraphs[0]
        p_q.space_after = Pt(10)
        TypographySystem.apply_to_paragraph(p_q, TypographySystem.SECTION_TITLE, f'"{statement}"', theme.text_primary)

        p_att = tf.add_paragraph()
        TypographySystem.apply_to_paragraph(p_att, TypographySystem.BODY_STRONG, f"— {attribution}", theme.text_accent)

        # Bottom 3 strategic pillars
        if pillars:
            pill_top = top + 2.4
            pill_h = height - 2.6
            cols = GridCalculator.get_columns(len(pillars), left=left + 0.35, total_width=width - 0.70, gap=0.25)
            for i, (p_title, p_desc) in enumerate(pillars):
                cx, cw = cols[i]
                pbox = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(pill_top), Inches(cw), Inches(pill_h))
                pbox.fill.solid()
                pbox.fill.fore_color.rgb = theme.surface_highlight
                pbox.line.color.rgb = theme.border
                p_tf = pbox.text_frame
                p_tf.word_wrap = True
                p_tf.margin_left = p_tf.margin_top = Inches(0.14)

                p1 = p_tf.paragraphs[0]
                TypographySystem.apply_to_paragraph(p1, TypographySystem.BODY_STRONG, p_title, theme.text_primary)
                p1.space_after = Pt(6)

                p2 = p_tf.add_paragraph()
                TypographySystem.apply_to_paragraph(p2, TypographySystem.BODY, p_desc, theme.text_muted)


class InsightAndEvidencePrimitive:
    """58. Insight + Evidence (Left: Dominant analytical insight; Right: Quantitative proof metrics)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               insight_tag: str, # E.g. "CORE ARCHITECTURAL BOTTLENECK"
               insight_headline: str, # Key takeaway
               insight_narrative: str, # Explanation of mechanics / root cause
               evidence_points: List[Tuple[str, str, str]], # [(metric_value, metric_label, evidence_detail)]
               theme: Theme):
        # 50/50 or 55/45 horizontal split
        split_x = left + width * 0.52
        left_w = width * 0.49
        right_w = width * 0.45

        # Left Surface: Insight
        SurfacePrimitive.render(slide, left, top, left_w, height, theme, border_color=theme.border_accent)
        tb_l = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.25), Inches(left_w - 0.50), Inches(height - 0.50))
        tf_l = tb_l.text_frame
        tf_l.word_wrap = True

        p_tag = tf_l.paragraphs[0]
        p_tag.space_after = Pt(8)
        TypographySystem.apply_to_paragraph(p_tag, TypographySystem.LABEL, insight_tag.upper(), theme.text_accent)

        p_hd = tf_l.add_paragraph()
        p_hd.space_after = Pt(14)
        TypographySystem.apply_to_paragraph(p_hd, TypographySystem.SECTION_TITLE, insight_headline, theme.text_primary)

        p_nar = tf_l.add_paragraph()
        TypographySystem.apply_to_paragraph(p_nar, TypographySystem.BODY, insight_narrative, theme.text_muted)

        # Right Surface: Quantitative Evidence stack
        SurfacePrimitive.render(slide, split_x, top, right_w, height, theme)
        hdr_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(split_x), Inches(top), Inches(right_w), Inches(0.42))
        hdr_box.fill.solid()
        hdr_box.fill.fore_color.rgb = theme.surface_highlight
        hdr_box.line.color.rgb = theme.border
        tf_h = hdr_box.text_frame
        TypographySystem.apply_to_paragraph(tf_h.paragraphs[0], TypographySystem.LABEL, "EMPIRICAL EVIDENCE & TELEMETRY PROOF", theme.text_accent)

        # Render evidence metric blocks
        num_ev = len(evidence_points)
        rows = GridCalculator.get_rows(num_ev, top=top + 0.55, total_height=height - 0.70, gap=0.15)
        for i, (val, lbl, detail) in enumerate(evidence_points):
            ry, rh = rows[i]
            # Metric Card
            mc = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(split_x + 0.15), Inches(ry), Inches(right_w - 0.30), Inches(rh))
            mc.fill.solid()
            mc.fill.fore_color.rgb = theme.surface_highlight
            mc.line.color.rgb = theme.border
            tf_m = mc.text_frame
            tf_m.word_wrap = True
            tf_m.margin_left = tf_m.margin_top = Inches(0.12)

            p_v = tf_m.paragraphs[0]
            TypographySystem.apply_to_paragraph(p_v, TypographySystem.KPI_NUMBER, val, theme.text_accent)

            p_l = tf_m.add_paragraph()
            TypographySystem.apply_to_paragraph(p_l, TypographySystem.KPI_LABEL, lbl, theme.text_primary)

            if detail:
                p_d = tf_m.add_paragraph()
                TypographySystem.apply_to_paragraph(p_d, TypographySystem.CAPTION, detail, theme.text_muted)


class KeyTakeawayPrimitive:
    """59. Key Takeaways & Strategic Summary (Numbered executive actions with anchors)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               takeaways: List[Tuple[str, str, str]], # [(number_str, takeaway_headline, description)]
               call_to_action: Optional[str],
               theme: Theme):
        SurfacePrimitive.render(slide, left, top, width, height, theme)

        # Header Pill
        hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(0.45))
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = theme.surface_highlight
        hdr.line.color.rgb = theme.border
        tf_h = hdr.text_frame
        tf_h.margin_left = Inches(0.20)
        TypographySystem.apply_to_paragraph(tf_h.paragraphs[0], TypographySystem.LABEL, "EXECUTIVE SUMMARY & STRATEGIC TAKEAWAYS", theme.text_accent)

        content_h = height - 0.60 - (0.65 if call_to_action else 0.0)
        cols = GridCalculator.get_columns(len(takeaways), left=left + 0.25, total_width=width - 0.50, gap=0.25)
        for i, (num_str, headline, desc) in enumerate(takeaways):
            cx, cw = cols[i]
            box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(top + 0.60), Inches(cw), Inches(content_h))
            box.fill.solid()
            box.fill.fore_color.rgb = theme.surface_highlight
            box.line.color.rgb = theme.border
            tf = box.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = Inches(0.16)

            p_num = tf.paragraphs[0]
            p_num.space_after = Pt(6)
            TypographySystem.apply_to_paragraph(p_num, TypographySystem.KPI_NUMBER, num_str, theme.text_accent)

            p_h = tf.add_paragraph()
            p_h.space_after = Pt(8)
            TypographySystem.apply_to_paragraph(p_h, TypographySystem.BODY_STRONG, headline, theme.text_primary)

            p_d = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_d, TypographySystem.BODY, desc, theme.text_muted)

        # Optional Bottom Call to Action Banner
        if call_to_action:
            cta_y = top + height - 0.55
            cta_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left + 0.25), Inches(cta_y), Inches(width - 0.50), Inches(0.45))
            cta_box.fill.solid()
            cta_box.fill.fore_color.rgb = theme.surface
            cta_box.line.color.rgb = theme.border_accent
            tf_cta = cta_box.text_frame
            tf_cta.margin_left = Inches(0.16)
            TypographySystem.apply_to_paragraph(tf_cta.paragraphs[0], TypographySystem.BODY_STRONG, f"DECISION REQUIRED: {call_to_action}", theme.text_accent)


class SectionDividerPrimitive:
    """60. Section Divider Slide (Full-width transition layout with section numbering & agenda preview)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               section_num: str, # E.g. "03"
               section_title: str, # E.g. "Integration Architecture & Shop Floor Telemetry"
               subtitle: str, # E.g. "Sub-second event streaming, SAP RFC ring-fencing, and edge resilience"
               agenda_items: List[str], # E.g. ["Event-Driven vs Polling Mechanics", "ISA-95 Boundary Defense", "Rollout Plan"]
               theme: Theme):
        # Section Backdrop Container
        SurfacePrimitive.render(slide, left, top, width, height, theme, border_color=theme.border_accent)

        # Large Section Number Pill
        num_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left + 0.40), Inches(top + 0.50), Inches(1.2), Inches(0.70))
        num_box.fill.solid()
        num_box.fill.fore_color.rgb = theme.surface_highlight
        num_box.line.color.rgb = theme.border_accent
        tf_n = num_box.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.alignment = PP_ALIGN.CENTER
        TypographySystem.apply_to_paragraph(p_n, TypographySystem.PRESENTATION_TITLE, section_num, theme.text_accent)

        # Title & Subtitle block
        tb = slide.shapes.add_textbox(Inches(left + 1.8), Inches(top + 0.40), Inches(width - 2.2), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p_lbl = tf.paragraphs[0]
        TypographySystem.apply_to_paragraph(p_lbl, TypographySystem.LABEL, "SECTION AGENDA", theme.text_muted)
        p_lbl.space_after = Pt(4)

        p_t = tf.add_paragraph()
        TypographySystem.apply_to_paragraph(p_t, TypographySystem.PRESENTATION_TITLE, section_title, theme.text_primary)
        p_t.space_after = Pt(8)

        p_s = tf.add_paragraph()
        TypographySystem.apply_to_paragraph(p_s, TypographySystem.SUBTITLE, subtitle, theme.text_muted)

        # Agenda Roadmap Track at bottom
        if agenda_items:
            track_top = top + 2.2
            track_h = height - 2.6
            cols = GridCalculator.get_columns(len(agenda_items), left=left + 0.40, total_width=width - 0.80, gap=0.25)
            for idx, item_text in enumerate(agenda_items, start=1):
                cx, cw = cols[idx - 1]
                abox = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(track_top), Inches(cw), Inches(track_h))
                abox.fill.solid()
                abox.fill.fore_color.rgb = theme.surface_highlight
                abox.line.color.rgb = theme.border
                tf_a = abox.text_frame
                tf_a.word_wrap = True
                tf_a.margin_left = tf_a.margin_top = Inches(0.14)

                p1 = tf_a.paragraphs[0]
                TypographySystem.apply_to_paragraph(p1, TypographySystem.LABEL, f"MODULE {idx:02d}", theme.text_accent)
                p1.space_after = Pt(6)

                p2 = tf_a.add_paragraph()
                TypographySystem.apply_to_paragraph(p2, TypographySystem.BODY_STRONG, item_text, theme.text_primary)
