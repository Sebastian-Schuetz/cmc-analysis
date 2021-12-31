# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 11:32:28 2021

@author: Sebastian
"""

import numpy as np
from load_data import load_xdf_file, get_chan_of_interest
from handle_cmc import calc_cmc_epoched

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
    
    window_len = 2
    
    #file = r"D:\Sebastian\Medizin\Doktorarbeit\Software\Github-Repos\cmc-test\data\right_30.xdf"
    file = r"D:\Sebastian\Medizin\Doktorarbeit\Software\Github-Repos\cmc-test\data\G005_d1\dominant_side_CMC_pre_R001.xdf"
    epoche_dur = 15
    emg_idx = [9]
    
    EDC_Epochs, EEG_Epochs, sampling_rate, channel_names = load_xdf_file(file, epoche_dur, emg_idx, clean_EEG=True)
    
    c3_coh = []
    
    for i in range(11):
        
        start = i * sampling_rate
        
        edc_e = np.array(EDC_Epochs)[:, start:start + window_len*sampling_rate]
        eeg_e = np.array(EEG_Epochs)[:, start:start + window_len*sampling_rate, :]
        
        edc_e = [edc_e[i, :] for i in range(len(edc_e))]
        eeg_e = [eeg_e[i, :, :] for i in range(len(eeg_e))]
    
        wcts = []
        chansel = ["C3"]
        for chan in chansel:
            C3 = get_chan_of_interest(eeg_e, chan, channel_names)
            wct, awct, freq = calc_cmc_epoched(edc_e, C3, sampling_rate)
            wcts.append(np.mean(np.mean(wct, axis=0), axis=1))
    
        freqs = np.mean(freq, axis=0)
        freq_of_int = np.where(np.logical_and(freqs>=fmin, freqs<=fmax))[0]    
        
        # plot_topomaps(np.array(wcts)[:, freq_of_int].T, freqs[freq_of_int], chansel, 5, 4, (0.3, 0.5), name="Shifted by " + str(i),
        #               path = r"D:\Sebastian\Medizin\Doktorarbeit\Software\Github-Repos\cmc-analysis\plots\topo_maps_wave\\" +"post_" +  str(i) + ".png")
        
        # plot_coh_over_freq_welch(np.array(wcts)[chansel.index("C3"), :], freqs,
        #                           "C3_post - Shifed by: " + str(i), fmin, fmax, True)
        
        c3_coh.append(np.array(wcts)[chansel.index("C3"), :])
        
    plot_coh_over_freq_welch(np.mean(c3_coh, axis=0), freqs, "C3 - avg", fmin, fmax, True)    
    freq_of_int = np.where(np.logical_and(np.mean(freq, axis=0)>=fmin, np.mean(freq, axis=0)<=fmax))[0]
    coh_of_int = [c[freq_of_int] for c in c3_coh]
    
    