from wpilib import SmartDashboard

from frc.AutoModes.AutoMode import AutoMode
from frc.robot.Drivetrain import Drivetrain
from frc.robot.Shooter import Shooter

class ShootFromCenterInit(AutoMode):

    gyroValue = 0

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        self.shooter = Shooter.getInstance()
        self.drivetrain = Drivetrain.getInstance()
        
        SmartDashboard.putNumber("velocity of shooter", self.shooter.getVelo())
        self.lookForTarget(2, 0.1, False, 0)
        self.shootFar(3, 1)
    
        self.turnToTarget(1, 0, 0, 170)
        self.driveStraight(3, -85, False, 0, 0)
        self.turnToTarget(0.8, 0, 0, 247.5)
        self.driveStraight(2, -27, False, 0, 0)
        self.turnToTarget(0.8, 0, 0, 337.5)
        self.driveStraight(3, -64, True, -0.9, 0)

    @classmethod
    def getGyro(cls) -> float:
        return cls.gyroValue