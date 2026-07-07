DOMAIN: design

TASK:
Build a single-file HTML pricing section (inline CSS, no frameworks, no external assets)
for Kilnroom, a subscription studio-management app for independent ceramics studios. Brand
tokens (the only colors allowed): ink #1C1B1A, clay #B4552D, glaze #7A8B8C, bone #F0EBE3.
Type: system-ui stack only. Three tiers from the spec: Solo (1 kiln, 40 member slots,
£29/mo), Studio (3 kilns, 150 member slots, firing-schedule automation, £79/mo), Collective
(unlimited kilns, unlimited members, multi-site, £190/mo). Studio is the recommended tier.
Annual billing takes 2 months off each price.

RUBRIC:
1. Only the four brand hex values (plus their opacity variants) appear in the CSS; no
   other colors, no gradients.
2. One tier visually dominates (the recommended Studio) through at most two devices
   (scale, border, or background shift); the other tiers do not compete.
3. Exactly one primary action per card; primary and secondary actions differ in weight,
   not just color.
4. Spacing sits on one grid (a single base unit and its multiples); no arbitrary one-off
   paddings.
5. All spec numbers appear exactly as given (kilns, slots, prices, annual = 2 months off
   computed correctly per tier and shown).
6. Works at 360px and 1200px wide without horizontal scroll (media query present; cards
   stack on narrow screens).
7. The kill test: no centered-hero-three-equal-cards default; at least one structural
   choice specific to ceramics studios (vocabulary or layout), not transplantable to any
   SaaS.
8. Semantic HTML: real buttons/links, one h2, tier names as h3; prices not inside heading
   tags.
