# Data access (private S3; non-public)

This repository does not store full raw TravelTide data due to size constraints.
Raw data is stored in a private S3 bucket and accessed via AWS IAM (read-only).

## Source of truth (raw data)

- S3 Bucket: `traveltide-data`
- Prefix: `bronze/`
- Objects:
  - `bronze/users.csv`
  - `bronze/sessions.csv`
  - `bronze/flights.csv`
  - `bronze/hotels.csv`

## Access model (no public access)

- The bucket remains private (Block Public Access enabled).
- Access is granted via IAM credentials (read-only).

## Required environment variables

Set the following environment variables (do not commit credentials):

- `S3_ACCESS_KEY_ID` (fallback: `AWS_ACCESS_KEY_ID`)
- `S3_SECRET_ACCESS_KEY` (fallback: `AWS_SECRET_ACCESS_KEY`)
- `AWS_DEFAULT_REGION`
- `TRAVELTIDE_S3_BUCKET` (e.g., `traveltide-data`)
- `TRAVELTIDE_S3_PREFIX` (e.g., `bronze/`)

## Verification commands

```bash
aws sts get-caller-identity
aws s3 ls s3://traveltide-data
aws s3 ls s3://traveltide-data/bronze/ --recursive --human-readable --summarize
```
