from types import MappingProxyType
from typing import Any, Iterator, Sequence, Type, Union, overload


class Immutable():
    def __init__(self, obj: Any):
        super().__setattr__('_obj', obj)
    
    def __getattribute__(self, name: str) -> Any:
        attr = getattr(super().__getattribute__('_obj'), name)
        if name == '__call__':
            return attr
        return Immutable(attr)
    
    def __setattr__(self, name: str, value: Any) -> None:
        raise TypeError('Immutable object cannot be modified')
    
    def __repr__(self) -> str:
        _repr = super().__repr__().split(' object at ')
        return f'{_repr[0]} object wrapper of {repr(super().__getattribute__("_obj"))} at {_repr[1]}'

def Immutable(obj: Any) -> Any:
    class NewObjType(type(obj)):
        def __setattr__(self, name: str, value: Any) -> None:
            raise TypeError('Immutable object cannot be modified')
    
    if isinstance(NewObjType, type):
        return NewObjType('ImmutableObject', obj.__bases__, vars(obj))
    
    return_obj = NewObjType.__new__(type(obj))
    for attr, val in vars(obj):
        super(NewObjType, return_obj).__setattr__(attr, val)
    
    return return_obj

class ReadonlyDict():
    """
    Dictionary-like object which stores key-value pairs

    Values can be accessed using the following notations: 
    ReadonlyDictObject[key],
    ReadonlyDictObject.key

    When the ReadonlyDict object is initialized, any nested dictionaries 
    (dictionary values) 
    are automatically converted to other ReadonlyDict objects

    Nested values can be accessed with the following notations 
    (works for more than two as well):
    ReadonlyDictObject[key1][key2],
    ReadonlyDictObject[key1, key2],
    ReadonlyDictObject[(key1, key2)],
    ReadonlyDictObject.key1.key2

    ReadonlyDictObject.key1 returns another ReadonlyDict object 
    with only the nested values
    """

    @overload
    def __init__(self, values: dict[str, Any] = None) -> None:
        """
        Initialize a read-only dictionary from a preexisting dictionary;
        Keys must be str
        """
    
    @overload
    def __init__(self, *args: Union[list[tuple[str, Any]], tuple[tuple[str, Any]]]) -> None:
        """
        Initialize a read-only dictionary from a list/tuple of key-value pairs;
        Keys must be str
        """
    
    @overload
    def __init__(self, **kwargs) -> None:
        """
        New read-only dictionary initialized with the name=value pairs
        Can also be used in addition to other initialization methods
        """

    def __init__(self, *args, **kwargs) -> None:
        try:
            if not args:
                values = {}
            elif len(args) == 1:
                values = dict(args[0]) or {}
            else:
                values = dict(args)
        except TypeError:
            raise TypeError('ReadonlyDict cannot be initialized with given argument(s)')
        
        values.update(kwargs)

        object.__setattr__(self, '_dict', {})
        
        for k, v in values.items():
            #Key must be a string
            if not isinstance(k, str):
                raise TypeError("ReadonlyDict keys must be of type 'str'")
            
            if isinstance(v, dict):
                self._dict[k] = ReadonlyDict(v)
            elif isinstance(v, list):
                self._dict[k] = tuple(v)
            else:
                self._dict[k] = v

    @overload
    def __getitem__(self, name: str) -> Any:
        """Get item from key"""

    @overload
    def __getitem__(self, name: tuple[str]) -> Any:
        """Get nested item from tuple of keys"""

    def __getitem__(self, name) -> Any:
        if name in self._getdict():
            return self._getdict()[name]
        try:
            if len(name) == 1:
                return self[name[0]]
            return self[name[0]][name[1:]]
        except (TypeError, IndexError):
            raise IndexError(f'Index {name} is not valid')
    
    def __getattr__(self, name: str) -> Any:
        return self[name]

    def _getdict(self) -> dict:
        return self._dict

    def __iter__(self) -> Iterator:
        return self._getdict().keys()

    def __str__(self) -> Any:
        return str(self._getdict())

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError('Constants cannot be changed')
    
    def __setitem__(self, name: str, value: Any) -> None:
        raise AttributeError('Constants cannot be changed')
    
    def __delattr__(self, name: str) -> None:
        raise AttributeError('Constants cannot be deleted')
    
    def __delitem__(self, name: str) -> None:
        raise AttributeError('Constants cannot be deleted')

    def __contains__(self, name: str) -> Any:
        return name in self._getdict().keys()
    
    def __repr__(self) -> str:
        return f'constantdict({dict(self._getdict())})'
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, dict):
            return self._getdict() == other
        if isinstance(other, ReadonlyDict):
            return self._getdict() == other._getdict()
        try:
            return self._getdict() == ReadonlyDict(other)._getdict()
        except TypeError:
            return False
    
    @property
    def __dict__(self):
        return MappingProxyType(self._getdict())


class Nonwritable(type):
    def __setattr__(self, name: str, value: Any) -> None:
        raise TypeError('Nonwritable attributes cannot be set')


class ConstantsClass(metaclass=Nonwritable): ...


class Interface(ConstantsClass):
    kDriverControllerPort = 0
    kManipControllerPort = 1


class Drivetrain(ConstantsClass):
    kLeftMotorIDs = ()
    kRightMotorIDs = ()


class Elevator(ConstantsClass):
    kMotorIDs = ()
    kPIDConstants = {'Kp': 0, 'Ki': 0, 'Kd': 0}


if __name__ == '__main__':
    
    test_instance = ReadonlyDict({
        'first': 1,
        'second': 2,
        'string': 'abcde',
        'int_list': [5, 6, 7, 8, 9]
    })

    #Normal lookup
    assert test_instance['first'] == 1
    assert test_instance['string'] == 'abcde'

    
    #Equivalent to B
    C = ReadonlyDict({
        ('a', 2),
        ['b', 3],
    })
