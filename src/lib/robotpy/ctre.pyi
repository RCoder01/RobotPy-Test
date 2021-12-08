import typing

import ctre
import wpilib


def getTalonEncoders(
        *talons: ctre.WPI_TalonFX
        ) -> typing.Union[
            ctre.TalonFXSensorCollection, 
            tuple[ctre.TalonFXSensorCollection, ...]
        ]:
    """
    Gets the sensor collections for a list of TalonFXs.
    """


@typing.final
class WPI_TalonFXCollection(wpilib.SpeedControllerGroup, ctre.WPI_TalonFX):
    """
    SpeedControllerGroup for a list of WPI_TalonFXs.

    Has the same methods as a WPI_TalonFX and SpeedControllerGroup and can be treated as one.
    """
    __slots__ = 'mMotorList',

    def __init__(self, *args: typing.Union[int, ctre.WPI_TalonFX]) -> None: ...


# @typing.final
# class TalonFXSensorCollectionCollection():
#     """
#     Acts as a TalonFXSensorCollection which returns optionally averaged sensor values for a list of sensors.
#     """
#     __slots__ = 'mSensors',

#     def __init__(self, *args: ctre.TalonFXSensorCollection) -> None: ...

