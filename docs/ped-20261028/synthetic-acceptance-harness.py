"""Synthetic acceptance harness outside application edit scope; zero real API calls."""
import json,sys,tempfile,time
from pathlib import Path
from unittest.mock import patch
root=Path(sys.argv[1]).resolve();sys.path[:0]=[str(root),str(root/'tests')]
from test_core import FakeProvider
from evidencepilot.core import Budget,research
class Mapped(FakeProvider):
    def model_json(self,purpose,instruction,data):
        result=super().model_json(purpose,instruction,data)
        if purpose=='plan':result['requirements']=['Check the monthly allowance']
        if purpose=='synthesis':result['claims'][0]['requirement_ids']=['R1']
        return result
class Unmapped(FakeProvider):
    def model_json(self,purpose,instruction,data):
        result=super().model_json(purpose,instruction,data)
        if purpose=='synthesis':result['claims'][0].pop('requirement_ids',None)
        return result
cases={'mapped_success':Mapped,'unmapped_success':Unmapped,'safe_search_failure':lambda:FakeProvider('search_error'),'review_failure':lambda:FakeProvider('review_error')}
records=[]
for name,factory in cases.items():
    for repetition in range(3):
        start=time.monotonic();p=factory()
        with tempfile.TemporaryDirectory() as d,patch('evidencepilot.core.post_json',side_effect=AssertionError('Real provider transport prohibited in synthetic test')):
            r=research('What are the synthetic plan limits?',p,Budget(d+'/quota.db'))
        lookup={s['id']:s for s in r['sources']}
        quotes_ok=all(e['source_id'] in lookup and e['quote'] in lookup[e['source_id']]['content'] for c in r['claims'] for e in c['evidence'])
        records.append({'case':name,'repetition':repetition+1,'execution_class':'simulation','provider_calls_real':0,'fixture_steps':p.calls,'report_status':r['status'],'requirements':r['requirement_outcomes'],'unmapped_claim_ids':r['unmapped_claim_ids'],'internal_quote_links_valid':quotes_ok,'simulated_elapsed_seconds':round(time.monotonic()-start,6),'actual_billed_cost':None,'live_latency':None,'report':r})
Path(sys.argv[2]).write_text(json.dumps(records,indent=2))
print(json.dumps([{k:r[k] for k in ['case','repetition','report_status','internal_quote_links_valid']} for r in records]))
