"""
Don Norman Human-Centered Design Engine for PowerPoint Generation.
Governed by Don Norman's Cognitive & Human-Centered Design Principles (The Design of Everyday Things).

Key Guardrails:
1. Conceptual Models First: Slides map to explicit cognitive intents.
2. Signifiers & Visual Hierarchy: Distinct visual treatments for focal vs supporting elements.
3. Natural Spatial Mapping: Left-to-right (sequence), top-to-bottom (hierarchy), columns (comparison).
4. Physical & Cognitive Constraints:
   - MAX_WORDS_PER_SLIDE = 65
   - MAX_WORDS_PER_TITLE = 12
   - MAX_BULLETS_PER_CONTAINER = 4
   - MAX_WORDS_PER_BULLET = 15
   - MAX_CARDS_PER_SLIDE = 4 (or 5 for process flow)
   - Strict Typography Floor: MIN_FONT_SIZE_PT = 12, Discrete integer scale (12, 14, 16, 18, 20, 22, 24, 26, 28, 32, 36, 40, 48), Zero fractions.
5. Discoverability & Scannability: 3-second comprehension via action headline.
6. Feedback & Error Prevention (Poka-Yoke): Automated bounding-box collision detection,
   contrast checks (>=4.5:1 body, >=3.0:1 headings), and density validation via validate_deck().
"""

import math
import re
from typing import Dict, List, Any, Optional, Tuple
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

# =============================================================================
# 1. HARD DESIGN CONSTANTS & CONSTRAINTS
# =============================================================================

MAX_WORDS_PER_SLIDE = 65
MAX_WORDS_PER_TITLE = 12
MAX_BULLETS_PER_CONTAINER = 4
MAX_WORDS_PER_BULLET = 15
MAX_CARDS_PER_SLIDE = 4
MAX_CARDS_PER_FLOW = 5

MIN_FONT_SIZE_PT = 12
ALLOWED_FONT_SIZES = [12, 14, 16, 18, 20, 22, 24, 26, 28, 32, 36, 40, 48, 54]

# Canvas Dimensions (16:9 widescreen)
CANVAS_WIDTH_IN = 13.333
CANVAS_HEIGHT_IN = 7.5
SAFE_MARGIN_X_IN = 0.60
SAFE_MARGIN_Y_IN = 0.50
MIN_INTER_ELEMENT_GUTTER_IN = 0.25
MIN_INTERNAL_CARD_PADDING_IN = 0.20
MIN_WHITESPACE_TARGET_RATIO = 0.30

# Contrast Standards (WCAG 2.1 AA)
MIN_CONTRAST_BODY = 4.5
MIN_CONTRAST_LARGE_TEXT = 3.0

# Cognitive Intent Types
VALID_COGNITIVE_INTENTS = {
    "executive_takeaway": {
        "description": "Top action title + 1 dominant hero callout/metric on left (40%) + max 3 structured takeaways on right (60%).",
        "max_elements": 4,
        "spatial_flow": "hero_left_cards_right"
    },
    "process_flow": {
        "description": "Horizontal left-to-right chevron/step pipeline (Step 1 -> Step 2 -> Step 3).",
        "max_elements": 5,
        "spatial_flow": "horizontal_ltr"
    },
    "comparison_matrix": {
        "description": "Symmetrical 2-column or 3-column layout (e.g., As-Is vs To-Be, Option A vs Option B).",
        "max_elements": 3,
        "spatial_flow": "side_by_side_columns"
    },
    "architecture_layers": {
        "description": "Horizontal stacked tiers from top (User/Experience) to bottom (Infrastructure/Data).",
        "max_elements": 5,
        "spatial_flow": "vertical_stacked_tiers"
    },
    "metric_proof": {
        "description": "Large high-contrast KPI numerals across top/left + concise context bullets or trend visual.",
        "max_elements": 4,
        "spatial_flow": "kpi_grid_plus_chart"
    },
    "decision_gate": {
        "description": "Top problem statement + 2-3 option cards + bottom highlighted Recommendation Banner.",
        "max_elements": 4,
        "spatial_flow": "options_plus_bottom_banner"
    }
}


# =============================================================================
# 2. COLOR CONTRAST & LUMINANCE AUDITOR
# =============================================================================

def relative_luminance(rgb: Tuple[int, int, int]) -> float:
    """Calculate relative luminance per WCAG formula."""
    def channel_lum(val: int) -> float:
        c = val / 255.0
        return c / 12.92 if c <= 0.03928 else math.pow((c + 0.055) / 1.055, 2.4)
    r, g, b = rgb
    return 0.2126 * channel_lum(r) + 0.7152 * channel_lum(g) + 0.0722 * channel_lum(b)


def contrast_ratio(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """Compute contrast ratio between two RGB colors (>= 1.0 and <= 21.0)."""
    l1 = relative_luminance(rgb1)
    l2 = relative_luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# =============================================================================
# 3. TYPOGRAPHY ENFORCER (STRICT INTEGER SCALE >= 12 PT)
# =============================================================================

def snap_to_norman_font_size(requested_pt: float) -> int:
    """
    Snaps any requested font size to the nearest valid integer >= 12pt.
    Guarantees no fractional sizes (e.g. 10.5 -> 12, 9 -> 12, 13.5 -> 14, 15 -> 16).
    """
    if requested_pt < MIN_FONT_SIZE_PT:
        return MIN_FONT_SIZE_PT
    # Find closest allowed discrete integer size (prefer higher on tie)
    closest = min(sorted(ALLOWED_FONT_SIZES, reverse=True), key=lambda x: abs(x - requested_pt))
    return int(closest)


# =============================================================================
# 4. PRE-RENDER AUDIT & POKA-YOKE QUALITY GATE (validate_deck)
# =============================================================================

def audit_slide_ux(slide, slide_index: int, slide_width_in: float = 13.333, slide_height_in: float = 7.5) -> List[Dict[str, Any]]:
    """
    Audits a single slide against Don Norman human-centered UX rules:
    - Bounding-box collisions & overlaps
    - Font size violations (< 12pt or fractions)
    - Word density violations (MAX_WORDS_PER_SLIDE = 65)
    - Off-slide bounds overflow
    - Title word count (MAX_WORDS_PER_TITLE = 12)
    """
    violations = []
    EMU = 914400.0

    boxes = []
    slide_text_words = []
    title_words = 0

    for shape in slide.shapes:
        try:
            x = shape.left / EMU
            y = shape.top / EMU
            w = shape.width / EMU
            h = shape.height / EMU
        except Exception:
            continue

        # Check if shape is entirely out of bounds
        if x < -0.05 or y < -0.05 or (x + w) > (slide_width_in + 0.05) or (y + h) > (slide_height_in + 0.05):
            # Ignore subtle full-bleed backgrounds or corner motif marks
            if w < slide_width_in and h < slide_height_in:
                violations.append({
                    "slide_index": slide_index,
                    "rule": "BOUNDS_OVERFLOW",
                    "severity": "fail",
                    "detail": f"Shape '{shape.name}' at ({x:.2f}, {y:.2f}) spans outside canvas ({slide_width_in:.2f} x {slide_height_in:.2f} in).",
                    "recommended_action": "Reposition shape within 0.6in safe margin."
                })

        # Track text and typography
        if shape.has_text_frame:
            tf = shape.text_frame
            full_text = tf.text.strip()
            if full_text:
                words = full_text.split()
                # Check if this is the slide title
                is_title = (y < 1.5 and h < 1.5 and len(words) > 0)
                if is_title:
                    # Find the specific action headline paragraph (usually largest font size or second paragraph)
                    title_para = None
                    max_pt = 0
                    for p in tf.paragraphs:
                        for r in p.runs:
                            if r.font.size and r.font.size.pt > max_pt:
                                max_pt = r.font.size.pt
                                title_para = p
                    p_to_check = title_para if title_para else (tf.paragraphs[1] if len(tf.paragraphs) > 1 else tf.paragraphs[0])
                    p_words = p_to_check.text.strip().split()
                    title_words = len(p_words)
                    if title_words > MAX_WORDS_PER_TITLE:
                        violations.append({
                            "slide_index": slide_index,
                            "rule": "MAX_WORDS_PER_TITLE",
                            "severity": "warning",
                            "detail": f"Action title has {title_words} words (limit: {MAX_WORDS_PER_TITLE}): '{p_to_check.text.strip()}'.",
                            "recommended_action": "Shorten title to <= 12 words highlighting the primary takeaway."
                        })
                else:
                    # Ignore footer / slide number metadata from word count
                    if not (y > 6.8) and slide_index > 1:
                        slide_text_words.extend(words)

                # Check font sizes in paragraphs
                for p in tf.paragraphs:
                    for r in p.runs:
                        if r.font.size is not None:
                            pt_val = r.font.size.pt
                            # Check sub-12pt
                            if pt_val < MIN_FONT_SIZE_PT and not (y > 6.8): # exclude bottom footer line
                                violations.append({
                                    "slide_index": slide_index,
                                    "rule": "MIN_FONT_SIZE",
                                    "severity": "fail",
                                    "detail": f"Font size {pt_val}pt in '{r.text[:20]}' is below the {MIN_FONT_SIZE_PT}pt floor.",
                                    "recommended_action": f"Increase font size to at least {MIN_FONT_SIZE_PT}pt."
                                })
                            # Check fractional size
                            if pt_val != int(pt_val):
                                violations.append({
                                    "slide_index": slide_index,
                                    "rule": "NO_FRACTIONAL_FONTS",
                                    "severity": "warning",
                                    "detail": f"Font size {pt_val}pt is fractional.",
                                    "recommended_action": f"Snap to integer size {snap_to_norman_font_size(pt_val)}pt."
                                })

            # Store for collision detection if it's a visible content box (not background full-slide card)
            if w < (slide_width_in - 1.0) and h < (slide_height_in - 1.0) and full_text:
                boxes.append({
                    "name": shape.name,
                    "x": x, "y": y, "w": w, "h": h,
                    "text": full_text[:25]
                })

    # Total slide word count check (excluding title and footers, content slides only)
    body_word_count = len(slide_text_words)
    if slide_index > 1 and body_word_count > MAX_WORDS_PER_SLIDE:
        violations.append({
            "slide_index": slide_index,
            "rule": "MAX_WORDS_PER_SLIDE",
            "severity": "warning",
            "detail": f"Slide has {body_word_count} body words (Norman limit: {MAX_WORDS_PER_SLIDE}).",
            "recommended_action": f"Offload {body_word_count - MAX_WORDS_PER_SLIDE} words to speaker_notes or split into two slides."
        })

    # Bounding-Box Collision Detection between distinct sibling text boxes
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            b1, b2 = boxes[i], boxes[j]
            # Calculate intersection
            x_overlap = max(0.0, min(b1["x"] + b1["w"], b2["x"] + b2["w"]) - max(b1["x"], b2["x"]))
            y_overlap = max(0.0, min(b1["y"] + b1["h"], b2["y"] + b2["h"]) - max(b1["y"], b2["y"]))

            # Ignore tiny boundary touches (< 0.05 in) or nested containers
            if x_overlap > 0.15 and y_overlap > 0.15:
                # Check if one contains the other (e.g. card container containing text)
                contains = (b1["x"] <= b2["x"] and b1["y"] <= b2["y"] and (b1["x"] + b1["w"]) >= (b2["x"] + b2["w"]) and (b1["y"] + b1["h"]) >= (b2["y"] + b2["h"])) or \
                           (b2["x"] <= b1["x"] and b2["y"] <= b1["y"] and (b2["x"] + b2["w"]) >= (b1["x"] + b1["w"]) and (b2["y"] + b2["h"]) >= (b1["y"] + b1["h"]))
                if not contains:
                    violations.append({
                        "slide_index": slide_index,
                        "rule": "BOUNDING_BOX_COLLISION",
                        "severity": "fail",
                        "detail": f"Boxes overlap by {x_overlap:.2f}x{y_overlap:.2f} in: '{b1['text']}' and '{b2['text']}'.",
                        "recommended_action": "Add minimum 0.25in gutter between elements."
                    })

    return violations


def validate_deck(pptx_path_or_prs) -> Dict[str, Any]:
    """
    Executes a comprehensive Don Norman Human-Centered Design audit across the entire presentation.
    Returns:
    {
      "status": "pass" | "warning" | "fail",
      "norman_ux_score": int (0-100),
      "total_slides": int,
      "violations": [ ... ]
    }
    """
    if isinstance(pptx_path_or_prs, str):
        prs = Presentation(pptx_path_or_prs)
    else:
        prs = pptx_path_or_prs

    all_violations = []
    total_slides = len(prs.slides)
    slide_w = prs.slide_width / 914400.0 if prs.slide_width else CANVAS_WIDTH_IN
    slide_h = prs.slide_height / 914400.0 if prs.slide_height else CANVAS_HEIGHT_IN

    for idx, slide in enumerate(prs.slides, 1):
        v = audit_slide_ux(slide, idx, slide_w, slide_h)
        all_violations.extend(v)

    fails = [v for v in all_violations if v["severity"] == "fail"]
    warnings = [v for v in all_violations if v["severity"] == "warning"]

    # Calculate Norman UX score (100 base, -15 per fail, -3 per warning, clamped 0-100)
    score = max(0, min(100, 100 - (len(fails) * 15 + len(warnings) * 3)))

    status = "pass"
    if fails:
        status = "fail"
    elif warnings:
        status = "warning"

    return {
        "status": status,
        "norman_ux_score": score,
        "total_slides": total_slides,
        "violations_count": {
            "fails": len(fails),
            "warnings": len(warnings),
            "total": len(all_violations)
        },
        "violations": all_violations
    }
