import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ops_model import (
    build_scaling_plan,
    build_decision_rights_matrix,
    build_compliance_calendar,
    build_summary,
    validate_org,
    DECISIONS,
    humanize_dept,
)

BASE_ORG = {
    "organization": "Test Org",
    "current_headcount": {"operations": 8, "donor_advising": 9, "ai_grantmaking": 10, "nuclear_grantmaking": 8},
    "target_multiplier": 2.0,
    "timeline_months": 18,
    "functional_leads": ["People Operations", "Business Operations", "Finance", "Talent", "Grants Management"],
    "jurisdictions": [{"name": "US", "entity_type": "501(c)(3)"}, {"name": "UK", "entity_type": "UK registered charity"}],
}


def test_scaling_plan_hits_target_headcount():
    current = {"operations": 8, "donor_advising": 9, "ai_grantmaking": 10, "nuclear_grantmaking": 8}
    plan = build_scaling_plan(current, target_multiplier=2.0, timeline_months=18)
    assert "Net new hires: **35**" in plan
    assert "Target headcount:" in plan


def test_scaling_plan_front_loads_management():
    current = {"ops": 10}
    plan = build_scaling_plan(current, target_multiplier=2.0, timeline_months=12)
    assert "Foundational leadership" in plan


def test_scaling_plan_differentiates_manager_and_ic_cost():
    current = {"ops": 10}
    # Manager-heavy Phase 1 (mgr_ratio 0.60) vs IC-heavy Phase 3 (mgr_ratio 0.15) should NOT
    # cost the same per hire once manager/IC costs are differentiated.
    plan = build_scaling_plan(current, target_multiplier=2.0, timeline_months=12,
                               avg_fully_loaded_cost_per_fte=150000, avg_fully_loaded_cost_manager=200000)
    assert "per IC and" in plan and "per manager/lead hire" in plan
    rows = [line for line in plan.splitlines() if line.startswith("| Q")]
    costs = [int(r.split("|")[-2].strip().replace("$", "").replace(",", "")) for r in rows]
    hires = [int(r.split("|")[2].strip()) for r in rows]
    cost_per_hire = [c / h for c, h in zip(costs, hires)]
    # Phase 1 (more managers) should cost more per hire than Phase 3 (fewer managers)
    assert cost_per_hire[0] > cost_per_hire[-1]

    plan_default_multiplier = build_scaling_plan(current, target_multiplier=2.0, timeline_months=12,
                                                 avg_fully_loaded_cost_per_fte=150000)
    assert "$195,000 per manager/lead hire" in plan_default_multiplier  # 150000 * 1.3 default


def test_scaling_plan_rounding_drift_preserves_total():
    current = {"ops": 7}
    plan = build_scaling_plan(current, target_multiplier=2.0, timeline_months=12)
    hires = []
    for line in plan.splitlines():
        if line.startswith("| Q"):
            cols = [c.strip() for c in line.strip("|").split("|")]
            hires.append(int(cols[1]))
    assert sum(hires) == 7


def test_decision_matrix_covers_all_decisions_and_resolves_named_leads():
    leads = ["People Operations", "Finance", "Talent", "Business Operations", "Grants Management"]
    matrix = build_decision_rights_matrix(leads)
    for d in DECISIONS:
        assert d["decision"] in matrix
    assert "Grants Management" in matrix
    assert "not in provided functional_leads list" not in matrix


def test_decision_matrix_flags_unresolved_lead():
    matrix = build_decision_rights_matrix(["Finance"])
    assert "not in provided functional_leads list" in matrix


def test_decision_matrix_includes_grant_approval_tiers_and_threshold_note():
    matrix = build_decision_rights_matrix(BASE_ORG["functional_leads"], budget_threshold=50000)
    assert "Individual grant approval (at or below the delegation threshold)" in matrix
    assert "Individual grant approval (above the delegation threshold)" in matrix
    assert "$50,000" in matrix
    matrix_no_threshold = build_decision_rights_matrix(BASE_ORG["functional_leads"])
    assert "Delegation threshold" not in matrix_no_threshold


def test_compliance_calendar_covers_all_jurisdictions_with_specific_deadlines():
    jurisdictions = [{"name": "US", "entity_type": "501(c)(3)"}, {"name": "UK", "entity_type": "UK registered charity"}]
    calendar = build_compliance_calendar(jurisdictions)
    assert "## US" in calendar and "## UK" in calendar
    assert "Form 990" in calendar
    assert "Charity Commission" in calendar
    assert "due-diligence" in calendar.lower()


def test_compliance_calendar_distinguishes_sector_specific_screening():
    calendar = build_compliance_calendar(BASE_ORG["jurisdictions"])
    assert "infohazard" in calendar.lower()
    assert "ITAR" in calendar or "EAR" in calendar
    assert "OFAC" in calendar


def test_humanize_dept_handles_acronyms():
    assert humanize_dept("ai_grantmaking") == "AI Grantmaking"
    assert humanize_dept("donor_advising") == "Donor Advising"


def test_validate_org_catches_bad_input():
    assert validate_org(BASE_ORG) == []

    bad = dict(BASE_ORG)
    bad["current_headcount"] = {"operations": -3}
    errors = validate_org(bad)
    assert any("non-negative" in e for e in errors)

    missing = {"organization": "X"}
    errors = validate_org(missing)
    assert len(errors) == 5  # the other five required fields


def test_build_summary_includes_lineage_and_taxonomy_map():
    summary = build_summary(BASE_ORG, "sample_org.yaml")
    assert summary["source_file"] == "sample_org.yaml"
    assert summary["net_new_hires"] == 35
    assert "generated_at" in summary
    assert summary["department_functional_lead_map"] == {}


if __name__ == "__main__":
    test_scaling_plan_hits_target_headcount()
    test_scaling_plan_front_loads_management()
    test_scaling_plan_differentiates_manager_and_ic_cost()
    test_scaling_plan_rounding_drift_preserves_total()
    test_decision_matrix_covers_all_decisions_and_resolves_named_leads()
    test_decision_matrix_flags_unresolved_lead()
    test_decision_matrix_includes_grant_approval_tiers_and_threshold_note()
    test_compliance_calendar_covers_all_jurisdictions_with_specific_deadlines()
    test_compliance_calendar_distinguishes_sector_specific_screening()
    test_humanize_dept_handles_acronyms()
    test_validate_org_catches_bad_input()
    test_build_summary_includes_lineage_and_taxonomy_map()
    print("All tests passed.")
