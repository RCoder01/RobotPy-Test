import abc

from frc.AutoCommands.AutoCommandBase import AutoCommandBase;
from frc.AutoCommands.driveDistance import driveDistance;
from frc.AutoCommands.lookForTarget import lookForTarget;
from frc.AutoCommands.turnToTarget import turnToTarget;
from frc.AutoCommands.waitTime import waitTime;
from frc.AutoCommands.shootFar import shootFar;

class AutoMode(abc.ABC):
    def start(self) -> None:
        self.run()

    @abc.abstractmethod
    def run(self) -> None: ...

    def driveStraight(self, seconds: float, distance: float, rollerDown: bool, rollerSpeed: float, intakeSpeed: float) -> None:
        self.runCommand(driveDistance(seconds, distance, rollerDown, rollerSpeed, intakeSpeed))

    def lookForTarget(self, seconds: float, power: float, isLeft: bool, shootSpeed: float) -> None:
        self.runCommand(lookForTarget(seconds, power, isLeft, shootSpeed))

    def waitTime(self, seconds: float) -> None:
        self.runCommand(waitTime(seconds))

    def shootFar(self, timeOut: float, beltSpeed: float) -> None:
        self.runCommand(shootFar(timeOut, beltSpeed))

    def turnToTarget(self, timeOut: float, power: float, distance: float, angle: float) -> None:
        self.runCommand(turnToTarget(timeOut, power, distance, angle))

    def runCommand(self, command: AutoCommandBase) -> None:
        command.execute()