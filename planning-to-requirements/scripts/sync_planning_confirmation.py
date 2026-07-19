#!/usr/bin/env python3
"""Synchronize one confirmed planner feature into a requirement Markdown document."""
from __future__ import annotations
import argparse,re
from pathlib import Path
FEATURE=lambda fid: re.compile(rf'^##\s+{re.escape(fid)}\s+.+$',re.M)
def bounds(text,fid):
 m=FEATURE(fid).search(text)
 if not m: raise ValueError(f'feature not found: {fid}')
 nxt=re.search(r'^##\s+[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+-\d{3}\s+',text[m.end():],re.M)
 return m.start(), (m.end()+nxt.start() if nxt else len(text))
def extract_confirmation(conf,fid):
 a,b=bounds(conf,fid); body=conf[a:b]
 if not re.search(r'-\s*确认状态：\s*(已确认|confirmed)',body,re.I): raise ValueError('feature is not confirmed')
 if re.search(r'是否阻塞开发：\s*是[\s\S]*?状态：\s*待确认',body): raise ValueError('pending blocking item remains')
 m=re.search(r'-\s*最终确认内容：\s*(.+)',body)
 if not m or not m.group(1).strip(): raise ValueError('final confirmation summary is empty')
 rev=re.search(r'-\s*确认文档 Revision：\s*(.+)',body); who=re.search(r'-\s*确认人：\s*(.+)',body); when=re.search(r'-\s*确认时间：\s*(.+)',body)
 return {'summary':m.group(1).strip(),'revision':rev.group(1).strip() if rev else '', 'who':who.group(1).strip() if who else '', 'when':when.group(1).strip() if when else ''}
def sync(req,conf,fid):
 info=extract_confirmation(conf,fid); a,b=bounds(req,fid); body=req[a:b]
 body=re.sub(r'planning_confirmation_status:\s*\S+','planning_confirmation_status: confirmed',body)
 replacement=f'''### 12. 策划确认同步\n\n- 策划确认状态：已确认\n- 最终确认摘要：{info['summary']}\n- 确认人：{info['who']}\n- 确认时间：{info['when']}\n- 确认 Revision：{info['revision']}\n- 技术方案状态：待生成\n'''
 pat=re.compile(r'^###\s+12\.\s*策划确认同步[\s\S]*?(?=^###\s+|\Z)',re.M)
 if pat.search(body): body=pat.sub(replacement+'\n',body)
 else: body=body.rstrip()+'\n\n'+replacement+'\n'
 return req[:a]+body+req[b:]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('requirements');ap.add_argument('confirmation');ap.add_argument('--feature',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();req=Path(a.requirements).read_text(encoding='utf-8-sig');conf=Path(a.confirmation).read_text(encoding='utf-8-sig');Path(a.out).write_text(sync(req,conf,a.feature),encoding='utf-8');print('synchronized',a.feature,'->',a.out)
if __name__=='__main__':main()
