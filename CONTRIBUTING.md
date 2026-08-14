# Contributing

Thanks for considering contributing to NCBI Sequence Downloader!

## Getting Started

1. Fork the repository and clone your fork.
2. Create a virtual environment and install dependencies (`pip install -r requirements.txt`).
3. Copy `.env.example` to `.env` and set your own `ENTREZ_EMAIL`.
4. Create a feature branch: `git checkout -b feature/your-feature-name`.

## Development Guidelines

- Follow PEP8 and include type hints on all new functions.
- Add docstrings to every public function/class.
- Write tests for any new logic (see `tests/` for examples) — mock network calls, don't hit the real NCBI API in tests.
- Run `pytest -v` and ensure all tests pass before opening a PR.
- Keep commits focused and write clear commit messages (e.g. `feat: add gene ID search support`).

## Reporting Issues

Please include: what you expected to happen, what actually happened, and steps to reproduce (including the accession number used, if relevant).

## Code of Conduct

Be respectful and constructive. This is a learning-oriented project — questions and beginner-friendly PRs are welcome.