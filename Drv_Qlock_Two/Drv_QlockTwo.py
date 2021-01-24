# -*- coding: utf-8 -*-

import numpy as np;
from internal.Qlock_Matrix import Qlock_Matrix
from internal.Qlock_Hardware_Binding import Qlock_Hardware_Binding
from internal.Json_QlockTwo import Json_QlockTwo
from internal.Json_Ws2812b import Json_Ws2812b
import sys

class Drv_QlockTwo:
    
    def __init__(self, json_qlocktwo_file_path, json_ws2812b_file_path):
        
        
        self.__json_qlocktwo = Json_QlockTwo(json_qlocktwo_file_path)
        if (not(self.__json_qlocktwo.is_json_valid())):
            sys.exit("QlockTwo Json does not yield a valid config. System will exit!")
        qlock_cfg = self.__json_qlocktwo.get_json_results()
        
        self.__json_ws2812b = Json_Ws2812b(json_ws2812b_file_path)
        if (not(self.__json_ws2812b.is_json_valid())):
            sys.exit("Ws2812b Json does not yield a valid config. System will exit!")
        ws_2812b_cfg = self.__json_ws2812b.get_json_results()
        
        
        num_letter_vertical = qlock_cfg[0]
        num_letter_horizontal = qlock_cfg[1]
        leds_per_letter = qlock_cfg[2]
        num_leds = num_letter_vertical * num_letter_horizontal * leds_per_letter;
        
        
        self.__qlock_matrix = Qlock_Matrix(num_letter_vertical, num_letter_horizontal, leds_per_letter);
        self.__qlock_hardware_binding = Qlock_Hardware_Binding(num_leds, qlock_cfg, ws_2812b_cfg);
     
    def clear_all_letter(self):
        self.__qlock_matrix.clear_all_letter();
        
    def enable_letter(self, pos_vertical, pos_horizontal):
        self.__qlock_matrix.enable_letter(pos_vertical, pos_horizontal)
        
    def disable_letter(self, pos_vertical, pos_horizontal):
        self.__qlock_matrix.disable_letter(pos_vertical, pos_horizontal)
        
    def flush(self, clear_letter_matrix_after_flush = True):
        led_list = self.__qlock_matrix.get_led_list();
        self.__qlock_hardware_binding.flush(led_list);
        
        if (clear_letter_matrix_after_flush):
            self.clear_all_letter();
            
    def flush_sync(self, clear_letter_matrix_after_flush = True):
        led_list = self.__qlock_matrix.get_led_list();
        self.__qlock_hardware_binding.flush_sync(led_list);
        
        if (clear_letter_matrix_after_flush):
            self.clear_all_letter();
        
    def set_font_color(self, font_color):
        self.__qlock_hardware_binding.set_font_color(font_color);
        
    def set_font_brightness(self, font_brightness):
        self.__qlock_hardware_binding.set_font_brightness(font_brightness);
        
    def set_frame_color(self, frame_color):
        self.__qlock_hardware_binding.set_frame_color(frame_color);
        
    def set_frame_brightness(self, frame_brightness):
        self.__qlock_hardware_binding.set_frame_brightness(frame_brightness);
        
    def set_minute_color(self, minute_color):
        self.__qlock_hardware_binding.set_minute_color(minute_color);
        
    def set_minute_brightness(self, minute_brightness):
        self.__qlock_hardware_binding.set_minute_brightness(minute_brightness);
        
    def set_general_brightness(self, general_brightness):
        self.__qlock_hardware_binding.set_general_brightness(general_brightness);
        
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
        