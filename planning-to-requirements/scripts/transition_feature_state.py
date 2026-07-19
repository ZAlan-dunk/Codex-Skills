#!/usr/bin/env python3
"""Apply validated feature-state transitions for PCTR workflows."""
from __future__ import annotations
import argparse,json
from pathlib import Path
EVENTS={
 'planning-partially-confirmed':{'planning_confirmation_status':'partial','final_feature_status':'blocked'},
 'planning-confirmed':{'planning_confirmation_status':'confirmed','technical_plan_status':'not-created','final_feature_status':'in-progress'},
 'plan-created':{'technical_plan_status':'pending-approval'},
 'plan-approved':{'technical_plan_status':'approved'},
 'implementation-started':{'development_status':'implementing','final_feature_status':'in-progress'},
 'submitted-for-planning-acceptance':{'development_status':'submitted-for-planning-acceptance','planning_acceptance_status':'pending'},
 'planning-acceptance-failed':{'development_status':'bug-fixing','planning_acceptance_status':'failed','final_feature_status':'in-progress'},
 're-submitted-for-planning-acceptance':{'development_status':'submitted-for-planning-acceptance','planning_acceptance_status':'pending'},
 'planning-accepted':{'planning_acceptance_status':'accepted'},
 'feature-completed':{'development_status':'completed','planning_acceptance_status':'accepted','final_feature_status':'completed'},
}
def apply(s,event):
 if event not in EVENTS: raise ValueError('unknown event')
 if event in ('plan-created','plan-approved','implementation-started') and s.get('planning_confirmation_status')!='confirmed': raise ValueError('planning confirmation required')
 if event=='implementation-started' and s.get('technical_plan_status')!='approved': raise ValueError('approved plan required')
 if event=='submitted-for-planning-acceptance' and s.get('development_status') not in ('implementing','integrating'): raise ValueError('implementation/integration state required')
 if event=='planning-accepted' and s.get('planning_acceptance_status') not in ('pending','in-review','partial'): raise ValueError('active acceptance round required')
 if event=='feature-completed':
  if s.get('planning_confirmation_status')!='confirmed': raise ValueError('planning confirmation required')
  if s.get('planning_acceptance_status')!='accepted': raise ValueError('planning acceptance required')
  if s.get('open_blocking_bugs',0): raise ValueError('open blocking bugs remain')
 n=dict(s); n.update(EVENTS[event]); return n
def main():
 ap=argparse.ArgumentParser();ap.add_argument('state');ap.add_argument('--event',required=True);ap.add_argument('--out');a=ap.parse_args();s=json.loads(Path(a.state).read_text(encoding='utf-8-sig'));n=apply(s,a.event);out=json.dumps(n,ensure_ascii=False,indent=2)
 if a.out:Path(a.out).write_text(out,encoding='utf-8')
 print(out)
if __name__=='__main__':main()
