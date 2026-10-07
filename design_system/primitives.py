"""
Visual Primitives for PowerPoint Slide Construction.

IMPORTANT PRINCIPLE: A card is ONE visual primitive, not the default slide layout.
All primitives strictly utilize TypographySystem tokens and SpacingScale dimensions.
Zero decorative blobs, zero gratuitous rounded corners, zero emoji, zero fake drop shadows.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

from .typography import TypographySystem
from .spacing import SpacingScale, Margins
from .color import Theme


class HeaderPrimitive:
    """Renders the executive category badge, slide title, and narrative subheader."""

    @staticmethod
    def render(slide, category_text: str, title_text: str, subtitle_text: Optional[str], theme: Theme):
        # 1. Category Badge Eyebrow
        badge_w = Inches(len(category_text) * 0.085 + 0.3)
        if badge_w < Inches(2.2):
            badge_w = Inches(2.2)
        if badge_w > Inches(5.5):
            badge_w = Inches(5.5)

        badge = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(Margins.left),
            Inches(SpacingScale.CATEGORY_TAG_TOP),
            badge_w,
            Inches(SpacingScale.CATEGORY_TAG_HEIGHT)
        )
        badge.fill.solid()
        badge.fill.fore_color.rgb = theme.surface_highlight
        badge.line.color.rgb = theme.border_accent
        badge.line.width = Pt(1.0)
        
        tf_b = badge.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = Inches(0.10)
        tf_b.margin_top = Inches(0.02)
        tf_b.margin_right = Inches(0.10)
        tf_b.margin_bottom = Inches(0.02)
        p_b = tf_b.paragraphs[0]
        TypographySystem.apply_to_paragraph(p_b, TypographySystem.LABEL, category_text, theme.border_accent)

        # 2. Main Slide Title
        t_box = slide.shapes.add_textbox(
            Inches(Margins.left),
            Inches(SpacingScale.TITLE_TOP),
            Inches(Margins().usable_width),
            Inches(SpacingScale.TITLE_HEIGHT)
        )
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        TypographySystem.apply_to_paragraph(p_t, TypographySystem.SLIDE_TITLE, title_text, theme.text_primary)

        # 3. Narrative Subheader (Action-oriented conversational thesis)
        if subtitle_text:
            s_box = slide.shapes.add_textbox(
                Inches(Margins.left),
                Inches(SpacingScale.SUBTITLE_TOP),
                Inches(Margins().usable_width),
                Inches(SpacingScale.SUBTITLE_HEIGHT)
            )
            tf_s = s_box.text_frame
            tf_s.word_wrap = True
            tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
            p_s = tf_s.paragraphs[0]
            TypographySystem.apply_to_paragraph(p_s, TypographySystem.SUBTITLE, subtitle_text, theme.text_accent)


class FooterPrimitive:
    """Renders the executive hairline divider, confidentiality notice, and slide pagination."""

    @staticmethod
    def render(slide, slide_num: int, total_slides: int, metadata_text: str, theme: Theme):
        # 1. Hairline divider rule
        divider = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(Margins.left),
            Inches(SpacingScale.FOOTER_DIVIDER_TOP),
            Inches(Margins().usable_width),
            Inches(0.01)
        )
        divider.fill.solid()
        divider.fill.fore_color.rgb = theme.border
        divider.line.fill.background()

        # 2. Metadata / Confidentiality Text
        m_box = slide.shapes.add_textbox(
            Inches(Margins.left),
            Inches(SpacingScale.FOOTER_TEXT_TOP),
            Inches(8.5),
            Inches(SpacingScale.FOOTER_HEIGHT)
        )
        tf_m = m_box.text_frame
        tf_m.margin_left = tf_m.margin_top = 0
        p_m = tf_m.paragraphs[0]
        TypographySystem.apply_to_paragraph(p_m, TypographySystem.FOOTNOTE, metadata_text, theme.text_muted)

        # 3. Pagination Counter (e.g., "04 / 12")
        num_box = slide.shapes.add_textbox(
            Inches(Margins.left + Margins().usable_width - 1.2),
            Inches(SpacingScale.FOOTER_TEXT_TOP),
            Inches(1.2),
            Inches(SpacingScale.FOOTER_HEIGHT)
        )
        tf_num = num_box.text_frame
        tf_num.margin_right = tf_num.margin_top = 0
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        page_str = f"{slide_num:02d} / {total_slides:02d}"
        TypographySystem.apply_to_paragraph(p_num, TypographySystem.FOOTNOTE, page_str, theme.text_accent)
        p_num.runs[0].font.bold = True


class SurfacePrimitive:
    """
    Flat, restrained rectangular surface for grouping related ideas.
    NOT a bubbly decorative card: flat solid fill, subtle border.
    """

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float, theme: Theme,
               fill_color: Optional[RGBColor] = None, border_color: Optional[RGBColor] = None,
               line_width_pt: float = 1.0):
        shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(left),
            Inches(top),
            Inches(width),
            Inches(height)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color if fill_color is not None else theme.surface
        shape.line.color.rgb = border_color if border_color is not None else theme.border
        shape.line.width = Pt(line_width_pt)
        return shape


class TextPrimitive:
    """Structured text block with lead-in run and descriptive body."""

    @staticmethod
    def render_lead_in_list(
        tf,
        items: List[Tuple[str, str]], # [(bold_lead_in, description)]
        theme: Theme,
        max_items: int = 4
    ):
        for idx, (lead_in, description) in enumerate(items[:max_items]):
            p = tf.paragraphs[0] if (idx == 0 and len(tf.paragraphs) == 1 and not tf.paragraphs[0].text) else tf.add_paragraph()
            p.space_after = Pt(8.0)
            
            # Bullet symbol + Bold lead-in run
            r_lead = p.add_run()
            TypographySystem.apply_to_run(r_lead, TypographySystem.BODY_STRONG, theme.text_primary, f"•  {lead_in} ")
            
            # Regular description run
            r_desc = p.add_run()
            TypographySystem.apply_to_run(r_desc, TypographySystem.BODY, theme.text_muted, description)


class MetricPrimitive:
    """Renders a prominent quantitative hero statistic with contextual explanation."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               value_str: str, label_str: str, context_str: Optional[str],
               theme: Theme, accent_color: Optional[RGBColor] = None):
        # Surface container
        SurfacePrimitive.render(slide, left, top, width, height, theme)

        # Text box inside
        box = slide.shapes.add_textbox(
            Inches(left + SpacingScale.CONTAINER_PAD_H),
            Inches(top + SpacingScale.CONTAINER_PAD_V),
            Inches(width - 2 * SpacingScale.CONTAINER_PAD_H),
            Inches(height - 2 * SpacingScale.CONTAINER_PAD_V)
        )
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # 1. Metric Value
        p_val = tf.paragraphs[0]
        color = accent_color if accent_color is not None else theme.accent_primary
        TypographySystem.apply_to_paragraph(p_val, TypographySystem.KPI_NUMBER, value_str, color)

        # 2. Metric Label
        p_lbl = tf.add_paragraph()
        TypographySystem.apply_to_paragraph(p_lbl, TypographySystem.KPI_LABEL, label_str, theme.text_primary)

        # 3. Context Description
        if context_str:
            p_ctx = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_ctx, TypographySystem.CAPTION, context_str, theme.text_muted)


class TablePrimitive:
    """Renders an enterprise data table with styled headers, alternating rows, and data alignment."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               headers: List[str], rows: List[List[str]],
               theme: Theme, col_weights: Optional[List[float]] = None):
        r_count = len(rows) + 1
        c_count = len(headers)
        tbl_shape = slide.shapes.add_table(r_count, c_count, Inches(left), Inches(top), Inches(width), Inches(height))
        tbl = tbl_shape.table

        # Column widths
        if col_weights and len(col_weights) == c_count:
            total_weight = sum(col_weights)
            for c_idx, weight in enumerate(col_weights):
                tbl.columns[c_idx].width = Inches((weight / total_weight) * width)
        else:
            default_w = width / c_count
            for c_idx in range(c_count):
                tbl.columns[c_idx].width = Inches(default_w)

        # Header Row
        for c_idx, h_text in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = theme.surface_alt if not theme.is_dark else theme.surface
            tf = cell.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_right = Inches(0.08)
            p = tf.paragraphs[0]
            TypographySystem.apply_to_paragraph(p, TypographySystem.TABLE_HEADER, h_text, theme.text_accent)

        # Data Rows
        for r_idx, row_data in enumerate(rows, start=1):
            row_fill = theme.surface if (r_idx % 2 == 1) else theme.surface_alt
            for c_idx, val in enumerate(row_data[:c_count]):
                cell = tbl.cell(r_idx, c_idx)
                cell.fill.solid()
                cell.fill.fore_color.rgb = row_fill
                tf = cell.text_frame
                tf.word_wrap = True
                tf.margin_left = tf.margin_right = Inches(0.08)
                p = tf.paragraphs[0]
                token = TypographySystem.TABLE_BODY
                TypographySystem.apply_to_paragraph(p, token, val, theme.text_primary)
                if c_idx == 0:
                    p.runs[0].font.bold = True


class ConnectorPrimitive:
    """Renders a directional flow arrow between systems or stages."""

    @staticmethod
    def render_arrow(slide, left: float, top: float, width: float, height: float,
                     direction: str, theme: Theme, label: Optional[str] = None):
        shape_type = MSO_SHAPE.RIGHT_ARROW if direction.lower() == "right" else MSO_SHAPE.DOWN_ARROW
        arr = slide.shapes.add_shape(shape_type, Inches(left), Inches(top), Inches(width), Inches(height))
        arr.fill.solid()
        arr.fill.fore_color.rgb = theme.border_accent
        arr.line.fill.background()

        if label:
            # Annotation text next to arrow
            tx = slide.shapes.add_textbox(Inches(left), Inches(top - 0.22), Inches(width + 0.4), Inches(0.22))
            tf = tx.text_frame
            tf.margin_left = tf.margin_top = 0
            p = tf.paragraphs[0]
            TypographySystem.apply_to_paragraph(p, TypographySystem.ANNOTATION, label, theme.text_accent)


class CalloutBannerPrimitive:
    """Full-width enclosed banner for security, architecture guarantees, and SLA callouts."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               headline: str, body_bullets: List[str], theme: Theme):
        banner = SurfacePrimitive.render(
            slide, left, top, width, height, theme,
            fill_color=theme.surface,
            border_color=theme.border_accent,
            line_width_pt=1.5
        )
        box = slide.shapes.add_textbox(
            Inches(left + SpacingScale.CONTAINER_PAD_H),
            Inches(top + 0.10),
            Inches(width - 2 * SpacingScale.CONTAINER_PAD_H),
            Inches(height - 0.20)
        )
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_h = tf.paragraphs[0]
        TypographySystem.apply_to_paragraph(p_h, TypographySystem.LABEL, headline, theme.accent_primary)

        for b_text in body_bullets[:3]:
            p_b = tf.add_paragraph()
            p_b.space_after = Pt(3.0)
            TypographySystem.apply_to_paragraph(p_b, TypographySystem.BODY, f"•  {b_text}", theme.text_secondary)
