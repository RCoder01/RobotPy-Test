from collections.abc import Callable

import commands2

from lib.py.utils import deadzone, unit_float
import frc.subsystems as subsystems


class AutonomousCommand(commands2.CommandBase):
    def __init__(self, drivetrain: subsystems.Drivetrain):
        self.addRequirements(drivetrain)
    
    def initialize(self) -> None:
        return super().initialize()
    
    def execute(self) -> None:
        return super().execute()
    
    def end(self, interrupted: bool) -> None:
        return super().end(interrupted)
    
    def isFinished(self) -> bool:
        return super().isFinished()

class Drivetrain:
    class default(commands2.CommandBase):
        def __init__(
                self, 
                drivetrain: subsystems.Drivetrain, 
                leftPowerSupplier: Callable[[], unit_float], 
                rightPowerSupplier: Callable[[], unit_float],
                ) -> None:
            """
            Sets drivetrain to arcade drive
            """

            self.drivetrain = drivetrain
            self.leftPowerSupplier = leftPowerSupplier
            self.rightPowerSupplier = rightPowerSupplier
            self.addRequirements(drivetrain)
        
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