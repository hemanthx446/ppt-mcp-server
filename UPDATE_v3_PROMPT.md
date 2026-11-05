# UPDATE v3: fix fixed sections and clipped text, install two skills

Paste this into the Antigravity agent. It extends `prompts/ANTIGRAVITY_MASTER_PROMPT_v1.md` (v1) and `prompts/ANTIGRAVITY_MASTER_PROMPT_v2.md` (v2). Where they conflict, v3 wins. **Work in the terminal, in this order. Do not skip step 1.**

New evidence: `reference/negative_example_datasphere_after_v2.pptx` is the deck your pipeline produced after v2. The theme, fonts and visual identity are right. Two defects remain, and a few smaller ones are listed in §4.

---

## 1. Terminal steps

1. Unzip this kit at the project root (or the folder you choose) and read this file, `README_TERMINAL.md` and the two skills.
2. Install the skills: `bash install_skills.sh` (see README_TERMINAL.md for the target path; confirm the path Antigravity actually reads before relying on it).
3. Reproduce the defects before changing code:
   `python3 -I tools/qa_pptx.py reference/negative_example_datasphere_after_v2.pptx --slack 1.12`
   Expected: BLOCKING `NOWRAP_OVERFLOW` on slide 3 ("Tier 1–4" labels need up to ~2.8in in a 1.8in box), `TEXT_TALLER_THAN_BOX` on slide 5, an unresolved `[SRC-DS-01]` token on slide 4, and a section finding. Warnings for 9–9.5pt text and 190 words on slide 7.
4. Find the code that (a) creates sections, (b) creates text boxes. Report file and line for each, then fix per §2 and §3.
5. Regenerate the Datasphere deck and one SGG-style proposal. Run `qa_pptx.py` on both. Zero BLOCKING findings is the exit criterion. Render previews and look at them.

---

## 2. Defect 1: sections are fixed, and some are empty

**Observed:** the v2 deck has the sections `Introduction / Solution / Workstreams / Implementation / Commercials`. In PowerPoint the navigator shows `Workstreams (2)`, `Implementation (0)` and a `Commercials` section on a career guide that has no commercials. These are the section names of the SGG proposal (`reference_build.js`), carried over as constants.

**Root cause to confirm in code:** the section list is a constant (or an LLM-fixed template) assigned by slide position, not derived from this deck's storyline.

**Required behaviour**
1. Sections are the **acts of this deck's storyline**. Decide them after the slide plan exists, name them in the topic's own language in 1 to 3 words (for example a career guide: "Where it started", "The shift", "Your pathway"; a transformation case: "The visible story", "What was beneath", "What changed").
2. Create **no sections** for a deck under 8 slides. Otherwise 2 to 5 sections, each with at least 2 slides, covering every slide exactly once, contiguous.
3. A section named `Commercials`, `Implementation` and so on exists only if the storyline has that act and slides in it.
4. Use `tools/sections.py` (`plan_ok`, `write_sections`) when building with python-pptx, or `tools/rebuild_sections.py in.pptx out.pptx sections.json` to rewrite or remove sections on an existing file (`[]` removes them all). python-pptx has no sections API, so the helper writes `p14:sectionLst` into `presentation.xml`.
5. `tools/qa_pptx.py` blocks on: empty section, stray `Default-N`, names not in the storyline, and the inherited SGG name set.
6. In `reference/reference_build.js` the section names are SGG-only data. Never reuse them.

---

## 3. Defect 2: letters cut off, text not wrapping

**Observed:** labels such as "Tier 4: Analytics Consumption" are cut at the edges of their rounded node (screenshot: "…Analytics Consumpt"). The cover pill "Career Architecture | SAP Datasphere" overflows its pill. Same pattern elsewhere.

**Evidence from the file (slide 3):** the label is a **separate text box** laid over the node: `<a:bodyPr wrap="none"><a:spAutoFit/>`, width 2.0in, text measured at 2.69in (Inter Bold 13pt). Text boxes are named `TextBox N`, which indicates the generator is **python-pptx**. python-pptx's `add_textbox()` defaults to `wrap="none"` plus `spAutoFit`, so text never wraps and runs past its container. The font on the viewing machine also appeared as a fallback font (Inter was not installed), which is wider or narrower and makes it worse.

**Required behaviour**
1. **Label text lives inside the shape** (node, pill, chevron, card, tile), not in an overlaid text box. Container and text cannot drift apart. Free-floating text boxes are only for captions and titles with explicit widths.
2. **Never `wrap="none"`.** Always `word_wrap = True`, `auto_size = NONE`, explicit insets, explicit vertical anchor.
3. **Run-level formatting.** Write font, size, bold, colour on every run (`a:rPr`), not only via `paragraph.font` (which writes `a:defRPr`).
4. **Measure, then size.** Use the real `Inter-*.otf` files (`themes/lumbini/fonts`) via `tools/textfit.py` to measure; lay out with a **12% safety margin** for font fallback and gate with `qa_pptx.py --slack 1.12`. If text does not fit at the type-scale size, in order: shorten the wording, widen or re-layout the container, split the slide. **Never go below 10pt body** (the v2 deck used 9.5pt on slide 5).
5. Use `tools/pptx_text_helpers.py`: `label_in_shape(shape, text, ...)` fits and writes, and raises `ValueError` when it cannot, so the pipeline must shorten or re-layout. `set_text(...)` writes safe text frames. `tools/textfit.py` is the shared measurement library.
6. **Fallback render test.** Render the deck twice: with Inter available and with Inter aliased to Arial (fontconfig alias). Both renders must show no clipped or overflowing text. Report both.
7. **Fonts for the audience.** OTF fonts cannot be embedded in .pptx. Ship `themes/lumbini/fonts/` with every deck and tell the user to install Inter on the presenting machine. Layouts must stay safe even if Inter is missing (step 4's safety margin).
8. Add the `qa_pptx.py` text checks to the QA stage as **blocking**: `wrap="none"` text wider than its box, any word wider than its box, text height over box height, body text under 10pt.

---

## 4. Other issues seen in the v2 output (fix as part of this pass)

| Slide | Issue | Fix |
|---|---|---|
| 5 | Staggered "career stage" cards are tall with most of the area empty; body 9.5pt overflows (0.79in needed, 0.65in available). | Size cards from content; use a staircase or ladder only if height encodes seniority, with the text inside each step. |
| 7 | Still uses the SGG commercials layout (A / B / C tables) for roles, certifications and action plan, leaving a large gap between the tables and the action plan. | Compose from the relationship: roles and compensation is a comparison; certifications are a sequence; the action plan is a timeline. Do not reuse commercials framing. |
| 1 | Cover pill text overflows the pill and the metadata block is centred oddly. | Pill width computed from measured text; metadata left-aligned in a two-column grid. |
| 2, 3 | Large empty rounded panels at the right. | Panels sized to content, or removed. |
| All | Footer text now comes from deck metadata: **keep this**. Slide 2's "iceberg" composition is the right kind of adaptive layout: **keep this approach**. | None. |

---

## 5. Skills added in this kit

Both live in `skills/` and must be available to the agent.

1. **`sap-consulting-principles`**: eight delivery lessons turned into review checks. Load it for SAP proposals, plans, go-live and handover decks. In the pipeline: Storyline/Distill (assumptions before commercials, business problem before system, support and handover slides) and QA (flag module-only scope, "minor impact" with no trace).
2. **`transformation-narrator`**: the narrator voice, the "visible vs invisible story" philosophy, Tell-Show-Tell structure, show-don't-tell rules, the 13-lens review panel and the quality test (`source_brief.txt` holds your original brief; it governs voice and philosophy). Load it for any transformation narrative, case reconstruction or executive storyline. In the pipeline: Storyline stage writes titles as insights and a spine of observation → scene → mechanism → lesson; Panel review stage applies the lens procedure from v2 §5. Also unresolved placeholders such as `[SRC-…]` must never reach a slide.

Skill loading rule: load by topic match. Do not load `sap-consulting-principles` for decks unrelated to SAP delivery.

---

## 6. Acceptance for v3

- `qa_pptx.py --slack 1.12` returns 0 BLOCKING on the regenerated Datasphere deck and on an SGG-style proposal.
- Sections: none for decks under 8 slides; otherwise story-named, none empty, none inherited.
- Both font renders (Inter present, Inter aliased to Arial) show no clipped text.
- No body text under 10pt; no `wrap="none"` outside purposely single-line captions that pass the width check.
- Slide 7-style information (roles, certifications, action plan) is composed per relationship, not with the commercials layout.
- Report: root cause with file and line for each defect, files changed, before/after QA output, previews.
