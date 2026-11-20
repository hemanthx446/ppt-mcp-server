# Scrutiny Review: Lens 03 — Ivar Jacobson (Architectural Intent & Use Case Engineering)

> **Honest Framing**: *Lens modelled from published work. It is not the person's own statement.*  
> This scrutiny review evaluates the "Supplier Delivery Tracker: CIO Briefing" deck and NARRATIVE.md through the use-case driven engineering, Entity-Control-Boundary architecture, and vertical slice principles of Dr. Ivar Jacobson.

---

### 1. Observe Deeply (Actors, Use Cases, and Flow Facts)
- **Human Actors Identified**: Carrier truck drivers, gate security guards, dock material coordinators, forklift drivers, dock supervisors, ERP posting clerks, and corporate procurement managers.
- **System Actors Identified**: Supplier Web Portal, Cloud PostgreSQL DB, Cron SFTP script, and corporate SAP ERP.
- **Documented Use Cases**: Slide 4 documents a 5-step operational flow: 1. Gate Check-in, 2. Bay Offload & Scan, 3. Visual QA Check, 4. Staging Bay Putaway, 5. Batch GR Posting.
- **Flow Patterns**: The presented workflow is entirely linear and portrays exclusively the "happy path" without branching, exception recovery, or offline handling.
- **Implementation Slicing**: Slide 7 plans deployment across horizontal layers: standalone UI and local database in Weeks 1-8 (Phase 1), with real-time enterprise backbone integration deferred to Phase 4 (Weeks 25-32).

---

### 2. Question Gently (10 Signature Questions)
1. **Actors & Goals**: *Partially Defined*. Actors are named, but their interactions are described as passive tasks rather than measurable actor goals (e.g., "Scan pallet barcode" rather than "Verify shipment against PO line items").
2. **Alternative & Exception Flows**: *Completely Absent*. No provision is made for damaged cartons, unreadable barcodes, delivery quantity mismatches, or unscheduled carrier arrivals.
3. **Entity-Control-Boundary**: *Violated*. Slide 6 shows a generic "Node.js Microservices" layer without separating workflow controllers (Use-Case Controllers) from domain entity persistence and boundary presentation.
4. **Architecturally Significant Use Cases**: *Unaddressed*. The most critical failure modes—such as receiving dock check-in during network dropouts or resolving supplier ASN discrepancies—are not evaluated.
5. **Just Enough Architecture**: *Diverted*. The architecture includes an isolated PostgreSQL RDS database, AWS ECS containers, and S3 document buckets, but fails to provide essential offline dock caching.
6. **Verification by Actor Goal**: *Unverified*. No test strategy is outlined tying automated tests to end-to-end actor success criteria.
7. **Resilience to External System Failure**: *Severely Vulnerable*. If the nightly batch SFTP script fails, dock coordinators have no documented mechanism to verify PO validity or trigger manual fallback receipts.
8. **Vertical Use-Case Slices**: *Violated (Horizontal Trap)*. Phase 1 delivers a disconnected front-end slice, leaving the end-to-end loop through SAP ERP incomplete until Phase 4.
9. **Persona to Actor Traceability**: *Moderate*. Personas in NARRATIVE.md correspond roughly to slide steps, but dock supervisors are given anomalous contract redirection powers on Slide 5 without an associated use case.
10. **SEMAT Requirements State**: *Bounded, but not Coherent*. Requirements are listed as discrete features, but the absence of exception flows means the system is not yet acceptable for production operations.

---

### 3. Reveal Patiently (Hidden Mechanics & Flow Vulnerabilities)
- **The Happy-Path Illusion**: In industrial logistics, exceptions are not rare edge cases; they represent 15% to 25% of all physical dock interactions. Truck drivers arrive with torn bills of lading, vendors deliver 95 cartons instead of 100, and barcode scanners fail in poor lighting. Presenting an 8-slide briefing to the CIO that models zero exception flows invites catastrophic dock bottlenecks on Day One of the pilot.
- **The Horizontal Slicing Anti-Pattern**: Jacobsonian architecture demands that systems be developed in vertical slices—thin, end-to-end threads connecting the user interface, business logic, and backend database for a specific use case. Deferring SAP ERP integration to Phase 4 means the Phase 1 pilot cannot validate the true business transaction (Goods Receipt 101/103), delivering an illusion of progress that leaves enterprise integration risks unresolved.

---

### 4. Conclude Structurally (Findings & Concrete Remediations)

| ID | Severity | Title | Slide | Observation | Root Cause | Concrete Fix |
|---|---|---|---|---|---|---|
| **JCOB-001** | **P1** | Happy-Path Blindness & Complete Omission of Exception Scenarios | Slide 4 | The dock receiving flow is depicted exclusively as a frictionless linear progression, completely ignoring damaged shipments, missing ASNs, unreadable barcodes, and count variances. | Assuming the happy path is sufficient for executive presentation, concealing real-world operational friction. | Expand Slide 4 to explicitly document primary exception flows: 1. Barcode Misread -> Manual PO Search; 2. Damage Detected -> Quarantine Bay Hold & Photo Log; 3. Network Offline -> Local Tablet Cache. |
| **JCOB-002** | **P1** | Horizontal Slicing Anti-Pattern: Deferring Core System Integration to Phase 4 | Slide 7 | The roadmap plans a standalone portal and isolated database in Phase 1 (Weeks 1-8), postponing true enterprise SAP ERP integration to Phase 4 (Weeks 25-32). | Designing project phases along horizontal technology layers rather than vertical end-to-end use-case slices. | Restructure roadmap into vertical use-case slices: Phase 1 must deliver an end-to-end vertical thread (ASN -> Dock Scan -> Real-Time Goods Receipt) for the top 5 critical components, validating enterprise integration immediately. |
| **JCOB-003** | **P2** | Violation of Entity-Control-Boundary (ECB) Pattern | Slide 6 | Slide 6 dumps all business logic into generic "Node.js Microservices" without distinguishing between presentation boundaries, use-case controllers, and domain entity objects. | Conceptual vagueness in backend component architecture. | Restructure the application architecture into clean ECB layers: Presentation Boundary (Tablet Web UI), Use-Case Controllers (`ReceivingWorkflowManager`, `InspectionCoordinator`), and Domain Entities (`PurchaseOrder`, `InboundShipment`). |
| **JCOB-004** | **P2** | Disconnection Between Frontline Actor Workflows and Executive OTIF Scorecards | Slide 4 & Slide 5 | Slide 5 calculates OTIF and empowers dock supervisors to reroute POs, but Slide 4 provides no operational use-case flow showing how dock supervisors execute this decision. | Specifying executive KPIs and governance policies without modeling the associated user interaction workflow. | Define an explicit Use Case: "Supervise Vendor Delivery Exception," detailing actor triggers, review of historical delivery variances, and formal escalation to procurement. |
| **JCOB-005** | **P2** | Untraced Technical Components Lacking Actor Use-Case Justification | Slide 6 | Amazon S3 document storage and AWS CloudFront CDN are included on Slide 6 without mapping them to specific actor use cases or document retention rules. | Including cloud components based on generic best-practice templates rather than actor requirements. | Explicitly annotate each infrastructure component on Slide 6 with its driving use case (e.g. "Amazon S3: Stores photographic evidence for damaged carrier BOL dispute workflows"). |
| **JCOB-006** | **P3** | Passive-Voice Process Descriptions Masking Operational Agency | Slide 3 | Architecture blocks on Slide 3 use passive phrases ("Push a consolidated flat CSV file") without identifying which system agent initiates and monitors the transfer. | Passive architectural drafting. | Clarify system actors on Slide 3 (e.g. "Automated SFTP Daemon initiates scheduled extract and verifies checksum confirmation from SAP Gateway"). |
