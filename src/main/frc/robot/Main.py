if __name__ == '__main__':
    import os
    import site
    os.chdir('src/main')
    site.addsitedir(os.getcwd())

import wpilib

import frc.robot.Robot as Robot

if __name__ == '__main__':
    wpilib.run(Robot)