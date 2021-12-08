from __future__ import annotations

from types import SimpleNamespace

import commands2
import ctre
from ctre import TalonFXSensorCollection
import wpilib
import wpilib.controller
import wpilib.drive

import frc.constants as constants
from lib.python.utils import avg
from lib.robotpy.ctre import WPI_TalonFXCollection, getTalonEncoders


class Drivetrain(commands2.Subsystem):
    def __init__(self):
        super().__init__()

        self.mLeftMotors = WPI_TalonFXCollection(constants.Drivetrain.kLeftMotorIDs)
        self.mRightMotors = WPI_TalonFXCollection(constants.Drivetrain.kRightMotorIDs)

        self.mDrive = wpilib.drive.DifferentialDrive(
            self.mLeftMotors,
            self.mRightMotors,
        )

    def arcadeDrive(self, forward: float, turning: float) -> None:
        self.mDrive.arcadeDrive(forward, turning)
    
    def tankDrive(self, leftSpeed: float, rightSpeed: float, squareInputs: bool=True) -> None:
        self.mDrive.tankDrive(leftSpeed, rightSpeed, squareInputs)
    
    def resetEncoders(self):
        for motor in self.mMotors.leftList + self.mMotors.rightList:
            motor.getSensorCollection().setQuadraturePosition(0, 0)
    
    def getLeftEncoderPosition(self) -> float:
        self.mLeftMotors.getSelectedSensorPosition()
        return avg(map(TalonFXSensorCollection.getIntegratedSensorPosition, getTalonEncoders(self.mMotors.left)))
        
    def getRightEncoderPosition(self) -> float:
        return avg(map(TalonFXSensorCollection.getIntegratedSensorPosition, getTalonEncoders(self.mMotors.right)))
    
    def getAverageEncoderPosition(self) -> float:
        return (self.getLeftEncoderPosition() + self.getRightEncoderPosition()) / 2