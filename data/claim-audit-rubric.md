# Claim-evidence rubric

The standard behind `claim-audit.tsv` and the figure and tables of Section 6.2.
Each method in the interpreted and executable update-target branches of
`figure/fig03_target_taxonomy.tex` was read from its primary source and given four
separate evidence verdicts. The verdicts describe what a report contains, not the
quality of the method.

Symbols match the badges used in the tables:

| | meaning |
|---|---|
| `C` | the criterion is met by the reported evidence |
| `O` | the criterion is partly met |
| `N` | the criterion is not met by the reported evidence |
| `U` | the report could not be obtained |
| `X` | the work reports no empirical evaluation at all |

`X` is kept apart from `N` and excluded from the rates. A product page or a
formal-calculus paper has no evaluation to fall short of, and folding it into
`N` would read as a failed evaluation rather than an absent one.

## Scope (a separate layer from the verdicts)

The audit covers comparisons between harness states under a fixed task model.
Scope is decided first and recorded in the `scope` column (`in` / `out`) with
its reason in `scope_note`; it is never expressed through a low verdict, and an
excluded work keeps its verdicts on file and is not re-graded `X`.

A work is `out` when its headline result does not compare harness states under
a fixed task model:

- the headline gain comes from updating the evaluated task model's weights
  (SFT, RL, GRPO and the like), and no separable experiment holds that model
  fixed while a harness update of the Section 2 kind changes; or
- the method is a fixed component (static middleware, a fixed context-management
  rule) with no update driven by the system's own execution feedback.

Training elsewhere does not by itself put a work out of scope. What is fixed is
the evaluated task model; an auxiliary proposer, skill generator, or judge may
be trained (`li2026codeskill`, the C3 evaluator of `xiong2026memorymgmt`), and
offline antecedents and within-run boundary cases that Sections 3-4 discuss
stay in, because their headline still compares harness states.

Out in the current file, with the reasons in `scope_note`: `gao2026swemem`,
`zhang2026action`, `wang2026swepruner`, `xiao2026socraticswe`, and
`aggarwal2026behavioral`. The first four fail the fixed-task-model or
fixed-component test above. `aggarwal2026behavioral` fails Section 2 itself: its
rule file is revised by engineers who codify accepted review comments, not by a
mechanism that forms or selects the revision from run feedback, and Section 2
excludes a human authoring the payload and installing it. That is a different
exception from the offline algorithmic antecedents kept in below, which do form
their updates algorithmically. Their rows stay
in the file as the record of the scope decision; they are not drawn in Figure 3
and not counted anywhere in Figure 6. Checked and kept in:
`zhang2025memevolve` (its outer loop rewrites the memory system's
encode/store/retrieve/manage code, an executable update to a component
implementation, which is why Figure 3 now files it under Section 4.1),
`tao2026sepo` ("pre-training" names a prompt-evolution stage),
`xiong2026memorymgmt`, `li2026codeskill`.

## Unit of audit

The four verdicts for a method are read off **one comparison**, its *primary
comparison*:

1. the update object in scope (the harness-side artifact the taxonomy files the
   method under, not a co-trained model or an unrelated component),
2. the evolved state against the same-model baseline that result is stated
   against: the pre-update state where the report gives one, otherwise the
   baseline it names (a human-written prompt, a competing optimizer's output,
   the base agent without the artifact), and
3. the result the report leads with: the number its abstract or first results
   paragraph quotes.

`claim-audit.tsv` records that number in the `headline` column. Every verdict
is about it; a cell may not borrow evidence from another experiment in the same
report. Other protocols the report runs (frozen transfer to a second benchmark,
a cross-model replay, a retention probe) are recorded in
`claim-audit-secondary.tsv` with their own selection and improvement verdicts
and are not counted in Figure 6.

Why: an earlier pass read the four cells of one row off different experiments,
for example selection from a clean transfer table and attribution from an
in-distribution ablation. Each cell was defensible and the row described no
comparison that exists.

The comparison is pinned by its update object and version, task model and
size, benchmark and split, comparator, round or configuration, and inference
budget. Evidence from a different model, benchmark, round, configuration or
comparator is not borrowed into a cell, even from the same report
(`zhang2026action`: 7B tool-call statistics against a 14B headline;
`ren2026taco`: per-step token reductions measured on other backbones;
`du2026livingharness`: a Cycle 1 case against Cycle 2/3 headline values;
`wang2025workflow`: a same-representation rerun against a published-baseline
headline).

**Aggregate headlines.** When the headline averages several benchmarks,
backbones or configurations, a cell has to hold for the aggregate. Evidence on
one component is recorded with its coverage and does not stand in for the
average (`xu2026lifeharness`: ablations on one of 18 backbones). Conversely,
evidence that covers every component is read as covering the aggregate
(`xia2026rrsi`: an interval excluding zero for each of the three averaged
benchmarks).

Activation is the one exception, and it is stated here so the two rules do not
collide. The activation `C` proposition is existence: some identified accepted
update was reached or carried in scored runs behind the headline. A single case
therefore satisfies it even under an aggregate headline, provided the case comes
from the runs behind that headline and its coverage is recorded
(`chen2026harnessx`: one of 15 configurations, the GAIA / Sonnet 4.6 case, with
the round-10 edit checked against the round-11 headline traces). The exception
is not a lowering of the bar for the other three columns, and it does not reach
any cell but activation: the same one-configuration case is not evidence that
the artifact caused the aggregate gain, and selection, attribution and
improvement are read on the aggregate as above.

Attribution is read against that baseline. Where it is a competing method
rather than the pre-update state, `C` still requires that the two arms differ
only in the artifact (same model, scaffold and decoding, one evolved prompt or
library against another), and the basis says which arm was the baseline.

Where the primary comparison is ambiguous the choice is stated in the basis.
`yuksekgonul2025textgrad` is read on the prompt-optimization result (Table 3),
which is the branch the taxonomy files it under.

## Shape of the four

Activation, attribution, and improvement ask whether an update operated, what
it caused, and how far the evidence extends. Selection concerns the use of the
reporting outcomes. The audit operationalizes these as separate criteria; a
final-state comparison need not establish component-level activation, and the
number of criteria met is not an overall method ranking.

Two consequences for scoring:

- **Selection and improvement are not the same column.** Improvement grades the
  distance between the reporting tasks and the tasks that formed the update.
  Selection grades whether that declared distance survived proposal, ranking,
  admission, and the choice of round and configuration. A report can name a
  clean held-out partition and still spend it.
- On a **static partition**, `Selection = C` implies `Improvement = C`: a
  reporting partition has to exist before it can be kept clean. The implication
  does not hold for a stream. Prequential online evaluation and test-time
  adaptation can keep every verdict off the update (`Selection = C`, below)
  while the reporting tasks are the stream the update forms on
  (`Improvement` at `O` or `N`). The current file has nine such rows:
  `ouyang2026reasoningbank`, `ren2026flowevo`, `shinn2023reflexion`,
  `wang2024voyager`, `wang2025workflow`, `wei2026evoharness`,
  `xia2025liveswe`, `xiong2026memorymgmt`, `zhang2026autogenesis`.
  An earlier version of this rubric stated the implication without the
  qualifier.

## Selection

Was the reported number measured, or was it picked? Four channels can spend
the reporting evidence:

1. **proposal**: the update was generated from the reporting tasks' *scored
   evidence*, meaning a verdict, a label, a reference answer, or a score;
2. **ranking**: that evidence ranked candidates;
3. **admission**: it was consulted by the promotion or acceptance rule;
4. **report choice**: it decided which round, which configuration, or which
   hyperparameter setting is reported.

- `C` — none of the four channels touched the evidence the reported number is
  read off, and the partition is shown rather than asserted. Two stream
  protocols also qualify, because no scored evidence reaches the update before
  it is scored:
  - *prequential online evaluation*: each task is scored first and only then
    may feed the update; no task is revisited, and neither the round nor the
    configuration is chosen afterwards on the stream's scores
    (`wang2025workflow`, `ren2026flowevo`, `wei2026evoharness`);
  - *test-time adaptation that never reads a verdict*: the update conditions on
    the model's own trajectory or self-generated tests, not on the benchmark's
    grader (`shinn2023reflexion`, `xia2025liveswe`, `zhang2026autogenesis`).
- `O` — a stated procedure exists but one channel partly overlaps the reporting
  evidence: a "held-out" split whose score is also an input to the promotion
  rule, a reporting set that partly coincides with the evolution set, a
  secondary design choice (retrieval key, memory format) made on the reporting
  columns, no rule for which of several discovered candidates supplies the
  number, or split names asserted without the partition being shown.
- `N` — the reported number is itself a choice: the maximum or best round of a
  trajectory on the tasks the system evolved against with no stopping rule
  fixed in advance; a headline configuration or hyperparameter picked on the
  reporting partition, including a sweep whose best row becomes the headline
  (`yang2026skillopt`, `chen2026prologue`) or a retuning re-run only on the
  reporting tasks that fell short (`zhou2023large`); or an update generated
  from the reporting tasks' scored evidence with no separation at all,
  including a library distilled only from trajectories the official verifier
  marked successful (`lin2026muse`).

Having no selection step is not `N`. A loop that commits unconditionally and
reports on a partition it never saw spent no reporting evidence, so the number
is still a measurement.

## Activation

Did the accepted change operate in the runs that produced the score?

Three grades, after Section 6.2.2: **available**, that the artifact entered the
run; **reached**, that its path executed; **carried**, that its effect reached
the model or its trajectory, either because its output survived into the next
model input (the weaker form: the model received it) or because the trajectory
conformed to it (the stronger form: the model acted on it).

- `C` — reached- or carried-grade evidence **from the runs that produced the
  headline number**: an execution beacon, a declared trace feature checked
  against later traces, an executed-graph node or tool record, an
  output-survival check, an adherence rate. The proposition is existence: some
  identified accepted update was reached or carried in scored runs behind the
  number. A single real case therefore counts when it comes from those runs and
  identifies the update content and the fact of its execution or of its
  entering the next input or the trajectory; the same rule applies to every
  row, and coverage is recorded rather than graded (`[coverage: ...]`: all
  scored runs, a sample, a single case, or which components of an aggregate).
  `C` asserts nothing beyond the recorded coverage, and nothing about whether
  the update caused the score.
- `O` — availability only, or reached/carried evidence that cannot be bound to
  the primary comparison. Specifically `O`:
  - evidence only from search, screening, or training-time runs;
  - a case from another model, benchmark, round, or configuration;
  - an illustrative example, motivating case, pseudocode, design description,
    or an edited showcase whose run provenance is not given
    (`hu2026evorepair`, `yang2026gse`, `zhao2024expel`);
  - an outcome comparison that does not name the update that was followed
    (`wang2026effiskill`), or a compliance score that is itself the metric
    (`yang2026vaso`);
  - "the program runs by construction": an evolved `forward()` that produces
    every answer shows the artifact was installed, not which of its paths ran;
  - aggregate token counts, or routing counts for a base component the update
    did not change;
  - attestations, load rates, and retrieval logs.
- `N` — no evidence it operated; activation is assumed from installation.

Section 6.2.2 calls availability the weakest grade, so a load rate alone cannot
sit at `C`. An earlier version of this rubric listed "a skill-load rate" under
`C`, which contradicted the section it scores against.

Evidence that an edit's predicted *effect* matched later outcomes is
attribution evidence, not activation evidence, and is not credited here.

A component counterfactual that changes the outcome beyond execution variation
implies activation in aggregate (Section 6.1), but this column credits only
direct execution evidence: the counterfactual says neither in which runs the
component operated nor at which grade. A row with `Attribution = C` and
`Activation = O` (9 of the in-scope rows in the current file, recounted after
the 2026-10-10 amendment) is therefore
consistent, not a contradiction.

## Attribution

Did the observed difference come from that change, rather than from execution
variation, a changed resource envelope, or a changed evaluator?

The claim has three conditions, read on the primary comparison: the arms
differ only in the evolved component (same model, scaffold, decoding, tools,
evaluator); the inference envelope is controlled; and the margin exceeds
execution variation that the report measured. Selection and improvement are
graded in their own columns and are not folded in here.

- `C` — all three conditions hold. The arms may be the evolved state against
  the pre-update state, or an ablation or counterfactual that removes the
  evolved component itself.
- `O` — one or two conditions hold: variation measured but the envelope only
  *declared*, or declared to have changed in the arm's favour; the envelope
  controlled but no measured variation; measured variation that the margin does
  not clear; an ablation over something other than the evolved component; or
  arms that differ in another uncontrolled way, such as a different model,
  effort setting, comparator setup, or number of attempts.
- `N` — a single run per task, no variance estimate, and no accounting of
  tokens, model calls, retries, or context growth.

Terms, fixed so that the same evidence gets the same cell everywhere:

- **Execution variation** is variation the report measured: repeated runs of
  the frozen states with a dispersion or interval, a paired test over per-task
  outcomes (McNemar, Wilcoxon, paired t, paired bootstrap), or per-run or
  per-task raw data from which such a statistic can be computed. Dispersion over
  *evaluator* seeds or judges does not count (`lee2026rhi`), nor does
  dispersion over candidate harnesses or stream orders, nor dispersion of a
  different quantity (cost, runtime, task-to-task spread). Repeats of the whole
  optimization count, because each repeat includes a fresh execution
  (`pryzant2023automatic`, Appendix C, 12 repeats; `zhao2024expel`, four
  train/evaluate folds). The basis states the unit (runs, seeds, folds, tasks)
  the statistic is computed over.
- **Clearing the variation.** The fixed standard is that the reported statistic
  distinguishes the margin from zero: a reported test at the 5% level, an
  interval for the difference that excludes zero, or, when only per-arm
  dispersions over independent runs are printed, a margin of at least two
  standard errors of the difference computed from them. Such a computation is
  marked in the basis as an audit computation from reported dispersion, with
  its inputs (`ren2026taco`: +1.36 against a standard error of 1.20, not
  cleared; `tao2025delvepo`, `zhou2026multiagent`, `ni2026trace2skill`:
  cleared). No particular test or p-value format is required.
- **Audit-computed bounds are not measured variation.** A binomial standard
  error computed by the auditor from a reported rate and task count does not
  meet the condition, however large the margin: it rests on assumptions the
  report does not check (independent executions across tasks, no state carried
  between scored tasks, plug-in rates) and is no part of the evidence the report
  supplies. It is recorded in the basis as a reading aid only (`fang2026memp`,
  `zhang2026selfharness`, `yang2026skillopt`, `xiong2026memorymgmt`,
  `ouyang2026reasoningbank`).
  For the record, the direction of the covariance term:
  `Var(X - Y) = Var(X) + Var(Y) - 2 Cov(X, Y)`, so positively correlated arms
  have a *smaller* variance of the difference than the independent sum and
  negatively correlated arms a *larger* one. Sharing the same tasks does not
  guarantee a non-negative covariance (an update can help one group of tasks
  and hurt another), so the independent sum is not unconditionally an upper
  bound. An earlier version of this rubric stated the negative-correlation case
  backwards and used the bound as a route to `C`; both are withdrawn, and every
  row that relied on that route was re-read.
- **Aggregates.** For an averaged headline the variation has to cover the
  average (Unit of audit): a test or interval on the aggregate, or component
  statistics that cover every component. Significance on some components with
  the others inconclusive and their dispersion unreported does not
  (`hao2026evolveteam`: six of nine columns significant, no statistic for the
  average).
- **Envelope** is the inference compute of the *scored* runs: model calls,
  turns, attempts or pass@k, reasoning-effort setting, candidates sampled, and
  generated tokens. Search and optimization cost is not envelope; a
  repair-time or evolution-time token total says nothing about the scored runs
  (`chen2026harnessfix`, `opsahlong2024optimizing`). The artifact's own context,
  the tokens of the skill or memory it inserts, is the update's own cost rather
  than a second cause, and is recorded separately from controlled inference effort, but it has to be declared
  (`zhao2024expel`: thought, action and observation counts essentially equal
  across arms, the extra tokens are retrieved context).
- **Controlled** means held equal across arms, reported as a
  performance/cost frontier, or changed in a direction that cannot explain the
  gain. *Declared but unmatched* is `O`: an envelope that is reported does not
  rule out that the envelope produced the difference; it only tells the reader
  that it might have (`zhang2026darwinx`: base at default effort, evolved at
  high; `suzgun2026dynamic`: AIME output tokens 494 under DC-empty, 1035 under
  DC-RS, none for the Game of 24 headline). Requiring control is not requiring
  identical absolute token counts across methods.
- **Selected margins.** If the reported arm was itself chosen among `k` rows on
  the reporting data (a sweep, the best round), the margin has to clear the
  noise of a maximum, which grows with `k`, roughly by `sqrt(2·ln k)` standard
  errors. A margin that clears a single comparison does not by that alone clear
  this.

An earlier version of this section held `suzgun2026dynamic` at `C` on the
since-withdrawn route that credited a large swing without a reported interval,
for its 19%-to-99% swing. Under the envelope
condition above it is `O`: the swing is not noise, but the only envelope
accounting is declared rather than matched and is absent for the headline task.
The old "route (a)" and "route (b)" labels named the earlier two-route rule.
They were removed from every basis entry on 2026-10-10 and replaced with the
condition each entry actually establishes; no verdict changed in the
replacement.

## Improvement

How far does the difference reach?

Three indices, after Section 6.1: the distance of the reporting tasks from the
tasks that formed the update, the strength of the state it was measured
against, and how many rounds after acceptance it was last confirmed. `C` is
scored on the first index alone. The other two are recorded but not graded: the
baseline (pre-update state or a named competing method, see Unit of audit) is
in the `headline` column, and no primary comparison in the file re-estimates a
particular accepted update's contribution after later updates. Secondary
measurements of retained performance exist and are recorded in
`claim-audit-secondary.tsv`: `wang2026valve` reports checkpoint-level final
gain, peak gain and peak-to-final drawdown of the whole bank on a fixed disjoint
panel, and `yu2025polyskill` revisits an earlier task distribution after
adapting to new sites. These track the retained performance of an evolving
state; the examples reviewed here do not by themselves isolate how one accepted
update's causal contribution changes after later revisions.

- `C` — the reporting tasks of the primary comparison sit at a distance from
  the tasks that formed the update: a held-out partition, transfer to a
  benchmark the loop never saw, or a retention probe on an earlier distribution
  the loop does not control.
- `O` — the distance is partial: the reporting set overlaps the evolution set,
  separation rests only on a per-instance retrieval rule
  (`chen2025sweexp`), or a rising online trajectory along one adaptive task
  stream is the only evidence of reach.
- `N` — reported only on the tasks that produced the update, including
  re-solving the failures that prompted the repair.

A transfer or retention result outside the primary comparison does not lift
this cell; it is recorded in `claim-audit-secondary.tsv`. `yu2025polyskill`
leads with its online in-domain Mind2Web number and so sits at `O`, although
its report also re-reads the starting WebArena Shopping benchmark after the loop
has moved on (a Fig 5 case study, +4.9% over ASI, not a retention rate over all
tasks).

Whether the declared distance survived the search is **not** graded here. A
held-out partition consulted by the promotion rule every round still earns
`Improvement = C` and loses its mark under selection. Scoring the same defect
in both columns was the earlier rubric's error: it defined `C` as "evaluated on
tasks that took no part in forming the update", a phrase that states both the
distance condition and the hygiene condition, and then applied only the first.

Two earlier notes that survive the rewrite. `nie2026evolvenet` was counted as a
retention probe in error: its 90% figure is merge-time capability preservation
within one round, not a probe on an earlier distribution. And the old `O`
level's "without a control for the resource or order change" imported an
attribution condition into an improvement grade and has been dropped; resource
control is graded under attribution.

## Procedure

The corpus is a curated literature map, not an exhaustive systematic sample.
Initial coding and repeated recoding were performed primarily with an LLM
(Opus 5.5), under successive versions of the rubric and claim definitions.
These passes are not independent human annotations, and no inter-rater
agreement is claimed. The final revision adds targeted primary-source checks
and mechanical consistency checks; it does not constitute a new full-corpus
human audit.

1. Read the experiments or evaluation section and any protocol appendix, not
   the abstract.
2. Fix the **primary comparison** and its headline number first (Unit of
   audit, above), and record the number in the `headline` column.
3. For selection only: a paper asserting "we evaluate on held-out data" without
   showing the partition boundaries is `O`, not `C`. The other three claims are
   read off the comparison as reported.
4. Record the concrete basis for every verdict: the table, figure, number, or
   sentence it was read off. `claim-audit.tsv` carries these, segmented as
   `SEL: ... ; ACT: ... ; ATT: ... ; IMP: ...` so that each verdict can be
   checked against its own stated evidence.
5. Record any other protocol the report runs in `claim-audit-secondary.tsv`.

`data/claim-audit.tsv` was written from the blind second pass plus per-cell
overrides. The two pass files, the override script, and the record of why each
override was made are kept outside the article project, in the authors' working
directory, and are available on request. Run `scripts/aggregate_claim_audit.py` after any
change: it recomputes Figure 6 and checks Table 4 against the file.

## Known limits

The `C`/`O` boundary is a judgement, and another reader could place some cells
differently; the recorded basis is there so that a disagreement can be taken up
against the source rather than against the verdict. The initial batch of 96
rows was read twice, the second reading blind to the first, and cells on which
the two disagreed were re-read against the primary source and decided under the
rules above; the second-pass file omits the two `X` rows, which have no
evaluation to grade, and `tan2026gskill`, whose full text was obtained only
after the second pass (ACM DL, free access) and which was read once, non-blind,
directly under these rules, and entered after the adjudication of the other
rows. Four rows entered later, `wang2026verse`, `yang2026guiharvest`,
`wang2026valve` and `tian2026ceiling`, appear in neither pass file, so this
record does not show a blind second reading for them; their verdicts were read
directly under these rules, and the 2026-10-10 amendment log kept beside the
pass files in the authors' working directory records the source paragraphs
checked for `wang2026valve` and `tian2026ceiling`.

The `C` rate for activation by update target, counted over the in-scope
branches of Figure 3, is 0/12 for prompts and instructions, 3/31 for context
and memory, 1/12 for workflow, 3/18 for tools and code patches, 0/16 for
repository and runtime logic, and 1/4 for plugin-level work
(`scripts/aggregate_claim_audit.py` prints these). An earlier version of this
note reported a spread from 8% for prompts to 60% for repository and runtime
logic, because "the program runs by construction" was then credited at `C`;
under the activation rule above those cells are `O`, since the artifacts are
executable but no scored run is instrumented.

## Revision of 2026-10-09

Rules changed: the scope layer was added; the activation `C` proposition was
stated as existence with recorded coverage, and the `O` list was extended to
cases that cannot be bound to the primary comparison; attribution was restated
as three conditions with a fixed standard for clearing measured variation, the
auditor's binomial bound was withdrawn as a route to `C` and its covariance
direction corrected, and an aggregate rule was added. Every row whose cell
depended on a changed rule was re-read against its source; the cells that
changed, each with its reason in the basis:

- scope `out`: `gao2026swemem`, `zhang2026action`, `wang2026swepruner`,
  `xiao2026socraticswe`;
- activation `C` to `O`: `ren2026taco` (other backbones), `lee2026metaharness`
  (program runs by construction; aggregate tokens), `yang2026vaso` (the
  compliance check is the metric), `zhang2026action` (7B statistics, 14B
  headline);
- attribution `C` to `O`: `fang2026memp`, `ouyang2026reasoningbank`,
  `xiong2026memorymgmt`, `yang2026skillopt`, `zhang2026selfharness` (auditor
  bound only); `ren2026taco` (margin within the measured variation);
  `wang2025workflow` (published-baseline comparator differs in setup);
  `xu2026lifeharness`, `hao2026evolveteam` (aggregate not covered);
  `lin2026muse` (no dispersion for the unchanged arm or the difference);
  `yue2026ecdysis`, `huang2026consumption`, `zhou2023large` (no dispersion for
  the headline margin).

Basis corrections without a verdict change: `zhao2024expel` (transfer is
HotpotQA to FEVER; what the fold SE measures; the showcase trajectories),
`opsahlong2024optimizing` (Wilcoxon over test examples; search budget is not
envelope), `tao2025delvepo` (task model DeepSeek-R1-Distill-Llama-8B at
temperature 0.5), `hu2026evorepair`, `yang2026gse`, `du2026livingharness`,
`xia2025liveswe`, `wang2026effiskill` (why each activation case does not bind),
and the coverage or audit-computation notes on `chen2026harnessx`,
`zhang2025supernet`, `zhou2026multiagent`, `xia2026rrsi`, `ni2026trace2skill`,
`gong2026skillmoo`.

## Revision of 2026-10-10

The scope layer, the activation exception and the amendment record were the
rules touched; no number in the tables was changed to preserve an earlier
total. Verdict changes, each with its source paragraph and the rule applied:

- scope `in` to `out`: `aggarwal2026behavioral`. The rules are authored by
  people, not formed by the system: an engineer decides whether an accepted
  review comment is a generalizable mistake and codifies it (Sec II-C, II-D),
  rule changes go through team pull-request review, deployment depends on
  engineers codifying each comment (Sec VIII), and automated rule proposal and
  conflict detection is listed under future work. Section 2 of the survey
  excludes a human authoring the payload and installing it, so this is a
  human-maintained rule file rather than an algorithmic update; it is kept as a
  boundary case in Section 3.2 and removed from Figure 3, from Figure 2's
  growth ledger and inset, and from the Figure 6 population.
- attribution `C` to `O`: `pryzant2023automatic`. The headline compares ProTeGi
  with the original prompt p0 (Sec 3.4, Fig 3: +15.3% test F1, averaged over 3
  trials). The repeated experiment (Appendix C, Table 5) compares ProTeGi with
  MC, not p0, at a different budget (6 queries per candidate against 12-50
  evaluations per prompt in Fig 3) and reports accuracy rather than the F1 of
  the main results, so it does not supply the variation for the comparison the
  headline states. No other dispersion, interval or test is reported for the p0
  margin. The report does measure variation; it is measured elsewhere.

Basis corrections without a verdict change:

- `pryzant2023automatic` (ACT): the prompt is the classifier instruction handed
  to gpt-3.5-turbo with a fixed, randomly selected pair of few-shot examples
  held constant while the rest of the prompt is optimized (Sec 3.1), not a
  zero-shot instruction.
- `chen2026harnessx` (ACT): the binding case is the round-10 composite edit
  C-R10-02 on GAIA / Sonnet 4.6, whose declared signature is `tool_call on
  WikiTextFetch, >= 1 call; verified against the next round's trace` (Fig 7),
  read together with Sec 6.6 ("trace analysis at R11 revealed that the tool
  genuinely fixed retrieval for most newly passing tasks") against the Table 4
  headline round R11 at 83.5%. The Appendix C.1 case (R10, 74.8% to 79.6%) is
  outcome evidence for round 10 and is noted as such rather than used as the
  activation record. Coverage is one of 15 configurations.
- `ren2026flowevo` (ACT): the 101-of-134 reuse count with 99 succeeding is the
  representative run behind Fig 2b and Tables 15-16, not a pooled count over the
  three seeds, and the direct-reuse route counts `direct_skill` and
  `direct_then_*` episodes rather than the `direct_skill` column alone.
- `tian2026ceiling` (headline and ATT): the headline is 0.164 (4-rollout mean)
  against 0.297, a closing anchor measured two nights earlier with 2 rollouts
  (Table 5 and its note; Limitations). No paired SE or interval is reported for
  that pair, and the Appendix A dispersion (per-rollout SD median 0.023, worst
  0.042, over 26 same-night cells) is a pooled quantity, so it is recorded as an
  audit computation carrying that limit rather than as the report's variance for
  this difference. The serving context was raised from 131k to 262k between
  round 11 and the close; both the closing anchor and the later seed
  re-measurement fall after that change, with the serving stack pinned.
- `yu2025polyskill` (secondary ledger): `+4.9%` over ASI is the case study of
  Fig 5, not a corpus-wide retention rate, and the report does not lead with it.

The secondary ledger also drops the phrase `inside any noise band at n=500`.
Task count alone does not define a noise band; the entry now says what the
report does and does not supply for the difference.

`wang2026valve` is added to the secondary ledger as a checkpoint-level retention
and drawdown measurement, at selection `O` because the peak checkpoint is picked
on the evaluation panel, which the report says is not an untouched final-test
estimate.



## Final revision of 2026-10-10

The table and figure labels now describe criterion coverage. Activation C is
existence with recorded coverage; Improvement C is task-distance evidence, not
a complete positive-effect claim. Four-of-four is not a method quality score.

`tian2026ceiling`: Attribution C -> O. The +0.133 headline compares a four-rollout
seed mean with a two-rollout evolved mean on different nights. Appendix A's
maximum SD across 26 other cells is neither dispersion for these arms nor an
upper bound on their variance. The prior calculation adding two SE from that
pooled maximum to an observed cross-night drift is withdrawn. This applies the
existing primary-comparison rule; no other verdict was changed in this revision.
The resulting Attribution counts are C/O/N = 10/82/1; criteria met per comparison
0..4 = 26/27/33/7/0, and the COOC profile occurs 28 times.
