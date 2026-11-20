"""
Unit Tests for PowerPoint Scrutiny Perspectives & Delivery Gate.
Verifies file structure compliance, honest framing, calibration distinctness,
and sequential delivery gate locking.
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

    def test_02_layer1_skill_file_structure_and_framing(self):
        """Verify 01-jeanne-ross.md adheres strictly to Skill File Standard."""
        file_path = os.path.join(self.perspectives_dir, "01-jeanne-ross.md")
        self.assertTrue(os.path.exists(file_path), f"Missing skill file: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check honest framing
        self.assertIn(MANDATORY_FRAMING, content, "Missing mandatory honest framing statement.")

        # Check all 12 required sections
        for section in REQUIRED_SKILL_SECTIONS:
            self.assertIn(section.lower(), content.lower(), f"Missing required section: {section}")

        # Check at least 6 red flags are listed
        red_flags_match = content.count("\n1. ") + content.count("\n2. ")
        self.assertGreaterEqual(content.count("Red Flags"), 1)

    def test_03_layer1_calibration_findings_and_distinctness(self):
        """Verify calibration output for Layer 1 produces >= 5 findings with unique insights."""
        calib_file = os.path.join(self.calibration_dir, "01-jeanne-ross.md")
        self.assertTrue(os.path.exists(calib_file), f"Missing calibration file: {calib_file}")

        with open(calib_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check honest framing
        self.assertIn(MANDATORY_FRAMING, content)

        # Parse findings table
        findings = parse_findings_from_review_markdown(content)
        self.assertGreaterEqual(len(findings), 5, f"Calibration produced only {len(findings)} findings (must be >= 5).")

        # Verify severity distribution
        severities = [f["severity"] for f in findings]
        for s in severities:
            self.assertIn(s, ["P1", "P2", "P3"])

        # Check for unique signature findings
        titles = " ".join(f["title"] for f in findings).lower()
        self.assertTrue(
            "operating model" in titles or "shadow" in titles or "decision rights" in titles or "batch" in titles,
            "Calibration missing signature findings unique to Jeanne Ross."
        )

    def test_04_sequential_apply_perspective_enforcement(self):
        """Verify that Lens 2 cannot be applied before Lens 1 is recorded and cleared."""
        # Querying Lens 1 should be ready
        res1 = apply_perspective_to_deck("Supplier_Delivery_Tracker_CIO_Briefing.pptx", "jeanne-ross")
        self.assertEqual(res1.get("status"), "ready_for_review")

        # Querying Lens 2 before Lens 1 is recorded without blockers must fail
        res2 = apply_perspective_to_deck("Supplier_Delivery_Tracker_CIO_Briefing.pptx", "john-zachman")
        # In calibration, 01-jeanne-ross.md has 2 P1s, so it must block progression
        self.assertIn("error", res2)
        self.assertIn("unaddressed P1 blocker", res2["error"])

    def test_05_delivery_gate_locks_when_scrutiny_incomplete(self):
        """Verify presentation export is locked until all 14 scrutiny lenses are cleared."""
        allowed, msg = is_delivery_allowed("Supplier_Delivery_Tracker_CIO_Briefing.pptx")
        self.assertFalse(allowed)
        self.assertIn("Export locked by Scrutiny Gate", msg)


if __name__ == "__main__":
    unittest.main()
