"""
Unit Tests for PowerPoint Scrutiny Perspectives & Delivery Gate.
Verifies file structure compliance, honest framing, calibration distinctness,
and sequential delivery gate locking across all implemented perspectives.
"""

import os
import unittest
from design_system.scrutiny import (
    PERSPECTIVES_REGISTRY,
    list_all_perspectives,
    get_perspective_brief,
    apply_perspective_to_deck,
    record_perspective_review_data,
    get_scrutiny_status,
    is_delivery_allowed,
    parse_findings_from_review_markdown
)

MANDATORY_FRAMING = "Lens modelled from published work. It is not the person's own statement."
REQUIRED_SKILL_SECTIONS = [
    "Identity and Domain",
    "Sources",
    "Core Beliefs",
    "What This Lens Notices First",
    "10 Signature Questions",
    "Red Flags",
    "What Good Looks Like",
    "Evidence Needed",
    "Severity Rubric",
    "Blind Spots",
    "Tensions with Other Lenses",
    "Output Template"
]


class TestScrutinyPerspectives(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        self.perspectives_dir = os.path.join(self.base_dir, "perspectives")
        self.calibration_dir = os.path.join(self.base_dir, "calibration")

    def test_01_registry_has_exact_14_ordered_perspectives(self):
        """Verify registry contains exactly the 14 required perspectives in exact sequence."""
        self.assertEqual(len(PERSPECTIVES_REGISTRY), 14)
        expected_names = [
            "jeanne-ross", "john-zachman", "ivar-jacobson", "dennis-brandl",
            "michael-mcclellan", "peter-senge", "russell-ackoff", "donella-meadows",
            "w-edwards-deming", "eliyahu-goldratt", "george-westerman", "andrew-mcafee",
            "erik-brynjolfsson", "human-dimension"
        ]
        actual_names = [p["name"] for p in PERSPECTIVES_REGISTRY]
        self.assertEqual(actual_names, expected_names)

    def test_02_all_implemented_skills_adhere_to_standard(self):
        """Verify all written skill files adhere strictly to Skill File Standard and honest framing."""
        implemented = [p for p in list_all_perspectives() if p["implemented"]]
        self.assertGreaterEqual(len(implemented), 1, "At least one skill must be implemented.")

        for p in implemented:
            file_path = p["skill_file"]
            self.assertTrue(os.path.exists(file_path), f"Missing skill file: {file_path}")

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn(MANDATORY_FRAMING, content, f"Missing mandatory framing in {file_path}")

            for section in REQUIRED_SKILL_SECTIONS:
                self.assertIn(section.lower(), content.lower(), f"Missing section '{section}' in {file_path}")

            self.assertGreaterEqual(content.count("Red Flags"), 1, f"Missing Red Flags section in {file_path}")

    def test_03_all_calibration_outputs_produce_at_least_5_findings(self):
        """Verify all calibration outputs produce >= 5 findings with valid P1/P2/P3 severity tags."""
        if not os.path.exists(self.calibration_dir):
            return

        calib_files = [f for f in os.listdir(self.calibration_dir) if f.endswith(".md")]
        self.assertGreaterEqual(len(calib_files), 1, "At least one calibration file must exist.")

        for cf in calib_files:
            cpath = os.path.join(self.calibration_dir, cf)
            with open(cpath, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn(MANDATORY_FRAMING, content, f"Missing framing in {cf}")
            findings = parse_findings_from_review_markdown(content)
            self.assertGreaterEqual(len(findings), 5, f"Calibration file {cf} has only {len(findings)} findings (must be >= 5).")

            for f in findings:
                self.assertIn(f["severity"], ["P1", "P2", "P3"], f"Invalid severity in {cf}: {f.get('id')}")

    def test_04_sequential_apply_perspective_enforcement(self):
        """Verify sequential gating: Lens N cannot be run if Lens N-1 is unrecorded or has blockers."""
        # For an unreviewed deck without prior recorded reviews, Lens 2 must return an error
        res_unreviewed = apply_perspective_to_deck("unreviewed_deck.pptx", "john-zachman")
        self.assertIn("error", res_unreviewed)
        self.assertIn("Sequential violation", res_unreviewed["error"])

        # For the smoke-test deck where Lens 1 has passed, Lens 2 is ready
        res1 = apply_perspective_to_deck("Supplier_Delivery_Tracker_CIO_Briefing.pptx", "jeanne-ross")
        self.assertEqual(res1.get("status"), "ready_for_review")
        res2 = apply_perspective_to_deck("Supplier_Delivery_Tracker_CIO_Briefing.pptx", "john-zachman")
        self.assertEqual(res2.get("status"), "ready_for_review")

    def test_05_delivery_gate_locks_when_scrutiny_incomplete(self):
        """Verify presentation export is locked until all 14 scrutiny lenses are cleared."""
        allowed, msg = is_delivery_allowed("unreviewed_deck.pptx")
        self.assertFalse(allowed)
        self.assertIn("Export locked by Scrutiny Gate", msg)

    def test_06_delivery_gate_unlocks_when_all_lenses_pass(self):
        """Verify presentation export is unlocked when all 14 scrutiny lenses pass with 0 P1 blockers."""
        allowed, msg = is_delivery_allowed("Supplier_Delivery_Tracker_CIO_Briefing.pptx")
        self.assertTrue(allowed)
        self.assertEqual(msg, "Scrutiny Gate cleared.")


if __name__ == "__main__":
    unittest.main()
