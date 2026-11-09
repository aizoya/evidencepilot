import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from score_reviewer import score
REF={'dataset_id':'synthetic-test','split':'development_only','cases':[{'id':'a','expected_status':'supported'},{'id':'b','expected_status':'not_established'}]}
class ScoringTests(unittest.TestCase):
    def test_wrong_approval_and_false_rejection(self):
        result=score(REF,{'execution_class':'simulation','predictions':[{'id':'a','status':'contradicted'},{'id':'b','status':'supported'}]})
        self.assertEqual(result['false_support_count'],1)
        self.assertEqual(result['missed_support_count'],1)
        self.assertEqual(result['accuracy_on_answered'],0)
        self.assertIsNone(result['actual_billed_cost'])
    def test_missing_not_counted_as_correct_abstention(self):
        result=score(REF,{'execution_class':'simulation','predictions':[]})
        self.assertIsNone(result['accuracy_on_answered'])
        self.assertEqual(result['missing_ids'],['a','b'])
        self.assertIsNone(result['supported_claim_precision'])
    def test_unknown_or_duplicate_ids_rejected(self):
        for rows in [[{'id':'x','status':'supported'}],[{'id':'a','status':'supported'}]*2]:
            with self.assertRaises(ValueError):score(REF,{'predictions':rows})
