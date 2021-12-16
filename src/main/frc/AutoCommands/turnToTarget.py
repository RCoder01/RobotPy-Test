import math

from frc.AutoCommands.AutoCommandBase import AutoCommandBase
from frc.robot.Drivetrain import Drivetrain
from frc.robot.Intake import Intake
from frc.robot.Shooter import Shooter


class turnToTarget(AutoCommandBase):


    def __init__(self, timeout: float, power: float, distance: float, angle: float):
        super().__init__(timeout)
        self.angle = angle

        self.shooter = Shooter.getInstance()
        self.intake = Intake.getInstance()
        self.drivetrain = Drivetrain.getInstance()

    def init(self) -> None:
        realAngle = 0

        currentAngle = self.drivetrain.getRealAngle()

        if currentAngle >= 360:
            realAngle = currentAngle % 360
        elif currentAngle < 0:
            realAngle = 360 - math.abs(currentAngle % 360)
        else:
            realAngle = currentAngle
        
        targetAngle = self.angle - realAngle
        if math.abs(targetAngle) <= 180:
            self.drivetrain.setAngle(currentAngle + targetAngle)
            print(currentAngle + targetAngle)

        if math.abs(targetAngle) > 180:
            if targetAngle > 0:
                self.drivetrain.setAngle(currentAngle + (targetAngle - 360))
                print(currentAngle + (targetAngle - 360))
            if targetAngle < 0:
                self.drivetrain.setAngle(currentAngle + (targetAngle + 360))
                self.System.out.println(currentAngle + (targetAngle + 360))

    def run(self) -> None:
        self.drivetrain.AutoTargetedDrive(0)

    def end(self) -> None:
        pass

    def getCommandName(self) -> str:
        return "Turn to target"