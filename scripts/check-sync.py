#!/usr/bin/env python3
"""Guard the judge encodings against silent drift.

The two judges exist in several encodings that must stay behaviorally identical:
references/judges.md (canonical), the two agent files, PROMPT.md, PROMPT-quick.md, the
inlined prompts in scripts/judge.py, and the structured-output fields in
references/judge-schemas.json. Hand-syncing is "remember to do it"; this script makes CI
remember. It checks that each load-bearing phrase and format marker appears in every
encoding that carries that judge; a miss means an edit landed in one encoding only.

Substring checks are deliberate: encodings compress differently, so full-text equality is
wrong, but the role line, the lens names, the format markers, and the coverage rule must
survive every compression.

Exit 0 clean, 1 on drift.
"""

import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

JUDGES = "fb5/references/judges.md"
AGENT_V = "agents/verifier.md"
AGENT_T = "agents/taste-judge.md"
PROMPT = "PROMPT.md"
QUICK = "PROMPT-quick.md"
SCRIPT = "scripts/judge.py"
SCHEMAS = "fb5/references/judge-schemas.json"

# phrase -> files it must appear in (case-insensitive substring)
INVARIANTS = {
    # Judge 1: the verifier
    "fresh-eyes verifier": [JUDGES, AGENT_V, PROMPT, SCRIPT],
    "did not produce": [JUDGES, AGENT_V, SCRIPT, QUICK],
    "coverage first, filtering never": [JUDGES, AGENT_V, PROMPT, SCRIPT],
    "could this exact frame, layout, or sentence appear unchanged": [JUDGES, AGENT_V, SCRIPT],
    "unverified: <line>": [JUDGES, PROMPT, SCRIPT, QUICK],
    "unverified: <rubric line>": [AGENT_V],
    "confidence: <h/m/l>": [JUDGES, AGENT_V, AGENT_T, PROMPT, QUICK],
    "empty findings list is a strong claim": [JUDGES, AGENT_V, SCRIPT],
    # Judge 2: the taste gate
    "you are the final quality gate": [JUDGES, AGENT_T, PROMPT, SCRIPT],
    "first-time audience": [JUDGES, AGENT_T, PROMPT, SCRIPT],
    "expert practitioner": [JUDGES, AGENT_T, PROMPT, SCRIPT],
    "brand owner": [JUDGES, AGENT_T, PROMPT, SCRIPT],
    "gate: <pass | fail>": [JUDGES, AGENT_T, PROMPT],
    "embarrass the work in front of an expert": [JUDGES, AGENT_T, PROMPT, SCRIPT],
    "distill": [JUDGES, AGENT_T, PROMPT, SCHEMAS],
    "the widest that is still true": [JUDGES, AGENT_T, PROMPT, SCRIPT],
    "rubric gaming": [JUDGES, AGENT_T, PROMPT, SCRIPT],
    # Schema fields the script and downstream parsers rely on
    '"enum": ["pass", "fail"]': [SCHEMAS],
    '"enum": ["h", "m", "l"]': [SCHEMAS],
    '"rubric_line"': [SCHEMAS],
    '"fix_direction"': [SCHEMAS],
}


def main():
    texts = {}
    missing_files = []
    for files in INVARIANTS.values():
        for f in files:
            if f in texts:
                continue
            path = os.path.join(ROOT, f)
            if not os.path.isfile(path):
                missing_files.append(f)
                texts[f] = ""
                continue
            with open(path, encoding="utf-8") as fh:
                # Collapse whitespace: encodings wrap lines at different widths.
                texts[f] = re.sub(r"\s+", " ", fh.read().lower())

    failures = []
    for phrase, files in INVARIANTS.items():
        needle = re.sub(r"\s+", " ", phrase.lower())
        for f in files:
            if needle not in texts[f]:
                failures.append("%s missing: %r" % (f, phrase))

    for f in sorted(set(missing_files)):
        failures.append("%s: file not found" % f)

    if failures:
        print("judge encodings drifted; sync all encodings of the edited judge "
              "(canonical: %s):" % JUDGES)
        for line in failures:
            print("  " + line)
        sys.exit(1)
    print("check-sync: %d invariants hold across %d files"
          % (len(INVARIANTS), len(texts)))


if __name__ == "__main__":
    main()
