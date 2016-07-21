# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 10:05:03 2016

@author: Ghassene Jebali jbali.ghassen@gmail.com
"""

from smap.archiver.client import SmapClient
from smap.contrib import dtutil
import warnings
import src
import time
import sys
from smap import driver
from smap.util import periodicSequentialCall
from control import bacnet

warnings.filterwarnings("ignore")

class VAV_Adaptive_control(driver.SmapDriver):
    
    def setup(self, opts):
        self.rate = 300 # in secondes
        self.area = 296 #sf
        self.add_timeseries("/error", "binary", data_type='double')
        self.add_timeseries("/Warning", "binary", data_type='double')
        self.add_timeseries("/Heat_Cool", "binary", data_type='double')
        self.add_timeseries("/Minimum_ventillation", "cfm", data_type='double')
        self.add_timeseries("/T_Setpoint", "F", data_type='double')
        self.add_timeseries("/Weighted_Running_Average", "C", data_type='double')
        self.error = False
        self.warning = 0
        self.debug = 0
        self.state = 'start'
#    try:
#        debug=int(sys.argv[1])
#    except Exception:
#        debug = 1
        
        db = '/smap/bacnet/db/db_sdh_8062015'
        bacnet_interface = 'eth0'
        bacnet_port = '47816'
                
        self.bacnet_c = bacnet.BACnetController(db, bacnet_interface, bacnet_port) 
        self.client = SmapClient("http://www.openbms.org/backend")
        self.DATA_LIST, self.KNN_model, self.BRR_model, self.Mean_Running_Average = src.setup()
        
    def start(self):
        periodicSequentialCall(self.read).start(self.rate)
    
    
    def read(self):
        try:
            self.Mean_Running_Average, self.state, self.vent, self.heat, self.setpt, self.warning = src.update(self.DATA_LIST, self.BRR_model, self.client, self.state, self.area, self.Mean_Running_Average, self.debug)
            self.error = False
            
            if (self.debug == 0):
                command = True
            if (self.debug == 1):
                command = False
        
            if (command and self.warning < 4):

                self.bacnet_c.write('SDH.S4-13:HEAT.COOL', 'SDH.PXCM-11', self.heat)
                self.bacnet_c.write('SDH.S4-13:CTL STPT', 'SDH.PXCM-11', self.setpt)    
                self.bacnet_c.write('SDH.S4-13:CTL FLOW MIN', 'SDH.PXCM-11', self.vent)
                
        
        except Exception, e:
            self.error = True
            print e
            pass
            #self.bacnet_c.write('SDH.S4-13:HEAT.COOL', 'SDH.PXCM-11', None, clear=True)
            #self.bacnet_c.write('SDH.S4-13:CTL STPT', 'SDH.PXCM-11', None, clear=True)
            #self.bacnet_c.write('SDH.S4-13:CTL FLOW MIN', 'SDH.PXCM-11', None, clear=True)
            
#        try:  
#            self.add("/error",time.time(), float(self.error))
#            self.add("/Warning",time.time(), float(self.warning))
#            self.add("/Heat_Cool",time.time(), float(self.heat))
#            self.add("/Minimum_ventillation",time.time(), float(self.vent))
#            self.add("/T_Setpoint",time.time(), float(self.setpt))
#            self.add("/Weighted_Running_Average",time.time(), float(self.Mean_Running_Average))
#                #bacnet_c.write('SDH.S4-13:HEAT.COOL', 'SDH.PXCM-11', None, clear=True)  
#        except Exception:
#            pass     
