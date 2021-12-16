
import math

from frc.robot.Constants import Constants
from frc.robot.Limelight import Limelight

class Utils:

    # also works for power
    @staticmethod
    def distToActuator(distance: float, slope: float, min: float) -> float:
        return slope * distance - min

    @staticmethod
    def autoPower() -> float:
        print(Utils.distance())
        distance = Utils.distance()

        if (distance <= 47.7):
            return Constants.LAYUP_SPEED * (50.0 / 15)
        elif (distance <= 79.5):
            return Utils.autoFormula(47.7, 79.5, 4400, 5000) * (50.0 / 15)
        elif (distance <= 116.5):
            return Utils.autoFormula(79.5, 116.5, 5000, 6000) * (50.0 / 15)
        else:
            return Utils.autoFormula(116.5, 145.65, 6000, 6200) * (50.0 / 15)

    @staticmethod
    def dist(tx: float, ty: float) -> float:
        return Constants.TARGET_HEIGHT / (math.tan(Utils.degToRad(ty + Constants.LIMELIGHT_ANGLE)))

    @staticmethod
    def degToRad(x: float) -> float:
        return (math.pi / 180.0) * x

    @staticmethod
    def ensureRange(v: float, min_: float, max_: float) -> float:
        return min(max(v, min_), max_)

    @staticmethod
    def feetToRotations(feet: float) -> float:
        return feet * 1.57

        # if you want to travel 4 feet in DriveDistance
        # use this formula in drive distance and set double feet to 4

    @staticmethod
    def autoFormula(minDist: float, maxDist: float, minAct: float, maxAct: float) -> float:
        return (((maxDist - Utils.dist(Limelight.getTx(), Limelight.getTy())) * minAct)
                + (((Utils.dist(Limelight.getTx(), Limelight.getTy()) - minDist)) * minAct)) / (maxDist - minDist)
    
    @staticmethod
    def expodeadZone(input: float) -> float:
        if (input > 0.1):
            return math.pow((1.1111111 *input - 0.111111111), 3)
        elif (input < -0.1):
            return math.pow((1.1111111 *input + 0.111111111), 3)
        else:
            return 0

    @staticmethod
    def distance() -> float:
        return Utils.dist(Limelight.getTx(), Limelight.getTy())