from rl_arc_agi_3.main import build_parser, main


def test_parser_defaults() -> None:
    parsed = build_parser().parse_args([])

    assert parsed.game == "hack1"
    assert parsed.mode == "auto"
    assert parsed.max_steps == 5


def test_online_mode_requires_api_key(monkeypatch, capsys) -> None:
    monkeypatch.delenv("ARC_API_KEY", raising=False)

    exit_code = main(["--mode", "online", "--dry-run"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "ARC_API_KEY is required" in captured.err


def test_offline_dry_run_succeeds_without_key(monkeypatch, capsys) -> None:
    monkeypatch.delenv("ARC_API_KEY", raising=False)

    exit_code = main(["--mode", "offline", "--dry-run", "--max-steps", "1"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Dry run successful" in captured.out