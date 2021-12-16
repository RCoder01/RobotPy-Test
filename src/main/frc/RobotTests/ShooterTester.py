from ctre import WPI_TalonFX

from wpilib import Timer
from frc.robot.Constants import Constants
from frc.robot.Shooter import Shooter

class ShooterTester:

    shooter = Shooter.getInstance()
    allMotorsFunctional = True
    TestFinished = False
    motors: list[WPI_TalonFX] = []

    def __init__(self) -> None:
        pass

    @classmethod
    def shooterTest(cls, launcherLeft: WPI_TalonFX, launcherRight: WPI_TalonFX) -> None:
        motornum = 0

        print()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("                       S H O O T E R                              ")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        
        cls.motors.add(launcherLeft)
        cls.motors.add(launcherRight)

        cls.shooter.launchNoPID(1)
        Timer.delay(2)


        for motor in cls.motors:
            print("Testing " + cls.motors[motornum].getDeviceID() + "...")
            
            if Constants.LAUNCHER_ACCEPTED_MIN_CURRENT >= motor.getStatorCurrent() or motor.getStatorCurrent() >= Constants.LAUNCHER_ACCEPTED_MAX_CURRENT:
                print("!!! CURRENT ERROR !!!")
                print("TalonFX: " + motor.getDeviceID() + " is currently outputting at " + motor.getStatorCurrent() + " Amps!")
                print("...Its expected output is around " + (Constants.LAUNCHER_ACCEPTED_MIN_CURRENT + Constants.LAUNCHER_ACCEPTED_MAX_CURRENT)/2 + " Amps!")
                print()
                cls.allMotorsFunctional = False

            if Constants.LAUNCHER_ACCEPTED_MIN_VELOCITY >= motor.getSelectedSensorVelocity() or motor.getSelectedSensorVelocity() >= Constants.LAUNCHER_ACCEPTED_MAX_VELOCITY:
                print("!!! VELOCITY ERROR !!!")
                print("TalonFX: " + motor.getDeviceID() + " is currently outputting at " + motor.getSelectedSensorVelocity() + " RPM!")
                print("...Its expected output is around " + (Constants.LAUNCHER_ACCEPTED_MIN_VELOCITY + Constants.LAUNCHER_ACCEPTED_MAX_VELOCITY)/2 + " RPM!")
                print()
                cls.allMotorsFunctional = False

            motornum = motornum + 1

        Timer.delay(4)

        cls.shooter.launchNoPID(0)
        if cls.allMotorsFunctional:
            print("All motors functional")

        cls.testFinished = True

    @classmethod
    def allMotorsFunctional(cls) -> bool:
        return cls.allMotorsFunctional

    @classmethod
    def isTestFinished(cls) -> bool:
        return cls.testFinished
        