# -*- coding: utf-8 -*-
"""
Created on Tue May 17 10:34:46 2016

@author: Ghassene Jebali jbali.ghassen@gmail.com
"""
import time
import datetime
import requests


# returns the mean temperature of a given date
def max_t_history(date):
    """ max temperature in history"""
    urlstart = 'http://api.wunderground.com/api/0d2ebd8eea932783/history_'
    urlend = '/q/CA/berkeley.json'
    url = urlstart + date + urlend
    data = requests.get(url).json()

    return data['history']['dailysummary'][0]['maxtempm']


# returns the date of a previous delta day
def previous_date(delta):
    """returns previous date"""
    if int(time.strftime("%j")) > int(delta):
        day = int(time.strftime("%j"))-int(delta)
        year = time.strftime("%Y")
    else:
        day = 366 + int(time.strftime("%j"))-int(delta)
        year = int(time.strftime("%Y")) - 1

    now = str(year)+' '+str(day)
    date = str(datetime.datetime.strptime(now, '%Y %j'))
    year = str(date[0:4])
    month = str(date[5:7])
    day = str(date[8:10])
    return year + month + day


def acz(previous_mean_running_average):
    """returns the minimum and maximum temperature for a given running average. 90% acceptability"""
    alpha = 0.7  # Higher alpha means slower adaptation
    t_history={}

    date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')    
    hour = int(date[11:13])
    if hour == 0:
        for i in range(1,8):
            t_history[str(i)] = max_t_history(previous_date(i)) 
        mean_running_average =  (1.0 - alpha) * sum(
            (alpha** (i-1) ) * int(t_history [str(i)]) for i in range(1,8)
            )
    else:
        mean_running_average = previous_mean_running_average

    upper_limit = 0.31 * mean_running_average + 21.3
    # Larger confort zone to avoid unnecessary cooling
    lower_limit = 0.31 * mean_running_average + 14.3 - 1

    return lower_limit, upper_limit, mean_running_average
    

def control(state, n_person, area, t_outdoor, co2, t_predicted, mean_running_average ):
    """ control instructions"""
    forecast = requests.get(
        "http://api.wunderground.com/api/0d2ebd8eea932783/forecast/q/CA/berkeley.json"
        ).json()
    next_day = forecast['forecast']['simpleforecast']['forecastday'][0]

    t_forecast_max = next_day['high']['celsius']

    # temperature setpoints
    lower_t_limit, upper_t_limit, mean_running_average  = acz(mean_running_average)

    hight_setpt = (lower_t_limit + 3*upper_t_limit) / 4
    center_setpt = (lower_t_limit + upper_t_limit) / 2
    low_setpt = (3*lower_t_limit + upper_t_limit) / 4
    hight_setpt=round(hight_setpt,1)
    center_setpt=round(center_setpt, 1)
    low_setpt=round(low_setpt,1)

    # ventillation setpoint
    ca_ = 0.06 # cfm/ft2
    cp_ = 5 # cfm/person
    zone_air_distribution_effectiveness = 1.0
    vent_min = (ca_ * area + cp_ * n_person) / zone_air_distribution_effectiveness
    vent_setpt = 5*vent_min #greater ventillation minimum to avoid overheating of the zone.

    # morning afternnon determination
    hour = time.strftime("%h")
    if hour < 12:
        am_pm = 'am'
    else:
        am_pm = 'pm'

    if state == 'not occupied':
        if mean_running_average > 15:
            vent = vent_setpt
            heat = 0
            setpt = upper_t_limit
            return   vent, heat, setpt, mean_running_average
        else:
            vent = vent_setpt
            heat = 1
            setpt = lower_t_limit
            return    vent, heat, setpt, mean_running_average
    if state == 'occupied':
        if co2 > 800:
            vent = vent_setpt*1.5
            heat = 0
            setpt = center_setpt
            return   vent, heat, setpt, mean_running_average
        if co2 <= 800:
            if t_predicted > upper_t_limit:
                vent = vent_setpt*1.5
                heat = 0
                setpt = center_setpt
                return  vent, heat, setpt, mean_running_average
            if t_predicted < lower_t_limit:
                vent = vent_setpt
                heat = 1
                setpt = low_setpt
                return  vent, heat, setpt, mean_running_average
            else:
                if mean_running_average <= 15:
                    if am_pm == 'am':
                        vent = vent_setpt
                        heat = 1
                        setpt = low_setpt
                        return   vent, heat, setpt, mean_running_average
                    if am_pm == 'pm':
                        vent = vent_setpt
                        heat = 1
                        setpt = center_setpt
                        return   vent, heat, setpt, mean_running_average
                if mean_running_average > 15:
                    if am_pm == 'am':
                        vent = vent_setpt
                        heat = 0
                        setpt = low_setpt
                        return   vent, heat, setpt, mean_running_average
                    if am_pm == 'pm':
                        vent = vent_setpt
                        heat = 0
                        setpt = center_setpt
                        return   vent, heat, setpt , mean_running_average    
    if state == 'slightly occupied':
        if ( (am_pm == 'pm') or ( (am_pm == 'am') and (t_forecast_max < 28) ) ):
            if mean_running_average > 15:
                if t_predicted > upper_t_limit:
                    vent = vent_setpt*1.5
                    heat = 0
                    setpt = center_setpt
                    return  vent, heat, setpt, mean_running_average
                if t_predicted < lower_t_limit:
                    vent = vent_setpt
                    heat = 0
                    setpt = low_setpt
                    return  vent, heat, setpt, mean_running_average
                else:
                    vent = vent_setpt
                    heat = 0
                    setpt = center_setpt
                    return  vent, heat, setpt, mean_running_average
            if mean_running_average <= 15:
                if t_predicted > upper_t_limit:
                    vent = vent_setpt
                    heat = 0
                    setpt = center_setpt
                    return  vent, heat, setpt, mean_running_average
                if t_predicted < lower_t_limit:
                    vent = vent_setpt
                    heat = 1
                    setpt = low_setpt
                    return   vent, heat, setpt, mean_running_average
                else:
                    vent = vent_setpt
                    heat = 1
                    setpt = center_setpt
                    return  vent, heat, setpt, mean_running_average
        else:
            vent = vent_setpt*1.5
            heat = 0
            setpt = center_setpt
            return   vent, heat, setpt, mean_running_average
