import numpy as np
import sys
from os.path import dirname
from tkinter import *
import time
import threading

class LedBinding:
    
    def __init__(self, ws2812bJson, numLeds, brightness):
        
        self.__LED_COUNT      = numLeds # Number of LED pixels.
        self.brightness = brightness      # Set to 0 for darkest and 255 for brightest

        self.initClock(["ESKISTAFÜNF",
                              "ZEHNZWANZIG",
                              "DREIVIERTEL",
                              "VORFUNKNACH",
                              "HALBAELFÜNF",
                              "EINSXAMZWEI",
                              "DREIPMJVIER",
                              "SECHSNLACHT",
                              "SIEBENZWÖLF",
                              "ZEHNEUNKUHR"])
        
        
    def showLedList(self, led_colors):
        #pixel_ref = self.__strip.getPixels()
        #pixel_ref[:] = led_colors.tolist()

        for i in range(0, 220, 2):
            self.clockMatrix[i // 2]['fg'] = f'#{led_colors[i]:0>6x}'
        for i in range(220, len(led_colors), 1):
            self.borderLeds[i - 220]['bg'] = f'#{led_colors[i]:0>6x}'
        self.root.update()

    def setBrightness(self, brightness):
        self.brightness = brightness
        
    def getBrightness(self):
        return self.brightness
        
            
    def initClock(self, lineStr):
        self.root = Tk()
        
        self.root.title("WordClock")
        self.root.configure(bg='gray')
        
        sizeOfLed = 5
        # Draw outer Border
        numberOfBorderElements = 2 * 24 + 2 * 26
        
        for i in range(numberOfBorderElements):
            if (i <= 26):
                a = Label (text = "", bg = "gray", fg = "black", font = ("Arial", sizeOfLed), width = 2, height = 1)
                a.grid(column = i, row = 0)
            elif (i <= 50):
                a = Label (text = "", bg = "gray", fg = "black", font = ("Arial", sizeOfLed), width = 2, height = 1)
                a.grid(column = 26, row = i - 26)
            elif (i <= 76):
                a = Label (text = "", bg = "gray", fg = "black", font = ("Arial", sizeOfLed), width = 2, height = 1)
                a.grid(column = 76 - i, row = 24)
            else:
                a = Label (text = "", bg = "gray", fg = "black", font = ("Arial", sizeOfLed), width = 2, height = 1)
                a.grid(column = 0, row = numberOfBorderElements - i)
                
        self.borderLeds = []
        # Generate Border
        numberOfLeds = 2 * 22 + 2 * 24
        
        for i in range(numberOfLeds):
            if (i <= 24):
                if ((i == 5) or (i == 24 - 5)):
                    continue
                a = Label (text = "", bg = "white", fg = "black", font = ("Arial", sizeOfLed), width = 2, height = 1)
                self.borderLeds.append(a)
                self.borderLeds[-1].grid(column = i + 1, row = 0 + 1)
            elif (i <= 46):
                if ((i == 24 + 5) or (i == 46 - 5)):
                    continue
                a = Label (text = "", bg = "white", fg = "black", font = ("Arial", sizeOfLed), width = 2, height = 1)
                self.borderLeds.append(a)
                self.borderLeds[-1].grid(column = 24 + 1, row = i - 24 + 1)
            elif (i <= 70):
                if ((i == 46 + 5) or (i == 70 - 5)):
                    continue
                a = Label (text = "", bg = "white", fg = "black", font = ("Arial", sizeOfLed), width = 2, height = 1)
                self.borderLeds.append(a)
                self.borderLeds[-1].grid(column = 70 - i + 1, row = 22 + 1)
            else:
                if ((i == 70 + 5) or (i == numberOfLeds - 5)):
                    continue
                a = Label (text = "", bg = "white", fg = "black", font = ("Arial", sizeOfLed), width = 2, height = 1)
                self.borderLeds.append(a)
                self.borderLeds[-1].grid(column = 0 + 1, row = numberOfLeds - i + 1)
                
        # Add damy letter
        a = Label (text = "", bg = "gray", fg = "black", font = ("Arial", sizeOfLed), width = 2, height = 1)
        a.grid(column = 2, row = 2)
        a = Label (text = "", bg = "gray", fg = "black", font = ("Arial", sizeOfLed), width = 2, height = 1)
        a.grid(column = 24, row = 22)
        
        self.clockMatrix = []
        for j in range(0, len(lineStr[0])):
            for i in range(0, len(lineStr)):
                if (j % 2 == 0):
                    i_1 = (10 - 1) - i
                else:
                    i_1 = i
                j_1 = (11 - 1) - j
                print("i: " + str(i_1) + " j: " + str(j_1))
                self.clockMatrix.append(Label (text = lineStr[i_1][j_1], bg = "gray", fg = "darkgray", font = ("Arial", 40), width = 2, height = 1))
                self.clockMatrix[-1].grid(column = 2*j_1 + 3, row = 2*i_1 + 3, columnspan = 1, rowspan = 1)
                           


    def update(self):
        self.root.update()
        


        
    def updateColer(self):
        self.clockMatrix[5]['bg'] = "#ffffff"  
        self.clockMatrix[15]['bg'] = "#ffffff"  

        




