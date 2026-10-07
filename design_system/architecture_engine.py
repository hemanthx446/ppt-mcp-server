"""
Enterprise Architecture Diagram Engine.

Creates genuine, native, editable PowerPoint architecture diagrams for:
- Multi-tier enterprise stacks (Enterprise -> Integration -> MES -> Edge -> Shop Floor)
- System boundaries and trust zones (Cloud, DMZ, Plant LAN, Air-Gapped OT)
- Distinct shape grammar: Systems, Data Stores (cylinders), Interfaces/APIs, Devices, Actors, Event Buses
- Directional, bidirectional, and asynchronous event flows with interface protocol and data object movement labels
- Visual hierarchy and whitespace between layers
- Architectural principles and zero-loss guarantees callout panels

Strictly avoids decorative bubble cards. Communicates "how the system works underneath".
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Any, Optional, Tuple

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
# 1. Architectural Element Taxonomy
# =============================================================================

class ArchElementType(Enum):
    SYSTEM = auto()           # Core enterprise/manufacturing software system
    SUBSYSTEM = auto()        # Modular service / calculation engine
    DATA_STORE = auto()       # Persistence / Database (rendered as cylinder MSO_SHAPE.CAN)
    INTERFACE_API = auto()    # API Endpoint, Gateway, or OData/REST service
    EVENT_BROKER = auto()     # Message Broker, Kafka topic, or Event Mesh
    DEVICE = auto()           # Physical machine, CNC, PLC, sensor, handheld scanner
    ACTOR = auto()            # Human user, operator, supervisor persona
    EXTERNAL_SYSTEM = auto()  # Third-party / partner / supplier system


class FlowDirection(Enum):
    DOWN = auto()             # Unidirectional downward flow
    UP = auto()               # Unidirectional upward flow
    BIDIRECTIONAL = auto()    # Two-way sync / handshake
    ASYNC_EVENT = auto()      # Asynchronous pub/sub event broadcast
    TELEMETRY = auto()        # Streaming telemetry


@dataclass
class ArchElement:
    """An individual architectural component inside a layer or system boundary."""
    name: str
    element_type: ArchElementType = ArchElementType.SYSTEM
    role: Optional[str] = None
    tech_stack: Optional[str] = None
    key_objects: List[str] = field(default_factory=list)


@dataclass
class ArchFlow:
    """Inter-tier or inter-system communication link."""
    protocol: str                              # e.g., "OData v4", "OPC UA (binary)", "Kafka Pub/Sub"
    data_object: str                          # e.g., "[ProductionOrder_v2]", "[GoodsMovement 101]"
    direction: FlowDirection = FlowDirection.DOWN
    flow_badge: Optional[str] = None           # e.g., "mTLS / Air-Gapped", "Near-Real-Time (50ms)"


@dataclass
class ArchLayer:
    """A distinct architectural tier, Purdue Level, or trust boundary."""
    name: str                                  # e.g., "ENTERPRISE / CORE ERP"
    level_tag: str                             # e.g., "ISA-95 LEVEL 4", "BTP INTEGRATION", "LEVEL 3 MOM"
    trust_zone: str                            # e.g., "Corporate Cloud", "Plant DMZ", "Air-Gapped OT"
    elements: List[ArchElement] = field(default_factory=list)
    flow_to_next: Optional[ArchFlow] = None    # Interface connector leading to layer below


@dataclass
class ArchAnnotation:
    """Structural design principle or technical guarantee explaining the mechanics."""
    category: str                              # e.g., "DATA OWNERSHIP", "RESILIENCE", "SECURITY PERIMETER"
    principle: str                             # e.g., "S/4HANA is the sole financial ledger; MES never replicates ACDOCA."


@dataclass
class ArchitectureDiagramSpec:
    """Complete specification for a native enterprise architecture slide."""
    title: str
    subtitle: str
    category_tag: str = "ENTERPRISE ARCHITECTURE BLUEPRINT"
    client_name: str = "Enterprise Architecture"
    is_dark: bool = True                       # Dark Navy provides maximum contrast for blueprints
    layers: List[ArchLayer] = field(default_factory=list)
    annotations: List[ArchAnnotation] = field(default_factory=list)


# =============================================================================
# 2. Native Shape Renderer for Architectural Elements
# =============================================================================

class ArchitectureElementRenderer:
    """Renders specific architectural shapes avoiding generic cards."""

    @staticmethod
    def render_element(slide, left: float, top: float, width: float, height: float,
                       elem: ArchElement, theme: Theme):
        etype = elem.element_type

        # ---------------------------------------------------------------------
        # 1. DATA STORE (Cylinder / Can)
        # ---------------------------------------------------------------------
        if etype == ArchElementType.DATA_STORE:
            can = slide.shapes.add_shape(MSO_SHAPE.CAN, Inches(left), Inches(top), Inches(width), Inches(height))
            can.fill.solid()
            can.fill.fore_color.rgb = theme.surface_alt
            can.line.color.rgb = theme.border_accent
            can.line.width = Pt(1.5)

            tb = slide.shapes.add_textbox(Inches(left + 0.10), Inches(top + 0.16), Inches(width - 0.20), Inches(height - 0.22))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

            p_type = tf.paragraphs[0]
            p_type.alignment = PP_ALIGN.CENTER
            TypographySystem.apply_to_paragraph(p_type, TypographySystem.ANNOTATION, "DATA STORE", theme.border_accent)

            p_name = tf.add_paragraph()
            p_name.alignment = PP_ALIGN.CENTER
            TypographySystem.apply_to_paragraph(p_name, TypographySystem.BODY_STRONG, elem.name, theme.text_primary)

            if elem.tech_stack:
                p_tech = tf.add_paragraph()
                p_tech.alignment = PP_ALIGN.CENTER
                TypographySystem.apply_to_paragraph(p_tech, TypographySystem.CAPTION, elem.tech_stack, theme.text_muted)

        # ---------------------------------------------------------------------
        # 2. DEVICE / EQUIPMENT (Beveled / Machine block)
        # ---------------------------------------------------------------------
        elif etype == ArchElementType.DEVICE:
            dev = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
            dev.fill.solid()
            dev.fill.fore_color.rgb = theme.surface_highlight
            dev.line.color.rgb = theme.border
            dev.line.width = Pt(1.2)

            tb = slide.shapes.add_textbox(Inches(left + 0.10), Inches(top + 0.08), Inches(width - 0.20), Inches(height - 0.16))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

            p_tag = tf.paragraphs[0]
            TypographySystem.apply_to_paragraph(p_tag, TypographySystem.ANNOTATION, "DEVICE / OT", theme.text_accent)

            p_name = tf.add_paragraph()
            TypographySystem.apply_to_paragraph(p_name, TypographySystem.BODY_STRONG, elem.name, theme.text_primary)

            if elem.role:
                p_role = tf.add_paragraph()
                TypographySystem.apply_to_paragraph(p_role, TypographySystem.CAPTION, elem.role, theme.text_secondary)

        # ---------------------------------------------------------------------
        # 3. INTERFACE / API GATEWAY (Hexagon / Gateway Node)
        # ---------------------------------------------------------------------
        elif etype == ArchElementType.INTERFACE_API:
            gate = slide.shapes.add_shape(MSO_SHAPE.HEXAGON, Inches(left), Inches(top), Inches(width), Inches(height))
            gate.fill.solid()
            gate.fill.fore_color.rgb = theme.surface
            gate.line.color.rgb = theme.accent_primary
            gate.line.width = Pt(1.4)

            tb = slide.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.08), Inches(width - 0.30), Inches(height - 0.16))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

            p_api = tf.paragraphs[0]
            p_api.alignment = PP_ALIGN.CENTER
            TypographySystem.apply_to_paragraph(p_api, TypographySystem.ANNOTATION, "API / ENDPOINT", theme.accent_primary)

            p_name = tf.add_paragraph()
            p_name.alignment = PP_ALIGN.CENTER
            TypographySystem.apply_to_paragraph(p_name, TypographySystem.BODY_STRONG, elem.name, theme.text_primary)

        # ---------------------------------------------------------------------
        # 4. ACTOR / PERSONA (Oval / Avatar badge)
        # ---------------------------------------------------------------------
        elif etype == ArchElementType.ACTOR:
            actor = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(left), Inches(top), Inches(width), Inches(height))
            actor.fill.solid()
            actor.fill.fore_color.rgb = theme.surface_alt
            actor.line.color.rgb = theme.border_accent
            actor.line.width = Pt(1.2)

            tb = slide.shapes.add_textbox(Inches(left + 0.08), Inches(top + 0.10), Inches(width - 0.16), Inches(height - 0.20))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

            p_act = tf.paragraphs[0]
            p_act.alignment = PP_ALIGN.CENTER
            TypographySystem.apply_to_paragraph(p_act, TypographySystem.ANNOTATION, "OPERATOR", theme.text_accent)

            p_name = tf.add_paragraph()
            p_name.alignment = PP_ALIGN.CENTER
            TypographySystem.apply_to_paragraph(p_name, TypographySystem.BODY_STRONG, elem.name, theme.text_primary)

        # ---------------------------------------------------------------------
        # 5. CORE SYSTEM / SUBSYSTEM (Architectural Solid Box)
        # ---------------------------------------------------------------------
        else:
            box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
            box.fill.solid()
            box.fill.fore_color.rgb = theme.surface
            box.line.color.rgb = theme.border
            box.line.width = Pt(1.0)

            # Left architectural accent strip
            strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(0.06), Inches(height))
            strip.fill.solid()
            strip.fill.fore_color.rgb = theme.border_accent
            strip.line.fill.background()

            tb = slide.shapes.add_textbox(Inches(left + 0.14), Inches(top + 0.08), Inches(width - 0.24), Inches(height - 0.16))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

            # Element Name
            p_name = tf.paragraphs[0]
            TypographySystem.apply_to_paragraph(p_name, TypographySystem.BODY_STRONG, elem.name, theme.text_primary)

            # Tech / Role
            detail = elem.role or elem.tech_stack or ""
            if detail:
                p_det = tf.add_paragraph()
                TypographySystem.apply_to_paragraph(p_det, TypographySystem.CAPTION, detail, theme.text_muted)

            # Key Data Objects
            if elem.key_objects:
                p_obj = tf.add_paragraph()
                p_obj.space_before = Pt(2.0)
                obj_text = " • ".join(elem.key_objects[:2])
                TypographySystem.apply_to_paragraph(p_obj, TypographySystem.ANNOTATION, obj_text, theme.text_accent)


# =============================================================================
# 3. Enterprise Architecture Layout & Composition Engine
# =============================================================================

class EnterpriseArchitectureComposer:
    """
    Renders high-fidelity, native PowerPoint architecture diagrams
    communicating 'how the system works underneath'.
    """

    @classmethod
    def compose_and_render(cls, prs: Presentation, spec: ArchitectureDiagramSpec):
        """Constructs a complete architecture blueprint slide."""
        theme = ExecutiveNavyTheme if spec.is_dark else ConsultingSlateTheme
        blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
        slide = prs.slides.add_slide(blank_layout)

        # 1. Canvas Background
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
            metadata_text=f"{spec.client_name} • Enterprise Architecture Blueprint • Systems-Thinking Guardrails",
            theme=theme
        )

        # Usable Canvas Geometry
        left = Margins.left
        total_w = Margins().usable_width
        canvas_top = 1.30
        canvas_height = 5.65

        # Split: Main Diagram (Left ~75%) vs Guarantees/Annotations (Right ~25%)
        has_annotations = bool(spec.annotations)
        if has_annotations:
            (diag_x, diag_w), (ann_x, ann_w) = GridCalculator.get_split(
                left_ratio=0.74, left=left, total_width=total_w, gap=0.30
            )
        else:
            diag_x, diag_w = left, total_w
            ann_x, ann_w = 0, 0

        # Render Main Architecture Layers Stack
        cls._render_layers_stack(slide, diag_x, canvas_top, diag_w, canvas_height, spec.layers, theme)

        # Render Right Architectural Principles / Guarantees Panel
        if has_annotations:
            cls._render_annotations_panel(slide, ann_x, canvas_top, ann_w, canvas_height, spec.annotations, theme)

        return slide

    @classmethod
    def _render_layers_stack(cls, slide, left: float, top: float, width: float, height: float,
                             layers: List[ArchLayer], theme: Theme):
        """Renders vertical hierarchy of layers with interface flows between them."""
        num_layers = len(layers)
        if num_layers == 0:
            return

        # Reserve vertical height for inter-layer connector channels
        connector_gap = 0.36 if num_layers >= 5 else 0.44
        total_connector_space = (num_layers - 1) * connector_gap
        available_layer_height = height - total_connector_space
        layer_h = max(0.65, available_layer_height / num_layers)

        cur_y = top
        for idx, layer in enumerate(layers):
            # Render Layer Row
            cls._render_layer_row(slide, left, cur_y, width, layer_h, layer, theme)

            # Render Connector to Next Layer
            if idx < num_layers - 1:
                conn_y = cur_y + layer_h
                flow = layer.flow_to_next
                cls._render_inter_layer_flow(slide, left, conn_y, width, connector_gap, flow, theme)
                cur_y += layer_h + connector_gap
            else:
                cur_y += layer_h

    @classmethod
    def _render_layer_row(cls, slide, left: float, top: float, width: float, height: float,
                          layer: ArchLayer, theme: Theme):
        """Renders an individual architecture tier container with left tag and internal elements."""
        # 1. Left Layer Boundary & Level Tag
        tag_w = 2.10
        tag_box = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(tag_w), Inches(height)
        )
        tag_box.fill.solid()
        tag_box.fill.fore_color.rgb = theme.surface_highlight
        tag_box.line.color.rgb = theme.border_accent
        tag_box.line.width = Pt(1.2)

        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = Inches(0.12)
        tf_tag.margin_top = Inches(0.08)

        p_lvl = tf_tag.paragraphs[0]
        TypographySystem.apply_to_paragraph(p_lvl, TypographySystem.ANNOTATION, layer.level_tag, theme.border_accent)

        p_name = tf_tag.add_paragraph()
        TypographySystem.apply_to_paragraph(p_name, TypographySystem.LABEL, layer.name, theme.text_primary)

        p_zone = tf_tag.add_paragraph()
        TypographySystem.apply_to_paragraph(p_zone, TypographySystem.CAPTION, f"ZONE: {layer.trust_zone}", theme.text_muted)

        # 2. Main Layer Enclosure (Whitespace container)
        cont_x = left + tag_w + 0.14
        cont_w = width - tag_w - 0.14
        cont_box = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(cont_x), Inches(top), Inches(cont_w), Inches(height)
        )
        cont_box.fill.solid()
        cont_box.fill.fore_color.rgb = theme.surface_muted
        cont_box.line.color.rgb = theme.border
        cont_box.line.width = Pt(1.0)

        # 3. Internal Architectural Elements
        num_elems = len(layer.elements)
        if num_elems > 0:
            elem_gap = 0.18
            elem_cols = GridCalculator.get_columns(
                num_elems, left=cont_x + 0.12, total_width=cont_w - 0.24, gap=elem_gap
            )
            elem_y = top + 0.08
            elem_h = height - 0.16

            for e_idx, elem in enumerate(layer.elements):
                ex, ew = elem_cols[e_idx]
                ArchitectureElementRenderer.render_element(
                    slide, ex, elem_y, ew, elem_h, elem, theme
                )

    @classmethod
    def _render_inter_layer_flow(cls, slide, left: float, top: float, width: float, height: float,
                                flow: Optional[ArchFlow], theme: Theme):
        """Renders explicit directional/bidirectional flow with protocol and data object movement labels."""
        if not flow:
            return

        arrow_x = left + 3.80
        arrow_w = 0.32
        arrow_h = height - 0.06
        arrow_y = top + 0.03

        # Choose arrow shape
        if flow.direction == FlowDirection.BIDIRECTIONAL:
            arr = slide.shapes.add_shape(MSO_SHAPE.UP_DOWN_ARROW, Inches(arrow_x), Inches(arrow_y), Inches(arrow_w), Inches(arrow_h))
        else:
            arr = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(arrow_x), Inches(arrow_y), Inches(arrow_w), Inches(arrow_h))

        arr.fill.solid()
        arr.fill.fore_color.rgb = theme.accent_primary if not flow.flow_badge else theme.status_warning
        arr.line.fill.background()

        # Interface Protocol (Left of Arrow)
        proto_box = slide.shapes.add_textbox(Inches(left + 1.20), Inches(top + 0.04), Inches(2.45), Inches(height - 0.08))
        tf_p = proto_box.text_frame
        tf_p.word_wrap = True
        tf_p.margin_left = tf_p.margin_top = tf_p.margin_right = tf_p.margin_bottom = 0
        p_p = tf_p.paragraphs[0]
        p_p.alignment = PP_ALIGN.RIGHT
        TypographySystem.apply_to_paragraph(p_p, TypographySystem.ANNOTATION, f"INTERFACE: {flow.protocol}", theme.text_accent)

        # Data Object Movement Token (Right of Arrow)
        obj_box = slide.shapes.add_textbox(Inches(arrow_x + arrow_w + 0.15), Inches(top + 0.04), Inches(width - (arrow_x + arrow_w + 0.20)), Inches(height - 0.08))
        tf_o = obj_box.text_frame
        tf_o.word_wrap = True
        tf_o.margin_left = tf_o.margin_top = tf_o.margin_right = tf_o.margin_bottom = 0
        p_o = tf_o.paragraphs[0]
        badge_prefix = f"[{flow.flow_badge}] " if flow.flow_badge else ""
        TypographySystem.apply_to_paragraph(p_o, TypographySystem.ANNOTATION, f"{badge_prefix}PAYLOAD: {flow.data_object}", theme.text_primary)

    @classmethod
    def _render_annotations_panel(cls, slide, left: float, top: float, width: float, height: float,
                                  annotations: List[ArchAnnotation], theme: Theme):
        """Renders architectural principles, trust boundaries, and zero-loss guarantees."""
        # Container
        SurfacePrimitive.render(slide, left, top, width, height, theme, border_color=theme.border_accent)

        # Header Strip
        strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(0.38))
        strip.fill.solid()
        strip.fill.fore_color.rgb = theme.surface_highlight
        strip.line.color.rgb = theme.border
        tf_h = strip.text_frame
        tf_h.margin_left = Inches(0.12)
        p_h = tf_h.paragraphs[0]
        TypographySystem.apply_to_paragraph(p_h, TypographySystem.LABEL, "ARCHITECTURAL GUARANTEES", theme.border_accent)

        # Annotation Items
        content_y = top + 0.48
        item_h = (height - 0.60) / max(1, len(annotations))

        for idx, ann in enumerate(annotations[:5]):
            tb = slide.shapes.add_textbox(Inches(left + 0.14), Inches(content_y), Inches(width - 0.28), Inches(item_h - 0.10))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

            p_cat = tf.paragraphs[0]
            TypographySystem.apply_to_paragraph(p_cat, TypographySystem.ANNOTATION, f"• {ann.category.upper()}", theme.accent_primary)

            p_prin = tf.add_paragraph()
            p_prin.space_before = Pt(2.0)
            TypographySystem.apply_to_paragraph(p_prin, TypographySystem.BODY, ann.principle, theme.text_secondary)

            content_y += item_h


# =============================================================================
# 4. Canonical Pre-Built Enterprise Architecture Templates
# =============================================================================

class ArchitectureBlueprintFactory:
    """Pre-built reference enterprise architectures adhering to systems-thinking."""

    @classmethod
    def clean_core_sap_to_shopfloor(cls, client_name: str = "Enterprise Manufacturing") -> ArchitectureDiagramSpec:
        """
        The Canonical ISA-95 Clean-Core Architecture:
        Enterprise (S/4HANA) -> Integration (BTP) -> MES/MOM -> Industrial Edge -> Shop Floor Devices
        """
        return ArchitectureDiagramSpec(
            title="Clean-Core SAP S/4HANA to Shopfloor Architecture",
            subtitle="Decoupled ISA-95 execution pipeline with air-gapped plant resilience and zero ledger duplication",
            category_tag="ENTERPRISE SOLUTION BLUEPRINT",
            client_name=client_name,
            is_dark=True,
            layers=[
                ArchLayer(
                    name="ENTERPRISE / ERP",
                    level_tag="ISA-95 LEVEL 4",
                    trust_zone="Corporate Cloud (AWS/GCP)",
                    elements=[
                        ArchElement(name="SAP S/4HANA Core", element_type=ArchElementType.SYSTEM, role="Financial & Order Ledger", tech_stack="S/4 2023 FPS02", key_objects=["Production Orders", "BOM / Routing"]),
                        ArchElement(name="SAP HANA Cloud DB", element_type=ArchElementType.DATA_STORE, role="ACDOCA / In-Memory", tech_stack="HANA Columnar"),
                        ArchElement(name="Enterprise PLM", element_type=ArchElementType.SYSTEM, role="Engineering Master Data", tech_stack="Teamcenter / Windchill")
                    ],
                    flow_to_next=ArchFlow(
                        protocol="OData v4 & SAP Event Mesh",
                        data_object="ProductionOrder_v2, MaterialMaster (MARA)",
                        direction=FlowDirection.DOWN,
                        flow_badge="TLS 1.3 Async"
                    )
                ),
                ArchLayer(
                    name="INTEGRATION MIDDLEWARE",
                    level_tag="BTP INTEGRATION",
                    trust_zone="Cloud DMZ / Proxy",
                    elements=[
                        ArchElement(name="SAP BTP Integration Suite", element_type=ArchElementType.SYSTEM, role="API Mediation & Policy", tech_stack="Cloud Integration"),
                        ArchElement(name="Enterprise Event Mesh", element_type=ArchElementType.EVENT_BROKER, role="Pub/Sub Event Broker", tech_stack="Kafka / Solace", key_objects=["GoodsIssue Event", "OrderStatus"]),
                        ArchElement(name="API Gateway & Security", element_type=ArchElementType.INTERFACE_API, role="Token Validation & mTLS", tech_stack="Reverse Proxy")
                    ],
                    flow_to_next=ArchFlow(
                        protocol="HTTPS / REST & WebSocket",
                        data_object="DispatchOrderPayload, OperationStepList",
                        direction=FlowDirection.BIDIRECTIONAL,
                        flow_badge="Bi-Directional Sync"
                    )
                ),
                ArchLayer(
                    name="MANUFACTURING MOM / MES",
                    level_tag="ISA-95 LEVEL 3",
                    trust_zone="Plant Local LAN",
                    elements=[
                        ArchElement(name="SAP Digital Manufacturing (DMC)", element_type=ArchElementType.SYSTEM, role="Work Order Dispatcher & POD", tech_stack="MES Execution Core", key_objects=["WIP Tracking", "Non-Conformance"]),
                        ArchElement(name="Plant Operational DB", element_type=ArchElementType.DATA_STORE, role="WIP Genealogy & History", tech_stack="PostgreSQL Timescale"),
                        ArchElement(name="Quality & Yield Engine", element_type=ArchElementType.SUBSYSTEM, role="SPC & Tolerance Limits", tech_stack="Statistical Process Control")
                    ],
                    flow_to_next=ArchFlow(
                        protocol="OPC UA (Binary) & MQTT",
                        data_object="WorkCenterDispatch, ToolParameters, BatchID",
                        direction=FlowDirection.DOWN,
                        flow_badge="Air-Gapped Gateway"
                    )
                ),
                ArchLayer(
                    name="INDUSTRIAL EDGE & CONNECTIVITY",
                    level_tag="ISA-95 LEVEL 2",
                    trust_zone="Industrial Edge IPC",
                    elements=[
                        ArchElement(name="Edge Runtime Gateway", element_type=ArchElementType.SYSTEM, role="Local Buffer & Protocol Conv", tech_stack="Linux Industrial IPC", key_objects=["48h Offline Buffer"]),
                        ArchElement(name="Kepware / OPC UA Server", element_type=ArchElementType.INTERFACE_API, role="Industrial Tag Server", tech_stack="OPC UA / Modbus"),
                        ArchElement(name="Edge Cache DB", element_type=ArchElementType.DATA_STORE, role="Local SQLite Telemetry", tech_stack="SQLite / Edge Disk")
                    ],
                    flow_to_next=ArchFlow(
                        protocol="PROFINET & Fieldbus I/O",
                        data_object="MachineSpeed, SpindleTemp, CycleCount, InterlockSignal",
                        direction=FlowDirection.BIDIRECTIONAL,
                        flow_badge="Sub-100ms Deterministic"
                    )
                ),
                ArchLayer(
                    name="SHOP FLOOR EXECUTION",
                    level_tag="ISA-95 LEVEL 1 / 0",
                    trust_zone="Isolated OT Machine Subnet",
                    elements=[
                        ArchElement(name="Siemens S7-1500 PLC", element_type=ArchElementType.DEVICE, role="Cell Automation & Interlocks", tech_stack="Step 7 / PROFINET"),
                        ArchElement(name="DMG 5-Axis CNC Spindle", element_type=ArchElementType.DEVICE, role="Precision Machining Center", tech_stack="Sinumerik 840D"),
                        ArchElement(name="Cognex Vision Camera", element_type=ArchElementType.DEVICE, role="Automated Optical Inspection", tech_stack="In-Sight 7000"),
                        ArchElement(name="Line Assembly Operator", element_type=ArchElementType.ACTOR, role="Workstation Touch POD", tech_stack="Operator Touchscreen")
                    ]
                )
            ],
            annotations=[
                ArchAnnotation(
                    category="Single Financial Ledger",
                    principle="S/4HANA ACDOCA remains the sole financial source of truth. MES never replicates general ledger postings."
                ),
                ArchAnnotation(
                    category="Air-Gapped Plant Resilience",
                    principle="Edge gateways buffer 48 hours of telemetry and execution confirmations during WAN network disconnects."
                ),
                ArchAnnotation(
                    category="Clean-Core Decoupling",
                    principle="Zero custom ABAP modifications in S/4HANA core. All MES orchestrations leverage standard OData v4 and Event Mesh."
                ),
                ArchAnnotation(
                    category="Deterministic Machine Interlock",
                    principle="Sub-100ms machine safety and cycle interlocks run exclusively at Level 1/2 PLC layer, immune to cloud latency."
                )
            ]
        )

    @classmethod
    def zero_trust_ot_security_perimeter(cls, client_name: str = "Enterprise Defense & Aerospace") -> ArchitectureDiagramSpec:
        """Zero-Trust Purdue Model Security & Trust Zones Blueprint."""
        return ArchitectureDiagramSpec(
            title="Zero-Trust Industrial OT Security & Trust Zones",
            subtitle="Purdue model perimeter protection with air-gapped inspection and unidirectional data diodes",
            category_tag="SECURITY ARCHITECTURE BLUEPRINT",
            client_name=client_name,
            is_dark=True,
            layers=[
                ArchLayer(
                    name="ENTERPRISE WAN & CLOUD",
                    level_tag="PURDUE LEVEL 4/5",
                    trust_zone="Corporate Untrusted Perimeter",
                    elements=[
                        ArchElement(name="Corporate Identity & SSO", element_type=ArchElementType.SYSTEM, role="Azure AD / Okta SAML", tech_stack="OAuth 2.0 / OIDC"),
                        ArchElement(name="Enterprise ERP & SCM", element_type=ArchElementType.SYSTEM, role="Corporate Supply Chain", tech_stack="SAP S/4HANA"),
                        ArchElement(name="Central Security SIEM", element_type=ArchElementType.SYSTEM, role="Threat Telemetry & Log Lake", tech_stack="Splunk / Sentinel")
                    ],
                    flow_to_next=ArchFlow(
                        protocol="TLS 1.3 / mTLS Reverse Proxy",
                        data_object="Encrypted Work Order Batches & Token Claims",
                        direction=FlowDirection.DOWN,
                        flow_badge="Terminated at DMZ"
                    )
                ),
                ArchLayer(
                    name="DEMILITARIZED ZONE (DMZ)",
                    level_tag="PURDUE LEVEL 3.5",
                    trust_zone="Plant DMZ Inspection Zone",
                    elements=[
                        ArchElement(name="Next-Gen Firewall / WAF", element_type=ArchElementType.INTERFACE_API, role="Packet Inspection & IPS", tech_stack="Palo Alto Networks"),
                        ArchElement(name="Air-Gapped Data Diode", element_type=ArchElementType.INTERFACE_API, role="Unidirectional Hardware Diode", tech_stack="Hardware Enforced"),
                        ArchElement(name="Jump Host & Bastion", element_type=ArchElementType.SYSTEM, role="Privileged Access Management", tech_stack="CyberArk / SSH Bastion")
                    ],
                    flow_to_next=ArchFlow(
                        protocol="Isolated Encrypted Proxy",
                        data_object="Sanitized Telemetry & Inspection Logs",
                        direction=FlowDirection.DOWN,
                        flow_badge="Zero Inbound Internet"
                    )
                ),
                ArchLayer(
                    name="PLANT OPERATIONS NETWORK",
                    level_tag="PURDUE LEVEL 3",
                    trust_zone="Plant Intranet (Restricted)",
                    elements=[
                        ArchElement(name="Plant MES Execution Core", element_type=ArchElementType.SYSTEM, role="Cell Orchestration & Genealogy", tech_stack="Local Factory Cluster"),
                        ArchElement(name="Plant SCADA & Historian", element_type=ArchElementType.DATA_STORE, role="Time-Series Process Store", tech_stack="OSIsoft PI / Wonderware"),
                        ArchElement(name="Engineering Workstation", element_type=ArchElementType.SYSTEM, role="PLC Logic & Tool Path Depot", tech_stack="Siemens TIA Portal")
                    ],
                    flow_to_next=ArchFlow(
                        protocol="OPC UA Security Profile (Basic256Sha256)",
                        data_object="Recipe Parameters, Tool Interlocks",
                        direction=FlowDirection.BIDIRECTIONAL,
                        flow_badge="Air-Gapped VLAN"
                    )
                ),
                ArchLayer(
                    name="CELL / MACHINE CONTROLLERS",
                    level_tag="PURDUE LEVEL 1/2",
                    trust_zone="Isolated OT Machine Subnet",
                    elements=[
                        ArchElement(name="Safety PLC S7-1500F", element_type=ArchElementType.DEVICE, role="Fail-Safe Emergency Interlocks", tech_stack="Safety Integrated"),
                        ArchElement(name="KUKA 6-Axis Articulated Robot", element_type=ArchElementType.DEVICE, role="Material Handling & Palletizing", tech_stack="KRC4 Controller"),
                        ArchElement(name="Physical Lockout E-Stop", element_type=ArchElementType.DEVICE, role="Hardware Safety Loop", tech_stack="Hardwired Relay")
                    ]
                )
            ],
            annotations=[
                ArchAnnotation(
                    category="Zero Inbound Internet Access",
                    principle="No direct TCP connection can traverse from Enterprise Cloud to Level 2/1 machine controllers."
                ),
                ArchAnnotation(
                    category="Hardware Data Diode",
                    principle="Sensor telemetry is pushed out of the plant via optical unidirectional diodes, preventing reverse intrusion."
                ),
                ArchAnnotation(
                    category="Segmented Cell VLANs",
                    principle="Every production line is isolated into dedicated Layer 2 micro-segmented broadcast domains."
                )
            ]
        )
