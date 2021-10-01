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
# nreal = np.random.uniform(1.10,1.4,3)
# jexp = np.random.uniform(3.2, 4.8, 3)
nreal = [1.1] #, 1.17, 1.23,]
jexp = [3.4]#, 4.0, 4.6]
dmax = [100.05]#[10.05,50.05,100.05]


l = np.arange(.3, .855, .005)
nprime = pd.read_csv(nprimepath,index_col=0)
kcore = nprime[species].values 
im_wv = nprime.index.values / 1000
last = kcore[-1:]
kcore = griddata(im_wv, kcore, l, 'linear',fill_value=last)

# Run
result = {}
for n in nreal:
    for j in jexp:
        for d in dmax:
        
            # name
            rho = (n - 0.7717) / 0.1475e-6 # (wozniak & stramski, 2004)
            rname = '{:.2f}_{:.2f}_{:.2f}_{}'.format(n, rho, j, d)
            result[rname] = {}
            
            # EAP run
            print ('------ {} ------'.format(rname))
            a, b, bb = twolay_min(kcore, n, rho, j, d)
            
            # dict for current run
            rname_data = {'a': a,
                          'b': b,
                          'bb':bb}
            
            # # pandafy params so Deff is index
            # for param in ['Qc','Sigma_c','c','Qb','Sigma_b','b','Qa','Sigma_a','a','Qbb','Sigma_bb','bb','bbtilde']:
            #     rname_data[param] = pandafy(rname_data[param], Deff)
            
            result[rname] = rname_data
            
            plt.plot(l,a[0,:])
            plt.show()
            
with open('/content/drive/My Drive/nasa_npp/2lay_min_test/{}.p'.format(species), 'wb') as fp:
    pickle.dump(result,fp)    

