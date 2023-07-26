from control import bacnet


bacnet_c = bacnet.BACnetController(
    db="/smap/bacnet/db/db_sdh_8062015",
    bacnet_interface="eth0",
    bacnet_port="47816",
)

bacnet_c.write("SDH.S4-13:HEAT.COOL", "SDH.PXCM-11", 1)
bacnet_c.write("SDH.S4-13:CTL STPT", "SDH.PXCM-11", 74)
