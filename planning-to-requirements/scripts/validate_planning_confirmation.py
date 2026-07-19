#!/usr/bin/env python3
"""Validate a PCTR planning confirmation and acceptance Markdown document."""
from __future__ import annotations
import argparse,re
from pathlib import Path
FEATURE_RE=re.compile(r'^##\s+([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+-\d{3})\s+(.+)$',re.M)
REQUIRED=('功能简述','当前实现范围','需要策划确认','策划最终确认摘要','策划验收点','策划验收记录')
def validate(text:str)->list[str]:
    errors=[]; matches=list(FEATURE_RE.finditer(text)); seen=set(); cids=[]; aids=[]
    if not matches:return ['no feature sections found']
    for i,m in enumerate(matches):
        fid=m.group(1); end=matches[i+1].start() if i+1<len(matches) else len(text); body=text[m.end():end]
        if fid in seen: errors.append(f'duplicate feature id: {fid}')
        seen.add(fid)
        for label in REQUIRED:
            if label not in body: errors.append(f'{fid}: missing {label}')
        local_c=re.findall(r'PC-'+re.escape(fid)+r'-\d{2}',body); local_a=re.findall(r'PA-'+re.escape(fid)+r'-\d{2}',body); cids+=local_c; aids+=local_a
        confirmed=bool(re.search(r'-\s*确认状态：\s*(已确认|confirmed)',body,re.I))
        if confirmed:
            pending_block=re.search(r'是否阻塞开发：\s*是[\s\S]*?状态：\s*待确认',body)
            if pending_block: errors.append(f'{fid}: confirmed with pending blocking item')
            if not re.search(r'-\s*最终确认内容：\s*\S+',body): errors.append(f'{fid}: confirmed without final summary')
    for label,vals in [('confirmation',cids),('acceptance',aids)]:
        dup={x for x in vals if vals.count(x)>1}
        for x in sorted(dup): errors.append(f'duplicate {label} id: {x}')
    return errors
def main():
    ap=argparse.ArgumentParser();ap.add_argument('document');a=ap.parse_args();p=Path(a.document);e=validate(p.read_text(encoding='utf-8-sig'))
    if e:
        print('INVALID:',p);[print('-',x) for x in e];raise SystemExit(1)
    print(f'VALID: {p} ({len(FEATURE_RE.findall(p.read_text(encoding="utf-8-sig")))} features)')
if __name__=='__main__':main()
