if __name__ == '__main__':
    import os
    import site
    os.chdir('src')
    site.addsitedir(os.getcwd())

import commands2
import wpilib
import wpilib.drive

import frc.constants as constants
import frc.subsystems as subsystems

class Robot(commands2.TimedCommandRobot):
    
    def robotInit(self) -> None:
        self.container = RobotContainer()

    def autonomousInit(self) -> None:
        self.autonomousCommand = self.container.getAutonomousCommand()
    
    def teleopInit(self) -> None:
        self.autonomousCommand.cancel()

    def teleopPeriodic(self) -> None:
        self.container.teleopPeriodic()
    
    def testInit():
        commands2.CommandScheduler.getInstance().cancelAll()


class RobotContainer():
    def __init__(self):
        self.driver = wpilib.Joystick(constants.Interface.kDriverControllerPort)
        self.manip = wpilib.Joystick(constants.Interface.kManipControllerPort)

        self.drivetrain = subsystems.Drivetrain()

    
    def getAutonomousCommand(self) -> commands2.Command:
        pass

    def teleopPeriodic(self) -> None:
        pass



if __name__ == '__main__':
    # wpilib.run(Robot)
    print('robot :)')