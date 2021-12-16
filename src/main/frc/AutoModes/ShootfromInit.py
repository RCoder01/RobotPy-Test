from wpilib import SmartDashboard
from frc.AutoModes.AutoMode import AutoMode
from frc.robot.Drivetrain import Drivetrain
from frc.robot.Shooter import Shooter

class ShootfromInit(AutoMode):
    gyroValue = 0

    def __init__(self) -> None:
        super().__init__()

        self.shooter = Shooter.getInstance()
        self.drivetrain = Drivetrain.getInstance()
        
    def run(self) -> None:

        SmartDashboard.putNumber("velocity of shooter", self.shooter.getVelo())
        self.lookForTarget(2, 0.1, False, 0)


        self.shootFar(3, 1)
    
        self.turnToTarget(1, 0, 0, 180)
    
    
    
        self.driveStraight(3, -100, True, -0.9, 0)
    
        self.turnToTarget(0.8, 0, 0, 0)
    
        self.driveStraight(2, -40, False, 0, 0)
    
        self.lookForTarget(1, 0.1, False, 0)
    
        self.shootFar(4, 1)

    @classmethod
    def getGyro(cls) -> float:
        return cls.gyroValue