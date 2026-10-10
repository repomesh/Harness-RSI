# Contributing

Keep the English and Chinese reading lists synchronized. Contributions can add papers, clarify mechanisms, or correct the evidence for a reported result.

## Papers and descriptions

Place each work under its primary update target or evaluation protocol. Describe what changes, what feedback drives it, and what state later runs retain. Note offline optimization or limited persistence when relevant. Theory may reference an already listed method to explain a correspondence.

Use a concise mechanism description, a primary-source link, and the confirmed venue or preprint label. Add code and project links identified by the paper. Keep technical names in the Chinese version.

```markdown
- **Name** `Venue'YY` — one-sentence mechanism. [[paper]](url) [[code]](url)
```

Use `：` instead of ` — ` in Chinese entries.

## Evidence corrections

Follow the [criteria](docs/evidence-criteria.md). Identify the report’s primary comparison, including model, benchmark, baseline, configuration, and round. Cite the passage or statistic supporting each changed judgment, and record how many runs the Activation evidence covers. Keep secondary experiments separate.

| Source file | What to edit |
|---|---|
| [README.md](README.md), [README_zh.md](README_zh.md) | Paper entries and section descriptions |
| [data/taxonomy.json](data/taxonomy.json) | Manuscript citation keys and primary placements |
| [data/reported-evidence.json](data/reported-evidence.json) | Comparisons, judgments, and supporting passages |
| [data/source-snapshot.json](data/source-snapshot.json) | Manuscript commit and source hashes when importing a revision |
| [Paper PDF](paper/harness-self-evolution.pdf) | Copy the verified PDF from that same manuscript revision |

The evidence summaries in the READMEs and website, [results document](docs/reported-evidence.md), and `site/corpus.js` are generated. Update their source files, then run:

```bash
python3 scripts/build_evidence.py
python3 scripts/build_site_data.py
python3 scripts/check_consistency.py
```

The checker verifies bilingual entries, links, anchors, taxonomy placement, generated files, and citation consistency. `--links` adds an optional network check. These checks establish consistency; source passages determine the judgments.

## Manuscript citation

Keep the title, full author list, and author order aligned with the manuscript title page. Update the BibTeX in both READMEs and `index.html` together. Add an arXiv identifier, DOI, or venue only after its public record is available.

## Website

Serve the repository with `python3 -m http.server 8000` and open `http://localhost:8000`. For visual changes, check desktop and mobile layouts, formulas, search, filters, figure enlargement, and keyboard navigation.

GitHub Pages publishes `main` from the repository root at [zgcagi.github.io/Harness-RSI](https://zgcagi.github.io/Harness-RSI/). The site and reading list share this repository.
