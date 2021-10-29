from __future__ import annotations

from utils import ConstantsClass


class Interface(ConstantsClass):
    kDriverControllerPort = 0
    kManipControllerPort = 1


class Drivetrain(ConstantsClass):
    kLeftMotorIDs = ()
    kRightMotorIDs = ()


class Elevator(ConstantsClass):
    kMotorIDs = ()

    class kPIDConstants(ConstantsClass):
        Kp = 0
        Ki = 0
        Kd = 0
