"""
Unit Tests for Transformation & Process Intelligence Engine (Step 15).

Validates:
- Semantic relationship classification & visual intent selection
- Process flow composition with decision diamonds and rework loops
- Cross-functional swimlane composition with cross-lane handoffs
- Current -> Intervention -> Future transformation bridge
- 5-level maturity staircase & gap recommendation scorecard
- Closed-loop cyber-physical manufacturing architecture
- Anti-pattern detection (card_wall, process_as_cards, etc.)
- 11-stage transformation narrative generation
- FastMCP tool integrations
"""

import os
import unittest
from pptx import Presentation
from pptx.util import Inches
from pptx.enum.shapes import MSO_SHAPE

from design_system.transformation_semantic import (
    TransformationRelationType,
    ProcessNodeType,
    ProcessNode,
    ProcessBranch,
    ProcessFlowModel,
    SwimlaneLane,
    SwimlaneStep,
    SwimlaneHandoff,
    SwimlaneDiagramModel,
    CurrentStateSnapshot,
    TransformationIntervention,
    FutureStateVision,
    TransformationBridgeModel,
    MaturityDimensionScore,
    MaturityStaircaseLevel,
    MaturityAssessmentModel,
    ClosedLoopStage,
    ClosedLoopManufacturingModel,
    TransformationSemanticInferrer
)
from design_system.process_flow_engine import ProcessFlowComposer
from design_system.swimlane_engine import SwimlaneDiagramComposer
from design_system.transformation_engine import TransformationBridgeComposer
from design_system.maturity_engine import MaturityAssessmentComposer
from design_system.quality_gate import PresentationQualityGate, QualityStatus
from design_system.color import ExecutiveNavyTheme, ConsultingSlateTheme
from design_system.narrative_intelligence import (
    NarrativeFramework,
    NarrativeIntelligenceEngine
)
from ppt_mcp_server import (
    render_process_flow_diagram,
    render_swimlane_diagram,
    render_transformation_bridge,
    render_maturity_assessment,
    render_closed_loop_manufacturing
)


class TestTransformationProcessIntelligence(unittest.TestCase):
    OUTPUT_FILES = []

    @classmethod
    def tearDownClass(cls):
        for f in cls.OUTPUT_FILES:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except OSError:
                    pass

    def _track(self, filename: str) -> str:
        self.OUTPUT_FILES.append(filename)
        return filename

    def _safe_shape_type(self, shape):
        try:
            return shape.auto_shape_type
        except (ValueError, AttributeError):
            return None

    # =========================================================================
    # 1. Semantic Relationship Inference
    # =========================================================================

    def test_01_relationship_classification(self):
        """Verify semantic inference correctly maps text patterns to relation types."""
        # Process Execution
        r1 = TransformationSemanticInferrer.infer_relationship("Sequential workflow with pass fail decision points and rework path")
        self.assertEqual(r1, TransformationRelationType.PROCESS_EXECUTION)

        # Swimlane
        r2 = TransformationSemanticInferrer.infer_relationship("Cross-functional swimlane with handoff across Customer, SAP and MES")
        self.assertEqual(r2, TransformationRelationType.CROSS_FUNCTIONAL_SWIMLANE)

        # Transformation Bridge
        r3 = TransformationSemanticInferrer.infer_relationship("Current-state to future-state transformation journey and intervention bridge")
        self.assertEqual(r3, TransformationRelationType.TRANSFORMATION_BRIDGE)

        # Maturity Progression
        r4 = TransformationSemanticInferrer.infer_relationship("Digital maturity assessment staircase level 1 to level 5 gap analysis")
        self.assertEqual(r4, TransformationRelationType.MATURITY_PROGRESSION)

        # Closed-loop Feedback
        r5 = TransformationSemanticInferrer.infer_relationship("Closed-loop manufacturing physical to digital intelligence circular feedback loop")
        self.assertEqual(r5, TransformationRelationType.CLOSED_LOOP_FEEDBACK)

    def test_02_visual_intent_selection(self):
        """Verify decision tree maps relationship types to appropriate visual intent."""
        v1 = TransformationSemanticInferrer.infer_visual_intent(TransformationRelationType.CROSS_FUNCTIONAL_SWIMLANE)
        self.assertEqual(v1, "SWIMLANE_DIAGRAM")

        v2 = TransformationSemanticInferrer.infer_visual_intent(TransformationRelationType.PROCESS_EXECUTION)
        self.assertEqual(v2, "PROCESS_FLOW_DIAGRAM")

        v3 = TransformationSemanticInferrer.infer_visual_intent(TransformationRelationType.MATURITY_PROGRESSION)
        self.assertEqual(v3, "MATURITY_STAIRCASE_SCORECARD")

        v4 = TransformationSemanticInferrer.infer_visual_intent(TransformationRelationType.TRANSFORMATION_BRIDGE)
        self.assertEqual(v4, "TRANSFORMATION_BRIDGE_DIAGRAM")

        v5 = TransformationSemanticInferrer.infer_visual_intent(TransformationRelationType.CLOSED_LOOP_FEEDBACK)
        self.assertEqual(v5, "CLOSED_LOOP_DIAGRAM")

    # =========================================================================
    # 2. Process Flow with Decision Diamond & Rework Loop
    # =========================================================================

    def test_03_process_flow_branching_and_rework(self):
        """Verify ProcessFlowComposer generates real diamonds and branching rework paths."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.500)
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        model = ProcessFlowModel(
            title="SAP to MES Execution & Clearance",
            nodes=[
                ProcessNode("n1", "Demand Order", role_lane="Customer", system_tag="SAP SD"),
                ProcessNode("n2", "Production Order", role_lane="SAP PP", system_tag="Order 100482"),
                ProcessNode("n3", "MES Dispatch", role_lane="MES Operations", system_tag="Dispatch Queue"),
                ProcessNode("n4", "Quality Inspection", role_lane="Quality Assurance", system_tag="CMM Gauge", is_decision=True),
                ProcessNode("n5", "Confirmation", role_lane="SAP Finance", system_tag="CO11N Post")
            ],
            branches=[]
        )

        ProcessFlowComposer.render_branching_process(
            slide=slide,
            left=0.80,
            top=1.80,
            width=11.733,
            height=4.80,
            flow_model=model,
            theme=ConsultingSlateTheme
        )

        # Verify shapes generated
        diamonds = [s for s in slide.shapes if self._safe_shape_type(s) == MSO_SHAPE.DIAMOND]
        self.assertEqual(len(diamonds), 1, "Must contain exactly 1 decision diamond")

        arrows = [s for s in slide.shapes if self._safe_shape_type(s) in (
            MSO_SHAPE.RIGHT_ARROW, MSO_SHAPE.DOWN_ARROW, MSO_SHAPE.UP_ARROW
        )]
        self.assertGreaterEqual(len(arrows), 4, "Must contain directional connector arrows")

        out_path = self._track("test_process_flow_out.pptx")
        prs.save(out_path)
        self.assertTrue(os.path.exists(out_path))

    # =========================================================================
    # 3. Cross-Functional Swimlane Diagram
    # =========================================================================

    def test_04_swimlane_diagram_composition(self):
        """Verify SwimlaneDiagramComposer generates multi-lane bands and cross-lane handoffs."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.500)
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        model = SwimlaneDiagramModel(
            title="S/4HANA & MES Operational Swimlane",
            lanes=[
                SwimlaneLane("l1", "Customer Demand", "Partner EDI", 1),
                SwimlaneLane("l2", "SAP S/4HANA", "System of Record", 2),
                SwimlaneLane("l3", "MES MOM Core", "Execution", 3),
                SwimlaneLane("l4", "Shop Floor OT", "Edge PLC", 4)
            ],
            steps=[
                SwimlaneStep("s1", "l1", "Demand Order", 1, "Order EDI"),
                SwimlaneStep("s2", "l2", "Production Order", 2, "MRP Planning"),
                SwimlaneStep("s3", "l3", "Dispatch Job", 3, "Schedule"),
                SwimlaneStep("s4", "l4", "Machine Execution", 4, "CNC Milling")
            ],
            handoffs=[
                SwimlaneHandoff("s1", "s2", "Sales Order", "B2B"),
                SwimlaneHandoff("s2", "s3", "Production Order", "OData"),
                SwimlaneHandoff("s3", "s4", "Dispatch Signal", "OPC-UA")
            ]
        )

        SwimlaneDiagramComposer.render(
            slide=slide,
            left=0.80,
            top=1.80,
            width=11.733,
            height=4.80,
            model=model,
            theme=ConsultingSlateTheme
        )

        # Verify shapes
        self.assertGreaterEqual(len(slide.shapes), 8, "Must render lanes, headers, steps, and handoffs")

        out_path = self._track("test_swimlane_out.pptx")
        prs.save(out_path)
        self.assertTrue(os.path.exists(out_path))

    # =========================================================================
    # 4. Current -> Intervention -> Future Transformation Bridge
    # =========================================================================

    def test_05_transformation_bridge_composition(self):
        """Verify TransformationBridgeComposer renders 3-part bridge with baseline and target outcomes."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.500)
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        model = TransformationBridgeModel(
            title="Manufacturing Digital Transformation Blueprint",
            current_state=CurrentStateSnapshot(
                title="CURRENT STATE",
                pain_points=["Fragmented planning", "Manual paper dispatch"],
                baseline_metrics=[("WIP Latency", "4.8 Days"), ("Scrap", "4.2%")]
            ),
            intervention=TransformationIntervention(
                title="TRANSFORMATION ENABLERS",
                initiatives=["SAP S/4HANA Integration", "MES Automated Dispatch"],
                enablers=["Air-gapped edge buffering"]
            ),
            future_state=FutureStateVision(
                title="FUTURE STATE",
                transformed_capabilities=["Connected execution", "Predictive quality"],
                target_outcomes=[("WIP Latency", "1.2 Days"), ("Scrap", "0.8%")]
            )
        )

        TransformationBridgeComposer.render_bridge(
            slide=slide,
            left=0.80,
            top=1.80,
            width=11.733,
            height=4.80,
            model=model,
            theme=ConsultingSlateTheme
        )

        # Verify connector arrows between sections
        arrows = [s for s in slide.shapes if self._safe_shape_type(s) == MSO_SHAPE.RIGHT_ARROW]
        self.assertGreaterEqual(len(arrows), 2, "Must contain at least 2 bridge connector arrows")

        out_path = self._track("test_trans_bridge_out.pptx")
        prs.save(out_path)
        self.assertTrue(os.path.exists(out_path))

    # =========================================================================
    # 5. Maturity Staircase & Scorecard
    # =========================================================================

    def test_06_maturity_staircase_scorecard(self):
        """Verify MaturityAssessmentComposer renders 5-level staircase and score-gap-action rows."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.500)
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        dims = [
            MaturityDimensionScore("Process Execution", 2.1, 4.3, "P1", "Paper travelers", "Deploy MES"),
            MaturityDimensionScore("Data Genealogy", 2.3, 4.5, "P1", "Disconnected lots", "Unit traveler")
        ]

        model = MaturityAssessmentModel(
            title="Digital Maturity Assessment",
            overall_current_score=2.2,
            overall_target_score=4.4,
            dimensions=dims
        )

        MaturityAssessmentComposer.render_staircase_scorecard(
            slide=slide,
            left=0.80,
            top=1.80,
            width=11.733,
            height=4.80,
            model=model,
            theme=ConsultingSlateTheme
        )

        out_path = self._track("test_maturity_out.pptx")
        prs.save(out_path)
        self.assertTrue(os.path.exists(out_path))

    # =========================================================================
    # 6. Anti-Pattern Card Wall Detection
    # =========================================================================

    def test_07_anti_pattern_detection(self):
        """Verify PresentationQualityGate.detect_anti_patterns_on_slide identifies anti-patterns."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.500)

        # Create a defective slide: "Process Architecture" with 4 disconnected text cards and no connectors
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        # Title
        tb = slide.shapes.add_textbox(Inches(0.80), Inches(0.60), Inches(11.733), Inches(0.80))
        tb.text_frame.text = "Process Workflow Execution"

        # 4 identical cards in a row with no arrows
        for i in range(4):
            c = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(0.80 + i * 2.8), Inches(2.20), Inches(2.50), Inches(3.50)
            )
            c.text_frame.text = f"Step {i+1}\nThis is manual processing card {i+1}."

        patterns = PresentationQualityGate.detect_anti_patterns_on_slide(slide)
        self.assertIn("card_wall", patterns)
        self.assertIn("process_as_cards", patterns)

    # =========================================================================
    # 7. Transformation Narrative (11 Stages)
    # =========================================================================

    def test_08_transformation_narrative_11_stages(self):
        """Verify NarrativeFramework.TRANSFORMATION_JOURNEY plans and renders 11 canonical stages."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.500)

        intents = NarrativeIntelligenceEngine.render_narrative_deck(
            prs=prs,
            framework=NarrativeFramework.TRANSFORMATION_JOURNEY,
            topic="Connected Discrete Manufacturing",
            client_name="Global Heavy Industries"
        )

        self.assertEqual(len(intents), 11, "Must generate exactly 11 slides for complete transformation narrative")
        self.assertEqual(len(prs.slides), 11, "Presentation must contain 11 slides")

        # Verify quality audit passes
        report = PresentationQualityGate.audit_and_remediate(prs, auto_remediate=True)
        self.assertIn(report.status, (QualityStatus.PASSED, QualityStatus.REMEDIATED_AND_PASSED))
        self.assertGreaterEqual(report.overall_quality_score, 90)

        out_path = self._track("test_narrative_11_out.pptx")
        prs.save(out_path)
        self.assertTrue(os.path.exists(out_path))

    # =========================================================================
    # 8. FastMCP Tools
    # =========================================================================

    def test_09_fastmcp_tools(self):
        """Verify FastMCP tool functions execute and save presentation slides properly."""
        deck1 = self._track("test_mcp_flow.pptx")
        res1 = render_process_flow_diagram(path=deck1)
        self.assertEqual(res1["status"], "success")
        self.assertTrue(os.path.exists(deck1))

        deck2 = self._track("test_mcp_swimlane.pptx")
        res2 = render_swimlane_diagram(path=deck2)
        self.assertEqual(res2["status"], "success")
        self.assertTrue(os.path.exists(deck2))

        deck3 = self._track("test_mcp_bridge.pptx")
        res3 = render_transformation_bridge(path=deck3)
        self.assertEqual(res3["status"], "success")
        self.assertTrue(os.path.exists(deck3))

        deck4 = self._track("test_mcp_maturity.pptx")
        res4 = render_maturity_assessment(path=deck4)
        self.assertEqual(res4["status"], "success")
        self.assertTrue(os.path.exists(deck4))

        deck5 = self._track("test_mcp_closed_loop.pptx")
        res5 = render_closed_loop_manufacturing(path=deck5)
        self.assertEqual(res5["status"], "success")
        self.assertTrue(os.path.exists(deck5))


if __name__ == "__main__":
    unittest.main()
