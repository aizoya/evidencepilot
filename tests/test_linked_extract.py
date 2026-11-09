"""Development fixtures only. No live provider, billing or page-access claims."""
import tempfile
import unittest
from unittest.mock import patch
from evidencepilot.core import Budget, Providers, ResearchError, research
from test_core import FakeProvider, PASSAGE

URL = 'https://rules.example.com/event?edition=2026'


class ExtractProvider(FakeProvider):
    def __init__(self, fail=False):
        super().__init__()
        self.fail = fail
        self.targets = []

    def search(self, query):
        self.calls.append('search')
        return [{'url': 'https://listing.example.com/event', 'raw_content':
                 'Event listing: [Main website](' + URL + ')'}]

    def extract(self, url):
        self.calls.append('extract')
        self.targets.append(url)
        if self.fail:
            raise ResearchError('Synthetic extract failure.')
        return [{'url': url, 'raw_content': PASSAGE}]

    def model_json(self, purpose, instruction, data):
        result = super().model_json(purpose, instruction, data)
        if purpose == 'synthesis':
            result['claims'][0]['evidence'][0]['source_id'] = 'S2'
        return result


class LinkedExtractTests(unittest.TestCase):
    def run_case(self, provider):
        with tempfile.TemporaryDirectory() as directory, patch(
                'socket.socket.connect', side_effect=AssertionError('Network forbidden')):
            return research('What are the synthetic plan limits?', provider, Budget(directory + '/quota.db'))

    def test_extract_replaces_final_search_and_preserves_url_identity(self):
        provider = ExtractProvider()
        report = self.run_case(provider)
        self.assertEqual(provider.calls.count('search'), 2)
        self.assertEqual(provider.calls.count('extract'), 1)
        self.assertEqual(provider.targets, [URL])
        self.assertEqual(report['sources'][1]['url'], URL)
        self.assertEqual(report['claims'][0]['status'], 'supported')
        self.assertTrue(any(e['proposed_action'] == 'extract' and e['actual_tool_result'] == 'returned'
                            for e in report['execution_events']))
        self.assertEqual(report['limits']['tavily_calls'], 3)

    def test_failed_extract_is_visible_without_retry_or_fourth_call(self):
        provider = ExtractProvider(fail=True)
        report = self.run_case(provider)
        self.assertEqual(provider.calls.count('search'), 2)
        self.assertEqual(provider.calls.count('extract'), 1)
        self.assertNotEqual(report['status'], 'evidence_found')
        self.assertFalse(any(c['status'] == 'supported' for c in report['claims']))
        self.assertTrue(any(e['proposed_action'] == 'extract' and e['actual_tool_result'] == 'failed'
                            for e in report['execution_events']))

    def test_adapter_uses_basic_single_url_and_records_returned_usage(self):
        provider = Providers()
        provider.tavily = 'synthetic-not-valid'
        with patch('evidencepilot.core.post_json', return_value={
                'results': [{'url': URL, 'raw_content': PASSAGE}],
                'failed_results': [], 'usage': {'credits': 1}}) as post:
            rows = provider.extract(URL)
        self.assertEqual(post.call_count, 1)
        endpoint, key, body = post.call_args.args
        self.assertEqual(endpoint, 'https://api.tavily.com/extract')
        self.assertEqual(body['urls'], [URL])
        self.assertEqual(body['extract_depth'], 'basic')
        self.assertTrue(body['include_usage'])
        self.assertEqual(rows[0]['raw_content'], PASSAGE)
        self.assertEqual(provider.usage[-1]['reserved_credits'], 1)
        self.assertEqual(provider.usage[-1]['credits'], 1)

    def test_http_200_failure_and_empty_content_are_not_success(self):
        for payload in ({'results': [], 'failed_results': [{'url': URL, 'error': 'private-canary'}]},
                        {'results': [{'url': URL, 'raw_content': '  '}], 'failed_results': []},
                        {'results': 'not-a-list', 'failed_results': []}):
            with self.subTest(payload=payload):
                with patch('evidencepilot.core.post_json', return_value=payload) as post:
                    with self.assertRaises(ResearchError) as caught:
                        Providers().extract(URL)
                self.assertEqual(post.call_count, 1)
                self.assertNotIn('private-canary', str(caught.exception))

    def test_unrequested_response_url_is_rejected(self):
        with patch('evidencepilot.core.post_json', return_value={
                'results': [{'url': 'https://other.example.com/', 'raw_content': PASSAGE}],
                'failed_results': []}):
            with self.assertRaises(ResearchError):
                Providers().extract(URL)

    def test_unsafe_target_makes_no_provider_request(self):
        with patch('evidencepilot.core.post_json') as post:
            for url in ('https://127.0.0.1/', 'http://rules.example.com/',
                        'https://user:secret@rules.example.com/'):
                with self.assertRaises(ResearchError):
                    Providers().extract(url)
        post.assert_not_called()

    def test_transport_failure_reserves_attempt_and_has_no_retry(self):
        provider = Providers()
        with patch('evidencepilot.core.post_json', side_effect=ResearchError('Synthetic timeout')) as post:
            with self.assertRaises(ResearchError):
                provider.extract(URL)
        self.assertEqual(post.call_count, 1)
        self.assertEqual(provider.usage[-1]['reserved_credits'], 1)
        self.assertIsNone(provider.usage[-1]['credits'])
