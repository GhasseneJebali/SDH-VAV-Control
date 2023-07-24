# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 10:05:03 2016

@author: Ghassene Jebali jbali.ghassen@gmail.com
"""

import time
import warnings
import src
from smap.archiver.client import SmapClient
from smap.contrib import dtutil
from smap import driver
from smap.util import periodicSequentialCall
from control import bacnet

warnings.filterwarnings("ignore")


class VAV_Adaptive_control(driver.SmapDriver):
    def __init__(self):
        self.error = None
        self.rate = None
        self.area = None
        self.warning = None
        self.debug = None
        self.state = None

    def setup(self):
        self.rate = 300  # in secondes
        self.area = 296  # sf
        self.add_timeseries("/error", "binary", data_type="double")
        self.add_timeseries("/Warning", "binary", data_type="double")
        self.add_timeseries("/Heat_Cool", "binary", data_type="double")
        self.add_timeseries("/Minimum_ventillation", "cfm", data_type="double")
        self.add_timeseries("/T_Setpoint", "F", data_type="double")
        self.add_timeseries("/Weighted_Running_Average", "C", data_type="double")
        self.error = False
        self.warning = 0
        self.debug = 0
        self.state = "start"

        db = "/smap/bacnet/db/db_sdh_8062015"
        bacnet_interface = "eth0"
        bacnet_port = "47816"

        self.bacnet_c = bacnet.BACnetController(db, bacnet_interface, bacnet_port)
        self.client = SmapClient("http://www.openbms.org/backend")
        self.DATA_LIST, self.KNN_model, self.BRR_model, self.mean_running_average = (
            src.setup()
        )

    def start(self):
        periodicSequentialCall(self.read).start(self.rate)

    def read(self):
        try:
            self.mean_running_average, self.state, self.vent, self.heat, self.setpt, self.warning = src.update(
                self.DATA_LIST,
                self.BRR_model,
                self.client,
                self.state,
                self.area,
                self.mean_running_average,
                self.debug,
            )
            self.error = False

            if self.debug == 0:
                command = True
            if self.debug == 1:
                command = False

            if command and self.warning < 4:

                self.bacnet_c.write("SDH.S4-02:HEAT.COOL", "SDH.PXCM-11", self.heat)
                self.bacnet_c.write("SDH.S4-02:CTL STPT", "SDH.PXCM-11", self.setpt)
                self.bacnet_c.write("SDH.S4-02:CTL FLOW MIN", "SDH.PXCM-11", self.vent)

                self.bacnet_c.write("SDH.S4-04:HEAT.COOL", "SDH.PXCM-11", self.heat)
                self.bacnet_c.write("SDH.S4-04:CTL STPT", "SDH.PXCM-11", self.setpt)
                self.bacnet_c.write("SDH.S4-04:CTL FLOW MIN", "SDH.PXCM-11", self.vent)

                self.bacnet_c.write("SDH.S4-13:HEAT.COOL", "SDH.PXCM-11", self.heat)
                self.bacnet_c.write("SDH.S4-13:CTL STPT", "SDH.PXCM-11", self.setpt)
                self.bacnet_c.write("SDH.S4-13:CTL FLOW MIN", "SDH.PXCM-11", self.vent)

                self.bacnet_c.write("SDH.S4-12:HEAT.COOL", "SDH.PXCM-11", self.heat)
                self.bacnet_c.write("SDH.S4-12:CTL STPT", "SDH.PXCM-11", self.setpt)
                self.bacnet_c.write("SDH.S4-12:CTL FLOW MIN", "SDH.PXCM-11", self.vent)

                self.bacnet_c.write("SDH.S4-18:HEAT.COOL", "SDH.PXCM-11", self.heat)
                self.bacnet_c.write("SDH.S4-18:CTL STPT", "SDH.PXCM-11", self.setpt)
                self.bacnet_c.write("SDH.S4-18:CTL FLOW MIN", "SDH.PXCM-11", self.vent)

                self.bacnet_c.write("SDH.S4-21:HEAT.COOL", "SDH.PXCM-11", self.heat)
                self.bacnet_c.write("SDH.S4-21:CTL STPT", "SDH.PXCM-11", self.setpt)
                self.bacnet_c.write("SDH.S4-21:CTL FLOW MIN", "SDH.PXCM-11", self.vent)

        except Exception as err:
            self.error = True
            print(err)

        if self.debug == 1:
            try:
                self.add("/error", time.time(), float(self.error))
                self.add("/Warning", time.time(), float(self.warning))
                self.add("/Heat_Cool", time.time(), float(self.heat))
                self.add("/Minimum_ventillation", time.time(), float(self.vent))
                self.add("/T_Setpoint", time.time(), float(self.setpt))
                self.add(
                    "/Weighted_Running_Average",
                    time.time(),
                    float(self.mean_running_average),
                )
                # bacnet_c.write('SDH.S4-13:HEAT.COOL', 'SDH.PXCM-11', None, clear=True)
            except Exception:
                pass
