"""
Governance & Compliance Visual Primitives (Primitives 47–50).

Native, editable PowerPoint diagrams for multi-tier approval gates,
RACI responsibility matrices, enterprise control frameworks, and organizational governance models.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

from ..typography import TypographySystem
from ..spacing import Margins, SpacingScale, GridCalculator
from ..color import Theme
from ..primitives import SurfacePrimitive, ConnectorPrimitive


class ApprovalGatesPrimitive:
    """47. Multi-Tier Approval Gates (Stage gates with sign-off roles, conditions, and sign-off slips)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               gates: List[Tuple[str, str, str, List[str], str]], # [(gate_label, role, timing, criteria_list, outcome_artifact)]
               theme: Theme):
        cols = GridCalculator.get_columns(len(gates), left=left, total_width=width, gap=0.30)
        for i, (gate_lbl, role, timing, criteria, outcome) in enumerate(gates):
            cx, cw = cols[i]
            SurfacePrimitive.render(slide, cx, top, cw, height, theme, border_color=theme.border_accent)

            # Gate Header Tag
            gtag = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(top), Inches(cw), Inches(0.40))
            gtag.fill.solid()
            gtag.fill.fore_color.rgb = theme.surface_highlight
            gtag.line.color.rgb = theme.border
            tf_g = gtag.text_frame
            tf_g.margin_left = Inches(0.12)
            TypographySystem.apply_to_paragraph(tf_g.paragraphs[0], TypographySystem.LABEL, gate_lbl.upper(), theme.text_accent)

            tb = slide.shapes.add_textbox(Inches(cx + 0.14), Inches(top + 0.46), Inches(cw - 0.28), Inches(height - 0.54))
            tf = tb.text_frame
            tf.word_wrap = True

            # Approver Role & Cadence
            p_r = tf.paragraphs[0]
            TypographySystem.apply_to_paragraph(p_r, TypographySystem.BODY_STRONG, role, theme.text_primary)
            p_t = tf.add_paragraph()
            p_t.space_after = Pt(8)
            TypographySystem.apply_to_paragraph(p_t, TypographySystem.CAPTION, f"Timing: {timing}", theme.text_muted)

            # Verification Criteria
            p_c_hdr = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_c_hdr, TypographySystem.LABEL, "VERIFICATION CRITERIA", theme.text_muted)
            p_c_hdr.space_after = Pt(4)

            for crit in criteria[:3]:
                p_c = tf.add_paragraph()
                p_c.space_after = Pt(4)
                TypographySystem.apply_to_paragraph(p_c, TypographySystem.BODY, f"• {crit}", theme.text_primary)

            # Outcome / Artifact Produced
            p_out = tf.add_paragraph()
            p_out.space_before = Pt(8)
            TypographySystem.apply_to_paragraph(p_out, TypographySystem.ANNOTATION, f"ARTIFACT: {outcome}", theme.status_success)

            # Chevron / Arrow connector to next gate
            if i < len(gates) - 1:
                ConnectorPrimitive.render_arrow(slide, cx + cw + 0.05, top + height / 2.0 - 0.12, 0.20, 0.24, "right", theme)


class RACIResponsibilityPrimitive:
    """48. RACI-Style Responsibility View (Deliverables vs Roles matrix with R/A/C/I pills)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               roles: List[str], # Column headers e.g. ["Enterprise Architect", "MES Tech Lead", "Plant QA", "Steering Comm"]
               deliverables: List[Tuple[str, List[str]]], # [(activity_title, [raci_codes_matching_roles])]
               theme: Theme):
        # Native editable PowerPoint Table
        num_rows = len(deliverables) + 1
        num_cols = len(roles) + 1
        table_shape = slide.shapes.add_table(num_rows, num_cols, Inches(left), Inches(top), Inches(width), Inches(height))
        table = table_shape.table

        # Column widths: 40% for deliverable/activity description, remaining divided among roles
        deliv_col_w = width * 0.38
        role_col_w = (width - deliv_col_w) / max(1, len(roles))
        table.columns[0].width = Inches(deliv_col_w)
        for c in range(1, num_cols):
            table.columns[c].width = Inches(role_col_w)

        # Header Row
        hdr_cell = table.cell(0, 0)
        hdr_cell.fill.solid()
        hdr_cell.fill.fore_color.rgb = theme.surface_highlight
        tf_h = hdr_cell.text_frame
        tf_h.word_wrap = True
        TypographySystem.apply_to_paragraph(tf_h.paragraphs[0], TypographySystem.TABLE_HEADER, "ACTIVITY / DELIVERABLE", theme.text_primary)

        for col_idx, role_name in enumerate(roles, start=1):
            cell = table.cell(0, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = theme.surface_highlight
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            TypographySystem.apply_to_paragraph(p, TypographySystem.TABLE_HEADER, role_name, theme.text_accent)

        # Body Rows
        for row_idx, (act_title, raci_codes) in enumerate(deliverables, start=1):
            # Alternating subtle row fill
            row_fill = theme.surface_alt if (row_idx % 2 == 1) else theme.surface
            c0 = table.cell(row_idx, 0)
            c0.fill.solid()
            c0.fill.fore_color.rgb = row_fill
            tf0 = c0.text_frame
            tf0.word_wrap = True
            TypographySystem.apply_to_paragraph(tf0.paragraphs[0], TypographySystem.TABLE_BODY, act_title, theme.text_primary)

            for col_idx, code in enumerate(raci_codes[:len(roles)], start=1):
                cell = table.cell(row_idx, col_idx)
                cell.fill.solid()
                cell.fill.fore_color.rgb = row_fill
                tf_c = cell.text_frame
                p_c = tf_c.paragraphs[0]
                p_c.alignment = PP_ALIGN.CENTER

                # Color-code RACI
                code_str = str(code).upper().strip()
                if "A" in code_str:
                    TypographySystem.apply_to_paragraph(p_c, TypographySystem.BODY_STRONG, "A", theme.status_critical)
                elif "R" in code_str:
                    TypographySystem.apply_to_paragraph(p_c, TypographySystem.BODY_STRONG, "R", theme.text_accent)
                elif "C" in code_str:
                    TypographySystem.apply_to_paragraph(p_c, TypographySystem.BODY_STRONG, "C", theme.status_warning)
                elif "I" in code_str:
                    TypographySystem.apply_to_paragraph(p_c, TypographySystem.BODY, "I", theme.text_muted)
                else:
                    TypographySystem.apply_to_paragraph(p_c, TypographySystem.CAPTION, "—", theme.text_muted)


class ControlFrameworkPrimitive:
    """49. Enterprise Control Framework (Preventive, Detective, and Corrective tiers or ISA-95 controls)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               tiers: List[Tuple[str, str, List[Tuple[str, str, str]]]], # [(tier_title, tier_type, [(ctrl_id, ctrl_desc, enforcement)])]
               theme: Theme):
        cols = GridCalculator.get_columns(len(tiers), left=left, total_width=width, gap=0.25)
        for i, (tier_title, tier_type, controls) in enumerate(tiers):
            cx, cw = cols[i]
            SurfacePrimitive.render(slide, cx, top, cw, height, theme)

            # Tier Banner
            tb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(top), Inches(cw), Inches(0.42))
            tb.fill.solid()
            tb.fill.fore_color.rgb = theme.surface_highlight
            tb.line.color.rgb = theme.border
            tf_b = tb.text_frame
            TypographySystem.apply_to_paragraph(tf_b.paragraphs[0], TypographySystem.LABEL, tier_type.upper(), theme.text_accent)
            p_t = tf_b.add_paragraph()
            TypographySystem.apply_to_paragraph(p_t, TypographySystem.BODY_STRONG, tier_title, theme.text_primary)

            # Controls List
            tbox = slide.shapes.add_textbox(Inches(cx + 0.14), Inches(top + 0.52), Inches(cw - 0.28), Inches(height - 0.60))
            tf = tbox.text_frame
            tf.word_wrap = True

            for idx, (cid, cdesc, enf) in enumerate(controls[:4]):
                p_id = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                p_id.space_before = Pt(6) if idx > 0 else Pt(0)
                TypographySystem.apply_to_paragraph(p_id, TypographySystem.BODY_STRONG, f"[{cid}] {cdesc}", theme.text_primary)
                p_enf = tf.add_paragraph()
                p_enf.space_after = Pt(4)
                TypographySystem.apply_to_paragraph(p_enf, TypographySystem.CAPTION, f"Enforcement: {enf}", theme.text_muted)


class GovernanceModelPrimitive:
    """50. Multi-Level Governance Model (Steering Committee -> Architecture Board -> Working Teams)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               layers: List[Tuple[str, str, str, List[str], str]], # [(body_name, cadence, chair, responsibilities, escalation_to)]
               theme: Theme):
        rows = GridCalculator.get_rows(len(layers), top=top, total_height=height, gap=0.18)
        for i, (b_name, cadence, chair, resps, esc) in enumerate(layers):
            ry, rh = rows[i]
            SurfacePrimitive.render(slide, left, ry, width, rh, theme)

            # Left Level Pill / Header
            l_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(ry), Inches(2.6), Inches(rh))
            l_box.fill.solid()
            l_box.fill.fore_color.rgb = theme.surface_highlight
            l_box.line.color.rgb = theme.border
            tf_l = l_box.text_frame
            tf_l.margin_left = Inches(0.12)
            TypographySystem.apply_to_paragraph(tf_l.paragraphs[0], TypographySystem.LABEL, cadence.upper(), theme.text_accent)
            p_b = tf_l.add_paragraph()
            TypographySystem.apply_to_paragraph(p_b, TypographySystem.BODY_STRONG, b_name, theme.text_primary)
            p_ch = tf_l.add_paragraph()
            TypographySystem.apply_to_paragraph(p_ch, TypographySystem.CAPTION, f"Chair: {chair}", theme.text_muted)

            # Responsibilities Textbox
            content_w = width - 2.8 - (2.0 if esc else 0.0)
            tb = slide.shapes.add_textbox(Inches(left + 2.7), Inches(ry + 0.10), Inches(content_w), Inches(rh - 0.20))
            tf = tb.text_frame
            tf.word_wrap = True
            for idx, r in enumerate(resps[:3]):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                p.space_after = Pt(3)
                TypographySystem.apply_to_paragraph(p, TypographySystem.BODY, f"• {r}", theme.text_primary)

            # Right Escalation Pill if defined
            if esc:
                esc_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left + width - 1.9), Inches(ry + 0.12), Inches(1.8), Inches(rh - 0.24))
                esc_box.fill.solid()
                esc_box.fill.fore_color.rgb = theme.surface
                esc_box.line.color.rgb = theme.border_accent
                tf_e = esc_box.text_frame
                tf_e.word_wrap = True
                TypographySystem.apply_to_paragraph(tf_e.paragraphs[0], TypographySystem.LABEL, "ESCALATES TO", theme.text_accent)
                p_e = tf_e.add_paragraph()
                TypographySystem.apply_to_paragraph(p_e, TypographySystem.CAPTION, esc, theme.text_muted)
