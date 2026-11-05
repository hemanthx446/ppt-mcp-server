import os
import yaml
from typing import Dict, Any, List, Optional, Tuple

class ContentDistiller:
    """
    Stage 3: Presentation Strategist Content Distillation Engine
    Enforces word budgets, capability registry classifications, and notes splitting in code.
    Supports all Level B parameterised visual compositions.
    """

    WORD_BUDGET_COVER = 50
    WORD_BUDGET_SLIDE_TARGET = 120
    WORD_BUDGET_SLIDE_HARD = 160
    WORD_BUDGET_DENSE_SLIDE = 200
    WORD_BUDGET_BULLET = 12

    def __init__(self, registry_path: Optional[str] = None):
        if not registry_path:
            registry_path = os.path.join(os.path.dirname(__file__), "capabilities.yaml")
        registry_path = os.path.abspath(registry_path)
        self.capabilities = {}
        if os.path.exists(registry_path):
            with open(registry_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                for item in data.get("capabilities", []):
                    self.capabilities[item["id"]] = item

    def count_words(self, text: Any) -> int:
        if not text:
            return 0
        if isinstance(text, (list, tuple)):
            return sum(self.count_words(item) for item in text)
        return len(str(text).strip().split())

    def audit_slide_content(self, slide_spec: Dict[str, Any]) -> Tuple[bool, int, List[str]]:
        """
        Audits a slide content object against word budgets and content constraints.
        Returns (is_valid, word_count, violation_messages).
        """
        violations = []
        total_words = 0
        s_num = slide_spec.get("slide_number", 0)
        c_shape = slide_spec.get("content_shape", "")

        # Action title
        title_w = self.count_words(slide_spec.get("title", ""))
        total_words += title_w

        # Subtitle
        sub_w = self.count_words(slide_spec.get("subtitle", ""))
        total_words += sub_w

        # Body items depending on shape
        if c_shape == "cover":
            for k, v in slide_spec.get("metadata", []):
                total_words += self.count_words(k) + self.count_words(v)
            if total_words > self.WORD_BUDGET_COVER:
                violations.append(f"Slide {s_num} (Cover) exceeded budget: {total_words} words (limit {self.WORD_BUDGET_COVER})")

        elif c_shape == "requirement_to_outcome":
            for item in slide_spec.get("items", []):
                w_req = self.count_words(item.get("requirement") or item.get("dimension") or item.get("title") or "")
                w_tod = self.count_words(item.get("today") or item.get("baseline") or item.get("from") or "")
                w_out = self.count_words(item.get("outcome") or item.get("target") or item.get("to") or "")
                total_words += w_req + w_tod + w_out
                if w_out > 20:
                    violations.append(f"Slide {s_num} outcome bullet too verbose: {w_out} words")

        elif c_shape == "hub_and_spokes":
            total_words += self.count_words(slide_spec.get("hub_title", ""))
            total_words += self.count_words(slide_spec.get("hub_subtitle", ""))
            for sp in slide_spec.get("spokes", []):
                total_words += self.count_words(sp.get("title", ""))
                total_words += self.count_words(sp.get("desc", ""))

        elif c_shape == "dashboard_concept":
            for step in slide_spec.get("flow_steps", []):
                total_words += self.count_words(step)
            for k_lbl, k_val, k_del in slide_spec.get("kpis", []):
                total_words += self.count_words(k_lbl) + self.count_words(k_val) + self.count_words(k_del)
            for d_name, d_desc in slide_spec.get("drill_steps", []):
                total_words += self.count_words(d_name) + self.count_words(d_desc)
            total_words += self.count_words(slide_spec.get("platform_note", ""))

        elif c_shape == "levels_x_dimensions":
            for r_title, r_desc, _ in slide_spec.get("row_headers", []):
                total_words += self.count_words(r_title) + self.count_words(r_desc)
            for row in slide_spec.get("cells", []):
                for cell in row:
                    total_words += self.count_words(cell)
            total_words += self.count_words(slide_spec.get("caveat_text", ""))
            for cap in slide_spec.get("confirmed_caps", []):
                total_words += self.count_words(cap)

        elif c_shape in ("process_linear", "step_line"):
            for title, desc in slide_spec.get("steps", []):
                total_words += self.count_words(title) + self.count_words(desc)
            for d in slide_spec.get("deliverables", []):
                total_words += self.count_words(d)
            total_words += self.count_words(slide_spec.get("caveat_text", ""))

        elif c_shape == "flow_with_actions":
            for b_title, b_sub, _ in slide_spec.get("flow_boxes", []):
                total_words += self.count_words(b_title) + self.count_words(b_sub)
            for act in slide_spec.get("actions", []):
                total_words += self.count_words(act)
            total_words += self.count_words(slide_spec.get("caveat_text", ""))

        elif c_shape == "phases_over_time":
            for p_name, p_act in slide_spec.get("phases", []):
                total_words += self.count_words(p_name) + self.count_words(p_act)
            total_words += self.count_words(slide_spec.get("future_readiness_title", ""))
            total_words += self.count_words(slide_spec.get("future_readiness_desc", ""))

        elif c_shape == "roles_and_terms":
            for itm, amt in slide_spec.get("commercial_rows", []):
                total_words += self.count_words(itm) + self.count_words(amt)
            for role, resp, alloc in slide_spec.get("resource_rows", []):
                total_words += self.count_words(role) + self.count_words(resp) + self.count_words(alloc)
            for t_title, t_desc in slide_spec.get("terms_list", []):
                total_words += self.count_words(t_title) + self.count_words(t_desc)

        # New v2 shapes
        elif c_shape in ("layered_stack", "platform_stack"):
            for l in slide_spec.get("layers", []):
                total_words += self.count_words(l.get("tier", "")) + self.count_words(l.get("title", "")) + self.count_words(l.get("desc", ""))
            total_words += self.count_words(slide_spec.get("callout_note", ""))

        elif c_shape in ("iceberg_shift", "before_after_shift"):
            v = slide_spec.get("visible_event", {})
            total_words += self.count_words(v.get("title", "")) + self.count_words(v.get("desc", ""))
            for sl in slide_spec.get("submerged_layers", []):
                total_words += self.count_words(sl.get("layer_name", "")) + self.count_words(sl.get("finding", ""))
            total_words += self.count_words(slide_spec.get("callout_text", ""))

        elif c_shape == "constraint_flow":
            for st in slide_spec.get("stages", []):
                total_words += self.count_words(st.get("name", "")) + self.count_words(st.get("desc", "")) + self.count_words(st.get("rate", ""))
            total_words += self.count_words(slide_spec.get("buffer_desc", ""))
            total_words += self.count_words(slide_spec.get("impact_annotation", ""))

        elif c_shape == "causal_loop":
            for n in slide_spec.get("nodes", []):
                total_words += self.count_words(n.get("label", "")) + self.count_words(n.get("desc", ""))
            for lp in slide_spec.get("loops", []):
                total_words += self.count_words(lp.get("type", "")) + self.count_words(lp.get("effect", ""))
            total_words += self.count_words(slide_spec.get("delay_annotation", ""))

        elif c_shape == "tradeoff_matrix":
            for q in slide_spec.get("quadrants", []):
                total_words += self.count_words(q.get("name", "")) + self.count_words(q.get("desc", ""))
            total_words += self.count_words(slide_spec.get("callout_note", ""))
            total_words += self.count_words(slide_spec.get("x_axis_title", ""))
            total_words += self.count_words(slide_spec.get("y_axis_title", ""))

        elif c_shape in ("capability_maturity_staircase", "staircase"):
            for st in slide_spec.get("steps", []):
                total_words += self.count_words(st.get("level_name", "")) + self.count_words(st.get("role_title", ""))
                for c in st.get("competencies", []):
                    total_words += self.count_words(c)
                total_words += self.count_words(st.get("gate_criterion", ""))
            total_words += self.count_words(slide_spec.get("caveat_text", ""))

        elif c_shape == "annotated_chart":
            total_words += self.count_words(slide_spec.get("chart_title", ""))
            total_words += self.count_words(slide_spec.get("key_takeaway", ""))
            total_words += self.count_words(slide_spec.get("callout_annotation", ""))
            total_words += self.count_words(slide_spec.get("source_id", ""))

        elif c_shape in ("career_trajectory_roadmap", "roles_and_enablement"):
            for r in slide_spec.get("roles", []):
                for item in r:
                    total_words += self.count_words(item)
            for c in slide_spec.get("certifications", []):
                for item in c:
                    total_words += self.count_words(item)
            for p in slide_spec.get("action_plan", []):
                for item in p:
                    total_words += self.count_words(item)
            total_words += self.count_words(slide_spec.get("caveat_text", ""))

        elif c_shape in ("metadata_vs_context", "metadata_comparison"):
            for lbl, desc in slide_spec.get("metadata_items", []):
                total_words += self.count_words(lbl) + self.count_words(desc)
            for lbl, desc in slide_spec.get("context_items", []):
                total_words += self.count_words(lbl) + self.count_words(desc)
            ex = slide_spec.get("example_box", {})
            total_words += self.count_words(ex.get("title", "")) + self.count_words(ex.get("metadata_text", "")) + self.count_words(ex.get("context_text", ""))

        elif c_shape == "closing":
            total_words += self.count_words(slide_spec.get("core_message", ""))
            total_words += self.count_words(slide_spec.get("concluding_statement", ""))
            for p_name, p_desc in slide_spec.get("pillars", []):
                total_words += self.count_words(p_name) + self.count_words(p_desc)
            total_words += self.count_words(slide_spec.get("pill_text", ""))

        # Budget Check
        budget_limit = self.WORD_BUDGET_COVER if c_shape in ("cover", "closing") else (self.WORD_BUDGET_DENSE_SLIDE if c_shape == "roles_and_terms" else self.WORD_BUDGET_SLIDE_HARD)
        if c_shape not in ("cover", "closing") and total_words > budget_limit:
            violations.append(f"Slide {s_num} exceeded word limit: {total_words} words (cap is {budget_limit})")

        return (len(violations) == 0, total_words, violations)
