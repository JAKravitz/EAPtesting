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

phyto = 'H. akashiwo' 
mf = '/Users/jkravz311/git/EAP/data/501nm_extended_e1701000.mat'
astarpath = '/Users/jkravz311/git/EAP/data/in_vivo_phyto_abs.csv'
batchinfo = pd.read_csv('/Users/jkravz311/git/EAP/data/EAP_batch_V1.csv', index_col=0)

params = {'Vs1': np.arange(0.04,0.26,0.02), # small
          'Vs2': np.arange(0.2,0.4,0.02), # medium
          'Vs3': np.arange(0.36,0.56,0.02), # large
          'Ci1': np.arange(.5e6,7e6,.5e6), # low
          'Ci2': np.arange(4e6,12e6,.5e6), # high
          'Ci3': np.arange(2e6,8e6,.5e6), # avg
          'nshell1': np.arange(1.06,1.16,.01), # low 
          'nshell2': np.arange(1.11, 1.22,.01), # high
          'nshell3': np.arange(1.1, 1.19,.01), # avg
          'nshell4': np.array([1.21, 1.22, 1.23]), # very high (huxleyi)
          'ncore': np.arange(1.014, 1.04, 0.005)}

def pandafy (array, Deff):
    out = pd.DataFrame(array, index=Deff)
    return out

# get sample info
info = batchinfo.loc[phyto,:]
clss = info.Class
VsF = np.random.choice(params[info.Vs], 2, replace=False)
CiF = np.random.choice(params[info.Ci], 2, replace=False)
nshellF = np.random.choice(params[info.nshell], 2, replace=False)
ncore = np.random.choice(params['ncore'], 1)
Deff = np.arange(info.Dmin, info.Dmax, .5)


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
            Qc, Sigma_c, c, Qb, Sigma_b, b, Qa, Sigma_a, a, Qbb, Sigma_bb, bb, bbtilde = EAP(phyto, mf, astarpath, Vs, ci, Deff, n, ncore)
            
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
            
with open('/Users/jkravz311/Desktop/akashiwo.p', 'wb') as fp:
    pickle.dump(result,fp)      
      
#%%

with open('/Users/jkravz311/Desktop/akashiwo.p', 'rb') as fp:
    data = pickle.load(fp)  

p = 'b'
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
val = {'a': pd.read_csv('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/smooth/a_smooth.csv'),
       'b': pd.read_csv('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/smooth/b_smooth.csv'),
       'c': pd.read_csv('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/smooth/c_smooth.csv'),
       'bb':pd.read_csv('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/bb.csv'),
       'Qa': pd.read_csv('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/smooth/Qa_smooth.csv'),
       'Qb':pd.read_csv('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/smooth/Qb_smooth.csv'),
       'Qc':pd.read_csv('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/smooth/Qc_smooth.csv'),
       'Qbb':pd.read_csv('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/Qbb.csv'),
       }

fig, ax = plt.subplots()
param = val[p]
sparam = param[param['Species'] == phyto]
res = sm.graphics.fboxplot(runs.values, l1, wfactor=50, ax=ax)
if p != 'bb':
    ax.plot(l2,sparam.iloc[:,2:].T.values,color='r')
else:
    ax.plot(l3,sparam.loc[:,['510','620']].T.values, c='r', marker='s', ls='--')  