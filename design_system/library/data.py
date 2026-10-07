"""
Data & Lineage Visual Primitives (Primitives 17–21).

Native, editable PowerPoint diagrams for ERP data lineage, entity relationships,
360° genealogy trees, BOM parent-child hierarchies, and data lifecycles.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE

from ..typography import TypographySystem
from ..spacing import Margins, SpacingScale, GridCalculator
from ..color import Theme
from ..primitives import SurfacePrimitive, ConnectorPrimitive


class DataLineagePrimitive:
    """17. Data lineage tracing from source transactional tables to executive consumption."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               lineage_nodes: List[Tuple[str, str, List[str]]], # [(stage_name, tech_component, entities)]
               theme: Theme):
        cols = GridCalculator.get_columns(len(lineage_nodes), left=left, total_width=width, gap=0.35)
        for i, (stage, tech, entities) in enumerate(lineage_nodes):
            cx, cw = cols[i]
            SurfacePrimitive.render(slide, cx, top, cw, height, theme)

            tb = slide.shapes.add_textbox(Inches(cx + 0.14), Inches(top + 0.14), Inches(cw - 0.28), Inches(height - 0.28))
            tf = tb.text_frame
            tf.word_wrap = True
            TypographySystem.apply_to_paragraph(tf.paragraphs[0], TypographySystem.LABEL, stage, theme.text_accent)
            p_t = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_t, TypographySystem.ANNOTATION, tech, theme.text_primary)
            p_t.space_after = Pt(8)

            for ent in entities[:4]:
                p_e = tf.add_paragraph()
                p_e.space_after = Pt(4)
                TypographySystem.apply_to_paragraph(p_e, TypographySystem.BODY, f"•  {ent}", theme.text_muted)

            if i < len(lineage_nodes) - 1:
                ConnectorPrimitive.render_arrow(slide, cx + cw + 0.05, top + height/2 - 0.12, 0.25, 0.24, "right", theme)


class EntityRelationshipPrimitive:
    """18. Entity Relationship schema view showing tables and primary/foreign key connections."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               entities: List[Tuple[str, str, List[Tuple[str, str]]]], # [(table_name, desc, [(field, type)])]
               theme: Theme):
        cols = GridCalculator.get_columns(len(entities), left=left, total_width=width, gap=0.30)
        for i, (t_name, desc, fields) in enumerate(entities):
            cx, cw = cols[i]
            SurfacePrimitive.render(slide, cx, top, cw, height, theme)

            # Table Header
            h_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(top), Inches(cw), Inches(0.48))
            h_box.fill.solid()
            h_box.fill.fore_color.rgb = theme.surface_highlight
            h_box.line.color.rgb = theme.border
            tf_h = h_box.text_frame
            TypographySystem.apply_to_paragraph(tf_h.paragraphs[0], TypographySystem.LABEL, t_name, theme.text_accent)
            TypographySystem.apply_to_paragraph(tf_h.add_paragraph(), TypographySystem.CAPTION, desc, theme.text_primary)

            # Fields
            tb = slide.shapes.add_textbox(Inches(cx + 0.14), Inches(top + 0.54), Inches(cw - 0.28), Inches(height - 0.60))
            tf = tb.text_frame
            tf.word_wrap = True
            for f_name, f_type in fields[:6]:
                p = tf.add_paragraph()
                p.space_after = Pt(3)
                TypographySystem.apply_to_paragraph(p, TypographySystem.TABLE_BODY, f"{f_name}: {f_type}", theme.text_muted)


class GenealogyTreePrimitive:
    """19. 360° As-Built genealogy tree linking finished good to sub-assemblies and component lots."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               finished_good: Tuple[str, str, str], # (serial_no, part_no, desc)
               sub_assemblies: List[Tuple[str, str, List[str]]], # [(sub_name, sub_lot, [component_lots])]
               theme: Theme):
        # 35% Left (Finished Good Root) + 65% Right (Component Branches)
        (lx, lw), (rx, rw) = GridCalculator.get_split(left_ratio=0.35, left=left, total_width=width, gap=0.40)

        # Finished Good Root Box
        SurfacePrimitive.render(slide, lx, top + height/2 - 1.0, lw, 2.0, theme, border_color=theme.border_accent)
        tb_fg = slide.shapes.add_textbox(Inches(lx + 0.16), Inches(top + height/2 - 0.85), Inches(lw - 0.32), Inches(1.7))
        tf_fg = tb_fg.text_frame
        TypographySystem.apply_to_paragraph(tf_fg.paragraphs[0], TypographySystem.LABEL, "FINISHED GOOD SERIAL", theme.border_accent)
        p_sn = tf_fg.add_paragraph()
        TypographySystem.apply_to_paragraph(p_sn, TypographySystem.BODY_STRONG, finished_good[0], theme.text_primary)
        p_sn.space_after = Pt(4)
        TypographySystem.apply_to_paragraph(tf_fg.add_paragraph(), TypographySystem.BODY, f"Part: {finished_good[1]}", theme.text_muted)
        TypographySystem.apply_to_paragraph(tf_fg.add_paragraph(), TypographySystem.CAPTION, finished_good[2], theme.text_muted)

        # Connector
        ConnectorPrimitive.render_arrow(slide, lx + lw + 0.05, top + height/2 - 0.15, 0.30, 0.28, "right", theme)

        # Sub-Assembly Branches
        sub_rows = GridCalculator.get_rows(len(sub_assemblies), top=top, total_height=height, gap=0.15)
        for i, (sub_name, sub_lot, comps) in enumerate(sub_assemblies):
            sy, sh = sub_rows[i]
            SurfacePrimitive.render(slide, rx, sy, rw, sh, theme)

            tb_s = slide.shapes.add_textbox(Inches(rx + 0.14), Inches(sy + 0.10), Inches(rw - 0.28), Inches(sh - 0.20))
            tf_s = tb_s.text_frame
            tf_s.word_wrap = True
            TypographySystem.apply_to_paragraph(tf_s.paragraphs[0], TypographySystem.LABEL, f"SUB-ASSEMBLY: {sub_name}", theme.text_accent)
            p_lt = tf_s.add_paragraph()
            TypographySystem.apply_to_paragraph(p_lt, TypographySystem.BODY_STRONG, f"Lot: {sub_lot}", theme.text_primary)
            p_lt.space_after = Pt(2)
            c_str = " | ".join(comps)
            TypographySystem.apply_to_paragraph(tf_s.add_paragraph(), TypographySystem.CAPTION, f"Components: {c_str}", theme.text_muted)


class ParentChildRelationshipPrimitive:
    """20. Multi-level indented BOM tree with quantities and revision numbers."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               bom_hierarchy: List[Tuple[int, str, str, str, str]], # [(depth_level, item_no, part_desc, qty, rev)]
               theme: Theme):
        # Full width structured hierarchy container
        SurfacePrimitive.render(slide, left, top, width, height, theme)

        # Header bar
        hbar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(0.40))
        hbar.fill.solid()
        hbar.fill.fore_color.rgb = theme.surface_highlight
        hbar.line.color.rgb = theme.border
        tf_h = hbar.text_frame
        TypographySystem.apply_to_paragraph(tf_h.paragraphs[0], TypographySystem.LABEL, "INDENTED BILL OF MATERIALS (BOM) LINEAGE", theme.text_accent)

        row_y = top + 0.48
        for depth, item_no, desc, qty, rev in bom_hierarchy[:8]:
            indent_x = left + 0.20 + (depth * 0.35)
            row_w = width - (depth * 0.35) - 0.40

            rb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(indent_x), Inches(row_y), Inches(row_w), Inches(0.46))
            rb.fill.solid()
            rb.fill.fore_color.rgb = theme.surface_alt if depth > 0 else theme.surface
            rb.line.color.rgb = theme.border
            tf_r = rb.text_frame
            tf_r.margin_left = Inches(0.08)
            p = tf_r.paragraphs[0]
            TypographySystem.apply_to_paragraph(p, TypographySystem.BODY, f"L{depth} • [{item_no}] {desc} | Qty: {qty} | Rev: {rev}", theme.text_primary)
            if depth == 0:
                p.runs[0].font.bold = True
            row_y += 0.52


class DataLifecyclePrimitive:
    """21. Data lifecycle progression: Ingest -> Process -> Storage -> Archival -> Purge."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               stages: List[Tuple[str, str, str]], # [(phase_name, retention_sla, policy_desc)]
               theme: Theme):
        cols = GridCalculator.get_columns(len(stages), left=left, total_width=width, gap=0.25)
        for i, (p_name, sla, policy) in enumerate(stages):
            cx, cw = cols[i]
            SurfacePrimitive.render(slide, cx, top, cw, height, theme)

            tb = slide.shapes.add_textbox(Inches(cx + 0.14), Inches(top + 0.14), Inches(cw - 0.28), Inches(height - 0.28))
            tf = tb.text_frame
            tf.word_wrap = True
            TypographySystem.apply_to_paragraph(tf.paragraphs[0], TypographySystem.LABEL, p_name, theme.text_accent)
            p_sla = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_sla, TypographySystem.ANNOTATION, f"RETENTION: {sla}", theme.status_info)
            p_sla.space_after = Pt(8)
            p_pol = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_pol, TypographySystem.BODY, policy, theme.text_muted)

            if i < len(stages) - 1:
                ConnectorPrimitive.render_arrow(slide, cx + cw + 0.05, top + height/2 - 0.12, 0.18, 0.22, "right", theme)
