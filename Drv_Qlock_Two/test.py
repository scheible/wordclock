# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 15:10:56 2021

@author: andre
"""

from Drv_QlockTwo import Drv_QlockTwo;
import time
drv_qlocktwo = Drv_QlockTwo()
while(False):
    for n in range(0,5):
        for i in range(6, 11):
            drv_qlocktwo.enable_letter(n, i);
            drv_qlocktwo.flush(False);
        time.sleep(2);
            
            
        drv_qlocktwo.flush();
    

drv_qlocktwo.flush();