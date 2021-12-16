from __future__ import annotations

import ctre
import wpilib

from frc.robot.Constants import Constants
from frc.robot.Subsystems import Subsystems

class Intake(Subsystems):
    instance = None
    @classmethod
    def getInstance(cls) -> Intake:
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self) -> None:
        self.belt = ctre.WPI_TalonSRX(Constants.INTAKE_BELT)
        self.ingestorBar = wpilib.Solenoid(Constants.INTAKE_INGESTORBAR)
        self.ingestor = ctre.WPI_TalonSRX(Constants.INTAKE_INGESTOR)
        self.lowSensor = wpilib.DigitalInput(Constants.COLOR_LOW)
        self.highSensor = wpilib.DigitalInput(Constants.COLOR_HIGH)
        self.belt.configSelectedFeedbackSensor(ctre.FeedbackDevice.CTRE_MagEncoder_Relative)
    
    def getLowSensor(self) -> bool:
        return self.lowSensor.get()
    
    def getHighSensor(self) -> bool:
        return self.highSensor.get()
    
    def ingest(self, power: float) -> None:
        self.ingestor.set(ctre.ControlMode.PercentOutput, power)
    
    def setFeederBrake(self) -> None:
        self.belt.setNeutralMode(ctre.NeutralMode.Brake)
    
    def setFeederCoast(self) -> None:
        self.belt.setNeutralMode(ctre.NeutralMode.Coast)
    
    def beltMove(self, power: float) -> None:
        self.belt.set(ctre.ControlMode.PercentOutput, power)
    
    def getBeltEncoder(self) -> float:
        return self.belt.getSelectedSensorPosition()
    
    def resetBeltEncoder(self) -> None:
        self.belt.setSelectedSensorPosition(0)
    
    def belotMovePosition(self, position: float) -> None:
        self.belt.set(ctre.ControlMode.Position, position)
    
    def barDown(self, isDown: bool) -> None:
        self.ingestorBar.set(isDown)
    
    def isBarDown(self) -> bool:
        return self.ingestorBar.get()
    
    def checkStart(self) -> None:
        from frc.RobotTests.IntakeTester import IntakeTester
        IntakeTester.itTester(self.belt, self.ingestor)
    
    def stop(self) -> None:
        self.ingestorBar.set(False)
        self.ingestor.set(ctre.ControlMode.PercentOutput, 0)
        self.belt.set(ctre.ControlMode.PercentOutput, 0)