import os
from typing import List, Optional, Dict, Any
from fastmcp import FastMCP
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

# Initialize FastMCP Server
mcp = FastMCP("PowerPoint-MCP-Server")

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

if __name__ == "__main__":
    mcp.run()
