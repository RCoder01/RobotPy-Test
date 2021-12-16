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

class TeleOp:
    instance = None

    dt = Drivetrain.getInstance()
    shooter = Shooter.getInstance()
    intake = Intake.getInstance()
    climber = Climber.getInstance()


    @classmethod
    def getInstance(cls) -> TeleOp:
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

        # PID VALUES
        cls.shooter.setkP(Constants.SHOOTER_kP)
        cls.shooter.setkI(Constants.SHOOTER_kI)
        cls.shooter.setkD(Constants.SHOOTER_kD)
        cls.shooter.setkF(Constants.SHOOTER_FEED_FWD)

        ### DRIVER CONTROLS ###

        # limelight tracking
        if cls.driver.getLeftBumper():
            if Limelight.getTv() == 1:
                Limelight.ledsOn()

                cls.dt.setAngle(cls.dt.getAHRS() + Limelight.getTx())
                
                cls.dt.targetedDrive(Utils.expodeadZone(-cls.driver.getRightStickYAxis())) # allows driver to move back and
                                                                                           # forth during lineup

                if not cls.manip.getYButton():
                    cls.shooter.hoodForward() # manip can override hood position with Y if shooting close
            
            else:
                # Limelight.ledsFlash()
                Limelight.ledsOn()
                # cls.dt.pidDisable()
                cls.dt.arcadeDrive(
                    Utils.expodeadZone(-cls.driver.getRightStickYAxis()), 
                    Utils.expodeadzone(-cls.driver.getLeftStickXAxis())
                )

        else:
            if not cls.manip.getRightTriggerButton():
                cls.shooter.hoodBack()
            
            Limelight.ledsOff()
            # cls.dt.pidDisable()

            # Unless driver is holding leftbumper manual drive is always active
            cls.dt.arcadeDrive(
                Utils.expodeadZone(-cls.driver.getRightStickYAxis()), 
                Utils.expodeadZone(-cls.driver.getLeftStickXAxis())
            )

        # Climber
        if Utils.expodeadZone(cls.driver.getRightTriggerAxis() > 0 and cls.climber.notHittingLimitSwitch()):
            if cls.driver.getRightTriggerAxis() > 0.3:
                cls.climber.disengageRachet()
                LEDs.setColor(-0.29) # blue light chase 
            else:
                cls.climber.engageRachet()

        elif Utils.expodeadZone(cls.driver.getLeftTriggerAxis() < 0): # Trying to un-climb
            if cls.climber.notHittingLimitSwitch(): # limit ok
                cls.climber.unlimit()
            else:
                cls.climber.limit()
            LEDs.setColor(-0.39)
            cls.climber.disengageRachet()
            cls.climber.climb(
                Utils.expodeadZone(cls.driver.getLeftTriggerAxis()),
                Utils.expodeadZone(cls.driver.getLeftTriggerAxis())
            )
        
        else:
            LEDs.setColor(-0.39)
            cls.climber.engageRachet()
            cls.climber.unlimit()
            cls.climber.climb(0, 0)
        
        ### MANIP CONTROLS ###
        
        # Shooter
        if cls.manip.getRightTriggerButton():
            cls.dt.compressorOff()

            cls.shooter.hoodForward()
            Limelight.ledsOn()

            cls.shooter.launch(Utils.autoPower())

            if cls.manip.getLeftStickYAxis() < -0.2:
                cls.intake.beltMove(1)
            elif cls.manip.getLeftStickYAxis() > 0.2:
                cls.intake.beltMove(-cls.manip.getLeftStickYAxis())
            else:
                cls.intake.beltMove(0)
            
            # if (cls.shooter.getVelo() < cls.speed - 5):
            #     cls.shootingLEDS = True
            #     cls.shooterLEDS = False
            # else:
            #     cls.shootingLEDS = False
            #     cls.shooterLEDS = True
        
        elif cls.manip.getYButton():
            cls.dt.compressorOff()
            # cls.shooter.launchNoPID(wpilib.SmartDashboard.getNumber("Jeff", 0))
            # layups / close range
            cls.shooter.hoodBack()
            cls.shooter.launch((50 / 15) * Constants.LAYUP_SPEED)

            if Utils.expodeadZone(cls.manip.getLeftStickYAxis()) < -0.1:
                cls.intake.beltMove(1.0)
            else:
                cls.intake.beltMove(0)
            
        else:

            cls.dt.compressorOn()
            # automatic belt

            if (cls.highSensorState() == 'new ball in') and (not cls.manip.getRightTriggerButton()) and (cls.lowSensorState() == 'no ball in'):
                cls.intake.resetBeltEncoder()
                LEDs.setColor(-0.29)
                cls.intake.beltMove(0.6)
                cls.shooter.launchNoPID(0.2)
            
            elif cls.highSensorState() == 'no ball in' and cls.lowSensorState() == 'same ball in':
                cls.intake.beltMove(-0.2)
            else:
                cls.shooter.launchNoPID(0)
                if (cls.instance.getBeltEncoder() < Constants.BELT_BALL_MOVED and not cls.manip.getRightTriggerButton()) or (cls.lowSensorState() == 'new ball in' and not cls.manip.getRightTriggerButton()):
                    cls.intake.setFeederBrake()
                    cls.intake.beltMove(0)
                else:
                    cls.intake.setFeederCoast()

        # intake bar and belt
        if cls.manip.getLeftBumper():
            cls.intake.barDown(True)
            
            cls.intake.ingest(Utils.expodeadZone(cls.manip.getRightStickYAxis()))
        else:
            cls.intake.barDown(False)
            cls.intake.ingest(0)
        
    @classmethod
    def smartDashboard(cls) -> str:
        wpilib.SmartDashboard.putNumber('Gyro #', cls.dt.getAHRS())

        # drivetrain set values

        '''
        cls.dt.setkP2(wpilib.SmartDashboard.getNumber('kP 2', 0))
        cls.dt.setkI2(wpilib.SmartDashboard.getNumber('kI 2', 0))
        cls.dt.setkD2(wpilib.SmartDashboard.getNumber('kD 2', 0))
        '''

        # cls.speed = wpilib.SmartDashboard.getNumber('jeff', cls.speed)

        distance = Utils.dist(Limelight.getTx(), Limelight.getTy())

        # Shooter values
        wpilib.SmartDashboard.putNumber('distance', distance)
        wpilib.SmartDashboard.putNumber('Velocity', (15.0 / 50.0) * cls.shooter.getVelo())
    
    @classmethod
    def highSensorState(cls) -> str:
        if (not cls.previousSensorValue) and cls.intake.getHighSensor():
            print('new ball in')
            return 'new ball in'
        
        if (not cls.previousSensorValue) and (not cls.intake.getHighSensor()):
            return 'no ball in'
        
        cls.previousSensorValue = cls.intake.getHighSensor()
        cls.previousLowSensorValue = cls.intake.getLowSensor()
        
        return 'same ball in'

    @classmethod
    def lowSensorState(cls) -> str:
        if (not cls.previousLowSensorValue) and cls.intake.getLowSensor():
            print('new ball in')
            return 'new ball in'
        
        if (not cls.previousLowSensorValue) and (not cls.intake.getLowSensor()):
            return 'no ball in'
        
        cls.previousSensorValue = cls.intake.getLowSensor()
        
        return 'same ball in'