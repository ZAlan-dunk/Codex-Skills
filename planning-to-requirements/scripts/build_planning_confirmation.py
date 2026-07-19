#!/usr/bin/env python3
"""Build a planner-facing confirmation/acceptance Markdown document from PCTR requirements."""
from __future__ import annotations
import argparse,re
from pathlib import Path

FEATURE_RE=re.compile(r'^##\s+([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+-\d{3})\s+(.+)$',re.M)

def section_text(body:str,label_pattern:str)->str:
    m=re.search(rf'^###\s+[^\n]*(?:{label_pattern})[^\n]*\n(.*?)(?=^###\s+|^---\s*$|\Z)',body,re.M|re.S)
    return m.group(1).strip() if m else ''

def clean_summary(text:str)->str:
    lines=[]
    for line in text.splitlines():
        s=line.strip()
        if not s or s.startswith('|') or s.startswith('```'): continue
        s=re.sub(r'^[-*]\s*','',s); s=re.sub(r'^\d+\.\s*','',s)
        if s: lines.append(s)
    return ' '.join(lines[:3]) or '待从需求开发文档补充功能简述。'

def extract_items(text:str)->list[str]:
    result=[]
    for line in text.splitlines():
        s=line.strip()
        if re.match(r'^- \[[ xX]\]',s): result.append(re.sub(r'^- \[[ xX]\]\s*','',s).strip())
        elif re.match(r'^[-*]\s+',s): result.append(re.sub(r'^[-*]\s+','',s).strip())
    if not result and text: result=[clean_summary(text)]
    return result

def build(req:str,title:str)->str:
    matches=list(FEATURE_RE.finditer(req)); out=[f'# {title}','', '## 文档状态','', '| 字段 | 内容 |','|---|---|','| 来源需求文档 | 待填写链接/文档ID |','| 需求文档 Revision | 待填写 |','| 本文档 Revision | 待填写 |','| 最后同步时间 | 待填写 |','', '> 本文档是策划确认和策划验收的权威来源。填写内容不会自动解锁开发，必须再执行明确的同步/确认指令。','', '## 功能确认与验收总表','', '| 功能 ID | 功能名称 | 简单实现说明 | 阻塞确认项 | 确认状态 | 开发状态 | 验收状态 |','|---|---|---|---:|---|---|---|']
    sections=[]
    for idx,m in enumerate(matches):
        end=matches[idx+1].start() if idx+1<len(matches) else len(req); body=req[m.end():end]; fid,title0=m.group(1),m.group(2).strip()
        goal=section_text(body,'需求目标|目标'); questions=section_text(body,'待确认'); acceptance=section_text(body,'验收标准')
        qitems=extract_items(questions) or ['当前没有自动提取到策划确认项；请人工复核是否确实无歧义。']
        aitems=extract_items(acceptance) or ['功能主流程与已确认需求一致。']
        short=clean_summary(goal)
        out.append(f'| `{fid}` | {title0} | {short} | {len(qitems)} | 待确认 | 未开始 | 未进入 |')
        sec=['', '---','',f'## {fid} {title0}','', '### 1. 功能简述','',short,'','### 2. 当前实现范围','', clean_summary(section_text(body,'功能范围|范围')),'','### 3. 需要策划确认','']
        for n,q in enumerate(qitems,1):
            cid=f'PC-{fid}-{n:02d}'; sec += [f'#### {cid} 确认项 {n}','',f'- 原始问题：{q}','- 当前歧义或缺失：待策划填写','- 对实现/验收的影响：待评估','- 可选方案或建议：Agent 不得静默选择','- 是否阻塞开发：是','- 策划答复：','- 状态：待确认','- 确认人：','- 确认时间：','']
        sec += ['### 4. 策划最终确认摘要','','- 最终确认内容：','- 确认状态：待确认','- 确认人：','- 确认时间：','- 确认文档 Revision：','','### 5. 策划验收点','']
        for n,a in enumerate(aitems,1): sec.append(f'- [ ] PA-{fid}-{n:02d} {a}')
        sec += ['','### 6. 策划验收记录','','#### 验收轮次 1','','- 提交版本/Commit：','- 提交时间：','- 验收状态：未进入','- 失败验收点：','- Bug 描述：','- 策划说明：','- 最终验收人：','- 最终验收时间：','']
        sections.extend(sec)
    return '\n'.join(out+sections).rstrip()+'\n'

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('requirements'); ap.add_argument('--out',required=True); ap.add_argument('--title',default='策划需求确认与验收文档'); a=ap.parse_args()
    req=Path(a.requirements).read_text(encoding='utf-8-sig'); result=build(req,a.title); Path(a.out).write_text(result,encoding='utf-8'); print(f'created {a.out}; features={len(FEATURE_RE.findall(req))}')
if __name__=='__main__': main()
