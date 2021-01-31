# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 18:46:56 2021

@author: andre
"""
import numpy as np

class Qlock_Matrix:
    
    def __init__(self, num_element_vertical, num_element_horizontal, leds_per_element, element_color):
        self.__num_element_vertical = num_element_vertical;
        self.__num_element_horizontal = num_element_horizontal;
        self.__leds_per_element = leds_per_element;
        self.__num_leds_vertical = self.__num_element_vertical * self.__leds_per_element;
        self.__num_leds_horizontal = self.__num_element_horizontal;
        

        self.__led_matrix = np.zeros((self.__num_element_horizontal, self.__num_element_vertical, 4), dtype=np.ubyte)
        self.__element_color = np.array(element_color, dtype=np.ubyte);
        self.__init();
        
        
    def __init(self):
        self.__led_look_up_table = np.zeros((self.__num_element_vertical * self.__num_element_horizontal * self.__leds_per_element, 2), dtype = int)
        
        # Init lookup table
        for i in range(self.__num_element_horizontal):
            for j in range(self.__num_leds_vertical):
                if (i % self.__leds_per_element == 1):
                    self.__led_look_up_table[i * self.__num_leds_vertical + j, 1] = j // self.__leds_per_element
                else:
                    self.__led_look_up_table[i * self.__num_leds_vertical + j, 1] = (self.__num_leds_vertical - j - 1) // self.__leds_per_element
                self.__led_look_up_table[i * self.__num_leds_vertical + j, 0] = self.__num_element_horizontal - i - 1
                
        # Init a clear led Matrix
        self.__led_clear_matrix = self.__led_matrix
                
    def get_led_list(self):
      
        led_list = self.__led_matrix[self.__led_look_up_table[:, 0], self.__led_look_up_table[:, 1], :]
        return led_list
    
    
    def clear_all_elements(self):
        self.__led_matrix = self.__led_clear_matrix
    
    def enable_element(self, pos_vertical, pos_horizontal, color = -1):
        if (color == -1):
            color = self.__element_color
        else:
            color = np.array(color)
        if (pos_vertical >= 0) and (pos_vertical < self.__num_element_vertical) and (pos_horizontal >= 0) and (pos_horizontal < self.__num_element_horizontal) and (color.shape == (3,)):
            self.__led_matrix[pos_horizontal, pos_vertical, 0] = 1;
            self.__led_matrix[pos_horizontal, pos_vertical, 1:4] = color;
            return True;
        else:
            return False;
        
    def disable_element(self, pos_vertical, pos_horizontal):
        if (pos_vertical >= 0) and (pos_vertical < self.__num_element_vertical) and (pos_horizontal >= 0) and (pos_horizontal < self.__num_element_horizontal):
            self.__led_matrix[pos_horizontal, pos_vertical, 0] = 0;
            self.__led_matrix[pos_horizontal, pos_vertical, 1:4] = np.zeros(3, dtype=np.ubyte);
            return True;
        else:
            return False;

    def set_font_color(self, element_color):
        self.__element_color = np.array(element_color, dtype=np.ubyte);

        
    def getmat(self):
        return self.__led_matrix