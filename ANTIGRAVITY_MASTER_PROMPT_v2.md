# MASTER INSTRUCTION v2: Adaptive layouts, nexus research, panel review, transformation storytelling

This **extends** `ANTIGRAVITY_MASTER_PROMPT.md` (v1). Everything in v1 still applies (Phase 0 audit, stage pipeline, Lumbini tokens, renderer primitives, QA gates, acceptance tests) **except where this file overrides it**. Where they conflict, v2 wins. Read v1 first, then this.

New evidence for this version: `reference/negative_example_datasphere.pptx`, a deck the current pipeline produced after it was given the Lumbini reference deck. It reused the reference deck's *layouts* instead of designing layouts for its own topic. This version fixes that.

---

## 1. The defect: "layout copying" (verify in code, do not assume)

Inspect `negative_example_datasphere.pptx` (topic: SAP Datasphere career path) against `reference/SGG_ELITIA_BI_Odoo_Proposal_Lumbini.pptx` (topic: SGG proposal). The facts below were read from the file.

| Evidence | What it shows |
|---|---|
| Slides 1–7 appear in the **same order and the same compositions** as reference slides 1, 2, 3, 4, 5, 9, 10: cover → requirement/today/outcome rows → hub diagram → dashboard mockup → matrix → roadmap → A/B/C tables. | Layout choice was inherited from the reference deck, not derived from the new topic. |
| Slide 2 keeps the column headers **REQUIREMENT / TODAY / DESIRED OUTCOME**; role names (Traditional BW Modeler…) sit under "REQUIREMENT". | Content was forced into a structure that does not fit it (a career-evolution story is not a requirements-to-outcomes story). |
| Slide 3 reuses the hub diagram with the letters **A–D** and the labels **"Data in / Data out / Improves"** for four unrelated "pillars". | The diagram claims a data-flow relationship that does not exist. Meaningless arrows are worse than no diagram. |
| Slide 4 keeps **"ELITIA BI"**, **"Illustrative layout, not SGG data"**, **"Drill from summary to source"**, and chart titles **"Revenue vs plan by business unit (%)"** over hiring statistics. A second chart plots seniority levels with rotated, overlapping labels. | Strings from the reference leaked into a different subject. A dashboard mockup was used because the reference had one, not because the story needed one. |
| Slide 5 keeps the strip **"Confirmed in ELITIA BI"**. Row-header text is clipped. | Same leak, plus no measure-then-size. |
| Slide 7 reuses the commercials/terms A/B/C table layout for roles, certifications and an action plan, leaving a large empty band. | Layout reused for a different information type. |
| Footer on every slide: **"Confidential proposal for SGG"**. | Master footer is not parameterised by deck metadata. |
| Slide 4 shows "+142%", "68%", "+35%", "84%" with no source. | Numbers presented as findings without provenance. This is an accuracy failure, not a design failure. |

**Root cause to confirm:** the agent treats a finished deck as a template ("fill slide N with new content") instead of treating it as evidence of a *quality standard*. The fix is architectural: separate **what is fixed** (brand and components) from **what must be decided fresh every time** (composition).

---

## 2. New principle: three levels, only two are fixed

| Level | What it is | Fixed or generated |
|---|---|---|
| **A. Design system** | Tokens, fonts, master/layout frames, motif, footer, type scale (v1 §3) | **Fixed.** Same for every Lumbini deck. |
| **B. Component library** | Content-free parameterised atoms: card, node, arrow, chevron, tile, table, native chart, band, axis, timeline marker, matrix cell, swimlane, stack layer, callout, icon | **Fixed.** No component may contain topic text or a default label. |
| **C. Composition** | Which components, arranged how, to express *this* slide's relationship | **Generated per slide, per topic.** Never copied from another deck or slide. |

The reference deck demonstrates the **craft** (hierarchy, spacing, density, native objects, restraint). It is **not** a catalogue of slide templates. Remove any code that loads the reference deck, a "layout per content_shape" table that maps to fixed slide geometries, or any slide-level template with embedded text. Keep only A and B as reusable assets. Port the patterns in `reference_build.js` into level-B functions with no strings inside.

---

## 3. Relationship-first visual planning (replaces v1 §2 Stage 4 table)

**Step 1: extract the relationship.** For each slide the Storyline stage already has a message. Add a `relationship` object, produced by the LLM and validated by schema:

```json
{
  "type": "causal_loop | constraint_flow | layered_stack | before_after_shift | tradeoff_matrix | sequence | progression | decomposition | comparison | distribution | trend | network | governance_map | evidence_claim",
  "elements": [{"id":"", "label":"", "role":"", "weight":0-1}],
  "links": [{"from":"", "to":"", "kind":"causes|feeds|constrains|contains|precedes|replaces|governs|measures", "strength":0-1}],
  "hierarchy": "none | tiers | nested",
  "time": "none | ordered | dated",
  "quantity": "none | ordinal | measured",
  "so_what": "one sentence"
}
```

If the content has no genuine links, the relationship is `decomposition` or `comparison`. **Do not invent links to justify a diagram.**

**Step 2: choose a visual grammar** from the relationship, with at least two candidates scored on fit. Fit uses: element count (3–7 is ideal), whether links are directional, whether time is ordered, whether quantities exist, and the audience's question. Pick by score and record the reason in `deck.spec.json` (`layout_rationale`). Examples (extend as needed; this is guidance, not an enumerated template list):

| Relationship | Strong grammars | Avoid |
|---|---|---|
| Reinforcing/balancing causes | causal loop diagram with R/B markers and delays | bullet columns |
| Throughput limited by one step | linear flow with the constraint highlighted, buffers, and a "what moves if this moves" annotation | equal-weight cards |
| Layers of responsibility (ISA-95 levels, enterprise layers, platform stack) | stack with level labels and the data/control flow between layers; swimlanes for who-does-what | hub diagram |
| Before → after change | two-state view plus an **iceberg or layered "what changed beneath"** panel (events → patterns → structures → mental models) | three-column "today / outcome" rows |
| Choice between options | 2×2 or weighted matrix with the decision criterion on the axes | long text comparison |
| Operating-model choice | standardisation-vs-integration quadrant | generic matrix |
| Capability maturity | staircase or heatmap by capability | roadmap bars |
| Variation, defects, quality | Pareto or control-chart style native chart with annotations | pie chart |
| Time with inflection points | timeline with decision markers and what almost failed | phase table |
| Quantity over time | native line/column with direct labels and a one-line "so what" | a dashboard mock |
| Ownership/decision rights | RACI or decision-rights grid | paragraph |

A dashboard mockup is justified **only** when the slide is about a monitoring/decision surface that the audience will use. A hub diagram only when one system really is the centre of several data flows.

**Step 3: compose geometry with a solver, not a template.** Use a 12-column grid, the content-top and margins from tokens, and the measure-then-size rule (v1 §4). Atoms are placed by rules: alignment, equal gutters, proportional weight by `weight`, label placement outside connectors, minimum 0.3" gaps. If no pre-written composer fits, **compose from atoms**; do not fall back to a generic card row. A new topic may produce a layout that has never existed before. That is the intent.

**Step 4: diversity constraints** (deck level): no composition grammar used more than twice in a deck; adjacent slides must differ; at least one slide must use an *annotated* visual (a diagram or chart with callouts that carry the argument).

### Anti-copy controls (blocking in QA)

1. **String-leak check:** build the set of n-grams (3-grams and up, plus all proper nouns) from every reference deck and every previous output in `tests/out/`. Any such n-gram that appears in the new deck but not in the current research, storyline or brief is a **blocking** finding. Specifically catches "ELITIA BI", "SGG", "Illustrative layout, not SGG data", "Confirmed in …", "Drill from summary to source", "Revenue vs plan", "REQUIREMENT / TODAY / DESIRED OUTCOME". Stock labels such as "Data in" are also blocked unless they describe real flows in the new content.
2. **Layout-fingerprint check:** for each slide compute a signature (normalised bounding boxes of shapes, grouped by type, plus text-length histogram). If any slide matches a slide from a reference or earlier deck with similarity > 0.85, flag it and require a written `layout_rationale` that cites the *relationship* (not "the reference had it"). Also fail if more than 40% of slides match.
3. **Parameterised master:** footer, eyebrow style, cover pill, and slide numbers read from `deck.meta` (client, document type, confidentiality). No client or project name in the master text.
4. **Chart integrity:** chart title, axis titles, categories and units are generated from the data's own semantics. Max label length 14 characters or horizontal bars; never rotate labels past 30°; verify on the render that labels do not overlap or clip.
5. **Provenance:** every number on a slide carries a `source_id` from `research.json`, or is tagged `illustrative` and visibly labelled as such. A number with neither is blocking.

---

## 4. Skill: `transformation-nexus-research` (replaces generic research for strategy/transformation decks)

Create a skill (SKILL.md plus a `lenses.md`) that structures research and synthesis through seven lenses. **These are analytical lenses based on each author's published ideas. The agent must not impersonate them, invent quotes, or claim they endorse a conclusion.** Every claim attributed to a framework needs a retrievable citation; if a source cannot be found, state the idea without attribution. Verify each work by search before citing it.

| Lens | Question the lens forces | Typical evidence to look for |
|---|---|---|
| **Westerman** (digital transformation) | Did the enterprise change *what* it does with technology (digital capability) and *how it leads* (vision, governance, engagement)? Where is the gap between the two? | Leadership intent, governance, capability vs. leadership matrix |
| **McAfee** (digital enterprise) | What changed in how decisions are made and who makes them (data over HiPPO, platforms, crowds, talent)? | Decision rights, data usage in decisions, platform use |
| **Brynjolfsson** (AI-driven business) | Is the technology complemented by process and organisational change, and is the productivity "J-curve" visible (initial dip, later gain)? | Time-lagged outcomes, complementary investments |
| **Hammer** (reengineering) | Which work was *obliterated* rather than automated? What process assumption was removed? | Process before/after, handoffs removed, cycle-time logic |
| **Carr** (commoditisation) | Which part of the technology is now a commodity, and where does advantage actually sit (execution, risk discipline, cost)? | Vendor/standard vs. differentiating practices |
| **Schallmo** (digital transformation and business models) | Which business-model elements (value proposition, customer, value chain, revenue) changed, and in what sequence? | Business-model elements and the transformation roadmap |
| **Zeng** (digital business/ecosystem) | Which stakeholders and ecosystem links changed, and how do they co-create value? | Ecosystem map, partner roles |

*Verify the specific works and claims for the Schallmo and Zeng lenses before citing them; if they cannot be sourced, keep the lens as a question set without attribution.*

**Procedure:** (1) Gather facts from `CASE_FACTS`, user documents and web research with source ids. (2) For each lens, answer its question with evidence or mark it `no evidence`. (3) Build a **contradiction table**: where lenses disagree (for example Carr vs McAfee on differentiation) and what the evidence says. (4) Output `nexus.json`: for each lens, findings, evidence ids, confidence, and "what would change my mind". (5) The Storyline stage must consume `nexus.json`, and the deck must make visible the tensions, not just a harmonised story.

Cap research cost: 7 lenses run as parallel short tasks with shared fact base; synthesis happens once.

---

## 5. Stage: Panel review (new, runs after v1 QA and before delivery)

Implement `panel_review(deck.pptx, storyline.json, nexus.json, previews/)`. Thirteen **independent** reviews, each in a fresh context that sees only the extracted slide text, rendered PNGs and the storyline (not the other reviewers' output), followed by one synthesiser.

**Honesty rules:** this is a *simulated lens review*, a structured critique using each thinker's published frameworks. It is not their opinion, endorsement or quote. Never put names, quotes or "reviewed by" claims on slides or in the client-facing file. Reports use the form "Lens: Ross (operating model)", never "Jeanne Ross says". The panel records evidence by slide number.

| Reviewer lens | Primary test | Typical failure |
|---|---|---|
| Ross (enterprise operating model) | Is the operating model choice (standardisation vs integration) explicit, and do the capabilities and decision rights follow from it? | Technology described without an operating model |
| Zachman (enterprise ontology) | Are the *what / how / where / who / when / why* of the enterprise each covered, and consistent in vocabulary? | A missing perspective; terms that change meaning between slides |
| Jacobson (architectural intent) | Is the architecture's purpose and its key use cases clear? Are the boundaries and responsibilities explicit? | Diagram of boxes with no stated intent |
| Brandl (ISA-95) | Are enterprise/plant/line/cell levels and the data exchanged between them correct and consistent? | Mixing levels; a MES described as an ERP |
| McClellan (MES architecture) | Are plant-floor execution functions placed correctly (dispatching, tracking, genealogy, quality, performance) and not overclaimed? | MES capabilities claimed that the evidence does not support |
| Senge (systems thinking) | Are feedback loops, delays and the mental models visible? | Linear story of a system with loops |
| Ackoff (interactive design) | Is the *problem* framed as a mess of interacting issues, with who designs the future? Is there an idealised end state? | Solving the stated problem rather than redesigning the system |
| Meadows (systems design) | Is the intervention at a high-leverage point (rules, information flows, goals, paradigms) or only parameters? | Only buying tools; leverage not discussed |
| Deming (quality philosophy) | Is variation understood (common vs special cause)? Is improvement systemic rather than blaming people? | Metrics without system understanding; targets driving gaming |
| Goldratt (constraints) | Is the constraint named, exploited, subordinated, elevated? Did the constraint move? | Optimising non-constraints |
| Westerman (digital transformation) | Digital capability and leadership capability both addressed? | One without the other |
| McAfee (digital enterprise) | Does the story show a change in decisions and information flow, not just tooling? | Tool deployment as the outcome |
| Brynjolfsson (AI-driven business) | Complementary organisational change and measurable outcomes over time; AI claims proportionate? | Unsupported AI claims; no complements |

**Scoring and gating.** Each reviewer returns: score 1–5, up to three **specific** findings with slide numbers, one concrete fix per finding, and a `blocking: true|false` flag for a factual or conceptual error. The synthesiser merges duplicates and orders by impact. **Gate:** mean ≥ 4.0, no lens below 3, no blocking finding open. If it fails, send findings to the Storyline/Distill/Visual/Render stages and re-run **only** the affected slides, at most **2 rounds**. Ship with the remaining items listed rather than hiding them. Also run an **audience pass** (CEO/COO, CIO/CTO, Plant Head, SAP architect): for each, "what decision does this deck help me make, and what would I challenge?".

Deliver `panel-report.md` alongside the deck, separate from the .pptx.

---

## 6. Brief template for transformation decks (the "reconstruction, not success story" brief)

Pass this as the deck brief with the case parameters filled in. If `CASE_FACTS` is empty, the agent must **stop and ask** for the case, or build a clearly labelled **archetype / prototype** (title carries "Illustrative reconstruction", all metrics tagged illustrative, no real company names). It must never present invented metrics or invented clients as fact.

```
TOPIC: {TOPIC}
CASE_FACTS: {facts, sources, or "none: build labelled archetype"}
AUDIENCE: CEO, COO, CIO, CTO, Plant Head, manufacturing leaders, digital transformation
leaders, SAP enterprise architects, executives making investment decisions.
They do not care about software. They want to understand why transformations succeed or fail.

You are reconstructing a business transformation that happened inside an enterprise. You are
not writing a customer success story. Reveal what actually changed beneath the implementation,
not merely what was deployed.
```

**Narrative spine (adapt, do not template):**
1. The belief the enterprise held, and the constraint that was actually binding.
2. What was really broken (structure, decision rights, information flow, incentives, mental models), not the symptom.
3. The intervention in terms of changed rules and flows, not product features.
4. How the system responded: reinforcing loops, delays, the constraint moving, what got worse first.
5. What almost failed and why (adoption, data ownership, governance, scope).
6. The new equilibrium: what is now different in how decisions are made, with evidence labelled observed / inferred / illustrative.
7. What leadership must decide next, and the conditions under which this would *not* work.

Slide-level rules: action titles; one message per slide; include at least one slide on **failure modes and counterfactuals**; no vanity metrics; no logo walls; no "seamless / world-class / revolutionary".

**One coherent industrial platform, not seven unrelated slides.**
- Build a single **platform map** (for manufacturing: enterprise → plant → line → cell, aligned to ISA-95 levels, with the data and control flows between them). Reuse a small version of it as a **locator** in a fixed corner of each content slide, highlighting where the slide sits. The locator is a Level-B component with data from `deck.meta`, not a copied picture.
- One running example (a plant, a line, a constraint) threaded through the slides so evidence accumulates.
- Consistent vocabulary: keep a `glossary.json` (term, definition, level). The QA stage checks that terms are used consistently.
- Consistent icon family and colour semantics (blue = system/enterprise, navy = control/governance, orange = constraint or decision point, grey = context). Define this in tokens.

---

## 7. Changes to v1 acceptance tests

Replace v1 §8 test 2 and 3 with:
- **Test A (anti-copy):** regenerate the SAP Datasphere career-path deck from the same brief. Pass only if the string-leak check is clean, the layout-fingerprint check matches the SGG reference on ≤ 1 slide, and at least three of its slides use compositions that do not exist in the SGG reference.
- **Test B (transformation):** a manufacturing transformation deck (ISA-95/MES context) from a supplied or labelled-archetype case, 10–12 slides, passing the panel gate.
- **Test C (strategy):** a corporate digital-transformation strategy deck with at least one chart built from supplied data.
- Report the layout grammar chosen for each slide with its rationale, so I can judge whether it fits the topic.

Updated acceptance additions: no leaked strings; every number sourced or tagged; footer/eyebrow come from metadata; panel gate passed or open items listed; chart labels legible on the render; no meaningless connectors.

---

## 8. Report back

Same as v1 §9, plus: (a) the confirmed root cause of the layout copying, with file and line; (b) the list of level-A and level-B assets and what you deleted as template-like; (c) the string-leak and fingerprint results for each test deck; (d) `panel-report.md` for each test deck; (e) anything you could not verify.
