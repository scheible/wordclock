# -*- coding: utf-8 -*-


from internal.Qlock_Matrix import Qlock_Matrix
import numpy as np

qlock_matrix = Qlock_Matrix(11, 10, 2, np.array((100, 20, 30)));

mat = qlock_matrix.getmat()
qlock_matrix.enable_element(1, 1)
led_list = qlock_matrix.get_led_list()
