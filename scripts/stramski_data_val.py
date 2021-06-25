#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 16:23:04 2021

@author: jakravit
"""
#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from src.EAP_proc import EAP
import pickle
import statsmodels.api as sm
import random


clas = 'Rhodophyceae'
phyto = 'P. cruentum' 
code = 'crue'

with open('/Users/jakravit/git/EAP/data/val/stram_optics.p', 'rb') as fp:
    val = pickle.load(fp)  

# with open('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/stramski_optics1.p'.format(phyto), 'rb') as fp:
#     data = pickle.load(fp)  
with open('/Users/jakravit/Desktop/nasa_npp/EAP/stramski_2layers/{}.p'.format(phyto), 'rb') as fp:
    data = pickle.load(fp)   

l1 = np.arange(400,905,5)
l2 = np.arange(400,901,1)

# combine runs
def combine(data,p,l):
    newnames = []
    runs = []
    for sname in data:
        s = data[sname][p] 
        for deff in s.index:
            runs.append(s.loc[deff,:])
            newname = sname + '_{0:.2f}'.format(deff)
            newnames.append(newname)
    runs = pd.concat(runs,axis=1,).T
    runs.index = newnames
    runs.columns = l    
    return runs

runs = {
        'a' : combine(data,'a',l1),
        'b' : combine(data,'b',l1),
        'bb' : combine(data,'bb',l1),
        }

print (runs['a'].shape[0])

fig, axs = plt.subplots(1,3,figsize=(20,5))
axs = axs.ravel()
for i, p in enumerate(runs):
    sparam = val[code][p]
    runs[p].T.plot(ax=axs[i], legend=False)
    axs[i].plot(l2,sparam, c='b',lw=3)
    axs[i].grid()

runs['class'] = clas
runs['species'] = phyto

#%% Get smaller range according to in-situ spectra

p = 'b'
a = runs[p]   
a = a[(a.loc[:,675] > .03) & (a.loc[:,675] < .035)]
#a = a[(a.loc[:,400] > .04) & (a.loc[:,400] < .05)]
#a = a[a.loc[:,400] < .4]
fig, ax = plt.subplots()
sparam = val[code][p]
a.T.plot(ax=ax,legend=False)
ax.plot(l2,sparam, c='b',lw=3)
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
sparam = val[code]['a']
a.T.plot(ax=axs[0],legend=False)
axs[0].plot(l2,sparam, c='b',lw=3)
# b
sparam = val[code]['b']
b.T.plot(ax=axs[1],legend=False)
axs[1].plot(l2,sparam, c='b',lw=3)
# bb
sparam = val[code]['bb']
bb.T.plot(ax=axs[2],legend=False)
axs[2].plot(l2,sparam, c='b',lw=3)

run = {'a':a,
       'b':b,
       'bb':bb,
       'species':phyto,
       'class':clas}


#%%
path = '/Users/jakravit/Desktop/nasa_npp/EAP/stramski_final/'
with open(path + '{}.p'.format(phyto), 'wb') as fp:
    pickle.dump(run,fp)  