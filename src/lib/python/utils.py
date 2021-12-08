from __future__ import annotations
import functools
if __name__ == '__main__':
    import os
    import site
    os.chdir('src')
    site.addsitedir(os.getcwd())

import math


class ValueRange: ...


unit_float = None


def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)


def deadzone(
        input,
        power=2,
        lower_maxzone=-1,
        lower_deadzone=-0.1,
        higher_deadzone=0.1,
        higher_maxzone=1,
        ):
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
    __slots__ = '_dict',

    def __init__(self, *args, **kwargs):
        if not args:
            values = {}
        
        try:
            if len(args) == 1:
                values = dict(args[0]) or {}
            else:
                values = dict(args)
        except (TypeError, ValueError) as e:
            raise ValueError(
                'ReadonlyDict cannot be initialized with given argument(s)'
            ) from e
        
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
    
    def __getitem__(self, name):
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
    
    def __getattr__(self, name: str):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(*e.args) from e

    def _getdict(self) -> dict:
        return object.__getattribute__(self, '_dict')

    def __iter__(self):
        return self._getdict().keys()

    def __str__(self):
        return str(self._getdict())

    def __setattr__(self, name: str, value) -> None:
        raise TypeError(f"type '{__class__}' does not support attribute assignment")
    
    def __setitem__(self, name: str, value) -> None:
        raise TypeError(f"type '{__class__}' does not support item assignment")
    
    def __delattr__(self, name: str) -> None:
        raise TypeError(f"type '{__class__}' does not support attribute deletion")
    
    def __delitem__(self, name: str) -> None:
        raise TypeError(f"type '{__class__}' does not support item deletion")

    def __contains__(self, name: str):
        return name in self._getdict().keys()
    
    def __repr__(self) -> str:
        return f'constantdict({dict(self._getdict())})'
    
    def __eq__(self, other) -> bool:
        if isinstance(other, dict):
            return self._getdict() == other
        if isinstance(other, ReadonlyDict):
            return self._getdict() == other._getdict()
        try:
            return self._getdict() == ReadonlyDict(other)._getdict()
        except TypeError:
            return False


class NonwritableType(type):
    __slots__ = ()
    
    def __setattr__(self, name: str, value) -> None:
        raise TypeError('Nonwritable attributes cannot be set')

    def __delattr__(self, name: str) -> None:
        raise TypeError('Nonwritable attributes cannot be deleted')


class SingletonType(type):
    __slots__ = ()

    def __new__(
            mcls: SingletonType,
            clsname: str,
            bases: tuple,
            clsdict: dict,
            ) -> SingletonType:
        clsdict.update({'_instance': None})
        return super().__new__(mcls, clsname, bases, clsdict)

    def __call__(cls, *args, **kwargs):
        return cls.get_instance(*args, **kwargs)

    def get_instance(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = cls.__new__(*args, **kwargs)
        return cls._instance


def avg(*args):
    return sum(args) / len(args)


@functools.singledispatch
def optional_average_method_wrapper(
        method_or_attr_name,
        object_list: list, 
        average_default=False
        ):
    pass

@optional_average_method_wrapper.register
def _(method, object_list: list, average_default=False):
    
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


if __name__ == '__main__':
    print('Testing lib.py.utils')

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

    try:
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
    except AssertionError as e:
        print('ReadonlyDict test failed')
        raise
    
    print('ReadonlyDict tests succeded')

    print('pyutils.py tests succeded')