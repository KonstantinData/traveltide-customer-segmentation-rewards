# TT-035 — Final Report (Customer Segmentation & Rewards Strategy)

## Executive summary

- Five behavioral segments reveal distinct intent patterns across research depth,
  booking propensity, discount sensitivity, and cancellation risk.
- Segment-aligned perks focus on **conversion lift** for high-intent users while
  protecting margin through tailored incentives (not blanket discounts).
- A/B experimentation and guardrails prioritize measurable lift without
  degrading retention or customer experience.

## Segment insights (what we learned)

| Segment id | Persona | Core insight | Primary opportunity | Risk / watchout |
| --- | --- | --- | --- | --- |
| 0 | Explorer Planners | High research behavior, moderate conversion. | Nurture intent with planning tools to move from exploration to booking. | Over-incentivizing may erode margin without conversion lift. |
| 1 | Deal-Driven Flyers | Strong flight booking intent with high discount responsiveness. | Use targeted airfare promotions to accelerate flight conversion. | Promo fatigue if discounts are too frequent. |
| 2 | Staycation Bundlers | Hotel-first, longer stays, multi-room behavior. | Bundle hotel perks to increase length-of-stay and room upgrades. | Ensure perks don’t cannibalize full-price rooms. |
| 3 | Frequent Business Travelers | Frequent, short-stay travel with low discount dependence. | Speed + loyalty accelerators to reduce friction and reinforce retention. | Over-rewarding already-loyal customers without incremental lift. |
| 4 | Cautious Evaluators | High cancellation signals and low conversion. | Reduce perceived risk to increase booking confidence. | Flexible policies could increase cancellations if not monitored. |

## Recommendation rationale (why these perks)

- **Segment 0 (Explorer Planners):** itinerary builders, price alerts, and planning tools
  support decision-making without heavy discounts.
- **Segment 1 (Deal-Driven Flyers):** airfare promos or miles multipliers capture intent at
  the moment of price change.
- **Segment 2 (Staycation Bundlers):** free-night thresholds and room upgrades reinforce
  hotel-first behavior and longer stays.
- **Segment 3 (Frequent Business Travelers):** loyalty accelerators and priority flows
  reduce friction and support retention.
- **Segment 4 (Cautious Evaluators):** flexible cancellation and price guarantees reduce
  hesitation and encourage booking.

## Measurement plan highlights (how we validate)

- **Primary lift metrics:** booking conversion, perk redemption, incremental revenue per
  user/session (by segment).
- **Retention checks:** repeat booking rate (30/60/90 days), return session rate, and
  re-engagement for high-intent segments.
- **Guardrails:** cancellation rate (+2% max), discount cost per booking, and customer
  support contact rate.
- **Decision rule:** ship if conversion lift is positive and guardrails hold; iterate if lift
  is neutral but retention/CLV proxies improve.

## Next steps

- Launch A/B test with segment-stratified assignment.
- Instrument perk exposure, redemption, booking value, and cancellation signals.
- Review weekly for lift and guardrail performance; adjust perks per segment.
