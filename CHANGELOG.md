# Changelog

All notable changes to the PowerPoint MCP Server project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.3.0] - 2026-11-21

### Added
- **Don Norman Human-Centered Design Engine (`design_system/norman_ux.py`)**:
  - Implemented core principles from *The Design of Everyday Things* (Conceptual Models First, Signifiers & Visual Hierarchy, Natural Spatial Mapping, Physical & Cognitive Constraints, Discoverability & Scannability, Feedback & Error Prevention).
  - Deterministic layout constraints: `MAX_WORDS_PER_SLIDE = 65`, `MAX_WORDS_PER_TITLE = 12`, `MAX_BULLETS_PER_CONTAINER = 4`, `MAX_WORDS_PER_BULLET = 15`, `MAX_CARDS_PER_SLIDE = 4` (5 for process flows).
  - Geometry standards: minimum 0.6in safe margins, 0.25in gutters, 0.20in internal card padding, 30% minimum open background whitespace target.
  - WCAG 2.1 relative luminance and contrast ratio auditor ($\ge 4.5:1$ body, $\ge 3.0:1$ headings).
  - Bounding-box collision detection between sibling shapes.
- **FastMCP Pre-Render Audit Tools**:
  - `validate_deck(path)`: Automated pre-render audit tool checking collisions, typography floors, density caps, and canvas boundaries, returning a Norman UX score (0-100) and structured diagnostics.
  - `audit_slide_ux(path, slide_index)`: Single-slide inspector returning itemized violations with recommended actions.
- **Dynamic PowerPoint Section Management**:
  - Automatically provisions 2 to 4 thematic acts covering all slides for presentations with 8 or more slides.

### Changed
- **Strict Integer Typography Floor ($\ge 12$pt, Zero Fractions)**:
  - Enforced a hard minimum font size floor of 12pt across all slides, shapes, tables, charts, metadata, and footers.
  - Upgraded all 88 sub-12pt and fractional font sizes in `design_system/lumbini/primitives.py`, `themes/lumbini/tokens.json`, and `tools/pptx_text_helpers.py` to discrete integer values (12, 14, 16, 18, 20, 22, 24, 26, 28, 32, 36).
- **Process Flow Redesign (`render_step_line`)**:
  - Replaced floating line and detached bottom deliverables box with 5 substantial, full-height vertical workflow cards ($y=1.95$ to $y=6.07$, height 4.12 in) with step badges, directional sequence arrows, 14pt bold headers, 12pt descriptions, integrated deliverable pills, and an Operational Standard banner, completely eliminating empty white space.
- **Executive Dashboard Layout Realignment (`render_dashboard_concept`)**:
  - Restructured dashboard into an enclosed Left Cockpit (62%) and Right AI Copilot (38%).
  - Automatically formats column chart category axis labels with concise signifiers and locks category/value axis tick labels to 12pt, eliminating horizontal label collisions.
  - Constrained all tabs and KPI cards within the left container card.
- **Deck Quality Gate**:
  - Updated `tools/qa_pptx.py` to default `--min-pt 12`.

---

## [1.2.0] - 2026-11-20

### Added
- **14-Perspective Scrutiny Architecture (`design_system/scrutiny.py`)**:
  - Implemented an expert human-judgment layer composed of 14 ordered analytical perspectives (13 scholar lenses + 1 Human Dimension lens).
  - Enforced strict 12-section Skill File Standard across all perspectives in `perspectives/`.
  - Embedded honest framing invariant across all tools and review reports: *"Lens modelled from published work. It is not the person's own statement."*
  - Exposed 6 new FastMCP scrutiny tools in `ppt_mcp_server.py`:
    - `list_perspectives`: Enumerates all 14 perspectives with implementation status.
    - `get_perspective`: Returns perspective brief and analytical guidelines.
    - `apply_perspective`: Enforces sequential execution; loads brief, narrative, and rendered slide previews for IDE agent inspection.
    - `record_perspective_review`: Validates structure, honest framing, and records review findings under `reviews/` or `calibration/`.
    - `scrutiny_status`: Tracks completion progress and delivery gate lock state across all 14 lenses.
    - `run_scrutiny`: Automated orchestrator for sequential multi-lens evaluation.
- **Mandatory Sequential Scrutiny Delivery Gate**:
  - Integrated `is_delivery_allowed()` gatekeeper check into `export_presentation_with_quality_gate()`.
  - Presentation export remains strictly locked until all 14 lenses have been executed in sequence with zero unresolved P1 blockers.
- **The Human Dimension (Integrating Lens 14)**:
  - Added `perspectives/14-human-dimension.md` word-for-word from practice declaration.
  - Focuses on frontline dignity, operator discretion over electronic surveillance, carrier driver hospitality, and human-centered transformation.
- **Dialectical Trade-Offs Architecture (`TRADEOFFS.md`)**:
  - Formal documentation of structural tensions and solutions:
    - *Jeanne Ross vs. Dennis Brandl*: Enterprise single system of record vs. L3 plant edge autonomous decoupling.
    - *Deming vs. Goldratt*: Eliminate all variation everywhere vs. buffer the constraint only.
    - *Westerman vs. McAfee*: Top-down executive steering vs. open platform APIs and The Geek Way.
    - *Goldratt vs. Human Dimension*: Constraint subordination vs. frontline dignity and craft.
    - *Zachman vs. Jacobson*: Exhaustive ontology vs. vertical use-case slices.
- **"Withstands Scrutiny" 3-Round Loop Calibration & Verification**:
  - Successfully calibrated all 14 lenses against the 8-slide executive deck `Supplier_Delivery_Tracker_CIO_Briefing.pptx`.
  - Addressed all P1 blockers in `build_smoke_test_deck.py` and `NARRATIVE.md`.
  - Verified 100% passing scrutiny run across all 14 lenses with 0 P1 blockers in `reviews/01-jeanne-ross.md` through `reviews/14-human-dimension.md`.
  - Delivery gate unlocked (`delivery_gate: PASSED`).

---

## [1.1.0] - 2026-11-13

### Added
- Enterprise Architecture & Industrial Engineering Visual Primitives:
  - Closed-loop manufacturing diagrams (`render_closed_loop_manufacturing`).
  - Executive dashboard cockpit (`render_executive_dashboard`).
  - Transformation bridge and maturity grids.
- Pre-flight automated OOXML Quality Gate (`tools/qa_pptx.py`).
- Lumbini Design System Reference Theme and Inter typography patcher.

---

## [1.0.0] - 2026-11-01

### Added
- Initial release of FastMCP PowerPoint Server.
- Native PowerPoint primitives (`create_presentation`, `add_slide`, `add_text`, `add_shape`, `add_picture`, `add_table`).
- Pyramid Principle storyline and visual layout planning pipeline.
