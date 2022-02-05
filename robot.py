import commands2
import commands2.button
import math
import rev
import wpilib
import wpilib.interfaces
import wpilib.drive
import wpilib.controller
import wpimath

def deadzone(
        input,
        power=2,
        lower_maxzone=-1,
        lower_deadzone=-0.1,
        higher_deadzone=0.1,
        higher_maxzone=1,
        ):
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
        return -math.pow(
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

RATE_LIMIT = 0.05

class RateLimiter:
    def __init__(self, rate = RATE_LIMIT):
        self._rate = rate
        self._last_value = 0

    def __call__(self, value):
        if not self._rate:
            return value

        self._last_value = max(min(value, self._last_value + self._rate), self._last_value - self._rate)
        return self._last_value

class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        self.leftMotors = [rev.CANSparkMax(ID, rev.MotorType.kBrushless) for ID in (15, 14, 13)]
        self.rightMotors = [rev.CANSparkMax(ID, rev.MotorType.kBrushless) for ID in (1, 2, 20)]
        self.leftMotorController = wpilib.SpeedControllerGroup(*self.leftMotors)
        self.rightMotorController = wpilib.SpeedControllerGroup(*self.rightMotors)
        self.drivetrain = wpilib.drive.DifferentialDrive(self.leftMotorController, self.rightMotorController)

        self.driver = wpilib.XboxController(0)

        self._left_rate_limiter = RateLimiter()
        self._right_rate_limiter = RateLimiter()

    def teleopPeriodic(self):
        fwd = deadzone(self._left_rate_limiter(self.driver.getY(wpilib.interfaces.GenericHID.Hand.kRightHand)))
        turn = deadzone(self._right_rate_limiter(-self.driver.getX(wpilib.interfaces.GenericHID.Hand.kLeftHand)))
        for motor in self.leftMotors:
            motor.set(fwd)
        self.drivetrain.tankDrive(
            fwd,
            turn,
        ) # Y is forward/backward, X is left/right
        wpilib.SmartDashboard.putNumber("Driver Y", fwd)
        wpilib.SmartDashboard.putNumber("Driver X", turn)

if __name__ == '__main__':
    wpilib.run(Robot)