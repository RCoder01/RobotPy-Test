
class Constant():
    def __new__(cls, *args, **kwargs):
        """Prevent constants classes from being instantiated"""

        raise TypeError('Constant cannot be instantiated')

class Interface(Constant):
    kDriverControllerPort = 0
    kManipControllerPort = 1

class Drivetrain(Constant):
    kLeftMotorIDs = []
    kRightMotorIDs = []

class Elevator(Constant):
    kMotorIDs = []
    kPIDConstants = {'Kp': 0, 'Ki': 0, 'Kd': 0}