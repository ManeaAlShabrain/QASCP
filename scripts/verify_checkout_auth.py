"""Inspect local and worktree checkout configuration without exposing values.

This boundary deliberately rejects every local include, even an inactive conditional
include, in either repository scope. Global/system/command configuration and
runner compromise remain outside this repository-configuration assertion.
"""

import subprocess
import sys
from pathlib import Path


class CheckoutAuthError(RuntimeError):
    """A safe diagnostic that never contains subprocess output or config values."""


def verify_checkout_auth(repository=Path(".")):
    inspections = ((scope, includes) for scope in ("--local", "--worktree")
                   for includes in ("--no-includes", "--includes"))
    for scope, includes in inspections:
        try:
            result = subprocess.run(
                ["git", "config", scope, includes, "--null", "--name-only", "--list"],
                cwd=repository, capture_output=True, check=False, timeout=15,
            )
            if result.returncode != 0:
                raise CheckoutAuthError("Cannot inspect local checkout configuration")
            raw = result.stdout
            if not isinstance(raw, bytes) or (raw and not raw.endswith(b"\0")):
                raise CheckoutAuthError("Invalid local checkout inspection result")
            names = raw.decode("utf-8", errors="strict").split("\0")[:-1]
            for name in names:
                key = name.lower()
                if not key or "\n" in key or "\r" in key:
                    raise CheckoutAuthError("Invalid local checkout configuration name")
                if (key == "include.path" or
                        (key.startswith("includeif.") and key.endswith(".path")) or
                        key.startswith("credential.") or key == "core.sshcommand" or
                        (key.startswith("http.") and key.endswith(".extraheader"))):
                    raise CheckoutAuthError("Prohibited local checkout authentication configuration")
        except (OSError, UnicodeError, subprocess.SubprocessError):
            raise CheckoutAuthError("Cannot inspect local checkout configuration") from None


def main():
    try:
        verify_checkout_auth()
    except CheckoutAuthError as error:
        print(str(error), file=sys.stderr)
        return 1
    print("Checkout authentication boundary passed; no local or worktree include paths remain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
