#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 17:08:35 2021

@author: jakravit
"""
import os
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import statsmodels.api as sm

strampath = '/Users/jakravit/Desktop/nasa_npp/EAP/stramski_final/'
vcourtpath = '/Users/jakravit/Desktop/nasa_npp/EAP/vcourt_final/'

stramlist = os.listdir(strampath)
vcourtlist = os.listdir(vcourtpath)

def get_phytos(plist,ppath):    
    phytos = {}
    for phy in plist:
        if phy.startswith('.'):
            continue
        fpath = ppath + phy
        with open(fpath, 'rb') as fp:
            data = pickle.load(fp)
            phytos[phy] = data
    return phytos

stramphy = get_phytos(stramlist, strampath)
vcourtphy = get_phytos(vcourtlist, vcourtpath)

#%%
l1 = np.arange(400,905,5)
l2 = np.arange(400,901,1)
l3 = np.array([440,470,510,620])

classes = {'Bacillariophyceae': {'truth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Chlorophyceae': {'truth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Coscinodiscophyceae': {'truth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Cryptophyceae': {'truth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Cyanophyceae': {'truth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Dinophyceae': {'truth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Fragilariophyceae': {'truth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Pelagophyceae': {'truth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Prasinophyceae': {'truth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Prymnesiophyceae': {'truth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Raphidophyceae': {'truth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Rhodophyceae': {'truth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Haptophyceae': {'truth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]}          
           }

def get_classes(classes,data,p):
    for phyto in data:
        c = data[phyto]['class']
        for sname in data[phyto][p].index:
            info = sname.split('_')
            classes[c]['vg'].append(float(info[0]))
            classes[c]['ci'].append(float(info[1]))
            classes[c]['nshell'].append(float(info[2]))
            classes[c]['deff'].append(float(info[3]))
            classes[c]['data'].append(data[phyto][p].loc[sname,:])
    return classes

p = 'b'
classes = get_classes(classes,stramphy,p)
classes = get_classes(classes,vcourtphy,p)


# stramski validation data
with open('/Users/jakravit/Desktop/nasa_npp/EAP/phyto_optics/dariusz/optics.p', 'rb') as fp:
    stram_val = pickle.load(fp) 

for code in stram_val:
    if code in ['hbac','viru']:
        continue
    info = stram_val[code]
    cl = info['Class']
    classes[cl]['truth'].append(info[p])

# vcourt validation data
path = '/Users/jakravit/Desktop/nasa_npp/EAP/phyto_optics/Vaillancourt/'
court_val = {'a': pd.read_csv(path + 'smooth/a_smooth.csv'),
             'b': pd.read_csv(path + 'smooth/b_smooth.csv'),
             'c': pd.read_csv(path + 'smooth/c_smooth.csv'),
             'bb':pd.read_csv(path + 'bb.csv'),
             'Qa': pd.read_csv(path + 'smooth/Qa_smooth.csv'),
             'Qb':pd.read_csv(path + 'smooth/Qb_smooth.csv'),
             'Qc':pd.read_csv(path + 'smooth/Qc_smooth.csv'),
             'Qbb':pd.read_csv(path + 'Qbb.csv'),
             }

vdata = court_val[p]
groups = vdata.groupby('Class')
for gi,gd in groups:
    if gi in ['Eustigmatophyceae']:
        continue
    classes[gi]['truth'].append(gd.iloc[:,2:].values)


# concat data groups
for c in classes:
    classes[c]['data'] = pd.concat(classes[c]['data'],axis=1).T
    
# concat truth groups
# for c in classes:
#     classes[c]['truth'] = np.vstack((classes[c]['truth']))
for c in classes:
    classes[c]['truth'] = pd.DataFrame(np.vstack((classes[c]['truth'])),columns=l2)
    
#%%

fig, axs = plt.subplots(4,4,figsize=(20,20))
axs = axs.ravel()
count = 0
for c in classes:
    print (c)
    res = sm.graphics.fboxplot(classes[c]['data'].values, l1, wfactor=50, ax=axs[count])
    classes[c]['truth'].T.plot(ax=axs[count],legend=False)
    axs[count].set_title(c)

    count = count+1
#fig.savefig('/Users/jkravz311/Desktop/bb_fda.png',bbox_inches='tight',dpi=300)




