# Tasks, Genres, Translation, and Long Documents

Guidance for adapting to document genres, translating between Chinese and English, drafting from notes, writing reviewer responses, and consolidating long documents.

## Contents

1. Genres and Structure
2. Chinese–English Translation
3. Drafting from Notes
4. Reviewer Responses
5. Long Documents and Note Consolidation

## 1. Genres and Structure

Match structural choices to the document's actual argument and venue conventions. Do not reorganize a whole manuscript during a `polish`.

- **Specialist journals and theses (IEEE, ACM, Elsevier, Springer):** Usually follow a funnel/hourglass arc—broad problem narrowing to a specific gap, then methods and results, then conclusions matching the opening scope without over-promising.
- **Broad-audience venues (*Nature*, *Science*), abstracts, and technical reports:** Usually put the main finding, decision, or status first, then expand conditions and reasoning.

| Genre | Main priority | Common mistake |
| --- | --- | --- |
| **Abstract** | Question, approach, key quantitative results, bounded conclusion | Inventing novelty, replacing numbers with vague adjectives, drifting from the main text |
| **Introduction** | Problem context, fair review of prior work, clear gap, explicit aim | Inventing citations, dismissing prior work unfairly, burying the aim |
| **Methods** | Reproducibility, sequence, apparatus, parameters, units, exclusions, conditions | Dropping boundary conditions, inventing an actor to avoid passive voice, describing an ideal rather than actual protocol |
| **Results** | Direct comparisons, values, units, denominators, uncertainty, direction | Mixing unverified mechanism claims into observations, hiding null or failed runs |
| **Discussion** | Interpretation tied to results, comparison with prior work, concrete limitations | Inflating correlation to causation, defensive phrasing, repeating Results verbatim, generic limitations |
| **Figure / Table Caption** | Self-contained variables, labels, units, sample size, test conditions | Interpreting trends or causes not shown in the figure or table |
| **Cover Letter** | Fit with the venue and evidence-backed contribution | Fabricating exclusivity, ethics approvals, co-author sign-off, or hype |
| **Technical / Engineering Report** | Conclusions, boundary conditions, safety margins, design rationale, verification status | Mixing design intent with tested performance, hiding failures or open items |
| **Study / Technical Notes** | Logical topic order, full technical detail, intact algebraic derivations | Keeping chat-turn order, dropping edge cases for brevity, turning derivations into qualitative prose |
| **General Professional Writing** | Clear takeaway for the reader, plain register | Importing stiff journal language or rigid paper templates |

For system or module design docs, a clean default order is: **purpose → implemented flow → interface or protocol → fault handling → verification and pending work**. Adapt the order for test reports or failure analyses, and always keep verified behavior separate from pending calibration, unconfirmed parameters, and planned tests.

## 2. Chinese–English Translation

Translate at clause and paragraph level so the logic, tone, and naturalness match target-language disciplinary prose.

1. **Adapt sentence structure across languages:**
   - **Chinese → English:** Chinese often joins clauses with commas while leaving cause, condition, or time implicit (`温度升高，反应加快，产率提高`). Convert these into clear main and subordinate clauses using the exact logical relationship present in the source. Do not guess causation when the source only states sequence, and do not join every clause with `and`. Avoid dangling modifiers (`Using this method, the SNR improved` → `With this method, the SNR improved` or `Using this method, we improved the SNR`) and stacked `of`-chains.
   - **English → Chinese:** Avoid stiff translation prose (overused `被`, empty light verbs such as `进行/做出/实现`, and deeply nested `……的……的` modifiers). Follow natural Chinese order: condition or time → subject → action and result.
2. **Keep precision and scope intact.** Preserve all qualifiers, negative findings, comparison targets, subjects, uncertainty, and sequence. Do not add commentary or omit caveats.
3. **Protect terminology and markup:**
   - Follow any user glossary first, then standard field terminology; keep one term per concept and flag genuine ambiguities in a brief note.
   - Keep LaTeX math, citation and cross-reference commands (`\cite*`, `\ref`, `\eqref`, `\cref`), code blocks, inline code, URLs, and citation keys untouched.
   - Keep numerical values and units unchanged unless conversion is requested; verify with `scripts/check_fidelity.py`.
   - Do not translate code identifiers or citation keys, and do not leave untranslated source fragments in the final text.

## 3. Drafting from Notes

1. **Group supplied material before writing:** (a) verified facts, data, and citations; (b) hypotheses or design intent; (c) planned or unverified work; (d) missing required items.
2. **Use only supplied facts.** Do not invent sample sizes, p-values, equipment models, hyperparameters, citations, DOIs, ethics approvals, or novelty claims. Do not borrow facts from style examples.
3. **Mark missing essentials clearly.** Insert `[Author to confirm: <missing item>]` (English) or `[作者待确认：<缺失项>]` (Chinese) wherever required details are absent.
4. **Distinguish inference from observation.** Present logical connections between facts as reasoning or interpretation, not measured results.

## 4. Reviewer Responses

Every claim about a revision must match the actual manuscript:

1. **Number every separable point verbatim.** Split multi-part comments into individual items (`R1.1`, `R1.2`, `R2.1`) without paraphrasing or softening criticism. Never invent reviewer comments.
2. **Anchor each revision.** Quote the updated text and its location (`Section X.Y` or `file:line`). If the revised file or diff is not available, state that locations are based on the user's description.
3. **Handle unaddressed and conflicting requests openly.** Mark declined, out-of-scope, or data-limited requests with a concise factual reason (and note any limitation added to the paper) rather than skipping them. If two reviewers ask for opposite changes, give consistent reasoning to both and cross-reference the decision.
4. **Respect length limits without dropping points.** If a venue caps response length, shorten the prose rather than omitting any numbered item.

Standard entry format:
- **Comment (`R1.1`):** `<verbatim reviewer point>`
- **Response:** `<direct answer grounded in evidence>`
- **Manuscript Revision:** `<Section / line + quoted revised text, or [Author to confirm: ...] / No change (reason)>`

## 5. Long Documents and Note Consolidation

- **Survey before editing.** Read surrounding sections (or the full outline) and track three lightweight items:
  1. **Terminology and abbreviations:** standard terms, symbols, and first-definition locations (for bilingual Chinese notes or papers, write `中文术语 (English Term, ABBR)` at first mention only).
  2. **Key claims and numbers:** values, units, denominators, and scope across Abstract, Methods, Results, Discussion, tables, and captions so sections do not contradict one another.
  3. **Section roles and numbering:** keep section responsibilities distinct and verify continuous numbering for headings, lists, tables, figures, and equations.
- **Consolidate overlapping notes without losing detail.** Drop turn-by-turn or chat-log order, organize by logical topic, start from the most complete passage, and merge every unique detail from duplicate sections into one authoritative place. Use `--allow-dedup` with `check_fidelity.py` when duplicate mentions are intentionally consolidated.
- **Protect full files and state limits.** Never replace a full manuscript with a partial excerpt. If only an excerpt was provided, briefly state which cross-section checks could not be run.
