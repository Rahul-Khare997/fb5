# Changelog

## 1.2.0 (2026-07-07)

The cross-model release: the "works on GPT and Gemini too" claim gets its levers, its
gates, and its measurement harness.

- `references/adapters.md`: per-family setup for Claude (Opus/Sonnet/Haiku), GPT-5.x and
  o-series, and Gemini: message placement, candidate variety with and without sampling
  params, each family's default failure (Claude cream-and-serif taste, GPT hedging, Gemini
  output compression and template drift) with standing compensations, pass budgets per
  tier, cross-family judging. Protocol section 6 and prompting.md section 4 now route to
  it; PROMPT.md carries the three per-model lines inline.
- Fresh eyes anywhere: `scripts/judge.py` runs both judges as stateless API calls
  (Anthropic, OpenAI, Gemini; stdlib only) with schema-enforced output
  (`references/judge-schemas.json`); judges.md now ranks the freshness ladder explicitly
  (stateless call > operator's second chat > same-context bracketed pass).
- Mechanical ban-list gate: `scripts/banscan.py` (files, stdin, or hook mode) plus
  `hooks/hooks.json`, so the plugin scans every file the model writes and feeds hits back
  in-turn. Law 7 enforced, not requested.
- Eval harness (`evals/`): A/B per task (bare vs protocol), scored by a fresh verifier on
  a strong judge model, across providers; six tasks covering writing, code, design,
  research, product, prompting. No results published yet; the README labels the
  cross-model claim an estimate until the table exists.
- `dist/` one-paste bundles per domain (PROMPT.md + craft standard merged, task slot
  last), built by `scripts/build-dist.mjs`; `PROMPT-quick.md` compact variant for weaker
  models and short tasks.
- CI (`.github/workflows/ci.yml`): judge-encoding sync guard (`scripts/check-sync.py`),
  dist freshness, banscan self-test, script compilation, skill-zip freshness.

## 1.1.1 (2026-07-04)

- Positioning: names the target models (Opus, Sonnet, GPT, Gemini) and the Fable 5
  provenance across the pitch surfaces; social card subline updated.

## 1.1.0 (2026-07-03)

The distillation release: the standards were adversarially audited and upgraded by Claude
Fable 5 (frontier tier) in the final days of its general access.

- All 21 craft files upgraded (about 260 documented change entries): vague lines converted to numbers, letter-vs-
  spirit loopholes closed, ban lists extended with the model's own named generation tells
  (machine-cadence prose tics, default design habits, hedge-everything analysis, fiction
  cliches, MT register defaults).
- Judge prompts unified into one parseable format across judges.md, both agents, and
  PROMPT.md, after a 42-finding prompt-engineering review; portable Judge 2 upgraded to the
  full 3-lens taste gate with mandatory DISTILL output.
- `taste-judge` agent added (3-lens panel plus frontier checks: momentum, restraint, optical
  balance, coherence, earned emphasis, rubric-gaming); runs on any model tier.
- Protocol gained section 4c, "Lessons from the frontier window": inertness is the gap not
  incorrectness, deletion is the strongest edit, endings deflate, parts pass while wholes
  drift, every rule needs a spirit check.
- Two operating forms: a single-response default (the standards plus one mandatory judge
  pass, the shape PROMPT.md ships) and a `full` convergence mode for work that must be
  right, bounded by a hard 8-pass cap with anything still open reported rather than
  silently shipped.
- Launch documentation: rebuilt README, docs/ (how it works, install, customizing), a full
  sample run transcript, contribution templates with the rule bar.

## 1.0.0 (2026-07-02)

Initial release.

- The Operating Protocol: ten laws, the convergence loop, weaker-model compensations, and
  four ceiling raisers (tail sampling, constraint ledger, strong-model gate, taste
  distillation).
- 21 craft standards, each with concrete numbers, a ban list, and a verification checklist:
  design, motion, writing, code, research, prompting, product, data, security, ops, media,
  marketing, decisions, sales, teaching, management, storytelling, academic, career,
  translation, coordination.
- Portable judge prompts (fresh-eyes verifier, taste gate, 3-lens panel) for surfaces
  without subagents.
- Phased SKILL.md procedure with modes (quick, full, gate), a part-inventory coverage rule,
  a pass ledger, and a two-consecutive-clean-passes stop condition.
- PROMPT.md single-file version for use in any capable agent outside Claude Code.
- A ready-made upload zip for claude.ai custom skills.
