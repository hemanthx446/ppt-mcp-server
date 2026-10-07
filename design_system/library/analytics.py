"""
Analytics & Charting Visual Primitives (Primitives 22–34).

Uses native, editable PowerPoint chart objects (via CategoryChartData & XL_CHART_TYPE)
and native shape widgets for KPI strips, heatmaps, aging analysis, and risk matrices.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION

from ..typography import TypographySystem
from ..spacing import Margins, SpacingScale, GridCalculator
from ..color import Theme
from ..primitives import SurfacePrimitive, MetricPrimitive


class KPIStripPrimitive:
    """22. Horizontal row of 3–5 hero KPI metric cards."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               kpis: List[Tuple[str, str, Optional[str], Optional[str], bool]], # [(val, label, context, delta, is_pos)]
               theme: Theme):
        cols = GridCalculator.get_columns(len(kpis), left=left, total_width=width, gap=0.20)
        for i, (val, lbl, ctx, delta, is_pos) in enumerate(kpis):
            cx, cw = cols[i]
            SurfacePrimitive.render(slide, cx, top, cw, height, theme)

            tb = slide.shapes.add_textbox(Inches(cx + 0.14), Inches(top + 0.12), Inches(cw - 0.28), Inches(height - 0.24))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = 0

            # Value
            val_color = theme.status_success if is_pos else theme.status_warning
            TypographySystem.apply_to_paragraph(tf.paragraphs[0], TypographySystem.KPI_NUMBER, val, val_color)

            # Label
            p_lbl = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_lbl, TypographySystem.KPI_LABEL, lbl, theme.text_primary)

            # Delta / Context
            if delta or ctx:
                p_c = tf.add_paragraph()
                txt = f"{delta} | {ctx}" if (delta and ctx) else (delta or ctx)
                TypographySystem.apply_to_paragraph(p_c, TypographySystem.CAPTION, txt, theme.text_muted)


class ExecutiveDashboardPrimitive:
    """23. Multi-widget operational cockpit with report inventory and KPI cards."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               cockpits: List[Tuple[str, str, List[Tuple[str, str]]]], # [(title, scope_badge, [(report_name, metric)])]
               theme: Theme):
        cols = GridCalculator.get_columns(len(cockpits), left=left, total_width=width, gap=0.25)
        for i, (title, badge, reports) in enumerate(cockpits):
            cx, cw = cols[i]
            SurfacePrimitive.render(slide, cx, top, cw, height, theme)

            # Header Banner
            hb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(top), Inches(cw), Inches(0.48))
            hb.fill.solid()
            hb.fill.fore_color.rgb = theme.surface_highlight
            hb.line.color.rgb = theme.border
            tf_h = hb.text_frame
            tf_h.margin_left = Inches(0.12)
            TypographySystem.apply_to_paragraph(tf_h.paragraphs[0], TypographySystem.LABEL, title, theme.text_accent)
            TypographySystem.apply_to_paragraph(tf_h.add_paragraph(), TypographySystem.CAPTION, badge, theme.text_muted)

            # Report items
            tb = slide.shapes.add_textbox(Inches(cx + 0.14), Inches(top + 0.58), Inches(cw - 0.28), Inches(height - 0.68))
            tf = tb.text_frame
            tf.word_wrap = True
            for r_title, r_desc in reports[:6]:
                p = tf.add_paragraph()
                p.space_after = Pt(4)
                TypographySystem.apply_to_paragraph(p, TypographySystem.BODY_STRONG, f"•  {r_title}", theme.text_primary)
                p_d = tf.add_paragraph()
                p_d.space_after = Pt(6)
                TypographySystem.apply_to_paragraph(p_d, TypographySystem.CAPTION, f"    {r_desc}", theme.text_muted)


class BarChartPrimitive:
    """25. Native, fully editable PowerPoint Clustered Bar/Column Chart."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               categories: List[str],
               series_data: List[Tuple[str, List[float]]], # [(series_name, values)]
               theme: Theme, is_horizontal: bool = False):
        chart_data = CategoryChartData()
        chart_data.categories = categories
        for s_name, s_vals in series_data:
            chart_data.add_series(s_name, s_vals)

        c_type = XL_CHART_TYPE.BAR_CLUSTERED if is_horizontal else XL_CHART_TYPE.COLUMN_CLUSTERED
        chart_shape = slide.shapes.add_chart(c_type, Inches(left), Inches(top), Inches(width), Inches(height), chart_data)
        chart = chart_shape.chart
        chart.has_legend = True
        chart.legend.position = XL_LEGEND_POSITION.TOP
        chart.legend.include_in_layout = False
        return chart_shape


class TrendChartPrimitive:
    """24. Native, fully editable PowerPoint Line Trend Chart."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               periods: List[str],
               series_data: List[Tuple[str, List[float]]],
               theme: Theme):
        chart_data = CategoryChartData()
        chart_data.categories = periods
        for s_name, s_vals in series_data:
            chart_data.add_series(s_name, s_vals)

        chart_shape = slide.shapes.add_chart(XL_CHART_TYPE.LINE, Inches(left), Inches(top), Inches(width), Inches(height), chart_data)
        chart = chart_shape.chart
        chart.has_legend = True
        chart.legend.position = XL_LEGEND_POSITION.TOP
        chart.legend.include_in_layout = False
        return chart_shape


class StackedBarPrimitive:
    """26. Native, fully editable PowerPoint Stacked Column Chart."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               categories: List[str],
               series_data: List[Tuple[str, List[float]]],
               theme: Theme):
        chart_data = CategoryChartData()
        chart_data.categories = categories
        for s_name, s_vals in series_data:
            chart_data.add_series(s_name, s_vals)

        chart_shape = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Inches(left), Inches(top), Inches(width), Inches(height), chart_data)
        chart = chart_shape.chart
        chart.has_legend = True
        chart.legend.position = XL_LEGEND_POSITION.TOP
        chart.legend.include_in_layout = False
        return chart_shape


class LineChartPrimitive:
    """27. Multi-series Line Chart with markers."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               categories: List[str],
               series_data: List[Tuple[str, List[float]]],
               theme: Theme):
        return TrendChartPrimitive.render(slide, left, top, width, height, categories, series_data, theme)


class WaterfallPrimitive:
    """28. Waterfall Bridge Chart (Starting Base -> Variances / Levers -> Ending Result)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               steps: List[Tuple[str, float, bool]], # [(label, amount, is_total)]
               theme: Theme):
        SurfacePrimitive.render(slide, left, top, width, height, theme)
        cols = GridCalculator.get_columns(len(steps), left=left + 0.2, total_width=width - 0.4, gap=0.15)

        base_val = steps[0][1]
        max_val = max(abs(s[1]) for s in steps) * 1.3
        bar_avail_h = height - 1.2

        for i, (lbl, val, is_tot) in enumerate(steps):
            cx, cw = cols[i]
            # Height proportional to value
            val_h = max(0.4, (abs(val) / max_val) * bar_avail_h)
            bar_y = top + height - 0.5 - val_h

            bar_color = theme.accent_primary if is_tot else (theme.status_success if val >= 0 else theme.status_critical)
            bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(bar_y), Inches(cw), Inches(val_h))
            bar.fill.solid()
            bar.fill.fore_color.rgb = bar_color
            bar.line.fill.background()

            # Value label on bar
            tf_b = bar.text_frame
            val_prefix = "+" if (val > 0 and not is_tot) else ""
            TypographySystem.apply_to_paragraph(tf_b.paragraphs[0], TypographySystem.ANNOTATION, f"{val_prefix}{val:,.0f}", theme.text_primary)

            # Category label below bar
            lb = slide.shapes.add_textbox(Inches(cx), Inches(top + height - 0.45), Inches(cw), Inches(0.40))
            tf_l = lb.text_frame
            tf_l.word_wrap = True
            TypographySystem.apply_to_paragraph(tf_l.paragraphs[0], TypographySystem.CAPTION, lbl, theme.text_muted)


class ParetoPrimitive:
    """29. Pareto Analysis (80/20 Distribution of defect causes or inventory stock values)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               items: List[Tuple[str, float]], # [(cause_name, frequency)]
               theme: Theme):
        SurfacePrimitive.render(slide, left, top, width, height, theme)
        # Header banner
        hbar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(0.40))
        hbar.fill.solid()
        hbar.fill.fore_color.rgb = theme.surface_highlight
        hbar.line.color.rgb = theme.border
        tf_h = hbar.text_frame
        TypographySystem.apply_to_paragraph(tf_h.paragraphs[0], TypographySystem.LABEL, "PARETO 80/20 ROOT CAUSE CONCENTRATION", theme.text_accent)

        total_freq = sum(f for _, f in items)
        running = 0.0

        cols = GridCalculator.get_columns(len(items), left=left + 0.2, total_width=width - 0.4, gap=0.15)
        for i, (cause, freq) in enumerate(items):
            cx, cw = cols[i]
            running += freq
            cum_pct = (running / total_freq) * 100.0 if total_freq > 0 else 0.0

            bar_h = (freq / total_freq) * (height - 1.2)
            bar_y = top + height - 0.5 - bar_h

            bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(bar_y), Inches(cw), Inches(bar_h))
            bar.fill.solid()
            bar.fill.fore_color.rgb = theme.accent_primary if cum_pct <= 80 else theme.surface_alt
            bar.line.color.rgb = theme.border

            # Cumulative % pill
            tb = slide.shapes.add_textbox(Inches(cx), Inches(top + 0.48), Inches(cw), Inches(0.35))
            tf = tb.text_frame
            TypographySystem.apply_to_paragraph(tf.paragraphs[0], TypographySystem.ANNOTATION, f"{cum_pct:.0f}%", theme.status_warning)

            # Label
            lbl_box = slide.shapes.add_textbox(Inches(cx), Inches(top + height - 0.45), Inches(cw), Inches(0.40))
            TypographySystem.apply_to_paragraph(lbl_box.text_frame.paragraphs[0], TypographySystem.CAPTION, cause, theme.text_muted)


class HeatmapPrimitive:
    """30. Matrix Heatmap grid color-coded by intensity values."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               row_labels: List[str],
               col_labels: List[str],
               values_matrix: List[List[float]], # 2D array
               theme: Theme):
        SurfacePrimitive.render(slide, left, top, width, height, theme)
        r_count = len(row_labels)
        c_count = len(col_labels)

        # Header columns
        col_w = (width - 1.8) / c_count
        row_h = (height - 0.6) / r_count

        for c_idx, c_lbl in enumerate(col_labels):
            cx = left + 1.8 + c_idx * col_w
            tb = slide.shapes.add_textbox(Inches(cx), Inches(top + 0.1), Inches(col_w), Inches(0.4))
            TypographySystem.apply_to_paragraph(tb.text_frame.paragraphs[0], TypographySystem.LABEL, c_lbl, theme.text_accent)

        for r_idx, r_lbl in enumerate(row_labels):
            ry = top + 0.5 + r_idx * row_h
            # Row label
            tb_r = slide.shapes.add_textbox(Inches(left + 0.1), Inches(ry), Inches(1.6), Inches(row_h))
            TypographySystem.apply_to_paragraph(tb_r.text_frame.paragraphs[0], TypographySystem.LABEL, r_lbl, theme.text_primary)

            for c_idx in range(c_count):
                val = values_matrix[r_idx][c_idx] if r_idx < len(values_matrix) and c_idx < len(values_matrix[r_idx]) else 0.0
                cx = left + 1.8 + c_idx * col_w
                cell = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx + 0.04), Inches(ry + 0.04), Inches(col_w - 0.08), Inches(row_h - 0.08))
                cell.fill.solid()
                cell.fill.fore_color.rgb = theme.status_critical if val > 75 else (theme.status_warning if val > 40 else theme.status_success)
                cell.line.color.rgb = theme.border
                TypographySystem.apply_to_paragraph(cell.text_frame.paragraphs[0], TypographySystem.ANNOTATION, f"{val:.0f}%", theme.text_primary)


class VarianceViewPrimitive:
    """31. Variance View (Actual vs Budget / Standard BOM with +/- delta flags)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               variances: List[Tuple[str, float, float, str]], # [(cost_element, actual, standard, uom)]
               theme: Theme):
        SurfacePrimitive.render(slide, left, top, width, height, theme)
        rows = GridCalculator.get_rows(len(variances), top=top + 0.5, total_height=height - 0.7, gap=0.12)

        # Header
        hb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(0.42))
        hb.fill.solid()
        hb.fill.fore_color.rgb = theme.surface_highlight
        hb.line.color.rgb = theme.border
        tf_h = hb.text_frame
        TypographySystem.apply_to_paragraph(tf_h.paragraphs[0], TypographySystem.LABEL, "ACTUAL VS STANDARD VARIANCE ENGINE (BOM / COSTING)", theme.text_accent)

        for i, (elem, act, std, uom) in enumerate(variances):
            ry, rh = rows[i]
            diff = act - std
            pct = (diff / std) * 100.0 if std != 0 else 0.0
            is_favorable = diff <= 0

            row_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left + 0.15), Inches(ry), Inches(width - 0.30), Inches(rh))
            row_box.fill.solid()
            row_box.fill.fore_color.rgb = theme.surface_alt if i % 2 == 1 else theme.surface
            row_box.line.color.rgb = theme.border
            tf_r = row_box.text_frame
            tf_r.word_wrap = True
            
            p = tf_r.paragraphs[0]
            TypographySystem.apply_to_paragraph(p, TypographySystem.BODY_STRONG, f"{elem:<25} Actual: {act:,.0f} {uom} | Std: {std:,.0f} {uom}", theme.text_primary)
            
            var_str = f"   Variance: {diff:+,.0f} {uom} ({pct:+.1f}%)"
            p_v = tf_r.add_paragraph()
            color = theme.status_success if is_favorable else theme.status_critical
            TypographySystem.apply_to_paragraph(p_v, TypographySystem.ANNOTATION, var_str, color)


class CapacityVsDemandPrimitive:
    """32. Capacity vs Demand (Work-Center Hours Available vs Loaded Work Orders)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               work_centers: List[Tuple[str, float, float]], # [(wc_name, capacity_hrs, demand_hrs)]
               theme: Theme):
        SurfacePrimitive.render(slide, left, top, width, height, theme)
        cols = GridCalculator.get_columns(len(work_centers), left=left + 0.2, total_width=width - 0.4, gap=0.20)
        max_val = max(max(c, d) for _, c, d in work_centers) * 1.25

        for i, (wc, cap, dem) in enumerate(work_centers):
            cx, cw = cols[i]
            utilization = (dem / cap) * 100.0 if cap > 0 else 0.0
            is_bottleneck = utilization > 100.0

            # Capacity bar (light outline)
            cap_h = (cap / max_val) * (height - 1.4)
            cap_y = top + height - 0.5 - cap_h
            b_cap = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(cap_y), Inches(cw * 0.45), Inches(cap_h))
            b_cap.fill.solid()
            b_cap.fill.fore_color.rgb = theme.surface_highlight
            b_cap.line.color.rgb = theme.border_accent

            # Demand bar
            dem_h = (dem / max_val) * (height - 1.4)
            dem_y = top + height - 0.5 - dem_h
            b_dem = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx + cw * 0.50), Inches(dem_y), Inches(cw * 0.45), Inches(dem_h))
            b_dem.fill.solid()
            b_dem.fill.fore_color.rgb = theme.status_critical if is_bottleneck else theme.accent_primary
            b_dem.line.fill.background()

            # Utilization tag
            tb = slide.shapes.add_textbox(Inches(cx), Inches(top + 0.15), Inches(cw), Inches(0.35))
            TypographySystem.apply_to_paragraph(tb.text_frame.paragraphs[0], TypographySystem.LABEL, f"{utilization:.0f}% UTIL", theme.status_critical if is_bottleneck else theme.text_accent)

            # Work center label below
            lbl = slide.shapes.add_textbox(Inches(cx), Inches(top + height - 0.45), Inches(cw), Inches(0.40))
            TypographySystem.apply_to_paragraph(lbl.text_frame.paragraphs[0], TypographySystem.CAPTION, wc, theme.text_muted)


class AgingAnalysisPrimitive:
    """33. Aging Analysis buckets (<30, 31–60, 61–90, >90 Days) for WIP, AP, or AR."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               buckets: List[Tuple[str, str, str]], # [(bucket_name, amount_str, count_str)]
               theme: Theme):
        cols = GridCalculator.get_columns(len(buckets), left=left, total_width=width, gap=0.25)
        for i, (b_name, amount, count_info) in enumerate(buckets):
            cx, cw = cols[i]
            border_c = theme.status_critical if ">90" in b_name else (theme.status_warning if "60" in b_name else theme.border)
            SurfacePrimitive.render(slide, cx, top, cw, height, theme, border_color=border_c)

            tb = slide.shapes.add_textbox(Inches(cx + 0.14), Inches(top + 0.14), Inches(cw - 0.28), Inches(height - 0.28))
            tf = tb.text_frame
            tf.word_wrap = True
            TypographySystem.apply_to_paragraph(tf.paragraphs[0], TypographySystem.LABEL, b_name, border_c)
            p_val = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_val, TypographySystem.KPI_NUMBER, amount, theme.text_primary)
            p_val.space_after = Pt(4)
            p_cnt = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_cnt, TypographySystem.CAPTION, count_info, theme.text_muted)


class RiskMatrixPrimitive:
    """34. Risk Matrix (Probability vs Impact Heatmap)."""

    @staticmethod
    def render(slide, left: float, top: float, width: float, height: float,
               risks: List[Tuple[str, int, int, str]], # [(risk_name, likelihood_1_to_3, impact_1_to_3, mitigation)]
               theme: Theme):
        SurfacePrimitive.render(slide, left, top, width, height, theme)
        grid_w = width * 0.55
        grid_h = height - 0.6
        cell_w = grid_w / 3.0
        cell_h = grid_h / 3.0

        # Draw 3x3 cells (1=Low, 2=Medium, 3=High)
        for row in range(3):
            for col in range(3):
                cx = left + 0.3 + col * cell_w
                cy = top + 0.3 + (2 - row) * cell_h
                score = (row + 1) * (col + 1)
                cell_color = theme.status_critical if score >= 6 else (theme.status_warning if score >= 3 else theme.status_success)

                cbox = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx + 0.04), Inches(cy + 0.04), Inches(cell_w - 0.08), Inches(cell_h - 0.08))
                cbox.fill.solid()
                cbox.fill.fore_color.rgb = theme.surface_alt
                cbox.line.color.rgb = cell_color
                cbox.line.width = Pt(1.5 if score >= 6 else 1.0)

        # Plot risks on right list (45% right)
        list_x = left + grid_w + 0.5
        list_w = width - grid_w - 0.7
        tb = slide.shapes.add_textbox(Inches(list_x), Inches(top + 0.3), Inches(list_w), Inches(height - 0.6))
        tf = tb.text_frame
        tf.word_wrap = True
        TypographySystem.apply_to_paragraph(tf.paragraphs[0], TypographySystem.LABEL, "IDENTIFIED RISKS & MITIGATIONS", theme.text_accent)
        for r_name, lk, imp, mit in risks[:4]:
            p = tf.add_paragraph()
            p.space_after = Pt(2)
            TypographySystem.apply_to_paragraph(p, TypographySystem.BODY_STRONG, f"•  {r_name} (L{lk}/I{imp})", theme.text_primary)
            p_m = tf.add_paragraph()
            p_m.space_after = Pt(6)
            TypographySystem.apply_to_paragraph(p_m, TypographySystem.CAPTION, f"    Mitigation: {mit}", theme.text_muted)
