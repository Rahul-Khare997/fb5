# fb5: the team guide

A plain-English walkthrough for anyone on the team. No prior context needed. If you only
read one file, read this one.

## What fb5 is, in one paragraph

When you ask an AI model to "make it great", you get its average: the same three-card
pricing page, the same "seamlessly leverage" marketing copy, the same report that hedges
every sentence. fb5 is a set of written instructions that make the model work the way a
careful expert does instead: decide what "good" means before it starts, write more than
one draft, check its own work against real evidence with fresh eyes, and refuse to stop at
"looks done". It works on Claude, GPT, and Gemini. It does not require a smarter model; it
changes how the model you already have works.

## Why it works (the one idea)

A stronger model mostly is not smarter about facts. It is better at *process*: it sets a
standard, verifies against reality, and iterates. Process can be written down. fb5 is that
process written down, so a cheaper model borrows it.

Three moves do the heavy lifting:

1. **Write the standard first.** You cannot aim at "premium". You can aim at "one accent
   color, body text 65-75 characters wide, prices not inside headings". fb5 makes the model
   write that checklist *before* it generates, then build against it.
2. **Draft one is a sample, not the answer.** For anything creative, the model makes several
   different attempts and picks the best, instead of polishing the first one.
3. **A fresh set of eyes checks the work.** The part of the model that wrote something will
   defend it. So a separate, clean pass (a different chat, or a scripted judge) reviews it
   and reports every flaw. Then the first pass fixes them.

## The three levels of effort

You choose how hard fb5 works based on how much the output matters:

| Mode | What it does | Use it for |
|---|---|---|
| **quick** | Write the standard, produce, one review pass, fix. One reply. | Everyday work: an email, a function, a summary. |
| **full** | Everything: multiple drafts, repeated review until two clean passes, a final taste check. | Work that ships: a landing page, a launch email, a real feature. |
| **gate** | Just the final taste check on something that already exists. | "Is this good enough to send?" |

Rule of thumb: **quick** for most things, **full** when a customer or your boss will see it.

## How to use it (pick your tool)

### In Claude Code (the terminal / IDE tool)

It is installed as a skill. Just type:

```
/fb5 the pricing page              (full quality, the default)
/fb5 fix the export bug quick      (fast, one review pass)
/fb5 landing-page.html gate        (only judge existing work)
```

fb5 figures out which of its 21 subject areas apply (design, code, writing, research, and
so on) automatically. You do not pick.

**To install it yourself** (if it is not already there):
```
/plugin marketplace add Rahul-Khare997/fb5
/plugin install fb5@Rahul-Khare997
```
Then open a new session so it loads.

### In claude.ai, ChatGPT, or Gemini (a normal chat window)

No slash commands exist in a chat window, so you paste the instructions instead. Easiest
path:

1. Open the `dist/` folder in the repo. Pick the file matching your job:
   `fb5-design.md`, `fb5-code.md`, `fb5-writing.md`, and so on (21 of them).
2. Paste that **whole file** into the chat.
3. Then paste **your actual task at the very bottom**, below everything.

That single file already contains the method plus the standards for your subject, so there
is nothing else to attach. For a short task on a weaker model, use `PROMPT-quick.md`
instead; it is the lightweight version.

**Give it a good brief.** The output can only be as sharp as the ask. If you have 60
seconds, fill in this five-liner instead of a one-sentence request (it is also printed at
the bottom of every paste file):

```
DELIVERABLE: what exactly gets produced
AUDIENCE:    who consumes it, and in what situation
CONSTRAINTS: brand rules, word limits, must-include facts
GOLD EXAMPLE: a past piece that sets the bar, if one exists
DONE MEANS:  the one or two outcomes that make this a success
```

**One trick that noticeably improves quality in a chat window:** when the work matters, open
a *second, empty chat*, paste in the review instructions (the "VERIFIER" block from the file)
plus the draft, and let that fresh chat critique it. Bring the critique back to the first
chat to fix. A chat cannot review its own work honestly; a blank one can.

## Make it speak your brand (once, 15 minutes)

Out of the box, fb5 aims at "excellent in general". The tailor interview aims it at *your*
excellent: run the one-paste prompt in [TAILOR.md](TAILOR.md) and the model interviews you
(one question at a time) about your brand colors, voice, banned words, and non-negotiables,
then writes them into a house file every future run obeys. It ends by running one small
task that would have come out generic before, so you see the difference immediately. Do
this once per team; the file is shared through the repo like everything else.

## What you actually get back

Not vibes. A report you can act on. Reviews come out as a fixed list, each flaw pinned to a
place and a rule:

```
1. pricing hero, mobile | one clear button per screen | two buttons compete, same weight | confidence: high
2. tier names | sounds generic | "Starter / Growth / Pro" could be any product | confidence: medium
```

An empty list is itself a claim: it means every rule was checked and nothing was found. And
the model tells you plainly what it could NOT verify, instead of pretending.

## The safety rails (built in, run automatically in Claude Code)

- **Slop scanner** (`banscan`): a script that catches filler words ("seamlessly",
  "world-class"), fake placeholders ("rest of the file unchanged"), and hedged claims, and
  makes the model fix them. In Claude Code this runs on every file the model writes.
- **Model-specific tuning**: each model has a known bad habit (Claude leans on cream-and-
  serif design defaults, GPT hedges, Gemini shortens long output). fb5 tells each model to
  watch for its own tell.
- **Honesty about limits**: if the model cannot actually check something (no screenshot
  tool in a chat window, say), it lists it as unverified rather than claiming it passed.

## What it will NOT do (set expectations)

- It does not make the model smarter on a genuinely novel hard problem. It makes the good
  work reliable and kills the lazy average.
- **full** mode costs more (it does several passes on purpose). Use **quick** for routine
  work.
- Two runs can produce different results; it raises quality, it does not make output
  identical every time.
- The taste ceiling is the judge model's ceiling. A model reviewing its own tier is good,
  not perfect. Use the strongest model you have as the reviewer when it counts.

## The 30-second version to tell a teammate

> fb5 makes Claude, GPT, or Gemini write a quality checklist before it starts, take a few
> attempts instead of one, and check its own work with fresh eyes until it is actually done.
> In Claude Code: type `/fb5 <your task>`. In a chat window: paste the matching `dist/`
> file, then your task underneath. Use `quick` for everyday work, `full` for anything a
> customer sees.

Deeper reading, when you want it: [the README](../README.md) for the pitch,
[HOW-IT-WORKS.md](HOW-IT-WORKS.md) for the ten-minute version, and
[fb5/references/](../fb5/references) for the actual standards.
