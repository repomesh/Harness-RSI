#!/usr/bin/env python3
"""Generate audit tables and bilingual summaries from data/claim-audit.json."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ['selection', 'activation', 'attribution', 'improvement']
BADGE = {'C': '✅', 'O': '◐', 'N': '—', 'X': 'n/a'}


def load_audit():
    data = json.loads((ROOT / 'data/claim-audit.json').read_text())
    methods = data['methods']
    assert len({r['key'] for r in methods}) == len(methods), 'Duplicate audit key'
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


def summary(data, scored, per, joint, zh=False):
    total, n = len(data['methods']), len(scored)
    if zh:
        intro=f'审计覆盖论文两个更新对象分支中的 **{total} 个方法**，其中 {total-n} 个没有实证评测，{n} 份报告计入评分。每行固定一项主结果对应的比较，再读取四个 verdicts。'
        reading='判定描述报告提供了什么证据。各列标准不同，不能把充分证据的数量直接当作方法质量排名。Activation 的充分证据可能只覆盖一个已确认实例，覆盖范围记录在逐方法依据中。'
        joint_intro='同一份报告达到充分证据的 claim 数量：'
        finding=f'最常见的组合是 Selection 与 Improvement 充分、Activation 与 Attribution 部分。Activation 充分的报告有 {per[1]["C"]} 份，Attribution 充分的有 {per[2]["C"]} 份；详细判定需结合各自主结果与覆盖范围阅读。'
        end='逐方法 verdicts、主结果与依据见[完整审计](docs/claim-audit.md)，判据见 [rubric](docs/audit-rubric.md)。'
    else:
        intro=f'The audit covers **{total} methods** in the manuscript’s two update-target branches. Of these, {total-n} have no empirical evaluation and {n} reports are scored. Every row fixes one headline comparison before assigning all four verdicts.'
        reading='Verdicts describe reported evidence. The criteria differ, so full-evidence counts are not a ranking of method quality. Activation can meet its criterion with one confirmed case; the per-method basis records the coverage.'
        joint_intro='Number of claims at full evidence within one report:'
        finding=f'The most common profile has full Selection and Improvement with partial Activation and Attribution. {per[1]["C"]} reports meet Activation and {per[2]["C"]} meet Attribution; interpret each verdict within its headline comparison and recorded coverage.'
        end='See the [full audit](docs/claim-audit.md) for verdicts, headline comparisons, and recorded evidence, and the [rubric](docs/audit-rubric.md) for criteria.'
    return '\n\n'.join([intro,table(per,zh),reading,joint_intro,'| 0 | 1 | 2 | 3 | 4 |\n|---:|---:|---:|---:|---:|\n| '+' | '.join(map(str,joint))+' |',finding,end])


def cell(text):
    return ' '.join(text.split()).replace('|', '\\|')


def render_doc(data, scored, per, joint):
    methods = sorted(data['methods'], key=lambda x:x['name'].lower())
    by_key = {r['key']:r for r in methods}
    out=['# Evidence Audit',summary(data,scored,per,joint).rsplit('\n\n',1)[0] + '\n\nRead the [rubric](audit-rubric.md) for the evidence criteria. The [reading-list summary](../README.md#audit) provides a shorter introduction.',
         'Source: [machine-readable audit](../data/claim-audit.json), [taxonomy](../data/taxonomy.json), and [manuscript snapshot](../data/source-snapshot.json). Regenerate with `python3 scripts/build_audit.py`.',
         '![Evidence audit from the companion manuscript](../assets/claim-audit.png)\n\n## By update target', '| Update target | n | Sel. ✅ | Act. ✅ | Att. ✅ | Imp. ✅ |\n|---|---:|---:|---:|---:|---:|']
    for sub in dict.fromkeys(r['sub'] for r in data['methods']):
        rs=[r for r in scored if r['sub']==sub]
        out.append('| '+sub+' | '+str(len(rs))+' | '+' | '.join(str(sum(r[c]=='C' for r in rs)) for c in CLAIMS)+' |')
    out+=['\n## Verdicts','All four cells refer to the same headline. `n/a` denotes no empirical evaluation.', '| Method | Branch · mechanism | Sel. | Act. | Att. | Imp. |\n|---|---|:-:|:-:|:-:|:-:|']
    for r in methods:
        out.append(f'| [**{r["name"]}**]({r["url"]}) <sub>`{r["venue"]}`</sub> | {r["branch"].split()[0]} · {r["mechanism"]} | '+' | '.join(BADGE[r[c]] for c in CLAIMS)+' |')
    out+=['\n## Recorded basis','Section and table references below refer to each linked primary report. SEL / ACT / ATT / IMP separate the four claims. Coverage and audit computations are preserved from the manuscript audit.', '| Method | Headline | Recorded basis |\n|---|---|---|']
    for r in methods:
        out.append(f'| [**{r["name"]}**]({r["url"]}) | {cell(r["headline"])} | {cell(r["basis"])} |')
    out+=['\n## Other protocols','Secondary experiments are recorded separately and excluded from the headline totals.', '| Method | Protocol | Sel. | Imp. | Basis |\n|---|---|:-:|:-:|---|']
    for r in data['secondary']:
        out.append(f'| **{by_key[r["key"]]["name"]}** | {cell(r["protocol"])} | {BADGE[r["selection"]]} | {BADGE[r["improvement"]]} | {cell(r["basis"])} |')
    result = ''
    previous_table = False
    for chunk in out:
        is_table = chunk.startswith('|')
        result += ('\n' if is_table and previous_table else '\n\n') + chunk.strip()
        previous_table = is_table
    return result.strip() + '\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data,scored,per,joint=load_audit()
    expected={ROOT/'docs/claim-audit.md':render_doc(data,scored,per,joint)}
    for lang,path in [('en','README.md'),('zh','README_zh.md')]:
        target=ROOT/path
        replacement='<!-- audit-summary:start -->\n\n'+summary(data,scored,per,joint,lang=='zh')+'\n\n<!-- audit-summary:end -->'
        text,count=re.subn(r'<!-- audit-summary:start -->.*?<!-- audit-summary:end -->',lambda _:replacement,target.read_text(),flags=re.S)
        assert count==1,path
        expected[target]=text
    stale=[str(p.relative_to(ROOT)) for p,text in expected.items() if not p.exists() or p.read_text()!=text]
    if args.check:
        if stale:raise SystemExit('Audit artifacts are stale: '+', '.join(stale))
    else:
        for path,text in expected.items():path.write_text(text)
    print(f'Audit: {len(data["methods"])} methods, {len(scored)} scored; '+('checked' if args.check else 'generated'))

if __name__=='__main__':
    main()
