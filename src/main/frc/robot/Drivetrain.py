from __future__ import annotations

import time

import wpilib
import rev
import navx

from frc.robot.Constants import Constants
from frc.robot.Subsystems import Subsystems
from frc.robot.Utils import Utils

class Drivetrain(Subsystems):
    instance = None
    @classmethod
    def getInstance(cls) -> Drivetrain:
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance
    
    def __init__(self) -> None:
        self.rightFront = rev.CANSparkMax(Constants.TALON_RIGHTFRONT, rev.MotorType.kBrushless)
        self.leftFront = rev.CANSparkMax(Constants.TALON_LEFTFRONT, rev.MotorType.kBrushless)
        self.leftBack = rev.CANSparkMax(Constants.TALON_LEFTBACK, rev.MotorType.kBrushless)
        self.rightBack = rev.CANSparkMax(Constants.TALON_RIGHTBACK, rev.MotorType.kBrushless)
        self.leftMiddle = rev.CANSparkMax(Constants.TALON_LEFTMIDDLE, rev.MotorType.kBrushless)
        self.rightMiddle = rev.CANSparkMax(Constants.TALON_RIGHTMIDDLE, rev.MotorType.kBrushless)

        self.encoderLeftFront = self.leftFront.getEncoder()
        self.encoderRightFront = self.rightFront.getEncoder()

        self.pidControllerLeftFront = self.leftFront.getEncoder()
        self.pidControllerRightFront = self.rightFront.getEncoder()
        self.shifter = wpilib.Solenoid(Constants.SOLENOID_SHIFTER)
        self.airBoi = wpilib.Compressor(0)

        self.gyro = navx.AHRS(wpilib.SPI.Port.kMXP)

        # set all PID values
        ##############################
        # Slot 1
        self.pidControllerRightFront.setP(Constants.kP, 1)
        self.pidControllerRightFront.setI(Constants.kI, 1)
        self.pidControllerRightFront.setD(Constants.kD, 1)
        self.pidControllerRightFront.setIZone(Constants.kIz, 1)

        self.pidControllerLeftFront.setP(Constants.kP, 1)
        self.pidControllerLeftFront.setI(Constants.kI, 1)
        self.pidControllerLeftFront.setD(Constants.kD, 1)
        self.pidControllerLeftFront.setIZone(Constants.kIz, 1)

        # Switch order of left and right
        self.pidControllerLeftFront.setOutputRange(Constants.kMinOutput, Constants.kMaxOutput, 1)
        self.pidControllerRightFront.setOutputRange(Constants.kMinOutput, Constants.kMaxOutput, 1)
        
        # Slot 2
        self.pidControllerRightFront.setP(Constants.kP, 2)
        self.pidControllerRightFront.setI(Constants.kI, 2)
        self.pidControllerRightFront.setD(Constants.kD, 2)
        self.pidControllerRightFront.setIZone(Constants.kIz, 2)

        self.pidControllerLeftFront.setP(Constants.kP, 2)
        self.pidControllerLeftFront.setI(Constants.kI, 2)
        self.pidControllerLeftFront.setD(Constants.kD, 2)
        self.pidControllerLeftFront.setIZone(Constants.kIz, 2)

        # Switch order of left and right
        self.pidControllerLeftFront.setOutputRange(Constants.kMinOutput, Constants.kMaxOutput, 2)
        self.pidControllerRightFront.setOutputRange(Constants.kMinOutput, Constants.kMaxOutput, 2)


        # GYRO
        self.setGkP(Constants.GYROkP)
        self.setGkI(Constants.GYROkI)
        self.setGkD(Constants.GYROkD)

        
        ##############################
        self.rightBack.follow(self.rightFront)
        self.rightMiddle.follow(self.rightFront)

        self.leftBack.follow(self.leftFront)
        self.leftMiddle.follow(self.leftFront)

        self.capSpeed(Constants.DTMAX_AUTO_SPEED)

    def drive(self, powerLeft: float, powerRight: float) -> None:
        self.pidControllerRightFront.setReference(-powerRight, rev.ControlType.kDutyCycle, 1)
        self.pidControllerLeftFront.setReference(powerLeft, rev.ControlType.kDutyCycle, 1)

    def driveRotations(self, rotLeft: float, rotRight: float) -> None:
        # on second pid slot   # change
        self.resetEncoders()
        self.pidControllerRightFront.setReference(rotRight, rev.ControlType.kPosition, 2)
        self.pidControllerLeftFront.setReference(-rotLeft, rev.ControlType.kPosition, 2)
    
    def driveNoPID(self, left: float, right: float) -> None:
        self.leftFront.set(left)
        self.rightFront.set(right)

    def arcadeDrive(self, fwd: float, tur: float) -> None:
        self.drive(Utils.ensureRange(fwd + tur, -1, 1), Utils.ensureRange(fwd - tur, -1, 1))
    
    def setCoast(self, setMode: bool) -> None:
        # set drivetrain to coast mode
        pass

    def setBrake(self, setMode: bool) -> None:
        # set drivetrain to brake mode
        pass
    
    def capSpeed(self, cap: float) -> None:
        self.pidControllerLeftFront.setOutputRange(-cap, cap, 2)
        self.pidControllerRightFront.setOutputRange(-cap, cap, 2)

    def getSpeed(self) -> float:
        return self.leftFront.getAppliedOutput()

    def compressorOn(self) -> None:
        self.airBoi.start()
    
    def compressorOff(self) -> None:
        self.airBoi.stop()
    
    def highGear(self) -> None:
        self.shifter.set(True)
    
    def lowGear(self) -> None:
        self.shifter.set(False)

    def getAHRS(self) -> bool:
        return self.gyro.getAngle()

    def setRealGyro(self, angle: float) -> None:
        self.realGyro = angle

    def getRealAngle(self) -> float:
        return self.realGyro
    
    def setGkP(self, kP: float) -> None:
        self.gyrokP = kP
    
    def setGkI(self, kI: float) -> None:
        self.gyrokI = kI

    def setGkD(self, kD: float) -> None:
        self.gyrokD = kD
    
    def getEncoderRight(self) -> float:
        return self.encoderRightFront.getPosition()
    
    def getEncoderLeft(self) -> float:
        return self.encoderLeftFront.getPosition()
    
    def getVelocityRight(self) -> float:
        return self.encoderRightFront.getVelocity()
    
    def getVelocityLeft(self) -> float:
        return self.encoderLeftFront.getVelocity()
    
    def resetEncoders(self) -> None:
        self.encoderLeftFront.setPosition(0)
        self.encoderRightFront.setPosition(0)

    def resetGyro(self) -> None:
        self.gyro.reset()
    
    # PID / auto
    def setAngle(self, angle: float) -> None:
        self.setPoint = angle
    
    def targetedDrive(self, power: float) -> None:
        self.arcadeDrive(power, self.pidCalculate(self.getAHRS()) / 1.1)
    
    def autoTargetedDrive(self, power: float) -> None:
        self.arcadeDrive(power, self.autoPidCalculate(self.getAHRS()) / 1.1)
    
    def resetAHRS(self) -> None:
        self.gyro.reset()
    
    def feedValues(self) -> None:
        self.prevTime = time.time_ns() / 1000000000
        self.prevError = self.getAHRS()
    
    def pidCalculate(self, error: float) -> float:
        timeChange = (time.time_ns() / 1000000000) - self.prevTime
        if timeChange == 0:
            timeChange = 100 # timeChange = timeChange or 100
        changeError = error - self.prevError
        
        # manual PID (NOTE: "setPoint" is the angle we are setting the drivetrain to! Refer to "setAngle")
        return ((Constants.GYROkD*(changeError/timeChange))+(Constants.GYROkP*(error-self.setPoint)))*(1.0/3.0)

        # return (SmartDashboard.getNumber("Gyro kD",0)*(changeError/timeChange))+(SmartDashboard.getNumber("Gyro kP", 0)*(error-self.setPoint))
    
    def autoPidCalculate(self, error: float) -> float:
        timeChange = (time.time_ns() / 1000000000) - self.prevTime
        if timeChange == 0:
            timeChange = 100 # timeChange = timeChange or 100
        changeError = error - self.prevError

        # manual PID
        return ((Constants.GYROkD*(changeError/timeChange))+(Constants.GYROkP*(error-self.setPoint)))*(1.0/3.0)

        # return (SmartDashboard.getNumber("Gyro kD",0)*(changeError/timeChange))+(SmartDashboard.getNumber("Gyro kP", 0)*(error-self.setPoint))
    
    '''
    def pidDisable(self) -> None:
        print('PID Disabled')
        self.isPidEnabled = False

    def pidEnable(self) -> None:
        self.isPidEnabled = True
        
    def ispidEnabled(self) -> bool:
        return self.isPidEnabled
    '''

    def setkD(self, kD: float) -> None:
        self.pidControllerLeftFront.setD(kD)
        self.pidControllerRightFront.setD(kD)
    
    def setkI(self, kI: float) -> None:
        self.pidControllerLeftFront.setI(kI)
        self.pidControllerRightFront.setI(kI)

    def setkP(self, kP: float) -> None:
        self.pidControllerLeftFront.setP(kP)
        self.pidControllerRightFront.setP(kP)
    
    # pid slot 2
    def setkP2(self, kP: float) -> None:
        self.pidControllerLeftFront.setP(kP, 2)
        self.pidControllerRightFront.setP(kP, 2)
    
    def setkI2(self, kI: float) -> None:
        self.pidControllerLeftFront.setI(kI, 2)
        self.pidControllerRightFront.setI(kI, 2)
    
    def setkD2(self, kD: float) -> None:
        self.pidControllerLeftFront.setD(kD, 2)
        self.pidControllerRightFront.setD(kD, 2)
    
    def checkStart(self) -> None:
        from frc.RobotTests.Drivetraintester import Drivetraintester # Should be DrivetrainTester
        Drivetraintester.dtTester(self.leftFront, self.leftMiddle, self.leftBack, self.rightFront, self.rightMiddle, self.rightBack)
    
    def stop(self) -> None:
        self.rightFront.set(0)
        self.leftFront.set(0)