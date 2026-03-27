from rl_arc_agi_3.config import load_runtime_config


def test_auto_mode_defaults_to_offline_without_api_key() -> None:
    config = load_runtime_config(
        game="ls20",
        requested_mode="auto",
        render_mode="terminal",
        max_steps=3,
        env={},
    )

    assert config.mode == "offline"
    assert config.api_key_status == "not set"


def test_auto_mode_uses_online_when_api_key_exists() -> None:
    config = load_runtime_config(
        game="ls20",
        requested_mode="auto",
        render_mode="terminal",
        max_steps=3,
        env={"ARC_API_KEY": "secret-value"},
    )

    assert config.mode == "online"
    assert config.api_key_status == "set (redacted)"


def test_explicit_offline_mode_wins_over_api_key() -> None:
    config = load_runtime_config(
        game="ls20",
        requested_mode="offline",
        render_mode="terminal",
        max_steps=3,
        env={"ARC_API_KEY": "secret-value"},
    )

    assert config.mode == "offline"