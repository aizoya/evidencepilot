"""SURFACE-2: reuse the failed-search provider; execute actual renderer in a DOM double."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evidencepilot.core import Budget, research
from test_core import FakeProvider


class SurfaceParityTests(unittest.TestCase):
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
