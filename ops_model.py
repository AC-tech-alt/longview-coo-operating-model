#!/usr/bin/env python3
"""
ops_model.py — a small toolkit for turning a description of a growing
organization into three artifacts a new COO would want ready in week one:

  1. A phased hiring plan (with an illustrative budget view) that sequences
     leadership/manager hires ahead of individual-contributor hires, so the
     org doesn't outgrow its own management capacity while doubling headcount.
  2. A RACI decision-rights matrix with named ownership per decision —
     including two decisions specific to a catastrophic-risk grantmaker.
  3. A jurisdiction-specific compliance-review cadence, plus a standing
     grantee/partner due-diligence item relevant to AI-safety and
     nuclear-policy grantmaking.

Built as a working demonstration for the Longview Philanthropy COO role
(https://www.longview.org/careers/chief-operating-officer/) by Ariel Carter.
This is a planning framework, not legal or financial advice — jurisdiction-
specific compliance detail and real comp figures should always be confirmed
with counsel/finance, not taken from this repo.
"""

import sys
import math
import json
import yaml
from pathlib import Path
from datetime import date

OUTPUT_DIR = Path("output")

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

_ACRONYMS = {"ai", "us", "uk", "hr", "it", "pr"}


def humanize_dept(name: str) -> str:
    """Turn 'ai_grantmaking' into 'AI Grantmaking' without brittle string surgery."""
    words = name.replace("-", " ").replace("_", " ").split()
    return " ".join(w.upper() if w.lower() in _ACRONYMS else w.capitalize() for w in words)


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


def build_scaling_plan(current_headcount: dict, target_multiplier: float, timeline_months: int,
                        avg_fully_loaded_cost_per_fte: float = None,
                        avg_fully_loaded_cost_manager: float = None) -> str:
    total_current = sum(current_headcount.values())
    total_target = math.ceil(total_current * target_multiplier)
    net_new = total_target - total_current

    lines = [
        "# Phased Hiring Plan\n",
        f"Current headcount: **{total_current}** across {len(current_headcount)} departments.",
        f"Target headcount: **{total_target}** ({target_multiplier}x) within **{timeline_months} months**.",
        f"Net new hires: **{net_new}**.\n",
    ]

    # Compute each phase's numbers as data first, then render — not string
    # surgery on a finished table — so the rounding-drift fix below can't
    # silently corrupt an unrelated column.
    phases = []
    running_total = 0
    for phase in PHASE_MIX:
        hires = round(net_new * phase["share"])
        running_total += hires
        phases.append({"label": phase["label"], "hires": hires, "mgr_ratio": phase["mgr_ratio"], "drift": 0})

    drift = net_new - running_total
    if drift != 0 and phases:
        phases[-1]["hires"] += drift
        phases[-1]["drift"] = drift

    has_cost = avg_fully_loaded_cost_per_fte is not None
    # A manager's fully-loaded cost isn't the same as an IC's — treating them as one
    # blended number makes a manager-heavy phase (Phase 1) look exactly as cheap per
    # hire as an IC-heavy phase (Phase 3), which understates early-phase cost. Default
    # the manager premium to 1.3x the IC rate if a real manager figure isn't supplied.
    manager_cost = avg_fully_loaded_cost_manager
    if has_cost and manager_cost is None:
        manager_cost = avg_fully_loaded_cost_per_fte * 1.3

    header = "| Phase | New hires | Manager/lead hires | IC hires |"
    sep = "|---|---|---|---|"
    if has_cost:
        header += " Incremental annualized cost |"
        sep += "---|"
    lines.append(header)
    lines.append(sep)

    running_budget = 0
    for p in phases:
        mgr_hires = round(p["hires"] * p["mgr_ratio"])
        ic_hires = p["hires"] - mgr_hires
        note = f" *(includes {p['drift']:+d} rounding adjustment)*" if p["drift"] else ""
        row = f"| {p['label']}{note} | {p['hires']} | {mgr_hires} | {ic_hires} |"
        if has_cost:
            phase_cost = mgr_hires * manager_cost + ic_hires * avg_fully_loaded_cost_per_fte
            running_budget += phase_cost
            row += f" ${phase_cost:,.0f} |"
        lines.append(row)

    if has_cost:
        lines.append(
            f"\n**Illustrative incremental budget impact: ~${running_budget:,.0f}/year** at a "
            f"fully-loaded cost of ${avg_fully_loaded_cost_per_fte:,.0f} per IC and "
            f"${manager_cost:,.0f} per manager/lead hire — placeholder assumptions, not real "
            "Longview comp bands, differentiated so the budget line doesn't understate "
            "manager-heavy phases. Doesn't include one-time costs (recruiting, relocation, "
            "visa/immigration sponsorship) or currency differences across US/UK hires — see "
            "Scope & limitations."
        )
    else:
        lines.append(
            "\n*No `avg_fully_loaded_cost_per_fte` provided in the org file — budget impact "
            "omitted. Add it (and optionally `avg_fully_loaded_cost_manager`) to see an "
            "illustrative incremental cost view.*"
        )

    lines.append("\n## Departmental distribution (proportional to current size)\n")
    lines.append("| Department | Current | Target | Net new |")
    lines.append("|---|---|---|---|")
    for dept, count in current_headcount.items():
        dept_target = math.ceil(count * target_multiplier)
        lines.append(f"| {humanize_dept(dept)} | {count} | {dept_target} | {dept_target - count} |")

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

# Each entry names a real owner instead of a generic "COO / Lead / CEO" column
# for every row. Roles prefixed "lead:" are resolved against whatever
# functional_leads are actually passed in (so the matrix is wrong loudly,
# not silently, if a role isn't provided). Two decisions — fund allocation
# across program areas, and grantee/partner due-diligence — are specific to
# a catastrophic-risk grantmaker and wouldn't appear in a generic template.
DECISIONS = [
    {
        "decision": "Headcount / new role approval",
        "R": "lead:Talent", "A": "COO", "C": ["lead:People Operations"], "I": ["CEO"],
    },
    {
        "decision": "Budget commitment above department threshold",
        "R": "lead:Finance", "A": "COO", "C": [], "I": ["CEO"],
    },
    {
        "decision": "Vendor & contractor agreements",
        "R": "lead:Business Operations", "A": "COO", "C": ["lead:Finance"], "I": ["CEO"],
    },
    {
        "decision": "Compliance filings & regulatory submissions",
        "R": "COO", "A": "CEO", "C": ["lead:Finance"], "I": ["All functional leads"],
    },
    {
        "decision": "Grant fund allocation across program areas (e.g., Frontier AI Fund vs. Nuclear Weapons Policy Fund)",
        "R": "lead:Grants Management", "A": "CEO", "C": ["COO", "lead:Finance"], "I": ["All functional leads"],
    },
    {
        "decision": "Individual grant approval (at or below the delegation threshold)",
        "R": "lead:Grants Management", "A": "COO", "C": ["lead:Finance"], "I": ["CEO"],
    },
    {
        "decision": "Individual grant approval (above the delegation threshold)",
        "R": "lead:Grants Management", "A": "CEO", "C": ["COO", "lead:Finance", "Outside counsel"], "I": ["All functional leads"],
    },
    {
        "decision": "Grantee & partner due-diligence / conflict-of-interest screening",
        "R": "lead:Grants Management", "A": "COO",
        "C": ["lead:Finance", "Outside counsel", "Technical/subject-matter reviewer (AI or nuclear-policy, as applicable)"],
        "I": ["CEO"],
    },
    {
        "decision": "Org chart / reporting-line changes",
        "R": "lead:People Operations", "A": "COO", "C": ["Affected functional lead"], "I": ["CEO"],
    },
    {
        "decision": "Performance management & PIP decisions",
        "R": "Employee's direct functional lead", "A": "lead:People Operations", "C": ["COO", "Outside counsel"], "I": ["CEO"],
    },
    {
        "decision": "Operations policy changes (org-wide)",
        "R": "lead:Business Operations", "A": "COO", "C": ["All functional leads"], "I": ["CEO"],
    },
]

DECISION_TYPES = [d["decision"] for d in DECISIONS]


def resolve_role(spec: str, functional_leads: list) -> str:
    if spec.startswith("lead:"):
        keyword = spec[5:]
        for lead in functional_leads:
            if keyword.lower() in lead.lower():
                return lead
        return f"{keyword} Lead *(not in provided functional_leads list)*"
    return spec


def build_decision_rights_matrix(functional_leads: list, budget_threshold: float = None) -> str:
    lines = [
        "# Decision-Rights Matrix (RACI)\n",
        "Named ownership by decision type, so it doesn't get renegotiated case by case as the "
        "org scales. Two rows below (fund allocation, grantee due-diligence) exist specifically "
        "because Longview funds catastrophic-risk work, not because every nonprofit needs them.\n",
        "| Decision | Responsible (R) | Accountable (A) | Consulted (C) | Informed (I) |",
        "|---|---|---|---|---|",
    ]
    for d in DECISIONS:
        r = resolve_role(d["R"], functional_leads)
        a = resolve_role(d["A"], functional_leads)
        c = ", ".join(resolve_role(x, functional_leads) for x in d["C"]) or "—"
        i = ", ".join(resolve_role(x, functional_leads) for x in d["I"]) or "—"
        lines.append(f"| {d['decision']} | {r} | {a} | {c} | {i} |")

    lines.append(f"\n**Functional leads covered:** {', '.join(functional_leads)}")
    if budget_threshold is not None:
        lines.append(
            f"\n**Delegation threshold: ${budget_threshold:,.0f}.** Below it, Finance and Grants "
            "Management act inside their own budget/grant authority day to day. At or above it, "
            "COO accountability (and, for grants, CEO accountability) kicks in — an undefined "
            "threshold makes a RACI row decorative rather than something a Finance or Grants lead "
            "can actually operate against."
        )
    lines.append(
        "\n*R = Responsible (does the work) · A = Accountable (owns the outcome — one name only) "
        "· C = Consulted before the decision · I = Informed after. A single generic 'COO / Lead / "
        "CEO' column was deliberately not used across every row — decision rights differ by "
        "function, and a matrix that doesn't reflect that isn't actually usable on day one.*"
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 3. Compliance review cadence
# ---------------------------------------------------------------------------

# Jurisdiction-specific, not a single generic template — this is the
# difference between showing compliance vocabulary and showing compliance
# knowledge.
US_FOCUS = [
    ("Q1", "State charitable solicitation registration renewals",
     "Confirm registration is current in every state where Longview solicits or receives contributions; renew before any lapse forces re-registration from scratch."),
    ("Q2", "IRS Form 990 preparation & filing",
     "File Form 990 (due the 15th day of the 5th month after fiscal year-end — May 15 for a calendar-year filer) or Form 8868 for an automatic 6-month extension."),
    ("Q3", "Grant & expenditure-responsibility compliance audit",
     "Sample-audit expenditure responsibility, anti-bribery/anti-corruption, and grant-agreement compliance across the year's disbursements."),
    ("Q4", "Budget, reserve policy & audit prep",
     "Board-approve next year's budget and reserve policy; prepare supporting schedules for the annual financial-statement audit."),
]

UK_FOCUS = [
    ("Q1", "Gift Aid & PAYE/RTI review",
     "Confirm Gift Aid claims are current; reconcile PAYE/Real Time Information payroll filings for UK-based staff."),
    ("Q2", "Trustees' Annual Report & Accounts",
     "Prepare and file with the Charity Commission — due within 10 months of the financial year-end."),
    ("Q3", "Companies House confirmation statement",
     "File the annual confirmation statement (if operating as a charitable company) and keep the register of persons with significant control current."),
    ("Q4", "Risk register & trustee review",
     "Refresh the charity's risk register with trustees ahead of year-end; confirm safeguarding and financial-controls policies are current."),
]

GENERIC_FOCUS = [
    ("Q1", "Annual filing & registration review",
     "Confirm all annual filings, licenses, and registrations are current for the entity and jurisdiction."),
    ("Q2", "Employment law & policy review",
     "Review employee handbook, contracts, and classification against current jurisdiction requirements."),
    ("Q3", "Grant / expenditure compliance audit",
     "Sample-audit expenditure responsibility, anti-bribery/anti-corruption, and grant-agreement compliance."),
    ("Q4", "Budget, audit prep & risk review",
     "Prepare for annual audit; reassess top operational and regulatory risks for the coming year."),
]


def _focus_for(entity_type: str, name: str) -> list:
    e = entity_type.lower()
    n = name.strip().lower()
    if "501(c)" in entity_type or n == "us":
        return US_FOCUS
    if "uk" in e or n == "uk":
        return UK_FOCUS
    return GENERIC_FOCUS


def build_compliance_calendar(jurisdictions: list) -> str:
    lines = [
        "# Compliance Review Cadence (Framework)\n",
        "*A planning cadence, not a legal filing calendar — actual deadlines, thresholds, and "
        "requirements should always be confirmed with local counsel/accountant before relying on "
        "them.*\n",
    ]
    for j in jurisdictions:
        focus = _focus_for(j["entity_type"], j["name"])
        lines.append(f"## {j['name']} — {j['entity_type']}\n")
        lines.append("| Quarter | Focus area | What it covers |")
        lines.append("|---|---|---|")
        for quarter, area, detail in focus:
            lines.append(f"| {quarter} | {area} | {detail} |")
        lines.append("")

    lines.append("## Ongoing — Grantee & partner due-diligence (all jurisdictions)\n")
    lines.append(
        "Reviewed at least quarterly, not just at filing time, and split into lenses a generic "
        "nonprofit compliance calendar would collapse into one line:\n"
    )
    lines.append(
        "- **Standard due-diligence:** sanctions/watch-list screening (e.g., OFAC's SDN list) and "
        "conflict-of-interest disclosure for all grantees and partners — the baseline any funder "
        "needs, in any jurisdiction.\n"
        "- **Capability/infohazard screening (AI-safety grants specifically):** a proposal can be "
        "safety-motivated and still be capabilities-uplifting if published — research that clarifies "
        "how to make a model more capable can do that even when framed as alignment work. That needs "
        "a technical reviewer in the loop before funding, not just Legal or Finance, and a "
        "responsible-disclosure/publication conversation with the applicant up front rather than "
        "after the fact.\n"
        "- **Export-control and sanctioned-jurisdiction awareness (nuclear-policy grants "
        "specifically):** grantees or collaborators with ties to nuclear-armed states under US "
        "sanctions (e.g., Russia, North Korea, Iran) raise OFAC questions, and anything touching "
        "controlled technical data raises ITAR/EAR-adjacent ones — a narrower, more specialized "
        "screen than standard nonprofit due-diligence, and one Legal alone can miss without "
        "nonproliferation-specific input.\n"
    )
    lines.append(
        "This is a planning flag, not legal or technical guidance — the actual screening workflow, "
        "and who has authority to pause a grant over it, should be built with counsel and the "
        "relevant subject-matter advisors, not assumed from a generic compliance template."
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def validate_org(org: dict) -> list:
    """Return a list of human-readable validation errors (empty = valid).

    Deliberately conservative: catches the kind of malformed input (negative
    headcount, a jurisdiction missing a name) that would otherwise fail
    confusingly deep inside a render function instead of at the door.
    """
    errors = []
    required = ["organization", "current_headcount", "target_multiplier", "timeline_months",
                "functional_leads", "jurisdictions"]
    for k in required:
        if k not in org:
            errors.append(f"missing required field '{k}'")
    if errors:
        return errors  # can't check shape further without the required fields present

    if not isinstance(org["current_headcount"], dict) or not org["current_headcount"]:
        errors.append("'current_headcount' must be a non-empty mapping of department -> count")
    else:
        for dept, count in org["current_headcount"].items():
            if not isinstance(count, (int, float)) or isinstance(count, bool) or count < 0:
                errors.append(f"'current_headcount.{dept}' must be a non-negative number, got {count!r}")

    if not isinstance(org["target_multiplier"], (int, float)) or isinstance(org["target_multiplier"], bool) or org["target_multiplier"] <= 0:
        errors.append("'target_multiplier' must be a positive number")

    if not isinstance(org["timeline_months"], (int, float)) or isinstance(org["timeline_months"], bool) or org["timeline_months"] <= 0:
        errors.append("'timeline_months' must be a positive number")

    if not isinstance(org["functional_leads"], list) or not org["functional_leads"]:
        errors.append("'functional_leads' must be a non-empty list")

    if not isinstance(org["jurisdictions"], list) or not org["jurisdictions"]:
        errors.append("'jurisdictions' must be a non-empty list")
    else:
        for j in org["jurisdictions"]:
            if not isinstance(j, dict) or "name" not in j or "entity_type" not in j:
                errors.append(f"each jurisdiction needs 'name' and 'entity_type', got {j!r}")

    return errors


def build_summary(org: dict, source_file: str) -> dict:
    """A small structured (machine-readable) export alongside the three markdown
    artifacts — a data architect's core complaint about v1 was that markdown was
    the *only* output, with no lineage (what input, generated when) and no
    reconciliation between the two department taxonomies Longview's JD actually
    uses (current_headcount's departments vs. the five named functional_leads)."""
    total_current = sum(org["current_headcount"].values())
    total_target = math.ceil(total_current * org["target_multiplier"])
    return {
        "generated_at": date.today().isoformat(),
        "source_file": source_file,
        "organization": org["organization"],
        "current_headcount_total": total_current,
        "target_headcount_total": total_target,
        "net_new_hires": total_target - total_current,
        "functional_leads": org["functional_leads"],
        "jurisdictions": [j["name"] for j in org["jurisdictions"]],
        "department_functional_lead_map": org.get("department_functional_lead_map", {}),
        "schema_note": (
            "current_headcount's departments and functional_leads are two separate "
            "taxonomies drawn from different parts of Longview's public JD, and they "
            "don't fully reconcile. See department_functional_lead_map for the attempted "
            "mapping — any department mapped to null is a real open question, not a bug, "
            "and should be one of the first things a new COO resolves with the CEO."
        ),
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python ops_model.py <org.yaml>")
        sys.exit(1)

    org_path = Path(sys.argv[1])
    try:
        with open(org_path) as f:
            # safe_load, deliberately — never yaml.load() on a file that could plausibly
            # come from outside this repo. yaml.load() can execute arbitrary Python
            # objects embedded in the YAML; safe_load() restricts parsing to plain data.
            org = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: could not find '{org_path}'.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: '{org_path}' is not valid YAML — {e}")
        sys.exit(1)

    errors = validate_org(org)
    if errors:
        print(f"Error: '{org_path}' failed validation:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(exist_ok=True)

    scaling_plan = build_scaling_plan(
        org["current_headcount"], org["target_multiplier"], org["timeline_months"],
        avg_fully_loaded_cost_per_fte=org.get("avg_fully_loaded_cost_per_fte"),
        avg_fully_loaded_cost_manager=org.get("avg_fully_loaded_cost_manager"),
    )
    (OUTPUT_DIR / "scaling_plan.md").write_text(scaling_plan + "\n")

    raci = build_decision_rights_matrix(org["functional_leads"], budget_threshold=org.get("budget_commitment_threshold"))
    (OUTPUT_DIR / "decision_rights_matrix.md").write_text(raci + "\n")

    calendar = build_compliance_calendar(org["jurisdictions"])
    (OUTPUT_DIR / "compliance_calendar.md").write_text(calendar + "\n")

    summary = build_summary(org, str(org_path))
    (OUTPUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    print(f"Generated for {org['organization']} on {date.today().isoformat()}:")
    print("  output/scaling_plan.md")
    print("  output/decision_rights_matrix.md")
    print("  output/compliance_calendar.md")
    print("  output/summary.json  (structured/machine-readable — lineage + taxonomy map)")


if __name__ == "__main__":
    main()
