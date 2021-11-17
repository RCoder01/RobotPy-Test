import commands2

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