"""Regression for root metadata selection with legitimate vendored metadata."""

import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile

from scripts.resolve_p2_inputs import wheel_evidence


class P2Discovery(unittest.TestCase):
    def test_vendored_metadata_does_not_replace_root_distribution(self):
        with tempfile.TemporaryDirectory() as folder:
            wheel = Path(folder)/"original-1.0-py3-none-any.whl"
            with ZipFile(wheel, "w") as archive:
                archive.writestr("original-1.0.dist-info/METADATA", "Name: original\nVersion: 1.0\n")
                archive.writestr("original/vendor/other-2.0.dist-info/METADATA", "Name: other\nVersion: 2.0\n")
            digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
            release = {"urls": [{"filename": wheel.name, "digests": {"sha256": digest}, "url": "https://files.pythonhosted.org/test"}],
                       "info": {"license_expression": "MIT"}, "vulnerabilities": []}
            with patch("scripts.resolve_p2_inputs.metadata", return_value=release) as source:
                result = wheel_evidence(wheel)
            source.assert_called_once_with("original", "1.0")
            self.assertEqual(result["name"], "original")

    def test_missing_root_metadata_fails_without_network_lookup(self):
        with tempfile.TemporaryDirectory() as folder:
            wheel = Path(folder)/"invalid.whl"
            with ZipFile(wheel, "w") as archive:
                archive.writestr("vendor/other-2.0.dist-info/METADATA", "Name: other\nVersion: 2.0\n")
            with patch("scripts.resolve_p2_inputs.metadata") as source:
                with self.assertRaises(ValueError):
                    wheel_evidence(wheel)
            source.assert_not_called()
