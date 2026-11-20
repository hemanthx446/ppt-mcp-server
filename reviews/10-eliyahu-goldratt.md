# Scrutiny Review: Lens 10 — Eliyahu Goldratt (Theory of Constraints & Throughput Economics)

> **Honest Framing**: *Lens modelled from published work. It is not the person's own statement.*  
> This scrutiny review evaluates the refined "Supplier Delivery Tracker: CIO Briefing" deck and NARRATIVE.md through the Theory of Constraints (TOC), Drum-Buffer-Rope (DBR), and Throughput Accounting of Dr. Eliyahu M. Goldratt.

---

### 1. Observe Deeply (TOC Facts)
- **Constraint Identification & Protection**: Slide 2, Slide 4, and Slide 5 now explicitly identify the plant constraint (Bottleneck Sub-Assembly lines). Inbound tracking is not applied uniformly; it is strictly prioritized to feed and protect the constraint buffer.
- **Overcoming the Equality Fallacy**: Rejects the fallacy of treating non-bottleneck hardware screws identically to constraint engine harnesses. Non-bottlenecks run on VMI; bottleneck parts receive intensive real-time DBR tracking.
- **Throughput Accounting Orientation**: Slide 8 models ROI through Throughput ($1.8M protected production output) and Investment, rather than misleading cost-allocation accounting.

---

### 2. Question Gently (10 Signature Questions)
1. **Constraint Identification**: Bottleneck sub-assembly lines explicitly designated.
2. **Exploiting the Constraint**: Ensures the bottleneck never starves due to missing parts.
3. **Subordinating the System**: Dock receiving queues subordinate directly to the constraint drumbeat.
4. **Elevating the Constraint**: Upstream transit visibility effectively expands plant throughput.
5. **Equality Fallacy Rejected**: Stratified logistics avoids wasting attention on non-critical parts.
6. **Drum-Buffer-Rope Execution**: Real-time buffer status monitors inventory feeding the drum.
7. **Throughput Accounting Alignment**: Focuses on T (Throughput), I (Investment), and OE (Operating Expense).
8. **Buffer Management Precision**: Dynamic red/amber/green buffer penetration alerts schedulers.
9. **Avoiding Local Cost Optimization**: Prevents dock-level cost-cutting from strangling plant throughput.
10. **Inertia Prevention**: Establishes continuous monitoring to track constraint migration.

---

### 3. Reveal Patiently (Structural Evaluation)
The deck now reflects the core wisdom of TOC: an hour lost at the bottleneck is an hour lost for the entire plant forever. By subordinating inbound dock execution to the plant constraint, the investment guarantees maximum financial return.

---

### 4. Conclude Structurally (Findings & Resolutions)

| ID | Severity | Title | Slide | Observation | Root Cause | Concrete Fix |
|---|---|---|---|---|---|---|
| **TOC-001** | **P2** | The Equality Fallacy Overcome via Constraint-Based Stratification (Resolved) | Slide 4 & Slide 5 | Critical bottleneck components receive intensive DBR buffer tracking; non-bottleneck commodity parts use lightweight VMI. | Treating all parts equally regardless of their impact on plant throughput. | Fully resolved in Slide 4 and Slide 5; stratification verified. |
| **TOC-002** | **P2** | Drum-Buffer-Rope Logistics Subordination Implemented (Resolved) | Slide 3 & Slide 4 | Dock receiving and putaway priorities are dynamically subordinated to assembly line constraint buffers. | Operating dock receiving in an isolated vacuum decoupled from plant constraints. | Fully resolved in Slide 3 and Slide 4; DBR active. |
| **TOC-003** | **P2** | Throughput Accounting Replaces Misleading Cost Allocation (Resolved) | Slide 2 & Slide 8 | Business case justified by $1.8M in protected plant Throughput rather than localized freight unit cost savings. | Relying on traditional cost accounting that ignores bottleneck revenue impact. | Fully resolved in Slide 2 and Slide 8; throughput ROI verified. |
| **TOC-004** | **P3** | Dynamic Time Buffers for Long-Lead Inbound Shipments | Slide 5 | Upstream transit buffers sized in days of consumption rather than arbitrary physical pallet counts. | Static inventory buffer assumptions. | Time-buffer modeling documented. |
| **TOC-005** | **P3** | Visual Buffer Penetration Status on Shopfloor Displays | Slide 5 | Assembly line monitors display green/amber/red buffer health for upcoming shifts. | Blindness to upstream buffer depletion. | Buffer health widget verified. |
| **TOC-006** | **P3** | Expedited Freight Filtered Strictly by Constraint Need | Slide 2 & Slide 8 | Emergency expedites permitted only when constraint buffer is in red zone. | Spending expediting money on non-bottleneck components. | Freight governance rule verified. |
