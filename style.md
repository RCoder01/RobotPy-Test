# Style Guide for Robostangs 548 Python Robot Code #


## Two Types of Module

The robotpy/wpilib python package is essentially a wrapper of the C++ library, as described on 
[the official robotpy documentation page](https://robotpy.readthedocs.io/en/stable/2020_notes.html#why-is-everything-so-different-this-year);
so all of its structure follows a more C++/Java-like syntax. 

This is in unlike the pythonic syntax present in the Python language, Python Standard Library, other pure python libraries, etc.
This can and will mean that at least some modules will have a mixed Python and C++ syntax.

To account for this, Robotpy project modules should be divided roughly into two categories;
A Python-like section, and a section with mixed Python and C++/Java (hereinafter reffered to as Pythonic and Mixed).


### Example:

In this project, the Python-like section would include [pyutils.py](./pyutils.py),
while the mixed section would inculde [utils.py](./utils.py), [constants.py](constants.py), [subsystems.py](subsystems.py) and most other modules.

The idea behind splitting the utility functions and classes into two modules, pyutils and utils,
is to distinguish between generally Python and generally Robotpy objects.

All objects defined in [pyutils](pyutils.py) (and other future Pythonic modules) should have some forseeable use outside of a Robotpy project,
and should never import anything from the Robotpy project;
while utils should only have practical use in Robotpy projects,
sometimes only being Robotpy-specific bindings/addons/extensions of pyutils or other python objects.

One example within the utils set would be the SingletonType class, defined in [pyutils](pyutils.py).
A singleton metaclass could be used [outside of a Robotpy project](https://en.wikipedia.org/wiki/Singleton_pattern#Common_uses);
The [utils](utils.py) module then extends this metaclass and integrates it with the wpilib commands2.Subsystem into SingletonSubsystemMeta and SingletonSubsystem,
forms in which they are most likely to be used in the rest of the project.


## Whitespace-Related Detail

### **Indentation**

All modules should follow [PEP-8 outlines](https://www.python.org/dev/peps/pep-0008/#indentation); namely 4-space indentation and clear visual indents between code blocks.

Closing syntax characters are preferred to be indented to the same level as in the last line. As with all style recommendations, consistency is more important than all else.

### Example:

```
# Preferred
my_list = [
    1, 2, 3,
    4, 5, 6,
]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
)

# Not preferred, but still acceptable
my_list = [
    1, 2, 3,
    4, 5, 6,
    ]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
    )
```


### **Line Length**

### Pythonic:

In Pythonic modules, line length should be restricted to 79 characters, as per [PEP-8](https://www.python.org/dev/peps/pep-0008/#maximum-line-length).

Line breaks within statements should occur where implicit continuation is present. If you need to use a backslash (\\), there's *probably* a better way to do it.

### Mixed:

In mixed modules, because of naming conventions (outlined later) and due to general standard in C++/Java robot code, lines length is not limited.

Docstrings and multi-line comments should still be limited to 72 or 79 characters for easier readability.


## Imports

- Different libraries/packages should be imported on separate lines.
- Importing from within libraries/packages is permitted, including the use of the `from` keyword.
- Importing functions, constants, and classes from modules is permitted.
- Use of the `as` keyword to prevent name conflicts is also permitted.
- Multiple importing from the same library/package using standard syntax is permitted (subject to change).
however, if in the future merge conflicts are an issue with this suggestion, it may be reversed or changed to require multi-line `from` syntax.
- Relative imports in top-level modules are recommended as the project folder's name may be subject to be change and/or may not fit Python's module naming syntax (subject to change)
  - Attempting to absolute import from the top level may cause a SyntaxError.
  - Absolute imports within sub-modules is still permitted.
- Order of imports should be as such:
  - `__future__` imports
  - Standard Library imports
  - Other installed library/package imports
  - Robotpy imports
    - Remember that pythonic modules should not import from Robotpy, only mixed modules
  - Local imports
- Within each group, imports should be ordered alphabetically; first by library/package/module, then by sub-imports (those after the `from` keyword).
- One line of whitespace should be given between each non-empty group (`__future__` is included in the standard library, and *must* be listed first).
- The conclusion of the imports section should be followed by two blank lines.
- Any testing-specific imports can and should be placed at the beginning of the `if __name__ == '__main__'` clause (abiding by the same guidlines as above).


### Example:

```
# Package src/subsystems
from __future__ import annotations
from typing import Any, Type

import numpy as np
import requests
from requests import get
from requests.exceptions import HTTPError

import commands2
import wpilib

from .. import utils
from ..commands import Arm.Idle as ArmIdle, Drivetrain.Idle as DrivetrainIdle
from subsystems import Arm

# Alternative:
from . import subsystems.Arm as Arm

# Multi-line from syntax (should always include final trailing comma)
from ..commands import (
  Arm.Idle as ArmIdle,
  Drivetrain.Idle as DrivetrainIdle,
)

# Not Recommended:
from src import utils
```


## Comments

### **Type Hinting**

Type hints should be given in all function/method declarations (excluding self/cls). This means including descriptive, multi-level types as required. The standard library package Typing is helpful for this.

Use a type definition T when input and output objects are the same but of unknowable type.

### Example:

```
def foo(bar: int, baz: list[str], bang: Callable[[T], Union[list, tuple][Generator]]) -> T:
    frobnicate(bang)
    ...

# Alternative syntax:
def foo(
        bar: int,
        baz: list[str],
        bang: Callable[[T], Union[list, tuple][Generator]]
        ) -> T:
    frobnicate(bang)
    ...
```


### **Docstrings**

Describe the overall purpose of all classes and functions in docstrings, even if function docstrings will never be seen (as in the case of `__getitem__`).

All docstrings should *always* use double-quotes.

Should type hints not provide enough information, use :param: and :returns: in the docstring to provide additional information.
- These should appear after the main body of the docstring, first with params then with return.
- Use one param tag for each parameter.
- Add one blank line between the main body and params, then another between params and return(s).
- If a function/method includes these, it must include a tag for all parameters and return(s); selectively including them is discouraged.

### Pythonic:

Use line breaks and blank lines to ensure no single line in a docstring exceeds the 72 character mark.

### Mixed:

Try to manage length, but it may not be possible given naming conventions.

### Example:

```
def foo(bar: int) -> list[Baz]:
    """
    Returns a list of Baz instances with from 0 to bar

    :param bar: integer greater than 0

    :returns: list of Baz objects intialized with ints 0 through bar
    """
    return [Baz(bat) for bat in range(bar)]
```


### **Comments**

Include where necessary; don't over do it, don't under do it.

"Comments that contradict the code are worse than no comments. Always make a priority of keeping the comments up-to-date when the code changes!"

Comments should start with a space.

### Example:

```
...

# Adds name to all the Foo
for bar in Foo:
    Baz.do(bar, 'gary')

...
```


## Naming

### **String Literal Definitions**

### Pythonic:

Single quotes should be used whenever possible, but use double quotes instead of `\'` should a single quote need to be in a string.

When string literal definitions exceed 79 characters, use implicit string literal concatenation to spread across lines.

### Mixed:

Single quotes are preferred, but either is fine.


### **Variables**

Any names clashing with builtin python types or keywords can be suffixed with a single underscore.

### Pythonic:

Follow general python naming conventions.

### Mixed:

Variables should follow standard C++/Java and standard robot code syntax.

This includes:
- Variables should be named using lowerCamelCase.
- Private instance variables should be prefixed with a lowercase m.
- Constant variables should be prefixed with a lowercase k.

Variable names following this syntax and building off of the wpilib library can tend to get quite long, hence why line length limits have been abandoned for this category of module.

Subclass name clash prevention using double leading underscores is still permitted when necessary.

### Example:

```
# Pythonic:
normal_variable = 3
self._private_instance_variable = -5
CONSTANT_VARIABLE = 10

# Mixed:
normalVariable = 3
self.mPrivateInstanceVariable = -5
kConstantVariable = 10
```


### **Functions/Methods**

The first variable of any instance method should be `self`; The first variable of any class method should be `cls`.

The arguments of `__new__` for any metaclass should be: `mcls`, `clsname`, `bases`, `clsdict`, in that order, followed by any user-passed arguments.

`__init__` and `__new__` methods should call super methods, unless they are intentionally not called, especially in classes intended to be subclassed.

Any names clashing with builtin python types or keywords can be suffixed with a single underscore.

### Pythonic:

Follow general python naming conventions.

### Mixed:

Functions and methods should be lowerCamelCased, and private class methods should be signified by a single leading underscore.

Subclass name clash prevention using double leading underscores is still permitted when necessary.

Methods beginning and ending with double underscores (so called "dunder" methods) are still permitted and recommended to enchance functionality.

### Example:

```
from typing import Any

# Pythonic:
def foo():
    ...

class Bar:
    def __init__(self, arg_1: Any) -> None:
        return super(self, Bar).__init__(self, arg1)

    def baz(self, arg_1: Any) -> Any:
        ...
    
    @classmethod
    def class_qux(cls, arg_1: Any) -> Any:
        ...
    
    @staticmethod
    def static_quux(arg_1: Any) -> Any:
        ...
    
    def _quuz(self, arg_1: Any) -> Any:
        """
        Does secret Bar things, 
        not to be used outside of Bar
        """
        ...

class CorgeType(type):
    def __new__(mcls, clsname, bases, clsdict) -> CorgeType:
        return super(mcls, CorgeType).__new__(mcls, clsname, bases, clsdict)

# Mixed:
def foo():
    ...

class Bar:
    def __init__(self, arg1: Any) -> None:
        return super(self, Bar).__init__(self, arg1)

    def baz(self, arg1: Any) -> Any:
        ...
    
    @classmethod
    def classQux(cls, arg1: Any) -> Any:
        ...
    
    @staticmethod
    def staticQuux(arg1: Any) -> Any:
        ...
    
    def _quuz(self, arg1: Any) -> Any:
        """
        Does secret Bar things, 
        not to be used outside of Bar
        """
        ...

class CorgeType(type):
    def __new__(mcls, clsname, bases, clsdict) -> CorgeType:
        return super(mcls, CorgeType).__new__(mcls, clsname, bases, clsdict)
```


### **Classes**

All classes should be named with UpperCamelCase.

Metaclasses can be signified by the last word being `Meta` or `Type`.

A leading underscore can be used to signify that the class is intended for intra-module use only.

Any names clashing with builtin python types or keywords can be suffixed with a single underscore.

### **Objects**

Objects should be named just as variables (everything in Python is an object, check with `variable.__bases__` or `type(variable).__bases__`).


## Addendum

Except as specified in this style guide, [PEP-8](https://www.python.org/dev/peps/pep-0008/) should be the primary guiding style. At the end of the day, remember that the files end in .py.

See also: [PEP-8](https://www.python.org/dev/peps/pep-0008/), [PEP-484](https://www.python.org/dev/peps/pep-0484/), `>>> import this`

This style guide is intended to be modified over time (refer to "subject to change" notices); as people and styles change, this doc should be updated. Especially the examples can be modified to better whichever spefic project this is added to.

The primary motivation to define two types of module is to essentially build a library of generic python code which has uses outside Robotpy projects. Additionally it should be clear why "mixed" modules must exist, given the clash between wpilib interface bindings and standard Python language requirements.
