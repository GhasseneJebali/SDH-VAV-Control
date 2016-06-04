# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 10:05:03 2016

@author: Ghassene Jebali jbali.ghassen@gmail.com
"""

import warnings
import src
import time
import sys
from smap import driver
from smap.util import periodicSequentialCall

warnings.filterwarnings("ignore")

class VAV_Adaptive_control(driver.SmapDriver):
    
    def setup(self, opts):
        self.rate = 900 # in secondes
        self.area = 296 #sf
        
        self.debug = 1
#    try:
#        debug=int(sys.argv[1])
#    except Exception:
#        debug = 1
        self.DATA_LIST, self.KNN_model, self.BRR_model, self.Mean_Running_Average = src.setup()
        
    def start(self):
        periodicSequentialCall(self.update).start(self.rate)
    
    
    def update(self):
        
        self.Mean_Running_Average = src.update(self.DATA_LIST, self.BRR_model, 'start', self.area, self.Mean_Running_Average, self.debug)
    
    
#    last_call = 0
#    while True:
#        if ((time.time()-last_call) >= update_time_step):  
#            Mean_Running_Average = src.update(DATA_LIST, BRR_model, 'start', area, Mean_Running_Average, debug)
#            last_call= time.time()
    