#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 11:03:30 2021

@author: jakravit
"""
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

strampath = '/Users/jakravit/git/EAP/data/final_ranges/stramski/'
vcourtpath = '/Users/jakravit/git/EAP/data/final_ranges/vcourt/'
phytos = ['I. galbana1.p', 'P. lutheri.p', 'T. pseudonana1.p', 'C. calcitrans.p',
          'A. carterae.p', 'P. micans.p', 'G. theta.p', 'R. lens.p', 'D. tertiolecta1.p',
          'N. atomus.p','Synechococcus.p']

alist = []
blist = []
bblist = []
splist = []
cllist = []
idxlist = []

for p in phytos:
    try:
        with open (strampath+p, 'rb') as fp:
            iops = pickle.load(fp)
    except:
        with open (vcourtpath+p, 'rb') as fp:
            iops = pickle.load(fp)
    
    # pick random spectra
    idx = np.random.choice(iops['a'].shape[0],replace=False, size=1)
    a1 = iops['a'].iloc[idx,:]
    b1 = iops['b'].iloc[idx,:]
    bb1 = iops['bb'].iloc[idx,:]
    
    splist.append(iops['species'])
    cllist.append(iops['class'])
    alist.append(a1)
    blist.append(b1)
    bblist.append(bb1)
    idxlist.append(idx)


adf = pd.concat(alist)
spdf = pd.DataFrame(splist,index=adf.index)
cldf = pd.DataFrame(cllist,index=adf.index)
adf = pd.concat([spdf,cldf,adf],axis=1)
bdf = pd.concat(blist)
bbdf = pd.concat(bblist)



    
            
            
            
            