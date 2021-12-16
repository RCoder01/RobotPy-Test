from rev import CANSparkMax
from wpilib import Timer

from frc.robot.Constants import Constants
from frc.robot.Drivetrain import Drivetrain

class Drivetraintester:

    dt = Drivetrain.getInstance()
    allMotorsFunctional = True
    testFinished = False

    @classmethod
    def dtTester(cls, leftFront: CANSparkMax, leftMiddle: CANSparkMax, leftBack: CANSparkMax, rightFront: CANSparkMax, rightMiddle: CANSparkMax, rightBack: CANSparkMax) -> None:
        cls.testFinished = False
        motors: list[CANSparkMax] = []

        motors.append(leftFront)
        motors.append(leftMiddle)
        motors.append(leftBack)
        motors.append(rightFront)
        motors.append(rightMiddle)
        motors.append(rightBack)

        cls.dt.driveNoPID(1, 1)
        Timer.delay(2)

        print()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("                      D R I V E T R A I N                         ")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        
        for motornum, motor in enumerate(motors):
            # returns name of motor for easier analysis
            print("Testing " + motors[motornum].getDeviceId() + "...")
            if Constants.DT_ACCEPTED_MIN_CURRENT >= motor.getOutputCurrent() or motor.getOutputCurrent() >= Constants.DT_ACCEPTED_MAX_CURRENT:
                print("!!! CURRENT ERROR !!!")
                print("CANSparkMax: " + motor.getDeviceId() + " is currently outputting at " + motor.getOutputCurrent() + " Amps!")
                print("...Its expected output is around " + (Constants.DT_ACCEPTED_MIN_CURRENT + Constants.DT_ACCEPTED_MAX_CURRENT)/2 + " Amps!")
                print()
                cls.allMotorsFunctional = False
            if Constants.DT_ACCEPTED_MIN_VELOCITY >= motor.getEncoder().getVelocity() or motor.getEncoder().getVelocity() >= Constants.DT_ACCEPTED_MAX_VELOCITY:   
                print("!!! VELOCITY ERROR !!!")
                print("CANSparkMax: " + motor.getDeviceId() + " is currently outputting at " + motor.getEncoder().getVelocity() + " RPM!")
                print("...Its expected output is around " + (Constants.DT_ACCEPTED_MIN_VELOCITY + Constants.DT_ACCEPTED_MAX_VELOCITY)/2 + " RPM!")
                print()
                cls.allMotorsFunctional = False

        if cls.allMotorsFunctional:
            print("All motors working...")

        Timer.delay(1)

        cls.dt.stop()
  
        cls.testFinished = True
    
    @classmethod
    def areAllMotorsFunctional(cls) -> bool:
        return cls.allMotorsFunctional

    @classmethod
    def isTestFinished(cls) -> bool:
        return cls.testFinished