from collections import namedtuple
from typing import _T, Any, Iterator, Type, Union, overload


class _ConstantClass(): ...


class _Constant():
    def __init__(self, values: dict = {}):
        self._consts = {}
        for k, v in values.items():
            
            #Key must be a string
            if not isinstance(k, str):
                raise TypeError("Constant keys must be of type 'str'")
            
            if isinstance(v, dict):
                self._consts[k] = _Constant(v)
            elif isinstance(v, list):
                self._consts[k] = tuple(v)
            else:
                self._consts[k] = v

    @overload
    def __getitem__(self, name: str) -> Any:
        return self._consts[name]

    @overload
    def __getitem__(self, name: tuple[str]) -> Any:
        if len(name) == 1:
            return self[name[0]]
        return self[name[0]][name[1:]]

    def __dict__(self) -> dict:
        _dict = {}
        for k, v in self._consts:
            if isinstance(v, _Constant):
                v = dict(_Constant)
            _dict[k] = v
        return _dict

    def __iter__(self) -> Iterator:
        return self.__dict__().items()

    def __str__(self) -> Any:
        return str(self._consts)

    def __getattribute__(self, name: str) -> Any:
        self[name]

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError('Constants cannot be changed')

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