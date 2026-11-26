# Review and Verification Protocol

Rules for running a read-only `review` task and for verifying high-stakes edits, translations, drafts, and reviewer responses.

## Contents

1. Review Rules
2. Severity and Dimensions
3. Independent Review (Subagent and Self-Review)
4. Local Check Script
5. Report Format

## 1. Review Rules

- **Stay read-only during `review`.** Do not edit manuscript files. If the user asks for edits mid-review, finish the report or handle edits as a separate step.
- **Read all provided text.** Do not review from an abstract or headings alone; check Methods, Results, tables, captions, and conclusions together.
- **Judge against the source and task goal, not personal taste.** Leaving a sound sentence unchanged is a pass, not a defect.
- **Anchor every finding.** Quote the exact span (and `file:line` for files). "Statistics are weak" is not actionable; `methods.tex:112 uses a t-test with n=7 and no normality check` is.
- **Escalate source contradictions.** If a `critical` or `major` issue comes from ambiguity or contradiction in the source itself, keep the original wording and flag it clearly for the author.

## 2. Severity and Dimensions

Evaluate each dimension separately rather than producing an arbitrary total score. **Fidelity is a pass/fail gate**: smooth prose never offsets a factual error.

| Severity | Meaning | Examples |
| --- | --- | --- |
| `critical` | Meaning, evidence, or markup integrity is broken; blocks acceptance | Fabricated fact, citation, or number; changed sign, magnitude, unit, or direction; association turned into causation; definite failure softened away; broken LaTeX math or citation key; untranslated text returned as translation |
| `major` | Clear harm to comprehension, emphasis, scope, or task boundary | Author emphasis shifted; ambiguous referent or dangling modifier affecting meaning; lost contrast or qualifier; structural rewrite during `proofread`; cross-section mismatch; unanswered reviewer sub-point |
| `minor` | Localized wording or formatting issue | Wordy phrasing, synonym cycling, trailing `-ing` filler, minor spacing or punctuation inconsistency |

Check these six dimensions:
1. **Factual and evidentiary fidelity (gate):** Propositions, numbers, units, denominators, qualifiers, direction, causality, negative results, and analysis status match the source or supplied notes.
2. **Author intent and emphasis:** The author's main point and contrasts remain prominent.
3. **Clarity and flow:** Clear given-to-new progression, unambiguous referents, direct verbs, clear logical hierarchy.
4. **Plainness and naturalness:** Idiomatic target-language prose free of AI habits and mechanical over-correction.
5. **Genre fit and scope control:** Tone and structure match the document role without exceeding the requested intervention level.
6. **Terminology, markup, and coherence:** Consistent terms and abbreviations, intact LaTeX/Markdown/code/URLs, sequential numbering, cross-section consistency.

Task-specific checks:
- **Translation:** Check accuracy (mistranslation, omission, addition, literalness, claim-strength shift), fluency (comma splices, dangling modifiers, stiff register), and terminology (glossary adherence, no synonym cycling).
- **Drafting:** Trace every factual claim to supplied notes and verify missing items use `[Author to confirm: ...]` or `[作者待确认：...]`.

## 3. Independent Review (Subagent and Self-Review)

Self-review in the same conversation tends to miss errors because the editor remembers why it made each change. For high-stakes work—full or long manuscripts, submissions, major translations, reviewer responses, large note consolidations, or when requested—use an isolated review pass whenever the host supports subagents:

1. **Spawn a read-only reviewer subagent** with a fresh context (without the editor's chain of thought or justifications).
2. **Provide only clean inputs:**
   - source text (or supplied notes) and candidate text;
   - task type, genre, scope limit, author emphasis, and active profile or glossary;
   - `check_fidelity.py` output, if run;
   - the severity levels, dimensions, and report format from this file.
3. **Evaluate findings before editing.** Fix confirmed `critical` and `major` defects—preferring a move back toward the original wording over a new paraphrase—and skip stylistic nitpicks that hurt clarity or voice. Re-run `check_fidelity.py` after repairs.
4. **Honest fallback.** When subagents are unavailable (or skipped on short, low-risk edits), perform a second-pass self-review and state plainly that it was a same-session self-review. Do not send unpublished manuscripts to external services.

## 4. Local Check Script

See `SKILL.md` for the command. Reference for flags and limits:

- **Flags:** `--task` (`proofread`/`polish`/`rewrite`/`translate`/`draft`), `--allow-dedup` (for consolidating `rewrite`: checks every unique source token still appears at least once while still catching newly added tokens), `--protect TERM`, `--allow-change TOKEN` (normalized automatically), `--format json|text`.
- **Exit codes:** `0` pass, `1` warnings only (for example, unit notation changes to confirm), `2` hard errors.
- **Checked automatically:** Numbers, signs, units, LaTeX math and citations/references, code spans/blocks, Markdown link URLs, protected terms, added numbers in `draft`, and unchanged text in `translate`.
- **Not checked (requires human/semantic review):** Flipped negation or causality (`A did not cause B` → `A caused B`), swapped attribution (`A: 92%, B: 85%` → `A: 85%, B: 92%`), Chinese numerals (`三组` → `两组`), emphasis or claim-strength shifts, and mistranslated concepts.

## 5. Report Format

Use this format for `review` tasks and reviewer subagent output:

```markdown
## Summary
- Verdict: pass | revise | needs author clarification
- Overview: <2–4 sentences on core argument, strengths, and main gaps>

## Strengths
- <1–3 concrete, anchored points that work well>

## Findings
1. **[critical | Fidelity | location/span]** `<quoted span>`
   - Issue: <what is wrong and why it matters>
   - Suggested fix: `<minimal concrete repair>`

## Review Limits
- <what could not be checked: e.g., external references, missing sections, compiled PDF layout>
```
