import sys
import time

from networktables import NetworkTables

if len(sys.argv) > 1:
    NetworkTables.initialize(server=sys.argv[1])
else:
    NetworkTables.initialize()

SmartDashboard = NetworkTables.getTable("SmartDashboard")

NetworkTables.addEntryListener(lambda *args: print(args))

while True:
    time.sleep(0.1)