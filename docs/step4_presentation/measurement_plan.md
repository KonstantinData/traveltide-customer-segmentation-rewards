# TT-029 — Measurement Plan (A/B lift, retention, CLV/proxies, guardrails)

This plan defines how to measure the impact of the segment-based perk strategy
in TT-028, with a focus on short-term lift, retention, and long-term value
proxies while protecting margin and experience quality.

## 1) Experiment design (A/B lift)

**Objective:** quantify incremental conversion and value from segment-tailored
perks versus the current experience.

- **Population:** all eligible web/app sessions that map to a segment
  (Segments 0–4).
- **Randomization:** user-level, persistent assignment (avoid cross-over).
- **Variants:**
  - **Control:** existing baseline offers and messaging.
  - **Treatment:** segment-specific perks + messaging from TT-028 strategy.
- **Stratification:** segment id to ensure balanced representation.
- **Primary analysis window:** 14–28 days post-launch (enough for repeat
  behavior to surface).

### Primary lift metrics

- **Segment-level booking conversion**
  - Definition: bookings / eligible sessions (or users) by segment.
- **Promo/perk redemption rate**
  - Definition: redeemed perks / offered perks by segment.
- **Incremental revenue per user/session (iRPU/iRPS)**
  - Definition: (treatment revenue − control revenue) / users (or sessions).

## 2) Retention measurement

**Objective:** confirm short-term conversion gains do not hurt repeat behavior.

- **Repeat booking rate (30/60/90 days):**
  - % of users who book again within 30/60/90 days of first booking in window.
- **Return session rate:**
  - % of users who return to the site/app within 30 days.
- **Segment re-engagement:**
  - Change in session frequency for high-intent segments (0, 3).

## 3) CLV and proxy metrics

**Objective:** evaluate long-term value impact where full CLV is not available.

- **CLV proxy = 90-day gross booking value per user (GBV/user)**
  - Sum of booking value in 90 days after exposure.
- **Margin proxy = 90-day contribution per user**
  - (GBV × estimated margin) − discount cost.
- **Average order value (AOV)**
  - Useful for Segments 2 and 3 where bundle size drives value.

## 4) Guardrails (protect margin & experience)

**Objective:** ensure changes do not introduce regressions or undue cost.

- **Cancellation rate:** should not increase > +2% relative to control.
- **Discount cost per booking:** capped by segment-specific thresholds
  (e.g., +$X per booking based on expected lift).
- **Customer support contacts per booking:** no material increase.
- **NPS / CSAT (if available):** no decline beyond pre-defined threshold.

## 5) Reporting cadence & decision rules

- **Weekly readout:** conversion lift, redemption, cancellation rate.
- **Bi-weekly readout:** retention and 90-day value proxies (rolling).
- **Decision rule:**
  - Ship if primary conversion lift is positive and guardrails hold.
  - Iterate if lift is neutral but retention/CLV proxies improve.
  - Roll back if guardrails are violated or lift is negative.

## 6) Data capture checklist

- Log segment id, variant assignment, perk exposure, redemption, and booking
  events at user/session granularity.
- Store discount cost and booking value for margin calculations.
- Ensure consistent user identifiers across sessions for retention.

## References

- Strategy recommendations: `docs/step3_insights_strategy/strategy_recommendations.md`
- Persona signals: `docs/step3_insights_strategy/segment_personas.md`
- Feature definitions: `docs/step2_features_segmentation/feature_data_dictionary.md`
