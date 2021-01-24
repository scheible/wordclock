# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 15:10:56 2021

@author: andre
"""

from Drv_QlockTwo import Drv_QlockTwo;
import time

json_qlocktwo_file_path = "cfg/Drv_QlockTwo.json"
json_ws2812b_file_path = "cfg/Drv_ws2812b.json"
drv_qlocktwo = Drv_QlockTwo(json_qlocktwo_file_path, json_ws2812b_file_path)

print("Set green")
drv_qlocktwo.set_font_color([0, 255, 0])
drv_qlocktwo.enable_letter(0, 0);
drv_qlocktwo.flush_sync(True);
print("Set red")
drv_qlocktwo.set_font_color([255, 0, 0])
drv_qlocktwo.enable_letter(0, 1);
drv_qlocktwo.flush_sync(False); 


if (False):
    for n in range(0,5):
        for i in range(6, 11):
            drv_qlocktwo.enable_letter(n, i);
            startTime = round(time.time() * 1000)
            drv_qlocktwo.flush(False);
            print("Application took ", round(time.time() * 1000) - startTime);
        #time.sleep(2);
        drv_qlocktwo.flush();
        #time.sleep(0.2);
            
    drv_qlocktwo.clear_all_letter();
    drv_qlocktwo.flush(); 
