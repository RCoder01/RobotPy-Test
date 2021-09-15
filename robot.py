import commands2
import wpilib
import wpilib.drive

class Robot(commands2.TimedCommandRobot):
    
    def robotInit(self):
        pass


if __name__ == '__main__':
    wpilib.run(Robot)