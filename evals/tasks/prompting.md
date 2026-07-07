DOMAIN: prompting

TASK:
Write the production prompt (system message + output schema) for an LLM step that triages
inbound support emails for a self-hosted CI product. It must classify each email into
exactly one of: bug_report, config_help, feature_request, billing, security_disclosure,
other; extract the product version if present (format like "v3.2.1" or "3.2.1"); flag
urgency (production_down | degraded | none) from the email content; and route
security_disclosure to a special queue regardless of anything else the email asks. Include
5 eval cases (input email -> expected JSON), at least 2 of them adversarial (an email that
mixes billing with a security report; a rant with no category signal).

RUBRIC:
1. The output is a JSON schema (fields, types, closed enums), not a prose description of
   JSON; unknown/absent version is an explicit null, not an empty string or a guess.
2. Every classification boundary that could be ambiguous has a stated tiebreak rule
   (security beats everything; bug vs config distinguished by a stated criterion).
3. No role theater ("you are the world's best support agent"), no ALL-CAPS pleading, no
   "think step by step" boilerplate.
4. The 5 eval cases are present with complete expected JSON; the two adversarial cases
   genuinely stress the tiebreak rules and their expected outputs follow those rules.
5. The eval inputs vary in length, register, and structure (no shared incidental format
   the model could latch onto).
6. Urgency rules are content-anchored (what phrases/facts imply production_down) rather
   than sentiment-anchored (angry does not mean urgent).
7. The prompt states what the model must do when confidence is low (which bucket, why
   "other" is or is not the dump bucket).
