# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 10:06:19 2016

@author: Ghassene Jebali jbali.ghassen@gmail.com
"""
from smap.archiver.client import SmapClient
from smap.contrib import dtutil
from scipy.interpolate import interp1d
import os
import xlsxwriter
import datetime
import time

# Temperature data uuid's
T_uuid1 = '35badc5a-4f58-5234-997b-d744605177dc' # capteur du VAV/ VAV zone 4
T_uuid2 = '9b506d3e-7e4c-5896-871f-a061a98a2a10' # capteur du VAV/ VAV zone 13 

# Humidity data uuid's
Hum_uuid3 = '29fdf95e-0b9e-5191-87d2-bab66a248b2a' #capteur 1631/ VAV zone 4
Hum_uuid4 = 'e57a5324-0129-569d-94b4-ec6659f15186' #capteur 1625 VAV zone 12

# Co2 data uuid's
co2_uuid5 = '04b072d6-6b18-5a4f-8469-c6e203646391' #capteur 2106 / VAV zone 9
co2_uuid6 = '17337697-a7aa-5277-a3ae-5dc936a4bd01' #capteur 2029 / VAV zone 18
#'85aac043-ded6-564e-ab87-373b302fe4d0''cc190116-9ccc-53de-bd30-762af630d380'

# Outdoor temperature uuid
T_outdoor_uuid7 = '395005af-a42c-587f-9c46-860f3061ef0d'

# power uuid's
light_uuid1 = 'cbe0422f-7721-5a9d-8713-f65575e27fa5' #kW
recep_uuid1 = '63f7d089-03b4-5364-9543-f08b541c306e' #kW
fan_power_total_uuid1 = 'fd0fddba-5b82-5d14-aae4-5f17ce6166bf' #kW
air_a_flow_uuid1 = '64aceef3-5034-574b-a803-f04ad1224d39' #cfm
air_b_flow_uuid1 = 'e4d4df35-2b0d-562a-801c-8f588dcf803a' #cfm
VAV_flow_uuid=[ 'bdc5d778-a18c-581c-8a71-55579b19cb3d',
            'a15e27db-466e-5a65-bd72-5c253456fb80',
            '42ee90aa-a984-56ad-af9d-7db89b92209d',
            '62febc32-9cae-5e55-9446-5c445f5fd242',
            'fc3eb129-45c8-53b1-9d98-70aa1406a703',
            'c52e0a56-2ee7-57ab-aa5b-90ecb7c865c0',
            '17df2ca6-1970-5e5e-bfa6-99017d84b970',
            '48d31aa3-6aca-539f-81d7-842dd298ca08',
            '42bea0eb-b55b-51bd-8f6e-615e722196e5',
            '9832b251-922f-5608-aa9e-4d1c66ad2dde',
            '14995177-48d9-54c0-a053-283b21168a1e',
            '841c4b64-44a1-565b-bc25-4f483d7afa74',
            'e4440358-c95e-5b3a-90b0-7318b1d1e06b',
            '9315deb4-58f8-5809-af4b-000cd9acf281',
            'faea298a-4525-500a-bde5-527afc29a8dd',
            '2b4aa131-0174-5438-bc86-c5d54910020d',
            '517d3c9c-a96e-5a36-bd7c-10fb7fce1780',
            'e892540f-1e62-58ab-adda-132b55d55b49',
            'f5fd84cb-fc25-537b-bdcb-8b2546158cd2',
            'e679467f-2535-5fa3-936a-ac6074032ae7',
            '4c966235-6c4a-5bdc-94c8-2129b686bb2b'
            ] #cfm
            
air_a_sat_uuid1 = 'a7aa36e6-10c4-5008-8a02-039988f284df' #fahrenheit
air_b_sat_uuid1 = 'a73a5e75-b6a0-50ca-acf2-303873876039' #fahrenheit
air_a_mat_uuid1 = '275d6375-d407-53d2-a600-7dfb3ee544b2' #fahrenheit
air_b_mat_uuid1 = '0133e620-fa49-5f03-86ba-762a4e318ea7' #fahrenheit

VAV_setpt_uuid=['3f9c81bc-16eb-5065-a630-1a288c60c466',#1
            '53c387fb-27a3-59e9-8f08-4ce38c7a9c0d',#2
            'fdab851a-038e-57ca-8a19-768be83cb311',#3
            '0739ff65-715e-5fc9-9cf0-f3ba3e188a7e',#4
            '5ec278b2-d5c6-5a56-b9bc-224960a6d4d8',#5
            'b30f1e46-6aa4-5e12-b959-5dcf8580a36c',#6
            '2cfad52a-7659-5e5b-b59d-7e9fa5e274bf',#7
            '6ea2940f-cc87-5d68-8513-3657c997466b',#8
            '8bdef099-cfd7-55d3-96c7-ec203b31742e',#9
            'c56eeb9f-3fa3-50a6-939a-18449b4fdc1e',#10
            'acc4f993-669c-5000-a5ff-04dc897c6c66',#11
            '2e3ebaf3-c45a-5b56-9e75-666eba2c547f',#12
            '81cf0974-51fe-500d-b24a-04185b970f4f',#13
            '0f28f419-d10b-5cb6-b58a-4ccd4a951ffd',#14
            '113d0082-9892-557e-9754-66f91a570a1e',#15
            'da90c353-8f41-582e-ba3f-44331a320881',#16
            'ef2c9a45-3788-5a09-8bec-6101e45b9425',#17
            'ec5b29e1-2391-56e5-8d45-78db7db10dbc',#18
            '96d4be52-bb4d-5963-8d33-cdb562a7e1fd',#19
            '485e26e4-1113-5ad4-b75c-254e2e475ef5',#20
            '25f277d9-94ee-5217-a4d1-b4d9fce5fafc' #21
            ]   



###############################################################################
def data_acquisition():
###############################################################################   

    day0 = '6-1-2014'
    day1 = '9-9-2015'
    timestep=15 # timestep in minutes
    
###############################################################################    
    # make a client
    client = SmapClient("http://www.openbms.org/backend")
    
    # start and end values are Unix timestamps
    start = dtutil.dt2ts(dtutil.strptime_tz(day0, "%m-%d-%Y"))
    end   = dtutil.dt2ts(dtutil.strptime_tz(day1, "%m-%d-%Y")) 
    
    print 'Download start..'
    # perform temperature data download
    T_tags1 = client.tags("uuid = '" + T_uuid1 + "'")[0]
    T_data1 = client.data_uuid([T_uuid1], start, end, cache=True)[0]
    
    T_tags2 = client.tags("uuid = '" + T_uuid2 + "'")[0]
    T_data2 = client.data_uuid([T_uuid2], start, end, cache=True)[0]
    
    # perform humidity data download
    Hum_tags3 = client.tags("uuid = '" + Hum_uuid3 + "'")[0]
    Hum_data3 = client.data_uuid([Hum_uuid3], start, end, cache=True)[0]
    
    Hum_tags4 = client.tags("uuid = '" + Hum_uuid4 + "'")[0]
    Hum_data4 = client.data_uuid([Hum_uuid4], start, end, cache=True)[0]
    
    # perform co2 data download
    co2_tags5 = client.tags("uuid = '" + co2_uuid5 + "'")[0]
    co2_data5 = client.data_uuid([co2_uuid5], start, end, cache=True)[0]
    
    co2_tags6 = client.tags("uuid = '" + co2_uuid6 + "'")[0]
    co2_data6 = client.data_uuid([co2_uuid6], start, end, cache=True)[0]
    
    # perform outdoor temperature download and correction
    T_outdoor_tags7 = client.tags("uuid = '" + T_outdoor_uuid7 + "'")[0]
    T_outdoor_data7 = client.data_uuid([T_outdoor_uuid7], start, end, cache=True)[0]
    for i in range(len(T_outdoor_data7)):
        if T_outdoor_data7 [i][1]>0:
            T_outdoor_data7 [i][1]=(T_outdoor_data7 [i][1]-32)*5/9
        else:
            T_outdoor_data7 [i][1]=T_outdoor_data7 [i-1][1]
        if T_outdoor_data7 [i][0]<10000:
            T_outdoor_data7 [i][0]=T_outdoor_data7 [i-1][0]+32000
    T_outdoor_tags7 = client.tags("uuid = '" + T_outdoor_uuid7 + "'")[0]
    
    # perform power data download
    light_data = client.data_uuid([light_uuid1], start, end, cache=True)[0]
    recep_data = client.data_uuid([recep_uuid1], start, end, cache=True)[0]
    fan_power_total_data = client.data_uuid([fan_power_total_uuid1], start, end, cache=True)[0]
    
    air_a_sat_data = client.data_uuid([air_a_sat_uuid1], start, end, cache=True)[0]
    air_b_sat_data = client.data_uuid([air_b_sat_uuid1 ], start, end, cache=True)[0]
    air_a_mat_data= client.data_uuid([air_a_mat_uuid1], start, end, cache=True)[0]
    air_b_mat_data = client.data_uuid([air_b_mat_uuid1], start, end, cache=True)[0]
    for data in [air_a_sat_data , air_a_mat_data , air_b_sat_data , air_b_mat_data]:
        for i in range(len(data)):
            data[i][1]=(data[i][1] - 32)*5/9
    
    air_a_flow_data = client.data_uuid([air_a_flow_uuid1], start, end, cache=True)[0]
    air_b_flow_data = client.data_uuid([air_b_flow_uuid1], start, end, cache=True)[0]
    vav_data=[]
    for i in VAV_flow_uuid:
        download=client.data_uuid([i], start, end, cache=True)[0]
        vav_data.append(download)
    flow_floor_4=[]
    for j in range(min([len(x) for x in vav_data])):
        somme=0
        for i in vav_data:
            somme=somme+i[j][1]
        flow_floor_4.append([vav_data[0][j][0] , somme])
    
    # perform temperature setpoints download
    T_setpt_data=[]
    setpt_download=[]
    for i in VAV_setpt_uuid:
        download=client.data_uuid([i], start, end, cache=True)[0]
        setpt_download.append(download)    
    for j in range(min([len(x) for x in setpt_download])):
        value = sum([setpt_download[i][j][1] for i in range(len(setpt_download))])/len(setpt_download)
        T_setpt_data.append([setpt_download[1][j][0] , value])
    
    
    print 'Download done' 
    print
    
###############################################################################    
    
    print 'Calculation start..'
    # convert temperature setpoint unit
    for i in range(len(T_setpt_data)):
        T_setpt_data[i][1]=( T_setpt_data[i][1]-32)*5/9
    
    # calculate ventilation power
    vent_power_data=[]
    for i in range(min(len(fan_power_total_data) , len(air_a_flow_data) , len(air_b_flow_data) , len(flow_floor_4))):
        power=fan_power_total_data[i][1]*flow_floor_4[i][1]/(air_a_flow_data[i][1] + air_b_flow_data[i][1])
        vent_power_data.append([flow_floor_4[i][0] , power])
    
    # calculate H/C power   
    capacity=0.00056937  #kW/C.cfm
    ratio=[]
    for i in range(min(len(air_a_flow_data), len(air_b_flow_data), len(flow_floor_4))):
        division=   flow_floor_4[i][1]/(air_a_flow_data[i][1] + air_b_flow_data[i][1]) 
        ratio.append([air_a_flow_data[i][0] , division ])
    cool_power_data=[]
    for i in range(min(len(air_a_sat_data) , len(air_b_sat_data) , len(air_a_mat_data) , len(air_b_mat_data) , len(ratio))): 
        result = ((capacity*(air_a_sat_data[i][1]-air_a_mat_data[i][1])*air_a_flow_data[i][1])  +  (capacity*(air_b_sat_data[i][1]-air_b_mat_data[i][1])*air_b_flow_data[i][1]))*ratio[i][1]
        cool_power_data.append([ ratio[i][0] , result])
    H_C_power_data=[]
    for i in range(min(len(light_data) , len(recep_data) , len(cool_power_data))): 
        H_C_power_data.append([cool_power_data[i][0] , cool_power_data[i][1] + light_data[i][1]+ recep_data[i][1]])
  
###############################################################################    
    # interpolate the data over a fixed time step    
    imposed_time=[]
    x = max( T_data1[0][0], T_data2[0][0], Hum_data3[0][0], Hum_data4[0][0], co2_data5[0][0], co2_data6[0][0],  T_outdoor_data7[0][0] ) 
    limit= min( T_data1[-1][0] , T_data2[-1][0], Hum_data3[-1][0], Hum_data4[-1][0], co2_data5[-1][0], co2_data6[-1][0],  T_outdoor_data7[-1][0] )
    while x <= limit:
        imposed_time.append(x)
        x += timestep*60*1000
        
    def interpole(data, time):
        time1 = [item[0] for item in data]
        value1= [item[1] for item in data]
        data_synchro = interp1d(time1,value1)(time)
        data_synchro = [i for i in data_synchro]
        return data_synchro
    
    # interpolate temperature setpoint data
    T_setpt_data_synchro=interpole(T_setpt_data, imposed_time)
    
    # interpolate temperature data
    T_data1_synchro=interpole(T_data1, imposed_time)
    T_data2_synchro=interpole(T_data2, imposed_time)
    
    # interpolate humidity data
    Hum_data3_synchro=interpole(Hum_data3, imposed_time)
    Hum_data4_synchro=interpole(Hum_data4, imposed_time)
    
    # interpolate co2 data
    co2_data5_synchro=interpole(co2_data5, imposed_time)
    co2_data6_synchro=interpole(co2_data6, imposed_time)
    
    # interpolate co2 data
    T_outdoor_data7_synchro=interpole(T_outdoor_data7, imposed_time)
    
    # intepole ventilation data
    vent_power_data_synchro=interpole(vent_power_data, imposed_time)
    
    # interpole cooling power data
    H_C_power_data_synchro=interpole(H_C_power_data, imposed_time)
    

    # average each type of data
    T_data_sychro_average= [(a+b)/2 for a,b in zip(T_data1_synchro, T_data2_synchro)]
    for i in range(len(T_data_sychro_average)):
        T_data_sychro_average[i]=(T_data_sychro_average[i]-32)*5/9
    Hum_data_sychro_average= [(a+b)/2 for a,b in zip(Hum_data3_synchro, Hum_data4_synchro)]
    co2_data_sychro_average= [(a+b)/2 for a,b in zip(co2_data5_synchro, co2_data6_synchro)]
    for i in range(len(co2_data_sychro_average)):
        if co2_data_sychro_average[i]>1500:
            co2_data_sychro_average [i]=co2_data_sychro_average [i-1]
    
    
    # calculate the calendar data
    Calendar_data=[]
    Season=[]
    Human_date=[]
    Human_power=[]
    ###### Calendar data=0 --> weekend
    ###### Calendar data=1 --> work night
    ###### Calendar data=2 --> work day
    ###### Season =  1 --> winter
    ###### Season =  0 --> mid season
    ###### Season = -1 --> summer
    for i in imposed_time:
        date = datetime.datetime.fromtimestamp(i/1000).strftime('%Y-%m-%d %H:%M:%S')
        Human_date.append(date)
        year = int (date[0:4])
        month = int (date[5:7])
        day = int (date[8:10])
        hour = int(date[11:13])
        day_number=datetime.date(year, month, day).weekday()
        if month==1 or month==2 or month==12:
            Season.append(1)
        if month==6 or month==7 or month==8 or month==9:
            Season.append(-1)
        if month==3 or month==4 or month==5 or month==10 or month==11:
            Season.append(0)
        
        if day_number!=5 and day_number!=6:
            if hour>=7 and hour<19:
                Cal_day = 2
            else: 
                Cal_day = 1
        else: 
            Cal_day = 0
        Calendar_data.append(Cal_day)
        
        
        
        if Cal_day==2 and (hour<16 and hour>=10):
            number=30
        else:
            if Cal_day==2 and ((hour<10 and hour>=7) or (hour<19 and hour>=16)):
                number=15
            else:
                number=0
        Human_power.append( number*0.1 )
    
###############################################################################    
    # output of the data aquisition            
    DATA_LIST={'Timestamp':imposed_time, 'Temperature':T_data_sychro_average, 'Humidity':Hum_data_sychro_average, 'Calendar data':Calendar_data,'Human date':Human_date , 'Season':Season, 'CO2':co2_data_sychro_average, 'Outdoor Temperature':T_outdoor_data7_synchro , 'Ventilation':vent_power_data_synchro , 'H/C power': H_C_power_data_synchro , 'Setpoint Temperature':T_setpt_data_synchro, 'Human_power':Human_power}
    
    print 'Calculation and interpolation done'
    print
    
    print 'Write start..'
    # Create a path and a file to save the data
    workbook = xlsxwriter.Workbook('DATA_LIST.xlsx')
    worksheet = workbook.add_worksheet()
    col=0
    for keys in DATA_LIST.keys():    
        worksheet.write(0, col , keys)
        col=col+1
    col=0
    for data in DATA_LIST.values():
        row=1    
        for value in data:
                worksheet.write(row, col , value)
                row += 1
        col=col+1
    workbook.close()
    
    # save the metadata of the used sensors 
    i=0
    for metadata in [T_tags1,T_tags2, Hum_tags3, Hum_tags4, co2_tags5, co2_tags6, T_outdoor_tags7]:
        i=i+1
        with open(os.path.join('.Cache', 'metadata'+str(i)+'.txt'), 'w') as f:
            for key, value in metadata.items():
                f.write(key+':'+value+'\n')
    
    print 'Write done'
    return DATA_LIST
    
    

###############################################################################
def Real_Time_Data(client):
###############################################################################  
    #client = SmapClient("http://www.openbms.org/backend")
    
    # Temperature
    T_data1 = client.latest("uuid = '"+ T_uuid1+"'")[0]['Readings'][0][1]
    T_data2 = client.latest("uuid = '"+ T_uuid2+"'")[0]['Readings'][0][1]
    T=(((T_data1+T_data2)/2)-32)*5/9
    
    # Co2 data
    co2_uuid5 = 'b706f40c-b7f1-568f-b676-be02200ba0cd' # VAV zone 21 / RPI 17
    co2_uuid6 = 'bd515b13-d391-5fb6-a272-c82504d7680a' # VAV zone 2 / RPI 16
    co2_uuid7 = '630d4fc1-6a64-5c54-a0c7-f502d7777abd' # VAV zone 13 / RPI 13

    co2_data1 = client.latest("uuid = '"+ co2_uuid5+"'")[0]['Readings'][0][1]
    co2_data2 = client.latest("uuid = '"+ co2_uuid6+"'")[0]['Readings'][0][1]
    co2_data3 = client.latest("uuid = '"+ co2_uuid7+"'")[0]['Readings'][0][1]
    
    #co2=(co2_data1 + co2_data2 + co2_data3 )/3
    co2= co2_data1
    
    # Set ponit 
    S=0
    for uuid in VAV_setpt_uuid:
        S=S + (client.latest("uuid = '"+ uuid+"'")[0]['Readings'][0][1]-32)*5/9
    set_point = S/len(VAV_setpt_uuid)
    
    # Humidity data
    hum_data1 = client.latest("uuid = '"+ Hum_uuid3+"'")[0]['Readings'][0][1]
    hum_data2 = client.latest("uuid = '"+ Hum_uuid4+"'")[0]['Readings'][0][1]
    hum=(hum_data1+hum_data2)/2
    
    # outdoor T
    T_outdoor = (client.latest("uuid = '"+ T_outdoor_uuid7+"'")[0]['Readings'][0][1]-32)*5/9
    
    # Calendar and season data
    date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    Human_date=date
    year = int (date[0:4])
    month = int (date[5:7])
    day = int (date[8:10])
    hour = int(date[11:13])
    day_number=datetime.date(year, month, day).weekday()
    if month==1 or month==2 or month==12:
        Season=1
    if month==6 or month==7 or month==8 or month==9:
        Season=-1
    if month==3 or month==4 or month==5 or month==10 or month==11:
        Season=0
    
    if day_number!=5 and day_number!=6:
        if hour>=7 and hour<19:
            Cal_data = 2
        else: 
            Cal_data = 1
    else: 
        Cal_data = 0
    
    # H/C power and ventilation
    light_data = client.latest("uuid = '"+ light_uuid1+"'")[0]['Readings'][0][1]
    recep_data = client.latest("uuid = '"+ recep_uuid1+"'")[0]['Readings'][0][1]
    fan_power_total_data = client.latest("uuid = '"+ fan_power_total_uuid1+"'")[0]['Readings'][0][1]
    
    air_a_sat_data = (client.latest("uuid = '"+ air_a_sat_uuid1+"'")[0]['Readings'][0][1]-32)*5/9
    air_b_sat_data = (client.latest("uuid = '"+ air_b_sat_uuid1 +"'")[0]['Readings'][0][1]-32)*5/9
    air_a_mat_data= (client.latest("uuid = '"+ air_a_mat_uuid1+"'")[0]['Readings'][0][1]-32)*5/9
    air_b_mat_data = (client.latest("uuid = '"+ air_b_mat_uuid1+"'")[0]['Readings'][0][1]-32)*5/9
    
    air_a_flow_data = client.latest("uuid = '"+ air_a_flow_uuid1+"'")[0]['Readings'][0][1]
    air_b_flow_data = client.latest("uuid = '"+ air_b_flow_uuid1+"'")[0]['Readings'][0][1]
    flow_floor_4=0
    for uuid in VAV_flow_uuid:
        flow_floor_4 = flow_floor_4 + client.latest("uuid = '"+ uuid+"'")[0]['Readings'][0][1]
    
    vent_power=fan_power_total_data*flow_floor_4/(air_a_flow_data + air_b_flow_data)
    
    capacity=0.00056937  #kW/C.cfm
    ratio=   flow_floor_4/(air_a_flow_data + air_b_flow_data) 
    cool_power = ((capacity*(air_a_sat_data-air_a_mat_data)*air_a_flow_data)  +  (capacity*(air_b_sat_data-air_b_mat_data)*air_b_flow_data))*ratio
    H_C_power = cool_power + light_data+ recep_data
      
    return [T, co2, set_point, hum, T_outdoor, Human_date, Season, Cal_data, vent_power, H_C_power, cool_power, hour]
