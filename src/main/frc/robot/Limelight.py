from __future__ import annotations

from networktables import NetworkTables
import wpilib

class Limelight:
    instance = None

    nt: NetworkTables.NetworkTable

    tx = 0
    ty = 0
    tv = 0
    ta = 0

    @classmethod
    def getInstance(cls) -> Limelight:
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance
    
    def __init__(self) -> None:
        cls = type(self)
        cls.nt = NetworkTables.getTable('limelight')
        cls.nt.getEntry('pipeline').setNumber(1)
        cls.nt.getEntry('ledMode').setNumber(3)
        cls.printTables()

    @classmethod
    def refresh(cls):
        cls.nt = NetworkTables.getTable('limelight')
        cls.tx = cls.nt.getEntry('tx').getDouble(0) - 2
        cls.ty = cls.nt.getEntry('ty').getDouble(100)
        cls.tv = cls.nt.getEntry('tv').getDouble(0)
        cls.ta = cls.nt.getEntry('ta').getDouble(0)
        cls.nt.getEntry('ledMode').setNumber(3)
    
    @classmethod
    def getTx(cls) -> float:
        return cls.tx
    
    @classmethod
    def getTy(cls) -> float:
        return cls.ty
    
    @classmethod
    def getTv(cls) -> float:
        return cls.tv
    
    @classmethod
    def getTa(cls) -> float:
        return cls.ta

    @classmethod
    def ledsOn(cls) -> None:
        cls.nt.getEntry('ledMode').setNumber(3)

    @classmethod
    def ledsOff(cls) -> None:
        # self.nt.getEntry('ledMode').setNumber(1)
        cls.nt.getEntry('ledMode').setNumber(3)

    @classmethod
    def ledsFlash(cls) -> None:
        cls.nt.getEntry('ledMode').setNumber(2)

    @classmethod
    def printTables(cls) -> None:
        wpilib.SmartDashboard.putString('nt', str(cls.nt.getKeys()))