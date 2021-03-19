# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 09:59:35 2021

@author: andre
"""
import time
startTime1 = time.time()

import numpy as np
from scipy.stats import norm
from time import tzset
endTime1 = time.time()
print ("StartUp took1: ", round((endTime1 - startTime1) * 1000), "ms")

DISABLED_LETTER = 1
ENABLED_LETTER = 2

DISABLE_LETTER = 3
ENABLE_LETTER = 4
TEMP_ENABLED_LETTER = 5
UPDATE_LETTER = 6
BORDER_ELEMENT = 7
MINUTE_ELEMENT = 8

DISABLED_MINUTE = 11
ENABLED_MINUTE = 12
DISABLE_MINUTE = 13
ENABLE_MINUTE = 14
TEMP_ENABLE_MINUTE = 15
UPDATE_MINUTE = 16



SECOND_ELEMENT = 40

class LedMatrix:
    
    def __init__(self, jsonConfig):
        
        # Set Matix Body
        self.__num_horizontal_fields = jsonConfig["numLetterHorizontal"]
        self.__num_vertical_fields = jsonConfig["numLetterVertical"]
        self.__matrixBodyState = np.zeros((self.__num_vertical_fields, self.__num_horizontal_fields), dtype=float)
        
         # Set Border Body
        self.__num_border_elements = 4 * jsonConfig["numLedBorderSide"] + 4 * jsonConfig["numLedBorderCorner"]
        self.__num_border_side = jsonConfig["numLedBorderSide"]
        self.__num_border_corner = jsonConfig["numLedBorderCorner"]
        self.__borderBody = np.zeros(self.__num_border_elements, dtype=float)
        self.__minuteBody = np.zeros(self.__num_border_elements, dtype=float)
        
        self.colorLetterRGB =   np.zeros(3, dtype = np.float)
        self.colorMinuteRGB = np.zeros(3, dtype = np.float)
        self.colorSecondRGB = np.zeros(3, dtype = np.float)
        self.colorBorderRGB = np.zeros(3, dtype = np.float)
        
        self.oldColorLetterRGB =   np.zeros(3, dtype = np.float)
        self.oldColorMinuteRGB = np.zeros(3, dtype = np.float)
        self.oldColorSecondRGB = np.zeros(3, dtype = np.float)
        self.oldColorBorderRGB = np.zeros(3, dtype = np.float)
        
        self.colorCurrentLetterRGB = np.zeros(3, dtype = np.float)
        self.colorCurrentMinuteRGB = np.zeros(3, dtype = np.float)
        # Transition times
        self.letterTransitionTime = 0
        self.__minuteTransitionTime = 0
        self.__secondTransitionTime = 0
        self.minute = 0
        self.secondWithMsInFloat = 0
        
        
        # Store Lookup Table for seconds
            
        self.T = 4
        dT = 1e-3
        
        mean = 0
        standard_deviation = self.T / 8
        
        x_values = np.arange(-self.T / 2, self.T / 2 + dT, dT)
        y_values = norm(mean, standard_deviation)
        
        y_values = y_values.pdf(x_values)
        y_values = y_values / np.max(y_values)
        self.secondWeightLookup  = np.round(y_values , 3)
        
        self.ledListToSeconds = 60 / 92 * ((np.arange(92) - self.__num_border_side // 2) % 92)
        
        
        # Init lookup table
        ledsPerElement = jsonConfig["ledsPerLetter"]
        numLedsVertical = ledsPerElement * self.__num_vertical_fields
        numLedsHorizontal = ledsPerElement * self.__num_horizontal_fields
        self.__led_look_up_table = np.zeros((self.__num_vertical_fields * self.__num_horizontal_fields * ledsPerElement, 2), dtype = int)
        for i in range(self.__num_horizontal_fields):
            for j in range(numLedsVertical):
                if (i % ledsPerElement == 1):
                    self.__led_look_up_table[i * numLedsVertical + j, 1] = j // ledsPerElement
                else:
                    self.__led_look_up_table[i * numLedsVertical + j, 1] = (numLedsVertical - j - 1) // ledsPerElement
                self.__led_look_up_table[i * numLedsVertical + j, 0] = self.__num_horizontal_fields - i - 1
                
        # Set Lookup Matrix to decide between border and minute fields
        self.minuteOrBorder = BORDER_ELEMENT * np.ones(self.__num_border_elements, dtype=float)
        for cornerElement in range(1, 5):
            startCorner = cornerElement * self.__num_border_side + (cornerElement - 1) * self.__num_border_corner
            endCorner = startCorner + self.__num_border_corner
            self.minuteOrBorder[startCorner : endCorner] = MINUTE_ELEMENT
        bodyList = self.__matrixBodyState[self.__led_look_up_table[:, 1], self.__led_look_up_table[:, 0]].copy()
        self.minuteOrBorder = np.concatenate((bodyList, self.minuteOrBorder))

    
    def __getTimeDifference(self, timestamp, timearray, base):
        tmp = timearray - timestamp
        tmp = np.sign(tmp) * np.min(np.array([np.abs(tmp), np.abs(tmp - 60)]), axis = 0)
        tmp = np.sign(tmp) * np.min(np.array([np.abs(tmp), np.abs(tmp + 60)]), axis = 0)
        return tmp
    
    def getListFromMatrix(self):
        
        bodyList = self.__matrixBodyState[self.__led_look_up_table[:, 1], self.__led_look_up_table[:, 0]]
        
        if (self.profile["colorBorderRGB"]):
            self.__borderBody = BORDER_ELEMENT * np.ones(self.__num_border_elements, dtype=float)
        else:
            self.__borderBody = np.zeros(self.__num_border_elements, dtype=float)
            
        if (self.profile["brightnessMinute"]):
            self.__borderBody[self.__minuteBody > 0] = self.__minuteBody[self.__minuteBody > 0] 

        
        if (self.profile["brightnessSecond"]):
            self.minuteOrBorder = np.concatenate((bodyList, self.__borderBody)).copy()
            t = self.secondWithMsInFloat
            lowerLimit = (t - self.T / 2) % 60
            upperLimit = (t + self.T / 2) % 60
            if (t < self.T / 2):
                ids = (self.ledListToSeconds > lowerLimit) | (self.ledListToSeconds < upperLimit)
            elif (t > (60 - self.T / 2)):
                ids = (self.ledListToSeconds > lowerLimit) | (self.ledListToSeconds < upperLimit)
            else:
                ids = (self.ledListToSeconds > (t - self.T / 2)) & (self.ledListToSeconds < (t + self.T / 2))
                
            values = self.__getTimeDifference(t, self.ledListToSeconds[ids], 60)
            
            values = np.rint(1000 * values).astype(int)
            
            weights = self.secondWeightLookup[values + self.secondWeightLookup.size // 2]
            self.__borderBody[ids] = SECOND_ELEMENT + weights

        ledList = np.concatenate((bodyList, self.__borderBody))
        return ledList
    def setColorsFromTime(self, time, jsonConfig):
        
        usedProfile = -1
        i = 0
        for userProfile in jsonConfig["userProfiles"]:
            
            # Only check this user profil, if it is marked as active
            if (userProfile["userProfileEnabled"]):
                startTime = userProfile["startTime"]
                stopTime = userProfile["stopTime"]
                
                startTime_s = startTime["hours"] * 3600 + startTime["minutes"] * 60 + startTime["seconds"]
                stopTime_s = stopTime["hours"] * 3600 + stopTime["minutes"] * 60 + stopTime["seconds"]
                
                currentTime_s = time.hour * 3600 + time.minute * 60 + time.second
                # stopTime > startTime-> So time is during the day
                if (stopTime_s > startTime_s):
                    if ((currentTime_s >= startTime_s) and (currentTime_s < stopTime_s)):
                        usedProfile = i
                        break
                    
                # In case startTime > stopTime, the time duration is over the night
                else:
                    if ((currentTime_s >= startTime_s) or (currentTime_s < stopTime_s)):
                        usedProfile = i
                        break
            i = i + 1
            
        # No valid profile found, thus default profile is used
        if (usedProfile == -1):
            self.profile = jsonConfig["defaultProfile"]
        else:
            self.profile = jsonConfig["userProfiles"][usedProfile]["config"]
            
        # Finally update colors and scale birghtness of colors directly here, once and for all
        
        if (self.letterTransitionTime == 0):
            self.oldColorLetterRGB = self.colorLetterRGB.copy()
            self.oldColorMinuteRGB = self.colorMinuteRGB.copy()
        else:
            self.oldColorLetterRGB = self.colorCurrentLetterRGB.copy()
            self.oldColorMinuteRGB = self.colorCurrentMinuteRGB.copy()
        self.oldColorSecondRGB = self.colorSecondRGB
        self.oldColorBorderRGB = self.colorBorderRGB
    
        self.colorLetterRGB =   (self.profile["brightnessBody"] / 255)   * np.array(self.profile["colorBodyRGB"], dtype=np.float)
        self.colorMinuteRGB = (self.profile["brightnessMinute"] / 255) * np.array(self.profile["colorMinuteRGB"], dtype=np.float)
        self.colorSecondRGB = (self.profile["brightnessSecond"] / 255) * np.array(self.profile["colorSecondRGB"], dtype=np.float)
        self.colorBorderRGB = (self.profile["brightnessBorder"] / 255) * np.array(self.profile["colorBorderRGB"], dtype=np.float)
        
    def preUpdate(self):
        self.__matrixBodyState[self.__matrixBodyState == DISABLE_LETTER] = DISABLED_LETTER
        self.__matrixBodyState[self.__matrixBodyState == ENABLE_LETTER]  = TEMP_ENABLED_LETTER
        self.__matrixBodyState[self.__matrixBodyState == ENABLED_LETTER] = TEMP_ENABLED_LETTER
        self.__matrixBodyState[self.__matrixBodyState == UPDATE_LETTER]  = TEMP_ENABLED_LETTER

        
        
        
        self.__minuteBody[self.__minuteBody == DISABLE_MINUTE] = BORDER_ELEMENT
        self.__minuteBody[self.__minuteBody == ENABLE_MINUTE] = TEMP_ENABLE_MINUTE
        self.__minuteBody[self.__minuteBody == ENABLED_MINUTE] = TEMP_ENABLE_MINUTE
        self.__minuteBody[self.__minuteBody == UPDATE_MINUTE] = TEMP_ENABLE_MINUTE


        
            
    def postUpdate(self, jsonUpdate):
        if (jsonUpdate):
            if (np.sum(np.abs(self.oldColorLetterRGB - self.colorLetterRGB)) > 0):
                self.__matrixBodyState[self.__matrixBodyState == ENABLED_LETTER] = UPDATE_LETTER
                self.__matrixBodyState[self.__matrixBodyState == ENABLE_LETTER] = UPDATE_LETTER
                
            if (np.sum(np.abs(self.oldColorMinuteRGB - self.colorMinuteRGB)) > 0):
                self.__minuteBody[self.__minuteBody == ENABLED_MINUTE] = UPDATE_MINUTE
                self.__minuteBody[self.__minuteBody == ENABLE_MINUTE] = UPDATE_MINUTE
                
        self.__matrixBodyState[self.__matrixBodyState == TEMP_ENABLED_LETTER] = DISABLE_LETTER
        self.__minuteBody[self.__minuteBody == TEMP_ENABLE_MINUTE] = DISABLE_MINUTE
        
        if (self.profile["isSoftTransitionEnabled"]):
            self.letterTransitionTime = self.profile["transitionTimeMs"]
            
        
            
    def enableLetters(self, line, start, length):
        if (self.__matrixBodyState[line, start] != TEMP_ENABLED_LETTER):
            self.__matrixBodyState[line, start : start + length] = ENABLE_LETTER
        else:
            self.__matrixBodyState[line, start : start + length] = ENABLED_LETTER
            
    def updateMinuteField(self, minute):
        
        if (self.profile["brightnessMinute"]):
            for cornerElement in range(1, minute + 1):
                startCorner = cornerElement * self.__num_border_side + (cornerElement - 1) * self.__num_border_corner
                endCorner = startCorner + self.__num_border_corner

                if (self.__minuteBody[startCorner] == TEMP_ENABLE_MINUTE):
                    self.__minuteBody[startCorner : endCorner] = ENABLED_MINUTE
                else:
                    self.__minuteBody[startCorner : endCorner] = ENABLE_MINUTE



        
from datetime import datetime
class ClockBackend:
    
    
    def __init__(self, jsonConfig):
        self.__ledMatrix = LedMatrix(jsonConfig)
        self.__lastHour = -1
        self.__lastMinute = -1
        self.__lastSecond = -1
        

    def isUpdateNecessary(self):
        currentTime = datetime.now()
        hour = currentTime.hour
        minute = currentTime.minute
        second = currentTime.second
        

        
        updateNecessary = False
        if(hour != self.__lastHour) or (minute != self.__lastMinute) or(second != self.__lastSecond):
            updateNecessary = True
        return updateNecessary
        
    def buildLedMatrixFromCurrentTime(self, jsonConfig, updateJson=False):
        
       # Call tzset() to check if timezone was changed.
       tzset()
       
       # Get current time
       currentTime = datetime.now()
       
       # Extract the current hour, minute and second
       hour = currentTime.hour
       minute = currentTime.minute
       second = currentTime.second
       
       
       # Store the currend second in a float variable inside LED matrix.
       self.__ledMatrix.secondWithMsInFloat = second + currentTime.microsecond / 1000000
        
       
       # Only perform update if either the hour or minute has changed - or
       # in case a json update is requested
       if(hour != self.__lastHour) or (minute != self.__lastMinute) or updateJson:

           # Update the colors of the LED matrix if needed
           self.__ledMatrix.setColorsFromTime(currentTime, jsonConfig)
           
           # Call the pre Update of the led matrix
           self.__ledMatrix.preUpdate()
           
           # Update the letter and minute for the matrix
           self.__setMatrixFromTime(currentTime)
           
           # Call the post Update of the led matrix
           self.__ledMatrix.postUpdate(updateJson)

       
       # Return the led matrix
       return self.__ledMatrix
        
    def __setMatrixFromTime(self, time):
        
        # Get the current hour, minute and second from the time
        hour = time.hour
        minute = time.minute
        second = time.second
        
        # save the current hour and minute as last hour and last minute
        self.__lastHour = hour
        self.__lastMinute = minute
        
        # Update the minute field of the led matrix
        self.__ledMatrix.updateMinuteField(minute % 5)
        
        self.__ES()
        self.__IST()
    
        if (minute < 5):
            self.__UHR()
        elif (minute < 10):
            self.__FUENF1()
            self.__NACH()
        elif (minute < 15):
            self.__ZEHN1()
            self.__NACH()
        elif (minute < 20):
            self.__VIERTEL()
            self.__NACH()
        elif (minute < 25):
            self.__ZWANZIG()
            self.__NACH()
        elif (minute < 30):
            self.__FUENF1()
            self.__VOR()
            self.__HALB()
        elif (minute < 35):
            self.__HALB()
        elif (minute < 40):
            self.__FUENF1()
            self.__NACH()
            self.__HALB()
        elif (minute < 45):
            self.__ZEHN1()
            self.__NACH()
            self.__HALB()
        elif (minute < 50):
            self.__DREIVIERTEL()
        elif (minute < 55):
            self.__ZEHN1()
            self.__VOR()
        else:
            self.__FUENF1()
            self.__VOR()


        if (minute >= 00 and minute < 25):
            self.__hour(hour % 12)
        else:
            self.__hour((hour+1)     % 12)
    

    def __hour(self, h):

        if (h == 0):
            self.__ZWOELF()
        elif (h == 1):
            self.__EIN()
        elif (h == 2):
            self.__ZWEI()
        elif (h == 3):
            self.__DREI()
        elif (h == 4):
            self.__VIER()
        elif (h == 5):
            self.__FUENF2()
        elif (h == 6):
            self.__SECHS()
        elif (h == 7):
            self.__SIEBEN()
        elif (h == 8):
            self.__ACHT()
        elif (h == 9):
            self.__NEUN()
        elif (h == 10):
            self.__ZEHN2()
        elif (h == 11):
            self.__ELF()
        elif (h == 12):
            self.__ZWOELF()
            
    def __ES(self):
        self.__ledMatrix.enableLetters(0, 0, 2)
    
    def __IST(self):
        self.__ledMatrix.enableLetters(0, 3, 3)
    
    def __FUENF1(self):
        self.__ledMatrix.enableLetters(0, 7, 4)
    
    def __ZEHN1(self):
        self.__ledMatrix.enableLetters(1, 0, 4)
    
    def __VIERTEL(self):
        self.__ledMatrix.enableLetters(2, 4, 7)
    
    def __ZWANZIG(self):
        self.__ledMatrix.enableLetters(1, 4, 7)
    
    def __DREIVIERTEL(self):
        self.__ledMatrix.enableLetters(2, 0, 11)
    
    def __VOR(self):
        self.__ledMatrix.enableLetters(3, 0, 3)
    
    def __NACH(self):
        self.__ledMatrix.enableLetters(3, 7, 4)
    
    def __HALB(self):
        self.__ledMatrix.enableLetters(4, 0, 4)
    
    def __UHR(self):
        self.__ledMatrix.enableLetters(9, 8, 3)
    
    def __EIN(self):
        self.__ledMatrix.enableLetters(5, 0, 3)
    
    def __ZWEI(self):
        self.__ledMatrix.enableLetters(5, 7, 4)
    
    def __DREI(self):
        self.__ledMatrix.enableLetters(6, 0, 4)
    
    def __VIER(self):
        self.__ledMatrix.enableLetters(6, 7, 4)
    
    def __FUENF2(self):
        self.__ledMatrix.enableLetters(4, 7, 4)
    
    def __SECHS(self):
        self.__ledMatrix.enableLetters(7, 0, 5)
    
    def __SIEBEN(self):
        self.__ledMatrix.enableLetters(8, 0, 6)
    
    def __ACHT(self):
        self.__ledMatrix.enableLetters(7, 7, 4)
    
    def __NEUN(self):
        self.__ledMatrix.enableLetters(9, 3, 4)
    
    def __ZEHN2(self):
        self.__ledMatrix.enableLetters(9, 0, 4)
    
    def __ELF(self):
        self.__ledMatrix.enableLetters(4, 5, 3)
    
    def __ZWOELF(self):
        self.__ledMatrix.enableLetters(8, 6, 5)
    
    
