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

@typing.overload
def optional_average_map_wrapper(
        method_name: typing.Callable,
        object_list: list,
        average_default = False,
        ) -> typing.Callable:
    """
    Wraps the given method such that it adds and average keyword argument to the method call.

    If average is True, the method will return the average of the values returned by the method call.
    If average is False, the method will return the list of values returned by the method call.
    """

@typing.overload
def optional_average_map_wrapper(
        attr_name: str,
        object_list: list,
        average_default = False,
        ) -> typing.Callable:
    """
    Wraps the given method such that it adds and average keyword argument to the method call.

    If average is True, the method will return the average of the values returned by the method call.
    If average is False, the method will return the list of values returned by the method call.
    """


@typing.final
class WPI_TalonFXCollection(wpilib.SpeedControllerGroup, ctre.WPI_TalonFX):
    """
    SpeedControllerGroup for a list of WPI_TalonFXs.

    Has the same methods as a WPI_TalonFX and SpeedControllerGroup and can be treated as one.
    """
    __slots__ = 'mMotorList',

    def __init__(self, *args: typing.Union[int, ctre.WPI_TalonFX]) -> None: ...


@typing.final
class TalonFXSensorCollectionCollection():
    """
    Acts as a TalonFXSensorCollection which returns optionally averaged sensor values for a list of sensors.
    """
    __slots__ = 'mSensors',

    def __init__(self, *args: ctre.TalonFXSensorCollection) -> None: ...

