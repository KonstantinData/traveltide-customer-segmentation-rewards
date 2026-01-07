# TT-028 — Strategy Recommendations (Data-Backed)

This document translates the evidence-based personas into **actionable segment
strategies**. Recommendations are grounded in the Step 2 feature signals and the
perk mapping decisions.

## Strategy goals

1. **Lift conversion** by aligning perks with segment intent signals.
2. **Protect margin** by targeting incentives where price sensitivity is clear.
3. **Reduce churn risk** by addressing cancellation and hesitation behaviors.

## Segment strategy recommendations

| Segment id | Persona | Core evidence (signal → implication) | Primary strategy | Supporting tactics | Primary KPIs |
| --- | --- | --- | --- | --- | --- |
| 0 | Explorer Planners | High `avg_page_clicks` + `avg_session_duration_sec` → high research intent but moderate conversion | **Guided planning journey** | - Personalized itinerary builders<br>- Price watchlists + fare alerts<br>- Bundled suggestions after 3+ sessions | Session-to-booking conversion, itinerary tool adoption |
| 1 | Deal-Driven Flyers | High `p_flight_booked` + `p_flight_discount_shown` → price-sensitive flight behavior | **Flight deal acceleration** | - Targeted fare promos<br>- Limited-time miles multipliers<br>- Triggered discounts when fares drop | Flight booking conversion, promo redemption rate |
| 2 | Staycation Bundlers | High `p_hotel_booked` + `avg_nights` + `avg_rooms` → lodging-first, longer stays | **Hotel-centric value bundle** | - Free-night thresholds (stay 3+ nights)<br>- Room upgrade credits<br>- Family/room bundle offers | Avg. nights per booking, room upsell rate |
| 3 | Frequent Business Travelers | High `n_sessions` + `p_return_flight_booked` + low `avg_nights` → frequent, short-stay travel | **Speed + loyalty accelerators** | - Priority support and faster checkout<br>- Status accelerators for repeat bookings<br>- Business traveler bundles (late check-out) | Repeat booking rate, loyalty tier progression |
| 4 | Cautious Evaluators | High `p_cancellation_session` + low booking conversion → risk-averse behavior | **Risk-reduction assurance** | - Flexible cancellation windows<br>- Price guarantees / hold options<br>- Travel protection add-ons | Cancellation rate, booking conversion lift |

## Cross-segment playbook (how to activate)

1. **Trigger-based messaging**
   - Use high browsing signals (sessions, clicks) to trigger planning nudges for
     Segment 0.
   - Use discount exposure and fare changes to trigger Segment 1 promos.
2. **Personalized merchandising**
   - Push hotel bundles and multi-room options for Segment 2 at the results
     page level.
   - Highlight quick rebook flows and loyalty status for Segment 3.
3. **Risk mitigation**
   - Surface flexible policies early for Segment 4 to reduce abandonment.

## Measurement guidance

- **Short-term conversion**: monitor lift in segment-level booking conversion and
  promo redemption after perk rollout.
- **Medium-term value**: track segment-level repeat bookings and average order
  value (AOV), especially for Segments 2 and 3.
- **Behavioral health**: track cancellation rate by segment to validate risk
  reduction outcomes for Segment 4.

## Evidence sources

- Persona signals: `docs/step3_insights_strategy/segment_personas.md`.
- Perk mapping decisions: `docs/step3_insights_strategy/perk_mapping_decision_table.md`.
- Feature definitions: `docs/step2_features_segmentation/feature_data_dictionary.md`.
