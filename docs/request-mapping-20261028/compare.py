"""Development simulation, not live inference or a held-out evaluation."""
import importlib.util,json,sys,tempfile
from pathlib import Path
from unittest.mock import patch
root=Path('/workspace/scratch/facb523d7379/ped_recovery/source/evidencepilot');sys.path[:0]=[str(root),str(root/'tests')]
from test_core import FakeProvider
import evidencepilot.core as current
spec=importlib.util.spec_from_file_location('mapping_baseline',str(Path(__file__).parent/'core-before.py'));baseline=importlib.util.module_from_spec(spec);spec.loader.exec_module(baseline)
class Fixture(FakeProvider):
 def __init__(self,mode):super().__init__();self.mode=mode
 def model_json(self,purpose,instruction,data):
  r=super().model_json(purpose,instruction,data)
  if purpose=='plan':
   records=[{'quote':'plan limits'}] if self.mode=='valid' else []
   r['requirements']=[{'text':'Check plan limits','user_spans':records}]
   if self.mode=='invalid':r['requirements'][0]['user_spans']=[{'quote':'invented'}]
   if self.mode=='overflow':r['requirements']=[{'text':'Check plan limits','user_spans':[{'quote':'plan limits'}]}]*6
  return r
results=[]
for name in ['valid','missing','invalid','overflow']:
 for repetition in range(3):
  row={'case':name,'repetition':repetition+1,'execution_class':'simulation','live_latency':None,'actual_billed_cost':None}
  for version,module in [('before',baseline),('after',current)]:
   with tempfile.TemporaryDirectory() as d,patch('socket.socket.connect',side_effect=AssertionError('Network blocked')):
    report=module.research('What are the synthetic plan limits?',Fixture(name),module.Budget(d+'/q.db'))
   row[version]={'status':report['status'],'link_statuses':[r.get('text_link_status') for r in report['requirements']],'warnings':report['warnings']}
  results.append(row)
Path(__file__).with_name('comparison-results.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results))
