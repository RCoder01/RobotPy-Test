from typing import Any

from wpilib import (
    SpeedControllerGroup,
)
from wpilib.interfaces import (
    SpeedController,
)
from ctre import TalonFX

class HeadedSpeedControllerGroup(SpeedControllerGroup):
    __slots__ = ('mMotors', 'motorType')

    def __init__(self, *args: SpeedController) -> None:
        self.mMotors = args
        self.motorType: type = type(args[0])
        if not all(map(lambda motor: type(motor) is self.motorType, args)):
            pass # Raise warning?
        super().__init__(*args)

    def __getattribute__(self, name: str) -> Any:
        try:
            return getattr(SpeedControllerGroup, name)(self)
        except AttributeError:
            outs = map(getattr(super().__getattribute__('motorType'), name), super().__getattribute__('mMotors'))
            try:
                sum(outs) / super().__getattribute__('numMotors')
            except AttributeError:
                return outs