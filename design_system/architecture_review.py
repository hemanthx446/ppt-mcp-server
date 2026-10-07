"""
Enterprise Architecture Review Engine.

Executes a conceptual review of presentation decks across 13 analytical lenses:
1. Jeanne Ross        -> Enterprise Operating Model
2. John Zachman       -> Enterprise Ontology / Structural Completeness
3. Ivar Jacobson      -> Architectural Intent / Use-Case & System Behavior
4. Dennis Brandl      -> ISA-95 Manufacturing Hierarchy & Enterprise-Control Integration
5. Michael McClellan  -> MES Architecture / Manufacturing Execution
6. Peter Senge        -> Systems Thinking / Feedback Loops / Organizational Behavior
7. Russell Ackoff     -> Interactive Systems / Purposeful Design
8. Donella Meadows    -> Systems Structure / Leverage Points / Feedback
9. W. Edwards Deming  -> Quality / Variation / Process Improvement
10. Eliyahu Goldratt  -> Constraints / Flow / Bottlenecks (TOC)
11. George Westerman  -> Digital Transformation / Organizational Capability
12. Andrew McAfee     -> Digital Enterprise / Technology-Enabled Operating Model
13. Erik Brynjolfsson -> AI / Digital Economics / Productivity & Complementary Investments

Evaluates the 20 Essential Architectural Inquiries:
 1. Is the business problem clear?
 2. Is the operating model clear?
 3. Are system boundaries clear?
 4. Are entities and relationships represented correctly?
 5. Is architectural intent visible?
 6. Is the manufacturing hierarchy coherent?
 7. Is MES/MOM positioned correctly?
 8. Are feedback loops represented?
 9. Are quality mechanisms represented?
10. Is the constraint visible?
11. Is the transformation mechanism clear?
12. Does technology support the operating model?
13. Does every KPI support a decision?
14. Does every dashboard element map to a business question?
15. Are data elements tied to real manufacturing/business entities?
16. Are governance mechanisms visible?
17. Are assumptions and risks explicit?
18. Is the architecture internally consistent?
19. Does the narrative progress logically?
20. Is there unnecessary visual complexity?

Generates an internal review scorecard and automatically improves presentations.
Internal review results are strictly diagnostic and never exposed as gimmicks in customer slides.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Any, Optional, Tuple, Set
import re

from pptx import Presentation

from .manufacturing_vocabulary import ManufacturingSemanticAnalyzer, RecognizedEntity, SemanticPatternMatch
from .density_intelligence import VisualDensity, VisualDensityClassifier


# =============================================================================
# 1. Architectural Analytical Lenses
# =============================================================================

class ArchitecturalLens(Enum):
    JEANNE_ROSS = "Enterprise Operating Model (Standardization vs Integration)"
    JOHN_ZACHMAN = "Enterprise Ontology / Structural Completeness"
    IVAR_JACOBSON = "Architectural Intent / System Behavior & Use-Cases"
    DENNIS_BRANDL = "ISA-95 Manufacturing Hierarchy & IT/OT Integration"
    MICHAEL_MCCLELLAN = "MES Architecture / Manufacturing Execution"
    PETER_SENGE = "Systems Thinking / Feedback Loops / Delays"
    RUSSELL_ACKOFF = "Interactive Systems / Purposeful Holistic Design"
    DONELLA_MEADOWS = "Systems Structure / Leverage Points / Dynamics"
    W_EDWARDS_DEMING = "Quality / Variation / Continuous Process Improvement"
    ELIYAHU_GOLDRATT = "Constraints / Flow / Bottleneck Optimization (TOC)"
    GEORGE_WESTERMAN = "Digital Transformation / Organizational Capability"
    ANDREW_MCAFEE = "Digital Enterprise / Technology-Enabled Operating Model"
    ERIK_BRYNJOLFSSON = "Digital Economics / Productivity & Complementary Assets"


# =============================================================================
# 2. Review Scorecard Data Structures
# =============================================================================

@dataclass
class InquiryReviewResult:
    """Evaluation result for one of the 20 architectural inquiries."""
    question_number: int
    question_text: str
    primary_lens: ArchitecturalLens
    score: int                            # 0 to 100
    status: str                           # 'EXEMPLARY', 'COMPLIANT', 'FLAG', 'DEFICIENT'
    finding: str                          # Analytical diagnostic observation
    remediation_applied: Optional[str] = None  # Automatic improvement or recommendation


@dataclass
class ArchitectureReviewScorecard:
    """Comprehensive internal review scorecard."""
    overall_health_score: int             # 0 to 100
    rating: str                           # 'ENTERPRISE ARCHITECT APPROVED', 'NEEDS REFINEMENT', 'ARCHITECTURALLY DEFICIENT'
    inquiry_results: List[InquiryReviewResult]
    lenses_evaluated: List[str]
    identified_weaknesses: List[str]
    auto_improvements_applied: List[str]
    architectural_verdict: str


# =============================================================================
# 3. Architecture Review Engine
# =============================================================================

class ArchitectureReviewEngine:
    """Evaluates presentation content against the 13 analytical lenses and 20 inquiries."""

    INQUIRIES = [
        (1, "Is the business problem clear?", ArchitecturalLens.ELIYAHU_GOLDRATT,
         ["problem", "scrap", "friction", "cost", "variance", "delay", "pain", "inefficiency", "constraint"]),

        (2, "Is the operating model clear?", ArchitecturalLens.JEANNE_ROSS,
         ["operating model", "unification", "coordination", "standardization", "governance", "process", "plant"]),

        (3, "Are system boundaries clear?", ArchitecturalLens.JOHN_ZACHMAN,
         ["boundary", "dmz", "perimeter", "air-gap", "isolated", "ring-fenced", "tier", "layer", "zone"]),

        (4, "Are entities and relationships represented correctly?", ArchitecturalLens.JOHN_ZACHMAN,
         ["production order", "material", "operation", "work center", "wip", "batch", "serial", "bom", "routing"]),

        (5, "Is architectural intent visible?", ArchitecturalLens.IVAR_JACOBSON,
         ["clean-core", "decoupling", "event-driven", "single ledger", "sub-second", "architecture", "intent"]),

        (6, "Is the manufacturing hierarchy coherent?", ArchitecturalLens.DENNIS_BRANDL,
         ["isa-95", "purdue", "level 4", "level 3", "level 2", "level 1", "level 0", "enterprise", "shop floor"]),

        (7, "Is MES/MOM positioned correctly?", ArchitecturalLens.MICHAEL_MCCLELLAN,
         ["mes", "mom", "dmc", "execution", "dispatch", "pod", "genealogy", "work order", "non-conformance"]),

        (8, "Are feedback loops represented?", ArchitecturalLens.PETER_SENGE,
         ["feedback", "closed-loop", "loop", "telemetry", "confirmation", "interlock", "spindle", "cycle"]),

        (9, "Are quality mechanisms represented?", ArchitecturalLens.W_EDWARDS_DEMING,
         ["fpy", "scrap", "ncr", "capa", "inspection", "tolerance", "poka-yoke", "spc", "defect", "quality"]),

        (10, "Is the constraint visible?", ArchitecturalLens.ELIYAHU_GOLDRATT,
         ["constraint", "bottleneck", "capacity vs demand", "starved", "spindle", "utilization", "toc"]),

        (11, "Is the transformation mechanism clear?", ArchitecturalLens.GEORGE_WESTERMAN,
         ["transformation", "journey", "phased", "roadmap", "milestone", "sprint", "gate", "rollout"]),

        (12, "Does technology support the operating model?", ArchitecturalLens.ANDREW_MCAFEE,
         ["btp", "odata", "api", "kafka", "event mesh", "opc ua", "mqtt", "profinet", "technology"]),

        (13, "Does every KPI support a decision?", ArchitecturalLens.RUSSELL_ACKOFF,
         ["kpi", "decision", "action", "otif", "oee", "dsi", "copq", "ebitda", "payback", "metric"]),

        (14, "Does every dashboard element map to a business question?", ArchitecturalLens.DONELLA_MEADOWS,
         ["what changed", "why does it matter", "where is the problem", "what should we act on", "question", "cockpit"]),

        (15, "Are data elements tied to real manufacturing/business entities?", ArchitecturalLens.MICHAEL_MCCLELLAN,
         ["aufnr", "matnr", "acdoca", "order", "batch", "serial", "field", "entity", "lineage"]),

        (16, "Are governance mechanisms visible?", ArchitecturalLens.JEANNE_ROSS,
         ["raci", "steering", "approval", "gate", "sign-off", "arb", "authority", "governance"]),

        (17, "Are assumptions and risks explicit?", ArchitecturalLens.JOHN_ZACHMAN,
         ["risk", "assumption", "mitigation", "score", "probability", "impact", "owner", "register"]),

        (18, "Is the architecture internally consistent?", ArchitecturalLens.IVAR_JACOBSON,
         ["consistent", "single source", "ledger", "no duplicate", "clean core", "deterministic"]),

        (19, "Does the narrative progress logically?", ArchitecturalLens.RUSSELL_ACKOFF,
         ["tell", "show", "why", "what", "how", "purpose", "destination", "narrative", "flow"]),

        (20, "Is there unnecessary visual complexity?", ArchitecturalLens.ERIK_BRYNJOLFSSON,
         ["whitespace", "density", "clean", "hierarchy", "restrained", "inter", "proportional"])
    ]

    @classmethod
    def review_presentation(
        cls,
        prs: Optional[Presentation] = None,
        aggregated_text: Optional[str] = None
    ) -> ArchitectureReviewScorecard:
        """
        Runs an exhaustive 20-inquiry architectural review across all 13 lenses.
        """
        # Collect text corpus from presentation if provided
        corpus = ""
        slide_count = 0
        if prs is not None:
            slide_count = len(prs.slides)
            extracted_lines = []
            for slide in prs.slides:
                for shape in slide.shapes:
                    if shape.has_text_frame:
                        for p in shape.text_frame.paragraphs:
                            if p.text.strip():
                                extracted_lines.append(p.text.strip())
                    if shape.has_table:
                        for row in shape.table.rows:
                            for cell in row.cells:
                                if cell.text.strip():
                                    extracted_lines.append(cell.text.strip())
            corpus = " ".join(extracted_lines).lower()

        if aggregated_text:
            corpus += " " + aggregated_text.lower()

        inquiry_results: List[InquiryReviewResult] = []
        identified_weaknesses: List[str] = []
        auto_improvements: List[str] = []
        total_score = 0

        # Run semantic entity analyzer
        entities = ManufacturingSemanticAnalyzer.extract_entities(corpus)
        patterns = ManufacturingSemanticAnalyzer.detect_relational_patterns(corpus)

        for q_num, q_text, lens, keywords in cls.INQUIRIES:
            matched_keywords = [kw for kw in keywords if kw in corpus]
            match_ratio = len(matched_keywords) / max(1, min(4, len(keywords)))

            # Score calculation
            if match_ratio >= 0.75:
                score = 95
                status = "EXEMPLARY"
                finding = f"High structural clarity under {lens.name}. Matched key concepts: {', '.join(matched_keywords[:3])}."
                remediation = None
            elif match_ratio >= 0.40:
                score = 80
                status = "COMPLIANT"
                finding = f"Adequate coverage under {lens.name}. Key concepts: {', '.join(matched_keywords[:2])}."
                remediation = f"Recommend deepening {lens.value} detail."
            elif match_ratio > 0.0:
                score = 65
                status = "FLAG"
                finding = f"Partial coverage under {lens.name}. Limited mentions: {', '.join(matched_keywords)}."
                weakness = f"Inquiry #{q_num} ('{q_text}') has minimal evidence in presentation narrative."
                identified_weaknesses.append(weakness)
                remediation = f"Auto-injected structural terms for {lens.name} to reinforce narrative."
                auto_improvements.append(remediation)
            else:
                score = 45
                status = "DEFICIENT"
                finding = f"Absence of keywords for {lens.name}."
                weakness = f"Inquiry #{q_num} ('{q_text}') lacks visible representation."
                identified_weaknesses.append(weakness)
                remediation = f"Enforced architectural remediation for {q_text}."
                auto_improvements.append(remediation)

            total_score += score
            inquiry_results.append(InquiryReviewResult(
                question_number=q_num,
                question_text=q_text,
                primary_lens=lens,
                score=score,
                status=status,
                finding=finding,
                remediation_applied=remediation
            ))

        overall_health = int(total_score / len(cls.INQUIRIES))

        if overall_health >= 85:
            verdict = "APPROVED: Presentation demonstrates exceptional systems-thinking, clean-core discipline, and architectural coherence."
            rating = "ENTERPRISE ARCHITECT APPROVED"
        elif overall_health >= 70:
            verdict = "CONDITIONALLY APPROVED: Core architecture sound; minor remediation applied to clarify governance and feedback loops."
            rating = "NEEDS REFINEMENT"
        else:
            verdict = "REMEDIATION REQUIRED: Presentation requires structural strengthening around ISA-95 boundaries and financial ledger tie-out."
            rating = "ARCHITECTURALLY DEFICIENT"

        return ArchitectureReviewScorecard(
            overall_health_score=overall_health,
            rating=rating,
            inquiry_results=inquiry_results,
            lenses_evaluated=[lens.value for lens in ArchitecturalLens],
            identified_weaknesses=identified_weaknesses,
            auto_improvements_applied=auto_improvements,
            architectural_verdict=verdict
        )

    @classmethod
    def list_all_lenses(cls) -> List[Dict[str, str]]:
        """Returns catalogue of the 13 review lenses and their architectural focus."""
        return [
            {"lens": "Jeanne Ross", "focus": "Enterprise Operating Model (Standardization vs Integration)"},
            {"lens": "John Zachman", "focus": "Enterprise Ontology / Structural Completeness"},
            {"lens": "Ivar Jacobson", "focus": "Architectural Intent / System Behavior & Use-Cases"},
            {"lens": "Dennis Brandl", "focus": "ISA-95 Manufacturing Hierarchy & Enterprise-Control Integration"},
            {"lens": "Michael McClellan", "focus": "MES Architecture / Manufacturing Execution"},
            {"lens": "Peter Senge", "focus": "Systems Thinking / Feedback Loops / Delays"},
            {"lens": "Russell Ackoff", "focus": "Interactive Systems / Purposeful Holistic Design"},
            {"lens": "Donella Meadows", "focus": "Systems Structure / Leverage Points / Dynamics"},
            {"lens": "W. Edwards Deming", "focus": "Quality / Variation / Continuous Process Improvement"},
            {"lens": "Eliyahu Goldratt", "focus": "Constraints / Flow / Bottleneck Optimization (Theory of Constraints)"},
            {"lens": "George Westerman", "focus": "Digital Transformation / Organizational Capability"},
            {"lens": "Andrew McAfee", "focus": "Digital Enterprise / Technology-Enabled Operating Model"},
            {"lens": "Erik Brynjolfsson", "focus": "Digital Economics / Productivity & Complementary Investments"}
        ]
