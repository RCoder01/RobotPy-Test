from frc.AutoCommands.AutoCommandBase import AutoCommandBase
from frc.robot.Drivetrain import Drivetrain

class waitTime(AutoCommandBase):

    def __init__(self, timeOut: float) -> None:
        super().__init__(timeOut)
        self.drivetrain = Drivetrain.getInstance()

    def init(self) -> None: pass

    def run(self) -> None:
        self.drivetrain.stop()

    def end(self) -> None: pass

    def getCommandName(self) -> None:
        return ''