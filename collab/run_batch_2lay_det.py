#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 11:57:11 2021

@author: jakravit
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from twolay_det import twolay_det
import pickle
import statsmodels.api as sm
import random
from scipy.interpolate import griddata


# sample info
#rho = np.random.uniform(.2e6, .5e6, 3)
rho = [.2e6, .35e6, .5e6]
#nreal = np.random.uniform(1.03, 1.05, 3)
nreal = [1.03, 1.04, 1.05]
#jexp = np.random.uniform(3.4, 4.6, 3)
jexp = [3.4, 4, 4.6]
dmax = [10.05, 50.05, 100.05]
l = np.arange(.3, .855, .005)    
kcore = 0.010658 * np.exp(-0.007186* (l*1000)) #Stramski 2001 

result = {}
for n in nreal:
    for j in jexp:
        for r in rho:
            for d in dmax:
        
                # name
                #rho = (n - 0.7717) / 0.1475e-6 # (wozniak & stramski, 2004 > more for min)
                rname = '{:.2f}_{:.2f}_{:.2f}_{}'.format(n, r, j, d)
                result[rname] = {}
                
                # EAP run
                print ('------ {} ------'.format(rname))
                a, b, bb = twolay_det(kcore, n, r, j, d)
                
                # dict for current run
                rname_data = {'a': a,
                              'b': b,
                              'bb': bb,
                              'nreal': n,
                              'rho': r,
                              'j': j,
                              'dmax': d}
                
                # # pandafy params so Deff is index
                # for param in ['Qc','Sigma_c','c','Qb','Sigma_b','b','Qa','Sigma_a','a','Qbb','Sigma_bb','bb','bbtilde']:
                #     rname_data[param] = pandafy(rname_data[param], Deff)
                
                result[rname] = rname_data
            
            
with open('/content/drive/My Drive/nasa_npp/2lay_min_test/det.p', 'wb') as fp:
    pickle.dump(result,fp)    


