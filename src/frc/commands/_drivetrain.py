from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections import Callable

import commands2

from lib.py.utils import (
    deadzone,
    unit_float,
)
import frc.subsystems as subsystems


class default(commands2.CommandBase):
    def __init__(
            self, 
            leftPowerSupplier: Callable[[], unit_float], 
            rightPowerSupplier: Callable[[], unit_float],
            ) -> None:
        """
        Sets drivetrain to arcade drive
        """
        self.leftPowerSupplier = leftPowerSupplier
        self.rightPowerSupplier = rightPowerSupplier
        self.addRequirements(subsystems.drivetrain)
        super().__init__()
    
    def initialize(self) -> None:
        return super().initialize()
    
    def execute(self) -> None:
        """
        Uses power suppliers to tankdrive the robot
        """
        #8======D
        self.drivetrain.tankDrive(
            deadzone(self.leftPowerSupplier()),
            deadzone(self.rightPowerSupplier()),
        )
    
    def end(self, interrupted: bool) -> None:
        """
        """
        self.drivetrain.tankDrive(0, 0)
    
    def isFinished(self) -> bool:
        return False


class forwardDistance(commands2.CommandBase):
    def __init__(self) -> None:
        
        
        self.addRequirements(subsystems.drivetrain)