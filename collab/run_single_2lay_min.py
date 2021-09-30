#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 12:29:45 2021

@author: jakravit
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from twolay_min import twolay_min
import pickle
import statsmodels.api as sm
import random
from scipy.interpolate import griddata

species = 'AUS1'
nprimepath = '/content/EAP/data/stramski_2007_mineral_nprime.csv'

# sample info
nreal = np.random.uniform(1.07, 1.22, 5)
rho = np.random.uniform(1.9e6, 2.85e6, 5)
jexp = np.random.uniform(3.6, 4.4, 5)

l = np.arange(.3, .855, .005)
nprime = pd.read_csv(nprimepath,index_col=0)
kcore = nprime[species].values 
im_wv = nprime.index.values / 1000
last = kcore[-1:]
kcore = griddata(im_wv, kcore, l, 'linear',fill_value=last)

# Run
result = {}
for n in nreal:
    for r in rho:
        for j in jexp:
        
            # run name format: 'Vs_Ci_nshell'
            rname = '{:.2f}_{:.2f}_{:.2f}'.format(n, r, j)
            result[rname] = {}
            
            # EAP run
            # standard
            #print ('####### i: {} - phyto: {} #######'.format(i,phyto))
            print ('------ {} ------'.format(rname))
            a, b, bb = twolay_min(kcore, n, r, j)
            
            # empty dict for current run
            rname_data = {'a': a,
                          'b': b,
                          'bb':bb}
            
            # # pandafy params so Deff is index
            # for param in ['Qc','Sigma_c','c','Qb','Sigma_b','b','Qa','Sigma_a','a','Qbb','Sigma_bb','bb','bbtilde']:
            #     rname_data[param] = pandafy(rname_data[param], Deff)
            
            result[rname] = rname_data
            
with open('/content/drive/My Drive/nasa_npp/2lay_min_test/{}.p'.format(species), 'wb') as fp:
    pickle.dump(result,fp)    