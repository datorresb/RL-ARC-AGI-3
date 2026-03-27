# ARC Hackathon Environment Guide

## Supported Path

This starter explicitly supports native Ubuntu/Linux and the current dev container. The project targets Python 3.12 because the upstream `arc-agi` package currently declares `Requires-Python: >=3.12`.

## Tooling Contract

- Package manager and virtual environment workflow: `uv`
- Supported interpreter for the documented path: Python 3.12
- Starter command: `uv run arc-starter`
- Verification command: `./scripts/check_arc_env.sh`
- Bundled offline smoke game: `hack1`

## First-Run Flow

```bash
uv sync --locked --dev
./scripts/check_arc_env.sh
uv run arc-starter --mode offline --game hack1 --max-steps 5
```

That flow is the golden path for this repo. If it passes, the environment is ready for local hackathon work.

The verifier is intentionally non-mutating. If `.venv` is missing, it will stop and tell you to run `uv sync --locked --dev` first.

To try an official ARC game such as `ls20`, switch to online mode after setting `ARC_API_KEY`:

```bash
uv run arc-starter --mode online --game ls20 --max-steps 5
```

## Optional Remote Setup

1. Create an ARC Prize account at https://arcprize.org/platform
2. Generate an API key from your profile
3. Copy `.env.example` to `.env` and set `ARC_API_KEY`

```bash
cp .env.example .env
```

The starter loads `.env` automatically for local development. Shell environment variables still take precedence.

## Troubleshooting

### `uv` is missing

Install `uv` from the official instructions:

https://docs.astral.sh/uv/getting-started/installation/

### Python 3.12 is missing

Use `uv` to install or pin Python 3.12, then rerun:

```bash
uv python install 3.12
uv sync --locked --dev
```

### `ARC_API_KEY` is not set

That is fine for local mode. The verification script will still mark local setup as ready.

### Online mode fails even with an API key

Treat that as an optional remote issue, not as a broken local environment. Re-check the key, then validate against the official ARC docs and service availability.

## Upstream Docs Worth Keeping Open

- Quickstart: https://docs.arcprize.org/index.md
- Agents quickstart: https://docs.arcprize.org/agents-quickstart.md
- Local vs online: https://docs.arcprize.org/local-vs-online.md
- API keys: https://docs.arcprize.org/api-keys.md
- Toolkit overview: https://docs.arcprize.org/toolkit/overview.md
- Toolkit minimal example: https://docs.arcprize.org/toolkit/minimal.md