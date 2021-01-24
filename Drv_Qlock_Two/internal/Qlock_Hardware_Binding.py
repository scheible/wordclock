# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 19:47:16 2021

@author: andre
"""
import numpy as np;
import time
from internal.Drv_ws2812b import Drv_ws2812b
from internal.Task_Pool import Task_Pool

class Qlock_Hardware_Binding:
    def __init__(self, num_leds, qlock_cfg, ws_2812b_cfg):
        
        
        self.__num_leds = num_leds;
        self.__font_color = np.array(qlock_cfg[3]);
        self.__font_brightness = qlock_cfg[4];
        self.__frame_color = np.array(qlock_cfg[5]);
        self.__frame_brightness = qlock_cfg[6];
        self.__minute_color = np.array(qlock_cfg[7]);
        self.__minute_brightness = qlock_cfg[8];
        self.__general_brightness = qlock_cfg[9];
        self.__off_color = np.zeros(3);
        
        self.__old_led_list = np.zeros((num_leds))
        
        
        self.__ist_soft_transition_enabled = qlock_cfg[12];
        transition_time_ms = qlock_cfg[13];
        transition_mode = qlock_cfg[14];
        
        self.__init__transition_intervals(transition_time_ms, transition_mode);
        
        self.__drv_ws2812b = Drv_ws2812b(num_leds, ws_2812b_cfg)
        
        
        self.__running_task_id = 0;
        self.__task_id_in_queue = 0;
        
        self.__task_pool = Task_Pool()
        

    
    def __init__transition_intervals(self, transition_time_ms, transition_mode, transition_interval_ms = 20):
        self.__transition_interval_ms = transition_interval_ms;
        self.__transition_time_ms = transition_time_ms;
        self.__transition_mode = transition_mode;
        self.__transition_intervals = self.__transition_time_ms // self.__transition_interval_ms;
        self.__A_on = 1 / (np.exp(1) - 1)
        self.__b_on = -self.__A_on;
        self.__A_off = 1 / (1 - np.exp(-1))
        self.__b_off = -self.__A_off * np.exp(-1)
        
    def __get_transitionColor_On(self, tick):
        
        col_led_on = np.array((1, 1, 1), dtype=np.ubyte)
        # Linear
        if (self.__transition_mode == 0):
            col_led_on = np.array(self.__font_color * ((tick + 1) / self.__transition_intervals), dtype=np.ubyte);
            
        # Exp
        elif (self.__transition_mode == 1):
            y = self.__A_on * np.exp((tick + 1) / self.__transition_intervals) + self.__b_on;
            col_led_on = np.array(y * self.__font_color, dtype=np.ubyte);
            
        return col_led_on
    
    def __get_transitionColor_Off(self, tick):
        
        col_led_off = np.array((1, 1, 1), dtype=np.ubyte)
        # Linear
        if (self.__transition_mode == 0):
            col_led_off = self.__font_color - np.array(self.__font_color * tick / self.__transition_intervals, dtype=np.ubyte);
            
        # Exp
        elif (self.__transition_mode == 1):
            y = self.__A_off * np.exp(-(tick + 1) / self.__transition_intervals) + self.__b_off;
            col_led_off = np.array(y * self.__font_color, dtype=np.ubyte);
            
        return col_led_off
        
    def flush(self, led_list):
        led_list_ = led_list.copy();
        self.__task_pool.add_task(self.flush_sync, led_list_)
        
    def flush_sync(self, led_list):
        led_list = np.array(led_list);
        
        if (led_list.ndim != 1):
            return -1;
        if (led_list.size != self.__num_leds):
            return -1;
        
        if (not self.__ist_soft_transition_enabled):
            for i in range(self.__num_leds):
                if (led_list[i] == 1):
                    self.__drv_ws2812b.setPixelColor(i, self.__font_color);
            self.__drv_ws2812b.show();
        else:
            for transitions in range(self.__transition_intervals):
                startTime = round(time.time() * 1000)
                for i in range(self.__num_leds):
                    if (led_list[i] == 1) and (self.__old_led_list[i] == 0):
                        self.__drv_ws2812b.setPixelColor(i, self.__get_transitionColor_On(transitions));
                    elif (led_list[i] == 0) and (self.__old_led_list[i] == 1):
                        self.__drv_ws2812b.setPixelColor(i, self.__get_transitionColor_Off(transitions));
                    elif (led_list[i] == 1) and (self.__old_led_list[i] == 1):
                        self.__drv_ws2812b.setPixelColor(i, self.__font_color);
                self.__drv_ws2812b.show();
                start_time = round(time.time() * 1000)
                strip_duration = round(time.time() * 1000) - startTime
                if (strip_duration < self.__transition_interval_ms):
                    sleep_duration = self.__transition_interval_ms - strip_duration
                    if (sleep_duration > 0):
                        time.sleep(sleep_duration/1000.0)
                    
        self.__old_led_list = led_list
                
    
    
    
    
    # Setter and Getter for Font Color
    def set_font_color(self, font_color):
        self.__font_color = np.array(font_color);
        
    def get_font_color(self):
        return self.__font_color;

    # Setter and Getter for Font Brightness
    def set_font_brightness(self, font_brightness):
        self.__font_brightness = np.array(font_brightness);
        
    def get___font_brightness(self):
        return self.__font_brightness;
    
    # Setter and Getter for Frame Color
    def set_frame_color(self, frame_color):
        self.__frame_color = np.array(frame_color);
        
    def get_frame_color(self):
        return self.__frame_color;
    
    # Setter and Getter for Frame Brightness
    def set_frame_brightness(self, frame_brightness):
        self.__frame_brightness = frame_brightness;
        
    def get_frame_brightness(self):
        return self.__frame_brightness;
    
    # Setter and Getter for Minute Color
    def set_minute_color(self, minute_color):
        self.__minute_color = minute_color;
        
    def get_minute_color(self):
        return self.__minute_color;
    
    # Setter and Getter for Minute Brightness
    def set_minute_brightness(self, minute_brightness):
        self.__minute_brightness = minute_brightness;
        
    def get_minute_brightness(self):
        return self.__minute_brightness;
    
    # Setter and Getter for General Brigthness
    def set_general_brightness(self, general_brightness):
        self.__general_brightness = general_brightness;
        
    def get_general_brightness(self):
        return self.__general_brightness;
    
    