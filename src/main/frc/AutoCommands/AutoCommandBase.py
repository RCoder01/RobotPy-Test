import abc
import logging

# import org.usfirst.frc.team548.robot.AutoCommands.AutoCommandBase;
from wpilib import DriverStation, Timer

class AutoCommandBase(abc.ABC):
    ds = DriverStation.getInstance()

    def __init__(self, timeOut: float) -> None:
        self.done = False
        self.timeOut = timeOut
        self.timer = Timer()
    
    @abc.abstractmethod
    def init(self) -> None: ...
    @abc.abstractmethod
    def run(self) -> None: ...
    @abc.abstractmethod
    def end() -> None: ...
    
    def execute(self) -> None:
        print("Starting command " + self.getCommandName())
        self.init()
        self.timer.start()
        while not self.done and not self.hasTimedOut() and not self.ds.isDisabled() and not self.ds.isOperatorControl():
            self.run()
            try:
            # '''
                pass
                # Thread.sleep(5)
            except InterruptedException as ex:
                logging.exception(type(self).__name__ + " interrupted")
            # '''
        
        print("Ending command " + self.getCommandName())
        self.end()
    
    def hasTimedOut(self) -> bool:
        return self.timeOut <= self.timer.get()

    def isDone(self): return self.done
    def setDone (self, d: bool) -> None:
        self.done = d
    
    @abc.abstractmethod
    def getCommandName(self) -> str: ...