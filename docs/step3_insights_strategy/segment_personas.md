# TT-024 — Segment Personas (Evidence-Based Profiles)

This document defines **five customer personas** tied to the K-Means segmentation
choice (`k = 5`). Each persona is expressed as an evidence-based profile derived
from the Step 2 feature set. Use the guidance in the Appendix to refresh the
profiles after each segmentation run.

## Persona overview (by segment id)

| Segment id | Persona name | Primary behaviors | Likely primary perk |
| --- | --- | --- | --- |
| 0 | Explorer Planners | Research-heavy planners with broad browsing and moderate bookings. | Planning tools + itinerary support |
| 1 | Deal-Driven Flyers | High flight booking intent, strong response to flight discounts. | Flight discounting |
| 2 | Staycation Bundlers | Hotel-heavy trips with longer stays and multiple rooms. | Hotel/room perks |
| 3 | Frequent Business Travelers | High session frequency, short stays, repeat flight bookings. | Loyalty accelerators |
| 4 | Cautious Evaluators | High cancellation signals and low booking conversion. | Risk-reduction perks |

> **Note:** Segment ids are assigned by K-Means and can shift across runs.
> Keep the mapping current by re-profiling after each segmentation refresh.

---

## Persona profiles (evidence-based)

### Segment 0 — Explorer Planners

**Core story:** Customers who research extensively, compare options, and book
selectively. They spend time browsing and clicking but do not convert as
aggressively as deal-driven or frequent flyers.

**Evidence signals**
- **High** `avg_page_clicks` and `avg_session_duration_sec` (extended browsing).
- **Moderate** `p_flight_booked` and `p_hotel_booked` (selective conversion).
- **Low** `p_cancellation_session` (intentional decision-making).

**Reward/perk hypothesis**
- Planning assistance (price tracking, flexible itineraries, curated bundles).

---

### Segment 1 — Deal-Driven Flyers

**Core story:** Flight-first customers who respond to discounts and book flights
more often than hotels. Price sensitivity shows up in discount exposure and
redemption.

**Evidence signals**
- **High** `p_flight_booked` with **lower** `p_hotel_booked`.
- **High** `p_flight_discount_shown` and `avg_flight_discount_amount`.
- **Moderate** `avg_base_fare_usd` (value-focused flight selection).

**Reward/perk hypothesis**
- Flight discounts, miles multipliers, or flash airfare promos.

---

### Segment 2 — Staycation Bundlers

**Core story:** Hotel-oriented travelers who book longer stays, multiple rooms,
or family-style trips. They are more likely to bundle lodging than flights.

**Evidence signals**
- **High** `p_hotel_booked` and `avg_nights`.
- **High** `avg_rooms` and `avg_hotel_per_room_usd`.
- **Lower** `p_flight_booked` relative to lodging behavior.

**Reward/perk hypothesis**
- Hotel credits, room upgrades, or free-night perks.

---

### Segment 3 — Frequent Business Travelers

**Core story:** Repeat travelers who book frequently with shorter stays. They
value speed and consistency over discounts.

**Evidence signals**
- **High** `n_sessions` and `p_return_flight_booked`.
- **Lower** `avg_nights` and `avg_rooms` (short, single-room stays).
- **Lower** `p_flight_discount_shown` (less promotion-driven).

**Reward/perk hypothesis**
- Loyalty accelerators, priority support, or fast-track perks.

---

### Segment 4 — Cautious Evaluators

**Core story:** Users who browse but show elevated cancellation behavior and
lower booking conversion. They may be risk-averse or indecisive.

**Evidence signals**
- **High** `p_cancellation_session`.
- **Low** `p_flight_booked` and `p_hotel_booked`.
- **Moderate** `avg_session_duration_sec` with **lower** booking-related
  conversion signals.

**Reward/perk hypothesis**
- Risk reduction (flexible cancellation, price guarantees, travel insurance).

---

## Appendix — How to refresh evidence

1. Produce the latest `customer_features.parquet` (Step 2 contract).
2. Run the segmentation pipeline with `k = 5`.
3. Create a segment summary table with:
   - Mean (or median) of key features by segment.
   - Segment size and share.
4. Update each persona profile with **relative** signals (e.g., high/low vs
   overall) and any specific numeric ranges that are stable.

Reference features: `docs/step2_features_segmentation/feature_data_dictionary.md`.
