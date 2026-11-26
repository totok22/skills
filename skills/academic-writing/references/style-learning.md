# Scoped Style Learning

How to extract, update, store, and apply writing preferences directly in a native agent session without bloating profiles, copying facts, or mixing styles across projects.

## Contents

1. Principles
2. Scope and Precedence
3. Building and Updating a Profile
4. Profile Fields

## 1. Principles

- **Guidance, not content:** Record recurring structure, voice, and terminology preferences—never experimental results, citations, or boilerplate claims copied from past papers.
- **Accuracy first, style second:** Lock down factual accuracy, claim strength, and protected terms before applying any style preference.
- **Record only specific preferences:** Store choices that go beyond this skill's built-in defaults (venue rules, voice splits, glossary terms, formatting habits). Do not fill profiles with generic reminders like "write clearly."
- **Scoped and human-approved:** Apply preferences only within their declared scope (`lab`, `author`, `journal`, `language`, `genre`), override them whenever they clash with clarity or fidelity, and write profile files only after explicit user approval. Do not count AI self-review as human approval.

## 2. Scope and Precedence

When multiple profiles apply, merge from broadest to narrowest (later overrides earlier):

```text
team / lab profile
  → author profile
    → journal / genre profile
      → language × genre intersection
        → current task instructions
          → factual accuracy (highest; never overridden)
```

Keep Chinese (`zh`) and English (`en`) preferences separate under `languages.zh` and `languages.en`. Do not apply English journal habits to Chinese technical reports, or vice versa.

## 3. Building and Updating a Profile

### Initial Extraction (`learn-style`)

1. **Confirm inputs and scope.** Identify 1–3 authorized samples, before/after edits, or journal instructions, plus the target `scope` (`lab`, `author`, or `journal`), `language`, and `genre`.
2. **Extract concrete, observable choices:**
   - sentence length variation and clause structure;
   - active vs. passive voice by section (for example, active `we` in Discussion, passive in Methods);
   - citation style (parenthetical `(Author, Year)`, integral `Author (Year) showed`, or numeric `[1]`);
   - how claims, limitations, and negative findings are framed;
   - transition, punctuation, and conclusion placement habits;
   - fixed conventions (glossary, do-not-translate terms, US/UK spelling, unit spacing, bilingual first-mention rules).
3. **Propose before saving.** Present a compact v1 draft based on [profile.example.json](../assets/profile.example.json) with supporting examples and explicit exceptions. Save only after the user approves.

### Updating from Daily Edits

- **Small patches from real edits:** When the user edits a candidate or gives a clear recurring correction, compare candidate vs. final text to see what they consistently delete, tighten, or reword, and propose a 1–3 line update to the active profile. Apply only on approval.
- **Optional local feedback log:** For multi-session or lab-wide tracking, append explicit user decisions to a private local JSONL file outside shared repositories:
  ```json
  {"timestamp":"2026-11-26T12:00:00Z","scope":"lab","task":"polish","language":"en","genre":"results","decision":"rejected","reason":"Softened an explicit wet-track failure into 'limitations'.","source":"...","candidate":"..."}
  ```
  Every `rejected` entry must include a concrete `reason`. When reading the log during a task, match `scope`, `language`, `genre`, and `task` exactly and load only the 3–5 most recent entries (`accepted` as examples, `rejected` as cautions).

### Promotion and Maintenance

- Promote a pattern into `languages.<lang>.genres.<genre>.preferences` only after repeated evidence (at least 2–3 instances) or explicit user instruction—not from one isolated edit.
- Periodically remove stale, conflicting, or overly generic entries so profiles stay small and easy to inspect.
- Increment `version` on each approved save and keep prior versions (or git history) for rollback. Do not commit private manuscript excerpts to public repositories.

## 4. Profile Fields

Start from [profile.example.json](../assets/profile.example.json):

- `profile_id` / `scope` / `version`: identifier, scope (`lab`, `author`, `journal`), and integer version number.
- `preferences`: broad specific choices (voice split, transition habits, abbreviation policy).
- `conventions`: fixed formatting rules (`spelling`, `citation_style`, `unit_spacing`, `bilingual_first_mention`).
- `languages.<lang>.preferences` and `languages.<lang>.genres.<genre>.preferences`: rules applied only on exact language (and genre) match.
- `glossary.do_not_translate` and `glossary.bilingual_terms`: verbatim terms (also usable with `check_fidelity.py --protect`) and standard bilingual pairs.
- `exceptions`: explicit limits that prevent mechanical over-application.
- `evidence`: brief dated provenance notes without confidential full paragraphs.
