

class Constants:

    ELEVATOR_TALON = 8
    SHOOTER_TALON_RIGHT = 4
    SHOOTER_TALON_LEFT = 11
    kPIDLoopIdx = 0
    kTimeoutMs = 30

    SHOOTER_kP = 0.15
    SHOOTER_kI = 0
    SHOOTER_kD = 4
    SHOOTER_FEED_FWD = .048

    XBOX_DRIVER = 0
    XBOX_MANIP = 1

    SOLENOID_HOOD = 3

    LAYUP_POSITION = -1
    LAYUP_SPEED = 5000

    TARGET_HEIGHT = 55
    LIMELIGHT_ANGLE = 39.14

    TALON_LEFTBACK = 15
    TALON_LEFTFRONT = 13
    TALON_RIGHTBACK = 1
    TALON_RIGHTFRONT = 2 
    TALON_RIGHTMIDDLE = 20
    TALON_LEFTMIDDLE = 14
	

    LED_CHANNEL = 3
    SOLENOID_SHIFTER = 1

    kP = 0
    kI = 0
    kD = 0
    kIz = 0

    kP2 = 0.04
    kI2 = 0
    kD2 = 0
    kIz2 = 0

    GYROkP = 0.02
    GYROkI = 0
    GYROkD = 0.0015

    kMinOutput = -1
    kMaxOutput = 1
    DRIVETRAIN_TEST_RPM = 0

    DTMAX_AUTO_SPEED = 0.28

	# motor checks
    DT_ACCEPTED_MAX_CURRENT = 0 # at 80% power
    DT_ACCEPTED_MIN_CURRENT = 0
	
    DT_ACCEPTED_MAX_VELOCITY = 0
    DT_ACCEPTED_MIN_VELOCITY = 0

    LAUNCHER_ACCEPTED_MAX_CURRENT = 5 # at 75% power
    LAUNCHER_ACCEPTED_MIN_CURRENT = 2.5 
	
    LAUNCHER_ACCEPTED_MIN_VELOCITY = 19000 
    LAUNCHER_ACCEPTED_MAX_VELOCITY = 22000 

    TALONSRX_ACCEPTED_MIN_VELOCITY = 0 # at 100% power
    TALONSRX_ACCEPTED_MIN_CURRENT = 0

    TALONSRX_ACCEPTED_MAX_CURRENT = 0
    TALONSRX_ACCEPTED_MAX_VELOCITY = 0


	# Intake
    INTAKE_BELT = 8
    INTAKE_INGESTORBAR = 5
    INTAKE_INGESTOR = 9


	# Shooter formulas
    ACTUATOR_LAYUP = -1 # minimum value at close range (layup value)
    POWER_LAYUP = 4000	# minimum power at close range (layup value)
    ACTUATOR_SLOPE = 0		
    POWER_SLOPE = 0
	
	
	# climber
    leftClimber = 7
    rightClimber = 12
    CLIMBER_SOLENOID = 4
    CLIMBER_STOPPER = 0

    CLIMB_I_LIMIT=10 # A
    CLIMB_I_THRESHOLD=20 # A
    CLIMB_I_THRESHOLD_TIME=100 # sec

	# sensor values
    COLOR_HIGH = 9
    BELT_BALL_MOVED = -3500 # encoder value belt moves up when ball is detected
    COLOR_LOW = 8
