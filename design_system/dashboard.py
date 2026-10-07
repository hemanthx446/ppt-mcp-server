"""
Executive Dashboard & Analytical Cockpit Composition Engine.

A dashboard is NOT a collection of KPI cards.
An executive analytical cockpit combines:
1. Executive KPI strip ("WHAT CHANGED?")
2. Analytical trend / comparison visualization ("WHY DOES IT MATTER?")
3. Breakdown / segmentation / distribution ("WHERE IS THE PROBLEM?")
4. Action-oriented exception detail & drill-down table ("WHAT SHOULD WE ACT ON?")

Determines composition directly from the business question:
- "Are we shipping what we promised?"   => OTIF KPI + Shipment Trend + Delayed Order Exception Table
- "Where is production constrained?"     => Capacity vs Demand + Bottleneck Ranking + Work-Center Action Table
- "What is driving poor quality?"       => Pareto Root Causes + Defect Trend + Station/Shift Heatmap
- "Where is working capital trapped?"   => Working Capital KPI + WIP Aging Analysis + Trapped Stock Action Table
- "Which suppliers are creating risk?"  => Supplier OTIF KPI + Lead-Time Drift Trend + Critical Shortage Table
- "How much is quality costing us?"     => COPQ KPI + Defect Cost Pareto + Work-Center Scrap Cost Breakdown

Strictly avoids decoration or fake Power BI chrome.
Every visualization is tied directly to a business decision and uses native PowerPoint shapes, charts, and tables.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Any, Optional, Tuple
import re

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

from .typography import TypographySystem
from .spacing import CanvasBounds, Margins, SpacingScale, GridCalculator
from .color import Theme, ExecutiveNavyTheme, ConsultingSlateTheme
from .primitives import HeaderPrimitive, FooterPrimitive, SurfacePrimitive, TablePrimitive
import design_system.library as lib


# =============================================================================
# 1. Dashboard Archetypes
# =============================================================================

class DashboardArchetype(Enum):
    SHIPPING_PROMISE = auto()         # "Are we shipping what we promised?"
    PRODUCTION_CONSTRAINTS = auto()   # "Where is production constrained?"
    QUALITY_DRIVERS = auto()          # "What is driving poor quality?"
    WORKING_CAPITAL_WIP = auto()      # "Where is working capital trapped?"
    SUPPLIER_RISK = auto()            # "Which suppliers are creating risk?"
    COPQ_FINANCIAL = auto()           # "How much is quality costing us?"
    CUSTOM_COCKPIT = auto()           # Dynamic / tailored business question


# =============================================================================
# 2. Business Question Classifier
# =============================================================================

class DashboardQuestionClassifier:
    """Classifies an executive business question into the target cockpit archetype."""

    QUESTION_RULES = [
        (DashboardArchetype.SHIPPING_PROMISE, [
            "shipping", "promised", "otif", "on-time", "delivery", "fulfillment",
            "backlog", "shipment", "customer sla", "dispatch", "order lead time"
        ]),
        (DashboardArchetype.PRODUCTION_CONSTRAINTS, [
            "production constrained", "constrained", "bottleneck", "capacity vs demand",
            "capacity", "demand", "work center", "machine load", "spindle", "throughput", "starved"
        ]),
        (DashboardArchetype.COPQ_FINANCIAL, [
            "quality costing", "cost of poor quality", "cost of quality", "copq", "scrap cost",
            "warranty cost", "rework expense", "quality cost", "financial waste"
        ]),
        (DashboardArchetype.QUALITY_DRIVERS, [
            "poor quality", "driving quality", "defect", "scrap", "first pass yield",
            "fpy", "tolerance", "ncr", "rework", "root cause", "non-conformance"
        ]),
        (DashboardArchetype.WORKING_CAPITAL_WIP, [
            "working capital", "trapped", "wip", "inventory aging", "aging",
            "excess stock", "holding cost", "inventory turns", "slow-moving", "days of supply"
        ]),
        (DashboardArchetype.SUPPLIER_RISK, [
            "supplier", "vendor", "shortage", "lead-time drift", "lead time drift",
            "supplier risk", "tier 1", "tier 2", "procurement risk", "stockout"
        ]),
    ]

    @classmethod
    def classify(cls, question_or_title: str) -> DashboardArchetype:
        lowered = question_or_title.lower()
        for archetype, keywords in cls.QUESTION_RULES:
            if any(k in lowered for k in keywords):
                return archetype
        return DashboardArchetype.CUSTOM_COCKPIT


# =============================================================================
# 3. Cockpit Specification Data Models
# =============================================================================

@dataclass
class ExecutiveCockpitSpec:
    """Specification for an executive analytical dashboard slide."""
    business_question: str             # e.g., "Are we shipping what we promised?"
    key_takeaway: str                  # e.g., "OTIF at 84.2% (-7.8% vs SLA) caused by Tier-1 harness delays"
    category_tag: str = "EXECUTIVE ANALYTICAL COCKPIT"
    is_dark: bool = False              # Slate Light provides maximum tabular & chart contrast
    client_name: str = "Executive Leadership"
    
    # 1. Executive KPI Strip ("WHAT CHANGED?")
    kpi_strip: Optional[List[Tuple[str, str, Optional[str], Optional[str], bool]]] = None
    
    # 2. Analytical Trend / Comparison ("WHY DOES IT MATTER?")
    trend_title: str = "HISTORICAL TREND & COMMITMENT TRAJECTORY"
    trend_type: str = "line"           # 'line', 'bar', 'variance'
    trend_periods: Optional[List[str]] = None
    trend_series: Optional[List[Tuple[str, List[float]]]] = None
    
    # 3. Structural Breakdown ("WHERE IS THE PROBLEM?")
    breakdown_title: str = "ROOT-CAUSE SEGMENTATION & BOTTLENECK CONCENTRATION"
    breakdown_type: str = "pareto"      # 'pareto', 'capacity', 'aging', 'heatmap'
    breakdown_data: Optional[Any] = None
    
    # 4. Action-Oriented Exception Detail Table ("WHAT SHOULD WE ACT ON?")
    action_table_title: str = "CRITICAL EXCEPTIONS & IMMEDIATE INTERVENTION REGISTER"
    action_table_headers: Optional[List[str]] = None
    action_table_rows: Optional[List[List[str]]] = None
    action_table_weights: Optional[List[float]] = None


# =============================================================================
# 4. Executive Dashboard Composer
# =============================================================================

class ExecutiveDashboardComposer:
    """
    Renders high-density, multi-visualization executive analytical cockpits.
    Avoids decorative clutter and fake Power BI chrome.
    """

    @classmethod
    def compose_and_render(
        cls,
        prs: Presentation,
        spec: ExecutiveCockpitSpec
    ):
        """Builds a complete, native PowerPoint analytical cockpit slide."""
        theme = ExecutiveNavyTheme if spec.is_dark else ConsultingSlateTheme
        blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
        slide = prs.slides.add_slide(blank_layout)

        # 1. Full Canvas Surface
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(CanvasBounds.width), Inches(CanvasBounds.height))
        bg.fill.solid()
        bg.fill.fore_color.rgb = theme.canvas
        bg.line.fill.background()

        # 2. Header: Business Question + Action Takeaway
        HeaderPrimitive.render(
            slide=slide,
            category_text=f"{spec.category_tag} • {spec.business_question.upper()}",
            title_text=spec.business_question,
            subtitle_text=f"ACTION SUMMARY: {spec.key_takeaway}",
            theme=theme
        )

        # 3. Universal Footer
        FooterPrimitive.render(
            slide=slide,
            slide_num=1,
            total_slides=1,
            metadata_text=f"{spec.client_name} • Operational Decision Cockpit • Confidential",
            theme=theme
        )

        # Spatial Coordinates (Usable width = 11.733")
        left = Margins.left
        total_w = Margins().usable_width

        # ---------------------------------------------------------------------
        # ZONE 1: Executive KPI Strip ("WHAT CHANGED?")
        # ---------------------------------------------------------------------
        kpi_top = 1.36
        kpi_height = 1.08
        if spec.kpi_strip:
            lib.KPIStripPrimitive.render(
                slide=slide,
                left=left,
                top=kpi_top,
                width=total_w,
                height=kpi_height,
                kpis=spec.kpi_strip,
                theme=theme
            )
            mid_top = kpi_top + kpi_height + 0.32
        else:
            mid_top = 1.40

        # ---------------------------------------------------------------------
        # ZONE 2 & ZONE 3: Analytical Core (Trend + Breakdown Side-by-Side)
        # ---------------------------------------------------------------------
        mid_height = 2.45
        (c1_x, c1_w), (c2_x, c2_w) = GridCalculator.get_split(left_ratio=0.50, left=left, total_width=total_w, gap=0.25)

        # Left Column: Trend / Comparison ("WHY DOES IT MATTER?")
        cls._render_zone_label(slide, c1_x, mid_top - 0.22, f"2. WHY DOES IT MATTER? ({spec.trend_title})", theme)
        cls._render_trend_component(slide, c1_x, mid_top, c1_w, mid_height, spec, theme)

        # Right Column: Root-Cause Breakdown / Segmentation ("WHERE IS THE PROBLEM?")
        cls._render_zone_label(slide, c2_x, mid_top - 0.22, f"3. WHERE IS THE PROBLEM? ({spec.breakdown_title})", theme)
        cls._render_breakdown_component(slide, c2_x, mid_top, c2_w, mid_height, spec, theme)

        # ---------------------------------------------------------------------
        # ZONE 4: Action-Oriented Exception Detail Table ("WHAT SHOULD WE ACT ON?")
        # ---------------------------------------------------------------------
        bot_top = mid_top + mid_height + 0.32
        bot_height = 6.95 - bot_top
        if bot_height >= 1.20 and spec.action_table_headers and spec.action_table_rows:
            cls._render_zone_label(slide, left, bot_top - 0.22, f"4. WHAT SHOULD WE ACT ON? ({spec.action_table_title})", theme)
            TablePrimitive.render(
                slide=slide,
                left=left,
                top=bot_top,
                width=total_w,
                height=bot_height,
                headers=spec.action_table_headers,
                rows=spec.action_table_rows,
                theme=theme,
                col_weights=spec.action_table_weights
            )

        return slide

    @staticmethod
    def _render_zone_label(slide, left: float, top: float, text: str, theme: Theme):
        """Renders an analytical section question label above each visualization zone."""
        tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(5.8), Inches(0.24))
        tf = tb.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        TypographySystem.apply_to_paragraph(p, TypographySystem.LABEL, text, theme.text_accent)

    @classmethod
    def _render_trend_component(cls, slide, left: float, top: float, width: float, height: float, spec: ExecutiveCockpitSpec, theme: Theme):
        """Renders the trend or comparative chart."""
        if spec.trend_periods and spec.trend_series:
            if spec.trend_type == "bar":
                lib.BarChartPrimitive.render(
                    slide=slide, left=left, top=top, width=width, height=height,
                    categories=spec.trend_periods,
                    series_data=spec.trend_series,
                    theme=theme
                )
            else:
                lib.TrendChartPrimitive.render(
                    slide=slide, left=left, top=top, width=width, height=height,
                    periods=spec.trend_periods,
                    series_data=spec.trend_series,
                    theme=theme
                )
        else:
            # Fallback surface container
            SurfacePrimitive.render(slide, left, top, width, height, theme)

    @classmethod
    def _render_breakdown_component(cls, slide, left: float, top: float, width: float, height: float, spec: ExecutiveCockpitSpec, theme: Theme):
        """Renders the breakdown, Pareto, capacity, or heatmap visualization."""
        b_type = spec.breakdown_type.lower()
        data = spec.breakdown_data

        if b_type == "pareto" and isinstance(data, list):
            lib.ParetoPrimitive.render(slide, left, top, width, height, items=data, theme=theme)
        elif b_type == "capacity" and isinstance(data, list):
            lib.CapacityVsDemandPrimitive.render(slide, left, top, width, height, work_centers=data, theme=theme)
        elif b_type == "aging" and isinstance(data, list):
            lib.AgingAnalysisPrimitive.render(slide, left, top, width, height, buckets=data, theme=theme)
        elif b_type == "heatmap" and isinstance(data, dict):
            lib.HeatmapPrimitive.render(
                slide, left, top, width, height,
                row_labels=data.get("rows", []),
                col_labels=data.get("cols", []),
                values_matrix=data.get("matrix", []),
                theme=theme
            )
        else:
            SurfacePrimitive.render(slide, left, top, width, height, theme)

    # =========================================================================
    # Factory Methods for Canonical Executive Questions
    # =========================================================================

    @classmethod
    def build_from_question(
        cls,
        question: str,
        custom_data: Optional[Dict[str, Any]] = None,
        client_name: str = "Executive Leadership"
    ) -> ExecutiveCockpitSpec:
        """
        Synthesizes a complete analytical cockpit specification directly from an executive business question.
        """
        archetype = DashboardQuestionClassifier.classify(question)
        cdata = custom_data or {}

        # 1. "Are we shipping what we promised?"
        if archetype == DashboardArchetype.SHIPPING_PROMISE:
            return ExecutiveCockpitSpec(
                business_question=question if question else "Are we shipping what we promised?",
                key_takeaway=cdata.get("takeaway", "Customer OTIF fell to 84.2% (Target 95.0%) due to sub-tier harness component shortages on SMT Line 2."),
                category_tag="OPERATIONAL FULFILLMENT COCKPIT",
                client_name=client_name,
                kpi_strip=cdata.get("kpi_strip", [
                    ("84.2%", "On-Time In-Full (OTIF)", "Global Fulfillment", "-10.8% vs SLA", False),
                    ("184", "Delayed Sales Orders", "Pending Release", "+28 orders", False),
                    ("2.4 Days", "Mean Dispatch Delay", "Shipping Dock Avg", "-0.6 Days", True),
                    ("$1.82M", "Revenue at Risk", "Past Due Orders", "+$420k WoW", False)
                ]),
                trend_title="6-MONTH OTIF COMMITMENT VS ACTUAL PERFORMANCE",
                trend_type="line",
                trend_periods=cdata.get("trend_periods", ["May", "Jun", "Jul", "Aug", "Sep", "Oct"]),
                trend_series=cdata.get("trend_series", [
                    ("Actual OTIF %", [94.0, 92.5, 91.0, 88.4, 86.2, 84.2]),
                    ("Target SLA %", [95.0, 95.0, 95.0, 95.0, 95.0, 95.0])
                ]),
                breakdown_title="ROOT-CAUSE DISPATCH DELAY PARETO",
                breakdown_type="pareto",
                breakdown_data=cdata.get("breakdown_data", [
                    ("Sub-Tier Component Shortage", 48.0),
                    ("Machine Spindle Breakdown", 24.0),
                    ("Carrier Booking Bottleneck", 14.0),
                    ("Quality Hold / Inspection", 10.0),
                    ("Label / Documentation Error", 4.0)
                ]),
                action_table_title="CRITICAL CUSTOMER SHIPMENT EXCEPTION REGISTER",
                action_table_headers=["SALES ORDER", "CUSTOMER", "PRODUCT LINE", "DELAY", "VALUE", "BLOCKING REASON", "ACTION"],
                action_table_weights=[1.1, 1.8, 1.4, 0.8, 0.9, 1.8, 1.0],
                action_table_rows=cdata.get("action_table_rows", [
                    ["SO-90142", "Boeing Defense", "Actuator Mod 24V", "+4 Days", "$420,000", "Titanium Fastener Lot Hold", "Expedite QA"],
                    ["SO-90188", "Airbus Atlantic", "Optical Sensors", "+6 Days", "$315,000", "Wire Harness Supplier Shortage", "Air Freight"],
                    ["SO-90204", "Raytheon Systems", "Solenoid Valves", "+3 Days", "$280,000", "CNC Bay 4 Spindle Maintenance", "Reroute Cell 2"],
                    ["SO-90220", "Lockheed Aero", "Power Regulators", "+5 Days", "$240,000", "Final Acceptance Calibration", "Overtime Shift"]
                ])
            )

        # 2. "Where is production constrained?"
        elif archetype == DashboardArchetype.PRODUCTION_CONSTRAINTS:
            return ExecutiveCockpitSpec(
                business_question=question if question else "Where is production constrained?",
                key_takeaway=cdata.get("takeaway", "CNC 5-Axis Milling and Cleanroom SMT assembly operate at >115% capacity demand, starving downstream packaging."),
                category_tag="PLANT BOTTLENECK & CAPACITY COCKPIT",
                client_name=client_name,
                kpi_strip=cdata.get("kpi_strip", [
                    ("118%", "Critical Bottleneck Load", "5-Axis Milling Bay", "+18% Over Capacity", False),
                    ("42.5 Hrs", "Unplanned Downtime", "Monthly Rolling Total", "-14% MoM", True),
                    ("71.4%", "Overall Plant OEE", "Benchmark 85.0%", "-13.6 pts vs Target", False),
                    ("14 Cells", "Active Work Centers", "All 3 Shifts", "3 Cells Overloaded", False)
                ]),
                trend_title="WEEKLY WORK LOAD VS OPERATING CAPACITY (HOURS)",
                trend_type="bar",
                trend_periods=cdata.get("trend_periods", ["Wk 38", "Wk 39", "Wk 40", "Wk 41", "Wk 42"]),
                trend_series=cdata.get("trend_series", [
                    ("Demand Hours", [520.0, 540.0, 580.0, 610.0, 595.0]),
                    ("Max Capacity", [500.0, 500.0, 500.0, 500.0, 500.0])
                ]),
                breakdown_title="WORK-CENTER CAPACITY VS DEMAND (HOURS)",
                breakdown_type="capacity",
                breakdown_data=cdata.get("breakdown_data", [
                    ("CNC 5-Axis Bay", 160.0, 192.0),
                    ("SMT Line Alpha", 140.0, 162.0),
                    ("Optical Testing", 120.0, 115.0),
                    ("Final Packaging", 100.0, 72.0)
                ]),
                action_table_title="BOTTLENECK WORK-CENTER RESOLUTION ACTIONS",
                action_table_headers=["WORK CENTER", "MACHINE ID", "CAPACITY", "DEMAND", "LOAD %", "ROOT CONSTRAINT", "IMMEDIATE ACTION"],
                action_table_weights=[1.4, 1.0, 0.9, 0.9, 0.9, 1.8, 1.4],
                action_table_rows=cdata.get("action_table_rows", [
                    ["CNC 5-Axis Bay", "DMG-5001", "160 Hrs", "192 Hrs", "120%", "Tool wear & 3.2h setup time", "Authorize Weekend OT"],
                    ["SMT Line Alpha", "Fuji-NXT3", "140 Hrs", "162 Hrs", "116%", "Nozzle feeder jam micro-stops", "Preventive Spindle Tune"],
                    ["Optical Test Bay", "Opti-9000", "120 Hrs", "115 Hrs", "96%", "Manual calibration steps", "Automate Cognex Vision"],
                    ["Final Assembly", "Assy-Bay-2", "100 Hrs", "72 Hrs", "72%", "Starved by upstream CNC delay", "Rebalance Manpower"]
                ])
            )

        # 3. "What is driving poor quality?"
        elif archetype == DashboardArchetype.QUALITY_DRIVERS:
            return ExecutiveCockpitSpec(
                business_question=question if question else "What is driving poor quality?",
                key_takeaway=cdata.get("takeaway", "Solder voiding on SMT Line Alpha and CNC tolerance drift on Shift C account for 74% of all defective lots."),
                category_tag="QUALITY DEFECT ROOT-CAUSE COCKPIT",
                client_name=client_name,
                kpi_strip=cdata.get("kpi_strip", [
                    ("91.2%", "First Pass Yield (FPY)", "Plant Wide Rolling 30D", "-4.8% vs Target", False),
                    ("2.84%", "Scrap & Rework Rate", "Total Material Cost", "+0.9% Unfavorable", False),
                    ("48 Lots", "NCR Holds in Quarantine", "Pending Review Board", "-12 Lots Resolved", True),
                    ("$460k", "Monthly Scrap Expense", "YTD Scrap Ledger", "+$72k vs Budget", False)
                ]),
                trend_title="DAILY FIRST PASS YIELD TRAJECTORY (%)",
                trend_type="line",
                trend_periods=cdata.get("trend_periods", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]),
                trend_series=cdata.get("trend_series", [
                    ("FPY % Actual", [94.5, 93.2, 90.8, 89.4, 91.0, 91.2]),
                    ("FPY % Target", [96.0, 96.0, 96.0, 96.0, 96.0, 96.0])
                ]),
                breakdown_title="QUALITY DEFECT CONCENTRATION PARETO",
                breakdown_type="pareto",
                breakdown_data=cdata.get("breakdown_data", [
                    ("SMT Solder Voiding", 52.0),
                    ("CNC Tolerance Drift", 22.0),
                    ("Component Pin Bending", 14.0),
                    ("Optical Misalignment", 8.0),
                    ("Surface Scratch / Cosmetic", 4.0)
                ]),
                action_table_title="ACTIVE NCR QUALITY INTERVENTION REGISTER",
                action_table_headers=["NCR ID", "WORK STATION", "DEFECT TYPE", "SEVERITY", "LOT SIZE", "ROOT CAUSE", "CONTAINMENT ACTION"],
                action_table_weights=[0.9, 1.3, 1.4, 0.9, 0.9, 1.8, 1.4],
                action_table_rows=cdata.get("action_table_rows", [
                    ["NCR-2026-081", "SMT Line Alpha", "Solder Voiding", "Critical", "450 Units", "Reflow oven zone 3 temp drop", "Recalibrate profile"],
                    ["NCR-2026-084", "CNC Cell 3", "Bore Diameter Drift", "Major", "120 Units", "Carbide insert thermal wear", "Tool offset update"],
                    ["NCR-2026-089", "Optical Test", "Photodiode Lux Bias", "Moderate", "200 Units", "Fixture ambient illumination", "Shield enclosure"],
                    ["NCR-2026-092", "Manual Assy", "Connector Pin Bend", "Minor", "80 Units", "Hand insertion pressure exceed", "Poka-yoke jig install"]
                ])
            )

        # 4. "Where is working capital trapped?"
        elif archetype == DashboardArchetype.WORKING_CAPITAL_WIP:
            return ExecutiveCockpitSpec(
                business_question=question if question else "Where is working capital trapped?",
                key_takeaway=cdata.get("takeaway", "$4.8M of working capital is trapped in aging WIP (>60 days), primarily in delayed sub-assemblies waiting on single-source ICs."),
                category_tag="WORKING CAPITAL & WIP AGING COCKPIT",
                client_name=client_name,
                kpi_strip=cdata.get("kpi_strip", [
                    ("$14.2M", "Total Plant WIP Value", "ACDOCA Material Ledger", "+$2.4M vs Target", False),
                    ("42 Days", "Days of Inventory Supply", "Average DSI", "+9 Days Unfavorable", False),
                    ("$4.8M", "Aging WIP (>60 Days)", "Sub-Assembly Quarantine", "34% of Total WIP", False),
                    ("18.2%", "WIP Holding Cost", "Annualized Cost of Capital", "$2.58M/Yr Cost", False)
                ]),
                trend_title="MONTHLY WORKING CAPITAL IN WIP ($ MILLIONS)",
                trend_type="line",
                trend_periods=cdata.get("trend_periods", ["May", "Jun", "Jul", "Aug", "Sep", "Oct"]),
                trend_series=cdata.get("trend_series", [
                    ("WIP Actual ($M)", [11.2, 11.8, 12.4, 13.1, 13.8, 14.2]),
                    ("WIP Target ($M)", [11.0, 11.0, 11.0, 11.0, 11.0, 11.0])
                ]),
                breakdown_title="WIP AGING BUCKETS ANALYSIS",
                breakdown_type="aging",
                breakdown_data=cdata.get("breakdown_data", [
                    ("< 30 Days", "$6.4M", "68 Batch Lots"),
                    ("31 - 60 Days", "$3.0M", "24 Batch Lots"),
                    ("61 - 90 Days", "$2.8M", "18 Batch Lots"),
                    ("> 90 Days", "$2.0M", "11 Batch Lots")
                ]),
                action_table_title="TOP TRAPPED INVENTORY LOTS & LIQUIDATION PLAN",
                action_table_headers=["MATERIAL", "PART DESCRIPTION", "AGING", "TRAPPED VALUE", "LOT STATUS", "BLOCKING REASON", "LIQUIDATION ACTION"],
                action_table_weights=[1.1, 1.8, 0.8, 1.0, 1.0, 1.6, 1.2],
                action_table_rows=cdata.get("action_table_rows", [
                    ["MAT-9021", "Turbine Actuator Sub-Assy", "104 Days", "$1,450,000", "Quarantined", "Missing optical chip", "Spot purchase broker IC"],
                    ["MAT-8840", "Sensor Circuit Boards", "88 Days", "$980,000", "QA Rework", "Solder rework backlog", "Authorize weekend shift"],
                    ["MAT-7721", "Titanium Cast Housings", "74 Days", "$820,000", "Hold", "Engineering ECN change", "Release revised BOM"],
                    ["MAT-6610", "High-Pressure Valves", "92 Days", "$650,000", "Quarantined", "Batch certification hold", "Expedite lab cert"]
                ])
            )

        # 5. "Which suppliers are creating risk?"
        elif archetype == DashboardArchetype.SUPPLIER_RISK:
            return ExecutiveCockpitSpec(
                business_question=question if question else "Which suppliers are creating risk?",
                key_takeaway=cdata.get("takeaway", "Three single-sourced electronic suppliers exhibit an average lead-time drift of +18 days, creating $3.2M in downstream stockout risk."),
                category_tag="SUPPLIER RESILIENCE & LEAD-TIME DRIFT COCKPIT",
                client_name=client_name,
                kpi_strip=cdata.get("kpi_strip", [
                    ("78.4%", "Supplier Delivery OTIF", "Direct Material Vendors", "-16.6% vs Target", False),
                    ("+14.2 Days", "Avg Lead-Time Drift", "Actual vs Contract SLA", "+6 Days Deterioration", False),
                    ("8 Vendors", "Critical High-Risk Suppliers", "Single-Sourced Parts", "3 At Severe Risk", False),
                    ("$3.2M", "Production Value at Risk", "Potential Stockouts", "Next 45-Day Horizon", False)
                ]),
                trend_title="LEAD-TIME DRIFT ACROSS CRITICAL VENDORS (DAYS)",
                trend_type="bar",
                trend_periods=cdata.get("trend_periods", ["Vendor A", "Vendor B", "Vendor C", "Vendor D", "Vendor E"]),
                trend_series=cdata.get("trend_series", [
                    ("Actual Lead Time", [48.0, 42.0, 36.0, 30.0, 24.0]),
                    ("Contract SLA", [30.0, 28.0, 28.0, 25.0, 21.0])
                ]),
                breakdown_title="SUPPLIER DEFECT & DELAY IMPACT PARETO",
                breakdown_type="pareto",
                breakdown_data=cdata.get("breakdown_data", [
                    ("Microchip Fab Allocation", 54.0),
                    ("Raw Titanium Mill Backlog", 22.0),
                    ("Custom Harness Cable Delay", 14.0),
                    ("Air Freight Customs Clearance", 7.0),
                    ("Packaging Vendor Damage", 3.0)
                ]),
                action_table_title="CRITICAL SUPPLIER DUAL-SOURCING & BUFFER PLAN",
                action_table_headers=["VENDOR", "COMMODITY", "CONTRACT SLA", "ACTUAL LEAD", "DRIFT", "SINGLE SOURCED", "MITIGATION STRATEGY"],
                action_table_weights=[1.4, 1.4, 1.0, 1.0, 0.8, 1.0, 1.8],
                action_table_rows=cdata.get("action_table_rows", [
                    ["Apex Semi", "Optical Sensor ICs", "30 Days", "48 Days", "+18 Days", "Yes (Sole Source)", "Qualify secondary Taiwan source"],
                    ["Titanium Forge", "M4 Titanium Rods", "28 Days", "42 Days", "+14 Days", "Yes (Direct Mill)", "Buffer 60-day safety stock"],
                    ["ElectroHarness", "Mil-Spec Wire Cable", "28 Days", "36 Days", "+8 Days", "No (Dual Vendor)", "Reroute volume to Vendor 2"],
                    ["Precision Seal", "High-Temp Viton O-Rings", "25 Days", "30 Days", "+5 Days", "No (Standard Part)", "Issue spot market PO"]
                ])
            )

        # 6. "How much is quality costing us?"
        elif archetype == DashboardArchetype.COPQ_FINANCIAL:
            return ExecutiveCockpitSpec(
                business_question=question if question else "How much is quality costing us?",
                key_takeaway=cdata.get("takeaway", "Total Cost of Poor Quality (COPQ) reached $3.42M annualized (4.8% of sales), heavily concentrated in scrap and rework."),
                category_tag="COST OF POOR QUALITY (COPQ) COCKPIT",
                client_name=client_name,
                kpi_strip=cdata.get("kpi_strip", [
                    ("$3.42M", "Annualized COPQ", "4.8% of Gross Sales", "+$620k vs Budget", False),
                    ("$1.84M", "Internal Scrap Expense", "Direct Material Loss", "54% of COPQ", False),
                    ("$940k", "Workstation Rework Cost", "Direct Labor Hours", "+18% YoY", False),
                    ("$640k", "Customer Warranty Claims", "Field Failure Returns", "-14% Favorable", True)
                ]),
                trend_title="MONTHLY COST OF POOR QUALITY ($ THOUSANDS)",
                trend_type="line",
                trend_periods=cdata.get("trend_periods", ["May", "Jun", "Jul", "Aug", "Sep", "Oct"]),
                trend_series=cdata.get("trend_series", [
                    ("Total COPQ ($k)", [260.0, 275.0, 285.0, 310.0, 295.0, 285.0]),
                    ("Budget Target ($k)", [220.0, 220.0, 220.0, 220.0, 220.0, 220.0])
                ]),
                breakdown_title="COPQ ELEMENT CONCENTRATION PARETO",
                breakdown_type="pareto",
                breakdown_data=cdata.get("breakdown_data", [
                    ("Raw Material Scrap", 54.0),
                    ("Assembly Line Rework", 26.0),
                    ("Field Warranty Repair", 12.0),
                    ("Re-Inspection Labor", 6.0),
                    ("Scrap Disposal Freight", 2.0)
                ]),
                action_table_title="PLANT-WIDE COPQ REDUCTION PROGRAM",
                action_table_headers=["PLANT CELL", "FAILURE MODE", "MONTHLY COST", "% OF COPQ", "ROOT CAUSE", "CONTAINMENT INTERVENTION", "ANNUAL SAVINGS"],
                action_table_weights=[1.2, 1.4, 1.0, 0.8, 1.6, 1.6, 1.1],
                action_table_rows=cdata.get("action_table_rows", [
                    ["CNC Bay 3", "Tool insert thermal fracture", "$68,000", "24%", "Coolant pump low pressure", "Replace pump & add sensor", "$816,000"],
                    ["SMT Alpha", "Reflow solder bridging", "$48,000", "17%", "Stencil aperture paste volume", "Laser-cut stencil redesign", "$576,000"],
                    ["Optical Lab", "Sensor photodiode misalignment", "$32,000", "11%", "Manual jig mounting variance", "Install computer vision guide", "$384,000"],
                    ["Final Test", "High-temp harness resistance", "$24,000", "8%", "Crimping tool calibration drift", "Automatic pneumatic crimper", "$288,000"]
                ])
            )

        # Fallback / Custom Cockpit
        else:
            return ExecutiveCockpitSpec(
                business_question=question,
                key_takeaway=cdata.get("takeaway", "Executive performance telemetry addressing core operational and financial drivers."),
                category_tag="EXECUTIVE DECISION COCKPIT",
                client_name=client_name,
                kpi_strip=cdata.get("kpi_strip", [
                    ("92.4%", "Overall Execution Index", "Enterprise Composite", "+3.2% vs Plan", True),
                    ("180ms", "System Event Latency", "Core SLA", "Sub-second met", True),
                    ("$2.4M", "Value Acceleration", "Delivered YTD", "+$400k Favorable", True),
                    ("99.1%", "First Pass Quality", "Plant Average", "+1.2% Improvement", True)
                ]),
                trend_title=cdata.get("trend_title", "PERFORMANCE TRAJECTORY OVER TIME"),
                trend_type=cdata.get("trend_type", "line"),
                trend_periods=cdata.get("trend_periods", ["P1", "P2", "P3", "P4", "P5", "P6"]),
                trend_series=cdata.get("trend_series", [
                    ("Actual Performance", [88.0, 89.5, 91.0, 90.8, 92.0, 92.4]),
                    ("Target Benchmark", [90.0, 90.0, 90.0, 90.0, 90.0, 90.0])
                ]),
                breakdown_title=cdata.get("breakdown_title", "CONTRIBUTION & SEGMENTATION BREAKDOWN"),
                breakdown_type=cdata.get("breakdown_type", "pareto"),
                breakdown_data=cdata.get("breakdown_data", [
                    ("Primary Segment Alpha", 45.0),
                    ("Secondary Segment Beta", 28.0),
                    ("Operating Node Gamma", 16.0),
                    ("Support Stream Delta", 11.0)
                ]),
                action_table_title=cdata.get("action_table_title", "PRIORITY ACTION & DECISION REGISTER"),
                action_table_headers=cdata.get("action_table_headers", ["ITEM ID", "WORKSTREAM", "METRIC IMPACT", "OWNER", "TARGET DATE", "ACTION PLAN"]),
                action_table_weights=[0.8, 1.4, 1.0, 1.0, 0.9, 2.0],
                action_table_rows=cdata.get("action_table_rows", [
                    ["ACT-01", "Core Operations", "+2.4% OEE", "Plant Lead", "Month 1", "Implement automated edge cycle capture"],
                    ["ACT-02", "Quality Control", "-0.8% Scrap", "QA Director", "Month 2", "Calibrate vision inspection tolerances"],
                    ["ACT-03", "Supply Chain", "+5 Days DSI", "SCM VP", "Month 3", "Enact supplier dual-sourcing framework"]
                ])
            )
