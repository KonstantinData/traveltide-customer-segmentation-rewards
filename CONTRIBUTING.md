
# Contributing

Thanks for your interest in contributing.

## Development setup

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

2. Verify your environment matches CI:

```bash
python scripts/ci.py
```

## Code style

* Formatting and linting are enforced by **ruff**.
* CI checks:

  * `python -m ruff format --check .`
  * `python -m ruff check .`
  * `pytest -q`

To auto-format locally:

```bash
python -m ruff format .
```

## Pull requests

* Keep PRs small and focused.
* Link related issues where applicable.
* Ensure `python scripts/ci.py` passes before requesting review.

## Commit messages

* Use clear, descriptive messages (e.g., `docs: clarify setup steps`, `ci: add python 3.12`).

## Reporting issues

Use the provided templates:

* Bug reports: `.github/ISSUE_TEMPLATE/bug_report.md`
* Feature requests: `.github/ISSUE_TEMPLATE/feature_request.md`
