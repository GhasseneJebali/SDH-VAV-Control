#from smap.archiver.client import SmapClient
#from smap.contrib import dtutil
#from scipy.interpolate import interp1d
#import os
#import xlsxwriter
#import calendar
#import datetime
#import time
#import math
#import openpyxl
##
#
#import os
#print("Path at terminal when executing this file")
#import os
#print os.path.dirname(os.path.abspath(__file__))

from control import bacnet
        
db = '/smap/bacnet/db/db_sdh_8062015'
bacnet_interface = 'eth0'
bacnet_port = '47816'

bacnet_c = bacnet.BACnetController(db, bacnet_interface, bacnet_port) 

bacnet_c.write('SDH.S4-13:HEAT.COOL', 'SDH.PXCM-11', 1)
bacnet_c.write('SDH.S4-13:CTL STPT', 'SDH.PXCM-11', 74)    

#cfm_uuid1 = 'e4440358-c95e-5b3a-90b0-7318b1d1e06b' 
#setpt_uuid1 = '81cf0974-51fe-500d-b24a-04185b970f4f' 
#
#heat_uuid = 'ee1d5ac4-f992-51e1-9760-ad204f53c4ca'
#
#
#
#day0 = '6-1-2014'
#day1 = '8-30-2014'
#timestep=15 # timestep in minutes
#
################################################################################    
## make a client
#client = SmapClient("http://www.openbms.org/backend")
#
## start and end values are Unix timestamps
#start = dtutil.dt2ts(dtutil.strptime_tz(day0, "%m-%d-%Y"))
#end   = dtutil.dt2ts(dtutil.strptime_tz(day1, "%m-%d-%Y")) 
#
##air_flow_data1 = client.data_uuid([air_flow_uuid], start, end, cache=True)[0]
##light_data1 = client.data_uuid([light_uuid1], start, end, cache=True)[0]
##recep_data1 = client.data_uuid([recep_uuid1], start, end, cache=True)[0]
#cfm_data1 = client.data_uuid([cfm_uuid1], start, end, cache=False)[0]
#setpt_sat_data1 = client.data_uuid([setpt_uuid1], start, end, cache=False)[0]
#heat_data1 = client.data_uuid([heat_uuid], start, end, cache=False)[0]
#
#
#
#imposed_time=[]
#x = 1402556996000
#limit = 1408903796000
#while x <= limit:
#    imposed_time.append(x)
#    x += timestep*60*1000
#    
#def interpole(data, t):
#    time1 = [item[0] for item in data]
#    value1= [item[1] for item in data]
#    data_synchro = interp1d(time1,value1)(t)
#    data_synchro = [i for i in data_synchro]
#    return data_synchro
#
## interpolate temperature setpoint data
#
##recep_data=interpole(recep_data1, imposed_time)
##light_data=interpole(light_data1, imposed_time)
##air_flow_data=interpole(air_flow_data1, imposed_time)
#cfm_data=interpole(cfm_data1, imposed_time)
#setpt_sat_data=interpole(setpt_sat_data1, imposed_time)
#heat_data=interpole(heat_data1, imposed_time)
#
#for i in range(len(setpt_sat_data)):
#    setpt_sat_data[i]= (setpt_sat_data[i]-30)*5/9
#
#
#DATA_LIST={'Timestamp':imposed_time, 'cfm':cfm_data, 'setpt':setpt_sat_data, 'heat':heat_data}
#    
#    
#workbook = xlsxwriter.Workbook('Energy_simulation.xlsx')
#worksheet = workbook.add_worksheet()
#col=0
#for keys in DATA_LIST.keys():    
#    worksheet.write(0, col , keys)
#    col=col+1
#col=0
#for data in DATA_LIST.values():
#    row=1    
#    for value in data:
#            worksheet.write(row, col , value)
#            row += 1
#    col=col+1
#workbook.close()

#
#
#from sklearn.svm import SVR
#from sklearn import neighbors
#from sklearn import linear_model
#import matplotlib.pyplot as plt
#
#
#def Support_Vector_Regression(data, Prediction_horizon):  
################################################################################
#    # Import data
#    print '####################################################'
#    print 'Support Vector Regression start....'  
#    X=[]
#    y=[]
#    X_train=[] 
#    X_valid=[]
#    y_train=[] 
#    y_valid=[] 
#    for i in range(len(data['Temperature'])-4):
#        X.append([data['Temperature'][i] , data['H/C power'][i], data['Setpoint Temperature'][i], data['Outdoor Temperature'][i], data['Calendar data'][i], data['Human_power'][i]])
#        y.append( data['Temperature'][i+4])
#    X_train=X[:6000]
#    X_valid=X[6000:]
#    y_train=y[:6000]
#    y_valid=y[6000:]
#
################################################################################
#    # Fit regression model
#    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
#
#    y_rbf = svr_rbf.fit(X_train, y_train)
#    
#    result=[]
#    error=[]
#    for i in range(len(X_valid)):
#        result.append(y_rbf.predict(X_valid[i]))
#        error.append(abs(result[i]-y_valid[i]))
#    me=[]
#    for i in range(len(X_valid)):
#
#        me.append(abs(result[i]-y_valid[i])**2)
################################################################################       
#    # Calculate the performance of the algorithm    
#    Mean_error= sum(error)/len(error)
#    RMSE= math.sqrt(sum(me)/len(me)) 
#    Max_error= max(error)
#    big_error=0.
#    for e in error:
#        if e>0.2:
#            big_error=big_error+1.
#    big_error=(big_error/float(len(error)))*100
#    print    
#    print 'Mean error : ' + str(Mean_error[0]) + ' C'
#    print 'RMSE : ' + str(RMSE)
#    print 'Max error : ' + str(Max_error[0]) + ' C'
#    print 'Large error : ' + str(big_error) + ' %'     
#    plt.figure(1)    
#    plt.plot(result)
#    plt.plot(y_valid, 'r')
#    plt.title('Support Vector Regression(C)')
#    plt.xlabel('Time')
#    plt.ylabel('T (C)')
#    plt.legend()    
#    plt.show()
#    print
#    plt.figure(2)  
#    plt.plot(error)
#    plt.title('Error')
#    plt.xlabel('Time')
#    plt.ylabel('Error (C)')
#    plt.legend()
#    plt.show()
#    
#    print 'Support Vector Regression end.'  
#    print '####################################################'
#    print
#
################################################################################
#
#
#
#
################################################################################
#def kNN_Regression(data, Prediction_horizon): 
################################################################################
#    # Import data
#    print '####################################################'
#    print 'K Nearest Neighbors Regression start....'      
#    X=[]
#    y=[]
#    X_train=[] 
#    X_valid=[]
#    y_train=[] 
#    y_valid=[] 
#    for i in range(len(data['Temperature'])-4):
#        X.append([data['Temperature'][i] , data['H/C power'][i], data['Setpoint Temperature'][i], data['Outdoor Temperature'][i], data['Calendar data'][i], data['Human_power'][i]])
#        y.append( data['Temperature'][i+4])
#    X_train=X[:6000]
#    X_valid=X[6000:]
#    y_train=y[:6000]
#    y_valid=y[6000:]
################################################################################
#    # Fit regression model
#    n_neighbors = 5
#    knn = neighbors.KNeighborsRegressor(n_neighbors, weights= 'distance')
#    
#    y_kNN = knn.fit(X_train, y_train)
#    
#    result=[]
#    error=[]
#    for i in range(len(X_valid)):
#        result.append(y_kNN.predict(X_valid[i]))
#        error.append(abs(result[i]-y_valid[i]))
#    me=[]
#    for i in range(len(X_valid)):
#
#        me.append(abs(result[i]-y_valid[i])**2)
#        
#        
################################################################################       
#    # Calculate the performance of the algorithm    
#    Mean_error= sum(error)/len(error)
#    RMSE= math.sqrt(sum(me)/len(me))    
#    
#    Max_error= max(error)
#    big_error=0.
#    for e in error:
#        if e>0.2:
#            big_error=big_error+1.
#    big_error=(big_error/float(len(error)))*100
#    print    
#    print 'Mean error : ' + str(Mean_error[0]) + ' C'
#    print 'Max error : ' + str(Max_error[0]) + ' C'
#    print 'RMSE : ' + str(RMSE)
#    print 'Large error : ' + str(big_error) + ' %'     
#    plt.figure(1)    
#    plt.plot(result)
#    plt.plot(y_valid, 'r')
#    plt.title('K-Nearest Neighbors Regression')
#    plt.xlabel('Time')
#    plt.ylabel('T (C)')
#    plt.legend()   
#    plt.show()
#    print
#    plt.figure(2)  
#    plt.plot(error)
#    plt.title('Error')
#    plt.xlabel('Time')
#    plt.ylabel('Error (C)')
#    plt.legend()
#    plt.show()
#    
#    print 'K Nearest Neighbors Regression end.'  
#    print '####################################################'
#    print
#
################################################################################
#
#
################################################################################
#def Bayesian_Ridge_Regression(data, Prediction_horizon): 
################################################################################
#    # Import data
#    print '####################################################'
#    print 'Bayesian Ridge Regression start....'    
#    X=[]
#    y=[]
#    X_train=[] 
#    X_valid=[]
#    y_train=[] 
#    y_valid=[] 
#    for i in range(len(data['Temperature'])-4):
#        X.append([data['Temperature'][i] , data['H/C power'][i], data['Setpoint Temperature'][i], data['Outdoor Temperature'][i], data['Calendar data'][i], data['Human_power'][i]])
#        y.append( data['Temperature'][i+4])
#    X_train=X[:6000]
#    X_valid=X[6000:]
#    y_train=y[:6000]
#    y_valid=y[6000:]
#    
################################################################################
#    # Fit regression model
#    clf = linear_model.BayesianRidge()
#    
#    clf.fit(X_train, y_train)
#    
#    result=[]
#    error=[]
#    for i in range(len(X_valid)):
#        result.append(clf.predict (X_valid[i]))
#        error.append(abs(result[i]-y_valid[i]))
#    me=[]
#    for i in range(len(X_valid)):
#        
#        me.append(abs(result[i]-y_valid[i])**2)
#    print len(X_valid)
#    print len(result)
################################################################################       
#    # Calculate the performance of the algorithm    
#    Mean_error= sum(error)/len(error)
#    RMSE= math.sqrt(sum(me)/len(me)) 
#    Max_error= max(error)
#    big_error=0.
#    for e in error:
#        if e>0.2:
#            big_error=big_error+1.
#    big_error=(big_error/float(len(error)))*100
#    print
#    print clf.coef_
#    print 'Mean error : ' + str(Mean_error[0]) + ' C'
#    print 'RMSE : ' + str(RMSE)
#    print 'Max error : ' + str(Max_error[0]) + ' C'
#    print 'Large error : ' + str(big_error) + ' %'     
#    plt.figure(1)    
#    plt.plot(result)
#    plt.plot(y_valid, 'r')
#    plt.title('Bayesian Ridge Regression')
#    plt.xlabel('Time')
#    plt.ylabel('T (C)')
#    plt.legend()
#    plt.show()
#    print
#    plt.figure(2)  
#    plt.plot(error)
#    plt.title('Error')
#    plt.xlabel('Time')
#    plt.ylabel('Error (C)')
#    plt.legend()
#    plt.show()
#    
#    print 'Bayesian Ridge Regression end.'  
#    print '####################################################'
#    print
#
################################################################################
#
#DATA_LIST={}
#wb = openpyxl.load_workbook('DATA_LIST.xlsx')
#sheet = wb.get_sheet_by_name('Sheet1')
#for key in range(1, sheet.max_column+1):
#    DATA_LIST[sheet.cell(row=1, column=key).value]=[]
#    for v in range(2, sheet.max_row+1):
#        DATA_LIST[sheet.cell(row=1, column=key).value].append(sheet.cell(row=v, column=key).value)
#
#Support_Vector_Regression(DATA_LIST ,4) 
#kNN_Regression(DATA_LIST ,4) 
#Bayesian_Ridge_Regression(DATA_LIST ,4)                   