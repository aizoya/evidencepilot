"""Synthetic HTTP transport failures; no real keys or external effects."""
import tempfile
import unittest
from http.client import IncompleteRead,RemoteDisconnected
from unittest.mock import MagicMock,patch
from evidencepilot.core import post_json,Providers,research,Budget,ResearchError
from test_core import FakeProvider

class InterruptedSearch(FakeProvider):
    tavily='synthetic-key-not-valid'
    def search(self,query):return Providers.search(self,query)
class InterruptedReview(FakeProvider):
    nebius='synthetic-key-not-valid'
    def model_json(self,purpose,instruction,data):
        if purpose=='evidence_review':return Providers.model_json(self,purpose,instruction,data)
        return super().model_json(purpose,instruction,data)

class TransportInterruptionTests(unittest.TestCase):
    def broken_opener(self,error):
        opener=MagicMock();opener.open.return_value.__enter__.return_value.read.side_effect=error
        return opener
    def test_interrupted_reads_are_redacted_and_not_retried(self):
        for error in [IncompleteRead(b'synthetic-private-partial',5),RemoteDisconnected('synthetic-private-partial'),ConnectionResetError('synthetic-private-partial')]:
            opener=self.broken_opener(error)
            with self.subTest(error=type(error).__name__),patch('evidencepilot.core.build_opener',return_value=opener):
                with self.assertRaises(ResearchError) as caught:post_json('https://api.tavily.com/search','synthetic-key',{'query':'synthetic'})
                self.assertNotIn('synthetic-private',str(caught.exception))
                self.assertEqual(opener.open.call_count,1)
    def test_interrupted_search_returns_no_fabricated_claims(self):
        opener=self.broken_opener(IncompleteRead(b'synthetic-private-partial',5))
        with tempfile.TemporaryDirectory() as d,patch('evidencepilot.core.build_opener',return_value=opener):
            b=Budget(d+'/q.db',1)
            r=research('What are the synthetic plan limits?',InterruptedSearch(),b)
            with self.assertRaises(ResearchError):b.reserve()
        self.assertEqual(r['status'],'insufficient_evidence')
        self.assertEqual(r['claims'],[])
        self.assertEqual(opener.open.call_count,3) # three bounded planned queries; zero per-call retries
        self.assertEqual(len([e for e in r['execution_events'] if e['actual_tool_result']=='failed']),3)
    def test_interrupted_review_cannot_promote_draft(self):
        opener=self.broken_opener(IncompleteRead(b'synthetic-private-partial',5))
        with tempfile.TemporaryDirectory() as d,patch('evidencepilot.core.build_opener',return_value=opener):
            r=research('What are the synthetic plan limits?',InterruptedReview(),Budget(d+'/q.db'))
        self.assertEqual(r['status'],'failed')
        self.assertFalse(any(c['status']=='supported' for c in r['claims']))
        self.assertEqual(opener.open.call_count,1)
        self.assertEqual(r['execution_events'][-1]['final_outcome'],'failed')
    def test_unrelated_programming_errors_not_hidden(self):
        opener=self.broken_opener(AssertionError('programmer defect'))
        with patch('evidencepilot.core.build_opener',return_value=opener):
            with self.assertRaises(AssertionError):post_json('https://api.tavily.com/search','synthetic-key',{})
