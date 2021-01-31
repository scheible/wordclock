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
#drv_qlocktwo.flush();


print("Set white")
drv_qlocktwo.set_font_color([180, 180, 180])
print("Set elements")

drv_qlocktwo.enable_element(0, 0, [180, 0, 0]);
drv_qlocktwo.enable_element(0, 1, [0, 180, 0]);
drv_qlocktwo.enable_element(0, 3, [0, 0, 180]);
drv_qlocktwo.enable_element(0, 4, [180, 180, 0]);
drv_qlocktwo.enable_element(0, 5, [0, 180, 180]);


drv_qlocktwo.enable_element(2, 0);
drv_qlocktwo.enable_element(2, 1);
drv_qlocktwo.enable_element(2, 2);
drv_qlocktwo.enable_element(2, 3);
drv_qlocktwo.enable_element(2, 4);
drv_qlocktwo.enable_element(2, 5);
drv_qlocktwo.enable_element(2, 6);
drv_qlocktwo.enable_element(2, 7);
drv_qlocktwo.enable_element(2, 8);
drv_qlocktwo.enable_element(2, 9);
drv_qlocktwo.enable_element(2, 10);







drv_qlocktwo.enable_element(7, 7);
drv_qlocktwo.enable_element(7, 8);
drv_qlocktwo.enable_element(7, 9);
drv_qlocktwo.enable_element(7, 10);



#drv_qlocktwo.enable_element(4, 0);
#drv_qlocktwo.enable_element(4, 1);
#drv_qlocktwo.enable_element(4, 2);
#drv_qlocktwo.enable_element(4, 3);
#drv_qlocktwo.enable_element(5, 0);
#drv_qlocktwo.enable_element(5, 1);
#drv_qlocktwo.enable_element(5, 2);
#drv_qlocktwo.enable_element(5, 3);
print("Flush")
drv_qlocktwo.flush_sync();

time.sleep(50);
drv_qlocktwo.enable_element(0, 0);
drv_qlocktwo.enable_element(0, 1);
drv_qlocktwo.enable_element(0, 3);
drv_qlocktwo.enable_element(0, 4);
drv_qlocktwo.enable_element(0, 5);

drv_qlocktwo.enable_element(7, 7);
drv_qlocktwo.enable_element(7, 8);
drv_qlocktwo.enable_element(7, 9);
drv_qlocktwo.enable_element(7, 10);

drv_qlocktwo.enable_element(9, 8);
drv_qlocktwo.enable_element(9, 9);
drv_qlocktwo.enable_element(9, 10);



if (False):
    for n in range(0,5):
        for i in range(6, 11):
            drv_qlocktwo.enable_element(n, i);
            startTime = round(time.time() * 1000)
            drv_qlocktwo.flush(False);
            print("Application took ", round(time.time() * 1000) - startTime);
        #time.sleep(2);
        drv_qlocktwo.flush();
        #time.sleep(0.2);
            
    drv_qlocktwo.clear_all_element();
    drv_qlocktwo.flush(); 
