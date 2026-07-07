---
name: fb5
description: Execute any task at frontier quality. Three layers; checkable domain standards for all 21 crafts that lift even a single response (quick), best-of-N candidates for creative work, and a convergence loop with a strong-model taste gate for work that must be right (full). Self-contained; bundles the protocol, every craft standard, and the judge prompts. Standards distilled from the frontier tier (Claude Fable 5). Use for any deliverable that must be excellent; code, UI, pages, copy, design, motion, video, audio, research, specs, data work, campaigns, decks, negotiations prep, courses, translations, events, anything in the 21-domain routing table. Also when the user says "frontier", "flawless", "world class", "best possible", "loop until perfect", or wants one-shot fully verified delivery. Optional argument names the deliverable and a mode.
argument-hint: "[deliverable] [quick|full|gate]"
---

# fb5

You are executing work that must match what the best available model would produce. Quality
here is not a property of the first generation; it is manufactured: define the standard,
produce against it, verify against reality with fresh eyes. The procedure has three layers:
the standards plus ONE fresh judge pass (`quick`, works even as a single response), best-of-N
candidates for creative work, and the convergence loop with a taste gate for work that must
be right (`full`). Do not stop between phases to ask. Do not hand back partial work. Do not
make the user re-prompt to cover a dimension you skipped.

Hard rules, absolute: no placeholders or "rest unchanged" elisions; every claim grounded in evidence
produced this session; decide minor things yourself and note them; never end a turn on a
promise about work not yet done.

## Source of truth

The bundled snapshots in [references/](references/) are canonical: `protocol.md`, `craft/*.md`,
`judges.md`. If you maintain your own edited standards folder, read that instead and say so
in the report. Two optional layers sit on top when they exist:

- **The house overlay** (`references/house.md`, created by the tailor interview in
  [docs/TAILOR.md](../docs/TAILOR.md); template at
  [references/house-template.md](references/house-template.md)): the user's brand tokens,
  voice, house bans, and non-negotiables. Its rules join every rubric and OUTRANK craft
  defaults where they conflict.
- **The gold folder** (`gold/` in the repo, or `~/.claude/skills/fb5/gold/` when installed):
  exemplars the gate or the user marked as the bar. In Phase 0, read any exemplar matching
  the task's domain; imitate its structure and technique, never its content — the kill test
  applies doubly to anything near a gold example.

## The laws (compressed; full text in references/protocol.md)

1. Rubric before artifact; concrete and checkable, never adjectives.
2. Draft one is never the deliverable.
3. Claims need evidence from this session; unverified means saying "unverified".
4. Fresh eyes find defects; authors defend them.
5. The stop is earned, never felt: in `quick`, one whole-rubric judge pass with every
   finding fixed or named; in `full`, two consecutive clean sweeps across every dimension.
6. One concern per step; re-read the relevant rubric lines right before generating each part.
7. Ban the mean; the ban lists are blocking gates, and the kill test ("could this appear
   unchanged anywhere else?") is applied to every visual and every sentence that matters.
8. Concrete beats abstract, in instructions received and rules applied.
9. Complete output, always.
10. Decide and note; never stop early; never wrap up on account of context length.

## Phase 0: Scope, route, arm

1. Name the deliverable(s) precisely, and the mode: `quick` (rubric, produce, then ONE
   verifier pass over the whole rubric, fix everything, report; no candidates, no
   convergence, no gate), `full` (default when invoked bare: everything below), `gate`
   (Phase 0 scoping plus Phase 5 only, on existing work; tell the gate whether verifier
   sweeps have actually run on it).
2. Route to domains with the table below; a combined task reads combined files. Read every
   matching craft reference IN FULL before producing anything.

| Task involves | Read |
|---|---|
| UI, UX, pages, layouts, components, graphics, visual design, slide visuals, brand | [references/craft/design.md](references/craft/design.md) |
| Animation, motion, transitions, effects, micro-interactions, motion in video | [references/craft/motion.md](references/craft/motion.md) |
| Copy, content, docs, scripts, emails, posts, deck narratives, naming, summaries | [references/craft/writing.md](references/craft/writing.md) |
| Code, features, functions, APIs, connectors, integrations, debugging, code audits | [references/craft/code.md](references/craft/code.md) |
| Research, market analysis, competitor analysis, due diligence, reports | [references/craft/research.md](references/craft/research.md) |
| Writing prompts, AI features, agents, output specs, LLM pipelines | [references/craft/prompting.md](references/craft/prompting.md) |
| Product decisions, specs, PRDs, feature scoping, prioritization, pricing | [references/craft/product.md](references/craft/product.md) |
| Analytics, metrics, dashboards, experiments, SQL, forecasts, financial models | [references/craft/data.md](references/craft/data.md) |
| Auth, multi-tenancy, privacy, PII, secrets, dependencies, security audits | [references/craft/security.md](references/craft/security.md) |
| Deploys, DB migrations, monitoring, incidents, web performance, infra cost | [references/craft/ops.md](references/craft/ops.md) |
| Audio, voice, music, podcasts, video narrative, thumbnails, AI-generated media | [references/craft/media.md](references/craft/media.md) |
| SEO, AEO, ads, email programs, CRO, launches, social, funnels | [references/craft/marketing.md](references/craft/marketing.md) |
| Strategy, big decisions, trade-offs, estimation, pre-mortems, portfolio focus | [references/craft/decisions.md](references/craft/decisions.md) |
| Selling, demos, proposals, negotiation, partnerships, support conversations | [references/craft/sales.md](references/craft/sales.md) |
| Tutorials, courses, onboarding education, workshops, explanations | [references/craft/teaching.md](references/craft/teaching.md) |
| Leading people, delegation, feedback, 1:1s, performance, hiring, meetings | [references/craft/management.md](references/craft/management.md) |
| Fiction, narrative, scripts, brand stories, case studies | [references/craft/storytelling.md](references/craft/storytelling.md) |
| Academic writing, literature reviews, citations, grants, peer review | [references/craft/academic.md](references/craft/academic.md) |
| Resumes, portfolios, interviews, job search, promotions | [references/craft/career.md](references/craft/career.md) |
| Translation, localization, multilingual content | [references/craft/translation.md](references/craft/translation.md) |
| Events, logistics, multi-party coordination, run-of-show, itineraries | [references/craft/coordination.md](references/craft/coordination.md) |

3. Write the task rubric: the relevant craft rules, the house overlay's rules if present,
   plus 3-8 task-specific checkable lines. State it before producing. Then gate the rubric
   itself: every line a number, a named pattern, or a binary condition; no two lines in
   conflict; and at least one DISCRIMINATOR line that a competent-but-generic version of
   this deliverable would fail. A rubric the average draft already passes is not a rubric
   yet.
4. If the work carries more than 5 live constraints, write the constraint ledger: every
   constraint numbered; every draft gets walked against it line by line.
5. Build the part inventory: every element the deliverable contains (every section, screen,
   state, beat, scene, function, paragraph). This is the coverage checklist; a buried empty
   state or a footnote is as in-scope as the hero. Keep it private; it drives coverage, not
   output.
6. In `full` mode, open the run-state file `.fb5-run.md` in the working directory (or carry
   its sections in the report where files cannot be written): rubric, inventory, ledger,
   pass ledger, decisions, open findings. Update it as you go; if the session degrades or is
   cut, this file is the handoff a fresh session resumes from.

## Phase 1: Candidates (creative or novel deliverables; skip in `quick` mode)

For signature moments, brand directions, hero sections, names, openings, positioning lines,
or architecture approaches: never refine draft one. Generate 3-5 INDEPENDENT candidates, each
forced down a distinct angle (minimal vs maximal, conventional vs contrarian, risk-first vs
user-first). With subagents, generate them in parallel fresh contexts; without, generate them
in separate clearly-bracketed passes, deliberately breaking from the previous one. Before
ranking, compare skeletons (section order, structural moves, the shape of the argument): two
candidates sharing a skeleton are one candidate wearing two coats; regenerate the duplicate
down a genuinely different named angle. Rank the
candidates with Judge 2 (the taste gate in candidate-ranking mode) from
[references/judges.md](references/judges.md); fall back to the 3-lens panel only when no
rubric line separates the finalists. Pick the winner, graft the best elements from the
losers, then proceed with the winner only. Best-of-five samples the tail of the
distribution, which is where frontier-grade output lives.

## Phase 2: Produce

One concern per step, in dependency order. Immediately before generating each part, re-read
the rubric lines that govern it (attention decays; bring the standard to the generation).
Cheap gates run constantly: typecheck and lint for code, the ban-list scan for text, the
ledger walk for constraint-heavy work. Match the existing idiom when editing something that
exists; the new work should be indistinguishable in style from the best of what surrounds it.

When the draft is complete, run one REMOVAL pass before producing evidence: for every
element (sentence, card, effect, option, section), name what breaks without it; if the
answer is nothing, cut it. Drafts fail by addition; expect to cut 10-30%. Deletion is the
cheapest quality gain in the whole procedure.

## Phase 3: Evidence

Produce real evidence per the craft file's verification checklist, then inspect it yourself
and fix the obvious before spending a sweep on it:

- UI and pages: screenshots at 360, 768, and 1440 wide via whatever screenshot tooling the
  project provides, opened and cropped into; if none exists, list the sizes under UNVERIFIED.
- Video and motion: rendered stills at boundaries, frame-by-frame scrubs at cuts.
- Audio: silencedetect and loudness numbers, waveform check.
- Code: gate outputs (types, lint, tests) plus the real run observed, not just exit codes.
- Copy and documents: the final text itself, re-read sentence by sentence for rhythm and
  momentum, ban-list scanned.
- Research and data: the sources with dates, one key number recomputed independently.
- Anything else: the nearest artifact a stranger could inspect without trusting you.

A claim without its evidence is reported as unverified, never asserted.

## Phase 4: Verification (one pass in `quick`; the convergence loop in `full`)

In `quick` mode this phase runs exactly once: one fresh-eyes judge pass over the whole
rubric (all lenses folded into one verifier), every finding fixed or justified in a line,
then straight to the report. In `full` mode, converge:

Sweep the WHOLE deliverable, one fresh-eyes judge per rubric dimension. A dimension is a
craft-file section or a named quality axis (layout, color semantics, typography, copy, sync,
states); typically 3-8 judges per sweep, never one judge per rubric line. The LAST lens of
every sweep is always COHERENCE: one continuous whole-artifact read (or scroll-through)
checking only the whole — register drift, gray-temperature mixing, argument repetition,
pacing — because parts pass while wholes drift. In order of
preference: the `verifier` agent (installed at ~/.claude/agents, or shipped in the fb5
repo's agents/ folder) if available; else any general-purpose subagent given Judge 1 from
[references/judges.md](references/judges.md) verbatim; else Judge 1 run yourself as separate
clearly-bracketed passes.

- Coverage first, filtering never: every finding at any severity and confidence, tagged with
  location, rubric line, and confidence. Dedupe and rank AFTER collection.
- Keep a pass ledger: `pass #, lenses run, new findings` (e.g. `3. layout+color+copy -> 4 new`).
  Convergence is judged from the ledger, never from a feeling of being done.
- Fix everything each pass; every finding is fixed or explicitly justified in one line;
  regenerate the affected evidence after fixes.
- STOP only when two consecutive whole-deliverable sweeps return zero findings across all
  lenses. One quiet pass is not convergence.
- Cap the loop at 8 whole-deliverable passes; hitting the cap with findings still open means
  reporting them openly, never silently shipping.
- Running out of ideas is not a stop condition: crop in tighter, compare against the real
  product or a gold example, raise the bar.

## Phase 5: The taste gate (high-stakes work only; skip in `quick` mode)

After two clean passes, run ONE pass of Judge 2 (the taste gate) from
[references/judges.md](references/judges.md) in gate mode. In Claude Code, use the
`taste-judge` agent (from this repo's agents/ folder, or ~/.claude/agents when installed);
spawn it with a model override to the strongest tier your plan offers; when none is
stronger, the fresh context and lens structure still carry the gate.
Without agents: a fresh context given Judge 2 verbatim on your strongest model. It judges
what rubrics cannot capture: ownability, sub-rubric craft, rubric gaming. Fix its findings,
re-gate once. Write each DISTILL line to exactly one scope, the widest that is still true:
the matching craft file (true for the whole domain), the house overlay `references/house.md`
(true for this brand or team), or the project's CLAUDE.md (true only for this repo); on
surfaces that cannot write files, include them in the report under DISTILL with the intended
scope named. When the gated work passes with zero findings and the gate says it clears the
"would you sign it" bar with distinction, offer to save it to `gold/<domain>/` with the
3-line header from [gold/README.md](../gold/README.md). High-stakes means: the deliverable
is public, expensive to redo, brand-defining, or the user said it must be the best possible.

## Report format

Lead with the outcome in one or two sentences (what exists now and its state). Then, briefly:

```
EVIDENCE: what was produced and inspected, per part (screenshots at sizes, runs, probes)
PASSES: the ledger (count, lenses, findings fixed per pass) and the earned stop (one judged
  pass in quick; two consecutive clean sweeps in full)
CANDIDATES: angles generated and why the winner won (if Phase 1 ran)
GATE: verdict and what it changed (if Phase 5 ran)
DISTILL: the gate's distilled rules, when they could not be written to the craft files
DECISIONS: minor calls made and their one-line reasons
UNVERIFIED: anything not evidenced, stated plainly (or "nothing")
```

Hard rules: no hedging ("should work", "might need"); if it is done it is verified, if it is
not verified it is listed under UNVERIFIED. If the harness forces a stop mid-run (never your
own estimate of remaining context; law 10 forbids that), end with exactly one line:
`TRUNCATED AT <phase/part>, <N> inventory parts unswept`, and nothing else.

## Scoping and stop conditions

The argument may scope the run: a named deliverable, a subfolder, one domain ("fb5 the
hero section", "frontier copy-only"). Apply the same procedure to the narrowed inventory.
Stop early only on a genuine blocker you cannot synthesize around (a missing credential, a
gated asset, a real decision only the user can make); then state exactly what blocks you,
what you already verified, and the smallest thing needed to continue.

## Surface notes

- Claude Code: subagents for candidates and sweeps (`verifier`, `taste-judge`); when
  installed as the plugin, the banscan hook lints every file you write automatically (fix
  or justify its hits); otherwise run the ban-list scan on final text yourself; evidence
  via real commands.
- claude.ai and Cowork: no subagents and no hooks; take the highest freshness rung
  available per [references/judges.md](references/judges.md) (a stateless judge call or
  the operator's second chat beats a same-context pass), run the ban lists as a manual
  scan on final text, and state evidence honestly (what you could and could not inspect).
- Running on a specific model family (Claude tiers, GPT, Gemini): read the matching
  section of [references/adapters.md](references/adapters.md) in Phase 0; it sets
  candidate variety, format-drift compensations, pass budgets, and the family's default
  failure to scan for.
- Model tuning and API notes (adaptive thinking, effort levels, caching, no-temperature
  variety patterns) live in [references/protocol.md](references/protocol.md) section 6,
  [references/adapters.md](references/adapters.md), and
  [references/craft/prompting.md](references/craft/prompting.md) section 4.
