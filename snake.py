# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 15:10:56 2021

@author: andre
"""

from Drv_Qlock_Two.Drv_Snake import *;
import time




json_snake_file_path = "Drv_Qlock_Two/cfg/Drv_Snake.json"
json_ws2812b_file_path = "Drv_Qlock_Two/cfg/Drv_ws2812b.json"
drv_snake = Drv_Snake(json_snake_file_path, json_ws2812b_file_path)
drv_snake.start_game()

import sys,tty,termios
class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch


def get():
    inkey = _Getch()
    key = 0
    while(1):
        k=inkey()
        if k!='':break
    print(k)
    if k=='\x1b[A':
        key = 1 #up
    elif k=='\x1b[B':
        key = 2 # down
    elif k=='\x1b[C':
        key = 3 # right
    elif k=='\x1b[D':
        key = 4 #left
    else:
        print ("not an arrow key! ", k)
    return key

for i in range(0,100):
    key = get()
    
    
    if (key == 1):
        print("up")
        drv_snake.send_control(SNAKE_CONTROL_TOP)
    if (key == 2):
        print("down")
        drv_snake.send_control(SNAKE_CONTROL_BOT)
    if (key == 3):
        print("right")
        drv_snake.send_control(SNAKE_CONTROL_RIGHT)
    if (key == 4):
        print("left")
        drv_snake.send_control(SNAKE_CONTROL_LEFT)

    
while(False):
    drv_snake.send_control(SNAKE_CONTROL_TOP)
    time.sleep(0.8)
    drv_snake.send_control(SNAKE_CONTROL_RIGHT)
    time.sleep(0.8)
    drv_snake.send_control(SNAKE_CONTROL_BOT)
    time.sleep(0.8)
    drv_snake.send_control(SNAKE_CONTROL_LEFT)
    time.sleep(0.8)