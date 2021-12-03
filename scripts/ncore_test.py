#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 11:17:55 2021

@author: jakravit
"""
#%%
import scipy.io as io
from scipy.interpolate import griddata
import numpy as np

l = np.arange(.4, .905, .005).astype('float32')
mf = '/Users/jakravit/git/EAPtesting/data/501nm_extended_e1701000.mat'
mf = io.loadmat(mf)
kcore = griddata(mf['RIs'][:, 5], mf['RIs'][:, 0], l, 'linear')

import matplotlib.pyplot as plt
plt.plot(l,kcore)

import scipy.optimize
def monoExp(x, m, t,):
    return m * np.exp(-t * x) #+ b

# perform the fit
p0 = (.1, .1, .1) # start with values near those we expect
params, cv = scipy.optimize.curve_fit(monoExp, l, kcore,)
m, t = params
sampleRate = 20_000 # Hz
tauSec = (1 / t) / sampleRate

# determine quality of the fit
squaredDiffs = np.square(kcore - monoExp(l, m, t))
squaredDiffsFromMean = np.square(kcore - np.mean(kcore))
rSquared = 1 - np.sum(squaredDiffs) / np.sum(squaredDiffsFromMean)
print(f"R² = {rSquared}")

# plot the results
plt.plot(l, kcore, '.', label="data")
plt.plot(l, monoExp(l, m, t, ), '--', label="fitted")
plt.title("Fitted Exponential Curve")
plt.legend()

# inspect the parameters
print(f"Y = {m} * e^(-{t} * x)")
print(f"Tau = {tauSec * 1e6} µs")



#%%
kcore2 = 0.041 * np.exp(-11.029 * l)

# plot the results
plt.plot(l, kcore, '.', label="data")
plt.plot(l, monoExp(l, m, t, ), '--', label="fitted")
plt.plot(l, kcore2, ':', label='eq')
plt.title("Fitted Exponential Curve")
plt.legend()