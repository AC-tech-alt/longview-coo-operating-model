# Longview Philanthropy — COO Operating Model

A working demonstration of how I would approach the Chief Operating Officer role, built directly against Longview's public job description.

**Ariel Carter** — [arielebright@gmail.com](mailto:arielebright@gmail.com) · [linkedin.com/in/ariel-carter1](https://www.linkedin.com/in/ariel-carter1) · [github.com/AC-tech-alt](https://github.com/AC-tech-alt)

## At a Glance

- **What this is:** a small, working toolkit (`ops_model.py`) that turns a description of Longview's org into three artifacts an incoming COO would want ready in week one — a phased, budget-aware hiring plan; a decision-rights matrix with named ownership; and a jurisdiction-specific compliance cadence — plus a structured `summary.json` export.
- **Why it's built this way:** every input is sourced from Longview's own public materials, not a generic operational template or invented data.
- **What it doesn't do:** solve the two real experience gaps named in Pillar 4, or substitute for legal or financial advice. Both are named plainly rather than smoothed over.
- **How to confirm it's real, not just markdown:** clone it, `pip install -r requirements.txt`, run `python ops_model.py sample_org.yaml`, and all four output files regenerate from scratch. `python tests/test_ops_model.py` runs the test suite.

## Why This Exists

Longview's COO posting asks for a leader who can build simple, robust systems for planning and decision-making that scale, and run operations as a service to the rest of Longview. While a cover letter can describe that instinct, this repository aims to demonstrate it. It contains a lightweight operational toolkit that turns an organizational footprint — headcount, departments, jurisdictions — into three core artifacts an incoming COO would want ready in week one:

1. **A Phased Hiring Plan** with a tiered budget view.
2. **A Decision-Rights Matrix** with clear, named ownership.
3. **A Jurisdiction-Specific Compliance Cadence.**

This repository is intentionally clean, readable, and focused — a functional blueprint rather than a finished product.

## Grounded in Longview's Mission & Priorities

Built using Longview's public materials rather than a generic operational template:

- **Mission & Theory of Change** ([longview.org](https://www.longview.org/)): Longview directs philanthropic capital toward catastrophic risks — including nuclear war between great powers, engineered pandemics, and AI misuse — under the premise that *"strategic generosity can... alter the course of history."* Capital flows through vehicles like the Frontier AI Fund and Nuclear Weapons Policy Fund. When capital and risk are both this consequential, operational rigor is not overhead — it is core to the mission.
- **Scale & Growth Trajectory:** Longview grew from roughly 24 to 35+ staff through 2026 while more than doubling annual grantmaking to >$60M. The COO posting calls for that same trajectory to repeat, doubling headcount toward ~70. Both `sample_org.yaml` and the phase-mix logic in `ops_model.py` are modeled specifically around this growth profile.
- **Culture & Working Style:** a Longview team member's public [EA Forum post](https://forum.effectivealtruism.org/posts/aX8xLjCLd4LMDpTYL/) describes a self-directed operating style where career growth comes through *"tackling progressively harder, important problems"* rather than a predetermined ladder — across a distributed team spanning eight time zones and four hubs (Berkeley, DC, NYC, London).

## Mapping to the Five Operational Pillars

### 1. Scaling & Growth Strategy

> "Design and execute the operations and hiring strategy to double Longview's headcount."

**Track Record:** I joined GlobalGiving at roughly 20 employees and helped architect the grant management infrastructure that supported its growth to 100+ team members. At Tides, I built, coached, and developed a 15-person team (including two direct-report managers), establishing management capacity across organizational layers during rapid portfolio scaling.

**Application in Model:** `build_scaling_plan()` shows the mechanics I would bring to Longview:

- **Sequenced hiring:** leadership and manager roles are placed ahead of individual-contributor (IC) roles so organizational management capacity stays ahead of growth, not behind it.
- **Tiered budgeting:** manager and IC roles are priced differently across quarterly phases. A flat blended rate would make a manager-heavy phase (Phase 1) look artificially cheap next to an IC-heavy phase (Phase 3). At an illustrative ~$6.1M/year, this budget view offers a pragmatic sanity-check against Longview's >$60M grantmaking scale — the kind of fiscal-governance check a COO should bring to a leadership meeting, not just a headcount chart.

### 2. Regulatory & Compliance

> "Stay on top of regulatory requirements across the jurisdictions we operate in."

**Track Record:** At Tides, I partnered with Legal and Compliance to design and execute a large-scale, multi-area compliance audit covering expenditure responsibility, anti-bribery/anti-corruption, and IRS and global regulatory frameworks. That work systematically fortified our systems — closing the large majority of priority findings within months and substantially completing the full scope within about a year. (Kept at that level of generality rather than exact figures here, since this is a former employer's internal audit, not something to detail on a public page.)

**Application in Model:** I have not personally managed UK-entity compliance, but the discipline transfers, and it has to — Longview operates US and UK entities across four hubs:

- **Jurisdictional precision:** `build_compliance_calendar()` builds distinct cadences for US entities (Form 990, state solicitation registrations) versus UK entities (Charity Commission Annual Return, Companies House filings) rather than one generic template.
- **Specialized due diligence:** the model splits grantee/partner due diligence into three lenses instead of one:
  1. **Standard** — sanctions and conflict-of-interest screening.
  2. **AI safety** — capability and infohazard screening, so a safety-motivated proposal doesn't inadvertently uplift dangerous capability without technical review.
  3. **Nuclear policy** — export-control and sanctioned-jurisdiction awareness (OFAC, ITAR/EAR-adjacent considerations).
- **Operational RACI:** technical reviewers are named as *Consulted* alongside Legal, and day-to-day grant approval is explicitly separated from board/CEO-level fund allocation across program areas (e.g., Frontier AI Fund vs. Nuclear Weapons Policy Fund).

### 3. Leadership Development

> "Manage and coach People Operations, Business Operations, Finance, Talent, and Grants Management leads."

**Track Record:** At Tides, managing managers was among my highest-leverage responsibilities. I guided leadership through six major organizational transformations, redesigning workflows, decision rights, and reporting structures as the portfolio grew.

**Application in Model:** `build_decision_rights_matrix()` reflects a week-one operational framework:

- **Named ownership:** replaces generic RACI rows with functional owners — Talent leads hiring approvals, Finance leads budget commitments, Grants Management leads fund allocation and due diligence.
- **Absorptive capacity:** Phase 1 of the hiring plan intentionally brings on more managers than ICs (4 vs. 3) to absorb existing reporting lines alongside new hires, not just manage net-new headcount.
- **Cross-border realities:** the matrix routes performance management and PIP decisions through outside counsel as a *Consulted* party, accommodating UK employment-law differences relative to US at-will practice.

### 4. Specialized & Innovative Functions — Named Honestly

> "Build finance function covering internal accounting and capital investment." / "Develop recruiting function that includes headhunting for grantee organizations."

I believe in naming professional-development areas plainly rather than overstating capability:

- **Capital investment:** my background at Tides centered on grant disbursement, compliance, and operational governance rather than investment-committee management or reserve investing. My primary hands-on P&L experience comes from founding and running two small businesses — Ariel Bright Fitness and D.C. Soccer Sessions — where I owned cash-flow management, budgeting, and operations for a combined base of 750+ clients with no finance team behind me. That built real financial discipline, but institutional endowment and capital-investment management at Longview's scale is an area I'd expect to actively ramp up in, not one I'd claim existing depth in.
- **Founder headhunting:** sourcing external founders for grantee organizations isn't a function I've directly owned. The closest adjacent evidence is GlobalGiving's confirmed role administering the Pepsi Refresh Project's grant disbursements — a program that, per PepsiCo's own 2011 newsroom release, had grown to $1M+ in monthly grants by 2011 — alongside GlobalGiving's independently documented partnerships with Nike and Microsoft. On the founder side specifically, having personally founded and run two organizations from zero gives me a genuine, lived sense of what an early-stage founder needs from a funder or operating partner. Neither is the same skill as sourcing and vetting external founders to fund, and I'm not presenting it as equivalent — but together they're closer than a purely administrative read of my resume would suggest.

### 5. Systems & Processes

> "Build simple, robust systems for planning and decision-making that can scale."

**Application in Model:** this repository mirrors the operational approach I'd bring — modular, versioned, tested (`tests/`), and continuously verified via CI (`.github/workflows/test.yml`). It reflects the same digital-adoption mindset I used at Tides to modernize executive reporting and accelerate decision-making speed, applied here to a codebase instead of a slide deck.

## Board & CEO Visibility

A COO's systems earn their keep by what they surface to the people who have to act on them — not just by existing. Two things this model is built to support:

**Reporting cadence.** The Q4 items in the compliance calendar (board-approved budget and reserve policy, audit prep) are timed to a typical annual board cycle rather than treated as a standalone compliance task. `summary.json`'s generation lineage (timestamp, source file) is meant to feed a recurring ops dashboard, not sit as a one-off report — the same structured-data instinct a board expects from monthly or quarterly management reporting. Every above-threshold grant or budget decision routes to the CEO by design in the RACI matrix, not as an exception someone has to remember to escalate.

**Top operational risks this model surfaces for year one:**

| Risk | Why It Matters | How This Model Handles It |
| --- | --- | --- |
| Management capacity lags headcount growth | Doubling staff in 18 months can outrun the org's ability to actually manage the new hires | Phase 1 front-loads managers (4 of 7 hires) ahead of ICs, sized to absorb existing reporting lines too, not just new headcount |
| A department has no clear functional owner | `donor_advising` doesn't map cleanly to any of the five named functional leads in the public JD | Flagged as `null` in `summary.json` on purpose rather than guessed — a real week-one question for the CEO |
| Cross-jurisdiction compliance treated as one template | US and UK entities carry materially different filings, deadlines, and employment law | `build_compliance_calendar()` generates separate cadences; the RACI matrix routes UK-relevant PIP/termination decisions through outside counsel |
| AI-safety or nuclear-policy grants get standard nonprofit due diligence only | A safety-motivated proposal can still be capabilities-uplifting if published; nonproliferation issues need specialist input a generalist review can miss | Due diligence splits into three lenses (standard, infohazard, export-control) with a technical reviewer named as Consulted, not folded into Legal |
| Illustrative budget figures get mistaken for real ones | `avg_fully_loaded_cost_per_fte` in `sample_org.yaml` is a placeholder, not a comp band | Called out explicitly in Scope & Operational Limitations — swap in real figures before using this as anything but a demonstration |

## Repository Architecture

- **`ops_model.py`** — core logic engine. Reads an organizational spec and outputs a phased hiring plan, a functional RACI matrix, a jurisdiction-specific compliance calendar, and a structured `summary.json`.
- **`sample_org.yaml`** — illustrative input file based on Longview's public footprint (four departments, ~35 staff scaling toward ~70 across US/UK hubs).
- **`output/`** — generated markdown artifacts and machine-readable data outputs.
- **`tests/`** — automated test suite verifying calculation logic, input validation, and data exports.
- **`.github/workflows/test.yml`** — CI pipeline running tests on every push.
- **`.github/dependabot.yml`** — automated dependency and Action version updates.
- **`LICENSE`** — MIT.
- **`NOTE_TO_CEO.md`** — a short, contextual note meant to accompany this link when I reach out directly.

## Sample Outputs

Real output from `python ops_model.py sample_org.yaml`, trimmed for length (full files in `output/`).

**1. Phased Hiring Plan** — 35 net-new hires phased over 18 months, with differentiated pricing for leadership vs. IC roles:

| Phase | Total New Hires | Manager/Lead Hires | IC Hires | Incremental Annualized Cost |
| --- | --- | --- | --- | --- |
| **Q1 — Foundational Leadership** | 7 | 4 | 3 | $1,315,000 |
| **Q2–Q3 — Core Team Build-out** | 12 | 3 | 9 | $2,100,000 |
| **Q4–Q6 — Scale & Specialize** | 16 | 2 | 14 | $2,720,000 |

**2. Decision-Rights Matrix** (excerpt):

| Decision | Responsible (R) | Accountable (A) | Consulted (C) | Informed (I) |
| --- | --- | --- | --- | --- |
| **Individual Grant Approval** *(Above threshold)* | Grants Management | CEO | COO, Finance, Outside Counsel | All Functional Leads |
| **Grantee Due Diligence & COI** | Grants Management | COO | Finance, Outside Counsel, Technical Reviewer | CEO |

**3. Machine-Readable Export** (`summary.json`):

```json
{
  "generated_at": "2026-09-01",
  "net_new_hires": 35,
  "department_functional_lead_map": {
    "operations": "Business Operations",
    "donor_advising": null,
    "ai_grantmaking": "Grants Management",
    "nuclear_grantmaking": "Grants Management"
  }
}
```

**4. Compliance Calendar** (excerpt):

| Jurisdiction | Q2 Primary Focus |
| --- | --- |
| **US — 501(c)(3) / 501(c)(4)** | IRS Form 990 preparation and filing (due 15th day of 5th month post fiscal year-end). |
| **UK — Registered Charity** | Trustees' Annual Report & Accounts (due within 10 months of financial year-end to the Charity Commission). |

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Execute model generator
python ops_model.py sample_org.yaml

# Run test suite
python tests/test_ops_model.py
```

Generated files land in `/output`. Tests also run automatically via GitHub Actions on every push.

## Scope & Operational Limitations

- **Public data only.** All models, costs, and organizational structures are derived exclusively from Longview's public job description and website — no proprietary or internal data appears anywhere in this repo.
- **Cost placeholders.** The `avg_fully_loaded_cost_per_fte` and `avg_fully_loaded_cost_manager` figures in `sample_org.yaml` are illustrative estimates, not real comp bands — swap in Longview's real figures before treating the budget line as anything but a demonstration.
- **Legal disclaimer.** The compliance calendar is an operational planning cadence, not formal legal or tax advice. Real deadlines, thresholds, and jurisdiction-specific requirements should always be confirmed with counsel or an accountant.
- **Named gaps, not fake solutions.** This model doesn't attempt to solve the two gaps named in Pillar 4 (capital investment, founder headhunting) — it names them honestly instead of building something that only looks complete.
- **Out-of-scope items.** This model does not allocate hires across Longview's specific hubs, calculate visa/immigration lead times, model multi-currency or cost-of-living differences, or design internal job leveling/career ladders — Longview's own stated culture makes career-ladder design a real question, not a checkbox, and it's out of scope here.
- **Due-diligence lenses describe intent, not a finished tool.** The infohazard and export-control lenses in the compliance calendar describe what should exist; building the actual screening workflow needs real technical and nonproliferation expertise, not a script.
- **`summary.json` is a first step,** not a full data build-out — a real version would extend the same structured-export pattern to all artifacts and integrate with an actual system of record (HRIS, grants CRM) with real access controls around due-diligence data.
- **The Board & CEO Visibility risk table is this model's own read of public data** — it is not Longview's actual risk register, and a real one would be built together with the CEO, board, and relevant functional leads.
- **Prior-employer neutrality.** Figures referenced from former employers (Tides, GlobalGiving) are the same non-confidential, summary-level figures already used in my resume and cover letter — not internal documents, systems, or methodologies. Mentions of PepsiCo, Nike, Microsoft, GlobalGiving, and Longview Philanthropy are for factual identification only; no endorsement, sponsorship, or affiliation by any named organization is implied, and no logos or trademarked material appear anywhere in this repo.

## Sources & References

1. Longview Philanthropy, COO job description — [longview.org/careers/chief-operating-officer](https://www.longview.org/careers/chief-operating-officer/)
2. Longview Philanthropy, mission and funds — [longview.org](https://www.longview.org/)
3. Longview team member, on culture and growth — [EA Forum post](https://forum.effectivealtruism.org/posts/aX8xLjCLd4LMDpTYL/)
4. PR Newswire, ["Pepsi Refresh Project To Award $1.3 Million In Grant Funding To Help Gulf Communities"](https://www.prnewswire.com/news-releases/pepsi-refresh-project-to-award-13-million-in-grant-funding-to-help-gulf-communities-97594079.html) (July 1, 2010) — the Gulf Coast relief round's scale and structure.
5. PepsiCo Newsroom, ["Pepsi Taps Consumers To Shake Up Refresh Project In 2011"](https://www.pepsico.com/newsroom/press-releases/2011/pepsi-taps-consumers-to-shake-up-refresh-project-in-2011) — PepsiCo's own confirmation that GlobalGiving administered grant disbursements and monitoring for the program.
6. Wikipedia, [Pepsi Refresh Project](https://en.wikipedia.org/wiki/Pepsi_Refresh_Project) — independent corroboration of the program's overall scale and categories.
7. GlobalGiving, [Nike employee giving program case study](https://tools.blog.globalgiving.org/2011/03/21/nikes-employee-giving-program-on-globalgiving/) and [Microsoft partnership case study](https://www.globalgiving.org/companies/case-studies/msft/) — independent documentation of the corporate partnerships named in Pillar 4.
