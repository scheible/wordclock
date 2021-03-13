# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 09:59:25 2021

@author: andre
"""
import time
from application.clock.ledMatrix import *
from shared.ledBinding import * 
class ClockFrontend:
    
    def __init__(self, jsonConfig, jsonWs2812b):
        self.__oldLedMatrix = -1
        self.__lastTimeStamp = round(time.time() * 1000)
        self.numberOfLeds = 312
        self.__ledBinding = LedBinding(jsonWs2812b, self.numberOfLeds )
        
        
        
    def __toIntegerColor(self, color):
        red = color[..., 0].astype(int)
        green = color[..., 1].astype(int)
        blue = color[..., 2].astype(int)

        col = (red << 16)| (green << 8) | blue
        return col
        
        
    def showLedMatrix(self, ledMatrix, jsonConfig = -1):
        
        currentTime = round(time.time() * 1000)
        executionTime = currentTime - self.__lastTimeStamp 
        
        self.__lastTimeStamp = currentTime
        
        
        ledList = np.zeros(self.numberOfLeds, dtype=int)
        
        if (ledMatrix.profile["isSoftTransitionEnabled"]):
            if (ledMatrix.letterTransitionTime  > 0):
                if (ledMatrix.letterTransitionTime  < executionTime):
                    ledMatrix.letterTransitionTime  = 0
                else:
                    ledMatrix.letterTransitionTime = ledMatrix.letterTransitionTime - executionTime
                    
            letterSoftTransitionRatio = 1 - (ledMatrix.letterTransitionTime / ledMatrix.profile["transitionTimeMs"])
            
            colorEnableLetter = self.__toIntegerColor(letterSoftTransitionRatio * ledMatrix.colorLetterRGB)
            colorDisableLetter = self.__toIntegerColor((1 - letterSoftTransitionRatio) * ledMatrix.colorLetterRGB)
            colorEnabledLetter = self.__toIntegerColor(ledMatrix.colorLetterRGB)
            
            
            listFromMatrix = ledMatrix.getListFromMatrix()
            
            ledList[listFromMatrix == ENABLED_LETTER] = colorEnabledLetter
            ledList[listFromMatrix == ENABLE_LETTER] = colorEnableLetter
            ledList[listFromMatrix == DISABLE_LETTER] = colorDisableLetter
        else:
            listFromMatrix = ledMatrix.getListFromMatrix()
            colorEnabledLetter = self.__toIntegerColor(ledMatrix.colorLetterRGB)
            ledList[listFromMatrix == ENABLED_LETTER] = colorEnabledLetter
            
        ledList[listFromMatrix == BORDER_ELEMENT] = self.__toIntegerColor(ledMatrix.colorBorderRGB)
        ledList[listFromMatrix == MINUTE_ELEMENT] = self.__toIntegerColor(ledMatrix.colorMinuteRGB)
        if (ledMatrix.profile["isSecondShown"]):
            ledList[listFromMatrix >= SECOND_ELEMENT] = self.__toIntegerColor(np.expand_dims((listFromMatrix[listFromMatrix >= SECOND_ELEMENT] - SECOND_ELEMENT), axis = 1) * (ledMatrix.colorSecondRGB - ledMatrix.colorBorderRGB)+ ledMatrix.colorBorderRGB)
        midTime = round(time.time() * 1000)
        self.__ledBinding.showLedList(ledList)
        endTime = round(time.time() * 1000)
        #print("Execution time took: ", executionTime, "ms, Flashing took: ", (endTime - midTime), "ms. The rest was: ", (midTime - currentTime), "ms")
        
        
        
        
        
        