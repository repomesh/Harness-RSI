# Contributing

Contributions should improve placement, mechanism descriptions, or evidence. Keep the English and Chinese lists synchronized.

## Adding or correcting a work

1. Identify the primary update object, feedback source, admission rule, and state retained for later execution. Evaluation protocols belong in Section 4; theory is Section 3. Offline antecedents and limited-persistence mechanisms must be described as such.
2. Use one primary placement. Theory may refer to an existing method to explain a correspondence.
3. Give a concise mechanism description and a verified primary-source link. Preserve technical names in the Chinese version. Add code or project links only when the paper identifies them.

```markdown
- **Name** `Venue'YY` — one-sentence mechanism. [[paper]](url) [[code]](url)
```

The Chinese version uses `：` in place of the English separator. Use the actual venue when confirmed; otherwise retain the preprint label.

## Audit changes

Read [the rubric](docs/audit-rubric.md). Each method’s four verdicts refer to one headline comparison. Record the model, benchmark, configuration, baseline, and round. Cite the passage, figure, table, or statistic supporting every changed cell, including the coverage of Activation evidence.

Edit [data/claim-audit.json](data/claim-audit.json), then regenerate the derived files. Keep [data/taxonomy.json](data/taxonomy.json) aligned with the manuscript. Secondary protocols remain separate from headline totals. Weight-only or fixed-component work does not enter the update-target population.

For disagreements, quote both the recorded basis and the primary-source passage, and propose a specific correction. Automated checks verify consistency; they do not replace source reading.

## Verification

```bash
python3 scripts/build_audit.py
python3 scripts/build_site_data.py
python3 scripts/check_consistency.py
python3 scripts/check_consistency.py --links  # optional network check
```

The checker covers anchors, bilingual entries and links, duplicate entries, local assets, taxonomy placement, and generated audit/site data. Check manuscript source hashes when synchronizing a new paper revision.

Preview `index.html` using a local HTTP server. Check the desktop and mobile layouts, search and filters, figure enlargement, keyboard navigation, and browser console. The site is published from `main` at the repository root to [GitHub Pages](https://zgcagi.github.io/Harness-RSI/).
