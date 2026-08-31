# Longview Philanthropy — COO Operating Model

**A working demonstration of how I'd approach the Chief Operating Officer role, built against Longview's actual public job description.**

Ariel Carter — [arielebright@gmail.com](mailto:arielebright@gmail.com) · [linkedin.com/in/ariel-carter1](https://www.linkedin.com/in/ariel-carter1) · [github.com/AC-tech-alt](https://github.com/AC-tech-alt)

## Why this exists

Longview's COO posting asks for someone who can "build simple, robust systems for planning and decision-making that can scale" and "run operations as a service to the rest of Longview." Rather than only describe that instinct in a cover letter, this repo is a small working example of it: a toolkit that turns a description of an org (headcount, departments, jurisdictions) into three concrete artifacts a new COO would actually want ready in week one — a phased hiring plan, a decision-rights matrix, and a compliance-review cadence. It's deliberately small and readable, not a finished product — the point is to show the way I think about building scalable systems, not to ship software.

## Grounded in Longview's actual mission and current priorities

I built this against Longview's own public materials, not a generic COO template:

- **Mission and theory of change** ([longview.org](https://www.longview.org/)): Longview directs philanthropic capital toward catastrophic risks — nuclear war between great powers, engineered pandemics, and AI misuse — on the premise that "strategic generosity can not merely better the world so much as alter the course of history." Donor capital flows through vehicles like the Frontier AI Fund and Nuclear Weapons Policy Fund. That framing is why the compliance and governance work in this repo isn't decorative: when the capital and the risk are both this consequential, operational rigor is part of the mission, not overhead on top of it.
- **Current scale and trajectory** (Longview's public hiring materials): the org grew from roughly 24 to 35+ staff through 2026 while more than doubling annual grantmaking to $60M+, and the COO posting asks for the same trajectory again — doubling headcount toward ~70. `sample_org.yaml` and `ops_model.py`'s phase-mix logic are built around exactly that shape of growth, not a hypothetical one.
- **Culture and working style** (published by a Longview team member): the org explicitly wants self-directed operators who are comfortable with ambiguity — "career progression isn't predetermined... advancement comes through tackling progressively harder, important problems" — across a distributed team spanning eight timezones and four hubs (Berkeley, DC, NYC, London). That's precisely the muscle six organizational transformations at Tides built: making a call, building the system, and adjusting rather than waiting for a fully specified process.

## Mapping to the role's five pillars

The job description groups the COO mandate into five clusters. Here's how I'd approach each, and what this repo demonstrates for it.

### 1. Scaling & growth strategy
*"Design and execute the operations and hiring strategy to double Longview's headcount."*

I joined GlobalGiving at roughly 20 employees and helped architect the grant management infrastructure that supported its growth to 100+ employees today. At Tides, I recruited, coached, and developed a 15-person team including two direct-report managers, building management capability across multiple organizational layers as the portfolio scaled. `ops_model.py`'s `build_scaling_plan()` shows the mechanics I'd bring to Longview specifically: sequencing leadership and manager hires ahead of individual-contributor hires so the org doesn't outgrow its own management capacity, phased by quarter against a headcount-doubling target.

### 2. Regulatory & compliance
*"Stay on top of regulatory requirements across the jurisdictions we operate in."*

At Tides, I partnered with Legal and Compliance to design and execute a 110-item compliance audit — covering expenditure responsibility, anti-bribery/anti-corruption, and IRS and global regulatory frameworks — that made our systems audit-proof: 70 high-priority items closed within 7 months, 95% of the full audit within a year. I have not personally run UK-entity compliance, but the discipline transfers directly, and it has to: Longview operates US and UK entities across four hubs, and `build_compliance_calendar()` generates a recurring, jurisdiction-by-jurisdiction review cadence for exactly that split (not a legal opinion — a planning framework a compliance lead and outside counsel would fill in with jurisdiction-specific detail).

### 3. Leadership development
*"Manage and coach People Operations, Business Operations, Finance, Talent, and Grants Management leads."*

This is close to the highest-leverage part of what I did at Tides: managing managers, not just individual contributors, during a period of real organizational change (six major transformations that redesigned workflows, decision rights, and reporting structures as the portfolio scaled). `build_decision_rights_matrix()` demonstrates the artifact I'd bring in week one — a RACI matrix across the five functional leads so authority is explicit rather than negotiated case by case.

### 4. Innovative functions — named honestly
*"Build finance function covering internal accounting and capital investment. Develop recruiting function that includes headhunting for grantee organizations."*

Two real gaps, named plainly rather than smoothed over:

- **Capital investment:** my Tides work was on the grants-disbursement and compliance side, not investment-committee or endowment/reserve management, though I worked closely with the impact team there. I'd expect to ramp up here rather than claim existing depth.
- **Headhunting founders for grantee orgs:** I haven't done this exact work. The closest adjacent evidence is leading GlobalGiving's first-of-its-kind Pepsi Refresh partnership, which required building cross-sector relationships with Nike, Microsoft, and Facebook from scratch — real ecosystem-building instinct, not a direct match.

### 5. Systems & processes
*"Build simple, robust systems for planning and decision-making that can scale. Streamline and automate operational work. Run operations as a service."*

This whole repo is the answer to this pillar: small, versioned, testable, and legible to anyone who has to pick it up after me — the same instinct behind the AI/digital adoption initiative I led at Tides, which modernized workflows and executive reporting and directly improved decision-making speed.

## What's in this repo

- **`ops_model.py`** — reads a description of an org and generates a phased hiring plan, a RACI decision-rights matrix, and a compliance-review cadence template.
- **`sample_org.yaml`** — an illustrative input modeled on Longview's public org description (four departments, roughly 35 people scaling toward ~70, US/UK jurisdictions). Built entirely from Longview's own published careers page — no internal data.
- **`output/`** — the three artifacts generated by running the model against the sample input (generated, not hand-written).
- **`tests/`** — a small test suite covering the planning logic.

## How to run it

```bash
pip install -r requirements.txt
python ops_model.py sample_org.yaml
```

Outputs land in `output/`: `scaling_plan.md`, `decision_rights_matrix.md`, `compliance_calendar.md`.

## A note on honesty

Two sections above name real gaps instead of papering over them. I'd rather walk into a work-trial having already told you where I'd need to ramp up than have that surface for the first time under pressure.
