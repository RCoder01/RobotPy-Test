from __future__ import annotations
from types import SimpleNamespace, _T

import commands2
import ctre
import wpilib
import wpilib.controller
import wpilib.drive

import constants


class Drivetrain(commands2.Subsystem):

    def __init__(self):
        super().__init__()

        self.mMotors = SimpleNamespace(
            left = wpilib.SpeedControllerGroup(
                *[ctre.TalonFX(ID) for ID in constants.Drivetrain.kLeftMotorIDs]
            ),

            right = wpilib.SpeedControllerGroup(
                *[ctre.TalonFX(ID) for ID in constants.Drivetrain.kRightMotorIDs]
            ),
        )

        self.drive = wpilib.drive.DifferentialDrive(
            self.mMotors.left,
            self.mMotors.right,
        )

    def arcadeDrive(self, forward: float, turning: float) -> None:
        self.drive.arcadeDrive(forward, turning)
    
    def tankDrive(self, leftSpeed: float, rightSpeed: float, squareInputs: bool = True) -> None:
        self.drive.tankDrive(leftSpeed, rightSpeed, squareInputs)

"""
class Elevator(commands2.PIDSubsystem):

    def __init__(self):
        super().__init__(wpilib.controller.PIDController(**constants.Elevator.kPIDConstants))
        self.mMotors = wpilib.SpeedControllerGroup(
            *[ctre.TalonFX(ID) for ID in constants.Elevator.kMotorIDs]
        )
"""