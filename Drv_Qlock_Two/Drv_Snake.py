# -*- coding: utf-8 -*-

import numpy as np;
from Drv_Qlock_Two.internal.Qlock_Matrix import Qlock_Matrix
from Drv_Qlock_Two.internal.Qlock_Hardware_Binding import Qlock_Hardware_Binding
from Drv_Qlock_Two.internal.Json_Snake import Json_Snake
from Drv_Qlock_Two.internal.Json_Ws2812b import Json_Ws2812b
from Drv_Qlock_Two.internal.Task_Pool import Task_Pool
from Drv_Qlock_Two.internal.Snake_Game import *
import sys


class Drv_Snake:
    
    
    def __init__(self, json_snake_file_path, json_ws2812b_file_path):
        
        
        self.__json_snake = Json_Snake(json_snake_file_path)
        if (not(self.__json_snake.is_json_valid())):
            sys.exit("Snake Json does not yield a valid config. System will exit!")
        snake_cfg = self.__json_snake.get_json_results()
        
        self.__json_ws2812b = Json_Ws2812b(json_ws2812b_file_path)
        if (not(self.__json_ws2812b.is_json_valid())):
            sys.exit("Ws2812b Json does not yield a valid config. System will exit!")
        ws_2812b_cfg = self.__json_ws2812b.get_json_results()
        
        
        num_letter_vertical = snake_cfg[0]
        num_letter_horizontal = snake_cfg[1]
        leds_per_letter = snake_cfg[2]
        
        game_speed = snake_cfg[6]
        self.__body_color = snake_cfg[7]
        self.__head_color = snake_cfg[8]
        background_color = snake_cfg[9]
        self.__token_color = snake_cfg[10]
        num_leds = num_letter_vertical * num_letter_horizontal * leds_per_letter;
        
        
        self.__snake_game = Snake_Game()
        self.__qlock_matrix = Qlock_Matrix(num_letter_vertical, num_letter_horizontal, leds_per_letter, background_color);
        self.__qlock_hardware_binding = Qlock_Hardware_Binding(num_leds, snake_cfg, ws_2812b_cfg);
        self.__next_control = SNAKE_CONTROL_LEFT
        self.__task_pool = Task_Pool(game_speed)
        
     
    def start_game(self):
        self.__task_pool.add_task(self.next_move, []);
        self.__task_pool.start_worker_thread();
        
        
    def next_move(self, args):
        #print("Next move")
        is_lost = self.__snake_game.next_move(self.__next_control)
        
        if (is_lost):
            self.__qlock_matrix.enable_element(2, 4, self.__token_color)
            self.__qlock_matrix.enable_element(2, 6, self.__token_color)
            self.__qlock_matrix.enable_element(2, 7, self.__token_color)
            self.__qlock_matrix.enable_element(2, 10, self.__token_color)
            self.__qlock_matrix.enable_element(3, 1, self.__token_color)
            self.__qlock_matrix.enable_element(3, 2, self.__token_color)
            self.__qlock_matrix.enable_element(4, 5, self.__token_color)
            self.__qlock_matrix.enable_element(4, 9, self.__token_color)
        else:
            game_field = self.__snake_game.get_game_field()
            # Draw Head
            id_head = np.where(game_field == 2)
            id_head_y = id_head[0]
            id_head_x = id_head[1]
            self.__qlock_matrix.enable_element(id_head_y[0], id_head_x[0], self.__head_color)
            
            # Draw Token
            id_token = np.where(game_field == 3)
            id_token_y = id_token[0]
            id_token_x = id_token[1]
            self.__qlock_matrix.enable_element(id_token_y[0], id_token_x[0], self.__token_color)
            
            # Draw Body
            id_body = np.where(game_field == 1)  
            id_body_y = id_body[0]
            id_body_x = id_body[1]
        
            for i in range(id_body_y.size):
                self.__qlock_matrix.enable_element(id_body_y[i], id_body_x[i], self.__body_color)
        self.flush_sync()
        
        if (not is_lost):
            self.__task_pool.add_task(self.next_move, []);
        
    def send_control(self, control):
        self.__next_control = control;
        
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
        