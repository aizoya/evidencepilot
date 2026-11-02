"""Isolated transport experiment: no network, real adapter with simulated HTTP reads."""
import json,sys,tempfile,time
from pathlib import Path
from unittest.mock import patch,MagicMock
from http.client import IncompleteRead
root=Path(sys.argv[1]).resolve();sys.path[:0]=[str(root),str(root/'tests')]
from evidencepilot.core import Providers,research,Budget
from test_core import FakeProvider
class BrokenSearch(FakeProvider):
    def search(self,query):
        self.calls.append('search')
        return Providers.search(self,query)
    tavily='synthetic-canary-not-a-real-key'
class BrokenReview(FakeProvider):
    nebius='synthetic-canary-not-a-real-key'
    def model_json(self,purpose,instruction,data):
        if purpose=='evidence_review':return Providers.model_json(self,purpose,instruction,data)
        return super().model_json(purpose,instruction,data)
results=[]
for label,cls in [('search_interrupted',BrokenSearch),('review_interrupted',BrokenReview),('normal',FakeProvider)]:
 for rep in range(3):
  opener=MagicMock();opener.open.return_value.__enter__.return_value.read.side_effect=IncompleteRead(b'synthetic-sensitive-partial-body',20)
  p=cls();start=time.monotonic()
  with tempfile.TemporaryDirectory() as d,patch('evidencepilot.core.build_opener',return_value=opener),patch('socket.socket.connect',side_effect=AssertionError('Network blocked')):
   budget=Budget(d+'/q.db')
   try:
    r=research('What are the synthetic plan limits?',p,budget)
    result={'outcome':'structured_report','report':r}
   except Exception as exc:
    result={'outcome':'uncaught_exception','exception_type':type(exc).__name__}
  result.update(case=label,repetition=rep+1,execution_class='simulation',simulated_http_attempts=opener.open.call_count,real_provider_calls=0,local_elapsed_seconds=round(time.monotonic()-start,6),live_latency=None,actual_cost=None)
  results.append(result)
Path(sys.argv[2]).write_text(json.dumps(results,indent=2))
print(json.dumps([{k:r[k] for k in ['case','repetition','outcome','simulated_http_attempts']} for r in results]))
