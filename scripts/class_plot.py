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

strampath = '/Users/jakravit/Desktop/nasa_npp/EAP/stramski_2layers/'
vcourtpath = '/Users/jakravit/Desktop/nasa_npp/EAP/vcourt_2layers/'

stramlist = os.listdir(strampath)
vcourtlist = os.listdir(vcourtpath)

phytos = {}

for phy in stramlist:
    fpath = strampath + phy
    with open(fpath, 'rb') as fp:
        data = pickle.load(fp)
        phytos[phy] = data
        
        
        

#%%
fpath = '/Users/jakravit/Desktop/nasa_npp/EAP/stramski_final/Prochlorococcus.p'
with open(fpath, 'rb') as fp:
    foo = pickle.load(fp)


