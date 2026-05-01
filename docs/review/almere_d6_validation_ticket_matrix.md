# Almere D6 validation ticket matrix

## Summary
Current sprint: Sprint 31.5 - Deep-research bronintake en top-layer verificatie.

This is the constrained handoff version of the D6 open questions. It turns the remaining questions into validation tickets with answer choices, evidence gates and register effects.

Use this file when asking policy owners, finance/controller roles, GGD/JGZ, Wijkteams, PGA/Zorgzaam/Flever, digital/data leads or regional governance contacts for validation. Do not hand them broad research questions. Ask them to confirm, correct, choose an option and provide evidence.

No D6 responsibility-register row may move to `settled` from this matrix alone. Settlement requires traceable evidence that directly answers classification, ownership, execution/coordination, scale, funding and mandate.

## How To Use

1. Start from the current repository prefill.
2. Ask the ticket question with the listed choice set.
3. Record the answer, evidence type and evidence path.
4. Apply the default register effect unless the evidence gate is fully met.
5. Escalate conflicts, missing owners, missing funding, unclear mandate or wording risk.

## Standard Choice Sets

### D6 Classification

A. Formal D6 infrastructure already decided  
B. Adjacent or supporting infrastructure  
C. Candidate D6 infrastructure / candidate upgrade  
D. Implementation context or example, not a D6 component  
E. Outside D6 scope  
F. Unknown / no decision yet  
G. Other, with explanation

### Current Status

A. Existing structural provision  
B. Existing project or pilot  
C. Planned / under development  
D. Historical / discontinued / no longer active  
E. Exists, but scale unclear  
F. Unknown  
G. Other, with explanation

### Scale

A. Almere-local  
B. GGD Flevoland scale  
C. IZA/AZWA Flevoland regional scale  
D. PGA / Zorgzaam Flevoland / Flever programme scale  
E. Zorgkantoor / insurer / Zvw scale  
F. Provider or partner-organization scale  
G. School, wijk or location-specific scale  
H. Mixed scale; split needed  
I. Other, with explanation

### Role

A. Accountable owner  
B. Coordinator  
C. Executor  
D. Partner / contributor  
E. Funder only  
F. Data/privacy accountable party  
G. No formal role  
H. Unknown  
I. Other, with explanation

### Funding

A. Regular municipal budget  
B. AZWA-D6  
C. D5 work-agenda resources  
D. SPUK/GALA  
E. PGA / IZA transformation funding  
F. GGD contribution / inwonerbijdrage / plustaak  
G. Zvw / insurer funding  
H. Provider funding  
I. Project subsidy, such as ZonMw or temporary programme funding  
J. Mixed funding; split required  
K. No funding decision yet  
L. Other, with explanation

### Evidence Type

A. Formal public/local source already in corpus  
B. New public source to ingest first  
C. Internal/local document  
D. Formal decision record  
E. Finance/controller confirmation  
F. Stakeholder validation-log entry  
G. No evidence yet

## Default Register Effects

| Situation | Default register effect |
| --- | --- |
| Public evidence only, no stakeholder confirmation | Keep `inferred`. |
| Stakeholder confirms but no evidence path | Keep `inferred`; add incomplete validation note. |
| Stakeholders disagree | Keep or move to `review_needed`. |
| Owner or funding unknown | Keep `unknown` or `review_needed`; do not settle. |
| Formal decision exists but does not settle D6 classification/funding | Record the decision, but do not settle the D6 row. |
| Classification, owner, executor/coordinator, scale, funding and evidence are all validated | Candidate for `settled`. |

## Validation Tickets

| Ticket | Current repository prefill | Question type | Choice set | Evidence gate | Default register effect | Escalation trigger |
| --- | --- | --- | --- | --- | --- | --- |
| Inloopvoorzieningen sociaal en gezond | Public sources show social-base, buurtontmoeting, wijkbudget, wijkteam social-contact access, De Schoor, resident initiatives, mantelzorg and volunteer-support routes as relevant candidates. | `classification_choice`, `role_split`, `funding_split` | For each named facility/mechanism: D6 classification, current status, role, scale, funding, evidence type. | Local inventory or validation record naming facilities, owner/coordinator and funding line. | Keep `inferred` until named facilities and funding are validated. | No named inventory, no coordinator, unclear double funding. |
| Wijkteams Almere | Public sources support Wijkteams as existing local support/access infrastructure. | `classification_choice`, `mandate_interpretation`, `role_split` | D6 classification; relation to SLT: separate baseline, transition path, execution partner, coordination partner, unknown, other. | Gemeente Almere/Wijkteams validation or implementation document on mandate, coverage, partner model and SLT relation. | Keep `inferred`. | Wijkteam mandate or SLT relation unclear. |
| Stevige Lokale Teams | Public council material shows a 19 February 2026 SLT decision route and connection with JGZ/wijkteams. | `mandate_interpretation`, `classification_choice`, `funding_split` | What does the decision settle: SLT development only, D6 classification, mandate, owner, funding, partial, other. Rows touched: SLT, Wijkteams, JGZ, funding, monitoring, other. | Decision interpretation tied to council attachments, validation record and budget lines. | Keep `inferred`; do not settle if decision only supports SLT development. | Decision is cited as D6 proof without explicit D6 classification or funding interpretation. |
| JGZ Almere | Public GGD/JGZ sources show broad 0-18 youth-health relevance to families, schools and local support. | `assurance`, `role_split`, `classification_choice` | For each JGZ role: regular JGZ, SLT-related, D6-specific, adjacent prevention, unknown, other. | JGZ/GGD/Gemeente task split or validation record. | Keep `inferred`. | JGZ regular work is collapsed into D6-specific work. |
| GGD Flevoland-coordinatie | Public GGD sources support regional public-health, prevention, knowledge, advice, JGZ and monitoring relevance. | `role_split`, `classification_choice`, `funding_split` | Task split: regular GGD/public health, GALA/SPUK, regional monitoring/advice, D6-specific Almere, other. Scale choice required. | GGD/Flevoland/Gemeente validation of task, scale and funding route. | Keep `inferred`. | GGD regional tasks are overclaimed as Almere D6 tasks. |
| Gezonde School / mentale gezonde school | Public Almere/GGD/JGZ/school sources now support school wellbeing and prevention context. | `classification_choice`, `role_split`, `funding_split`, `wording_approval` | D6 classification, current status, owner/coordinator, scale, funding, evidence type. | Local school/prevention arrangement or validation record naming owner, coordinator and funding. | Keep `inferred`. | School-prevention context is presented as formal D6 without validation. |
| Kennis & Advies / monitoring / dashboards | GGD Kennis & Advies sources show monitors, dashboards, epidemiology, data analysis and advice functions. | `assurance`, `role_split`, `data_governance` | Which monitors steer D6: GGD Kennis & Advies, GGD dashboards, municipal dashboard, PGA/regional dashboard, D5 work-agenda monitoring, none, unknown, other. | Monitoring arrangement naming reporting owner, maintainer, frequency and funding. | Keep `inferred`. | Monitoring capability is confused with accepted D6 steering arrangement. |
| Samen Sterker in de Wijk | Public sources show active mental-health neighbourhood implementation context through Almere, Zorglandschap Wmo, ZonMw, PGA and project material. | `assurance`, `classification_choice`, `role_split`, `funding_split` | Current status, scale, D6 classification, owner/coordinator, funding, evidence type. | Current project/governance validation, evaluation steering evidence and funding status. | Keep `inferred`. | Project status, citywide scale or structural funding unclear. |
| PGA / Zorgzaam Flevoland-interface | Public sources clarify a role split: PGA local transformation programme, Zorgzaam regional IZA/regioplan movement, Flever participation/support, GGD monitoring/advice. | `role_split`, `classification_choice`, `funding_split` | Per actor: local programme, regional governance layer, participation-support actor, monitoring/advisory actor, funder, D6 owner, unknown, other. | Programme governance validation and funding-role split. | Keep `inferred`. | PGA, Zorgzaam, Flever, GGD and AZWA/D5/D6 roles are merged into one actor or budget line. |
| Digitale en operationele infrastructuur | Public sources support RTP, RSO/data infrastructure, thuismonitoring, GGD monitoring and ACP/PZP data-sharing pilots as separate public components. | `data_governance`, `role_split`, `classification_choice`, `funding_split` | Split before validation: RTP; RSO/data infrastructure; thuismonitoring; GGD dashboards/monitoring; ACP/PZP pilots; other digital support. Per subcomponent: D6 classification, owner, data/privacy accountable party, operations, funding, continuity. | Component split plus ICT/privacy/accountability and funding validation. | Keep `inferred`; create sub-rows only when governance needs separate tracking. | One broad digital row hides different owners, data controllers, privacy risks or funding routes. |
| Burgerinitiatieven en informele steun | Public sources show wijkbudget, resident-led support, De Schoor, VMCA, Humanitas, mantelzorg and prevention-network context. | `classification_choice`, `role_split`, `funding_split` | Per mechanism/actor: inside D6, adjacent social base, candidate, context, outside, unknown, other. | Local inventory, classification and funding validation. | Keep `inferred`. | Known actors are treated as inside D6 because they are publicly visible. |
| Financiering en budgetafbakening | Public sources support funding-route awareness and double-counting risk, but not a component-level funding matrix. | `funding_split`, `mandate_interpretation`, `wording_approval` | Use as master matrix, not a normal component: AZWA-D6, D5, SPUK/GALA, PGA/IZA, regular municipal budget, GGD contribution/plustaak, Zvw/insurer, provider funding, project subsidy, structural/project/undecided, double-counting risk. | Finance/controller matrix or budget decision per component. | Keep `unknown` until component-level funding is validated. | Any final wording calls a component structural, funded or assigned without finance validation. |

## Work Packages For Handoff

| Work package | Rows covered | Output |
| --- | --- | --- |
| Gemeente Almere classification session | Inloop, Wijkteams, SLT, Gezonde School, informal support | Classification choices, owner candidates, decision route and safe wording issues. |
| GGD/JGZ/monitoring session | JGZ, GGD coordination, Gezonde School, Kennis & Advies | Task split, scale split and dashboard/reporting ownership. |
| Mental-health / Samen Sterker session | Samen Sterker, PGA interface, SLT relation if relevant | Current status, scale, D6 relation, owner/coordinator and evaluation status. |
| Digital/data/privacy session | Digital and operational infrastructure, monitoring overlap | Subcomponent owner, data controller, privacy/security accountability, operations and funding. |
| Finance/controller review | All rows | Component-level funding matrix and double-counting control. |

## Source-Intake Ticket

| Source candidate | Current status | Next action | Register effect |
| --- | --- | --- | --- |
| `Stand van zaken Gezondheidsbeleid (IZA en GALA)` | Stable Documentwijzer landing URL found; underlying raadsbrief text/PDF not retrieved. Candidate is recorded in `data/raw/source_intake_candidates.json` as `pending_full_text`. | Find stable download/API document URL, ingest through manifest if claim-ready, rerun pipeline and verify top-layer appearance. | No D6 register change until claim-ready source text or validation evidence exists. |

## Settlement Rule

A row can become `settled` only when all of these are traceably answered:

- D6 classification;
- accountable owner;
- executor and/or coordinator;
- scale;
- funding source and funding status;
- mandate or decision route where relevant;
- evidence path.

If any of those remain missing, keep `inferred`, `unknown` or `review_needed`.
