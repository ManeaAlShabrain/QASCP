"""Exercise the exact CI auth guard on disposable Git repositories; no credentials."""
import json, pathlib, subprocess, sys, tempfile, textwrap
BASE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path(sys.argv[1]).resolve()
workflow = (ROOT / ".github/workflows/ci.yml").read_text("utf-8")
body = textwrap.dedent(workflow.split("python3 - <<'PY'\n", 1)[1].split("\n          PY", 1)[0])
results = []
with tempfile.TemporaryDirectory(prefix="qascp-review-auth-") as directory:
    root = pathlib.Path(directory).resolve()
    for case in ["clean", "direct", "include", "includeIf"]:
        repo = root / case
        repo.mkdir()
        subprocess.run(["git", "init", "--quiet", str(repo)], check=True, capture_output=True)
        if case == "direct":
            subprocess.run(["git", "config", "--local", "credential.helper", "qascp-review-nonsecret-marker"], cwd=repo, check=True)
        elif case in ["include", "includeIf"]:
            config = root / (case + "-nonsecret.cfg")
            config.write_text("[credential]\n\thelper = qascp-review-nonsecret-marker\n", encoding="utf-8")
            key = "include.path" if case == "include" else "includeIf.gitdir/i:**/includeIf/.git.path"
            subprocess.run(["git", "config", "--local", key, str(config)], cwd=repo, check=True)
        guard = subprocess.run([sys.executable, "-c", body], cwd=repo, capture_output=True, text=True)
        effective = subprocess.run(["git","config","--local","--includes","--name-only","--get-regexp",r"^(http(\..*)?\.extraheader|credential\..*|core\.sshcommand)$"], cwd=repo, capture_output=True, text=True)
        results.append({"case":case, "guard_exit":guard.returncode, "guard_output":guard.stdout+guard.stderr, "included_prohibited_key_names":effective.stdout.splitlines(),"effective_exit":effective.returncode})
(BASE / "checkout-probe.json").write_text(json.dumps({"exact_guard":body,"results":results}, indent=2), encoding="utf-8")
print(json.dumps(results, indent=2))

