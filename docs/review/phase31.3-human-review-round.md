# Sprint 31.3 Human Review Round

## Summary
Current sprint: Sprint 31.3 - Reviewronde met menselijke beoordelaars.
Generated on: 2026-04-30.
Review items: 387.
Warnings: 6.
Review-level items: 381.
Unassigned items: 7.

This pack is for human reviewers. It does not settle policy, D6 ownership, funding, timing, or execution questions by itself.

## How To Use This Pack
- Reviewers should answer the questions for their perspective and cite the source, validation record, or decision basis they used.
- Treat lower-authority, local-adoption, funding, governance and execution signals as review prompts until confirmed.
- Record reviewer decisions separately from source claims. Do not rewrite the claim layer to match a judgement unless the judgement has source or validation evidence.
- D6 guardrail: Do not mark D6 responsibility-register rows as settled during Sprint 31.3. Sprint 25.6 remains parked until stakeholder validation records, local/internal documents, finance/controller confirmation, or an explicit policy decision exist.

## Monthly Source Audit Carry-In

- Audit generated on: 2026-04-30.
- Watchlist rows: 6.
- Pending replacements: 1.
- Pending timeline items: 3.
- Live link issues: 1.
- Live link review items: 1.
- Boundary: Pending sources and watchlist items are not public evidence until they are saved, added to the raw manifest, processed by the pipeline and represented in generated layers.

## Perspective Review Lists

### Norm

Review items: 202.

Reviewer questions:
- Welke bronhouder of bronsoort moet expliciet worden genoemd voordat deze normtaal veilig is?
- Is dit bindend, een afspraak, een verwachting, guidance of alleen context?

Top reason codes:
- `lower_authority_norm_signal`: 37
- `authority_unclear`: 30
- `municipality_relevance_inferred`: 27
- `actor_context_needs_role_split`: 21
- `execution_context_needs_action_split`: 16
- `expected_time_not_deadline`: 14
- `execution_sequencing_need`: 10
- `vague_region_actor`: 10

Sample items:
- `rvw_008` / `execution_capacity_need`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 1 execution capacity claim(s). Action: Use these as capacity questions; do not infer staffing, fte, or ownership.
- `rvw_011` / `execution_sequencing_need`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 3 execution sequencing claim(s). Action: Treat these as sequencing or phasing signals; do not turn them into a hard local implementation plan without source evidence.
- `rvw_012` / `expected_time_not_deadline`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 3 expected or indicative time claim(s). Action: Keep these as expected moments unless a stronger source establishes a formal deadline.
- `rvw_013` / `lower_authority_norm_signal`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 10 lower-authority norm signal claim(s). Action: Attribute these passages explicitly and do not present them as binding without a stronger source.
- `rvw_014` / `municipality_relevance_inferred`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 6 contextual claim(s) where municipal relevance is inferred rather than explicitly stated. Action: Review these claims before treating them as firm municipal obligations or implementation facts.

### Time

Review items: 172.

Reviewer questions:
- Is dit een formele deadline, een verwacht moment, een publicatiedatum of lokale planningscontext?
- Mag deze datum in publieke tekst als termijn worden gebruikt, of alleen als indicatieve planning?

Top reason codes:
- `execution_review_task`: 28
- `expected_time_not_deadline`: 22
- `execution_context_needs_action_split`: 22
- `authority_unclear`: 15
- `execution_sequencing_need`: 13
- `execution_dependency`: 12
- `actor_context_needs_role_split`: 12
- `local_planning_context_not_policy_deadline`: 10

Sample items:
- `rvw_010` / `execution_review_task`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 4 execution review or monitoring claim(s). Action: Keep these as review, monitoring, or validation tasks; do not present them as settled implementation choices.
- `rvw_012` / `expected_time_not_deadline`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 3 expected or indicative time claim(s). Action: Keep these as expected moments unless a stronger source establishes a formal deadline.
- `rvw_017` / `authority_unclear`: mun_almere_2024_2026_visie_gezondheidsbeleid contributes lower-authority claims that still require human review. Action: Keep these claims as contextual support only until a stronger primary source confirms or replaces them.
- `rvw_018` / `execution_decision_question`: mun_almere_2024_2026_visie_gezondheidsbeleid contains 2 execution decision-question claim(s). Action: Keep these as possible decision questions; do not present them as decided actions.
- `rvw_019` / `execution_review_task`: mun_almere_2024_2026_visie_gezondheidsbeleid contains 1 execution review or monitoring claim(s). Action: Keep these as review, monitoring, or validation tasks; do not present them as settled implementation choices.

### Money

Review items: 55.

Reviewer questions:
- Welke financieringsroute, budgetperiode of verantwoordingsregel volgt direct uit de bron?
- Welke lokale middelenmix, dekking of dubbeltelling blijft een finance/controller-vraag?

Top reason codes:
- `finance_context_needs_verification`: 13
- `lower_authority_norm_signal`: 10
- `actor_context_needs_role_split`: 9
- `authority_unclear`: 6
- `execution_sequencing_need`: 4
- `execution_dependency`: 3
- `vague_region_actor`: 2
- `execution_decision_question`: 2

Sample items:
- `rvw_027` / `execution_sequencing_need`: mun_almere_2024_2026_visie_gezondheidsbeleid_beleidstekst contains 2 execution sequencing claim(s). Action: Treat these as sequencing or phasing signals; do not turn them into a hard local implementation plan without source evidence.
- `rvw_029` / `lower_authority_norm_signal`: mun_almere_2024_2026_visie_gezondheidsbeleid_beleidstekst contains 6 lower-authority norm signal claim(s). Action: Attribute these passages explicitly and do not present them as binding without a stronger source.
- `rvw_031` / `vague_region_actor`: mun_almere_2024_2026_visie_gezondheidsbeleid_beleidstekst contains 1 claim(s) where 'regio' is the only detected actor signal. Action: Clarify whether the source means IZA/AZWA-regio, GGD-regio, zorgkantoorregio, ROAZ/subregio, province, mandaatgemeente, or practical execution structure before using this as a role claim.
- `rvw_037` / `lower_authority_norm_signal`: mun_almere_2024_2026_visie_gezondheidsbeleid_raadsvoorstel_geamendeerd contains 3 lower-authority norm signal claim(s). Action: Attribute these passages explicitly and do not present them as binding without a stronger source.
- `rvw_047` / `execution_dependency`: mun_almere_2024_2034_maatschappelijke_agenda_beleidstekst contains 3 execution dependency claim(s). Action: Name the dependency and keep it open unless a source shows it has been resolved.

### Governance

Review items: 75.

Reviewer questions:
- Noemt de bron besluitvorming, coordinatie, uitvoering, eigenaarschap, goedkeuring of alleen een actor?
- Welke actorrol moet expliciet door een mens worden bevestigd voordat de tekst sterker mag worden?

Top reason codes:
- `actor_context_needs_role_split`: 46
- `vague_region_actor`: 14
- `lower_authority_norm_signal`: 5
- `authority_unclear`: 3
- `regional_split_context`: 2
- `governance_gap`: 1
- `execution_sequencing_need`: 1
- `execution_context_needs_action_split`: 1

Sample items:
- `rvw_007` / `actor_context_needs_role_split`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 3 actor-context claim(s) without a more specific governance role. Action: Review these before treating an actor mention as decision-making, coordination, execution, approval, application, accountability or monitoring responsibility.
- `rvw_015` / `vague_region_actor`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 1 claim(s) where 'regio' is the only detected actor signal. Action: Clarify whether the source means IZA/AZWA-regio, GGD-regio, zorgkantoorregio, ROAZ/subregio, province, mandaatgemeente, or practical execution structure before using this as a role claim.
- `rvw_016` / `actor_context_needs_role_split`: mun_almere_2024_2026_visie_gezondheidsbeleid contains 3 actor-context claim(s) without a more specific governance role. Action: Review these before treating an actor mention as decision-making, coordination, execution, approval, application, accountability or monitoring responsibility.
- `rvw_023` / `actor_context_needs_role_split`: mun_almere_2024_2026_visie_gezondheidsbeleid_beleidstekst contains 1 actor-context claim(s) without a more specific governance role. Action: Review these before treating an actor mention as decision-making, coordination, execution, approval, application, accountability or monitoring responsibility.
- `rvw_031` / `vague_region_actor`: mun_almere_2024_2026_visie_gezondheidsbeleid_beleidstekst contains 1 claim(s) where 'regio' is the only detected actor signal. Action: Clarify whether the source means IZA/AZWA-regio, GGD-regio, zorgkantoorregio, ROAZ/subregio, province, mandaatgemeente, or practical execution structure before using this as a role claim.

### Locality

Review items: 269.

Reviewer questions:
- Is de claim expliciet Almere, expliciet Flevoland, algemeen landelijk of alleen lokaal relevant door interpretatie?
- Welke lokale bron of stakeholdervalidatie is nodig voordat dit als Almeerse keuze kan worden geschreven?

Top reason codes:
- `actor_context_needs_role_split`: 36
- `municipality_relevance_inferred`: 30
- `lower_authority_norm_signal`: 29
- `national_claim_local_relevance`: 22
- `authority_unclear`: 21
- `execution_review_task`: 19
- `execution_sequencing_need`: 14
- `expected_time_not_deadline`: 14

Sample items:
- `rvw_007` / `actor_context_needs_role_split`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 3 actor-context claim(s) without a more specific governance role. Action: Review these before treating an actor mention as decision-making, coordination, execution, approval, application, accountability or monitoring responsibility.
- `rvw_008` / `execution_capacity_need`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 1 execution capacity claim(s). Action: Use these as capacity questions; do not infer staffing, fte, or ownership.
- `rvw_009` / `execution_dependency`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 1 execution dependency claim(s). Action: Name the dependency and keep it open unless a source shows it has been resolved.
- `rvw_010` / `execution_review_task`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 4 execution review or monitoring claim(s). Action: Keep these as review, monitoring, or validation tasks; do not present them as settled implementation choices.
- `rvw_011` / `execution_sequencing_need`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 3 execution sequencing claim(s). Action: Treat these as sequencing or phasing signals; do not turn them into a hard local implementation plan without source evidence.

### Execution

Review items: 345.

Reviewer questions:
- Is dit een feitelijke uitvoeringsactiviteit, een mogelijke opvolgactie, een afhankelijkheid of een reviewtaak?
- Welke actie, volgorde, capaciteit of eigenaar mag niet worden ingevuld zonder lokale bevestiging?

Top reason codes:
- `actor_context_needs_role_split`: 41
- `lower_authority_norm_signal`: 33
- `execution_review_task`: 31
- `municipality_relevance_inferred`: 30
- `execution_context_needs_action_split`: 28
- `authority_unclear`: 26
- `execution_dependency`: 23
- `execution_sequencing_need`: 23

Sample items:
- `rvw_007` / `actor_context_needs_role_split`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 3 actor-context claim(s) without a more specific governance role. Action: Review these before treating an actor mention as decision-making, coordination, execution, approval, application, accountability or monitoring responsibility.
- `rvw_008` / `execution_capacity_need`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 1 execution capacity claim(s). Action: Use these as capacity questions; do not infer staffing, fte, or ownership.
- `rvw_009` / `execution_dependency`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 1 execution dependency claim(s). Action: Name the dependency and keep it open unless a source shows it has been resolved.
- `rvw_010` / `execution_review_task`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 4 execution review or monitoring claim(s). Action: Keep these as review, monitoring, or validation tasks; do not present them as settled implementation choices.
- `rvw_011` / `execution_sequencing_need`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 3 execution sequencing claim(s). Action: Treat these as sequencing or phasing signals; do not turn them into a hard local implementation plan without source evidence.

## Decision Recording Rule
Reviewer decisions must be recorded as human review decisions or validation records. They do not become source claims unless backed by a canonical source or explicit validation evidence.
