import unittest
import os
from design_system.norman_ux import snap_to_norman_font_size, contrast_ratio, validate_deck

class TestNormanUX(unittest.TestCase):
    def test_typography_floor_snapping(self):
        self.assertEqual(snap_to_norman_font_size(9), 12)
        self.assertEqual(snap_to_norman_font_size(10.5), 12)
        self.assertEqual(snap_to_norman_font_size(11.5), 12)
        self.assertEqual(snap_to_norman_font_size(12.0), 12)
        self.assertEqual(snap_to_norman_font_size(13.5), 14)
        self.assertEqual(snap_to_norman_font_size(15.0), 16)
        self.assertEqual(snap_to_norman_font_size(23.0), 24)

    def test_contrast_ratio(self):
        white = (255, 255, 255)
        black = (0, 0, 0)
        navy = (31, 73, 125)
        self.assertAlmostEqual(contrast_ratio(white, black), 21.0, places=1)
        self.assertGreater(contrast_ratio(white, navy), 4.5)

    def test_deck_validation_no_critical_fails(self):
        target = "Supplier_Delivery_Tracker_CIO_Briefing_Updated.pptx"
        if os.path.exists(target):
            report = validate_deck(target)
            self.assertEqual(report["violations_count"]["fails"], 0, f"Critical fails detected: {report['violations']}")
            self.assertIn(report["status"], ("pass", "warning"))
            self.assertGreaterEqual(report["norman_ux_score"], 70)

if __name__ == "__main__":
    unittest.main()
