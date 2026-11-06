#!/usr/bin/env python3
"""Offline checks only. Never import or execute code from the scanned tree."""
import argparse
import hashlib
import html
import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

CODE_ROOT = Path(__file__).resolve().parents[1]
ADDRESS = re.compile(r"(?<![\w])(?:0x[0-9a-fA-F]{40}|T[1-9A-HJ-NP-Za-km-z]{33})(?![\w])")
ABS_URL = re.compile(r"https?://[^\s<>\x22\x27)\]\x60}]+", re.I)
SECRETS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b"),
    "aws-key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "wallet-key": re.compile(r"(?i)(?:private[_ -]?key|mnemonic|seed phrase)[\x22\x27]?\s*[:=]\s*[\x22\x27]?(?:0x)?[a-f0-9]{64}\b"),
    "credential-literal": re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)[\x22\x27]?\s*[:=]\s*[\x22\x27]([A-Za-z0-9_+/=.-]{24,})[\x22\x27]"),
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_address(value):
    return value.lower() if value.startswith("0x") else value


def markdown_links(text):
    """Yield inline destinations, including GitBook filenames with spaces/parentheses."""
    for match in re.finditer(r"!?\[([^\]\n]*)\]\(", text):
        start, pos, depth = match.end(), match.end(), 1
        while pos < len(text) and text[pos] != "\n":
            if text[pos] == "\\":
                pos += 2
                continue
            if text[pos] == "(":
                depth += 1
            elif text[pos] == ")":
                depth -= 1
                if depth == 0:
                    raw = text[start:pos].strip()
                    target = raw[1:raw.find(">", 1)] if raw.startswith("<") and ">" in raw else re.split(r"\s+[\x22\x27]", raw, maxsplit=1)[0]
                    yield match.start(), match.group(1), target
                    break
            pos += 1
    for match in re.finditer(r"(?m)^\s*\[[^\]\n]+\]:\s*(<[^>]+>|\S+)", text):
        yield match.start(), "", match.group(1).strip("<>")
    for match in re.finditer(r"{%\s*(?:file|embed|include)\b[^%]*\b(?:src|url)=[\x22\x27]([^\x22\x27]+)", text):
        yield match.start(), "", match.group(1)


class Markup(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.targets, self.unsafe, self.anchors = [], [], []
        self.anchor = None

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        values = dict(attrs)
        if tag in {"script", "iframe", "object", "embed", "form", "meta", "base", "link"}:
            self.unsafe.append((line, "active-html"))
        for key, value in attrs:
            if key.startswith("on") or key == "srcdoc":
                self.unsafe.append((line, "active-html-attribute"))
            if value and key in {"href", "src", "xlink:href", "action", "formaction", "data", "poster"}:
                self.targets.append((line, value))
            if value and key == "srcset":
                self.targets.extend((line, part.strip().split()[0]) for part in value.split(",") if part.strip())
        if tag == "a":
            self.anchor = [line, values.get("href", ""), ""]

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_data(self, data):
        if self.anchor is not None:
            self.anchor[2] += data

    def handle_endtag(self, tag):
        if tag == "a" and self.anchor is not None:
            self.anchors.append(self.anchor)
            self.anchor = None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def accepted_hashes(value):
    return [value] if isinstance(value, str) else value


def validate_policy(policy, baseline):
    if policy.get("version") != 1 or baseline.get("version") != 1:
        raise ValueError("unsupported policy/baseline version")
    for field in ("allowed_hosts", "http_exceptions", "critical_pages", "asset_extensions"):
        if not isinstance(policy[field], list) or any(not isinstance(item, str) for item in policy[field]):
            raise ValueError("policy fields must be string lists")
    if not policy["allowed_hosts"] or not isinstance(baseline["files"], dict):
        raise ValueError("empty origins or invalid file inventory")
    for host in policy["allowed_hosts"]:
        if not re.fullmatch(r"[a-z0-9]+(?:[.-][a-z0-9]+)*", host):
            raise ValueError("allowed_hosts must contain exact lowercase hostnames")
    for path, value in baseline["files"].items():
        digests = accepted_hashes(value)
        if Path(path).is_absolute() or ".." in Path(path).parts or not isinstance(digests, list) or not 1 <= len(digests) <= 2 or any(not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest) for digest in digests):
            raise ValueError("invalid baseline path/hash")
    if any(path not in baseline["files"] for path in baseline.get("optional_files", [])):
        raise ValueError("optional files must be present in baseline")
    for path in policy["critical_pages"]:
        if path not in baseline["files"] or Path(path).is_absolute() or ".." in Path(path).parts:
            raise ValueError("critical page missing from baseline")


def check(root, policy, baseline):
    root = root.resolve()
    findings = []

    def report(path, line, rule):
        # Deliberately omit matching content, URLs, keys and token values from CI logs.
        findings.append({"file": str(path), "line": line, "rule": rule})

    def safe_file(path):
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            report(path.relative_to(root), 1, "symlink-or-path-escape")
            return False
        return True

    def target_check(path, line, target):
        target = html.unescape(target).strip()
        normalized = re.sub(r"[\x00-\x20]", "", unquote(target))
        if normalized.startswith("//"):
            report(path.relative_to(root), line, "protocol-relative-url")
            return
        try:
            parsed = urlsplit(normalized)
            port = parsed.port
        except ValueError:
            report(path.relative_to(root), line, "invalid-url")
            return
        if parsed.scheme:
            if parsed.scheme not in {"http", "https"}:
                report(path.relative_to(root), line, "unapproved-url-scheme")
            elif parsed.username or parsed.password or re.search(r"(?i)(?:api[_-]?key|access[_-]?token|password|private[_-]?key)=", parsed.query):
                report(path.relative_to(root), line, "credential-in-url")
            elif target in policy["http_exceptions"]:
                return
            elif parsed.scheme != "https" or parsed.hostname not in policy["allowed_hosts"] or port not in (None, 443):
                report(path.relative_to(root), line, "unapproved-url-origin")
        elif parsed.path:
            local = path.parent / unquote(urlsplit(target).path)
            if target.startswith("/") or not local.resolve().is_relative_to(root) or not local.exists() or local.is_symlink():
                report(path.relative_to(root), line, "broken-or-unsafe-local-link")

    def address_link(path, line, label, href):
        shown = {canonical_address(a) for a in ADDRESS.findall(label)}
        destination = {canonical_address(a) for a in ADDRESS.findall(unquote(href))}
        if shown and not shown.issubset(destination):
            report(path.relative_to(root), line, "address-link-mismatch")

    current = root / "usdd/en"
    if not current.is_dir():
        report("usdd/en", 1, "missing-current-documentation")
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if ".git" in rel.parts or "__pycache__" in rel.parts:
            continue
        if not safe_file(path) or not path.is_file():
            continue
        is_current = rel.parts[:2] == ("usdd", "en")
        if is_current and path.suffix.lower() not in {".md", *policy["asset_extensions"]}:
            report(rel, 1, "unapproved-content-file-type")
        if path.suffix.lower() not in {".md", ".svg"}:
            continue
        text = path.read_text(encoding="utf-8")
        if path.suffix.lower() == ".md":
            for rule, pattern in SECRETS.items():
                for match in pattern.finditer(text):
                    if rule == "credential-literal" and any(word in match.group(1).lower() for word in ("your_", "example", "placeholder")):
                        continue
                    report(rel, text.count("\n", 0, match.start()) + 1, rule)
        # Historical content gets secret checks, not the current site's origin policy.
        if rel.parts[0] == "legacy-usdd":
            continue
        parser = Markup()
        parser.feed(text)
        for line, rule in parser.unsafe:
            report(rel, line, rule)
        for line, target in parser.targets:
            target_check(path, line, target)
        for line, href, label in parser.anchors:
            address_link(path, line, label, href)
        if path.suffix.lower() == ".md":
            for offset, label, target in markdown_links(text):
                line = text.count("\n", 0, offset) + 1
                target_check(path, line, target)
                address_link(path, line, label, target)
            for match in ABS_URL.finditer(text):
                target_check(path, text.count("\n", 0, match.start()) + 1, match.group().rstrip(".,;\\"))
        requires_pin = is_current and (path.suffix.lower() != ".md" or ADDRESS.search(text) or str(rel) in policy["critical_pages"])
        if requires_pin and str(rel) not in baseline["files"]:
            report(rel, 1, "unreviewed-sensitive-file")
    # Include binary assets; missing or changed pinned files must also fail.
    for path in sorted(current.rglob("*")):
        if path.is_file() and path.suffix.lower() != ".md" and str(path.relative_to(root)) not in baseline["files"]:
            report(path.relative_to(root), 1, "unreviewed-asset")
    for relative, expected in baseline["files"].items():
        path = root / relative
        if not path.exists() and relative in baseline.get("optional_files", []):
            continue
        if not path.is_file() or not safe_file(path) or sha256(path) not in accepted_hashes(expected):
            report(relative, 1, "sensitive-file-baseline-mismatch")
    return sorted({json.dumps(item, sort_keys=True) for item in findings})


def refresh(root, policy, destination, finalize=False):
    if os.environ.get("CI"):
        raise ValueError("baseline refresh is forbidden in CI")
    root = root.resolve()
    previous = load_json(destination) if destination.exists() and not finalize else {"files": {}}
    files = dict(previous["files"])
    optional = set(previous.get("optional_files", []))
    seen = set()
    for path in sorted((root / "usdd/en").rglob("*")):
        if path.is_symlink():
            raise ValueError("baseline refresh refuses symlinks")
        if not path.is_file():
            continue
        relative = str(path.relative_to(root))
        if path.suffix.lower() != ".md" or relative in policy["critical_pages"] or ADDRESS.search(path.read_text(encoding="utf-8")):
            seen.add(relative)
            digest = sha256(path)
            hashes = sorted(set(accepted_hashes(files.get(relative, digest))) | {digest})
            if len(hashes) > 2:
                raise ValueError("finalize previous baseline transition before another update")
            if relative not in previous["files"] and previous["files"]:
                optional.add(relative)
            files[relative] = hashes[0] if len(hashes) == 1 else hashes
    optional.update(set(previous["files"]) - seen)
    destination.write_text(json.dumps({"version": 1, "optional_files": sorted(optional), "files": dict(sorted(files.items()))}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=CODE_ROOT)
    parser.add_argument("--policy", type=Path, default=CODE_ROOT / "security/doc-policy.json")
    parser.add_argument("--baseline", type=Path, default=CODE_ROOT / "security/doc-baseline.json")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--refresh-baseline", action="store_true", help="local-only old/new transition generation; requires source verification before merging")
    mode.add_argument("--finalize-baseline", action="store_true", help="local-only prune to reviewed current content after a transition")
    args = parser.parse_args()
    try:
        policy = load_json(args.policy)
        if args.refresh_baseline or args.finalize_baseline:
            refresh(args.root.resolve(), policy, args.baseline, finalize=args.finalize_baseline)
            print("Candidate baseline written; verify each change against source evidence before merging.")
            return 0
        baseline = load_json(args.baseline)
        validate_policy(policy, baseline)
        findings = check(args.root.resolve(), policy, baseline)
    except (OSError, ValueError, KeyError, UnicodeError):
        print("ERROR: invalid/unreadable documentation, policy or baseline", file=sys.stderr)
        return 2
    for finding in findings:
        print(finding)
    print(f"Documentation security: {len(findings)} finding(s). Offline checks only.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
