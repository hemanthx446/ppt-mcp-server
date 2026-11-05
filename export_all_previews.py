import os
import json
from pipeline.renderer import DeckRenderer
from pipeline.qa import QualityGate
from build_test_a_datasphere import build_test_a_spec
from build_test_b_manufacturing import build_test_b_spec
from build_test_c_strategy import build_test_c_spec

tasks = [
    {
        "name": "Test A (Datasphere Career Path)",
        "pptx": os.path.abspath("tests/out/test_a_datasphere_v2/SAP_Datasphere_Career_Path_v2.pptx"),
        "out_dir": os.path.abspath("tests/out/test_a_datasphere_v2"),
        "spec_fn": build_test_a_spec
    },
    {
        "name": "Test B (Manufacturing Transformation)",
        "pptx": os.path.abspath("tests/out/test_b_manufacturing_v2/Apex_Manufacturing_Transformation_v2.pptx"),
        "out_dir": os.path.abspath("tests/out/test_b_manufacturing_v2"),
        "spec_fn": build_test_b_spec
    },
    {
        "name": "Test C (Corporate Digital Strategy)",
        "pptx": os.path.abspath("tests/out/test_c_strategy_v2/Meridian_Digital_Strategy_v2.pptx"),
        "out_dir": os.path.abspath("tests/out/test_c_strategy_v2"),
        "spec_fn": build_test_c_spec
    }
]

renderer = DeckRenderer(theme_name="lumbini")

for t in tasks:
    print(f"\n--- Re-rendering, Exporting Previews and Auditing: {t['name']} ---")
    spec = t["spec_fn"]()
    renderer.render(spec, t["pptx"])
    preview_dir = os.path.join(t["out_dir"], "previews")
    qa_report = QualityGate.audit_deck(t["pptx"], spec, render_images=True, preview_dir=preview_dir)
    qa_json_path = os.path.join(t["out_dir"], "qa-report.json")
    with open(qa_json_path, "w", encoding="utf-8") as f:
        json.dump(qa_report, f, indent=2)
    print(f"QA Status: {qa_report['status']}, Blocking: {qa_report['blocking_count']}, Warnings: {qa_report['warning_count']}")
    print(f"Anti-Copy Audit: {qa_report['anti_copy_audit']}")
