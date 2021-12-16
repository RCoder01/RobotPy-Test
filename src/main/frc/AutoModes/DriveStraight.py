from frc.AutoModes.AutoMode import AutoMode

class DriveStraight(AutoMode):
    def __init__(self):
        super().__init__()

    def run(self) -> None:
        # self.lookForTarget(2, 0.2, true, 5000)
        self.driveStraight(2, 20, False, 0, 0)