#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 11:57:11 2021

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

species = ['NIG1','SAH1','OAH1','SAN1'] #'AUS1','ICE1','KUW1',
nprimepath = '/content/EAP/data/stramski_2007_mineral_nprime.csv'
nprime = pd.read_csv(nprimepath,index_col=0)

# sample info
nreal = np.random.uniform(1.10, 1.3, 5)
jexp = np.random.uniform(3.4, 4.6, 4)
dmax = [10.05, 50.05, 100.05]
l = np.arange(.3, .855, .005)

# Run
for sp in species:
    
    kcore = nprime[sp].values 
    im_wv = nprime.index.values / 1000
    last = kcore[-1:]
    kcore = griddata(im_wv, kcore, l, 'linear',fill_value=last)
    
    result = {}
    for n in nreal:
        for j in jexp:
            for d in dmax:
            
                # name
                rho = (n - 0.7717) / 0.1475e-6 # (wozniak & stramski, 2004)
                rname = '{}_{:.2f}_{:.2f}_{:.2f}_{}'.format(sp, n, rho, j, d)
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
                
                
    with open('/content/drive/My Drive/nasa_npp/2lay_min_test/{}.p'.format(sp), 'wb') as fp:
        pickle.dump(result,fp)    


