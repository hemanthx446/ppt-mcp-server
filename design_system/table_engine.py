"""
Enterprise Structured Information & Table Composition Engine.

Tables are first-class visual objects for enterprise documentation and consulting proposals:
- Strong typographic and visual hierarchy
- Section rows with full-width merged group headers
- Compact typography (Inter Regular, Inter Semi Bold, Inter Bold)
- Clear column relationships and calculated proportional widths
- Restrained borders (clean architectural outlines, no excessive cards or bubble boxes)
- Alignment strictly appropriate to data type:
  * Text/Descriptions -> Left aligned
  * IDs, Codes, Status, RACI -> Center aligned
  * Numbers, Financials ($), Percentages (%), Quantities -> Right aligned
- Semantic status indicators and badge coloring (Critical, Warning, Success, Must, Should, RACI)
- Hierarchy indentation for sub-items

Supports 12 canonical enterprise table archetypes:
1. Architecture Comparison
2. Requirements
3. Interface Catalogue
4. KPI Definitions
5. Risks
6. Assumptions
7. Commercial Proposal
8. Implementation Scope
9. Responsibility Matrix (RACI)
10. Roadmap
11. Business Benefits
12. Data Mappings
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Any, Optional, Tuple, Union
import re

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

from .typography import TypographySystem
from .spacing import CanvasBounds, Margins, SpacingScale, GridCalculator
from .color import Theme, ExecutiveNavyTheme, ConsultingSlateTheme, RGB
from .primitives import HeaderPrimitive, FooterPrimitive, SurfacePrimitive


# =============================================================================
# 1. Table Archetypes & Data Structures
# =============================================================================

class TableArchetype(Enum):
    ARCHITECTURE_COMPARISON = auto()
    REQUIREMENTS = auto()
    INTERFACE_CATALOGUE = auto()
    KPI_DEFINITIONS = auto()
    RISKS = auto()
    ASSUMPTIONS = auto()
    COMMERCIAL_PROPOSAL = auto()
    IMPLEMENTATION_SCOPE = auto()
    RESPONSIBILITY_MATRIX = auto()
    ROADMAP = auto()
    BUSINESS_BENEFITS = auto()
    DATA_MAPPINGS = auto()
    CUSTOM_TABLE = auto()


@dataclass
class TableRowItem:
    """An individual row, supporting either standard tabular cells or merged section headers."""
    cells: List[str]
    is_section_header: bool = False
    section_title: Optional[str] = None
    indent_level: int = 0              # Indentation for hierarchical sub-items


@dataclass
class EnterpriseTableSpec:
    """Specification for an enterprise structured information table slide."""
    title: str
    subtitle: str
    category_tag: str = "ENTERPRISE SPECIFICATION TABLE"
    client_name: str = "Enterprise Architecture"
    archetype: TableArchetype = TableArchetype.CUSTOM_TABLE
    headers: List[str] = field(default_factory=list)
    rows: List[Union[List[str], TableRowItem]] = field(default_factory=list)
    col_weights: Optional[List[float]] = None
    callout_note: Optional[str] = None # Strategic architectural footnote or guidance
    is_dark: bool = False              # Slate Light is recommended for dense tables for maximum legibility


# =============================================================================
# 2. Alignment & Data Type Classification
# =============================================================================

class TableDataClassifier:
    """Infers appropriate column alignment and typographic emphasis from data content."""

    NUMERIC_HEADER_KEYWORDS = {
        "value", "cost", "investment", "amount", "hours", "days", "latency",
        "score", "baseline", "target", "savings", "budget", "run-rate", "price",
        "payback", "units", "yield", "rate", "fpy", "otif"
    }

    CODE_OR_STATUS_HEADER_KEYWORDS = {
        "id", "code", "status", "priority", "severity", "probability", "gate",
        "phase", "raci", "tier", "quarter", "src type", "tgt type", "frequency",
        "owner", "moscow", "level", "state"
    }

    NUMERIC_PATTERN = re.compile(r"^[\$€£]?\s*[\+\-]?\d+(\.\d+)?%?(k|m|b|days|hrs|ms|s)?$", re.IGNORECASE)

    STATUS_CRITICAL = {"critical", "high", "severe", "blocker", "out of sla", "delayed", "red"}
    STATUS_WARNING = {"medium", "warning", "should", "major", "in progress", "amber", "moderate"}
    STATUS_SUCCESS = {"low", "resolved", "must", "active", "pass", "completed", "green", "minor", "verified"}
    RACI_ROLES = {"r", "a", "c", "i"}

    @classmethod
    def get_column_alignment(cls, header: str, sample_cells: List[str]) -> PP_ALIGN:
        """Determines left, center, or right alignment based on header and cell values."""
        h_clean = header.strip().lower()

        # Check header keywords first
        if any(kw in h_clean for kw in cls.NUMERIC_HEADER_KEYWORDS):
            return PP_ALIGN.RIGHT

        if any(kw == h_clean or kw in h_clean.split() for kw in cls.CODE_OR_STATUS_HEADER_KEYWORDS):
            return PP_ALIGN.CENTER

        # Inspect cell sample
        numeric_matches = sum(1 for c in sample_cells if cls.NUMERIC_PATTERN.match(c.strip()))
        if len(sample_cells) > 0 and (numeric_matches / len(sample_cells)) >= 0.5:
            return PP_ALIGN.RIGHT

        return PP_ALIGN.LEFT

    @classmethod
    def get_cell_text_color(cls, text: str, theme: Theme, is_header: bool = False) -> RGBColor:
        """Returns semantic status coloring for status tokens while preserving theme primary for regular text."""
        if is_header:
            return theme.text_accent

        t_clean = text.strip().lower()
        if t_clean in cls.STATUS_CRITICAL:
            return theme.status_critical
        elif t_clean in cls.STATUS_WARNING:
            return theme.status_warning
        elif t_clean in cls.STATUS_SUCCESS:
            return theme.status_success
        elif t_clean in cls.RACI_ROLES:
            return theme.text_accent

        return theme.text_primary


# =============================================================================
# 3. Enterprise Table Composer
# =============================================================================

class EnterpriseTableComposer:
    """
    Renders high-density, professional enterprise tables adhering to consulting standards:
    - Merged section header rows
    - Data-type alignment
    - Compact typography (Inter tokens)
    - Semantic status highlighting
    """

    @classmethod
    def compose_and_render(cls, prs: Presentation, spec: EnterpriseTableSpec):
        """Builds a complete, native PowerPoint structured table slide."""
        theme = ExecutiveNavyTheme if spec.is_dark else ConsultingSlateTheme
        blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
        slide = prs.slides.add_slide(blank_layout)

        # 1. Full Canvas Background
        bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0), Inches(0), Inches(CanvasBounds.width), Inches(CanvasBounds.height)
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = theme.canvas
        bg.line.fill.background()

        # 2. Header
        HeaderPrimitive.render(
            slide=slide,
            category_text=f"{spec.category_tag} • {spec.client_name.upper()}",
            title_text=spec.title,
            subtitle_text=spec.subtitle,
            theme=theme
        )

        # 3. Universal Footer
        FooterPrimitive.render(
            slide=slide,
            slide_num=1,
            total_slides=1,
            metadata_text=f"{spec.client_name} • Structured Architecture Specification • Strict Governance",
            theme=theme
        )

        # Usable Geometry
        left = Margins.left
        total_w = Margins().usable_width
        top = 1.30

        has_callout = bool(spec.callout_note)
        table_h = 5.20 if has_callout else 5.60

        # Render Table
        cls.render_table(
            slide=slide,
            left=left,
            top=top,
            width=total_w,
            height=table_h,
            headers=spec.headers,
            rows=spec.rows,
            theme=theme,
            col_weights=spec.col_weights
        )

        # Optional Strategic Callout / Footnote Banner
        if has_callout:
            callout_top = top + table_h + 0.12
            cls._render_callout_banner(slide, left, callout_top, total_w, 0.32, spec.callout_note, theme)

        return slide

    @classmethod
    def render_table(
        cls,
        slide,
        left: float,
        top: float,
        width: float,
        height: float,
        headers: List[str],
        rows: List[Union[List[str], TableRowItem]],
        theme: Theme,
        col_weights: Optional[List[float]] = None
    ):
        """Renders an enterprise table onto an existing slide with native python-pptx shapes."""
        c_count = len(headers)
        if c_count == 0:
            return

        # Normalize rows to TableRowItem
        norm_rows: List[TableRowItem] = []
        for r in rows:
            if isinstance(r, TableRowItem):
                norm_rows.append(r)
            elif isinstance(r, list):
                # Check if it's a section row marker (e.g., ["SECTION: 1. CORE ERP", ...])
                first_val = str(r[0]).strip() if r else ""
                if first_val.upper().startswith("SECTION:") or (len(r) == 1 and not first_val.startswith("•")):
                    sec_title = first_val.replace("SECTION:", "").strip()
                    norm_rows.append(TableRowItem(cells=[sec_title], is_section_header=True, section_title=sec_title))
                else:
                    norm_rows.append(TableRowItem(cells=[str(x) for x in r]))

        total_rows = len(norm_rows) + 1  # +1 for header row
        tbl_shape = slide.shapes.add_table(total_rows, c_count, Inches(left), Inches(top), Inches(width), Inches(height))
        tbl = tbl_shape.table

        # Proportional Column Widths
        if col_weights and len(col_weights) == c_count:
            sum_w = sum(col_weights)
            for c_idx, w in enumerate(col_weights):
                tbl.columns[c_idx].width = Inches((w / sum_w) * width)
        else:
            default_col = width / c_count
            for c_idx in range(c_count):
                tbl.columns[c_idx].width = Inches(default_col)

        # Determine column alignments
        col_alignments = []
        for c_idx, h in enumerate(headers):
            samples = [r.cells[c_idx] for r in norm_rows if not r.is_section_header and len(r.cells) > c_idx]
            col_alignments.append(TableDataClassifier.get_column_alignment(h, samples))

        # ---------------------------------------------------------------------
        # 1. Header Row
        # ---------------------------------------------------------------------
        for c_idx, h_text in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = theme.surface_highlight if not theme.is_dark else theme.surface
            tf = cell.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_right = Inches(0.08)
            tf.margin_top = tf.margin_bottom = Inches(0.04)

            p = tf.paragraphs[0]
            p.alignment = col_alignments[c_idx]
            TypographySystem.apply_to_paragraph(p, TypographySystem.TABLE_HEADER, h_text.upper(), theme.text_accent)

        # ---------------------------------------------------------------------
        # 2. Data Rows & Section Rows
        # ---------------------------------------------------------------------
        for r_idx, item in enumerate(norm_rows, start=1):
            if item.is_section_header:
                # Merge across all columns for clean full-width section divider
                first_cell = tbl.cell(r_idx, 0)
                last_cell = tbl.cell(r_idx, c_count - 1)
                first_cell.merge(last_cell)

                first_cell.fill.solid()
                first_cell.fill.fore_color.rgb = theme.surface_alt if not theme.is_dark else theme.surface_muted

                tf = first_cell.text_frame
                tf.word_wrap = True
                tf.margin_left = Inches(0.10)
                tf.margin_top = tf.margin_bottom = Inches(0.04)

                p = tf.paragraphs[0]
                sec_text = item.section_title or (item.cells[0] if item.cells else "SECTION")
                TypographySystem.apply_to_paragraph(p, TypographySystem.LABEL, f"• {sec_text.upper()}", theme.border_accent)

            else:
                row_fill = theme.surface if (r_idx % 2 == 1) else theme.surface_alt

                for c_idx in range(c_count):
                    val = item.cells[c_idx] if c_idx < len(item.cells) else ""
                    cell = tbl.cell(r_idx, c_idx)
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = row_fill

                    tf = cell.text_frame
                    tf.word_wrap = True
                    tf.margin_left = tf.margin_right = Inches(0.08)
                    tf.margin_top = tf.margin_bottom = Inches(0.04)

                    p = tf.paragraphs[0]
                    p.alignment = col_alignments[c_idx]

                    # Indentation support for child hierarchy items
                    display_text = val
                    if item.indent_level > 0 and c_idx == 0:
                        display_text = ("    " * item.indent_level) + f"↳ {val}"

                    # Color classification
                    txt_color = TableDataClassifier.get_cell_text_color(val, theme)
                    TypographySystem.apply_to_paragraph(p, TypographySystem.TABLE_BODY, display_text, txt_color)

                    # Bold primary column (Key ID or Subject)
                    if c_idx == 0 and not item.indent_level:
                        p.runs[0].font.bold = True

    @classmethod
    def _render_callout_banner(cls, slide, left: float, top: float, width: float, height: float,
                               note_text: str, theme: Theme):
        """Renders a strategic governance note below the table."""
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        banner.fill.solid()
        banner.fill.fore_color.rgb = theme.surface_highlight
        banner.line.color.rgb = theme.border_accent
        banner.line.width = Pt(1.0)

        tf = banner.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.12)
        tf.margin_top = tf.margin_bottom = Inches(0.02)

        p = tf.paragraphs[0]
        TypographySystem.apply_to_paragraph(p, TypographySystem.ANNOTATION, f"ARCHITECTURAL GOVERNANCE NOTE:  {note_text}", theme.text_accent)


# =============================================================================
# 4. Canonical Pre-Built Enterprise Table Templates (12 Archetypes)
# =============================================================================

class EnterpriseTableFactory:
    """Pre-built canonical enterprise tables for the 12 core solution disciplines."""

    @classmethod
    def get_table_spec(cls, archetype: TableArchetype, client_name: str = "Enterprise Architecture") -> EnterpriseTableSpec:
        """Returns rich, realistic enterprise table specifications for each canonical discipline."""

        # 1. Architecture Comparison
        if archetype == TableArchetype.ARCHITECTURE_COMPARISON:
            return EnterpriseTableSpec(
                title="Architecture Comparison: Legacy Replication vs Clean-Core Event Driven",
                subtitle="Structural evaluation of system coupling, financial ledger integrity, and latency",
                category_tag="ENTERPRISE ARCHITECTURE COMPARISON",
                client_name=client_name,
                archetype=archetype,
                headers=["EVALUATION DIMENSION", "LEGACY POINT-TO-POINT", "TARGET CLEAN-CORE BTP", "ARCHITECTURAL ADVANTAGE"],
                col_weights=[1.4, 2.0, 2.0, 1.8],
                callout_note="Zero custom Z-tables in S/4HANA core; all MES dispatch logic runs outside the financial ledger.",
                rows=[
                    TableRowItem(cells=["1. CORE FINANCIAL LEDGER & ERP INTEGRATION"], is_section_header=True),
                    TableRowItem(cells=["General Ledger Tie-Out", "Nightly batch replication to MES staging DB", "Real-time ACDOCA ledger via Event Mesh", "Eliminates reconciliation variance"]),
                    TableRowItem(cells=["Custom ERP Modifications", "34 custom Z-tables & user exits in ECC core", "Clean-core ABAP Cloud with standard OData v4", "Seamless SAP cloud upgrades"]),
                    TableRowItem(cells=["2. LATENCY & OPERATIONAL EXECUTION"], is_section_header=True),
                    TableRowItem(cells=["Shopfloor Order Latency", "Batch synch every 4 hours (Starves line)", "Sub-second event trigger on order release", "Eliminates operator idle wait time"]),
                    TableRowItem(cells=["Plant Offline Resilience", "MES stalls immediately if WAN drops", "48h edge queue buffer on local IPC", "Zero production downtime during WAN cuts"])
                ]
            )

        # 2. Requirements Specification
        elif archetype == TableArchetype.REQUIREMENTS:
            return EnterpriseTableSpec(
                title="Traceable Requirements & Capability Allocation Matrix",
                subtitle="De-risked capability allocation mapped to ISA-95 layers and MoSCoW prioritization",
                category_tag="REQUIREMENTS TRACEABILITY SPECIFICATION",
                client_name=client_name,
                archetype=archetype,
                headers=["REQ ID", "CAPABILITY REQUIREMENT", "ISA-95 TIER", "MOSCOW", "TARGET COMPONENT", "ACCEPTANCE CRITERIA"],
                col_weights=[0.9, 2.2, 1.1, 0.8, 1.4, 1.8],
                rows=[
                    TableRowItem(cells=["REQ-0101", "Sub-second production order dispatch from S/4HANA", "Level 4 / BTP", "MUST", "SAP Event Mesh", "Latency < 250ms p99"]),
                    TableRowItem(cells=["REQ-0102", "Automated component serial genealogy capture", "Level 3 MOM", "MUST", "SAP DMC Core", "100% trace without manual entry"]),
                    TableRowItem(cells=["REQ-0103", "Offline tool wear & spindle vibration monitoring", "Level 2 Edge", "MUST", "Industrial Edge IPC", "48-hour local disk buffer"]),
                    TableRowItem(cells=["REQ-0104", "Automated non-conformance quarantine lock", "Level 3 MOM", "SHOULD", "Quality Engine", "PLC safety interlock trigger < 50ms"]),
                    TableRowItem(cells=["REQ-0105", "Dynamic visual assembly instructions on touch POD", "Level 1 / 0", "SHOULD", "Operator Touch POD", "3D CAD model load < 1.2s"])
                ]
            )

        # 3. Interface Catalogue
        elif archetype == TableArchetype.INTERFACE_CATALOGUE:
            return EnterpriseTableSpec(
                title="Enterprise Integration Interface Catalogue",
                subtitle="Standardized protocol and payload specifications governing IT/OT boundary exchanges",
                category_tag="INTERFACE CATALOGUE & API SPECIFICATION",
                client_name=client_name,
                archetype=archetype,
                headers=["INTERFACE ID", "SOURCE SYSTEM", "TARGET SYSTEM", "PROTOCOL / PATTERN", "FREQUENCY", "DATA OBJECT / PAYLOAD"],
                col_weights=[1.1, 1.4, 1.4, 1.5, 1.0, 1.8],
                callout_note="All interfaces enforce mTLS with JWT token exchange; payload validation handled by API Gateway.",
                rows=[
                    TableRowItem(cells=["INT-001", "SAP S/4HANA", "BTP Event Mesh", "AMQP / Event Mesh", "Real-Time Push", "[ProductionOrderCreated_v2]"]),
                    TableRowItem(cells=["INT-002", "BTP Event Mesh", "SAP DMC (MES)", "WebSocket / REST", "Sub-Second", "[DispatchWorkCenterPayload]"]),
                    TableRowItem(cells=["INT-003", "SAP DMC (MES)", "Kepware Edge", "OPC UA (Binary)", "On Event", "[ToolParameters, Setpoints]"]),
                    TableRowItem(cells=["INT-004", "Siemens S7-1500", "Edge IPC Gateway", "PROFINET / I/O", "100ms Stream", "[SpindleSpeed, Temperature]"]),
                    TableRowItem(cells=["INT-005", "SAP DMC (MES)", "SAP S/4HANA", "OData v4 BAPI", "On Completion", "[GoodsMovement 101, ScrapPost]"])
                ]
            )

        # 4. KPI Definitions
        elif archetype == TableArchetype.KPI_DEFINITIONS:
            return EnterpriseTableSpec(
                title="Operational & Financial KPI Governance Master",
                subtitle="Rigorous mathematical formulas, source of truth ledgers, and reporting cadences",
                category_tag="DECISION INTELLIGENCE KPI GOVERNANCE",
                client_name=client_name,
                archetype=archetype,
                headers=["KPI METRIC", "MATHEMATICAL DEFINITION", "BASELINE", "TARGET SLA", "SOURCE LEDGER", "CADENCE"],
                col_weights=[1.4, 2.2, 0.9, 0.9, 1.4, 0.9],
                rows=[
                    TableRowItem(cells=["Overall Equipment Eff (OEE)", "(Availability) × (Performance) × (Quality)", "68.4%", "85.0%", "MES Machine Logs", "Shift / Real-Time"]),
                    TableRowItem(cells=["First Pass Yield (FPY)", "(Good Units Completed) ÷ (Total Units Started)", "91.2%", "96.5%", "MES Inspection Table", "Hourly"]),
                    TableRowItem(cells=["On-Time In-Full (OTIF)", "(Orders Shipped On-Time) ÷ (Total Promised)", "84.2%", "95.0%", "S/4HANA Sales Order", "Daily"]),
                    TableRowItem(cells=["Days of Inventory Supply (DSI)", "(Average WIP Value) ÷ (Daily COGS)", "42 Days", "28 Days", "S/4HANA ACDOCA", "Weekly"]),
                    TableRowItem(cells=["Cost of Poor Quality (COPQ)", "(Scrap Expense + Rework Hours + Warranty)", "$3.42M/Yr", "< $1.80M/Yr", "Financial Material Ledger", "Monthly"])
                ]
            )

        # 5. Risks & Mitigation
        elif archetype == TableArchetype.RISKS:
            return EnterpriseTableSpec(
                title="Enterprise Transformation Risk & Mitigation Matrix",
                subtitle="Proactive assessment of architectural constraints, organizational friction, and mitigations",
                category_tag="RISK MANAGEMENT REGISTER",
                client_name=client_name,
                archetype=archetype,
                headers=["RISK ID", "RISK EVENT / CONSTRAINT", "PROBABILITY", "IMPACT", "SCORE", "MITIGATION STRATEGY", "OWNER"],
                col_weights=[0.8, 2.2, 1.0, 1.0, 0.8, 2.0, 1.0],
                rows=[
                    TableRowItem(cells=["RSK-01", "Legacy CNC machines lack OPC UA network interfaces", "HIGH", "CRITICAL", "HIGH", "Install isolated edge serial-to-ethernet bridge hardware", "OT Architect"]),
                    TableRowItem(cells=["RSK-02", "Custom Z-table dependency in ECC hinders clean-core", "MEDIUM", "HIGH", "MEDIUM", "Wrap custom logic in BTP extension app before cutover", "SAP Lead"]),
                    TableRowItem(cells=["RSK-03", "Factory floor operators resist touch POD interface", "MEDIUM", "MEDIUM", "MEDIUM", "Involve shop floor leads in sprint reviews & gamified UX", "Change Lead"]),
                    TableRowItem(cells=["RSK-04", "WAN network latency spikes exceed 350ms during shifts", "LOW", "HIGH", "LOW", "Deploy local edge runtime buffer ensuring 48h autonomy", "Infra Lead"])
                ]
            )

        # 6. Assumptions
        elif archetype == TableArchetype.ASSUMPTIONS:
            return EnterpriseTableSpec(
                title="Architectural Baseline Assumptions & Validation Milestones",
                subtitle="Foundational operational assumptions underpinning solution feasibility and delivery",
                category_tag="TRANSFORMATION ASSUMPTIONS REGISTER",
                client_name=client_name,
                archetype=archetype,
                headers=["ASSUMPTION ID", "CATEGORY", "STATED ASSUMPTION", "IMPACT IF INVALID", "VALIDATION GATE", "OWNER"],
                col_weights=[1.1, 1.2, 2.4, 1.8, 1.2, 1.0],
                rows=[
                    TableRowItem(cells=["ASM-001", "Infrastructure", "Plant shopfloor Gigabit LAN deployed with redundant switches", "Requires edge hardware buffer upgrade", "Gate 1 (Day 15)", "Plant IT"]),
                    TableRowItem(cells=["ASM-002", "SAP Licensing", "SAP BTP tenant and Cloud Integration licenses provisioned", "Delays middleware staging sprints", "Gate 0 (Day 1)", "Client CPO"]),
                    TableRowItem(cells=["ASM-003", "Data Quality", "Material Master (MARA) and Routing (PLKO) data cleansed", "Requires 3-week data staging scrub", "Gate 2 (Day 30)", "Master Data Lead"]),
                    TableRowItem(cells=["ASM-004", "Shop Floor Access", "Access granted to machine cell PLCs during scheduled weekend shifts", "Extends integration timeline by 2 weeks", "Gate 3 (Day 45)", "Plant Manager"])
                ]
            )

        # 7. Commercial Proposal
        elif archetype == TableArchetype.COMMERCIAL_PROPOSAL:
            return EnterpriseTableSpec(
                title="Fixed-Price Turnkey Commercial Proposal & Milestone Payments",
                subtitle="Deliverable-linked milestone gates tied to architectural clarity and business acceptance",
                category_tag="COMMERCIAL INVESTMENT PROPOSAL",
                client_name=client_name,
                archetype=archetype,
                headers=["MILESTONE GATE", "DELIVERABLE & SCOPE DESCRIPTION", "TARGET TIMELINE", "INVESTMENT", "PAYMENT TRIGGER"],
                col_weights=[1.2, 2.5, 1.1, 1.1, 1.6],
                callout_note="Fixed-price commercial commitment inclusive of 90-day post-go-live architectural hypercare.",
                rows=[
                    TableRowItem(cells=["Gate 1: Foundation", "Target Architecture Blueprint & Clean-Core BTP Scaffolding", "Month 1 (Day 30)", "$180,000", "Architecture Review Sign-Off"]),
                    TableRowItem(cells=["Gate 2: Integration", "Event Mesh, S/4HANA OData Connectors & Kepware Edge Setup", "Month 2 (Day 60)", "$240,000", "End-to-End Test Pass"]),
                    TableRowItem(cells=["Gate 3: MES Pilot", "Pilot Line Deployment (CNC Bay 1), Operator POD & Genealogy", "Month 3 (Day 90)", "$280,000", "Pilot Production Go-Live"]),
                    TableRowItem(cells=["Gate 4: Scale Out", "Full Plant Rollout (All 14 Work Centers) & Hypercare Support", "Month 4 (Day 120)", "$150,000", "Final Acceptance Gate"]),
                    TableRowItem(cells=["TOTAL COMMITMENT", "Turnkey Consulting, Architecture & Implementation Delivery", "4 Months", "$850,000", "Milestone-Linked Invoicing"])
                ]
            )

        # 8. Implementation Scope
        elif archetype == TableArchetype.IMPLEMENTATION_SCOPE:
            return EnterpriseTableSpec(
                title="Workstream Implementation Scope & Boundary Exclusions",
                subtitle="Exhaustive capability definition establishing in-scope commitments and explicit boundaries",
                category_tag="WORKSTREAM SCOPE SPECIFICATION",
                client_name=client_name,
                archetype=archetype,
                headers=["WORKSTREAM", "IN-SCOPE CORE CAPABILITIES", "EXCLUSIONS & BOUNDARIES", "PREREQUISITE DELIVERABLES"],
                col_weights=[1.4, 2.4, 1.8, 1.4],
                rows=[
                    TableRowItem(cells=["1. CORE SAP S/4HANA"], is_section_header=True),
                    TableRowItem(cells=["Clean-Core ERP", "Standard OData v4 APIs, Event Mesh triggers, Confirmation BAPIs", "No custom ABAP core mods; no custom Z-tables", "S/4HANA 2023 Sandbox Access"]),
                    TableRowItem(cells=["2. MANUFACTURING MES (DMC)"], is_section_header=True),
                    TableRowItem(cells=["Shop Floor Execution", "Work order dispatch, Operator POD, Serial genealogy, Scrap posting", "Excluded: Automated warehouse AS/RS robotics", "Master BOM / Routing Sign-Off"]),
                    TableRowItem(cells=["3. INDUSTRIAL EDGE & OT"], is_section_header=True),
                    TableRowItem(cells=["Machine Connectivity", "Kepware OPC UA, 14 machine telemetry connectors, 48h buffer", "Excluded: Physical machine re-wiring / PLC code rewrite", "Plant Network VLAN Isolation"])
                ]
            )

        # 9. Responsibility Matrix (RACI)
        elif archetype == TableArchetype.RESPONSIBILITY_MATRIX:
            return EnterpriseTableSpec(
                title="Governance Responsibility Matrix (RACI)",
                subtitle="Clear delineation of accountability across Client Steering, Systems Integrator, and Operations",
                category_tag="PROGRAM GOVERNANCE & RACI MATRIX",
                client_name=client_name,
                archetype=archetype,
                headers=["DELIVERY DOMAIN / KEY DECISION", "CLIENT CXO", "LEAD ARCHITECT", "SYSTEMS INTEGRATOR", "PLANT OPERATIONS"],
                col_weights=[2.4, 1.0, 1.0, 1.0, 1.0],
                callout_note="R = Responsible (Doer), A = Accountable (Final Decision), C = Consulted (Input), I = Informed.",
                rows=[
                    TableRowItem(cells=["Target Architecture & Clean-Core Sign-Off", "A", "R", "C", "I"]),
                    TableRowItem(cells=["BTP Integration Suite Configuration & Tests", "I", "A", "R", "I"]),
                    TableRowItem(cells=["Shop Floor POD Usability & Operator Feedback", "I", "C", "R", "A"]),
                    TableRowItem(cells=["Machine PLC Tag Mapping & Safety Clearance", "I", "C", "R", "A"]),
                    TableRowItem(cells=["Cutover Authorization & Go-Live Go/No-Go", "A", "R", "C", "C"])
                ]
            )

        # 10. Roadmap Table
        elif archetype == TableArchetype.ROADMAP:
            return EnterpriseTableSpec(
                title="Phased Implementation Roadmap & Milestone Gating",
                subtitle="Sequential rollout cadence with verified exit criteria for each transformation stage",
                category_tag="IMPLEMENTATION ROADMAP SPECIFICATION",
                client_name=client_name,
                archetype=archetype,
                headers=["PHASE / TIMELINE", "STRATEGIC MILESTONE", "EXIT GATE CRITERIA", "CORE DELIVERABLES", "STATUS"],
                col_weights=[1.1, 1.8, 1.8, 1.8, 0.9],
                rows=[
                    TableRowItem(cells=["Sprint 1-2 (Wks 1-4)", "Architecture Foundation", "Architecture review board sign-off", "Solution blueprint, BTP tenant setup", "COMPLETED"]),
                    TableRowItem(cells=["Sprint 3-4 (Wks 5-8)", "Edge & ERP Integration", "Zero-loss synthetic transaction test", "Event Mesh queues, OPC UA drivers", "ACTIVE"]),
                    TableRowItem(cells=["Sprint 5-6 (Wks 9-12)", "MES Pilot Line Cutover", "99.5% FPY & automated genealogy match", "DMC operator POD, CNC Bay 1 live", "ACTIVE"]),
                    TableRowItem(cells=["Sprint 7-8 (Wks 13-16)", "Plant Scale-Out", "All 14 cells live with 0 rollbacks", "Full factory deployment & training", "PLANNED"])
                ]
            )

        # 11. Business Benefits
        elif archetype == TableArchetype.BUSINESS_BENEFITS:
            return EnterpriseTableSpec(
                title="Quantified Business Benefits & Financial Payback Model",
                subtitle="Audited financial impact mapping operational efficiency levers directly to EBITDA returns",
                category_tag="BUSINESS VALUE & ROI REALIZATION",
                client_name=client_name,
                archetype=archetype,
                headers=["VALUE AREA", "OPERATIONAL EFFICIENCY LEVER", "BASELINE", "TARGET", "ANNUAL EBITDA IMPACT", "PAYBACK"],
                col_weights=[1.4, 2.2, 0.9, 0.9, 1.4, 0.9],
                rows=[
                    TableRowItem(cells=["Scrap Reduction", "Automated vision inspection stops defective runs", "2.84% Scrap", "1.10% Scrap", "$1,240,000 / Yr", "4.2 Mos"]),
                    TableRowItem(cells=["OEE Throughput", "Eliminates paper work orders & setup wait time", "71.4% OEE", "84.5% OEE", "$920,000 / Yr", "5.8 Mos"]),
                    TableRowItem(cells=["WIP Inventory", "Real-time dispatch eliminates bottleneck queues", "42 Days DSI", "28 Days DSI", "$640,000 / Yr", "6.5 Mos"]),
                    TableRowItem(cells=["Quality Labor", "Automated digital genealogy replaces manual audits", "4,200 Hrs/Yr", "650 Hrs/Yr", "$310,000 / Yr", "8.0 Mos"]),
                    TableRowItem(cells=["TOTAL BENEFIT", "Composite Financial Value Acceleration", "-", "-", "$3,110,000 / Yr", "3.3 Months"])
                ]
            )

        # 12. Data Mappings
        elif archetype == TableArchetype.DATA_MAPPINGS:
            return EnterpriseTableSpec(
                title="Technical Data Mapping: S/4HANA to Manufacturing Operations (DMC)",
                subtitle="Field-level entity lineage, data types, and transformation logic",
                category_tag="DATA LINEAGE & TRANSFORMATION MAPPING",
                client_name=client_name,
                archetype=archetype,
                headers=["SOURCE S/4HANA FIELD", "SRC TYPE", "TARGET MES FIELD", "TGT TYPE", "TRANSFORMATION & VALIDATION RULE"],
                col_weights=[1.6, 0.9, 1.6, 0.9, 2.5],
                rows=[
                    TableRowItem(cells=["AFKO.AUFNR", "CHAR(12)", "Order.OrderNumber", "STRING", "Direct 1:1 mapping; strip leading zeros"]),
                    TableRowItem(cells=["AFPO.MATNR", "CHAR(40)", "Material.MaterialId", "STRING", "Prefix with client prefix; validate active BOM in MARA"]),
                    TableRowItem(cells=["AFKO.GAMNG", "DEC(13,3)", "Order.TargetQuantity", "FLOAT", "Convert to metric unit of measure base units"]),
                    TableRowItem(cells=["AFKO.GSTRP", "DATS(8)", "Order.ScheduledStart", "DATETIME", "Convert UTC timestamp from ISO 8601 string"]),
                    TableRowItem(cells=["AFVC.ARBPL", "CHAR(8)", "Operation.WorkCenter", "STRING", "Resolve plant work center mapping table via DMC API"])
                ]
            )

        # Fallback Custom
        else:
            return EnterpriseTableSpec(
                title="Enterprise Specification Table",
                subtitle="Structured technical matrix and governance register",
                client_name=client_name,
                archetype=archetype,
                headers=["ITEM ID", "WORKSTREAM", "CAPABILITY DESCRIPTION", "STATUS", "OWNER"],
                col_weights=[1.0, 1.8, 2.5, 1.0, 1.2],
                rows=[
                    TableRowItem(cells=["SPEC-01", "Core Operations", "Real-time ledger reconciliation", "ACTIVE", "Lead Architect"]),
                    TableRowItem(cells=["SPEC-02", "Quality Control", "Automated non-conformance quarantine", "COMPLETED", "Quality Lead"]),
                    TableRowItem(cells=["SPEC-03", "Edge Telemetry", "Industrial OPC UA buffer", "IN PROGRESS", "Edge Specialist"])
                ]
            )
