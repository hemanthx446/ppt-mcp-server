"""
Centralized Spacing, Layout Geometry & Grid Math.

Standard Widescreen 16:9 Canvas (13.333" x 7.500").
Restrained, architectural, executive grid alignment.
"""

from dataclasses import dataclass
from typing import List, Tuple
from pptx.util import Inches, Pt


@dataclass(frozen=True)
class CanvasBounds:
    """Dimensions of standard 16:9 widescreen presentation canvas in inches."""
    width: float = 13.333
    height: float = 7.500

    @property
    def width_in(self) -> Inches:
        return Inches(self.width)

    @property
    def height_in(self) -> Inches:
        return Inches(self.height)


@dataclass(frozen=True)
class Margins:
    """Safe margins around the canvas perimeter."""
    left: float = 0.800
    right: float = 0.800
    top: float = 0.380
    bottom: float = 0.450

    @property
    def usable_width(self) -> float:
        return CanvasBounds.width - (self.left + self.right)  # 11.733 inches

    @property
    def usable_height(self) -> float:
        return CanvasBounds.height - (self.top + self.bottom) # 6.670 inches


class SpacingScale:
    """Consistent spatial rhythm and spacing scale."""
    # Increments in inches
    TIGHT = 0.08      # Intra-group spacing, micro gap
    COMPACT = 0.16    # Compact gap between adjacent elements
    STANDARD = 0.24   # Standard column gap and vertical section gap
    GENEROUS = 0.32   # Generous breathing gap between distinct modules
    EXPANSIVE = 0.48  # Major section divider gap

    # Padding inside surfaces / containers
    CONTAINER_PAD_H = 0.18
    CONTAINER_PAD_V = 0.14

    # Vertical Structure Offsets
    CATEGORY_TAG_TOP = 0.38
    CATEGORY_TAG_HEIGHT = 0.26
    
    TITLE_TOP = 0.66
    TITLE_HEIGHT = 0.44

    SUBTITLE_TOP = 1.10
    SUBTITLE_HEIGHT = 0.32

    # Content Canvas Top & Bottom
    CONTENT_TOP = 1.62
    CONTENT_BOTTOM = 6.85
    CONTENT_HEIGHT = CONTENT_BOTTOM - CONTENT_TOP  # 5.23 inches

    # Footer Offsets
    FOOTER_DIVIDER_TOP = 6.95
    FOOTER_TEXT_TOP = 7.02
    FOOTER_HEIGHT = 0.30


class GridCalculator:
    """
    Mathematical grid engine for dividing available space cleanly
    across N columns or rows with exact spacing.
    """

    @staticmethod
    def get_columns(
        count: int,
        left: float = Margins.left,
        total_width: float = Margins().usable_width,
        gap: float = SpacingScale.STANDARD
    ) -> List[Tuple[float, float]]:
        """
        Calculates (col_x, col_width) for N evenly spaced columns.
        Returns list of (left_in, width_in) tuples.
        """
        if count <= 0:
            return []
        if count == 1:
            return [(left, total_width)]

        total_gaps = (count - 1) * gap
        col_width = (total_width - total_gaps) / count

        columns = []
        for i in range(count):
            col_x = left + i * (col_width + gap)
            columns.append((col_x, col_width))
        return columns

    @staticmethod
    def get_rows(
        count: int,
        top: float = SpacingScale.CONTENT_TOP,
        total_height: float = SpacingScale.CONTENT_HEIGHT,
        gap: float = SpacingScale.STANDARD
    ) -> List[Tuple[float, float]]:
        """
        Calculates (row_y, row_height) for N evenly spaced horizontal rows.
        Returns list of (top_in, height_in) tuples.
        """
        if count <= 0:
            return []
        if count == 1:
            return [(top, total_height)]

        total_gaps = (count - 1) * gap
        row_height = (total_height - total_gaps) / count

        rows = []
        for i in range(count):
            row_y = top + i * (row_height + gap)
            rows.append((row_y, row_height))
        return rows

    @staticmethod
    def get_split(
        left_ratio: float = 0.5,
        left: float = Margins.left,
        total_width: float = Margins().usable_width,
        gap: float = SpacingScale.STANDARD
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """
        Calculates asymmetric 2-column split (e.g. 60/40 or 70/30).
        Returns ((left_x, left_w), (right_x, right_w)).
        """
        avail_width = total_width - gap
        left_w = avail_width * left_ratio
        right_w = avail_width * (1.0 - left_ratio)
        right_x = left + left_w + gap
        return ((left, left_w), (right_x, right_w))


class SpacingSystem:
    """Central gateway to the presentation spacing and layout system."""
    CANVAS = CanvasBounds()
    MARGINS = Margins()
    SCALE = SpacingScale()
    GRID = GridCalculator()
