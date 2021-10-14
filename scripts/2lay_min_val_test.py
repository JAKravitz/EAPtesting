#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 17:43:41 2021

@author: jakravit
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle

with open('/Users/jakravit/Desktop/2lay_min_test/det.p', 'rb') as fp:
    data = pickle.load(fp) 

l = np.arange(.3, .855, .005)
l = np.arange(.4, .705, .005)
atot = []
btot = []
bbtot = []

for s in data:
    a = data[s]['a']
    atot.append(a[0,:])
atot = pd.DataFrame(atot,columns=l)

atot.T.plot(legend=False)


for s in data:
    b = data[s]['b']
    btot.append(b[0,:])
btot = pd.DataFrame(btot,columns=l)

btot.T.plot(legend=False)


for s in data:
    bb = data[s]['bb']
    bbtot.append(bb[0,:])
bbtot = pd.DataFrame(bbtot,columns=l)

bbtot.T.plot(legend=False)
