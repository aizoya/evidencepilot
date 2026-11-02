"""Synthetic development experiment, NOT reconstruction of unknown live C4 output."""
import tempfile
import unittest
from unittest.mock import patch
from evidencepilot.core import Budget, apply_review, research, validate_claims
from test_core import FakeProvider, PASSAGE


class CitationAttachmentTests(unittest.TestCase):
    def assess(self, content, quote, status='supported'):
        sources = [{'id': 'S1', 'content': content, 'content_type': 'extracted_page'}]
        claims = validate_claims({'claims': [{'text': 'The synthetic plan permits five reports.',
                 'evidence': [{'source_id': 'S1', 'quote': quote}]}]}, sources)
        apply_review(claims, {'reviews': [{'claim_id': 'C1', 'status': status,
                     'reason': 'Synthetic reviewer judgment; not observed model behavior.'}]}, sources)
        return claims[0]

    def test_whitespace_only_match_stores_exact_original_passage(self):
        source = '# Limits\nThe synthetic plan\tpermits five\nreports per month.'
        claim = self.assess(source, 'The synthetic plan permits five reports per month.')
        self.assertEqual(claim['status'], 'supported')
        evidence = claim['evidence'][0]
        self.assertEqual(evidence['quote_match'], 'whitespace_only')
        self.assertEqual(evidence['quote'], 'The synthetic plan\tpermits five\nreports per month.')
        self.assertEqual(source[evidence['span_start']:evidence['span_end']], evidence['quote'])
        self.assertEqual(evidence['section_heading'], '# Limits')

    def test_invented_words_or_removed_negation_stay_unsupported(self):
        source = 'The synthetic plan does not permit private hosting.'
        claim = self.assess(source, 'The synthetic plan does permit private hosting.')
        self.assertEqual(claim['status'], 'unsupported')
        self.assertEqual(claim['evidence_rejections'], {'quote_not_in_source': 1})

    def test_punctuation_is_not_silently_rewritten(self):
        claim = self.assess('The synthetic plan permits five reports, not fifty.',
                            'The synthetic plan permits five reports; not fifty.')
        self.assertEqual(claim['status'], 'unsupported')

    def test_whitespace_equivalent_occurrences_remain_ambiguous(self):
        source = '# Old\nThe synthetic plan\tpermits five reports.\n# New\nThe synthetic plan\npermits five reports.'
        claim = self.assess(source, 'The synthetic plan permits five reports.')
        self.assertEqual(claim['status'], 'uncertain')
        self.assertGreater(claim['evidence'][0]['match_count'], 1)

    def test_model_scope_rejection_still_controls_semantic_support(self):
        claim = self.assess('# Dedicated only\nThe synthetic plan\tpermits five reports.',
                            'The synthetic plan permits five reports.', status='uncertain')
        self.assertTrue(claim['evidence'])
        self.assertEqual(claim['status'], 'uncertain')

    def test_overlapping_whitespace_matches_stay_ambiguous(self):
        claim = self.assess('longtoken\tlongtoken\tlongtoken', 'longtoken longtoken')
        self.assertEqual(claim['status'], 'uncertain')
        self.assertEqual(claim['evidence'][0]['match_count'], 2)

    def test_pipeline_recovers_spacing_without_extra_calls(self):
        class SpacedProvider(FakeProvider):
            def search(self, query):
                self.calls.append('search')
                return [{'url': 'https://example.com/limits', 'raw_content': PASSAGE.replace(' ', '  ')}]
        provider = SpacedProvider()
        with tempfile.TemporaryDirectory() as directory, patch(
                'socket.socket.connect', side_effect=AssertionError('Network forbidden')):
            report = research('What are the synthetic plan limits?', provider, Budget(directory + '/quota.db'))
        self.assertEqual(report['status'], 'evidence_found')
        self.assertEqual(report['claims'][0]['evidence'][0]['quote_match'], 'whitespace_only')
        self.assertEqual(provider.calls.count('search'), 3)
        self.assertEqual(len([c for c in provider.calls if c in ('plan', 'synthesis', 'evidence_review')]), 3)
