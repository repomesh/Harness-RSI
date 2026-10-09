# Evidence Criteria

These criteria follow the companion manuscript’s evaluation framework as of 2026-10-09. The [source snapshot](../data/source-snapshot.json) records the source hashes; [reported-evidence.json](../data/reported-evidence.json) supplies the verdicts and their recorded basis.

## Unit of comparison

All four verdicts describe **one primary comparison**: the result the report leads with, its harness-side update, baseline, model, benchmark, configuration, and round. Evidence from another experiment cannot fill a cell. An aggregate result requires evidence covering that aggregate. Secondary protocols are recorded separately and excluded from headline totals.

Scope is determined by the harness-side update. Weight-only training and fixed components without a feedback-driven revision are excluded. A system that also trains weights can be included for its harness arm; model changes in the comparison affect Attribution. Offline antecedents and limited-persistence mechanisms remain identified in the reading list.

| Code | Meaning |
|:-:|---|
| C / ✅ | Evidence meets the claim’s criterion within its recorded coverage |
| O / ◐ | Partial evidence |
| N / — | The reported evidence does not support the claim |
| X / n/a | No empirical evaluation; excluded from rates |

The verdicts concern reported evidence, not overall method quality. The four criteria differ in difficulty, so their counts are not a ranking of claims or methods.

## Selection

Did the reporting evidence remain separate from **proposal**, **ranking**, **admission**, and **report choice** (round, configuration, or hyperparameters)?

- **C:** The report shows that all four channels are separate. Prequential evaluation also qualifies when each outcome is scored before it can influence an update, and no later choice selects on stream scores. Test-time adaptation without access to benchmark verdicts can qualify.
- **O:** A stated procedure leaves partial overlap or an unresolved channel, such as a held-out score used for promotion, a partly overlapping task set, or unsubstantiated split names.
- **N:** Reporting outcomes generate the update, rank the reported candidate, or select a peak round or configuration without independent reporting evidence.

An unconditional update is not automatically N. What matters is whether reporting evidence influenced it. Protecting scorer, verifier, and bookkeeping code from candidate edits is a separate structural requirement.

## Activation

Did an identified accepted update operate in the scored runs?

- **Available:** the artifact entered the run.
- **Reached:** the changed path executed.
- **Carried:** its output survived into the next model input, or the trajectory followed it. Receipt and adherence differ in strength.

**C** requires reached or carried evidence bound to the primary comparison: execution beacons, executed-node or tool records, output-survival checks, or adherence measurements. A single real case can qualify when it identifies both the update and its execution in those runs. The basis records coverage; C does not imply that every run or every component was observed.

**O** includes load/retrieval logs, execution only during search or screening, another model or benchmark, illustrations without run provenance, aggregate token counts, an unchanged base component’s routing counts, and the assertion that a program runs by construction. **N** means no evidence that the update operated.

A counterfactual score change is Attribution evidence. It does not replace a direct record of where and how the update operated.

## Attribution

Three conditions must hold in the primary comparison: **the arms isolate the update**, **the inference envelope is controlled**, and **the margin exceeds measured execution variation**.

- **C:** All three hold, whether comparing to the pre-update state or removing the evolved component in an ablation.
- **O:** One or more remain unresolved: unmatched compute, variation unmeasured or not cleared, another component ablated, or differences in model, decoding, tools, effort, or evaluator.
- **N:** A single run per task, no variance estimate, and no accounting of inference resources.

Measured variation comes from repeated executions of frozen states, a paired test over task outcomes, or reported per-run/per-task data. Variation across judges, candidate harnesses, task orders, or costs does not meet this criterion. The recorded basis states the measurement unit.

The margin clears variation when a reported test distinguishes it from zero at the 5% level, an interval for the difference excludes zero, or the margin exceeds two standard errors computed from reported per-arm dispersion over independent runs. Calculations based on reported statistics must record their inputs. For an averaged headline, significance on only some components does not establish significance of the average.

A binomial bound inferred from success rates and task count is a reading aid, **not measured variation**, regardless of margin size. A selected maximum also needs an account of selection among comparisons; a single-comparison noise threshold is insufficient.

The inference envelope concerns the **scored runs**: model calls, generated tokens, turns, attempts/pass@k, sampled candidates, and reasoning effort. Search cost is separate. Context inserted by the evolved artifact is its own cost and should be declared. Control means matched budgets, a performance–cost frontier, or a resource change that cannot explain the gain. Declaring an unmatched increase is partial evidence.

## Improvement

Record three indices: **distance** from tasks that formed the update, **baseline**, and **round**. The verdict grades distance; baseline and round remain part of the recorded comparison.

- **C:** Held-out tasks, transfer to an unseen benchmark, or probes on an earlier distribution outside the loop’s control.
- **O:** Partly overlapping tasks, separation only through a retrieval rule, or an online trajectory within one adaptive stream.
- **N:** Only the tasks that generated the update, including retries on the failures that prompted it.

Selection separately checks whether the reporting partition later influenced candidate or report choice. A held-out comparison at acceptance does not establish that the gain survives later updates.

## Limitations

The C/O boundary requires judgment. The manuscript records two readings for all reports except GSkill, with the second blind to the first and disagreements adjudicated against the primary source. GSkill was read once after its full text became available. This repository reproduces those judgments; its automated checks verify consistency, not an independent re-reading of every source. Corrections should identify the comparison, source passage, and affected verdict.
