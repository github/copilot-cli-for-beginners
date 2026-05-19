# Dependency Notes

## Scope

These notes cover the primary sample in `samples/book-app-project/`.

## Critical Dependencies

- Python: `>=3.10`
  - Reason: the sample course content assumes a modern Python version and the project metadata already requires 3.10 or newer.
- pytest: `>=8,<9`
  - Reason: pytest is the project's test dependency, and constraining it to the current major version reduces surprise breakage from future major releases.

## Current Policy

- Prefer bounded version ranges for tool dependencies used in course exercises.
- Keep changes small: allow patch and minor updates within a known-good major version before considering an upgrade.
- Re-run the sample test suite after any dependency change.

## Current Gaps

- `pytest` is listed in core dependencies even though it is only needed for validation workflows.
- There is no lock file for the Python sample, so installs can still vary slightly across environments within the allowed version range.

## Verification

Run from the repo root:

```bash
python -m pytest samples/book-app-project/tests -q
```