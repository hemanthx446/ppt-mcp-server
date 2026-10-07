"""
Centralized Typography Design Tokens.

STRICT RULE: Uses ONLY Inter (Inter Regular, Inter Semi Bold, Inter Bold).
No other fonts allowed.
"""

from dataclasses import dataclass
from typing import Optional
from pptx.util import Pt
from pptx.dml.color import RGBColor

# Strict Single Font Family
FONT_FAMILY = "Inter"

@dataclass(frozen=True)
class TypographyToken:
    """Immutable specification for a text typographic element."""
    font_name: str
    size_pt: float
    bold: bool
    italic: bool = False
    all_caps: bool = False
    line_spacing: Optional[float] = None
    space_after_pt: Optional[float] = None
    weight_name: str = "Regular"

    @property
    def pt(self) -> Pt:
        return Pt(self.size_pt)

    @property
    def space_after(self) -> Optional[Pt]:
        return Pt(self.space_after_pt) if self.space_after_pt is not None else None


class TypographySystem:
    """
    Centralized Typographic Hierarchy for Enterprise Architecture & Consulting Slides.
    All tokens strictly reference the Inter typography scale.
    """

    # 1. Presentation Title (Hero title on cover / title slide)
    PRESENTATION_TITLE = TypographyToken(
        font_name=FONT_FAMILY,
        size_pt=32.0,
        bold=True,
        line_spacing=1.1,
        space_after_pt=6.0,
        weight_name="Bold"
    )

    # 2. Section Title (Major agenda or transition slide title)
    SECTION_TITLE = TypographyToken(
        font_name=FONT_FAMILY,
        size_pt=24.0,
        bold=True,
        line_spacing=1.15,
        space_after_pt=6.0,
        weight_name="Bold"
    )

    # 3. Slide Title (Standard slide action title)
    SLIDE_TITLE = TypographyToken(
        font_name=FONT_FAMILY,
        size_pt=19.0,
        bold=True,
        line_spacing=1.15,
        space_after_pt=4.0,
        weight_name="Bold"
    )

    # 4. Subtitle (Conversational / narrative subheader underneath slide title)
    SUBTITLE = TypographyToken(
        font_name=FONT_FAMILY,
        size_pt=11.0,
        bold=False,
        italic=True,
        line_spacing=1.2,
        space_after_pt=6.0,
        weight_name="Regular"
    )

    # 5. Body (Standard narrative text, paragraph descriptions)
    BODY = TypographyToken(
        font_name=FONT_FAMILY,
        size_pt=10.5,
        bold=False,
        line_spacing=1.25,
        space_after_pt=6.0,
        weight_name="Regular"
    )

    # 5b. Body Emphasized / Lead-in run
    BODY_STRONG = TypographyToken(
        font_name=FONT_FAMILY,
        size_pt=10.5,
        bold=True,
        weight_name="Semi Bold"
    )

    # 6. Label (Badges, category tags, eyebrow pills, column tags)
    LABEL = TypographyToken(
        font_name=FONT_FAMILY,
        size_pt=8.5,
        bold=True,
        all_caps=True,
        space_after_pt=2.0,
        weight_name="Bold"
    )

    # 7. KPI Number (Prominent quantitative figure / metric hero)
    KPI_NUMBER = TypographyToken(
        font_name=FONT_FAMILY,
        size_pt=24.0,
        bold=True,
        line_spacing=1.0,
        space_after_pt=2.0,
        weight_name="Bold"
    )

    # 8. KPI Label (Descriptor / context line beneath KPI number)
    KPI_LABEL = TypographyToken(
        font_name=FONT_FAMILY,
        size_pt=9.0,
        bold=True,
        line_spacing=1.15,
        space_after_pt=4.0,
        weight_name="Semi Bold"
    )

    # 9. Table Header (Columns in enterprise governance matrices & tables)
    TABLE_HEADER = TypographyToken(
        font_name=FONT_FAMILY,
        size_pt=8.5,
        bold=True,
        space_after_pt=2.0,
        weight_name="Bold"
    )

    # 10. Table Body (Cell content in tables)
    TABLE_BODY = TypographyToken(
        font_name=FONT_FAMILY,
        size_pt=8.0,
        bold=False,
        line_spacing=1.15,
        space_after_pt=2.0,
        weight_name="Regular"
    )

    # 11. Annotation (Technical parameter badge, protocol label, SLA tag)
    ANNOTATION = TypographyToken(
        font_name=FONT_FAMILY,
        size_pt=8.2,
        bold=True,
        weight_name="Semi Bold"
    )

    # 12. Caption (Image descriptions, diagram step captions, sub-card notes)
    CAPTION = TypographyToken(
        font_name=FONT_FAMILY,
        size_pt=7.5,
        bold=False,
        italic=True,
        line_spacing=1.1,
        weight_name="Regular"
    )

    # 13. Footnote (Footer confidentiality line, data lineage disclaimer, source notes)
    FOOTNOTE = TypographyToken(
        font_name=FONT_FAMILY,
        size_pt=8.0,
        bold=False,
        line_spacing=1.0,
        weight_name="Regular"
    )

    @classmethod
    def apply_to_run(
        cls,
        run,
        token: TypographyToken,
        color_rgb: Optional[RGBColor] = None,
        override_text: Optional[str] = None
    ):
        """Applies a typography token strictly to a python-pptx Run object."""
        if override_text is not None:
            run.text = override_text.upper() if token.all_caps else override_text
        elif token.all_caps and run.text:
            run.text = run.text.upper()

        run.font.name = token.font_name
        run.font.size = token.pt
        run.font.bold = token.bold
        run.font.italic = token.italic
        if color_rgb is not None:
            run.font.color.rgb = color_rgb

    @classmethod
    def apply_to_paragraph(
        cls,
        paragraph,
        token: TypographyToken,
        text: Optional[str] = None,
        color_rgb: Optional[RGBColor] = None
    ):
        """Applies a typography token to a python-pptx Paragraph object and its primary run."""
        if token.space_after is not None:
            paragraph.space_after = token.space_after

        if text is not None:
            formatted_text = text.upper() if token.all_caps else text
            if len(paragraph.runs) > 0:
                run = paragraph.runs[0]
                run.text = formatted_text
            else:
                run = paragraph.add_run()
                run.text = formatted_text
            cls.apply_to_run(run, token, color_rgb)
        else:
            for run in paragraph.runs:
                cls.apply_to_run(run, token, color_rgb)
