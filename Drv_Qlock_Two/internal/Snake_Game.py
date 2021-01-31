# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 11:00:14 2021

@author: andre
"""

import numpy as np
import sys


SNAKE_CONTROL_RIGHT = 1
SNAKE_CONTROL_BOT = 2
SNAKE_CONTROL_LEFT = 3
SNAKE_CONTROL_TOP = 4

class Snake_Game:
    def __init__(self, num_element_vertical = 10, num_element_horizontal = 11):
        self.__num_element_vertical = num_element_vertical;
        self.__num_element_horizontal = num_element_horizontal;
        
        self.__name_length = 5
        self.__direction = SNAKE_CONTROL_LEFT
        
        self.__game_field = np.zeros((num_element_vertical, num_element_horizontal))
        
        self.__head_position = np.array((4, 2))
        for i in range(self.__name_length):
            self.__game_field[self.__head_position[0], self.__head_position[1] + i] = self.__name_length - i
        self.set_next_token()
            
    def next_move(self, direction = -1):
        is_lost = False
        if ((direction > 0) and (direction < 5)):
            self.__direction = direction
            
        
        
        if (direction == SNAKE_CONTROL_RIGHT):
            new_pos = self.__head_position
            new_pos[1] = new_pos[1] + 1
            new_pos[1] = new_pos[1] % self.__num_element_horizontal
            
        elif (direction == SNAKE_CONTROL_BOT):
            new_pos = self.__head_position
            new_pos[0] = new_pos[0] + 1
            new_pos[0] = new_pos[0] % self.__num_element_vertical
                
        elif (direction == SNAKE_CONTROL_LEFT):
            new_pos = self.__head_position
            new_pos[1] = new_pos[1] - 1
            new_pos[1] = new_pos[1] % self.__num_element_horizontal
            
        elif (direction == SNAKE_CONTROL_TOP):
            new_pos = self.__head_position
            new_pos[0] = new_pos[0] - 1
            new_pos[0] = new_pos[0] % self.__num_element_vertical
        
            
        # Check if new_pos hit the token field
        if ((new_pos[0] == self.__next_token[0]) and (new_pos[1] == self.__next_token[1])):
            self.__name_length = self.__name_length + 1
            self.set_next_token()
        else:
            # Check if the snake was hit
            if (self.__game_field[new_pos[0], new_pos[1]] > 0):
                print("you lost!")
                is_lost = True
            self.__game_field[self.__game_field > 0] = self.__game_field[self.__game_field > 0] - 1  
            
        self.__game_field[new_pos[0], new_pos[1]] = self.__name_length
        self.__head_position = new_pos
        
        return is_lost
        
    def get_game_field(self):
        game_field = np.zeros((self.__num_element_vertical, self.__num_element_horizontal))
        game_field[self.__next_token[0], self.__next_token[1]] = 3
        game_field[self.__game_field == self.__name_length] = 2
        game_field[(self.__game_field < self.__name_length) & (self.__game_field > 0)] = 1
        return game_field
    
    
    def set_next_token(self):
        
        id_free_fields = np.where(self.__game_field == 0)
        
        if (len(id_free_fields) == 0):
            print("YOU WON! Application will end!")
            sys.exit("YOU WON! Application will end!")
            
        rand_seed = np.random.randint(id_free_fields[0].size)
        y = id_free_fields[0][rand_seed]
        x = id_free_fields[1][rand_seed]
        self.__next_token = np.array((y, x))
