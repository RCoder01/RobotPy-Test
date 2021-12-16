from __future__ import annotations

import wpilib
import ctre


from frc.robot.Constants import Constants
from frc.robot.Subsystems import Subsystems

class Shooter(Subsystems):
    instance = None
    @classmethod
    def getInstance(cls) -> Shooter:
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance
    
    def __init__(self) -> None:
        self.launcherLeft = ctre.WPI_TalonFX(Constants.SHOOTER_TALON_LEFT)
        self.launcherRight = ctre.WPI_TalonFX(Constants.SHOOTER_TALON_RIGHT)

        self.elevator = ctre.WPI_TalonSRX(Constants.ELEVATOR_TALON)

        self.hood = wpilib.Solenoid(Constants.SOLENOID_HOOD)





        # resets before setting configs
        self.launcherLeft.configFactoryDefault()
        self.launcherRight.configFactoryDefault()

        # sets feedback device (encoder) and type of loop (controlled)
        self.launcherLeft.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor, Constants.kPIDLoopIdx, Constants.kTimeoutMs)

        # setting sensorphase to true simply allows setinverted to be called
        self.launcherLeft.setSensorPhase(True)
        self.launcherRight.setSensorPhase(True)

        # maxes and mins
        self.launcherLeft.configNominalOutputForward(0, Constants.kTimeoutMs)
        self.launcherLeft.configNominalOutputReverse(0, Constants.kTimeoutMs)
        self.launcherLeft.configPeakOutputForward(1, Constants.kTimeoutMs)
        self.launcherLeft.configPeakOutputReverse(-1, Constants.kTimeoutMs)

        self.launcherLeft.config_kP(Constants.kPIDLoopIdx, Constants.SHOOTER_kP, Constants.kTimeoutMs)
        self.launcherLeft.config_kI(Constants.kPIDLoopIdx, Constants.SHOOTER_kI, Constants.kTimeoutMs)
        self.launcherLeft.config_kD(Constants.kPIDLoopIdx, Constants.SHOOTER_kD, Constants.kTimeoutMs)
        self.launcherLeft.config_kF(Constants.kPIDLoopIdx, Constants.SHOOTER_FEED_FWD, Constants.kTimeoutMs)

        self.launcherLeft.setInverted(True)
        self.launcherRight.follow(self.launcherLeft)

    def launch(self, speed: float) -> None:
        self.launcherLeft.set(speed)
        self.launcherRight.follow(self.launcherLeft)
    
    def launchNoPID(self, speed: float) -> None:
        self.launcherLeft.set(ctre.ControlMode.PercentOutput, speed)
        self.launcherRight.follow(self.launcherLeft)
    
    def getPercentOutput(self) -> float:
        return self.launcherLeft.getMotorOutputPercent()
    
    def elevate(self, power: float) -> None:
        self.elevator.set(ctre.ControlMode.PercentOutput, power)
    
    def elevatePercent(self) -> float:
        return self.elevator.getMotorOutputPercent()
    
    def hoodBack(self) -> None:
        self.hood.set(False)

    def hoodForward(self) -> None:
        self.hood.set(True)
    
    def setkP(self, x: float) -> None:
        self.launcherLeft.config_kP(Constants.kPIDLoopIdx, x, Constants.kTimeoutMs)
    
    def setkI(self, x: float) -> None:
        self.launcherLeft.config_kI(Constants.kPIDLoopIdx, x, Constants.kTimeoutMs)
    
    def setkD(self, x: float) -> None:
        self.launcherLeft.config_kD(Constants.kPIDLoopIdx, x, Constants.kTimeoutMs)
    
    def setkF(self, x: float) -> None:
        self.launcherLeft.config_kF(Constants.kPIDLoopIdx, x, Constants.kTimeoutMs)
    
    def getVelo(self) -> float:
        return self.launcherLeft.getSelectedSensorVelocity() * 2
    
    def getVeloRight(self) -> float:
        return self.launcherLeft.getSelectedSensorVelocity()
    
    def getTemp(self) -> float:
        return self.launcherLeft.getTemperature()
    
    def getRightTemp(self) -> float:
        return self.launcherRight.getTemperature()
    
    def checkStart(self) -> None:
        from frc.RobotTests.ShooterTester import ShooterTester
        ShooterTester.shooterTest(self.launcherLeft, self.launcherRight)
    
    def stop(self) -> None:
        pass