# Phase 31.5 - Regional Governance Deep-Research Intake

## Summary
Current state: `docs/dr/Regional governance.md` is an intake signal, not corpus evidence. The report identified a thin but important regional-governance actor set around Zorgzaam Flevoland: Verbindende Coalitie Zorgzaam Flevoland, Netwerkbureau Zorgzaam Flevoland, gemeente Almere as mandaatgemeente, and the need to keep province Flevoland separate from IZA/AZWA-regio Flevoland.

Current sprint: Sprint 31.5 - deep-research source intake and top-layer verification.

## Intake Decision
The deep-research report itself was not added to the source manifest. Selected public sources were added because they materially improve role separation, mandate wording and validation-question safety.

| Source ID | Treatment | Use | Boundary |
| --- | --- | --- | --- |
| `reg_noordoostpolder_iza_status_memo_2024` | Added | Verbindende Coalitie, subregional execution logic, Netwerkbureau setup and financing signal. | Does not prove final owner, host or mandate per D5/D6 component. |
| `reg_provincie_flevoland_verbindende_coalitie_2024` | Added | Transition from Zorgtafel to Verbindende Coalitie, province context, five-municipality IZA-regio note and Zeewolde split. | Does not make the province the IZA/AZWA actor or mandaatgemeente. |
| `reg_zonmw_zorgzaam_flevoland_project` | Added | Three subregions, PGA as subregion Zuid example and regional Netwerkbureau. | Project page is useful context, not formal local ownership. |
| `nat_dusi_spuk_iza_2023_2026` | Added | SPUK IZA mandate-structure, municipal coordination and mandaathouder context. | Does not settle local execution or Verbindende Coalitie/Netwerkbureau roles. |
| `nat_vws_spuk_iza_brede_spuk_mandaatgemeente_2025` | Added | SPUK IZA/Brede SPUK financing context with separate region and mandaatgemeente fields for Flevoland and Almere. | Use as two fields, not as a combined actor label. |
| `reg_centrumregeling_sociaal_domein_flevoland` | Added | Almere as centrumgemeente for specified social-domain cooperation tasks and mandate mechanics. | Not the same as IZA/AZWA mandaatgemeente or province wording. |
| `reg_proscoop_zorgzaam_flevoland_netwerkbureau_2024` | Added | Supporting evidence for coordinator/secretary contribution and Netwerkbureau support role. | Provider article; not proof of budget holder or formal owner. |
| `reg_ggd_flevoland_bestuursrapportage_aug_2024` | Added | GGD advisory and monitoring context around Netwerkbureau Zorgzaam Flevoland. | Does not settle D6 ownership or funding. |

## Deferred Signals
Vacancy mirrors and unstable role attachments for Netwerkbureau staffing were not added. They can be reconsidered only if stable public copies are found and the role evidence is stronger than the current official/project sources.

## Actor Guardrail
Use the following wording rules in research and generated outputs:

- `Almere` means gemeente Almere unless a source names a specific Almere programme or organisation.
- `Flevoland` must be qualified as province, IZA/AZWA-regio, GGD-regio, zorgkantoor/ROAZ context or broader regional wording.
- SPUK/mandaatgemeente tables should be read as two separate fields: regio Flevoland plus gemeente Almere as mandaatgemeente.
- Verbindende Coalitie Zorgzaam Flevoland is a regional steering/forum actor, not automatically a legal entity or owner.
- Netwerkbureau Zorgzaam Flevoland is a support-bureau actor, not automatically a mandaatgemeente, owner or budget holder.

## Top-Layer Verification
Verification must confirm that the new actors surface outside the intake note:

- `data/extracted/document_inventory.json` should include all eight selected source IDs.
- `data/extracted/claims/claims_master.jsonl` should include claims from the selected sources.
- `data/extracted/d6_governance_collaboration.json` should name Verbindende Coalitie Zorgzaam Flevoland and Netwerkbureau Zorgzaam Flevoland.
- `data/extracted/municipal/almere_d6_responsibility_register.json` should keep the PGA/Zorgzaam/Flevoland interface row `inferred`, not `settled`, while adding the new actors and source IDs.
- `data/workagenda/almere_regional_workagenda_input_objects.json` should carry the mandaatgemeente and coordination/support actor guardrails into regional handoff context.
- `data/site/site_sources_view.json` should surface the eight added source IDs.

## Verification Result
Regenerated on 2026-05-11. All eight selected source IDs are present in `data/raw/manifest.json`, `data/extracted/document_inventory.json`, `data/site/site_sources_view.json` and source view models.

Claim extraction surfaced each selected source in `data/extracted/claims/claims_master.jsonl`: `reg_noordoostpolder_iza_status_memo_2024` has 11 claims, `reg_provincie_flevoland_verbindende_coalitie_2024` 5, `reg_zonmw_zorgzaam_flevoland_project` 6, `nat_dusi_spuk_iza_2023_2026` 9, `nat_vws_spuk_iza_brede_spuk_mandaatgemeente_2025` 9, `reg_centrumregeling_sociaal_domein_flevoland` 11, `reg_proscoop_zorgzaam_flevoland_netwerkbureau_2024` 10 and `reg_ggd_flevoland_bestuursrapportage_aug_2024` 9.

Higher-layer actor check:

- `data/extracted/d6_governance_collaboration.json` names Verbindende Coalitie Zorgzaam Flevoland and Netwerkbureau Zorgzaam Flevoland and carries the actor-separation guardrail.
- `data/extracted/municipal/almere_d6_responsibility_register.json` includes both actors and all eight new source IDs in the PGA/Zorgzaam/Flevoland interface evidence while keeping decision status `inferred` and `needs_human_review: true`.
- `data/workagenda/almere_regional_workagenda_input_objects.json` includes the mandaatgemeente distinction and a `regional_coordination_entities` block for Verbindende Coalitie and Netwerkbureau.
- `data/extracted/claims/current_interpretation.json` does not synthesize these thin regional actors by name; for actor-aware work use the curated role map, D6 governance layer, D6 responsibility register and regional input object rather than relying on the current-interpretation summary alone.

Shorthand search was also run for combined Flevoland-and-Almere labels. Active generated data should not keep those labels as repository wording; use separate fields or named actors instead. One validation-workbook audit sample was rewritten by the audit builder to `gemeente Almere en de relevante Flevoland-schaal`.
