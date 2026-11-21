# PowerPoint Model Context Protocol (MCP) Server

An enterprise-grade Model Context Protocol (MCP) server for PowerPoint presentation generation, inspection, transformation, and automated quality assurance. Powered by `fastmcp` and `python-pptx`, this server exposes high-level tools for executive presentations, architectural visual grammars, and end-to-end consulting delivery.

---

## Architecture Overview

```
ppt-mcp-server/
├── ppt_mcp_server.py           # FastMCP server entrypoint registering all tools
├── pipeline/                   # Lumbini Reference Standard 7-stage presentation pipeline
│   ├── storyline.py            # Stage 2: Pyramid Principle executive storylines
│   ├── distill.py              # Stage 3: Content distillation & word budget enforcement
│   ├── visual_plan.py          # Stage 4: Deterministic layout diversity & visual mapping
│   ├── renderer.py             # Stage 5: 16:9 widescreen master rendering & section acts
│   ├── qa.py                   # Stage 6: Pre-flight quality gate & preview rendering
│   ├── panel_review.py         # Architect review panel validations
│   └── nexus_research.py       # Analytical transformation lenses
├── design_system/              # Design systems and visual grammar engines
│   ├── lumbini/                # Lumbini reference theme, tokens, & vector primitives
│   │   ├── primitives.py       # 12+ presentation primitives (benchmark tables, stacks, etc.)
│   │   ├── theme_patcher.py    # OOXML color & font scheme patcher
│   │   └── tokens.py           # Color palette, spacing, and typography scales
│   ├── architecture_engine.py  # Enterprise architecture diagrams
│   ├── dashboard.py            # Executive KPIs and analytics mockups
│   ├── maturity_engine.py      # Capability maturity matrices
│   ├── process_flow_engine.py  # End-to-end process pipelines
│   ├── swimlane_engine.py      # Cross-functional swimlane flows
│   └── transformation_engine.py# Transformation roadmaps & timelines
├── tools/                      # Core engineering and audit utilities
│   ├── qa_pptx.py              # Automated CLI quality gate auditor
│   ├── sections.py             # Dynamic PowerPoint section & act management
│   ├── textfit.py              # Accurate font metric text-fitting engine
│   └── pptx_text_helpers.py    # Text formatting and shape utilities
├── themes/                     # Theme definitions and templates
│   └── lumbini/                # Master template, tokens.json, and Inter typography
└── .agents/                    # Agent skills, plugins, and presentation guardrails
```

---

## Key Features & Tool Suite

### 1. Lumbini Reference Standard Pipeline
- **`list_themes()`**: Lists available themes (e.g. `lumbini`).
- **`list_layouts()`**: Enumerates all supported content shapes (`cover`, `levels_x_dimensions`, `benchmark_table`, `flow_with_actions`, `requirement_to_outcome`, `layered_stack`, `tradeoff_matrix`, `phases_over_time`, `closing`, etc.).
- **`plan_storyline(brief, research_data)`**: Synthesizes an executive pyramid storyline with action titles ($\le 9$ words), single-allocation fact distribution, and strict word budgets.
- **`plan_visuals(storyline_data, theme)`**: Enforces deterministic layout selection rules (no layout used $> 2$ consecutive slides, $\ge 6$ distinct layouts in 10-slide decks, $\ge 1$ non-text visual per slide).
- **`render_deck(spec, path, theme)`**: Generates widescreen (16:9) presentations using clean vector shapes, native tables, and master slide placeholders with zero placeholder prompt leaks.
- **`qa_deck(path, spec, render_images)`**: Runs pre-flight quality checks (font size floor $\ge 10.0$pt, slide words $\le 160$, container empty space $< 35\%$, zero shape collisions).
- **`generate_presentation_pipeline(brief, research_data, path, theme)`**: End-to-end orchestrator running Stages 1 through 7 with automatic fix loops.

### 2. Enterprise Architecture & Transformation Tools
- **`render_manufacturing_capability_overview`**: Industrial automation and enterprise manufacturing capabilities.
- **`render_sap_mes_transformation_roadmap`**: Phased enterprise SAP & MES transition architectures.
- **`render_closed_loop_manufacturing`**: ISA-95 level 4 to 0 feedback loop topology.
- **`render_executive_dashboard`**: CXO analytics cockpit with native column/line charts and KPI deltas.
- **`render_maturity_assessment`**: Capability maturity grids across digital dimensions.
- **`render_transformation_timeline`**: Strategic transformation timelines with workstreams.
- **`render_governance_framework`**: Enterprise governance and decision rights matrices.
- **`render_swimlane_process`**: Cross-functional swimlane process models.

### 3. Native PPTX Primitives
- **`create_presentation`**, **`add_slide`**, **`add_text`**, **`add_bullet_points`**, **`add_shape`**, **`add_picture`**, **`add_table`**, **`get_presentation_info`**, **`search_replace_text`**, **`delete_slide`**.

### 4. 14-Perspective Human-Judgment Scrutiny Suite
- **`list_perspectives()`**: Enumerates all 14 ordered lenses and implementation states.
- **`get_perspective(name)`**: Retrieves perspective brief, 10 signature questions, and rubric.
- **`apply_perspective(deck_path, name)`**: Loads narrative, slide images, and enforces sequential order.
- **`record_perspective_review(deck_path, name, review_markdown)`**: Records validated findings table into `reviews/`.
- **`scrutiny_status(deck_path)`**: Evaluates delivery lock state (requires all 14 lenses complete with 0 P1 blockers).
- **`run_scrutiny(deck_path, max_rounds)`**: End-to-end multi-round scrutiny orchestrator.

### 5. Don Norman Human-Centered Design Engine & Pre-Render Audit
- **`validate_deck(path)`**: Automated pre-render audit tool verifying bounding-box collisions, typography floors ($\ge 12$pt integer scale, zero fractions), density caps ($\le 65$ words/slide, $\le 12$ words/title), safe margins ($\ge 0.6$in), and WCAG contrast ratios ($\ge 4.5:1$ body, $\ge 3.0:1$ headings). Returns an executive Norman UX score (0–100) with structured diagnostic fixes.
- **`audit_slide_ux(path, slide_index)`**: Single-slide inspector returning itemized violations and recommended actions.
- **Dynamic PowerPoint Section Management**: Automatically groups slides into 2–4 contiguous thematic acts for presentations of 8 or more slides.

---

## The 14 Scrutiny Perspectives

Every executive presentation is evaluated through 14 sequential perspectives (13 scholars + 1 Human Dimension lens) before delivery:

| # | Perspective | Scholar / Originator | Focus & Analytical Scope |
|---|---|---|---|
| 01 | `jeanne-ross` | Dr. Jeanne W. Ross | Operating models, standardized operational backbone, and avoiding shadow data stores. |
| 02 | `john-zachman` | John A. Zachman | Enterprise ontology completeness (What, How, Where, Who, When, Why) and state lifecycles. |
| 03 | `ivar-jacobson` | Dr. Ivar Jacobson | Architectural intent, vertical use-case slices, and explicit exception flows. |
| 04 | `dennis-brandl` | Dennis Brandl | ANSI/ISA-95 Level 3 vs Level 4 boundary decoupling and material lot/batch traceability. |
| 05 | `michael-mcclellan` | Michael McClellan | MES architecture, shopfloor real-time flow, and closed-loop plan-to-plant feedback. |
| 06 | `peter-senge` | Dr. Peter Senge | Systems thinking, mental models, and dismantling "Fixes that Fail" bullwhip loops. |
| 07 | `russell-ackoff` | Dr. Russell L. Ackoff | Interactive design, problem dissolution via VMI, and frontline worker co-design. |
| 08 | `donella-meadows` | Dr. Donella Meadows | Leverage points (#6 information flows vs #12 parameters) and feedback delay alignment. |
| 09 | `w-edwards-deming` | Dr. W. Edwards Deming | Shewhart SPC charts, eliminating management tampering on common-cause noise, and PDCA. |
| 10 | `eliyahu-goldratt` | Dr. Eliyahu M. Goldratt | Theory of Constraints (TOC), Drum-Buffer-Rope, and Throughput Accounting ROI. |
| 11 | `george-westerman` | Dr. George Westerman | Digital mastery, transformation steering governance, and avoiding the "Fashionista" trap. |
| 12 | `andrew-mcafee` | Dr. Andrew McAfee | Open platform APIs, carrier self-service, cognitive augmentation, and The Geek Way. |
| 13 | `erik-brynjolfsson` | Dr. Erik Brynjolfsson | The Productivity J-Curve transition dip, Turing Trap avoidance, and 40%+ intangible capital. |
| 14 | `human-dimension` | Human Dimension | Frontline worker dignity, situational judgment over surveillance, and driver hospitality. |

---

## Delivery Gate Policy

Presentations cannot be exported for final client delivery until the **Scrutiny Gate** is unlocked:
1. All 14 perspectives must be applied in strict sequential order.
2. Zero (0) P1 blocking findings may remain open.
3. Open P2 recommendations must have documented rationale and trade-offs in `TRADEOFFS.md`.

---

## Installation & Setup

### Prerequisites
- Python 3.10+ (Recommended: Python 3.12)
- Windows / macOS / Linux

### Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## MCP Server Configuration

To connect this server with an MCP host (such as Claude Desktop, Cursor, or Antigravity), add the following entry to your MCP configuration file:

```json
{
  "mcpServers": {
    "powerpoint": {
      "command": "python",
      "args": [
        "c:/path/to/ppt-mcp-server/ppt_mcp_server.py"
      ],
      "env": {}
    }
  }
}
```

---

## Running the Server

### Direct Execution
```bash
python ppt_mcp_server.py
```

### Pre-Flight Quality Gate Audit
```bash
python tools/qa_pptx.py presentation.pptx --slack 1.12
```

---

## License

Internal / Proprietary — Lumbini Elite Solutions & Services.
