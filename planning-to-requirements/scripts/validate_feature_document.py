#!/usr/bin/env python3
"""Validate the enhanced PCTR requirement development document."""
from __future__ import annotations
import argparse,re
from pathlib import Path
FEATURE_RE=re.compile(r'^##\s+([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+-\d{3})\s+(.+)$',re.M)
REQUIRED=('功能定位','来源追溯','需求目标','功能范围','非功能范围','ACSDM','待确认','策划确认','技术方案','策划验收','可复制 Agent 任务')
def validate(text):
 e=[];ms=list(FEATURE_RE.finditer(text));seen=set()
 if not ms:return ['no atomic feature headings found']
 for i,m in enumerate(ms):
  fid=m.group(1);body=text[m.end():(ms[i+1].start() if i+1<len(ms) else len(text))]
  if fid in seen:e.append(f'duplicate feature id: {fid}')
  seen.add(fid)
  for x in REQUIRED:
   if x not in body:e.append(f'{fid}: missing section containing {x}')
  if not re.search(r'```text\s+[\s\S]+?```',body):e.append(f'{fid}: missing task capsule')
  if '策划确认门禁' not in body:e.append(f'{fid}: task capsule missing confirmation gate')
  if not re.search(r'planning_confirmation_status:\s*(pending|partial|confirmed|rejected)',body):e.append(f'{fid}: invalid/missing confirmation state')
 return e
def main():
 ap=argparse.ArgumentParser();ap.add_argument('document');a=ap.parse_args();p=Path(a.document);t=p.read_text(encoding='utf-8-sig');e=validate(t)
 if e:print('INVALID:',p);[print('-',x) for x in e];raise SystemExit(1)
 print(f'VALID: {p} ({len(FEATURE_RE.findall(t))} atomic features)')
if __name__=='__main__':main()
