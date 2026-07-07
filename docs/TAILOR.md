# The tailor interview: make fb5 yours

The craft standards define excellent in general. Your team's excellent is narrower: your
tokens, your voice, your bans, your bar. This one-paste prompt has the model interview you
and write the house overlay (`fb5/references/house.md`) that every future run folds into
its rubric. Run it once per team or brand, with the smartest model you have; revisit it
when the brand does.

Paste this into Claude Code at the repo root (or any chat that can read the repo):

```
Set up my fb5 house overlay — the standing standards every fb5 run will fold
into its rubric, outranking the craft defaults where they conflict.

1. Read fb5/references/house-template.md (the shape) and skim one or two of
   the craft files in fb5/references/craft/ (the bar the overlay sits on).
   Then look at whatever real work of mine you can reach: this repo, linked
   sites, documents I attach.

2. Interview me, one question at a time. No fixed count — each question must
   earn its place, build on what I already said, and stop as soon as another
   answer would not change what you write. Work out: what we make and for
   whom; the visual tokens if any (exact hex, named faces, the grid); the
   voice (register, owned words, banned words); the non-negotiables (what
   must always and never be true); and 1-3 past pieces that set the bar. If
   I say "just set it up", stop asking, use what you inferred, and flag
   every assumption at the end.

3. Write fb5/references/house.md from the template: keep only sections I
   have opinions on, every line a number, a named pattern, or a binary
   condition, nothing the craft files already say, under 60 lines. If I
   named past pieces that set the bar, save each to gold/<domain>/ with the
   3-line header from gold/README.md.

4. Show me the finished file, tell me what you deliberately left out and
   why, and then run one small fb5 task that would have come out generic
   before the overlay existed — so I can see the difference immediately.
```

On a surface that cannot write files: same prompt, but ask for the finished `house.md` as
a block to save by hand, and keep it pasted after the craft file in future runs.

Maintenance is the same garden rule as everything else in the kit: the gate's DISTILL
lines scoped "house" get appended here; a rule the team keeps overriding gets deleted.
Date-stamp additions (`<!-- 2026-07-07, from gate run on pricing page -->`) so stale taste
is findable later.
