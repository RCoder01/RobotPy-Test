
class Constant():
    def __setattr__(self, name: str, value) -> None:
        pass

class Interface(Constant):
    kDriverControllerPort = 0
    kManipControllerPort = 1

class Drivetrain(Constant):
    kLeftMotorIDs = []
    kRightMotorIDs = []

class Elevator(Constant):
    kMotorIDs = []
    kPIDConstants = {'Kp': 0, 'Ki': 0, 'Kd': 0}