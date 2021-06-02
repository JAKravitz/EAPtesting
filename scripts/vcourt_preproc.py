#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 17:18:56 2021

@author: jakravit
"""
#%%
from scipy.interpolate import griddata
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import BSpline, LSQUnivariateSpline, UnivariateSpline
from scipy import interpolate

path = '/Users/jakravit/Desktop/npp_projects/EAP/phyto_optics/Vaillancourt/Qc.csv'
outpath = '/Users/jakravit/Desktop/npp_projects/EAP/phyto_optics/Vaillancourt/smooth/Qc_smooth.csv'

l = np.arange(400, 901, 1)
data = pd.read_csv(path, index_col=0)

# separate spectra and metadata
spectra = data.filter(regex='\d')
meta = data.filter(regex='[a-zA-Z]')
wv = spectra.columns.values.astype(float)

# define knot positions
# minus first and last (400,900)
kp = [410,420,425,430,440,460,480,500,515,530,545,560,575,590,600,610,
      620,630,640,650,665,680,695,710,725,740,760,780,800,850]

smoothspec = []
for k in spectra.index:
    
    # resolve to standard 400-900nm @ 1nm res
    s1 = spectra.loc[k,:].values
    s = griddata(wv, s1, l, 'linear') # interpolate
    s = np.where(s < 0, np.nan, s) # replace negatives w/ nan
    s = np.where(s == 0, np.nan, s) # replace zeros w/ nan
    nans, x0 = np.isnan(s), lambda z: z.nonzero()[0] # replace nans
    s[nans] = np.interp(x0(nans), x0(~nans), s[~nans])       
    
    # smooth using bspline
    fit = LSQUnivariateSpline(l, s, kp) # spline fit
    kn = fit.get_knots() # knots
    kn = 3*[kn[0]] + list(kn) + 3*[kn[-1]] 
    c = fit.get_coeffs()
    s2 = BSpline(kn,c,3)
    smoothspec.append(s2(l))

smoothspec = pd.DataFrame(smoothspec,index=data.index,columns=l)
final = pd.concat([meta,smoothspec],axis=1)
final.to_csv(outpath)
    
    






