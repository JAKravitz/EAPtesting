#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run single phyto species using EAP for plot and validation against in-situ 

@author: jkravz311
"""
#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.EAP_proc import EAP
import pickle
import statsmodels.api as sm
import random


phyto = 'G. simplex' 
#code = 'parv'
mf = '/Users/jkravz311/git/EAP/data/501nm_extended_e1701000.mat'
astarpath = '/Users/jkravz311/git/EAP/data/in_vivo_phyto_abs.csv'
batchinfo = pd.read_csv('/Users/jkravz311/git/EAP/data/vcourt_batch_F.csv', index_col=0)

params = {'Vs1': np.arange(0.04,0.26,0.02), # small
          'Vs2': np.arange(0.2,0.4,0.02), # medium
          'Vs3': np.arange(0.4,0.6,0.02), # large
          'VsX': np.arange(0.04,0.6,0.02),
          'Ci1': np.arange(.1e6,2.2e6,.2e6), # low
          'Ci2': np.arange(2e6,7.5e6,.5e6), # med
          'Ci3': np.arange(7e6,12e6,.5e6), # high
          'CiX': np.arange(.1e6,12e6,.5e6),
          'nshell1': np.arange(1.06,1.12,.01), # low 
          'nshell2': np.arange(1.12, 1.17,.01), # med
          'nshell3': np.arange(1.17, 1.23,.01), # high
          'nshellX': np.arange(1.06, 1.23,.01),
          'ncore1': np.arange(1.014, 1.027, 0.005), # low
          'ncore2': np.arange(1.027, 1.04, 0.005), # hig
          'ncoreX': np.arange(1.014, 1.04, 0.005)
          }


def pandafy (array, Deff):
    out = pd.DataFrame(array, index=Deff)
    return out

# get sample info
info = batchinfo.loc[phyto,:]
clss = info.Class
# VsF = np.random.choice(params[info.Vs], 2, replace=False)
# CiF = np.random.choice(params[info.Ci], 2, replace=False)
# nshellF = np.random.choice(params[info.nshell], 2, replace=False)
# ncoreF = np.random.choice(params[info.ncore], 1)
# Deff = np.arange(info.Dmin, info.Dmax, info.Dint)
VsF = np.random.uniform(info.Vmin, info.Vmax, 4)
CiF = np.random.uniform(info.Cmin, info.Cmax, 4) * 1e6
nshellF = np.random.uniform(info.nmin, info.nmax, 4)
ncoreF = 1.04
Deff = np.arange(info.Dmin, info.Dmax, info.Dint)

# Run
result = {}
for Vs in VsF:
    for ci in CiF:
        for n in nshellF:
        
            # run name format: 'Vs_Ci_nshell'
            rname = '{:.2f}_{:.2f}_{:.2f}'.format(Vs, ci/1e6, n)
            result[rname] = {}
            
            # EAP run
            # standard
            #print ('####### i: {} - phyto: {} #######'.format(i,phyto))
            print ('------ {} ------'.format(rname))
            Qc, Sigma_c, c, Qb, Sigma_b, b, Qa, Sigma_a, a, Qbb, Sigma_bb, bb, bbtilde = EAP(phyto, mf, astarpath, Vs, ci, Deff, n, ncoreF)
            
            # empty dict for current run
            rname_data = {'Qc': Qc,
                          'Sigma_c': Sigma_c,
                          'c': c,
                          'Qb': Qb,
                          'Sigma_b': Sigma_b,
                          'b': b,
                          'Qa': Qa,
                          'Sigma_a': Sigma_a,
                          'a': a,
                          'Qbb': Qbb,
                          'Sigma_bb': Sigma_bb,
                          'bb': bb,
                          'bbtilde': bbtilde}  
            
            # pandafy params so Deff is index
            for param in ['Qc','Sigma_c','c','Qb','Sigma_b','b','Qa','Sigma_a','a','Qbb','Sigma_bb','bb','bbtilde']:
                rname_data[param] = pandafy(rname_data[param], Deff)
            
            result[rname] = rname_data
            
with open('/Users/jkravz311/GoogleDrive/vcourt_2layers/{}.p'.format(phyto), 'wb') as fp:
    pickle.dump(result,fp)      
    
#%% stramski data validation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.EAP_proc import EAP
import pickle
import statsmodels.api as sm
import matplotlib as mpl

clas = 'Haptophyceae'
phyto = 'P. parvum' 
code = 'parv'

with open('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/dariusz/optics.p', 'rb') as fp:
    val = pickle.load(fp)  

# with open('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/stramski_optics1.p'.format(phyto), 'rb') as fp:
#     data = pickle.load(fp)  
with open('/Users/jkravz311/Desktop/2layers/{}.p'.format(phyto), 'rb') as fp:
    data = pickle.load(fp)   

p = 'b'
l1 = np.arange(400,905,5)
l2 = np.arange(400,901,1)

# combine runs
newnames = []
runs = []
for sname in data:
    s = data[sname][p]
    for deff in s.index:
        runs.append(s.loc[deff,:])
        newname = sname + '_{}'.format(deff)
        newnames.append(newname)

# runs = []
# for sname in data[clas][phyto]:
#     s = data[clas][phyto][sname][p]
#     for deff in s.index:
#         runs.append(s.loc[deff,:])

runs = pd.concat(runs,axis=1).T 
runs.index = newnames

fig, ax = plt.subplots()
sparam = val[code][p]
res = sm.graphics.fboxplot(runs.values, l1, wfactor=50, ax=ax)
ax.plot(l2,sparam,color='b')

fig, ax = plt.subplots()
sparam = val[code][p]
runs.columns = l1
runs.T.plot(ax=ax, legend=False)
ax.plot(l2,sparam,color='b')

#%%

check = runs[(runs.loc[:,675] > .185) & (runs.loc[:,675] < .25)]
#check = check[(check.loc[:,400] > .04) & (check.loc[:,400] < .2)]
check = check[check.loc[:,400] < .185]
fig, ax = plt.subplots()
sparam = val[code][p]
runs.columns = l1
check.T.plot(ax=ax, legend=False)
ax.plot(l2,sparam,color='b')



#%% vaillancourt data validation

phyto = 'D. tertiolecta1'
with open('/Users/jkravz311/Desktop/vcourt_2layers/{}.p'.format(phyto), 'rb') as fp:
    data = pickle.load(fp)  

p = 'a'
l1 = np.arange(400,905,5)
l2 = np.arange(400,901,1)
l3 = np.array([510,620])

# combine runs
runs = []
for sname in data:
    s = data[sname][p] 
    for deff in s.index:
        runs.append(s.loc[deff,:])

runs = pd.concat(runs,axis=1).T                   
# for c in data:
#     classes[c] = pd.concat(classes[c],axis=1).T

# validation data
val = {'a': pd.read_csv('/Users/jkravz311/GoogleDrive/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/smooth/a_smooth.csv'),
       'b': pd.read_csv('/Users/jkravz311/GoogleDrive/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/smooth/b_smooth.csv'),
       'c': pd.read_csv('/Users/jkravz311/GoogleDrive/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/smooth/c_smooth.csv'),
       'bb':pd.read_csv('/Users/jkravz311/GoogleDrive/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/bb.csv'),
       'Qa': pd.read_csv('/Users/jkravz311/GoogleDrive/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/smooth/Qa_smooth.csv'),
       'Qb':pd.read_csv('/Users/jkravz311/GoogleDrive/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/smooth/Qb_smooth.csv'),
       'Qc':pd.read_csv('/Users/jkravz311/GoogleDrive/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/smooth/Qc_smooth.csv'),
       'Qbb':pd.read_csv('/Users/jkravz311/GoogleDrive/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/Qbb.csv'),
       }

fig, ax = plt.subplots()
param = val[p]
sparam = param[param['Species'] == phyto]
res = sm.graphics.fboxplot(runs.values, l1, wfactor=50, ax=ax)
if p != 'bb':
    ax.plot(l2,sparam.iloc[:,2:].T.values,color='r')
else:
    ax.plot(l3,sparam.loc[:,['510','620']].T.values, c='r', marker='s', ls='--')  
    
#%%
runs = pd.concat(runs,axis=1).T 
runs.index = newnames

fig, ax = plt.subplots()
param = val[p]
sparam = param[param['Species'] == phyto]
runs.columns = l1
runs.T.plot(ax=ax, legend=False)
ax.plot(l2,sparam.iloc[:,2:].T.values,color='b')
ax.grid()
    
#%%
check = runs[(runs.loc[:,675] > .011) & (runs.loc[:,675] < .014)]
#check = check[(check.loc[:,400] > .04) & (check.loc[:,400] < .2)]
#check = check[check.loc[:,400] < .185]
fig, ax = plt.subplots()
param = val[p]
sparam = param[param['Species'] == phyto]
runs.columns = l1
check.T.plot(ax=ax, legend=False)
ax.plot(l2,sparam.iloc[:,2:].T.values,color='b')
ax.grid()