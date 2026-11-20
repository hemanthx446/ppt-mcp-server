import os
from typing import Dict, Any, Optional
from pptx import Presentation

from design_system.lumbini.tokens import get_lumbini_theme, LumbiniTheme
from design_system.lumbini.primitives import LumbiniPrimitives
from design_system.lumbini.theme_patcher import apply_lumbini_theme_to_pptx

class DeckRenderer:
    """
    Stage 5: PowerPoint Engineer Rendering Engine
    Renders presentation slides natively using slide masters and vector primitives.
    Enforces Level B content-free atom parameters and parameterised footers.
    """

    def __init__(self, theme_name: str = "lumbini"):
        self.theme = get_lumbini_theme()
        self.primitives = LumbiniPrimitives(self.theme)
        self.template_path = os.path.join(os.path.dirname(__file__), "..", "themes", theme_name, "template.pptx")
        self.template_path = os.path.abspath(self.template_path)

    def render(self, deck_spec: Dict[str, Any], output_path: str) -> str:
        output_path = os.path.abspath(output_path)
        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        if os.path.exists(self.template_path):
            prs = Presentation(self.template_path)
        else:
            prs = Presentation()
            prs.slide_width = self.theme.IN_WIDTH
            prs.slide_height = self.theme.IN_HEIGHT

        cover_layout = prs.slide_layouts[2] if len(prs.slide_layouts) > 2 else prs.slide_layouts[0]
        content_layout = prs.slide_layouts[1] if len(prs.slide_layouts) > 1 else prs.slide_layouts[0]

        meta = deck_spec.get("meta", {})
        if not meta and "client" in deck_spec:
            meta = {
                "client": deck_spec.get("client"),
                "confidentiality": deck_spec.get("confidentiality", "Confidential"),
                "doc_type": deck_spec.get("doc_type", "Executive Briefing")
            }

        slides_data = deck_spec.get("slides", [])
        total_slides = len(slides_data)

        for idx, s_spec in enumerate(slides_data, 1):
            c_shape = s_spec.get("content_shape", "content")
            title = s_spec.get("title", "")
            subtitle = s_spec.get("subtitle")
            eyebrow = s_spec.get("eyebrow", "")
            notes = s_spec.get("notes", "")

            if c_shape == "cover":
                slide = prs.slides.add_slide(cover_layout)
                self.primitives.render_cover(
                    slide=slide,
                    title=title,
                    subtitle=subtitle or "",
                    metadata_rows=s_spec.get("metadata", []),
                    pill_text=s_spec.get("pill_text"),
                    dark_theme=s_spec.get("dark_theme", False)
                )
            elif c_shape == "closing":
                slide = prs.slides.add_slide(cover_layout)
                self.primitives.render_closing(
                    slide=slide,
                    title=title,
                    subtitle=subtitle or "",
                    core_message=s_spec.get("core_message", ""),
                    pillars=s_spec.get("pillars", []),
                    concluding_statement=s_spec.get("concluding_statement", ""),
                    pill_text=s_spec.get("pill_text")
                )
            else:
                slide = prs.slides.add_slide(content_layout)
                self.primitives.add_title_block(
                    slide=slide,
                    eyebrow_text=eyebrow,
                    title_text=title,
                    subtitle_text=subtitle
                )

                # Locator if configured
                locator_level = s_spec.get("locator_level")
                platform_levels = meta.get("platform_levels")
                if locator_level and platform_levels:
                    self.primitives.add_locator(
                        slide=slide,
                        x=10.6, y=0.48, w=2.08, h=0.28,
                        current_level=locator_level,
                        levels=platform_levels
                    )

                # Render content based on relationship-first visual grammar
                if c_shape == "requirement_to_outcome":
                    self.primitives.render_requirement_to_outcome(
                        slide=slide,
                        items=s_spec.get("items", []),
                        headers=s_spec.get("headers")
                    )

                elif c_shape == "hub_and_spokes":
                    self.primitives.render_hub_and_spokes(
                        slide=slide,
                        hub_title=s_spec.get("hub_title", "Enterprise Core"),
                        hub_subtitle=s_spec.get("hub_subtitle", "Platform Anchor"),
                        spokes=s_spec.get("spokes", [])
                    )

                elif c_shape == "dashboard_concept":
                    self.primitives.render_dashboard_concept(
                        slide=slide,
                        flow_steps=s_spec.get("flow_steps", []),
                        tabs=s_spec.get("tabs", []),
                        kpis=s_spec.get("kpis", []),
                        column_chart_labels=s_spec.get("column_chart_labels", []),
                        column_chart_values=s_spec.get("column_chart_values", []),
                        line_chart_categories=s_spec.get("line_chart_categories", []),
                        line_actual=s_spec.get("line_actual", []),
                        line_plan=s_spec.get("line_plan", []),
                        drill_steps=s_spec.get("drill_steps", []),
                        platform_note=s_spec.get("platform_note", ""),
                        platform_title=s_spec.get("platform_title"),
                        platform_disclaimer=s_spec.get("platform_disclaimer"),
                        chart1_title=s_spec.get("chart1_title"),
                        chart2_title=s_spec.get("chart2_title"),
                        drill_title=s_spec.get("drill_title")
                    )

                elif c_shape == "levels_x_dimensions":
                    self.primitives.render_matrix_grid(
                        slide=slide,
                        col_headers=s_spec.get("col_headers", []),
                        row_headers=s_spec.get("row_headers", []),
                        matrix_cells=s_spec.get("cells", []),
                        caveat_text=s_spec.get("caveat_text", ""),
                        confirmed_caps=s_spec.get("confirmed_caps", []),
                        confirmed_title=s_spec.get("confirmed_title")
                    )

                elif c_shape in ("process_linear", "step_line"):
                    variant = s_spec.get("variant", "stepline")
                    if variant == "blocks" and c_shape != "step_line":
                        self.primitives.render_numbered_blocks(
                            slide=slide,
                            steps=s_spec.get("steps", []),
                            caveat_text=s_spec.get("caveat_text", ""),
                            deliverables=s_spec.get("deliverables", [])
                        )
                    else:
                        self.primitives.render_step_line(
                            slide=slide,
                            steps=s_spec.get("steps", []),
                            deliverables=s_spec.get("deliverables", []),
                            caveat_text=s_spec.get("caveat_text", "")
                        )

                elif c_shape == "flow_with_actions":
                    self.primitives.render_flow_with_actions(
                        slide=slide,
                        flow_boxes=s_spec.get("flow_boxes", []),
                        actions=s_spec.get("actions", []),
                        legend_items=s_spec.get("legend_items", []),
                        caveat_text=s_spec.get("caveat_text", "")
                    )

                elif c_shape == "phases_over_time":
                    self.primitives.render_roadmap_rows(
                        slide=slide,
                        phases=s_spec.get("phases", []),
                        future_readiness_title=s_spec.get("future_readiness_title", "Continuous Innovation"),
                        future_readiness_desc=s_spec.get("future_readiness_desc", "")
                    )

                elif c_shape == "phase_wise_delivery_plan":
                    self.primitives.render_phase_wise_delivery_table(
                        slide=slide,
                        left=s_spec.get("left", 0.65),
                        top=s_spec.get("top", 1.76),
                        width=s_spec.get("width", 7.80),
                        height=s_spec.get("height", 5.04),
                        header_title=s_spec.get("header_title", "PHASE WISE DELIVERY PLAN"),
                        phases=s_spec.get("phases", None),
                        col_widths=s_spec.get("col_widths", None),
                        border_hex=s_spec.get("border_hex", "0070C0")
                    )

                elif c_shape == "roles_and_terms":
                    self.primitives.render_roles_and_terms(
                        slide=slide,
                        commercial_rows=s_spec.get("commercial_rows", []),
                        resource_rows=s_spec.get("resource_rows", []),
                        terms_list=s_spec.get("terms_list", []),
                        sec_a_title=s_spec.get("sec_a_title", "A   Commercial proposal"),
                        sec_b_title=s_spec.get("sec_b_title", "B   Proposed manpower resources"),
                        sec_c_title=s_spec.get("sec_c_title", "C   Terms & conditions"),
                        table_a_headers=s_spec.get("table_a_headers"),
                        table_b_headers=s_spec.get("table_b_headers")
                    )

                elif c_shape == "benchmark_table":
                    self.primitives.render_benchmark_table(
                        slide=slide,
                        headers=s_spec.get("headers", []),
                        rows=s_spec.get("rows", []),
                        col_widths=s_spec.get("col_widths"),
                        callout_text=s_spec.get("callout_text")
                    )

                # --- NEW V2 VISUAL GRAMMARS ---
                elif c_shape in ("layered_stack", "platform_stack"):
                    self.primitives.render_layered_stack(
                        slide=slide,
                        layers=s_spec.get("layers", []),
                        callout_note=s_spec.get("callout_note")
                    )

                elif c_shape in ("iceberg_shift", "before_after_shift"):
                    self.primitives.render_iceberg_shift(
                        slide=slide,
                        visible_event=s_spec.get("visible_event", {}),
                        submerged_layers=s_spec.get("submerged_layers", []),
                        callout_text=s_spec.get("callout_text", "")
                    )

                elif c_shape == "constraint_flow":
                    self.primitives.render_constraint_flow(
                        slide=slide,
                        stages=s_spec.get("stages", []),
                        constraint_idx=s_spec.get("constraint_idx", 0),
                        buffer_desc=s_spec.get("buffer_desc", ""),
                        impact_annotation=s_spec.get("impact_annotation", "")
                    )

                elif c_shape == "causal_loop":
                    self.primitives.render_causal_loop(
                        slide=slide,
                        nodes=s_spec.get("nodes", []),
                        loops=s_spec.get("loops", []),
                        delay_annotation=s_spec.get("delay_annotation", "")
                    )

                elif c_shape == "tradeoff_matrix":
                    self.primitives.render_tradeoff_matrix(
                        slide=slide,
                        x_axis_title=s_spec.get("x_axis_title", ""),
                        y_axis_title=s_spec.get("y_axis_title", ""),
                        quadrants=s_spec.get("quadrants", []),
                        callout_note=s_spec.get("callout_note", "")
                    )

                elif c_shape in ("capability_maturity_staircase", "staircase"):
                    self.primitives.render_capability_maturity_staircase(
                        slide=slide,
                        steps=s_spec.get("steps", []),
                        caveat_text=s_spec.get("caveat_text", "")
                    )

                elif c_shape == "annotated_chart":
                    self.primitives.render_annotated_chart(
                        slide=slide,
                        chart_type=s_spec.get("chart_type", "column"),
                        categories=s_spec.get("categories", []),
                        series_data=s_spec.get("series_data", []),
                        title=s_spec.get("chart_title", ""),
                        x_label=s_spec.get("x_label", ""),
                        y_label=s_spec.get("y_label", ""),
                        callout_annotation=s_spec.get("callout_annotation", ""),
                        key_takeaway=s_spec.get("key_takeaway", ""),
                        source_id=s_spec.get("source_id")
                    )

                elif c_shape in ("career_trajectory_roadmap", "roles_and_enablement"):
                    self.primitives.render_career_trajectory_roadmap(
                        slide=slide,
                        roles=s_spec.get("roles", []),
                        certifications=s_spec.get("certifications", []),
                        action_plan=s_spec.get("action_plan", []),
                        caveat_text=s_spec.get("caveat_text", "")
                    )

                elif c_shape in ("metadata_vs_context", "metadata_comparison"):
                    self.primitives.render_metadata_vs_context(
                        slide=slide,
                        metadata_items=s_spec.get("metadata_items", []),
                        context_items=s_spec.get("context_items", []),
                        example_box=s_spec.get("example_box", {})
                    )

                # Parameterised footer on every content slide
                self.primitives.render_footer(
                    slide=slide,
                    meta=meta,
                    slide_num=idx,
                    total_slides=total_slides
                )

            # Remove any unpopulated empty placeholders to guarantee zero "Click to add title/text" prompts
            sp_tree = slide.shapes._spTree
            for ph in list(slide.placeholders):
                if ph.has_text_frame and not ph.text.strip():
                    sp_tree.remove(ph._element)

            # Speaker Notes
            if notes and hasattr(slide, "notes_slide"):
                slide.notes_slide.notes_text_frame.text = notes

        # Dynamic Section Management (UPDATE v3 §2)
        # Rules: Decks < 8 slides get 0 sections; >= 8 slides get 2-5 contiguous acts covering all slides
        from tools.sections import plan_ok, write_sections, remove_sections
        sections_data = deck_spec.get("sections", [])
        if len(slides_data) < 8:
            remove_sections(prs)
        elif sections_data:
            normalized_acts = []
            for item in sections_data:
                if isinstance(item, (tuple, list)) and len(item) == 2:
                    normalized_acts.append((str(item[0]), int(item[1])))
                elif isinstance(item, dict):
                    name = item.get("name", "")
                    if "count" in item:
                        cnt = int(item["count"])
                    elif "slides" in item:
                        cnt = len(item["slides"])
                    else:
                        cnt = 0
                    normalized_acts.append((name, cnt))

            ok, reason = plan_ok(len(slides_data), normalized_acts)
            if ok:
                write_sections(prs, normalized_acts)
            else:
                remove_sections(prs)
        else:
            remove_sections(prs)

        prs.save(output_path)
        apply_lumbini_theme_to_pptx(output_path)
        return output_path
