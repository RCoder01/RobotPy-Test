import functools
from typing import Any, Callable, Union, final
import ctre
import wpilib
from wpilib import SpeedControllerGroup

from lib.py.utils import avg, T


def getTalonEncoders(*talons: ctre.WPI_TalonFX
        ) -> Union[
            ctre.TalonFXSensorCollection,
            tuple[ctre.TalonFXSensorCollection, ...],
        ]:
    if len(talons) == 1:
        return talons[0].getSensorCollection()
    return tuple(talon.getSensorCollection() for talon in talons)


@functools.singledispatch
def optional_average_method_wrapper(
        method_or_attr_name: Union[Callable, str],
        object_list: list, 
        average_default=False
        ):
    pass

@optional_average_method_wrapper.register
def _(method: Callable, object_list: list, average_default=False):
    
    @functools.wraps(method)
    def wrapper(*args, average=average_default, **kwargs):
        val_list = [method(self, *args, **kwargs) for self in object_list]
    
        if average:
            return avg(val_list)
        return val_list

    return wrapper

@optional_average_method_wrapper.register
def _(attr_name: str, object_list: list, average_default=False):
    
    def wrapper(*args, average=average_default, **kwargs):
        attr_list = []
        
        for obj in object_list:
            attr = getattr(obj, attr_name)
            if callable(attr):
                attr_list.append(attr(*args, **kwargs))
            else:
                attr_list.append(attr)
    
        if average:
            return avg(attr_list)
        return attr_list

    return wrapper


# def optional_average_map_wrapper(
#         method_or_attr_name: Union[Callable, str],
#         object_list: list,
#         average_default = False,
#         ) -> Callable:
    
#     if callable(method_or_attr_name):
#         @functools.wraps(method_or_attr_name)
#         def wrapper(*args, average=average_default, **kwargs):
#             val_list = [method_or_attr_name(self, *args, **kwargs) for self in object_list]
#             if average:
#                 return avg(val_list)
#             return val_list
        
#         return wrapper
    
#     def wrapper(*args, average=average_default, **kwargs):
#         attr_list = []
        
#         for obj in object_list:
#             attr = getattr(obj, method_or_attr_name)
#             if callable(attr):
#                 attr_list.append(attr(*args, **kwargs))
#             else:
#                 attr_list.append(attr)
    
#         if average:
#             return avg(attr_list)
#         return attr_list

#     return wrapper

@final
class WPI_TalonFXCollection(wpilib.SpeedControllerGroup):
    """
    SpeedControllerGroup for a list of WPI_TalonFXs.

    Has the same methods as a WPI_TalonFX and SpeedControllerGroup and can be treated as one.
    """
    __slots__ = 'mMotorList',

    def __init__(self, *args: Union[int, ctre.WPI_TalonFX]) -> None:
        self.mMotorList = []
        for arg in args:
            if isinstance(arg, int):
                self.mMotorList.append(ctre.WPI_TalonFX(arg))
            else:
                self.mMotorList.append(arg)

        SpeedControllerGroup.__init__(self, *self.mMotorList)
    
    def __getattr__(self, name: str, list_: bool = False) -> Any:
        
        if hasattr(ctre.WPI_TalonFX, name):
            if list_:
                return [getattr(talon, name) for talon in self.mMotorList]

            if callable(getattr(ctre.WPI_TalonFX, name)):
                return optional_average_method_wrapper(
                    name,
                    self.mMotorList,
                    True,
                )
            
            return [getattr(motor, name) for motor in self.mMotorList]
        
        raise AttributeError(f'{self.__class__.__name__} has no attribute {name}')
    
    def get_talon_attr(self, name: str, list_: bool = False) -> Any:
        return self.__getattr__(name, list_)


@final
class TalonFXSensorCollectionCollection():
    """
    Acts as a TalonFXSensorCollection which returns optionally averaged sensor values for a list of sensors.
    """
    __slots__ = 'mSensors',

    def __init__(self, *args: ctre.TalonFXSensorCollection) -> None:
        self.mSensors = args

    def __getattribute__(self, name: str) -> Any:
        if name in __class__.__slots__:
            return object.__getattribute__(self, name)
        
        super_attr = ctre.TalonFXSensorCollection.__getattribute__(name)
        
        if callable(super_attr):
            return optional_average_method_wrapper(
                name,
                self.mSensors,
            )
        
        return super_attr