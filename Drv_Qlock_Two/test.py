# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 15:10:56 2021

@author: andre
"""

from Drv_QlockTwo import Drv_QlockTwo;

drv_qlocktwo = Drv_QlockTwo()

drv_qlocktwo.enable_letter(1, 1);
drv_qlocktwo.flush();

print(" ")
print(" ")
print(" ")

drv_qlocktwo.flush();