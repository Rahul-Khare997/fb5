#!/usr/bin/env python3
"""Mechanical ban-list scan: the blocking gate from protocol Law 7, as a script.

Instructions get skipped; a script does not. This scans delivered text for the universal
ban categories (filler vocabulary, placeholder elisions, stock names, round vanity stats,
hedged completion claims) and reports file:line findings in the verifier's spirit:
coverage first, every hit reported, judging happens downstream.

The lists here are the UNIVERSAL bans (protocol Law 7 + the writing/code craft files'
shared core). Craft files carry domain-specific bans on top; the scan does not replace
reading them. A hit is a finding, not a verdict: a quoted example or a ban list itself
(like this file) legitimately contains banned words; justify or fix, per Law 5.

Usage:
  banscan.py FILE [FILE...]      scan files, findings to stdout, exit 1 on any hit
  banscan.py -                   scan stdin
  banscan.py --hook              Claude Code PostToolUse hook mode: reads the hook JSON
                                 from stdin, scans the written/edited file, and reports
                                 findings back to the model (exit 2) so they get fixed
                                 in-turn; silent (exit 0) when clean.

Prose checks run on prose files (.md .txt .html .mdx .rst and stdin); placeholder and
completion checks run everywhere, including code.
"""

import json
import os
import re
import sys

PROSE_EXT = {".md", ".mdx", ".txt", ".rst", ".html"}

# Category: filler vocabulary (protocol Law 7: the ban is the category, not the list).
FILLER = [
    r"\bseamless\w*", r"\bleverag\w+", r"\bunlock\b", r"\bsupercharge\w*",
    r"\brobust\b", r"\bat scale\b", r"\bworld[- ]class\b", r"\bcutting[- ]edge\b",
    r"\bnext[- ]generation\b", r"\belevate\w*", r"\bempower\w*", r"\bdelve\w*",
    r"\beffortless\w*", r"\bgame[- ]chang\w+", r"\brevolutioni\w+", r"\brevolutionary\b",
    r"\btransformative\b", r"\bstreamlin\w+", r"\bsynerg\w+", r"\bbest[- ]in[- ]class\b",
    r"\bstate[- ]of[- ]the[- ]art\b", r"harness the power", r"in today's fast-paced",
    r"look no further", r"takes .{0,20} to the next level",
]

# Category: stock names and lorem (any file type where they appear in prose).
STOCK = [
    r"\bacme\b", r"\bjohn smith\b", r"\bjane doe\b", r"\bjohn doe\b", r"\blorem ipsum\b",
]

# Category: round vanity stats in prose (10x, 100x, 99%, 99.9% as bare claims).
VANITY = [
    r"\b10x\b", r"\b100x\b", r"\b99(?:\.9)?%\b",
]

# Category: placeholder elisions and stubs (Law 9: complete output, always). All files.
PLACEHOLDER = [
    r"rest (?:of the file |of the code )?(?:remains |stays )?unchanged",
    r"\.\.\. ?(?:rest|remaining|other|more) ",
    r"# ?TODO\b", r"// ?TODO\b", r"<!-- ?TODO\b", r"\bFIXME\b",
    r"(?:implementation|content|details?) (?:goes|go) here",
    r"left as an exercise",
]

# Category: hedged completion claims (report format hard rule). Prose files.
HEDGE = [
    r"\bshould work\b", r"\bmight need\b", r"\bshould now\b", r"\bhopefully\b",
    r"\blikely works\b", r"\bprobably works\b",
]

CATEGORIES = [
    ("filler", FILLER, True),
    ("stock-name", STOCK, True),
    ("vanity-stat", VANITY, True),
    ("placeholder", PLACEHOLDER, False),
    ("hedge", HEDGE, True),
]


def scan_text(text, name, prose):
    findings = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for category, patterns, prose_only in CATEGORIES:
            if prose_only and not prose:
                continue
            for pat in patterns:
                m = re.search(pat, line, re.IGNORECASE)
                if m:
                    findings.append("%s:%d | %s | %r" % (name, lineno, category, m.group(0)))
    return findings


def scan_file(path):
    ext = os.path.splitext(path)[1].lower()
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except (UnicodeDecodeError, OSError):
        return []
    return scan_text(text, path, ext in PROSE_EXT)


def hook_mode():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)
    path = (payload.get("tool_input") or {}).get("file_path")
    if not path or not os.path.isfile(path):
        sys.exit(0)
    # Never lint the kit's own standards, ban lists, or examples.
    norm = path.replace(os.sep, "/")
    if any(seg in norm for seg in ("/references/", "/scripts/banscan", "/evals/")):
        sys.exit(0)
    findings = scan_file(path)
    if findings:
        print("banscan: ban-list hits (fix, or justify each in one line in your report):",
              file=sys.stderr)
        for f in findings:
            print("  " + f, file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    if args[0] == "--hook":
        hook_mode()
    findings = []
    for arg in args:
        if arg == "-":
            findings += scan_text(sys.stdin.read(), "stdin", True)
        else:
            findings += scan_file(arg)
    for f in findings:
        print(f)
    print("%d finding(s)" % len(findings), file=sys.stderr)
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
