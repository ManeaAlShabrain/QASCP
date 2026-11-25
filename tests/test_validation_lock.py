"""A modified wheel/pin cannot silently keep the original provenance assertion."""

from pathlib import Path
import shutil
import tempfile
import unittest

from scripts.verify_validation_lock import ROOT, verify_lock


class ValidationLockTests(unittest.TestCase):
    def test_retained_lock_and_pin_tampering(self):
        self.assertEqual(verify_lock(), 19)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = ("requirements-contracts.txt", "requirements-contracts-linux-cp314.lock",
                     "docs/verification/remediation/P1-2026-11-25/dependency-evidence.json")
            for path in paths:
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / path, root / path)
            for path in paths[:2]:
                with self.subTest(path=path):
                    original = (root / path).read_text(encoding="utf-8")
                    (root / path).write_text(original.replace("attrs==25.4.0", "attrs==25.4.1"), encoding="utf-8")
                    with self.assertRaises(ValueError):
                        verify_lock(root)
                    (root / path).write_text(original, encoding="utf-8")
            lock = root / paths[1]
            original = lock.read_text(encoding="utf-8")
            lock.write_text(original.replace("--hash=sha256:a", "--hash=sha256:0", 1), encoding="utf-8")
            with self.assertRaises(ValueError):
                verify_lock(root)
