from wpilib import Timer

from frc.AutoCommands.AutoCommandBase import AutoCommandBase
from frc.robot.Intake import Intake
from frc.robot.Limelight import Limelight
from frc.robot.Shooter import Shooter
from frc.robot.Utils import Utils

class shootFar(AutoCommandBase):

    def __init__(self, timeout: float, beltSpeed: float) -> None:

        super().__init__(timeout)
        self.beltSpeed = beltSpeed
        
        self.shooter = Shooter.getInstance()
        self.intake = Intake.getInstance()

    def init(self) -> None:
        pass

    def run(self) -> None:
        Limelight.ledsOn()

        self.shooter.hoodForward()
        self.shooter.launch(Utils.autoPower())

        Timer.delay(1)

        self.intake.beltMove(self.beltSpeed)

    def end(self) -> None:

        self.shooter.hoodBack()
        self.shooter.stop()
        self.intake.stop()

    def getCommandName(self) -> str:
        return "shootFar"