#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 13:44:20 2022

@author: troyobernolte
"""
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from astrodendro import Dendrogram


#Importing image data
image_file = 'data/cleanimage.G10.99.SiO.12m.7m.combined.image.mom0.fits'
image_data = fits.getdata(image_file, ext=0)

def get_info():
    """Finding the average noise level in the data"""
    data_array = []
    layer = image_data[0][0]
    #First calculate the mean noise level
    for x in range(400,500):
        for y in range(400,500):
            data_array.append(layer[x][y])
    data = np.array(data_array)
    mean_noise = np.mean(data)
    
    #Now calculate standard deviation within actual data
    data_array = []
    for x in range(100, 400):
        for y in range(90, 410):
            data_array.append(layer[x][y])
    noise_data = np.array(data_array)
    standard = np.std(noise_data)
    return(mean_noise, standard)

info = get_info()
standard = info[1]
mean_noise = info[0]

#Made a dendrogram with the min value being the general mean noise + one sand
#deviation and a min_delta of the standard deviation within the actual data
d = Dendrogram.compute(image_data, min_value= mean_noise + standard, min_delta = standard,
                       min_npix=10)
trunk = d.trunk 

def max_pixel():
    max_value = 0
    position = None
    peak = None
    for element in trunk:
        local_peak = element.get_peak()
        if local_peak[1] > max_value:
            max_value = local_peak[1]
            position = local_peak[0]
            peak = local_peak
    return peak


def show():
    photo_data = image_data[0][0]
    plt.figure()
    plt.imshow(photo_data, cmap='nipy_spectral', vmin = mean_noise)
    plt.colorbar()
    
def show_peak():
    photo_data = image_data[0][0]
    plt.figure()
    largest = max_pixel()
    x = largest[0][2]
    y = largest[0][3]
    plt.imshow(photo_data, cmap='nipy_spectral', vmin = mean_noise)
    circle1 = plt.Circle((x,y), 25, color = 'r', fill = False)
    fig = plt.gcf()
    ax = fig.gca()
    ax.add_patch(circle1)
    plt.colorbar()
    