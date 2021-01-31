# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 07:55:24 2021

@author: andre
"""

import time
import threading

class Task_Pool:
    def __init__(self, sleep_duration = 10, thread_pool_size = 100):
        self.__task_queue = list()
        self.__param_queue = list()
        self.__task_pool_size = thread_pool_size;
        self.__sleep_duration = sleep_duration / 1000;
        
        self.stop_threads = False;
        self.__run_thread = threading.Thread(target = self.__thread_runner, args = (lambda : self.stop_threads, )) 
        

    def start_worker_thread(self):
        self.__run_thread.start()
        
    def add_task(self, task, args):
        print("Add Task")
        if (len(self.__task_queue) <= self.__task_pool_size):
            self.__task_queue.append(task)
            self.__param_queue.append(args)
            
    def stop(self):
        self.stop_threads = True;
            
    def __thread_runner(self, stop_threads):
        print("Start runner")
        while(True):
            
            if stop_threads():
                break
            if (len(self.__task_queue) > 0):
                t1 = time.time()
                self.__task_queue[0](self.__param_queue[0]);
                self.__task_queue.pop(0);
                self.__param_queue.pop(0);
                task_duration = time.time() - t1
                
                if (task_duration < self.__sleep_duration):
                    time.sleep(self.__sleep_duration - task_duration)
            else:
                time.sleep(self.__sleep_duration)