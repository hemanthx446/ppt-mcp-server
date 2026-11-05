# PowerPoint Model Context Protocol (MCP) Server

A Python-based Model Context Protocol (MCP) server that provides tools for creating, inspecting, and editing PowerPoint presentations using `fastmcp` and `python-pptx`.

## Prerequisites

- Windows OS
- Python 3.12 (already installed in `C:\Users\Lumbini_User\AppData\Local\Programs\Python\Python312`)
- Local virtual environment `.venv` with installed dependencies.

## Exposed Tools

The server registers and runs the following tools:

1. **`create_presentation(path: str)`**: Creates a new, blank PowerPoint presentation at the specified path.
2. **`add_slide(path: str, layout_idx: int = 6)`**: Adds a new slide to the presentation at `path` using layout template indices (e.g. `6` for blank).
3. **`add_text(path, slide_idx, text, left_in, top_in, width_in, height_in, font_name, font_size_pt, bold, italic, color_hex, align)`**: Adds a textbox with custom formatted text.
4. **`add_bullet_points(path, slide_idx, points, left_in, top_in, width_in, height_in, font_name, font_size_pt, color_hex)`**: Adds a formatted list of bullet points.
5. **`add_shape(path, slide_idx, shape_type, left_in, top_in, width_in, height_in, fill_color_hex, line_color_hex, line_width_pt)`**: Inserts geometric shapes like rectangles, ellipses, triangles, etc.
6. **`add_picture(path, slide_idx, image_path, left_in, top_in, width_in, height_in)`**: Inserts a local image.
7. **`add_table(path, slide_idx, rows, cols, left_in, top_in, width_in, height_in, data)`**: Inserts and populates tables.
8. **`get_presentation_info(path)`**: Returns detailed structures, shape locations, texts, and tables of all slides.
9. **`search_replace_text(path, search_str, replace_str)`**: Performs full-presentation find-and-replace across textboxes, shapes, and tables.
10. **`delete_slide(path, slide_idx)`**: Deletes the slide at the specified index.

## MCP Client Configuration

To register this server with an MCP host (such as Claude Desktop or cursor), add the following entry to your host configuration file:

```json
{
  "mcpServers": {
    "powerpoint": {
      "command": "c:\\Users\\Lumbini_User\\Desktop\\PPT\\.venv\\Scripts\\python.exe",
      "args": [
        "c:\\Users\\Lumbini_User\\Desktop\\PPT\\ppt_mcp_server.py"
      ],
      "env": {}
    }
  }
}
```

## Local Development & Testing

1. Active the virtual environment:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
2. Run the server directly:
   ```bash
   python ppt_mcp_server.py
   ```
