# Sprint 31.5 - Samen Sterker Deep Research Intake

## Summary

Current sprint: Sprint 31.5 - Deep-research bronintake en top-layer verificatie.

The deep-research report in `docs/dr/Samen Sterker in de Wijk in Almere.md` is an intake signal, not a corpus source. The report was used to identify public sources that should be processed through the normal source pipeline and then checked against the top data layers.

## Intake Result

The public source base for Samen Sterker in de Wijk has been strengthened. The new source set supports the finding that Samen Sterker is an active mental-health neighbourhood initiative with municipal, regional, ZonMw, PGA and project-level evidence.

The sources do not settle formal D6 classification, final owner/coordinator, mandate, citywide or pilot status, structural/component funding, accepted evaluation steering, or the formal relation to Stevige Lokale Teams.

## Selected Sources

| Document ID | Source | Intake reason |
| --- | --- | --- |
| `reg_almere_zorglandschap_wmo` | Regio Almere - Zorglandschap Wmo | Regional programme context for mental-health support landscape. |
| `reg_zorglandschap_wmo_uitvoeringsprogramma_2022` | Uitvoeringsprogramma Zorglandschap Wmo Flevoland 2022 | Programme source for Samen Sterker start, method, partners and expansion. |
| `reg_zorglandschap_wmo_monitor_2025` | Monitor Zorglandschap Wmo 2025 | Current regional monitor and cross-domain implementation context. |
| `reg_zonmw_samen_sterker_uitvoeringsplan` | ZonMw uitvoeringsplan Samen Sterker | Public programme/funding timeline evidence. |
| `reg_zonmw_samen_sterker_startsubsidie` | ZonMw Samen sterker in de wijk | Historical start-subsidy and programme evidence. |
| `mun_almere_pga_samen_sterker_wijk` | PGA Samen Sterker in de Wijk | Row-specific PGA project context. |
| `mun_almere_subsidieregister_2023` | Gemeente Almere Subsidieregister 2023 | Public funding trace, not structural D6 proof. |
| `mun_almere_evaluatie_schakelteams_2021` | Evaluatie schakelteams | Adjacent historical interface evidence. |
| `reg_samen_sterker_in_de_wijk_home` | Samen Sterker in de Wijk project site | Current lower-authority project framing. |

## Already Present Sources

The intake also reuses existing corpus sources:

- `mun_almere_samenwerkingsprojecten`
- `mun_almere_pga_transformatieplan`
- `mun_almere_pga_seo_businesscase_2024`
- `reg_flevoland_2023_regioplan_iza`
- `nat_zorgakkoorden_pga_20_miljoen_2024`
- `mun_almere_pga_current_home`

## Top-Layer Verification Target

After pipeline regeneration, verify:

- all selected sources appear in `data/raw/manifest.json`;
- all selected sources appear in `data/extracted/document_inventory.json`;
- generated document and claim files exist for the selected sources;
- the D6 register row `samen_sterker_wijk_mental_health` includes the selected evidence sources;
- the row remains `inferred`, not `settled`;
- the row keeps `needs_human_review: true`;
- review handoff documents keep D6 classification, owner, mandate and funding as validation questions.

## Human-Only Questions

These cannot be resolved from the public source set alone:

- Is Samen Sterker formal D6 infrastructure, adjacent infrastructure, or implementation context?
- Who owns, coordinates and executes the D6-relevant part?
- Is the work citywide, wijk-specific, pilot-based or programme-specific?
- Which funding line applies now and structurally?
- Is there a formal relation to Stevige Lokale Teams?
- Which evaluation conclusions are accepted for steering and which remain project learning?
