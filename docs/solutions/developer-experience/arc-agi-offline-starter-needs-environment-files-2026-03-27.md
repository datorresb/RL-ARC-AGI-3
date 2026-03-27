---
title: ARC offline starter needs environment_files assets
category: developer-experience
date: 2026-03-27
tags:
  - arc-agi
  - offline-mode
  - setup
  - starter
problem_type: developer_experience
component: tooling
root_cause: incomplete_setup
resolution_type: environment_setup
severity: medium
---

## Problem

The repo initially installed the `arc-agi` toolkit and tried to run `ls20` in offline mode, but the local starter crashed before a real game session could begin.

## Symptoms

- `Game ls20 not found in scanned environments. Available games: []`
- `Starter run failed: 'NoneType' object has no attribute 'reset'`
- The Python dependency install succeeded, but the advertised offline smoke path still failed.

## What Didn't Work

- Assuming the `arc-agi` package bundles offline game assets.
- Treating `Arcade(operation_mode=OperationMode.OFFLINE)` as enough to make official games like `ls20` available locally.

## Solution

Bundle a tiny local game inside `environment_files/` and point the starter at that directory explicitly.

```python
from arc_agi import Arcade, OperationMode

arc = Arcade(
    operation_mode=OperationMode.OFFLINE,
    environments_dir="environment_files",
)
env = arc.make("hack1", render_mode="terminal")
```

The bundled local environment needs both pieces:

- `environment_files/<game-id>/metadata.json`
- `environment_files/<game-id>/<class_name>.py` or lowercase equivalent

In this repo, the working smoke asset is:

- [environment_files/hack1/metadata.json](/workspaces/RL-ARC-AGI-3/environment_files/hack1/metadata.json)
- [environment_files/hack1/hack.py](/workspaces/RL-ARC-AGI-3/environment_files/hack1/hack.py)

## Why This Works

`arc_agi` offline mode scans `environments_dir` recursively for `metadata.json` files, then loads the matching game class from the local directory. Without those assets, `Arcade.make()` returns `None` in offline mode, even when the Python package is installed correctly.

## Prevention

- Do not advertise an offline smoke test unless the repo actually ships local `environment_files/` assets.
- Pass `environments_dir` explicitly from starter code so local assets resolve independently of the caller's working directory.
- Keep at least one bundled smoke game in the repo, even if normal hackathon work later uses online tasks like `ls20`.
- Run both the Python tests and the setup verifier before claiming the environment is ready.