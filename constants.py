

class Interface():
    kDriverControllerPort = 0
    kManipControllerPort = 1

class Drivetrain():
    kLeftMotorIDs = []
    kRightMotorIDs = []

class Elevator():
    kMotorIDs = []
    kPIDConstants = {
        'Kp': 0,
        'Ki': 0,
        'Kd': 0,
    }