from collections import namedtuple
from typing import _T, Any, Type


class _Constants_Set():
    def __init__(values: dict = {}):
        for k, v in values.items():
            if not isinstance(k, str):
                raise TypeError("Constant keys must be of type 'str'")
            

'''
class _BaseConstant():
    def __new__(cls: Type[_T]) -> _T:
        """Prevent constants classes from being instantiated"""

        raise TypeError('Constant cannot be instantiated')
    
    def __setattr__(self, name: str, value: Any) -> None:
        pass


class _Constant():
    def __init__(self, value):
        self._value = value
    
    def __get__(self, obj, objtype=None):
        return self._value

    def __set__(self, obj, value):
        raise AttributeError('Constants cannot be changed')


def _ConstantClass(cls) -> object:
    default_dict = type('', (), {}).__dict__.keys()
    unique_attrs = [attr for attr in cls.__dict__.keys() if attr not in default_dict]
    
    return type(
        cls.__name__,
        (_BaseConstant,),
        {attr: _Constant(getattr(cls, attr)) for attr in unique_attrs},
    )()

@_ConstantClass
class Interface():
    kDriverControllerPort = 0
    kManipControllerPort = 1

@_ConstantClass
class Drivetrain():
    kLeftMotorIDs = ()
    kRightMotorIDs = ()

@_ConstantClass
class Elevator():
    kMotorIDs = ()
    kPIDConstants = {'Kp': 0, 'Ki': 0, 'Kd': 0}
'''