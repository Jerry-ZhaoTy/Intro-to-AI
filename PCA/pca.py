# -*- coding: utf-8 -*-
"""
Created on Oct 2020

@author: Tianyi Zhao
"""

import numpy as np
import scipy.linalg
import matplotlib.pyplot

def load_and_center_dataset(filename):
    x = np.load(filename)  
    x = np.reshape(x,(2000,784))
    x = x - np.mean(x, axis=0)
    return x

def get_covariance(dataset):
    S = np.dot(np.transpose(dataset), dataset)/(len(dataset)-1)
    return S
    
def get_eig(S, m):
    w, v = scipy.linalg.eigh(S)
    w = w[-m:]
    v = v[:,-m:]
    w = np.flip(w)
    v = np.flip(v)
    return np.diag(w), v

def get_eig_perc(S, perc):
    w, v = scipy.linalg.eigh(S)
    sum = np.sum(w)
    i = len(w) - 1
    while(w[i]/sum > perc):
        i-=1    
    w = w[-(len(w)-i-1):]
    v = v[:, -(len(v)-i-1):]
    w = np.flip(w)
    v = np.flip(v)
    return np.diag(w), v
    
def project_image(image, U):
    a = np.dot(np.transpose(U)[0], image)
    xP = np.dot(a, U[:,0])
    project_image = xP
    for i in range (1, len(U[0])):
        a = np.dot(np.transpose(U)[i], image)
        xP = np.dot(a, U[:,i])
        project_image += xP
    return xP
    
def display_image(orig, proj):
    orig = np.reshape(orig,(28,28))
    proj = np.reshape(proj,(28,28))
    fig, axs = matplotlib.pyplot.subplots(nrows=1, ncols=2, figsize = (9,3))
    axs[0].set_title('Original')
    axs[0].imshow(orig, aspect='equal', cmap='gray')
    axs[1].set_title('Projection')
    axs[1].imshow(proj, aspect='equal', cmap='gray')
    fig.colorbar(matplotlib.cm.ScalarMappable(cmap='gray'), ax=axs[0])
    fig.colorbar(matplotlib.cm.ScalarMappable(cmap='gray'), ax=axs[1])
    
    

















