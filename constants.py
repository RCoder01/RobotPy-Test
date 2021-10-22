import abc
from collections import Hashable
from typing import Any, Iterator, Sequence, Type, Union, overload


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
    def __init__(self, values: dict[Hashable, Any] = None):
        """
        Initialize a read-only dictionary from a preexisting dictionary;
        Keys must be of type str
        """
    
    @overload
    def __init__(self, *args: Sequence[tuple[Hashable, Any]]):
        """
        Initialize a read-only dictionary from a list/tuple of key-value pairs;
        Keys must be hashable
        """

    def __init__(self, *args) -> None:

        try:
            if not args:
                values = {}
            elif len(args) == 1:
                values = dict(args[0]) or {}
            else:
                values = dict(args)
        except TypeError:
            raise TypeError('ReadonlyDict cannot be initialized with given argument(s)')
        
        self._dict = {}

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
        if name in self._dict:
            return self._dict[name]
        try:
            if len(name) == 1:
                return self[name[0]]
            return self[name[0]][name[1:]]
        except (TypeError, IndexError):
            raise IndexError('Index is not of type str or sequence[str]')

    def _getdict(self) -> dict:
        return self._dict

    def __iter__(self) -> Iterator:
        return self._getdict().items()

    def __str__(self) -> Any:
        return str(self._consts)

    def __getattr__(self, name: str) -> Any:
        return self[name]

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError('Constants cannot be changed')
    
    def __setitem__(self, name: str, value: Any) -> None:
        raise AttributeError('Constants cannot be changed')
    
    def __delitem__(self, name: str) -> None:
        raise AttributeError('Constants cannot be deleted')

    def __contains__(self, name: str) -> Any:
        return name in self._getdict()
    
    def __repr__(self) -> str:
        return str(self._getdict())
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, dict):
            return self._getdict() == other
        if isinstance(other, ReadonlyDict):
            return self._getdict() == other._getdict()
        try:
            return self._getdict() == ReadonlyDict(other)._getdict()
        except TypeError:
            return False


class Interface():
    kDriverControllerPort = 0
    kManipControllerPort = 1


class Drivetrain():
    kLeftMotorIDs = ()
    kRightMotorIDs = ()


class Elevator():
    kMotorIDs = ()
    kPIDConstants = {'Kp': 0, 'Ki': 0, 'Kd': 0}


if __name__ == '__main__':
    
    test_instance = ReadonlyDict({
        'first': 1,
        'second': 2,
        'string': 'abcde',
        'int_list': [5, 6, 7, 8, 9]
        ''
    })

    #Normal lookup
    assert test_instance['first'] == 1
    assert test_instance['string'] == 'abcde'

    

    #Equivalent to B
    C = ReadonlyDict({
        ('a', 2),
        ['b', 3],
    })
