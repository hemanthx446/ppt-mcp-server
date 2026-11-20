# Scrutiny Review: Lens 06 — Peter Senge (Systems Thinking & Organizational Learning)

> **Honest Framing**: *Lens modelled from published work. It is not the person's own statement.*  
> This scrutiny review evaluates the "Supplier Delivery Tracker: CIO Briefing" deck and NARRATIVE.md through the systems thinking, system archetypes, and dynamic feedback frameworks of Dr. Peter M. Senge.

---

### 1. Observe Deeply (Feedback Loops & Archetype Facts)
- **Balancing Loops Identified**: Dock check-in attempts to balance physical yard congestion against gate arrivals. However, the feedback delay (24-hour batch sync) causes severe operational lag.
- **Reinforcing Dynamics Identified**: Slide 5 introduces a policy where falling below 80% OTIF empowers dock supervisors to downgrade supplier qualification tiers and redirect orders to secondary vendors.
- **System Delays Observed**: Slide 3 embeds a 24-hour information delay (nightly cron extract), while Slide 7 depicts a multi-quarter rollout delay across four manufacturing sites.
- **Mental Models Expressed**: Slide 2 and Slide 5 express an unexamined mental model: that delivery disruptions are exclusively caused by unreliable external suppliers ("the enemy out there"), while internal plant receiving delays (4.2 hours average dwell) and late PO issuance are treated as passive background realities.

---

### 2. Question Gently (10 Signature Questions)
1. **Fundamental vs Symptomatic Fixes**: *Symptomatic*. The deck accepts $2.4M in annual expedited freight as a baseline expense to be tracked, rather than attacking the root causes of supplier lead-time volatility and internal order turbulence.
2. **Reinforcing Vicious Cycles**: *Severe Risk*. Penalizing suppliers by rerouting orders reduces vendor revenue and goodwill, causing vendors to reallocate capacity to other customers, triggering further delivery failures and volume cuts.
3. **Baked-In Mental Models**: *Adversarial Supplier Model*. The software assumes suppliers are transactional adversaries that must be policed and punished by dock supervisors.
4. **Time Delays in Feedback Loops**: *Significant*. A 24-hour delay between dock receipt and ERP awareness prevents timely balancing interventions.
5. **Fixes that Fail Archetype**: *Active on Slide 5*. Symptom: vendor is late -> Fix: dock supervisor reroutes orders -> Unintended Consequence: secondary vendor lacks tooling capacity, causing worse stockouts and higher spot-freight costs.
6. **Tragedy of the Commons Across Plants**: *High Vulnerability*. Deploying Plant 1 first allows Plant 1 expediters to hoard shared supplier capacity, starving Plants 2, 3, and 4.
7. **Cross-Functional Team Learning**: *Absent*. No mechanism exists for dock coordinators, assembly line leads, and corporate buyers to jointly review and resolve recurring failure patterns.
8. **High-Leverage Intervention Point**: *Missed*. The high-leverage point is joint demand forecast visibility with Tier-1 suppliers; the project intervenes at the lowest leverage point: policing the dock gate.
9. **The Enemy Out There Syndrome**: *Evident on Slide 2*. Suppliers are blamed for assembly line downtime without evaluating plant schedule churn.
10. **System Compensating Pushback**: Suppliers will respond to rigid OTIF metrics by padding quoted lead times or rejecting urgent purchase orders to avoid failing "In-Full" scores.

---

### 3. Reveal Patiently (Hidden System Mechanics & Dynamic Traps)
- **The "Fixes that Fail" Escalation Loop**: When a supplier experiences a temporary production hiccup and delivers at 78% OTIF, Slide 5 triggers an immediate penalty: the dock supervisor downgrades the vendor and cancels upcoming POs, transferring volume to a backup supplier. But backup suppliers rarely have raw materials or dedicated tooling queued. The backup supplier delivers even later, expedited freight costs surge, and the original supplier deprioritizes the relationship. The symptomatic fix has worsened the system's core disease.
- **Shifting the Burden to Freight Expedites**: The company has developed an organizational addiction to expedited air and hot-shot freight ($2.4M annually). Instead of treating expediting as an alarm indicating broken upstream collaboration, the project treats it as a cost center to justify software ROI (Slide 8), institutionalizing the symptomatic crutch.

---

### 4. Conclude Structurally (Findings & Concrete Remediations)

| ID | Severity | Title | Slide | Observation | Root Cause | Concrete Fix |
|---|---|---|---|---|---|---|
| **SENG-001** | **P1** | Severe "Fixes that Fail" Dynamic: Unilateral Vendor Rerouting Induces Supply Network Instability | Slide 5 | Empowering dock supervisors to unilaterally downgrade suppliers below 80% OTIF and reroute orders triggers vendor relationship breakdown and capacity loss. | Instituting punitive algorithmic penalties without modeling supplier behavioral feedback loops. | Replace unilateral dock rerouting with a collaborative balancing loop: OTIF dips trigger joint Root-Cause Problem-Solving workflows between Corporate Procurement and Supplier Engineering before altering contract allocations. |
| **SENG-002** | **P1** | "Shifting the Burden" to Expedited Freight Masking Fundamental Upstream Instability | Slide 2 & Slide 8 | The business case justifies software investment by claiming 25% savings on $2.4M expedited freight, treating freight expedites as an acceptable operating habit rather than an unsustainable symptom. | Focusing on managing the symptoms of supply chain failure rather than curing upstream forecast volatility and supplier capacity constraints. | Redefine project core objective from "managing expediting costs" to "eliminating the systemic drivers of expedites" through collaborative advance capacity reservation and shared production schedules. |
| **SENG-003** | **P2** | The "Enemy Out There" Syndrome Blaming Suppliers for Internal Dock Bottlenecks | Slide 2 & Slide 4 | Presentation attributes assembly line stockouts entirely to supplier delivery failures while Slide 2 simultaneously reports 4.2 hours of internal truck yard dwell time caused by plant dock congestion. | Blaming external partners ("the enemy out there") for disruptions exacerbated by internal process friction. | Broaden operational scope on Slide 2 to evaluate internal receiving dock cycle times and plant schedule turbulence alongside external carrier transit variance. |
| **SENG-004** | **P2** | "Tragedy of the Commons" Risk Across Sequential Multi-Plant Rollout | Slide 7 | Rolling out the tool to Plant 1 in isolation allows Plant 1 expediters to monopolize constrained supplier part allocations at the expense of sister plants. | Implementing local plant optimizations without central enterprise allocation governance. | Establish an Enterprise Allocation Governance rule in the core engine preventing single-plant expediters from claiming shared supplier inventory without multi-plant visibility. |
| **SENG-005** | **P2** | Unmodeled System Delays in Batch Feedback Loop Distorting Management Perception | Slide 3 | The 24-hour batch synchronization lag introduces an unacknowledged temporal delay, causing management KPIs to reflect yesterday's state while today's crisis unfolds. | Treating information delay as a negligible technical detail rather than a primary driver of operational oscillation. | Eliminate information delays by upgrading to event-driven webhooks, ensuring balancing feedback occurs within minutes rather than after a 24-hour delay. |
| **SENG-006** | **P3** | Adversarial Mental Model Hardcoded into Software Governance | Slide 5 | The presentation labels suppliers as entities to be "quarantined," "downgraded," and "rerouted," embedding an adversarial mental model into the software architecture. | Inherited industrial procurement culture treating external suppliers as untrustworthy adversaries. | Reframe interface tone from punitive surveillance to collaborative partnership, establishing shared visibility portals and mutual scorecard reviews. |
