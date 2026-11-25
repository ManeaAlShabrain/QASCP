"""Real disposable Git repositories exercise the exact CI entry point; no secrets."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts.verify_checkout_auth import CheckoutAuthError, verify_checkout_auth


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/verify_checkout_auth.py"
MARKER = "QASCP-NONSECRET-REGRESSION-MARKER"


class CheckoutAuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        # Deterministic probe: never invoke a real configured helper or remote.
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        self.git("init", "--quiet")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, env=self.env,
                              capture_output=True, check=True)

    def check_cli(self, expected):
        result = subprocess.run([sys.executable, "-B", str(SCRIPT)], cwd=self.repo,
                                env=self.env, capture_output=True)
        self.assertEqual(result.returncode, expected, result.stderr)
        self.assertNotIn(MARKER.encode(), result.stdout + result.stderr)
        return result

    def test_clean_repository_passes(self):
        self.check_cli(0)

    def test_direct_prohibited_keys_fail(self):
        for key in ("credential.helper", "credential.https://example.invalid.helper",
                    "http.extraheader", "http.https://example.invalid/.extraheader",
                    "core.sshCommand"):
            with self.subTest(key=key):
                self.git("config", "--local", key, MARKER)
                self.check_cli(1)
                self.git("config", "--local", "--unset-all", key)

    def test_included_prohibited_keys_fail(self):
        for key in ("credential.helper", "http.extraheader", "core.sshCommand"):
            with self.subTest(key=key):
                included = self.root / "included-config"
                self.git("config", "--file", str(included), key, MARKER)
                self.git("config", "--local", "include.path", str(included))
                # Confirm the actual effective local key is present, without logging its value.
                effective = self.git("config", "--local", "--includes", "--name-only", "--list")
                self.assertIn(key.lower().encode(), effective.stdout.lower())
                self.check_cli(1)
                self.git("config", "--local", "--unset-all", "include.path")
                included.unlink()

    def test_matching_conditional_includes_fail(self):
        for condition in ("gitdir:**/repo/.git", "gitdir/i:**/REPO/.git"):
            for key in ("credential.helper", "http.extraheader", "core.sshCommand"):
                with self.subTest(condition=condition, key=key):
                    included = self.root / "conditional-config"
                    self.git("config", "--file", str(included), key, MARKER)
                    directive = "includeIf." + condition + ".path"
                    self.git("config", "--local", directive, str(included))
                    effective = self.git("config", "--local", "--includes", "--name-only", "--list")
                    self.assertIn(key.lower().encode(), effective.stdout.lower())
                    self.check_cli(1)
                    self.git("config", "--local", "--unset-all", directive)
                    included.unlink()

    def test_inactive_and_missing_includes_also_fail_closed(self):
        self.git("config", "--local", "includeIf.gitdir:/qas-test-never-match/.path", MARKER)
        self.check_cli(1)
        self.git("config", "--local", "--unset-all", "includeIf.gitdir:/qas-test-never-match/.path")
        self.git("config", "--local", "include.path", str(self.root / "missing"))
        self.check_cli(1)

    def test_malformed_config_does_not_expose_git_stderr(self):
        (self.repo / ".git/config").write_text("[" + MARKER, encoding="utf-8")
        self.check_cli(1)

    def test_non_repository_fails(self):
        with self.assertRaises(CheckoutAuthError):
            verify_checkout_auth(self.root)

    def test_inspection_failures_and_unexpected_output_fail_closed(self):
        for output, code in ((b"", 2), (b"credential.helper", 0), (b"\xff\0", 0), (b"\0", 0)):
            with self.subTest(code=code, output=output):
                result = subprocess.CompletedProcess([], code, output, MARKER.encode())
                with patch("scripts.verify_checkout_auth.subprocess.run", return_value=result):
                    with self.assertRaises(CheckoutAuthError) as caught:
                        verify_checkout_auth(self.repo)
                    self.assertNotIn(MARKER, str(caught.exception))

    def test_second_effective_inspection_failure_is_not_ignored(self):
        results = [subprocess.CompletedProcess([], 0, b"core.bare\0", b""),
                   subprocess.CompletedProcess([], 128, b"", MARKER.encode())]
        with patch("scripts.verify_checkout_auth.subprocess.run", side_effect=results):
            with self.assertRaises(CheckoutAuthError):
                verify_checkout_auth(self.repo)

    def test_unavailable_git_and_timeout_fail_closed(self):
        for error in (OSError(MARKER), subprocess.TimeoutExpired("git", 15, stderr=MARKER)):
            with patch("scripts.verify_checkout_auth.subprocess.run", side_effect=error):
                with self.assertRaises(CheckoutAuthError) as caught:
                    verify_checkout_auth(self.repo)
                self.assertNotIn(MARKER, str(caught.exception))
