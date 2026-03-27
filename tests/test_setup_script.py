from __future__ import annotations

import os
import subprocess
from pathlib import Path


def test_check_arc_env_script_passes() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PATH"] = f"{Path.home() / '.local' / 'bin'}:{env.get('PATH', '')}"

    result = subprocess.run(
        [str(repo_root / "scripts" / "check_arc_env.sh")],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    output = result.stdout + result.stderr
    assert result.returncode == 0, output
    assert "Local setup is ready." in output