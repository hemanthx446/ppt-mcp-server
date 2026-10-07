"""
Semantic Color Tokens & Enterprise Consulting Themes.

Restrained, executive color palettes avoiding saturated rainbow noise or decorative UI blobs.
"""

from dataclasses import dataclass
from pptx.dml.color import RGBColor


def RGB(hex_str: str) -> RGBColor:
    """Helper to convert hex string ('0B132B' or '#0B132B') to pptx RGBColor."""
    clean = hex_str.lstrip('#')
    if len(clean) != 6:
        raise ValueError(f"Invalid hex color: {hex_str}. Must be 6 characters.")
    return RGBColor(int(clean[0:2], 16), int(clean[2:4], 16), int(clean[4:6], 16))


@dataclass(frozen=True)
class Theme:
    """Semantic color token mapping for a cohesive presentation theme."""
    is_dark: bool

    # Surfaces & Canvas
    canvas: RGBColor
    surface: RGBColor
    surface_alt: RGBColor
    surface_muted: RGBColor
    surface_highlight: RGBColor

    # Outlines & Dividers (Flat architectural borders, never heavy shadows)
    border: RGBColor
    border_muted: RGBColor
    border_accent: RGBColor

    # Typographic Colors
    text_primary: RGBColor
    text_secondary: RGBColor
    text_muted: RGBColor
    text_accent: RGBColor

    # Semantic Accents (Enterprise SAP Blue, Tech Cyan, etc.)
    accent_primary: RGBColor
    accent_secondary: RGBColor
    accent_gold: RGBColor

    # Operational Status Accents (Used sparingly for metrics and alerts)
    status_success: RGBColor
    status_warning: RGBColor
    status_critical: RGBColor
    status_info: RGBColor


# 1. Executive Dark Theme (Navy - used for Strategic Titles, Architecture Blueprints)
ExecutiveNavyTheme = Theme(
    is_dark=True,
    canvas=RGB("0A162C"),             # Deep Executive Navy
    surface=RGB("132240"),            # Elevated Container Surface
    surface_alt=RGB("16284B"),        # Alternating Surface
    surface_muted=RGB("0E1B33"),      # Subdued Surface
    surface_highlight=RGB("1C3159"),  # Focus / Selected Surface

    border=RGB("263B63"),             # Restrained Container Outline
    border_muted=RGB("1B2B48"),       # Subdued Outline
    border_accent=RGB("00B4D8"),      # Cyan Accent Outline

    text_primary=RGB("F8FAFC"),       # Off-White High Contrast
    text_secondary=RGB("CBD5E1"),     # Slate Soft
    text_muted=RGB("94A3B8"),         # Slate Muted
    text_accent=RGB("00B4D8"),        # Tech Cyan Accent

    accent_primary=RGB("00B4D8"),     # Tech Cyan
    accent_secondary=RGB("0066CC"),   # Enterprise Blue
    accent_gold=RGB("D97706"),        # Amber / Gold

    status_success=RGB("10B981"),     # Emerald Green
    status_warning=RGB("F59E0B"),     # Warm Amber
    status_critical=RGB("EF4444"),    # Crimson Red
    status_info=RGB("3B82F6")         # Informational Blue
)


# 2. Consulting Slate Theme (Light - used for Dashboards, Data Tables, Roadmaps)
ConsultingSlateTheme = Theme(
    is_dark=False,
    canvas=RGB("F8FAFC"),             # Slate Ice Canvas
    surface=RGB("FFFFFF"),            # Pure White Surface
    surface_alt=RGB("F1F5F9"),        # Soft Slate Row Alternate
    surface_muted=RGB("F8FAFC"),      # Subdued Surface
    surface_highlight=RGB("EEF2FF"),  # Soft Blue Tint Highlight

    border=RGB("E2E8F0"),             # Soft Slate Outline
    border_muted=RGB("F1F5F9"),       # Subtle Divider Outline
    border_accent=RGB("0066CC"),      # Enterprise SAP Blue Outline

    text_primary=RGB("0F172A"),       # Deep Slate Charcoal
    text_secondary=RGB("334155"),     # Slate Charcoal Secondary
    text_muted=RGB("64748B"),         # Cool Muted Slate
    text_accent=RGB("0066CC"),        # Enterprise Blue Accent

    accent_primary=RGB("0066CC"),     # Enterprise SAP Blue
    accent_secondary=RGB("00B4D8"),   # Tech Cyan
    accent_gold=RGB("D97706"),        # Warm Amber / Gold

    status_success=RGB("10B981"),     # Emerald Green
    status_warning=RGB("D97706"),     # Warm Amber
    status_critical=RGB("DC2626"),    # Crimson Red
    status_info=RGB("2563EB")         # Information Blue
)


class ColorSystem:
    """Gateway for color resolution and active themes."""
    DARK = ExecutiveNavyTheme
    LIGHT = ConsultingSlateTheme

    @staticmethod
    def resolve_theme(is_dark: bool) -> Theme:
        return ExecutiveNavyTheme if is_dark else ConsultingSlateTheme
