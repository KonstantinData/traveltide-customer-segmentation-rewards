# Release checklist

Use this checklist for portfolio-style releases. The target tag for the first excellence milestone is **`v1.0.0-excellence`**.

## 1) Pre-release readiness

- [ ] All CI checks pass locally and in CI (tests, lint, format).
- [ ] Documentation reflects the latest analysis outputs and artifacts.
- [ ] Artifacts are regenerated (EDA reports, plots) and committed when appropriate.
- [ ] No secrets are present in the repo (scan `.env`, `config/`, `artifacts/`).
- [ ] Dependency audit completed (see Security Policy).

## 2) Versioning + tagging

- [ ] Confirm the version string in `pyproject.toml` (if applicable).
- [ ] Create an annotated tag for the release milestone:

```bash
git tag -a v1.0.0-excellence -m "Release v1.0.0-excellence"
```

- [ ] Push the tag to the remote:

```bash
git push origin v1.0.0-excellence
```

## 3) Release notes

- [ ] Summarize the completed analysis steps and decision points.
- [ ] Link to key artifacts (EDA report, gallery plots, strategy deck).
- [ ] Note any follow-up work queued for the next iteration.
