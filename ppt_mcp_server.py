import os
from typing import List, Optional, Dict, Any
from fastmcp import FastMCP
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

# Professional Presentation Design Guardrails for MCP Server
MCP_PPT_SYSTEM_PROMPT = """
You are an expert Enterprise Solutions Architect and Presentation Designer. When generating slides using python-pptx or MCP tools, you MUST strictly follow these layout rules:

1. THE "3-BULLET MAXIMUM" RULE:
   - Never output dense walls of text or long vertical bullet lists.
   - Limit any text block/card to a maximum of 3 concise, high-impact bullet points or short lines.

2. MULTI-COLUMN CARD LAYOUTS:
   - For comparisons, value propositions, or feature overviews, divide the slide canvas into 2 or 3 distinct side-by-side rectangular container cards with clear visual headers and whitespace.

3. ARCHITECTURE & WORKFLOW SPLIT LAYOUTS:
   - For slides categorized under "Architecture", "Pipeline", or "Workflow", allocate at least 50% of the slide to structured horizontal block diagrams (e.g., [ SAP Core ] -> [ Middleware ] -> [ Edge Terminals ]) or numbered sequence cards (1, 2, 3) rather than text descriptions.

4. NARRATIVE HEADINGS & SUBHEADERS:
   - Slide titles must use action-oriented narrative subheaders (e.g., "HOW IT WORKS: One-way reads out of SAP, a human gate back in") rather than dry single-word labels.

5. TYPOGRAPHY & EMPHASIS:
   - Dynamically increase font sizing for key metrics (ROI figures, timeline days, percentages) while keeping body text clean and readable (14pt-16pt range).
"""

# Enterprise Architecture & Systems-Thinking Guardrails for MCP Server
EXENTRIC_ARCHITECT_SYSTEM_PROMPT = """
You are a Principal Enterprise Solutions Architect and Digital Transformation Strategist (synthesizing principles from Jeanne Ross, John Zachman, Eliyahu Goldratt, Peter Senge, and Dennis Brandl). 

When generating presentation decks or solution designs through this MCP server, you must strictly adhere to these architectural standards:

1. UNDERLYING MECHANICS & TRUTH:
   - Never use superficial buzzwords or generic bullet lists. 
   - Explain the "hidden truth" and system mechanics: how data flows, where constraints live, how memory or performance is protected, and why conventional approaches fail.

2. SYSTEMS THINKING & FEEDBACK LOOPS (Senge / Meadows / Goldratt):
   - Design flows that highlight constraints, bottlenecks, feedback loops, and closed-loop validation rather than isolated static screens.
   - Every metric must connect to an operational lever and a financial outcome.

3. ENTERPRISE ONTOLOGY & GOVERNANCE (Zachman / Ross):
   - Structure solutions across clear operational dimensions: Foundation, Data Lineage, Execution Reality, Governance, and Business Value.
   - Maintain strict separation of concerns (e.g., ring-fenced analytical layers, zero data duplication, single source of truth tied directly to the universal ledger).

4. LAYOUT & NARRATIVE RHYTHM:
   - Use narrative, conversational subheaders (e.g., "HOW IT WORKS: The maths happens where the data already lives").
   - Balance clean multi-column comparison layouts with deep architectural breakdown tables, sequence flows, and quantitative impact metrics. Avoid text clutter.
"""

COMBINED_MCP_SYSTEM_PROMPT = f"{MCP_PPT_SYSTEM_PROMPT}\n\n{EXENTRIC_ARCHITECT_SYSTEM_PROMPT}"

# Initialize FastMCP Server
mcp = FastMCP("PowerPoint-MCP-Server", instructions=COMBINED_MCP_SYSTEM_PROMPT)

@mcp.prompt("presentation_design_guardrails")
def get_design_guardrails() -> str:
    """Returns the professional presentation design guardrails and layout rules."""
    return MCP_PPT_SYSTEM_PROMPT

@mcp.prompt("enterprise_architecture_guardrails")
def get_architect_guardrails() -> str:
    """Returns the enterprise architecture and systems-thinking guardrails."""
    return EXENTRIC_ARCHITECT_SYSTEM_PROMPT

# Map user-friendly shape names to MSO_SHAPE enums
SHAPE_MAP = {
    "rectangle": MSO_SHAPE.RECTANGLE,
    "rounded_rectangle": MSO_SHAPE.ROUNDED_RECTANGLE,
    "oval": MSO_SHAPE.OVAL,
    "circle": MSO_SHAPE.OVAL,
    "ellipse": MSO_SHAPE.OVAL,
    "triangle": MSO_SHAPE.ISOSCELES_TRIANGLE,
    "diamond": MSO_SHAPE.DIAMOND,
    "right_arrow": MSO_SHAPE.RIGHT_ARROW,
    "left_arrow": MSO_SHAPE.LEFT_ARROW,
    "up_arrow": MSO_SHAPE.UP_ARROW,
    "down_arrow": MSO_SHAPE.DOWN_ARROW,
    "star": MSO_SHAPE.STAR_5_POINT,
    "hexagon": MSO_SHAPE.HEXAGON,
    "pentagon": MSO_SHAPE.PENTAGON,
    "cube": MSO_SHAPE.CUBE,
    "cloud": MSO_SHAPE.CLOUD,
    "heart": MSO_SHAPE.HEART,
}

# Helper to parse hex colors
def parse_hex_color(hex_str: str) -> RGBColor:
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6:
        raise ValueError(f"Invalid hex color format: {hex_str}. Must be 6 hex characters.")
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return RGBColor(r, g, b)

# Helper to load a presentation
def load_prs(path: str) -> Presentation:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Presentation file not found at: {path}")
    return Presentation(path)

# Helper to resolve slide layout
def get_slide_layout(prs: Presentation, layout_idx: int):
    try:
        return prs.slide_layouts[layout_idx]
    except IndexError:
        # Fall back to Blank layout if layout index is invalid
        return prs.slide_layouts[6]

@mcp.tool
def create_presentation(path: str) -> str:
    """
    Creates a new, blank PowerPoint presentation at the specified path.
    If directories in the path do not exist, they will be created.
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    prs = Presentation()
    prs.save(path)
    return f"Successfully created a new PowerPoint presentation at: {path}"

@mcp.tool
def add_slide(path: str, layout_idx: int = 6) -> str:
    """
    Adds a new slide to the presentation at path.
    layout_idx: Index of layout template to use (0: Title, 1: Title & Content, 5: Title Only, 6: Blank).
    Returns a success message with the index of the newly added slide.
    """
    prs = load_prs(path)
    layout = get_slide_layout(prs, layout_idx)
    slide = prs.slides.add_slide(layout)
    prs.save(path)
    slide_idx = len(prs.slides) - 1
    return f"Successfully added slide at index {slide_idx} using layout index {layout_idx}."

@mcp.tool
def delete_slide(path: str, slide_idx: int) -> str:
    """
    Deletes the slide at the specified index from the presentation.
    """
    prs = load_prs(path)
    if slide_idx < 0 or slide_idx >= len(prs.slides):
        return f"Error: Slide index {slide_idx} is out of range. Slide count is {len(prs.slides)}."
    
    # Delete slide by modifying the slide ID list
    id_list = prs.slides._sldIdLst
    del id_list[slide_idx]
    
    prs.save(path)
    return f"Successfully deleted slide at index {slide_idx}."

@mcp.tool
def add_text(
    path: str,
    slide_idx: int,
    text: str,
    left_in: float,
    top_in: float,
    width_in: float,
    height_in: float,
    font_name: str = "Calibri",
    font_size_pt: int = 18,
    bold: bool = False,
    italic: bool = False,
    color_hex: str = "000000",
    align: str = "left"
) -> str:
    """
    Adds a textbox with formatted text to a slide.
    left_in, top_in, width_in, height_in: Dimensions in inches.
    align: 'left', 'center', 'right', or 'justify'.
    color_hex: Hex code for font color (e.g. 'FF0000' for red).
    """
    prs = load_prs(path)
    if slide_idx < 0 or slide_idx >= len(prs.slides):
        return f"Error: Slide index {slide_idx} is out of range."
    
    slide = prs.slides[slide_idx]
    tx_box = slide.shapes.add_textbox(Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in))
    tf = tx_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = font_name
    p.font.size = Pt(font_size_pt)
    p.font.bold = bold
    p.font.italic = italic
    p.font.color.rgb = parse_hex_color(color_hex)
    
    align_lower = align.lower()
    if align_lower == "center":
        p.alignment = PP_ALIGN.CENTER
    elif align_lower == "right":
        p.alignment = PP_ALIGN.RIGHT
    elif align_lower == "justify":
        p.alignment = PP_ALIGN.JUSTIFY
    else:
        p.alignment = PP_ALIGN.LEFT
        
    prs.save(path)
    return f"Successfully added text to slide {slide_idx}."

@mcp.tool
def add_bullet_points(
    path: str,
    slide_idx: int,
    points: List[str],
    left_in: float,
    top_in: float,
    width_in: float,
    height_in: float,
    font_name: str = "Calibri",
    font_size_pt: int = 16,
    color_hex: str = "000000"
) -> str:
    """
    Adds a list of bullet points in a single textbox.
    """
    prs = load_prs(path)
    if slide_idx < 0 or slide_idx >= len(prs.slides):
        return f"Error: Slide index {slide_idx} is out of range."
    
    slide = prs.slides[slide_idx]
    tx_box = slide.shapes.add_textbox(Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in))
    tf = tx_box.text_frame
    tf.word_wrap = True
    
    for i, pt_text in enumerate(points):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = pt_text
        p.level = 0
        p.font.name = font_name
        p.font.size = Pt(font_size_pt)
        p.font.color.rgb = parse_hex_color(color_hex)
        
    prs.save(path)
    return f"Successfully added {len(points)} bullet points to slide {slide_idx}."

def add_split_cards_to_slide(slide, left_title: str, left_bullets: List[str], right_title: str, right_bullets: List[str],
                             bg_rgb: RGBColor = RGBColor(245, 247, 250),
                             border_rgb: RGBColor = RGBColor(210, 215, 225),
                             top_in: float = 1.8, height_in: float = 4.5):
    """Creates a clean 2-column comparison or architectural breakdown card layout."""
    # Left Card Container
    left_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(top_in), Inches(5.6), Inches(height_in))
    left_box.fill.solid()
    left_box.fill.fore_color.rgb = bg_rgb
    left_box.line.color.rgb = border_rgb
    
    tf = left_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = left_title
    p.font.bold = True
    p.font.size = Pt(16)
    
    for bullet in left_bullets[:3]: # Enforce max 3 bullets
        bp = tf.add_paragraph()
        bp.text = f"• {bullet}"
        bp.font.size = Pt(13)

    # Right Card Container
    right_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(top_in), Inches(5.6), Inches(height_in))
    right_box.fill.solid()
    right_box.fill.fore_color.rgb = bg_rgb
    right_box.line.color.rgb = border_rgb
    
    rtf = right_box.text_frame
    rtf.word_wrap = True
    rp = rtf.paragraphs[0]
    rp.text = right_title
    rp.font.bold = True
    rp.font.size = Pt(16)
    
    for bullet in right_bullets[:3]: # Enforce max 3 bullets
        rbp = rtf.add_paragraph()
        rbp.text = f"• {bullet}"
        rbp.font.size = Pt(13)
        
    return left_box, right_box

@mcp.tool
def add_split_cards(
    path: str,
    slide_idx: int,
    left_title: str,
    left_bullets: List[str],
    right_title: str,
    right_bullets: List[str],
    bg_color_hex: str = "F5F7FA",
    border_color_hex: str = "D2D7E1",
    top_in: float = 1.8,
    height_in: float = 4.5
) -> str:
    """
    Creates a clean 2-column comparison or architectural breakdown card layout.
    Enforces the '3-bullet maximum' rule per card container.
    """
    prs = load_prs(path)
    if slide_idx < 0 or slide_idx >= len(prs.slides):
        return f"Error: Slide index {slide_idx} is out of range."
        
    slide = prs.slides[slide_idx]
    bg_rgb = parse_hex_color(bg_color_hex)
    border_rgb = parse_hex_color(border_color_hex)
    add_split_cards_to_slide(slide, left_title, left_bullets, right_title, right_bullets, bg_rgb, border_rgb, top_in, height_in)
    
    prs.save(path)
    return f"Successfully added split cards layout to slide {slide_idx}."

@mcp.tool
def add_shape(
    path: str,
    slide_idx: int,
    shape_type: str,
    left_in: float,
    top_in: float,
    width_in: float,
    height_in: float,
    fill_color_hex: Optional[str] = None,
    line_color_hex: Optional[str] = None,
    line_width_pt: float = 1.0
) -> str:
    """
    Adds a geometric shape to the slide.
    shape_type: 'rectangle', 'rounded_rectangle', 'oval'/'circle', 'triangle', 'diamond', 'star', 'hexagon', 'pentagon', 'cube', 'cloud', 'heart'.
    fill_color_hex: Fill color hex code (e.g. '3399FF'), or omit for transparent/default.
    line_color_hex: Border color hex code (e.g. '000000'), or omit for no border.
    """
    prs = load_prs(path)
    if slide_idx < 0 or slide_idx >= len(prs.slides):
        return f"Error: Slide index {slide_idx} is out of range."
    
    shape_type_lower = shape_type.lower()
    if shape_type_lower not in SHAPE_MAP:
        return f"Error: Unsupported shape type '{shape_type}'. Supported types: {list(SHAPE_MAP.keys())}"
    
    slide = prs.slides[slide_idx]
    shape = slide.shapes.add_shape(
        SHAPE_MAP[shape_type_lower],
        Inches(left_in),
        Inches(top_in),
        Inches(width_in),
        Inches(height_in)
    )
    
    # Configure Fill
    if fill_color_hex:
        shape.fill.solid()
        shape.fill.fore_color.rgb = parse_hex_color(fill_color_hex)
    else:
        shape.fill.background()
        
    # Configure Line (Border)
    if line_color_hex:
        shape.line.color.rgb = parse_hex_color(line_color_hex)
        shape.line.width = Pt(line_width_pt)
    else:
        shape.line.fill.background()
        
    prs.save(path)
    return f"Successfully added '{shape_type}' shape to slide {slide_idx}."

@mcp.tool
def add_picture(
    path: str,
    slide_idx: int,
    image_path: str,
    left_in: float,
    top_in: float,
    width_in: Optional[float] = None,
    height_in: Optional[float] = None
) -> str:
    """
    Adds a picture to the slide from a file path.
    If width_in or height_in are specified, scales the image accordingly.
    """
    prs = load_prs(path)
    if slide_idx < 0 or slide_idx >= len(prs.slides):
        return f"Error: Slide index {slide_idx} is out of range."
    
    if not os.path.exists(image_path):
        return f"Error: Image file not found at: {image_path}"
        
    slide = prs.slides[slide_idx]
    
    w = Inches(width_in) if width_in else None
    h = Inches(height_in) if height_in else None
    
    slide.shapes.add_picture(image_path, Inches(left_in), Inches(top_in), width=w, height=h)
    prs.save(path)
    return f"Successfully added picture to slide {slide_idx}."

@mcp.tool
def add_table(
    path: str,
    slide_idx: int,
    rows: int,
    cols: int,
    left_in: float,
    top_in: float,
    width_in: float,
    height_in: float,
    data: Optional[List[List[str]]] = None
) -> str:
    """
    Adds a table to the slide.
    data: Optional 2D list of strings to populate the table cells initially.
    """
    prs = load_prs(path)
    if slide_idx < 0 or slide_idx >= len(prs.slides):
        return f"Error: Slide index {slide_idx} is out of range."
        
    slide = prs.slides[slide_idx]
    table_shape = slide.shapes.add_table(rows, cols, Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in))
    table = table_shape.table
    
    if data:
        for r_idx, row_data in enumerate(data):
            if r_idx >= rows:
                break
            for c_idx, val in enumerate(row_data):
                if c_idx >= cols:
                    break
                table.cell(r_idx, c_idx).text = str(val)
                
    prs.save(path)
    return f"Successfully added table to slide {slide_idx}."

@mcp.tool
def get_presentation_info(path: str) -> Dict[str, Any]:
    """
    Inspects a presentation at path and returns a detailed structure of its slides and elements.
    """
    prs = load_prs(path)
    info = {
        "path": path,
        "slide_count": len(prs.slides),
        "slides": []
    }
    
    for idx, slide in enumerate(prs.slides):
        slide_info = {
            "index": idx,
            "shapes": []
        }
        
        for shape in slide.shapes:
            shape_info = {
                "name": shape.name,
                "id": shape.shape_id,
                "left_in": round(shape.left / Inches(1), 2) if shape.left else 0,
                "top_in": round(shape.top / Inches(1), 2) if shape.top else 0,
                "width_in": round(shape.width / Inches(1), 2) if shape.width else 0,
                "height_in": round(shape.height / Inches(1), 2) if shape.height else 0,
                "type": str(shape.shape_type)
            }
            
            # Extract text if textbox/shape has it
            if shape.has_text_frame:
                texts = [p.text for p in shape.text_frame.paragraphs if p.text]
                if texts:
                    shape_info["text"] = "\n".join(texts)
                    
            # Extract table content
            if shape.has_table:
                table_data = []
                table = shape.table
                for r in range(len(table.rows)):
                    row_cells = []
                    for c in range(len(table.columns)):
                        row_cells.append(table.cell(r, c).text)
                    table_data.append(row_cells)
                shape_info["table"] = table_data
                
            slide_info["shapes"].append(shape_info)
            
        info["slides"].append(slide_info)
        
    return info

@mcp.tool
def search_replace_text(path: str, search_str: str, replace_str: str) -> str:
    """
    Searches for search_str and replaces it with replace_str in all slides, textboxes, shapes, and tables.
    """
    prs = load_prs(path)
    replacements_count = 0
    
    # Helper to replace text in a text frame while maintaining run structures
    def replace_in_tf(tf) -> int:
        count = 0
        for paragraph in tf.paragraphs:
            if search_str in paragraph.text:
                if len(paragraph.runs) == 1:
                    run = paragraph.runs[0]
                    if search_str in run.text:
                        run.text = run.text.replace(search_str, replace_str)
                        count += 1
                else:
                    paragraph.text = paragraph.text.replace(search_str, replace_str)
                    count += 1
        return count

    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                replacements_count += replace_in_tf(shape.text_frame)
            if shape.has_table:
                table = shape.table
                for r in range(len(table.rows)):
                    for c in range(len(table.columns)):
                        cell = table.cell(r, c)
                        if cell.text_frame:
                            replacements_count += replace_in_tf(cell.text_frame)
                            
    if replacements_count > 0:
        prs.save(path)
        
    return f"Successfully performed {replacements_count} replacements in presentation."


# -----------------------------------------------------------------------------
# Enterprise Visual Primitive Library & Semantic Slide Tools
# -----------------------------------------------------------------------------
import json
import inspect
from design_system.spacing import CanvasBounds, Margins, SpacingScale
from design_system.color import ExecutiveNavyTheme, ConsultingSlateTheme, ColorSystem
from design_system.library import (
    PRIMITIVE_CATALOG,
    list_primitives_catalog,
    get_primitive_metadata,
    normalize_primitive_key,
)
from design_system.library.architecture import ArchTierData
from design_system.semantic import (
    SemanticSlide,
    VisualIntent,
    KeyMetric,
    ProcessStep,
    RoadmapPhase,
    TableData,
    ContentBlock,
    ArchitectureTier,
)
from design_system.renderer import PPTXRenderer


@mcp.tool
def list_visual_primitives() -> Dict[str, Any]:
    """
    Returns the complete catalog of all 60 first-class Visual Primitives supported
    by the MCP server across 9 enterprise domains:
    1. ARCHITECTURE (1–9)
    2. PROCESS (10–16)
    3. DATA (17–21)
    4. ANALYTICS (22–34)
    5. BUSINESS (35–41)
    6. DELIVERY (42–46)
    7. GOVERNANCE (47–50)
    8. STRUCTURED INFORMATION (51–56)
    9. NARRATIVE (57–60)
    """
    catalog = list_primitives_catalog()
    domains: Dict[str, List[Dict[str, Any]]] = {}
    for item in catalog:
        cat = item["category"]
        if cat not in domains:
            domains[cat] = []
        domains[cat].append({
            "id": item["id"],
            "key": item["key"],
            "name": item["name"],
            "description": item["description"]
        })
    return {
        "total_primitives": len(catalog),
        "domains": domains
    }


@mcp.tool
def render_visual_primitive(
    path: str,
    slide_idx: int,
    primitive_name: str,
    data: Any,
    theme_name: str = "navy",
    left_in: Optional[float] = None,
    top_in: Optional[float] = None,
    width_in: Optional[float] = None,
    height_in: Optional[float] = None
) -> str:
    """
    Renders any of the 60 enterprise visual primitives directly onto a slide.
    
    primitive_name: Key, ID (1-60), or name of the primitive (e.g. 'system_architecture', 'kpi_strip', 'waterfall', 'approval_gates').
    data: JSON string or object containing the data payload for the primitive.
    theme_name: 'navy' (Executive Dark) or 'slate' (Consulting Light).
    left_in, top_in, width_in, height_in: Optional bounding box in inches. Defaults to safe canvas margins.
    """
    prs = load_prs(path)
    if slide_idx < 0 or slide_idx >= len(prs.slides):
        return f"Error: Slide index {slide_idx} is out of range. Slide count is {len(prs.slides)}."

    meta = get_primitive_metadata(primitive_name)
    if not meta:
        valid_keys = [k for k in sorted(PRIMITIVE_CATALOG.keys())]
        return f"Error: Unknown visual primitive '{primitive_name}'. Valid primitives include: {valid_keys[:10]}... (use list_visual_primitives for all 60)"

    slide = prs.slides[slide_idx]
    prim_class = meta["class"]
    norm_key = meta["key"]

    # Resolve Theme
    theme = ConsultingSlateTheme if theme_name.lower() in ("slate", "light", "white") else ExecutiveNavyTheme

    # Resolve Dimensions
    l = left_in if left_in is not None else Margins.left
    t = top_in if top_in is not None else 1.40
    w = width_in if width_in is not None else Margins().usable_width
    h = height_in if height_in is not None else 5.40

    # Parse payload if JSON string
    parsed_data = json.loads(data) if isinstance(data, str) else data

    # Prepare Arguments
    sig = inspect.signature(prim_class.render)
    all_param_names = [p.name for p in sig.parameters.values()]
    custom_params = [name for name in all_param_names if name not in ("slide", "left", "top", "width", "height", "theme")]

    kwargs = {
        "slide": slide,
        "left": l,
        "top": t,
        "width": w,
        "height": h,
        "theme": theme,
    }

    if isinstance(parsed_data, dict):
        for k, v in parsed_data.items():
            if k in custom_params:
                kwargs[k] = v
    elif isinstance(parsed_data, list):
        if len(custom_params) == 1:
            kwargs[custom_params[0]] = parsed_data
        else:
            return f"Error: Primitive '{norm_key}' expects arguments: {custom_params}. Provide a dictionary/JSON object mapping these parameters."

    # Special handling for dataclasses like ArchTierData
    if norm_key == "system_architecture" and "tiers" in kwargs:
        converted_tiers = []
        for tier in kwargs["tiers"]:
            if isinstance(tier, dict):
                converted_tiers.append(ArchTierData(**tier))
            elif isinstance(tier, (list, tuple)):
                converted_tiers.append(ArchTierData(
                    tier_name=tier[0],
                    subtitle=tier[1] if len(tier) > 1 and isinstance(tier[1], str) else "System Tier",
                    subsystems=tier[2] if len(tier) > 2 and isinstance(tier[2], list) else (tier[1] if isinstance(tier[1], list) else []),
                    protocol_to_next=tier[3] if len(tier) > 3 else None
                ))
            else:
                converted_tiers.append(tier)
        kwargs["tiers"] = converted_tiers

    try:
        prim_class.render(**kwargs)
        prs.save(path)
        return f"Successfully rendered '{meta['name']}' (Primitive #{meta['id']}) on slide {slide_idx}."
    except Exception as e:
        return f"Error executing primitive '{meta['name']}': {str(e)}"


@mcp.tool
def render_semantic_slide(
    path: str,
    title: str,
    narrative_subtitle: str,
    category_tag: str = "EXECUTIVE ARCHITECTURE",
    visual_intent: str = "SYSTEM_ARCHITECTURE",
    is_dark: bool = True,
    slide_number: int = 1,
    total_slides: int = 1,
    callout_banner: Optional[str] = None,
    content_blocks: Optional[List[Dict[str, Any]]] = None,
    key_metrics: Optional[List[Dict[str, Any]]] = None,
    process_steps: Optional[List[Dict[str, Any]]] = None,
    table_data: Optional[Dict[str, Any]] = None
) -> str:
    """
    Renders an end-to-end publication-grade Semantic Slide using the Presentation Design System.
    Strictly enforces 16:9 widescreen canvas, 'Inter' typography tokens, safe margins, and visual intent.
    """
    prs = load_prs(path)

    # Resolve Visual Intent enum
    intent_map = {
        "SYSTEM_ARCHITECTURE": VisualIntent.SYSTEM_ARCHITECTURE,
        "GOVERNANCE_MATRIX": VisualIntent.GOVERNANCE_MATRIX,
        "VALUE_REALIZATION": VisualIntent.VALUE_REALIZATION,
        "PROBLEM_FRICTION": VisualIntent.PROBLEM_FRICTION,
        "GENERIC_COMPARISON": VisualIntent.GENERIC_COMPARISON,
        "EXECUTIVE_OPENING": VisualIntent.EXECUTIVE_OPENING,
        "PROCESS_JOURNEY": VisualIntent.PROCESS_JOURNEY,
        "PHASED_ROADMAP": VisualIntent.PHASED_ROADMAP,
        "OPERATIONAL_COCKPIT": VisualIntent.OPERATIONAL_COCKPIT,
    }
    v_intent = intent_map.get(visual_intent.upper(), VisualIntent.SYSTEM_ARCHITECTURE)

    # Flexible builders for nested structures
    def _parse_content_block(b: Dict[str, Any]) -> ContentBlock:
        title = b.get("title", "")
        subtitle = b.get("subtitle")
        annotation = b.get("annotation")
        bullets = []
        if "bullets" in b and isinstance(b["bullets"], list):
            for it in b["bullets"]:
                if isinstance(it, (list, tuple)) and len(it) >= 2:
                    bullets.append((str(it[0]), str(it[1])))
                else:
                    bullets.append(("", str(it)))
        elif "description" in b:
            lead = b.get("lead_in", "")
            bullets.append((lead, str(b["description"])))
        return ContentBlock(title=title, subtitle=subtitle, bullets=bullets, annotation=annotation)

    c_blocks = [_parse_content_block(b) for b in (content_blocks or [])]
    k_metrics = [KeyMetric(**m) for m in (key_metrics or [])]
    p_steps = [ProcessStep(**s) for s in (process_steps or [])]
    t_data = TableData(**table_data) if table_data else None

    elements: List[Any] = []
    if v_intent == VisualIntent.SYSTEM_ARCHITECTURE and content_blocks:
        for idx, b in enumerate(content_blocks, start=1):
            bullets = [it[1] if isinstance(it, (list, tuple)) else str(it) for it in b.get("bullets", [])] if "bullets" in b else ([b["description"]] if "description" in b else [])
            elements.append(ArchitectureTier(
                tier_number=idx,
                tier_name=b.get("title", f"TIER {idx}"),
                subtitle=b.get("lead_in", b.get("subtitle", "Subsystem Tier")),
                components=bullets
            ))
    else:
        elements.extend(c_blocks)

    elements.extend(k_metrics)
    elements.extend(p_steps)
    if t_data:
        elements.append(t_data)

    semantic_slide = SemanticSlide(
        title=title,
        narrative_subtitle=narrative_subtitle,
        category_tag=category_tag,
        slide_number=slide_number,
        total_slides=total_slides,
        visual_intent=v_intent,
        is_dark=is_dark,
        callout_banner=callout_banner,
        elements=elements,
    )

    PPTXRenderer.render(prs, semantic_slide)
    prs.save(path)
    new_idx = len(prs.slides) - 1
    return f"Successfully rendered semantic slide '{title}' at index {new_idx}."


# -----------------------------------------------------------------------------
# Enterprise Architecture Composition Engine Tools
# -----------------------------------------------------------------------------
from design_system.composition import (
    NarrativeSection,
    SectionArchetype,
    SECTION_ARCHETYPES,
    VisualRhythmController,
    ArchitectureDeckSpec,
    EnterpriseArchitectureCompositionEngine,
)


@mcp.tool
def list_narrative_sections() -> Dict[str, Any]:
    """
    Returns the 15 canonical enterprise architecture narrative sections with their
    archetypes, dominant questions, layout families, and recommended visual primitives:
    1. EXECUTIVE_CONTEXT
    2. CURRENT_REALITY
    3. BUSINESS_PROBLEM
    4. ROOT_CAUSE_CONSTRAINT
    5. OPPORTUNITY
    6. TARGET_ARCHITECTURE
    7. PROCESS_TRANSFORMATION
    8. DATA_INTEGRATION_ARCHITECTURE
    9. OPERATIONAL_EXECUTION
    10. GOVERNANCE
    11. ANALYTICS_INTELLIGENCE
    12. IMPLEMENTATION_ROADMAP
    13. BUSINESS_OUTCOMES
    14. RISKS_ASSUMPTIONS
    15. COMMERCIAL_NEXT_STEPS
    """
    sections_list = []
    for s_enum, arch in sorted(SECTION_ARCHETYPES.items(), key=lambda x: x[0].value):
        sections_list.append({
            "section_number": s_enum.value,
            "section_key": s_enum.name,
            "title": arch.display_title,
            "category_tag": arch.category_tag,
            "dominant_question": arch.dominant_question,
            "primary_primitives": arch.primary_primitives,
            "preferred_theme_mode": arch.preferred_theme_mode,
            "layout_family": arch.layout_family
        })
    return {
        "total_sections": len(sections_list),
        "narrative_sections": sections_list
    }


@mcp.tool
def compose_architecture_deck(
    path: str,
    presentation_title: str,
    client_name: str,
    target_solution: str,
    sections: List[Dict[str, Any]],
    author: str = "Enterprise Architecture Advisory"
) -> str:
    """
    Composes and renders a complete, multi-slide enterprise architecture solution presentation
    as a coherent narrative arc enforcing visual rhythm and anti-monotony pacing.
    
    path: Destination file path for .pptx
    presentation_title: Main proposal/deck title
    client_name: Client organization name
    target_solution: Focus solution or architecture scope
    sections: List of section dicts specifying section number/key, title, subtitle, data, and optional primitive overrides.
    """
    # Create or load presentation
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    prs = Presentation()

    # Map input sections into NarrativeSection enum
    parsed_sections: List[Tuple[NarrativeSection, Dict[str, Any]]] = []
    for sec_data in sections:
        raw_sec = sec_data.get("section", 1)
        target_enum = None
        if isinstance(raw_sec, int):
            for e in NarrativeSection:
                if e.value == raw_sec:
                    target_enum = e
                    break
        elif isinstance(raw_sec, str):
            clean_str = raw_sec.strip().upper().replace(" ", "_")
            for e in NarrativeSection:
                if e.name == clean_str:
                    target_enum = e
                    break
                if str(e.value) == raw_sec.strip():
                    target_enum = e
                    break

        if not target_enum:
            target_enum = NarrativeSection.TARGET_ARCHITECTURE

        parsed_sections.append((target_enum, sec_data))

    deck_spec = ArchitectureDeckSpec(
        presentation_title=presentation_title,
        client_name=client_name,
        target_solution=target_solution,
        author=author,
        sections=parsed_sections
    )

    msg = EnterpriseArchitectureCompositionEngine.render_deck(prs, deck_spec)
    prs.save(path)
    return f"{msg} Saved presentation at: {path}"


# -----------------------------------------------------------------------------
# Manufacturing Semantic Vocabulary Tool
# -----------------------------------------------------------------------------
from design_system.manufacturing_vocabulary import (
    ManufacturingSemanticAnalyzer,
    EntityCategory,
    SemanticPatternType
)


@mcp.tool
def analyze_manufacturing_semantics(text: str) -> Dict[str, Any]:
    """
    Analyzes presentation text against the Manufacturing Enterprise Architecture semantic vocabulary.
    
    Recognizes entities across:
      - ENTERPRISE: Business Unit, Plant, Site, Customer, Supplier
      - SAP / ERP: S/4HANA, Orders, Material, BOM, Routing, Batch, Serial, Inventory, Movements, Costs
      - MANUFACTURING: MES, MOM, Work Order, Operation, WIP, Work Center, Machine, Operator, Shift
      - QUALITY: Characteristic, Specification, Tolerance, Defect, NCR, CAPA, Calibration, Inspection Result
      - TRACEABILITY: Serial, Batch, Component, Genealogy, As-Built, Parent, Child, Consumption
      - INTEGRATION: API, OData, IDoc, Event, Message, Middleware, BTP, Edge, OPC UA, MQTT, Power BI

    Detects relational patterns:
      - SAP -> MES                          => Integration Architecture
      - Production Order -> Operation -> WIP => Manufacturing Process Flow
      - Serial -> Components -> Parameters  => Genealogy / As-Built Tree
      - Plant -> Work Center -> Machine     => Operational Hierarchy
      - KPI -> Decision -> Action           => Decision Loop / Outcome Chain
      - Tolerance -> Defect -> NCR -> CAPA  => Quality Exception Rework Flow
    """
    entities = ManufacturingSemanticAnalyzer.extract_entities(text)
    patterns = ManufacturingSemanticAnalyzer.detect_relational_patterns(text)

    entity_list = []
    for ent in entities:
        entity_list.append({
            "term": ent.term,
            "canonical_name": ent.canonical_name,
            "category": ent.category.name,
            "position": ent.position
        })

    pattern_list = []
    for pat in patterns:
        pattern_list.append({
            "pattern_type": pat.pattern_type.name,
            "matched_sequence": pat.matched_sequence,
            "confidence": round(pat.confidence, 2),
            "recommended_primitive": pat.recommended_primitive,
            "explanation": pat.explanation
        })

    recommended_primitive = patterns[0].recommended_primitive if patterns else "card_grid"

    return {
        "text_analyzed": text,
        "total_entities_found": len(entity_list),
        "entities": entity_list,
        "relational_patterns_detected": pattern_list,
        "recommended_visual_primitive": recommended_primitive
    }



# -----------------------------------------------------------------------------
# Executive Dashboard & Analytical Cockpit Tools
# -----------------------------------------------------------------------------
from design_system.dashboard import (
    DashboardArchetype,
    DashboardQuestionClassifier,
    ExecutiveCockpitSpec,
    ExecutiveDashboardComposer
)


@mcp.tool
def list_dashboard_archetypes() -> Dict[str, Any]:
    """
    Lists supported executive analytical dashboard archetypes and their canonical business questions.
    
    Demonstrates how the engine maps business decisions into 4-zone analytical cockpits:
    1. Executive KPI Strip ("WHAT CHANGED?")
    2. Analytical Trend / Comparison ("WHY DOES IT MATTER?")
    3. Structural Breakdown / Bottleneck ("WHERE IS THE PROBLEM?")
    4. Action-Oriented Exception Detail ("WHAT SHOULD WE ACT ON?")
    """
    archetypes = [
        {
            "archetype": "SHIPPING_PROMISE",
            "business_question": "Are we shipping what we promised?",
            "components": {
                "what_changed": "OTIF & Past Due KPI Strip",
                "why_it_matters": "6-Month OTIF Commitment vs Actual Line Chart",
                "where_is_the_problem": "Root-Cause Dispatch Delay Pareto",
                "what_should_we_act_on": "Critical Customer Shipment Exception Register"
            }
        },
        {
            "archetype": "PRODUCTION_CONSTRAINTS",
            "business_question": "Where is production constrained?",
            "components": {
                "what_changed": "Critical Bottleneck Load & Downtime KPI Strip",
                "why_it_matters": "Weekly Work Load vs Operating Capacity Bar Chart",
                "where_is_the_problem": "Work-Center Capacity vs Demand Comparison",
                "what_should_we_act_on": "Bottleneck Work-Center Resolution Action Table"
            }
        },
        {
            "archetype": "QUALITY_DRIVERS",
            "business_question": "What is driving poor quality?",
            "components": {
                "what_changed": "First Pass Yield & Scrap Rate KPI Strip",
                "why_it_matters": "Daily FPY Trajectory Trend Line Chart",
                "where_is_the_problem": "Quality Defect Concentration Pareto",
                "what_should_we_act_on": "Active NCR Quality Intervention Register"
            }
        },
        {
            "archetype": "WORKING_CAPITAL_WIP",
            "business_question": "Where is working capital trapped?",
            "components": {
                "what_changed": "Total WIP & Days of Supply KPI Strip",
                "why_it_matters": "Monthly Working Capital in WIP Trend Line Chart",
                "where_is_the_problem": "WIP Aging Buckets (<30d, 31-60d, 61-90d, >90d)",
                "what_should_we_act_on": "Top Trapped Inventory Lots & Liquidation Action Plan"
            }
        },
        {
            "archetype": "SUPPLIER_RISK",
            "business_question": "Which suppliers are creating risk?",
            "components": {
                "what_changed": "Supplier Delivery OTIF & Lead-Time Drift KPI Strip",
                "why_it_matters": "Vendor Actual Lead Time vs SLA Bar Chart",
                "where_is_the_problem": "Supplier Defect & Delay Impact Pareto",
                "what_should_we_act_on": "Critical Supplier Dual-Sourcing & Buffer Action Plan"
            }
        },
        {
            "archetype": "COPQ_FINANCIAL",
            "business_question": "How much is quality costing us?",
            "components": {
                "what_changed": "Annualized COPQ & Scrap Expense KPI Strip",
                "why_it_matters": "Monthly COPQ Actual vs Budget Trend Line Chart",
                "where_is_the_problem": "COPQ Element Concentration Pareto",
                "what_should_we_act_on": "Plant-Wide COPQ Reduction Program Action Register"
            }
        },
        {
            "archetype": "CUSTOM_COCKPIT",
            "business_question": "Dynamic executive question",
            "components": {
                "what_changed": "Executive Composite KPI Strip",
                "why_it_matters": "Analytical Performance Trajectory Chart",
                "where_is_the_problem": "Contribution & Segmentation Breakdown",
                "what_should_we_act_on": "Priority Action & Decision Register"
            }
        }
    ]
    return {
        "total_archetypes": len(archetypes),
        "archetypes": archetypes,
        "design_philosophy": "A dashboard is NOT a collection of KPI cards. Every visualization answers a business question without fake Power BI chrome."
    }


@mcp.tool
def render_executive_dashboard(
    path: str,
    business_question: str,
    key_takeaway: Optional[str] = None,
    client_name: str = "Executive Leadership",
    is_dark: bool = False,
    custom_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Renders an executive analytical cockpit slide mapped directly from a business question.
    
    Synthesizes a 4-zone analytical cockpit:
      1. 'WHAT CHANGED?' - Executive KPI strip
      2. 'WHY DOES IT MATTER?' - Historical trend / commitment trajectory
      3. 'WHERE IS THE PROBLEM?' - Root-cause breakdown / Pareto / capacity / aging
      4. 'WHAT SHOULD WE ACT ON?' - Action-oriented exception detail table
    
    Parameters:
      path: File path to PowerPoint presentation (created if not existing).
      business_question: The core executive inquiry (e.g. 'Are we shipping what we promised?').
      key_takeaway: Optional override for executive action summary.
      client_name: Enterprise client / organization banner.
      is_dark: True for Executive Navy, False for Consulting Slate Light (recommended for analytical contrast).
      custom_data: Optional override dictionary for kpis, trend, breakdown, and action table.
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    if os.path.exists(path):
        prs = Presentation(path)
    else:
        prs = Presentation()
        # Enforce standard widescreen 16:9 canvas
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.500)

    # Build cockpit specification from question
    spec = ExecutiveDashboardComposer.build_from_question(
        question=business_question,
        custom_data=custom_data,
        client_name=client_name
    )

    if key_takeaway:
        spec.key_takeaway = key_takeaway
    spec.is_dark = is_dark

    # Render native PowerPoint cockpit slide
    ExecutiveDashboardComposer.compose_and_render(prs, spec)
    prs.save(path)

    archetype = DashboardQuestionClassifier.classify(business_question)

    return {
        "status": "success",
        "presentation_path": path,
        "total_slides": len(prs.slides),
        "business_question": spec.business_question,
        "archetype": archetype.name,
        "key_takeaway": spec.key_takeaway,
        "theme": "Executive Navy (Dark)" if is_dark else "Consulting Slate (Light)",
        "analytical_zones_rendered": [
            "1. WHAT CHANGED? (Executive KPI Trajectory)",
            f"2. WHY DOES IT MATTER? ({spec.trend_title})",
            f"3. WHERE IS THE PROBLEM? ({spec.breakdown_title})",
            f"4. WHAT SHOULD WE ACT ON? ({spec.action_table_title})"
        ],
        "message": f"Successfully rendered Executive Cockpit '{spec.business_question}' to {path}"
    }



# -----------------------------------------------------------------------------
# Enterprise Architecture Diagram Tools
# -----------------------------------------------------------------------------
from design_system.architecture_engine import (
    ArchElementType,
    FlowDirection,
    ArchElement,
    ArchFlow,
    ArchLayer,
    ArchAnnotation,
    ArchitectureDiagramSpec,
    EnterpriseArchitectureComposer,
    ArchitectureBlueprintFactory
)


@mcp.tool
def list_architecture_templates() -> Dict[str, Any]:
    """
    Lists canonical enterprise architecture diagram blueprints.
    
    Shows how the engine renders genuine architecture using editable PowerPoint shapes:
      - Layers & boundaries (ISA-95 Level 4 down to Level 0)
      - Systems, Data Stores (cylinders MSO_SHAPE.CAN), Interfaces (hexagons), Devices, and Actors
      - Directional, Bidirectional, and Asynchronous Event Flows with protocol & data object labels
      - Whitespace between layers (no generic rounded cards)
      - Architectural principles & zero-loss guarantees callout panel
    """
    templates = [
        {
            "template_id": "CLEAN_CORE_SAP_TO_SHOPFLOOR",
            "title": "Clean-Core SAP S/4HANA to Shopfloor Architecture",
            "description": "5-tier ISA-95 architecture: S/4HANA Core -> BTP Integration -> MOM/MES -> Industrial Edge -> Shop Floor Devices.",
            "layers": [
                "ISA-95 LEVEL 4: Enterprise ERP & Cloud PLM",
                "BTP INTEGRATION: API Mediation & Event Mesh",
                "ISA-95 LEVEL 3: Plant MES & Execution Core",
                "ISA-95 LEVEL 2: Industrial Edge & Protocol Gateways",
                "ISA-95 LEVEL 1/0: Shop Floor PLCs, CNCs & Operators"
            ],
            "guarantees": [
                "Single financial ledger (zero ACDOCA replication)",
                "Air-gapped 48h edge buffering during WAN outage",
                "Sub-100ms deterministic machine safety loop"
            ]
        },
        {
            "template_id": "ZERO_TRUST_OT_PERIMETER",
            "title": "Zero-Trust Industrial OT Security & Trust Zones",
            "description": "Purdue Model security zones: Enterprise WAN -> DMZ Inspection -> Plant LAN -> Isolated OT Cells.",
            "layers": [
                "PURDUE LEVEL 4/5: Enterprise Cloud & Identity (Azure AD/Okta)",
                "PURDUE LEVEL 3.5: DMZ Reverse Proxy & Hardware Data Diode",
                "PURDUE LEVEL 3: Plant Operations MES & SCADA Historian",
                "PURDUE LEVEL 1/2: Isolated Cell Safety PLCs & Robotics"
            ],
            "guarantees": [
                "Zero inbound internet access to plant floor",
                "Unidirectional hardware data diode for telemetry egress",
                "Micro-segmented Layer 2 cell networks"
            ]
        },
        {
            "template_id": "CUSTOM_ARCHITECTURE",
            "title": "Custom Enterprise Solution Blueprint",
            "description": "Customizable multi-tier architecture with custom systems, data stores, interfaces, and protocols."
        }
    ]
    return {
        "total_templates": len(templates),
        "templates": templates,
        "design_principles": [
            "1. Establish visual hierarchy and layer whitespace.",
            "2. Distinguish systems, databases (cylinders), devices, and actors with distinct native shapes.",
            "3. Explicitly label interfaces, protocols, and moving data objects.",
            "4. Avoid decorative bubble boxes; communicate how the system works underneath."
        ]
    }


@mcp.tool
def render_enterprise_architecture_diagram(
    path: str,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    template_id: str = "CLEAN_CORE_SAP_TO_SHOPFLOOR",
    client_name: str = "Enterprise Architecture",
    is_dark: bool = True,
    custom_layers: Optional[List[Dict[str, Any]]] = None,
    custom_annotations: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """
    Renders a genuine enterprise architecture diagram using native editable PowerPoint shapes.
    
    Supports:
      - Layers & Trust Zones (Cloud, DMZ, Plant LAN, Air-Gapped OT)
      - Systems, Data Stores (cylinders MSO_SHAPE.CAN), Interfaces (hexagons), Devices, and Actors
      - Directional, Bidirectional, and Asynchronous Flows with protocol and data object movement labels
      - Architectural principles & zero-loss guarantees callout panel
      - Strict Inter font family typography compliance
    
    Parameters:
      path: File path to save PowerPoint presentation.
      title: Optional override for blueprint title.
      subtitle: Optional override for blueprint subtitle.
      template_id: 'CLEAN_CORE_SAP_TO_SHOPFLOOR', 'ZERO_TRUST_OT_PERIMETER', or 'CUSTOM_ARCHITECTURE'.
      client_name: Enterprise client or initiative name.
      is_dark: True for Executive Navy (recommended blueprint contrast), False for Slate Light.
      custom_layers: Optional list of layer definitions if customizing the stack.
      custom_annotations: Optional list of architectural principles [{'category': ..., 'principle': ...}].
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    if os.path.exists(path):
        prs = Presentation(path)
    else:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.500)

    # 1. Base Blueprint Selection
    clean_id = template_id.upper().strip()
    if clean_id == "ZERO_TRUST_OT_PERIMETER":
        spec = ArchitectureBlueprintFactory.zero_trust_ot_security_perimeter(client_name=client_name)
    elif custom_layers:
        # Build from custom layers
        parsed_layers = []
        for l_data in custom_layers:
            elements = []
            for e_data in l_data.get("elements", []):
                e_type_str = e_data.get("type", "SYSTEM").upper()
                e_type = getattr(ArchElementType, e_type_str, ArchElementType.SYSTEM)
                elements.append(ArchElement(
                    name=e_data.get("name", "System Component"),
                    element_type=e_type,
                    role=e_data.get("role"),
                    tech_stack=e_data.get("tech_stack") or e_data.get("tech"),
                    key_objects=e_data.get("key_objects", [])
                ))

            flow = None
            if "flow_to_next" in l_data and l_data["flow_to_next"]:
                f_data = l_data["flow_to_next"]
                f_dir_str = f_data.get("direction", "DOWN").upper()
                f_dir = getattr(FlowDirection, f_dir_str, FlowDirection.DOWN)
                flow = ArchFlow(
                    protocol=f_data.get("protocol", "HTTPS / REST"),
                    data_object=f_data.get("data_object", "[Data Payload]"),
                    direction=f_dir,
                    flow_badge=f_data.get("badge")
                )

            parsed_layers.append(ArchLayer(
                name=l_data.get("name", "ARCH LAYER"),
                level_tag=l_data.get("level_tag", "TIER"),
                trust_zone=l_data.get("trust_zone", "Enterprise Network"),
                elements=elements,
                flow_to_next=flow
            ))

        parsed_annotations = []
        if custom_annotations:
            for a_data in custom_annotations:
                parsed_annotations.append(ArchAnnotation(
                    category=a_data.get("category", "PRINCIPLE"),
                    principle=a_data.get("principle", "")
                ))

        spec = ArchitectureDiagramSpec(
            title=title or "Enterprise Solution Architecture Blueprint",
            subtitle=subtitle or "Multi-tier system architecture and interface topology",
            client_name=client_name,
            is_dark=is_dark,
            layers=parsed_layers,
            annotations=parsed_annotations
        )
    else:
        # Default canonical ISA-95 clean core
        spec = ArchitectureBlueprintFactory.clean_core_sap_to_shopfloor(client_name=client_name)

    # Apply overrides
    if title:
        spec.title = title
    if subtitle:
        spec.subtitle = subtitle
    spec.is_dark = is_dark
    spec.client_name = client_name

    # Render native PowerPoint architecture diagram
    EnterpriseArchitectureComposer.compose_and_render(prs, spec)
    prs.save(path)

    return {
        "status": "success",
        "presentation_path": path,
        "total_slides": len(prs.slides),
        "title": spec.title,
        "template_id": clean_id,
        "total_layers": len(spec.layers),
        "layer_names": [l.name for l in spec.layers],
        "total_annotations": len(spec.annotations),
        "theme": "Executive Navy (Dark Blueprint)" if is_dark else "Consulting Slate (Light)",
        "message": f"Successfully rendered Enterprise Architecture Blueprint '{spec.title}' to {path}"
    }



# -----------------------------------------------------------------------------
# Enterprise Table & Structured Information Tools
# -----------------------------------------------------------------------------
from design_system.table_engine import (
    TableArchetype,
    TableRowItem,
    EnterpriseTableSpec,
    TableDataClassifier,
    EnterpriseTableComposer,
    EnterpriseTableFactory
)


@mcp.tool
def list_table_archetypes() -> Dict[str, Any]:
    """
    Lists the 12 canonical enterprise table archetypes and their standard headers.
    
    Demonstrates first-class enterprise table features:
      - Merged section header rows
      - Data-type alignment (left for text, center for codes/status, right for numbers/financials)
      - Semantic status highlighting (Critical, Warning, Success, RACI roles)
      - Restrained borders and compact Inter typography
    """
    archetypes = [
        {"archetype": "ARCHITECTURE_COMPARISON", "title": "Architecture Comparison", "description": "Legacy vs target clean-core structural evaluation across coupling, ledger tie-out, and latency."},
        {"archetype": "REQUIREMENTS", "title": "Requirements Specification", "description": "Traceable capabilities mapped to ISA-95 layers, MoSCoW priorities, and acceptance criteria."},
        {"archetype": "INTERFACE_CATALOGUE", "title": "Interface Catalogue", "description": "IT/OT boundary protocols (OData, OPC UA, RFC, WebSocket), frequencies, and payload schemas."},
        {"archetype": "KPI_DEFINITIONS", "title": "KPI Definitions Master", "description": "Mathematical definitions, baseline/target SLAs, source of truth ledgers, and reporting cadences."},
        {"archetype": "RISKS", "title": "Risk & Mitigation Register", "description": "Transformation risks, probabilities, impacts, scores, and proactive architectural mitigations."},
        {"archetype": "ASSUMPTIONS", "title": "Assumptions Matrix", "description": "Technical and operational assumptions, impacts if invalid, validation gates, and owners."},
        {"archetype": "COMMERCIAL_PROPOSAL", "title": "Commercial Proposal", "description": "Fixed-price milestone deliverables, target gates, investments, and payment triggers."},
        {"archetype": "IMPLEMENTATION_SCOPE", "title": "Implementation Scope", "description": "Workstream commitments, explicit out-of-scope exclusions, and prerequisite deliverables."},
        {"archetype": "RESPONSIBILITY_MATRIX", "title": "Responsibility Matrix (RACI)", "description": "Governance allocation across CXO, Lead Architect, Integrator, and Operations."},
        {"archetype": "ROADMAP", "title": "Roadmap Specification", "description": "Phased implementation cadence with verified exit criteria and core deliverables."},
        {"archetype": "BUSINESS_BENEFITS", "title": "Business Benefits & ROI", "description": "Audited operational levers, run-rate baselines/targets, annual EBITDA impact, and payback."},
        {"archetype": "DATA_MAPPINGS", "title": "Technical Data Mappings", "description": "Field-level entity lineage, types, and transformation/validation rules (e.g. S/4HANA to DMC)."},
        {"archetype": "CUSTOM_TABLE", "title": "Custom Specification Table", "description": "Customizable enterprise table with custom headers, section rows, and data rows."}
    ]
    return {
        "total_archetypes": len(archetypes),
        "archetypes": archetypes,
        "formatting_standards": [
            "Strong hierarchy with merged section rows",
            "Automatic data-type alignment (left text, center codes, right numbers/financials)",
            "Semantic status coloring for Critical/Warning/Success/RACI",
            "Compact Inter typography with restrained borders"
        ]
    }


@mcp.tool
def render_enterprise_table(
    path: str,
    archetype: str = "ARCHITECTURE_COMPARISON",
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    client_name: str = "Enterprise Architecture",
    is_dark: bool = False,
    custom_headers: Optional[List[str]] = None,
    custom_rows: Optional[List[Any]] = None,
    custom_col_weights: Optional[List[float]] = None,
    callout_note: Optional[str] = None
) -> Dict[str, Any]:
    """
    Renders an enterprise structured information table slide using native PowerPoint table shapes.
    
    Supports:
      - 12 canonical archetypes (ARCHITECTURE_COMPARISON, REQUIREMENTS, INTERFACE_CATALOGUE,
        KPI_DEFINITIONS, RISKS, ASSUMPTIONS, COMMERCIAL_PROPOSAL, IMPLEMENTATION_SCOPE,
        RESPONSIBILITY_MATRIX, ROADMAP, BUSINESS_BENEFITS, DATA_MAPPINGS)
      - Merged section header rows (full-width grouping across columns)
      - Data-type alignment (Left text, Center codes/status, Right numbers/financials)
      - Semantic status highlights (Critical, Warning, Success, RACI roles)
      - Strict Inter typography compliance
    
    Parameters:
      path: File path to PowerPoint presentation.
      archetype: One of the 12 canonical archetypes or 'CUSTOM_TABLE'.
      title: Optional override for slide title.
      subtitle: Optional override for slide subtitle.
      client_name: Enterprise client or initiative name.
      is_dark: False for Consulting Slate Light (recommended for dense tables), True for Navy Dark.
      custom_headers: Optional list of column header strings.
      custom_rows: Optional list of row lists or section headers (e.g., ['SECTION: Header', ...] or ['Val1', 'Val2']).
      custom_col_weights: Optional list of relative column width weights.
      callout_note: Optional architectural governance footnote.
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    if os.path.exists(path):
        prs = Presentation(path)
    else:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.500)

    # 1. Resolve Archetype
    clean_arch = archetype.upper().strip().replace(" ", "_").replace("-", "_")
    target_enum = getattr(TableArchetype, clean_arch, TableArchetype.CUSTOM_TABLE)

    # 2. Get baseline or build custom spec
    if target_enum != TableArchetype.CUSTOM_TABLE and not custom_headers:
        spec = EnterpriseTableFactory.get_table_spec(target_enum, client_name=client_name)
    else:
        spec = EnterpriseTableSpec(
            title=title or "Enterprise Specification Table",
            subtitle=subtitle or "Structured enterprise data matrix and governance register",
            client_name=client_name,
            archetype=target_enum,
            headers=custom_headers or ["ITEM ID", "CAPABILITY", "STATUS", "VALUE"],
            rows=custom_rows or [["SPEC-01", "Core Integration", "ACTIVE", "$100,000"]],
            col_weights=custom_col_weights,
            callout_note=callout_note
        )

    # Apply overrides
    if title:
        spec.title = title
    if subtitle:
        spec.subtitle = subtitle
    if custom_headers:
        spec.headers = custom_headers
    if custom_rows:
        spec.rows = custom_rows
    if custom_col_weights:
        spec.col_weights = custom_col_weights
    if callout_note is not None:
        spec.callout_note = callout_note
    spec.is_dark = is_dark
    spec.client_name = client_name

    # Render table slide
    EnterpriseTableComposer.compose_and_render(prs, spec)
    prs.save(path)

    return {
        "status": "success",
        "presentation_path": path,
        "total_slides": len(prs.slides),
        "title": spec.title,
        "archetype": target_enum.name,
        "total_columns": len(spec.headers),
        "total_rows": len(spec.rows),
        "theme": "Executive Navy (Dark)" if is_dark else "Consulting Slate (Light)",
        "message": f"Successfully rendered Enterprise Table '{spec.title}' to {path}"
    }



# -----------------------------------------------------------------------------
# Visual-Density & Whitespace Intelligence Tools
# -----------------------------------------------------------------------------
from design_system.density_intelligence import (
    VisualDensity,
    VisualDensityClassifier,
    DensityEvaluation,
    WhitespaceIntelligenceEngine,
    LowDensitySlideRenderer
)


@mcp.tool
def evaluate_visual_density(
    slide_title: str,
    primitive_hint: Optional[str] = None
) -> Dict[str, Any]:
    """
    Evaluates visual density tier and intentional whitespace allocation for a slide.
    
    Tiers:
      - LOW DENSITY (50% - 70% whitespace): Executive statements, architectural principles, key insights.
      - MEDIUM DENSITY (30% - 45% whitespace): Architecture diagrams, process flows, roadmaps.
      - HIGH DENSITY (15% - 25% whitespace): Executive dashboards, analytical tables, interface catalogues.
    
    Enforces anti-filler rules: A slide with one strong architecture diagram or one table is complete.
    """
    eval_res = WhitespaceIntelligenceEngine.evaluate(slide_title, primitive_hint or "")
    return {
        "slide_title": slide_title,
        "density_class": eval_res.density_class.name,
        "target_whitespace_percentage": f"{int(eval_res.target_whitespace_ratio * 100)}%",
        "content_importance": round(eval_res.content_importance, 2),
        "visual_complexity": round(eval_res.visual_complexity, 2),
        "readability_score": round(eval_res.readability_score, 2),
        "is_self_sufficient": eval_res.is_self_sufficient,
        "allow_auxiliary_cards": eval_res.allow_auxiliary_cards,
        "layout_recommendation": eval_res.layout_recommendation,
        "anti_filler_rules": eval_res.anti_filler_rules
    }


@mcp.tool
def render_low_density_slide(
    path: str,
    archetype: str,
    headline: str,
    supporting_text: Optional[str] = None,
    author_or_detail: Optional[str] = None,
    metric_value: Optional[str] = None,
    category_tag: Optional[str] = None,
    client_name: str = "Executive Leadership",
    is_dark: bool = True
) -> Dict[str, Any]:
    """
    Renders a high-impact low-density slide with intentional, generous whitespace.
    Zero decorative clutter, zero filler cards.
    
    Archetypes:
      - 'EXECUTIVE_STATEMENT': Large hero statement commanding the canvas (~65% whitespace).
      - 'ARCHITECTURAL_PRINCIPLE': Authoritative architectural rule or North Star with vertical accent bar (~60% whitespace).
      - 'HERO_KPI': Monumental hero metric (64pt) + single definitive takeaway sentence (~55% whitespace).
    
    Parameters:
      path: File path to PowerPoint presentation.
      archetype: 'EXECUTIVE_STATEMENT', 'ARCHITECTURAL_PRINCIPLE', or 'HERO_KPI'.
      headline: Main statement text, principle title, or KPI label.
      supporting_text: Supporting thesis rationale or takeaway conclusion sentence.
      author_or_detail: Attribution source or context caption.
      metric_value: Required for 'HERO_KPI' (e.g. '$14.2M', '99.98%', '48 Hrs').
      category_tag: Banner tag text.
      client_name: Enterprise client or initiative name.
      is_dark: True for Executive Navy, False for Consulting Slate.
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    if os.path.exists(path):
        prs = Presentation(path)
    else:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.500)

    clean_arch = archetype.upper().strip().replace(" ", "_")

    if clean_arch == "ARCHITECTURAL_PRINCIPLE":
        LowDensitySlideRenderer.render_architectural_principle(
            prs=prs,
            principle_title=headline,
            core_rule=supporting_text or headline,
            architectural_rationale=author_or_detail or "Underlying system constraint and ledger isolation rule.",
            category_tag=category_tag or "ARCHITECTURAL PRINCIPLE",
            client_name=client_name,
            is_dark=is_dark
        )
    elif clean_arch == "HERO_KPI":
        LowDensitySlideRenderer.render_hero_kpi_with_conclusion(
            prs=prs,
            metric_value=metric_value or "84.2%",
            metric_label=headline,
            conclusion_statement=supporting_text or "Definitive operational trajectory requiring board intervention.",
            context_detail=author_or_detail,
            category_tag=category_tag or "STRATEGIC TELEMETRY",
            client_name=client_name,
            is_dark=is_dark
        )
    else:  # EXECUTIVE_STATEMENT
        LowDensitySlideRenderer.render_executive_statement(
            prs=prs,
            statement=headline,
            supporting_thesis=supporting_text,
            author_or_source=author_or_detail,
            category_tag=category_tag or "STRATEGIC MANDATE",
            client_name=client_name,
            is_dark=is_dark
        )

    prs.save(path)

    return {
        "status": "success",
        "presentation_path": path,
        "total_slides": len(prs.slides),
        "archetype": clean_arch,
        "headline": headline,
        "whitespace_ratio": "55% - 65% (Generous Whitespace)",
        "theme": "Executive Navy (Dark)" if is_dark else "Consulting Slate (Light)",
        "message": f"Successfully rendered Low-Density Slide '{headline[:40]}...' to {path}"
    }



# -----------------------------------------------------------------------------
# Narrative Intelligence Tools
# -----------------------------------------------------------------------------
from design_system.narrative_intelligence import (
    NarrativeFramework,
    AudienceCognitiveObjective,
    NarrativeSlideIntent,
    NarrativeIntelligenceEngine
)


@mcp.tool
def list_narrative_frameworks() -> Dict[str, Any]:
    """
    Lists the 4 macro storytelling frameworks and their stages.
    
    Frameworks:
      1. TELL -> SHOW -> TELL (3 slides):
         - OPENING TELL: Why does this matter?
         - SHOW: What is actually happening?
         - CLOSING TELL: What does this mean for the customer?
      2. PRIDE & PURPOSE -> DESTINATION (6 slides):
         - Pride & Purpose -> Current Reality -> Opportunity -> Journey -> Changes -> Destination
      3. SOLUTION SELLING (4 slides):
         - WHY -> WHAT -> HOW -> BUSINESS VALUE
      4. EXECUTIVE DEMONSTRATION (6 slides):
         - Opening -> Business Outcomes -> Challenges -> Opportunities -> Demonstration -> Close
    """
    frameworks = [
        {
            "framework_id": "TELL_SHOW_TELL",
            "name": "Tell -> Show -> Tell (Triad Narrative)",
            "slide_count": 3,
            "stages": [
                "1. OPENING TELL: Strategic Mandate (Low Density)",
                "2. SHOW: System Architecture / Execution Topology (Medium Density)",
                "3. CLOSING TELL: Commercial Impact & Action Plan (High Density)"
            ]
        },
        {
            "framework_id": "PRIDE_PURPOSE_DESTINATION",
            "name": "Pride & Purpose -> Destination (Transformation Narrative)",
            "slide_count": 6,
            "stages": [
                "1. PRIDE & PURPOSE: Heritage & Mission (Low Density)",
                "2. CURRENT REALITY: Bottlenecks & Friction (High Density)",
                "3. OPPORTUNITY: Strategic Leap & ROI Target (Low Density)",
                "4. JOURNEY: Phased Implementation Roadmap (High Density)",
                "5. CHANGES: Architecture & Integration Topology (Medium Density)",
                "6. DESTINATION: Target Operating Model (Low Density)"
            ]
        },
        {
            "framework_id": "WHY_WHAT_HOW_VALUE",
            "name": "Solution Selling (Why -> What -> How -> Value)",
            "slide_count": 4,
            "stages": [
                "1. WHY: Compelling Reason to Act / COPQ Cockpit (High Density)",
                "2. WHAT: Clean-Core Architecture Blueprint (Medium Density)",
                "3. HOW: Governance RACI & Operational Execution (High Density)",
                "4. BUSINESS VALUE: Audited Financial Payback & EBITDA (High Density)"
            ]
        },
        {
            "framework_id": "EXECUTIVE_DEMONSTRATION",
            "name": "Executive Demonstration Narrative",
            "slide_count": 6,
            "stages": [
                "1. OPENING: Executive Context & Mission (Low Density)",
                "2. OUTCOMES: Target SLA Telemetry Cockpit (High Density)",
                "3. CHALLENGES: As-Is vs To-Be Architecture Friction (High Density)",
                "4. OPPORTUNITIES: Clean-Core Decoupling Principle (Low Density)",
                "5. DEMONSTRATION: Live IT/OT Architecture Flow (Medium Density)",
                "6. CLOSE: Milestone Commercial Proposal (High Density)"
            ]
        }
    ]
    return {
        "total_frameworks": len(frameworks),
        "frameworks": frameworks,
        "governing_principle": "Every slide has a reason for existing: What does the audience need to understand, believe, decide or do? Internal reasoning is strictly kept off the slide."
    }


@mcp.tool
def generate_narrative_presentation(
    path: str,
    framework: str = "TELL_SHOW_TELL",
    topic: str = "Clean-Core SAP S/4HANA & MES Integration",
    client_name: str = "Executive Leadership",
    custom_story_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generates a complete multi-slide narrative presentation following macro storytelling frameworks.
    
    Applies the cognitive intent framework:
      - 'What does the audience need to understand, believe, decide or do?'
      - Chooses visual representation and density tier per slide.
      - Never exposes internal reasoning on slide content.
    
    Parameters:
      path: File path to save PowerPoint presentation.
      framework: 'TELL_SHOW_TELL', 'PRIDE_PURPOSE_DESTINATION', 'WHY_WHAT_HOW_VALUE', or 'EXECUTIVE_DEMONSTRATION'.
      topic: The core transformation topic or initiative.
      client_name: Enterprise client or initiative banner.
      custom_story_data: Optional dictionary to customize story points.
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.500)

    clean_fw = framework.upper().strip().replace(" ", "_").replace("-", "_")
    target_enum = getattr(NarrativeFramework, clean_fw, NarrativeFramework.TELL_SHOW_TELL)

    # Render complete narrative arc
    intents = NarrativeIntelligenceEngine.render_narrative_deck(
        prs=prs,
        framework=target_enum,
        topic=topic,
        client_name=client_name,
        custom_data=custom_story_data
    )

    prs.save(path)

    stages_summary = []
    for idx, it in enumerate(intents, 1):
        stages_summary.append({
            "slide": idx,
            "stage": it.stage_id,
            "title": it.slide_title,
            "density": it.recommended_density.name,
            "primitive": it.recommended_primitive,
            "theme": "Dark" if it.is_dark else "Light"
        })

    return {
        "status": "success",
        "presentation_path": path,
        "total_slides": len(prs.slides),
        "framework": target_enum.name,
        "topic": topic,
        "client_name": client_name,
        "narrative_arc": stages_summary,
        "message": f"Successfully generated {len(prs.slides)}-slide narrative presentation '{topic}' to {path}"
    }



# -----------------------------------------------------------------------------
# Architecture Review Engine Tools
# -----------------------------------------------------------------------------
from design_system.architecture_review import (
    ArchitecturalLens,
    InquiryReviewResult,
    ArchitectureReviewScorecard,
    ArchitectureReviewEngine
)


@mcp.tool
def list_architecture_review_lenses() -> Dict[str, Any]:
    """
    Lists the 13 analytical review lenses and the 20 essential architectural inquiries.
    
    Lenses:
      1. Jeanne Ross        -> Enterprise Operating Model
      2. John Zachman       -> Enterprise Ontology / Structural Completeness
      3. Ivar Jacobson      -> Architectural Intent / System Behavior & Use-Cases
      4. Dennis Brandl      -> ISA-95 Manufacturing Hierarchy & IT/OT Integration
      5. Michael McClellan  -> MES Architecture / Manufacturing Execution
      6. Peter Senge        -> Systems Thinking / Feedback Loops / Delays
      7. Russell Ackoff     -> Interactive Systems / Purposeful Holistic Design
      8. Donella Meadows    -> Systems Structure / Leverage Points / Dynamics
      9. W. Edwards Deming  -> Quality / Variation / Continuous Process Improvement
      10. Eliyahu Goldratt  -> Constraints / Flow / Bottleneck Optimization (TOC)
      11. George Westerman  -> Digital Transformation / Organizational Capability
      12. Andrew McAfee     -> Digital Enterprise / Technology-Enabled Operating Model
      13. Erik Brynjolfsson -> AI / Digital Economics / Productivity & Complementary Assets
    """
    lenses = ArchitectureReviewEngine.list_all_lenses()
    inquiries = [
        {"q_num": q[0], "question": q[1], "primary_lens": q[2].name}
        for q in ArchitectureReviewEngine.INQUIRIES
    ]
    return {
        "total_lenses": len(lenses),
        "analytical_lenses": lenses,
        "total_inquiries": len(inquiries),
        "architectural_inquiries": inquiries,
        "governing_standard": "Run as an internal diagnostic review scorecard to auto-improve decks before customer delivery. Never exposed as slide content."
    }


@mcp.tool
def review_presentation_architecture(
    path: Optional[str] = None,
    text_corpus: Optional[str] = None
) -> Dict[str, Any]:
    """
    Runs a conceptual architecture review across the 13 lenses and 20 architectural inquiries.
    
    Generates an internal review scorecard assessing:
      - Operating model & system boundary clarity
      - ISA-95 manufacturing hierarchy & MES positioning
      - Feedback loops, constraints, and quality mechanisms
      - KPI decision support & data entity grounding
      - Governance, risk explicit articulation, and visual restraint
    
    Parameters:
      path: Optional PowerPoint file path to inspect and evaluate.
      text_corpus: Optional raw text summary or presentation transcript to evaluate.
    """
    prs = None
    if path and os.path.exists(path):
        prs = Presentation(path)

    scorecard = ArchitectureReviewEngine.review_presentation(prs=prs, aggregated_text=text_corpus)

    inquiry_summary = []
    for r in scorecard.inquiry_results:
        inquiry_summary.append({
            "inquiry_num": r.question_number,
            "question": r.question_text,
            "lens": r.primary_lens.name,
            "score": r.score,
            "status": r.status,
            "finding": r.finding,
            "remediation": r.remediation_applied
        })

    return {
        "status": "success",
        "presentation_evaluated": path or "Direct Text Corpus",
        "overall_health_score": scorecard.overall_health_score,
        "rating": scorecard.rating,
        "verdict": scorecard.architectural_verdict,
        "total_inquiries_evaluated": len(scorecard.inquiry_results),
        "inquiries_breakdown": inquiry_summary,
        "identified_weaknesses": scorecard.identified_weaknesses,
        "auto_improvements_applied": scorecard.auto_improvements_applied,
        "confidentiality_note": "Internal architectural diagnostic. Do NOT expose this review panel as content in client-facing presentations."
    }



# -----------------------------------------------------------------------------
# Presentation Quality Gate Tools
# -----------------------------------------------------------------------------
from design_system.quality_gate import (
    QualityStatus,
    QualityDimensionAudit,
    QualityGateReport,
    PresentationQualityGate
)


@mcp.tool
def audit_presentation_quality(path: str) -> Dict[str, Any]:
    """
    Evaluates a presentation file against the 9 Enterprise Quality Gate dimensions:
      1. Card Overuse (Flags if card usage exceeds 25%)
      2. Visual Variety (Ensures presence of diagrams, tables, cockpits, narratives)
      3. Architectural Quality (System boundaries, cylinders, interfaces, flow labels)
      4. Data Quality (Analytical trend charts and action tables in dashboards)
      5. Narrative Progression (Advancement without repetitive filler)
      6. Typography (100% Inter font family compliance across all runs)
      7. Layout & Whitespace (Bounds containment within 13.333" x 7.500" and safe margins)
      8. Editability (Native PowerPoint shapes, tables, charts)
      9. Executive Quality (Action titles, takeaway subtitles, multi-stakeholder clarity)
    
    Parameters:
      path: Path to the PowerPoint presentation file to audit.
    """
    if not os.path.exists(path):
        return {"status": "error", "message": f"Presentation file not found at: {path}"}

    prs = Presentation(path)
    report = PresentationQualityGate.audit_and_remediate(prs, auto_remediate=False)

    dimensions_summary = []
    for d in report.dimensions:
        dimensions_summary.append({
            "dimension": d.dimension_name,
            "score": d.score,
            "status": d.status,
            "observations": d.observations
        })

    return {
        "status": "success",
        "presentation_path": path,
        "overall_quality_score": report.overall_quality_score,
        "gate_status": report.status.name,
        "is_export_authorized": report.is_export_authorized,
        "typography_compliance": f"{report.typography_compliance_percent}%",
        "card_usage_ratio": f"{int(report.card_usage_ratio * 100)}%",
        "visual_diversity_score": report.visual_diversity_score,
        "verdict": report.executive_verdict,
        "dimensions_audited": dimensions_summary,
        "violations_detected": report.violations_detected
    }


@mcp.tool
def export_presentation_with_quality_gate(
    path: str,
    output_path: Optional[str] = None,
    auto_remediate: bool = True
) -> Dict[str, Any]:
    """
    Audits and automatically remediates presentation quality defects before final export.
    
    Auto-remediations:
      - Converts non-Inter fonts to strict Inter family tokens
      - Bounds and margin containment checks
      - Authorizes export if all quality gates pass
    
    Parameters:
      path: Path to source presentation file.
      output_path: Optional target path to save the remediated presentation (defaults to path).
      auto_remediate: If True, automatically fixes detected defects before saving.
    """
    if not os.path.exists(path):
        return {"status": "error", "message": f"Presentation file not found at: {path}"}

    prs = Presentation(path)
    report = PresentationQualityGate.audit_and_remediate(prs, auto_remediate=auto_remediate)

    dest_path = output_path or path
    if report.is_export_authorized or auto_remediate:
        prs.save(dest_path)

    return {
        "status": "success",
        "exported_path": dest_path,
        "overall_quality_score": report.overall_quality_score,
        "gate_status": report.status.name,
        "is_export_authorized": report.is_export_authorized,
        "typography_compliance": f"{report.typography_compliance_percent}%",
        "card_usage_ratio": f"{int(report.card_usage_ratio * 100)}%",
        "remediations_applied": report.auto_remediations_applied,
        "verdict": report.executive_verdict,
        "message": f"Quality gate successfully validated presentation at {dest_path}"
    }


# -----------------------------------------------------------------------------
# Semantic Scenario Presentation Engine Tool
# -----------------------------------------------------------------------------
from design_system.scenario_engine import ScenarioPresentationEngine


@mcp.tool
def generate_scenario_presentation(
    scenario_id: str,
    title: str,
    topic: str,
    client_name: str,
    requirements: List[str],
    output_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates an automated, visually diverse enterprise presentation for a specific scenario.
    
    Dynamically maps semantic requirements into distinct visual representations
    (architecture blueprints, process flows, genealogy trees, KPI strips, trend charts,
    Pareto charts, capacity/bottleneck views, commercial tables, milestone gates),
    enforces anti-monotony rhythm, and executes the Presentation Quality Gate.

    Parameters:
      scenario_id: Identifier for the presentation (e.g. 'scenario_1_sap_mes').
      title: Presentation title (e.g. 'SAP S/4HANA & MES Integration Architecture').
      topic: Subject matter / focus (e.g. 'SAP S/4HANA + MES + shop-floor integration architecture').
      client_name: Client or target enterprise name (e.g. 'Global Aerospace Manufacturing').
      requirements: List of desired semantic visual elements (e.g. ['enterprise architecture diagram', 'integration/data flow', ...]).
      output_path: Optional path to save the generated PPTX file.
    """
    res = ScenarioPresentationEngine.build_scenario_presentation(
        scenario_id=scenario_id,
        title=title,
        topic=topic,
        client_name=client_name,
        requirements=requirements,
        output_path=output_path
    )

    return {
        "status": "success",
        "scenario_id": res.scenario_id,
        "presentation_title": res.scenario_title,
        "output_path": res.output_path,
        "slide_count": res.slide_count,
        "visual_forms_chosen": res.visual_forms_chosen,
        "primitives_used": res.primitives_used,
        "is_export_authorized": res.is_export_authorized,
        "overall_quality_score": res.quality_report.overall_quality_score,
        "gate_status": res.quality_report.status.name,
        "typography_compliance": f"{res.quality_report.typography_compliance_percent}%",
        "diversity_score": f"{res.diversity_score}%",
        "verdict": res.quality_report.executive_verdict
    }


# -----------------------------------------------------------------------------
# Transformation & Process Intelligence MCP Tools (Step 15)
# -----------------------------------------------------------------------------
from design_system.transformation_semantic import (
    TransformationRelationType,
    ProcessNodeType,
    ProcessNode,
    ProcessBranch,
    ProcessFlowModel,
    SwimlaneLane,
    SwimlaneStep,
    SwimlaneHandoff,
    SwimlaneDiagramModel,
    CurrentStateSnapshot,
    TransformationIntervention,
    FutureStateVision,
    TransformationBridgeModel,
    MaturityDimensionScore,
    MaturityStaircaseLevel,
    MaturityAssessmentModel,
    ClosedLoopStage,
    ClosedLoopManufacturingModel,
    TransformationSemanticInferrer
)
from design_system.process_flow_engine import ProcessFlowComposer
from design_system.swimlane_engine import SwimlaneDiagramComposer
from design_system.transformation_engine import TransformationBridgeComposer
from design_system.maturity_engine import MaturityAssessmentComposer
from design_system.primitives import HeaderPrimitive, FooterPrimitive
from design_system.spacing import Margins, SpacingScale
from design_system.color import ExecutiveNavyTheme, ConsultingSlateTheme


@mcp.tool
def render_process_flow_diagram(
    path: str,
    title: str = "SAP S/4HANA to MES Production Execution & Quality Clearance",
    subtitle: Optional[str] = "Sequential order-to-dispatch flow with quality gate and rework loopback",
    client_name: str = "Enterprise Manufacturing",
    is_dark: bool = False,
    steps_data: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Renders an enterprise process flow with decision diamonds, branching paths,
    and rework/feedback loops into a presentation slide.
    
    Guarantees:
      - Inter-only typography
      - Real geometric shapes (not disconnected card boxes)
      - Explicit MSO_SHAPE.DIAMOND for quality/decision points
      - Directional connector arrows and branch condition badges
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    prs = Presentation(path) if os.path.exists(path) else Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.500)

    theme = ExecutiveNavyTheme if is_dark else ConsultingSlateTheme
    blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
    slide = prs.slides.add_slide(blank_layout)

    # Background
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.500))
    bg.fill.solid()
    bg.fill.fore_color.rgb = theme.canvas
    bg.line.fill.background()

    # Header & Footer
    HeaderPrimitive.render(slide, "PROCESS ARCHITECTURE", title, subtitle, theme)
    FooterPrimitive.render(slide, len(prs.slides), len(prs.slides), f"{client_name} • Operational Process Architecture", theme)

    # Build or parse nodes
    if steps_data:
        nodes = []
        for s in steps_data:
            nodes.append(ProcessNode(
                id=s.get("id", f"node_{len(nodes)}"),
                label=s.get("label", "Process Step"),
                role_lane=s.get("role_lane", "Operations"),
                system_tag=s.get("system_tag"),
                action_detail=s.get("action_detail"),
                poka_yoke=s.get("poka_yoke"),
                is_decision=s.get("is_decision", False)
            ))
    else:
        nodes = [
            ProcessNode("n1", "Demand & Sales Order", role_lane="Customer Demand", system_tag="SAP SD"),
            ProcessNode("n2", "Production Order & MRP", role_lane="SAP Core", system_tag="PP Order 100482"),
            ProcessNode("n3", "MES Dispatch & Setup", role_lane="MES Operations", system_tag="Digital Dispatch"),
            ProcessNode("n4", "Machine Execution", role_lane="Shop Floor OT", system_tag="CNC Work Center"),
            ProcessNode("n5", "Quality Gate & SPC", role_lane="Quality Assurance", system_tag="Vision / CMM", is_decision=True),
            ProcessNode("n6", "Confirmation & Ledger", role_lane="SAP Finance", system_tag="CO11N / 101 GR"),
            ProcessNode("n7", "Finished Goods Dispatch", role_lane="Logistics", system_tag="Outbound Delivery")
        ]

    flow_model = ProcessFlowModel(
        title=title,
        nodes=nodes,
        branches=[],
        subtitle=subtitle
    )

    ProcessFlowComposer.render_branching_process(
        slide=slide,
        left=Margins.left,
        top=SpacingScale.CONTENT_TOP,
        width=Margins().usable_width,
        height=SpacingScale.CONTENT_HEIGHT,
        flow_model=flow_model,
        theme=theme
    )

    prs.save(path)
    return {
        "status": "success",
        "path": path,
        "slide_index": len(prs.slides) - 1,
        "nodes_rendered": len(nodes),
        "visual_type": "PROCESS_FLOW_DIAGRAM"
    }


@mcp.tool
def render_swimlane_diagram(
    path: str,
    title: str = "SAP S/4HANA & MES Cross-Functional Operational Swimlane",
    subtitle: Optional[str] = "Multi-tier transactional handoffs and Poka-Yoke interlocks across 5 enterprise lanes",
    client_name: str = "Enterprise Manufacturing",
    is_dark: bool = False
) -> Dict[str, Any]:
    """
    Renders an enterprise cross-functional swimlane diagram with horizontal lane bands,
    step placements, and cross-lane handoffs into a presentation slide.
    
    Lanes:
      - CUSTOMER
      - SAP S/4HANA (ERP Core)
      - MES (Manufacturing Execution)
      - SHOP FLOOR / OT (Machine & Operator)
      - QUALITY ASSURANCE
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    prs = Presentation(path) if os.path.exists(path) else Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.500)

    theme = ExecutiveNavyTheme if is_dark else ConsultingSlateTheme
    blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
    slide = prs.slides.add_slide(blank_layout)

    # Background
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.500))
    bg.fill.solid()
    bg.fill.fore_color.rgb = theme.canvas
    bg.line.fill.background()

    # Header & Footer
    HeaderPrimitive.render(slide, "CROSS-FUNCTIONAL SWIMLANE", title, subtitle, theme)
    FooterPrimitive.render(slide, len(prs.slides), len(prs.slides), f"{client_name} • Operational Swimlane Architecture", theme)

    lanes = [
        SwimlaneLane("lane_cust", "Customer Demand", "External Partner", 1),
        SwimlaneLane("lane_sap", "SAP S/4HANA", "System of Record", 2),
        SwimlaneLane("lane_mes", "MES Operations", "Execution Core", 3),
        SwimlaneLane("lane_shop", "Shop Floor / OT", "Edge Physical Layer", 4),
        SwimlaneLane("lane_qm", "Quality Assurance", "Compliance Interlock", 5)
    ]

    steps = [
        SwimlaneStep("s1", "lane_cust", "Demand Forecast / EDI", 1, "Sales Demand Signal", system_badge="EDI 850"),
        SwimlaneStep("s2", "lane_sap", "Sales & Production Order", 2, "MRP Planning Run", system_badge="S/4HANA PP"),
        SwimlaneStep("s3", "lane_mes", "Dispatch & Work Queue", 3, "Operation Scheduling", system_badge="MES MOM"),
        SwimlaneStep("s4", "lane_shop", "CNC Machining & Setup", 4, "Physical Execution", system_badge="PLC / OPC UA"),
        SwimlaneStep("s5", "lane_shop", "Material Consumption", 5, "Batch Component Binding", system_badge="261 Movement"),
        SwimlaneStep("s6", "lane_qm", "Optical Inspection Gate", 6, "SPC Tolerance Validation", is_decision=True, system_badge="CMM Gauge"),
        SwimlaneStep("s7", "lane_sap", "Confirmation & Ledger", 7, "CO11N & 101 Goods Receipt", system_badge="ACDOCA Post")
    ]

    handoffs = [
        SwimlaneHandoff("s1", "s2", "Sales Order", "B2B EDI"),
        SwimlaneHandoff("s2", "s3", "Production Order", "BAPI / OData"),
        SwimlaneHandoff("s3", "s4", "Dispatch Job", "OPC-UA / MQTT"),
        SwimlaneHandoff("s4", "s5", "As-Built Log", "Unit Traveler"),
        SwimlaneHandoff("s5", "s6", "Inspection Trigger", "Quality Call"),
        SwimlaneHandoff("s6", "s7", "Clearance GR", "101 Receipt")
    ]

    model = SwimlaneDiagramModel(
        title=title,
        lanes=lanes,
        steps=steps,
        handoffs=handoffs,
        subtitle=subtitle
    )

    SwimlaneDiagramComposer.render(
        slide=slide,
        left=Margins.left,
        top=SpacingScale.CONTENT_TOP,
        width=Margins().usable_width,
        height=SpacingScale.CONTENT_HEIGHT,
        model=model,
        theme=theme
    )

    prs.save(path)
    return {
        "status": "success",
        "path": path,
        "slide_index": len(prs.slides) - 1,
        "lanes_count": len(lanes),
        "steps_count": len(steps),
        "visual_type": "SWIMLANE_DIAGRAM"
    }


@mcp.tool
def render_transformation_bridge(
    path: str,
    title: str = "Enterprise Transformation Blueprint: Current State to Target Operating Model",
    subtitle: Optional[str] = "Bridging legacy operational friction through S/4HANA clean-core and MES execution enablers",
    client_name: str = "Enterprise Manufacturing",
    is_dark: bool = False
) -> Dict[str, Any]:
    """
    Renders an enterprise Current State -> Intervention -> Future State transformation bridge
    with baseline KPIs, strategic enablers, and target business outcomes.
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    prs = Presentation(path) if os.path.exists(path) else Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.500)

    theme = ExecutiveNavyTheme if is_dark else ConsultingSlateTheme
    blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
    slide = prs.slides.add_slide(blank_layout)

    # Background
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.500))
    bg.fill.solid()
    bg.fill.fore_color.rgb = theme.canvas
    bg.line.fill.background()

    HeaderPrimitive.render(slide, "TRANSFORMATION BLUEPRINT", title, subtitle, theme)
    FooterPrimitive.render(slide, len(prs.slides), len(prs.slides), f"{client_name} • Transformation Advisory", theme)

    model = TransformationBridgeModel(
        title=title,
        current_state=CurrentStateSnapshot(
            title="CURRENT STATE (Baseline)",
            pain_points=[
                "Fragmented master data & BOM mismatches",
                "Manual paper travelers & dispatch clipboards",
                "Disconnected quality logs tracked in Excel",
                "Delayed inventory confirmation (2-3 day lag)"
            ],
            baseline_metrics=[
                ("WIP Latency", "4.8 Days"),
                ("Scrap Rate", "4.2%"),
                ("OTIF Delivery", "81.4%")
            ]
        ),
        intervention=TransformationIntervention(
            title="TRANSFORMATION ENABLERS",
            initiatives=[
                "SAP S/4HANA Clean-Core Integration",
                "MES Digital Dispatch & Real-Time Tracking",
                "Automated Closed-Loop Quality Interlocks",
                "Unified Industrial Data Fabric & BTP Mesh"
            ],
            enablers=[
                "Air-gapped edge buffering",
                "Deterministic PLC connectors",
                "Zero custom Z-tables in ERP"
            ]
        ),
        future_state=FutureStateVision(
            title="FUTURE OPERATING MODEL",
            transformed_capabilities=[
                "Synchronized MRP-to-machine dispatch",
                "Full serial & batch genealogy trace",
                "Predictive quality interlocks at station",
                "Sub-second financial ledger postings"
            ],
            target_outcomes=[
                ("WIP Latency", "1.2 Days (-75%)"),
                ("Scrap Rate", "0.8% (-81%)"),
                ("OTIF Delivery", "97.5% (+16 pts)")
            ]
        ),
        subtitle=subtitle,
        timeframe="12–18 Month Execution Horizon"
    )

    TransformationBridgeComposer.render_bridge(
        slide=slide,
        left=Margins.left,
        top=SpacingScale.CONTENT_TOP,
        width=Margins().usable_width,
        height=SpacingScale.CONTENT_HEIGHT,
        model=model,
        theme=theme
    )

    prs.save(path)
    return {
        "status": "success",
        "path": path,
        "slide_index": len(prs.slides) - 1,
        "visual_type": "TRANSFORMATION_BRIDGE_DIAGRAM"
    }


@mcp.tool
def render_maturity_assessment(
    path: str,
    title: str = "Digital Transformation Maturity Assessment & Gaps",
    subtitle: Optional[str] = "5-Level capability staircase and prioritized dimension gap scorecard",
    client_name: str = "Enterprise Manufacturing",
    overall_current: float = 2.4,
    overall_target: float = 4.2,
    is_dark: bool = False
) -> Dict[str, Any]:
    """
    Renders an enterprise 5-level maturity staircase and dimension scorecard:
    Score -> Gap -> Recommendation consulting layout.
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    prs = Presentation(path) if os.path.exists(path) else Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.500)

    theme = ExecutiveNavyTheme if is_dark else ConsultingSlateTheme
    blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
    slide = prs.slides.add_slide(blank_layout)

    # Background
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.500))
    bg.fill.solid()
    bg.fill.fore_color.rgb = theme.canvas
    bg.line.fill.background()

    HeaderPrimitive.render(slide, "MATURITY ASSESSMENT", title, subtitle, theme)
    FooterPrimitive.render(slide, len(prs.slides), len(prs.slides), f"{client_name} • Operational Maturity Audit", theme)

    dimensions = [
        MaturityDimensionScore("Process & Execution", 2.1, 4.3, "P1", "Paper travel cards & manual dispatch", "Deploy MES automated dispatch & digital traveler"),
        MaturityDimensionScore("Data & Genealogy", 2.3, 4.5, "P1", "Missing component-to-serial batch linkage", "Automated barcode & OPC-UA genealogy binding"),
        MaturityDimensionScore("SAP Clean Core", 2.6, 4.2, "P2", "Excess custom Z-tables blocking cloud upgrade", "Migrate custom code to BTP event mesh"),
        MaturityDimensionScore("Quality & Rework", 2.2, 4.0, "P1", "Delayed defect logging & missing CAPA loops", "Closed-loop digital inspection interlocks"),
        MaturityDimensionScore("Governance & RACI", 2.8, 4.0, "P2", "Ambiguous IT/OT boundary ownership", "Formalize unified IT/OT operating charter")
    ]

    model = MaturityAssessmentModel(
        title=title,
        overall_current_score=overall_current,
        overall_target_score=overall_target,
        dimensions=dimensions,
        subtitle=subtitle
    )

    MaturityAssessmentComposer.render_staircase_scorecard(
        slide=slide,
        left=Margins.left,
        top=SpacingScale.CONTENT_TOP,
        width=Margins().usable_width,
        height=SpacingScale.CONTENT_HEIGHT,
        model=model,
        theme=theme
    )

    prs.save(path)
    return {
        "status": "success",
        "path": path,
        "slide_index": len(prs.slides) - 1,
        "overall_current": overall_current,
        "overall_target": overall_target,
        "visual_type": "MATURITY_STAIRCASE_SCORECARD"
    }


@mcp.tool
def render_closed_loop_manufacturing(
    path: str,
    title: str = "Physical-to-Digital Closed-Loop Manufacturing Architecture",
    subtitle: Optional[str] = "Continuous cyber-physical feedback from machine sensors through S/4HANA intelligence",
    client_name: str = "Enterprise Manufacturing",
    is_dark: bool = True
) -> Dict[str, Any]:
    """
    Renders a circular, closed-loop manufacturing architecture:
    Physical World -> Digital Capture -> Contextualization -> Intelligence -> Decision -> Action -> Physical World.
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    prs = Presentation(path) if os.path.exists(path) else Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.500)

    theme = ExecutiveNavyTheme if is_dark else ConsultingSlateTheme
    blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
    slide = prs.slides.add_slide(blank_layout)

    # Background
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.500))
    bg.fill.solid()
    bg.fill.fore_color.rgb = theme.canvas
    bg.line.fill.background()

    HeaderPrimitive.render(slide, "CLOSED-LOOP MANUFACTURING", title, subtitle, theme)
    FooterPrimitive.render(slide, len(prs.slides), len(prs.slides), f"{client_name} • Cyber-Physical Architecture", theme)

    stages = [
        ClosedLoopStage(1, "Physical World", ["CNC Machine", "Operator Tooling", "Physical Sensors"], ["Vibration & Current", "Spindle Speed"]),
        ClosedLoopStage(2, "Digital Capture", ["Edge Industrial Gateway", "OPC UA Collector"], ["Raw Telemetry Stream", "Time-Series Logs"]),
        ClosedLoopStage(3, "Contextualization", ["MES MOM Engine", "Unit Genealogy Traveler"], ["Order #100482 Context", "Lot & Serial Binding"]),
        ClosedLoopStage(4, "Enterprise Intelligence", ["SAP S/4HANA", "Predictive AI / SPC"], ["ACDOCA Ledger Postings", "Deviation Anomaly"]),
        ClosedLoopStage(5, "Decision Engine", ["Autonomous Control Logic", "Supervisor Approval"], ["Tool Offset Adjustment", "Hold/Release Clearance"]),
        ClosedLoopStage(6, "Directed Action", ["PLC Actuator", "Operator Terminal"], ["Automated Parameter Update", "Closed-Loop Physical Execution"])
    ]

    model = ClosedLoopManufacturingModel(
        title=title,
        stages=stages,
        loop_closed_summary="Sub-second closed-loop telemetry updates machine tool offsets directly before tolerance drift causes non-conformance.",
        subtitle=subtitle
    )

    ProcessFlowComposer.render_closed_loop_manufacturing(
        slide=slide,
        left=Margins.left,
        top=SpacingScale.CONTENT_TOP,
        width=Margins().usable_width,
        height=SpacingScale.CONTENT_HEIGHT,
        model=model,
        theme=theme
    )

    prs.save(path)
    return {
        "status": "success",
        "path": path,
        "slide_index": len(prs.slides) - 1,
        "stages_count": len(stages),
        "visual_type": "CLOSED_LOOP_DIAGRAM"
    }


if __name__ == "__main__":
    mcp.run()



