"""
Test Suite for Manufacturing Enterprise Architecture Semantic Vocabulary.

Validates that:
1. Vocabulary recognizes entities across all 6 domains:
   - ENTERPRISE (Business Unit, Plant, Site, Customer, Supplier)
   - SAP / ERP (S/4HANA, Orders, Material, BOM, Routing, Work Center, Batch, Serial, Inventory)
   - MANUFACTURING (MES, MOM, Work Order, Operation, WIP, Machine, Operator, Shift)
   - QUALITY (Characteristic, Specification, Tolerance, Defect, NCR, CAPA, Calibration)
   - TRACEABILITY (Serial, Batch, Component, Genealogy, As-Built, Parent, Child)
   - INTEGRATION (API, OData, IDoc, Event, Message, Middleware, BTP, Edge, OPC UA, MQTT)
2. Detects multi-entity relational patterns:
   - SAP -> MES                          => Integration relationship (NOT two cards)
   - Production Order -> Operation -> WIP => Manufacturing process flow
   - Serial -> Components -> Parameters  => Genealogy / As-Built tree
   - Plant -> Work Center -> Machine     => Operational hierarchy
   - KPI -> Business Decision -> Action  => Decision loop / Outcome chain
   - Tolerance -> Defect -> NCR -> CAPA  => Exception / Rework flow
3. Faithfully represents supplied architecture without inventing unstated integrations.
4. MCP tool 'analyze_manufacturing_semantics' executes successfully.
"""

from design_system.manufacturing_vocabulary import (
    ManufacturingSemanticAnalyzer,
    EntityCategory,
    SemanticPatternType,
    MANUFACTURING_VOCABULARY
)
import ppt_mcp_server as mcp_server


def test_entity_extraction():
    """Verify entity extraction across all 6 domains."""
    sample_text = (
        "In our Bangalore Plant, S/4HANA dispatches a Production Order for Material MAT-9021. "
        "The MES workstation tracks Operation 0020, WIP movement, and machine cycle times. "
        "Quality inspectors log Tolerance deviations and file an NCR for defect triage. "
        "Complete Genealogy links the Serial Number to component lot batches. "
        "OPC UA collectors stream telemetry via BTP Event Mesh directly into Power BI."
    )

    entities = ManufacturingSemanticAnalyzer.extract_entities(sample_text)
    assert len(entities) >= 10, f"Expected at least 10 entities, found {len(entities)}"

    categories_found = {e.category for e in entities}
    assert EntityCategory.ENTERPRISE in categories_found
    assert EntityCategory.SAP_ERP in categories_found
    assert EntityCategory.MANUFACTURING in categories_found
    assert EntityCategory.QUALITY in categories_found
    assert EntityCategory.TRACEABILITY in categories_found
    assert EntityCategory.INTEGRATION in categories_found

    print(f"[PASS] Successfully extracted {len(entities)} entities across all 6 enterprise domains.")


def test_core_relational_patterns():
    """Verify the exact relationship patterns specified in the user request."""

    # 1. SAP -> MES
    text_1 = "Real-time bidirectional synchronization from SAP S/4HANA to shop floor MES edge terminals."
    patterns_1 = ManufacturingSemanticAnalyzer.detect_relational_patterns(text_1)
    assert len(patterns_1) > 0
    assert patterns_1[0].pattern_type == SemanticPatternType.INTEGRATION_FLOW
    assert patterns_1[0].recommended_primitive == "integration_architecture"
    print("[PASS] 'SAP -> MES' recognized as Integration Architecture (not two cards).")

    # 2. Production Order -> Operation -> Material -> WIP
    text_2 = "Production Order release routing to Operation sequence with raw Material staging and WIP tracking."
    patterns_2 = ManufacturingSemanticAnalyzer.detect_relational_patterns(text_2)
    assert len(patterns_2) > 0
    assert patterns_2[0].pattern_type == SemanticPatternType.MANUFACTURING_FLOW
    assert patterns_2[0].recommended_primitive == "horizontal_process_flow"
    print("[PASS] 'Production Order -> Operation -> Material -> WIP' recognized as Manufacturing Process Flow.")

    # 3. Serial Number -> Components -> Process Parameters -> Quality Results
    text_3 = "Serial Number traceability linking sub-assembly component lots with machine process parameters and quality inspection results."
    patterns_3 = ManufacturingSemanticAnalyzer.detect_relational_patterns(text_3)
    assert len(patterns_3) > 0
    assert patterns_3[0].pattern_type == SemanticPatternType.GENEALOGY_TRACEABILITY
    assert patterns_3[0].recommended_primitive == "genealogy_tree"
    print("[PASS] 'Serial Number -> Components -> Parameters' recognized as Genealogy Tree.")

    # 4. Plant -> Work Center -> Machine -> Operator -> Shift
    text_4 = "Operational hierarchy decomposing Bangalore Plant into Work Center bays, CNC Machine cells, Operator credentials, and Shift rosters."
    patterns_4 = ManufacturingSemanticAnalyzer.detect_relational_patterns(text_4)
    assert len(patterns_4) > 0
    assert patterns_4[0].pattern_type == SemanticPatternType.OPERATIONAL_HIERARCHY
    assert patterns_4[0].recommended_primitive == "enterprise_to_shopfloor"
    print("[PASS] 'Plant -> Work Center -> Machine -> Operator -> Shift' recognized as Operational Hierarchy.")

    # 5. KPI -> Business Decision -> Action
    text_5 = "Shop floor OEE KPI telemetry triggering closed-loop management business decision and corrective action."
    patterns_5 = ManufacturingSemanticAnalyzer.detect_relational_patterns(text_5)
    assert len(patterns_5) > 0
    assert patterns_5[0].pattern_type == SemanticPatternType.DECISION_LOOP
    assert patterns_5[0].recommended_primitive == "decision_flow"
    print("[PASS] 'KPI -> Business Decision -> Action' recognized as Decision Loop.")

    # 6. Quality Exception: Tolerance -> Defect -> NCR -> CAPA -> Rework
    text_6 = "Tolerance breach triggering defect classification, automated NCR creation, and rework loopback."
    patterns_6 = ManufacturingSemanticAnalyzer.detect_relational_patterns(text_6)
    assert len(patterns_6) > 0
    assert patterns_6[0].pattern_type == SemanticPatternType.QUALITY_EXCEPTION
    assert patterns_6[0].recommended_primitive == "exception_rework_flow"
    print("[PASS] 'Tolerance -> Defect -> NCR -> CAPA -> Rework' recognized as Exception Rework Flow.")


def test_faithful_representation():
    """Ensure engine does not invent unstated technical integrations."""
    plain_text = "The machine operator works on shift A with standard tools."
    patterns = ManufacturingSemanticAnalyzer.detect_relational_patterns(plain_text)
    # Should NOT invent SAP, BTP, or Kafka integrations
    for p in patterns:
        assert p.pattern_type != SemanticPatternType.INTEGRATION_FLOW, (
            "Anti-pattern: Integration flow was falsely invented for text without ERP/integration nodes!"
        )
    print("[PASS] Faithfulness verified: No unstated technical integrations invented.")


def test_mcp_tool_analyze_semantics():
    """Verify FastMCP analyze_manufacturing_semantics tool."""
    query = "SAP S/4HANA pushes production orders through BTP Event Mesh to plant MES edge nodes."
    res = mcp_server.analyze_manufacturing_semantics(query)

    assert res["total_entities_found"] >= 4
    assert len(res["relational_patterns_detected"]) > 0
    assert res["recommended_visual_primitive"] == "integration_architecture"
    print(f"[PASS] FastMCP analyze_manufacturing_semantics verified: Recommended '{res['recommended_visual_primitive']}'.")


if __name__ == "__main__":
    test_entity_extraction()
    test_core_relational_patterns()
    test_faithful_representation()
    test_mcp_tool_analyze_semantics()
    print("\nALL MANUFACTURING SEMANTIC VOCABULARY TESTS PASSED SUCCESSFULLY!")
