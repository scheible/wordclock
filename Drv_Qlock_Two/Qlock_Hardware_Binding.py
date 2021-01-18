# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 19:47:16 2021

@author: andre
"""
import numpy as np;
import time
from rpi_ws281x import *

class Qlock_Hardware_Binding:
    def __init__(self, num_leds, transition_time_ms, transition_mode, font_color):
        self.__num_leds = num_leds;
        self.__transition_interval_ms = 20;
        self.__transition_time_ms = transition_time_ms;
        self.__transition_mode = transition_mode;
        self.__font_color = font_color;
        
        self.__transition_intervals = self.__transition_time_ms // self.__transition_interval_ms;
        self.__A_on = 1 / (np.exp(1) - 1)
        self.__b_on = -A;
        self.__A_off = - 1 / (np.exp(1) - 1);
        self.__b_off = -A;
        
        self.__old_led_list = np.zeros((self.__num_leds));
        
        self.__strip = Adafruit_NeoPixel(num_leds, 18, 800000, 10, False, 255, 0)
        # Intialize the library (must be called once before other functions).
        self.__strip.begin()
        
        
    def get_transitionColor_On(self, tick):
        
        col_led_on = np.array((1, 1, 1), dtype=np.ubyte)
        # Linear
        if (self.__transition_mode == 0):
            col_led_on = np.array(self.__font_color * tick / self.__transition_intervals, dtype=np.ubyte);
            
        # Exp
        elif (self.__transition_mode == 1):
            y = self.__A_on * np.exp(tick / self.__transition_intervals) + self.__b_on;
            col_led_on = np.array(y * self.__font_color, dtype=np.ubyte);
            
        return col_led_on
    
    def get_transitionColor_Off(self, tick):
        
        col_led_off = np.array((1, 1, 1), dtype=np.ubyte)
        # Linear
        if (self.__transition_mode == 0):
            col_led_off = self.__font_color - np.array(self.__font_color * tick / self.__transition_intervals, dtype=np.ubyte);
            
        # Exp
        elif (self.__transition_mode == 1):
            y = self.__A_off * np.exp(-tick / self.__transition_intervals) + self.__b_off;
            col_led_off = np.array(y * self.__font_color, dtype=np.ubyte);
            
        return col_led_off
        
    def flush_sync(self, led_list):
        led_list = np.array(led_list);
        
        if (led_list.ndim != 1):
            return -1;
        if (led_list.shape != self.__num_leds):
            return -1;
        
        for transitions in range(self.__transition_intervals):
            for i in range(self.__num_leds):
                if (led_list[i] == 1) and (__old_led_list[i] == 0):
                    strip.setPixelColor(i, get_transitionColor_On(transitions));
                elif (led_list[i] == 0) and (__old_led_list[i] == 1):
                    strip.setPixelColor(i, get_transitionColor_On(transitions));
            start_time = round(time.time() * 1000)
            self.__strip.show()
            self.__strip_duration = round(time.time() * 1000) - startTime
            if (strip_duration > self.__transition_interval_ms):
                sleep_duration = self.__transition_interval_ms - strip_duration
                time.sleep(sleep_duration/1000.0)
                
    
    def set_font_color(font_color):
        self.__font_color = font_color;