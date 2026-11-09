"""Development-only date/scope regressions; all reviews are simulated."""
import tempfile
import unittest
from evidencepilot.core import Budget, apply_review, research, validate_claims
from test_core import FakeProvider

EVENT = 'October 28–November 20, 2026. Kickoff and virtual build.'


class SubmissionScopeTests(unittest.TestCase):
    def review(self, text, quote=EVENT, content=None):
        sources = [{'id': 'S1', 'content': content or quote,
                    'content_type': 'extracted_page'}]
        claims = validate_claims({'claims': [{'text': text, 'evidence': [
            {'source_id': 'S1', 'quote': quote}]}]}, sources)
        apply_review(claims, {'reviews': [{'claim_id': 'C1', 'status': 'supported',
                     'reason': 'The date range matches.'}]}, sources)
        return claims[0]

    def test_event_dates_cannot_establish_submission_period(self):
        claim = self.review('The submission period runs from October 28 to November 20, 2026.')
        self.assertEqual(claim['status'], 'uncertain')
        self.assertIn('submission', claim['reason'])

    def test_event_end_cannot_establish_submission_deadline(self):
        self.assertEqual(self.review('The submission deadline is November 20, 2026.')['status'], 'uncertain')

    def test_unquoted_submission_text_cannot_rescue_wrong_passage(self):
        content = EVENT + '\nSubmit questions to the support team at any time.'
        self.assertEqual(self.review('Submissions close on November 20, 2026.', content=content)['status'], 'uncertain')

    def test_explicit_submission_passage_can_still_be_supported(self):
        quote = 'Submissions close on November 19, 2026 at noon Pacific Time.'
        self.assertEqual(self.review('The submission deadline is November 19, 2026 at noon Pacific Time.', quote)['status'], 'supported')

    def test_event_window_claim_is_not_a_submission_claim(self):
        self.assertEqual(self.review('The event runs October 28–November 20, 2026.')['status'], 'supported')

    def test_mixed_valid_and_scope_error_report_remains_partial(self):
        class DateProvider(FakeProvider):
            def search(self, query):
                self.calls.append('search')
                return [{'url': 'https://example.com/event', 'title': 'Event', 'raw_content': EVENT}]

            def model_json(self, purpose, instruction, data):
                result = super().model_json(purpose, instruction, data)
                if purpose == 'synthesis':
                    result['claims'] = [
                        {'text': value, 'requirement_ids': ['R1'], 'evidence': [
                            {'source_id': 'S1', 'quote': EVENT}]}
                        for value in ('The event runs October 28–November 20, 2026.',
                                      'The submission period runs October 28–November 20, 2026.')]
                if purpose == 'evidence_review':
                    result['reviews'] = [{'claim_id': cid, 'status': 'supported',
                                          'reason': 'The date range matches.'} for cid in ('C1', 'C2')]
                return result
        provider = DateProvider()
        with tempfile.TemporaryDirectory() as directory:
            report = research('What are the plan limits?', provider, Budget(directory + '/quota.db'))
        self.assertEqual(report['status'], 'partial')
        self.assertEqual([c['status'] for c in report['claims']], ['supported', 'uncertain'])
        self.assertEqual(provider.calls.count('search'), 3)
        self.assertEqual(provider.calls.count('evidence_review'), 1)
