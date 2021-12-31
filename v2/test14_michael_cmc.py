# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 10:34:14 2021

@author: Sebastian
"""

import mne
import liesl
import numpy as np
from pyprep.find_noisy_channels import NoisyChannels
import matplotlib.pyplot as plt

def load_file(path, edcix=9, c3ix=14):
    streams = liesl.XDFFile(path)
    sampling_rate = int(streams['eego'].nominal_srate)
    channel_labels = streams['eego'].channel_labels[:64]
    
    
    edcdat = streams['eego'].time_series[:,63+edcix]*1e6
    edcdat = mne.filter.notch_filter(edcdat.astype('float64'),sampling_rate,freqs=(50,100,150,200), method = 'spectrum_fit', verbose = 0) 

    c3dat = streams['eego'].time_series[:,c3ix]*1e6
    c3dat = mne.filter.notch_filter(c3dat.astype('float64'),sampling_rate,freqs=(50,100,150,200), method = 'spectrum_fit', verbose = 0)
    return edcdat, c3dat, sampling_rate

def calc_cmc(signal1, signal2, show_plot, sf, foi=(2,40)):
    if show_plot: 
        plt.figure()
        coh, f = plt.cohere(signal1, signal2, NFFT=int((2/foi[0])*sf), Fs=sf)
        plt.xlabel('frequency [Hz]')
        plt.ylabel('Coherence')
        plt.title('CMC between C3 and EDC_R')
        plt.xlim(foi[0], foi[1])
        plt.show()



if __name__ == "__main__":
    #path = r"D:\Sebastian\Medizin\Doktorarbeit\Software\Github-Repos\cmc-test\data\G005_d1\dominant_side_CMC_pre_R001.xdf"
    path = r"D:\Sebastian\Medizin\Doktorarbeit\Software\Github-Repos\cmc-test\data\G005_d1\sub_cond_0_slalom_pre_R001.xdf"
    
    edc, c3, sf = load_file(path)
    calc_cmc(edc, c3, True, sf)