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

strampath = '/Users/jakravit/git/EAP/data/final_ranges/stramski/'
vcourtpath = '/Users/jakravit/git/EAP/data/final_ranges/vcourt/'

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
# lac9 = np.array([412,440,488,510,532,555,620,650,676,715])
# lhs6 = np.array([442,488,532,555,620,676])

classes = {'Bacillariophyceae': {'wtruth':[],'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Chlorophyceae': {'wtruth':[],'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Coscinodiscophyceae': {'wtruth':[],'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Cryptophyceae': {'wtruth':[],'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Cyanophyceae': {'wtruth':[],'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Dinophyceae': {'wtruth':[],'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Fragilariophyceae': {'wtruth':[],'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Pelagophyceae': {'wtruth':[],'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Prasinophyceae': {'wtruth':[],'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Prymnesiophyceae': {'wtruth':[],'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Raphidophyceae': {'wtruth':[],'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Rhodophyceae': {'wtruth':[],'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},
           'Haptophyceae': {'wtruth':[],'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]},          
           'Eustigmatophyceae': {'wtruth':[],'struth':[],'vtruth':[],'data':[],'vg':[],'ci':[],'nshell':[],'deff':[]} 
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
with open('/Users/jakravit/git/EAP/data/val/stram_optics.p', 'rb') as fp:
    stram_val = pickle.load(fp) 
for code in stram_val:
    if code in ['hbac','viru']:
        continue
    info = stram_val[code]
    cl = info['Class']
    classes[cl]['struth'].append(info[p])

# vcourt validation data
path = '/Users/jakravit/git/EAP/data/val/'
court_val = {'a': pd.read_csv(path + 'vcourt_a.csv'),
             'b': pd.read_csv(path + 'vcourt_b.csv'),
             'bb':pd.read_csv(path + 'vcourt_bb.csv'),
             }
vdata = court_val[p]
groups = vdata.groupby('Class')
for gi,gd in groups:
    # if gi in ['Eustigmatophyceae']:
    #     continue
    classes[gi]['vtruth'].append(gd.iloc[:,2:].values)

# whitmire validation data
# path = '/Users/jakravit/git/EAP/data/val/'
# whit_val = {'a': pd.read_csv(path + 'whit_a_subset.csv'),
#              'b': pd.read_csv(path + 'whit_b_subset.csv'),
#              'bb':pd.read_csv(path + 'whit_bb_subset.csv'),
#              }
# wdata = whit_val[p]
# groups = wdata.groupby('Class')
# for gi,gd in groups:
#     classes[gi]['wtruth'] = gd.iloc[:,4:].div(gd.Chl,axis=0)

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

# for c in classes:
#     if len(classes[c]['wtruth']): 
#         if p == 'bb':
#             col = lhs6
#         else:
#             col = lac9
#         classes[c]['wtruth'].columns = col
    
#%%
import matplotlib.pylab as pylab
params = {'legend.fontsize': 'small',
          'axes.labelsize': 18,
          'axes.titlesize': 24,
          'xtick.labelsize': 13,
          'ytick.labelsize': 13
          }
pylab.rcParams.update(params)

fig, axs = plt.subplots(4,4,figsize=(20,20), sharex=True, sharey=True)
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
        # if not isinstance(classes[c]['wtruth'], list):
        #     classes[c]['wtruth'].T.plot(ax=axs[count],color='g',ls='--',marker='o',legend=False)
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
            classes[c]['vtruth'].T.plot(ax=axs[count],color='b',ls='--',marker='o', legend=False)
        if not isinstance(classes[c]['struth'], list):
            classes[c]['struth'].T.plot(ax=axs[count],color='r',legend=False)
        # if not isinstance(classes[c]['wtruth'], list):
        #     classes[c]['wtruth'].T.plot(ax=axs[count],color='g',ls='--',marker='o',legend=False)
        axs[count].set_title(c)
        axs[count].set_ylim(0,.01)
        axs[count].set_xlim(400,800)
        count = count+1   
    
plt.subplots_adjust(hspace=.2,wspace=.1)
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


