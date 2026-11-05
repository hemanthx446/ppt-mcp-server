import os
import json
from pipeline.renderer import DeckRenderer
from pipeline.qa import QualityGate
from pipeline.distill import ContentDistiller
from pipeline.visual_plan import VisualPlanner
from pipeline.panel_review import PanelReviewEngine
from build_test_a_datasphere import build_test_a_spec

if __name__ == "__main__":
    spec = build_test_a_spec()

    # Targets in root directory
    out_pptx = os.path.abspath("SAP_Datasphere_Career_Path.pptx")
    out_pptx_guide = os.path.abspath("SAP_Datasphere_Career_Path_Guide.pptx")
    preview_dir = os.path.abspath("previews_datasphere")
    os.makedirs(preview_dir, exist_ok=True)

    # 1. Audit content & word budgets
    distiller = ContentDistiller()
    total_words = 0
    for s in spec["slides"]:
        valid, w, viols = distiller.audit_slide_content(s)
        total_words += w
        print(f"Slide {s['slide_number']} ({s['content_shape']}): {w} words. Valid: {valid}")
        if viols:
            print("  Violations:", viols)
    print(f"Total Words: {total_words}, Avg words/slide: {total_words / len(spec['slides']):.1f}")

    # 2. Audit visual layout diversity
    valid_layouts, l_viols = VisualPlanner.validate_layout_rules(spec["slides"])
    print(f"Layout diversity valid: {valid_layouts}, violations: {l_viols}")

    # 3. Render presentation
    renderer = DeckRenderer(theme_name="lumbini")
    rendered_file = renderer.render(spec, out_pptx)
    print(f"Rendered presentation: {rendered_file}")

    # 4. Automated Pre-Flight QA Audit with COM 1080p image export
    qa_report = QualityGate.audit_deck(rendered_file, spec, render_images=True, preview_dir=preview_dir)
    qa_json_path = os.path.abspath("qa_datasphere_report.json")
    with open(qa_json_path, "w", encoding="utf-8") as f:
        json.dump(qa_report, f, indent=2)
    print(f"QA Status: {qa_report['status']}, Blocking: {qa_report['blocking_count']}, Warnings: {qa_report['warning_count']}")
    print(f"Anti-Copy Audit: {qa_report['anti_copy_audit']}")

    # 5. Strategic Panel Review
    panel_results = PanelReviewEngine.review_deck(rendered_file, storyline=spec, output_report_path=os.path.abspath("panel_review_datasphere.md"))
    print(f"Panel Review Gate: {panel_results['panel_gate_status']}, Mean Score: {panel_results['mean_score']}/5.0")
