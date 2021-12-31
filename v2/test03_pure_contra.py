# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 19:52:31 2021

@author: Sebastian
"""

from load_data import load_xdf_file, get_chan_of_interest
from handle_cmc import calc_cmc_epoched
from plot_figure import plot



if __name__ == '__main__':

    file = r"D:\Sebastian\Medizin\Doktorarbeit\Software\Github-Repos\cmc-test\data\right_30.xdf"
    epoche_dur = 10
    emg_idx = [9]
    
    EDC_Epochs, EEG_Epochs, sampling_rate, channel_names = load_xdf_file(file, epoche_dur, emg_idx, clean_EEG=True)
    
    
    C3 = get_chan_of_interest(EEG_Epochs, "C3", channel_names)
    
    
    
    # contraction only
    import numpy as np
    wct, awct, freq = calc_cmc_epoched(list(np.array(EDC_Epochs)[:, 2*sampling_rate:4*sampling_rate]), \
                                       list(np.array(C3)[:, 2*sampling_rate:4*sampling_rate]), sampling_rate)
    plot(EDC_Epochs[0], C3[0], np.mean(wct, axis=0), awct, np.mean(freq, axis=0), "Contraction only")