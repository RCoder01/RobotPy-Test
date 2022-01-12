from rev import CANSparkMax, MotorType
import commands2
import wpilib
import wpilib.interfaces
import wpilib.drive

class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        self.leftMotors = [CANSparkMax(ID, MotorType.kBrushless) for ID in (15, 14, 13)]
        self.rightMotors = [CANSparkMax(ID, MotorType.kBrushless) for ID in (1, 2, 20)]
        self.leftMotorController = wpilib.SpeedControllerGroup(*self.leftMotors)
        self.rightMotorController = wpilib.SpeedControllerGroup(*self.rightMotors)
        self.drivetrain = wpilib.drive.DifferentialDrive(self.leftMotorController, self.rightMotorController)
        
        self.driver = wpilib.XboxController(0)
    
    def teleopPeriodic(self):
        self.drivetrain.arcadeDrive(
            self.driver.getY(wpilib.interfaces.GenericHID.Hand.kRightHand),
            self.driver.getX(wpilib.interfaces.GenericHID.Hand.kLeftHand)
        ) # Y is forward/backward, X is left/right
        wpilib.SmartDashboard.putNumber("Driver Y", self.driver.getY(wpilib.interfaces.GenericHID.Hand.kRightHand))
        wpilib.SmartDashboard.putNumber("Driver X", self.driver.getX(wpilib.interfaces.GenericHID.Hand.kLeftHand))

if __name__ == '__main__':
    wpilib.run(Robot)