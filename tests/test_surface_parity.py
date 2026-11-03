"""SURFACE-2: reuse the failed-search provider; execute actual renderer in a DOM double."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evidencepilot.core import Budget, research
from test_core import FakeProvider


class CapabilityFixtureProvider(FakeProvider):
    """Fictional endpoint and review labels; never a live-success demo."""
    domain = 'The synthetic search endpoint supports domain restriction.'
    limit = 'The synthetic result limit is a maximum, not a guaranteed count.'
    def search(self, query):
        self.calls.append('search')
        return [{'url': 'https://example.com/synthetic-search', 'title': 'Synthetic endpoint',
                 'raw_content': self.domain + '\n' + self.limit}]
    def model_json(self, purpose, instruction, data):
        result = super().model_json(purpose, instruction, data)
        if purpose == 'plan':
            result['requirements'] = [{'text': value, 'user_spans': [{'quote': value}]}
                                      for value in ('domain restriction', 'result limit')]
        if purpose == 'synthesis':
            result['claims'] = [{'text': value, 'requirement_ids': ['R' + str(i)],
                                 'evidence': [{'source_id': 'S1', 'quote': value}]}
                                for i, value in enumerate((self.domain, self.limit), 1)]
        if purpose == 'evidence_review':
            result['reviews'] = [{'claim_id': 'C' + str(i), 'status': 'supported',
                                  'reason': 'Synthetic fixture judgment only.'} for i in (1, 2)]
        return result


class SurfaceParityTests(unittest.TestCase):
    def test_supported_fixture_quotes_links_and_export(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory, patch('socket.socket.connect', side_effect=AssertionError('Network forbidden')):
            provider = CapabilityFixtureProvider()
            report = research('Does the synthetic endpoint support domain restriction and a result limit?',
                              provider, Budget(directory + '/quota.db'))
            self.assertEqual(report['status'], 'evidence_found')
            path = Path(directory) / 'supported-fixture.json'
            path.write_text(json.dumps(report))
            result = subprocess.run(['node', str(root / 'tests/surface_parity.cjs'), str(path), 'supported'],
                                    cwd=root, capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(provider.calls.count('search'), 3)
            print(result.stdout.strip())

    def test_failed_search_card_text_and_bound_export(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory, patch('socket.socket.connect', side_effect=AssertionError('Network forbidden')):
            provider = FakeProvider('search_error')
            report = research('What are the synthetic plan limits?', provider, Budget(directory+'/q.db'))
            self.assertEqual(report['status'], 'insufficient_evidence')
            self.assertEqual(report['claims'], [])
            self.assertNotIn('synthesis', provider.calls)
            path = Path(directory)/'failed-search.json'
            path.write_text(json.dumps(report))
            result = subprocess.run(['node', str(root/'tests/surface_parity.cjs'), str(path)], cwd=root,
                                    capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
            print(result.stdout.strip())
