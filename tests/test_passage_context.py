"""Context preservation only; model entailment accuracy is not measured."""
import unittest
from evidencepilot.core import passage_context, validate_claims, apply_review

class PassageContextTests(unittest.TestCase):
    def test_dedicated_scope_and_public_exception(self):
        quote='Choose where your deployment runs.'
        src={'id':'S1','content':'# Dedicated endpoints\n'+quote+'\nPublic serverless routing is not region-fixed.'}
        e=passage_context(src,quote)
        self.assertEqual(e['section_heading'],'# Dedicated endpoints')
        self.assertIn('not region-fixed',e['context'])
        self.assertEqual(src['content'][e['span_start']:e['span_end']],quote)
    def test_negation_and_conditions_retained(self):
        quote='A fixed region is available'
        src={'id':'S1','content':'# Policy\n'+quote+' only for dedicated deployments, not public serverless.'}
        self.assertIn('not public serverless',passage_context(src,quote)['context'])
    def test_table_header_retained(self):
        src={'id':'S1','content':'# Plans\n| Plan | Rate |\n| --- | --- |\n| Growth | $5 per unit |\n'}
        self.assertEqual(passage_context(src,'$5 per unit')['table_header'],['| Plan | Rate |','| --- | --- |'])
    def test_absent_quote_rejected(self):
        with self.assertRaises(ValueError):passage_context({'id':'S1','content':'Original'},'Invented')
    def test_repeated_quote_stays_uncertain(self):
        q='This capability is available.'
        src={'id':'S1','content':'# Old plan\n'+q+'\n# New plan\n'+q}
        cs=validate_claims({'claims':[{'text':'Available on current plan','evidence':[{'source_id':'S1','quote':q}]}]},[src])
        apply_review(cs,{'reviews':[{'claim_id':'C1','status':'supported','reason':'Quoted'}]},[src])
        self.assertEqual(cs[0]['evidence'][0]['match_count'],2)
        self.assertEqual(cs[0]['status'],'uncertain')
    def test_context_bounded_unknown_heading(self):
        src={'id':'S1','content':'a'*2000+'A uniquely worded statement.'+'b'*2000}
        e=passage_context(src,'A uniquely worded statement.')
        self.assertEqual(len(e['context']),1600+len(e['quote']))
        self.assertIsNone(e['section_heading'])
