from __future__ import annotations

import argparse
import random
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any, Sequence

from .config import RuntimeConfig, load_runtime_config


DEFAULT_GAME = "hack1"


def bundled_environments_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "environment_files"


def has_local_environment(game: str) -> bool:
    return (bundled_environments_dir() / game.split("-", 1)[0] / "metadata.json").exists()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a local-first ARC Prize starter session.",
    )
    parser.add_argument("--game", default=DEFAULT_GAME, help="ARC game identifier to run.")
    parser.add_argument(
        "--mode",
        choices=["auto", "offline", "online"],
        default="auto",
        help="Use offline by default, or opt into online mode with ARC_API_KEY.",
    )
    parser.add_argument(
        "--render-mode",
        default="terminal",
        help="Render mode passed to the ARC environment wrapper.",
    )
    parser.add_argument(
        "--max-steps",
        type=positive_int,
        default=5,
        help="Maximum number of starter steps to execute.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=7,
        help="Seed for deterministic random action choice.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Resolve configuration without starting the ARC environment.",
    )
    return parser


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be a positive integer")
    return parsed


def pick_action_data(action: Any) -> dict[str, int] | None:
    if getattr(action, "is_complex", lambda: False)():
        return {"x": 32, "y": 32}
    return None


def run_session(config: RuntimeConfig, *, seed: int) -> int:
    from arc_agi import Arcade, OperationMode

    mode = OperationMode.ONLINE if config.mode == "online" else OperationMode.OFFLINE
    arc = Arcade(
        operation_mode=mode,
        environments_dir=str(bundled_environments_dir()),
    )
    env = arc.make(config.game, render_mode=config.render_mode)
    if env is None:
        available_games = sorted(
            {item.game_id.split("-", 1)[0] for item in arc.available_environments}
        )
        print(
            "Starter could not load the requested game. "
            f"Requested: {config.game}. Available local games: {available_games}",
            file=sys.stderr,
        )
        if config.mode == "offline":
            print(
                "Offline mode only scans the repo-local environment_files directory. "
                f"Try the bundled default game `{DEFAULT_GAME}` or add more local environment metadata.",
                file=sys.stderr,
            )
        return 1

    observation = env.reset()
    randomizer = random.Random(seed)
    steps_taken = 0

    while observation is not None and steps_taken < config.max_steps:
        actions = list(getattr(env, "action_space", []) or [])
        if not actions:
            print("No actions available; ending starter run.")
            break

        simple_actions = [
            action
            for action in actions
            if not getattr(action, "is_complex", lambda: False)()
        ]
        action = randomizer.choice(simple_actions or actions)
        observation = env.step(action, data=pick_action_data(action))
        steps_taken += 1

    print(
        f"Completed {steps_taken} step(s) in {config.mode} mode for game {config.game}."
    )
    print("Scorecard:")
    print(arc.get_scorecard())
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_runtime_config(
        game=args.game,
        requested_mode=args.mode,
        render_mode=args.render_mode,
        max_steps=args.max_steps,
    )
    if args.mode == "auto" and has_local_environment(args.game):
        config = replace(config, mode="offline")

    print(
        f"Mode: {config.mode} | Game: {config.game} | ARC_API_KEY: {config.api_key_status}"
    )

    if config.mode == "online" and not config.has_api_key:
        print(
            "ARC_API_KEY is required for --mode online. Export the key or use --mode offline.",
            file=sys.stderr,
        )
        return 2

    if args.dry_run:
        print("Dry run successful. Configuration resolved without launching ARC.")
        return 0

    try:
        return run_session(config, seed=args.seed)
    except ImportError:
        print(
            "Dependencies are not installed. Run `uv sync --locked --dev` and try again.",
            file=sys.stderr,
        )
        return 3
    except Exception as exc:  # pragma: no cover - exercised in live smoke checks
        print(f"Starter run failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())