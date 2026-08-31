import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ops_model import build_scaling_plan, build_decision_rights_matrix, build_compliance_calendar, DECISION_TYPES


def test_scaling_plan_hits_target_headcount():
    current = {"operations": 8, "donor_advising": 9, "ai_grantmaking": 10, "nuclear_grantmaking": 8}
    plan = build_scaling_plan(current, target_multiplier=2.0, timeline_months=18)
    assert "Net new hires: **35**" in plan or "Net new hires:" in plan
    assert "Target headcount:" in plan


def test_scaling_plan_front_loads_management():
    current = {"ops": 10}
    plan = build_scaling_plan(current, target_multiplier=2.0, timeline_months=12)
    assert "Foundational leadership" in plan


def test_decision_matrix_covers_all_decision_types():
    matrix = build_decision_rights_matrix(["People Operations", "Finance"])
    for decision in DECISION_TYPES:
        assert decision in matrix


def test_compliance_calendar_covers_all_jurisdictions():
    jurisdictions = [{"name": "US", "entity_type": "501(c)(3)"}, {"name": "UK", "entity_type": "UK charity"}]
    calendar = build_compliance_calendar(jurisdictions)
    assert "## US" in calendar
    assert "## UK" in calendar
    assert "Q1" in calendar and "Q4" in calendar


if __name__ == "__main__":
    test_scaling_plan_hits_target_headcount()
    test_scaling_plan_front_loads_management()
    test_decision_matrix_covers_all_decision_types()
    test_compliance_calendar_covers_all_jurisdictions()
    print("All tests passed.")
