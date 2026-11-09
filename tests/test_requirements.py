"""Development checks only. Human coverage/semantic accuracy remain unmeasured."""
import tempfile
import unittest
from evidencepilot.core import requirements_from, requirement_outcomes, validate_claims, research, Budget
from test_core import FakeProvider, PASSAGE

class RequirementTests(unittest.TestCase):
    def test_ids_are_backend_assigned_and_bounded(self):
        rs=requirements_from({'requirements':[{'id':'attacker','text':'Check price'}]*9})
        self.assertEqual([r['id'] for r in rs],['R1','R2','R3','R4','R5'])
    def test_malformed_plan_falls_back_without_inventing_subrequirements(self):
        rs=requirements_from({'requirements':{'text':'not a list'}})
        self.assertEqual(rs[0]['origin'],'whole_question_fallback')
    def test_unregistered_ids_cannot_claim_coverage(self):
        rs=requirements_from({'requirements':['Check price']})
        cs=validate_claims({'claims':[{'text':'Price finding','requirement_ids':['R1','R99',[], 'R1'],'evidence':[{'source_id':'S1','quote':PASSAGE}]}]},[{'id':'S1','content':PASSAGE}],rs)
        self.assertEqual(cs[0]['requirement_ids'],['R1'])
    def test_missing_mapping_remains_unknown(self):
        rs=requirements_from({'requirements':['Check price','Check region']})
        result=requirement_outcomes(rs,[{'id':'C1','status':'supported','requirement_ids':['R1']}])
        self.assertEqual(result[0]['state'],'supported_findings')
        self.assertEqual(result[1]['state'],'not_established')
    def test_partial_and_conflicting_findings_remain_visible(self):
        rs=requirements_from({'requirements':['Check price']})
        cs=[{'id':'C1','status':'supported','requirement_ids':['R1']},{'id':'C2','status':'uncertain','requirement_ids':['R1']}]
        self.assertEqual(requirement_outcomes(rs,cs)[0]['state'],'partial_findings')
        cs[1]['status']='contradicted'
        self.assertEqual(requirement_outcomes(rs,cs)[0]['state'],'conflicting_findings')
    def test_empty_and_failed_runs_preserve_unknown_requirements(self):
        for mode in ['empty','review_error']:
            with tempfile.TemporaryDirectory() as d:
                result=research('What are the synthetic plan limits?',FakeProvider(mode),Budget(d+'/q.db'))
            self.assertEqual(result['requirement_outcomes'][0]['state'],'not_established')
            self.assertIn('not verified',result['coverage_note'])
