"""Regression for misleading overall success. No real providers."""
import tempfile
import unittest
from evidencepilot.core import research,Budget
from test_core import FakeProvider
class CoverageProvider(FakeProvider):
    def __init__(self,mode):super().__init__();self.coverage_mode=mode
    def model_json(self,purpose,instruction,data):
        result=super().model_json(purpose,instruction,data)
        if purpose=='plan':result['requirements']=[{'text':value,'user_spans':[{'quote':'plan limits'}]} for value in (['Check price','Check region'] if self.coverage_mode=='missing_requirement' else ['Check price'])]
        if purpose=='synthesis':
            if self.coverage_mode=='unmapped':result['claims'][0].pop('requirement_ids',None)
            else:result['claims'][0]['requirement_ids']=['R1']
        return result
class CompletenessTests(unittest.TestCase):
    def run_case(self,p):
        with tempfile.TemporaryDirectory() as d:return research('What are the synthetic plan limits?',p,Budget(d+'/q.db'))
    def test_unknown_requirement_prevents_full_success(self):
        r=self.run_case(CoverageProvider('missing_requirement'))
        self.assertEqual(r['status'],'partial')
        self.assertEqual(r['requirement_outcomes'][1]['state'],'not_established')
        self.assertTrue(r['warnings'])
    def test_unmapped_claim_prevents_full_success(self):
        r=self.run_case(CoverageProvider('unmapped'))
        self.assertEqual(r['status'],'partial');self.assertEqual(r['unmapped_claim_ids'],['C1'])
    def test_fully_mapped_fixture_still_succeeds(self):
        self.assertEqual(self.run_case(CoverageProvider('mapped'))['status'],'evidence_found')
    def test_review_failure_not_overwritten(self):
        r=self.run_case(FakeProvider('review_error'))
        self.assertEqual(r['status'],'failed')
        self.assertEqual(r['execution_events'][-1]['final_outcome'],'failed')
