# PowerPoint Generation MCP Server Audit & Upgrade Blueprint
## Phase 0: Forensic Inspection, Hypotheses Verification & Gap Analysis

**Author:** Antigravity Engineering Team (Management Consultant, Presentation Strategist, Corporate Graphic Designer, PowerPoint Engineer)  
**Date:** November 2026  
**Artifact Path:** `docs/ppt-audit.md`  
**Target Quality Bar:** `reference/SGG_ELITIA_BI_Odoo_Proposal_Lumbini.pptx`  
**Baseline / "Before" Sample:** `reference/mcp_generated_sample.pptx`

---

## 1. Project Architecture Map

### 1.1 Entry Points & System Configuration
- **MCP Server Entry Point:** `C:\Users\Lumbini_User\Desktop\PPT\ppt_mcp_server.py`
- **MCP Client Launch Configuration:** `.agents\mcp_config.json` launches `.\.venv\Scripts\python.exe ppt_mcp_server.py` using standard STDIO transport.
- **FastMCP Instance:** Initialized at line 57 of `ppt_mcp_server.py` as `mcp = FastMCP("PowerPoint-MCP-Server", instructions=COMBINED_MCP_SYSTEM_PROMPT)`.
- **System Prompts Registered:**
  - `MCP_PPT_SYSTEM_PROMPT` (`ppt_mcp_server.py:11-29`): Contains the "3-bullet maximum rule", multi-column cards, architecture workflow split, narrative subheaders, and typography emphasis.
  - `EXENTRIC_ARCHITECT_SYSTEM_PROMPT` (`ppt_mcp_server.py:32-52`): Enterprise systems-thinking, constraints, Zachman/Ross ontology, and feedback loops.
- **Underlying Rendering Engine:** `python-pptx` (version 1.0.2 in `.venv`) alongside PIL / Pillow (12.3.0) and Windows COM dispatch (`win32com.client`) for headless PowerPoint rendering and QA.
- **Registered Tools (37 Tools Total):**
  1. *Core CRUD:* `create_presentation`, `add_slide`, `delete_slide`, `add_text`, `add_bullet_points`, `add_shape`, `add_picture`, `add_table`, `get_presentation_info`, `search_replace_text`.
  2. *Primitives & Composition:* `list_visual_primitives`, `render_visual_primitive`, `render_semantic_slide`, `list_narrative_sections`, `compose_architecture_deck`, `analyze_manufacturing_semantics`.
  3. *Dashboards & Tables:* `list_dashboard_archetypes`, `render_executive_dashboard`, `list_table_archetypes`, `render_enterprise_table`.
  4. *Architecture & Reviews:* `list_architecture_templates`, `render_enterprise_architecture_diagram`, `list_narrative_frameworks`, `generate_narrative_presentation`, `list_architecture_review_lenses`, `review_presentation_architecture`.
  5. *Quality & Density:* `evaluate_visual_density`, `render_low_density_slide`, `audit_presentation_quality`, `export_presentation_with_quality_gate`, `generate_scenario_presentation`.
  6. *Specialized Flow Engines:* `render_process_flow_diagram`, `render_swimlane_diagram`, `render_transformation_bridge`, `render_maturity_assessment`, `render_closed_loop_manufacturing`.

---

## 2. End-to-End Generation Trace ("The Disconnect")

When tracing a generation from user brief to final `.pptx` file:
1. **User Request / Brief:** The user requests an executive presentation (e.g. SGG 10-slide proposal).
2. **Research & Extraction:** The system reads technical specifications (e.g., `Elitia_BI_Functional_Specification.md`) and extracts factual requirements, capabilities, and caveats with high fidelity.
3. **The Architectural Gap (No Intermediate Planning):**
   - The LLM attempts to bridge the entire gap between *unfiltered research notes* and *slide geometry* in a single leap.
   - The MCP tools provide discrete, disconnected primitives (`add_split_cards`, `add_text`), but lack an end-to-end orchestration pipeline.
   - Consequently, the model defaults to scripting ad-hoc Python scripts (`build_sgg_proposal.py`, `build_jbvnl_proposal.py`) that repeat a rigid, templated layout across all slides.
4. **Layout, Box Sizing & Font Size Decisions:**
   - **Where decided:** Hard-coded inside the script generation loop prior to measuring content.
   - **By whom:** The LLM improvises fixed coordinate boxes (`left = Inches(0.8 + i * 2.9)`, `width = Inches(2.7)`, `height = Inches(4.8)`).
   - **Font sizing reaction:** When 60–100 words of dense bullet points are forced into a narrow 2.7" box, the font size is shrunken down to **7.8 pt – 8.19 pt** so text doesn't visibly overflow the slide border.
   - **Resulting failure:** Over 55% of the card container is left completely empty at the bottom, while the text inside is unreadable from more than 2 feet away.

---

## 3. Hypotheses Verification Table (Sample Deck vs. Reference Deck)

Every hypothesis provided in the briefing has been verified against the actual XML, rendering metrics, and code implementations:

| # | Observation in `mcp_generated_sample.pptx` | Reference Deck (`reference/SGG_ELITIA_BI_Odoo_Proposal_Lumbini.pptx`) | Finding & Line Evidence in Code / XML | Status |
|---|---|---|---|---|
| **H1** | Average **316 words per slide** (range 154–430). | Average **107.4 words per slide** (~118 target). | Word counter script confirmed: Sample deck has 3,161 total words across 10 slides (avg 316.1 words/slide). Slide 1 = 154 words; Slide 10 = 430 words. In `build_sgg_proposal.py`, raw research sentences are written directly to paragraphs without any word-budget constraint. | **CONFIRMED** |
| **H2** | Body text mostly **8–9.5 pt**; smallest 7.8 pt. Most runs are 8.19 pt. | Body **11–13 pt**, floor **10 pt** (footers 9 pt). | Paragraph & run inspection: 127 runs are at 8.19 pt, 40 runs at 8.0 pt, 34 runs at 8.5 pt. Smallest run is 7.8 pt on Slide 10 (`build_sgg_proposal.py:1509`). Font sizes were reduced to fit bulky text into fixed-height boxes. | **CONFIRMED** |
| **H3** | Rounded cards are **~60% empty** while the text inside is tiny. | Card height dynamically follows content; zero wasted vertical space. | In `build_sgg_proposal.py:185, 320, 480`, card rectangles are instantiated with fixed `height = Inches(4.8)`. The text inside only fills 1.8"–2.2" of vertical space. ~58%–62% of the card area is empty white canvas. No measure-then-size calculation exists. | **CONFIRMED** |
| **H4** | **7 of 10 slides use the same layout** (title + row of 3–5 tall rounded cards). | **8 distinct layouts** across 10 slides (`cover`, `requirement_to_outcome`, `hub_and_spokes`, `dashboard_concept`, `levels_x_dimensions`, `process_linear`, `flow_with_actions`, `phases_over_time`, `roles_and_terms`). | Slides 2, 4, 5, 6, 7, 8, 9, 10 in the sample deck all use the identical visual pattern: Header + row of 2 to 6 vertical rounded cards + bottom full-width banner. No layout selection logic or layout archetype table exists. | **CONFIRMED** |
| **H5** | **0 charts, 0 tables, 0 pictures** (except the logo). Slide 4 is ELITIA BI and has no dashboard mockup. | **2 native charts**, interactive dashboard mockup, **2 native tables**, process flows, hub diagram. | OpenXML inspection: `mcp_generated_sample.pptx` contains **zero** `<p:graphicFrame>` elements across all 10 slides (no `<c:chart>`, no `<a:tbl>`). Slide 4 has 4 text cards. In contrast, the reference deck has 2 native charts on Slide 4 and 2 native tables on Slide 10. | **CONFIRMED** |
| **H6** | Theme part is the **default Office 2007 palette** (1F497D / EEECE1 / 4F81BD…); every colour and font is hard-coded on shapes (Calibri, slate/navy hex). | Real theme colours/fonts applied (**Inter**, Lumbini 12-slot palette written into `ppt/theme/theme1.xml`). | In `mcp_generated_sample.pptx` `ppt/theme/theme1.xml`, `<a:clrScheme name="Office">` contains the default Microsoft Office 2007 palette. All shapes in `build_sgg_proposal.py` have hard-coded `RGBColor` objects and font family `"Calibri"` applied run by run. | **CONFIRMED** |
| **H7** | **No placeholders on any slide** (titles are plain text boxes); default layouts unused. `presentation.xml` declares 4:3 while size is 16:9. | Titles are real `<p:ph>` placeholders on defined master layouts. Clean 16:9 widescreen declaration. | In `mcp_generated_sample.pptx`, `ppt/presentation.xml` contains `<p:sldSz cx="12191695" cy="6858000" type="screen4x3"/>`. In all slide XML files, `<p:ph>` elements = 0. All titles are arbitrary `<p:sp>` textboxes on blank layout (`prs.slide_layouts[6]`). In reference deck, `sldSz` is pure 16:9 and titles are real placeholders. | **CONFIRMED** |
| **H8** | Flat near-white background; logo only on cover; no footer, no slide numbers, no brand motif. | Textured background (`bg_light.jpg`), corner "E" brand motif, master footer, and slide number on the master. | `mcp_generated_sample.pptx` draws an ad-hoc `#F8FAFC` rectangle per slide; logo placed manually only on Slide 1; zero master-level slide numbers, footers, or motifs exist. | **CONFIRMED** |
| **H9** | Each section has 3–6 dense bullets plus "Strategic Value / Deliverable / Core Objective" sub-lines. The slide reads like a document page. | One message per slide; concise statements; visual constructs carry the logic. | In `mcp_generated_sample.pptx`, every card is crammed with 4-6 bullet points plus bold nested prefix labels, making the slide unpresentable as a projection deck. | **CONFIRMED** |
| **H10** | Speaker notes are long scripted paragraphs. | Short, bulleted notes with caveats, methodology, and sourcing. | In `build_sgg_proposal.py`, speaker notes contain 150-220 word conversational monologues ("Good morning, esteemed leadership team of Saeed Godharan Group...") that repeat slide points verbatim rather than serving as presenter memory aids. | **CONFIRMED** |
| **H11** | Cover slide carries a "Four Integrated Workstreams" box that belongs on the solution-overview slide. | Cover is strictly cover (title, subtitle, metadata, logo, visual illustration). | In `mcp_generated_sample.pptx` Slide 1, the right-hand container holds a complete breakdown of Workstreams A, B, C, D which directly duplicates Slide 3's core content before the presentation even starts. | **CONFIRMED** |
| **H12** | No visible QA step: overlaps and emptiness shipped. | Pre-flight QA with automated rules and rendered visual inspection loop. | `qa_sgg.py` only asserted `len(prs.slides) == 10` and font family == "Calibri". It had zero checks for empty container volume, word count overages, font sizes below 10 pt (7.8 pt passed without warning), or layout redundancy. | **CONFIRMED** |

---

## 4. Strengths of Current System (To Preserve & Protect)

The audit revealed notable strengths that must not be lost during the upgrade:
1. **Research Depth & Content Accuracy:** The factual grounding in real enterprise products (e.g., ELITIA BI's single PostgreSQL semantic layer, star schema, Explain Change variance analysis, drill-through down to Odoo line items) is exemplary.
2. **Integrity of Scope Boundaries:** Clear governance warnings (e.g., distinguishing illustrative KPIs from confirmed platform features; recognizing that WPS export requires bank-specific format validation; acknowledging that Resort ERP migration depth depends on available Excel extracts).
3. **Commercial Safeguards:** Strict refusal to invent prices or staffing percentages; preserving editable placeholders (`[Amount]`, `[Allocation Placeholder]`) and quarantining commercial terms to the final slide.
4. **Fast Generation & Direct Execution:** The ability to generate presentations programmatically and audit them rapidly via native PowerPoint COM automation.

---

## 5. Architectural Upgrade Plan: The "Keep, Change, Add" Register

### KEEP (Unchanged)
- **Domain Research & Retrieval:** Existing fact-gathering logic and technical specification ingestion.
- **FastMCP Transport & Tool Registry:** Standard FastMCP infrastructure running in the Python environment.
- **Integrity Rules:** Strict capability labeling (`confirmed`, `proposed`, `illustrative`) and commercial placeholder governance.
- **PowerPoint COM Rendering Automation:** Native headless 1080p slide export via PowerPoint dispatch (`qa_sgg.py` / `win32com.client`) for automated visual inspection.

### CHANGE (Rework)
- **Direct Text-to-Slide Rendering:** Replaced by a 5-stage staged pipeline producing validated intermediate JSON artifacts (`storyline.json`, `slides.content.json`, `deck.spec.json`).
- **Ad-Hoc Canvas Coordinates:** Replaced by a **"Measure-Then-Size"** engine using real Pillow font metrics (`ImageFont` on Inter TTF) to compute dynamic card heights based on distilled content, eliminating the 60% empty space defect.
- **Hard-Coded Palette & Calibri:** Replaced by theme-token extraction (`themes/lumbini/tokens.json`) with automated OOXML theme patching (`ppt/theme/theme1.xml`), real Inter font bindings, and clean 16:9 canvas dimensions.
- **Blank Layout Dependency:** Replaced by pre-engineered slide masters (`COVER`, `CONTENT`) containing real title placeholders, background textures, corner brand motifs, footers, and slide numbers.
- **Monolithic Speaker Notes:** Replaced by concise presenter cues, capability caveats, and data source citations.

### ADD (New Capabilities)
1. **Stage 2: Storyline Planner (`plan_storyline`):**
   - Implements Barbara Minto's Pyramid Principle: context ➔ requirements ➔ solution ➔ proof ➔ approach ➔ commercials.
   - Enforces action-oriented titles (≤ 9 words, stating the conclusion rather than the topic).
   - Enforces the **Single-Allocation Rule** (each fact lives on exactly one slide; zero cross-slide repetition).
2. **Stage 3: Content Distillation Engine (`distill_content`):**
   - Hard word budgets enforced in code: ≤ 120 words target, 160 hard cap per slide; cover ≤ 50 words; bullets ≤ 12 words; ≤ 6 items per container.
   - Formal Capability Registry (`capabilities.yaml`) integration: automatically tags items as `confirmed`, `proposed`, or `illustrative` (rendering illustrative KPIs with dashed borders).
3. **Stage 4: Deterministic Visual Planner (`plan_visuals`):**
   - Applies the layout rule table: no layout used on > 2 consecutive slides; ≥ 6 distinct layouts in a 10-slide deck; ≥ 1 non-text visual per slide.
   - Assigns explicit `content_shape` tokens (`requirement_to_outcome`, `hub_and_spokes`, `dashboard_concept`, `levels_x_dimensions`, `process_linear`, `flow_with_actions`, `phases_over_time`, `roles_and_terms`).
4. **Stage 5: Native Visual Primitives Library:**
   - `hubDiagram`: Central hub with directional labeled arrows and surrounding node cards.
   - `dashboardMock`: Native BI cockpit with filter tabs, KPI tiles with ▲/▼ deltas, 2 native charts (bar/column and line), and a 4-level drill-down ladder.
   - `nativeChart`: Real PowerPoint editable charts (`ChartData`, `XL_CHART_TYPE.COLUMN_CLUSTERED`, `XL_CHART_TYPE.LINE`).
   - `matrixGrid`: Structured matrix with dashed borders for illustrative KPIs and bottom confirmed capability band.
   - `stepLine`: Connecting pipeline line with numbered circle badges and matching deliverables band.
   - `flowWithActions`: Boxed integration flow with vertical dashed drop-lines to action descriptions and bottom legend.
   - `roadmapRows`: Sequence bars without invented dates and future-readiness callout strip.
   - `nativeTable`: Real PowerPoint tables with navy headers and orange placeholder cells.
5. **Stage 6 & 7: Automated Quality Gate & Fix Loop (`qa_deck`):**
   - Automated blocking assertions: font floor ≥ 10 pt (except footers/slide numbers ≥ 9 pt); words ≤ 160; zero empty containers > 35%; zero shape collisions; theme and layout compliance.
   - Automated visual review loop: headless rendering to PNG, visual scoring, and maximum 3 fix iterations before delivery.

---

## 6. Implementation Strategy & Next Steps

Phase 0 confirms that the current server has deep factual intelligence but suffers from a lack of intermediate architectural stages, resulting in repetitive, unstyled, low-density cards.

By porting the visual primitives and master layouts from `reference/reference_build.js` and `themes/lumbini/tokens.json` into Python native rendering engines, we will elevate the MCP server output to match the Lumbini reference standard across every metric.
