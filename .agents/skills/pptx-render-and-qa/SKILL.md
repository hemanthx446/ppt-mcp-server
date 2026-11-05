---
name: pptx-render-and-qa
description: Rules for OOXML template rendering, deterministic layout selection, library gotchas, and the automated pre-flight quality gate.
---

# PPTX Render & Quality Gate Skill

## 1. Deterministic Layout Selection Rules
The layout archetype for each slide is picked strictly by the rule table, stopping the "same card row everywhere" anti-pattern:
- **No layout archetype used on more than 2 consecutive slides.**
- **A 10-slide deck must utilize at least 6 distinct layouts.**
- **Every slide (except cover/closing) must include at least 1 non-text visual** (diagram, chart, mockup, step-line, or table).

| content_shape | Archetype | Key Primitives |
|---|---|---|
| `cover` | Cover Hero | Title, Subtitle, Metadata Key-Values, Orange Rule, Logo, Illustration |
| `requirement_to_outcome` | 3-Column Comparative | Numbered Badges, Divider Lines, Right Arrows, Outcome text |
| `hub_and_spokes` | Central Core Hub | Central Navy Circle, 4 Spoke Cards, Directional Labeled Arrows |
| `dashboard_concept` | Analytics Cockpit | Chevron Flow, Dashboard Mockup, 2 Native Charts, Drill Ladder |
| `levels_x_dimensions` | Stakeholder Matrix | 3x3 Grid (Dashed for illustrative), Confirmed Capability Band |
| `process_linear` | Sequential Pipeline | Step Line with Numbered Badges, Deliverables Band, Info Callout |
| `flow_with_actions` | Action-Oriented Flow | 6 Box Nodes, Horizontal Arrows, Dashed Drop-lines, Actions, Legend |
| `phases_over_time` | Phased Roadmap | Staggered Pill Sequence Bars, Key Activities, Future Readiness Box |
| `roles_and_terms` | Dual Compact Tables | 2 Native PowerPoint Tables (Navy Headers, Orange Placeholders), Terms |

## 2. Library Gotchas & OOXML Rules
- **Font Floor:** Body text floor is strictly **10.0 pt**. Only footers and slide numbers are allowed at 9.0 pt.
- **Measure-Then-Size:** Always measure text using Pillow `ImageFont` on Inter TTF before sizing boxes. If content is too long, distill text; never shrink the font below 10 pt.
- **Theme XML Patching:** Write the 12 Lumbini colors into `ppt/theme/theme1.xml` and enforce `<p:sldSz cx="12192000" cy="6858000"/>` (clean 16:9, no `type="screen4x3"`).
- **Placeholders & Prompt Elimination:**
  - Titles must ALWAYS populate the slide master's native title placeholder (`slide.placeholders[0]` / `ph.placeholder_format.type in (TITLE, CENTER_TITLE)`) rather than creating a disconnected textbox.
  - At the conclusion of slide rendering, a sweep MUST remove any remaining unpopulated empty placeholders from `slide.shapes._spTree`. Empty placeholders trigger PowerPoint to render ugly "Click to add title" or "Click to add text" prompt boxes over slide content.
- **Table Formatting:** Navy headers (`#1F497D`) with bold white text; orange text (`#F78B15`) for all editable placeholders (`[Amount]`, `[Days / %]`).

## 3. Automated Quality Gate Checklist (`qa_deck`)
- **Blocking (Rejects deck and triggers fix loop):**
  - Empty placeholders or leftover placeholder prompt text ("Click to add title", "Click to add text").
  - Font size < 10 pt (except footers/slide numbers ≥ 9 pt).
  - Slide words > 160 (cover > 50 words).
  - Text or shape bounding box outside slide canvas.
  - Shape collisions / overlapping bounding boxes.
  - Banned buzzwords ("world-class", "revolutionary", etc.).
  - Unconfirmed capabilities stated as confirmed.
  - Same layout on > 2 consecutive slides.
  - Fewer than 6 distinct layouts in a 10-slide deck.
  - File fails to reopen in PowerPoint or `python-pptx`.
- **Warnings:** Container empty space > 35%; missing non-text visual; missing speaker notes.
- **Fix Loop:** Up to 3 iterations returning specific violation feedback to Distill/Visual Plan stages.
