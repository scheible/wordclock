# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 15:02:12 2021

@author: andre
"""
from internal.Json_Ws2812b import Json_Ws2812b
import sys

class Drv_ws2812b:
    
    def __init__(self, leds_num, ws_2812b_cfg):
        
       
        # LED strip configuration:
        self.__LED_COUNT      = leds_num # Number of LED pixels.
        self.__LED_PIN        = ws_2812b_cfg[0]   # GPIO pin connected to the pixels (18 uses PWM!).
        #LED_PIN        = 10             # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        self.__LED_FREQ_HZ    = ws_2812b_cfg[1]   # LED signal frequency in hertz (usually 800khz)
        self.__LED_DMA        = ws_2812b_cfg[2]   # DMA channel to use for generating signal (try 10)
        self.__LED_BRIGHTNESS = 255      # Set to 0 for darkest and 255 for brightest
        self.__LED_INVERT     = ws_2812b_cfg[3]   # True to invert the signal (when using NPN transistor level shift)
        self.__LED_CHANNEL    = ws_2812b_cfg[4]   # set to '1' for GPIOs 13, 19, 41, 45 or 53
        
        print("Led count: ", self.__LED_COUNT)
        print("Led pin: ", self.__LED_PIN)
        print("Led freq hz: ", self.__LED_FREQ_HZ)
        print("Led DMA: ", self.__LED_DMA)
        print("Led invert: ", self.__LED_INVERT)
        print("Led channel: ", self.__LED_CHANNEL)
        
    def setPixelColor(self, index, color):
        print("Set Pixel ", index, " with Color ", color);
        
    def show(self):
        print("Update all colors");
            
            