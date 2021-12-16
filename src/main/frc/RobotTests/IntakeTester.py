from ctre import WPI_TalonSRX
from wpilib import Timer


from frc.robot.Constants import Constants
from frc.robot.Intake import Intake

class IntakeTester:

    IT = Intake.getInstance()
    allMotorsFunctional = True
    testFinished = False

    @classmethod
    def itTester(cls, belt: WPI_TalonSRX, ingestor: WPI_TalonSRX) -> None:
        cls.testFinished = False
        
        motors: list[WPI_TalonSRX] = []
       
        motors.append(belt)
        motors.append(ingestor)
        print()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("                       I N T A K E                                ")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                
        cls.IT.beltMove(1.0)
        cls.IT.ingest(1.0)
        Timer.delay(2)

        
        for motornum, motor in enumerate(motors):
            print("Testing " + motors.get(motornum).getDeviceID() + "...")
            if Constants.TALONSRX_ACCEPTED_MIN_CURRENT >= motor.getStatorCurrent() or motor.getStatorCurrent() >= Constants.TALONSRX_ACCEPTED_MAX_CURRENT:
                print("!!! CURRENT ERROR !!!")
                print("TalonSRX: " + motor.getDeviceID() + " is currently outputting at " + motor.getStatorCurrent() + " Amps!")
                print("...Its expected output is around " + (Constants.TALONSRX_ACCEPTED_MIN_CURRENT + Constants.TALONSRX_ACCEPTED_MAX_CURRENT)/2 + " Amps!")
                print()
                cls.allMotorsFunctional = False

            if Constants.TALONSRX_ACCEPTED_MIN_VELOCITY >= motor.getSelectedSensorVelocity()*(50.0/15) or motor.getSelectedSensorVelocity()*(50.0/15) >= Constants.TALONSRX_ACCEPTED_MAX_VELOCITY:
                print("!!! VELOCITY ERROR !!!")
                print("TalonSRX: " + motor.getDeviceID() + " is currently outputting at " + motor.getSelectedSensorVelocity()*(50.0/15) + " RPM!")
                print("...Its expected output is around " + (Constants.TALONSRX_ACCEPTED_MIN_VELOCITY + Constants.TALONSRX_ACCEPTED_MAX_VELOCITY)/2 + " RPM!")
                print()
                cls.allMotorsFunctional = False

        if cls.allMotorsFunctional:
            print("All motors working...")

        Timer.delay(5)

        cls.IT.stop()

        cls.testFinished = True

    @classmethod
    def allMotorsFunctional(cls) -> bool:
        return cls.allMotorsFunctional

    @classmethod
    def isTestFinished(cls) -> bool:
        return cls.testFinished