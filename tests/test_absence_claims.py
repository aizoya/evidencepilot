"""Development regressions from the first live run; never a held-out benchmark.

All providers are fixtures. A matching excerpt and a positive model review do
not establish that information is absent from the governing documentation.
"""
import tempfile
import unittest
from evidencepilot.core import Budget, apply_review, research, validate_claims
from test_core import FakeProvider

PASSAGE = 'Final tracks, partner challenges, and prizes will be announced before the event.'


class AbsenceClaimTests(unittest.TestCase):
    def review_claim(self, text, passage=PASSAGE):
        sources = [{'id': 'S1', 'content': passage, 'content_type': 'extracted_page'}]
        claims = validate_claims({'claims': [{'text': text, 'evidence': [
            {'source_id': 'S1', 'quote': passage}]}]}, sources)
        apply_review(claims, {'reviews': [{'claim_id': 'C1', 'status': 'supported',
                     'reason': 'The retrieved page does not mention further requirements.'}]}, sources)
        return claims[0]

    def test_positive_reviewer_cannot_certify_missing_rules(self):
        for text in (
            'The hackathon does not specify detailed submission requirements.',
            'The hackathon does not establish specific technical submission formats.',
            'The hackathon does not establish a submission deadline beyond its end date.',
            'The rules do not mention an age restriction.',
            'No submission requirements are specified.',
            'Eligible participants include developers, with no restrictions mentioned beyond being open to everyone.',
        ):
            with self.subTest(text=text):
                claim = self.review_claim(text)
                self.assertEqual(claim['status'], 'uncertain')
                self.assertIn('absence', claim['reason'])

    def test_directly_documented_positive_finding_still_supported(self):
        self.assertEqual(self.review_claim(
            'Tracks and prizes will be announced before the event.')['status'], 'supported')

    def test_documented_capability_restriction_is_not_documentation_absence(self):
        passage = 'The basic plan does not support custom domains or private deployments.'
        self.assertEqual(self.review_claim(
            'The basic plan does not support custom domains.', passage)['status'], 'supported')

    def test_uncertain_absence_cannot_create_fully_verified_report(self):
        class MissingRulesProvider(FakeProvider):
            def model_json(self, purpose, instruction, data):
                result = super().model_json(purpose, instruction, data)
                if purpose == 'synthesis':
                    result['claims'][0]['text'] = 'The service does not specify additional limits.'
                return result
        provider = MissingRulesProvider()
        with tempfile.TemporaryDirectory() as directory:
            report = research('What are the plan limits?', provider, Budget(directory + '/quota.db'))
        self.assertNotEqual(report['status'], 'evidence_found')
        self.assertEqual(report['claims'][0]['status'], 'uncertain')
        self.assertNotEqual(report['requirement_outcomes'][0]['state'], 'supported_findings')
        self.assertEqual(provider.calls.count('search'), 3)
        self.assertEqual(provider.calls.count('evidence_review'), 1)
