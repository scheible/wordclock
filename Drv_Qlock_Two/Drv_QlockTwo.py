# -*- coding: utf-8 -*-

import numpy as np;
from Qlock_Matrix import Qlock_Matrix
from Qlock_Hardware_Binding import Qlock_Hardware_Binding
class Drv_QlockTwo:
    
    def __init__(self, num_letter_vertical = 10, num_letter_horizontal = 11, leds_per_letter = 2):        
        self.__font_color = np.array((100, 100, 100), dtype=np.ubyte);
        self.__font_brightness = 100;
        self.__frame_color = np.array((100, 100, 100), dtype=np.ubyte);
        self.__frame_brightness = 100;
        self.__minute_color = np.array((100, 100, 100), dtype=np.ubyte);
        self.__minute_brightness = 100;
        self.__general_brightness = 100;
        self.__is_minutes_shown = False;
        self.__is_frame_shown = False;
        self.__is_soft_transistion_enabled = True;
        self.__transition_time_ms = 1000;
        self.__transition_mode = 0;
        
        self.__qlock_matrix = Qlock_Matrix(num_letter_vertical, num_letter_horizontal, leds_per_letter);
        self.__qlock_hardware_binding = Qlock_Hardware_Binding()
     
    def clear_all_letter(self):
        self.__qlock_matrix.clear_all_letter();
        
    def enable_letter(self, pos_vertical, pos_horizontal):
        self.__qlock_matrix.enable_letter(pos_vertical, pos_horizontal)
        
    def disable_letter(self, pos_vertical, pos_horizontal):
        self.__qlock_matrix.disable_letter(pos_vertical, pos_horizontal)
        
    def flush(self):
        self.__qlock_hardware_binding.flush_sync();
        
    def flush_sync(self):
        self.__qlock_hardware_binding.flush_sync();
        
    def set_font_color(self, font_color):
        self.__font_color = font_color
        
    def set_font_brightness(self, font_brightness):
        self.__font_brightness = font_brightness
        
    def set_frame_color(self, frame_color):
        self.__frame_color = frame_color
        
    def set_frame_brightness(self, frame_brightness):
        self.__frame_brightness = frame_brightness
        
    def set_minute_color(self, minute_color):
        self.__minute_color = minute_color
        
    def set_minute_brightness(self, minute_brightness):
        self.__minute_brightness = minute_brightness
        
    def set_general_brightness(self, general_brightness):
        self.__general_brightness = general_brightness
        
    def set_is_minutes_shown(self, is_minutes_shown):
        self.__is_minutes_shown = is_minutes_shown
        
    def set_is_frame_shown(self, is_frame_shown):
        self.__is_frame_shown = is_frame_shown
        
    def set_is_soft_transistion_enabled(self, is_soft_transistion_enabled):
        self.__is_soft_transistion_enabled = is_soft_transistion_enabled
        
    def set_transition_time(self, transition_time):
        self.__transition_time = transition_time
        
    def set_transition_mode(self, transition_mode):
        self.__transition_mode = transition_mode
        