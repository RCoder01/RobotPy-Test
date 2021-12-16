from __future__ import annotations

import wpilib

from frc.robot.Climber import Climber
from frc.robot.Constants import Constants
from frc.robot.Drivetrain import Drivetrain
from frc.robot.Intake import Intake
from frc.robot.LEDs import LEDs
from frc.robot.Limelight import Limelight
from frc.robot.Shooter import Shooter
from frc.robot.Utils import Utils
from frc.robot.XBoxController import XBoxController

class TeleOpTester:
    """
    This class is a clone of the TeleOp class
    that allows for the manual input of various
    values during Teleoperated mode...
    """
    
    instance = None

    dt = Drivetrain.getInstance()
    shooter = Shooter.getInstance()
    intake = Intake.getInstance()
    climber = Climber.getInstance()

    @classmethod
    def getInstance(cls) -> TeleOpTester:
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance
    
    @classmethod
    def __init__(cls) -> None:
        cls.driver = XBoxController(Constants.XBOX_DRIVER)
        cls.manip = XBoxController(Constants.XBOX_MANIP)

        # shooter default
        cls.pdp = wpilib.PowerDistributionPanel()

        cls.previousSensorValue = False

        cls.movingDown = False

    @classmethod
    def run(cls):
        cls.smartDashboard()

        Limelight.refresh()

        # P and I set manually in shuffleboard
        cls.shooter.setkI(Constants.SHOOTER_kI)
        cls.shooter.setkF(Constants.SHOOTER_FEED_FWD)



        ### DRIVER CONTROLS ###
        
        if cls.driver.getLeftBumper():
            if Limelight.getTv() == 1:
                Limelight.ledsOn()
           

                cls.dt.setAngle(cls.dt.getAHRS() + Limelight.getTx())
                cls.dt.targetedDrive(cls.Utils.expodeadZone(-cls.driver.getRightStickYAxis())) # allows driver to move back and forth during lineup


                if not cls.manip.getYButton():
                    cls.shooter.hoodForward()
           
            else:
                # Limelight.ledsFlash()
                Limelight.ledsOn()
                cls.dt.pidDisable()
                cls.dt.arcadeDrive(cls.Utils.expodeadZone(-cls.driver.getRightStickYAxis()), Utils.expodeadZone(-cls.driver.getLeftStickXAxis()))
        else:

            if not cls.manip.getRightTriggerButton():
                cls.shooter.hoodBack()

            Limelight.ledsOff()
            # cls.dt.pidDisable()
            cls.dt.arcadeDrive(Utils.expodeadZone(-cls.driver.getRightStickYAxis()), Utils.expodeadZone(-cls.driver.getLeftStickXAxis()))

        # Climber
        if Utils.expodeadZone(cls.driver.getRightTriggerAxis()) > 0 and cls.climber.notHittingLimitSwitch():
            if cls.driver.getRightTriggerAxis() > 0.3:
                cls.climber.disengageRatchet()
                LEDs.setColor(-0.29) # blue light chase
            else:
                cls.climber.engageRatchet()
            
            
            
            cls.climber.climb(Utils.expodeadZone(-cls.driver.getRightTriggerAxis()), Utils.expodeadZone(-cls.driver.getRightTriggerAxis()))
        elif Utils.expodeadZone(cls.driver.getLeftTriggerAxis()) > 0:
            LEDs.setColor(-0.39)
            cls.climber.disengageRatchet()
            cls.climber.climb(Utils.expodeadZone(cls.driver.getLeftTriggerAxis()), Utils.expodeadZone(cls.driver.getLeftTriggerAxis()))
        else:
            LEDs.setColor(-0.39)
            cls.climber.engageRatchet()
            cls.climber.climb(0, 0)

        ### MANIP CONTROLS ###

        # Shooter
        if cls.manip.getRightTriggerButton():
            cls.dt.compressorOff()

            cls.shooter.hoodForward()
            Limelight.ledsOn()

            cls.shooter.launch(wpilib.SmartDashboard.getNumber("Jeff", 0))

            if cls.manip.getLeftStickYAxis() < -0.2:
                cls.intake.beltMove(1.0)
            elif cls.manip.getLeftStickYAxis() > 0.2:
                cls.intake.beltMove(-cls.manip.getLeftStickYAxis())
            else:
                cls.intake.beltMove(0)
            
            '''
            if cls.shooter.getVelo() < speed - 5:
                shootingLEDS = True
                shooterLEDS = False
            else:
                shootingLEDS = False
                shooterLEDS = True
            '''

        elif cls.manip.getYButton():
            cls.dt.compressorOff()

            # layups / close range
            cls.shooter.hoodBack()
            cls.shooter.launch((50.0 / 15.0) * Constants.LAYUP_SPEED)

            if Utils.expodeadZone(cls.manip.getLeftStickYAxis()) < -0.1:
                cls.intake.beltMove(1.0)
            else:
                cls.intake.beltMove(0)

        else:
            cls.dt.compressorOn()
            #  automatic belt

            if cls.highSensorState().equals("new ball in") and not cls.manip.getRightTriggerButton() and cls.lowSensorState().equals("no ball in"):
                cls.intake.resetBeltEncoder()
                LEDs.setColor(-0.29) # blue light chase
                cls.intake.beltMove(0.6)
                cls.shooter.launchNoPID(0.2)

            elif cls.highSensorState().equals("no ball in") and cls.lowSensorState().equals("same ball in"):
                cls.intake.beltMove(-0.2)
            else:
                cls.shooter.launchNoPID(0)
                if cls.intake.getBeltEncoder() < Constants.BELT_BALL_MOVED and not cls.manip.getRightTriggerButton() or cls.lowSensorState().equals("new ball in") and not cls.manip.getRightTriggerButton():
                    cls.intake.setFeederBrake()
                    cls.intake.beltMove(0)
                else:
                    cls.intake.setFeederCoast()

        #  intake bar and belt
        if cls.manip.getLeftBumper():
            cls.intake.barDown(True)
            
            cls.intake.ingest(Utils.expodeadZone(cls.manip.getRightStickYAxis()))

        else:
            cls.intake.barDown(False)
            cls.intake.ingest(0)

    @classmethod
    def smartDashboard(cls):
        cls.shooter.setkP(wpilib.SmartDashboard.getNumber("Shooter kP", Constants.SHOOTER_kP))
        cls.shooter.setkD(wpilib.SmartDashboard.getNumber("Shooter kD", Constants.SHOOTER_kD))

        cls.dt.setGkP(wpilib.SmartDashboard.getNumber("Gyro kP", Constants.GYROkP))
        cls.dt.setGkI(wpilib.SmartDashboard.getNumber("Gyro kI", Constants.GYROkI))
        cls.dt.setGkD(wpilib.SmartDashboard.getNumber("Gyro kD", Constants.GYROkD))

        wpilib.SmartDashboard.putNumber("Gyro #", cls.dt.getAHRS())

        

        distance = Utils.dist(Limelight.getTx(), Limelight.getTy())

        # Shooter values
        wpilib.SmartDashboard.putNumber("distance", distance)
        wpilib.SmartDashboard.putNumber("Velocity", (15.0 / 50.0) * cls.shooter.getVelo())


    @classmethod
    def highSensorState(cls):

        if not cls.previousSensorValue and cls.intake.getHighSensor():
            print("new ball in")
            return "new ball in"

        if not cls.previousSensorValue and not cls.intake.getHighSensor():
            return "no ball in"

        cls.previousSensorValue = cls.intake.getHighSensor()
        cls.previousLowSensorValue = cls.intake.getLowSensor()

        return "same ball in"

    @classmethod
    def lowSensorState(cls):
        if not cls.previousLowSensorValue and cls.intake.getLowSensor():
            print("new ball in")
            return "new ball in"

        if not cls.previousLowSensorValue and not cls.intake.getLowSensor():
            return "no ball in"

        cls.previousLowSensorValue = cls.intake.getLowSensor()

        return "same ball in"