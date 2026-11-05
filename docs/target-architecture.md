# Target PowerPoint Generation Architecture
## Staged Pipeline, JSON Artifacts, Visual Primitives & Quality Gates

**Author:** Antigravity Engineering Team  
**Date:** November 2026  
**Artifact Path:** `docs/target-architecture.md`  
**Companion Document:** `docs/ppt-audit.md`

---

## 1. Staged Pipeline Overview

To eliminate the "text-to-cards" collapse and achieve the Lumbini reference quality bar, the generation engine separates responsibilities into five discrete, inspectable stages with automated quality gates and fix loops:

```
Brief / Request
      │
      ▼
[Stage 1: Research & Grounding] (Existing, Unchanged)
      │ ──► research.json (Verified facts, sources, confidence, caveats)
      ▼
[Stage 2: Storyline Planning]   (NEW - Management Consultant)
      │ ──► storyline.json (Pyramid logic, action titles, 1 message/slide, 0 repetition)
      ▼
[Stage 3: Content Distillation]  (NEW - Presentation Strategist)
      │ ──► slides.content.json (Enforced word budgets, notes split, capability tags)
      ▼
[Stage 4: Visual & Layout Plan]  (NEW - Corporate Graphic Designer)
      │ ──► deck.spec.json (Deterministic layout selection, content shapes, no consecutive dups)
      ▼
[Stage 5: Rendering Engine]      (NEW/REWORK - PowerPoint Engineer)
      │ ──► deck.pptx (Theme XML, slide masters, native charts, tables, mockups, measure-then-size)
      ▼
[Stage 6: Automated Quality Gate] (NEW - QA Inspector)
      │ ──► qa-report.json + previews/*.png (Blocking assertions, warnings, 1080p renders)
      ▼
[Stage 7: Fix Loop]             (NEW)
      └──► Max 3 iterations back to Stage 3/4/5 upon any blocking findings
```

---

## 2. Stage Contracts & Artifact Schemas

### Stage 1: Research (`research.json`)
- **Inputs:** Client brief, domain references, technical functional specifications.
- **Responsibility:** Extract accurate business facts, product specifications, integration constraints, and governance requirements.
- **Output Artifact:** `research.json` containing:
  - `client`: Organization name, industry, current ERP / technical state.
  - `workstreams`: List of core project initiatives.
  - `capabilities`: Verified product capabilities with source references.
  - `boundaries`: Technical qualifications (e.g. WPS format dependencies, Odoo v20 clean-core separation, Excel data extract dependency).
  - `commercial_rules`: Strict prohibition against inventing unconfirmed prices or staffing quotas.

### Stage 2: Storyline (`storyline.json`)
- **Inputs:** `research.json`.
- **Responsibility:** Executive storyline synthesis using Minto's Pyramid Principle:
  1. Executive Context & Objectives
  2. Requirements & Discovery
  3. Integrated Solution Architecture
  4. Core Solution Proof & Drill-down
  5. Executive Reporting Framework
  6. Diagnostic & Methodology Deep-dive
  7. Data Migration Continuity
  8. Operational Automation & Integration
  9. Phased Delivery Roadmap & Upgrade Compatibility
  10. Commercial Framework, Staffing & Governance
- **Storyline Rules:**
  - **Action Titles Only:** Every title must state the conclusion or takeaway, not just a topic label (e.g., *"Four connected workstreams around Odoo"* instead of *"Workstreams"*). Length: ≤ 9 words.
  - **Single-Allocation Rule:** Every fact, metric, and scope description is allocated to **exactly one slide**. Zero cross-slide duplication.
  - **Message Focus:** Exactly one primary takeaway per slide.
- **Output Artifact:** `storyline.json`.

### Stage 3: Distillation (`slides.content.json`)
- **Inputs:** `storyline.json`, `capabilities.yaml`.
- **Responsibility:** Word budget enforcement, capability classification, and speaker notes separation:
  - **Word Budgets (Enforced in Code):**
    - Target: ≤ 120 words per slide.
    - Hard Cap: 160 words per slide.
    - Cover Slide: ≤ 50 words.
    - Dense Commercial / Legal Slides: ≤ 200 words.
    - Bullets: ≤ 12 words per bullet.
    - Card Descriptions: ≤ 3 lines (≤ 25 words).
    - Containers: ≤ 6 items maximum.
  - **Capability Registry Binding:** Every feature/claim is tagged:
    - `confirmed`: Supported native functionality.
    - `proposed`: Activity or integration subject to discovery validation.
    - `illustrative`: Mockup KPIs, dashboard layouts, or indicative metrics.
  - **Notes Extraction:** Long explanatory narratives or technical details are moved to the slide's `notes` field rather than crowding the visual canvas.
- **Output Artifact:** `slides.content.json`.

### Stage 4: Visual Plan (`deck.spec.json`)
- **Inputs:** `slides.content.json`.
- **Responsibility:** Assigning layout archetypes and visual primitives according to the deterministic layout selection table:
  - **Layout Diversity Rules:**
    - No single layout archetype may appear on more than **2 consecutive slides**.
    - A 10-slide deck must utilize at least **6 distinct layouts**.
    - Every slide (except cover/closing) must include at least **1 non-text visual** (diagram, chart, mockup, step-line, or native table).

| content_shape | Layout Archetype | Mandatory Visual Primitive | Typical Slide Usage |
|---|---|---|---|
| `cover` | Cover Hero | Title, Subtitle, Metadata, Accent Rule, Brand Assets | Slide 1 (Cover) |
| `requirement_to_outcome` | 3-Column Comparative Rows | Numbered Badges + Action Arrows + Divided Rows | Slide 2 (Requirements) |
| `hub_and_spokes` | Central Core Hub | Central Navy Hub + 4 Directional Labeled Spokes | Slide 3 (Solution Architecture) |
| `dashboard_concept` | Analytics Cockpit | Chevron Flow + Dashboard Mockup + 2 Native Charts + Drill Ladder | Slide 4 (BI & Analytics Products) |
| `levels_x_dimensions` | Stakeholder Matrix Grid | Matrix Cells (Dashed if illustrative) + Confirmed Band | Slide 5 (Executive Reporting) |
| `process_linear` (4–7 steps) | Sequential Pipeline | Connecting Step-Line + Numbered Circles + Deliverables Band | Slide 6 & 7 (Audits, Migrations) |
| `flow_with_actions` | Action-Oriented Flow | System Boxes + Dashed Vertical Drop-lines + Action Sub-blocks | Slide 8 (Integrations & Payroll) |
| `phases_over_time` | Phased Roadmap | Staggered Pill Sequence Bars (No fake dates) + Future Callout | Slide 9 (Roadmap & Upgrades) |
| `roles_and_terms` | Dual Compact Tables | 2 Native PowerPoint Tables (Navy Headers, Orange Placeholders) | Slide 10 (Commercials & Resources) |

- **Output Artifact:** `deck.spec.json` (validated against strict JSON Schema).

### Stage 5: Rendering Engine (`deck.pptx`)
- **Inputs:** `deck.spec.json`, theme tokens (`themes/lumbini/tokens.json`), base template (`themes/lumbini/template.pptx`).
- **Responsibility:** Constructing native, editable PowerPoint slides:
  - **Slide Masters & Placeholders:** Uses defined slide layouts (`COVER` and `CONTENT`). Slide titles populate the master's native title placeholder (`slide.placeholders[0]`).
  - **Background & Brand Motifs:** Inherited directly from slide masters (light textured background `bg_light.jpg`, top-right "E" corner rectangles, bottom-left strip, master footer, and slide number).
  - **Theme Colors & Fonts:** Written directly into `ppt/theme/theme1.xml` (Inter font family, Lumbini 12-slot color scheme).
  - **Measure-Then-Size Algorithm:** Before rendering any card or container, text blocks are measured using real font metrics (Pillow `ImageFont` on `Inter-Regular.otf`). Container heights are computed as `measured_text_height + padding`. If content exceeds available height, the engine triggers text distillation rather than shrinking font size below 10 pt.
  - **Native Objects:** Renders native editable charts (`XL_CHART_TYPE.COLUMN_CLUSTERED`, `XL_CHART_TYPE.LINE`), native PowerPoint tables with navy headers (`1F497D`) and orange accent text (`F78B15`), vector shapes, and clean connector lines.

---

## 3. Quality Gate Architecture (`qa_deck`)

The quality gate evaluates the rendered presentation across two distinct tiers:

### Tier 1: Automated Programmatic Checks (`qa-report.json`)
- **Blocking Failures (Causes Immediate Rejection & Fix Loop Trigger):**
  - Any text or shape bounding box falling outside slide canvas (`13.333" x 7.50"`).
  - Any bounding box collisions/overlaps between unrelated shape objects.
  - Any font size below **10.0 pt** (footers and slide numbers allowed at ≥ 9.0 pt).
  - Slide word count exceeding **160 words** (cover > 50 words).
  - Contrast ratio below **4.5:1** between text and background.
  - Empty title placeholders or lingering placeholder tokens (`TODO`, `Lorem ipsum`, `[insert`).
  - Distorted images (aspect ratio variance > 2%).
  - Charts missing titles, missing axis units, or containing > 6 categories.
  - Stating an unconfirmed or proposed capability as confirmed.
  - Same layout archetype used on > 2 consecutive slides.
  - Fewer than 6 distinct layouts in a 10-slide deck.
  - File integrity failure (fails to re-open in `python-pptx` or PowerPoint COM).
- **Warning Checks:**
  - Container empty volume > 35%.
  - Zero non-text visuals on a non-cover slide.
  - Missing speaker notes.

### Tier 2: Visual Review & Image Export
- Native PowerPoint COM automation renders all slides to 1920×1080 PNG images in `previews/`.
- Automated visual scoring evaluates hierarchy, alignment, whitespace balance, and brand consistency.
- If blocking failures occur, the engine triggers an automated **Fix Loop** (up to 3 iterations) passing specific violation feedback back to Stage 3 (Distill), Stage 4 (Visual Plan), or Stage 5 (Render).

---

## 4. MCP Tool Changes & Public Interface

The PowerPoint MCP Server will expose the following unified tools:

1. **`list_themes()` -> `List[str]`**
   Lists available design system themes (`lumbini`, etc.).
2. **`list_layouts()` -> `List[Dict[str, Any]]`**
   Lists supported layout archetypes, descriptions, and required data schemas.
3. **`plan_storyline(brief: str, research_data: Dict[str, Any]) -> Dict[str, Any]`**
   Generates `storyline.json` enforcing pyramid structure, action titles, and single allocation.
4. **`plan_visuals(storyline_data: Dict[str, Any], theme: str = "lumbini") -> Dict[str, Any]`**
   Applies deterministic layout selection rules, enforces word budgets, and produces `deck.spec.json`.
5. **`render_deck(spec: Dict[str, Any], path: str, theme: str = "lumbini") -> Dict[str, Any]`**
   Renders the `.pptx` file using measure-then-size geometry, slide masters, native charts, tables, and themes.
6. **`qa_deck(path: str, spec: Optional[Dict[str, Any]] = None) -> Dict[str, Any]`**
   Executes automated programmatic assertions, renders 1080p preview images, and outputs `qa-report.json`.
7. **`generate_presentation_pipeline(brief: str, research_data: Dict[str, Any], path: str, theme: str = "lumbini") -> Dict[str, Any]`**
   Full end-to-end autonomous orchestrator running Stages 1 through 7 with automatic fix loop.
8. **Backward Compatibility:**
   Existing tools (`create_presentation`, `add_slide`, `render_executive_dashboard`, etc.) remain accessible to ensure existing automations continue to function smoothly.
