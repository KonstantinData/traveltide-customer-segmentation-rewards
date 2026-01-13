# TT-031 — Strategy validation checks (sanity + fairness/guardrails notes)

This document defines **pre-launch validation checks** for the segment-based
strategy in TT-028, ensuring the recommendations are **sane, fair, and safe**
before rollout. It complements the measurement plan guardrails in TT-029.

## 1) Data sanity checks (segment integrity)

Validate that the segmentation signals used to trigger strategies are stable
and interpretable before activation.

- **Segment distribution stability**
  - Confirm segment counts match expected proportions (no sudden >±20% shifts).
  - Compare to the baseline snapshot used in TT-028 to detect drift.
- **Feature coverage**
  - Ensure key feature rates are non-null and within historical bounds:
    `avg_session_duration_sec`, `avg_page_clicks`, `p_flight_booked`,
    `p_hotel_booked`, `p_cancellation_session`.
- **Signal coherence**
  - Spot-check top signals for each segment to confirm they match personas
    (e.g., Segment 1 has higher `p_flight_discount_shown` than global).
- **Outlier containment**
  - Verify that extreme values are capped per the EDA outlier policy to avoid
    over-triggering incentives.

## 2) Strategy sanity checks (perk ↔ intent alignment)

Confirm the mapped perks are consistent with the intent signals and do not
contradict segment behaviors.

- **Alignment review**
  - Segment 0: planning nudges should not include aggressive discounts.
  - Segment 1: discount-led offers should be capped and time-bound.
  - Segment 2: hotel bundles should prioritize multi-night incentives.
  - Segment 3: loyalty accelerators should not add friction to checkout.
  - Segment 4: flexible policies must be surfaced early in the funnel.
- **Redundancy scan**
  - Ensure multiple perks do not stack in a way that exceeds margin guardrails.
- **Trigger logic validation**
  - Validate that trigger conditions (e.g., session count, discount exposure)
    are reachable without being overly sensitive.

## 3) Fairness & guardrails notes (pre-launch)

These checks ensure the strategy does not introduce unfair treatment or
experience regressions.

- **Coverage parity (non-sensitive cohorts)**
  - Compare offer exposure rates by device, region, and acquisition channel to
    ensure no material exclusion of a cohort.
- **Cost guardrails by cohort**
  - Verify discount cost per booking remains within the TT-029 caps across
    cohorts to prevent uneven subsidy.
- **Cancellation & support impact**
  - Confirm no cohort sees a disproportionate increase in cancellation or
    support contacts during pilot.
- **Transparency**
  - Ensure terms (refund windows, deal eligibility) are clear and consistent
    across cohorts.

## 4) Launch readiness checklist

| Check area | Pass criteria | Owner |
| --- | --- | --- |
| Segment distribution | No drift >±20% vs baseline | Analytics |
| Feature coverage | Key signals within expected bounds | Data Eng |
| Perk alignment | No contradictions vs personas | Product |
| Guardrail thresholds | Discount cost + cancellation within caps | Finance |
| Cohort parity | No material exposure gaps | Ops |

## References

- Strategy recommendations: `docs/step3_insights_strategy/strategy_recommendations.md`
- Perk mapping decisions: `docs/step3_insights_strategy/perk_mapping_decision_table.md`
- Measurement plan guardrails: `docs/step4_presentation/measurement_plan.md`
