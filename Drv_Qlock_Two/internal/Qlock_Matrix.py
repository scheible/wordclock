# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 18:46:56 2021

@author: andre
"""
import numpy as np

class Qlock_Matrix:
    
    def __init__(self, num_letter_vertical, num_letter_horizontal, leds_per_letter):
        self.__num_letter_vertical = num_letter_vertical;
        self.__num_letter_horizontal = num_letter_horizontal;
        self.__leds_per_letter = leds_per_letter;
        self.__num_leds_vertical = self.__num_letter_vertical * self.__leds_per_letter;
        self.__num_leds_horizontal = self.__num_letter_horizontal;
        
        self.__led_matrix = np.zeros((self.__num_letter_horizontal, self.__num_letter_vertical))
        
        self.__init();
        
        
    def __init(self):
        self.__led_look_up_table = np.zeros((self.__num_letter_vertical * self.__num_letter_horizontal * self.__leds_per_letter, 2), dtype = int)
        
        
        for i in range(self.__num_letter_horizontal):
            for j in range(self.__num_leds_vertical):
                if (i % self.__leds_per_letter == 0):
                    self.__led_look_up_table[i * self.__num_leds_vertical + j, 1] = j // self.__leds_per_letter
                else:
                    self.__led_look_up_table[i * self.__num_leds_vertical + j, 1] = (self.__num_leds_vertical - j - 1) // self.__leds_per_letter
                self.__led_look_up_table[i * self.__num_leds_vertical + j, 0] = i
                
    def get_led_list(self):
      
        led_list = self.__led_matrix[self.__led_look_up_table[:, 0], self.__led_look_up_table[:, 1]]
        return led_list
    
    
    def clear_all_letter(self):
        self.__led_matrix = np.zeros((self.__num_letter_horizontal, self.__num_letter_vertical))
    
    def enable_letter(self, pos_vertical, pos_horizontal):
        if (pos_vertical >= 0) and (pos_vertical < self.__num_letter_vertical) and (pos_horizontal >= 0) and (pos_horizontal < self.__num_letter_horizontal):
            self.__led_matrix[pos_horizontal, pos_vertical] = 1;
            return True;
        else:
            return False;
        
    def disable_letter(self, pos_vertical, pos_horizontal):
        if (pos_vertical >= 0) and (pos_vertical < self.__num_letter_vertical) and (pos_horizontal >= 0) and (pos_horizontal < self.__num_letter_horizontal):
            self.__led_matrix[pos_horizontal, pos_vertical] = 0;
            return True;
        else:
            return False;