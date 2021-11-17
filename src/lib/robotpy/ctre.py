import ctre


def getTalonEncoders(*talons: ctre.WPI_TalonFX):
    if len(talons) == 1:
        return talons[0].getSensorCollection()
    return tuple(talon.getSensorCollection() for talon in talons)


class TalonFXSensorCollectionCollection(ctre.WPI_TalonSensorCollection):
    ...