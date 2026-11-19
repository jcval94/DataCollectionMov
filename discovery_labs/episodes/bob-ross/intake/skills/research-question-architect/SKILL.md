---
name: research-question-architect
description: Create compelling, evidence-grounded multi-order questions and scientific story arcs from datasets plus verified historical/social context. Use before planning an investigation report, lesson, storyboard or video.
---

# Research Question Architect · AI Discovery Labs

## Purpose

A question is not good because its answer is countable. A question is good when **its answer changes what a human believes or decides**, and the next question naturally follows from what the data revealed.

**Input:** source manifest, sample, raw data or data dictionary, external Deep Research evidence ledger, prior analyses, lesson context.

**Output:** question_graph.json, human-readable research arc cards, question scorecard, experimental contracts and visualization briefs. Output states DRAFT until data and evidence pass checks.

## Workflow (repeatable for ALL datasets)

### 0. Investigate the real-world story FIRST

Find who/what produced the records, when, why, for whom, and what the data omit. Investigate external historical, institutional, social, biological, cultural and geographic context. Cite each consequential claim. Identify rival explanations and rights of visuals; distinguish authentic story from unsupported speculation.

### 1. Generate candidate tensions, not SQL tasks

Search for: paradox, belief vs observation, hidden cost/trade-off, change over time, disruptions/life events, surprising comparisons, extreme cases, rare combinations, winners vs losers, confounding, invisible population, segmentation instability and counterfactual decisions.

A query like "how many records have trees?" is merely **Q0 / evidence primitive**, not a publishable core question.

### 2. Build a graph with orders

- **Q0 (instrumentation):** What exactly is measured? Units, completeness, schema, denominator.
- **Q1 (human question):** Why could a reasonable person care? Set competing hypotheses and a clear outcome.
- **Q2 (react to actual Q1 evidence):** At least TWO conditional branches (e.g., if trend rises, test whether subgroup mix explains it; if flat, test whether fluctuations cancel). These MUST depend on observed Q1 results; label as conditional before execution.
- **Q3 (mechanism/generalizability):** At least ONE question probing explanation, robustness, causal identification, transfer, outliers or changed aggregation. No automatic causal language.

Every Q2/Q3 needs its data dependency and a falsifier. A third-order question cannot be "make a prettier graph".

### 3. Test six necessary properties

1. **Human stakes:** changes belief or a real-world decision; avoid invented revenue/health effects.
2. **Novelty:** extends prior known results instead of rephrasing an existing query.
3. **Answerability:** specify how to retrieve, verify and join all data; external data required when appropriate.
4. **Hypothesis collision:** at least two plausible explanations yield distinguishable observations.
5. **Scientific integrity:** correct unit, denominators, confounders, uncertainty, missingness and time order.
6. **Visual insight:** specify a figure whose geometry exposes a pattern and an interaction that reveals the exceptions.

Reject, do not force a hypothesis when evidence, temporal coverage, licenses or causal identification are absent.

### 4. Run an adversarial review

For each arc ask:
- Which reasonable alternative could explain the same chart?
- Will this change with a different unit (row, episode, season, decade, region, cohort)?
- Is it a multiple-comparison artifact or a mechanical correlation between engineered features?
- Are rare groups too small?
- Was the definition of the variable chosen after viewing results?
- Is this beyond the coverage of the source (e.g., Bob Ross's health not in the CSV)?
- Can we actually show representative paintings or are image rights separate?

### 5. Score 100 points (do not optimize only for drama)

| Criterion | Weight |
|---|---:|
| Human significance / meaningful decision | 15 |
| Originality and counterintuitive tension | 15 |
| Q2/Q3 depth and conditional branching | 15 |
| Evidence, falsifiability and answerability | 20 |
| Causal/ethical safeguards and uncertainties | 15 |
| Visual explanatory potential | 10 |
| Reusability across datasets and teaching value | 10 |

Interpretation:
- 85–100: excellent **candidate**, still needs data.
- 70–84: revise or supplement.
- Below 70: discard or demote to Q0.
- Critical veto at ANY score: fake source, unauthorized visual asset, unidentifiable causal claim treated as fact, invented results, data snooping presented as confirmatory, unsupported health assertion.

Require a *differentiating rival explanation* and at least one third-order question for a top-tier arc.

### 6. Choose visual forms by hypothesis

- Life events/time → provenance timeline + production/emission alignment + change-point bands.
- Outliers → multiscale anomaly matrix, sortable records and representative factual tooltips.
- Belief test → chart with count, denominator, relevant counterexamples and changed subgroups.
- Segments/clusters → linked scatter/mosaic + hover/focus metadata + *licensed* image only if rights verified.
- Composition effects → small multiples, weighted counts, uncertainty and decomposition.
- Rare combos → co-occurrence network under a baseline/null model.
- Coverage → nested universe chart (observed vs unobserved).

Do not infer art style from 12 binary motif families alone. A static image is not automatically available for use in video.

## REQUIRED schema per arc

`id`, `title`, `human_hook`, `q0_measurement`, `q1`, `q2_if_result_A`, `q2_if_result_B`, `q3`, `competing_explanations`, `required_fields`, `required_external_sources`, `experiment_plan`, `unit_and_denominator`, `confounders`, `robustness_checks`, `visual_spec`, `ethical_and_rights_checks`, `falsification_criterion`, `scorecard`, `approval_status`.

Generate both machine-readable JSON and a narrative one-pager that a teacher can understand.

## Context-dependent gate

This skill proposes **research questions only**, not a video script. It is used in the Stage-0 intake, then revisited while building Stage-1 HTML. Stage-2 audiovisual storytelling is forbidden until the exact Stage-1 report version is explicitly approved. Stage-3 video production is forbidden until the storytelling HTML is separately approved.

## Prompt to activate manually

"Use the research-question-architect skill in this folder. Review the source metadata, sample, primary dataset and verified external research. Produce at least 12 substantive arcs with two second-order branches and one third-order test each. Score them, reject superficial SQL-only tasks, define visual evidence and approval blockers. Keep hypotheses as hypotheses until executed."

This skill is a **portable file**, not automatically registered in a global Codex/Claude skill directory. To use it, pass the file to an agent or install/copy into that agent's permitted skills location after review.
