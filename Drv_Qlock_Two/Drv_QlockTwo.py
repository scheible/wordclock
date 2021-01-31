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
        font_color = qlock_cfg[3]
        num_leds = num_letter_vertical * num_letter_horizontal * leds_per_letter;
        
        
        
        self.__qlock_matrix = Qlock_Matrix(num_letter_vertical, num_letter_horizontal, leds_per_letter, font_color);
        self.__qlock_hardware_binding = Qlock_Hardware_Binding(num_leds, qlock_cfg, ws_2812b_cfg);
     
    def clear_all_elements(self):
        self.__qlock_matrix.clear_all_elements();
        
    def enable_element(self, pos_vertical, pos_horizontal, color = -1):
        self.__qlock_matrix.enable_element(pos_vertical, pos_horizontal, color)
        
    def disable_element(self, pos_vertical, pos_horizontal):
        self.__qlock_matrix.disable_element(pos_vertical, pos_horizontal)
        
    def flush(self, clear_elements_matrix_after_flush = True):
        led_list = self.__qlock_matrix.get_led_list();
        self.__qlock_hardware_binding.flush(led_list);
        
        if (clear_elements_matrix_after_flush ):
            self.clear_all_elements();
            
    def flush_sync(self, clear_elements_matrix_after_flush = True):
        led_list = self.__qlock_matrix.get_led_list();
        self.__qlock_hardware_binding.flush_sync(led_list);
        
        if (clear_elements_matrix_after_flush):
            self.clear_all_elements();
        
        
        
    def set_font_color(self, font_color):
        is_updated = False;
        if (len(font_color) == 3):
            is_updated = self.__json_qlocktwo.update_json_entry(3, list(font_color))
            self.__qlock_matrix.set_font_color(font_color);
        return is_updated
        
    def set_font_brightness(self, font_brightness):
        is_updated = self.__json_qlocktwo.update_json_entry(4, font_brightness)
        self.__qlock_hardware_binding.set_font_brightness(font_brightness);
        return is_updated
        
    def set_frame_color(self, frame_color):
        is_updated = False;
        if (len(frame_color) == 3):
            is_updated = self.__json_qlocktwo.update_json_entry(5, list(frame_color))
        self.__qlock_hardware_binding.set_frame_color(frame_color);
        return is_updated
        
    def set_frame_brightness(self, frame_brightness):
        is_updated = self.__json_qlocktwo.update_json_entry(6, frame_brightness)
        self.__qlock_hardware_binding.set_frame_brightness(frame_brightness);
        return is_updated
        
    def set_minute_color(self, minute_color):
        is_updated = False;
        if (len(minute_color) == 3):
            is_updated = self.__json_qlocktwo.update_json_entry(7, list(minute_color))
        self.__qlock_hardware_binding.set_minute_color(minute_color);
        return is_updated
        
    def set_minute_brightness(self, minute_brightness):
        is_updated = self.__json_qlocktwo.update_json_entry(8, minute_brightness)
        self.__qlock_hardware_binding.set_minute_brightness(minute_brightness);
        return is_updated
        
    def set_general_brightness(self, general_brightness):
        is_updated = self.__json_qlocktwo.update_json_entry(9, general_brightness)
        self.__qlock_hardware_binding.set_general_brightness(general_brightness);
        return is_updated
        
    def set_is_minutes_shown(self, is_minutes_shown):
        is_updated = self.__json_qlocktwo.update_json_entry(10, is_minutes_shown)
        self.__is_minutes_shown = is_minutes_shown
        return is_updated
        
    def set_is_frame_shown(self, is_frame_shown):
        is_updated = self.__json_qlocktwo.update_json_entry(11, is_frame_shown)
        self.__is_frame_shown = is_frame_shown
        return is_updated
        
    def set_is_soft_transistion_enabled(self, is_soft_transistion_enabled):
        is_updated = self.__json_qlocktwo.update_json_entry(12, is_soft_transistion_enabled)
        self.__is_soft_transistion_enabled = is_soft_transistion_enabled
        return is_updated
        
    def set_transition_time(self, transition_time):
        is_updated = self.__json_qlocktwo.update_json_entry(13, transition_time)
        self.__transition_time = transition_time
        return is_updated
        
    def set_transition_mode(self, transition_mode):
        is_updated = self.__json_qlocktwo.update_json_entry(14, transition_mode)
        self.__transition_mode = transition_mode
        return is_updated
        