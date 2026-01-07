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

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`

## Verification commands

```bash
aws sts get-caller-identity
aws s3 ls s3://traveltide-data
aws s3 ls s3://traveltide-data/bronze/ --recursive --human-readable --summarize
```
