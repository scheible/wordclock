# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 09:58:46 2021

@author: andre
"""

import threading
import json
import os.path
from os import path
from shared.ipc import *
from shared.jsonhandler import *
class Application:
    
    def __init__(self, jsonFilePath, jsonWs2812bPath):
        
        
        self.__jsonFilePath = jsonFilePath
        self.__jsonWs2812bPath = jsonWs2812bPath
        self.__readFromJsonFile()
        self.__isJsonValid = self.validateJson(self.__jsonFilePath)
        
        if (self.__isJsonValid):
            self.stop_threads = False;
            self.updateJsonCounter = 0;
            self.__application_thread = threading.Thread(target = self.applicationThread, args = (lambda : self.stop_threads, lambda : self.updateJsonCounter, lambda : self.__jsonConfig)) 
            self.applicationInit()
        else:
            print("The file: ", jsonFilePath, " was not valid. Application will exit!")
            exit()
        
        
        
        
    def __writeJsonFile(self):
        if (self.__isJsonValid):
            with open(self.__jsonFilePath, "w") as write_file:
                json.dump(self.__jsonConfig, write_file, indent=4)
                
    def __readFromJsonFile(self):
        if path.exists(self.__jsonFilePath):
            with open(self.__jsonFilePath, "r") as jsonReadFile:
                self.__jsonConfig = json.load(jsonReadFile)
                
        if path.exists(self.__jsonWs2812bPath):
            with open(self.__jsonWs2812bPath, "r") as jsonReadFile:
                self.__jsonWs2812b = json.load(jsonReadFile)
    
        
    def modifyJsonConfig(self, jsonConfig, operationType):
        print ("Request json config update")
        _tempJsonConfig = self.__jsonConfig.copy()
        
        isUpdated = False
        if ((operationType == NEW_JSON_UPDATE)):
            isUpdated = updateJson(_tempJsonConfig, jsonConfig)
        elif (operationType == NEW_JSON_ADD):
            pass
        elif (operationType == NEW_JSON_REMOVE):
            isUpdated = updateJson(_tempJsonConfig, jsonConfig)
    
        if (isUpdated):
             if (self.validateJson(_tempJsonConfig)):
                 self.__jsonConfig = _tempJsonConfig.copy()
                 self.__writeJsonFile()
                 self.updateJsonCounter = (self.updateJsonCounter + 1) & 0xFF
             else:
                print("Given json config is not valid!")
                
                
        
    def getJsonConfig(self):
        return self.__jsonConfig
    
    def getWs2812bJson(self):
        return self.__jsonWs2812b


    def validateJson(self, jsonConfig):
        return True
    
    def start(self):
        self.__application_thread.start()
            
    def stop(self):
        print("Request application thread to stop")
        self.stop_threads = True;

    def applicationThread(self, stop_threads, updateJsonCounter, jsonConfig):
        oldUpdateCounter = 0
        print("Start runner")
        while(True):
            
            if stop_threads():
                print("Application thread will stop")
                break                
            
            if (oldUpdateCounter != updateJsonCounter()):
                print("Detect json Update")
                oldUpdateCounter = updateJsonCounter()
                self.applicationTask(jsonConfig(), True)
            else:
                self.applicationTask(jsonConfig(), False)
            

        
    def applicationTask(self, jsonConfig, isUpdateJson):
        pass
    
    def applicationInit(self):
        pass