# Style Guide for Robostangs 548 Python Robot Code #


## Notes

Except as specified in this style guide, [PEP-8](https://www.python.org/dev/peps/pep-0008/) should be the primary guiding style. At the end of the day, remember that the files end in .py.

See also: `import this`


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

In Pythonic modules, line length should be restricted to 79 characters, as per [PEP-8](https://www.python.org/dev/peps/pep-0008/#maximum-line-length)

Line breaks within statements should occur where implicit continuation is present. If you need to use a backslash (\\), there's *probably* a better way to do it.

### Mixed:

In mixed modules, because of naming conventions (outlined later) and due to general standard in C++/Java robot code, lines length is not limited.

Docstrings and multi-line comments should still be limited to 72 or 79 characters for easier readability.


## Imports

- Different libraries/packages should be imported on separate lines.
- Importing from within libraries/packages is permitted, including the use of the `from` keyword.
- Importing functions, constants, and classes from modules is permitted
- Use of the `as` keyword to prevent name conflicts is also permitted.
- Multiple importing from the same library/package using standard syntax is permitted (subject to change)
however, if in the future merge conflicts are an issue with this suggestion, it may be reversed or changed to require multi-line `from` syntax
- Relative imports in top-level modules are recommended as the project folder's name may be subject to be change and/or may not fit Python's module naming syntax (subject to change)
  - `__future__` imports
  - Attempting to absolute import from the top level may cause a SyntaxError
  - Absolute imports within sub-modules is still permitted
- Order of imports should be as such:
  - Standard Library imports
  - Other installed library/package imports
  - Robotpy imports
    - Remember that pythonic modules should not import from Robotpy, only mixed modules
  - Local imports
- Within each group, imports should be ordered alphabetically; first by library/package/module, then by sub-imports (those after the `from` keyword)
- One line of whitespace should be given between each non-empty group (`__future__` is included in the standard library, and *must* be listed first)
- The conclusion of the imports section should be followed by two blank lines
- Any testing-specific imports can and should be placed at the beginning of the `if __name__ == '__main__'` clause (abiding by the same guidlines as above)


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

Type hints should be given in all function/method declarations. This means including descriptive, multi-level types as required. The standard library package Typing is helpful for this.

Use a type definition T when input and output objects are the same but of unknowable type.

### Example:

```
def foo(bar: int, baz: list[str], bang: Callable[[T], Union[list, tuple][Generator]]) -> T:

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

For documenting extra function parameter output, use :param: and :returns:

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
    """
    return [Baz(bat) for bat in range(bar)]
```


## Naming

### **String Literal Definitions**

When string literal definitions exceed 79 characters, use implicit string literal concatenation to spread across lines.

### Pythonic:

Single quotes should be used whenever possible, but use double quotes instead of `\'`

### Mixed:

Single quotes are preferred, but either is fine.

