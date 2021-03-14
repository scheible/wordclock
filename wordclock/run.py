
from application.applicationManager import *
import time


print("Init application manager")
applicationManager = ApplicationManager()

print("Start application")
applicationManager.startApplication(APPLICATION_ID_CLOCK)

time.sleep(5)
applicationManager.stopApplication()