# Sprint 31.5 Digital and Operational Infrastructure Deep-Research Intake

## Summary
Current sprint: Sprint 31.5 - Deep-research bronintake en top-layer verificatie.

`docs/dr/Digital and operational infrastructure.md` is treated as a source-discovery signal, not as evidence. The intake goal is to strengthen the public-source basis for the D6 row `digital_operational_infrastructure` and then verify whether the findings appear in the manifest, document inventory, D6 responsibility register, review documents, site updates and tests.

## Selected Sources

| Source ID | Source | Why selected |
| --- | --- | --- |
| `nat_zorgakkoorden_pga_20_miljoen_2024` | Zorgakkoorden/VWS news page on EUR 20 million for PGA | Official context for PGA transformation funding; not component-level D6 funding. |
| `mun_almere_pga_regionaal_transferpunt` | PGA Regionaal Transferpunt page | Programme evidence for RTP as operational care-coordination project. |
| `reg_flevoziekenhuis_rtp_flevoland_2025` | Flevoziekenhuis RTP launch page | Provider evidence that RTP Flevoland is live and originated from PGA. |
| `reg_rtp_flevoland_home` | RTP Flevoland home page | Live operational service evidence for RTP scope, access and care questions. |
| `mun_almere_pga_rso_data_infrastructuur` | PGA RSO/data-infrastructure page | Public source for RSO, data-infrastructure and shared-information capability. |
| `reg_flevoziekenhuis_thuismonitoring` | Flevoziekenhuis thuismonitoring page | Concrete telemonitoring/remote-monitoring source in Almere. |
| `reg_ggd_flevoland_kadernota_2027` | GGD Flevoland Kadernota 2027 | Strong GGD source for data, monitoring, Kennis & Advies and AZWA/GALA/IZA links. |
| `reg_woonzorg_flevoland_beleidsplan_2026` | Woonzorg Flevoland beleidsplan 2026 | Provider-side corroboration of PGA, RSO, data exchange and care coordination. |
| `reg_npz_almere_pilot_viewer_acp` | NPZ Almere Pilot viewer-ACP | Concrete Almere data-sharing use case for ACP/PZP. |
| `reg_npz_almere_evaluatie_viewer_pzp_acp_2025` | NPZ Almere viewer PZP/ACP evaluation | Evaluates the pilot and documents mandate/implementation questions. |
| `nat_palliaweb_digitale_initiatieven_pzp` | Palliaweb digital PZP initiatives overview | National/sector corroboration that PGA is a named PZP digital initiative. |
| `reg_npz_almere_jaarplan_2025` | NPZ Almere Jaarplan 2025 | Source for intended ACP/PZP data-exchange work and evaluation action. |

## Deferred Or Substituted Sources

- `reg_flevoland_2023_regioplan_iza`, `mun_almere_pga_transformatieplan`, `mun_almere_pga_current_home`, `reg_ggd_flevoland_begroting_2026` and `reg_ggd_flevoland_kennis_en_advies` were already in the formal corpus and are reused rather than duplicated.
- The deep-research report mentioned `Jaarverslag NPZAlmere 2025`. The URL found by search returned a 404 to the local downloader on 2026-04-30, so it is not ingested. Stable NPZ pilot, evaluation and year-plan sources are used instead.
- The selected sources do not settle D6 ownership, mandate, data-controller roles, privacy/security architecture or structural funding.

## Top-Layer Verification Targets

- `data/raw/manifest.json` contains source IDs 64-75.
- `data/extracted/document_inventory.json` marks the sources as digital/operational, monitoring, governance or implementation context where relevant.
- `data/extracted/municipal/almere_d6_responsibility_register.json` changes `digital_operational_infrastructure` from a public-source gap to source-backed prefill/inferred, while keeping human review required and `settled` false.
- Review documents narrow the remaining question from "is there public evidence?" to "how should the subcomponents be classified, owned, governed and funded?"
- Tests verify that the deep-research report itself is not in the raw manifest and that the selected public sources appear in the top layers.
