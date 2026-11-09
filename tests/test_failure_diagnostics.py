"""Development-only failure classification; no raw rejected payload retention."""
import json
import unittest
from unittest.mock import patch
from evidencepilot.core import Providers, ResearchError, validate_claims, apply_review
from test_core import PASSAGE
import test_linked_extract
from test_linked_extract import ExtractProvider, URL


class FailureDiagnosticsTests(unittest.TestCase):
    def test_extract_failure_categories_keep_raw_payload_private(self):
        cases = [
            ({'results': [], 'failed_results': [{'error': 'private-canary'}]}, 'extract_url_failed'),
            ({'results': [], 'failed_results': []}, 'extract_empty_results'),
            ({'results': 'private-canary'}, 'extract_invalid_structure'),
            ({'results': [{'url': URL, 'raw_content': ' '}]}, 'extract_empty_content'),
            ({'results': [{'url': 'https://other.example.com/private-canary', 'raw_content': PASSAGE}]}, 'extract_url_mismatch'),
        ]
        for payload, code in cases:
            with self.subTest(code=code), patch('evidencepilot.core.post_json', return_value=payload):
                with self.assertRaises(ResearchError) as caught:
                    Providers().extract(URL)
                self.assertEqual(getattr(caught.exception, 'code', None), code)
                self.assertNotIn('private-canary', str(caught.exception))

    def test_rejected_citation_counts_do_not_retain_input_or_promote_claim(self):
        sources = [{'id': 'S1', 'content': PASSAGE, 'content_type': 'extracted_page'}]
        cases = [
            ([{'source_id': 'private-canary', 'quote': PASSAGE}], 'unknown_source'),
            ([{'source_id': 'S1', 'quote': 'Invented private-canary quotation.'}], 'quote_not_in_source'),
            ([{'source_id': 'S1', 'quote': 123}], 'invalid_quote'),
            ([{'source_id': 'S1', 'quote': 'short'}], 'short_quote'),
            ([], 'no_evidence'),
            ('private-canary', 'invalid_evidence_list'),
        ]
        for evidence, code in cases:
            with self.subTest(code=code):
                claims = validate_claims({'claims': [{'text': 'A bounded factual claim.', 'evidence': evidence}]}, sources)
                apply_review(claims, {'reviews': [{'claim_id': 'C1', 'status': 'supported', 'reason': 'Model approval'}]}, sources)
                self.assertEqual(claims[0]['status'], 'unsupported')
                self.assertEqual(claims[0].get('evidence_rejections'), {code: 1})
                self.assertNotIn('private-canary', json.dumps(claims))

    def test_valid_exact_evidence_still_supported(self):
        sources = [{'id': 'S1', 'content': PASSAGE, 'content_type': 'extracted_page'}]
        claims = validate_claims({'claims': [{'text': 'The service offers a free plan.',
                 'evidence': [{'source_id': 'S1', 'quote': PASSAGE}]}]}, sources)
        apply_review(claims, {'reviews': [{'claim_id': 'C1', 'status': 'supported', 'reason': 'Explicit passage'}]}, sources)
        self.assertEqual(claims[0]['status'], 'supported')
        self.assertEqual(claims[0].get('evidence_rejections'), {})

    def test_classification_reaches_trace_without_retry_or_payload(self):
        class ClassifiedProvider(ExtractProvider):
            tavily = 'synthetic-not-valid'
            def extract(self, url):
                self.calls.append('extract')
                return Providers.extract(self, url)
        provider = ClassifiedProvider()
        with patch('evidencepilot.core.post_json', return_value={
                'results': [], 'failed_results': [{'error': 'private-canary'}]}) as post:
            report = test_linked_extract.LinkedExtractTests().run_case(provider)
        failed = [e for e in report['execution_events'] if e['actual_tool_result'] == 'failed']
        self.assertEqual(len(failed), 1)
        self.assertEqual(failed[0].get('failure_code'), 'extract_url_failed')
        self.assertNotIn('private-canary', json.dumps(report))
        self.assertEqual(post.call_count, 1)
        self.assertEqual(provider.calls.count('search'), 2)
        self.assertEqual(provider.calls.count('extract'), 1)
        self.assertNotEqual(report['status'], 'evidence_found')
