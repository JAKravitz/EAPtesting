#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 12:29:45 2021

@author: jakravit
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from EAP import EAP
import pickle
import statsmodels.api as sm
import random

phyto = 'Nannochloropsis sp.' 
#code = 'parv'
mf = '/content/EAP/data/501nm_extended_e1701000.mat'
astarpath = '/content/EAP/data/in_vivo_phyto_abs.csv'
batchinfo1 = pd.read_csv('/content/EAP/data/vcourt_batch_F.csv', index_col=0)
batchinfo2 = pd.read_csv('/content/EAP/data/stram_batch_F.csv', index_col=0)


def pandafy (array, Deff):
    out = pd.DataFrame(array, index=Deff)
    return out

# get sample info
try:
    info = batchinfo1.loc[phyto,:]
except:
    info = batchinfo2.loc[phyto,:]
clss = info.Class
VsF = np.random.uniform(info.Vmin, info.Vmax, 7)
CiF = np.random.uniform(info.Cmin, info.Cmax, 7) * 1e6
nshellF = np.random.uniform(info.nmin, info.nmax, 7)
ncoreF = 1.02
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
            
with open('/content/drive/My Drive/eap_test/{}.p'.format(phyto), 'wb') as fp:
    pickle.dump(result,fp)    