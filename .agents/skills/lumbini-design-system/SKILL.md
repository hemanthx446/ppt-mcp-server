---
name: lumbini-design-system
description: Design tokens, typography hierarchy, master layouts, brand motifs, and component guidelines for the Lumbini corporate presentation standard.
---

# Lumbini Design System Skill

## 1. Brand Tokens & Typography
- **Slide Dimensions:** 16:9 Widescreen (`13.333" x 7.50"`).
- **Font Family:** **Inter** for all text.
  - Headings/Titles: `Inter Bold`
  - Labels, Badges, Eyebrows: `Inter SemiBold`
  - Body & Descriptions: `Inter Regular`
  - Fallback Chain: `Inter` ➔ `Segoe UI` ➔ `Calibri`
- **Color Palette (12-Slot OOXML Theme Scheme):**
  - Text Dark (`dk1`): `#141E2D`
  - White Surface (`lt1`): `#FFFFFF`
  - Navy (`dk2` / `accent6`): `#1F497D` (Table headers, dark pills, hub circles)
  - Pale Surface (`lt2`): `#EEF3F8` (Tile backgrounds, callout containers)
  - Primary Blue (`accent1` / `hlink`): `#0070C0` (Eyebrows, active tabs, major nodes)
  - Orange Accent (`accent2`): `#F78B15` (Highlight rules, commercial placeholders, single accent per slide)
  - Primary Deep (`accent3`): `#0066B4` (Corner motif, badges)
  - Muted Grey (`accent4` / `folHlink`): `#646E78` (Subtitles, secondary descriptions)
  - Border Grey (`accent5`): `#DCE1E6` (Card outlines, gridlines, table borders)

## 2. Type Scale
- **Cover Title:** 36 pt Bold
- **Slide Title:** 24 pt Bold (Left-aligned, sitting in native master placeholder)
- **Eyebrow:** 11 pt SemiBold Uppercase Blue (`0070C0`)
- **Subtitle:** 13 pt Muted Grey (`646E78`)
- **Card Titles:** 14–15 pt Bold
- **Body Text:** 12–13 pt (Never below 10 pt floor)
- **Captions & Secondary Badges:** 10–10.5 pt
- **Footers & Slide Numbers:** 9 pt

## 3. Brand Motifs & Masters
- **Content Master (`CONTENT`):**
  - Textured background (`bg_light.jpg`)
  - Top-right corner "E" brand mark (four blue rectangles)
  - Bottom-left vertical blue strip (`[0, 6.72, 0.3, 0.78]`)
  - Master footer: *"Lumbini Elite Solutions & Services Pvt. Ltd. | Confidential proposal for [Client]"* (y = 7.1")
  - Native slide number placeholder (right-aligned at x = 11.2", y = 7.1")
- **Cover Master (`COVER`):**
  - Faded illustration top-left (`illus.png`, x = 0.25, y = 0.2, w = 2.8, h = 2.9)
  - Corporate logo top-right (`logo.png`, x = 10.35, y = 0.5, w = 2.4, h = 1.017)
  - Orange accent line (`#F78B15`, width 3, y = 4.68)
  - Navy metadata pill bottom-right (`#1F497D`, 18pt bold white)

## 4. Design Do's & Don'ts
- **DO** measure text before sizing containers (dynamic card height = content + padding).
- **DO NOT** place horizontal accent lines under content slide titles (reserved only for Cover).
- **DO NOT** center body text (always left-align or center in tight circular badges).
- **DO NOT** use more than one orange accent element per slide.
- **DO NOT** allow empty vertical white space > 35% in any container.
