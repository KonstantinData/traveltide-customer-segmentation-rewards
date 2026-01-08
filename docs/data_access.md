# Data access (local Bronze data)

This repository ships the raw TravelTide Bronze tables directly in the
`data/bronze` directory, enabling offline and reproducible analysis without any
external storage dependencies.

## Source of truth (raw data)

- Location: `data/bronze/`
- Tables:
  - `data/bronze/users_full.csv`
  - `data/bronze/sessions_full.csv`
  - `data/bronze/flights_full.csv`
  - `data/bronze/hotels_full.csv`

## Access model

- Files are committed to the repository for local access.
- No credentials or network calls are required.

## Verification commands

```bash
ls -lh data/bronze
```
