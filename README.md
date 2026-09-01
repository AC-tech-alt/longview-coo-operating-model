# Longview Philanthropy — COO Operating Model

**A working demonstration of how I'd approach the Chief Operating Officer role, built against Longview's actual public job description.**

Ariel Carter — [arielebright@gmail.com](mailto:arielebright@gmail.com) · [linkedin.com/in/ariel-carter1](https://www.linkedin.com/in/ariel-carter1) · [github.com/AC-tech-alt](https://github.com/AC-tech-alt)

## Why this exists

Longview's COO posting asks for someone who can "build simple, robust systems for planning and decision-making that can scale" and "run operations as a service to the rest of Longview." A cover letter can describe that instinct; this repo tries to show it — a small toolkit that turns a description of an org (headcount, departments, jurisdictions) into three artifacts a new COO would actually want ready in week one: a phased hiring plan with a budget view, a decision-rights matrix with named owners, and a jurisdiction-specific compliance cadence. It's deliberately small and readable, not a finished product.

## Grounded in Longview's actual mission and current priorities

Built against Longview's own public materials, not a generic COO template:

- **Mission and theory of change** ([longview.org](https://www.longview.org/)): Longview directs philanthropic capital toward catastrophic risks — nuclear war between great powers, engineered pandemics, and AI misuse — on the premise that "strategic generosity can... alter the course of history." Capital flows through vehicles like the Frontier AI Fund and Nuclear Weapons Policy Fund. That's why compliance and governance in this repo aren't decorative: when the capital and the risk are both this consequential, operational rigor is part of the mission, not overhead on top of it.
- **Current scale and trajectory** (Longview's public hiring materials): the org grew from roughly 24 to 35+ staff through 2026 while more than doubling annual grantmaking to $60M+, and the COO posting asks for the same trajectory again — doubling headcount toward ~70. `sample_org.yaml` and `ops_model.py`'s phase-mix logic are built around exactly that shape of growth.
- **Culture and working style** (published by a Longview team member on the [EA Forum](https://forum.effectivealtruism.org/posts/aX8xLjCLd4LMDpTYL/)): the org wants self-directed operators comfortable with ambiguity — "career progression isn't predetermined... advancement comes through tackling progressively harder, important problems" — across a distributed team spanning eight timezones and four hubs (Berkeley, DC, NYC, London).

## Mapping to the role's five pillars

### 1. Scaling & growth strategy
*"Design and execute the operations and hiring strategy to double Longview's headcount."*

I joined GlobalGiving at roughly 20 employees and helped architect the grant management infrastructure that supported its growth to 100+ employees today. At Tides, I recruited, coached, and developed a 15-person team including two direct-report managers, building management capability across multiple organizational layers as the portfolio scaled. `build_scaling_plan()` shows the mechanics I'd bring to Longview specifically: leadership/manager hires sequenced ahead of individual-contributor hires so the org doesn't outgrow its own management capacity, phased by quarter against the headcount-doubling target — and converted into an illustrative budget view that prices manager and IC hires *differently* — a flat blended rate would make a manager-heavy quarter (Phase 1) look exactly as cheap as an IC-heavy one (Phase 3), which understates real cost. At an illustrative ~$6.1M/year, that's a number worth sanity-checking against Longview's own public scale (>$60M in annual grantmaking) rather than handing over a hiring plan with no budget context — the kind of check a fiscal-governance-minded COO brings to a leadership meeting, not just a headcount chart.

### 2. Regulatory & compliance
*"Stay on top of regulatory requirements across the jurisdictions we operate in."*

At Tides, I partnered with Legal and Compliance to design and execute a large-scale, multi-area compliance audit — covering expenditure responsibility, anti-bribery/anti-corruption, and IRS and global regulatory frameworks — that made our systems audit-proof, closing the large majority of priority items within months and substantially completing the full scope within about a year. (Deliberately kept at that level of generality rather than exact figures — this is a former employer's internal audit, not something to detail publicly.) I haven't personally run UK-entity compliance, but the discipline transfers, and it has to: Longview operates US and UK entities across four hubs. `build_compliance_calendar()` generates jurisdiction-specific cadences rather than one generic template — US Form 990 and state solicitation-registration deadlines are different animals from a UK Charity Commission Annual Return and Companies House filing, and a compliance plan that treats them identically isn't a real plan. It also splits grantee/partner due-diligence into three lenses instead of one, because a generic nonprofit template collapses them: standard sanctions/COI screening; **capability/infohazard screening for AI-safety grants** (a proposal can be safety-motivated and still be capabilities-uplifting if published, which needs a technical reviewer in the loop, not just Legal); and **export-control/sanctioned-jurisdiction awareness for nuclear-policy grants** (OFAC and ITAR/EAR-adjacent questions a generalist legal review can miss without nonproliferation-specific input). The RACI matrix reflects that directly — due-diligence now names a technical/subject-matter reviewer as Consulted, not just Finance and outside counsel — and separates two decisions a grants-operations lead actually lives with day to day: individual grant approval (tiered by a delegation threshold) versus the board/CEO-level call of allocating capital across program areas (Frontier AI Fund vs. Nuclear Weapons Policy Fund). The first draft of this repo only modeled the second one.

### 3. Leadership development
*"Manage and coach People Operations, Business Operations, Finance, Talent, and Grants Management leads."*

This is close to the highest-leverage part of what I did at Tides: managing managers, not just individual contributors, through six major organizational transformations that redesigned workflows, decision rights, and reporting structures as the portfolio scaled. `build_decision_rights_matrix()` demonstrates the artifact I'd bring in week one — but rather than one templated "COO / Lead / CEO" row repeated across every decision, each one names a specific owner (Talent leads hiring approvals, Finance leads budget commitments, Grants Management leads fund allocation and due-diligence) so authority is explicit and function-specific from day one, not negotiated case by case. One honest wrinkle worth naming: Phase 1 of the hiring plan brings on more managers than ICs (4 vs. 3) — that's deliberate, not an error, because those leadership hires are expected to also absorb reporting lines from *existing* staff via the org-chart-change decision above, not just manage the net-new ICs arriving the same quarter. A plan that only reconciled against net-new headcount and ignored the org's existing management structure is the kind of gap a People lead catches immediately. The matrix also now routes performance management and PIP decisions through outside counsel as a Consulted party, not just People Operations and the COO — UK termination law is considerably less forgiving than at-will US practice, and that's not a difference a US-centric instinct catches on its own.

### 4. Innovative functions — named honestly
*"Build finance function covering internal accounting and capital investment."* *"Develop recruiting function that includes headhunting for grantee organizations."*

Two real gaps, named plainly rather than smoothed over:

- **Capital investment:** my Tides work was on the grants-disbursement and compliance side, not investment-committee or endowment/reserve management, though I worked closely with the impact team there. The closest adjacent evidence I have is founder-side, not investment-side: I founded and scaled two organizations from the ground up — Ariel Bright Fitness and D.C. Soccer Sessions — owning full P&L, budgeting, and cash-flow management for a combined base of 750+ clients with no finance team behind me. That's real, hands-on ownership of a finance function; it isn't the institutional capital-investment or endowment-management experience Longview is asking for, and I'd expect to ramp up there rather than claim existing depth.
- **Headhunting founders for grantee orgs:** I haven't done this exact work. The closest adjacent evidence is twofold. First, GlobalGiving's confirmed role in the Pepsi Refresh Project: PepsiCo's own newsroom states that "Pepsi will also continue its partnership with Global Giving to administer grant disbursements and monitoring" for the program, which by 2011 had grown to $1M+ in monthly grants across $5,000–$50,000 tiers ([PepsiCo, 2011](https://www.pepsico.com/newsroom/press-releases/2011/pepsi-taps-consumers-to-shake-up-refresh-project-in-2011)) — alongside GlobalGiving's independently documented relationships with [Nike](https://tools.blog.globalgiving.org/2011/03/21/nikes-employee-giving-program-on-globalgiving/) and [Microsoft](https://www.globalgiving.org/companies/case-studies/msft/). Second, on the founder side specifically: having personally founded and run two organizations from zero gives me a genuine, lived sense of what an early-stage founder actually needs from a funder or operating partner. Neither is the same skill as sourcing and vetting external founders to fund, and I'm not presenting it as equivalent — but together they're closer than a purely administrative read of my resume would suggest.

### 5. Systems & processes
*"Build simple, robust systems for planning and decision-making that can scale. Streamline and automate operational work. Run operations as a service."*

The repo itself is built the way this pillar asks: small, versioned, tested (`tests/`), and checked by CI on every push (`.github/workflows/test.yml`) — the same instinct behind the AI/digital adoption initiative I led at Tides, which modernized workflows and executive reporting and directly improved decision-making speed. It's meant to be legible to whoever has to pick it up after me, not just to me.

## What's in this repo

- **`ops_model.py`** — reads a description of an org and generates a phased hiring plan (manager/IC-differentiated budget view), a named-ownership RACI matrix with tiered grant-approval and delegation-threshold logic, a jurisdiction- and sector-specific compliance cadence, and a structured `summary.json` export.
- **`sample_org.yaml`** — an illustrative input modeled on Longview's public org description (four departments, ~35 people scaling toward ~70, US/UK jurisdictions, a department→functional-lead map). Built entirely from Longview's own published careers page — no internal data.
- **`output/`** — the four artifacts generated by running the model against the sample input, including a machine-readable `summary.json` with generation lineage (generated, not hand-written — see below for the real output).
- **`tests/`** — a test suite covering the planning logic, input validation, and the structured-data export.
- **`.github/workflows/test.yml`** — CI that runs the test suite on every push.
- **`.github/dependabot.yml`** — automated dependency and Action version updates.
- **`LICENSE`** — MIT.
- **`NOTE_TO_CEO.md`** — the short note meant to accompany this link when I reach out directly.

## Sample output

Real output from `python ops_model.py sample_org.yaml`, trimmed for length (full files in `output/`):

**Phased hiring plan** — 35 net-new hires to double headcount in 18 months, manager and IC hires priced differently so an early, leadership-heavy phase doesn't look as cheap as a later, IC-heavy one:

| Phase | New hires | Manager/lead hires | IC hires | Incremental annualized cost |
|---|---|---|---|---|
| Q1 — Foundational leadership | 7 | 4 | 3 | $1,315,000 |
| Q2–Q3 — Core team build-out | 12 | 3 | 9 | $2,100,000 |
| Q4–Q6 — Scale & specialize | 16 | 2 | 14 | $2,720,000 |

**Decision-rights matrix** — rows a generic RACI template wouldn't include:

| Decision | R | A | C | I |
|---|---|---|---|---|
| Individual grant approval (above the delegation threshold) | Grants Management | CEO | COO, Finance, Outside counsel | All functional leads |
| Grantee & partner due-diligence / conflict-of-interest screening | Grants Management | COO | Finance, Outside counsel, Technical/subject-matter reviewer | CEO |

**`summary.json`** — a structured, machine-readable export alongside the three markdown files, with generation lineage and the department↔functional-lead taxonomy map (including the one department, `donor_advising`, that doesn't cleanly map to any of the five named leads — flagged as `null` on purpose rather than guessed):

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

**Compliance calendar** — jurisdiction-specific, not identical templates for US and UK:

| Jurisdiction | Q2 focus |
|---|---|
| US — 501(c)(3)/(c)(4) | IRS Form 990 preparation & filing (due the 15th day of the 5th month after fiscal year-end) |
| UK — UK registered charity | Trustees' Annual Report & Accounts (due within 10 months of financial year-end to the Charity Commission) |

## How to run it

```bash
pip install -r requirements.txt
python ops_model.py sample_org.yaml
python tests/test_ops_model.py
```

Outputs land in `output/`: `scaling_plan.md`, `decision_rights_matrix.md`, `compliance_calendar.md`. Tests also run automatically in CI on every push.

## Scope & limitations

- No real Longview financial or personnel data anywhere in this repo — everything is derived from Longview's public job description and website.
- `avg_fully_loaded_cost_per_fte` in `sample_org.yaml` is an illustrative placeholder, not a comp band — swap in Longview's real figures before treating the budget line as anything but a demonstration.
- The compliance calendar is a planning cadence, not legal advice. Real deadlines, thresholds, and jurisdiction-specific requirements should always be confirmed with counsel/accountant.
- This repo doesn't attempt to solve the two gaps named in Pillar 4 (capital investment, founder headhunting) — it names them honestly instead of building a fake solution to look complete.
- No confidential or proprietary information from any current or former employer appears here — the Tides figures referenced (audit scope, portfolio size, team size) are the same summary-level figures already used in my resume and cover letter, not internal documents, systems, or methodologies.
- Mentions of PepsiCo, Nike, Microsoft, GlobalGiving, and Longview Philanthropy are for factual identification only — no endorsement, sponsorship, or affiliation by any named organization is implied, and no logos or other trademarked material appear anywhere in this repo.
- Quotations from public sources (Longview's website, a Longview team member's public post, the Longview job posting, PepsiCo's newsroom) are short, attributed excerpts used for identification and context — see Sources below for the full originals.
- Doesn't allocate new hires across Longview's four hubs, model visa/immigration lead time for international hires, or account for US/UK currency and cost-of-living differences in the budget line — a real hiring plan needs that layer; this one names the gap instead of faking it.
- Doesn't design job leveling or career ladders — Longview's own stated culture ("career progression isn't predetermined") makes that a real design question, not a checkbox, and it's out of scope here.
- The due-diligence lenses named in the compliance calendar (capability/infohazard review, export-control awareness) describe what should exist, not a working screening tool — building the actual workflow needs real technical and nonproliferation expertise, not a script.
- `summary.json` is a first step toward separating structured data from markdown presentation, not a full data build-out — a real version would extend the same pattern to all three artifacts and integrate with an actual system of record (HRIS, grants CRM) with real access controls around anything touching due-diligence data.

## Sources

- Longview Philanthropy, COO job description: [longview.org/careers/chief-operating-officer](https://www.longview.org/careers/chief-operating-officer/)
- Longview Philanthropy, mission and funds: [longview.org](https://www.longview.org/)
- Longview team member, on culture and growth: [EA Forum post](https://forum.effectivealtruism.org/posts/aX8xLjCLd4LMDpTYL/)
- PR Newswire, ["Pepsi Refresh Project To Award $1.3 Million In Grant Funding To Help Gulf Communities"](https://www.prnewswire.com/news-releases/pepsi-refresh-project-to-award-13-million-in-grant-funding-to-help-gulf-communities-97594079.html) (July 1, 2010) — the Gulf Coast relief round's scale and structure.
- PepsiCo Newsroom, ["Pepsi Taps Consumers To Shake Up Refresh Project In 2011"](https://www.pepsico.com/newsroom/press-releases/2011/pepsi-taps-consumers-to-shake-up-refresh-project-in-2011) — PepsiCo's own confirmation that GlobalGiving administered grant disbursements and monitoring for the program.
- Wikipedia, [Pepsi Refresh Project](https://en.wikipedia.org/wiki/Pepsi_Refresh_Project) — independent corroboration of the program's overall scale and categories.
- GlobalGiving, [Nike employee giving program case study](https://tools.blog.globalgiving.org/2011/03/21/nikes-employee-giving-program-on-globalgiving/) and [Microsoft partnership case study](https://www.globalgiving.org/companies/case-studies/msft/) — independent documentation of the corporate partnerships named in Pillar 4.

## A note on honesty

Two sections above name real gaps instead of papering over them, and the "Scope & limitations" section above says plainly what this repo doesn't do. I'd rather walk into a work-trial having already told you where I'd need to ramp up than have that surface for the first time under pressure.
