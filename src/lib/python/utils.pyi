import typing


T = typing.TypeVar('T')


class ValueRange:
    """
    Type annotation for ranged values

    SHOULD NOT BE USED FUNTIONALLY AT RUNTIME;
    only defined for type-checking purposes
    (exists as a blank class at runtime)
    """
    def __init__(self, value, min_value: T, max_value: T):
        if not min_value <= max_value:
            raise ValueError('min_value must be less than max_value')

        self.min_value = min_value
        self.max_value = max_value


    def check(self, value: T) -> bool:
        return self.min_value <= value <= self.max_value


unit_float = typing.Annotated[float, ValueRange[-1, 1]]


def clamp(value: T, min_value: T, max_value: T) -> T:
    '''Clamp value to min_value and max_value'''


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


def remove_dunder_attrs(dict_: dict) -> dict:
    ...


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
    def __init__(self, values: dict[str, typing.Any] = None) -> None:
        """
        Initialize a read-only dictionary from a preexisting dictionary;
        Keys must be str
        """
    
    @typing.overload
    def __init__(self, *args: typing.Iterable[tuple[str, typing.Any]]) -> None:
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
    
    @typing.overload
    def __getitem__(self, name: str) -> typing.Any:
        """Get item from key"""

    @typing.overload
    def __getitem__(self, name: tuple[str]) -> typing.Any:
        """Get nested item from tuple of keys"""
    
    def __setattr__(self, name: str, value: typing.Any) -> None:
        """
        Does not support attribute assignment
        
        Raises TypeError
        """
    
    def __setitem__(self, name: str, value: typing.Any) -> None:
        """
        Does not support item assignment

        Raises TypeError
        """
    
    def __delattr__(self, name: str) -> None:
        """
        Does not support attribute deletion

        Raises TypeError
        """
    
    def __delitem__(self, name: str) -> None:
        """
        Does not support item deletion

        Raises TypeError
        """


class NonwritableType(type):
    """
    When as metaclass, prevents any attribute from being set or deleted\n
    Mutable atttributes can still be modifed\n
    In the event an attribute must be modified, 
    'object.__setattr__(object, name, value)' or 
    'object.__delattr__(object, name)'
    can be used
    """
    __slots__ = ()


class SingletonType(type):
    """
    Metaclass for singleton classes
    """
    __slots__ = ()

    def __new__(
            mcls: SingletonType,
            clsname: str,
            bases: tuple,
            clsdict: dict,
            ) -> SingletonType:
        """
        Updates clsdict with _instance attribute
        """
    
    def __call__(cls: type[T], *args, **kwargs) -> T:
        """
        Overrides call phrasing of __new__ to prevent __init__ calls
        """
    
    def get_instance(cls, *args, **kwargs) -> T:
        """
        Uses _instance attribute to check if an instance already exists
        """


def avg(*args: typing.Any) -> typing.Any:
    """
    Returns the average of the given arguments
    """


@typing.overload
def optional_average_method_wrapper(
        method_name: typing.Callable,
        object_list: list,
        average_default = False,
        ) -> typing.Callable:
    """
    Wraps the given method such that it adds and average keyword argument to the method call.

    If average is True, the method will return the average of the values returned by the method call.
    If average is False, the method will return the list of values returned by the method call.
    """

@typing.overload
def optional_average_method_wrapper(
        attr_name: str,
        object_list: list,
        average_default = False,
        ) -> typing.Callable:
    """
    Wraps the given method such that it adds and average keyword argument to the method call.

    If average is True, the method will return the average of the values returned by the method call.
    If average is False, the method will return the list of values returned by the method call.
    """