# Evals: does the protocol actually close the gap?

The kit's own Law 3 applies to the kit: "these standards hold any model close to the
frontier bar" is a claim, and claims need evidence. This harness produces it: each task
runs twice per model (bare task vs task + the merged protocol file from `dist/`), every
output is scored by a fresh-eyes verifier on a strong judge model against the task's
rubric, and the deltas land in a table you can read and rerun.

What it measures: rubric findings per output (fewer is better), split by confidence. What
it cannot measure: taste beyond the rubric; add a Judge 2 gate pass manually on finalists
when you care. A/B on the same judge, same rubric, same task keeps the comparison honest;
absolute scores mean nothing across tasks.

## Run

```
export ANTHROPIC_API_KEY=...   # judge (and Claude producers)
export OPENAI_API_KEY=...      # GPT producers (optional)
export GEMINI_API_KEY=...      # Gemini producers (optional)

node scripts/build-dist.mjs                  # the protocol condition pastes dist/ files
python3 evals/run.py                         # all tasks, all providers with keys set
python3 evals/run.py --tasks writing code    # subset
python3 evals/run.py --models claude-sonnet-5 gemini-2.5-flash
python3 evals/run.py --judge-model claude-opus-4-8
```

Outputs land in `evals/results/<timestamp>/`: every raw generation, every judge verdict
(JSON), and `summary.md` with the findings table. Rerun with the same flags to reproduce;
generation is sampled, so expect variance: run 3+ seeds before believing a small delta
(prompting.md section 3 applies to this eval too).

## Cost and honesty

A full run (6 tasks x 2 conditions x 3 models + judging) is roughly 150-300k tokens.
Published numbers belong in this README with the run date, models, judge, and seed count;
no cherry-picking single seeds. Until a table with those stamps sits below this line, the
cross-model claim in the README remains an author estimate, not a measurement.

## Results

None published yet for this fork. Run the harness and put the table here.

## Adding a task

Copy any file in `tasks/`: a `DOMAIN` line naming the craft file, a `TASK` section (the
user request, concrete, with real inputs), and a `RUBRIC` section (6-12 checkable lines;
these are what the judge scores, so no adjectives). Hard tasks earn their place; a task
every condition passes proves nothing.
