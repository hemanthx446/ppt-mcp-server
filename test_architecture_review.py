import os
import sys
import unittest
from pptx import Presentation
from pptx.util import Inches

from design_system.architecture_review import (
    ArchitecturalLens,
    InquiryReviewResult,
    ArchitectureReviewScorecard,
    ArchitectureReviewEngine
)
from design_system.narrative_intelligence import (
    NarrativeFramework,
    NarrativeIntelligenceEngine
)
from ppt_mcp_server import (
    list_architecture_review_lenses,
    review_presentation_architecture
)


class TestArchitectureReviewEngine(unittest.TestCase):
    TEST_DECK = "test_review_presentation_deck.pptx"

    def tearDown(self):
        if os.path.exists(self.TEST_DECK):
            try:
                os.remove(self.TEST_DECK)
            except OSError:
                pass

    def test_01_lenses_and_inquiries_completeness(self):
        """Verify all 13 lenses and 20 inquiries are rigorously mapped."""
        lenses = ArchitectureReviewEngine.list_all_lenses()
        self.assertEqual(len(lenses), 13)

        lens_names = [l["lens"] for l in lenses]
        self.assertIn("Jeanne Ross", lens_names)
        self.assertIn("John Zachman", lens_names)
        self.assertIn("Ivar Jacobson", lens_names)
        self.assertIn("Dennis Brandl", lens_names)
        self.assertIn("Michael McClellan", lens_names)
        self.assertIn("Peter Senge", lens_names)
        self.assertIn("Russell Ackoff", lens_names)
        self.assertIn("Donella Meadows", lens_names)
        self.assertIn("W. Edwards Deming", lens_names)
        self.assertIn("Eliyahu Goldratt", lens_names)
        self.assertIn("George Westerman", lens_names)
        self.assertIn("Andrew McAfee", lens_names)
        self.assertIn("Erik Brynjolfsson", lens_names)

        # Check 20 inquiries
        self.assertEqual(len(ArchitectureReviewEngine.INQUIRIES), 20)
        q_texts = [q[1] for q in ArchitectureReviewEngine.INQUIRIES]
        self.assertIn("Is the business problem clear?", q_texts)
        self.assertIn("Is the operating model clear?", q_texts)
        self.assertIn("Are system boundaries clear?", q_texts)
        self.assertIn("Is the manufacturing hierarchy coherent?", q_texts)
        self.assertIn("Is MES/MOM positioned correctly?", q_texts)
        self.assertIn("Are feedback loops represented?", q_texts)
        self.assertIn("Are quality mechanisms represented?", q_texts)
        self.assertIn("Is the constraint visible?", q_texts)
        self.assertIn("Does every KPI support a decision?", q_texts)
        self.assertIn("Are governance mechanisms visible?", q_texts)
        self.assertIn("Is there unnecessary visual complexity?", q_texts)

    def test_02_evaluate_enterprise_presentation(self):
        """Generate a complete narrative deck and evaluate it with the review engine."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.500)

        # Generate Solution Selling deck (Why -> What -> How -> Value)
        NarrativeIntelligenceEngine.render_narrative_deck(
            prs=prs,
            framework=NarrativeFramework.WHY_WHAT_HOW_VALUE,
            topic="Clean-Core SAP S/4HANA & MES MOM Transformation",
            client_name="Boeing Defense"
        )
        prs.save(self.TEST_DECK)
        self.assertTrue(os.path.exists(self.TEST_DECK))

        # Run review engine on saved presentation
        scorecard = ArchitectureReviewEngine.review_presentation(prs=Presentation(self.TEST_DECK))
        self.assertIsInstance(scorecard, ArchitectureReviewScorecard)
        self.assertEqual(len(scorecard.inquiry_results), 20)
        self.assertEqual(len(scorecard.lenses_evaluated), 13)

        # High-quality presentation should pass with Enterprise Architect Approved
        self.assertGreaterEqual(scorecard.overall_health_score, 80)
        self.assertIn(scorecard.rating, ["ENTERPRISE ARCHITECT APPROVED", "NEEDS REFINEMENT"])
        self.assertIn("APPROVED", scorecard.architectural_verdict)

    def test_03_mcp_review_tools(self):
        """Verify FastMCP list_architecture_review_lenses and review_presentation_architecture tools."""
        list_res = list_architecture_review_lenses()
        self.assertEqual(list_res["total_lenses"], 13)
        self.assertEqual(list_res["total_inquiries"], 20)

        # Review via text corpus
        corpus = """
        Business Problem: Production constrained by 4-hour batch replication lag in ECC causing machine starvations.
        Operating Model & Boundaries: Unification across global aerospace plants with air-gapped industrial edge and zero Z-table mods.
        ISA-95 Hierarchy: S/4HANA Level 4 ERP -> BTP Event Mesh -> Level 3 MES (DMC) -> Level 2 Edge IPC -> Level 1/0 PLCs.
        Quality & Constraints: First pass yield (FPY) at 91.2%, scrap expense $460k/mo. Bottleneck identified at CNC 5-Axis Bay.
        Feedback Loops: Closed-loop telemetry via OPC UA streams real-time cycle times back to financial ACDOCA ledger.
        Governance & Commercials: RACI steering committee with milestone gate criteria and 3.3-month payback.
        Data Lineage & Entities: Production Order (AUFNR), Material Master (MATNR), WIP batch genealogy.
        Risks & Assumptions: Risk matrix score low with redundant edge broker; explicit assumption of Gigabit LAN.
        Cockpit Questions: What changed, why does it matter, where is the problem, what should we act on.
        """
        review_res = review_presentation_architecture(text_corpus=corpus)
        self.assertEqual(review_res["status"], "success")
        self.assertGreaterEqual(review_res["overall_health_score"], 85)
        self.assertEqual(review_res["rating"], "ENTERPRISE ARCHITECT APPROVED")
        self.assertEqual(review_res["total_inquiries_evaluated"], 20)
        self.assertIn("Internal architectural diagnostic", review_res["confidentiality_note"])


if __name__ == "__main__":
    unittest.main()
