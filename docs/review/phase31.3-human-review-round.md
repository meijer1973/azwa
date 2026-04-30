# Sprint 31.3 Human Review Round

## Summary
Current sprint: Sprint 31.3 - Reviewronde met menselijke beoordelaars.
Generated on: 2026-04-30.
Review items: 565.
Warnings: 15.
Review-level items: 550.
Unassigned items: 15.

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

Review items: 330.

Reviewer questions:
- Welke bronhouder of bronsoort moet expliciet worden genoemd voordat deze normtaal veilig is?
- Is dit bindend, een afspraak, een verwachting, guidance of alleen context?

Top reason codes:
- `lower_authority_norm_signal`: 65
- `municipality_relevance_inferred`: 55
- `authority_unclear`: 54
- `execution_context_needs_action_split`: 32
- `actor_context_needs_role_split`: 28
- `expected_time_not_deadline`: 18
- `vague_region_actor`: 16
- `execution_sequencing_need`: 15

Sample items:
- `rvw_017` / `execution_capacity_need`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 2 execution capacity claim(s). Action: Use these as capacity questions; do not infer staffing, fte, or ownership.
- `rvw_020` / `execution_sequencing_need`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 2 execution sequencing claim(s). Action: Treat these as sequencing or phasing signals; do not turn them into a hard local implementation plan without source evidence.
- `rvw_021` / `expected_time_not_deadline`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 3 expected or indicative time claim(s). Action: Keep these as expected moments unless a stronger source establishes a formal deadline.
- `rvw_022` / `lower_authority_norm_signal`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 9 lower-authority norm signal claim(s). Action: Attribute these passages explicitly and do not present them as binding without a stronger source.
- `rvw_023` / `municipality_relevance_inferred`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 5 contextual claim(s) where municipal relevance is inferred rather than explicitly stated. Action: Review these claims before treating them as firm municipal obligations or implementation facts.

### Time

Review items: 231.

Reviewer questions:
- Is dit een formele deadline, een verwacht moment, een publicatiedatum of lokale planningscontext?
- Mag deze datum in publieke tekst als termijn worden gebruikt, of alleen als indicatieve planning?

Top reason codes:
- `execution_review_task`: 40
- `expected_time_not_deadline`: 32
- `authority_unclear`: 30
- `execution_context_needs_action_split`: 25
- `execution_sequencing_need`: 17
- `execution_dependency`: 14
- `actor_context_needs_role_split`: 14
- `local_planning_context_not_policy_deadline`: 11

Sample items:
- `rvw_019` / `execution_review_task`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 4 execution review or monitoring claim(s). Action: Keep these as review, monitoring, or validation tasks; do not present them as settled implementation choices.
- `rvw_021` / `expected_time_not_deadline`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 3 expected or indicative time claim(s). Action: Keep these as expected moments unless a stronger source establishes a formal deadline.
- `rvw_026` / `authority_unclear`: mun_almere_2024_2026_visie_gezondheidsbeleid contributes lower-authority claims that still require human review. Action: Keep these claims as contextual support only until a stronger primary source confirms or replaces them.
- `rvw_027` / `execution_decision_question`: mun_almere_2024_2026_visie_gezondheidsbeleid contains 2 execution decision-question claim(s). Action: Keep these as possible decision questions; do not present them as decided actions.
- `rvw_028` / `execution_review_task`: mun_almere_2024_2026_visie_gezondheidsbeleid contains 1 execution review or monitoring claim(s). Action: Keep these as review, monitoring, or validation tasks; do not present them as settled implementation choices.

### Money

Review items: 56.

Reviewer questions:
- Welke financieringsroute, budgetperiode of verantwoordingsregel volgt direct uit de bron?
- Welke lokale middelenmix, dekking of dubbeltelling blijft een finance/controller-vraag?

Top reason codes:
- `finance_context_needs_verification`: 18
- `actor_context_needs_role_split`: 9
- `lower_authority_norm_signal`: 8
- `execution_sequencing_need`: 4
- `authority_unclear`: 4
- `execution_dependency`: 3
- `vague_region_actor`: 2
- `execution_decision_question`: 2

Sample items:
- `rvw_036` / `execution_sequencing_need`: mun_almere_2024_2026_visie_gezondheidsbeleid_beleidstekst contains 2 execution sequencing claim(s). Action: Treat these as sequencing or phasing signals; do not turn them into a hard local implementation plan without source evidence.
- `rvw_038` / `lower_authority_norm_signal`: mun_almere_2024_2026_visie_gezondheidsbeleid_beleidstekst contains 5 lower-authority norm signal claim(s). Action: Attribute these passages explicitly and do not present them as binding without a stronger source.
- `rvw_040` / `vague_region_actor`: mun_almere_2024_2026_visie_gezondheidsbeleid_beleidstekst contains 1 claim(s) where 'regio' is the only detected actor signal. Action: Clarify whether the source means IZA/AZWA-regio, GGD-regio, zorgkantoorregio, ROAZ/subregio, province, mandaatgemeente, or practical execution structure before using this as a role claim.
- `rvw_046` / `lower_authority_norm_signal`: mun_almere_2024_2026_visie_gezondheidsbeleid_raadsvoorstel_geamendeerd contains 5 lower-authority norm signal claim(s). Action: Attribute these passages explicitly and do not present them as binding without a stronger source.
- `rvw_056` / `execution_dependency`: mun_almere_2024_2034_maatschappelijke_agenda_beleidstekst contains 3 execution dependency claim(s). Action: Name the dependency and keep it open unless a source shows it has been resolved.

### Governance

Review items: 95.

Reviewer questions:
- Noemt de bron besluitvorming, coordinatie, uitvoering, eigenaarschap, goedkeuring of alleen een actor?
- Welke actorrol moet expliciet door een mens worden bevestigd voordat de tekst sterker mag worden?

Top reason codes:
- `actor_context_needs_role_split`: 61
- `vague_region_actor`: 21
- `lower_authority_norm_signal`: 4
- `authority_unclear`: 2
- `regional_split_context`: 2
- `governance_gap`: 1
- `execution_sequencing_need`: 1
- `execution_context_needs_action_split`: 1

Sample items:
- `rvw_016` / `actor_context_needs_role_split`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 3 actor-context claim(s) without a more specific governance role. Action: Review these before treating an actor mention as decision-making, coordination, execution, approval, application, accountability or monitoring responsibility.
- `rvw_024` / `vague_region_actor`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 1 claim(s) where 'regio' is the only detected actor signal. Action: Clarify whether the source means IZA/AZWA-regio, GGD-regio, zorgkantoorregio, ROAZ/subregio, province, mandaatgemeente, or practical execution structure before using this as a role claim.
- `rvw_025` / `actor_context_needs_role_split`: mun_almere_2024_2026_visie_gezondheidsbeleid contains 3 actor-context claim(s) without a more specific governance role. Action: Review these before treating an actor mention as decision-making, coordination, execution, approval, application, accountability or monitoring responsibility.
- `rvw_032` / `actor_context_needs_role_split`: mun_almere_2024_2026_visie_gezondheidsbeleid_beleidstekst contains 1 actor-context claim(s) without a more specific governance role. Action: Review these before treating an actor mention as decision-making, coordination, execution, approval, application, accountability or monitoring responsibility.
- `rvw_040` / `vague_region_actor`: mun_almere_2024_2026_visie_gezondheidsbeleid_beleidstekst contains 1 claim(s) where 'regio' is the only detected actor signal. Action: Clarify whether the source means IZA/AZWA-regio, GGD-regio, zorgkantoorregio, ROAZ/subregio, province, mandaatgemeente, or practical execution structure before using this as a role claim.

### Locality

Review items: 427.

Reviewer questions:
- Is de claim expliciet Almere, expliciet Flevoland, algemeen landelijk of alleen lokaal relevant door interpretatie?
- Welke lokale bron of stakeholdervalidatie is nodig voordat dit als Almeerse keuze kan worden geschreven?

Top reason codes:
- `municipality_relevance_inferred`: 58
- `lower_authority_norm_signal`: 55
- `actor_context_needs_role_split`: 51
- `authority_unclear`: 43
- `execution_review_task`: 31
- `execution_context_needs_action_split`: 28
- `national_claim_local_relevance`: 24
- `expected_time_not_deadline`: 22

Sample items:
- `rvw_016` / `actor_context_needs_role_split`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 3 actor-context claim(s) without a more specific governance role. Action: Review these before treating an actor mention as decision-making, coordination, execution, approval, application, accountability or monitoring responsibility.
- `rvw_017` / `execution_capacity_need`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 2 execution capacity claim(s). Action: Use these as capacity questions; do not infer staffing, fte, or ownership.
- `rvw_018` / `execution_dependency`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 1 execution dependency claim(s). Action: Name the dependency and keep it open unless a source shows it has been resolved.
- `rvw_019` / `execution_review_task`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 4 execution review or monitoring claim(s). Action: Keep these as review, monitoring, or validation tasks; do not present them as settled implementation choices.
- `rvw_020` / `execution_sequencing_need`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 2 execution sequencing claim(s). Action: Treat these as sequencing or phasing signals; do not turn them into a hard local implementation plan without source evidence.

### Execution

Review items: 505.

Reviewer questions:
- Is dit een feitelijke uitvoeringsactiviteit, een mogelijke opvolgactie, een afhankelijkheid of een reviewtaak?
- Welke actie, volgorde, capaciteit of eigenaar mag niet worden ingevuld zonder lokale bevestiging?

Top reason codes:
- `lower_authority_norm_signal`: 61
- `municipality_relevance_inferred`: 58
- `actor_context_needs_role_split`: 54
- `authority_unclear`: 50
- `execution_review_task`: 43
- `execution_context_needs_action_split`: 43
- `execution_sequencing_need`: 30
- `execution_dependency`: 29

Sample items:
- `rvw_016` / `actor_context_needs_role_split`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 3 actor-context claim(s) without a more specific governance role. Action: Review these before treating an actor mention as decision-making, coordination, execution, approval, application, accountability or monitoring responsibility.
- `rvw_017` / `execution_capacity_need`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 2 execution capacity claim(s). Action: Use these as capacity questions; do not infer staffing, fte, or ownership.
- `rvw_018` / `execution_dependency`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 1 execution dependency claim(s). Action: Name the dependency and keep it open unless a source shows it has been resolved.
- `rvw_019` / `execution_review_task`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 4 execution review or monitoring claim(s). Action: Keep these as review, monitoring, or validation tasks; do not present them as settled implementation choices.
- `rvw_020` / `execution_sequencing_need`: mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak contains 2 execution sequencing claim(s). Action: Treat these as sequencing or phasing signals; do not turn them into a hard local implementation plan without source evidence.

## Decision Recording Rule
Reviewer decisions must be recorded as human review decisions or validation records. They do not become source claims unless backed by a canonical source or explicit validation evidence.
