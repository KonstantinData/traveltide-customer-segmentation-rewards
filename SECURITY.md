
# Security Policy

## Supported versions

This is a portfolio/case-study repository. Security fixes are provided on a best-effort basis for the default branch.

## Reporting a vulnerability

Please report security issues privately by emailing: <PLACEHOLDER_EMAIL>

Include:

* A description of the issue and potential impact
* Steps to reproduce (proof-of-concept if available)
* Affected files/versions (if known)

## Response expectations

* Acknowledgement within **7 days**
* Best-effort remediation timeline depending on severity and maintainer availability

Do not open public issues for sensitive vulnerabilities.

## Security baseline

* **No secrets in Git.** Do not commit credentials, API keys, or production data to this repository.
* **Use environment variables.** Copy `.env.example` to `.env` for local-only configuration.
* **Scrub artifacts.** Ensure generated artifacts contain only aggregated or anonymized data.

## Dependency audit policy

Run a dependency audit at least once per release cycle (or monthly, whichever is more frequent).

Recommended command:

```bash
pip-audit
```
