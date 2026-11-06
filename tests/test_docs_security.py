import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("docs_security", SOURCE / "scripts/check_docs_security.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class DocumentationSecurityTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ, {"CI": ""})
        environment.start()
        self.addCleanup(environment.stop)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "usdd/en").mkdir(parents=True)
        self.page = self.root / "usdd/en/README.md"
        self.page.write_text("# Docs\n[App](https://app.usdd.io/)\n")
        self.policy = {"version": 1, "allowed_hosts": ["app.usdd.io", "etherscan.io"], "http_exceptions": [], "critical_pages": [], "asset_extensions": [".png", ".svg", ".pdf"]}
        self.baseline = {"version": 1, "files": {}}

    def rules(self):
        return {json.loads(item)["rule"] for item in checker.check(self.root, self.policy, self.baseline)}

    def test_normal_document_passes(self):
        self.assertEqual(self.rules(), set())

    def test_policy_rejects_string_instead_of_exact_host_list(self):
        self.policy["allowed_hosts"] = "app.usdd.io.attacker.invalid"
        with self.assertRaises(ValueError):
            checker.validate_policy(self.policy, self.baseline)

    def test_exact_hosts_and_https(self):
        for url in ("https://app.usdd.io.attacker.invalid/", "http://app.usdd.io/", "https://app.usdd.io:444/", "https://evil.invalid/"):
            with self.subTest(url=url):
                self.page.write_text(f"[App]({url})")
                self.assertIn("unapproved-url-origin", self.rules())

    def test_local_health_exception_is_exact(self):
        self.policy["http_exceptions"] = ["http://127.0.0.1:3101/health"]
        self.page.write_text("[health](http://127.0.0.1:3101/health)")
        self.assertEqual(self.rules(), set())
        self.page.write_text("[health](http://127.0.0.1:3101/other)")
        self.assertIn("unapproved-url-origin", self.rules())

    def test_encoded_active_url_and_html_are_blocked(self):
        for content in ("[x](java%73cript:alert(1))", '<a href="java&#x73;cript:alert(1)">x</a>', "[x](//evil.invalid/)", '<img src="https://app.usdd.io/a.png" onerror="x()">', '<iframe src="https://app.usdd.io/"></iframe>', '<script src="https://app.usdd.io/a.js"></script>', '<meta http-equiv="refresh" content="0;url=https://app.usdd.io/">'):
            with self.subTest(content=content):
                self.page.write_text(content)
                self.assertTrue(self.rules())

    def test_missing_local_file_and_escape(self):
        for target in ("missing.md", "../../../outside.md", "/etc/passwd"):
            self.page.write_text(f"[x]({target})")
            self.assertIn("broken-or-unsafe-local-link", self.rules())

    def test_parenthesized_asset_and_reference_links(self):
        asset = self.root / "usdd/en/screen (1).png"
        asset.write_bytes(b"test image")
        self.baseline["files"]["usdd/en/screen (1).png"] = checker.sha256(asset)
        self.page.write_text('![screen](screen (1).png)\n[app]: <https://app.usdd.io/>\n')
        self.assertEqual(self.rules(), set())

    def test_url_credentials_never_printed(self):
        token = "ghp_" + "a" * 36
        self.page.write_text(f"{token}\n[x](https://user:password@app.usdd.io/)\n")
        findings = checker.check(self.root, self.policy, self.baseline)
        self.assertIn("github-token", self.rules())
        self.assertIn("credential-in-url", self.rules())
        self.assertNotIn(token, "\n".join(findings))
        self.assertNotIn("password", "\n".join(findings))

    def test_legacy_secret_still_fails(self):
        legacy = self.root / "legacy-usdd/en/README.md"
        legacy.parent.mkdir(parents=True)
        legacy.write_text("AKIA" + "A" * 16)
        self.assertIn("aws-key", self.rules())

    def test_address_destination_mismatch(self):
        one, two = "0x" + "1" * 40, "0x" + "2" * 40
        self.page.write_text(f"[{one}](https://etherscan.io/address/{two})")
        self.assertIn("address-link-mismatch", self.rules())
        self.page.write_text(f'<a href="https://etherscan.io/address/{two}">{one}</a>')
        self.assertIn("address-link-mismatch", self.rules())

    def test_sensitive_content_requires_baseline_and_detects_swaps(self):
        self.page.write_text("A: 0x" + "1" * 40)
        self.assertIn("unreviewed-sensitive-file", self.rules())
        self.baseline["files"]["usdd/en/README.md"] = checker.sha256(self.page)
        self.assertEqual(self.rules(), set())
        self.page.write_text("B: 0x" + "1" * 40)
        self.assertIn("sensitive-file-baseline-mismatch", self.rules())
        self.page.unlink()
        self.assertIn("sensitive-file-baseline-mismatch", self.rules())

    def test_asset_add_replace_delete(self):
        asset = self.root / "usdd/en/report.pdf"
        asset.write_bytes(b"original")
        self.assertIn("unreviewed-asset", self.rules())
        self.baseline["files"]["usdd/en/report.pdf"] = checker.sha256(asset)
        self.assertEqual(self.rules(), set())
        asset.write_bytes(b"replaced")
        self.assertIn("sensitive-file-baseline-mismatch", self.rules())
        asset.unlink()
        self.assertIn("sensitive-file-baseline-mismatch", self.rules())

    def test_symlink_rejected(self):
        (self.root / "usdd/en/linked.md").symlink_to(self.page)
        self.assertIn("symlink-or-path-escape", self.rules())

    def test_unknown_executable_file_rejected(self):
        (self.root / "usdd/en/payload.js").write_text("alert(1)")
        self.assertIn("unapproved-content-file-type", self.rules())

    def test_ci_cannot_regenerate_baseline(self):
        with patch.dict(os.environ, {"CI": "true"}):
            with self.assertRaises(ValueError):
                checker.refresh(self.root, self.policy, self.root / "baseline.json")

    def test_transition_keeps_old_and_new_then_finalize_requires_current(self):
        self.policy["critical_pages"] = ["usdd/en/README.md"]
        destination = self.root / "baseline.json"
        checker.refresh(self.root, self.policy, destination)
        old = self.page.read_text()
        self.page.write_text(old + "Approved change\n")
        checker.refresh(self.root, self.policy, destination)
        self.baseline = checker.load_json(destination)
        checker.validate_policy(self.policy, self.baseline)
        self.assertEqual(self.rules(), set())
        self.page.write_text(old)
        self.assertEqual(self.rules(), set())
        checker.refresh(self.root, self.policy, destination, finalize=True)
        self.baseline = checker.load_json(destination)
        self.page.write_text(old + "Approved change\n")
        self.assertIn("sensitive-file-baseline-mismatch", self.rules())

    def test_transition_accepts_only_reviewed_new_asset_and_planned_deletion(self):
        destination = self.root / "baseline.json"
        self.policy["critical_pages"] = ["usdd/en/README.md"]
        checker.refresh(self.root, self.policy, destination)
        asset = self.root / "usdd/en/report.pdf"
        asset.write_bytes(b"reviewed")
        checker.refresh(self.root, self.policy, destination)
        self.baseline = checker.load_json(destination)
        self.assertEqual(self.rules(), set())
        asset.unlink()
        self.assertEqual(self.rules(), set())
        asset.write_bytes(b"unreviewed")
        self.assertIn("sensitive-file-baseline-mismatch", self.rules())

    def test_trusted_policy_wins_over_candidate_policy(self):
        # Candidate cannot approve its own new origin by changing its local policy.
        self.page.write_text("[App](https://evil.invalid/)")
        candidate_policy = self.root / "security/doc-policy.json"
        candidate_policy.parent.mkdir()
        expanded = dict(self.policy, allowed_hosts=["evil.invalid"])
        candidate_policy.write_text(json.dumps(expanded))
        policy = self.root / "trusted-policy.json"
        baseline = self.root / "trusted-baseline.json"
        policy.write_text(json.dumps(self.policy))
        baseline.write_text(json.dumps(self.baseline))
        result = subprocess.run([sys.executable, "-I", str(SOURCE / "scripts/check_docs_security.py"), "--root", str(self.root), "--policy", str(policy), "--baseline", str(baseline)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("unapproved-url-origin", result.stdout)


if __name__ == "__main__":
    unittest.main()
