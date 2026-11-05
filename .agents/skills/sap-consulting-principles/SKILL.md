---
name: sap-consulting-principles
description: Apply field-tested SAP delivery principles when reviewing SAP plans, change requests, proposals, go-live readiness, client messages or handover docs, or advising consultants.
---

# SAP Consulting Principles

Eight lessons from a practitioner with 27 years in SAP (programs from $1M to $200M, teams from 5 to 4,000+), shared in a post by Viswas Anantharangachar. This skill turns them into checks and behaviours. Use it as a review lens and a drafting guide, not as quotes to recite.

## When to use

Use this skill when the task involves any of:
- Reviewing or writing an SAP proposal, SOW, project plan, risk log or status report
- Assessing a change request or "quick fix" in an integrated landscape
- Go-live, cutover or hypercare readiness
- Drafting client communication, especially bad news or scope pushback
- Writing or reviewing handover, runbook or design documentation
- Coaching a junior consultant or planning someone's growth
- Positioning a consultant as advisor rather than implementer

Skip it for pure technical how-to questions (a specific configuration step, a transaction code) unless the question hides a scope or impact decision.

## The eight principles as working checks

### 1. Business before system
Check: can the plan, proposal or design state how this client makes money, where margin leaks, and which process outcome matters most?
- Before any configuration advice, ask or state: what business outcome does this serve, and who owns it?
- Flag deliverables described only in system terms (modules, objects, T-codes) with no business result.
- In proposals, open with the client's business problem, then the system.

### 2. No change is simple
Check: has the ripple effect been traced?
- For any change, list the touched areas: pricing/conditions, finance posting and reconciliation, reporting and analytics, interfaces and integrations, authorizations, master data, batch jobs, custom code, downstream/upstream systems, training.
- Ask specifically: "Which interface or report nobody remembered reads this?"
- Do not sign off an impact statement that says "minor" or "no impact" without the trace. Require a regression scope and an owner for each touched area.

### 3. Crisis is remembered, not the party
Check: is there a real support model for the first hours of trouble?
- Go-live readiness must name who answers at 2 AM, the escalation path, response expectations and a rollback or workaround for the top operational stoppages (shipping, billing, production confirmation, payroll).
- Plan hypercare around the business-critical flows, not around module lists.
- In status reports, surface operational risks that could stop the business before cosmetic items.

### 4. Early "no" beats late "sorry"
Check: has anything that won't work been said while there's still time to fix it?
- Actively look for what the client is assuming that is not feasible, not funded, not in scope or not in the standard product.
- When drafting, state the constraint plainly, give the reason in one or two sentences, then offer options with trade-offs and a recommended path. Never hide a "no" inside caveats.
- In proposals, put dependencies, assumptions and exclusions where the buyer will read them, with a decision date.

### 5. Curiosity beats certification
Check: does the person or plan rely on credentials instead of understanding?
- When coaching, steer toward asking "why does the process work this way?" and tracing a transaction end to end, not collecting badges.
- When reviewing a design, ask for the reason behind each non-standard choice.
- Certifications are useful for access. Treat them as a starting point, not as evidence of judgment.

### 6. Write it down for whoever comes next
Check: could a stranger in five years run, support and change this?
- Handover must cover: purpose and business context, design decisions and the alternatives rejected, configuration and custom objects, interfaces and data flows, known issues, operating procedures, contacts and ownership.
- Record decisions and their rationale as they are made, not at the end.
- Flag undocumented workarounds and tribal knowledge as risks.

### 7. Technology changes, fundamentals don't
Check: is the plan solving the durable problems?
- Whatever the platform (ECC, S/4HANA, cloud, AI agents), test for: clean and owned data, clear and agreed processes, named people accountable for outcomes.
- Challenge any plan that leads with the technology and has no data quality plan, process owners or accountable business owner.
- For new technology (including AI agents), ask what happens to bad data, unclear process and missing ownership. The technology amplifies them.

### 8. Relationships outlast projects
Check: does the way the work is run build trust beyond the project?
- Communicate honestly, keep commitments, credit others, and treat junior people and counterparts as future senior stakeholders.
- After closure, leave the relationship in better shape than the contract required.

## How to apply this skill

1. Identify the artifact or decision (plan, change, proposal, go-live, message, doc, coaching question).
2. Run only the principles that are relevant. Most tasks need two to four.
3. Report findings in this order:
   - Verdict in one line (ready, ready with conditions, not ready).
   - Top issues, each tied to a principle, with the evidence from the artifact.
   - Concrete fixes or the exact questions to ask the client or team.
   - What is missing and needs to be confirmed.
4. Keep the output direct and actionable. Give honest assessments, including unwelcome ones, with the reasoning.
5. Draft client-facing text in plain, calm business English. No lecturing, no quoting the principles at the client.

## Output patterns

- **Change-impact review:** table with columns Area touched, Why affected, Test or owner, Risk.
- **Go-live readiness:** checklist grouped by business-critical flow, with owner, support window, rollback or workaround.
- **Early-no message:** situation, what won't work, why, options with trade-offs, recommendation, decision needed by.
- **Handover check:** list missing sections against the documentation list above.
- **Coaching note:** one principle, one practical habit, one question to ask in the next meeting.

## Use inside the presentation pipeline

- Storyline and Distill stages, for proposals, plans and go-live decks about SAP delivery: put assumptions, dependencies and exclusions before commercials (principle 4); state the business outcome before the system scope (1); include a support/hypercare slide naming who responds out of hours (3); include a handover/documentation commitment (6).
- QA stage: fail a proposal deck that has no assumptions/exclusions slide or section, or that describes scope only in modules and objects.
- Do not load this skill for decks that are not about SAP delivery.

## Guardrails

- Do not invent facts about the client, the system or the project. Mark assumptions.
- Do not present these principles as rules that override the client's situation. They are a lens for judgment.
- Do not reproduce the source post at length. Attribute it when asked where the principles come from.
- If a principle does not apply, say so and move on.
