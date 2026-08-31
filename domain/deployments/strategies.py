class DeploymentStrategy:
    CANARY = "CANARY"
    BLUE_GREEN = "BLUE_GREEN"
    ROLLING = "ROLLING"

    def __init__(self, strategy_type: str = ROLLING, batch_percentage: int = 25, canary_weight: float = 10.0):
        self.strategy_type = strategy_type
        self.batch_percentage = batch_percentage
        self.canary_weight = canary_weight

    def get_step_increments(self) -> list:
        if self.strategy_type == self.CANARY:
            return [10, 25, 50, 100]
        elif self.strategy_type == self.BLUE_GREEN:
            return [0, 100]
        return [25, 50, 75, 100]
