from commands2 import TimedCommandRobot
import wpilib
from wpilib import SmartDashboard
from ctre import WPI_TalonFX


from frc.AutoModes.AutoMode import AutoMode
from frc.AutoModes.ShootfromInit import ShootfromInit # Should be ShootFromInit
from frc.AutoModes.ShootFromCenterInit import ShootFromCenterInit
from frc.AutoModes.ShootFromLeftInit import ShootFromLeftInit

from frc.RobotTests.Drivetraintester import Drivetraintester # Should be DrivetrainTester
from frc.RobotTests.IntakeTester import IntakeTester
from frc.RobotTests.ShooterTester import ShooterTester

from frc.robot.Climber import Climber
from frc.robot.Constants import Constants
from frc.robot.Drivetrain import Drivetrain
from frc.robot.Intake import Intake
from frc.robot.LEDs import LEDs
from frc.robot.Limelight import Limelight
from frc.robot.Music import Music
from frc.robot.Shooter import Shooter
from frc.robot.TeleOp import TeleOp
from frc.robot.TeleOpTester import TeleOpTester


class Robot(TimedCommandRobot):
    """
    the wpilib wpilib is configured to automatically run this class, and to call the
    functions corresponding to each mode, as described in the TimedRobot
    documentation. If you change the name of this class or the package after
    creating this project, you must also update the build.gradle file in the
    project.
    """

    def robotInit(self):
        """
        This function is run when the robot is first started up and should be
        used for any initialization code.
        """
        self.m_chooser = wpilib.SendableChooser()
        self.m_chooser.setDefaultOption('Right', ShootfromInit())
        self.m_chooser.addOption('Centered', ShootFromCenterInit())
        self.m_chooser.addOption('Left', ShootFromLeftInit())
        SmartDashboard.putData('Auto choices', self.m_chooser)
        self.dt = Drivetrain.getInstance()
        self.sh = Shooter.getInstance()
        LEDs.getInstance()
        Climber.getInstance()
        self.it = Intake.getInstance()
        self.tp = TeleOp.getInstance()
        self.tpt = TeleOpTester.getInstance()
        Limelight.getInstance()
        Limelight.ledsOff()
        self.pdp = wpilib.PowerDistributionPanel()
        self.climber = Climber.getInstance()
    
    def robotPeriodic(self) -> None:
        """
        This function is called every robot packet, no matter the mode. Use
        this for items like diagnostics that you want ran during disabled,
        autonomous, teleoperated and test.

        This runs after the mode specific periodic functions, but before
        LiveWindow and SmartDashboard integrated updating.
        """
        self.dt.setRealGyro(self.dt.getAHRS() - self.gyroStart)
        SmartDashboard.putNumber('Gyro value', self.dt.getRealAngle())
        SmartDashboard.putNumber('NAVX value', self.dt.getAHRS())

    def autonomousInit(self) -> None:
        """
        This autonomous (along with the chooser code above) shows how to select
        between different autonomous modes using the dashboard. The sendable
        chooser code works with the Java SmartDashboard. If you prefer the
        LabVIEW Dashboard, remove all of the chooser code and uncomment the
        getString line to get the auto name from the text box below the Gyro

        You can add additional auto modes by adding additional comparisons to
        the switch structure below with additional strings. If using the
        SendableChooser make sure to add them to the chooser code above as well.
        """
        self.dt.resetAHRS()
        self.phillip = self.m_chooser.getSelected()
        # self.m_autoSelected = SmartDashboard.getString('Auto Selector', kDefaultAuto)
        print(f'Auto selected: {self.phillip}')
        self.gyroStart = self.dt.getAHRS()
        self.phillip.start()
    
    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous."""
        pass

    def teleopInit(self) -> None:
        SmartDashboard.putNumber('Jeff', 0)  # (Shooter velocity) consult Dan for more info on naming this variable
    

        SmartDashboard.putNumber('Gyro kP', Constants.GYROkP)
        SmartDashboard.putNumber('Gyro kI', Constants.GYROkI)
        SmartDashboard.putNumber('Gyro kD', Constants.GYROkD) 
    


        SmartDashboard.putNumber('Shooter kP', Constants.SHOOTER_kP)
        # SmartDashboard.putNumber('Shooter kI', 0)
        SmartDashboard.putNumber('Shooter kD', Constants.SHOOTER_kD)
        # SmartDashboard.putNumber('Shooter kF', 0)
    
    def teleopPeriodic(self) -> None:
        """This function is called periodically during operator control."""
        TeleOp.run()
        # TeleOpTester.run()
        self.dt.feedValues()
        self.climber.climberCurrents()
    
    def testInit(self) -> None:
        # set music selection and LEDS to indicate testing
    
        LEDs.setColor(0.61) # change to flashing red

        # adds subsystems to list to iterate through
        subsystems = [self.dt, self.sh, self.it]

        print(' Running Subsystem checks... ')
        print('----------------------------')

        # iterate through each subsystem check

        print()
        self.dt.checkStart()
        print('------------------------------')
        print()
        self.sh.checkStart()
        print('------------------------------')
        print()
        self.it.checkStart()
        print('------------------------------')
        

        Music.loadMusicSelection(WPI_TalonFX(Constants.SHOOTER_TALON_LEFT), WPI_TalonFX(Constants.SHOOTER_TALON_RIGHT), WPI_TalonFX(Constants.leftClimber), WPI_TalonFX(Constants.rightClimber), 'low_rider.chrp')