from typing import Dict, Any, List, Tuple, Optional

class VisualPlanner:
    """
    Stage 4: Corporate Graphic Designer Visual & Layout Planner (v2)
    Applies relationship-first visual planning, scores grammar candidates,
    records layout rationales, and enforces strict deck diversity constraints.
    """

    ALLOWED_SHAPES = [
        "cover",
        "requirement_to_outcome",
        "hub_and_spokes",
        "dashboard_concept",
        "levels_x_dimensions",
        "process_linear",
        "step_line",
        "flow_with_actions",
        "phases_over_time",
        "roles_and_terms",
        "benchmark_table",
        # New v2 relationship grammars:
        "layered_stack",
        "iceberg_shift",
        "constraint_flow",
        "causal_loop",
        "tradeoff_matrix",
        "capability_maturity_staircase",
        "annotated_chart",
        "career_trajectory_roadmap",
        "metadata_vs_context",
        "closing"
    ]

    ALLOWED_RELATIONSHIPS = [
        "causal_loop",
        "constraint_flow",
        "layered_stack",
        "before_after_shift",
        "tradeoff_matrix",
        "career_trajectory_roadmap",
        "metadata_vs_context",
        "closing",
        "sequence",
        "progression",
        "decomposition",
        "comparison",
        "distribution",
        "trend",
        "network",
        "governance_map",
        "evidence_claim"
    ]

    @classmethod
    def score_visual_grammar(cls, rel: Dict[str, Any]) -> Tuple[str, str]:
        """
        Scores candidate visual grammars based on element count, link directionality,
        time ordering, quantities, and relationship semantics.
        Returns (chosen_grammar, rationale).
        """
        rel_type = rel.get("type", "decomposition")
        elem_count = len(rel.get("elements", []))
        has_directional_links = any(l.get("kind") in ("causes", "feeds", "constrains", "precedes") for l in rel.get("links", []))
        is_time_ordered = rel.get("time") in ("ordered", "dated")
        has_quantity = rel.get("quantity") in ("ordinal", "measured")

        candidates = []

        if rel_type == "causal_loop" or any(l.get("kind") == "causes" for l in rel.get("links", [])):
            candidates.append(("causal_loop", 9.5, "Reinforcing and balancing feedback loops with systemic delays."))
        
        if rel_type == "constraint_flow" or any(l.get("kind") == "constrains" for l in rel.get("links", [])):
            candidates.append(("constraint_flow", 9.2, "Linear throughput pipeline with binding constraint highlighted."))

        if rel_type == "layered_stack" or rel.get("hierarchy") in ("tiers", "nested"):
            candidates.append(("layered_stack", 9.0, "Hierarchical platform layers with vertical data/control flow."))

        if rel_type == "before_after_shift":
            candidates.append(("iceberg_shift", 9.1, "Two-state shift separating visible events from submerged structures."))
            candidates.append(("requirement_to_outcome", 7.5, "Three-column baseline to target outcome transformation."))

        if rel_type == "tradeoff_matrix":
            candidates.append(("tradeoff_matrix", 9.0, "2x2 decision space with explicit strategic criteria on axes."))

        if rel_type == "progression":
            candidates.append(("capability_maturity_staircase", 8.8, "Ascending maturity stages with competencies and gate criteria."))
            candidates.append(("phases_over_time", 8.0, "Sequential timeline phases."))

        if rel_type in ("trend", "distribution") or has_quantity:
            candidates.append(("annotated_chart", 9.3, "Native quantitative chart with direct labels and executive argument panel."))

        if rel_type == "sequence" or is_time_ordered:
            candidates.append(("process_linear", 8.5, "Phased execution pathway with audit deliverables."))

        if rel_type == "governance_map":
            candidates.append(("levels_x_dimensions", 8.7, "Multi-tier stakeholder matrix across operational dimensions."))

        if rel_type == "network":
            candidates.append(("hub_and_spokes", 8.2, "Central platform core orchestrating integration domains."))

        if not candidates:
            candidates.append(("requirement_to_outcome", 7.0, "Structured multi-column capability decomposition."))

        candidates.sort(key=lambda x: x[1], reverse=True)
        chosen_grammar, score, rationale = candidates[0]
        full_rationale = f"Selected '{chosen_grammar}' (fit score {score:.1f}/10): {rationale} Matches relationship '{rel_type}' with {elem_count} elements."
        return (chosen_grammar, full_rationale)

    @classmethod
    def validate_layout_rules(cls, slides: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        violations = []
        if not slides:
            return False, ["Slide list is empty."]

        layouts_used = [s.get("content_shape") for s in slides if s.get("content_shape") not in ("cover", "closing")]
        
        # 1. No composition grammar used more than twice in a deck
        from collections import Counter
        counts = Counter(layouts_used)
        for shape, count in counts.items():
            if count > 2:
                violations.append(f"Layout grammar '{shape}' used {count} times (max 2 allowed per deck).")

        # 2. Adjacent slides must differ
        for i in range(len(layouts_used) - 1):
            if layouts_used[i] == layouts_used[i+1] and layouts_used[i] is not None:
                violations.append(f"Adjacent slides {i+2} and {i+3} share identical layout grammar '{layouts_used[i]}'. Adjacent slides must differ.")

        # 3. Shape validity
        for i, s in enumerate(slides, 1):
            c_shape = s.get("content_shape")
            if c_shape not in cls.ALLOWED_SHAPES:
                violations.append(f"Slide {i} has invalid content_shape: '{c_shape}'. Must be one of {cls.ALLOWED_SHAPES}.")

        return (len(violations) == 0, violations)
