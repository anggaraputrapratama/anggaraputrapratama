#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 11:36:53 2021

@author: pi
"""

# Library 
from timeit import default_timer as timer
start = timer()

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
import sklearn.metrics as metrics
from scipy.fft import fft,ifft
#np.set_printoptions(precision=17, suppress=True)

# Dataset
toe = np.genfromtxt('BT50.txt', delimiter=',') #Toeplitz Matrix
eeg = np.genfromtxt('eeg.txt', delimiter=',') #dataset 256 sample eeg

# Prerequisites Process
N = len(eeg) #panjang dataset
A = toe  #Toeplitz Matrix
x = fft(eeg) #Input
y = np.dot(A,x) #Compressive Sensing
def f(x):  #function handle
    return np.dot(A,x)

# Reconstruction Process
D = np.zeros((len(eeg),len(eeg)), dtype=complex) #Make zeros nxn dimensional array from length dataset
[p, d] = D.shape
def g(x):
    return (y-f(x))
def fun2 (g,D,x):
    return np.concatenate([g(x),np.dot(-D,x)]) 
def myfun(x):
    q = fun2(g,D,x)[0:len(fun2(g,D,x))].real + 1j*fun2(g,D,x)[0:len(fun2(g,D,x))].imag
    return q.real+q.imag
o = np.random.uniform(1,0,p)
xr = least_squares(myfun, o, bounds=(- np.inf, np.inf),verbose=2, method='trf')
n1 = np.linalg.norm(y-f(x))
supp = np.arange(p)
j = 1

while (j<=N and n1>10**3):
    c=np.dot(D,x)
    i=np.where(c ==max(np.abs (c)))
    supp=np.delete(supp,i)
    myfun(g,D,x)
    xr = least_squares(myfun,o,bounds=(- np.inf, np.inf), verbose=2,method='trf')
    j=j+1
    n1 = np.linalg.norm(y-f(A,x)) 
  
xy=xr.x+xr.x*1j
xy.shape

inv_fft = ifft(xy)
real_num = inv_fft.real
real_num.shape

fig, axs = plt.subplots(3, figsize=(20,15))


fig.suptitle('Reconstruction')
axs[0].plot(eeg,label='Original dataset')
axs[0].title.set_text('Original Dataset')
axs[0].set_ylabel('Amplitudo')
axs[0].set_xlabel('Panjang Sample')
axs[0].legend()
axs[0].grid()
fig.tight_layout(pad=3.2)


axs[1].plot(real_num, color='xkcd:orange', label='Greedy Analysis Pursuit')
axs[1].title.set_text('Greedy Analysus Pursuit (reconstructed)')
axs[1].set_ylabel('Amplitudo')
axs[1].set_xlabel('Panjang Sample')
axs[1].grid()
axs[1].legend()


axs[2].plot(eeg,marker = 'o',label='Original')
axs[2].plot(real_num,marker = '*',label = 'Greedy Analysus Pursuit')
axs[2].set_ylabel('Amplitudo')
axs[2].set_xlabel('Panjang Sample')
axs[2].grid()
axs[2].legend()

#Parameter Performansi(MAPE, MSE)
abseeg = max(np.abs(eeg))
mae = metrics.mean_absolute_error(eeg, real_num)
mape = (mae/abseeg)
mse = metrics.mean_squared_error(eeg, real_num)
rmse = np.sqrt(mse) # or mse**(0.5)  
r2 = metrics.r2_score(eeg, real_num)

print("Results of sklearn.metrics:")
print("MAE:",mae)
print("MAPE", mape)
print("MSE:", mse)
print("RMSE:", rmse)
print("R-Squared:", r2)

end = timer()
print("Processing Time: ",end - start,'second')