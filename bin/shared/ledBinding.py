import numpy as np
import sys
from os.path import dirname
from rpi_ws281x import *

class LedBinding:
    
    def __init__(self, ws2812bJson, numLeds, brightness):
        
        # LED strip configuration:
        self.__LED_COUNT      = numLeds # Number of LED pixels.
        self.__LED_PIN        = ws2812bJson["ledPin"]   # GPIO pin connected to the pixels (18 uses PWM!).
        #LED_PIN        = 10             # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        self.__LED_FREQ_HZ    = ws2812bJson["ledFreqHz"]   # LED signal frequency in hertz (usually 800khz)
        self.__LED_DMA        = ws2812bJson["ledDma"]   # DMA channel to use for generating signal (try 10)
        self.__LED_BRIGHTNESS = brightness      # Set to 0 for darkest and 255 for brightest
        self.__LED_INVERT     = ws2812bJson["ledInvert"]   # True to invert the signal (when using NPN transistor level shift)
        self.__LED_CHANNEL    = ws2812bJson["ledChannel"]   # set to '1' for GPIOs 13, 19, 41, 45 or 53

        # Create NeoPixel object with appropriate configuration.
        self.__strip = Adafruit_NeoPixel(self.__LED_COUNT, self.__LED_PIN, self.__LED_FREQ_HZ, self.__LED_DMA, self.__LED_INVERT, self.__LED_BRIGHTNESS, self.__LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.__strip.begin()
        
        
    def showLedList(self, led_colors):
        pixel_ref = self.__strip.getPixels()
        pixel_ref[:] = led_colors.tolist()
        
        self.__strip.show()

    def setBrightness(self, brightness):
        self.__strip.setBrightness(brightness)
        
    def getBrightness(self):
        return self.__strip.getBrightness()

    def clear(self):
        pixel_ref = self.__strip.getPixels()
        for i in range(self.__strip.numPixels()):
            pixel_ref[i] = 0

    def setLedRGB(self, index, r, g, b):
        self.__strip.setPixelColorRGB(index, r, g, b)

    def show(self):
        self.__strip.show()

        
            
            