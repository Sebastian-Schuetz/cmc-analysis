# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 19:55:57 2021

@author: Sebastian
"""

from load_data import load_xdf_file, get_chan_of_interest
from handle_cmc import calc_cmc_epoched
from plot_figure import plot



if __name__ == '__main__':

    file = r"D:\Sebastian\Medizin\Doktorarbeit\Software\Github-Repos\cmc-test\data\right_30.xdf"
    epoche_dur = 10
    emg_idx = [9]
    
    chan_of_int = ["FC3", "C5", "C3", "C1", "CP3",
                   "FC4", "C6", "C4", "C2", "CP4"]
    
    EDC_Epochs, EEG_Epochs, sampling_rate, channel_names = load_xdf_file(file, epoche_dur, emg_idx, clean_EEG=True)
    
    
    _wct =  []
    _freq = []
    for coi in chan_of_int:
        C = get_chan_of_interest(EEG_Epochs, coi, channel_names)
        
        import numpy as np
        wct, awct, freq = calc_cmc_epoched(EDC_Epochs, C, sampling_rate)
        _wct.append(np.mean(wct, axis=0))
        _freq.append(np.mean(freq, axis=0))
        #plot(EDC_Epochs[0], C[0], np.mean(wct, axis=0), awct, np.mean(freq, axis=0), coi)
    
    plot(EDC_Epochs[0], C[0], np.mean(_wct, axis=0), np.mean(_wct, axis=0), np.mean(_freq, axis=0), "Total average")
    plot(EDC_Epochs[0], C[0], np.mean(_wct[:5], axis=0), np.mean(_wct, axis=0), np.mean(_freq, axis=0), "FC3 bis CP3")
    plot(EDC_Epochs[0], C[0], np.mean(_wct[5:], axis=0), np.mean(_wct, axis=0), np.mean(_freq, axis=0), "FC4 bis CP4")