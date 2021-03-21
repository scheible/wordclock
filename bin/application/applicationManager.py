# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 09:58:31 2021

@author: andre
"""
APPLICATION_ID_ALL = 0
APPLICATION_ID_CLOCK = 1

from application.clock.applicationClock import ApplicationClock
class ApplicationManager():
    
    def __init__(self):
        self.__jsonClockConfigPath = "cfg/Cfg_Clock.json"
        self.__jsonWs2812bPath = "cfg/Drv_ws2812b.json"
        self.__currentApplication = 0
        self.__applicationClock = ApplicationClock(self.__jsonClockConfigPath, self.__jsonWs2812bPath)

    def startApplication(self, appId):
        
        if (appId == APPLICATION_ID_CLOCK):
            self.__applicationClock.start()
            self.__currentApplication = self.__applicationClock
        else:
            print(appId, " is not a valid application Id, no application could be started.")
            
            
    def stopApplication(self):
        self.__currentApplication.stop()
        
        
    def modifyJsonConfig(self, jsonConfig, operationType):
        
        if "brightness" in jsonConfig:
            incr = 0
            print("Change birghtness")
            if jsonConfig["brightness"] == "increase":
                self.__applicationClock.increaseBrightness(1)
            elif jsonConfig["brightness"] == "decrease":
                self.__applicationClock.decreaseBrightness(1)
            if jsonConfig["brightness"] == "increaseHold":
                self.__applicationClock.increaseBrightness(5)
            elif jsonConfig["brightness"] == "decreaseHold":
                self.__applicationClock.decreaseBrightness(5)
            
        else:
            
            applicationJsons = jsonConfig["applications"]
            for applicationJson in applicationJsons:
                appId = applicationJson["appId"]
                
                if (appId == APPLICATION_ID_CLOCK):
                    
                    self.__applicationClock.modifyJsonConfig(applicationJson, operationType)
                    
                    
                else:
                    print(appId, " is not a valid application Id, json could not be set for this application.")
            
    def getJsonConfig(self, appId = APPLICATION_ID_ALL):
        if (appId == APPLICATION_ID_ALL): 
            
            jsonConfig = self.__applicationClock.getJsonConfig()
            localConfig = jsonConfig.copy()
            localConfig = self.buildGeneralJson(localConfig)
            
        elif (appId == APPLICATION_ID_CLOCK):
            jsonConfig = self.__applicationClock.getJsonConfig()
            localConfig = jsonConfig.copy()
            localConfig = self.buildGeneralJson(localConfig)
        else:
            print(appId, " is not a valid application Id, json could not be obtained for this application.")
            
        return localConfig
    
    
    
    def buildGeneralJson(self, jsonConfig):
        generalJson = {
          "applications": [
              jsonConfig
              ]
        }
        return generalJson