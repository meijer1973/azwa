# Sprint 31.5 PGA / Zorgzaam Flevoland / Flever Deep-Research Intake

## Summary
Current sprint: Sprint 31.5 - Deep-research bronintake en top-layer verificatie.

`docs/dr/Zorgzaam Flevoland, and Flever interface.md` is treated as a source-discovery signal, not as evidence. The selected public sources below were added to the formal corpus and the top layers were checked for whether the PGA/Zorgzaam/Flever interface is represented more clearly without moving any D6 responsibility row to `settled`.

## Selected Sources

| Document ID | Source | Why selected |
| --- | --- | --- |
| `reg_ggd_flevoland_kadernota_2025` | GGD Flevoland Kadernota 2025 | Regional public-authority source for GALA, Regiobeeld/Regioplan, PGA monitoring and GGD advisory role. |
| `reg_flever_zorgzaam_flevoland_project` | Flever Zorgzaam Flevoland project page | Public role-splitting source: Zorgzaam Flevoland as regional IZA movement and Flever as resident-perspective support actor. |
| `reg_flever_meerjarenplan_2025_2028` | Flever Meerjarenplan 2025-2028 | Supporting role/context source for Flever's regional network, participation and research functions. |
| `reg_flever_inwoners_onderdeel_pga` | Inwoners onderdeel van Positief Gezond Almere | Narrow partner-role source for Flever's project-lead support around inwonerparticipatie within PGA. |

## Already Present

| Source | Repository status |
| --- | --- |
| PGA transformatieplan | Already present as `mun_almere_pga_transformatieplan`. |
| National Zorgakkoorden/VWS PGA approval and EUR 20 million funding context | Already present as `nat_zorgakkoorden_pga_20_miljoen_2024`. |
| Regioplan IZA Flevoland / Zorgzaam Flevoland 2023 | Already present as `reg_flevoland_2023_regioplan_iza`. |
| ZonMw Zorgzaam Flevoland project | Already present as `reg_zonmw_doorontwikkeling_zorgzaam_flevoland`. |
| GGD Flevoland Begroting 2026 | Already present as `reg_ggd_flevoland_begroting_2026`. |

## Top-Layer Verification Target

The intake should make the row `pga_zorgzaam_flevoland_interface` show stronger public prefill:

- PGA as local transformation programme with approved IZA funding context;
- Zorgzaam Flevoland as regional IZA/regioplan movement and governance-development structure;
- Flever as supporting participation and connecting actor;
- GGD Flevoland as monitoring/advisory/prevention actor;
- no public-source settlement of formal D6 classification, final owner, mandate or component-level budget allocation.

## Verified Result

After pipeline processing, the expected result is:

- `data/raw/manifest.json` includes the four new public sources;
- `data/extracted/document_inventory.json` includes the four new public sources;
- `data/extracted/municipal/almere_d6_responsibility_register.json` keeps `pga_zorgzaam_flevoland_interface` as `inferred`, not `settled`;
- the row includes the new role-splitting evidence sources;
- `needs_human_review` remains `true`;
- public-search gaps are reduced, but formal D6 governance and financing questions remain stakeholder or policy validation.

## Remaining Human-Only Questions

- Is PGA formal D6 infrastructure, adjacent programme infrastructure, or implementation context?
- Is Zorgzaam Flevoland a formal governance layer for this D6 component or a regional collaboration context?
- Does Flever have any formal coordinator responsibility beyond public participation/support roles?
- Which actor owns the interface for work-agenda purposes?
- Which funding line applies per component after current IZA/PGA/GALA arrangements?
