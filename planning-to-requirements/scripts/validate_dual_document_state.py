#!/usr/bin/env python3
"""Validate feature IDs and confirmation states across paired PCTR documents."""
from __future__ import annotations
import argparse,re
from pathlib import Path
F=re.compile(r'^##\s+([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+-\d{3})\s+(.+)$',re.M)
def map_sections(text):
 ms=list(F.finditer(text));d={}
 for i,m in enumerate(ms): d[m.group(1)]=text[m.start():(ms[i+1].start() if i+1<len(ms) else len(text))]
 return d
def status(s,kind):
 if kind=='req':
  m=re.search(r'planning_confirmation_status:\s*(\S+)',s);return m.group(1) if m else 'unknown'
 m=re.search(r'-\s*确认状态：\s*(待确认|部分确认|已确认|退回修改|pending|partial|confirmed|rejected)',s,re.I);return m.group(1) if m else 'unknown'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('requirements');ap.add_argument('confirmation');a=ap.parse_args();r=map_sections(Path(a.requirements).read_text(encoding='utf-8-sig'));c=map_sections(Path(a.confirmation).read_text(encoding='utf-8-sig'));e=[]
 for x in sorted(set(r)-set(c)):e.append(f'missing confirmation feature: {x}')
 for x in sorted(set(c)-set(r)):e.append(f'missing requirement feature: {x}')
 for x in sorted(set(r)&set(c)):
  rs=status(r[x],'req');cs=status(c[x],'conf'); confirmed=cs in ('已确认','confirmed')
  if confirmed and rs!='confirmed':e.append(f'{x}: planner confirmed but requirement not synchronized')
  if not confirmed and rs=='confirmed':e.append(f'{x}: requirement confirmed but planner document is not')
 if e:
  print('INVALID');[print('-',x) for x in e];raise SystemExit(1)
 print(f'VALID: paired features={len(set(r)&set(c))}')
if __name__=='__main__':main()
