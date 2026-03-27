from __future__ import annotations

from dataclasses import dataclass
from os import environ
from typing import Literal, Mapping

from dotenv import load_dotenv

ModeLiteral = Literal["offline", "online"]
RequestedMode = Literal["auto", "offline", "online"]


@dataclass(frozen=True, slots=True)
class RuntimeConfig:
    game: str
    mode: ModeLiteral
    render_mode: str
    max_steps: int
    has_api_key: bool

    @property
    def api_key_status(self) -> str:
        return "set (redacted)" if self.has_api_key else "not set"


def load_runtime_config(
    *,
    game: str,
    requested_mode: RequestedMode,
    render_mode: str,
    max_steps: int,
    env: Mapping[str, str] | None = None,
) -> RuntimeConfig:
    """Resolve runtime settings from CLI inputs and environment."""
    if env is None:
        load_dotenv(override=False)
        resolved_env: Mapping[str, str] = environ
    else:
        resolved_env = env

    api_key = resolved_env.get("ARC_API_KEY", "").strip()
    if requested_mode == "auto":
        mode: ModeLiteral = "online" if api_key else "offline"
    else:
        mode = requested_mode

    return RuntimeConfig(
        game=game,
        mode=mode,
        render_mode=render_mode,
        max_steps=max_steps,
        has_api_key=bool(api_key),
    )