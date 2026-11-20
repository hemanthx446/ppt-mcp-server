# Scrutiny Review: Lens 09 — W. Edwards Deming (Quality Philosophy & Statistical Variation)

> **Honest Framing**: *Lens modelled from published work. It is not the person's own statement.*  
> This scrutiny review evaluates the "Supplier Delivery Tracker: CIO Briefing" deck and NARRATIVE.md through the System of Profound Knowledge (SoPK), common-cause variation, the tampering trap, and quality philosophy of Dr. W. Edwards Deming.

---

### 1. Observe Deeply (Statistical Variation & SoPK Facts)
- **Common vs Special Cause Handling**: The presentation treats all delivery variations as assignable supplier faults. No Shewhart control charts or statistical distributions are presented to distinguish common-cause background noise from true special-cause disruptions.
- **Reliance on Inspection**: Slide 4 places full reliance on receiving dock inspection (Step 3: "Visual QA Check: Coordinator confirms packaging integrity, counts cartons, and logs damage photos") to catch supplier defects after transportation has completed.
- **Operational Definitions**: Slide 5 introduces metrics for "Vendor OTIF Compliance" (78.4%), "Dock Rejection Rate" (3.8%), and "Carrier Dwell Time" (252 mins), but provides zero operational definitions defining testing instruments, timestamp clocks, or measurement rounding criteria.
- **Management Atmosphere (Fear vs Pride)**: Slide 5 mandates a punitive rule: "When a supplier drops below 80% OTIF, dock supervisors have direct authority within the portal to downgrade supplier qualification tier and reroute upcoming purchase order shipments to secondary backup vendors."

---

### 2. Question Gently (10 Signature Questions)
1. **Common vs Special Cause Distinction**: *Completely Absent*. The software treats every delayed shipment as an assignable defect, ignoring highway transit variance and weather noise.
2. **Tampering Trap in Software Rules**: *Severe Tampering Present*. Automatically altering supplier qualification tiers and switching vendors based on a rigid 80% cutoff is textbook tampering (Deming's Funnel Experiment Rule 2/3).
3. **Cease Dependence on Dock Inspection**: *Violated*. Quality is inspected on the loading dock rather than verified through supplier statistical process control (SPC) at the source.
4. **Driving Out Fear**: *Failed*. Public "high-risk" vendor rankings and automated volume cancellations drive fear into suppliers, encouraging them to hide transit delays until the last minute.
5. **Numerical Targets Without Method**: *Management by Slogan*. Slide 5 sets arbitrary targets ("95.0% OTIF", "<1.0% Rejection") without providing any statistical method, process capability study, or supplier coaching program.
6. **Operational Definitions Completeness**: *Missing*. What constitutes "On-Time"? Guard gate arrival? Dock bay docking? Tablet barcode scan? The deck provides no operational definitions.
7. **Long-Term Supplier Partnership vs Churn**: *Promotes Churn*. The system makes it trivial to discard long-term vendors and transfer purchase orders to unvetted secondary suppliers.
8. **Frontline Pride of Workmanship**: Dock staff are reduced to barcode-scanning operatives executing rigid tablet scripts.
9. **Measurement Error Analysis**: Assumes 100% measurement accuracy during tablet scanning without accounting for operator mis-scans or label print defects.
10. **Supplier Capability Development**: Zero investment or tooling is provided to help suppliers build quality into their own manufacturing operations.

---

### 3. Reveal Patiently (Hidden Tampering Mechanics & Inspection Traps)
- **The Textbook Tampering Disaster**: Deming proved conclusively that reacting to common-cause variation as if it were a special cause dramatically *increases* total system variance. Transit times across public highways naturally vary by $\pm 15\%$ due to weather, traffic, and weigh-station queues. When a reliable supplier experiences normal common-cause highway delay and lands at 78% OTIF for the week, the software rule automatically downgrades the supplier and diverts purchase orders to a secondary vendor. The secondary vendor has higher baseline variance, higher costs, and no familiarity with plant specs. Total enterprise variation explodes, delivery performance worsens, and freight expediting costs surge—all caused by software tampering.
- **Inspecting Quality In (Deming's Point 3)**: Catching a damaged carton or wrong part count at the factory loading dock is a catastrophic failure of quality management. By the time a forklift operator spots damage in Bay 4, production is already starved, freight money is spent, and line changeovers are triggered. True quality engineering certifies supplier process capability ($C_{pk} \ge 1.33$) at the supplier's manufacturing line, enabling direct-to-line dock bypass.

---

### 4. Conclude Structurally (Findings & Concrete Remediations)

| ID | Severity | Title | Slide | Observation | Root Cause | Concrete Fix |
|---|---|---|---|---|---|---|
| **DEM-001** | **P1** | Textbook Tampering Trap: Algorithmic Vendor Downgrades on Common-Cause Variation | Slide 5 | Automatically downgrading suppliers and rerouting purchase orders at an arbitrary 80% OTIF cutoff reacts to routine common-cause transit noise, dramatically increasing system variation. | Ignorance of statistical variation; attempting to control a complex supply chain via crude threshold triggers (Deming Funnel Trap). | Eliminate automated order rerouting on Slide 5; replace with Shewhart Control Charts: trigger management reviews only when a data point breaches statistical Upper/Lower Control Limits (Special Cause). |
| **DEM-002** | **P1** | Total Dependence on Receiving Dock Mass Inspection (Violating Deming's Point 3) | Slide 4 | The solution relies on warehouse workers visually inspecting cartons and counting parts on tablets to protect assembly lines, accepting dock defects as inevitable. | Believing quality can be inspected into components at the receiving dock after physical transportation has occurred. | Cease dependence on dock inspection: institute a Supplier Source Quality Certification program, requiring Tier-1 suppliers to transmit SPC data and CoCs, enabling pre-cleared dock-to-line delivery. |
| **DEM-003** | **P2** | Arbitrary Numerical Targets (95% OTIF, <1% Rejection) Without a Statistical Method | Slide 5 | The presentation demands executive targets (95.0% OTIF, <1.0% rejection rate) without providing any statistical process capability studies or improvement methods. | Management by numerical slogans (Deming Point 11: Eliminate numerical quotas and slogans for the workforce). | Replace arbitrary percentage slogans with a concrete Statistical Capability Roadmap: establish baseline process capability ($C_p / C_{pk}$) and provide joint Six Sigma problem-solving support to suppliers. |
| **DEM-004** | **P2** | Absence of Rigorous Operational Definitions for Core Metrics | Slide 5 | Terms such as "On-Time," "In-Full," and "Dock Rejection" lack operational definitions specifying exact testing methods, clock synchronization, and boundary criteria. | Assuming business terminology has self-evident meaning without rigorous operational definitions. | Add explicit Operational Definitions to the narrative and data model: define "On-Time" as plant gate geo-fence timestamp within contracted $\pm 30$-minute delivery window, with explicit exclusions for carrier yard detention. |
| **DEM-005** | **P2** | Institutionalizing Fear and Transactional Vendor Churn (Violating Points 4 & 8) | Slide 5 | Publicly badging suppliers as "High Risk" and cutting PO allocations induces fear, motivating vendors to hide delivery issues rather than collaborating openly. | Managing suppliers through adversarial fear and transactional price competition rather than long-term partnership (Deming Point 4). | Reframe vendor governance: replace punitive blacklisting with collaborative single-team supplier development, driving out fear to surface delivery risks days in advance. |
| **DEM-006** | **P3** | Omission of Shewhart Statistical Process Control (SPC) Charts on Analytics Displays | Slide 5 | Slide 5 presents static percentages and averages rather than time-series SPC run charts, concealing trend degradation and process capability shifts. | Defaulting to simplistic commercial dashboard KPIs instead of statistical process engineering displays. | Replace static percentage cards on Slide 5 with Shewhart X-bar and R control charts displaying lead-time stability and 3-sigma process boundaries. |
