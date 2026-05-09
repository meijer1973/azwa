# Sprint 33 - Operational Deep-Research Intake

## Summary

Current sprint: Sprint 33.P7 is blocked pending the human internal dry run. This note records a targeted operational source intake carried out while send-readiness remains blocked.

The deep-research report in `docs/dr/azwa operational.md` is an intake signal, not a corpus source. It proposed operational examples and reusable implementation documents for D5 workagenda preparation. The selected public sources below were saved in the raw corpus, added to the manifest, processed through the pipeline and checked against top data layers.

## Intake Decision

The report produced good public source candidates for operational detail around valpreventie, Welzijn op Recept, vroegsignalering kwetsbare zwangeren, Kind naar Gezonder Gewicht, ggz-consultatiefunctie and brugfuncties between huisartsenzorg and sociaal domein.

These sources are useful for D5 validation prefill and workagenda design. They are not local Almere stakeholder validation and they do not settle ownership, component-level funding, coverage, local capacity, Zvw contracting, D6 classification or privacy/data accountability.

## Selected Sources

| Document ID | Source | Intake role | Boundary |
| --- | --- | --- | --- |
| `reg_ggd_flevoland_valpreventie_almere_ketendocument_2026` | Ketendocument Valpreventie Almere | Strong local operational source for Almere valpreventie chain design, roles, financing context and monitoring. | Still needs local validation before treating roles, funding or 2027 readiness as final workagenda truth. |
| `reg_ggd_flevoland_valpreventie_lelystad_2025` | Ketendocument Valpreventie Lelystad | Flevoland comparator for valpreventie chain steps, roles, inloopmomenten, financing and monitoring. | Lelystad source; not direct Almere proof. |
| `reg_amstellandzorg_welzijn_op_recept_procesflow_2024` | Procesflow Welzijn op Recept | Operational example for sociaal verwijzen/Welzijn op Recept route design and follow-up logic. | Amstelland source; only reusable as comparator or design input. |
| `reg_ros_friesland_zorgpad_vroegsignalering_zwangeren_2024` | Zorgpad Vroegsignalering Zwangeren Fryslan including PHB-JGZ | Operational example for Kansrijke Start / kwetsbare zwangeren task split and routing. | Friesland source; not Almere governance evidence. |
| `reg_samen_nijmegen_protocol_kwetsbare_zwangere_2024` | VSV protocol kwetsbare zwangere 6.0 | Operational example for VSV routing, kwetsbare zwangeren and MDO-style coordination. | Nijmegen source; not Almere governance evidence. |
| `nat_kind_naar_gezonder_gewicht_monitoring_matrix_2023` | Monitoring & Evaluatie matrix Kind naar Gezonder Gewicht | Reusable national monitoring matrix for Kind naar Gezonder Gewicht / overgewicht kinderen. | Monitoring aid; not a local funding or ownership decision. |
| `nat_leidraad_consultatiefunctie_ggz_sociaal_domein_2024` | Leidraad consultatiefunctie ggz voor het sociaal domein | Reusable national guidance for ggz consultation support to sociaal domein and MGN-related design. | National guidance; local implementation and funding remain validation questions. |
| `nat_pharos_brugfuncties_huisartsenzorg_sociaal_domein_2025` | Brugfuncties tussen huisartsenzorg en sociaal domein | Reusable national guidance for bridge functions, referral, feedback and role design between huisartsenzorg and sociaal domein. | National guidance; not a local Almere staffing or funding decision. |

## Top-Layer Verification

The pipeline run on 2026-05-09 processed the selected sources into the top layers.

| Check | Result |
| --- | --- |
| Document inventory | 117 documents total after intake; all eight selected operational sources are present. |
| Claims | 94 source-grounded claims were produced from the eight selected sources. |
| Source pages | Eight new source view models were created, including `/sources/ketendocument-valpreventie-almere/`, `/sources/brugfuncties-huisartsenzorg-en-sociaal-domein/` and `/sources/procesflow-welzijn-op-recept/`. |
| D5 operational layer | Valpreventie, Welzijn op Recept and brugfuncties are visible in `data/extracted/workagenda_d5_operational_requirements.json`. |
| Almere current view | Valpreventie, Welzijn op Recept, consultatiefunctie, brugfunctie, kwetsbare zwangeren and vroegsignalering are visible in `data/extracted/municipal/almere_current_view.json`. |
| D6 responsibility register | No D6 row moved to settled; the operational intake remains supporting context only. |

## Practical Use

Use the selected sources to sharpen D5 validation questions and workagenda field prefill:

- valpreventie: chain steps, GGD/projectlead role, municipal role, financing split and monitoring;
- sociaal verwijzen / Welzijn op Recept: routing, bridge function, feedback and follow-up;
- Kansrijke Start / kwetsbare zwangeren: task split, referral route, JGZ/VSV coordination and evidence fields;
- overgewicht kinderen: monitoring questions and Kind naar Gezonder Gewicht evaluation fields;
- MGN / ggz consultation: consultation function, role split and funding questions;
- D5-D6 dependency work: bridge functions and social-domain access infrastructure.

## Remaining Validation Boundary

Do not use this intake to fill final local answers. The following still require human validation, finance/controller confirmation or formal local decision evidence:

- Almere-local owner, coordinator and executor per D5 component;
- component-level funding and double-counting control;
- Zvw/insurer contracting or provider capacity;
- structural versus temporary continuation status;
- local coverage and capacity;
- ICT/privacy/data accountability;
- whether any operational component is also a formal D6 dependency.

