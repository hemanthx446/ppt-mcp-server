import os
import json
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

class LumbiniTheme:
    def __init__(self, token_path: str = None):
        if not token_path:
            token_path = os.path.join(os.path.dirname(__file__), "..", "..", "themes", "lumbini", "tokens.json")
        token_path = os.path.abspath(token_path)
        with open(token_path, "r", encoding="utf-8") as f:
            self.raw = json.load(f)

        self.name = self.raw.get("name", "lumbini")
        c = self.raw["colors"]
        self.HEX = c
        self.C_TEXT = self._parse_hex(c["text"])             # 141E2D
        self.C_PRIMARY = self._parse_hex(c["primary"])       # 0070C0
        self.C_PRIMARY_DEEP = self._parse_hex(c["primary_deep"]) # 0066B4
        self.C_NAVY = self._parse_hex(c["navy"])             # 1F497D
        self.C_ACCENT = self._parse_hex(c["accent"])         # F78B15
        self.C_MUTED = self._parse_hex(c["muted"])           # 646E78
        self.C_BORDER = self._parse_hex(c["border"])         # DCE1E6
        self.C_SURFACE = self._parse_hex(c["surface"])       # EEF3F8
        self.C_WHITE = self._parse_hex(c["white"])           # FFFFFF

        # Semantic palette (v2 §6)
        self.C_BLUE = self.C_PRIMARY                         # Blue = system / enterprise
        self.C_ORANGE = self.C_ACCENT                        # Orange = constraint / decision point
        self.C_GREEN = self._parse_hex("198038")             # Green = target outcome / healthy
        self.C_ALERT = self._parse_hex("DA1E28")             # Red / Alert = critical failure mode / bottleneck

        f_data = self.raw["fonts"]
        self.FONT_HEADING = f_data["heading"]
        self.FONT_BODY = f_data["body"]
        self.FONT_BOLD = f_data["bold"]
        self.FONT_SEMIBOLD = f_data["semibold"]

        t = self.raw["type_scale_pt"]
        self.PT_TITLE = Pt(t["title"])
        self.PT_COVER_TITLE = Pt(t["cover_title"])
        self.PT_EYEBROW = Pt(t["eyebrow"])
        self.PT_SUBTITLE = Pt(t["subtitle"])
        self.PT_BODY = Pt(t["body"])
        self.PT_CAPTION_MIN = Pt(t["caption_min"])
        self.PT_FOOTER = Pt(t["footer"])
        self.PT_KPI_VALUE = Pt(t["kpi_value"])

        s = self.raw["slide"]
        self.IN_WIDTH = Inches(s["width_in"])
        self.IN_HEIGHT = Inches(s["height_in"])
        self.IN_MARGIN_X = Inches(s["margin_x_in"])
        self.IN_CONTENT_TOP = Inches(s["content_top_in"])
        self.IN_FOOTER_Y = Inches(s["footer_y_in"])

        self.ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(token_path), "assets"))
        self.LOGO_PATH = os.path.join(self.ASSETS_DIR, "logo.png")
        self.ILLUS_PATH = os.path.join(self.ASSETS_DIR, "illus.png")
        self.BG_LIGHT_PATH = os.path.join(self.ASSETS_DIR, "bg_light.jpg")

    def _parse_hex(self, hex_code: str) -> RGBColor:
        h = hex_code.lstrip("#")
        return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

_DEFAULT_THEME = None

def get_lumbini_theme() -> LumbiniTheme:
    global _DEFAULT_THEME
    if _DEFAULT_THEME is None:
        _DEFAULT_THEME = LumbiniTheme()
    return _DEFAULT_THEME
