from __future__ import annotations

import commands2
import ctre
import wpilib
import wpilib.controller
import wpilib.drive

import frc.constants as constants


class Elevator(commands2.PIDSubsystem):

    def __init__(self):
        super().__init__(wpilib.controller.PIDController(**constants.Elevator.kPIDConstants))
        self.mMotorList = [ctre.WPI_TalonFX(ID) for ID in constants.Elevator.kMotorIDs]
        self.mMotors = wpilib.SpeedControllerGroup(
            *self.mMotorList
        )