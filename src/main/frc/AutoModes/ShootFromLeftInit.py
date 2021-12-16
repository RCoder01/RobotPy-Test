from wpilib import SmartDashboard
from frc.AutoModes.AutoMode import AutoMode
from frc.robot.Drivetrain import Drivetrain
from frc.robot.Shooter import Shooter

class ShootFromLeftInit(AutoMode):

    gyroValue = 0

    def ShootFromLeftInit(self) -> None:
        super()
        self.shooter = Shooter.getInstance()
        self.drivetrain = Drivetrain.getInstance()

    def run(self) -> None:

        SmartDashboard.putNumber("velocity of shooter", self.shooter.getVelo())
        # self.lookForTarget(2, 0.1, false, 0)
        # self.shootFar(3, 1)
    
        self.turnToTarget(1, 0, 0, 157.5)
        self.driveStraight(3, -95, True, -0.9, 0)
        self.turnToTarget(1, 0, 0, -22.5)
        self.driveStraight(3, -95, False, 0, 0)
        self.turnToTarget(1, 0, 0, 35)

    @classmethod
    def getGyro(cls) -> float:
        return cls.gyroValue