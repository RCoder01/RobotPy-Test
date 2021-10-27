from types import MappingProxyType
from typing import Any, Iterator, Sequence, Type, Union, overload


def Immutable(obj):
    class ImmutableType(type(obj)):
        def __setattr__(self, name: str, value: Any) -> None:
            raise TypeError('Immutable object cannot be modified')
    
    if isinstance(obj, type):
        returnObj = ImmutableType("ImmutableTypeObject", obj.__bases__, dict(obj.__dict__))
    else:
        returnObj = object.__new__(ImmutableType)
        for name, value in obj.__dict__.items():
            object.__setattr__(returnObj, name, value)
    
    return returnObj


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
        if name == '_getdict':
            return object.__getattribute__(self, name)
        if name in self._getdict():
            return self._getdict()[name]

        try:
            if not isinstance(name, tuple):
                raise ValueError()
            if len(name) > 1:
                return self[name[0]][name[1:]]
            if name[0] == name:
                raise ValueError()
            return self[name[0]]
        except ValueError as e:
            e.val = [name] + e.val if e.args else [name]
            e.args = f'{tuple(e.val)} not found in {self}',
            raise
        except (TypeError, IndexError) as e:
            new_e = ValueError(f'{tuple(name)} not found in {self}')
            new_e.val = [name]
            raise new_e from e
        except RecursionError:
            print(name)
            raise
    
    def __getattr__(self, name: str) -> Any:
        return self[name]

    def _getdict(self) -> dict:
        return object.__getattribute__(self, '_dict')

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
        'int_list': [5, 6, 7, 8, 9],
        'dict': {
            'negative1': -1,
            'negative2': -2,
        },
    })

    #Normal lookup
    assert test_instance['first'] == 1
    assert test_instance['string'] == 'abcde'

    
    #Equivalent to B
    C = ReadonlyDict({
        ('a', 2),
        ['b', 3],
    })

    @Immutable
    class C:
        abcd = 4
        efgh = '123'