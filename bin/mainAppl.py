#!env/bin/python -u

from application.applicationManager import *
from shared.ipc import *

import time


print("Init application manager")
applicationManager = ApplicationManager()

print ("Start application")
#applicationManager.startApplication(APPLICATION_ID_CLOCK)

print("Daemon Component Ipc Bindung")
daemonComponentIpcBindung = DaemonComponentIpcBindung()

jsonConfig = applicationManager.getJsonConfig()
daemonComponentIpcBindung.sendCommand(jsonConfig)
lasttime = 0
framecount = 0
while True:
    applicationManager.startApplication(APPLICATION_ID_CLOCK)
    jsonConfig = applicationManager.getJsonConfig()
    state, data = daemonComponentIpcBindung.receiveCommand(jsonConfig)
    
    if ((state == NEW_JSON_UPDATE) or (state == NEW_JSON_REMOVE) or (state == NEW_JSON_ADD)):
        applicationManager.modifyJsonConfig(data, state)
        jsonConfig = applicationManager.getJsonConfig()
        daemonComponentIpcBindung.sendCommand(jsonConfig)

    framecount = framecount + 1
    if (time.time() - lasttime > 1):
        lasttime = time.time()
        print("Frame count: " + str(framecount))
        framecount = 0
    
     


print("Start application")
applicationManager.startApplication(APPLICATION_ID_CLOCK)

time.sleep(5)
applicationManager.stopApplication()