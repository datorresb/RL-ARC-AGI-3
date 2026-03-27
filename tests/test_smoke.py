from __future__ import annotations

import sys
import types

from rl_arc_agi_3.config import RuntimeConfig
from rl_arc_agi_3.main import run_session


class FakeAction:
    def __init__(self, *, complex_action: bool = False) -> None:
        self._complex_action = complex_action

    def is_complex(self) -> bool:
        return self._complex_action


class FakeEnvironment:
    def __init__(self) -> None:
        self.action_space = [FakeAction()]
        self.step_calls = 0

    def reset(self) -> object:
        return object()

    def step(self, action, data=None):
        self.step_calls += 1
        return None


class FakeArcade:
    def __init__(self, *, operation_mode, environments_dir=None) -> None:
        self.operation_mode = operation_mode
        self.environments_dir = environments_dir
        self.environment = FakeEnvironment()

    def make(self, game: str, render_mode: str):
        assert game == "hack1"
        assert render_mode == "terminal"
        return self.environment

    def get_scorecard(self):
        return {"status": "ok"}


def test_run_session_uses_arc_wrapper(monkeypatch, capsys) -> None:
    fake_arc_agi = types.SimpleNamespace(
        Arcade=FakeArcade,
        OperationMode=types.SimpleNamespace(OFFLINE="offline", ONLINE="online"),
    )
    monkeypatch.setitem(sys.modules, "arc_agi", fake_arc_agi)

    exit_code = run_session(
        RuntimeConfig(
            game="hack1",
            mode="offline",
            render_mode="terminal",
            max_steps=1,
            has_api_key=False,
        ),
        seed=7,
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Completed 1 step" in captured.out