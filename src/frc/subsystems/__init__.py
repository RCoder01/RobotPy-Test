# TODO: Replace this with subsystems import and such
from frc.subsystems._drivetrain import Drivetrain
from frc.subsystems._elevator import Elevator

drivetrain = Drivetrain()
elevator = Elevator()

__all__ = [
    drivetrain,
    elevator,
]