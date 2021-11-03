from __future__ import annotations
import typing
from typing import Any, Generator, Type
import warnings

import commands2

from pyutils import T, NonwritableType, SingletonType, remove_dunder_attrs


class ConstantsType(NonwritableType):
    """
    Defines a get item and repr method
    """
    def __new__(mcls: ConstantsType, clsname: str, bases: tuple, clsdict: dict) -> ConstantsType:
        """
        Checks for potentially dubious keys attribute
        """
        if 'keys' in clsdict:
            warnings.warn('Defining a keys attribute may cause issues with "**" unpacking syntax', UserWarning)
        return super(ConstantsType, mcls).__new__(mcls, clsname, bases, clsdict)
    
    @typing.overload
    def __getitem__(self, name: str) -> Any:
        """Get item from key"""

    @typing.overload
    def __getitem__(self, name: tuple[str]) -> Any:
        """Get nested item from tuple of keys"""

    def __getitem__(self, name) -> Any:
        if not isinstance(name, (str, tuple)):
            raise TypeError(f'Items must be of type str or tuple[str], not {type(name)}')
        
        try:
            if name in self.__dict__:
                return getattr(self, name)
            # If name is a tuple, iterate over sub-objects and their attributes
            if isinstance(name, tuple):
                obj = self

                for item in name:
                    # If it has items, check only those
                    # Otherwise, check attributes
                    if hasattr(obj, '__getitem__'):
                        obj = obj[item]
                    else:
                        obj = getattr(obj, item)
                
                return obj
        
        except AttributeError as e:
            raise KeyError(*e.args) from e
        except KeyError:
            raise

        raise KeyError(f'Attribute(s) {name} not in {self}')
    
    # Taken practically directly from types.SimpleNamespace documentation page
    def __repr__(self) -> str:
        return f'{self.__name__}({", ".join([f"{k}={v!r}" for k, v in remove_dunder_attrs(self.__dict__).items()])})'
    
    def keys(self) -> tuple:
        return tuple(k for k, _ in remove_dunder_attrs(self.__dict__).items())

    def values(self) -> tuple:
        return tuple(v for k, v in remove_dunder_attrs(self.__dict__).items())

    def items(self) -> tuple:
        return tuple((k, v) for k, v in remove_dunder_attrs(self.__dict__).items())
    
    def __iter__(self) -> Generator:
        return self.keys().__iter__()


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


class SingletonSubsystemType(SingletonType, type(commands2.Subsystem)):
    """
    Primarily to create valid metaclass for subclasses of commands2.Subsystem and SingletonType
    """
    def getInstance(cls: type[T], *args, **kwargs) -> T:
        """
        Rephrases get_instance to follow C++/Java syntax
        """
        return SingletonType.get_instance(cls, *args, **kwargs)

    def get_instance(cls: Type[T], *args, **kwargs) -> None:
        raise AttributeError('get_instance should be called using the method "getInstance"')


class SingletonSubsystem(commands2.Subsystem, metaclass=SingletonSubsystemType):
    __slots__ = ()


if __name__ == '__main__':
    test_object = object()

    class TestConstant(ConstantsClass):
        first = 1
        second = 2
        string = 'abcde'
        int_list = [5, 6, 7, 8, 9]
        class Dict_(ConstantsClass):
            negative1 = -1
            negative2 = -2
            object1 = test_object
            object2 = None

    # Testing
    assert issubclass(TestConstant, ConstantsClass)
    assert TestConstant['first'] == 1
    assert TestConstant.second == 2
    assert TestConstant['string'] == 'abcde'
    assert TestConstant['int_list'][0] == 5
    assert TestConstant['int_list', 2] == 7

    assert issubclass(TestConstant['Dict_'], ConstantsClass)
    assert issubclass(TestConstant.Dict_, ConstantsClass)
    assert TestConstant['Dict_']['negative1'] == -1
    assert TestConstant['Dict_', 'negative2'] == -2
    assert TestConstant.Dict_.object1 is test_object
    assert TestConstant.Dict_['object2'] is None

    assert tuple(TestConstant.keys()) == ('first', 'second', 'string', 'int_list', 'Dict_')
    assert tuple(TestConstant.values()) == (1, 2, 'abcde', [5, 6, 7, 8, 9], TestConstant.Dict_)
    assert tuple(TestConstant.items()) == (('first', 1), ('second', 2), ('string', 'abcde'), ('int_list', [5, 6, 7, 8, 9]), ('Dict_', TestConstant.Dict_))
    assert 'first' in TestConstant
    assert tuple(item for item in TestConstant) == TestConstant.keys()
    assert {**TestConstant} == dict(TestConstant.items())