from __future__ import annotations

from src.lib.robotpy.utils import ConstantsClass


# Any values with just a type hint are placeholders for the actual value

class Interface(ConstantsClass):
    kDriverControllerPort: int
    kManipControllerPort: int


class Drivetrain(ConstantsClass):
    kLeftMotorIDs: tuple[int]
    kRightMotorIDs: tuple[int]


class Elevator(ConstantsClass):
    kMotorIDs: tuple[int]

    class kPIDConstants(ConstantsClass):
        Kp: int
        Ki: int
        Kd: int
