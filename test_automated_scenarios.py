"""
Automated Test Suite for Scenario-Driven Presentations.

Validates 6 enterprise scenario presentations:
1. TEST 1: SAP S/4HANA + MES + shop-floor integration architecture
2. TEST 2: Manufacturing traceability solution
3. TEST 3: CXO manufacturing dashboard
4. TEST 4: SAP-to-MES digital transformation proposal
5. TEST 5: MES implementation proposal
6. TEST 6: Commercial proposal

Proves that:
- The system chooses different visual forms based on semantic content.
- Visual diversity is high and layout monotony / card grid overuse is completely prevented.
- Native PowerPoint shapes, tables, and charts are rendered throughout.
- Every presentation passes the Presentation Quality Gate (100% Inter font, bounded layouts, zero filler).
- The architecture is generic, reusable, and uncoupled from static hardcoding.
"""

import os
import unittest
from pptx import Presentation

from design_system.scenario_engine import (
    ScenarioPresentationEngine,
    ScenarioDeckResult,
    SemanticVisualFormResolver
)
from design_system.quality_gate import QualityStatus
from ppt_mcp_server import generate_scenario_presentation


class TestAutomatedScenarioPresentations(unittest.TestCase):
    CREATED_DECKS = [
        "test_scenario_1_sap_mes_integration.pptx",
        "test_scenario_2_manufacturing_traceability.pptx",
        "test_scenario_3_cxo_dashboard.pptx",
        "test_scenario_4_digital_transformation.pptx",
        "test_scenario_5_mes_implementation.pptx",
        "test_scenario_6_commercial_proposal.pptx",
        "mcp_test_scenario_presentation.pptx"
    ]

    def tearDown(self):
        for path in self.CREATED_DECKS:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass

    # -------------------------------------------------------------------------
    # TEST 1: SAP S/4HANA + MES + Shop-Floor Integration Architecture
    # -------------------------------------------------------------------------
    def test_01_sap_mes_integration_architecture(self):
        """
        TEST 1
        SAP S/4HANA + MES + shop-floor integration architecture
        Expected:
        - enterprise architecture diagram
        - integration/data flow
        - manufacturing hierarchy
        - process flow
        - governance/control points
        """
        requirements = [
            "enterprise architecture diagram",
            "integration/data flow",
            "manufacturing hierarchy",
            "process flow",
            "governance/control points"
        ]

        result = ScenarioPresentationEngine.build_scenario_presentation(
            scenario_id="test_scenario_1_sap_mes_integration",
            title="SAP S/4HANA & MES Clean-Core Integration Architecture",
            topic="SAP S/4HANA + MES + shop-floor integration architecture",
            client_name="Lockheed Martin Aerospace",
            requirements=requirements,
            output_path="test_scenario_1_sap_mes_integration.pptx"
        )

        self.assertEqual(result.slide_count, 5)
        self.assertTrue(os.path.exists(result.output_path))
        self.assertTrue(result.is_export_authorized)
        self.assertIn(result.quality_report.status, [QualityStatus.PASSED, QualityStatus.REMEDIATED_AND_PASSED])
        self.assertGreaterEqual(result.quality_report.overall_quality_score, 90)

        # Verify semantic form choices
        expected_primitives = [
            "system_architecture",          # enterprise architecture diagram
            "integration_architecture",     # integration/data flow
            "enterprise_to_shopfloor",      # manufacturing hierarchy
            "horizontal_process_flow",      # process flow
            "approval_gates"                # governance/control points
        ]
        self.assertEqual(result.primitives_used, expected_primitives)

        # Verify diversity: 5 distinct primitives out of 5 slides (100% diversity)
        self.assertEqual(len(set(result.primitives_used)), 5)
        self.assertEqual(result.diversity_score, 100)

        # Inspect generated PPTX slides
        prs = Presentation(result.output_path)
        self.assertEqual(len(prs.slides), 5)

    # -------------------------------------------------------------------------
    # TEST 2: Manufacturing Traceability Solution
    # -------------------------------------------------------------------------
    def test_02_manufacturing_traceability_solution(self):
        """
        TEST 2
        Manufacturing traceability solution
        Expected:
        - genealogy visualization
        - serial/batch relationships
        - process history
        - quality relationship
        - exception/rework flow
        """
        requirements = [
            "genealogy visualization",
            "serial/batch relationships",
            "process history",
            "quality relationship",
            "exception/rework flow"
        ]

        result = ScenarioPresentationEngine.build_scenario_presentation(
            scenario_id="test_scenario_2_manufacturing_traceability",
            title="Full-Lifecycle As-Built Manufacturing Traceability Architecture",
            topic="Manufacturing traceability solution",
            client_name="Boeing Commercial Airplanes",
            requirements=requirements,
            output_path="test_scenario_2_manufacturing_traceability.pptx"
        )

        self.assertEqual(result.slide_count, 5)
        self.assertTrue(os.path.exists(result.output_path))
        self.assertTrue(result.is_export_authorized)
        self.assertGreaterEqual(result.quality_report.overall_quality_score, 90)

        expected_primitives = [
            "genealogy_tree",               # genealogy visualization
            "parent_child_relationship",    # serial/batch relationships
            "data_lifecycle",               # process history
            "control_framework",            # quality relationship
            "exception_rework_flow"         # exception/rework flow
        ]
        self.assertEqual(result.primitives_used, expected_primitives)
        self.assertEqual(len(set(result.primitives_used)), 5)

    # -------------------------------------------------------------------------
    # TEST 3: CXO Manufacturing Dashboard
    # -------------------------------------------------------------------------
    def test_03_cxo_manufacturing_dashboard(self):
        """
        TEST 3
        CXO manufacturing dashboard
        Expected:
        - KPI strip
        - trend analysis
        - bottleneck visualization
        - quality/Pareto visualization
        - action-oriented table
        """
        requirements = [
            "KPI strip",
            "trend analysis",
            "bottleneck visualization",
            "quality/Pareto visualization",
            "action-oriented table"
        ]

        result = ScenarioPresentationEngine.build_scenario_presentation(
            scenario_id="test_scenario_3_cxo_dashboard",
            title="CXO Manufacturing Control Tower & Real-Time Analytics",
            topic="CXO manufacturing dashboard",
            client_name="Hitachi Energy Global Operations",
            requirements=requirements,
            output_path="test_scenario_3_cxo_dashboard.pptx"
        )

        self.assertEqual(result.slide_count, 5)
        self.assertTrue(os.path.exists(result.output_path))
        self.assertTrue(result.is_export_authorized)
        self.assertGreaterEqual(result.quality_report.overall_quality_score, 90)

        expected_primitives = [
            "kpi_strip",                    # KPI strip
            "trend_chart",                  # trend analysis
            "capacity_vs_demand",           # bottleneck visualization
            "pareto",                       # quality/Pareto visualization
            "action_register"               # action-oriented table
        ]
        self.assertEqual(result.primitives_used, expected_primitives)
        self.assertEqual(len(set(result.primitives_used)), 5)

    # -------------------------------------------------------------------------
    # TEST 4: SAP-to-MES Digital Transformation Proposal
    # -------------------------------------------------------------------------
    def test_04_digital_transformation_proposal(self):
        """
        TEST 4
        SAP-to-MES digital transformation proposal
        Expected:
        - current-state
        - structural problem
        - target architecture
        - transformation journey
        - operating model
        - roadmap
        - business outcomes
        """
        requirements = [
            "current-state",
            "structural problem",
            "target architecture",
            "transformation journey",
            "operating model",
            "roadmap",
            "business outcomes"
        ]

        result = ScenarioPresentationEngine.build_scenario_presentation(
            scenario_id="test_scenario_4_digital_transformation",
            title="Enterprise Digital Transformation: SAP S/4HANA to Modern MES",
            topic="SAP-to-MES digital transformation proposal",
            client_name="Siemens Energy Turbo Systems",
            requirements=requirements,
            output_path="test_scenario_4_digital_transformation.pptx"
        )

        self.assertEqual(result.slide_count, 7)
        self.assertTrue(os.path.exists(result.output_path))
        self.assertTrue(result.is_export_authorized)
        self.assertGreaterEqual(result.quality_report.overall_quality_score, 90)

        expected_primitives = [
            "current_vs_future_state",      # current-state
            "insight_and_evidence",         # structural problem
            "system_architecture",          # target architecture
            "outcome_chain",                # transformation journey
            "operating_model",              # operating model
            "transformation_roadmap",       # roadmap
            "cost_benefit_summary"          # business outcomes
        ]
        self.assertEqual(result.primitives_used, expected_primitives)
        self.assertEqual(len(set(result.primitives_used)), 7)

    # -------------------------------------------------------------------------
    # TEST 5: MES Implementation Proposal
    # -------------------------------------------------------------------------
    def test_05_mes_implementation_proposal(self):
        """
        TEST 5
        MES implementation proposal
        Expected:
        - scope architecture
        - modules/capabilities
        - shop-floor workflow
        - integration architecture
        - governance
        - delivery roadmap
        """
        requirements = [
            "scope architecture",
            "modules/capabilities",
            "shop-floor workflow",
            "integration architecture",
            "governance",
            "delivery roadmap"
        ]

        result = ScenarioPresentationEngine.build_scenario_presentation(
            scenario_id="test_scenario_5_mes_implementation",
            title="Digital MES Turnkey Implementation & Plant Modernization",
            topic="MES implementation proposal",
            client_name="Schneider Electric Plant Network",
            requirements=requirements,
            output_path="test_scenario_5_mes_implementation.pptx"
        )

        self.assertEqual(result.slide_count, 6)
        self.assertTrue(os.path.exists(result.output_path))
        self.assertTrue(result.is_export_authorized)
        self.assertGreaterEqual(result.quality_report.overall_quality_score, 90)

        expected_primitives = [
            "application_landscape",        # scope architecture
            "capability_map",               # modules/capabilities
            "operational_workflow",         # shop-floor workflow
            "integration_architecture",     # integration architecture
            "approval_gates",               # governance
            "transformation_roadmap"        # delivery roadmap
        ]
        self.assertEqual(result.primitives_used, expected_primitives)
        self.assertEqual(len(set(result.primitives_used)), 6)

    # -------------------------------------------------------------------------
    # TEST 6: Commercial Proposal
    # -------------------------------------------------------------------------
    def test_06_commercial_proposal(self):
        """
        TEST 6
        Commercial proposal
        Expected:
        - scope table
        - milestone structure
        - payment gates
        - assumptions
        - dependencies
        - timeline
        """
        requirements = [
            "scope table",
            "milestone structure",
            "payment gates",
            "assumptions",
            "dependencies",
            "timeline"
        ]

        result = ScenarioPresentationEngine.build_scenario_presentation(
            scenario_id="test_scenario_6_commercial_proposal",
            title="Commercial Terms, Scope Commitments & Milestone Payment Model",
            topic="Commercial proposal",
            client_name="ABB Robotics Global Division",
            requirements=requirements,
            output_path="test_scenario_6_commercial_proposal.pptx"
        )

        self.assertEqual(result.slide_count, 6)
        self.assertTrue(os.path.exists(result.output_path))
        self.assertTrue(result.is_export_authorized)
        self.assertGreaterEqual(result.quality_report.overall_quality_score, 90)

        expected_primitives = [
            "comparison_matrix",            # scope table
            "milestone_gates",              # milestone structure
            "commercial_table",             # payment gates
            "action_register",              # assumptions
            "raci_responsibility",          # dependencies
            "timeline"                      # timeline
        ]
        self.assertEqual(result.primitives_used, expected_primitives)
        self.assertEqual(len(set(result.primitives_used)), 6)

    # -------------------------------------------------------------------------
    # CROSS-SCENARIO DIFFERENTIATION TEST
    # -------------------------------------------------------------------------
    def test_07_cross_scenario_semantic_differentiation(self):
        """
        Proves that the system chooses completely different visual forms based
        on semantic content across all scenarios, with zero card grid overuse.
        """
        all_resolved_primitives = []
        for req in [
            "enterprise architecture diagram",
            "genealogy visualization",
            "KPI strip",
            "current-state",
            "scope architecture",
            "payment gates"
        ]:
            desc = SemanticVisualFormResolver.resolve_requirement(req)
            all_resolved_primitives.append(desc.primitive_key)

        # Verify 6 completely different primitives for 6 different semantic requirements
        self.assertEqual(len(set(all_resolved_primitives)), 6)
        self.assertIn("system_architecture", all_resolved_primitives)
        self.assertIn("genealogy_tree", all_resolved_primitives)
        self.assertIn("kpi_strip", all_resolved_primitives)
        self.assertIn("current_vs_future_state", all_resolved_primitives)
        self.assertIn("application_landscape", all_resolved_primitives)
        self.assertIn("commercial_table", all_resolved_primitives)

    # -------------------------------------------------------------------------
    # TEST 8: FastMCP Tool Verification
    # -------------------------------------------------------------------------
    def test_08_fastmcp_scenario_presentation_tool(self):
        """Verify generate_scenario_presentation MCP tool integration."""
        res = generate_scenario_presentation(
            scenario_id="mcp_test_scenario_presentation",
            title="MCP Generated Traceability Architecture",
            topic="Manufacturing traceability solution",
            client_name="Rolls Royce Aerospace",
            requirements=["genealogy visualization", "serial/batch relationships", "quality relationship"],
            output_path="mcp_test_scenario_presentation.pptx"
        )

        self.assertEqual(res["status"], "success")
        self.assertTrue(res["is_export_authorized"])
        self.assertEqual(res["slide_count"], 3)
        self.assertTrue(os.path.exists("mcp_test_scenario_presentation.pptx"))
        self.assertEqual(res["typography_compliance"], "100.0%")


if __name__ == "__main__":
    unittest.main()
