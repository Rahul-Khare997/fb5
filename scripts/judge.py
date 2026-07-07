#!/usr/bin/env python3
"""Run a frontier judge as a stateless API call: true fresh eyes on any surface.

The judge sees ONLY the judge prompt, the rubric, the lens, and the evidence files you
pass. Nothing of the producing conversation leaks in, which is the whole point (protocol
Law 4: fresh eyes find defects; authors defend them).

Zero dependencies: stdlib only. Reads the judge prompts from references/judges.md is NOT
done at runtime; the prompts are inlined below and kept in sync by scripts/check-sync.py.

Usage:
  judge.py --judge verifier --lens layout --rubric rubric.md page.tsx shot-360.png.txt
  judge.py --judge gate --rubric rubric.md final.md
  judge.py --judge gate --rubric rubric.md --candidates cand-a.md cand-b.md cand-c.md

  --provider anthropic|openai|gemini   (default: first provider with an API key set)
  --model <id>                         (default: a strong tier per provider, see DEFAULTS)
  --json                               (force structured output; on by default where supported)

Keys from env: ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY.
Evidence files are read and inlined as text; binary files are skipped with a warning
(screenshots should be described or pre-converted; judges must inspect real evidence, so
prefer providers/models you can send images to via your own tooling when the evidence is
visual, and record what was NOT inspectable).

Exit codes: 0 = no findings (verifier) / gate pass; 1 = findings / gate fail; 2 = error.
"""

import argparse
import json
import os
import sys
import urllib.request

DEFAULTS = {
    "anthropic": "claude-opus-4-8",
    "openai": "gpt-5",
    "gemini": "gemini-2.5-pro",
}

ENV_KEYS = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "gemini": "GEMINI_API_KEY",
}

# Inlined from fb5/references/judges.md (Judge 1). check-sync.py verifies drift.
VERIFIER_PROMPT = """You are a fresh-eyes verifier. You did not produce this work and you do not defend it. You
never fix; you only find.

Judge ONLY against the rubric below, through the single lens you were given, plus one
standing rubric line that always applies on visual and copy lenses: the kill test (could
this exact frame, layout, or sentence appear unchanged in any other product or document?
If yes, report it as slop).

Inspect the actual evidence provided, not descriptions of it. A rubric line you could not
verify from the evidence goes INTO the findings list as "unverified: <line>"; reserve
not_checkable for rubric lines outside this lens's scope.

Coverage first, filtering never: report EVERY defect at any severity and confidence (h, m,
l) with location, rubric line, and a concrete failure description; ranking happens
downstream. An empty findings list is a strong claim: it means you actively checked every
rubric line in your lens and found nothing. It is better to surface a finding that gets
dismissed than to silently drop a real defect."""

# Inlined from fb5/references/judges.md (Judge 2). check-sync.py verifies drift.
GATE_PROMPT = """You are the final quality gate. Your power comes from a fresh context, an adversarial
stance, and the lenses below. You never fix; you judge. Two modes: in gate mode the work
has ALREADY passed rule-based verification twice, so do not re-litigate mechanical rules
unless you find a real violation the sweeps missed; in candidate-ranking mode (best-of-N,
before any sweeps) judge raw candidates without that assumption.

Run an internal panel of three lenses, in order, each producing its own findings:
1. First-time audience: does the point land in the first three seconds or first sentence?
   Where did attention skip, stall, or backtrack? What was misunderstood on first read?
2. Expert practitioner: a master of this craft reviewing a peer. Name the amateur tells
   (too-even spacing, hedged claims, borrowed structure, effects that do not argue).
   Would you sign it?
3. Brand owner: could a competitor ship this unchanged tomorrow? Does every element sound
   and look like THIS product and no other? Generic competence is a finding here.

Within every lens apply the frontier checks: momentum in prose (deflation points, endings
that trail); real-specific vs specific-sounding numbers; optical over mathematical balance
(one element dominates; two competing means neither wins); restraint (for each element, what
breaks without it? nothing = report it as removable); coherence of the whole (one hand, one
gray temperature, one register, end to end); earned emphasis (bold, color, motion spent only
at the argument's peak); load-bearing novelty (surprise must carry meaning, not costume);
rubric gaming (letter met, spirit missed).

Coverage-first from all three lenses; dedupe across lenses before reporting. The gate
verdict: fail if ANY finding would embarrass the work in front of an expert practitioner.

In distill items, each rule names its scope, exactly one, the widest that is still true:
craft file (whole domain), house overlay (this brand or team), or project memory (this
repo only)."""


def read_schemas():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "fb5", "references", "judge-schemas.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def read_text(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        return None


def build_user_message(args):
    parts = []
    rubric = read_text(args.rubric)
    if rubric is None:
        sys.exit("rubric is not readable as text: " + args.rubric)
    if args.judge == "verifier":
        parts.append("LENS: " + args.lens)
    parts.append("RUBRIC:\n" + rubric)
    skipped = []
    for path in args.evidence:
        text = read_text(path)
        if text is None:
            skipped.append(path)
            continue
        parts.append("EVIDENCE FILE " + path + ":\n" + text)
    if args.candidates:
        for i, path in enumerate(args.candidates, 1):
            text = read_text(path)
            if text is None:
                skipped.append(path)
                continue
            parts.append("CANDIDATE %d (%s):\n%s" % (i, path, text))
    if skipped:
        print("WARNING: skipped binary/unreadable evidence (report as unverified): "
              + ", ".join(skipped), file=sys.stderr)
        parts.append("NOTE: these evidence files could not be inlined and were NOT "
                     "inspected; any rubric line depending on them is unverified: "
                     + ", ".join(skipped))
    return "\n\n".join(parts)


def post(url, headers, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={**headers, "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as resp:
        return json.load(resp)


def call_anthropic(model, system, user, schema):
    body = {
        "model": model,
        "max_tokens": 8192,
        "system": system,
        "messages": [{"role": "user", "content": user}],
        "output_config": {"format": {
            "type": "json_schema",
            "schema": schema["schema"],
        }},
    }
    out = post("https://api.anthropic.com/v1/messages",
               {"x-api-key": os.environ["ANTHROPIC_API_KEY"],
                "anthropic-version": "2023-06-01"}, body)
    text = "".join(b.get("text", "") for b in out["content"] if b.get("type") == "text")
    return json.loads(text)


def call_openai(model, system, user, schema):
    body = {
        "model": model,
        "messages": [{"role": "developer", "content": system},
                     {"role": "user", "content": user}],
        "response_format": {"type": "json_schema", "json_schema": {
            "name": schema["name"], "strict": True, "schema": schema["schema"]}},
    }
    out = post("https://api.openai.com/v1/chat/completions",
               {"authorization": "Bearer " + os.environ["OPENAI_API_KEY"]}, body)
    return json.loads(out["choices"][0]["message"]["content"])


def call_gemini(model, system, user, schema):
    # Gemini's responseSchema is an OpenAPI subset: additionalProperties and some
    # keywords are unsupported, so strip to the tolerated core.
    def strip(s):
        if isinstance(s, dict):
            return {k: strip(v) for k, v in s.items()
                    if k not in ("additionalProperties", "$comment")}
        if isinstance(s, list):
            return [strip(v) for v in s]
        return s
    body = {
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {
            "temperature": 0.3,
            "responseMimeType": "application/json",
            "responseSchema": strip(schema["schema"]),
        },
    }
    url = ("https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s"
           % (model, os.environ["GEMINI_API_KEY"]))
    out = post(url, {}, body)
    cand = out["candidates"][0]
    if cand.get("finishReason") not in (None, "STOP"):
        sys.exit("gemini did not finish cleanly (finishReason=%s); rerun or rephrase"
                 % cand.get("finishReason"))
    return json.loads(cand["content"]["parts"][0]["text"])


CALLERS = {"anthropic": call_anthropic, "openai": call_openai, "gemini": call_gemini}


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--judge", choices=["verifier", "gate"], required=True)
    p.add_argument("--lens", help="required for the verifier: one rubric dimension")
    p.add_argument("--rubric", required=True, help="path to the rubric file")
    p.add_argument("--provider", choices=list(DEFAULTS))
    p.add_argument("--model")
    p.add_argument("--candidates", nargs="*", default=[],
                   help="candidate files (gate in candidate-ranking mode)")
    p.add_argument("evidence", nargs="*", help="evidence files, inlined as text")
    args = p.parse_args()

    if args.judge == "verifier" and not args.lens:
        p.error("--lens is required for the verifier")
    if args.judge == "verifier" and not args.evidence:
        p.error("the verifier needs evidence files")

    provider = args.provider or next(
        (name for name, env in ENV_KEYS.items() if os.environ.get(env)), None)
    if not provider:
        sys.exit("no API key found; set one of: " + ", ".join(ENV_KEYS.values()))
    if not os.environ.get(ENV_KEYS[provider]):
        sys.exit("missing " + ENV_KEYS[provider])

    model = args.model or DEFAULTS[provider]
    schemas = read_schemas()
    schema = schemas["verifier" if args.judge == "verifier" else "taste_gate"]
    system = VERIFIER_PROMPT if args.judge == "verifier" else GATE_PROMPT
    user = build_user_message(args)

    result = CALLERS[provider](model, system, user, schema)
    print(json.dumps(result, indent=2))

    if args.judge == "verifier":
        sys.exit(1 if result.get("findings") else 0)
    sys.exit(0 if result.get("gate") == "pass" else 1)


if __name__ == "__main__":
    main()
