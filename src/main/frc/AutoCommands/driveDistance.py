from frc.AutoCommands.AutoCommandBase import AutoCommandBase

from frc.robot.Constants import Constants
from frc.robot.Drivetrain import Drivetrain
from frc.robot.Intake import Intake
from frc.robot.LEDs import LEDs
from frc.robot.Shooter import Shooter

class driveDistance(AutoCommandBase):

    def __init__(self, timeout: float, distance: float, rollerDown: bool, rollerSpeed: float, intakeSpeed: float):
        super().__init__(timeout)

        self.distance = distance
        self.rollerDown = rollerDown
        self.rollerSpeed = rollerSpeed
        self.intakeSpeed = intakeSpeed

        self.drivetrain = Drivetrain.getInstance()
        self.intake = Intake.getInstance()
        self.shooter = Shooter.getInstance()

        # convert time to distance when encoders finished

        self.previousSensorValue = False

    def init(self):
        self.drivetrain.driveRotations(-self.distance,-self.distance)

    def run(self):

        self.intake.barDown(self.rollerDown)
        self.intake.beltMove(self.intakeSpeed)
        self.intake.ingest(self.rollerSpeed)
        
        if self.highSensorState() == "new ball in":
            self.intake.resetBeltEncoder()
            LEDs.setColor(-0.29) # blue light chase
            self.intake.beltMove(0.5)
            self.shooter.launchNoPID(0.3)
        else:
            self.shooter.launchNoPID(0)
        
        if self.intake.getBeltEncoder() < Constants.BELT_BALL_MOVED:
            self.intake.setFeederBrake()
            self.intake.beltMove(0)
        else:
            self.intake.setFeederCoast()

    def end(self) -> None:
        self.drivetrain.stop()
        self.intake.stop()
        self.shooter.stop()

    def getCommandName(self) -> str:
        return "Drive Distance"

    def highSensorState(self) -> str:
        if not self.previousSensorValue and self.intake.getHighSensor():
            print("new ball in")
            return "new ball in"

        if not self.previousSensorValue and not self.intake.getHighSensor():
            return "no ball in"

        self.previousSensorValue = self.intake.getHighSensor()

        return "same ball in"