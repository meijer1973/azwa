# Sprint 31.5 Informal Support Deep-Research Intake

## Summary
Current sprint: Sprint 31.5 - Deep-research source intake and top-layer verification.

This note records the repository-side intake of `docs/dr/Informal support.md`. The deep-research report is not a source. It was used only to identify public-source candidates for the D6 rows `inloopvoorzieningen_sociaal_en_gezond` and `citizen_initiatives_informal_support`.

## Intake Decision
Selected public sources were added because they materially strengthen the public-source basis for informal support, neighbourhood meeting places, citizen initiatives, mantelzorg, volunteer support, and low-threshold social-base access in Almere.

The intake deliberately does not settle formal D6 classification, ownership, mandate, coordination, structural funding or final work-agenda wording.

## Added Sources
| Source ID | Source | Role in repository |
|---|---|---|
| `mun_almere_welzijnskader_2020` | Welzijnskader: WELzijn in Almere | Municipal social-base policy frame; dated source, use with current pages. |
| `mun_almere_subsidie_buurtontmoeting` | Financiele ondersteuning voor (buurt)ontmoeting | Current municipal subsidy route for neighbourhood meeting places and activities. |
| `mun_almere_nadere_regels_buurtontmoeting` | Nadere regels (buurt)ontmoetingsplekken en -activiteiten | Municipal rules, criteria, cofinancing and anti-double-funding signal. |
| `mun_almere_wijkbudget` | Wijkbudget | Municipal resident-initiative funding route. |
| `mun_almere_ondersteuning_mantelzorg` | Ondersteuning voor mantelzorg | Municipal informal-care support route through Wmo and VMCA. |
| `mun_almere_mantelzorgwaardering` | Mantelzorgwaardering | Municipal mantelzorgwaardering and VMCA role signal. |
| `mun_almere_sociaal_domein_aanbod_jeugd_gezin` | Aanbod jeugd en gezin | Preventive referral/inventory route and Sociale Kaart Flevoland signal. |
| `mun_almere_sociale_veerkracht_almeerders` | Sociale veerkracht van Almeerders | Municipal-commissioned social-base advice and gap framing. |
| `mun_deschoor_buurtkamers` | De Schoor Buurtkamers | Partner implementation source for named meeting places. |
| `mun_deschoor_initiatievenbureau` | De Schoor Initiatievenbureau | Partner implementation source for resident-initiative support. |
| `mun_deschoor_buurtkracht` | De Schoor Buurtkracht | Partner implementation source for neighbourhood activation. |
| `mun_deschoor_opbouwwerk_almere` | De Schoor Opbouwwerk in Almere | Partner implementation source for opbouwwerk and wijkteam link. |
| `mun_vmca_meerjarenvisie_2022_2025` | VMCA Meerjarenvisie 2022-2025 | Partner policy source for volunteer work, mantelzorg and wijkteam contribution. |
| `mun_humanitas_almere` | Humanitas Almere | Supporting local volunteer-support mapping source. |
| `mun_almere_almeers_preventieakkoord` | Almeers Preventieakkoord | Municipal prevention-network bridge source. |
| `mun_almere_wijkteams_ontmoeting` | Wijkteams Almere Ontmoeting | Current social-contact/access route with VMCA, Humanitas and De Schoor links. |

## Deferred or Lower-Priority Candidates
- Older Humanitas brochures were not prioritized because a current local Humanitas Almere page was available.
- Gebiedsmarkt and wijkbijeenkomst pages were treated as optional live-inventory signals. They can be searched later if a specific row still needs neighbourhood-level examples, but broad searching is no longer needed for the D6 register prefill.

## Top-Layer Verification Target
The intake is successful only if:

- all selected source IDs appear in `data/raw/manifest.json`;
- all selected source IDs appear in `data/extracted/document_inventory.json`;
- `data/extracted/municipal/almere_d6_responsibility_register.json` keeps both affected rows conservative;
- both affected rows remain non-`settled` and `needs_human_review: true`;
- public-site update pages and internal dashboard update history mention the intake as a clickable update.

## Verified Result
After pipeline regeneration, the D6 register shows:

- `inloopvoorzieningen_sociaal_en_gezond`: `decision_status` is `inferred`, evidence-backed, human review still required.
- `citizen_initiatives_informal_support`: `decision_status` is `inferred`, evidence-backed, human review still required.
- No D6 row moved to `settled`.

