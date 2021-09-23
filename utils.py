from math import pow


class unit_float(float):
    """A floating point number value between -1 and 1"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not(-1 <= self <= 1):
            raise AttributeError('unit_float must be in range [-1, 1]')
        

def deadzone(
    input: unit_float,
    power: float = 2,
    lowerMaxzone: unit_float = -1,
    lowerDeadzone: unit_float = -0.1,
    higherDeadzone: unit_float = 0.1,
    higherMaxzone: unit_float = 1,
    ) -> unit_float:
    """
    Highly customizable deadzone function, 
    Follows equations at https://www.desmos.com/calculator/yt5brsfh1m

    :param input: The value to be set into deadzone
    :param power: The power to which the function should be taken; 1 is linear, 2 is quadratic, etc.
    :param lowerMaxzone: The negative point past which all inputs return -1
    :param lowerDeadzone: The negative point past which all less inputs return 0
    :param higherDeadzone: The positive point past which all less inputs return 0
    :param higherMaxzone: The positive point at which all past inputs return 1

    -1 <= lowerMaxzone < lowerDeadzone <= 0 <= higherDeadzone < higherMaxzone <= 1

    :returns: Input modified by the different parameters
    """
    if not(-1 <= lowerMaxzone < lowerDeadzone <= 0 <= higherDeadzone < higherMaxzone <= 1):
        raise ValueError('The following must be true:-1 <= lowerMaxzone < lowerDeadzone <= 0 <= higherDeadzone < higherMaxzone <= 1')
    if not(power >= 0):
        raise ValueError('Power must be greater than or equal to zero')
    
    if input <= lowerMaxzone:
        return -1
    if lowerMaxzone < input < lowerDeadzone:
        return pow((-input + lowerDeadzone) / (lowerDeadzone - lowerMaxzone), power)
    if lowerDeadzone <= input <= higherDeadzone:
        return 0
    if higherDeadzone < input < higherMaxzone:
        return pow((input - higherDeadzone) / (higherMaxzone - higherDeadzone), power)
    if higherMaxzone <= input:
        return 1
