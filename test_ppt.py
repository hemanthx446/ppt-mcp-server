import os
import json
from ppt_mcp_server import (
    create_presentation,
    add_slide,
    add_text,
    add_bullet_points,
    add_shape,
    add_table,
    get_presentation_info,
    search_replace_text,
    delete_slide
)

def test_flow():
    test_file = "test_output.pptx"
    
    # 1. Clean up old test file
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"Removed existing {test_file}")
        
    # 2. Create Presentation
    print("\n--- Testing create_presentation ---")
    res = create_presentation(test_file)
    print(res)
    assert os.path.exists(test_file), "Presentation file should be created"
    
    # 3. Add Slide (Title slide)
    print("\n--- Testing add_slide (Title) ---")
    res = add_slide(test_file, layout_idx=0)
    print(res)
    
    # Add slide title text
    res = add_text(
        test_file,
        slide_idx=0,
        text="Welcome to PowerPoint MCP",
        left_in=1.0,
        top_in=2.0,
        width_in=8.0,
        height_in=1.5,
        font_name="Arial",
        font_size_pt=40,
        bold=True,
        color_hex="003366",
        align="center"
    )
    print(res)
    
    # 4. Add Slide 2 (Blank slide for Content)
    print("\n--- Testing add_slide (Blank) ---")
    res = add_slide(test_file, layout_idx=6)
    print(res)
    
    # Add bullet points
    print("\n--- Testing add_bullet_points ---")
    bullets = [
        "First major point about the server",
        "Second important aspect of FastMCP",
        "Third slide detailing shapes and layouts"
    ]
    res = add_bullet_points(
        test_file,
        slide_idx=1,
        points=bullets,
        left_in=0.5,
        top_in=1.0,
        width_in=5.0,
        height_in=3.0,
        font_size_pt=18,
        color_hex="333333"
    )
    print(res)
    
    # Add shape (Rectangle)
    print("\n--- Testing add_shape (Rectangle) ---")
    res = add_shape(
        test_file,
        slide_idx=1,
        shape_type="rectangle",
        left_in=6.0,
        top_in=1.0,
        width_in=3.0,
        height_in=2.0,
        fill_color_hex="E6F2FF",
        line_color_hex="0066CC",
        line_width_pt=2.0
    )
    print(res)
    
    # Add table
    print("\n--- Testing add_table ---")
    table_data = [
        ["Header A", "Header B"],
        ["Value 1", "Value 2"],
        ["Value 3", "Value 4"]
    ]
    res = add_table(
        test_file,
        slide_idx=1,
        rows=3,
        cols=2,
        left_in=0.5,
        top_in=4.5,
        width_in=5.0,
        height_in=2.0,
        data=table_data
    )
    print(res)
    
    # 5. Fetch Info before search/replace
    print("\n--- Testing get_presentation_info ---")
    info = get_presentation_info(test_file)
    print(json.dumps(info, indent=2))
    
    # Verify slide counts and basic data
    assert info["slide_count"] == 2
    assert len(info["slides"][1]["shapes"]) >= 3 # bullets, shape, table
    
    # 6. Search and Replace
    print("\n--- Testing search_replace_text ---")
    res = search_replace_text(test_file, search_str="Value 2", replace_str="Updated Value 2")
    print(res)
    
    # Fetch Info again to check replacement
    info2 = get_presentation_info(test_file)
    shapes_s2 = info2["slides"][1]["shapes"]
    table_found = False
    for shape in shapes_s2:
        if "table" in shape:
            table_found = True
            assert shape["table"][1][1] == "Updated Value 2", "Text replacement in table cell failed!"
            print("Verified: Text replacement in table cell succeeded!")
    assert table_found, "Table shape not found in slide 2"
    
    # 7. Add slide and delete it
    print("\n--- Testing delete_slide ---")
    add_slide(test_file, layout_idx=6)
    info_before_del = get_presentation_info(test_file)
    assert info_before_del["slide_count"] == 3
    
    res = delete_slide(test_file, slide_idx=2)
    print(res)
    
    info_after_del = get_presentation_info(test_file)
    assert info_after_del["slide_count"] == 2, "Slide deletion failed"
    print("Verified: Slide deletion succeeded!")
    
    print("\nALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_flow()
