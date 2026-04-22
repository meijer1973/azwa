# Human Review Guidance

This note explains how to communicate review-heavy items to human readers without weakening the extraction model.

## Principle

The database should preserve the claims as extracted and interpreted.
The human-facing layer should explain clearly why some items still need human judgment.

## 1. Authority Unclear

Use this when a claim comes from a lower-authority source such as:

- a VNG FAQ
- a municipal summary page
- a commentary or business-case report
- a gateway page that is not itself the binding or primary document

### How to communicate it

- Name the source explicitly.
- Name the source level if useful.
- Do not phrase the claim as settled fact.

### Preferred phrasing

- `According to a VNG FAQ, ...`
- `A municipal summary page states that ...`
- `SEO Economisch Onderzoek notes that ...`
- Dutch-facing version:
  - `De VNG stelt in een FAQ dat ...`
  - `Een gemeentelijke samenvattingspagina vermeldt dat ...`

### Avoid

- `It is agreed that ...`
- `This means that ...` when the source is only commentary or FAQ-level guidance

## 2. Municipality Relevance Inferred

Use this when a national or regional claim appears relevant to Almere, but the collected public Almere documents do not yet explicitly show adoption, localization, or commitment.

This is not a database error.
It is useful information for policymakers.

### How to communicate it

- State that the national or regional goal exists.
- State that public Almere documents do not yet clearly show explicit local adoption.
- Flag this as a possible documentation gap, adoption gap, or follow-up question.

### Preferred phrasing

- `A national agreement sets this as a goal, but the currently collected public Almere documents do not yet make explicit whether or how Almere has adopted it.`
- `This may require local clarification, adoption, or publication in municipal policy documents.`
- Dutch-facing version:
  - `Er is een landelijke afspraak of doelstelling, maar in de verzamelde openbare Almere-documenten is nog niet expliciet zichtbaar of en hoe Almere deze heeft overgenomen.`

## 3. Definition Or Terminology Ambiguity

Use this when the same term appears in multiple sources, but it is not yet clear whether the same policy-defined concept is meant.

Typical example:

- `stevige lokale teams`

This may be:

- a formal policy concept with a defined meaning
- a looser public-facing description
- a local translation of a national concept

### How to communicate it

- Do not assume equivalence too early.
- Explain that the term is used in multiple contexts.
- Ask for human clarification of the intended definition.

### Preferred phrasing

- `The term 'stevige lokale teams' appears in both national and local sources, but human review is needed to confirm whether the same policy-defined concept is intended.`
- Dutch-facing version:
  - `De term 'stevige lokale teams' komt terug in zowel landelijke als lokale bronnen, maar menselijke duiding is nodig om vast te stellen of hier dezelfde beleidsmatige definitie wordt bedoeld.`

## Practical Implication

These cases are generally not weaknesses of the database.
They are signals that:

- source hierarchy matters
- local public adoption may lag behind national policy
- terminology may need human interpretation before it can be treated as settled policy guidance
