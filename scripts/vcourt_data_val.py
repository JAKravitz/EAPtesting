#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 13:44:50 2021

@author: jakravit
"""
#%% vaillancourt data validation

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import statsmodels.api as sm
import random

phyto = 'Nannochloropsis sp.'
clas = 'Eustigmatophyceae'
with open('/Users/jakravit/Desktop/phyto_optics/eap_test/{}.p'.format(phyto), 'rb') as fp:
    data = pickle.load(fp)  


l1 = np.arange(400,905,5)
l2 = np.arange(400,901,1)
l3 = np.array([440,470,510,620])

# combine runs
def combine(data,p,l):
    newnames = []
    runs = []
    for sname in data:
        s = data[sname][p] 
        for deff in s.index:
            runs.append(s.loc[deff,:])
            newname = sname + '_{}'.format(deff)
            newnames.append(newname)
    runs = pd.concat(runs,axis=1,).T
    runs.index = newnames
    runs.columns = l    
    return runs

runs = {
        'a' : combine(data,'a',l1),
        'b' : combine(data,'b',l1),
        'bb' : combine(data,'bb',l1),
        'Qa' : combine(data,'Qa',l1),
        'Qb' : combine(data,'Qb',l1),
        'Qbb' : combine(data,'Qbb',l1)
        }
print (runs['a'].shape[0])


# validation data
path = '/Users/jakravit/Desktop/phyto_optics/Vaillancourt/'
val = {'a': pd.read_csv(path + 'smooth/a_smooth.csv'),
       'b': pd.read_csv(path + 'smooth/b_smooth.csv'),
       'c': pd.read_csv(path + 'smooth/c_smooth.csv'),
       'bb':pd.read_csv(path + 'bb.csv'),
       'Qa': pd.read_csv(path + 'smooth/Qa_smooth.csv'),
       'Qb':pd.read_csv(path + 'smooth/Qb_smooth.csv'),
       'Qc':pd.read_csv(path + 'smooth/Qc_smooth.csv'),
       'Qbb':pd.read_csv(path + 'Qbb.csv'),
       }


fig, axs = plt.subplots(2,3,figsize=(20,10))
axs = axs.ravel()
for i,p in enumerate(runs):
    param = val[p]
    sparam = param[param['Species'] == phyto]
    runs[p].T.plot(ax=axs[i], legend=False)
    if p not in ['bb','Qbb']:
        axs[i].plot(l2,sparam.iloc[:,2:].T.values,color='b',lw=3)
    else:
        axs[i].plot(l3,sparam.iloc[:,2:].T.values, c='b', marker='s', ls='--', lw=3,) 
    axs[i].grid()
    

#%% Get smaller range according to in-situ spectra

p = 'b'
a = runs[p]   
a = a[(a.loc[:,675] > .3) & (a.loc[:,675] < .5)]
#check = check[(check.loc[:,400] > .04) & (check.loc[:,400] < .2)]
#a = a[a.loc[:,400] < .12]
fig, ax = plt.subplots()
param = val[p]
sparam = param[param['Species'] == phyto]
a.T.plot(ax=ax,legend=False)
ax.plot(l2,sparam.iloc[:,2:].T.values,color='b')
ax.grid()
print (a.shape[0])

#%%
idx = a.index
a = runs['a'].loc[idx,:]
b = runs['b'].loc[idx,:]
bb = runs['bb'].loc[idx,:]

fig, axs = plt.subplots(1,3,figsize=(20,5))
axs = axs.ravel()
# a
param = val['a']
sparam = param[param['Species'] == phyto]
a.T.plot(ax=axs[0],legend=False)
axs[0].plot(l2,sparam.iloc[:,2:].T.values,color='b',lw=3)
# b
param = val['b']
sparam = param[param['Species'] == phyto]
b.T.plot(ax=axs[1],legend=False)
axs[1].plot(l2,sparam.iloc[:,2:].T.values,color='b',lw=3)
# bb
param = val['bb']
sparam = param[param['Species'] == phyto]
bb.T.plot(ax=axs[2],legend=False)
axs[2].plot(l3,sparam.iloc[:,2:].T.values, c='b', marker='s', ls='--', lw=3)


run = {'a':a,
       'b':b,
       'bb':bb,
       'species':phyto,
       'class':clas}

#%%
path = '/Users/jakravit/Desktop/nasa_npp/EAP/vcourt_final/'
with open(path + '{}.p'.format(phyto), 'wb') as fp:
    pickle.dump(run,fp)  

#%%
# fpath = '/Users/jakravit/Desktop/nasa_npp/EAP/vcourt_final/Pavlova sp..p'
# with open(fpath, 'rb') as fp:
#     foo = pickle.load(fp)

