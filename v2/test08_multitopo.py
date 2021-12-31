# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 09:22:56 2021

@author: Sebastian
"""

import numpy as np
from load_data import load_xdf_file, get_chan_of_interest
from handle_cmc import calc_cmc_epoched_welch

from plot_figure import plot_topomaps, plot_coh_over_freq_welch


chansel=[
'Fp1',
 'Fpz',
 'Fp2',
 'F7',
 'F3',
 'Fz',
 'F4',
 'F8',
 'FC5',
 'FC1',
 'FC2',
 'FC6',
 'C3',
 'Cz',
 'C4',
 'CP5',
 'CP1',
 'CP2',
 'CP6',
 'P3',
 'Pz',
 'P4',
 'POz',
 'AF7',
 'AF3',
 'AF4',
 'AF8',
 'F5',
 'F1',
 'F2',
 'F6',
 'FC3',
 'FCz',
 'FC4',
 'C5',
 'C1',
 'C2',
 'C6',
 'CP3',
 'CPz',
 'CP4',
 'P5',
 'P1',
 'P2',
 'P6',
 'PO3',
 'PO4',
 'PO6']


if __name__ == '__main__':

    
    fmin = 12
    fmax = 30
    
    #file = r"D:\Sebastian\Medizin\Doktorarbeit\Software\Github-Repos\cmc-test\data\right_30.xdf"
    file = r"D:\Sebastian\Medizin\Doktorarbeit\Software\Github-Repos\cmc-test\data\G005_d1\dominant_side_CMC_pre_R001.xdf"
    epoche_dur = (1, 9)
    emg_idx = [9]
    
    EDC_Epochs, EEG_Epochs, sampling_rate, channel_names = load_xdf_file(file, epoche_dur, emg_idx, clean_EEG=True)
    
    wcts = []
    for chan in chansel:
        C3 = get_chan_of_interest(EEG_Epochs, chan, channel_names)
        wct, freq = calc_cmc_epoched_welch(EDC_Epochs, C3, sampling_rate)
        wcts.append(np.mean(wct, axis=0))
    
    
    
    freqs = np.mean(freq, axis=0)
    freq_of_int = np.where(np.logical_and(freqs>=fmin, freqs<=fmax))[0]    
    
    
    plot_topomaps(np.array(wcts)[:, freq_of_int].T, freqs[freq_of_int], chansel, 5, 2, (0, 0.07))
    
    plot_coh_over_freq_welch(np.array(wcts)[chansel.index("C3"), :], freqs,
                             "C3", fmin, fmax, True)