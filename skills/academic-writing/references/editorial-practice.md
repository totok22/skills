# Editorial Practice

Practical guidelines for proofreading, polishing, rewriting, and drafting academic and technical text in English and Chinese. Apply each rule according to context; if a rule hurts clarity, accuracy, or the author's voice, skip it.

## Contents

1. Tone and Reader Purpose
2. Structure and Flow
3. Plain Language and Common AI Habits
4. Meaning and Detail Fidelity
5. Examples
6. Revision Checklist

## 1. Tone and Reader Purpose

Match the tone to the document's role before editing:

| Document role | Typical examples | Tone |
| --- | --- | --- |
| Specifications and contracts | `README.md`, interface specs, config tables, code comments | Direct and restrained: state what it is, what it does, and under what condition |
| Papers, calculations, and formal reports | Journal manuscripts, theses, design calculations, test reports | Objective and precise: state boundary conditions, evidence, and conclusions clearly |
| Notes, reviews, and summaries | Technical notes, study guides, comparisons, troubleshooting | Plain and readable: prioritize cause-effect, concrete comparisons, and clear engineering judgment |

- Stay restrained: do not insert editorial praise, unsolicited commentary, slogans, lecturing, filler, or unnecessary repetition.
- Tighten prose without over-compressing it: say what is needed clearly and keep enough connective flow for comfortable reading, rather than terse telegram-style shorthand.
- Do not impose an academic paper style on informal notes or practical engineering reports.

## 2. Structure and Flow

- **Given to new:** Start sentences with familiar context that links back to the previous sentence; place the new finding, contrast, or main point at the end, where readers naturally place emphasis.
- **Clear pronouns:** Replace standalone `This`, `It`, `其`, or `该` with a concrete noun phrase (`This discrepancy`, `该偏差`) whenever more than one referent is possible.
- **Conclusions up front when appropriate:** In abstracts, technical reports, design reviews, and multi-part sections, state the main conclusion or status first, then give conditions and details. State each full conclusion once; refer briefly elsewhere.
- **Voice follows focus:** Use concrete verbs instead of wordy noun phrases (`conducted an evaluation of` → `evaluated`; `进行了评估` → `评估了`). Keep passive voice when the apparatus, sample, or system state is the main topic, as is common in Methods and specifications.
- **Positive rules, kept boundaries:** State rules and completion criteria positively with observable signals when clearer (`以保存等待位清零为准`). Add a negative clarification only where readers are likely to misunderstand, and give the reason immediately; drop unmotivated negations (`不代表 X`, `不能只看 X`). Keep explicit negative findings and functional or safety boundaries (`该接口仅用于诊断，不参与实时控制`).

## 3. Plain Language and Common AI Habits

Address recurring writing habits rather than applying mechanical word bans:

- **Trailing commentary and forced closers:** Cut tacked-on `-ing` commentary (`..., highlighting its pivotal role and paving the way for...`), Chinese summary endings that add no new facts (`……，彰显了……，为……奠定了基础`), and dramatic paragraph wrap-ups.
- **Formulaic contrasts and padding:** Trim unnecessary `not merely X, but rather Y` or `不是……而是……` patterns when a direct statement is clearer. Avoid forcing items into artificial groups of three or using em-dashes (`—`) repeatedly as a syntax crutch.
- **Synonym cycling:** Use one consistent term for each technical concept (`estimator`, `controller`) instead of rotating substitutes (`framework` → `paradigm` → `approach`) across adjacent sentences.
- **Dramatic metaphors and meta-commentary:** Replace theatrical metaphors with plain descriptions (`物理天花板` → `物理限制`; `心脏/呼吸/博弈` → actual component, process, or trade-off). Remove narrator openings (`为我们揭示了…`, `以下是对…的解析`, `It is worth noting that`, `Here's the thing`), rhetorical questions (`你是否想了解…？`), and unneeded second-person pronouns (`you`, `你`).
- **Promotional wording, empty praise, and unbounded absolutes:** Replace commercial buzzwords (`赋能`, `打造`, `极致`, `无缝`, `delve`, `tapestry`, `groundbreaking`, `seamless`), unsupported praise (`设计优秀`, `精妙`, `致命硬伤`), and unbounded absolutes (`极其`, `完全`, `绝对`, `一定`) with concrete mechanisms, ranges, or measured values. Never invent missing numbers to replace them.

**Do not ban words blindly.** Keep valid technical and statistical terms whenever they fit the context: `significant` (with a statistical test), `robust` (when the disturbance or fault is stated), `however` (at a real logical turn), defined physical quantities (`最大充电电流`, `100% 占空比`), and domain terms (`闭环控制`, `门控`, `语义`, `消费`, `落盘`, `最优`).

## 4. Meaning and Detail Fidelity

Watch for four quiet distortions that often slip in during polishing:

- **Claim strength drift:** Non-significance (`p = 0.12`) is neither "a minor difference" nor proof of no effect; observed trends are not confirmed mechanisms; exploratory or post-hoc analyses must not read like prespecified confirmatory tests.
- **Zero vs. absent:** Keep `0`, `below detection limit`, `missing`, `not measured`, and `not applicable` distinct.
- **Detail loss while shortening:** Retain exact numbers, units, denominators, test conditions, formula variants, derivation steps and conditions, component names, and failure cases. Do not reduce an algebraic derivation to a qualitative summary.
- **Emphasis shift:** Moving a key caveat into a minor parenthetical—or softening a direct failure behind a polite opening—changes the author's point even when all facts remain present.

## 5. Examples

| Case | Weak or distorted | Preferred |
| --- | --- | --- |
| Keep definite failure | `The controller showed certain limitations under challenging conditions.` *(source: failed in all 3 wet-track trials)* | `The controller failed in all three wet-track trials.` |
| Keep association distinct from causation | `Higher temperatures reduced estimation accuracy.` *(source: was associated with)* | `Higher temperatures were associated with lower estimation accuracy.` |
| Keep valid statistical term | `The difference was minor (p = 0.12).` *(source: not statistically significant)* | `The difference was not statistically significant (p = 0.12).` |
| Cut trailing `-ing` filler without adding facts | `Latency fell by 18 ms, underscoring its transformative potential and paving the way for real-time use.` | `Latency fell by 18 ms.` *(add real-time budget comparison only if supplied)* |
| Keep one technical term | `The estimator converged in 4 s. The framework tolerated noise, and this paradigm stayed stable.` | `The estimator converged in 4 s and remained stable under sensor noise.` |
| State rule positively with reason | `保存是否完成，不是看命令应答，而是看保存等待位。` | `保存是否完成以保存等待位清零为准。命令应答只表示命令已收到，此时数据可能仍在写入。` |
| Remove metaphor and hype | `进气系统的演进是人类与物理天花板的精妙博弈，极具鲁棒性。` | `进气系统设计需在充气效率与流动阻力间权衡。` *(add measured data only if supplied)* |
| Leave accurate prose alone | `The samples were stored at 4 °C until analysis.` | `The samples were stored at 4 °C until analysis.` *(unchanged)* |

## 6. Revision Checklist

Check the finished text by whether a reader grasps it accurately in one pass:

- Do numbers, units, conditions, claim strength, and author emphasis still match the source?
- Are technical terms consistent across sentences, with no unnecessary synonym rotation?
- Are rules and conclusions stated directly, with reasons attached to any negative clarification?
- Have promotional words, theatrical metaphors, narrator openings, and empty paragraph closers been removed without deleting domain terms or details?
- Is the prose concise and readable without feeling over-compressed or padded with unsolicited commentary?
- Were sound, clear sentences left alone rather than rewritten for the sake of editing?
