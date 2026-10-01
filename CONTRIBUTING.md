# Contributing

Pull requests are welcome. This list is organized by a theory, not by coverage, so the review bar is about **placement and evidence** rather than volume.

## 1. Scope check

State explicitly which of the three conditions the work satisfies:

| Condition | Test |
|---|---|
| **Persistence** | The revision is written into harness state that a *later* run loads, so it governs rollouts it did not generate. |
| **Recursion** | Adopted revisions govern later execution, and the resulting rollouts inform further revisions. |
| **Fixed model** | No weight update inside the loop. |

If the work fails any of them, it may still belong in [Boundary Cases & Exclusions](README.md#boundary-cases--exclusions) — add it there with the reason, which is more useful than a borderline entry in the taxonomy.

Out of scope, with no exceptions:

- Runtime-only self-correction (the correction is consumed inside the same rollout).
- Weight-side self-improvement (violates the fixed-model premise).
- Static agent frameworks that are not revised from feedback.

## 2. Pick exactly one node

Every work is listed **once**, under the node matching what the work **itself** contributes — not every surface it touches. In your PR, name the path:

```
branch → subsection → mechanism
e.g. Executable Update Targets → Tools & Code Patches → Evidence-Grounded Component Patching
```

Three rules settle most hard cases:

1. **Contribution, not surface.** A system that patches tools *and* rewrites prompts goes under its primary contribution; mention the extra surface in the mechanism sentence instead of adding a second entry.
2. **Protocols go to Section 3.** If the work's own contribution is an evaluation protocol, benchmark, or audit, it belongs in *Evaluation & Benchmarks* even if it also ships a system. Conversely, a system that Section 3 merely *cites as an example* stays in its update-target branch.
3. **Section 4 is the one exception to listing-once**, because its contribution is the mapping itself.

A work needing a new mechanism node is a reasonable PR — say which existing node it would otherwise distort and why, and expect discussion.

## 3. Entry format

One line, no exceptions:

```markdown
- **Name** `Venue'YY` — one-sentence mechanism. [[paper]](url) [[code]](url)
```

- **Name** — the short name the paper gives itself, not the full title.
- **Venue'YY** — a two-digit year and the venue short form (`ICLR'26`, `ACL'26 Findings`, `arXiv'26`, `TMLR'25`). Use `arXiv'YY` until the work is accepted somewhere, then upgrade it. If the label names a published venue, the link should point at that venue's page rather than the preprint.
- **Mechanism sentence** — what the system does *to its own harness*: what it proposes, what admits it, what persists. Not what it scores. One sentence, no results, no adjectives.
- **Link** — a confirmed arXiv ID, DOI, or venue page. **Do not guess a URL.** A proceedings path that merely returns HTTP 200 is not confirmation; check that the page is the right paper. If no stable identifier exists, say so in the PR rather than inventing one.
- **Second link, optional** — `[[code]]` for a repository, `[[project]]` for a project page, `[[list]]` for a sibling reading list. **Add one only if the paper itself states it**, in its abstract, comment, or body. A repository you found by searching the authors' GitHub does not qualify: a plausible-looking wrong repo is worse than no link. Every second link currently in the list came from the paper's own arXiv abstract or comment field and was then checked for a 200.

### Counts that have to move with the entry

Adding or removing an entry changes three places besides the entry itself:

- the `papers` badge at the top,
- the count in the **Jump to a mechanism** index for that node,
- the audit totals in [Section 5](README.md#5-evidence-audit-of-96-methods), if the entry is a Section 1–2 method and you supply verdicts.

Say in the PR which of these you updated.

## 4. Claim verdicts (optional, high value)

For a new method in Sections 1–2, a row for [`docs/claim-audit.md`](docs/claim-audit.md) makes the entry considerably more useful than the link alone.

Before scoring anything, read the [rubric](docs/claim-audit.md#rubric). Then:

1. Read the **experiments section and any protocol appendix of the primary source** — not the abstract, and not another paper's description of it.
2. Give four independent verdicts: ✅ / ◐ / — (or `n/a` if the work reports no empirical evaluation).
3. **Record the basis for every cell**: the table, figure, number, or sentence the verdict was read off. A verdict without a basis will not be merged.

Two recurring mistakes:

- A paper asserting "we evaluate on held-out data" without showing the partition boundaries is **◐**, not ✅.
- Evidence that an edit's predicted *effect* matched later outcomes is **attribution** evidence, not activation evidence.

## 5. Disagreeing with an existing verdict

This is a legitimate PR and the reason the basis is recorded. Quote the recorded basis, quote the passage from the source you think it misreads, and propose the replacement verdict. Arguments about the method's quality are out of scope — the verdicts describe what a report contains.

## 6. Before opening the PR

Run the checker:

```bash
python3 scripts/check_consistency.py           # structure, no network
python3 scripts/check_consistency.py --links   # also resolves every URL
```

It verifies five things: every `](#anchor)` matches a real heading, no heading carries an emoji (which would change its id and break hand-written links to it), no entry is listed twice, the two language versions cover the same works with the same links, and no file is either linked-but-missing or present-but-unreachable. A green run is necessary, not sufficient — it cannot tell you a link points at the *wrong* paper, which is the check only you can do.

Then confirm by hand:

- The link opens the paper you meant, not merely something that returns HTTP 200.
- The mechanism sentence would still be accurate if the reported numbers changed.

## 7. Two structural rules

- **Do not use `<details>` to carry a taxonomy level.** Collapsed content is not findable with the browser's own search, so a mechanism node hidden inside one is effectively missing for anyone scanning the page. `<details>` is for an aside a reader can skip — the scope exclusions, the longitudinal control table — never for entries.
- **Do not add a file nothing links to.** Every page and asset must be reachable from `README.md` or `README_zh.md`; the checker fails on an unreachable one. A better-formatted list in an unlinked subdirectory helps nobody.
