# MASTER INSTRUCTION: Upgrade the PowerPoint-generation MCP server to the Lumbini reference standard

You are working inside the project that contains my PowerPoint-generation MCP server. Your job is to raise the **visual and structural quality** of the decks it produces to the standard of the reference deck, **without degrading the research and content accuracy it already does well**.

Act as four people at once: an experienced management consultant (storyline), a presentation strategist (what each slide must prove), a corporate graphic designer (layout and hierarchy), and a PowerPoint engineer (clean, editable, native files).

Work in the order below. **Do not skip Phase 0. Do not change code before the audit is written.**

---

## 0. Kit contents (read first)

This kit sits next to this file:

| Path | What it is |
|---|---|
| `reference/SGG_ELITIA_BI_Odoo_Proposal_Lumbini.pptx` | **The quality bar.** Treat as the visual and structural standard. |
| `reference/reference_build.js` | The script that produced it (pptxgenjs). A working example of every pattern needed: theme, masters, hub diagram, chevron flow, native charts, dashboard mockup, tables, roadmap. Port the *patterns*, not the SGG content. |
| `reference/mcp_generated_sample.pptx` | Output of the **current** server for the same brief. This is the "before". |
| `reference/previews/` | PNG renders of both decks for side-by-side comparison. |
| `themes/lumbini/tokens.json` | Design tokens extracted from the Lumbini corporate deck. |
| `themes/lumbini/assets/` | Logo, lightened background, cover illustration. |

The brief both decks answer: a 10-slide client proposal for Saeed Godharan Group (ELITIA BI + Odoo health check + Resort ERP migration + payroll/WPS integration). Use it as your regression test.

---

## 1. Phase 0: Inspect before changing anything

1. Map the project: entry point of the MCP server, every registered tool (name, input schema, what it returns), prompts/system instructions, installed skills, config, dependencies, and **exactly which library writes the .pptx** (python-pptx, pptxgenjs, other) and from what (a template file, or built from scratch).
2. Trace one full generation end to end: user request → research → content → slide objects → file. Note where decisions about *layout*, *font size* and *box size* are made, and by whom (LLM, template, code).
3. Open `reference/mcp_generated_sample.pptx` and the reference deck and compare. **Verify or refute each hypothesis below against the code.** They come from inspecting the sample's XML and renders; I could not see the server code, so treat them as leads, not facts.

### Findings from the sample deck (verify in code)

| # | Observation in `mcp_generated_sample.pptx` | Reference deck | Likely cause to check |
|---|---|---|---|
| H1 | Average **316 words per slide** (range 154–430). | ~118 | No word budget; content goes straight from research to slide. |
| H2 | Body text mostly **8–9.5 pt**; smallest 7.8 pt. Most runs are 8.19 pt. | Body 11–13 pt, floor 10 pt (footers 9) | Font size is shrunk to fit text into fixed boxes instead of cutting or splitting content. |
| H3 | Rounded cards are **~60% empty** while the text inside is tiny. | Card height follows content | Box geometry is a fixed grid chosen before the content is known; no measure-then-size step. |
| H4 | **7 of 10 slides use the same layout** (title + row of 3–5 tall rounded cards). | 8 distinct layouts across 10 slides | No layout selection logic; one generic renderer. |
| H5 | **0 charts, 0 tables, 0 pictures** (except the logo). Slide 4 is the ELITIA BI slide and has no dashboard mockup. | 2 native charts, dashboard mockup, 2 native tables, process and hub diagrams | Renderer only knows "textbox + rounded rectangle". No chart, table, diagram or dashboard primitives. |
| H6 | Theme part is the **default Office 2007 palette** (1F497D / EEECE1 / 4F81BD…); every colour and font is hard-coded on shapes (Calibri, slate/navy hex). | Real theme colours/fonts applied (Inter, Lumbini palette) | Starts from the library's default template and never edits the theme. |
| H7 | **No placeholders on any slide** (titles are plain text boxes); the 11 default layouts are unused. `presentation.xml` declares 4:3 while the size is 16:9. | Titles are real placeholders on defined layouts | Slides built on a blank layout. Outline view, accessibility and "Reset slide" are broken. |
| H8 | Flat near-white background; Lumbini logo only on the cover; no footer, no slide numbers, no brand motif. | Background texture, corner motif, footer and slide number on the master | Branding is applied per slide (or not at all), not on a master. |
| H9 | Each section has 3–6 dense bullets plus "Strategic Value / Deliverable / Core Objective" sub-lines. The slide reads like a document page. | One message per slide, short statements, visuals carry the logic | The prompt asks for "comprehensive" content per slide; nothing distils it for a presenter. |
| H10 | Speaker notes are long scripted paragraphs. | Short notes with caveats and sourcing | Fine to keep, but content that belongs in notes is also on the slide. |
| H11 | Cover slide also carries a "Four Integrated Workstreams" box that belongs on the solution-overview slide. | Cover is cover only | Content-to-slide allocation is not planned. |
| H12 | No visible QA step: overlaps and emptiness shipped. | Rendered and reviewed before delivery | No render-and-inspect loop. |

**Also record what the current system does well** (research quality, content accuracy, caveats such as "illustrative KPIs vs confirmed capabilities", placeholders for commercials). Preserve all of it.

**Deliverable of Phase 0:** `docs/ppt-audit.md` with: architecture map, the table above marked CONFIRMED / REFUTED / PARTIAL with file and line evidence, anything else you find, and a keep / change / add list. Show me this before Phase 2 if you can; otherwise continue but flag decisions.

---

## 2. Target architecture

Do **not** rebuild the server. Keep research as it is. Insert separate, inspectable stages between research and file output, each producing a JSON artifact that the next stage validates. The core defect is that one step goes from "text" to "slides". Split it.

```
brief ─► [1 Research]        EXISTING, unchanged  ─► research.json (facts + sources + confidence)
      ─► [2 Storyline]       NEW  ─► storyline.json   one message per slide, action titles, flow
      ─► [3 Distill]         NEW  ─► slides.content.json  word budgets enforced, notes split out
      ─► [4 Visual plan]     NEW  ─► deck.spec.json   layout + visual chosen per slide (deterministic rules)
      ─► [5 Render]          REWORK ─► deck.pptx      theme + masters + native objects, no ad-hoc geometry
      ─► [6 QA]              NEW  ─► qa-report.json + previews/*.png   automated checks + visual review
      ─► [7 Fix loop]        max 3 iterations back to 3/4/5 based on QA findings
```

### Stage rules

**2 Storyline (consultant).**
- Produce an executive-level pyramid: the single deck message first, then supporting slides, then the ask or next step. For proposals: context → requirements → solution → proof/how it works → approach → commercials.
- Every slide gets: `message` (one sentence stating what the audience must conclude), an **action title** (≤ 9 words, states the point, not the topic), `evidence` (which facts support it), and `audience_takeaway`.
- Reject topic-label titles ("Overview", "Details"). Reject slides that carry two messages: split them.
- Allocate each fact to **exactly one slide**; cross-slide repetition is a defect.

**3 Distill (word budgets, hard limits enforced in code, not by prompt).**
- Slide ≤ 120 words target, 160 hard. Cover ≤ 50. Dense reference slides (commercials, terms) ≤ 200 and flagged.
- Bullet ≤ 12 words. ≤ 6 items per container. ≤ 3 lines per card description.
- Anything cut from the slide moves to **speaker notes** (trimmed) or an appendix list, never silently dropped. Keep facts intact; shorten wording.
- Never invent numbers, names, dates, durations or prices. Unknown commercial values become visible editable placeholders (`[Amount]`).
- Maintain a **capability registry** (`capabilities.yaml`): each product/service claim with `status: confirmed | proposed | illustrative` and a `source`. The Distill and QA stages must label slide content accordingly (for example dashed boxes + caption for illustrative KPIs) and must refuse to state a `proposed` item as a confirmed capability.

**4 Visual plan (layout intelligence).**
- Every slide gets a `content_shape` tag (the LLM may propose it; code validates it) and the layout is then picked by the **rule table below**, not by free choice. This is what stops the "same card row everywhere" problem.
- Rules: no layout used on more than 2 consecutive slides; a 10-slide deck uses ≥ 6 distinct layouts; every slide except cover/closing has at least one non-text visual (diagram, chart, table, icon set, mockup).

| content_shape | Layout | Use when |
|---|---|---|
| `cover` | cover | first slide |
| `requirement_to_outcome` | 3-column "today → outcome" rows | challenges vs desired results |
| `hub_and_spokes` | hub diagram with labelled arrows | one system fed by several workstreams |
| `process_linear` (4–7 steps) | chevron or numbered step line with deliverables band | methods, migrations, pipelines |
| `flow_with_actions` | boxed flow with a dashed drop-line to an action under each box | integration/data flows |
| `phases_over_time` | roadmap rows with sequence bars (no invented dates) | phased plans |
| `levels_x_dimensions` | matrix grid with row headers (stakeholder level × domain) | audiences × reporting areas |
| `metrics_trend` | native chart(s) + KPI row | any quantitative message |
| `dashboard_concept` | dashboard mockup (KPI tiles, filter tabs, 2 charts, drill ladder) | BI / analytics products |
| `architecture` | layered or left-to-right component diagram | systems and integrations |
| `comparison` | side-by-side columns or table | options, before/after |
| `roles_and_terms` | native table(s), compact | resources, commercials, T&Cs |
| `key_takeaways` | 3–4 stat/claim tiles | executive summary |
| `deliverables` | icon + label band | outputs per workstream |

**5 Render.** See sections 3 and 4.

**6 QA and 7 Fix loop.** See section 6.

---

## 3. Corporate theme as a reusable design system

Create `themes/<name>/` as the unit of branding. Lumbini is the first. Nothing in the renderer may hard-code a colour, font, size or margin. Everything reads from `tokens.json`.

**Lumbini tokens (extracted from the Lumbini SAP GRC corporate deck; already in `themes/lumbini/tokens.json`):**

- Fonts: **Inter** for everything, **Inter Bold** for titles/headings, **Inter SemiBold** for labels and eyebrows. No other fonts. Fallback chain for rendering where Inter is absent: `Inter → Segoe UI → Calibri`; bundle the OFL font files in `themes/lumbini/fonts/` and note that machines without Inter will substitute.
- Colours: text dark `141E2D`; primary blue `0070C0`; deep blue `0066B4`; navy `1F497D` (pills, dark bands, table headers); orange `F78B15` (highlights, placeholders, one accent per slide); grey text `646E78`; border `DCE1E6`; pale surface `EEF3F8`. One dominant colour (blue) plus navy; orange is an accent only.
- Background: the lightened paper-fold image on every slide.
- Motif: blue corner blocks top-right (four rectangles forming the "E" mark; coordinates in tokens) and a blue strip bottom-left. These live on the **master**, never on slides.
- Cards: white, `DCE1E6` 1 pt border, soft shadow, large corner radius. Cards are a component, not the architecture of every slide.
- Cover: logo top-right, faded wireframe illustration top-left, bold left-aligned title, orange rule, blue subtitle, navy pill bottom-right.
- Type scale: title 24 pt bold; eyebrow 11 pt SemiBold caps blue; subtitle 13 pt grey; body 12–13 pt; caption/labels ≥ 10 pt; footer/slide number 9 pt. **Nothing else below 10 pt.**
- Spacing: 0.65" side margins, content starts y = 1.85", 0.3" minimum gap between blocks, footer at y = 7.1".

**Implementation requirements**
1. Write the theme into the file's real theme part (`theme1.xml` colours and font names) so a user can restyle in PowerPoint. (pptxgenjs: `pres.theme` + a post-write step that writes colours; python-pptx: edit the theme XML.)
2. Define **slide masters/layouts** (cover, content, section divider if needed) containing background, motif, footer, slide number and a **title placeholder**. Slides fill the title placeholder; they do not draw their own title.
3. Use scheme colours for shapes wherever the API allows; hex only where it does not (chart series, some shadows).
4. Set slide size 13.333" × 7.5" and make sure `presentation.xml` is consistent (no 4:3 flag).
5. Theme selection is a parameter (`theme: "lumbini"`). Adding another brand = adding a folder, not touching the renderer.

---

## 4. Renderer primitives (what to add to the server)

Port these from `reference/reference_build.js` into reusable, tested functions. Each takes a spec object and tokens, and **computes its own geometry from content** (see "measure then size" below).

- `titleBlock(eyebrow, title, subtitle)`
- `card(box, content)`; `cardColumns(n, items)` with height driven by tallest content (no fixed tall boxes)
- `hubDiagram(hub, spokes[])` with labelled directional arrows
- `chevronFlow(steps[])`; `stepLine(steps[], deliverables[])`; `flowWithActions(boxes[], actions[])`
- `roadmapRows(phases[], activities[])` (sequence bars; **no durations unless supplied**)
- `matrixGrid(rowHeaders[], colHeaders[], cells[][], illustrative: bool)` (dashed borders when illustrative)
- `kpiTile(label, value, delta)`; `dashboardMock({tabs, kpis, charts, drillSteps})`
- `nativeChart(type, series, options)` (bar / column / line / combo / doughnut) with a shared style preset
- `table(headers, rows, colWidths)` (native table, header in navy, placeholder cells in orange)
- `deliverablesBand(items[])`, `calloutStrip(text, icon)`, `iconCircle(name)`
- `legend(items[])`

**Measure then size (fixes H2 and H3).** Before drawing, measure each text block with real font metrics (e.g. Pillow `ImageFont` on the Inter TTF, or the library's own measurer) at the token font size. Then:
1. Compute the required height and set the box/card to it plus padding.
2. If it does not fit the slot, **do not shrink the font**. In order: shorten wording (re-call Distill), reduce item count, split the slide. Floor is 10 pt.
3. If a container ends up > 35% empty, shrink the container or add the missing visual. Do not leave tall empty cards.

**Charts and dashboards (fixes H5; section "meaningful and relevant").**
- Use **native, editable** PowerPoint charts, never pictures of charts.
- Chart type chosen by data shape: trend over time → line; ranking/category comparison → bar/column; part-to-whole (≤ 5 parts) → doughnut or stacked; target vs actual → bar + line. Max 6 categories, one message per chart, the chart title states the measure and unit, data labels on, gridlines light, same palette and font on every chart.
- Data provenance rule: chart values come from research, user input or a named source. If none exist and the chart is a concept, it must be visibly labelled **"Illustrative layout, not client data"** and generated with fixed seeds so it is stable between runs. Never present invented numbers as findings.
- Dashboard mockups must mirror the **real** product's structure from the capability registry (for example KPI cards vs plan and prior year, dimension split, records view, detail page), not generic charts. Include filter tabs and a drill-down ladder so the slide explains the concept.

**Images.**
- Prefer diagrams, native shapes and the brand assets over stock photography. Do not add decorative stock images.
- Any raster must be ≥ 150 dpi at its placed size, keep its aspect ratio (no stretching), be cropped not squeezed, and carry alt text.
- No AI-generated images containing text or logos. Logo only from `themes/<name>/assets`.
- Do not add an image-generation MCP/tool unless the audit shows a concrete need.

**Editability.** Everything is native: text boxes, shapes, tables, charts, grouped logically with meaningful names (`objectName`), speaker notes via the notes API, no flattened images of slides or text.

---

## 5. Skills: create only what is genuinely needed

First check whether the IDE/agent already has presentation skills installed; reuse them. Otherwise create these four (short SKILL.md each, with trigger conditions, rules, and 1–2 worked examples taken from the reference deck). Keep them small and rule-based so the agent reads them every time.

1. **`presentation-storytelling`**: pyramid structure, action titles, one message per slide, the allocation rule (each fact once), proposal/strategy/technical-deck templates, word budgets, banned phrases ("world-class", "revolutionary", "seamless", "best-in-class", unsubstantiated superlatives).
2. **`lumbini-design-system`**: the tokens, typography scale, spacing, motif, component specs, cover and content layouts, do/don't list (no accent lines under titles, no centred body text, no more than one orange accent per slide).
3. **`data-viz-and-dashboards`**: chart-type decision table, chart style preset, provenance and "illustrative" labelling rules, dashboard-mockup anatomy, KPI formatting (units, ▲▼ semantics), how to read the capability registry.
4. **`pptx-render-and-qa`**: the renderer API, the layout rule table, library gotchas (below), the QA checklist, and how to run the render-and-inspect loop.

**Library gotchas learned building the reference (pptxgenjs; adapt if you use python-pptx):** hex colours without `#`; never share an options object between calls (it is mutated); shadow offset must be ≥ 0; `rectRadius` applies only to rounded rectangles; table cell margins are in inches in recent versions (points make cells explode); title placeholder alignment must be set on the master or titles centre; stacked-bar data labels cannot be `outEnd`; set the theme colours with a post-write step; text boxes carry internal padding, so set margin 0 when aligning with shapes; LibreOffice substitutes fonts it lacks, so layout checks must use the real font metrics.

---

## 6. Quality gates (automated, in code)

Implement `qa_deck(pptx, spec)` returning `qa-report.json` with `blocking`, `warning` and `info` findings per slide and per deck. Also render every slide to PNG (LibreOffice headless → PDF → `pdftoppm`; check availability and install guidance in the audit) into `previews/`.

**Slide-level, blocking:**
- Any shape outside the slide, or text overflowing its shape (measure with real metrics and confirm on the render).
- Overlap between unrelated shapes (containment of a label inside its card is allowed).
- Any font < 10 pt (footers/slide number ≥ 9 pt allowed).
- Words > 160 (cover > 60).
- Text/background contrast below 4.5:1.
- Empty title placeholder; leftover placeholder text; `lorem`, `TODO`, `[insert`.
- Image distortion (aspect ratio differs from source by > 2%) or low resolution.
- Chart with no title, no units, or > 6 categories.
- A `proposed` capability stated as `confirmed`; a numeric claim not traceable to a source or flagged illustrative.
- Banned marketing phrases.

**Slide-level, warning:** container > 35% empty; fewer than 1 non-text visual (non-cover); three or more lines of a bullet > 12 words; missing alt text; missing speaker notes.

**Deck-level, blocking:** slide count differs from the brief; the same layout on > 2 consecutive slides; fewer than 6 distinct layouts in a 10-slide deck; duplicated content across slides (similarity > 0.8); inconsistent terminology or numbers for the same entity across slides; the file fails to reopen (re-open with the writer library and convert with LibreOffice without error).

**Visual review step.** After the automated checks, look at the rendered PNGs (use a vision-capable model call or, at minimum, a contact-sheet review) and score each slide 1–5 on: hierarchy, alignment/spacing, density, visual relevance, brand consistency. Anything < 4 returns to Stage 3/4/5 with the reason. **Maximum 3 fix iterations**, then ship with the remaining issues listed, not hidden.

Never claim the file "opens perfectly in PowerPoint" from a LibreOffice render alone. State what was actually verified.

---

## 7. MCP tool changes (minimal)

Inspect the current tool list first and map. Expected shape (rename to fit what exists):

- Keep: existing research/search/content tools unchanged.
- Add `plan_storyline(brief, research)` → `storyline.json`
- Add `plan_visuals(storyline)` → `deck.spec.json` (applies the layout rule table and word budgets, validates against a JSON Schema)
- Rework `create_presentation` / `render_deck(spec, theme)` → `.pptx`; it must refuse specs that fail schema validation instead of guessing
- Add `qa_deck(pptx, spec)` and `render_previews(pptx)`
- Add `list_layouts()` and `list_themes()` so the agent can discover options
- Backwards compatibility: if the old single-call tool is used, route it through the new pipeline.

Define the spec with a JSON Schema checked into the repo. The LLM fills **content and `content_shape`**; code owns geometry, fonts, colours and layout choice. That division is the main architectural change.

---

## 8. Test and acceptance

Generate and keep under `tests/out/`, each with its `qa-report.json` and previews:

1. **Regression:** the SGG proposal from the same brief as the reference (10 slides). Compare against the reference deck side by side.
2. A 10–12 slide **SAP/S/4HANA migration approach** deck for a manufacturing client.
3. A **corporate strategy / digital transformation roadmap** deck including at least one quantitative slide with real chart data supplied in the brief.

**Acceptance (all must hold):**
- Average ≤ 130 words/slide; no body text < 10 pt; no blocking QA findings.
- ≥ 6 distinct layouts per 10 slides; ≥ 1 native chart where the brief has numbers; ≥ 1 native table where there are roles/commercials; a dashboard mockup for any BI product slide.
- Titles are real placeholders on master-defined layouts; theme colours/fonts are the real theme; brand motif, footer and slide number come from the master.
- Re-opens cleanly in the writer library and converts in LibreOffice; every shape editable.
- No unsupported claims: every capability line traces to the registry; illustrative items are visibly labelled.
- Research accuracy unchanged versus before: diff the facts in `research.json` for the regression brief.

**Known weaknesses of the reference deck itself. Do not copy them:** slide 10 carries ~200 words at 10 pt (split into two slides or use an appendix when allowed); the dashboard mockup labels are 9 pt (raise to 10); no executive-summary slide exists (add one for decks over 8 slides); decorative orange is used sparingly, keep it that way.

---

## 9. How to report back

When finished, give me:
1. `docs/ppt-audit.md`: findings confirmed / refuted with evidence.
2. `docs/target-architecture.md`: stages, artifacts, tool list, the rule tables.
3. A change list: files added/modified, what was kept, what was replaced and why.
4. Test results: the three decks, their QA reports, before/after previews, the acceptance checklist with PASS/FAIL per line.
5. Anything not done or not verified (for example "PowerPoint desktop rendering not tested").

**Constraints:** preserve working research and content features; no new dependencies without a one-line justification; small, reviewable commits; configuration and tokens in files, not in prompts; never trade information accuracy for visual appeal. If a rule here conflicts with what the audit shows, tell me and propose the smallest change that achieves the goal.
