# Making fb5 yours

The standards ship strong, but the system is designed around one loop: your taste, written
down, compounds. This page covers the three ways to feed it and the rules that keep the
files sharp.

## 1. Harvest DISTILL lines (the built-in flywheel)

Every taste-gate run ends with DISTILL lines: taste judgments converted into candidate
rules, like:

```
DISTILL:
- writing.md ban list candidate: headlines that ask the question the body answers
  ("What if deploys were instant?") -> assert the capability instead
```

Review them after each high-stakes run. Each rule names its scope; append the ones you
agree with at that scope, exactly one, the widest that is still true: the matching file in
`fb5/references/craft/` (true for the whole domain), `fb5/references/house.md` (true for
your brand or team), or the project's CLAUDE.md (true only for that repo). Scoped wrong,
one team's taste bloats the universal standards. Date-stamp what you append
(`<!-- 2026-07-07, gate run on pricing page -->`) so stale taste is findable later.
Discard the rest; the gate proposes, you decide.

## 2. Add rules from observed failures

Caught the model doing something the files miss, twice? That is a rule. The contribution
bar (same for your fork as for PRs here):

- **Sourced from a real failure**, not theory. The best rules name the exact failure ("the
  drop in the last week is an incomplete week").
- **Checkable**: a verifier reading the rule can mark work pass or fail. "Be more careful
  with joins" is not a rule; "row counts at each join step" is.
- **Placed with its family**: rules go in the file's numbered sections, machine tells go in
  the ban list WITH a replacement (never a bare "don't"), checks go in the verification
  checklist.
- **One statement, once**: if a rule needs restating for emphasis, it needs rewriting for
  clarity. Conflicting rules: delete the loser, never stack a third rule to arbitrate.
- **Style**: keep each file under ~190 lines (deletion of weak lines is always welcome),
  and match the file's voice.

## 3. The house overlay and the gold library

- The craft files are deliberate defaults for when no brand exists. Your real standards
  live in `fb5/references/house.md`: brand tokens, voice, house bans, non-negotiables.
  Phase 0 folds it into every rubric, and it outranks craft defaults where they conflict.
  Do not write it by hand cold: run the one-paste tailor interview in
  [TAILOR.md](TAILOR.md), which interviews you and writes it (template:
  `fb5/references/house-template.md`).
- Gold examples outperform rules for anchoring taste: work the gate passed with
  distinction, or past pieces the team holds up as the bar, live in `gold/<domain>/` with
  the 3-line IMITATE / IGNORE / ADDED header ([gold/README.md](../gold/README.md) has the
  format and the garden rules). Phase 0 reads the matching exemplar and imitates its
  structure, never its content. Imitation of a known-excellent skeleton is the single
  cheapest quality lift available.

## Editing the judges

`fb5/references/judges.md` is the canonical judge source; `agents/verifier.md`,
`agents/taste-judge.md`, and the judge blocks in `PROMPT.md` are encodings of it. If you
edit one, sync all four, and keep the output formats byte-compatible (fixed field counts,
h/m/l confidence tokens, NONE for empty): downstream steps parse them.

## Structural invariants (do not break these)

1. Every craft file keeps: numbered rule sections, a ban list with replacements, a
   verification checklist. The loop depends on all three existing.
2. The routing table in SKILL.md maps every craft file exactly once.
3. `quick|full|gate` mode semantics stay stable; scripts and habits build on them.
4. The 8-pass hard cap stays: it is the operator's brake on token spend.
5. Judge outputs stay parseable (see above).

