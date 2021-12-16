from frc.AutoCommands.AutoCommandBase import AutoCommandBase

from frc.robot.Drivetrain import Drivetrain
from frc.robot.Limelight import Limelight
from frc.robot.Shooter import Shooter

class lookForTarget(AutoCommandBase):
	
    def __init__(self, timeOut: float, power: float, isLeft: bool, shootSpeed: float):

        super().__init__(timeOut)
        self.power = power
        self.isLeft = isLeft
        self.shootPower = shootSpeed

        self.drivetrain = Drivetrain.getInstance()
        self.shooter = Shooter.getInstance()

    def init(self): ...

    def run(self) -> None:

        Limelight.refresh()
        if Limelight.getTv() == 1:
            Limelight.ledsOn()
            self.drivetrain.setAngle(self.drivetrain.getAHRS() + Limelight.getTx())
            self.drivetrain.AutoTargetedDrive(0)


            print("Target Found")
        else:
            Limelight.ledsOn()
            # self.drivetrain.pidDisable()
            if self.isLeft:
                self.drivetrain.drive(-self.power, self.power) # turns left
            else:
                self.drivetrain.drive(self.power, -self.power) # turns rigt

            print("Searching for Target....")
            
    def end(self):
        self.drivetrain.stop()

    def getCommandName() -> str:
        return ''