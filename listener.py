import sys
import time
import keyboard

from networktables import NetworkTables

print('waiting')
keyboard.wait('[')

if len(sys.argv) > 1:
    NetworkTables.initialize(server=sys.argv[1])
else:
    NetworkTables.initialize()

SmartDashboard = NetworkTables.getTable("SmartDashboard")

SmartDashboard.addEntryListener(lambda *args: print(args), flags=0)

print('initialized')

while True:
    time.sleep(0.1)