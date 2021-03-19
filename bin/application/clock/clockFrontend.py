# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 09:59:25 2021

@author: andre
"""
import time
startTime2 = time.time()
from application.clock.ledMatrix import *
from shared.ledBinding import * 
endTime2 = time.time()
print ("StartUp took2: ", round((endTime2 - startTime2) * 1000), "ms")
class ClockFrontend:
    
    def __init__(self, jsonConfig, jsonWs2812b):
        self.__oldLedMatrix = -1
        self.__lastTimeStamp = round(time.time() * 1000)
        self.numberOfLeds = 312
        self.__ledBinding = LedBinding(jsonWs2812b, self.numberOfLeds, jsonConfig["brightness"] )
        
        
        
    def __toIntegerColor(self, color):
        red = color[..., 0].astype(int)
        green = color[..., 1].astype(int)
        blue = color[..., 2].astype(int)

        col = (red << 16)| (green << 8) | blue
        return col
        
    def setBrightness(self, brightness):
        self.__ledBinding.setBrightness(brightness)
        
    def showLedMatrix(self, ledMatrix):
        
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
            colorUpdateLetter = self.__toIntegerColor(letterSoftTransitionRatio * (ledMatrix.colorLetterRGB - ledMatrix.oldColorLetterRGB) + ledMatrix.oldColorLetterRGB)
            
            
            # Min
            if (ledMatrix.profile["brightnessBorder"] > 0):
                colorEnableMinute = self.__toIntegerColor(letterSoftTransitionRatio * (ledMatrix.colorMinuteRGB - ledMatrix.colorBorderRGB) + ledMatrix.colorBorderRGB)
                colorDisableMinute = self.__toIntegerColor((1 - letterSoftTransitionRatio) * (ledMatrix.colorMinuteRGB - ledMatrix.colorBorderRGB) + ledMatrix.colorBorderRGB)
            else:
                colorEnableMinute = self.__toIntegerColor(letterSoftTransitionRatio * ledMatrix.colorMinuteRGB)
                colorDisableMinute = self.__toIntegerColor((1 - letterSoftTransitionRatio) * ledMatrix.colorMinuteRGB)
            colorEnabledMinute = self.__toIntegerColor(ledMatrix.colorMinuteRGB)
            colorUpdateMinute = self.__toIntegerColor(letterSoftTransitionRatio * (ledMatrix.colorMinuteRGB - ledMatrix.oldColorMinuteRGB) + ledMatrix.oldColorMinuteRGB)
            
            
            
            listFromMatrix = ledMatrix.getListFromMatrix()
            #print(colorUpdateLetter)
            #print(ledList[listFromMatrix == UPDATE_LETTER])
            ledList[listFromMatrix == ENABLED_LETTER] = colorEnabledLetter
            ledList[listFromMatrix == ENABLE_LETTER] = colorEnableLetter
            ledList[listFromMatrix == DISABLE_LETTER] = colorDisableLetter
            ledList[listFromMatrix == UPDATE_LETTER] = colorUpdateLetter
            
            # Minute
            ledList[listFromMatrix == ENABLED_MINUTE] = colorEnabledMinute
            ledList[listFromMatrix == ENABLE_MINUTE] = colorEnableMinute
            ledList[listFromMatrix == DISABLE_MINUTE] = colorDisableMinute
            ledList[listFromMatrix == UPDATE_MINUTE] = colorUpdateMinute
            
            
            ledMatrix.colorCurrentLetterRGB = letterSoftTransitionRatio * (ledMatrix.colorLetterRGB - ledMatrix.oldColorLetterRGB) + ledMatrix.oldColorLetterRGB
            ledMatrix.colorCurrentMinuteRGB = letterSoftTransitionRatio * (ledMatrix.colorMinuteRGB - ledMatrix.oldColorMinuteRGB) + ledMatrix.oldColorMinuteRGB
        else:
            listFromMatrix = ledMatrix.getListFromMatrix()
            colorEnabledLetter = self.__toIntegerColor(ledMatrix.colorLetterRGB)
            ledList[listFromMatrix == ENABLED_LETTER | listFromMatrix == UPDATE_LETTER] = colorEnabledLetter
            ledList[listFromMatrix == MINUTE_ELEMENT] = self.__toIntegerColor(ledMatrix.colorMinuteRGB)
            
        ledList[listFromMatrix == BORDER_ELEMENT] = self.__toIntegerColor(ledMatrix.colorBorderRGB)
        
        if (ledMatrix.profile["brightnessSecond"]):
            
            if (ledMatrix.profile["brightnessBorder"] and ledMatrix.profile["brightnessMinute"]):
                borderIds = (listFromMatrix >= SECOND_ELEMENT) & ((ledMatrix.minuteOrBorder == BORDER_ELEMENT) | (ledMatrix.minuteOrBorder == DISABLE_MINUTE) | (ledMatrix.minuteOrBorder == DISABLED_MINUTE))
                minuteIds = (listFromMatrix >= SECOND_ELEMENT) & ((ledMatrix.minuteOrBorder == ENABLED_MINUTE) | (ledMatrix.minuteOrBorder == ENABLE_MINUTE) | (ledMatrix.minuteOrBorder == UPDATE_MINUTE))
                ledList[borderIds] = self.__toIntegerColor(np.expand_dims((listFromMatrix[borderIds] - SECOND_ELEMENT), axis = 1) * (ledMatrix.colorSecondRGB - ledMatrix.colorBorderRGB)+ ledMatrix.colorBorderRGB)
                ledList[minuteIds] = self.__toIntegerColor(np.expand_dims((listFromMatrix[minuteIds] - SECOND_ELEMENT), axis = 1) * (ledMatrix.colorSecondRGB - ledMatrix.colorMinuteRGB)+ ledMatrix.colorMinuteRGB)
            elif (ledMatrix.profile["brightnessBorder"] and ledMatrix.profile["brightnessMinute"] == 0):
                borderIds = (listFromMatrix >= SECOND_ELEMENT) & ((ledMatrix.minuteOrBorder == BORDER_ELEMENT) | (ledMatrix.minuteOrBorder == DISABLE_MINUTE) | (ledMatrix.minuteOrBorder == DISABLED_MINUTE))
                minuteIds = (listFromMatrix >= SECOND_ELEMENT) & ((ledMatrix.minuteOrBorder == ENABLED_MINUTE) | (ledMatrix.minuteOrBorder == ENABLE_MINUTE) | (ledMatrix.minuteOrBorder == UPDATE_MINUTE))
                ledList[borderIds] = self.__toIntegerColor(np.expand_dims((listFromMatrix[borderIds] - SECOND_ELEMENT), axis = 1) * (ledMatrix.colorSecondRGB - ledMatrix.colorBorderRGB)+ ledMatrix.colorBorderRGB)
                ledList[minuteIds] = self.__toIntegerColor(np.expand_dims((listFromMatrix[minuteIds] - SECOND_ELEMENT), axis = 1) * ledMatrix.colorSecondRGB)
            elif (ledMatrix.profile["brightnessBorder"] == 0 and ledMatrix.profile["brightnessMinute"]):
                borderIds = (listFromMatrix >= SECOND_ELEMENT) & ((ledMatrix.minuteOrBorder == BORDER_ELEMENT) | (ledMatrix.minuteOrBorder == DISABLE_MINUTE) | (ledMatrix.minuteOrBorder == DISABLED_MINUTE))
                minuteIds = (listFromMatrix >= SECOND_ELEMENT) & ((ledMatrix.minuteOrBorder == ENABLED_MINUTE) | (ledMatrix.minuteOrBorder == ENABLE_MINUTE) | (ledMatrix.minuteOrBorder == UPDATE_MINUTE))
                ledList[borderIds] = self.__toIntegerColor(np.expand_dims((listFromMatrix[borderIds] - SECOND_ELEMENT), axis = 1) * ledMatrix.colorSecondRGB)
                ledList[minuteIds] = self.__toIntegerColor(np.expand_dims((listFromMatrix[minuteIds] - SECOND_ELEMENT), axis = 1) * (ledMatrix.colorSecondRGB - ledMatrix.colorMinuteRGB)+ ledMatrix.colorMinuteRGB)
            else:
                borderIds = (listFromMatrix >= SECOND_ELEMENT) & ((ledMatrix.minuteOrBorder == BORDER_ELEMENT) | (ledMatrix.minuteOrBorder == DISABLE_MINUTE) | (ledMatrix.minuteOrBorder == DISABLED_MINUTE))
                minuteIds = (listFromMatrix >= SECOND_ELEMENT) & ((ledMatrix.minuteOrBorder == ENABLED_MINUTE) | (ledMatrix.minuteOrBorder == ENABLE_MINUTE) | (ledMatrix.minuteOrBorder == UPDATE_MINUTE))
                ledList[borderIds] = self.__toIntegerColor(np.expand_dims((listFromMatrix[borderIds] - SECOND_ELEMENT), axis = 1) * ledMatrix.colorSecondRGB)
                ledList[minuteIds] = self.__toIntegerColor(np.expand_dims((listFromMatrix[minuteIds] - SECOND_ELEMENT), axis = 1) * ledMatrix.colorSecondRGB)
        midTime = round(time.time() * 1000)
        self.__ledBinding.showLedList(ledList)
        endTime = round(time.time() * 1000)
        #print("Execution time took: ", executionTime, "ms, Flashing took: ", (endTime - midTime), "ms. The rest was: ", (midTime - currentTime), "ms")
        
        
        
        
        
        