from __future__ import annotations

from lib.robotpy.utils import ConstantsClass, IDList


# Any values with just a type hint are placeholders for the actual value

class Interface(ConstantsClass):
    kDriverControllerPort: int
    kManipControllerPort: int


class Drivetrain(ConstantsClass):
    kLeftMotorIDs: IDList
    kRightMotorIDs: IDList


class Elevator(ConstantsClass):
    kMotorIDs: IDList

    class kPIDConstants(ConstantsClass):
        Kp: int
        Ki: int
        Kd: int
