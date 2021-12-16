
from wpilib import Joystick

class XBoxControlle(Joystick):
	
	def __init__(port: int):
		super().__init__(port)
	
	def setLeftRumble(self, rumble: float) -> None:
		self.setRumble(Joystick.RumbleType.kLeftRumble, float(rumble))
	
	def setRightRumble(self, rumble: float) -> None:
		self.setRumble(Joystick.RumbleType.kRightRumble, float(rumble))
	
	def getLeftStickXAxis(self) -> float:
		return self.getRawAxis(0)
	
	def getLeftStickYAxis(self) -> float:
		return -self.getRawAxis(1)
	
	def getRightTriggerAxis(self) -> float:
		return self.getRawAxis(3)
	
	def getLeftTriggerAxis(self) -> float:
		return self.getRawAxis(2)
	
	def getRightStickXAxis(self) -> float:
		return self.getRawAxis(4)
	
	def getRightStickYAxis(self) -> float:
		return -self.getRawAxis(5)

	def getAButton(self) -> bool:
		return self.getRawButton(1)

	def getBButton(self) -> bool:
		return self.getRawButton(2)

	def getXButton(self) -> bool:
		return self.getRawButton(3)

	def getYButton(self) -> bool:
		return self.getRawButton(4)

	def getLeftBumper(self) -> bool:
		return self.getRawButton(5)

	def getRightBumper(self) -> bool:
		return self.getRawButton(6)

	def getBackButton(self) -> bool:
		return self.getRawButton(7)

	def getStartButton(self) -> bool:
		return self.getRawButton(8)
	
	def getLeftJoystickButton(self) -> bool:
		return self.getRawButton(9)
	
	def getRightJoystickButton(self) -> bool:
		return self.getRawButton(10)
	
	def getRightTriggerButton(self) -> bool:
		if self.getRightTriggerAxis() > 0.5:
			return True
		else:
			return False
	
	def getLeftTriggerButton(self) -> bool:
		if self.getLeftTriggerAxis() > 0.5:
			return True
		else:
			return False
	
	def getDPad(self) -> bool:
		return self.getPOV()
	
	def isDPadTopHalf(self) -> bool:
		if self.getDPad() == 315 or self.getDPad() == 0 or self.getDPad() == 45:
			return True
		else:
			return False
	
	def isDPadBottomHalf(self) -> bool:
		if self.getDPad() == 135 or self.getDPad() == 180 or self.getDPad() == 225:
			return True
		else:
			return False
	
	def getBothTriggerAxis(self) -> float:
		return self.getRightTriggerAxis()- self.getLeftTriggerAxis()
	
	def getTriggers(self) -> float:
		return self.getRawAxis(3) - self.getRawAxis(2)
	
	def isButtonClicked(self) -> bool:
		if self.getLeftBumper():
			return True
		else:
			return False