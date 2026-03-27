from arcengine import ARCBaseGame, GameAction, Level, Sprite


class Hack(ARCBaseGame):
    """Tiny bundled game used to prove local ARC wiring works."""

    def __init__(self, seed: int = 0) -> None:
        level = Level(
            sprites=[Sprite([[1]], name="marker", x=0, y=0)],
            grid_size=(8, 8),
            name="Smoke",
        )
        super().__init__(
            game_id="hack1",
            levels=[level],
            available_actions=[GameAction.ACTION1.value],
            seed=seed,
        )

    def step(self) -> None:
        if self.action.id == GameAction.ACTION1:
            self.win()
        self.complete_action()