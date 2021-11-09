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

case1 = {'chla':5,
         'min':.01,
         'det':.01,
         'cdom':.01}


# Total choices: (list all classes...)
phyto_class_frxn = {   'Haptophytes'              :             .3,
                       'Diatoms'                  :             .2,
                       'Dinoflagellates'          :             .1,
                       'Cryptophytes'             :             .2,
                       'Chlorophytes'             :             .15,
                       'Cyanobacteria'            :             .05
                       }

phyto_spec_frxn = {    'I. galbana1'              :             .2, 
                       'P. lutheri'               :             .1, 
                       'T. pseudonana1'           :             .15, 
                       'C. calcitrans'            :             .05,
                       'A. carterae'              :             .05, 
                       'P. micans'                :             .05, 
                       'G. theta'                 :             .15, 
                       'R. lens'                  :             .05, 
                       'D. tertiolecta1'          :             .1,
                       'N. atomus'                :             .05,
                       'Synechococcus'            :             .05
                       }

min_frxn = {           'AUS'                      :             .7,
                       'KUW'                      :             .3
                       }


## phytos

strampath = '/Users/jakravit/git/EAP/data/final_ranges/stramski/'
vcourtpath = '/Users/jakravit/git/EAP/data/final_ranges/vcourt/'

alist = []
blist = []
bblist = []
splist = []
cllist = []
idxlist = []
afraclist = []
bfraclist = []

for p in phyto_spec_frxn.keys():
    try:
        with open (strampath+p+'.p', 'rb') as fp:
            iops = pickle.load(fp)
    except:
        with open (vcourtpath+p+'.p', 'rb') as fp:
            iops = pickle.load(fp)
    
    # pick random spectra
    idx1 = np.random.choice(iops['a'].shape[0],replace=False, size=1)
    a1 = iops['a'].iloc[idx1,:]
    b1 = iops['b'].iloc[idx1,:]
    bb1 = iops['bb'].iloc[idx1,:]
    
    # species
    # if iops['species'] in ['T. pseudonanna']:
    #     sp = 'T. pseudonona1'
    # else:
    #     sp = iops['species']
        
    # class
    if iops['class'] in ['Prymnesiophyceae']:
        cl = 'Haptophyceae'
    elif iops['class'] in ['Coscinodiscophyceae']:
        cl = 'Diatoms'    
    else:    
        cl = iops['class']
    
    # append lists
    splist.append(p)
    cllist.append(cl)
    alist.append(a1)
    blist.append(b1)
    bblist.append(bb1)
    name = '{}_{}_{}'.format(iops['class'],iops['species'],a1.index[0])
    idxlist.append(name)
    
    afrac = phyto_spec_frxn[p] * case1['chla']
    afraclist.append(afrac)
    bfrac = phyto_spec_frxn[p] * case1['chla']
    bfraclist.append(bfrac)

#% minerals

l = np.arange(400, 905, 5)
auspath = '/Users/jakravit/Desktop/2lay_min_test/AUS1.p'
kuwpath = '/Users/jakravit/Desktop/2lay_min_test/KUW1.p'
with open (auspath,'rb') as fp:
    aus = pickle.load(fp)
with open (kuwpath,'rb') as fp:
    kuw = pickle.load(fp)

def resize (x):
    from scipy import interpolate    
    l = np.arange(300, 855, 5)
    l2 = np.arange(400, 905, 5)
    f = interpolate.interp1d(l, x, kind='nearest', fill_value='extrapolate')
    xnew = f(l2)
    return xnew

# mineral 1 (aus)
idx2 = np.random.choice(list(aus.keys()))    
a2 = pd.DataFrame(resize(aus[idx2]['a']),columns=l)
b2 = pd.DataFrame(resize(aus[idx2]['b']),columns=l)
bb2 = pd.DataFrame(resize(aus[idx2]['bb']),columns=l)

alist.append(a2)
blist.append(b2)
bblist.append(bb2)
splist.append('AUS')
cllist.append('AUS')
name = str(idx2)
idxlist.append(name)
# fraction = min_frxn['AUS'] * abs_component_frxn['min']
# fraclist.append(fraction)
afrac = min_frxn['AUS'] * case1['min']
afraclist.append(afrac)
bfrac = min_frxn['AUS'] * case1['min']
bfraclist.append(bfrac)
  
# mineral 2 (kuw)        
idx3 = np.random.choice(list(kuw.keys()))    
a3 = pd.DataFrame(resize(kuw[idx3]['a']),columns=l)
b3 = pd.DataFrame(resize(kuw[idx3]['b']),columns=l)
bb3 = pd.DataFrame(resize(kuw[idx3]['bb']),columns=l)

alist.append(a3)
blist.append(b3)
bblist.append(bb3) 
splist.append('KUW')
cllist.append('KUW')
name = str(idx3)
idxlist.append(name)
# fraction = min_frxn['KUW'] * abs_component_frxn['min']
# fraclist.append(fraction)
afrac = min_frxn['KUW'] * case1['min']
afraclist.append(afrac)
bfrac = min_frxn['KUW'] * case1['min']
bfraclist.append(bfrac)


#% detrital 

detpath = '/Users/jakravit/Desktop/2lay_min_test/det_model.p'
with open (detpath,'rb') as fp:
    det = pickle.load(fp)
alist.append(pd.DataFrame(det['a'],columns=l))
blist.append(pd.DataFrame(det['b'],columns=l))
bblist.append(pd.DataFrame(det['bb'],columns=l))
# blist.append(det['b'])
# bblist.append(det['bb'])
splist.append('DET')
cllist.append('DET')
idxlist.append('DET_1.03_4_120')
afraclist.append(case1['det'])
bfraclist.append(case1['det'])

#% total scattering and backscattering (no cdom)

bdf = pd.concat(blist)
bbdf = pd.concat(bblist)
spdf = pd.DataFrame(splist,index=bdf.index,columns=['Species'])
cldf = pd.DataFrame(cllist,index=bdf.index,columns=['Class'])
idxdf = pd.DataFrame(idxlist,index=bdf.index,columns=['ID'])
bfracdf = pd.DataFrame(bfraclist,index=bdf.index,columns=['Fraction'])
btot = pd.concat([idxdf,cldf,spdf,bfracdf,bdf],axis=1)
bbtot = pd.concat([idxdf,cldf,spdf,bfracdf,bbdf],axis=1)


#% CDOM

l = np.arange(400, 905, 5)
s_cdom = np.linspace(0.012,0.021,10)
s = np.random.choice(s_cdom)
ag = case1['cdom']*np.exp(-s*(l-440))
alist.append(pd.DataFrame(ag.reshape(1,-1),columns=l))
splist.append('CDOM')
cllist.append('CDOM')
idxlist.append('cdom_{}'.format(s))
afraclist.append(1)


#% total absorption (w/ cdom)

adf = pd.concat(alist)
spdf = pd.DataFrame(splist,index=adf.index,columns=['Species'])
cldf = pd.DataFrame(cllist,index=adf.index,columns=['Class'])
idxdf = pd.DataFrame(idxlist,index=adf.index,columns=['ID'])
afracdf = pd.DataFrame(afraclist,index=adf.index,columns=['Fraction'])
atot = pd.concat([idxdf,cldf,spdf,afracdf,adf],axis=1)

#% plot

spectra = atot.filter(regex='^[0-9]')
spectra_fracs = spectra.multiply(afracdf.values)
at = spectra_fracs.sum()

fig,ax = plt.subplots()
spectra_fracs.T.plot(ax=ax)
at.plot(ax=ax,lw=2)



#%% SAVE SIOPs to CSV
atot.reset_index(inplace=True,drop=True)
btot.reset_index(inplace=True,drop=True)
bbtot.reset_index(inplace=True,drop=True)
atot.to_csv('/Users/jakravit/Desktop/absorption_case1.csv')
btot.to_csv('/Users/jakravit/Desktop/scatter_case1.csv')
bbtot.to_csv('/Users/jakravit/Desktop/backscatter_case1.csv')


   
            