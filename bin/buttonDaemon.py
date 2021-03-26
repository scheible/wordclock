# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 11:31:35 2021

@author: andre
"""

import time
from shared.myButton import *
import shared.ipc


communication = shared.ipc.WebserverComponentIpcSender()
increaseBrightness = '{  "commandType": "set", "dat": 	{"brightness": "increase"}}'
decreaseBrightness = '{  "commandType": "set", "dat": 	{"brightness": "decrease"}}'
increaseBrightnessHold = '{  "commandType": "set", "dat": 	{"brightness": "increaseHold"}}'
decreaseBrightnessHold = '{  "commandType": "set", "dat": 	{"brightness": "decreaseHold"}}'


def leftButtonFunction():
    r = communication.send(decreaseBrightness)
def leftButtonFunctionHold():
    r = communication.send(decreaseBrightnessHold)

def middleButtonFunctionHold():
     print("You are pressing the middle button: ")
     
     
def rightButtonFunction():
     r = communication.send(increaseBrightness)
def rightButtonFunctionHold():
     r = communication.send(increaseBrightnessHold)
     
     
bounceTime = 20
leftButton = myButton(17, bounceTime)
leftButton.addButtonAction(ACTION_TYPE_KEY_PRESSED, leftButtonFunction, 100)
leftButton.addButtonAction(ACTION_TYPE_KEY_HOLD, leftButtonFunctionHold, 150)


middleButton = myButton(27, bounceTime)
middleButton.addButtonAction(ACTION_TYPE_KEY_HOLD, middleButtonFunctionHold, 2000)
rightButton = myButton(22, bounceTime)
rightButton.addButtonAction(ACTION_TYPE_KEY_PRESSED, rightButtonFunction, 100)
rightButton.addButtonAction(ACTION_TYPE_KEY_HOLD, rightButtonFunctionHold, 150)


  


while(True):
    time.sleep(1)