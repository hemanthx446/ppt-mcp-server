---
name: transformation-nexus-research
description: Structures research and synthesis through seven analytical lenses (Westerman, McAfee, Brynjolfsson, Hammer, Carr, Schallmo, Zeng) to uncover tensions, contradictions, and systemic realities beneath enterprise transformations.
---

# Transformation Nexus Research

This skill guides deep research and strategic synthesis for enterprise transformation presentations.
It ensures presentations reconstruct what *actually changed beneath the implementation* rather than writing marketing success stories.

## Principles & Honesty Rules

1. **Analytical Lenses, Not Impersonation:**
   The seven lenses are analytical frameworks based on each author's published academic and business literature. The agent must never impersonate the thinkers, invent quotes, or claim they endorse a conclusion.
2. **Retrievable Citations:**
   Every claim attributed to a framework requires a retrievable citation. If a source cannot be confirmed, state the analytical question or idea without personal attribution.
3. **Surfacing Contradictions:**
   Real transformations involve trade-offs and tensions (e.g. Carr's commodity risk vs McAfee's digital differentiation). The synthesis must produce a **contradiction table** showing where lenses disagree.

## The 7 Analytical Lenses

1. **Westerman (Digital Transformation):**
   *Question:* Did the enterprise change *what* it does with technology (digital capability) and *how it leads* (vision, governance, culture)? Where is the gap between capability and leadership?
2. **McAfee (Digital Enterprise):**
   *Question:* What changed in how decisions are made and who makes them (data over HiPPO, platform ecosystems, crowds, decentralized talent)?
3. **Brynjolfsson (AI-Driven Business & Productivity J-Curve):**
   *Question:* Is technology complemented by process, human capital, and organizational redesign? Is the productivity "J-curve" visible (initial performance dip during restructuring, followed by compounded gains)?
4. **Hammer (Reengineering & Process Obliteration):**
   *Question:* Which work was *obliterated* rather than paved over / automated? What fundamental legacy process assumption was eliminated?
5. **Carr (Commoditization of Infrastructure):**
   *Question:* Which part of the technology is now a standardized commodity, and where does true strategic advantage sit (operational execution, risk discipline, cost controls)?
6. **Schallmo (Business Model Transformation):**
   *Question:* Which business model elements (value proposition, customer segments, value network, revenue model) changed, and in what sequence?
7. **Zeng (Smart Business & Ecosystem Co-creation):**
   *Question:* Which ecosystem links, customer-to-business (C2B) loops, and network partners co-create value through real-time data feedback?

## Standard Procedure

1. **Ingest Facts:** Extract facts from `CASE_FACTS`, user documents, and verified research, assigning each fact a persistent ID (`[SRC-01]`, `[SRC-02]`, etc.).
2. **Evaluate Lenses:** For each lens, answer its core question with evidence or mark `no evidence`.
3. **Construct Contradiction Table:** Identify tensions between lenses (e.g. standardization vs differentiation).
4. **Produce `nexus.json`:** Export findings, evidence IDs, confidence ratings, and "what would change my mind" criteria.
5. **Feed Storyline:** Storyline stage must consume `nexus.json` and make visible the systemic friction, delays, and counterfactuals.
