import os
from typing import Dict, Any, List, Optional, Tuple
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE, PP_PLACEHOLDER
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION

from design_system.lumbini.tokens import LumbiniTheme
from tools.pptx_text_helpers import set_text, label_in_shape, fit_pt, width_in
from tools.textfit import measure

def measure_text_dimensions(text: str, font_name: str, font_size_pt: float, max_width_in: float) -> Tuple[float, float]:
    """Measures estimated text dimensions in inches."""
    words = text.split()
    if not words:
        return (0.0, 0.0)
    avg_char_w = font_size_pt * 0.0075
    line_h = font_size_pt * 0.016
    
    lines = 1
    curr_w = 0.0
    for w in words:
        w_len = len(w) * avg_char_w
        if curr_w + w_len > max_width_in:
            lines += 1
            curr_w = w_len
        else:
            curr_w += w_len + avg_char_w
    return (max_width_in, lines * line_h)

class LumbiniPrimitives:
    """
    Level B: Component Library
    Content-free parameterised atoms and visual composers.
    Zero topic text or default hardcoded client strings inside.
    """

    def __init__(self, theme: LumbiniTheme):
        self.theme = theme

    def _find_or_create_title_box(self, slide, left: Inches, top: Inches, width: Inches, height: Inches):
        """
        Finds the inherited Title placeholder if present on the slide to prevent PowerPoint
        from rendering 'Click to add title' prompt boxes. If not present, creates a textbox.
        """
        for ph in slide.placeholders:
            try:
                if ph.placeholder_format.type in (PP_PLACEHOLDER.TITLE, PP_PLACEHOLDER.CENTER_TITLE):
                    ph.left = left
                    ph.top = top
                    ph.width = width
                    ph.height = height
                    return ph
            except Exception:
                pass
        return slide.shapes.add_textbox(left, top, width, height)

    # =========================================================================
    # CORE ATOMS & LAYOUT INFRASTRUCTURE
    # =========================================================================
    def add_title_block(self, slide, eyebrow_text: Optional[str], title_text: str, subtitle_text: Optional[str] = None):
        """Standardized title block adhering strictly to the Lumbini type hierarchy."""
        # 1. Eyebrow
        if eyebrow_text:
            tb_e = slide.shapes.add_textbox(self.theme.IN_MARGIN_X, Inches(0.48), Inches(10.0), Inches(0.28))
            tf_e = tb_e.text_frame
            tf_e.word_wrap = True
            tf_e.margin_left = tf_e.margin_right = tf_e.margin_top = tf_e.margin_bottom = 0
            p_e = tf_e.paragraphs[0]
            p_e.text = eyebrow_text.upper()
            p_e.font.name = self.theme.FONT_SEMIBOLD
            p_e.font.size = self.theme.PT_EYEBROW
            p_e.font.bold = True
            p_e.font.color.rgb = self.theme.C_PRIMARY

        # 2. Action Title
        top_y = Inches(0.78) if eyebrow_text else Inches(0.55)
        tb_t = self._find_or_create_title_box(slide, self.theme.IN_MARGIN_X, top_y, Inches(11.8), Inches(0.58))
        tf_t = tb_t.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = self.theme.FONT_HEADING
        p_t.font.size = self.theme.PT_TITLE
        p_t.font.bold = True
        p_t.font.color.rgb = self.theme.C_TEXT

        # 3. Subtitle
        if subtitle_text:
            tb_s = slide.shapes.add_textbox(self.theme.IN_MARGIN_X, Inches(1.36), Inches(11.8), Inches(0.50))
            tf_s = tb_s.text_frame
            tf_s.word_wrap = True
            tf_s.auto_size = MSO_AUTO_SIZE.NONE
            tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
            p_s = tf_s.paragraphs[0]
            p_s.text = subtitle_text
            p_s.font.name = self.theme.FONT_BODY
            p_s.font.size = self.theme.PT_SUBTITLE
            p_s.font.color.rgb = self.theme.C_MUTED

    def render_footer(self, slide, meta: Dict[str, Any], slide_num: int, total_slides: int):
        """Parameterised footer adhering strictly to v2 anti-copy requirements."""
        confidentiality = meta.get("confidentiality", "Confidential")
        client = meta.get("client") or meta.get("topic") or ""
        doc_type = meta.get("doc_type", "Executive Presentation")

        parts = ["Lumbini Elite Solutions & Services Pvt. Ltd.", confidentiality]
        if client:
            parts.append(client)
        if doc_type:
            parts.append(doc_type)
        footer_text = "  |  ".join(parts)

        # Left text
        tb_f = slide.shapes.add_textbox(Inches(0.65), Inches(self.theme.raw["slide"]["footer_y_in"]), Inches(10.2), Inches(0.28))
        tf_f = tb_f.text_frame
        tf_f.word_wrap = True
        tf_f.margin_left = tf_f.margin_right = tf_f.margin_top = tf_f.margin_bottom = 0
        pf = tf_f.paragraphs[0]
        pf.text = footer_text
        pf.font.name = self.theme.FONT_BODY
        pf.font.size = Pt(12)
        pf.font.color.rgb = self.theme.C_MUTED

        # Right slide number
        tb_n = slide.shapes.add_textbox(Inches(11.0), Inches(self.theme.raw["slide"]["footer_y_in"]), Inches(1.68), Inches(0.28))
        tf_n = tb_n.text_frame
        tf_n.margin_left = tf_n.margin_right = tf_n.margin_top = tf_n.margin_bottom = 0
        pn = tf_n.paragraphs[0]
        pn.text = f"{slide_num} / {total_slides}"
        pn.alignment = PP_ALIGN.RIGHT
        pn.font.name = self.theme.FONT_BODY
        pn.font.size = Pt(12)
        pn.font.color.rgb = self.theme.C_MUTED

    def add_locator(self, slide, x: float, y: float, w: float, h: float, current_level: str, levels: List[str]):
        """Renders an enterprise / platform locator in the header corner."""
        if not levels:
            return
        btn_w = w / len(levels)
        for i, lvl in enumerate(levels):
            bx = x + i * btn_w
            is_active = (lvl.strip().lower() == current_level.strip().lower())
            box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(bx), Inches(y), Inches(btn_w - 0.03), Inches(h))
            box.fill.solid()
            box.fill.fore_color.rgb = self.theme.C_PRIMARY if is_active else self.theme.C_SURFACE
            box.line.color.rgb = self.theme.C_PRIMARY if is_active else self.theme.C_BORDER
            box.line.width = Pt(1)

            tf = box.text_frame
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = tf.paragraphs[0]
            p.text = lvl
            p.alignment = PP_ALIGN.CENTER
            p.font.name = self.theme.FONT_SEMIBOLD
            p.font.size = Pt(12)
            p.font.bold = is_active
            p.font.color.rgb = self.theme.C_WHITE if is_active else self.theme.C_MUTED

    def add_card(self, slide, x: Inches, y: Inches, w: Inches, h: Inches,
                 bg_color: Optional[RGBColor] = None, border_color: Optional[RGBColor] = None,
                 is_dashed: bool = False):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color or self.theme.C_WHITE
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
            if is_dashed:
                card.line.dash_style = 2
        else:
            card.line.fill.background()
        return card

    def add_line(self, slide, x1: float, y1: float, x2: float, y2: float,
                 color: Optional[RGBColor] = None, width_pt: float = 1.5,
                 is_dashed: bool = False):
        color = color or self.theme.C_MUTED
        left = Inches(min(x1, x2))
        top = Inches(min(y1, y2))
        width = Inches(abs(x2 - x1) if abs(x2 - x1) > 0.001 else 0.001)
        height = Inches(abs(y2 - y1) if abs(y2 - y1) > 0.001 else 0.001)

        conn = slide.shapes.add_connector(1, left, top, left + width, top + height)
        conn.line.color.rgb = color
        conn.line.width = Pt(width_pt)
        if is_dashed:
            conn.line.dash_style = 2
        return conn

    def add_circle_badge(self, slide, cx: float, cy: float, diameter: float, label: str,
                         fill_color: RGBColor, font_size_pt: float = 14):
        d = Inches(diameter)
        x = Inches(cx - diameter / 2.0)
        y = Inches(cy - diameter / 2.0)
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, d, d)
        circle.fill.solid()
        circle.fill.fore_color.rgb = fill_color
        circle.line.fill.background()

        tf = circle.text_frame
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = label
        p.alignment = PP_ALIGN.CENTER
        p.font.name = self.theme.FONT_HEADING
        p.font.size = Pt(font_size_pt)
        p.font.bold = True
        p.font.color.rgb = self.theme.C_WHITE
        return circle

    # =========================================================================
    # COMPOSITION 1: COVER
    # =========================================================================
    def render_cover(self, slide, title: str, subtitle: str, metadata_rows: List[Tuple[str, str]],
                     pill_text: Optional[str] = None, dark_theme: bool = False):
        if dark_theme:
            bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
            bg.fill.solid()
            bg.fill.fore_color.rgb = RGBColor(10, 25, 47)  # #0A192F Dark Executive Navy
            bg.line.fill.background()
            title_color = "FFFFFF"
            subtitle_color = "38BDF8"  # Sky blue
            meta_k_color = "94A3B8"    # Slate 400
            meta_v_color = "FFFFFF"    # White
            pill_bg = RGBColor(2, 132, 199) # Blue accent
        else:
            title_color = "141E2D"
            subtitle_color = "0070C0"
            meta_k_color = "4F6F8F"
            meta_v_color = "0B192C"
            pill_bg = self.theme.C_NAVY

        if os.path.exists(self.theme.ILLUS_PATH):
            try:
                slide.shapes.add_picture(self.theme.ILLUS_PATH, Inches(0.25), Inches(0.2), Inches(2.8), Inches(2.9))
            except Exception:
                pass

        if os.path.exists(self.theme.LOGO_PATH):
            try:
                slide.shapes.add_picture(self.theme.LOGO_PATH, Inches(10.35), Inches(0.5), Inches(2.4), Inches(1.017))
            except Exception:
                pass

        # Title (uses native title placeholder if available to avoid 'Click to add title' prompts)
        t_box = self._find_or_create_title_box(slide, Inches(0.9), Inches(2.45), Inches(9.6), Inches(2.0))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = self.theme.FONT_HEADING
        p_t.font.size = Pt(36)
        p_t.font.bold = True
        p_t.font.color.rgb = RGBColor(255, 255, 255) if dark_theme else self.theme.C_TEXT

        # Orange Accent Rule
        rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(4.68), Inches(5.3), Inches(0.04))
        rule.fill.solid()
        rule.fill.fore_color.rgb = self.theme.C_ACCENT
        rule.line.fill.background()

        # Subtitle
        s_box = slide.shapes.add_textbox(Inches(0.9), Inches(4.85), Inches(9.4), Inches(0.65))
        tf_s = s_box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle
        p_s.font.name = self.theme.FONT_SEMIBOLD
        p_s.font.size = Pt(16)
        p_s.font.bold = True
        p_s.font.color.rgb = RGBColor(56, 189, 248) if dark_theme else self.theme.C_PRIMARY

        # Metadata key-value rows
        for i, (k, v) in enumerate(metadata_rows):
            y = Inches(5.55 + i * 0.36)
            tb_k = slide.shapes.add_textbox(Inches(0.9), y, Inches(1.8), Inches(0.3))
            set_text(tb_k, k, face="Inter", weight="semibold", pt=12.0, color=meta_k_color, align="left", anchor="middle", pad_in=0.0)

            tb_v = slide.shapes.add_textbox(Inches(2.8), y, Inches(5.2), Inches(0.3))
            set_text(tb_v, v, face="Inter", weight="regular", pt=12.0, color=meta_v_color, align="left", anchor="middle", pad_in=0.0)

        # Category Pill (measured and fitted within slide boundaries with 12% safety slack)
        if pill_text:
            pt_sz = 12.0
            w_needed = measure(pill_text, True, pt_sz) * 1.12 + 0.5
            pill_w = max(2.5, min(4.2, w_needed))
            pill_x = 12.68 - pill_w
            pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(pill_x), Inches(6.25), Inches(pill_w), Inches(0.65))
            pill.fill.solid()
            pill.fill.fore_color.rgb = pill_bg
            pill.line.fill.background()
            set_text(pill, pill_text, face="Inter", weight="bold", pt=pt_sz, color="FFFFFF", align="center", anchor="middle", pad_in=0.1)

    # =========================================================================
    # COMPOSITION 2: BEFORE / AFTER TRANSFORMATION ROWS
    # =========================================================================
    def render_requirement_to_outcome(self, slide, items: List[Dict[str, Any]], headers: Optional[List[str]] = None):
        h_labels = headers or ["DIMENSION", "BASELINE STATE", "TRANSFORMATION SHIFT"]
        header_configs = [
            (h_labels[0], 0.65, 3.8, self.theme.C_MUTED),
            (h_labels[1], 4.75, 3.8, self.theme.C_MUTED),
            (h_labels[2], 9.2, 3.48, self.theme.C_PRIMARY)
        ]
        for h, x, w, col in header_configs:
            tb = slide.shapes.add_textbox(Inches(x), Inches(1.9), Inches(w), Inches(0.28))
            tf = tb.text_frame
            tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = h
            p.font.name = self.theme.FONT_SEMIBOLD
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = col

        colors = [self.theme.C_PRIMARY, self.theme.C_NAVY, self.theme.C_ACCENT, self.theme.C_MUTED]

        for i, item in enumerate(items[:4]):
            y = 2.25 + i * 1.12
            self.add_line(slide, 0.65, y, 12.68, y, color=self.theme.C_BORDER, width_pt=1.25)

            badge_col = item.get("badge_color") or colors[i % len(colors)]
            self.add_circle_badge(slide, 0.92, y + 0.56, 0.52, str(i + 1), badge_col, font_size_pt=16)

            title = item.get("title") or item.get("requirement") or item.get("dimension") or ""
            today = item.get("today") or item.get("baseline") or item.get("from") or ""
            outcome = item.get("outcome") or item.get("target") or item.get("to") or ""

            # Col 1: Dimension
            tb1 = slide.shapes.add_textbox(Inches(1.5), Inches(y + 0.08), Inches(3.0), Inches(0.96))
            tf1 = tb1.text_frame
            tf1.word_wrap = True
            tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0
            p1 = tf1.paragraphs[0]
            p1.text = title
            p1.font.name = self.theme.FONT_HEADING
            p1.font.size = Pt(14)
            p1.font.bold = True
            p1.font.color.rgb = self.theme.C_TEXT

            # Col 2: Baseline
            tb2 = slide.shapes.add_textbox(Inches(4.75), Inches(y + 0.08), Inches(3.55), Inches(0.96))
            tf2 = tb2.text_frame
            tf2.word_wrap = True
            tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = 0
            p2 = tf2.paragraphs[0]
            p2.text = today
            p2.font.name = self.theme.FONT_BODY
            p2.font.size = Pt(12)
            p2.font.color.rgb = self.theme.C_MUTED

            # Arrow
            arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(8.5), Inches(y + 0.38), Inches(0.45), Inches(0.36))
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = self.theme.C_PRIMARY
            arrow.line.fill.background()

            # Col 3: Target Outcome
            tb3 = slide.shapes.add_textbox(Inches(9.2), Inches(y + 0.08), Inches(3.48), Inches(0.96))
            tf3 = tb3.text_frame
            tf3.word_wrap = True
            tf3.margin_left = tf3.margin_right = tf3.margin_top = tf3.margin_bottom = 0
            p3 = tf3.paragraphs[0]
            p3.text = outcome
            p3.font.name = self.theme.FONT_SEMIBOLD
            p3.font.size = Pt(12)
            p3.font.color.rgb = self.theme.C_TEXT

    # =========================================================================
    # COMPOSITION 3: RADIAL HUB AND SPOKES (PARAMETERISED CONNECTORS)
    # =========================================================================
    def render_hub_and_spokes(self, slide, hub_title: str, hub_subtitle: str, spokes: List[Dict[str, Any]]):
        # Center Hub
        hub = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.08), Inches(3.1), Inches(3.17), Inches(2.25))
        hub.fill.solid()
        hub.fill.fore_color.rgb = self.theme.C_NAVY
        hub.line.fill.background()

        tf_h = hub.text_frame
        tf_h.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_h1 = tf_h.paragraphs[0]
        p_h1.text = hub_title
        p_h1.font.name = self.theme.FONT_HEADING
        p_h1.font.size = Pt(16)
        p_h1.font.bold = True
        p_h1.font.color.rgb = self.theme.C_WHITE
        p_h1.alignment = PP_ALIGN.CENTER

        p_h2 = tf_h.add_paragraph()
        p_h2.text = hub_subtitle
        p_h2.font.name = self.theme.FONT_BODY
        p_h2.font.size = Pt(12)
        p_h2.font.color.rgb = self.theme.C_SURFACE
        p_h2.alignment = PP_ALIGN.CENTER

        if len(spokes) == 4:
            spoke_coords = [
                {"x": 0.65, "y": 2.05, "w": 4.15, "h": 2.25, "ax1": 4.80, "ay1": 3.15, "ax2": 5.08, "ay2": 3.55, "lx": 4.85, "ly": 2.90},
                {"x": 0.65, "y": 4.50, "w": 4.15, "h": 2.25, "ax1": 4.80, "ay1": 5.25, "ax2": 5.08, "ay2": 4.85, "lx": 4.85, "ly": 5.15},
                {"x": 8.53, "y": 2.05, "w": 4.15, "h": 2.25, "ax1": 8.53, "ay1": 3.15, "ax2": 8.25, "ay2": 3.55, "lx": 8.35, "ly": 2.90},
                {"x": 8.53, "y": 4.50, "w": 4.15, "h": 2.25, "ax1": 8.53, "ay1": 5.25, "ax2": 8.25, "ay2": 4.85, "lx": 8.35, "ly": 5.15}
            ]
        else:
            spoke_coords = [
                {"x": 0.65, "y": 2.10, "w": 4.0, "h": 1.60, "ax1": 4.65, "ay1": 2.95, "ax2": 5.08, "ay2": 3.5, "lx": 4.75, "ly": 2.35},
                {"x": 0.65, "y": 4.55, "w": 4.0, "h": 1.60, "ax1": 4.65, "ay1": 5.30, "ax2": 5.08, "ay2": 4.6, "lx": 4.75, "ly": 5.05},
                {"x": 8.68, "y": 3.20, "w": 4.0, "h": 1.60, "ax1": 8.25, "ay1": 4.00, "ax2": 8.68, "ay2": 4.0, "lx": 8.15, "ly": 3.60},
                {"x": 4.25, "y": 5.50, "w": 4.83, "h": 1.50, "ax1": 6.67, "ay1": 5.35, "ax2": 6.67, "ay2": 5.50, "lx": 6.85, "ly": 5.30}
            ]
        colors = [self.theme.C_ACCENT, self.theme.C_MUTED, self.theme.C_PRIMARY, self.theme.C_NAVY]

        for i, sc in enumerate(spoke_coords):
            if i >= len(spokes):
                break
            sp = spokes[i]
            title = sp.get("title", f"Domain {i+1}")
            desc = sp.get("desc", "")
            letter = sp.get("letter") or str(i + 1)
            col = sp.get("badge_color") or colors[i % len(colors)]
            conn_label = sp.get("connector_label")

            # Card
            self.add_card(slide, Inches(sc["x"]), Inches(sc["y"]), Inches(sc["w"]), Inches(sc["h"]),
                          bg_color=self.theme.C_WHITE, border_color=self.theme.C_BORDER)

            # Badge
            self.add_circle_badge(slide, sc["x"] + 0.55, sc["y"] + sc["h"] / 2.0, 0.52, letter, col, font_size_pt=16)

            # Text
            tb = slide.shapes.add_textbox(Inches(sc["x"] + 0.95), Inches(sc["y"] + 0.1), Inches(sc["w"] - 1.05), Inches(sc["h"] - 0.2))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.auto_size = MSO_AUTO_SIZE.NONE
            tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

            p1 = tf.paragraphs[0]
            p1.text = title
            p1.font.name = self.theme.FONT_HEADING
            p1.font.size = Pt(14)
            p1.font.bold = True
            p1.font.color.rgb = self.theme.C_TEXT

            p2 = tf.add_paragraph()
            p2.text = desc
            p2.font.name = self.theme.FONT_BODY
            p2.font.size = Pt(12)
            p2.font.color.rgb = self.theme.C_MUTED
            p2.space_before = Pt(2)

            # Connector Line
            self.add_line(slide, sc["ax1"], sc["ay1"], sc["ax2"], sc["ay2"], color=col, width_pt=2.0)

            # Only render connector label if explicitly specified
            if conn_label:
                tb_lbl = slide.shapes.add_textbox(Inches(sc["lx"]), Inches(sc["ly"]), Inches(1.2), Inches(0.3))
                tf_lbl = tb_lbl.text_frame
                tf_lbl.margin_left = tf_lbl.margin_right = tf_lbl.margin_top = tf_lbl.margin_bottom = 0
                pl = tf_lbl.paragraphs[0]
                pl.text = conn_label
                pl.font.name = self.theme.FONT_BODY
                pl.font.size = Pt(12)
                pl.font.italic = True
                pl.font.color.rgb = self.theme.C_MUTED

    # =========================================================================
    # COMPOSITION 4: DASHBOARD / EXECUTIVE COCKPIT (PARAMETERISED)
    # =========================================================================
    def render_dashboard_concept(self, slide, flow_steps: List[str], tabs: List[str],
                                 kpis: List[Tuple[str, str, str]],
                                 column_chart_labels: List[str], column_chart_values: List[float],
                                 line_chart_categories: List[str], line_actual: List[float], line_plan: List[float],
                                 drill_steps: List[Tuple[str, str]], platform_note: str,
                                 platform_title: Optional[str] = None, platform_disclaimer: Optional[str] = None,
                                 chart1_title: Optional[str] = None, chart2_title: Optional[str] = None,
                                 drill_title: Optional[str] = None):
        # 1. Flow Chevrons
        flow_colors = [self.theme.C_MUTED, self.theme.C_PRIMARY_DEEP, self.theme.C_NAVY, self.theme.C_PRIMARY, self.theme.C_ACCENT]
        for i, step in enumerate(flow_steps[:5]):
            x = 0.65 + i * 2.37
            ch = slide.shapes.add_shape(MSO_SHAPE.PENTAGON, Inches(x), Inches(1.85), Inches(2.28), Inches(0.48))
            ch.fill.solid()
            ch.fill.fore_color.rgb = flow_colors[i % len(flow_colors)]
            ch.line.fill.background()

            tf_c = ch.text_frame
            tf_c.vertical_anchor = MSO_ANCHOR.MIDDLE
            pc = tf_c.paragraphs[0]
            pc.text = step
            pc.alignment = PP_ALIGN.CENTER
            pc.font.name = self.theme.FONT_HEADING
            pc.font.size = Pt(12)
            pc.font.bold = True
            pc.font.color.rgb = self.theme.C_WHITE

        # 2. Main Cockpit Card (Left 62%)
        mx, my, mw, mh = 0.65, 2.45, 7.50, 4.45
        self.add_card(slide, Inches(mx), Inches(my), Inches(mw), Inches(mh),
                      bg_color=self.theme.C_WHITE, border_color=self.theme.C_BORDER)

        hbar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(mx), Inches(my), Inches(mw), Inches(0.40))
        hbar.fill.solid()
        hbar.fill.fore_color.rgb = self.theme.C_NAVY
        hbar.line.fill.background()

        tb_ht = slide.shapes.add_textbox(Inches(mx + 0.15), Inches(my), Inches(4.20), Inches(0.40))
        tf_ht = tb_ht.text_frame
        tf_ht.word_wrap = True
        tf_ht.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf_ht.paragraphs[0]
        p.text = platform_title or "Operational Analytics Cockpit"
        p.font.name = self.theme.FONT_HEADING
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = self.theme.C_WHITE

        if platform_disclaimer:
            tb_hi = slide.shapes.add_textbox(Inches(mx + mw - 3.10), Inches(my), Inches(2.95), Inches(0.40))
            tf_hi = tb_hi.text_frame
            tf_hi.word_wrap = True
            tf_hi.vertical_anchor = MSO_ANCHOR.MIDDLE
            p_hi = tf_hi.paragraphs[0]
            p_hi.text = platform_disclaimer
            p_hi.font.name = self.theme.FONT_BODY
            p_hi.font.size = Pt(12)
            p_hi.font.italic = True
            p_hi.font.color.rgb = self.theme.C_BORDER
            p_hi.alignment = PP_ALIGN.RIGHT

        # Tabs (Contained within Left Card mw=7.50)
        n_tabs = min(len(tabs), 4)
        tab_gap = 0.08
        tab_w = (mw - 0.30 - (n_tabs - 1) * tab_gap) / max(1, n_tabs)
        for i, t in enumerate(tabs[:n_tabs]):
            tx = mx + 0.15 + i * (tab_w + tab_gap)
            is_active = (i == 0)
            if is_active:
                tab_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(tx), Inches(my + 0.48), Inches(tab_w), Inches(0.30))
                tab_shape.fill.solid()
                tab_shape.fill.fore_color.rgb = self.theme.C_PRIMARY
                tab_shape.line.fill.background()

            tb_t = slide.shapes.add_textbox(Inches(tx), Inches(my + 0.48), Inches(tab_w), Inches(0.30))
            tf_t = tb_t.text_frame
            tf_t.vertical_anchor = MSO_ANCHOR.MIDDLE
            pt = tf_t.paragraphs[0]
            pt.text = t
            pt.alignment = PP_ALIGN.CENTER
            pt.font.name = self.theme.FONT_BODY
            pt.font.size = Pt(12)
            pt.font.bold = is_active
            pt.font.color.rgb = self.theme.C_WHITE if is_active else self.theme.C_MUTED

        # KPI Tiles (4 Enclosed Containers with 12pt and 22pt Typography)
        kpi_w = 1.74
        kpi_gap = 0.08
        for i, (label, val, delta) in enumerate(kpis[:4]):
            kx = mx + 0.12 + i * (kpi_w + kpi_gap)
            tile = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(kx), Inches(my + 0.88), Inches(kpi_w), Inches(0.96))
            tile.fill.solid()
            tile.fill.fore_color.rgb = self.theme.C_SURFACE
            tile.line.color.rgb = self.theme.C_BORDER
            tile.line.width = Pt(1)

            tb_k = slide.shapes.add_textbox(Inches(kx + 0.06), Inches(my + 0.90), Inches(kpi_w - 0.12), Inches(0.92))
            tf_k = tb_k.text_frame
            tf_k.word_wrap = True
            tf_k.auto_size = MSO_AUTO_SIZE.NONE
            tf_k.margin_left = tf_k.margin_right = tf_k.margin_top = tf_k.margin_bottom = 0

            p1 = tf_k.paragraphs[0]
            p1.text = label
            p1.font.name = self.theme.FONT_BODY
            p1.font.size = Pt(12)
            p1.font.bold = True
            p1.font.color.rgb = self.theme.C_MUTED

            p2 = tf_k.add_paragraph()
            p2.text = val
            p2.font.name = self.theme.FONT_HEADING
            p2.font.size = Pt(22)
            p2.font.bold = True
            p2.font.color.rgb = self.theme.C_TEXT

            p3 = tf_k.add_paragraph()
            p3.text = delta
            p3.font.name = self.theme.FONT_BODY
            p3.font.size = Pt(12)
            p3.font.bold = True
            p3.font.color.rgb = self.theme.C_PRIMARY

        # Native Chart 1 (Column Clustered with Clean Concise Categories and 12pt Labels)
        chart_data1 = CategoryChartData()
        raw_cats = column_chart_labels or ["Unit A", "Unit B", "Unit C", "Unit D", "Unit E"]
        clean_cats = []
        for lbl in raw_cats:
            s = str(lbl).replace("Plant ", "P").replace("(", "").replace(")", "").replace("Baseline", "Base").replace("Post-Pilot", "Pilot")
            clean_cats.append(s)
        chart_data1.categories = clean_cats
        chart_data1.add_series("Metric", column_chart_values or [100, 120, 150, 180, 210])

        c1 = slide.shapes.add_chart(
            XL_CHART_TYPE.COLUMN_CLUSTERED,
            Inches(mx + 0.12), Inches(my + 1.94), Inches(3.50), Inches(2.25),
            chart_data1
        ).chart
        c1.has_legend = False
        c1.has_title = True
        c1.chart_title.text_frame.text = chart1_title or "Distribution vs Target (%)"
        c1.chart_title.text_frame.paragraphs[0].font.size = Pt(14)
        c1.chart_title.text_frame.paragraphs[0].font.name = self.theme.FONT_HEADING
        c1.chart_title.text_frame.paragraphs[0].font.bold = True
        try:
            c1.category_axis.tick_labels.font.size = Pt(12)
            c1.category_axis.tick_labels.font.name = self.theme.FONT_BODY
            c1.value_axis.tick_labels.font.size = Pt(12)
            c1.value_axis.tick_labels.font.name = self.theme.FONT_BODY
        except Exception:
            pass

        # Native Chart 2 (Operating Trend Line Chart with 12pt Legend & Axes)
        chart_data2 = CategoryChartData()
        chart_data2.categories = line_chart_categories or ["T1", "T2", "T3", "T4", "T5", "T6"]
        chart_data2.add_series("Actual", line_actual or [90, 95, 100, 110, 125, 140])
        chart_data2.add_series("Plan", line_plan or [85, 90, 95, 100, 105, 110])

        c2 = slide.shapes.add_chart(
            XL_CHART_TYPE.LINE,
            Inches(mx + 3.82), Inches(my + 1.94), Inches(3.50), Inches(2.25),
            chart_data2
        ).chart
        c2.has_legend = True
        c2.legend.position = XL_LEGEND_POSITION.BOTTOM
        c2.legend.include_in_layout = False
        try:
            c2.legend.font.size = Pt(12)
            c2.legend.font.name = self.theme.FONT_BODY
        except Exception:
            pass
        c2.has_title = True
        c2.chart_title.text_frame.text = chart2_title or "Operating Trend vs Target"
        c2.chart_title.text_frame.paragraphs[0].font.size = Pt(14)
        c2.chart_title.text_frame.paragraphs[0].font.name = self.theme.FONT_HEADING
        c2.chart_title.text_frame.paragraphs[0].font.bold = True
        try:
            c2.category_axis.tick_labels.font.size = Pt(12)
            c2.category_axis.tick_labels.font.name = self.theme.FONT_BODY
            c2.value_axis.tick_labels.font.size = Pt(12)
            c2.value_axis.tick_labels.font.name = self.theme.FONT_BODY
        except Exception:
            pass

        # 3. AI Copilot / Drilldown Card (Right 38%, Enclosed & Balanced)
        rx, ry, rw, rh = 8.35, 2.45, 4.33, 4.45
        self.add_card(slide, Inches(rx), Inches(ry), Inches(rw), Inches(rh),
                      bg_color=self.theme.C_WHITE, border_color=self.theme.C_BORDER)

        r_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(rx), Inches(ry), Inches(rw), Inches(0.40))
        r_bar.fill.solid()
        r_bar.fill.fore_color.rgb = self.theme.C_PRIMARY
        r_bar.line.fill.background()

        tb_dt = slide.shapes.add_textbox(Inches(rx + 0.15), Inches(ry), Inches(rw - 0.30), Inches(0.40))
        tf_dt = tb_dt.text_frame
        tf_dt.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_dt = tf_dt.paragraphs[0]
        p_dt.text = drill_title or "Root Cause Analysis Sequence"
        p_dt.font.name = self.theme.FONT_HEADING
        p_dt.font.size = Pt(14)
        p_dt.font.bold = True
        p_dt.font.color.rgb = self.theme.C_WHITE

        self.add_line(slide, rx + 0.35, ry + 1.0, rx + 0.35, ry + 3.8, color=self.theme.C_PRIMARY, width_pt=1.5)

        for i, (st_name, st_desc) in enumerate(drill_steps[:4]):
            y = ry + 0.62 + i * 0.88
            self.add_circle_badge(slide, rx + 0.35, y + 0.28, 0.40, str(i + 1), self.theme.C_PRIMARY, font_size_pt=14)

            tb_s = slide.shapes.add_textbox(Inches(rx + 0.70), Inches(y), Inches(rw - 0.85), Inches(0.80))
            tf_s = tb_s.text_frame
            tf_s.word_wrap = True
            tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0

            p1 = tf_s.paragraphs[0]
            p1.text = st_name
            p1.font.name = self.theme.FONT_HEADING
            p1.font.size = Pt(14)
            p1.font.bold = True
            p1.font.color.rgb = self.theme.C_TEXT

            p2 = tf_s.add_paragraph()
            p2.text = st_desc
            p2.font.name = self.theme.FONT_BODY
            p2.font.size = Pt(12)
            p2.font.color.rgb = self.theme.C_MUTED
            p2.space_before = Pt(2)
            p2.font.color.rgb = self.theme.C_MUTED

    # =========================================================================
    # COMPOSITION 5: MATRIX GRID (LEVELS X DIMENSIONS)
    # =========================================================================
    def render_matrix_grid(self, slide, col_headers: List[str], row_headers: List[Tuple[str, str, RGBColor]],
                           matrix_cells: List[List[str]], caveat_text: str, confirmed_caps: List[str],
                           confirmed_title: Optional[str] = None):
        col_w = 2.85
        for j, ch in enumerate(col_headers[:3]):
            tb = slide.shapes.add_textbox(Inches(4.1 + j * col_w), Inches(1.80), Inches(col_w - 0.1), Inches(0.42))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.auto_size = MSO_AUTO_SIZE.NONE
            tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = ch.upper()
            p.font.name = self.theme.FONT_SEMIBOLD
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = self.theme.C_PRIMARY

        for i, (r_name, r_sub, r_col) in enumerate(row_headers[:3]):
            y = 2.22 + i * 1.22
            row_h = 1.15

            # Left Row Header Card
            self.add_card(slide, Inches(0.65), Inches(y), Inches(3.2), Inches(row_h),
                          bg_color=r_col, border_color=None)

            tb_r = slide.shapes.add_textbox(Inches(0.8), Inches(y + 0.12), Inches(2.9), Inches(row_h - 0.24))
            tf_r = tb_r.text_frame
            tf_r.word_wrap = True
            tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

            pr1 = tf_r.paragraphs[0]
            pr1.text = r_name
            pr1.font.name = self.theme.FONT_HEADING
            pr1.font.size = Pt(14)
            pr1.font.bold = True
            pr1.font.color.rgb = self.theme.C_WHITE

            pr2 = tf_r.add_paragraph()
            pr2.text = r_sub
            pr2.font.name = self.theme.FONT_BODY
            pr2.font.size = Pt(12)
            pr2.font.color.rgb = self.theme.C_SURFACE
            pr2.space_before = Pt(3)

            # Cells
            cells_in_row = matrix_cells[i] if i < len(matrix_cells) else []
            for j, c_text in enumerate(cells_in_row[:3]):
                cx = 4.1 + j * col_w
                self.add_card(slide, Inches(cx), Inches(y), Inches(col_w - 0.1), Inches(row_h),
                              bg_color=self.theme.C_WHITE, border_color=self.theme.C_BORDER, is_dashed=True)

                tb_c = slide.shapes.add_textbox(Inches(cx + 0.15), Inches(y + 0.12), Inches(col_w - 0.4), Inches(row_h - 0.24))
                tf_c = tb_c.text_frame
                tf_c.word_wrap = True
                tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
                pc = tf_c.paragraphs[0]
                pc.text = c_text
                pc.font.name = self.theme.FONT_BODY
                pc.font.size = Pt(12)
                pc.font.color.rgb = self.theme.C_TEXT

        # Bottom Confirmed Strip
        band = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), Inches(6.05), Inches(12.03), Inches(0.75))
        band.fill.solid()
        band.fill.fore_color.rgb = self.theme.C_SURFACE
        band.line.color.rgb = self.theme.C_PRIMARY
        band.line.width = Pt(1)

        tb_bt = slide.shapes.add_textbox(Inches(0.85), Inches(6.05), Inches(2.8), Inches(0.75))
        set_text(tb_bt, confirmed_title or "Verified Architectural Baseline", face="Inter", weight="bold", pt=12.0, color="0070C0", align="left", anchor="middle", pad_in=0.0)

        for i, cap in enumerate(confirmed_caps[:4]):
            bx = 3.75 + i * 2.2
            self.add_circle_badge(slide, bx + 0.1, 6.42, 0.22, "✓", self.theme.C_PRIMARY, font_size_pt=12)

            tb_cp = slide.shapes.add_textbox(Inches(bx + 0.28), Inches(6.05), Inches(1.85), Inches(0.75))
            set_text(tb_cp, cap, face="Inter", weight="regular", pt=12.0, color="0B192C", align="left", anchor="middle", pad_in=0.0)

    # =========================================================================
    # COMPOSITION 6: NUMBERED STEP BLOCKS + DELIVERABLES BAND
    # =========================================================================
    def render_numbered_blocks(self, slide, steps: List[Tuple[str, List[str]]], caveat_text: str, deliverables: List[str]):
        for i, (title, bullets) in enumerate(steps[:4]):
            px = 0.65 + i * 3.05
            tb_n = slide.shapes.add_textbox(Inches(px), Inches(1.9), Inches(1.2), Inches(0.8))
            tf_n = tb_n.text_frame
            pn = tf_n.paragraphs[0]
            pn.text = f"0{i+1}"
            pn.font.name = self.theme.FONT_HEADING
            pn.font.size = Pt(36)
            pn.font.bold = True
            pn.font.color.rgb = self.theme.C_PRIMARY

            self.add_card(slide, Inches(px), Inches(2.75), Inches(2.88), Inches(2.15),
                          bg_color=self.theme.C_WHITE, border_color=self.theme.C_BORDER)

            tb_c = slide.shapes.add_textbox(Inches(px + 0.15), Inches(2.85), Inches(2.58), Inches(1.95))
            tf_c = tb_c.text_frame
            tf_c.word_wrap = True
            tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0

            p_st = tf_c.paragraphs[0]
            p_st.text = title
            p_st.font.name = self.theme.FONT_HEADING
            p_st.font.size = Pt(14)
            p_st.font.bold = True
            p_st.font.color.rgb = self.theme.C_TEXT

            bullet_list = bullets if isinstance(bullets, list) else [bullets]
            for b in bullet_list:
                p_b = tf_c.add_paragraph()
                p_b.text = f"• {b}"
                p_b.font.name = self.theme.FONT_BODY
                p_b.font.size = Pt(12)
                p_b.font.color.rgb = self.theme.C_MUTED
                p_b.space_before = Pt(3)

        # Bottom deliverables band
        band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.65), Inches(5.1), Inches(12.03), Inches(0.8))
        band.fill.solid()
        band.fill.fore_color.rgb = self.theme.C_SURFACE
        band.line.color.rgb = self.theme.C_BORDER

        tb_dt = slide.shapes.add_textbox(Inches(0.85), Inches(5.1), Inches(2.2), Inches(0.8))
        set_text(tb_dt, "Key Deliverables", face="Inter", weight="bold", pt=12.0, color="0B192C", align="left", anchor="middle", pad_in=0.0)

        for i, d in enumerate(deliverables[:4]):
            dx = 3.2 + i * 2.35
            self.add_circle_badge(slide, dx + 0.1, 5.5, 0.22, "✓", self.theme.C_PRIMARY, font_size_pt=12)

            tb_d = slide.shapes.add_textbox(Inches(dx + 0.28), Inches(5.1), Inches(1.95), Inches(0.8))
            set_text(tb_d, d, face="Inter", weight="regular", pt=12.0, color="0B192C", align="left", anchor="middle", pad_in=0.0)

    # =========================================================================
    # COMPOSITION 7: STEP LINE / DATA CUTOVER PIPELINE (Don Norman Process Flow)
    # =========================================================================
    def render_step_line(self, slide, steps: List[Tuple[str, str]], deliverables: List[str], caveat_text: str):
        """
        Don Norman Human-Centered Process Flow:
        Renders substantial, full-height vertical workflow cards side-by-side.
        Natural spatial mapping (Left-to-Right sequence), zero dead white space,
        integrated deliverables, and strict >= 12pt discrete integer typography.
        """
        n_steps = max(1, min(len(steps), 5))
        total_w = 12.03  # from x=0.65 to 12.68
        gutter = 0.20
        card_w = (total_w - (n_steps - 1) * gutter) / n_steps
        card_h = 4.12  # from y=1.95 to 6.07
        top_y = 1.95

        for i, step_data in enumerate(steps[:n_steps]):
            title = step_data[0] if isinstance(step_data, (tuple, list)) else str(step_data)
            desc = step_data[1] if isinstance(step_data, (tuple, list)) and len(step_data) > 1 else ""

            cx = 0.65 + i * (card_w + gutter)

            # Substantial vertical card container filling canvas
            self.add_card(slide, Inches(cx), Inches(top_y), Inches(card_w), Inches(card_h),
                          bg_color=self.theme.C_WHITE, border_color=self.theme.C_BORDER)

            # Card Header Pill / Top Accent Strip with Step Badge
            badge_y = top_y + 0.35
            badge_x = cx + card_w / 2.0
            self.add_circle_badge(slide, badge_x, badge_y, 0.44, str(i + 1), self.theme.C_PRIMARY, font_size_pt=14)

            # Directional Connector Arrow linking to next step
            if i < n_steps - 1:
                conn_x1 = cx + card_w + 0.02
                conn_x2 = cx + card_w + gutter - 0.02
                self.add_line(slide, conn_x1, badge_y, conn_x2, badge_y, color=self.theme.C_PRIMARY, width_pt=2.0)

            # Step Title Textbox (14pt Bold)
            tb_t = slide.shapes.add_textbox(Inches(cx + 0.10), Inches(top_y + 0.70), Inches(card_w - 0.20), Inches(0.68))
            tf_t = tb_t.text_frame
            tf_t.word_wrap = True
            tf_t.auto_size = MSO_AUTO_SIZE.NONE
            tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
            pt = tf_t.paragraphs[0]
            pt.text = title
            pt.alignment = PP_ALIGN.CENTER
            pt.font.name = self.theme.FONT_HEADING
            pt.font.size = Pt(14)
            pt.font.bold = True
            pt.font.color.rgb = self.theme.C_TEXT

            # Step Narrative Description (12pt Regular)
            tb_d = slide.shapes.add_textbox(Inches(cx + 0.12), Inches(top_y + 1.45), Inches(card_w - 0.24), Inches(1.45))
            tf_d = tb_d.text_frame
            tf_d.word_wrap = True
            tf_d.auto_size = MSO_AUTO_SIZE.NONE
            tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
            pd = tf_d.paragraphs[0]
            pd.text = desc
            pd.alignment = PP_ALIGN.CENTER
            pd.font.name = self.theme.FONT_BODY
            pd.font.size = Pt(12)
            pd.font.color.rgb = self.theme.C_MUTED

            # Integrated Deliverable Container at Base of Card
            if i < len(deliverables):
                deliv_box_y = top_y + 3.02
                deliv_box_h = 0.96
                deliv_w = card_w - 0.24
                # Subtle surface pill container
                self.add_card(slide, Inches(cx + 0.12), Inches(deliv_box_y), Inches(deliv_w), Inches(deliv_box_h),
                              bg_color=self.theme.C_SURFACE, border_color=self.theme.C_BORDER)

                tb_dl = slide.shapes.add_textbox(Inches(cx + 0.14), Inches(deliv_box_y + 0.08), Inches(deliv_w - 0.04), Inches(deliv_box_h - 0.12))
                tf_dl = tb_dl.text_frame
                tf_dl.word_wrap = True
                tf_dl.auto_size = MSO_AUTO_SIZE.NONE
                tf_dl.margin_left = tf_dl.margin_right = tf_dl.margin_top = tf_dl.margin_bottom = 0

                p_dl1 = tf_dl.paragraphs[0]
                p_dl1.text = "DELIVERABLE"
                p_dl1.alignment = PP_ALIGN.CENTER
                p_dl1.font.name = self.theme.FONT_HEADING
                p_dl1.font.size = Pt(12)
                p_dl1.font.bold = True
                p_dl1.font.color.rgb = self.theme.C_PRIMARY

                p_dl2 = tf_dl.add_paragraph()
                p_dl2.text = str(deliverables[i])
                p_dl2.alignment = PP_ALIGN.CENTER
                p_dl2.font.name = self.theme.FONT_BODY
                p_dl2.font.size = Pt(12)
                p_dl2.font.bold = True
                p_dl2.font.color.rgb = self.theme.C_TEXT
                p_dl2.space_before = Pt(2)

        # Bottom Executive Principle Banner (Eliminates any bottom void)
        if caveat_text:
            banner_y = top_y + card_h + 0.10
            self.add_card(slide, Inches(0.65), Inches(banner_y), Inches(total_w), Inches(0.52),
                          bg_color=self.theme.C_SURFACE, border_color=self.theme.C_BORDER)
            tb_c = slide.shapes.add_textbox(Inches(0.85), Inches(banner_y + 0.03), Inches(total_w - 0.40), Inches(0.46))
            tf_c = tb_c.text_frame
            tf_c.word_wrap = True
            tf_c.vertical_anchor = MSO_ANCHOR.MIDDLE
            p_cv = tf_c.paragraphs[0]
            p_cv.text = f"Operational Standard: {caveat_text}"
            p_cv.font.name = self.theme.FONT_BODY
            p_cv.font.size = Pt(12)
            p_cv.font.color.rgb = self.theme.C_MUTED

    # =========================================================================
    # COMPOSITION 8: FLOW WITH ACTION STRIP & LEGEND
    # =========================================================================
    def render_flow_with_actions(self, slide, flow_boxes: List[Tuple[str, str, RGBColor]],
                                 actions: List[str], legend_items: List[Tuple[RGBColor, str]], caveat_text: str):
        total_w = 12.03  # from x=0.65 to 12.68
        
        # 1. Flow boxes at top (y=1.95, h=1.60)
        n_flow = max(1, min(len(flow_boxes), 6))
        flow_gap = 0.22
        box_w = (total_w - (n_flow - 1) * flow_gap) / n_flow

        for i, (b_title, b_sub, b_col) in enumerate(flow_boxes[:6]):
            bx = 0.65 + i * (box_w + flow_gap)
            self.add_card(slide, Inches(bx), Inches(1.95), Inches(box_w), Inches(1.60),
                          bg_color=self.theme.C_WHITE, border_color=b_col)

            stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(bx), Inches(1.95), Inches(box_w), Inches(0.08))
            stripe.fill.solid()
            stripe.fill.fore_color.rgb = b_col
            stripe.line.fill.background()

            tb = slide.shapes.add_textbox(Inches(bx + 0.08), Inches(2.10), Inches(box_w - 0.16), Inches(1.35))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.auto_size = MSO_AUTO_SIZE.NONE
            tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

            p1 = tf.paragraphs[0]
            p1.text = b_title
            p1.font.name = self.theme.FONT_HEADING
            p1.font.size = Pt(12)
            p1.font.bold = True
            p1.font.color.rgb = self.theme.C_TEXT

            p2 = tf.add_paragraph()
            p2.text = b_sub
            p2.font.name = self.theme.FONT_BODY
            p2.font.size = Pt(12)
            p2.font.color.rgb = self.theme.C_MUTED
            p2.space_before = Pt(2)

            if i < n_flow - 1:
                ax = bx + box_w + 0.02
                arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(ax), Inches(2.65), Inches(0.18), Inches(0.22))
                arrow.fill.solid()
                arrow.fill.fore_color.rgb = self.theme.C_MUTED
                arrow.line.fill.background()

        # 2. Action strip (y=3.75, h=1.45)
        n_act = max(1, min(len(actions), 6))
        act_gap = 0.22
        act_w = (total_w - (n_act - 1) * act_gap) / n_act
        for i, act in enumerate(actions[:6]):
            bx = 0.65 + i * (act_w + act_gap)
            self.add_card(slide, Inches(bx), Inches(3.75), Inches(act_w), Inches(1.45),
                          bg_color=self.theme.C_SURFACE, border_color=self.theme.C_BORDER)
            tb_a = slide.shapes.add_textbox(Inches(bx + 0.12), Inches(3.83), Inches(act_w - 0.24), Inches(1.28))
            tf_a = tb_a.text_frame
            tf_a.word_wrap = True
            tf_a.auto_size = MSO_AUTO_SIZE.NONE
            tf_a.margin_left = tf_a.margin_right = tf_a.margin_top = tf_a.margin_bottom = 0
            pa = tf_a.paragraphs[0]
            pa.text = f"Action {i+1}: {act}"
            pa.font.name = self.theme.FONT_BODY
            pa.font.size = Pt(12)
            pa.font.color.rgb = self.theme.C_TEXT

        # 3. Legend (y=5.35)
        n_leg = max(1, len(legend_items))
        leg_slot_w = total_w / n_leg
        for i, (l_col, l_text) in enumerate(legend_items):
            lx = 0.65 + i * leg_slot_w
            dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(lx), Inches(5.35), Inches(0.16), Inches(0.16))
            dot.fill.solid()
            if isinstance(l_col, str):
                h = l_col.lstrip("#")
                dot.fill.fore_color.rgb = RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
            else:
                dot.fill.fore_color.rgb = l_col
            dot.line.fill.background()

            tb_l = slide.shapes.add_textbox(Inches(lx + 0.25), Inches(5.30), Inches(leg_slot_w - 0.35), Inches(0.32))
            tf_l = tb_l.text_frame
            tf_l.word_wrap = True
            tf_l.auto_size = MSO_AUTO_SIZE.NONE
            tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
            pl = tf_l.paragraphs[0]
            pl.text = l_text
            pl.font.name = self.theme.FONT_BODY
            pl.font.size = Pt(12)
            pl.font.color.rgb = self.theme.C_MUTED

        # 4. Caveat text at bottom if present
        if caveat_text:
            tb_c = slide.shapes.add_textbox(Inches(0.65), Inches(5.85), Inches(total_w), Inches(0.45))
            tf_c = tb_c.text_frame
            tf_c.word_wrap = True
            tf_c.auto_size = MSO_AUTO_SIZE.NONE
            tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
            pc = tf_c.paragraphs[0]
            pc.text = caveat_text
            pc.font.name = self.theme.FONT_BODY
            pc.font.size = Pt(12)
            pc.font.color.rgb = self.theme.C_MUTED

    # =========================================================================
    # COMPOSITION 9: ROADMAP ROWS (PHASES OVER TIME)
    # =========================================================================
    def render_roadmap_rows(self, slide, phases: List[Tuple[str, str]], future_readiness_title: str, future_readiness_desc: str):
        for h, x, w in [("PHASE", 0.65, 2.5), ("SEQUENCE (INDICATIVE)", 3.45, 3.4), ("KEY ACTIVITIES", 7.2, 5.4)]:
            tb = slide.shapes.add_textbox(Inches(x), Inches(1.85), Inches(w), Inches(0.25))
            tf = tb.text_frame
            p = tf.paragraphs[0]
            p.text = h
            p.font.name = self.theme.FONT_SEMIBOLD
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = self.theme.C_MUTED

        for i, (p_name, p_act) in enumerate(phases[:5]):
            y = 2.15 + i * 0.77
            self.add_line(slide, 0.65, y, 12.68, y, color=self.theme.C_BORDER, width_pt=1.25)

            tb_n = slide.shapes.add_textbox(Inches(0.65), Inches(y + 0.03), Inches(2.75), Inches(0.7))
            set_text(tb_n, p_name, face="Inter", weight="bold", pt=12.0, color="0B192C", align="left", anchor="middle", pad_in=0.0)

            bx = 3.45 + i * 0.55
            bar_col = self.theme.C_NAVY if i == 4 else self.theme.C_PRIMARY
            bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(bx), Inches(y + 0.17), Inches(1.1), Inches(0.4))
            bar.fill.solid()
            bar.fill.fore_color.rgb = bar_col
            bar.line.fill.background()
            set_text(bar, f"Phase {i+1}", face="Inter", weight="bold", pt=12.0, color="FFFFFF", align="center", anchor="middle", pad_in=0.05)

            tb_a = slide.shapes.add_textbox(Inches(7.2), Inches(y + 0.03), Inches(5.4), Inches(0.7))
            set_text(tb_a, p_act, face="Inter", weight="regular", pt=12.0, color="0B192C", align="left", anchor="middle", pad_in=0.0)

        # Future readiness callout
        self.add_card(slide, Inches(0.65), Inches(6.05), Inches(12.03), Inches(0.85),
                      bg_color=self.theme.C_SURFACE, border_color=self.theme.C_BORDER)

        tb_ft = slide.shapes.add_textbox(Inches(0.9), Inches(6.05), Inches(3.4), Inches(0.85))
        set_text(tb_ft, future_readiness_title or "Architecture Currency", face="Inter", weight="semibold", pt=12.0, color="1E3E62", align="left", anchor="middle", pad_in=0.0)

        tb_fd = slide.shapes.add_textbox(Inches(4.5), Inches(6.05), Inches(8.0), Inches(0.85))
        set_text(tb_fd, future_readiness_desc, face="Inter", weight="regular", pt=12.0, color="4F6F8F", align="left", anchor="middle", pad_in=0.0)

    # =========================================================================
    # COMPOSITION 9B: PHASE-WISE CONCURRENT DELIVERY TABLE (SOW PROTECTION)
    # =========================================================================
    def render_phase_wise_delivery_table(
        self,
        slide,
        left: float = 0.65,
        top: float = 1.76,
        width: float = 7.80,
        height: float = 5.04,
        header_title: str = "PHASE WISE DELIVERY PLAN",
        phases: Optional[List[Dict[str, Any]]] = None,
        col_widths: Optional[List[float]] = None,
        border_hex: str = "0070C0"
    ):
        """
        Renders a native executive Phase-Wise Concurrent Delivery Plan table.
        Protects SOW scope and revenue by proving why the multi-month duration is justified
        through overlapping, concurrent delivery across all scoped products rather than sequential silos.
        """
        if phases is None:
            phases = [
                {
                    "phase_name": "Phase 1",
                    "product_scope": "MES + DMS",
                    "activities": [
                        ("Weeks 1-2", "Onsite Requirement Gathering"),
                        ("Weeks 2-6", "System Configuration"),
                        ("Weeks 7-8", "UAT"),
                        ("Weeks 9", "Go Live"),
                    ]
                },
                {
                    "phase_name": "Phase 2",
                    "product_scope": "SAP Integrations",
                    "activities": [
                        ("Weeks 3-4", "Onsite Requirement Gathering"),
                        ("Weeks 4-8", "Interface Developments"),
                        ("Weeks 9-10", "UAT"),
                        ("Weeks 11", "Go Live"),
                    ]
                },
                {
                    "phase_name": "Phase 3",
                    "product_scope": "Track & Trace",
                    "activities": [
                        ("Weeks 12-13", "Track & Trace Setup / Alignment"),
                        ("Weeks 13-14", "System Configuration"),
                        ("Weeks 14-15", "UAT + Go Live"),
                        ("Weeks 16 onwards", "1 Month Hypercare Support"),
                    ]
                }
            ]

        total_act_rows = sum(len(p.get("activities", [])) for p in phases)
        n_rows = total_act_rows + 1  # +1 for header
        n_cols = 4

        table_shape = slide.shapes.add_table(n_rows, n_cols, Inches(left), Inches(top), Inches(width), Inches(height))
        table = table_shape.table

        # Default column width ratios
        if col_widths and len(col_widths) == n_cols:
            for c_idx, cw in enumerate(col_widths):
                table.columns[c_idx].width = Inches(cw)
        else:
            w_ratios = [0.165, 0.235, 0.22, 0.38]
            for c_idx, r in enumerate(w_ratios):
                table.columns[c_idx].width = Inches(width * r)

        # Header row merged across all 4 cols
        table.cell(0, 0).merge(table.cell(0, 3))
        h_cell = table.cell(0, 0)
        h_cell.fill.solid()
        h_cell.fill.fore_color.rgb = self.theme.C_WHITE
        h_cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_h = h_cell.text_frame
        tf_h.word_wrap = True
        p_h = tf_h.paragraphs[0]
        p_h.text = header_title
        p_h.font.name = self.theme.FONT_HEADING
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = self.theme.C_NAVY
        p_h.alignment = PP_ALIGN.CENTER

        from pptx.oxml import parse_xml
        def apply_border(c, col_hex):
            tcPr = c._tc.get_or_add_tcPr()
            for b_name in ["lnL", "lnR", "lnT", "lnB"]:
                xml = f'<a:{b_name} xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" w="12700"><a:solidFill><a:srgbClr val="{col_hex}"/></a:solidFill></a:{b_name}>'
                tcPr.append(parse_xml(xml))

        apply_border(h_cell, border_hex)

        curr_r = 1
        for p_idx, phase in enumerate(phases):
            acts = phase.get("activities", [])
            p_len = len(acts)
            if p_len == 0:
                continue
            start_r = curr_r
            end_r = curr_r + p_len - 1

            # Populate activity rows first
            for act_idx, (wks, act_desc) in enumerate(acts):
                row_num = curr_r + act_idx
                # Col 2 (Timeline/Weeks)
                c_w = table.cell(row_num, 2)
                c_w.fill.solid()
                c_w.fill.fore_color.rgb = self.theme.C_SURFACE
                c_w.vertical_anchor = MSO_ANCHOR.MIDDLE
                tf_w = c_w.text_frame
                tf_w.word_wrap = True
                tf_w.margin_left = tf_w.margin_right = Inches(0.08)
                p_w = tf_w.paragraphs[0]
                p_w.text = wks
                p_w.font.name = self.theme.FONT_HEADING
                p_w.font.size = Pt(12)
                p_w.font.bold = True
                p_w.font.color.rgb = self.theme.C_NAVY
                p_w.alignment = PP_ALIGN.CENTER
                apply_border(c_w, border_hex)

                # Col 3 (Activity/Deliverable)
                c_a = table.cell(row_num, 3)
                c_a.fill.solid()
                c_a.fill.fore_color.rgb = self.theme.C_WHITE
                c_a.vertical_anchor = MSO_ANCHOR.MIDDLE
                tf_a = c_a.text_frame
                tf_a.word_wrap = True
                tf_a.margin_left = tf_a.margin_right = Inches(0.12)
                p_a = tf_a.paragraphs[0]
                p_a.text = act_desc
                p_a.font.name = self.theme.FONT_BODY
                p_a.font.size = Pt(12)
                is_milestone = "Go Live" in act_desc or "Hypercare" in act_desc
                p_a.font.bold = is_milestone
                p_a.font.color.rgb = self.theme.C_PRIMARY if is_milestone else self.theme.C_TEXT
                p_a.alignment = PP_ALIGN.LEFT
                apply_border(c_a, border_hex)

            # Merge Phase col
            if p_len > 1:
                table.cell(start_r, 0).merge(table.cell(end_r, 0))
            c_p = table.cell(start_r, 0)
            c_p.fill.solid()
            c_p.fill.fore_color.rgb = self.theme.C_NAVY
            c_p.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf_p = c_p.text_frame
            tf_p.word_wrap = True
            p_p = tf_p.paragraphs[0]
            p_p.text = phase.get("phase_name", f"Phase {p_idx+1}")
            p_p.font.name = self.theme.FONT_HEADING
            p_p.font.size = Pt(12)
            p_p.font.bold = True
            p_p.font.color.rgb = self.theme.C_WHITE
            p_p.alignment = PP_ALIGN.CENTER
            apply_border(c_p, border_hex)

            # Merge Product col
            if p_len > 1:
                table.cell(start_r, 1).merge(table.cell(end_r, 1))
            c_prod = table.cell(start_r, 1)
            c_prod.fill.solid()
            c_prod.fill.fore_color.rgb = self.theme.C_WHITE
            c_prod.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf_prod = c_prod.text_frame
            tf_prod.word_wrap = True
            tf_prod.margin_left = tf_prod.margin_right = Inches(0.08)
            p_prod = tf_prod.paragraphs[0]
            p_prod.text = phase.get("product_scope", "")
            p_prod.font.name = self.theme.FONT_HEADING
            p_prod.font.size = Pt(12)
            p_prod.font.bold = True
            p_prod.font.color.rgb = self.theme.C_TEXT
            p_prod.alignment = PP_ALIGN.CENTER
            apply_border(c_prod, border_hex)

            curr_r += p_len

        # Apply borders to all cells in grid
        from pptx.oxml import parse_xml
        for row in table.rows:
            for cell in row.cells:
                tcPr = cell._tc.get_or_add_tcPr()
                for b_name in ["lnL", "lnR", "lnT", "lnB"]:
                    xml = f'<a:{b_name} xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" w="12700"><a:solidFill><a:srgbClr val="{border_hex}"/></a:solidFill></a:{b_name}>'
                    tcPr.append(parse_xml(xml))

        return table_shape

    # =========================================================================
    # COMPOSITION 10: ROLES AND TERMS (DUAL NATIVE TABLES)
    # =========================================================================
    def render_roles_and_terms(self, slide, commercial_rows: List[Tuple[str, str]],
                               resource_rows: List[Tuple[str, str, str]], terms_list: List[Tuple[str, str]],
                               sec_a_title: str = "A   Commercial proposal",
                               sec_b_title: str = "B   Proposed manpower resources",
                               sec_c_title: str = "C   Terms & conditions",
                               table_a_headers: Optional[List[str]] = None,
                               table_b_headers: Optional[List[str]] = None):
        # Section A Title
        tb_a = slide.shapes.add_textbox(Inches(0.65), Inches(1.5), Inches(5.3), Inches(0.35))
        tf_a = tb_a.text_frame
        pa = tf_a.paragraphs[0]
        pa.text = sec_a_title
        pa.font.name = self.theme.FONT_HEADING
        pa.font.size = Pt(14)
        pa.font.bold = True
        pa.font.color.rgb = self.theme.C_PRIMARY

        # Table A
        t_a = slide.shapes.add_table(len(commercial_rows) + 1, 2, Inches(0.65), Inches(1.9), Inches(5.3), Inches(0.43 * (len(commercial_rows) + 1))).table
        t_a.columns[0].width = Inches(3.0)
        t_a.columns[1].width = Inches(2.3)

        a_headers = table_a_headers or ["Item", "Amount"]
        for c_idx, h_text in enumerate(a_headers[:2]):
            cell = t_a.cell(0, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = self.theme.C_NAVY
            cell.text = h_text
            p = cell.text_frame.paragraphs[0]
            p.font.name = self.theme.FONT_HEADING
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = self.theme.C_WHITE

        for r_idx, (item, amt) in enumerate(commercial_rows):
            cell0 = t_a.cell(r_idx + 1, 0)
            cell0.fill.solid()
            cell0.fill.fore_color.rgb = self.theme.C_WHITE
            cell0.text = item
            p0 = cell0.text_frame.paragraphs[0]
            p0.font.name = self.theme.FONT_BODY
            p0.font.size = Pt(12)
            p0.font.color.rgb = self.theme.C_TEXT

            cell1 = t_a.cell(r_idx + 1, 1)
            cell1.fill.solid()
            cell1.fill.fore_color.rgb = self.theme.C_WHITE
            cell1.text = amt
            p1 = cell1.text_frame.paragraphs[0]
            p1.font.name = self.theme.FONT_HEADING
            p1.font.size = Pt(12)
            p1.font.bold = True
            p1.font.color.rgb = self.theme.C_ACCENT

        # Section B Title
        tb_b = slide.shapes.add_textbox(Inches(6.2), Inches(1.5), Inches(6.5), Inches(0.35))
        tf_b = tb_b.text_frame
        pb = tf_b.paragraphs[0]
        pb.text = sec_b_title
        pb.font.name = self.theme.FONT_HEADING
        pb.font.size = Pt(14)
        pb.font.bold = True
        pb.font.color.rgb = self.theme.C_PRIMARY

        # Table B
        t_b = slide.shapes.add_table(len(resource_rows) + 1, 3, Inches(6.2), Inches(1.9), Inches(6.48), Inches(0.43 * (len(resource_rows) + 1))).table
        t_b.columns[0].width = Inches(2.5)
        t_b.columns[1].width = Inches(2.88)
        t_b.columns[2].width = Inches(1.1)

        b_headers = table_b_headers or ["Role", "Key responsibility", "Allocation"]
        for c_idx, h_text in enumerate(b_headers[:3]):
            cell = t_b.cell(0, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = self.theme.C_NAVY
            cell.text = h_text
            p = cell.text_frame.paragraphs[0]
            p.font.name = self.theme.FONT_HEADING
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = self.theme.C_WHITE

        for r_idx, (role, resp, alloc) in enumerate(resource_rows):
            c0 = t_b.cell(r_idx + 1, 0)
            c0.fill.solid()
            c0.fill.fore_color.rgb = self.theme.C_WHITE
            c0.text = role
            p0 = c0.text_frame.paragraphs[0]
            p0.font.name = self.theme.FONT_HEADING
            p0.font.size = Pt(12)
            p0.font.bold = True
            p0.font.color.rgb = self.theme.C_TEXT

            c1 = t_b.cell(r_idx + 1, 1)
            c1.fill.solid()
            c1.fill.fore_color.rgb = self.theme.C_WHITE
            c1.text = resp
            p1 = c1.text_frame.paragraphs[0]
            p1.font.name = self.theme.FONT_BODY
            p1.font.size = Pt(12)
            p1.font.color.rgb = self.theme.C_TEXT

            c2 = t_b.cell(r_idx + 1, 2)
            c2.fill.solid()
            c2.fill.fore_color.rgb = self.theme.C_WHITE
            c2.text = alloc
            p2 = c2.text_frame.paragraphs[0]
            p2.font.name = self.theme.FONT_HEADING
            p2.font.size = Pt(12)
            p2.font.bold = True
            p2.font.color.rgb = self.theme.C_ACCENT

        # Section C Title
        tb_c = slide.shapes.add_textbox(Inches(0.65), Inches(5.05), Inches(6.0), Inches(0.35))
        tf_c = tb_c.text_frame
        pc = tf_c.paragraphs[0]
        pc.text = sec_c_title
        pc.font.name = self.theme.FONT_HEADING
        pc.font.size = Pt(14)
        pc.font.bold = True
        pc.font.color.rgb = self.theme.C_PRIMARY

        # 2-column terms
        col_split = max(1, len(terms_list) // 2)
        for c in range(2):
            c_terms = terms_list[c * col_split : (c + 1) * col_split]
            tb_t = slide.shapes.add_textbox(Inches(0.65 + c * 6.2), Inches(5.45), Inches(5.85), Inches(1.55))
            tf_t = tb_t.text_frame
            tf_t.word_wrap = True
            tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0

            for k, (t_title, t_desc) in enumerate(c_terms):
                p = tf_t.paragraphs[0] if k == 0 else tf_t.add_paragraph()
                r1 = p.add_run()
                r1.text = f"{t_title}: "
                r1.font.name = self.theme.FONT_SEMIBOLD
                r1.font.size = Pt(12)
                r1.font.bold = True
                r1.font.color.rgb = self.theme.C_TEXT

                r2 = p.add_run()
                r2.text = t_desc
                r2.font.name = self.theme.FONT_BODY
                r2.font.size = Pt(12)
                r2.font.color.rgb = self.theme.C_MUTED

    # =========================================================================
    # COMPOSITION 10: BENCHMARK COMPARISON TABLE
    # =========================================================================
    def render_benchmark_table(self, slide, headers: List[str], rows: List[List[str]],
                               col_widths: Optional[List[float]] = None,
                               callout_text: Optional[str] = None):
        """
        Renders an executive benchmarking table with clear column hierarchy,
        high-contrast navy header, subtle alternating rows, and bottom qualification card.
        """
        n_rows = len(rows) + 1
        n_cols = len(headers)

        tbl_x = Inches(0.65)
        tbl_y = Inches(1.85)
        tbl_w = Inches(12.03)
        row_h = 0.58
        tbl_h = Inches(row_h * n_rows)

        table_shape = slide.shapes.add_table(n_rows, n_cols, tbl_x, tbl_y, tbl_w, tbl_h)
        table = table_shape.table

        if col_widths and len(col_widths) == n_cols:
            for c_idx, cw in enumerate(col_widths):
                table.columns[c_idx].width = Inches(cw)
        else:
            w_each = 12.03 / n_cols
            for c_idx in range(n_cols):
                table.columns[c_idx].width = Inches(w_each)

        for c_idx, h_text in enumerate(headers):
            cell = table.cell(0, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = self.theme.C_NAVY
            tf = cell.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_right = Inches(0.12)
            tf.margin_top = tf.margin_bottom = Inches(0.08)
            p = tf.paragraphs[0]
            p.text = h_text
            p.font.name = self.theme.FONT_HEADING
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = self.theme.C_WHITE

        for r_idx, row_data in enumerate(rows):
            is_alt = (r_idx % 2 == 1)
            row_bg = self.theme.C_SURFACE if is_alt else self.theme.C_WHITE
            for c_idx, val in enumerate(row_data[:n_cols]):
                cell = table.cell(r_idx + 1, c_idx)
                cell.fill.solid()
                cell.fill.fore_color.rgb = row_bg
                tf = cell.text_frame
                tf.word_wrap = True
                tf.margin_left = tf.margin_right = Inches(0.12)
                tf.margin_top = tf.margin_bottom = Inches(0.08)
                p = tf.paragraphs[0]
                p.text = val
                p.font.name = self.theme.FONT_HEADING if c_idx == 0 else self.theme.FONT_BODY
                p.font.size = Pt(12)
                p.font.bold = (c_idx == 0)
                p.font.color.rgb = self.theme.C_TEXT

        if callout_text:
            call_y = Inches(5.60)
            call_h = Inches(0.80)
            card = self.add_card(slide, Inches(0.65), call_y, Inches(12.03), call_h,
                                 bg_color=self.theme.C_SURFACE, border_color=self.theme.C_PRIMARY)
            tb = slide.shapes.add_textbox(Inches(0.85), call_y, Inches(11.63), call_h)
            set_text(tb, callout_text, face="Inter", weight="regular", pt=12.0, color="1E3E62", align="left", anchor="middle", pad_in=0.0)

    # =========================================================================
    # NEW V2 COMPOSITIONS: RELATIONSHIP-FIRST VISUAL GRAMMARS
    # =========================================================================

    # --- GRAMMAR A: LAYERED STACK (ISA-95 / PLATFORM TIERS) ---
    def render_layered_stack(self, slide, layers: List[Dict[str, Any]], callout_note: Optional[str] = None):
        """
        Renders an enterprise architecture stack (e.g. ISA-95 levels 4 to 0, or cloud data fabric tiers).
        Each layer has a tier badge, title, capability tags, and bidirectional control/data flow connectors.
        """
        num_layers = min(len(layers), 5)
        layer_h = 0.98 if num_layers <= 4 else 0.85
        spacing = 0.12 if num_layers <= 4 else 0.10
        start_y = 1.95

        for i, l in enumerate(layers[:num_layers]):
            y = start_y + i * (layer_h + spacing)
            tier_name = l.get("tier", f"Level {num_layers - 1 - i}")
            title = l.get("title", "")
            desc = l.get("desc", "")
            tier_col = l.get("color") or (self.theme.C_NAVY if i == 0 else self.theme.C_PRIMARY)

            # Left Tier Badge Card (text written directly inside shape to prevent clipping/floating textboxes)
            tier_card = self.add_card(slide, Inches(0.65), Inches(y), Inches(2.75), Inches(layer_h),
                                      bg_color=tier_col, border_color=None)
            set_text(tier_card, tier_name, face="Inter", weight="bold", pt=12.0, color="FFFFFF", align="center", anchor="middle", pad_in=0.1)

            # Main Layer Card (text written directly inside shape)
            card_w = 9.13 if not callout_note else 6.3
            main_card = self.add_card(slide, Inches(3.55), Inches(y), Inches(card_w), Inches(layer_h),
                                      bg_color=self.theme.C_WHITE, border_color=self.theme.C_BORDER)

            tf_m = main_card.text_frame
            tf_m.word_wrap = True
            tf_m.auto_size = MSO_AUTO_SIZE.NONE
            tf_m.margin_left = tf_m.margin_right = Inches(0.18)
            tf_m.margin_top = tf_m.margin_bottom = Inches(0.04)
            tf_m.vertical_anchor = MSO_ANCHOR.MIDDLE

            p1 = tf_m.paragraphs[0]
            p1.alignment = PP_ALIGN.LEFT
            r1 = p1.add_run()
            r1.text = title
            r1.font.name = self.theme.FONT_HEADING
            r1.font.size = Pt(12)
            r1.font.bold = True
            r1.font.color.rgb = self.theme.C_TEXT

            p2 = tf_m.add_paragraph()
            p2.alignment = PP_ALIGN.LEFT
            r2 = p2.add_run()
            r2.text = desc
            r2.font.name = self.theme.FONT_BODY
            r2.font.size = Pt(12)
            r2.font.color.rgb = self.theme.C_MUTED

            # Flow arrow to next layer
            if i < num_layers - 1:
                self.add_line(slide, 2.02, y + layer_h, 2.02, y + layer_h + spacing, color=self.theme.C_MUTED, width_pt=1.5)

        if callout_note:
            cx = 10.0
            callout_card = self.add_card(slide, Inches(cx), Inches(1.95), Inches(2.68), Inches(4.85),
                                          bg_color=self.theme.C_SURFACE, border_color=self.theme.C_BORDER)
            tf_c = callout_card.text_frame
            tf_c.word_wrap = True
            tf_c.auto_size = MSO_AUTO_SIZE.NONE
            tf_c.margin_left = tf_c.margin_right = Inches(0.18)
            tf_c.margin_top = tf_c.margin_bottom = Inches(0.18)

            p_ct = tf_c.paragraphs[0]
            r_ct = p_ct.add_run()
            r_ct.text = "Architectural Intent"
            r_ct.font.name = self.theme.FONT_HEADING
            r_ct.font.size = Pt(14)
            r_ct.font.bold = True
            r_ct.font.color.rgb = self.theme.C_PRIMARY

            p_cb = tf_c.add_paragraph()
            p_cb.space_before = Pt(8)
            r_cb = p_cb.add_run()
            r_cb.text = callout_note
            r_cb.font.name = self.theme.FONT_BODY
            r_cb.font.size = Pt(12)
            r_cb.font.color.rgb = self.theme.C_TEXT
            p_cb.space_before = Pt(8)

    # --- GRAMMAR B: ICEBERG VIEW (BEFORE / AFTER SYSTEMIC SHIFT) ---
    def render_iceberg_shift(self, slide, visible_event: Dict[str, Any], submerged_layers: List[Dict[str, Any]], callout_text: str):
        """
        Renders a systems iceberg model: Visible events/symptoms above the waterline
        vs deep systemic structures/mental models submerged beneath.
        """
        water_y = 3.3
        self.add_line(slide, 0.65, water_y, 8.8, water_y, color=self.theme.C_PRIMARY, width_pt=2.5, is_dashed=True)
        tb_wl = slide.shapes.add_textbox(Inches(0.65), Inches(water_y - 0.28), Inches(4.5), Inches(0.28))
        set_text(tb_wl, "--- WATERLINE (VISIBLE VS SUBMERGED) ---", face="Inter", weight="semibold", pt=10.0, color="1E3E62", align="left", anchor="middle", pad_in=0.0)

        # 1. Visible Layer
        self.add_card(slide, Inches(0.65), Inches(1.95), Inches(8.0), Inches(1.0),
                      bg_color=self.theme.C_WHITE, border_color=self.theme.C_BORDER)
        tb_v = slide.shapes.add_textbox(Inches(0.85), Inches(2.05), Inches(7.6), Inches(0.8))
        tf_v = tb_v.text_frame
        tf_v.word_wrap = True
        tf_v.auto_size = MSO_AUTO_SIZE.NONE
        pv1 = tf_v.paragraphs[0]
        pv1.text = f"EVENT LEVEL (SYMPTOMS): {visible_event.get('title', '')}"
        pv1.font.name = self.theme.FONT_HEADING
        pv1.font.size = Pt(12)
        pv1.font.bold = True
        pv1.font.color.rgb = self.theme.C_ALERT

        pv2 = tf_v.add_paragraph()
        pv2.text = visible_event.get("desc", "")
        pv2.font.name = self.theme.FONT_BODY
        pv2.font.size = Pt(12)
        pv2.font.color.rgb = self.theme.C_TEXT

        # 2. Submerged Layers
        for i, layer in enumerate(submerged_layers[:3]):
            ly = 3.5 + i * 1.15
            self.add_card(slide, Inches(0.65), Inches(ly), Inches(8.0), Inches(1.05),
                          bg_color=self.theme.C_SURFACE, border_color=self.theme.C_BORDER)
            tb_l = slide.shapes.add_textbox(Inches(0.85), Inches(ly + 0.1), Inches(7.6), Inches(0.85))
            tf_l = tb_l.text_frame
            tf_l.word_wrap = True
            tf_l.auto_size = MSO_AUTO_SIZE.NONE
            pl1 = tf_l.paragraphs[0]
            pl1.text = layer.get("layer_name", f"Level {i+1}").upper()
            pl1.font.name = self.theme.FONT_SEMIBOLD
            pl1.font.size = Pt(12)
            pl1.font.bold = True
            pl1.font.color.rgb = self.theme.C_NAVY

            pl2 = tf_l.add_paragraph()
            pl2.text = layer.get("finding", "")
            pl2.font.name = self.theme.FONT_BODY
            pl2.font.size = Pt(12)
            pl2.font.color.rgb = self.theme.C_TEXT

        # Right Callout Card (sized to content)
        words_count = len(callout_text.split())
        h_card = max(2.4, min(4.85, 0.7 + (words_count / 5.0) * 0.28))
        callout_card = self.add_card(slide, Inches(9.0), Inches(1.95), Inches(3.68), Inches(h_card),
                                     bg_color=self.theme.C_WHITE, border_color=self.theme.C_BORDER)
        tf_rc = callout_card.text_frame
        tf_rc.word_wrap = True
        tf_rc.auto_size = MSO_AUTO_SIZE.NONE
        tf_rc.margin_left = tf_rc.margin_right = Inches(0.2)
        tf_rc.margin_top = tf_rc.margin_bottom = Inches(0.18)

        prc1 = tf_rc.paragraphs[0]
        r_rc1 = prc1.add_run()
        r_rc1.text = "Transformation Reality"
        r_rc1.font.name = self.theme.FONT_HEADING
        r_rc1.font.size = Pt(14)
        r_rc1.font.bold = True
        r_rc1.font.color.rgb = self.theme.C_PRIMARY

        prc2 = tf_rc.add_paragraph()
        prc2.space_before = Pt(8)
        r_rc2 = prc2.add_run()
        r_rc2.text = callout_text
        r_rc2.font.name = self.theme.FONT_BODY
        r_rc2.font.size = Pt(12)
        r_rc2.font.color.rgb = self.theme.C_TEXT
        prc2.font.color.rgb = self.theme.C_TEXT
        prc2.space_before = Pt(8)

    # --- GRAMMAR C: CONSTRAINT FLOW (GOLDRATT THEORY OF CONSTRAINTS) ---
    def render_constraint_flow(self, slide, stages: List[Dict[str, Any]], constraint_idx: int,
                               buffer_desc: str, impact_annotation: str):
        """
        Renders a production or data pipeline highlighting the binding constraint (Goldratt),
        local buffers, and what throughput moves when the constraint is subordinated/elevated.
        """
        num_stages = min(len(stages), 5)
        col_w = 2.2
        spacing = 0.25
        start_x = 0.65

        for i, st in enumerate(stages[:num_stages]):
            x = start_x + i * (col_w + spacing)
            is_constraint = (i == constraint_idx)
            bg = self.theme.C_WHITE
            border = self.theme.C_ORANGE if is_constraint else self.theme.C_BORDER

            self.add_card(slide, Inches(x), Inches(1.95), Inches(col_w), Inches(2.8),
                          bg_color=bg, border_color=border)

            ind = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(1.95), Inches(col_w), Inches(0.1))
            ind.fill.solid()
            ind.fill.fore_color.rgb = self.theme.C_ORANGE if is_constraint else self.theme.C_PRIMARY
            ind.line.fill.background()

            tb = slide.shapes.add_textbox(Inches(x + 0.12), Inches(2.15), Inches(col_w - 0.24), Inches(2.4))
            tf = tb.text_frame
            tf.word_wrap = True
            p1 = tf.paragraphs[0]
            p1.text = st.get("name", f"Stage {i+1}")
            p1.font.name = self.theme.FONT_HEADING
            p1.font.size = Pt(14)
            p1.font.bold = True
            p1.font.color.rgb = self.theme.C_ALERT if is_constraint else self.theme.C_TEXT

            if is_constraint:
                p_c = tf.add_paragraph()
                p_c.text = "★ BINDING CONSTRAINT"
                p_c.font.name = self.theme.FONT_SEMIBOLD
                p_c.font.size = Pt(12)
                p_c.font.bold = True
                p_c.font.color.rgb = self.theme.C_ORANGE

            p2 = tf.add_paragraph()
            p2.text = st.get("desc", "")
            p2.font.name = self.theme.FONT_BODY
            p2.font.size = Pt(12)
            p2.font.color.rgb = self.theme.C_MUTED
            p2.space_before = Pt(4)

            p3 = tf.add_paragraph()
            p3.text = f"Cycle / Rate: {st.get('rate', 'N/A')}"
            p3.font.name = self.theme.FONT_SEMIBOLD
            p3.font.size = Pt(12)
            p3.font.color.rgb = self.theme.C_TEXT
            p3.space_before = Pt(6)

            if i < num_stages - 1:
                ax = x + col_w + 0.04
                arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(ax), Inches(3.2), Inches(0.18), Inches(0.24))
                arrow.fill.solid()
                arrow.fill.fore_color.rgb = self.theme.C_MUTED
                arrow.line.fill.background()

        # Bottom Impact Callout Card
        self.add_card(slide, Inches(0.65), Inches(5.0), Inches(12.03), Inches(1.8),
                      bg_color=self.theme.C_SURFACE, border_color=self.theme.C_BORDER)

        tb_i = slide.shapes.add_textbox(Inches(0.9), Inches(5.1), Inches(11.5), Inches(1.6))
        tf_i = tb_i.text_frame
        tf_i.word_wrap = True
        pi1 = tf_i.paragraphs[0]
        pi1.text = f"Buffer Policy: {buffer_desc}"
        pi1.font.name = self.theme.FONT_HEADING
        pi1.font.size = Pt(12)
        pi1.font.bold = True
        pi1.font.color.rgb = self.theme.C_NAVY

        pi2 = tf_i.add_paragraph()
        pi2.text = f"Throughput Impact (What Moves): {impact_annotation}"
        pi2.font.name = self.theme.FONT_BODY
        pi2.font.size = Pt(12)
        pi2.font.color.rgb = self.theme.C_TEXT
        pi2.space_before = Pt(4)

    # --- GRAMMAR D: CAUSAL LOOP / FEEDBACK SYSTEMS (SENGE) ---
    def render_causal_loop(self, slide, nodes: List[Dict[str, Any]], loops: List[Dict[str, Any]], delay_annotation: str):
        """
        Renders a systems thinking causal loop diagram (Senge) showing reinforcing (R)
        and balancing (B) feedback loops and delayed systemic responses.
        """
        for i, n in enumerate(nodes[:4]):
            nx = 0.65 + (i % 2) * 4.4
            ny = 1.95 + (i // 2) * 1.8
            self.add_card(slide, Inches(nx), Inches(ny), Inches(4.0), Inches(1.5),
                          bg_color=self.theme.C_WHITE, border_color=self.theme.C_BORDER)

            tb = slide.shapes.add_textbox(Inches(nx + 0.15), Inches(ny + 0.12), Inches(3.7), Inches(1.25))
            tf = tb.text_frame
            tf.word_wrap = True
            p1 = tf.paragraphs[0]
            p1.text = n.get("label", "")
            p1.font.name = self.theme.FONT_HEADING
            p1.font.size = Pt(14)
            p1.font.bold = True
            p1.font.color.rgb = self.theme.C_TEXT

            p2 = tf.add_paragraph()
            p2.text = n.get("desc", "")
            p2.font.name = self.theme.FONT_BODY
            p2.font.size = Pt(12)
            p2.font.color.rgb = self.theme.C_MUTED

        # Right Loop Dynamics Card
        self.add_card(slide, Inches(9.3), Inches(1.95), Inches(3.38), Inches(4.85),
                      bg_color=self.theme.C_SURFACE, border_color=self.theme.C_BORDER)
        tb_l = slide.shapes.add_textbox(Inches(9.45), Inches(2.1), Inches(3.08), Inches(4.5))
        tf_l = tb_l.text_frame
        tf_l.word_wrap = True

        pl1 = tf_l.paragraphs[0]
        pl1.text = "System Feedback Dynamics"
        pl1.font.name = self.theme.FONT_HEADING
        pl1.font.size = Pt(14)
        pl1.font.bold = True
        pl1.font.color.rgb = self.theme.C_PRIMARY

        for lp in loops:
            pl_t = tf_l.add_paragraph()
            l_type = lp.get("type", "Reinforcing (R)")
            pl_t.text = f"• Loop: {l_type}"
            pl_t.font.name = self.theme.FONT_SEMIBOLD
            pl_t.font.size = Pt(12)
            pl_t.font.bold = True
            pl_t.font.color.rgb = self.theme.C_NAVY
            pl_t.space_before = Pt(6)

            pl_d = tf_l.add_paragraph()
            pl_d.text = lp.get("effect", "")
            pl_d.font.name = self.theme.FONT_BODY
            pl_d.font.size = Pt(12)
            pl_d.font.color.rgb = self.theme.C_TEXT

        p_dy = tf_l.add_paragraph()
        p_dy.text = f"System Delay: {delay_annotation}"
        p_dy.font.name = self.theme.FONT_SEMIBOLD
        p_dy.font.size = Pt(12)
        p_dy.font.color.rgb = self.theme.C_ACCENT
        p_dy.space_before = Pt(8)

    # --- GRAMMAR E: TRADEOFF / DECISION QUADRANT (ROSS OPERATING MODEL) ---
    def render_tradeoff_matrix(self, slide, x_axis_title: str, y_axis_title: str,
                               quadrants: List[Dict[str, Any]], callout_note: str):
        """
        Renders a 2x2 decision quadrant (e.g. Ross operating model: Standardisation vs Integration,
        or Westerman: Digital Capability vs Leadership Capability).
        """
        qx, qy = 1.0, 2.0
        qw, qh = 3.6, 2.2
        coords = [
            (qx, qy),
            (qx + qw + 0.2, qy),
            (qx, qy + qh + 0.2),
            (qx + qw + 0.2, qy + qh + 0.2)
        ]

        for i, (cx, cy) in enumerate(coords):
            if i >= len(quadrants):
                break
            q = quadrants[i]
            is_target = q.get("is_target", False)
            bg = self.theme.C_SURFACE if is_target else self.theme.C_WHITE
            border = self.theme.C_PRIMARY if is_target else self.theme.C_BORDER

            self.add_card(slide, Inches(cx), Inches(cy), Inches(qw), Inches(qh),
                          bg_color=bg, border_color=border)

            tb = slide.shapes.add_textbox(Inches(cx + 0.15), Inches(cy + 0.12), Inches(qw - 0.3), Inches(qh - 0.24))
            tf = tb.text_frame
            tf.word_wrap = True

            p1 = tf.paragraphs[0]
            p1.text = q.get("name", f"Quadrant {i+1}")
            p1.font.name = self.theme.FONT_HEADING
            p1.font.size = Pt(14)
            p1.font.bold = True
            p1.font.color.rgb = self.theme.C_PRIMARY if is_target else self.theme.C_TEXT

            if is_target:
                pt = tf.add_paragraph()
                pt.text = "★ TARGET OPERATING EQUILIBRIUM"
                pt.font.name = self.theme.FONT_SEMIBOLD
                pt.font.size = Pt(12)
                pt.font.bold = True
                pt.font.color.rgb = self.theme.C_PRIMARY

            p2 = tf.add_paragraph()
            p2.text = q.get("desc", "")
            p2.font.name = self.theme.FONT_BODY
            p2.font.size = Pt(12)
            p2.font.color.rgb = self.theme.C_MUTED
            p2.space_before = Pt(4)

        # Right Decision Narrative Card
        self.add_card(slide, Inches(8.7), Inches(2.0), Inches(4.0), Inches(4.6),
                      bg_color=self.theme.C_WHITE, border_color=self.theme.C_BORDER)
        tb_r = slide.shapes.add_textbox(Inches(8.9), Inches(2.2), Inches(3.6), Inches(4.2))
        tf_r = tb_r.text_frame
        tf_r.word_wrap = True

        pr1 = tf_r.paragraphs[0]
        pr1.text = "Strategic Decision Framing"
        pr1.font.name = self.theme.FONT_HEADING
        pr1.font.size = Pt(14)
        pr1.font.bold = True
        pr1.font.color.rgb = self.theme.C_PRIMARY

        pr2 = tf_r.add_paragraph()
        pr2.text = callout_note
        pr2.font.name = self.theme.FONT_BODY
        pr2.font.size = Pt(12)
        pr2.font.color.rgb = self.theme.C_TEXT
        pr2.space_before = Pt(8)

    # --- GRAMMAR F: CAPABILITY MATURITY STAIRCASE ---
    def render_capability_maturity_staircase(self, slide, steps: List[Dict[str, Any]], caveat_text: str):
        """
        Renders an ascending capability or career maturity staircase.
        Each ascending step displays competency requirements, focus deliverables, and gate criteria.
        """
        num_steps = min(len(steps), 4)
        col_w = 2.85
        spacing = 0.18
        base_y = 6.0

        base_y = 6.05
        for i, st in enumerate(steps[:num_steps]):
            x = 0.65 + i * (col_w + spacing)
            step_h = 2.45 + i * 0.45
            y = base_y - step_h

            is_lead = (i == num_steps - 1)
            col = self.theme.C_NAVY if is_lead else self.theme.C_PRIMARY

            self.add_card(slide, Inches(x), Inches(y), Inches(col_w), Inches(step_h),
                          bg_color=self.theme.C_WHITE, border_color=self.theme.C_BORDER)

            hbar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(col_w), Inches(0.42))
            hbar.fill.solid()
            hbar.fill.fore_color.rgb = col
            hbar.line.fill.background()
            set_text(hbar, f"Stage 0{i+1}: {st.get('level_name', '')}", face="Inter", weight="bold", pt=11.5, color="FFFFFF", align="center", anchor="middle", pad_in=0.08)

            tb_b = slide.shapes.add_textbox(Inches(x + 0.12), Inches(y + 0.48), Inches(col_w - 0.24), Inches(step_h - 0.54))
            tf_b = tb_b.text_frame
            tf_b.word_wrap = True
            tf_b.auto_size = MSO_AUTO_SIZE.NONE
            tf_b.margin_left = tf_b.margin_right = Inches(0.08)
            tf_b.margin_top = tf_b.margin_bottom = Inches(0.06)

            p1 = tf_b.paragraphs[0]
            p1.alignment = PP_ALIGN.LEFT
            r1 = p1.add_run()
            r1.text = st.get("role_title", "")
            r1.font.name = self.theme.FONT_HEADING
            r1.font.size = Pt(12)
            r1.font.bold = True
            r1.font.color.rgb = self.theme.C_TEXT

            for c in st.get("competencies", []):
                pc = tf_b.add_paragraph()
                pc.alignment = PP_ALIGN.LEFT
                rc = pc.add_run()
                rc.text = f"• {c}"
                rc.font.name = self.theme.FONT_BODY
                rc.font.size = Pt(12)
                rc.font.color.rgb = self.theme.C_MUTED
                pc.space_before = Pt(2)

            if st.get("gate_criterion"):
                pg = tf_b.add_paragraph()
                pg.alignment = PP_ALIGN.LEFT
                rg = pg.add_run()
                rg.text = f"Gate: {st['gate_criterion']}"
                rg.font.name = self.theme.FONT_SEMIBOLD
                rg.font.size = Pt(12)
                rg.font.bold = True
                rg.font.color.rgb = self.theme.C_ACCENT
                pg.space_before = Pt(4)

        if caveat_text:
            tb_cv = slide.shapes.add_textbox(Inches(0.65), Inches(6.25), Inches(12.03), Inches(0.35))
            set_text(tb_cv, caveat_text, face="Inter", weight="regular", pt=12.0, color="646E78", align="left", anchor="middle", pad_in=0.0, italic=True)

    # --- GRAMMAR G: ANNOTATED NATIVE CHART WITH EVIDENCE CALLOUT ---
    def render_annotated_chart(self, slide, chart_type: str, categories: List[str], series_data: List[Dict[str, Any]],
                               title: str, x_label: str, y_label: str, callout_annotation: str, key_takeaway: str,
                               source_id: Optional[str] = None):
        """
        Renders a native chart with direct labels, axes, and an executive argument callout panel.
        Ensures strict chart integrity (labels <= 14 chars, <= 30 deg rotation, visible provenance).
        """
        chart_data = CategoryChartData()
        chart_data.categories = categories
        for s in series_data:
            chart_data.add_series(s.get("name", "Metric"), s.get("values", []))

        c_type = XL_CHART_TYPE.COLUMN_CLUSTERED if chart_type == "column" else XL_CHART_TYPE.LINE
        cx, cy, cw, ch = 0.65, 1.95, 7.8, 4.4

        chart_shape = slide.shapes.add_chart(
            c_type,
            Inches(cx), Inches(cy), Inches(cw), Inches(ch),
            chart_data
        )
        c = chart_shape.chart
        c.has_title = True
        c.chart_title.text_frame.text = title
        c.chart_title.text_frame.paragraphs[0].font.size = Pt(12)
        c.chart_title.text_frame.paragraphs[0].font.name = self.theme.FONT_HEADING

        c.has_legend = len(series_data) > 1
        if c.has_legend:
            c.legend.position = XL_LEGEND_POSITION.BOTTOM
            c.legend.include_in_layout = False

        # Right Callout Card
        self.add_card(slide, Inches(8.7), Inches(1.95), Inches(4.0), Inches(4.4),
                      bg_color=self.theme.C_WHITE, border_color=self.theme.C_BORDER)

        tb_c = slide.shapes.add_textbox(Inches(8.9), Inches(2.15), Inches(3.6), Inches(4.0))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True

        p1 = tf_c.paragraphs[0]
        p1.text = "Executive Takeaway"
        p1.font.name = self.theme.FONT_HEADING
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = self.theme.C_PRIMARY

        p2 = tf_c.add_paragraph()
        p2.text = key_takeaway
        p2.font.name = self.theme.FONT_BODY
        p2.font.size = Pt(12)
        p2.font.color.rgb = self.theme.C_TEXT
        p2.space_before = Pt(6)

        p3 = tf_c.add_paragraph()
        p3.text = "Operational Implication:"
        p3.font.name = self.theme.FONT_SEMIBOLD
        p3.font.size = Pt(12)
        p3.font.bold = True
        p3.font.color.rgb = self.theme.C_NAVY
        p3.space_before = Pt(8)

        p4 = tf_c.add_paragraph()
        p4.text = callout_annotation
        p4.font.name = self.theme.FONT_BODY
        p4.font.size = Pt(12)
        p4.font.color.rgb = self.theme.C_MUTED

        if source_id:
            p_src = tf_c.add_paragraph()
            clean_src = source_id.strip("[]")
            p_src.text = f"Source: {clean_src}"
            p_src.font.name = self.theme.FONT_BODY
            p_src.font.size = Pt(12)
            p_src.font.italic = True
            p_src.font.color.rgb = self.theme.C_PRIMARY
            p_src.space_before = Pt(8)

    # --- GRAMMAR H: CAREER TRAJECTORY & ENABLEMENT ROADMAP ---
    def render_career_trajectory_roadmap(self, slide, roles: List[Tuple[str, str]], certifications: List[Tuple[str, str, str]],
                                         action_plan: List[Tuple[str, str]], caveat_text: Optional[str] = None):
        """
        Specialized Level B composition for Career Trajectory, Enablement & Action Milestones.
        Replaces SGG commercials table framing with a clean 3-zone relationship layout:
          - Zone 1 (Left): Roles & Compensation Comparison
          - Zone 2 (Center): Certification Credential Sequence
          - Zone 3 (Right): 90-Day Execution Timeline
        """
        top_y = 1.95
        zone_h = 4.8

        # --- Zone 1: Roles & Compensation Comparison (Width 3.8in) ---
        z1_w = 3.8
        self.add_card(slide, Inches(0.65), Inches(top_y), Inches(z1_w), Inches(zone_h),
                      bg_color=self.theme.C_WHITE, border_color=self.theme.C_BORDER)

        h1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.65), Inches(top_y), Inches(z1_w), Inches(0.42))
        h1.fill.solid()
        h1.fill.fore_color.rgb = self.theme.C_NAVY
        h1.line.fill.background()
        set_text(h1, "Role Profile & Compensation", face="Inter", weight="bold", pt=12.0, color="FFFFFF", align="center", anchor="middle")

        for idx, (role, comp) in enumerate(roles[:4]):
            ry = top_y + 0.52 + idx * 1.02
            rcard = self.add_card(slide, Inches(0.8), Inches(ry), Inches(z1_w - 0.3), Inches(0.92),
                                  bg_color=self.theme.C_SURFACE, border_color=self.theme.C_BORDER)
            tf_r = rcard.text_frame
            tf_r.word_wrap = True
            tf_r.auto_size = MSO_AUTO_SIZE.NONE
            tf_r.margin_left = tf_r.margin_right = Inches(0.12)
            tf_r.margin_top = tf_r.margin_bottom = Inches(0.08)

            p1 = tf_r.paragraphs[0]
            r1 = p1.add_run()
            r1.text = role
            r1.font.name = self.theme.FONT_HEADING
            r1.font.size = Pt(12)
            r1.font.bold = True
            r1.font.color.rgb = self.theme.C_TEXT

            p2 = tf_r.add_paragraph()
            p2.space_before = Pt(3)
            r2 = p2.add_run()
            r2.text = f"Benchmark: {comp}"
            r2.font.name = self.theme.FONT_BODY
            r2.font.size = Pt(12)
            r2.font.color.rgb = self.theme.C_PRIMARY

        # --- Zone 2: Certification Credential Sequence (Width 3.8in) ---
        z2_x = 4.65
        z2_w = 3.8
        self.add_card(slide, Inches(z2_x), Inches(top_y), Inches(z2_w), Inches(zone_h),
                      bg_color=self.theme.C_WHITE, border_color=self.theme.C_BORDER)

        h2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(z2_x), Inches(top_y), Inches(z2_w), Inches(0.42))
        h2.fill.solid()
        h2.fill.fore_color.rgb = self.theme.C_PRIMARY
        h2.line.fill.background()
        set_text(h2, "Credentialing Sequence", face="Inter", weight="bold", pt=12.0, color="FFFFFF", align="center", anchor="middle")

        for idx, (code, title, plat) in enumerate(certifications[:3]):
            cy = top_y + 0.55 + idx * 1.35
            ccard = self.add_card(slide, Inches(z2_x + 0.15), Inches(cy), Inches(z2_w - 0.3), Inches(1.22),
                                  bg_color=self.theme.C_SURFACE, border_color=self.theme.C_BORDER)
            tf_c = ccard.text_frame
            tf_c.word_wrap = True
            tf_c.auto_size = MSO_AUTO_SIZE.NONE
            tf_c.margin_left = tf_c.margin_right = Inches(0.12)
            tf_c.margin_top = tf_c.margin_bottom = Inches(0.08)

            p1 = tf_c.paragraphs[0]
            r1 = p1.add_run()
            r1.text = code
            r1.font.name = self.theme.FONT_HEADING
            r1.font.size = Pt(12)
            r1.font.bold = True
            r1.font.color.rgb = self.theme.C_PRIMARY

            p2 = tf_c.add_paragraph()
            r2 = p2.add_run()
            r2.text = title
            r2.font.name = self.theme.FONT_BODY
            r2.font.size = Pt(12)
            r2.font.color.rgb = self.theme.C_TEXT
            p2.space_before = Pt(2)

            p3 = tf_c.add_paragraph()
            r3 = p3.add_run()
            r3.text = f"Platform: {plat}"
            r3.font.name = self.theme.FONT_BODY
            r3.font.size = Pt(12)
            r3.font.color.rgb = self.theme.C_MUTED
            p3.space_before = Pt(2)

        # --- Zone 3: 90-Day Execution Timeline (Width 4.03in) ---
        z3_x = 8.65
        z3_w = 4.03
        self.add_card(slide, Inches(z3_x), Inches(top_y), Inches(z3_w), Inches(zone_h),
                      bg_color=self.theme.C_WHITE, border_color=self.theme.C_BORDER)

        h3 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(z3_x), Inches(top_y), Inches(z3_w), Inches(0.42))
        h3.fill.solid()
        h3.fill.fore_color.rgb = self.theme.C_MUTED
        h3.line.fill.background()
        set_text(h3, "90-Day Execution Pathway", face="Inter", weight="bold", pt=12.0, color="FFFFFF", align="center", anchor="middle")

        for idx, (tf_step, action) in enumerate(action_plan[:4]):
            ay = top_y + 0.52 + idx * 1.02
            acard = self.add_card(slide, Inches(z3_x + 0.15), Inches(ay), Inches(z3_w - 0.3), Inches(0.92),
                                  bg_color=self.theme.C_SURFACE, border_color=self.theme.C_BORDER)
            tf_a = acard.text_frame
            tf_a.word_wrap = True
            tf_a.auto_size = MSO_AUTO_SIZE.NONE
            tf_a.margin_left = tf_a.margin_right = Inches(0.12)
            tf_a.margin_top = tf_a.margin_bottom = Inches(0.08)

            p1 = tf_a.paragraphs[0]
            r1 = p1.add_run()
            r1.text = tf_step
            r1.font.name = self.theme.FONT_HEADING
            r1.font.size = Pt(12)
            r1.font.bold = True
            r1.font.color.rgb = self.theme.C_TEXT

            p2 = tf_a.add_paragraph()
            r2 = p2.add_run()
            r2.text = action
            r2.font.name = self.theme.FONT_BODY
            r2.font.size = Pt(12)
            r2.font.color.rgb = self.theme.C_MUTED
            p2.space_before = Pt(2)

    # =========================================================================
    # COMPOSITION 11: METADATA VS. BUSINESS CONTEXT COMPARISON
    # =========================================================================
    def render_metadata_vs_context(self, slide, metadata_items: List[Tuple[str, str]],
                                   context_items: List[Tuple[str, str]],
                                   example_box: Dict[str, Any]):
        """
        Two-column comparative architecture contrasting System Metadata (What exists)
        with Business Context (What matters, when, and why), plus an operational DTR case strip.
        """
        top_y = 1.95
        card_h = 3.65
        col_w = 5.86

        # Left Card: Metadata (What Exists)
        left_card = self.add_card(slide, Inches(0.65), Inches(top_y), Inches(col_w), Inches(card_h),
                                  bg_color=self.theme.C_WHITE, border_color=self.theme.C_BORDER)
        h_left = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.65), Inches(top_y), Inches(col_w), Inches(0.42))
        h_left.fill.solid()
        h_left.fill.fore_color.rgb = self.theme.C_NAVY
        h_left.line.fill.background()
        set_text(h_left, "System Metadata: What Exists", face="Inter", weight="bold", pt=12.0, color="FFFFFF", align="center", anchor="middle")

        tb_lm = slide.shapes.add_textbox(Inches(0.85), Inches(top_y + 0.52), Inches(col_w - 0.4), Inches(card_h - 0.6))
        tf_lm = tb_lm.text_frame
        tf_lm.word_wrap = True
        tf_lm.auto_size = MSO_AUTO_SIZE.NONE
        tf_lm.margin_left = tf_lm.margin_right = tf_lm.margin_top = tf_lm.margin_bottom = 0

        for k, (lbl, desc) in enumerate(metadata_items):
            p = tf_lm.paragraphs[0] if k == 0 else tf_lm.add_paragraph()
            r1 = p.add_run()
            r1.text = f"• {lbl}: "
            r1.font.name = self.theme.FONT_HEADING
            r1.font.size = Pt(12)
            r1.font.bold = True
            r1.font.color.rgb = self.theme.C_NAVY

            r2 = p.add_run()
            r2.text = desc
            r2.font.name = self.theme.FONT_BODY
            r2.font.size = Pt(12)
            r2.font.color.rgb = self.theme.C_TEXT
            if k > 0:
                p.space_before = Pt(4)

        # Right Card: Business Context (What Matters & Why)
        right_x = 6.82
        right_card = self.add_card(slide, Inches(right_x), Inches(top_y), Inches(col_w), Inches(card_h),
                                   bg_color=self.theme.C_WHITE, border_color=self.theme.C_BORDER)
        h_right = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(right_x), Inches(top_y), Inches(col_w), Inches(0.42))
        h_right.fill.solid()
        h_right.fill.fore_color.rgb = self.theme.C_PRIMARY
        h_right.line.fill.background()
        set_text(h_right, "Business Context: What Matters, When & Why", face="Inter", weight="bold", pt=12.0, color="FFFFFF", align="center", anchor="middle")

        tb_rm = slide.shapes.add_textbox(Inches(right_x + 0.2), Inches(top_y + 0.52), Inches(col_w - 0.4), Inches(card_h - 0.6))
        tf_rm = tb_rm.text_frame
        tf_rm.word_wrap = True
        tf_rm.auto_size = MSO_AUTO_SIZE.NONE
        tf_rm.margin_left = tf_rm.margin_right = tf_rm.margin_top = tf_rm.margin_bottom = 0

        for k, (lbl, desc) in enumerate(context_items):
            p = tf_rm.paragraphs[0] if k == 0 else tf_rm.add_paragraph()
            r1 = p.add_run()
            r1.text = f"• {lbl}: "
            r1.font.name = self.theme.FONT_HEADING
            r1.font.size = Pt(12)
            r1.font.bold = True
            r1.font.color.rgb = self.theme.C_PRIMARY

            r2 = p.add_run()
            r2.text = desc
            r2.font.name = self.theme.FONT_BODY
            r2.font.size = Pt(12)
            r2.font.color.rgb = self.theme.C_TEXT
            if k > 0:
                p.space_before = Pt(4)

        # Bottom DTR Case Strip
        band_y = 5.75
        band = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), Inches(band_y), Inches(12.03), Inches(1.15))
        band.fill.solid()
        band.fill.fore_color.rgb = self.theme.C_SURFACE
        band.line.color.rgb = self.theme.C_PRIMARY
        band.line.width = Pt(1)

        tb_ex = slide.shapes.add_textbox(Inches(0.85), Inches(band_y + 0.08), Inches(11.63), Inches(0.98))
        tf_ex = tb_ex.text_frame
        tf_ex.word_wrap = True
        tf_ex.auto_size = MSO_AUTO_SIZE.NONE
        tf_ex.margin_left = tf_ex.margin_right = tf_ex.margin_top = tf_ex.margin_bottom = 0

        p_ex1 = tf_ex.paragraphs[0]
        r_eh = p_ex1.add_run()
        r_eh.text = f"PRACTICAL UTILITY ILLUSTRATION — {example_box.get('title', 'Distribution Transformer (DTR) Asset')}: "
        r_eh.font.name = self.theme.FONT_HEADING
        r_eh.font.size = Pt(12)
        r_eh.font.bold = True
        r_eh.font.color.rgb = self.theme.C_PRIMARY

        r_em = p_ex1.add_run()
        r_em.text = f"Metadata: {example_box.get('metadata_text', '')}"
        r_em.font.name = self.theme.FONT_BODY
        r_em.font.size = Pt(12)
        r_em.font.color.rgb = self.theme.C_MUTED

        p_ex2 = tf_ex.add_paragraph()
        p_ex2.space_before = Pt(3)
        r_ec1 = p_ex2.add_run()
        r_ec1.text = "Operational Context: "
        r_ec1.font.name = self.theme.FONT_HEADING
        r_ec1.font.size = Pt(12)
        r_ec1.font.bold = True
        r_ec1.font.color.rgb = self.theme.C_NAVY

        r_ec2 = p_ex2.add_run()
        r_ec2.text = example_box.get('context_text', '')
        r_ec2.font.name = self.theme.FONT_BODY
        r_ec2.font.size = Pt(12)
        r_ec2.font.color.rgb = self.theme.C_TEXT

    # =========================================================================
    # COMPOSITION 12: DARK EXECUTIVE CLOSING (SLIDE 15)
    # =========================================================================
    def render_closing(self, slide, title: str, subtitle: str, core_message: str,
                       pillars: List[Tuple[str, str]], concluding_statement: str,
                       pill_text: Optional[str] = None):
        """
        Renders a premium dark navy executive closing slide (Slide 15).
        Combines strategic conclusion, connected enterprise pillars, and the final mandate.
        """
        # Dark navy background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(10, 25, 47)  # #0A192F
        bg.line.fill.background()

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.9), Inches(0.7), Inches(11.5), Inches(0.9))
        set_text(t_box, title, face="Inter", weight="bold", pt=26.0, color="FFFFFF", align="left", anchor="top", pad_in=0.0)

        # Orange Accent Rule
        rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(1.65), Inches(4.5), Inches(0.04))
        rule.fill.solid()
        rule.fill.fore_color.rgb = self.theme.C_ACCENT
        rule.line.fill.background()

        # Core Message Callout Card
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.85), Inches(11.533), Inches(1.2))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(15, 35, 65)  # #0F2341
        card.line.color.rgb = RGBColor(2, 132, 199)      # #0284C7
        card.line.width = Pt(1.5)

        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.auto_size = MSO_AUTO_SIZE.NONE
        tf_c.margin_left = tf_c.margin_right = Inches(0.3)
        tf_c.margin_top = tf_c.margin_bottom = Inches(0.15)
        p_c = tf_c.paragraphs[0]
        p_c.text = f'"{core_message}"'
        p_c.font.name = self.theme.FONT_HEADING
        p_c.font.size = Pt(14)
        p_c.font.bold = True
        p_c.font.italic = True
        p_c.font.color.rgb = RGBColor(224, 242, 254)   # #E0F2FE

        # 4 Connected Enterprise Pillars
        col_w = 2.68
        gap = 0.27
        for idx, (p_name, p_desc) in enumerate(pillars[:4]):
            px = 0.9 + idx * (col_w + gap)
            p_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(px), Inches(3.25), Inches(col_w), Inches(2.1))
            p_card.fill.solid()
            p_card.fill.fore_color.rgb = RGBColor(23, 42, 69)  # #172A45
            p_card.line.color.rgb = RGBColor(51, 65, 85)       # #334155
            p_card.line.width = Pt(1)

            tf_p = p_card.text_frame
            tf_p.word_wrap = True
            tf_p.auto_size = MSO_AUTO_SIZE.NONE
            tf_p.margin_left = tf_p.margin_right = Inches(0.18)
            tf_p.margin_top = tf_p.margin_bottom = Inches(0.15)
            pp1 = tf_p.paragraphs[0]
            pp1.text = p_name
            pp1.font.name = self.theme.FONT_HEADING
            pp1.font.size = Pt(12)
            pp1.font.bold = True
            pp1.font.color.rgb = RGBColor(56, 189, 248)      # #38BDF8

            pp2 = tf_p.add_paragraph()
            pp2.text = p_desc
            pp2.font.name = self.theme.FONT_BODY
            pp2.font.size = Pt(12)
            pp2.font.color.rgb = RGBColor(203, 213, 225)     # #CBD5E1
            pp2.space_before = Pt(4)

        # Concluding Mandate & Pill
        mandate_box = slide.shapes.add_textbox(Inches(0.9), Inches(5.65), Inches(8.0), Inches(0.95))
        tf_m = mandate_box.text_frame
        tf_m.word_wrap = True
        tf_m.auto_size = MSO_AUTO_SIZE.NONE
        tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = tf_m.margin_bottom = 0
        pm1 = tf_m.paragraphs[0]
        pm1.text = "STRATEGIC IMPERATIVE"
        pm1.font.name = self.theme.FONT_SEMIBOLD
        pm1.font.size = Pt(12)
        pm1.font.bold = True
        pm1.font.color.rgb = self.theme.C_ACCENT

        pm2 = tf_m.add_paragraph()
        pm2.text = concluding_statement
        pm2.font.name = self.theme.FONT_HEADING
        pm2.font.size = Pt(12)
        pm2.font.bold = True
        pm2.font.color.rgb = RGBColor(255, 255, 255)
        pm2.space_before = Pt(3)

        if pill_text:
            pt_sz = 11.5
            w_needed = measure(pill_text, True, pt_sz) * 1.12 + 0.5
            pill_w = max(2.6, min(4.2, w_needed))
            pill_x = 12.43 - pill_w
            pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(pill_x), Inches(5.75), Inches(pill_w), Inches(0.65))
            pill.fill.solid()
            pill.fill.fore_color.rgb = RGBColor(2, 132, 199)
            pill.line.fill.background()
            set_text(pill, pill_text, face="Inter", weight="bold", pt=pt_sz, color="FFFFFF", align="center", anchor="middle", pad_in=0.1)
