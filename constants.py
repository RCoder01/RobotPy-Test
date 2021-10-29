from __future__ import annotations
import typing
from typing import _T, Any, Iterator, Type, Union

import commands2


class ReadonlyDict:
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
    __slots__ = '_dict',

    @typing.overload
    def __init__(self, values: dict[str, Any] = None) -> None:
        """
        Initialize a read-only dictionary from a preexisting dictionary;
        Keys must be str
        """
    
    @typing.overload
    def __init__(self, *args: Union[list[tuple[str, Any]], tuple[tuple[str, Any]]]) -> None:
        """
        Initialize a read-only dictionary from a list/tuple of key-value pairs;
        Keys must be str
        """
    
    @typing.overload
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
        
        return super().__init__()

    @typing.overload
    def __getitem__(self, name: str) -> Any:
        """Get item from key"""

    @typing.overload
    def __getitem__(self, name: tuple[str]) -> Any:
        """Get nested item from tuple of keys"""

    def __getitem__(self, name) -> Any:
        if isinstance(name, str):
            if name in self._getdict():
                return self._getdict()[name]
            raise KeyError(f'{name} not found in {self!r}')

        elif isinstance(name, tuple):
            obj = self

            try:
                for attr in name:
                    if hasattr(obj, '__getitem__'):
                        obj = obj[attr]
                    else:
                        obj = getattr(obj, attr)
            except (TypeError, ValueError, LookupError, AttributeError) as e:
                raise KeyError(f'{name} not found in {self!r}') from e
            
            return obj
        
        raise TypeError(f'Object of type {type(name).__name__} does not match required type of (str, tuple)')
    
    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(*e.args) from e

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


class NonwritableType(type):
    """
    When as metaclass, prevents any attribute from being set or deleted\n
    Mutable atttributes can still be modifed\n
    In the event an attribute must be modified, 
    'object.__setattr__(object, name, value)' or 
    'object.__delattr__(object, name)'
    can be used
    """
    
    def __setattr__(self, name: str, value: Any) -> None:
        raise TypeError('Nonwritable attributes cannot be set')

    def __delattr__(self, name: str) -> None:
        raise TypeError('Nonwritable attributes cannot be deleted')


class ConstantsType(NonwritableType):
    """
    Defines a get item and repr method
    """
    @typing.overload
    def __getitem__(self, name: str) -> Any:
        """Get item from key"""

    @typing.overload
    def __getitem__(self, name: tuple[str]) -> Any:
        """Get nested item from tuple of keys"""

    def __getitem__(self, name) -> Any:
        try:
            if name in self.__dict__:
                return getattr(self, name)
            #If name is a tuple, iterate over sub-objects and their attributes
            if isinstance(name, tuple):
                obj = self

                for item in name:
                    #If it has items, check only those, otherwise, check attributes
                    if hasattr(obj, '__getitem__'):
                        obj = obj[name]
                    else:
                        obj = getattr(obj, item)
                
                return obj
        
        except AttributeError as e:
            raise KeyError(*e.args) from e
        except KeyError:
            raise

        if not isinstance(name, (str, tuple)):
            raise TypeError(f'Items must be of type str or tuple[str], not {type(name)}')
        raise KeyError(f'Attribute(s) {name} not in {self}')
    
    #Taken practically directly from types.SimpleNamespace documentation page
    def __repr__(self) -> str:
        return f'{self.__name__}({", ".join([f"{k}={v!r}" for k, v in self.__dict__.items() if k.startswith("__") and k.endswith("__")])})'


class ConstantsClass(metaclass=ConstantsType):
    """
    Unique properties of a ConstantsClass:

    - Any class attributes cannot be changed or deleted;
    new class attributes cannot be added

    - Values can be accessed using the following notations: 
    ConstantsClass[key],
    ConstantsClass.key

    - Nested values can be accessed with the following notations
    if a class contains a nested class that inherits from ConstantsClass
    (works for more than two as well):
    ConstantsClass[key1][key2],
    ConstantsClass[key1, key2],
    ConstantsClass[(key1, key2)],
    ConstantsClass.key1.key2

    - Initializing a class returns the class itself, not an instance

    - Provides a useful repr;
    similar to that of types.SimpleNamespace,
    but ignores attributes with both two leading and underscores 
    ('dunder' attributes)
    """
    __slots__ = ()

    def __new__(cls: ConstantsClass) -> ConstantsClass:
        return cls


class SingletonType(type):
    """
    Metaclass for singleton classes
    """
    def __new__(mcls: SingletonType, clsname: str, bases: tuple, clsdict: dict):
        """
        Updates clsdict with _instance attribute
        """
        clsdict.update({'_instance': None})
        return super(mcls, SingletonType).__new__(mcls, clsname, bases, clsdict)

    def __call__(cls: Type[_T], *args: Any, **kwargs: Any) -> _T:
        """
        Overrides call phrasing of __new__ to prevent __init__ calls
        """
        return cls.get_instance(*args, **kwargs)

    def get_instance(cls: Type[_T], *args, **kwargs) -> _T:
        """
        Uses _instance attribute to check if an instance already exists
        """
        if cls._instance is None:
            cls._instance = cls.__new__(*args, **kwargs)
        return cls._instance


class SingletonSubsystemType(SingletonType, type(commands2.Subsystem)):
    """
    Primarily to create valid metaclass for subclasses of commands2.Subsystem and SingletonType
    """
    def getInstance(cls: type[_T], *args, **kwargs) -> _T:
        """
        Rephrases get_instance to follow C++/Java syntax
        """
        return SingletonType.get_instance(cls, *args, **kwargs)

    def get_instance(cls: Type[_T], *args, **kwargs) -> None:
        raise AttributeError('get_instance should be called using the method "getInstance"')


class SingletonSubsystem(commands2.Subsystem, metaclass=SingletonSubsystemType):
    __slots__ = ()


class Interface(ConstantsClass):
    kDriverControllerPort = 0
    kManipControllerPort = 1


class Drivetrain(ConstantsClass):
    kLeftMotorIDs = ()
    kRightMotorIDs = ()


class Elevator(ConstantsClass):
    kMotorIDs = ()

    class kPIDConstants(ConstantsClass):
        Kp = 0
        Ki = 0
        Kd = 0


if __name__ == '__main__':
    test_object = object()
    
    test_instance = ReadonlyDict({
        'first': 1,
        'second': 2,
        'string': 'abcde',
        'int_list': [5, 6, 7, 8, 9],
        'dict': {
            'negative1': -1,
            'negative2': -2,
            'object1': test_object,
            'object2': None,
        },
    })

    #Testing
    assert isinstance(test_instance, ReadonlyDict)
    assert test_instance['first'] == 1
    assert test_instance.second == 2
    assert test_instance['string'] == 'abcde'
    assert test_instance['int_list'][0] == 5
    assert isinstance(test_instance['dict'], ReadonlyDict)
    assert isinstance(test_instance.dict, ReadonlyDict)
    assert test_instance['dict']['negative1'] == -1
    assert test_instance['dict', 'negative2'] == -2
    assert test_instance.dict.object1 is test_object
    assert test_instance.dict.object2 is None

    
    #Equivalent to B
    C = ReadonlyDict({
        ('a', 2),
        ['b', 3],
    })