# Kit v3: terminal quick start

```bash
# 1. unzip at your project root
unzip -o antigravity_ppt_kit_v3.zip -d ./ppt-kit && cd ppt-kit

# 2. install the two skills (default target: ./.agent/skills)
bash install_skills.sh                      # workspace skills
bash install_skills.sh ~/.gemini/antigravity/skills   # or a global skills folder

# 3. python deps for the QA and text helpers
python3 -m pip install python-pptx pillow lxml

# 4. reproduce the defects on the v2 output
python3 -I tools/qa_pptx.py reference/negative_example_datasphere_after_v2.pptx --slack 1.12

# 5. check any new deck (exit code 1 on any BLOCKING finding)
python3 -I tools/qa_pptx.py path/to/new_deck.pptx --slack 1.12
```

Then paste `UPDATE_v3_PROMPT.md` into the Antigravity agent.

## Notes

- **Skill folders:** I could not verify Antigravity's skills path from here. `.agent/skills/` (workspace) and a global folder under `~/.gemini/antigravity/` are what I understand it to use; confirm in the IDE's docs or settings and pass the right path to `install_skills.sh`.
- **Fonts:** install the three Inter files in `themes/lumbini/fonts/` on any machine that presents the decks. Without them PowerPoint substitutes a fallback font.
- **Exit codes:** `qa_pptx.py` exits 1 when a BLOCKING finding exists, so it can gate a build step.

## Contents

| Path | Purpose |
|---|---|
| `UPDATE_v3_PROMPT.md` | The prompt to paste into the agent |
| `prompts/ANTIGRAVITY_MASTER_PROMPT_v1.md`, `..._v2.md` | v1 and v2 prompts (still apply) |
| `skills/sap-consulting-principles/` | SAP delivery lessons as review checks |
| `skills/transformation-narrator/` | Narrative voice, structure and review panel (`source_brief.txt` is your original brief) |
| `tools/qa_pptx.py` | Deck QA: sections, text fit with real Inter metrics, bounds, leaks, density |
| `tools/textfit.py` | Shared text measurement and fitting library |
| `tools/pptx_text_helpers.py` | python-pptx helpers: safe text frames, label-in-shape, measure-then-fit |
| `tools/sections.py` | Write story-named sections while building with python-pptx |
| `tools/rebuild_sections.py` | Rewrite or remove sections on an existing .pptx |
| `themes/lumbini/` | Tokens, assets, Inter fonts |
| `reference/` | Reference deck and build script, MCP sample, Datasphere outputs (first and after v2), previews |
