# Evidence Criteria

These criteria describe the companion manuscript’s evaluation framework in the [2026-10-09 source snapshot](../data/source-snapshot.json). See [Reported Evidence](reported-evidence.md) for the results and [the data](../data/reported-evidence.json) for each recorded comparison.

## Unit of comparison

Use **one primary comparison per report**: its leading result, harness update, baseline, model, benchmark, configuration, and round. All four judgments refer to this comparison. An aggregate result needs evidence for the aggregate; another model, benchmark, or secondary experiment cannot supply missing evidence.

The [reading-list definition](../README.md#definition) determines scope. Model changes within a comparison affect Attribution. Offline antecedents and limited-persistence mechanisms remain identified in their entries.

| Code | Meaning |
|:-:|---|
| C / ✅ | Full evidence within the recorded coverage |
| O / ◐ | Partial evidence |
| N / — | The reported evidence does not support the claim |
| X / n/a | No empirical evaluation; excluded from totals |

Criteria differ across claims. Their counts describe reported evidence, not overall method quality.

## Selection

Reporting outcomes must remain separate from **proposal**, **ranking**, **admission**, and **report choice** (round, configuration, or hyperparameters).

- **C:** All four uses are separate. Prequential evaluation qualifies when each outcome is scored before it can influence an update and later report choice does not select on stream scores. Test-time adaptation without access to benchmark verdicts can also qualify.
- **O:** A stated procedure leaves partial overlap or an unresolved use, such as a held-out score used for promotion, partly overlapping tasks, or split names without a documented separation.
- **N:** Reporting outcomes generate the update, rank the reported candidate, or select a peak round or configuration without independent reporting evidence.

An unconditional update is judged by the feedback it uses. Protecting scorer, verifier, and bookkeeping code from candidate edits is a separate structural requirement.

## Activation

Identify whether the accepted update operated in the scored runs:

- **Available:** the artifact entered the run.
- **Reached:** the changed path executed.
- **Carried:** its output reached the next model input, or the trajectory followed it. Receiving content and following it provide different evidence.

**C** requires reached or carried evidence tied to the primary comparison, such as execution beacons, executed-node records, output-survival checks, or adherence measurements. One confirmed case can qualify; always record whether coverage is one case, a sample, or all scored runs.

**O** covers loading or retrieval alone; execution during search, screening, or another experiment; illustrations without run provenance; aggregate token counts; unchanged-component routing; and claims that code runs by construction. **N** means no evidence that the update operated. A counterfactual score change belongs to Attribution.

## Attribution

Full evidence requires three conditions: **isolate the update**, **control inference resources**, and **show a margin beyond measured execution variation**.

- **C:** All three hold, using either the pre-update state or an ablation of the evolved component as the reference.
- **O:** At least one remains unresolved, including unmatched compute, variation unmeasured or not cleared, an unrelated ablation, or changes to model, decoding, tools, effort, or evaluator.
- **N:** One run per task, no variance estimate, and no accounting of inference resources.

Measure variation through repeated executions of frozen states, a paired test over task outcomes, or reported per-run/per-task data. Variation across judges, candidate harnesses, task orders, or costs does not satisfy this condition. State the measurement unit.

The margin must meet one of these thresholds: a test distinguishes it from zero at the 5% level; an interval for the difference excludes zero; or it exceeds two standard errors computed from reported per-arm dispersion over independent runs. Record calculation inputs. Significance for some components does not establish significance of an average, and a selected maximum requires accounting for selection among comparisons. A binomial bound inferred from success rates and task counts is a reading aid, not measured variation.

Inference resources concern the **scored runs**: calls, generated tokens, turns, attempts/pass@k, sampled candidates, and reasoning effort. Report search cost separately and declare context added by evolved artifacts. Control can use matched budgets, a performance–cost frontier, or a resource change that cannot explain the gain. Merely declaring an unmatched increase gives partial evidence.

## Improvement

Record **task distance**, **baseline**, and **round**. The judgment grades distance from the tasks that formed the update:

- **C:** Held-out tasks, transfer to an unseen benchmark, or probes on an earlier distribution outside the loop’s control.
- **O:** Partly overlapping tasks, separation only by a retrieval rule, or an online trajectory within one adaptive stream.
- **N:** Only the tasks that generated the update, including retries of the failures that prompted it.

Selection separately checks whether reporting outcomes influenced candidate or report choice. A held-out result at acceptance does not establish that its gain survives later updates.

## Reading procedure and limitations

The manuscript records two readings per report, with the second blind to the first and disagreements resolved against the primary source. GSkill was read once after its full text became available. The full/partial boundary requires judgment; corrections should identify the comparison, source passage, and affected claim.

This repository reproduces those records. Automated checks verify consistency and completeness of the generated files; they do not independently reassess the sources.
