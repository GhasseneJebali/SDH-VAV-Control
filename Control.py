# -*- coding: utf-8 -*-
"""
Created on Tue May 17 10:34:46 2016

@author: Ghassene Jebali jbali.ghassen@gmail.com
"""
# returns the mean temperature of a given date
def max_T_history(date):
    import requests
    
    urlstart = 'http://api.wunderground.com/api/0d2ebd8eea932783/history_'
    urlend = '/q/CA/berkeley.json'
    url = urlstart + date + urlend
    data = requests.get(url).json()

    return data['history']['dailysummary'][0]['maxtempm']
    
    
# returns the date of a previous delta day
def previous_date(delta):
    
    import time
    import datetime
    
    if int(time.strftime("%j")) > int(delta):
        day = int(time.strftime("%j"))-int(delta)
        year = time.strftime("%Y")
    else:
        day = 366 + int(time.strftime("%j"))-int(delta)
        year = int(time.strftime("%Y"))-1
        
    now = str(year)+' '+str(day)
    date = str(datetime.datetime.strptime(now, '%Y %j'))
    y = str(date[0:4])
    m = str(date[5:7])
    d = str(date[8:10])
    return y+m+d
 
# returns the minimum and maximum temperature for a given running average. 90% acceptability
def ACZ(previous_Mean_Running_Average):    
    import time
    import datetime
    
    alpha = 0.7 # Higher alpha means slower adaptation
    T_history={}
    
    date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')    
    hour = int(date[11:13])
    if hour == 0:
        for i in range(1,8):
            T_history[str(i)] = max_T_history(previous_date(i)) 
        Mean_Running_Average =  (1.0 - alpha) * sum( (alpha** (i-1) ) * int(T_history [str(i)]) for i in range(1,8) )
    else:
        Mean_Running_Average = previous_Mean_Running_Average
    
    Upper_limit = 0.31 * Mean_Running_Average + 20.3
    Lower_limit = 0.31 * Mean_Running_Average + 15.3
    
    return Lower_limit, Upper_limit, Mean_Running_Average
    

def control(state, N_person, area, T_outdoor, co2, T_predicted, Mean_Running_Average ):
    import time
    import requests
       
    
    forecast = requests.get("http://api.wunderground.com/api/0d2ebd8eea932783/forecast/q/CA/berkeley.json").json()
    next_day = forecast['forecast']['simpleforecast']['forecastday'][0]
    
    T_forecast_max = next_day['high']['celsius'] 
    
    # temperature setpoints
    Lower_T_limit, Upper_T_limit, Mean_Running_Average  = ACZ(Mean_Running_Average)
    
    Hight_setpt = (Lower_T_limit + 3*Upper_T_limit)/4
    Center_setpt = (Lower_T_limit + Upper_T_limit)/2
    Low_setpt = (3*Lower_T_limit + Upper_T_limit)/4
    Hight_setpt=round(Hight_setpt,1)
    Center_setpt=round(Center_setpt,1)
    Low_setpt=round(Low_setpt,1)
    
    
    # ventillation setpoint
    CA = 0.06 # cfm/ft2
    CP = 5 # cfm/person
    Zone_Air_Distribution_Effectiveness = 1.0
    Vent_min = (CA*area + CP*N_person) / Zone_Air_Distribution_Effectiveness
    Vent_setpt = 2*Vent_min

    # morning afternnon determination
    hour = time.strftime("%H")
    if hour < 12:
        AM_PM = 'AM'
    else:
        AM_PM = 'PM'        
         
         
    if state == 'not occupied':
        if Mean_Running_Average > 15 :
           
            vent = Vent_setpt*2
            heat = 0
            setpt = Lower_T_limit
            return   vent, heat, setpt, Mean_Running_Average
        else:
           
            vent = Vent_setpt*2
            heat = 1
            setpt = Lower_T_limit
            return    vent, heat, setpt, Mean_Running_Average
                   
    if state == 'occupied':
        if co2 > 800:
      
            vent = Vent_setpt*4
            heat = 0
            setpt = Center_setpt
            return   vent, heat, setpt, Mean_Running_Average
        if co2 <= 800:
            if T_predicted > Upper_T_limit:
              
                vent = Vent_setpt*4
                heat = 0
                setpt = Center_setpt
                return  vent, heat, setpt, Mean_Running_Average
            if T_predicted < Lower_T_limit:
              
                vent = Vent_setpt*3
                heat = 1
                setpt = Low_setpt
                return  vent, heat, setpt, Mean_Running_Average
            else:
                if Mean_Running_Average <= 15:
                    if AM_PM == 'AM':
                      
                        vent = Vent_setpt*3
                        heat = 1
                        setpt = Low_setpt
                        return   vent, heat, setpt, Mean_Running_Average
                    if AM_PM == 'PM':
                      
                        vent = Vent_setpt*3
                        heat = 1
                        setpt = Center_setpt
                        return   vent, heat, setpt, Mean_Running_Average
                if Mean_Running_Average > 15:
                    if AM_PM == 'AM':
                       
                        vent = Vent_setpt*3
                        heat = 0
                        setpt = Low_setpt
                        return   vent, heat, setpt, Mean_Running_Average
                    if AM_PM == 'PM':
                      
                        vent = Vent_setpt*3
                        heat = 0
                        setpt = Center_setpt
                        return   vent, heat, setpt , Mean_Running_Average    

    if state == 'slightly occupied':
        if ( (AM_PM == 'PM') or ( (AM_PM == 'AM') and (T_forecast_max < 28) ) ):
            
            if Mean_Running_Average > 15:
                if T_predicted > Upper_T_limit:
          
                    vent = Vent_setpt*3
                    heat = 0
                    setpt = Center_setpt
                    return  vent, heat, setpt, Mean_Running_Average
                if T_predicted < Lower_T_limit:
                
                    vent = Vent_setpt*2
                    heat = 0
                    setpt = Low_setpt
                    return  vent, heat, setpt, Mean_Running_Average
                else:
                 
                    vent = Vent_setpt*2
                    heat = 0
                    setpt = Center_setpt
                    return  vent, heat, setpt, Mean_Running_Average
            if Mean_Running_Average <= 15:
                if T_predicted > Upper_T_limit:
               
                    vent = Vent_setpt*3
                    heat = 0
                    setpt = Center_setpt
                    return  vent, heat, setpt, Mean_Running_Average
                if T_predicted < Lower_T_limit:

                    vent = Vent_setpt*2
                    heat = 1
                    setpt = Low_setpt
                    return   vent, heat, setpt, Mean_Running_Average
                else:

                    vent = Vent_setpt*2
                    heat = 1
                    setpt = Center_setpt
                    return  vent, heat, setpt, Mean_Running_Average
        else:
            vent = Vent_setpt*3
            heat = 0
            setpt = Center_setpt
            return   vent, heat, setpt, Mean_Running_Average

  
  
  