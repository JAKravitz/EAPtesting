#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 13:08:30 2021

@author: jkravz311
"""
#%%
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

path = '/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/dariusz/'
chl = '/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/dariusz/chl.dat'

codes = {}
codes['hbac'] = {'Name':'Heterotrophic bacteria','Class':'Bacteria','Citation':'Stramski et al., 2011','ax':[],'bx':[],'cx':[],'c':[],'a':[],'b':[],'chl':[],'lx':[]}
codes['viru'] = {'Name':'Virus','Class':'Virus','Citation':'Stramski et al., 2011','ax':[],'bx':[],'cx':[],'c':[],'a':[],'b':[],'chl':[],'lx':[]}
codes['proc'] = {'Name':'Prochlorococcus','Class':'Cyanophyceae','Citation':'Stramski et al., 2011','ax':[],'bx':[],'cx':[],'c':[],'a':[],'b':[],'chl':[],'lx':[]}
codes['syne'] = {'Name':'Synechococcus','Class':'Cyanophyceae','Citation':'Stramski et al., 2011','ax':[],'bx':[],'cx':[],'c':[],'a':[],'b':[],'chl':[],'lx':[]}
codes['syma'] = {'Name':'Anacystis marina','Class':'Cyanophyceae','Citation':'Stramski et al., 2011','ax':[],'bx':[],'cx':[],'c':[],'a':[],'b':[],'chl':[],'lx':[]}
codes['ping'] = {'Name':'Pavlova pinguis','Class':'Haptophyceae','Citation':'Stramski et al., 2011','ax':[],'bx':[],'cx':[],'c':[],'a':[],'b':[],'chl':[],'lx':[]}
codes['pseu'] = {'Name':'Thalassiosira pseudonana','Class':'Bacillariophyceae','Citation':'Stramski et al., 2011','ax':[],'bx':[],'cx':[],'c':[],'a':[],'b':[],'chl':[],'lx':[]}
codes['luth'] = {'Name':'Pavlova lutheri','Class':'Haptophyceae','Citation':'Stramski et al., 2011','ax':[],'bx':[],'cx':[],'c':[],'a':[],'b':[],'chl':[],'lx':[]}
codes['galb'] = {'Name':'Isochrysis galbana','Class':'Haptophyceae','Citation':'Stramski et al., 2011','ax':[],'bx':[],'cx':[],'c':[],'a':[],'b':[],'chl':[],'lx':[]}
codes['huxl'] = {'Name':'Emiliania huxleyi','Class':'Haptophyceae','Citation':'Stramski et al., 2011','ax':[],'bx':[],'cx':[],'c':[],'a':[],'b':[],'chl':[],'lx':[]}
codes['crue'] = {'Name':'Porphyridium cruentum','Class':'Rhodophyceae','Citation':'Stramski et al., 2011','ax':[],'bx':[],'cx':[],'c':[],'a':[],'b':[],'chl':[],'lx':[]}
codes['frag'] = {'Name':'Chroomonas fragarioides','Class':'Cryptophyceae','Citation':'Stramski et al., 2011','ax':[],'bx':[],'cx':[],'c':[],'a':[],'b':[],'chl':[],'lx':[]}
codes['parv'] = {'Name':'Prymnesium parvum','Class':'Haptophyceae','Citation':'Stramski et al., 2011','ax':[],'bx':[],'cx':[],'c':[],'a':[],'b':[],'chl':[],'lx':[]}
codes['bioc'] = {'Name':'Dunaliella bioculata','Class':'Chlorophyceae','Citation':'Stramski et al., 2011','ax':[],'bx':[],'cx':[],'c':[],'a':[],'b':[],'chl':[],'lx':[]}
codes['tert'] = {'Name':'Dunaliella tertiolecta','Class':'Chlorophyceae','Citation':'Stramski et al., 2011','ax':[],'bx':[],'cx':[],'c':[],'a':[],'b':[],'chl':[],'lx':[]}
codes['curv'] = {'Name':'Chaetoceros curvisetum','Class':'Bacillariophyceae','Citation':'Stramski et al., 2011','ax':[],'bx':[],'cx':[],'c':[],'a':[],'b':[],'chl':[],'lx':[]}
codes['elon'] = {'Name':'Hymenomonas elongata','Class':'Haptophyceae','Citation':'Stramski et al., 2011','ax':[],'bx':[],'cx':[],'c':[],'a':[],'b':[],'chl':[],'lx':[]}
codes['mica'] = {'Name':'Prorocentrum micans','Class':'Dinophyceae','Citation':'Stramski et al., 2011','ax':[],'bx':[],'cx':[],'c':[],'a':[],'b':[],'chl':[],'lx':[]}


## get cell chl for calculating astarphy
with open(chl,'r') as f: 
    while True:
        line = f.readline()
        if line in ['\n']:
            break 

        p = line.split(' ')[0].lower()
        #print (p)
        c = float(line.split(' ')[1].rstrip()) 
        if p in list(codes.keys()):
            codes[p]['chl'] = c 
        else:
            continue
        

#%% get cross section data
import pickle
from scipy.interpolate import griddata

l1 = np.arange(350,751,1)
l2 = np.arange(400,901,1)

for f in os.listdir(path):
    info = f.split('_')
    if len(info) > 1:
        p = f.split('_')[0]
        data = np.loadtxt(path+f)
        codes[p]['lx'] = data[:,0]
        codes[p]['cx'] = data[:,1]
        codes[p]['ax'] = data[:,2]
        codes[p]['bx'] = data[:,3]
        codes[p]['bbx'] = data[:,4]
        codes[p]['l'] = l2
        if p not in ['hbac','viru']:
            c = data[:,1] / (codes[p]['chl'] * 1000)
            a = data[:,2] / (codes[p]['chl'] * 1000)
            b = data[:,3] / (codes[p]['chl'] * 1000)
            bb = data[:,4] / (codes[p]['chl'] * 1000)
            codes[p]['c'] = griddata(l1, c, l2, 'linear', fill_value=c.min())
            codes[p]['a'] = griddata(l1, a, l2, 'linear', fill_value=a.min())
            codes[p]['b'] = griddata(l1, b, l2, 'linear', fill_value=b.min())   
            codes[p]['bb'] = griddata(l1, bb, l2, 'linear', fill_value=bb.min())   
            
    else:
        continue
 
with open('/Users/jkravz311/Desktop/nasa_npp/groundtruth_data/phyto_optics/dariusz/optics.p', 'wb') as fp:
    pickle.dump(codes,fp)     

#%% save abs to file to act as imag ref idx
from scipy.interpolate import griddata

a = pd.DataFrame()
count = 0
for s in codes:
    name = codes[s]['Name']
    clas = codes[s]['Class']
    a1 = codes[s]['a']
    line = np.hstack((name,clas,a1))
    a[count] = line
    count = count+1
a = a.T
idx = np.hstack(('Species','Class',l2))
a.columns = idx
a.to_csv('/Users/jkravz311/git/EAP/data/stamski_phyto_a.csv')



