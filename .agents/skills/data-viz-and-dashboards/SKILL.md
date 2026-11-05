---
name: data-viz-and-dashboards
description: Standards for native editable charts, interactive executive dashboard mockups, KPI delta formatting, and data provenance rules.
---

# Data Visualization & Dashboards Skill

## 1. Native Editable Charts (Never Static Images)
PowerPoint charts must be native `<c:chart>` graphic frames generated via `slide.shapes.add_chart`:
- **Chart Selection Decision Table:**
  - *Trend over time (monthly, quarterly):* Line Chart (`XL_CHART_TYPE.LINE`)
  - *Ranking, category comparison, business units:* Clustered Column (`XL_CHART_TYPE.COLUMN_CLUSTERED`) or Clustered Bar
  - *Part-to-whole (≤ 5 slices):* Doughnut or Stacked Bar
  - *Target vs Actual:* Clustered Column + Line combo
- **Chart Styling Constraints:**
  - Max 6 categories per chart.
  - Title states the exact metric and unit (e.g., *"Revenue vs plan by business unit (%)"*).
  - Light gridlines (`#DCE1E6`, 0.5 pt), no heavy backgrounds.
  - Data labels on for key series.
  - Colors drawn strictly from theme (`#0070C0` Primary Blue, `#F78B15` Orange Accent).

## 2. Executive Dashboard Mockup Anatomy
When presenting BI or analytics platforms (e.g. ELITIA BI):
- **Mockup Container:** White card with `#DCE1E6` border and soft shadow.
- **Top Brand Bar:** Navy `#1F497D` header with platform name and mandatory provenance notice: *"Illustrative layout, not client data"*.
- **Filter Tabs:** Realistic business dimensions (e.g. `Executive`, `Finance` [active], `HR`, `Supply Chain`, `Business unit`).
- **KPI Summary Strip:** 4 comparative tiles with value, unit, and directional delta badges:
  - `▲ +4% vs last year` (Green or Blue for positive)
  - `▼ -2% vs last year` (Muted or Accent for negative)
- **Embedded Dual Charts:** Side-by-side native column and line charts reflecting operational performance.
- **Drill Ladder:** 4-step vertical sequence explaining data depth:
  1. *KPI Summary:* High-level performance against plan.
  2. *Dimension Split:* Decomposition by business unit or cost center.
  3. *Source Records:* Underlying documents with CSV export.
  4. *Detail Page:* Individual vendor, customer, or transaction ledger in focus.

## 3. Data Provenance & Capability Registry
- **Confirmed Capabilities:** Grounded in formal functional specs (e.g. `Elitia_BI_Functional_Specification.md`).
- **Proposed Activities:** Label as activities subject to technical validation during Discovery.
- **Illustrative Layouts:** Charts, mockups, or matrix KPIs that are indicative must carry the explicit visible label: *"Dashed boxes are illustrative KPI examples. Final KPI set agreed during discovery."*
- **Stable Seeds:** Never randomize mockup numbers at runtime; use fixed deterministic values for reproducible output.
