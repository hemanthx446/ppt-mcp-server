import sys
sys.path.insert(0, ".")
from design_system.norman_ux import validate_deck

report = validate_deck("JBVNL_Transformation_Decision_Playbook.pptx")
print("=== JBVNL DECISION PLAYBOOK NORMAN UX REPORT ===")
print("Overall Status:", report["status"])
print("Score:", f"{report['norman_ux_score']} / 100")
print("Fails:", report["violations_count"]["fails"])
print("Warnings:", report["violations_count"]["warnings"])
if report["violations"]:
    for v in report["violations"]:
        print(f" - [{v['severity'].upper()}] Slide {v['slide_index']} {v['rule']}: {v['detail']}")
else:
    print("100% CLEAN: Zero violations!")
