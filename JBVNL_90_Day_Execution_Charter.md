# JBVNL 90-DAY ENTERPRISE PILOT EXECUTION CHARTER
**Operational Implementation Blueprint & Field Deployment Manual**

---

### Document Control & Identification

* **Project Title:** JBVNL Enterprise Process Optimization & Value Realization Pilot (90-Day Quick Win)
* **Client Organization:** Jharkhand Bijli Vitran Nigam Limited (JBVNL)
* **Target Delivery Partner:** Lumbini Elite Solutions & Services Pvt. Ltd. (Lumbini Elite Group)
* **Target Operating Footprint:** 
  - Headquarters: Engineering Building, HEC, Dhurwa, Ranchi
  - Pilot Electric Supply Circles: **Ranchi Central Electric Supply Circle** & **Jamshedpur Electric Supply Circle**
  - Pilot Area Stores: **Ranchi Central Central Store** & **Jamshedpur Central Store**
* **Target Streams:** 
  1. Stream 1: Procurement-to-Payment (MM-FI Rate Contract Compliance & Digital Approvals)
  2. Stream 2: Stores Inventory & Material Control (MM-IM Serialization, Digital Store Issues & Scrap Visibility)
  3. Stream 3: Capital Work-in-Progress (CWIP) & Asset Capitalization (PS-FI Project Handover & RAB Pass-Through)
* **Date of Issue:** November 2026
* **Classification:** Highly Confidential — JBVNL Operational Charter

---

## 1. Executive Mandate & Strategic Objectives

### 1.1 The Operational Mandate
This Charter translates the high-level recommendations of the **10-Slide Executive Presentation** (`JBVNL_10_Slide_Executive_Presentation.pptx`) and **Board Memorandum** (`JBVNL_Board_Memorandum.md`) into a field-executable, 90-day implementation sprint.

### 1.2 Core Financial & Operational Goals
By Day 90, the pilot must achieve verifiable baseline metrics in Ranchi Central and Jamshedpur circles:

```
+----------------------------------------------------------------------------------------------------+
| TARGET METRIC                         | PRE-PILOT BASELINE               | DAY-90 TARGET MILESTONE |
+----------------------------------------------------------------------------------------------------+
| Offline Store Chits Issued           | 100% Paper Chits                 | 0% (100% Digital MIGO)  |
| Off-Contract Purchase Variances       | 18–25% Circle Emergency Buying   | < 3% Contract Bypasses  |
| Circle Store Inventory Holding Days   | 125 Days Average                 | <= 110 Days (-15 Days)  |
| Pending CWIP Handover Backlog         | > 14 Months Uncapitalized Works  | 100% Completed Reconciled|
| Daily Cash & Ledger Reconciliation    | 3–4 Weeks Delayed                | T+24 Hours Automated    |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Governance Framework & Project Steering Committee

To ensure accountability and prevent bureaucratic stagnation, a strict three-tier governance hierarchy is instituted:

```
                          +-------------------------------------------------+
                          |           PROJECT STEERING COMMITTEE (PSC)       |
                          | Chair: Managing Director, JBVNL                 |
                          | Members: Director (Finance), Director (Ops),    |
                          |          General Manager (IT), Lumbini Lead     |
                          | Cadence: Fortnightly (Every 2nd & 4th Tuesday)  |
                          +-------------------------------------------------+
                                                   |
                                                   v
                          +-------------------------------------------------+
                          |        PROJECT MANAGEMENT OFFICE (PMO)          |
                          | Leads: Superintending Engineer (HQ / IT)        |
                          |        Senior Accounts Officer (Finance / ERP)  |
                          |        Lumbini Project Delivery Manager         |
                          | Cadence: Weekly Review (Every Friday 4:00 PM)   |
                          +-------------------------------------------------+
                                                   |
                        +--------------------------+--------------------------+
                        |                                                     |
                        v                                                     v
      +-----------------------------------+                 +-----------------------------------+
      |   RANCHI CENTRAL EXECUTION TEAM   |                 |    JAMSHEDPUR EXECUTION TEAM      |
      | Lead: Superintending Engineer     |                 | Lead: Superintending Engineer     |
      | Members: Executive Engineer (Stores)|               | Members: Executive Engineer (Stores)|
      |          Assistant Accounts Officer|                |          Assistant Accounts Officer|
      |          Lumbini Circle Specialist|                 |          Lumbini Circle Specialist|
      +-----------------------------------+                 +-----------------------------------+
```

---

## 3. Scope Boundaries & Technical Interfaces

### 3.1 In-Scope Process Streams
1. **Material Management (SAP MM):**
   - Material Master deduplication and categorization.
   - Central Store to Circle Store stock transfer orders (STOs).
   - Goods Receipt (MIGO) against valid purchase orders.
   - Digital Goods Issue (MIGO 261) against approved maintenance work orders.
2. **Financial Accounting & Controlling (SAP FICO):**
   - Three-way invoice matching (PO, GRN, Vendor Invoice) in MIRO.
   - Budget Availability Control (AVAC) active blocking at circular commitment.
   - Daily automated bank scroll reconciliation against consumer collection accounts.
3. **Project Systems & Asset Accounting (SAP PS / FI-AA):**
   - Work breakdown structure (WBS) mapping for ongoing 33/11 kV feeder schemes.
   - Monthly settlement of CWIP line items to Asset Under Construction (AuC).
   - Final asset capitalization (ABUMN/AIBU) upon issuance of Electrical Inspector certificate.

### 3.2 Out-of-Scope (Boundaries Preserved)
- **Consumer Billing Engine (CIS):** No replacement of existing consumer billing software; automated daily batch interface for energy billed and cash collected is in-scope.
- **Field SCADA / AMR:** Field operational hardware remains untouched; meter data management system (MDMS) outbound energy feeds into SAP are in-scope.

---

## 4. Phase-by-Phase Work Breakdown Structure (Days 1–90)

```
====================================================================================================
PHASE 1: UNDERSTAND, AUDIT & CLEANSE (DAYS 1 TO 30)
====================================================================================================
Week 1 (Days 1–5): Project Mobilization & System Access Setup
  - Mobilize 1 Central Delivery Lead, 2 Functional Architects (MM/FICO), and 2 Circle Coordinators.
  - Execute read-only system access authorization for SAP production tables and basis logs.
  - Conduct kick-off orientation with Area Board General Managers and Circle Superintending Engineers.

Week 2 (Days 6–10): Forensic Transaction & Adoption Diagnostic
  - Extract and analyze user transaction history (ST03N, SM20) across all 15 circles for past 12 months.
  - Map transaction failure points: where do users drop out of SAP and revert to Excel?
  - Identify open purchase order commitments, unposted GRNs, and parked vouchers in pilot circles.

Week 3 (Days 11–15): Master Data Health Assessment & Cleansing Blueprint
  - Audit Material Master: identify duplicate codes for distribution transformers, conductors, and poles.
  - Audit Vendor Master: cross-verify active vendors against GSTIN numbers and MSME designations.
  - Establish standardized naming convention and mandatory field templates for all new entries.

Week 4 (Days 16–20): Baseline Telemetry & Target Alignment Workshop
  - Calculate exact pre-pilot baselines for Ranchi Central and Jamshedpur circles.
  - Finalize customized circular KPI scorecards approved by Director (Finance).
  - Deliver **Diagnostic Milestone Report (DMR)** to Project Steering Committee.

====================================================================================================
PHASE 2: STANDARDIZE, CONFIGURE & ENABLE (DAYS 31 TO 60)
====================================================================================================
Week 5 (Days 21–25): Process Simplification & Screen Optimization
  - Configure simplified SAP Fiori / WebGUI tiles for field storekeepers (one-click goods issue).
  - Activate hard Budget Availability Checks (AVAC) on Circle O&M cost centers.
  - Set up digital multi-level workflow approval paths for purchase requisitions > ₹50,000.

Week 6 (Days 26–30): Master Data Cleansing Execution
  - Execute data cleansing scripts: deactivate obsolete materials, block unverified vendor accounts.
  - Perform physical stock count in Ranchi Central and Jamshedpur stores; enter reconciliation adjustments.
  - Establish opening inventory balances locked and certified by Executive Engineer (Stores).

Week 7 (Days 31–35): Role-Based User Enablement & Hands-On Training
  - Conduct classroom and simulation training for 45 circle personnel (Engineers, Storekeepers, Accountants).
  - Provide laminated SOP cheat sheets: "How to Issue Material in 3 Minutes", "How to Clear an Invoice".
  - Conduct competency assessments; certify pilot operators prior to cutover.

Week 8 (Days 36–40): Mock Run & Operational Cutover Readiness Review
  - Conduct full end-to-end simulation of 50 sample transactions (Requisition -> PO -> GRN -> Issue -> Payment).
  - Issue formal circular mandate from Managing Director: **"Retirement of Paper Registers in Pilot Circles"**.
  - Pass Gate 2 Review with Project Steering Committee.

====================================================================================================
PHASE 3: GO-LIVE, MONITOR & MEASURE (DAYS 61 TO 90)
====================================================================================================
Week 9 (Days 41–45): Pilot Go-Live & Floor-Walking Support
  - Cutover execution in Ranchi Central and Jamshedpur circle stores.
  - Deploy floor-walking support specialists alongside storekeepers and accounts officers.
  - Disable paper requisition books; all material movements strictly backed by SAP reservations.

Week 10 (Days 46–50): Exception Cockpit & Real-Time Tracking
  - Launch Executive Exception Cockpit on Managing Director's desktop (live daily dashboard).
  - Monitor exception metrics: unposted MIGO receipts, delayed approvals, and unlinked cash deposits.
  - Daily 15-minute standup between Circle SEs and Lumbini Lead to clear transaction blocks.

Week 11 (Days 51–55): Initial Performance Audit & Value Realization Check
  - Review 30 days of live operational data: measure inventory drawdown and procurement rate compliance.
  - Verify zero paper register entries; confirm 100% digital audit trail on store movements.
  - Prepare true-up capitalization dossiers for completed 33/11 kV feeder assets in pilot circles.

Week 12 (Days 56–60): Final Pilot Evaluation & Statewide Rollout Blueprint
  - Quantify hard financial gains achieved during 30 days of live operations.
  - Present **Pilot Final Value Report (FVR)** to Chairman and Board of Directors.
  - Deliver Phase 2 Statewide Rollout Roadmap covering remaining 13 electric supply circles.
```

---

## 5. Field Resource Deployment Model

The pilot utilizes an agile, high-touch hybrid team structure ensuring full operational support without overwhelming JBVNL staff:

```
+----------------------------------------------------------------------------------------------------+
| ROLE / DESIGNATION                   | COUNT | DEPLOYMENT LOCATION         | CORE RESPONSIBILITY   |
+----------------------------------------------------------------------------------------------------+
| Engagement Partner / Strategic Lead  | 1     | Ranchi HQ / Boardroom       | PSC Cadence, MD Sync  |
| Senior Functional Architect (MM/SCM) | 1     | Ranchi HQ & Central Store   | Stores & PO Workflow  |
| Senior Functional Architect (FICO/PS)| 1     | Ranchi HQ & Accounts Div.   | Budgeting & CWIP Tie  |
| Circle Field Specialist (Ranchi)     | 2     | Ranchi Central Store Yard   | Floor-Walking, Users  |
| Circle Field Specialist (Jamshedpur) | 2     | Jamshedpur Store Yard       | Floor-Walking, Users  |
| Master Data Cleansing Specialist     | 1     | Central Processing / Remote | Cleansing & Uploads   |
+----------------------------------------------------------------------------------------------------+
| TOTAL LUMBINI DEDICATED TEAM         | 8 FTE | On-Site / Field Hybrid      | 90-Day Sprint Duration|
+----------------------------------------------------------------------------------------------------+
```

---

## 6. Daily Executive Exception Cockpit Metrics

Starting on Day 61, the executive dashboard surfaces 5 real-time operational indicators directly to the Managing Director and Director (Finance):

1. **Circle Store Movement Compliance:** Percentage of store material issues backed by digital SAP reservation (Target: 100%).
2. **Rate Contract Adherence:** Value of purchase orders placed outside approved central rate contracts (Target: ₹0).
3. **Pending Approval Ageing:** Count of purchase requisitions or store issues pending signature > 48 hours (Target: 0).
4. **CWIP Capitalization Tracker:** Value of completed distribution works capitalized into Fixed Assets during the month (Target: > ₹25 Cr/month).
5. **Cash-Ledger Reconciliation Delta:** Value of bank collections received but unlinked to consumer ledgers (Target: < 0.5% of monthly gross collection).

---

## 7. Risk Management & Mitigation Matrix

```
+----------------------------------------------------------------------------------------------------+
| RISK EVENT                    | PROBABILITY | IMPACT | MITIGATION STRATEGY                         |
+----------------------------------------------------------------------------------------------------+
| Field User Resistance &        | HIGH        | HIGH   | MD circular formally retiring paper;        |
| Reversion to Paper Registers  |             |        | floor-walking support assists operators.    |
+----------------------------------------------------------------------------------------------------+
| Unclean Master Data Causing   | HIGH        | MED    | Aggressive Days 15–30 cleansing sprint;     |
| Transaction Errors in MIGO    |             |        | lock master data creation authority at HQ.  |
+----------------------------------------------------------------------------------------------------+
| Network / Connectivity Outage | MED         | MED    | Offline store caching protocol; local       |
| at Circle Store Yards         |             |        | store SIM dongle backup provided.           |
+----------------------------------------------------------------------------------------------------+
| Delayed Approval Sign-Offs by | MED         | HIGH   | Escalation matrix: approvals un-actioned in |
| Superintending Engineers      |             |        | 48 hours escalate automatically to CE/Dir.  |
+----------------------------------------------------------------------------------------------------+
```

---
*Charter ready for formal sign-off by JBVNL Executive Sponsors.*  
**Lumbini Elite Solutions & Services**
