import commands2
import wpilib
import wpilib.drive

class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        print('init?')
        # self.leftMotors = [ctre.WPI_TalonFX(ID) for ID in (15, 14, 13)]
        # self.rightMotors = [ctre.WPI_TalonFX(ID) for ID in (1, 2, 20)]
        # self.leftMotorController = wpilib.SpeedControllerGroup(*self.leftMotors)
        # self.rightMotorController = wpilib.SpeedControllerGroup(*self.rightMotors)
        # self.drivetrain = wpilib.drive.DifferentialDrive(self.leftMotorController, self.rightMotorController)
        
        self.driver = wpilib.Joystick(0)
    
    def teleopPeriodic(self):
        # self.drivetrain.arcadeDrive(self.driver.getY(), self.driver.getX()) # Y is forward/backward, X is left/right
        wpilib.SmartDashboard.putNumber("Driver Y", self.driver.getY())
        wpilib.SmartDashboard.putNumber("Driver X", self.driver.getX())

if __name__ == '__main__':
    wpilib.run(Robot)