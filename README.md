# code-sentinel
A minimal, pure‑Python implementation of a GitHub Action scanner that can be used in CI/CD pipelines.

## Features
- Configurable via a YAML file.
- Scans a string of source code for simple rule violations.
- Produces a formatted comment for a PR.
- Returns a status (`success` or `failure`) based on critical issues.
- Exits with a non‑zero code when critical issues are found (handled by the caller).

## Usage (as a GitHub Action)
The action would call the `main` function, passing the path to the config file and the code to scan (e.g., via environment variables or temporary files).
The library itself is pure Python and has no runtime dependencies beyond the standard library.

## Development
Run the test suite:
