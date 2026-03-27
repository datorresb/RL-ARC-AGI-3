# RL-ARC-AGI-3

Hackathon-ready ARC Prize starter environment for Ubuntu/Linux. The repo is set up around the official `arc-agi` Python toolkit, with a bundled offline smoke game so you can get to a real ARC run before worrying about API keys or online scorecards.

## Quickstart

1. Install `uv`: https://docs.astral.sh/uv/getting-started/installation/
2. Ensure Python 3.12 is available to `uv`
3. Sync the project

```bash
uv sync --locked --dev
```

4. Verify the already-synced environment and run the golden-path local smoke check

```bash
./scripts/check_arc_env.sh
```

5. Run the starter directly

```bash
uv run arc-starter --mode offline --game hack1 --max-steps 5
```

If `ARC_API_KEY` is set in your shell or in `.env`, you can switch to a remote ARC task such as `ls20`:

```bash
cp .env.example .env
uv run arc-starter --mode online --game ls20 --max-steps 5
```

## What This Repo Gives You

- A pinned Python 3.12 `uv` project
- A bundled local ARC smoke game (`hack1`) that does not require secrets
- A secret-safe verification script that distinguishes local readiness from optional remote readiness
- Tests for configuration and starter wiring
- A deeper setup guide in [docs/setup/arc-hackathon-environment.md](/workspaces/RL-ARC-AGI-3/docs/setup/arc-hackathon-environment.md)

## Local Vs Online

- Local mode is the default development path and does not require `ARC_API_KEY`
- Online mode is optional and depends on ARC Prize service availability
- Benchmarking is a separate workflow from this starter; use the official benchmarking repo if you need leaderboard-oriented harnesses

## References

- ARC quickstart: https://docs.arcprize.org/index.md
- Local vs online: https://docs.arcprize.org/local-vs-online.md
- API keys: https://docs.arcprize.org/api-keys.md
- Toolkit minimal example: https://docs.arcprize.org/toolkit/minimal.md