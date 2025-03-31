# scrollshot2pdf Project Guidelines

## Build & Development Commands
- Setup: `just setup` (installs dependencies with uv)
- Format code: `just format` (fixes formatting with ruff)
- Fix linting issues: `just fix` (includes unsafe fixes)
- Lint: `just lint` (runs ruff checks without modifying files)
- Type check: `just typecheck` (runs pyright)
- Run tests: `just test` or `just test path/to/test_file.py::test_function`
- Combined check: `just check` (runs lint + typecheck + test)
- Run app: `just run [args]` or directly `python -m scrollshot2pdf [args]`

## Code Style Guidelines
- Python version: 3.10+
- Formatting: PEP 8 style, enforced by ruff
- Imports order: standard library → third-party → local
- Typing: Use type hints for all function params and return values
- Naming: snake_case for functions/variables, UPPER_CASE for constants
- Docstrings: Triple double-quotes with function purpose and return values
- Error handling: Use try/except blocks with specific error messages
- CLI interface: Well-documented argparse with clear help messages
- Comments: Explain why, not just what; document complex algorithms

See `docs/` directory for detailed implementation documentation.
