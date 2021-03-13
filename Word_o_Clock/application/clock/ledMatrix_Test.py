# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 10:10:41 2021

@author: andre
"""
import json
import sys
from os import path
from LedMatrix import LedMatrix
from datetime import datetime
# Load json file

json_file_path = "D:/Projekte/Git/uhrthree/Documentation/Cfg_Clock.json"
if not path.exists(json_file_path):
    sys.exit("Json invalid, Test will exit!")
    

with open(json_file_path, "r") as json_read_file:
    jsonConfig = json.load(json_read_file)

currentTime = datetime.now()

time1 = currentTime.replace(hour=11, minute=55, second=0)
time2 = currentTime.replace(hour=12, minute=0, second=0)
print(time1, " ", time2)


ledMatrix_time1 = LedMatrix(time1, jsonConfig)
ledMatrix_time2 = LedMatrix(time2, jsonConfig)


diffLedMatrix = ledMatrix_time1 - ledMatrix_time2