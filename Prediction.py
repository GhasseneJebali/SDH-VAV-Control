# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 10:06:19 2016

@author: Ghassene Jebali jbali.ghassen@gmail.com
"""

from sklearn.svm import SVR
from sklearn import neighbors
from sklearn import linear_model
#import matplotlib.pyplot as plt



###############################################################################
def Data_Validation(data, X):
###############################################################################
    valid=1    
    upper={}
    lower={}    
    for k in data.keys():
        upper[k]=max(data[k])
        lower[k]=min(data[k])
    if (X[0]<lower['Temperature']*0.75) or (X[0]>upper['Temperature']*1.25):
        valid=0
    if (X[1]<lower['H/C power']*0.75) or (X[1]>upper['H/C power']*1.25):
        valid=0
    if (X[2]<lower['Setpoint Temperature']*0.75) or (X[2]>upper['Setpoint Temperature']*1.25):
        valid=0
    if (X[3]<lower['Outdoor Temperature']*0.75) or (X[3]>upper['Outdoor Temperature']*1.25):
        valid=0
    if (X[4]<lower['Calendar data']*0.75) or (X[4]>upper['Calendar data']*1.25):
        valid=0
    return valid



###############################################################################
def Support_Vector_Regression(data, Prediction_horizon):  
###############################################################################

    X=[]
    y=[]
    X_train=[] 
    X_valid=[]
    y_train=[] 
    y_valid=[] 
    for i in range(len(data['Temperature'])-int(Prediction_horizon/15)):
        X.append([data['Temperature'][i] , data['H/C power'][i], data['Setpoint Temperature'][i], data['Outdoor Temperature'][i], data['Calendar data'][i], data['Human_power'][i]])
        y.append( data['Temperature'][i+int(Prediction_horizon/15)])
    X_train=X[:6000]
    X_valid=X[6000:]
    y_train=y[:6000]
    y_valid=y[6000:]

###############################################################################
    # Fit regression model
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)

    y_rbf = svr_rbf.fit(X_train, y_train)
    
    result=[]
    error=[]
    for i in range(len(X_valid)):
        result.append(y_rbf.predict(X_valid[i]))
        error.append(abs(result[i]-y_valid[i]))
        
###############################################################################       
    # Calculate the performance of the algorithm    
#    Mean_error= sum(error)/len(error)
#    Max_error= max(error)
#    big_error=0.
#    for e in error:
#        if e>0.2:
#            big_error=big_error+1.
#    big_error=(big_error/float(len(error)))*100
#    print    
#    print 'Mean error : ' + str(Mean_error[0]) + ' C'
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
    return y_rbf
###############################################################################




###############################################################################
def kNN_Regression(data, Prediction_horizon): 
###############################################################################
     
    X=[]
    y=[]
    X_train=[] 
    X_valid=[]
    y_train=[] 
    y_valid=[] 
    for i in range(len(data['Temperature'])-int(Prediction_horizon/15)):
        X.append([data['Temperature'][i] , data['H/C power'][i], data['Setpoint Temperature'][i], data['Outdoor Temperature'][i], data['Calendar data'][i], data['Human_power'][i]])
        y.append( data['Temperature'][i+int(Prediction_horizon/15)])
    X_train=X[:6000]
    X_valid=X[6000:]
    y_train=y[:6000]
    y_valid=y[6000:]
###############################################################################
    # Fit regression model
    n_neighbors = 5
    knn = neighbors.KNeighborsRegressor(n_neighbors, weights= 'distance')
    
    y_kNN = knn.fit(X_train, y_train)
    
    result=[]
    error=[]
    for i in range(len(X_valid)):
        result.append(y_kNN.predict(X_valid[i]))
        error.append(abs(result[i]-y_valid[i]))
        
    return y_kNN
###############################################################################


###############################################################################
def Bayesian_Ridge_Regression(data, Prediction_horizon): 
###############################################################################
   
    X=[]
    y=[]
    X_train=[] 
    X_valid=[]
    y_train=[] 
    y_valid=[] 
    for i in range(len(data['Temperature'])-int(Prediction_horizon/15)):
        X.append([data['Temperature'][i] , data['H/C power'][i], data['Setpoint Temperature'][i], data['Outdoor Temperature'][i], data['Calendar data'][i], data['Human_power'][i]])
        y.append( data['Temperature'][i+int(Prediction_horizon/15)])
    X_train=X[:6000]
    X_valid=X[6000:]
    y_train=y[:6000]
    y_valid=y[6000:]
###############################################################################
    # Fit regression model
    clf = linear_model.BayesianRidge()
    
    clf.fit(X_train, y_train)
    
    result=[]
    error=[]
    for i in range(len(X_valid)):
        result.append(clf.predict (X_valid[i]))
        error.append(abs(result[i]-y_valid[i]))
        
    return clf
###############################################################################


###############################################################################
def T_prediciton(data, X , model):    
###############################################################################  
    if Data_Validation(data, X):
        T = model.predict(X)[0]
    else:
        T = X[0]
        print 'Input data is invalid or may be outside boundaries'
    return T
###############################################################################


###############################################################################
def occupancy(state, cal, h, co2):
###############################################################################
    if state=='start':
        if cal==2 and h<17 and h>=10:
            state='occupied'
            Human_power=3.0
            number=30
            return state, Human_power, number
        if cal==2 and ((h<10 and h>=7) or (h<19 and h>=17)):
            state='slightly occupied'
            Human_power=1.5
            number=15
            return state, Human_power, number
        else:
            state='not occupied'
            Human_power=0.0
            number=0
            return state, Human_power, number
    if state=='not occupied':
        if cal==1 or cal==0:
            state='not occupied'
            Human_power=0.0
            number=0
            return state, Human_power, number
        else:
            state='slightly occupied'
            Human_power=1.5
            number=15
            return state, Human_power, number
    if state=='slightly occupied':
        if (cal==2 and h<17 and h>=10) or co2>500:
            state='occupied'
            Human_power=3.0
            number=30
            return state, Human_power, number
        if cal==0 or cal==1:
            state='not occupied'
            Human_power=0.0
            number=0
            return state, Human_power, number
        else:
            state='slightly occupied'
            Human_power=1.5
            number=15
            return state, Human_power, number
    if state=='occupied':
        if (cal==2 and h<17 and h>=10) or co2>500:
            state='occupied'
            Human_power=3.0
            number=30
            return state, Human_power, number
        else:
            state='slightly occupied'
            Human_power=1.5
            number=15
            return state, Human_power, number
            
###############################################################################