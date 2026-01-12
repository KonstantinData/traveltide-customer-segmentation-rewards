# Data access (local raw data)

This repository ships the raw TravelTide tables directly in the
`data/` directory, enabling offline and reproducible analysis without any
external storage dependencies.

## Source of truth (raw data)

- Location: `data/`
- Tables:
  - `data/users_full.csv`
  - `data/sessions_full.csv`
  - `data/flights_full.csv`
  - `data/hotels_full.csv`

## Access model

- Files are committed to the repository for local access.
- No credentials or network calls are required.

## Verification commands

```bash
ls -lh data
```
