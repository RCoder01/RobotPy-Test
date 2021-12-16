from __future__ import annotations

import wpilib
import ctre

from frc.robot.Constants import Constants
from frc.robot.Subsystems import Subsystems


class Climber(Subsystems):
    instance = None
    @classmethod
    def getInstance(cls) -> Climber:
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance
    
    def __init__(self) -> None:
        self.leftClimber = ctre.WPI_TalonFX(Constants.leftClimber) 
        self.rightClimber = ctre.WPI_TalonFX(Constants.rightClimber)
        self.cylinder = wpilib.Solenoid(Constants.CLIMBER_SOLENOID)

        self.leftClimber.setNeutralMode(ctre.NeutralMode.Brake)
        self.rightClimber.setNeutralMode(ctre.NeutralMode.Brake)

        self.stopper = wpilib.DigitalInput(Constants.CLIMBER_STOPPER)
    
    def climb(self, left: float, right: float) -> None:
        self.leftClimber.set(ctre.ControlMode.PercentOutput, left)
        self.rightClimber.set(ctre.ControlMode.PercentOutput, right)
    
    def disengageRachet(self) -> None:
        self.cylinder.set(True)
    
    def engageRachet(self) -> None:
        self.cylinder.set(False)
    
    def notHittingLimitSwitch(self) -> bool:
        return self.stopper.get()
    
    def limit(self) -> None:
        config = ctre.StatorCurrentLimitConfiguration(False, Constants.CLIMB_I_LIMIT, Constants.CLIMB_I_THRESHOLD, Constants.CLIMB_I_THRESHOLD_TIME) # TODO: code seems broken
        self.leftClimber.configStatorCurrentLimit(config)
        self.rightClimber.configStatorCurrentLimit(config)
    
    def unlimit(self) -> None:
        config = ctre.StatorCurrentLimitConfiguration(False, Constants.CLIMB_I_LIMIT, Constants.CLIMB_I_THRESHOLD, Constants.CLIMB_I_THRESHOLD_TIME) # TODO: code seems broken
        self.leftClimber.configStatorCurrentLimit(config)
        self.rightClimber.configStatorCurrentLimit(config)

    def climberCurrents(self) -> None:
        wpilib.SmartDashboard.putNumber('Left Climber Current', self.leftClimber.getStatorCurrent())
        wpilib.SmartDashboard.putNumber('Right Climber Current', self.rightClimber.getStatorCurrent())
    
    def checkStart(self) -> None:
        pass

    def stop(self) -> None:
        pass