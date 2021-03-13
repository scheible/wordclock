# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 09:59:04 2021

@author: andre
"""

from application.clock.ledMatrix import *
from application.clock.clockFrontend import *
from application.application import *
class ApplicationClock(Application):
    
       
    def applicationInit(self):
        jsonConfig = super().getJsonConfig()
        jsonWs2812b = super().getWs2812bJson()
        self.__clockBackend = ClockBackend(jsonConfig)
        self.__clockFrontend = ClockFrontend(jsonConfig, jsonWs2812b)
        
        
    def applicationTask(self, jsonConfig, isUpdateJson):   
        ledMatrix = self.__clockBackend.buildLedMatrixFromCurrentTime(jsonConfig, isUpdateJson)
        self.__clockFrontend.showLedMatrix(ledMatrix)
        