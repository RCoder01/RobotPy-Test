from __future__ import annotations

import ctre

class Music:
    instance = None
    @classmethod
    def getInstance(cls) -> Music:
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance
    
    def __init__(self) -> None:
        self.songs: list[str] = []
        self.orchestra_ = ctre.Orchestra()

    def loadMusicSelection(self, Falcon1: ctre.WPI_TalonFX, Falcon2: ctre.WPI_TalonFX, Falcon3: ctre.WPI_TalonFX, Falcon4: ctre.WPI_TalonFX, songSelection: str) -> None:

        # .chrp files are converted from .midi in pheonix tuner and placed into src/main/deploy~

        self.orchestra_.addInstrument(Falcon1)
        self.orchestra_.addInstrument(Falcon2)
        self.orchestra_.addInstrument(Falcon3)
        self.orchestra_.addInstrument(Falcon4)

        self.orchestra_.loadMusic(songSelection)

        # wpilib.Timer.delay(2) # delay so that midi can parse # Timer has no delay method, so commented out
    
    def play(self) -> None:
        self.orchestra_.play()