# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 09:59:16 2021

@author: andre
"""

from datetime import datetime
from application.clock.ledMatrix import LedMatrix
class ClockBackend:
    
       
    def buildLedMatrixFromCurrentTime(jsonConfig):
        currentTime = datetime.now()
        ledMatrix = LedMatrix(currentTime, jsonConfig)
        return ledMatrix
                