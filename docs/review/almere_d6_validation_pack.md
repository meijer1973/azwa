# Almere D6 validation pack

## Summary
Current sprint: Sprint 25.5 - D6 stakeholder validation, under the reopened Sprint 25.4 D6 Almere responsibility pack.

This pack is for stakeholder validation only. It is not final bestuurlijke text, not a public D6 publication, and not a final Almere work-agenda section. The D6 register currently structures the public-source evidence and the open decision questions, but no row is marked `settled`.

## Register Summary

Source register: `data/extracted/municipal/almere_d6_responsibility_register.json`.

| Metric | Value |
| --- | ---: |
| Register rows | 12 |
| `settled` rows | 0 |
| `inferred` rows | 6 |
| `proposed` rows | 0 |
| `unknown` rows | 1 |
| `review_needed` rows | 5 |
| Rows needing human review | 12 |
| Rows without owner | 4 |
| Rows with unknown or needs-decision funding | 9 |

Validation artifacts:

- Stakeholder validation log: `docs/review/almere_d6_stakeholder_validation_log.md`.
- Stakeholder information request: `docs/review/almere_d6_stakeholder_information_request.md`.
- Decision-needed list: `docs/review/almere_d6_decision_needed.md`.
- Funding gap table: `docs/review/almere_d6_funding_gap_table.md`.

Rows without owner:

- Inloopvoorzieningen sociaal en gezond.
- Gezonde School / mentale gezonde school.
- Digitale en operationele infrastructuur.
- Burgerinitiatieven en informele steun.

Rows with unknown or needs-decision funding:

- Inloopvoorzieningen sociaal en gezond.
- Wijkteams Almere.
- Stevige Lokale Teams.
- Gezonde School / mentale gezonde school.
- Kennis & Advies / monitoring / dashboards.
- Samen Sterker in de Wijk / mentale-gezondheidswijkinfrastructuur.
- Digitale en operationele infrastructuur.
- Burgerinitiatieven en informele steun.
- Financiering en budgetafbakening.

## D6 For Almere

D6 is treated here as the practical basisinfrastructuur underneath D5. For Almere that means recognizable access and inloop, wijkteams and Stevige Lokale Teams, social-base and informal support, GGD/JGZ coordination, school and mental-health prevention, monitoring and learning infrastructure, and clear local/regional governance and financing.

The public source base is now strong enough to prepare validation questions. It is not strong enough to settle formal D6 classification, ownership, mandate, budget allocation, or accountability.

## Decision Table

| D6 component | Status | Owner / owner question | Executor(s) | Scale | Funding | Evidence | Open question | Who must validate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Inloopvoorzieningen sociaal en gezond | `review_needed` | Unknown | Social work, GGD/JGZ, citizen initiatives, informal support candidates | Almere local, needs validation | Unknown | `data/extracted/d6_governance_collaboration.json` | Which existing Almere inloop or social-base facilities formally count as D6 infrastructure? | Gemeente Almere, social-base partners, GGD/JGZ |
| Wijkteams Almere | `inferred` | Gemeente Almere needs confirmation | Wijkwerkers and represented care/welfare organizations | Almere local | Unknown | `mun_almere_wijkteams` | Are Wijkteams formal D6 infrastructure, adjacent infrastructure, or candidate infrastructure needing upgrade? | Gemeente Almere, Wijkteams Almere |
| Stevige Lokale Teams | `inferred` | Almere council/college line needs source-passage confirmation | JGZ Almere, wijkteams, schools and childcare partners | Almere local | Investeringsfonds Jeugd en Gezin candidate; split needs confirmation | SLT council page, amended proposal, budget amendment, decision list | What exactly is settled by the council decision, and does it classify SLT as formal D6 infrastructure? | Gemeente Almere, council/college, JGZ Almere, Wijkteams Almere |
| JGZ Almere | `inferred` | JGZ Almere / GGD Flevoland, municipal governance needs confirmation | JGZ Almere | Almere local with GGD Flevoland governance | GGD/JGZ funding split needs source-specific review | `reg_ggd_flevoland_jgz_almere_profile`, `reg_ggd_flevoland_begroting_2026` | Which JGZ roles are D6, which are regular JGZ, and which are part of SLT development? | GGD Flevoland, JGZ Almere, Gemeente Almere |
| GGD Flevoland-coordinatie | `inferred` | GGD Flevoland under six-municipality governance | GGD Flevoland | GGD Flevoland | Inwonerbijdrage, subsidies/plustaken, other source-specific funding | `reg_ggd_flevoland_begroting_2026` | Which GGD tasks belong to D6 for Almere versus broader GGD public-health tasks? | GGD Flevoland, Flevoland municipalities |
| Gezonde School / mentale gezonde school | `review_needed` | Unknown | GGD/JGZ and schools candidates | Almere local or GGD region, needs validation | Unknown | `reg_ggd_flevoland_jgz_almere_profile` | What is the Almere-specific implementation source and who owns delivery? | GGD/JGZ, schools, Gemeente Almere |
| Kennis & Advies / monitoring / dashboards | `inferred` | GGD Flevoland candidate, decision owner needs confirmation | GGD Flevoland Kennis en Advies | GGD Flevoland with Almere use | Unknown/source-specific split needed | `reg_ggd_flevoland_kennis_en_advies`, `reg_ggd_flevoland_begroting_2026` | Which dashboards and monitors steer D6, and who owns reporting? | GGD Flevoland, Gemeente Almere, regional programme governance |
| Samen Sterker in de Wijk / mentale-gezondheidswijkinfrastructuur | `inferred` | Shared responsibility needs validation | Zorgplatform Flevoland partners, local professionals, ervaringsdeskundigen | Almere local and regional project scale | Unknown | `mun_almere_samenwerkingsprojecten` | Is this formal D6 infrastructure, supporting infrastructure, or a separate implementation project? | Gemeente Almere, GGD Flevoland, GGZ/welfare partners, Zorgplatform Flevoland |
| Positief Gezond Almere / Zorgzaam Flevoland-interface | `review_needed` | Shared programme roles need validation | Not settled | Almere local and IZA/AZWA Flevoland | PGA transformation funding candidate; AZWA/D5/D6 split needed | `mun_almere_pga_transformatieplan`, `mun_almere_pga_current_home`, `reg_zonmw_doorontwikkeling_zorgzaam_flevoland` | How are PGA, Zorgzaam/Flever and AZWA work-agenda roles separated? | PGA/Zorgzaam Flevoland/Flever, Gemeente Almere, regional governance |
| Digitale en operationele infrastructuur | `review_needed` | Unknown | Unknown | Programme or project scale, needs validation | Unknown | `data/extracted/d6_governance_collaboration.json` | Which sources confirm RTP Almere, RSO, Monitoring@home and shared information picture for D6? | Gemeente Almere, regional digital/data leads, care partners |
| Burgerinitiatieven en informele steun | `review_needed` | Unknown | Citizen initiatives and volunteer/informal support candidates | Almere local | Unknown | `data/extracted/d6_governance_collaboration.json` | Which public local sources identify social-base partners, citizen initiatives and informal networks? | Gemeente Almere, De Schoor/VMCA/social-base partners |
| Financiering en budgetafbakening | `unknown` | Municipality and regional work-agenda governance need component-specific validation | Not settled | Mixed scale, must be split | Unknown | `data/extracted/workagenda_d5_operational_requirements.json` | How are AZWA-D6, D5, SPUK/GALA, PGA, municipal regular budget and Zvw/insurer funding separated per component? | Gemeente Almere finance, mandaatgemeente/regional table, insurer/work-agenda governance |

## Validation Status Per Row

No stakeholder validation session has been recorded yet. All rows remain in their pre-validation status.

| D6 component | Current status | Validation status | Ready to become `settled`? | Safe work-agenda wording | Unsafe wording |
| --- | --- | --- | --- | --- | --- |
| Inloopvoorzieningen sociaal en gezond | `review_needed` | Not yet validated | No | Almere must validate which inloop and social-base facilities are relevant to D6. | Almere has already designated specific inloopvoorzieningen as D6 infrastructure. |
| Wijkteams Almere | `inferred` | Not yet validated | No | Wijkteams Almere are a public-source-backed candidate for local access/social infrastructure validation. | Wijkteams Almere are formal D6 infrastructure. |
| Stevige Lokale Teams | `inferred` | Not yet validated | No | The SLT council route is relevant to D6 validation and touches JGZ Almere and wijkteams. | The SLT council decision settles D6 ownership or classification. |
| JGZ Almere | `inferred` | Not yet validated | No | JGZ Almere is a public-source-backed actor to validate for D6/JGZ and SLT-related roles. | JGZ Almere owns the D6 JGZ component. |
| GGD Flevoland-coordinatie | `inferred` | Not yet validated | No | GGD Flevoland has public-source-backed relevance for coordination, monitoring and prevention validation. | GGD Flevoland is confirmed as D6 owner for Almere. |
| Gezonde School / mentale gezonde school | `review_needed` | Not yet validated | No | Local implementation and ownership still need validation. | Almere has a settled D6 Gezonde School arrangement. |
| Kennis & Advies / monitoring / dashboards | `inferred` | Not yet validated | No | GGD Kennis & Advies is a candidate monitoring/data actor requiring D6-specific validation. | GGD Kennis & Advies owns D6 monitoring. |
| Samen Sterker in de Wijk | `inferred` | Not yet validated | No | Samen Sterker is a public-source-backed candidate for mental-health wijkinfrastructure validation. | Samen Sterker is formal D6 infrastructure. |
| PGA / Zorgzaam Flevoland-interface | `review_needed` | Not yet validated | No | PGA/Zorgzaam roles must be separated from AZWA/D5/D6 roles before drafting. | PGA/Zorgzaam is the D6 governance vehicle. |
| Digitale en operationele infrastructuur | `review_needed` | Not yet validated | No | Digital/operational infrastructure needs direct source or stakeholder validation. | RTP/RSO/Monitoring@home are confirmed D6 infrastructure for Almere. |
| Burgerinitiatieven en informele steun | `review_needed` | Not yet validated | No | Informal support and citizen initiatives need inventory and classification. | Named informal-support actors are D6 owners. |
| Financiering en budgetafbakening | `unknown` | Not yet validated | No | Funding must be mapped per component to prevent double counting. | D6 funding is already locally allocated. |

## Stakeholder Feedback Summary

No stakeholder feedback has been recorded yet. Use the validation log to add each session before changing register status, owner, executor, funding or safe wording.

Access status: stakeholder validation still needs to be conducted. The repository can supply the question structure and public-source prefill, but it cannot answer non-public/local validation points such as formal D6 classification, internal mandate, component-level budget allocation or safe local work-agenda wording. Use `docs/review/almere_d6_stakeholder_information_request.md` for first-round outreach.

Rows ready to become `settled`: none.

Rows remaining `inferred`:

- Wijkteams Almere.
- Stevige Lokale Teams.
- JGZ Almere.
- GGD Flevoland-coordinatie.
- Kennis & Advies / monitoring / dashboards.
- Samen Sterker in de Wijk / mentale-gezondheidswijkinfrastructuur.

Rows remaining `review_needed`:

- Inloopvoorzieningen sociaal en gezond.
- Gezonde School / mentale gezonde school.
- Positief Gezond Almere / Zorgzaam Flevoland-interface.
- Digitale en operationele infrastructuur.
- Burgerinitiatieven en informele steun.

Rows remaining `unknown`:

- Financiering en budgetafbakening.

## One Local Decision

Local decision id: `almere_2026_02_19_stevige_lokale_teams_geamendeerd_aangenomen`.

Source documents:

- `mun_almere_2026_stevige_lokale_teams_raad`.
- `mun_almere_2026_stevige_lokale_teams_geamendeerd_raadsvoorstel`.
- `mun_almere_2026_stevige_lokale_teams_besluitenlijst`.

What the decision settles:

- A public council decision route exists for Stevige Lokale Teams and inzet Investeringsfonds Jeugd en Gezin.
- The decision is relevant to SLT, JGZ Almere and wijkteams.

What the decision does not settle in this register:

- It does not by itself classify Stevige Lokale Teams as formal D6 infrastructure.
- It does not settle all D6 ownership, execution responsibility, monitoring responsibility or budget allocation.
- It does not settle whether Wijkteams Almere, JGZ Almere or related partners are formal D6 components or supporting infrastructure.

Touched D6 rows:

- Stevige Lokale Teams.
- Wijkteams Almere.
- JGZ Almere.
- Financiering en budgetafbakening.

Reason for zero `settled` rows:

The local decision is source-backed and important, but the D6 register is stricter than the local-decision file. A row becomes `settled` only when the source also settles the D6 responsibility question for that component: classification, owner, executor, scale and funding. That threshold has not yet been met.

## Stakeholder Validation Questions

Questions for Gemeente Almere:

- Which existing inloopvoorzieningen and social-base facilities count as D6 infrastructure?
- Is D6 ownership organized per component, per programme, or through another governance line?
- Which rows can be validated as Almere-local responsibilities, and which belong to regional governance?
- Which funding source applies per component?

Questions for GGD Flevoland:

- Which GGD tasks are D6-specific for Almere and which are regular public-health tasks?
- Who owns D6 monitoring and dashboard reporting?
- How should GGD-region scale be separated from IZA/AZWA Flevoland scale?

Questions for JGZ Almere:

- Which JGZ Almere roles are part of SLT development?
- Which JGZ roles support D6 but are not formal D6 infrastructure?
- What is the correct owner/executor language for JGZ-related rows?

Questions for Wijkteams Almere:

- Are Wijkteams Almere formal D6 infrastructure, supporting infrastructure, or candidate infrastructure to upgrade?
- Which organizations execute which wijkteam roles?
- How do wijkteams relate to Stevige Lokale Teams?

Questions for PGA/Zorgzaam Flevoland:

- Which PGA activities are relevant to D6 and which belong to another programme line?
- How should PGA, Zorgzaam/Flever and AZWA work-agenda governance be separated?
- Which D6 rows use PGA transformation funding, if any?

Questions for insurer/regional work-agenda governance:

- Which D6 components have a Zvw/insurer or work-agenda financing relation?
- Which responsibilities sit with the mandaatgemeente or regional table, and which sit with local execution owners?
- How should double funding be prevented across AZWA-D6, D5, SPUK/GALA, PGA and regular budgets?

## Source Appendix

Primary local and regional evidence currently used:

- Raad van Almere - Stevige Lokale Teams council page and Documentwijzer/Notubiz attachments.
- Wijkteams Almere.
- GGD Flevoland Begroting 2026.
- GGD Flevoland Kennis en Advies.
- GGD Flevoland JGZ Almere profile.
- Almere Samenwerkingsprojecten / Samen Sterker in de Wijk.
- Current Positief Gezond Almere homepage.
- PGA transformation plan and Zorgzaam Flevoland context.
- VNG Richtinggevend Kader toegang, lokale teams en integrale dienstverlening.
- Toezicht Sociaal Domein - Basisfuncties lokale teams.

## No-Overclaiming Warning

No D6 responsibility row is settled. This pack is a validation product. It should not be used as final public text, final bestuurlijke advice, final work-agenda text, final ownership recommendation or final budget-allocation advice.
