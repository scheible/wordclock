# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 11:59:14 2021

@author: andre
"""

import RPi.GPIO as GPIO
import time
import threading

ACTION_TYPE_KEY_PRESSED = 1
ACTION_TYPE_KEY_RELEASED = 2
ACTION_TYPE_KEY_HOLD = 3

class myButton:
    
    def __init__(self, gpioPin, bounceTime):
        self.gpioPin = gpioPin

        self.keyPressedActions = []
        self.keyReleasedActions = []
        self.keyHoldActions = []
        
        self.bounceTime = bounceTime
        #self.__buttonThread = threading.Thread(target = self.buttonThread, args = (lambda : self.isButtonReleased, self.actionList)) 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpioPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        
        
        self.buttonPressTimeForRelease = 0
        self.lastButtonPressTime = time.time()
        
        self.hasRegisteredEvent = False
        
        
    def __del__(self):
        GPIO.cleanup()
        
        
    def buttonThread(self, isButtonReleased, actionList):
        startTime = time.time()
        
        actionPressed = [False] * len(actionList)
        while(True):
            if isButtonReleased():
                break
            
            buttonTime = round((time.time()- startTime) * 1000)
            
            for actionId in range(len(actionList)):
                if not actionPressed[actionId]:
                    action = actionList[actionId]
                    if (buttonTime >= action["MinTime"]):
                        action["Callback"]()
                        actionPressed[actionId] = True
                    
            
            time.sleep(0.01)
            
            
            
        print ("Button duration was: ", buttonTime, "ms")
            
        
    def buttonAction(self, channel):
        if (GPIO.input(channel) == 0):
            self.buttonPressed()
        else:
            self.buttonReleased()
        
        
    def buttonHold(self):
        
        #Check if button is still pressed
        if (GPIO.input(self.gpioPin) == 0):
            for holdAction in self.keyHoldActions:
                holdAction[1]()
                threading.Timer(holdAction[0] / 1000, self.buttonHold).start()
                
    def buttonPressed(self):
        pressTime = round((time.time() - self.lastButtonPressTime) * 1000)
        print("Key pressed. Time past since last press: ", pressTime, "ms")
        
        
        # Start a thread with the min duration to check if a button was hold for the period of time.
        for holdTime in self.keyHoldActions:
            threading.Timer(holdTime[0] / 1000, self.buttonHold).start()
        
        
        for protectionTime in self.keyPressedActions:
            if (pressTime) > protectionTime[0]:
                protectionTime[1]()
                self.lastButtonPressTime = time.time()
                
        if (self.buttonPressTimeForRelease == 0):
            self.buttonPressTimeForRelease = time.time()
                
    
    def buttonReleased(self):
        releaseTime = round((time.time() - self.buttonPressTimeForRelease) * 1000)
        print("Button released. Button was pressed for: ", releaseTime, "ms")
        print("")
        for releaseAction in self.keyReleasedActions:
            if (releaseTime) > releaseAction[0]:
                releaseAction[1]()
                
        self.buttonPressTimeForRelease = 0

        
    
    
    def addButtonAction(self, actionType, callbackFunction, time):
                
        if (not self.hasRegisteredEvent):
            GPIO.add_event_detect(self.gpioPin, GPIO.BOTH, callback=self.buttonAction , bouncetime = self.bounceTime)
            self.hasRegisteredEvent = True
            
        if (actionType == ACTION_TYPE_KEY_PRESSED):
            self.keyPressedActions.append([time, callbackFunction])
        elif (actionType == ACTION_TYPE_KEY_RELEASED):
            self.keyReleasedActions.append([time, callbackFunction])
        elif (actionType == ACTION_TYPE_KEY_HOLD):
            self.keyHoldActions.append([time, callbackFunction])
            


    
    