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

classes = {'Bacillariophyceae': {'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Chlorophyceae': {'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Coscinodiscophyceae': {'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Cryptophyceae': {'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Cyanophyceae': {'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Dinophyceae': {'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Fragilariophyceae': {'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Pelagophyceae': {'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Prasinophyceae': {'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Prymnesiophyceae': {'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Raphidophyceae': {'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Rhodophyceae': {'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Haptophyceae': {'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},          
           'Eustigmatophyceae': {'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]} 
           }

def get_classes(classes,data,p):
    for phyto in data:
        c = data[phyto]['class']
        for sname in data[phyto][p].index:
            info = sname.split('_')
            classes[c]['vg'].append(float(info[0]))
            classes[c]['ci'].append(float(info[1]))
            classes[c]['nshell'].append(float(info[2]))
            if len(info) == 4:
                classes[c]['deff'].append(float(info[3]))
            else:
                classes[c]['deff'].append(float(info[4]))
            classes[c]['data'].append(data[phyto][p].loc[sname,:])
    return classes

p = 'bb'
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
    classes[cl]['struth'].append(info[p])

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
    # if gi in ['Eustigmatophyceae']:
    #     continue
    classes[gi]['vtruth'].append(gd.iloc[:,2:].values)


# concat data groups
for c in classes:
    classes[c]['data'] = pd.concat(classes[c]['data'],axis=1).T
    
# concat truth groups
for c in classes:
    if len(classes[c]['vtruth']): 
        if p == 'bb':
            col = l3
        else:
            col = l2
        classes[c]['vtruth'] = pd.DataFrame(np.vstack((classes[c]['vtruth'])),columns=col)

for c in classes:
    if len(classes[c]['struth']):
        classes[c]['struth'] = pd.DataFrame(np.vstack((classes[c]['struth'])),columns=l2)

    
    
#%%

fig, axs = plt.subplots(4,4,figsize=(20,20))
axs = axs.ravel()
count = 0

if p in ['a','b']:
    for c in classes:
        print (c)
        res = sm.graphics.fboxplot(classes[c]['data'].values, l1, wfactor=1000, ax=axs[count])
        if not isinstance(classes[c]['vtruth'], list):    
            classes[c]['vtruth'].T.plot(ax=axs[count],color='b',legend=False)
        if not isinstance(classes[c]['struth'], list):
            classes[c]['struth'].T.plot(ax=axs[count],color='r',legend=False)
        axs[count].set_title(c)
        if p == 'b':
            axs[count].set_ylim(0,.7)
        else:
            axs[count].set_ylim(0,.1)
        axs[count].set_xlim(400,800)
        count = count+1
        
else:
    for c in classes:
        print (c)
        res = sm.graphics.fboxplot(classes[c]['data'].values, l1, wfactor=1000, ax=axs[count])
        if not isinstance(classes[c]['vtruth'], list):    
            classes[c]['vtruth'].T.plot(ax=axs[count],color='b',ls='--',marker='s', legend=False)
        if not isinstance(classes[c]['struth'], list):
            classes[c]['struth'].T.plot(ax=axs[count],color='r',legend=False)
        axs[count].set_title(c)
        #axs[count].set_ylim(0,.1)
        axs[count].set_xlim(400,800)
        count = count+1   
    
    
fig.savefig('/Users/jakravit/Desktop/{}.png'.format(p),bbox_inches='tight',dpi=300)


#%%
fig, axs = plt.subplots(1,4, figsize=(15,7),sharey=True)
axs = axs.ravel()
for i,v in enumerate(['deff','ci','vg','nshell']):
    df = {}
    for c in classes:
        df[c] = classes[c][v]    
    axs[i].boxplot(df.values(),vert=False,whis=1.5)
axs[0].set_yticks(range(1,len(df.keys())+1))
axs[0].set_yticklabels(df.keys())
axs[0].set_xlabel(u'Deff (\u03bcm)')
axs[1].set_xlabel('Ci (kgm$^{-3}$)')
axs[2].set_xlabel('Vg (%)')
axs[3].set_xlabel('n_shell')
plt.subplots_adjust(wspace=.1)
fig.savefig('/Users/jakravit/Desktop/2layer_params.png',bbox_inches='tight',dpi=300)


