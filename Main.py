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
        self.rate = 60 # in secondes
        self.area = 296 #sf
        self.add_timeseries("/error", "binary", data_type='double')
        self.error = False
        self.debug = 1
#    try:
#        debug=int(sys.argv[1])
#    except Exception:
#        debug = 1
        self.DATA_LIST, self.KNN_model, self.BRR_model, self.Mean_Running_Average = src.setup()
        
    def start(self):
        periodicSequentialCall(self.update).start(self.rate)
    
    
    def update(self):
        try:
            self.Mean_Running_Average = src.update(self.DATA_LIST, self.BRR_model, 'start', self.area, self.Mean_Running_Average, self.debug)
            self.error = False
        except Exception:
            self.error = True
        self.add("/error",time.time(), float(self.error))
            #bacnet_c.write('SDH.S4-13:HEAT.COOL', 'SDH.PXCM-11', None, clear=True)    
