# Sprint 31.4 Review Triage And Deep-Research Offload

## Summary
Current sprint: Sprint 31.4 - Review triage and deep-research offload.
Generated on: 2026-04-30.
Review queue items triaged: 565.
Deep-research assignments prepared: 6.
D6 rows still requiring human validation: 12.
D6 rows with named public-search gaps: 0.

Send only public-source gaps, authority/source hierarchy checks, explicit local adoption searches and source-replacement searches to deep research agents. Keep ownership, mandate, funding, D6 classification and settled-status decisions with human stakeholders or policy owners.

## Triage Buckets

| Bucket | Item count | What it means | Top reason codes |
| --- | ---: | --- | --- |
| `human_only` | 76 | Requires policy judgement, stakeholder validation, finance/controller confirmation, or local mandate clarification. | `execution_review_task` (43), `execution_capacity_need` (17), `execution_decision_question` (13), `table_extraction_missing` (1), `governance_gap` (1) |
| `deep_research_candidate` | 309 | May be reducible by a careful public-source search for stronger sources, clearer dates, actor scope, or explicit local adoption. | `lower_authority_norm_signal` (65), `municipality_relevance_inferred` (58), `authority_unclear` (54), `expected_time_not_deadline` (32), `national_claim_local_relevance` (24) |
| `mixed_public_search_then_human` | 163 | Public search may clarify the source basis, but final role, action, sequencing or responsibility language may still need human validation. | `actor_context_needs_role_split` (61), `execution_context_needs_action_split` (43), `execution_sequencing_need` (30), `execution_dependency` (29) |
| `pipeline_or_extraction_cleanup` | 17 | Mostly repository/pipeline cleanup rather than policy review. | `missing_d6_content` (8), `missing_d5_content` (6), `extraction_noise_detected` (3) |

## Human-Only D6 Rows

These rows still need policy-owner, stakeholder, finance/controller or internal-document validation. Do not send them to deep research as if public search can settle them.

- Burgerinitiatieven en informele steun
- Digitale en operationele infrastructuur
- Financiering en budgetafbakening
- GGD Flevoland-coordinatie
- Gezonde School / mentale gezonde school
- Inloopvoorzieningen sociaal en gezond
- JGZ Almere
- Kennis & Advies / monitoring / dashboards
- Positief Gezond Almere / Zorgzaam Flevoland-interface
- Samen Sterker in de Wijk / mentale-gezondheidswijkinfrastructuur
- Stevige Lokale Teams
- Wijkteams Almere

## D6 Rows With Public-Search Gaps

Deep research may look for additional public sources for these rows, but it may not settle classification, owner, mandate or funding.


## Deep-Research Assignments

| Assignment | D6 rows | Search question | May resolve | Must not resolve |
| --- | --- | --- | --- | --- |
| `dr_gezonde_school_almere` Gezonde School / mentale gezonde school Almere | Gezonde School / mentale gezonde school, JGZ Almere | Find public Almere, GGD/JGZ, school-board or programme sources that show whether and how Gezonde School or mental-health school prevention is implemented in Almere, who coordinates it, and whether it is linked to D6, JGZ or SLT. | public-source gap, implementation evidence, candidate owner/executor evidence | formal D6 classification, funding allocation, mandate without local validation |
| `dr_digitale_operationele_infrastructuur` Digital and operational infrastructure for D6 Almere/Flevoland | Digitale en operationele infrastructuur, Kennis & Advies / monitoring / dashboards | Find public sources for RTP Almere, RSO, Monitoring@home, shared information picture, regional data infrastructure or digital cooperation that are relevant to D5/D6 execution in Almere/Flevoland. | named-source gap, actor/context evidence, scope evidence | D6 ownership, budget split, formal governance role |
| `dr_burgerinitiatieven_informele_steun` Burgerinitiatieven, informele steun and social-base access | Burgerinitiatieven en informele steun, Inloopvoorzieningen sociaal en gezond | Find public Almere sources that identify social-base partners, volunteer support, citizen initiatives, informal care, walk-in/access points or inloopvoorzieningen relevant to D6 basisinfrastructuur. | local inventory candidates, public-source evidence, partner mapping | formal D6 classification, assigned responsibility, confirmed funding |
| `dr_pga_zorgzaam_flever_interface` PGA / Zorgzaam Flevoland / Flever interface | Positief Gezond Almere / Zorgzaam Flevoland-interface, Financiering en budgetafbakening | Find public sources that clarify the relation between Positief Gezond Almere, Zorgzaam Flevoland, Flever, IZA/AZWA work-agenda governance, transformation funding and D5/D6 execution. | programme-role evidence, public funding context, interface terminology | component-level budget allocation, formal D6 governance vehicle, controller validation |
| `dr_samen_sterker_wijk` Samen Sterker in de Wijk source strengthening | Samen Sterker in de Wijk / mentale-gezondheidswijkinfrastructuur | Find public sources beyond the current Almere page that describe Samen Sterker in de Wijk governance, project status, partners, funding, evaluation, or relation to mental-health neighbourhood infrastructure. | project evidence, partner evidence, public implementation context | formal D6 status, owner/coordinator without validation, funding assignment |
| `dr_stronger_authority_sources` Stronger public source hunt for review-queue authority/adoption items | Cross-cutting review queue | For high-volume review reasons such as authority_unclear, lower_authority_norm_signal, municipality_relevance_inferred and national_claim_local_relevance, search whether stronger public sources exist in the corpus domains or official publisher sites. | authority hierarchy, public-source replacement, explicit local adoption evidence | human policy judgement, non-public decision status, local validation |

## D6 Guardrail
No D6 responsibility-register row may move to settled from a deep research result alone. A deep research result can add source candidates or reduce public-source gaps; formal classification, ownership, mandate and funding still need validation evidence.
