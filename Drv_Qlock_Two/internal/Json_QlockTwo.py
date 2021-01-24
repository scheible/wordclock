# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 10:05:30 2021

@author: andre
"""

import json
import os.path
from os import path

class Json_QlockTwo:
    def __init__(self, json_file_path):
        
        self.__searchedVariables = ["num_letter_vertical", int,              \
                                    "num_letter_horizontal", int,            \
                                    "leds_per_letter", int,                  \
                                    "font_color", list,                      \
                                    "font_brightness", int,                  \
                                    "frame_color", list,                     \
                                    "frame_brightness", int,                 \
                                    "minute_color", list,                    \
                                    "minute_brightness", int,                \
                                    "general_brightness", int,               \
                                    "is_minutes_shown", bool,                \
                                    "is_frame_shown", bool,                  \
                                    "is_soft_transistion_enabled", bool,     \
                                    "transition_time_ms", int,               \
                                    "transition_mode", int]
          
        self.__cfg = []
        self.__is_valid = self.__parse_json_qlocktwo(json_file_path);
        
        
    def is_json_valid(self):
        return self.__is_valid;
    
    def get_json_results(self):
        return self.__cfg
        
    def __parse_json_qlocktwo(self, json_file_path):
        
        is_valid = False;
        
        if path.exists(json_file_path):
            with open(json_file_path, "r") as json_read_file:
                self.__json_data = json.load(json_read_file)
            
            is_valid = self.__valid_json_qlocktwo()
            
        return is_valid;
            
            
    def __valid_json_qlocktwo(self):
        
        is_valid = True
        
        for i in range(0, len(self.__searchedVariables), 2):
            if (not (self.__searchedVariables[i].upper() in self.__json_data)): 
                is_valid = False
                print("Error: ", self.__searchedVariables[i].upper(), " was not found in json")
                break
            if isinstance(self.__json_data[self.__searchedVariables[i].upper()], self.__searchedVariables[i + 1]): 
                self.__cfg.append(self.__json_data[self.__searchedVariables[i].upper()])
            else:
                is_valid = False
                print("Error: ", self.__searchedVariables[i].upper(), " seems not to be a ", self.__searchedVariables[i + 1])
                break
       
        return is_valid;