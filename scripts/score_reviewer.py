"""Offline scorer: no provider calls; developer-visible labels only."""
import json
import sys
from pathlib import Path
LABELS={'supported','contradicted','not_established'}
def score(reference,prediction):
    cases={c['id']:c for c in reference['cases']}
    rows=prediction.get('predictions')
    if not isinstance(rows,list): raise ValueError('Missing prediction list')
    indexed={}
    for row in rows:
        if not isinstance(row,dict) or row.get('id') not in cases or row.get('status') not in LABELS: raise ValueError('Invalid ID/status')
        if row['id'] in indexed: raise ValueError('Duplicate ID')
        indexed[row['id']]=row['status']
    decisions=[{'id':cid,'expected':c['expected_status'],'predicted':indexed.get(cid)} for cid,c in cases.items()]
    answered=[r for r in decisions if r['predicted'] is not None]
    supports=[r for r in answered if r['predicted']=='supported']
    abstentions=[r for r in decisions if r['expected']=='not_established']
    correct=sum(r['expected']==r['predicted'] for r in answered)
    return {'dataset_id':reference['dataset_id'],'split':reference['split'],
            'execution_class':prediction.get('execution_class','unspecified'),
            'provenance':'Caller-supplied execution class; not independently verified by scorer.',
            'reference_cases':len(cases),'answered':len(answered),
            'missing_ids':[r['id'] for r in decisions if r['predicted'] is None],
            'accuracy_on_answered':correct/len(answered) if answered else None,
            'all_case_correct_fraction':correct/len(cases) if cases else None,
            'supported_claim_precision':sum(r['expected']=='supported' for r in supports)/len(supports) if supports else None,
            'false_support_count':sum(r['predicted']=='supported' and r['expected']!='supported' for r in answered),
            'missed_support_count':sum(r['expected']=='supported' and r['predicted']!='supported' for r in answered),
            'appropriate_abstention_fraction':sum(r['predicted']=='not_established' for r in abstentions)/len(abstentions) if abstentions else None,
            'serious_violations_missed':None,'false_action_alarms':None,'recoverability':None,
            'actual_billed_cost':None,'live_latency':None,'decisions':decisions,
            'limits':'Claim-label development calibration only. No action-safety ground truth; no broad reliability claims.'}
if __name__=='__main__':
    if len(sys.argv)!=3:sys.exit('Usage: python3 scripts/score_reviewer.py REFERENCE_JSON PREDICTIONS_JSON')
    print(json.dumps(score(json.loads(Path(sys.argv[1]).read_text()),json.loads(Path(sys.argv[2]).read_text())),indent=2))
