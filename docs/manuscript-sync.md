# Manuscript synchronization — 17 October 2026

The full report and short paper are separate source projects. Their current sources were synchronized from Overleaf; the public OpenReview and arXiv URLs remain the publication links and are not assumed to serve these exact builds.

| Artifact | Source commit | Local verification build |
|---|---|---|
| [Full report](../paper/harness-self-evolution.pdf) | `75a40cdb3bcc0045518be84acc85ca5ae0d8d05c` | 66 pages, 262 bibliography entries |
| [Short paper](../paper/self-evolving-agent-harness.pdf) | `fd8ad5c518f5372f66df6857d5339814ddb6037a` | 18 pages, 85 bibliography entries |

Source and PDF hashes are recorded in [source-snapshot.json](../data/source-snapshot.json). Bibliographies are copied verbatim from the respective sources: [full](../paper/harness-self-evolution-references.bib) and [short](../paper/self-evolving-agent-harness-references.bib).

## Changes reflected in the companion materials

- Replace the website abstract with the current full-report abstract; align the Chinese author list with all eight manuscript authors.
- Refresh the evaluation diagram and manuscript-derived tables and taxonomy, including current citation numbering.
- Clarify activation's carried grade: downstream runtime decisions and outputs count alongside model-input propagation and interpreted-guidance adherence. This is a terminology clarification, not a recoding of primary comparisons.
- Reflect the expanded discussion of runtime composition, medical tool admission, environment design, compositional contracts, dynamic evaluation, and authorization boundaries.
- Preserve the short paper's case-study qualifications: unmatched-cost model crossovers, inconsistent first-task and cumulative EIP costs, and fixed-deployment latency evidence.

The 95-method scope, 93 scored comparisons, raw audit records, and verdicts are unchanged. The evidence date remains 10 October 2026 and the literature cutoff remains 8 October; the synchronization date does not imply a new literature search or audit.

## Verification

At the 17 October synchronization, both PDFs were built locally with `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` from the recorded source commits. Builds resolve citations and references without overfull boxes. The full report retains font-size substitution and caption/hypcap warnings; these were not source edits. Local compilation does not verify Overleaf cloud compilation or update the external publication PDFs.

## Full-report PDF update — 18 October 2026

The distributed [full-report PDF](../paper/harness-self-evolution.pdf) was replaced with the user-provided `HarnessOpt_survey (4).pdf` (66 pages). The README and project-page full-version links now open the GitHub PDF. Its SHA-256 is recorded as `sha256.main.pdf` in [source-snapshot.json](../data/source-snapshot.json). The source snapshot and short paper remain unchanged; correspondence between the replacement PDF and the recorded source commit has not been verified. The local-build verification above describes the earlier PDFs.

## Harness-Zero citation update — 23 October 2026

Added [Harness-Zero](https://arxiv.org/abs/2609.24974) to the full report's Model–Harness–Environment Co-Evolution subsection and the short paper's Model–Harness Co-Design subsection. Both describe distillation into model weights while retaining a minimal target harness, and connect it to future harness evolution.

| Artifact | Source commit | Local verification build |
|---|---|---|
| [Full report](../paper/harness-self-evolution.pdf) | `e76b3ffafba3aa6fe4548539e785090e57a0c1a6` | 66 pages, 263 bibliography entries |
| [Short paper](../paper/self-evolving-agent-harness.pdf) | `ff66a471e3f0fe07c9e35bd0c0147fd74af7a8e8` | 18 pages, 86 bibliography entries |

Both distributed PDFs and bibliography files now match these source revisions; this supersedes the 18 October PDF provenance caveat. Builds resolve all citations and references without overfull boxes. The new paragraphs and bibliography entries were visually inspected. Existing full-report font substitution and caption/hypcap warnings remain. Overleaf cloud compilation has not been verified. No audit entries or verdicts were changed, and arXiv has not been updated.
