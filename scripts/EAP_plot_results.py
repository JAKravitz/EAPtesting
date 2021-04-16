#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot EAP optics data

@author: jkravz311
"""
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import statsmodels.api as sm

with open('/Users/jkravz311/Desktop/EAP_optics.p', 'rb') as fp:
    data = pickle.load(fp)

# lambda
l = np.arange(400,905,5)

#%% Quick look - all lines

fig, axs = plt.subplots(4,4,figsize=(20,20))
axs = axs.ravel()
count = 0
for c in data:
    for phyto in data[c]:
        for sname in data[c][phyto]:
            s = data[c][phyto][sname]['a'] 
            for deff in s.index:
                axs[count].plot(l,s.loc[deff,:])
    axs[count].set_title(c)
    count = count + 1
fig.savefig('/Users/jkravz311/Desktop/a_all.png',bbox_inches='tight',dpi=300)
            
#%% prepare data for functional box plot

classes = {'Bacillariophyceae': [],
          'Chlorophyceae': [],
          'Coscinodiscophyceae': [],
          'Cryptophyceae': [],
          'Cyanophyceae': [],
          'Dinophyceae': [],
          'Eustigmatophyceae': [],
          'Fragilariophyceae': [],
          'Pelagophyceae': [],
          'Prasinophyceae': [],
          'Prymnesiophyceae': [],
          'Raphidophyceae': [],
          'Rhodophyceae': []
          }

for c in data:
    for phyto in data[c]:
        for sname in data[c][phyto]:
            s = data[c][phyto][sname]['bb'] 
            for deff in s.index:
                classes[c].append(s.loc[deff,:])
                   
for c in data:
    classes[c] = pd.concat(classes[c],axis=1).T

#%% functional box plot

l1 = np.arange(400,905,5)
l2 = np.arange(400,901,1)
l3 = np.array([510,620])

# validation data
val = {'a': pd.read_csv('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/smooth/a_smooth.csv'),
       'b': pd.read_csv('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/smooth/b_smooth.csv'),
       'c': pd.read_csv('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/smooth/c_smooth.csv'),
       'bb':pd.read_csv('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/bb.csv'),
       'Qa': pd.read_csv('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/smooth/Qa_smooth.csv'),
       'Qb':pd.read_csv('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/smooth/Qb_smooth.csv'),
       'Qc':pd.read_csv('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/smooth/Qc_smooth.csv'),
       'Qbb':pd.read_csv('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/Vaillancourt/Qbb.csv'),
       }

fig, axs = plt.subplots(4,4,figsize=(20,20))
axs = axs.ravel()
count = 0
for c in classes:
    print (c)
    res = sm.graphics.fboxplot(classes[c].values, l1, wfactor=50, ax=axs[count])
    axs[count].set_title(c)
    param = val['bb']
    cparam = param[param['Class'] == c]
    if cparam.shape[0] == 0:
        count = count+1
        continue
    # axs[count].plot(l2,cparam.iloc[:,2:].T.values,color='r')
    axs[count].plot(l3,cparam.loc[:,['510','620']].T.values, c='r', marker='s', ls='--')
    count = count+1
fig.savefig('/Users/jkravz311/Desktop/bb_fda.png',bbox_inches='tight',dpi=300)


# bac = classes['Bacillariophyceae']
# bac.columns=l
# res = sm.graphics.fboxplot(bac.values, l, wfactor=20)
# depth = res[1]
# depthix = res[2]


#%% validation plots





