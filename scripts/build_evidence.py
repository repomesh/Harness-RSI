#!/usr/bin/env python3
"""Generate evidence tables and bilingual summaries from data/reported-evidence.json."""
import argparse
import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ['selection', 'activation', 'attribution', 'improvement']
BADGE = {'C': '✅', 'O': '◐', 'N': '—', 'X': 'n/a'}


def load_evidence():
    data = json.loads((ROOT / 'data/reported-evidence.json').read_text())
    methods = data['methods']
    assert len({r['key'] for r in methods}) == len(methods), 'Duplicate method key'
    for row in methods:
        assert all(row[c] in BADGE for c in CLAIMS), row['key']
        assert all(row[c] == 'X' for c in CLAIMS) or all(row[c] != 'X' for c in CLAIMS), row['key']
        assert row['basis'] and (row['headline'] or row['selection'] == 'X'), row['key']
    scored = [r for r in methods if r['selection'] != 'X']
    per = [{code: sum(r[c] == code for r in scored) for code in 'CON'} for c in CLAIMS]
    joint = [sum(sum(r[c] == 'C' for c in CLAIMS) == k for r in scored) for k in range(5)]
    return data, scored, per, joint


def table(per, zh=False):
    lines = ['| Claim | ✅ '+('充分' if zh else 'Full')+' | ◐ '+('部分' if zh else 'Partial')+' | — '+('不支持' if zh else 'Not supported')+' |', '|---|---:|---:|---:|']
    for name, counts in zip(CLAIMS, per):
        lines.append('| '+name.capitalize()+' | '+' | '.join(str(counts[c]) for c in 'CON')+' |')
    return '\n'.join(lines)


def summary(data, scored, per, joint, zh=False, compact=True):
    total, n = len(data['methods']), len(scored)
    if zh:
        intro = f'两个更新对象分支共收录 {total} 个方法，其中 {total-n} 个没有实证评测。下表依据其余 {n} 份报告的主要比较，分别判定四项 claims 的证据。'
        all_four = '没有报告四项均充分' if joint[4] == 0 else f'{joint[4]} 份报告四项均充分'
        finding = f'同一项比较中，{joint[3]} 份报告有三项 claim 的证据充分，{all_four}。各项标准与覆盖范围不同，数量不能直接用于比较方法质量。'
        links = '各方法的比较设置、判定与来源见[完整结果](docs/reported-evidence.md)，具体要求见[判定标准](docs/evidence-criteria.md)。'
    else:
        intro = f'The two update-target branches contain {total} methods; {total-n} report no empirical evaluation. The counts below cover the other {n} reports, using one primary comparison per report for all four claims.'
        all_four = 'none establish all four' if joint[4] == 0 else f'{joint[4]} establish all four'
        finding = f'Within one comparison, {joint[3]} reports establish three claims in full and {all_four}. Criteria and coverage differ across claims, so these counts do not rank method quality.'
        links = 'See the [full results](docs/reported-evidence.md) for comparisons, judgments, and sources, and the [criteria](docs/evidence-criteria.md) for their definitions.'
    parts = [intro, table(per, zh), finding]
    if compact:
        parts.append(links)
    else:
        parts.extend([
            'Number of claims at full evidence within one report. A report with none may still provide partial evidence.',
            '| 0 | 1 | 2 | 3 | 4 |\n|---:|---:|---:|---:|---:|\n| ' + ' | '.join(map(str, joint)) + ' |',
            'The most common profile combines full Selection and Improvement with partial Activation and Attribution. Full Activation can rest on one confirmed case; each method’s details record the coverage.',
        ])
    return '\n\n'.join(parts)


def prose(text):
    """Keep source comparisons such as < and > visible in Markdown."""
    return html.escape(' '.join(text.split()), quote=False)


def render_basis(row):
    if row['selection'] == 'X':
        return prose(row['basis'])
    parts = re.split(r'(?:^|;)\s*(SEL|ACT|ATT|IMP):\s*', row['basis'])
    assert not parts[0].strip() and parts[1::2] == ['SEL', 'ACT', 'ATT', 'IMP'], row['key']
    labels = {'C': 'Full evidence', 'O': 'Partial', 'N': 'Not supported'}
    return '\n\n'.join(
        f'**{claim.capitalize()} ({labels[row[claim]]}).** {prose(basis)}'
        for claim, basis in zip(CLAIMS, parts[2::2])
    )


def render_doc(data, scored, per, joint):
    methods = sorted(data['methods'], key=lambda row: row['name'].lower())
    by_key = {row['key']: row for row in methods}
    out = [
        '# Reported Evidence',
        'Evidence for Selection, Activation, Attribution, and Improvement in each method’s primary reported comparison. The [criteria](evidence-criteria.md) define the judgments; the [reading list](../README.md#evidence) gives a short summary.',
        '[Summary](#summary) · [By update target](#by-update-target) · [Verdicts](#verdicts) · [Method details](#method-details) · [Other protocols](#other-protocols)',
        '## Summary',
        summary(data, scored, per, joint, compact=False),
        '![Reported evidence from the companion manuscript](../assets/reported-evidence.png)',
        '## By update target',
    ]
    rows = ['| Update target | Reports | Sel. ✅ | Act. ✅ | Att. ✅ | Imp. ✅ |', '|---|---:|---:|---:|---:|---:|']
    for sub in dict.fromkeys(row['sub'] for row in data['methods']):
        group = [row for row in scored if row['sub'] == sub]
        counts = [sum(row[claim] == 'C' for row in group) for claim in CLAIMS]
        rows.append('| ' + sub + ' | ' + ' | '.join(map(str, [len(group), *counts])) + ' |')
    out.extend(['\n'.join(rows), '## Verdicts', '✅ Full evidence · ◐ Partial · — Not supported · n/a No empirical evaluation. All four cells refer to the same primary comparison. Open a method’s details for the supporting passages and coverage.'])
    rows = ['| Method · primary report | Update target · details | Sel. | Act. | Att. | Imp. |', '|---|---|:-:|:-:|:-:|:-:|']
    for row in methods:
        rows.append(
            f'| [**{row["name"]}**]({row["url"]}) <sub>`{row["venue"]}`</sub> | '
            f'{row["branch"].split()[0]} · {row["mechanism"]} · [details](#{row["key"]}) | '
            + ' | '.join(BADGE[row[claim]] for claim in CLAIMS) + ' |'
        )
    out.extend(['\n'.join(rows), '## Method details', 'Expand a method to read its primary comparison and the basis for each claim. Section, table, and figure references refer to the linked primary report. Calculations and coverage come from the manuscript’s per-method records.'])
    for row in methods:
        headline = prose(row['headline']) if row['headline'] else 'No empirical evaluation.'
        out.append(
            f'<a id="{row["key"]}"></a>\n\n<details>\n'
            f'<summary><strong>{html.escape(row["name"])}</strong></summary>\n\n'
            f'[Primary report]({row["url"]})\n\n**Primary comparison.** {headline}\n\n'
            + render_basis(row) + '\n\n</details>'
        )
    out.extend(['## Other protocols', 'These secondary experiments are recorded separately and excluded from the totals above.'])
    for row in data['secondary']:
        out.append(
            f'### {by_key[row["key"]]["name"]}\n\n'
            f'**Protocol.** {prose(row["protocol"])}\n\n'
            f'Selection: {BADGE[row["selection"]]} · Improvement: {BADGE[row["improvement"]]}\n\n'
            f'{prose(row["basis"])}'
        )
    out.extend([
        '## Data and reproduction',
        '[Evidence data](../data/reported-evidence.json) · [Taxonomy](../data/taxonomy.json) · [Manuscript snapshot](../data/source-snapshot.json). This document is generated by `python3 scripts/build_evidence.py`; see [Contributing](../CONTRIBUTING.md) for corrections.',
    ])
    return '\n\n'.join(out) + '\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data,scored,per,joint=load_evidence()
    expected={ROOT/'docs/reported-evidence.md':render_doc(data,scored,per,joint)}
    for lang,path in [('en','README.md'),('zh','README_zh.md')]:
        target=ROOT/path
        replacement='<!-- evidence-summary:start -->\n\n'+summary(data,scored,per,joint,lang=='zh')+'\n\n<!-- evidence-summary:end -->'
        text,count=re.subn(r'<!-- evidence-summary:start -->.*?<!-- evidence-summary:end -->',lambda _:replacement,target.read_text(),flags=re.S)
        assert count==1,path
        expected[target]=text
    stale=[str(p.relative_to(ROOT)) for p,text in expected.items() if not p.exists() or p.read_text()!=text]
    if args.check:
        if stale:raise SystemExit('Evidence artifacts are stale: '+', '.join(stale))
    else:
        for path,text in expected.items():path.write_text(text)
    print(f'Evidence: {len(data["methods"])} methods, {len(scored)} scored; '+('checked' if args.check else 'generated'))

if __name__=='__main__':
    main()
