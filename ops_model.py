#!/usr/bin/env python3
"""
ops_model.py — a small toolkit for turning a description of a growing
organization into three artifacts a new COO would want ready in week one:

  1. A phased hiring plan that sequences leadership/manager hires ahead of
     individual-contributor hires, so the org doesn't outgrow its own
     management capacity while doubling headcount.
  2. A RACI decision-rights matrix across functional leads.
  3. A compliance-review cadence template across jurisdictions.

Built as a working demonstration for the Longview Philanthropy COO role
(https://www.longview.org/careers/chief-operating-officer/) by Ariel Carter.
This is a planning framework, not legal or financial advice — jurisdiction-
specific compliance detail should always be filled in with counsel.
"""

import sys
import math
import yaml
from pathlib import Path
from datetime import date

OUTPUT_DIR = Path("output")

# ---------------------------------------------------------------------------
# 1. Scaling & hiring plan
# ---------------------------------------------------------------------------

# Rough allocation of each new hire as "leadership/manager" vs "individual
# contributor" per phase. Front-loads management capacity so growth doesn't
# outrun the org's ability to actually manage it — the lesson from managing
# managers through six organizational transformations at Tides.
PHASE_MIX = [
    {"label": "Q1 — Foundational leadership", "share": 0.20, "mgr_ratio": 0.60},
    {"label": "Q2–Q3 — Core team build-out", "share": 0.35, "mgr_ratio": 0.25},
    {"label": "Q4–Q6 — Scale & specialize", "share": 0.45, "mgr_ratio": 0.15},
]


def build_scaling_plan(current_headcount: dict, target_multiplier: float, timeline_months: int) -> str:
    total_current = sum(current_headcount.values())
    total_target = math.ceil(total_current * target_multiplier)
    net_new = total_target - total_current

    lines = [
        "# Phased Hiring Plan\n",
        f"Current headcount: **{total_current}** across {len(current_headcount)} departments.",
        f"Target headcount: **{total_target}** ({target_multiplier}x) within **{timeline_months} months**.",
        f"Net new hires: **{net_new}**.\n",
        "| Phase | New hires | Manager/lead hires | IC hires |",
        "|---|---|---|---|",
    ]

    running_total = 0
    for phase in PHASE_MIX:
        phase_hires = round(net_new * phase["share"])
        running_total += phase_hires
        mgr_hires = round(phase_hires * phase["mgr_ratio"])
        ic_hires = phase_hires - mgr_hires
        lines.append(f"| {phase['label']} | {phase_hires} | {mgr_hires} | {ic_hires} |")

    # correct rounding drift onto the final phase
    drift = net_new - running_total
    if drift != 0 and lines:
        lines[-1] = lines[-1][:-1] + f" *(includes {drift:+d} rounding adjustment)* |"

    lines.append("\n## Departmental distribution (proportional to current size)\n")
    lines.append("| Department | Current | Target | Net new |")
    lines.append("|---|---|---|---|")
    for dept, count in current_headcount.items():
        dept_target = math.ceil(count * target_multiplier)
        lines.append(f"| {dept.replace('_', ' ').title().replace('Ai ', 'AI ')} | {count} | {dept_target} | {dept_target - count} |")

    lines.append(
        "\n*Principle: leadership and manager capacity is front-loaded in Phase 1 so the "
        "org has the management bandwidth to absorb Phases 2–3 without decision-making "
        "bottlenecking at the top — the same problem six organizational transformations at "
        "Tides were built to solve.*"
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 2. Decision-rights (RACI) matrix
# ---------------------------------------------------------------------------

DECISION_TYPES = [
    "Headcount / new role approval",
    "Budget commitment above department threshold",
    "Vendor & contractor agreements",
    "Compliance filings & regulatory submissions",
    "Org chart / reporting-line changes",
    "Performance management & PIP decisions",
    "Operations policy changes (org-wide)",
]


def build_decision_rights_matrix(functional_leads: list) -> str:
    lines = [
        "# Decision-Rights Matrix (RACI)\n",
        "Explicit authority by decision type, so it doesn't get renegotiated case by case "
        "as the org scales.\n",
        "| Decision | COO | Functional Lead | CEO |",
        "|---|---|---|---|",
    ]
    # A simple, defensible default allocation — meant to be tuned per org,
    # not treated as gospel.
    default_raci = {
        "Headcount / new role approval": ("A", "R", "C"),
        "Budget commitment above department threshold": ("A", "C", "I"),
        "Vendor & contractor agreements": ("A", "R", "I"),
        "Compliance filings & regulatory submissions": ("R", "C", "I"),
        "Org chart / reporting-line changes": ("A", "C", "C"),
        "Performance management & PIP decisions": ("C", "R", "I"),
        "Operations policy changes (org-wide)": ("A", "C", "I"),
    }
    for decision in DECISION_TYPES:
        coo, lead, ceo = default_raci.get(decision, ("A", "R", "I"))
        lines.append(f"| {decision} | {coo} | {lead} | {ceo} |")

    lines.append(f"\n**Functional leads covered:** {', '.join(functional_leads)}")
    lines.append(
        "\n*R = Responsible (does the work) · A = Accountable (owns the outcome) · "
        "C = Consulted · I = Informed.*"
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 3. Compliance review cadence
# ---------------------------------------------------------------------------

QUARTERLY_FOCUS = [
    ("Q1", "Annual filing & registration review", "Confirm all annual filings, licenses, and registrations are current for the entity and jurisdiction."),
    ("Q2", "Employment law & policy review", "Review employee handbook, contracts, and classification against current jurisdiction requirements."),
    ("Q3", "Grant / expenditure compliance audit", "Sample-audit expenditure responsibility, anti-bribery/anti-corruption, and grant-agreement compliance."),
    ("Q4", "Budget, audit prep & risk review", "Prepare for annual audit; reassess top operational and regulatory risks for the coming year."),
]


def build_compliance_calendar(jurisdictions: list) -> str:
    lines = [
        "# Compliance Review Cadence (Framework)\n",
        "*This is a planning cadence, not a legal filing calendar — jurisdiction-specific "
        "deadlines and requirements should be confirmed with local counsel and filled in here.*\n",
    ]
    for j in jurisdictions:
        lines.append(f"## {j['name']} — {j['entity_type']}\n")
        lines.append("| Quarter | Focus area | What it covers |")
        lines.append("|---|---|---|")
        for quarter, focus, detail in QUARTERLY_FOCUS:
            lines.append(f"| {quarter} | {focus} | {detail} |")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) != 2:
        print("Usage: python ops_model.py <org.yaml>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        org = yaml.safe_load(f)

    OUTPUT_DIR.mkdir(exist_ok=True)

    scaling_plan = build_scaling_plan(
        org["current_headcount"], org["target_multiplier"], org["timeline_months"]
    )
    (OUTPUT_DIR / "scaling_plan.md").write_text(scaling_plan + "\n")

    raci = build_decision_rights_matrix(org["functional_leads"])
    (OUTPUT_DIR / "decision_rights_matrix.md").write_text(raci + "\n")

    calendar = build_compliance_calendar(org["jurisdictions"])
    (OUTPUT_DIR / "compliance_calendar.md").write_text(calendar + "\n")

    print(f"Generated for {org['organization']} on {date.today().isoformat()}:")
    print("  output/scaling_plan.md")
    print("  output/decision_rights_matrix.md")
    print("  output/compliance_calendar.md")


if __name__ == "__main__":
    main()
