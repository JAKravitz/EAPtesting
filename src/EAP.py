#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EAP
IOP 2-layer base code
@author: S.Bernard, L. lain, H. Evers-King, J. Kravitz
"""
# fortran wrapper
from numpy import f2py
try:
    sourcefile = open('/Users/jakravit/git/EAPtesting/src/Dmmex_R14B_4.f','rb')
except:
    sourcefile = open('/content/EAP/src/Dmmex_R14B_4.f','rb') # to run in google collab
sourcecode = sourcefile.read()
f2py.compile(sourcecode, modulename='Dmmex_R14B_4')
import Dmmex_R14B_4
import numpy as np
import pandas as pd
import scipy.io as io
import matplotlib.pyplot as plt

#%%
#def EAP (phyto, mf, astarpath, Vs, ci, Deff, nshell, ncore):
  
phyto = 'Nannochloropsis sp.'
mf = '/Users/jakravit/git/EAPtesting/data/501nm_extended_e1701000.mat'
astarpath = '/Users/jakravit/git/EAPtesting/data/in_vivo_phyto_abs.csv'
Vs = .2 
ci = 2e6 # intracellular chl
D_eff = [.5,1,1.5,2]
nshell = 1.13
ncore = 1.02
Ci = 200 # (kg m^-3) intracellular carbon

      
l = np.arange(.4, .905, .005).astype(np.float32) # wavelength range and resolution (changing this changes your interp value when normalising kshell)
int_val = 55 # refers to l[55] which is 675 nm. 255 for 1 nm resolution

# Vs = Vs
# ci = ci
# D_eff = Deff

V_eff= 0.6
mf = io.loadmat(mf)

# using absorption for imaginary refractive index
im = pd.read_csv(astarpath, index_col=0)
im = im.filter(regex='^[0-9]')
im_wv = np.arange(.4,.901,.005)
im_a1 = im.loc[phyto,:].values

Vc=1 - Vs
FR=(1- Vs) ** (1/ 3)# relative volume of core to shell
nmedia = 1.334
wavelength = l/ nmedia

wvno = 2 * np.pi / wavelength # this is a Mie param - combo of size and wavelength

# hilbert transform
def analytic_signal(x):
    from scipy.fftpack import fft, ifft
    N = len(x)
    X = fft(x, N)
    h = np.zeros(N)
    h[0] = 1
    h[1:N//2] = 2* np.ones(N// 2-1)
    h[N// 2] = 1
    Z = X * h
    z = ifft(Z, N)
    return z

# core imaginary RI
from scipy.interpolate import griddata
kcore = 0.041 * np.exp(-11.029 * l)
#kcore = griddata(mf['RIs'][:, 5], mf['RIs'][:, 0], l, 'linear')
#kshell_base = griddata(mf['RIs'][:, 5], mf['RIs'][:, 2], l, 'linear')

# shell imaginary RI
kshell_base = im_a1
kshell_base = griddata(im_wv, im_a1, l, 'linear',)
kshell_norm = (6.75e-7/ nmedia) * (0.027 * ci/ Vs) / (4 * np.pi) #scale to this theoretical max unpackaged chl abs at 675 nm
kshell = kshell_base * (kshell_norm / kshell_base[int_val]) #55 is index of 675 nm

# Real RI from Ci 
n660_stram = (Ci + 3404.99) / 3441.055 # stramski 98

# Final RI's
nshell = nshell + np.imag(analytic_signal(kshell))
ncore = ncore + np.imag(analytic_signal(kcore))
khom = kcore*Vc + kshell*Vs # imag refractive index 
nhom = ncore*Vc + nshell*Vs # real RI
# nhom660 = nhom[52]
# dif = n660_stram - nhom660
# nhom = nhom + dif # real RI accounting for carbon (Ci) using stramski98 eqs
mshell = nshell - kshell*1j
mcore = ncore - kcore*1j
mhom = nhom - khom*1j

# psd
psd = np.arange(1, 101, 1)
deltad=1
deltadm=1
theta901 = np.arange(0, 90.1, 0.1) # length 901

# angles for VSF
nang=901
angles=np.cos(np.deg2rad(theta901)) # length 901
theta1 = np.deg2rad(theta901) 
theta2 = np.flipud(np.pi-np.deg2rad(theta901[0:900]))
theta=np.append(theta1,theta2)

back1=np.where(theta==(np.pi/2)) 
back2=np.where(theta==(np.pi))
d1=np.diff(theta)
dtheta = np.append(d1, d1[0])

# preparing variables to be filled
VSF = np.zeros((len(D_eff),len(l), 1801))   #dimensions jjj(deff), nii(wavelength), 1801 angles    
PF_check = np.zeros((len(D_eff),len(l)))
d_alpha = []  
PF = np.zeros((len(D_eff), len(wavelength), 1801))
psdv = np.zeros((len(D_eff))) # cell volume
Cc = np.zeros((len(D_eff))) # carbon content mass

# declare all lists and arrays to fill in the jjj loop (refilled each iteration)
Qc, Sigma_c, c, Qb, Sigma_b, b, Qa, Sigma_a, a, Qbb, Sigma_bb, bb, bbtilde = (np.zeros([len(D_eff),len(l)]) for i in range(13))
a_sol, a_solm, Qastar2_dir, Qas21 = (np.zeros([len(D_eff),len(l)]) for i in range(4))

for nii in np.arange(0,len(l)): # this is the wavelength loop
    print(nii)

    # declare lists to be filled on each iteration of the psd loop
    II, phaseMB, alpha, bbprob, bbprob1, Qbbro, checkMB, Qbro, Qcro, M1 = ([] for i in range (10))
    

    for jj in np.arange(0, len(psd)): # this is the psd loop

        [QEXT,QSCA,GQSC,QBS,m1,m2,s21,d21] = Dmmex_R14B_4.dmilay((psd[jj]*FR)/2,psd[jj]/2,wvno[nii],mshell[nii],mcore[nii],angles,901,901)
    
        # on each iteration of jj, we get a different QEXT and QSCA out. So these must be stored in their own array
        Qcro.insert(jj,QEXT) 
        Qbro.insert(jj,QSCA)    
        
        m1_seta = [num[0] for num in m1]
        m1_setb = [num[1] for num in m1]
        M1 = np.append(m1_seta,m1_setb[900:0:-1])
        M2 = np.append(m2[0:901,0], m2[900:0:-1,1])
        myval = (M1+M2)/2 
        II.insert(jj, myval) 
        
        alpha2=2*np.pi*(psd[jj]/2)/wavelength[nii] 
        alpha.insert(jj, alpha2) 

        phaseMB_jj = [II[jj] / (np.pi* Qbro[jj]* (alpha[jj]**2))]
        phaseMB.insert(jj,phaseMB_jj)

        checkMB_jj = [2* np.pi* np.sum(phaseMB_jj * np.sin(theta) * dtheta)]
        checkMB.insert(jj,checkMB_jj)

        section_jj = [item[900:1801] for item in phaseMB_jj]
        bbprob_jj = 2*np.pi* np.sum((section_jj *np.sin(theta[900:1801]) *dtheta[900:1801]))
        bbprob.insert(jj, bbprob_jj) 
        Qbbro_jj = QSCA * bbprob_jj 
        Qbbro.insert(jj,Qbbro_jj) 
    
	# we are still in the nii loop here! just the jj loop has ended

    d_alpha_nii = alpha[1] - alpha[0]
    d_alpha.insert(nii,d_alpha_nii)

	# jjj loop starts here
    for jjj in np.arange(0,len(D_eff)):

        exponent = (-psd/ 2)/ ((D_eff[jjj]/ 2) * V_eff)
        psd2 = 1.0e20 * np.power((psd/2),((1-3* V_eff)/V_eff)) * np.exp(exponent)
        psdm1 = psd / 1e6; psdm2 = psd2 * 1e3; 
        civol = np.pi/ 6 * sum(psdm2 * psdm1 **3 * deltadm)
        psdm2 = psdm2 * (1./ (civol * ci))
        psdvol = np.pi/6 * sum(psdm2 * np.power(psdm1, 3) * deltadm)
        Cc[jjj] = psdvol * Ci
        psdv[jjj] = psdvol
        
        Qc[jjj, nii] = sum(Qcro *psdm2 * np.power(psdm1,2) * deltadm)/ sum(psdm2 * np.power(psdm1,2) *deltadm)
        Sigma_c[jjj,nii] = np.pi/4 * Qc[jjj, nii] * sum(np.power(psdm1, 2) * deltadm)
        c[jjj,nii] = np.pi/4* Qc[jjj, nii]* sum(psdm2* np.power(psdm1,2)* deltadm)
        
        Qb[jjj, nii] = sum(Qbro * psdm2 * np.power(psdm1,2) * deltadm) /sum(psdm2* np.power(psdm1,2)* deltadm) 	            
        Sigma_b[jjj,nii] = np.pi/4 * Qb[jjj,nii]* sum(np.power(psdm1,2)* deltadm)
        b[jjj, nii] = np.pi/4* Qb[jjj, nii]* sum(psdm2* np.power(psdm1,2)* deltadm)

        Qbb[jjj, nii] = sum(Qbbro * psdm2 * np.power(psdm1,2) * deltadm) /sum(psdm2* np.power(psdm1,2)* deltadm)
        Sigma_bb[jjj, nii] = np.pi/4 * Qbb[jjj, nii] * sum(np.power(psdm1, 2) * deltadm)
        bb[jjj, nii] =  np.pi/4* Qbb[jjj, nii]* sum(psdm2 * np.power(psdm1, 2) * deltadm)
        
        Qa[jjj, nii] = Qc[jjj, nii] - Qb[jjj, nii]
        Sigma_a[jjj, nii] = np.pi/4 * Qa[jjj, nii]* sum(np.power(psdm1,2)* deltadm)
        a[jjj, nii] = c[jjj, nii] - b[jjj, nii]

        betabar, VSF_1 = ([] for i in range(2))
        checkbar = []
        b_check, bb_check = (np.zeros((len(D_eff),len(wavelength))) for i in range(2))
        
        bbtilde[jjj, nii] = bb[jjj, nii] / b[jjj, nii]
			
		# this little sub loop is INSIDE the jjj loop		
        for ai in range (0, nang * 2 - 1): # this should go 1801 times - doesn't include the last in range  
    		   # need a variable to get(II(:,ai)):
            varII = [item[ai] for item in II]
            betabar_ai = (1 / np.pi) * (sum(varII * psdm2 * d_alpha[nii]) / sum(Qbro * psdm2 * np.power(alpha, 2) * d_alpha[nii]))
            betabar.insert(ai, betabar_ai)
            VSF_1_ai = betabar[ai] * b[jjj, nii]  
            VSF_1.insert(ai, VSF_1_ai) # this gives VSF_1 of 1801 angles. For the current instance of nii (wavelength) and jjj (Deff)

        # checkbar is back outside of the sub loop
        checkbar = (2* np.pi * sum(betabar * np.sin(theta) * dtheta))
        PF_check[jjj,nii] = checkbar
        
        b_check[jjj,nii] = 2 * np.pi * sum((VSF_1) * np.sin(theta) * dtheta)
        
        PF[jjj,nii,:] = betabar
        VSF[jjj,nii,:] = VSF_1 # VSF_1s are put into matrix on each iteration of Deff, then wavelength.
        # We want to get out all wavelengths but backscatter only angles for each Deff:
            
        slice_obj = slice(900, 1801) 
        VSF_b = VSF[jjj, nii, slice_obj] # want to get the backward angles for this instance of Deff and all the wavelengths 
        bb_check[jjj,nii] = 2 * np.pi * sum((VSF_b) * np.sin(theta[900: 1801]) * dtheta[900: 1801])      
        
        ## Package effect calculations:
	
        ##Set up all phase lag and optical thickness parameters
        ##Calculate acm (absorption celular material) for all layers
        acm_core = (4 * np.pi * kcore[nii]) / (wavelength[nii] * 1e-6)
        acm_shell=(4 * np.pi * kshell[nii]) / (wavelength[nii] * 1e-6)
        acm_hom = (4 * np.pi * khom[nii]) / (wavelength[nii] * 1e-6)
        q = (D_eff[jjj] / 2 * FR) / (D_eff[jjj] / 2)

        Qas21[jjj, nii] = 3 / 2 * (Qa[jjj, nii] / (acm_core * np.power(q, 3) + acm_shell * (1 - np.power(q, 3)) * 1e-6 * D_eff[jjj]))
      
        ##Direct volume equivalent determination of package effect
        a_sol[jjj, nii] = psdvol * Vc * acm_core + psdvol * Vs * acm_shell
        a_solm[jjj, nii] = psdvol * acm_hom
        Qastar2_dir[jjj,nii] = a[jjj, nii] / a_sol[jjj, nii] #Hayley for input into fluorescence algorithm
      
 	    # both the jjj loop and the nii loop end here.
             
#    return a, b, bb, VSF, VSF_b, bbtilde, theta

#%% VSF and PF
from scipy.signal import savgol_filter
from scipy.interpolate import splrep, splev

theta2 = np.rad2deg(theta)
vsf440 = VSF[0,8,:]
vsf660 = VSF[0,52,:]

fig, ax = plt.subplots()
ax.plot(theta2, vsf440, label='440nm')
ax.plot(theta2, vsf660, label='660nm')
# ax.plot(theta2,y_filt, label='svgol')
# ax.plot(theta2, y_hat, label='spline')
ax.set_yscale('log')
ax.set_xlabel('Degrees')
ax.set_ylabel('\u03B2 ($m^{-1} sr^{-1}$)')
ax.legend()
#fig.savefig('/Users/jakravit/Desktop/VSF.png',bbox_inches='tight',dpi=300)


pf440 = PF[0,8,:]
pf660 = PF[0,52,:]

fig, ax = plt.subplots()
ax.plot(theta2, pf440, label='440nm')
ax.plot(theta2, pf660, label='660nm')
ax.set_yscale('log')
ax.set_xlabel('Degrees')
ax.set_ylabel('phase func ($m^{-1} sr^{-1}$)')
ax.legend()

#%% VSF integration to b

# 440 nm 
slice_obj = slice(900, 1801) 
VSF_bb = VSF[0, 8, slice_obj] # want to get the backward angles for this instance of Deff and all the wavelengths 
bb_check = 2 * np.pi * sum((VSF_bb) * np.sin(theta[900: 1801]) * dtheta[900: 1801])  

VSF_b = VSF[0,8,:]
b_check = 2 * np.pi * sum((VSF_b) * np.sin(theta) * dtheta)

#%% smooth VSF 

bvsf = []
bbvsf = []
bsav = []
bbsav = []
bspl = []
bbspl = []

for i,k in enumerate(l):
    vsf = VSF[0,i,:]
    y_sav = savgol_filter(vsf, 101, 1)
    bspl = splrep(theta2, vsf, s=.5)
    y_spl = splev(theta2,bspl)
    
    # bb
    # unfiltered
    slice_obj = slice(900, 1801) 
    vsf_bb = vsf[slice_obj] 
    bbvsf.append( 2 * np.pi * sum((vsf_bb) * np.sin(theta[900: 1801]) * dtheta[900: 1801]))  
    # savgol
    vsf_sav_bb = y_sav[slice_obj]
    bbsav.append( 2 * np.pi * sum((vsf_sav_bb) * np.sin(theta[900: 1801]) * dtheta[900: 1801]))
    # spline
    vsf_spl_bb = y_spl[slice_obj]
    bbspl.append( 2 * np.pi * sum((vsf_spl_bb) * np.sin(theta[900: 1801]) * dtheta[900: 1801]))
    
    # b
    # unfiltered
    bvsf.append(2 * np.pi * sum((vsf) * np.sin(theta) * dtheta))    
    # svgol
    bsav.append(2 * np.pi * sum((y_sav) * np.sin(theta) * dtheta))
    # spline
    #bspl.append(2 * np.pi * sum((y_spl) * np.sin(theta) * dtheta)) 


fig, ax = plt.subplots()
ax.plot(l, bbvsf, label='unfilt')
#ax.plot(theta2, vsf660, label='660nm')
ax.plot(l, bbsav, label='svgol')
ax.plot(l, bbspl, label='spline')
#ax.set_yscale('log')
#ax.set_xlabel('Degrees')
#ax.set_ylabel('\u03B2 ($m^{-1} sr^{-1}$)')
ax.legend()           
