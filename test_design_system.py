"""
Automated Test Suite for Presentation Design System.
Verifies typography tokens, spacing grid math, semantic models, and PPTX rendering.
"""

import os
from pptx import Presentation
from design_system import (
    FONT_FAMILY,
    TypographySystem,
    SpacingSystem,
    CanvasBounds,
    Margins,
    GridCalculator,
    ColorSystem,
    VisualIntent,
    SemanticSlide,
    ArchitectureTier,
    TableData,
    KeyMetric,
    ContentBlock,
    RoadmapPhase,
    PPTXRenderer
)

def test_typography_tokens():
    print("\n--- Testing Typography Tokens ---")
    tokens = [
        ("presentation_title", TypographySystem.PRESENTATION_TITLE, 32.0, True),
        ("section_title", TypographySystem.SECTION_TITLE, 24.0, True),
        ("slide_title", TypographySystem.SLIDE_TITLE, 19.0, True),
        ("subtitle", TypographySystem.SUBTITLE, 11.0, False),
        ("body", TypographySystem.BODY, 10.5, False),
        ("label", TypographySystem.LABEL, 8.5, True),
        ("kpi_number", TypographySystem.KPI_NUMBER, 24.0, True),
        ("kpi_label", TypographySystem.KPI_LABEL, 9.0, True),
        ("table_header", TypographySystem.TABLE_HEADER, 8.5, True),
        ("table_body", TypographySystem.TABLE_BODY, 8.0, False),
        ("annotation", TypographySystem.ANNOTATION, 8.2, True),
        ("caption", TypographySystem.CAPTION, 7.5, False),
        ("footnote", TypographySystem.FOOTNOTE, 8.0, False),
    ]

    for name, token, exp_size, exp_bold in tokens:
        assert token.font_name == FONT_FAMILY, f"{name} font must be Inter, got {token.font_name}"
        assert token.size_pt == exp_size, f"{name} size expected {exp_size}, got {token.size_pt}"
        assert token.bold == exp_bold, f"{name} bold expected {exp_bold}, got {token.bold}"
        print(f"Verified token: {name:<20} -> {token.font_name} {token.size_pt}pt (Bold: {token.bold})")

    assert FONT_FAMILY == "Inter", "Only Inter font is allowed"
    print("ALL 13 TYPOGRAPHY TOKENS STRICTLY ENFORCE 'INTER'!")


def test_spacing_and_grid_math():
    print("\n--- Testing Spacing & Grid Math ---")
    assert CanvasBounds.width == 13.333
    assert CanvasBounds.height == 7.500
    assert Margins.left == 0.8
    assert Margins.right == 0.8
    assert round(Margins().usable_width, 3) == 11.733

    # Test 3-column split
    cols3 = GridCalculator.get_columns(3, gap=0.24)
    assert len(cols3) == 3
    # Check that (3 * col_w) + (2 * 0.24) == 11.733
    col_w = cols3[0][1]
    total_w = 3 * col_w + 2 * 0.24
    assert abs(total_w - 11.733) < 0.001
    print(f"Verified 3-Column Grid: Width={col_w:.3f}\" each, Gap=0.24\"")

    # Test 2-column split
    cols2 = GridCalculator.get_columns(2, gap=0.24)
    assert len(cols2) == 2
    col_w2 = cols2[0][1]
    assert abs((2 * col_w2 + 0.24) - 11.733) < 0.001
    print(f"Verified 2-Column Grid: Width={col_w2:.3f}\" each, Gap=0.24\"")


def test_semantic_rendering():
    print("\n--- Testing Semantic Slide Rendering ---")
    output_test_file = "test_design_system_output.pptx"
    if os.path.exists(output_test_file):
        os.remove(output_test_file)

    prs = Presentation()
    PPTXRenderer.initialize_presentation(prs)

    # 1. Slide 1: Architecture Blueprint (Dark Theme)
    arch_slide = SemanticSlide(
        title="Enterprise Architecture Diagram: The Air-Gapped Pipeline",
        category_tag="TECHNICAL ARCHITECTURE BLUEPRINT",
        visual_intent=VisualIntent.SYSTEM_ARCHITECTURE,
        narrative_subtitle="Decoupled multi-tier flow isolating SAP from shop-floor transactions while ensuring 100% operational fidelity",
        is_dark=True,
        slide_number=1,
        total_slides=4,
        footer_metadata="Lumbini Elite Solutions | Enterprise Architecture Practice | Confidential",
        callout_banner="Zero direct writes to SAP database tables (AFKO, AFRU, ACDOCA). Live ERP remains 100% unharmed with zero lock contention.",
        elements=[
            ArchitectureTier(
                tier_number=1,
                tier_name="TIER 1: SAP S/4HANA CORE",
                subtitle="System of Record (Transactional Truth)",
                components=[
                    "Exposes standard read-only OData endpoints.",
                    "Universal Journal (ACDOCA) single source of truth.",
                    "Master data governance: BOMs & routing tolerances."
                ],
                guarantee_badge="100% READ-ONLY | ZERO WRITE CALLS",
                protocol_to_next="OData GET"
            ),
            ArchitectureTier(
                tier_number=2,
                tier_name="TIER 2: ENTERPRISE MIDDLEWARE",
                subtitle="Decoupled Microservice & Event Queue",
                components=[
                    "Token-authenticated API gateway with rate-limiting.",
                    "Timestamp delta synchronization on S/4HANA.",
                    "Local graph database storing As-Built Genealogy."
                ],
                guarantee_badge="AIR-GAPPED OPERATIONAL CACHE",
                protocol_to_next="HTTPS REST"
            ),
            ArchitectureTier(
                tier_number=3,
                tier_name="TIER 3: SHOP-FLOOR EDGE",
                subtitle="Rugged Handheld Execution Terminals",
                components=[
                    "Offline-tolerant Progressive Web App on Zebra HHTs.",
                    "Zero Named User SAP Fiori licenses required.",
                    "Hardware-enforced barcode Poka-Yoke error proofing."
                ],
                guarantee_badge="TOUCHLESS FLOOR EXECUTION"
            )
        ]
    )
    PPTXRenderer.render(prs, arch_slide)

    # 2. Slide 2: Governance Matrix (Light Theme)
    matrix_slide = SemanticSlide(
        title="The 5 W’s Strategic Evaluation Matrix",
        category_tag="GOVERNANCE & IMPACT MATRIX",
        visual_intent=VisualIntent.GOVERNANCE_MATRIX,
        narrative_subtitle="Mapping Organizational Personas, Data Entities, Cadences, and P&L/EBITDA Drivers across Cockpits",
        is_dark=False,
        slide_number=2,
        total_slides=4,
        elements=[
            TableData(
                headers=["MODULE / COCKPIT", "WHO (Personas)", "WHAT (Scope & Metrics)", "WHEN (Cadence)", "WHERE (ERP Tables)", "WHY (EBITDA Impact)"],
                rows=[
                    ["Cash Flow & Fulfillment", "CFO, VP Finance, CEO", "Shipments vs SLAs, AP/AR aging, Liquidity runway simulator.", "Daily 06:00 AM & Intraday", "ACDOCA, BSID, BSIK, VBAK", "Accelerates Free Cash Flow; captures cash discounts."],
                    ["52-Week Procurement Pipeline", "CPO, SCM Leads, Buyers", "52-week PO releases, BOM component lineage, vendor concentration.", "Daily morning refresh", "EKKO, EKPO, EKET, MSEG", "Prevents spot freight premiums; stops job-work material bleed."],
                    ["Manufacturing & Batch Cost", "COO, Plant Directors, Controllers", "Full-kitting readiness, batch cost variance, machine utilization.", "Shift-wise (3x daily)", "AFKO, AFPO, AFRU, RESB", "Releases 10–18% trapped WIP; prevents line halts."]
                ],
                column_weights=[1.8, 1.8, 2.5, 1.6, 2.0, 2.0]
            )
        ]
    )
    PPTXRenderer.render(prs, matrix_slide)

    # 3. Slide 3: Value Realization / ROI Scorecard (Light Theme)
    roi_slide = SemanticSlide(
        title="Quantified Financial & Operational ROI",
        category_tag="TANGIBLE BUSINESS OUTCOMES",
        visual_intent=VisualIntent.VALUE_REALIZATION,
        narrative_subtitle="MEASURABLE IMPACT: Transforming plant floor accuracy into 38% faster order turnaround and 14-month payback.",
        is_dark=False,
        slide_number=3,
        total_slides=4,
        elements=[
            KeyMetric(value="-65%", label="WIP INVENTORY LATENCY", context="Automated confirmations replace end-of-shift paper backlog.", is_positive=True),
            KeyMetric(value="14-MO", label="FULL CAPITAL PAYBACK", context="Recurring cost elimination delivers rapid self-funding cash flow.", is_positive=True),
            ContentBlock(
                title="Operational Agility & Quality Proof Points",
                bullets=[
                    ("38% Faster Order Turnaround:", "Digital travelers eliminate paper transcription backlog across bays."),
                    ("22% Reduction in Scrap:", "Hardware barcode Poka-Yoke halts unverified component assemblies."),
                    ("100% Audit Compliance:", "Generates AS9100 as-built genealogy records in under 15 seconds.")
                ]
            ),
            ContentBlock(
                title="Financial ROI & Bottom-Line Levers",
                bullets=[
                    ("₹45L–₹75L OpEx Avoidance:", "Zero Named User SAP licenses required for hundreds of floor assemblers."),
                    ("₹1.8M Annual Scrap Recovery:", "Stops component obsolescence and incorrect drawing revision usage."),
                    ("4.2x 3-Year Program IRR:", "Accelerated capital return across multi-site plant expansion.")
                ]
            )
        ]
    )
    PPTXRenderer.render(prs, roi_slide)

    # 4. Slide 4: Phased Implementation Roadmap
    roadmap_slide = SemanticSlide(
        title="90-Day Agile Implementation Roadmap & Hypercare",
        category_tag="PROJECT PLAN & MILESTONES",
        visual_intent=VisualIntent.PHASED_ROADMAP,
        narrative_subtitle="Five structured milestone stages ensuring rapid shop-floor deployment with zero operational risk",
        is_dark=False,
        slide_number=4,
        total_slides=4,
        elements=[
            RoadmapPhase(
                phase_id="PHASE 1",
                duration="Days 1–15",
                title="Shop-Floor Blueprint",
                workstreams=[
                    "Walkthrough of 8–15 assembly work centers.",
                    "Barcode syntax definition (1D/2D QR code).",
                    "Specification of Read-Only OData endpoints."
                ],
                gate_criteria="Blueprint Sign-Off"
            ),
            RoadmapPhase(
                phase_id="PHASE 2",
                duration="Days 16–45",
                title="Core App Build",
                workstreams=[
                    "HHT Client build for Zebra/Honeywell scanners.",
                    "Local graph database schema for genealogy.",
                    "Poka-Yoke business logic and interlock engine."
                ],
                gate_criteria="Lab Poka-Yoke Pass"
            ),
            RoadmapPhase(
                phase_id="PHASE 3",
                duration="Days 46–65",
                title="OData Integration",
                workstreams=[
                    "Secure API Gateway deployment with TLS 1.3.",
                    "Read-only delta synchronization from S/4HANA.",
                    "Air-gapped posting slip generator testing."
                ],
                gate_criteria="Delta Sync Latency <1s"
            ),
            RoadmapPhase(
                phase_id="PHASE 4",
                duration="Days 66–90",
                title="Pilot & Go-Live",
                workstreams=[
                    "Live pilot on primary assembly work center.",
                    "Operator & supervisor enablement on HHTs.",
                    "Plant-wide production cutover and sign-off."
                ],
                gate_criteria="100% Traveler Digitization"
            )
        ]
    )
    PPTXRenderer.render(prs, roadmap_slide)

    prs.save(output_test_file)
    assert os.path.exists(output_test_file), "Output presentation must be saved"

    # Verify font fidelity in generated presentation
    prs_verify = Presentation(output_test_file)
    assert len(prs_verify.slides) == 4, "Must generate exactly 4 slides"

    font_names = set()
    for s in prs_verify.slides:
        for shape in s.shapes:
            if shape.has_text_frame:
                for p in shape.text_frame.paragraphs:
                    for r in p.runs:
                        if r.font.name:
                            font_names.add(r.font.name)
            if shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:
                        for p in cell.text_frame.paragraphs:
                            for r in p.runs:
                                if r.font.name:
                                    font_names.add(r.font.name)

    print(f"Fonts found in generated slides: {font_names}")
    for fn in font_names:
        assert fn == "Inter", f"Disallowed font detected: {fn}. ONLY 'Inter' is permitted!"

    print("ALL SLIDES STRICTLY AND EXCLUSIVELY USE 'INTER'!")
    print(f"Verified test presentation successfully created: {output_test_file}")


if __name__ == "__main__":
    test_typography_tokens()
    test_spacing_and_grid_math()
    test_semantic_rendering()
    print("\nALL DESIGN SYSTEM TESTS PASSED SUCCESSFULLY!")
