#!/usr/bin/env python3
"""A/B eval: bare task vs task + protocol, scored by a fresh-eyes judge. See evals/README.md.

Stdlib only. Providers and the judge come from scripts/judge.py (same auth, same schemas).
"""

import argparse
import importlib.util
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

spec = importlib.util.spec_from_file_location(
    "judge", os.path.join(ROOT, "scripts", "judge.py"))
judge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(judge)


def provider_of(model):
    if model.startswith("claude"):
        return "anthropic"
    if model.startswith(("gpt", "o1", "o3", "o4")):
        return "openai"
    if model.startswith("gemini"):
        return "gemini"
    sys.exit("cannot infer provider from model id: " + model)


def generate(model, prompt):
    provider = provider_of(model)
    if provider == "anthropic":
        out = judge.post("https://api.anthropic.com/v1/messages",
                         {"x-api-key": os.environ["ANTHROPIC_API_KEY"],
                          "anthropic-version": "2023-06-01"},
                         {"model": model, "max_tokens": 16000,
                          "messages": [{"role": "user", "content": prompt}]})
        return "".join(b.get("text", "") for b in out["content"]
                       if b.get("type") == "text")
    if provider == "openai":
        out = judge.post("https://api.openai.com/v1/chat/completions",
                         {"authorization": "Bearer " + os.environ["OPENAI_API_KEY"]},
                         {"model": model,
                          "messages": [{"role": "user", "content": prompt}]})
        return out["choices"][0]["message"]["content"]
    out = judge.post(
        "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s"
        % (model, os.environ["GEMINI_API_KEY"]), {},
        {"contents": [{"role": "user", "parts": [{"text": prompt}]}]})
    cand = out["candidates"][0]
    if cand.get("finishReason") not in (None, "STOP"):
        raise RuntimeError("finishReason=" + str(cand.get("finishReason")))
    return "".join(p.get("text", "") for p in cand["content"]["parts"])


def parse_task(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    domain = text.split("DOMAIN:", 1)[1].split("\n", 1)[0].strip()
    task = text.split("TASK:", 1)[1].split("RUBRIC:", 1)[0].strip()
    rubric = text.split("RUBRIC:", 1)[1].strip()
    return domain, task, rubric


def score(judge_model, rubric, output_text):
    """One whole-rubric verifier pass; returns the parsed verdict."""
    schemas = judge.read_schemas()
    system = judge.VERIFIER_PROMPT
    user = ("LENS: whole rubric\n\nRUBRIC:\n" + rubric
            + "\n\nEVIDENCE (the deliverable under judgment):\n" + output_text)
    caller = judge.CALLERS[provider_of(judge_model)]
    return caller(judge_model, system, user, schemas["verifier"])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tasks", nargs="*",
                   help="task names (files in evals/tasks/ without .md); default all")
    p.add_argument("--models", nargs="*",
                   help="producer model ids; default one per provider with a key set")
    p.add_argument("--judge-model", default="claude-opus-4-8")
    p.add_argument("--seeds", type=int, default=1,
                   help="repeats per combo; deltas under seed variance mean nothing")
    args = p.parse_args()

    task_dir = os.path.join(HERE, "tasks")
    names = args.tasks or sorted(
        f[:-3] for f in os.listdir(task_dir) if f.endswith(".md"))
    models = args.models or [m for env, m in
                             [("ANTHROPIC_API_KEY", "claude-sonnet-5"),
                              ("OPENAI_API_KEY", "gpt-5"),
                              ("GEMINI_API_KEY", "gemini-2.5-pro")]
                             if os.environ.get(env)]
    if not models:
        sys.exit("no provider keys set; see evals/README.md")
    if not os.environ.get(judge.ENV_KEYS[provider_of(args.judge_model)]):
        sys.exit("judge model %s needs %s set"
                 % (args.judge_model, judge.ENV_KEYS[provider_of(args.judge_model)]))

    out_dir = os.path.join(HERE, "results", time.strftime("%Y%m%d-%H%M%S"))
    os.makedirs(out_dir)
    rows = []

    for name in names:
        domain, task, rubric = parse_task(os.path.join(task_dir, name + ".md"))
        dist_path = os.path.join(ROOT, "dist", "frontier-%s.md" % domain)
        if not os.path.isfile(dist_path):
            sys.exit("missing %s; run: node scripts/build-dist.mjs" % dist_path)
        with open(dist_path, encoding="utf-8") as f:
            protocol_prefix = f.read()
        conditions = {"bare": task, "protocol": protocol_prefix + "\n\n" + task}

        for model in models:
            for cond, prompt in conditions.items():
                for seed in range(args.seeds):
                    tag = "%s.%s.%s.s%d" % (name, model, cond, seed)
                    print("running " + tag, file=sys.stderr)
                    try:
                        output = generate(model, prompt)
                    except Exception as e:  # a failed combo is a result, not a crash
                        rows.append((name, model, cond, seed, "GEN ERROR: %s" % e))
                        continue
                    with open(os.path.join(out_dir, tag + ".out.md"), "w",
                              encoding="utf-8") as f:
                        f.write(output)
                    try:
                        verdict = score(args.judge_model, rubric, output)
                    except Exception as e:
                        rows.append((name, model, cond, seed, "JUDGE ERROR: %s" % e))
                        continue
                    with open(os.path.join(out_dir, tag + ".verdict.json"), "w",
                              encoding="utf-8") as f:
                        json.dump(verdict, f, indent=2)
                    counts = {"h": 0, "m": 0, "l": 0}
                    for finding in verdict.get("findings", []):
                        counts[finding.get("confidence", "l")] += 1
                    rows.append((name, model, cond, seed,
                                 "h:%d m:%d l:%d" % (counts["h"], counts["m"], counts["l"])))

    lines = ["# Eval run " + os.path.basename(out_dir),
             "",
             "Judge: %s. Findings per output (fewer is better); compare bare vs protocol"
             " within the same task+model only." % args.judge_model,
             "",
             "| task | model | condition | seed | findings |",
             "|---|---|---|---|---|"]
    for r in rows:
        lines.append("| %s | %s | %s | %d | %s |" % r)
    summary = "\n".join(lines) + "\n"
    with open(os.path.join(out_dir, "summary.md"), "w", encoding="utf-8") as f:
        f.write(summary)
    print(summary)
    print("results in " + out_dir, file=sys.stderr)


if __name__ == "__main__":
    main()
