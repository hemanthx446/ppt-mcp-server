"""
Unit Test Suite for Semantic Visual Intelligence Layer.
Verifies the 6 architectural questions and visual representation selection hierarchy.
"""

from design_system import (
    AudienceType,
    InformationRelationship,
    VisualRepresentation,
    VisualIntelligenceEngine,
    SlideContext,
    CompositeSlideSpec
)

def test_visual_intent_classification():
    print("\n--- Testing Visual Intent & Relationship Classification ---")

    test_cases = [
        # 1. Systems and their relationships -> ARCHITECTURE_DIAGRAM
        (
            "Enterprise Architecture Diagram: The Air-Gapped Pipeline",
            "TECHNICAL ARCHITECTURE BLUEPRINT",
            "Decoupled multi-tier stack isolating SAP from shop-floor transactions",
            VisualRepresentation.ARCHITECTURE_DIAGRAM,
            InformationRelationship.COMPONENT_STRUCTURE
        ),
        # 2. Systems exchanging information -> INTEGRATION_FLOW
        (
            "Real-Time Delta Synchronization & OData Message Broker",
            "INTEGRATION PIPELINE",
            "Bi-directional event mesh and API streaming between S/4HANA and edge terminals",
            VisualRepresentation.INTEGRATION_FLOW,
            InformationRelationship.EXCHANGE_FLOW
        ),
        # 3. Sequence of operational steps with Poka-Yoke -> JOURNEY_WORKFLOW
        (
            "Workstation Quality Enforcement & Hardware Poka-Yoke",
            "SHOP-FLOOR OPERATIONAL JOURNEY",
            "Assembly bay barcode scanning stopping unverified component mount",
            VisualRepresentation.JOURNEY_WORKFLOW,
            InformationRelationship.OPERATIONAL_JOURNEY
        ),
        # 4. Parent-child genealogy -> GENEALOGY_GRAPH
        (
            "360° As-Built Genealogy & Multi-Tier Indented BOM Lineage",
            "TRACEABILITY & AUDIT COMPLIANCE",
            "Bi-directional component-to-part genealogy tree for AS9100 customer defense audits",
            VisualRepresentation.GENEALOGY_GRAPH,
            InformationRelationship.GENEALOGICAL_LINEAGE
        ),
        # 5. Current vs Future State -> AS_IS_TO_BE
        (
            "The Aerospace Manufacturing Reality: 3 Operating Disconnects",
            "PROBLEM CONTEXT & OPERATIONAL PAIN",
            "Why high-reliability manufacturing struggles with legacy paper travelers vs target state",
            VisualRepresentation.AS_IS_TO_BE,
            InformationRelationship.CONTRAST_TENSION
        ),
        # 6. Transformation stages -> TRANSFORMATION_ROADMAP
        (
            "90-Day Agile Implementation Roadmap & Hypercare Rollout",
            "PROJECT PLAN & MILESTONES",
            "Five structured rollout stages ensuring rapid deployment with zero operational risk",
            VisualRepresentation.TRANSFORMATION_ROADMAP,
            InformationRelationship.TRANSFORMATION_STAGES
        ),
        # 7. Timeline / temporal schedule -> TIMELINE
        (
            "52-Week Sourcing Pipeline & Master Production Schedule",
            "PROCUREMENT TIMELINE",
            "Rolling 52-week PO release horizon across multi-year defense programs",
            VisualRepresentation.TIMELINE,
            InformationRelationship.TEMPORAL_MILESTONES
        ),
        # 8. Governance / approvals -> CONTROL_GATES
        (
            "Two-Tier Operational Approval Desk & Quality Gatekeeper",
            "OPERATIONAL GOVERNANCE & CONTROL",
            "Supervisor verification and QC stamp generating verified Ready-to-Post slips",
            VisualRepresentation.CONTROL_GATES,
            InformationRelationship.GOVERNANCE_CONTROL
        ),
        # 9. KPI performance & cockpit -> EXECUTIVE_DASHBOARD
        (
            "Executive Cash Flow & Operational Fulfillment Cockpit",
            "EXECUTIVE DASHBOARD 1 | DAILY - WEEKLY - MONTHLY",
            "Real-time visibility into customer SLAs, OTIF %, and machine line utilization",
            VisualRepresentation.EXECUTIVE_DASHBOARD,
            InformationRelationship.QUANTITATIVE_PERFORMANCE
        ),
        # 10. Structured business information matrix -> TABLE_MATRIX
        (
            "The 5 W’s Strategic Evaluation Matrix",
            "GOVERNANCE & IMPACT MATRIX",
            "Mapping Organizational Personas, Data Entities, Cadences, and P&L Drivers across Cockpits",
            VisualRepresentation.TABLE_MATRIX,
            InformationRelationship.STRUCTURED_ATTRIBUTES
        ),
        # 11. Financial or commercial information -> COMMERCIAL_TABLE
        (
            "Turnkey Commercial Investment & Milestone Pricing Framework",
            "COMMERCIAL PROPOSAL",
            "Fixed-price implementation backed by milestone invoicing and 60-day hypercare warranty",
            VisualRepresentation.COMMERCIAL_TABLE,
            InformationRelationship.FINANCIAL_COMMERCIAL
        ),
        # 12. Alternatives / Trade-offs -> DECISION_MATRIX
        (
            "Middleware Architecture Evaluation & Decision Trade-Offs",
            "STRATEGIC EVALUATION",
            "Multi-criteria comparison scoring across direct RFC vs BTP Event Mesh vs Custom Gateway",
            VisualRepresentation.DECISION_MATRIX,
            InformationRelationship.DECISION_EVALUATION
        ),
        # 13. Risks -> RISK_MATRIX
        (
            "Enterprise Risk Mitigation & Cyber Perimeter Heatmap",
            "RISK & RESILIENCE MATRIX",
            "Severity and probability scoring across edge network failure scenarios and mitigations",
            VisualRepresentation.RISK_MATRIX,
            InformationRelationship.RISK_PROBABILITY_IMPACT
        ),
        # 14. Business outcomes (cause and effect) -> OUTCOME_CHAIN
        (
            "Quantified Free Cash Flow Acceleration & Working Capital Payback",
            "BUSINESS VALUE REALIZATION",
            "EBITDA expansion through scrap reduction and ₹14.2M trapped inventory release",
            VisualRepresentation.OUTCOME_CHAIN,
            InformationRelationship.CAUSE_AND_EFFECT
        ),
        # 15. Independent peer concepts -> CARD_GRID
        (
            "Overview of Three Independent Regional Operating Entities",
            "ORGANIZATIONAL OVERVIEW",
            "Autonomous business divisions operating parallel discrete lines",
            VisualRepresentation.CARD_GRID,
            InformationRelationship.INDEPENDENT_PEER_CONCEPTS
        )
    ]

    for title, cat, sub, exp_visual, exp_rel in test_cases:
        ctx = VisualIntelligenceEngine.classify_intent(title=title, category=cat, narrative_subtitle=sub)
        print(f"\nEvaluating: '{title[:40]}...'")
        print(f"  -> Audience: {ctx.audience.name}")
        print(f"  -> Relationship: {ctx.information_relationship.name} (Expected: {exp_rel.name})")
        print(f"  -> Visual Representation: {ctx.visual_representation.name} (Expected: {exp_visual.name})")
        print(f"  -> Business Question: {ctx.business_question}")
        print(f"  -> Decision Supported: {ctx.decision_supported}")
        assert ctx.visual_representation == exp_visual, f"Failed for {title}: got {ctx.visual_representation}, expected {exp_visual}"
        assert ctx.information_relationship == exp_rel, f"Failed rel for {title}: got {ctx.information_relationship}, expected {exp_rel}"

    print("\nALL 15 VISUAL REPRESENTATION CLASSIFICATIONS MATCHED EXACTLY!")


def test_composite_slide_composition():
    print("\n--- Testing Multi-Primitive Composite Slide Composition ---")

    # Composite Spec: Title + Architecture Diagram + Bottom Guarantee Banner
    spec = VisualIntelligenceEngine.compose_slide_spec(
        title="Enterprise Architecture Diagram: The Air-Gapped Operational Pipeline",
        category_tag="TECHNICAL ARCHITECTURE BLUEPRINT",
        narrative_subtitle="Decoupled multi-tier flow isolating SAP from shop-floor transactions while ensuring 100% operational fidelity",
        content_elements=["Tier 1: Core", "Tier 2: Middleware", "Tier 3: Edge"],
        callout_banner="Zero direct write calls to SAP database tables. Live ERP remains 100% unharmed."
    )

    assert spec.primary_representation == VisualRepresentation.ARCHITECTURE_DIAGRAM
    assert spec.is_dark == True, "Architecture slide should default to Executive Dark"
    assert len(spec.slots) == 2, f"Expected 2 slots (Main Stage + Bottom Banner), got {len(spec.slots)}"
    assert spec.slots[0].role == "MAIN_STAGE"
    assert spec.slots[0].height_ratio == 0.75
    assert spec.slots[1].role == "BOTTOM_CALLOUT"
    assert spec.slots[1].height_ratio == 0.25

    print(f"Verified Composite Spec: '{spec.title}'")
    print(f"  Primary: {spec.primary_representation.name} | Theme: {'Dark' if spec.is_dark else 'Light'}")
    print(f"  Slot 0: {spec.slots[0].role} ({spec.slots[0].primitive_type}) - Height: {spec.slots[0].height_ratio*100:.0f}%")
    print(f"  Slot 1: {spec.slots[1].role} ({spec.slots[1].primitive_type}) - Height: {spec.slots[1].height_ratio*100:.0f}%")

    # Composite Spec 2: Executive Dashboard with Top KPI Strip + Main Action Grid
    spec2 = VisualIntelligenceEngine.compose_slide_spec(
        title="Executive Cash Flow & Operational Fulfillment Cockpit",
        category_tag="EXECUTIVE DASHBOARD",
        narrative_subtitle="Real-time visibility into customer SLAs, OTIF %, and machine line utilization",
        content_elements=[]
    )
    assert spec2.primary_representation == VisualRepresentation.EXECUTIVE_DASHBOARD
    assert len(spec2.slots) >= 2, "Dashboard should split into Top Metric Strip + Main Proof Stage"
    assert spec2.slots[0].role == "TOP_METRIC_STRIP"
    assert spec2.slots[1].role == "MAIN_STAGE"
    print(f"Verified Dashboard Spec: Slot 0={spec2.slots[0].role}, Slot 1={spec2.slots[1].role}")

    print("\nALL COMPOSITE SLIDE COMPOSITION TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_visual_intent_classification()
    test_composite_slide_composition()
    print("\nALL SEMANTIC VISUAL INTELLIGENCE TESTS PASSED SUCCESSFULLY!")
