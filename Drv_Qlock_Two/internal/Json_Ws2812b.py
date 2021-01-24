# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 10:05:30 2021

@author: andre
"""

import json
import os.path
from os import path

class Json_Ws2812b:
    def __init__(self, json_file_path):
        
        self.__is_valid = self.__parse_json_ws2812b(json_file_path);
        
        
    def is_json_valid(self):
        return self.__is_valid;
    
    def get_json_results(self):
        if (self.__is_valid):
            cfg = [self.__LED_PIN, self.__LED_FREQ_HZ, self.__LED_DMA, self.__LED_INVERT, self.__LED_CHANNEL];
        else:
            cfg = []
        return cfg
        
    def __parse_json_ws2812b(self, json_file_path):
        
        is_valid = False;
        
        if path.exists(json_file_path):
            with open(json_file_path, "r") as json_read_file:
                self.__json_data = json.load(json_read_file)
            
            is_valid = self.__valid_json_ws128b()
            
        return is_valid;
            
            
    def __valid_json_ws128b(self):
        
        led_pin_found = led_freq_hz = led_dma = led_invert = led_channel = False
        
        # Check if LED_PIN exist
        if "LED_PIN" in self.__json_data:
            # Expect int
            if isinstance(self.__json_data["LED_PIN"], int): 
                self.__LED_PIN = self.__json_data["LED_PIN"];
                led_pin_found = True
            else:
                print("Error: Led pin is not a integer!")
                
        # Check if LED_PIN exist
        if "LED_FREQ_HZ" in self.__json_data:
            # Expect int
            if isinstance(self.__json_data["LED_FREQ_HZ"], int): 
                self.__LED_FREQ_HZ = self.__json_data["LED_FREQ_HZ"];
                led_freq_hz = True
            else:
                print("Error: Led freq is not an integer!")
                
        # Check if LED_PIN exist
        if "LED_DMA" in self.__json_data:
            # Expect int
            if isinstance(self.__json_data["LED_DMA"], int): 
                self.__LED_DMA = self.__json_data["LED_DMA"];
                led_dma = True
            else:
                print("Error: Led DMA is not an integer!")
                
        # Check if LED_PIN exist
        if "LED_INVERT" in self.__json_data:
            # Expect int
            if isinstance(self.__json_data["LED_INVERT"], bool): 
                self.__LED_INVERT = self.__json_data["LED_INVERT"];
                led_invert = True
            else:
                print("Error: Led invert is not an boolean!")
                
        # Check if LED_PIN exist
        if "LED_CHANNEL" in self.__json_data:
            # Expect int
            if isinstance(self.__json_data["LED_CHANNEL"], int): 
                self.__LED_CHANNEL = self.__json_data["LED_CHANNEL"];
                led_channel = True
            else:
                print("Error: Led channel is not an integer!")
                
        is_valid = led_pin_found & led_freq_hz & led_dma & led_invert & led_channel;
        return is_valid;
    
    