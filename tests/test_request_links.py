"""Development location checks, not semantic interpretation or holdout evaluation."""
import tempfile
import unittest
from evidencepilot.core import request_links,requirements_from,research,Budget
from test_core import FakeProvider
class LinkedProvider(FakeProvider):
    def __init__(self,mode):super().__init__();self.mode=mode;self.questions=[]
    def model_json(self,purpose,instruction,data):
        self.questions.append(data['question'])
        result=super().model_json(purpose,instruction,data)
        if purpose=='plan':
            result['requirements']=[{'text':'Check plan limits','user_spans':[{'quote':'plan limits'}]}]
            if self.mode=='missing':result['requirements'][0]['user_spans']=[]
            if self.mode=='overflow':result['requirements']*=6
        return result
class RequestLinkTests(unittest.TestCase):
    def test_unique_quote_resolves_exact_offsets(self):
        spans,status=request_links([{'quote':'plan limits'}],'Check plan limits please')
        self.assertEqual(status,'matched');self.assertEqual(spans,[{'start':6,'end':17,'quote':'plan limits'}])
    def test_mixed_validity_cannot_be_masked(self):
        for broken in [{},{'quote':'invented'},{'quote':'plan','start':True,'end':5}]:
            spans,status=request_links([{'quote':'limits'},broken],'Check plan limits please')
            self.assertNotEqual(status,'matched');self.assertEqual(len(spans),1)
    def test_repeated_quote_requires_selected_span(self):
        self.assertEqual(request_links([{'quote':'plan'}],'plan and plan')[1],'ambiguous')
        self.assertEqual(request_links([{'quote':'plan','start':9,'end':13}],'plan and plan')[1],'matched')
    def test_excess_and_out_of_bounds_rejected(self):
        self.assertEqual(request_links([{'quote':'plan'}]*4,'Check plan please')[1],'invalid')
        for start,end in [(-1,5),(0,100),(5,1),(0,False)]:
            self.assertEqual(request_links([{'quote':'plan','start':start,'end':end}],'Check plan please')[1],'invalid')
    def test_unicode_codepoints_preserved(self):
        self.assertEqual(request_links([{'quote':'plan','start':2,'end':6}],'😀 plan please')[1],'matched')
        self.assertEqual(request_links([{'quote':'e\u0301'}],'Check e\u0301 please')[1],'matched')
    def test_full_question_not_reused_as_proposal_provenance(self):
        self.assertEqual(request_links([{'quote':'Check plan'}],'Check plan')[1],'invalid')
    def test_no_human_authority_from_model_fields(self):
        r=requirements_from({'requirements':[{'text':'Check plan','origin':'human_clarified','interpretation_status':'human_confirmed','user_spans':[{'quote':'plan'}]}]},'Check plan please')[0]
        self.assertEqual(r['origin'],'planner_proposal');self.assertEqual(r['interpretation_status'],'not_reviewed')
    def test_canonical_question_and_partial_gates(self):
        for mode,expected in [('linked','evidence_found'),('missing','partial'),('overflow','partial')]:
            p=LinkedProvider(mode)
            with tempfile.TemporaryDirectory() as d:r=research('  What are the plan limits?  ',p,Budget(d+'/q.db'))
            self.assertEqual(r['status'],expected)
            self.assertTrue(all(q==r['question'] for q in p.questions))
            self.assertEqual(r['coverage_assurance'],'not_verified')
            if mode=='overflow':
                self.assertEqual(r['omitted_requirement_count'],1)
                self.assertTrue(any('five' in w and '1 additional' in w for w in r['warnings']))
