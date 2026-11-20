# Scrutiny Review: Lens 01 — Jeanne Ross (Enterprise Operating Model & Digital Platforms)

> **Honest Framing**: *Lens modelled from published work. It is not the person's own statement.*  
> This scrutiny review evaluates the "Supplier Delivery Tracker: CIO Briefing" deck and NARRATIVE.md through the enterprise architecture, operating model, and digital platform frameworks of Dr. Jeanne W. Ross (MIT CISR).

---

### 1. Observe Deeply (Facts in Storyline & Rendered Slides)
- **Slide 1**: Positions the solution as "Real-Time Inbound Supply Chain Visibility & Plant Execution Architecture" for executive CIO review.
- **Slide 2**: Documents $2.4M annual expedited freight costs, 4.2 hours average yard dwell, and 18 hours/month assembly line downtime across four manufacturing plants. Uses three disconnected text cards.
- **Slide 3**: Displays the core architecture diagram: External Portal -> Isolated PostgreSQL Cloud DB -> Nightly Batch Extract (02:00 AM SFTP Cron) -> SAP ERP Backbone. Explicitly notes: "Avoids direct ERP API calls to minimize initial integration complexity."
- **Slide 4**: Details dock operations on mobile tablets. Material coordinators scan barcodes and log defects into the Tracker portal. Step 5 notes: "Disconnected Manual ERP Posting: ERP clerk manually keys bulk Goods Receipts into SAP ERP at end-of-day or relies on nightly batch."
- **Slide 5**: Features OTIF compliance (78.4% vs 95% target) and dock rejections. Contains an explicit governance policy card: "When a supplier drops below 80% OTIF, dock supervisors have direct authority within the portal to downgrade supplier qualification tier and reroute upcoming purchase order shipments to secondary backup vendors without awaiting central procurement review."
- **Slide 6**: Illustrates technical stack: React 18 SPA, Node.js microservices, dedicated PostgreSQL 15 RDS instance, and AWS S3 document bucket. Concludes: "Completely decoupled cloud stack with no direct dependency on enterprise SAP middleware or central master data governance."
- **Slide 7**: Lays out a 4-phase sequential rollout: Plant 1 Pilot (Weeks 1-8), Plant 2 Expansion (Weeks 9-16), Plants 3 & 4 Rollout (Weeks 17-24), and Enterprise Evaluation of real-time SAP APIs (Weeks 25-32).
- **Slide 8**: Requests $420,000 for Phase 1 (Plant 1 only), allocating $180k to custom portal build, $70k to nightly batch scripts, and only 9 months payback based on saving $600k in freight expedites.

---

### 2. Question Gently (10 Signature Questions)
1. **Operating Model**: *Unknown / Undefined*. The deck assumes a multi-plant rollout across four manufacturing facilities without stating whether the enterprise operates under Unification, Coordination, Replication, or Diversification.
2. **Core Processes**: *Inbound Dock Receiving & Shipment Tracking*. The boundary between edge operational tracking and the core enterprise record is severed by a 24-hour batch delay.
3. **System of Record**: *Ambiguous and Conflicted*. The standalone PostgreSQL database stores supplier performance ratings, shipment statuses, and delivery confirmations independently of SAP ERP.
4. **Operational Backbone**: *Compromised / Bypassed*. The architecture deliberately circumvents the SAP ERP backbone to "minimize initial integration complexity," creating an uncoordinated data silo.
5. **Reusable Integrations**: *None*. Point-to-point flat CSV files pushed over SFTP via nightly cron jobs rather than reusable enterprise API services or event streams.
6. **Central vs. Local Balance**: *Unbalanced*. Local dock supervisors are granted unilateral authority over corporate supplier tiers and purchase order re-routing.
7. **Data Synchronization**: *Latent (24-Hour Batch Lag)*. Contradicts the executive storyline claim of "real-time inbound visibility."
8. **Business Rule Standardization**: *Unstandardized*. OTIF calculation and qualification rules are embedded within local Node.js application services without central policy governance.
9. **Decision Rights**: *Misallocated*. Slide 5 assigns binding vendor contract decisions to frontline warehouse coordinators.
10. **Digital Platform Foundation**: *Isolated Island*. The proposed architecture does not establish reusable platform components (canonical PO schemas, event buses) that benefit broader enterprise supply chain initiatives.

---

### 3. Reveal Patiently (Hidden Mechanics & Root Causes)
- **The Speed Trap vs. Enterprise Debt**: The project team chose an isolated cloud database and nightly batch flat-files to deliver a working pilot in 8 weeks. While this satisfies the immediate desire for localized speed at Plant 1, it introduces severe architectural fragmentation that will impede rollout to Plants 2, 3, and 4.
- **The Real-Time Illusion**: The deck repeatedly promises "real-time inbound visibility" to leadership, but the technical plumbing relies on a 24-hour batch cycle. A shipment rejected at 9:00 AM at the receiving gate remains "in transit" or "open" in SAP ERP until the following morning, risking erroneous accounts payable releases and blind material planning (MRP) runs.
- **Governance Usurpation**: Granting warehouse supervisors the power to alter vendor qualification tiers and redirect purchase orders directly inside an operational tool violates enterprise IT governance (Weill & Ross). It confuses operational exception logging with contractual category management.

---

### 4. Conclude Structurally (Findings & Concrete Remediations)

| ID | Severity | Title | Slide | Observation | Root Cause | Concrete Fix |
|---|---|---|---|---|---|---|
| **ROSS-001** | **P1** | System of Record Ambiguity & Shadow Master Data Store | Slide 3 & Slide 6 | The architecture instantiates a standalone PostgreSQL database storing supplier profiles, PO line items, and delivery statuses without real-time bidirectional synchronization with SAP S/4HANA. | Designing an isolated point-solution database to bypass enterprise ERP governance and expedite local pilot delivery. | Formally declare SAP S/4HANA as the sole System of Record for POs, vendors, and inventory status. Replace the standalone database with an operational cache populated via real-time enterprise APIs. |
| **ROSS-002** | **P1** | Nightly Batch Synchronization Contradicts "Real-Time" Storyline | Slide 1, Slide 3 & Slide 4 | The presentation titles promise "Real-Time Visibility," but the architecture explicitly relies on a 02:00 AM nightly cron batch SFTP CSV export, leaving ERP planning blind for up to 24 hours. | Deferring enterprise integration to Phase 4 (Weeks 25-32) while advertising real-time benefits to executive stakeholders on Slide 1. | Upgrade integration architecture from nightly batch SFTP to event-driven webhooks or SAP OData APIs for instantaneous Goods Receipt (MIGO 101/103) event publishing. |
| **ROSS-003** | **P2** | Governance Violation in Operational Decision Rights | Slide 5 | Slide 5 empowers frontline dock supervisors to downgrade supplier qualification tiers and unilaterally reroute purchase orders to secondary vendors. | Conflating operational fact-recording (identifying damaged shipments) with contractual decision rights (supplier relationship management). | Revise decision rights matrix: dock supervisors record physical condition and delivery variance; automated workflows trigger alerts to Corporate Procurement Category Managers, who retain sole rights to alter supplier qualification or re-route purchase orders. |
| **ROSS-004** | **P2** | Undefined Enterprise Operating Model for Multi-Plant Rollout | Slide 2 & Slide 7 | The proposal plans deployment across four regional manufacturing plants without defining whether the enterprise operates under Unification, Coordination, or Replication. | Assuming a software pilot can scale across plants without aligning on shared process standardization versus local operational autonomy. | Explicitly define the operating model in the Executive Summary (e.g. Unification for supplier master data and procurement policies, with Coordination for physical dock scheduling). |
| **ROSS-005** | **P2** | Isolated Architectural Island with Zero Reusable Platform Components | Slide 6 & Slide 8 | The technology stack is engineered purely as a standalone point solution, requesting $420k without producing any reusable enterprise platform capabilities. | Treating digital delivery as a one-off project rather than building a strategic digital platform foundation (Ross, Beath, Mocker 2019). | Restructure the solution into reusable enterprise digital services: a canonical Inbound Event Broker and a reusable Carrier Notification Service applicable across all plants and logistics divisions. |
| **ROSS-006** | **P3** | Card-Centric Visual Layout Disguises System Dependencies | Slide 2 & Slide 6 | Key architecture and context slides use repetitive text cards that conceal the actual system boundaries, data flows, and enterprise handshakes. | Defaulting to generic card containers instead of drawing rigorous architectural topology diagrams. | Replace text cards with an enterprise architecture topology diagram contrasting the Digital Solution Layer against the Operational Backbone. |
