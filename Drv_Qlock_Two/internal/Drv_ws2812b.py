# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 15:02:12 2021

@author: andre
"""

import numpy as np
import sys
from os.path import dirname
#sys.path.append(dirname("/home/pi/QlockTwo/uhrthree/Drv_Qlock_Two"))
from rpi_ws281x import *

class Drv_ws2812b:
    
    def __init__(self, leds_num):
        # LED strip configuration:
        self.__LED_COUNT      = leds_num     # Number of LED pixels.
        self.__LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
        #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        self.__LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        self.__LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
        self.__LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
        self.__LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        self.__LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

        # Create NeoPixel object with appropriate configuration.
        self.__strip = Adafruit_NeoPixel(self.__LED_COUNT, self.__LED_PIN, self.__LED_FREQ_HZ, self.__LED_DMA, self.__LED_INVERT, self.__LED_BRIGHTNESS, self.__LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.__strip.begin()
        
        
    def setPixelColor(self, index, color):
        self.__strip.setPixelColor(index, Color(int(color[0]), int(color[1]), int(color[2])))
        
    def show(self):
        self.__strip.show()
            
            