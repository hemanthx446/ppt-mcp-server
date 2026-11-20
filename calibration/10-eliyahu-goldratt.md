# Scrutiny Review: Lens 10 — Eliyahu Goldratt (Theory of Constraints & Throughput Economics)

> **Honest Framing**: *Lens modelled from published work. It is not the person's own statement.*  
> This scrutiny review evaluates the "Supplier Delivery Tracker: CIO Briefing" deck and NARRATIVE.md through the Theory of Constraints (TOC), Throughput Accounting, Drum-Buffer-Rope scheduling, and Five Focusing Steps of Dr. Eliyahu M. Goldratt.

---

### 1. Observe Deeply (Constraints & Throughput Accounting Facts)
- **Plant Throughput Constraint Identified**: Unidentified. The presentation treats the entire factory as an undifferentiated system, failing to locate whether the bottleneck is final assembly, paint, testing, or component supply.
- **Exploitation & Subordination Logic**: Non-existent. Dock workers unload incoming shipments in FIFO arrival order rather than subordinating dock tasks to the immediate raw material demand of the plant bottleneck.
- **Drum-Buffer-Rope (DBR) Presence**: Absent. The application acts as a passive push-tracking tool, allowing vendors to ship whenever they choose without a pull signal ("Rope") tied to the constraint's consumption rate ("Drum").
- **Throughput Accounting Classification**: Slide 8 justifies the $420,000 capital expenditure by claiming a 25% reduction ($600k/year) in expedited freight, failing to model the impact on true enterprise Throughput ($T$) or inventory holding costs ($I$).

---

### 2. Question Gently (10 Signature Questions)
1. **Plant Throughput Bottleneck**: *Unidentified*. The deck never specifies which work center or assembly stage governs plant output.
2. **Exploitation of the Constraint**: *Unexploited*. Because bottleneck parts are not prioritized at the receiving dock, the constraint frequently starves for materials while non-constraint parts are unloaded.
3. **Subordination of Dock Receiving**: *Violated*. Dock receiving operates as an independent silo, optimizing its own unloading schedule rather than subordinating to the constraint.
4. **Non-Bottleneck Hour Saving Mirage**: *Active Trap*. The deck claims labor and tracking efficiencies on docks where labor is a fixed Operating Expense ($OE$), producing zero new cash.
5. **Throughput Accounting Justification**: *Deficient*. Lacks any analysis of how the software increases the rate of finished product sales ($T$) or reduces working capital tied up in inventory ($I$).
6. **The Haystack Syndrome Presence**: *Acute*. Slide 5 inundates leadership with vendor OTIF %, rejection %, and dwell times, but cannot answer: *Which missing part will halt the constraint today?*
7. **Push-Based Yard Flooding**: Vendors push trucks into the yard based on their own batch schedules, causing 4.2 hours of yard dwell and tying up cash in non-bottleneck materials.
8. **Constraint Buffer Management**: *Absent*. No dynamic Time Buffer monitors whether the constraint's protective inventory cushion is green, yellow, or red.
9. **Delivery Variance Impact on Throughput**: A 1-day delay on a non-critical bolt is treated with identical alarm as a 1-day delay on a sole-source wire harness feeding the bottleneck.
10. **Global Cash Generation vs Local Scores**: Boosting an individual supplier's local OTIF from 78% to 95% generates zero new profit if that supplier produces non-bottleneck parts.

---

### 3. Reveal Patiently (Hidden Constraint Mechanics & Local Optima Traps)
- **The Equality Fallacy (The Cardinal Sins of Supply Chain)**: The presentation commits the fundamental operational error of treating all inbound parts as equally important. In reality, a manufacturing plant is limited by at most one or two physical bottlenecks. Expediting an abundant non-bottleneck part is a complete waste of human effort and freight money; it increases inventory ($I$) and operating expense ($OE$) without adding a single dollar of throughput ($T$). By failing to prioritize materials by their constraint impact, the software squanders dock worker attention on trivia while the true bottleneck starves.
- **The Haystack Syndrome**: Goldratt defined information as "the answer to the question asked." Slide 5 delivers an ocean of data (vendor rankings, composite OTIF scores, historical dwell statistics) that leaves the plant manager completely unable to answer the only operational question that matters: *Which inbound shipment holds the parts needed to prevent a line stoppage in the next 6 hours?*

---

### 4. Conclude Structurally (Findings & Concrete Remediations)

| ID | Severity | Title | Slide | Observation | Root Cause | Concrete Fix |
|---|---|---|---|---|---|---|
| **TOC-001** | **P1** | The Equality Fallacy: Treating All Inbound Materials as Equally Critical | Slide 2 & Slide 5 | The system tracks and scores all supplier shipments identically, expending equal urgency and freight expediting on non-bottleneck parts as on critical constraint components. | Failure to apply Theory of Constraints focusing steps; treating supply chain items as an undifferentiated mass. | Restructure data architecture and UI to classify materials into **Constraint Feeders** vs **Non-Constraint Items**; prioritize expediting and tracking energy strictly on parts that protect the plant bottleneck. |
| **TOC-002** | **P1** | Total Omission of Plant Constraint Identification & DBR Subordination | Slide 3 & Slide 4 | The architecture does not identify the plant bottleneck and fails to subordinate dock unloading to the plant's Drum-Buffer-Rope (DBR) schedule. | Designing receiving dock software as an isolated local silo disconnected from plant production constraints. | Explicitly identify the plant constraint in the operational architecture; subordinate dock unloading queues so shipments containing constraint buffer stock are automatically unloaded first. |
| **TOC-003** | **P2** | The Haystack Syndrome: Retrospective Data Deluge Obscuring Constraint Starvation | Slide 5 | Slide 5 presents high-level vendor OTIF averages and historical percentages that conceal which specific missing shipments immediately threaten plant throughput. | Defaulting to generic corporate BI scorecards rather than actionable decision-support displays (Goldratt's Haystack Syndrome). | Replace generic OTIF dials on Slide 5 with a **Constraint Buffer Status Cockpit**: display a red/yellow/green buffer penetration board showing incoming shipments tied to active line jobs. |
| **TOC-004** | **P2** | Missing Time Buffer Management for Plant Constraint Protection | Slide 4 | The system does not monitor the consumption of time buffers protecting the assembly line, leaving schedulers blind to stockouts until physical bins are empty. | Lack of TOC dynamic buffer management logic. | Implement TOC Buffer Management: establish a 48-hour time buffer in front of the plant constraint; trigger visual expediting alerts only when buffer consumption enters the red zone. |
| **TOC-005** | **P2** | Absence of Throughput Accounting ($T, I, OE$) in Business Justification | Slide 8 | The $420k investment is justified via conventional cost-accounting expediting cuts, without modeling the direct impact on Throughput ($T$) or inventory carrying costs ($I$). | Relying on distorted cost-accounting models rather than Throughput Accounting. | Restructure the business case on Slide 8 using Throughput Accounting: quantify how eliminating line halts unlocks $4.8M in annualized finished-goods Throughput ($T$) while slashing buffer inventory ($I$). |
| **TOC-006** | **P3** | Promoting Local Dock Scan Optima Regardless of Plant Consumption | Slide 4 | Step 2 and Step 4 emphasize fast tablet scanning and warehouse staging without verifying whether the staged materials are needed by production today. | Measuring local departmental activity rather than global system velocity. | Tie dock worker KPIs to "Constraint Starvation Avoidance" rather than raw cartons scanned per hour. |
