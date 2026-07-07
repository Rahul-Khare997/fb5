DOMAIN: product

TASK:
Write a one-page PRD for adding offline mode to Fieldnote, a mobile inspection app used by
housing-association surveyors (Android tablets, often in basements and stairwells with no
signal; median inspection: 74 photos, 40 checklist items, 25 minutes). Constraints from
engineering: photo uploads are the only server dependency during an inspection; the sync
service already exists for a different feature; conflict case = two surveyors editing the
same property record offline; the team is 2 engineers for 6 weeks; iOS is out of scope
this cycle.

RUBRIC:
1. The problem is stated with the given numbers (74 photos, 25 minutes, basements), not a
   generic "users need offline".
2. Scope fits 2 engineers x 6 weeks and says what is explicitly OUT (iOS is out; at least
   two more cut lines with reasons).
3. The conflict case (two surveyors, same property) has a designed resolution the reader
   could implement, not "handle conflicts gracefully".
4. Success metrics are measurable post-launch with the app's own data, each with a target
   number and the query-able event it comes from; no vanity metrics.
5. Failure states designed: storage full mid-inspection, sync dies at 90%, app killed
   while photos pending. Each with the user-visible behavior.
6. Every requirement is checkable by QA as written (a tester could pass/fail it); no
   "fast", "intuitive", "reliable" without a number.
7. Under 550 words; a reader who knows nothing about Fieldnote can build the right thing
   from this page alone.
