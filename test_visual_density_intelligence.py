import os
import sys
import unittest
from pptx import Presentation
from pptx.util import Inches

from design_system.density_intelligence import (
    VisualDensity,
    VisualDensityClassifier,
    DensityEvaluation,
    WhitespaceIntelligenceEngine,
    LowDensitySlideRenderer
)
from ppt_mcp_server import (
    evaluate_visual_density,
    render_low_density_slide
)


class TestVisualDensityIntelligence(unittest.TestCase):
    OUTPUT_DECK = "test_low_density_deck.pptx"
    MCP_OUTPUT_DECK = "test_mcp_density_deck.pptx"

    def tearDown(self):
        for p in [self.OUTPUT_DECK, self.MCP_OUTPUT_DECK]:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except OSError:
                    pass

    def test_01_density_classification(self):
        """Verify classification into LOW, MEDIUM, and HIGH density tiers."""
        # LOW DENSITY
        self.assertEqual(VisualDensityClassifier.classify("CEO Strategic Mandate & North Star", "executive_statement"), VisualDensity.LOW_DENSITY)
        self.assertEqual(VisualDensityClassifier.classify("Architectural Principle: Zero Replication", "architectural_principle"), VisualDensity.LOW_DENSITY)
        self.assertEqual(VisualDensityClassifier.classify("Key Strategic Insight: Working Capital", "key_insight"), VisualDensity.LOW_DENSITY)
        self.assertEqual(VisualDensityClassifier.classify("Section 2: Solution Architecture", "section_divider"), VisualDensity.LOW_DENSITY)

        # MEDIUM DENSITY
        self.assertEqual(VisualDensityClassifier.classify("Clean-Core S/4HANA to Shop Floor Topology", "architecture_diagram"), VisualDensity.MEDIUM_DENSITY)
        self.assertEqual(VisualDensityClassifier.classify("Order-to-Cash End-to-End Execution Flow", "process_flow"), VisualDensity.MEDIUM_DENSITY)
        self.assertEqual(VisualDensityClassifier.classify("90-Day Agile Implementation Roadmap", "roadmap"), VisualDensity.MEDIUM_DENSITY)
        self.assertEqual(VisualDensityClassifier.classify("Two-Tier Approval Desk & Governance Model", "governance"), VisualDensity.MEDIUM_DENSITY)
        self.assertEqual(VisualDensityClassifier.classify("Current Reality vs Target State Comparison", "comparison"), VisualDensity.MEDIUM_DENSITY)

        # HIGH DENSITY
        self.assertEqual(VisualDensityClassifier.classify("Operational Fulfillment Cockpit", "dashboard"), VisualDensity.HIGH_DENSITY)
        self.assertEqual(VisualDensityClassifier.classify("Plant-Wide Scrap & Defect Analytical Table", "analytical_table"), VisualDensity.HIGH_DENSITY)
        self.assertEqual(VisualDensityClassifier.classify("IT/OT Interface Protocol Catalogue", "interface_catalogue"), VisualDensity.HIGH_DENSITY)
        self.assertEqual(VisualDensityClassifier.classify("Field-Level S/4HANA Data Mapping Matrix", "data_mapping"), VisualDensity.HIGH_DENSITY)

    def test_02_whitespace_evaluation_and_anti_filler(self):
        """Verify that evaluation optimizes content importance, visual complexity, and blocks filler cards."""
        low_eval = WhitespaceIntelligenceEngine.evaluate("Executive Statement", "executive_statement")
        self.assertEqual(low_eval.density_class, VisualDensity.LOW_DENSITY)
        self.assertGreaterEqual(low_eval.target_whitespace_ratio, 0.55)
        self.assertTrue(low_eval.is_self_sufficient)
        self.assertFalse(low_eval.allow_auxiliary_cards)
        self.assertGreater(len(low_eval.anti_filler_rules), 0)

        med_eval = WhitespaceIntelligenceEngine.evaluate("System Architecture Blueprint", "architecture_diagram")
        self.assertEqual(med_eval.density_class, VisualDensity.MEDIUM_DENSITY)
        self.assertTrue(med_eval.is_self_sufficient)
        self.assertFalse(med_eval.allow_auxiliary_cards)
        self.assertTrue(any("COMPLETE on its own" in rule for rule in med_eval.anti_filler_rules))

        high_eval = WhitespaceIntelligenceEngine.evaluate("Executive Cockpit", "dashboard")
        self.assertEqual(high_eval.density_class, VisualDensity.HIGH_DENSITY)
        self.assertLessEqual(high_eval.target_whitespace_ratio, 0.25)
        self.assertTrue(high_eval.is_self_sufficient)

    def test_03_render_low_density_slides_deck(self):
        """Render low-density slides and verify generous whitespace, minimal shape count, and Inter typography."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.500)

        # 1. Executive Statement
        s1 = LowDensitySlideRenderer.render_executive_statement(
            prs=prs,
            statement="The maths happens where the data already lives.",
            supporting_thesis="By eliminating live data replication into external data lakes, S/4HANA memory integrity is preserved.",
            author_or_source="Lead Enterprise Architect",
            client_name="Boeing Aerospace",
            is_dark=True
        )
        self.assertIsNotNone(s1)

        # 2. Architectural Principle
        s2 = LowDensitySlideRenderer.render_architectural_principle(
            prs=prs,
            principle_title="Zero Financial Ledger Replication",
            core_rule="S/4HANA ACDOCA remains the sole universal ledger for operational and financial truth.",
            architectural_rationale="Manufacturing execution systems post event confirmations via standard OData v4 APIs but never replicate double-entry journals.",
            client_name="Boeing Aerospace",
            is_dark=False
        )
        self.assertIsNotNone(s2)

        # 3. Hero KPI with Conclusion
        s3 = LowDensitySlideRenderer.render_hero_kpi_with_conclusion(
            prs=prs,
            metric_value="$14.2M",
            metric_label="Working Capital in Stalled WIP",
            conclusion_statement="34% of working capital is trapped in sub-assemblies waiting for single-source microchips.",
            context_detail="ACDOCA Material Ledger • Rolling 90-Day Analysis",
            client_name="Boeing Aerospace",
            is_dark=True
        )
        self.assertIsNotNone(s3)

        self.assertEqual(len(prs.slides), 3)
        prs.save(self.OUTPUT_DECK)
        self.assertTrue(os.path.exists(self.OUTPUT_DECK))

        # Reopen and audit contents
        saved_prs = Presentation(self.OUTPUT_DECK)
        for slide_idx, slide in enumerate(saved_prs.slides):
            # Shape count should be intentionally low (<= 10 shapes including canvas/header/footer, zero satellite filler cards)
            self.assertLessEqual(len(slide.shapes), 10, f"Slide {slide_idx} has too many shapes for low-density ({len(slide.shapes)})")

            for shape in slide.shapes:
                if shape.has_text_frame:
                    for p in shape.text_frame.paragraphs:
                        for r in p.runs:
                            if r.font and r.font.name:
                                self.assertTrue(
                                    r.font.name.startswith("Inter"),
                                    f"Non-Inter font '{r.font.name}' found on slide {slide_idx}"
                                )

    def test_04_mcp_tools_density(self):
        """Verify FastMCP evaluate_visual_density and render_low_density_slide tools."""
        eval_res = evaluate_visual_density("CEO Keynote Statement", "executive_statement")
        self.assertEqual(eval_res["density_class"], "LOW_DENSITY")
        self.assertTrue(eval_res["is_self_sufficient"])
        self.assertFalse(eval_res["allow_auxiliary_cards"])

        # Render statement
        res = render_low_density_slide(
            path=self.MCP_OUTPUT_DECK,
            archetype="EXECUTIVE_STATEMENT",
            headline="Simplicity is the prerequisite for reliability.",
            supporting_text="Decoupled clean-core architectures outperform tightly bound monoliths across every operational dimension.",
            author_or_detail="Edsger Dijkstra / Enterprise Architecture",
            client_name="Raytheon",
            is_dark=True
        )
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["total_slides"], 1)
        self.assertTrue(os.path.exists(self.MCP_OUTPUT_DECK))

        # Append Hero KPI
        res2 = render_low_density_slide(
            path=self.MCP_OUTPUT_DECK,
            archetype="HERO_KPI",
            headline="Annualized Cost of Poor Quality",
            supporting_text="Scrap and rework costs consume 4.8% of gross manufacturing revenue.",
            metric_value="$3.42M",
            client_name="Raytheon",
            is_dark=False
        )
        self.assertEqual(res2["status"], "success")
        self.assertEqual(res2["total_slides"], 2)


if __name__ == "__main__":
    unittest.main()
