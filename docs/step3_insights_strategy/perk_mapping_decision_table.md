# TT-026 — Perk Mapping Decision Table (Segment → Perk + Evidence + Confidence)

This decision table ties each segment to its recommended primary perk based on
observed behavioral evidence from the Step 2 feature set.

## Decision table

| Segment id | Persona name | Primary perk decision | Evidence highlights | Confidence |
| --- | --- | --- | --- | --- |
| 0 | Explorer Planners | Planning tools + itinerary support | High `avg_page_clicks` and `avg_session_duration_sec` with only moderate booking conversion indicates research-heavy planning behavior. | Medium |
| 1 | Deal-Driven Flyers | Flight discounting (miles multipliers, airfare promos) | High `p_flight_booked` with high `p_flight_discount_shown` and `avg_flight_discount_amount` signals strong responsiveness to flight deals. | High |
| 2 | Staycation Bundlers | Hotel/room perks (credits, upgrades, free nights) | High `p_hotel_booked`, `avg_nights`, and `avg_rooms` show lodging-first, longer-stay behavior. | High |
| 3 | Frequent Business Travelers | Loyalty accelerators + priority support | High `n_sessions` and `p_return_flight_booked` with shorter stays indicate frequent, time-sensitive travel. | High |
| 4 | Cautious Evaluators | Risk-reduction perks (flexible cancellation, guarantees) | High `p_cancellation_session` with low booking conversion points to risk aversion and hesitation to commit. | Medium |

## Evidence sources

- Persona definitions and evidence signals: `docs/step3_insights_strategy/segment_personas.md`.
- Feature definitions: `docs/step2_features_segmentation/feature_data_dictionary.md`.
