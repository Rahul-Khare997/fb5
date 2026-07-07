# Model adapters: running the protocol on each model family

The protocol is model-agnostic; the levers are not. This file maps each family's knobs to
the phases that need them: candidate variety (Phase 1), format discipline (Phases 4-5),
pass budgets, judge freshness, and API mechanics. Read the section for the model you are
running BEFORE Phase 0. API details current as of 2026-07; verify against live docs when
building, and treat a mismatch as the docs winning.

The one rule that outranks everything here: the protocol text and craft file go FIRST
(system or developer role where one exists), the task goes LAST. Every family weights the
end of the prompt; every family with caching caches the stable prefix.

---

## 1. Claude Opus 4.8 / Sonnet 5 / Haiku 4.5 (Anthropic)

- Message placement: protocol + craft file in the system prompt; task in the user turn.
- Variety for best-of-N: no temperature, top_p, or top_k on Opus 4.7+ and Sonnet 5 (they
  400). Force variety through the prompt: each candidate gets a distinct named angle and an
  explicit instruction to break from the previous structure. Fresh contexts (subagents or
  separate calls) per candidate; same-context "now do another" converges.
- Effort: `thinking: {type: "adaptive"}` plus `output_config.effort`: `high` default,
  `xhigh` for the hardest reasoning, `low` for mechanical judge passes on small scopes.
- Structured outputs via `output_config.format` with a JSON schema (never prefills; they
  400). Judge runs should use [judge-schemas.json](judge-schemas.json).
- Caching: stable prefix first, verify `usage.cache_read_input_tokens > 0`; a timestamp in
  the system prompt silently kills it.
- Instruction style: literal. Scope must be stated ("every section, not just the first").
  Coverage-first reporting must be explicit or recall drops (protocol section 6).
- Pass budgets: Opus 2-3 sweeps typical; Sonnet 3-4; Haiku is a gate-runner and ban-scanner,
  not a producer of frontier work: use it for mechanical lenses only.
- Default-taste warning (all Claude tiers): cream/off-white around #F4F1EA, serif display,
  terracotta accents, Inter everywhere. Concrete hex values and named fonts in the rubric
  override it; "don't use cream" just shifts the default.

## 2. GPT-5.x and o-series (OpenAI)

- Message placement: protocol + craft file in the `developer` (or `system`) message; the
  Responses API is the current surface, Chat Completions still works. Task in the user turn.
- Variety for best-of-N: reasoning models ignore or reject `temperature`; force variety
  through named angles exactly as on Claude. Non-reasoning tiers accept `temperature` /
  `top_p`: for candidates, temperature 0.9-1.1 across parallel calls PLUS distinct angles
  beats either alone; drop back to default for produce and judge passes. Never sample
  variety on a judge.
- Effort: `reasoning: {effort: "high"}` for produce and gate passes, `"medium"` or
  `"low"` for mechanical lenses.
- Format discipline: good schema adherence via structured outputs (`response_format` /
  `text.format` json_schema with `strict: true`); use it for judges instead of trusting the
  prose template. In plain chat (no API), GPT drifts on "Return exactly this shape" after
  long outputs: restate the template at the END of the judge prompt, and reject-and-rerun
  any judge output that breaks shape rather than repairing it yourself.
- Instruction hierarchy: developer message reliably outranks user content; put the hard
  rules (no placeholders, coverage-first) there. GPT generalizes scope more than Claude but
  hedges more: the ban list's hedging category earns its keep here; scan for it explicitly.
- Caching: automatic prefix caching; same rule, stable prefix first.
- Pass budgets: flagship tiers 2-3 sweeps; mini tiers 3-4 with smaller sweep scopes.

## 3. Gemini 2.5 / 3 (Google)

- Message placement: protocol + craft file in `systemInstruction`; task in `contents`.
- Variety for best-of-N: `temperature` available on all tiers (default 1.0); candidates at
  temperature 1.1-1.3 with named angles, produce and judge passes at 0.2-0.4. Thinking
  tiers: set the thinking budget high for produce/gate, low for mechanical lenses.
- Known failure shapes to compensate (each is a standing check, not a maybe):
  - **Output compression.** On long deliverables Gemini summarizes the tail ("...and
    similar for the remaining sections"). That violates Law 9 (complete output, always).
    Split production per part-inventory item and demand each part complete; never ask for
    the whole deliverable in one generation above ~2k output tokens.
  - **Template drift.** "Return exactly this shape" decays fastest of the three families.
    Give judges the one-line filled example AND the empty template, restate the template
    last, and use `responseSchema` (structured output) on API calls; reject-and-rerun on
    drift.
  - **Instruction decay over long context.** Re-anchoring (Law 6: re-read rubric lines
    before each part) is mandatory, not advisory: paste the governing rubric lines into
    the request for each part rather than referring back to them.
- Safety filters can silently truncate or block mid-generation on ordinary content
  (violence in fiction, security topics in audits): check `finishReason` on every call;
  `SAFETY` or truncation means regenerate with rephrased framing, never accept the stub.
- Caching: context caching is explicit (cachedContent); worth it when the protocol + craft
  prefix is reused across many calls in one run.
- Pass budgets: Pro tiers 3 sweeps typical; Flash tiers 4, with sweep scopes a judge can
  hold (one screen, one section, one function group).

## 4. Any chat surface, any family (no API access)

- The two-chat protocol from [judges.md](judges.md) is the single highest-value adaptation:
  judges run in a NEW chat that has never seen the producing conversation. Same-context
  bracketed passes are the fallback, not the method.
- Paste order per chat: protocol (or PROMPT.md) first, craft file second, task last.
- Candidates: separate regenerations (or separate chats) per angle; never "give me five
  options" in one message: the five converge on one skeleton with cosmetic swaps.
- The ban-list scan is manual here: run [scripts/banscan.py](../../scripts/banscan.py)
  locally on the final text, or walk the craft file's ban list line by line against the
  output as its own bracketed pass.

## 5. Choosing the judge model

Judgment costs a fraction of generation: run judges on the strongest model you can reach
even when producing on a cheaper one. Cross-family judging works and removes shared
blind spots: a Claude producer judged by a GPT verifier (or the reverse) catches
family-default taste (section 1's cream/serif default; GPT's hedging; Gemini's compression)
that a same-family judge inherits. The taste gate (Judge 2) should be the strongest model
available to you, whatever family it is from; the verifier (Judge 1) can run on a mid tier
if its sweep scope is small.
