from __future__ import annotations
import math
import typing
from typing import Any, Iterator, Type, TypeVar, Union


T = TypeVar('T')


class unit_float(float):
    """A floating point number value between -1 and 1"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not(-1 <= self <= 1):
            raise ValueError('unit_float must be in range [-1, 1]')
        

def deadzone(
        input: unit_float,
        power: float = 2,
        lower_maxzone: unit_float = -1,
        lower_deadzone: unit_float = -0.1,
        higher_deadzone: unit_float = 0.1,
        higher_maxzone: unit_float = 1,
        ) -> unit_float:
    """
    Highly customizable deadzone function, 
    Follows equations at https://www.desmos.com/calculator/yt5brsfh1m

    :param input:
    The value to be set into deadzone
    :param power:
    The power to which the function should be taken;
    1 is linear, 2 is quadratic, etc.
    :param lower_maxzone:
    The negative point past which all inputs return -1
    :param lower_deadzone:
    The negative point past which all less inputs return 0
    :param higher_deadzone:
    The positive point past which all less inputs return 0
    :param higher_maxzone:
    The positive point at which all past inputs return 1

    :returns:
    Input modified by the different parameters

    Values must follow:
    -1 <= lower_maxzone < lower_deadzone <= 0
    <= higher_deadzone < higher_maxzone <= 1
    or ValueError will be raised
    """
    if not(
        -1 <= lower_maxzone < lower_deadzone <= 0
        <= higher_deadzone < higher_maxzone <= 1
    ):
        raise ValueError(
            'The following must be true: '
            '-1 <= lower_maxzone < lower_deadzone <= 0'
            '<= higher_deadzone < higher_maxzone <= 1'
        )
    if not(power >= 0):
        raise ValueError('Power must be greater than or equal to zero')
    
    # Depedning on range, use a different output formula
    if input <= lower_maxzone:
        return -1
    if lower_maxzone < input < lower_deadzone:
        return math.pow(
            (-input + lower_deadzone) / (lower_deadzone - lower_maxzone),
            power,
        )
    if lower_deadzone <= input <= higher_deadzone:
        return 0
    if higher_deadzone < input < higher_maxzone:
        return math.pow(
            (input - higher_deadzone) / (higher_maxzone - higher_deadzone),
            power,
        )
    if higher_maxzone <= input:
        return 1


def remove_dunder_attrs(dict_: dict) -> dict:
    return {k: v for k, v in dict_.items() if not(k.startswith('__') and k.endswith('__'))}


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
    def __init__(self, *args: Union[list, tuple][tuple[str, Any]]) -> None:
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
            raise TypeError(
                'ReadonlyDict cannot be initialized with given argument(s)'
            )
        
        values.update(kwargs)

        object.__setattr__(self, '_dict', {})
        
        for k, v in values.items():
            # Key must be a string
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
        
        raise TypeError(
            f'Object of type {type(name).__name__} '
            'does not match required type of (str, tuple)'
        )
    
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


class SingletonType(type):
    """
    Metaclass for singleton classes
    """
    def __new__(
            mcls: SingletonType,
            clsname: str,
            bases: tuple,
            clsdict: dict,
            ) -> SingletonType:
        """
        Updates clsdict with _instance attribute
        """
        clsdict.update({'_instance': None})
        return super(SingletonType, mcls).__new__(mcls, clsname, bases, clsdict)

    def __call__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        """
        Overrides call phrasing of __new__ to prevent __init__ calls
        """
        return cls.get_instance(*args, **kwargs)

    def get_instance(cls: Type[T], *args, **kwargs) -> T:
        """
        Uses _instance attribute to check if an instance already exists
        """
        if cls._instance is None:
            cls._instance = cls.__new__(*args, **kwargs)
        return cls._instance


if __name__ == '__main__':
    print('Testing pyutils.py')

    test_object = object()
    
    print('Testing ReadonlyDict')
    
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

    # Testing
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
    assert test_instance.dict['object2'] is None
    
    print('ReadonlyDict tests succeded')

    print('pyutils.py tests succeded')