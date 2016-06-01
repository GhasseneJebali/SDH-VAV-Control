# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 10:05:03 2016

@author: Ghassene Jebali jbali.ghassen@gmail.com
"""

import warnings
import src
import time

warnings.filterwarnings("ignore")

update_time_step = 900 # in secondes
area = 296 #sf
debug = 1

DATA_LIST, KNN_model, BRR_model, Mean_Running_Average = src.setup()

last_call = 0
while True:
    if ((time.time()-last_call) >= update_time_step):  
        Mean_Running_Average = src.update(DATA_LIST, BRR_model, 'start', area, Mean_Running_Average, debug)
        last_call= time.time()
        