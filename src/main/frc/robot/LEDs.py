from __future__ import annotations

import wpilib

from frc.robot.Constants import Constants

class LEDs:
    instance = None
    @classmethod
    def getInstance(cls) -> LEDs:
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance
    
    def __init__(self):
        self.leds = wpilib.Spark(Constants.LED_CHANNEL)
    
    def setColor(self, color: float) -> None:
        self.leds.set(color)
    
    def getColor(self) -> float:
        return self.leds.get()