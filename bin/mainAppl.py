#!env/bin/python -u

from application.applicationManager import *
from shared.ipc import *

import time


print("Init application manager")
applicationManager = ApplicationManager()

print ("Start application")
applicationManager.startApplication(APPLICATION_ID_SNAKE)

print("Daemon Component Ipc Bindung")
daemonComponentIpcBindung = DaemonComponentIpcBindung()

jsonConfig = applicationManager.getJsonConfig()
daemonComponentIpcBindung.sendCommand(jsonConfig)

while True:
    
    jsonConfig = applicationManager.getJsonConfig()
    state, data = daemonComponentIpcBindung.receiveCommand(jsonConfig)
    
    if ((state == NEW_JSON_UPDATE) or (state == NEW_JSON_REMOVE) or (state == NEW_JSON_ADD)):
        if (applicationManager.modifyJsonConfig(data, state)):
            jsonConfig = applicationManager.getJsonConfig()
            daemonComponentIpcBindung.sendCommand(jsonConfig)
    elif (state == START_APP):
        appId = data.get('appId')
        applicationManager.startApplication(appId)
        jsonConfig = applicationManager.getJsonConfig()
        daemonComponentIpcBindung.sendCommand(jsonConfig)

    else:
        time.sleep(0.1)
        
        
        
     


print("Start application")
applicationManager.startApplication(APPLICATION_ID_CLOCK)

time.sleep(5)
applicationManager.stopApplication()