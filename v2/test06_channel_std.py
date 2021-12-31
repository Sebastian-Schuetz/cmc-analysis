# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 11:18:54 2021

@author: Sebastian
"""

from load_data import load_xdf_file, get_chan_of_interest
from handle_cmc import calc_cmc, calc_cmc_epoched
from plot_figure import plot



if __name__ == '__main__':

    file = r"D:\Sebastian\Medizin\Doktorarbeit\Software\Github-Repos\cmc-test\data\right_30.xdf"
    epoche_dur = 10
    emg_idx = [9]
    
    chan_of_int = ["FC3", "C5", "C3", "C1", "CP3",
                   "FC4", "C6", "C4", "C2", "CP4"]
    
    EDC_Epochs, EEG_Epochs, sampling_rate, channel_names = load_xdf_file(file, epoche_dur, emg_idx, clean_EEG=True)
    
    
    EEGoi = []
    for coi in chan_of_int:
        EEGoi.append(get_chan_of_interest(EEG_Epochs, coi, channel_names))
    
    
    # Calculates the CMC over the STD of the channels with 20 Epochs
    import numpy as np
    EEGstd = np.std(EEGoi, axis=0)
    wct, awct, freq = calc_cmc_epoched(EDC_Epochs, EEGstd, sampling_rate)
    plot(EDC_Epochs[0], EEGstd[0], np.mean(wct, axis=0), awct, np.mean(freq, axis=0), "STD over channels")
    
    
    # Calculates the CMC of the std of one channel (C3), over 20 Epochs
    EDCstd = np.std(EDC_Epochs, axis=0)
    EDCstd = np.mean(EDC_Epochs, axis= 0)
    C3std =  np.std(EEGoi, axis=1)[2]
    C3std =  np.mean(EEGoi, axis=1)[2]
    wct, awct, freq = calc_cmc(EDCstd, C3std, sampling_rate)
    plot(EDCstd, C3std, wct, awct, freq, "STD of one channel + std of EDC over 20 Eochs")
    
    
    # Calculates the CMC of the std of one channel and the mean of the EDC
    EDCstd = np.mean(EDC_Epochs, axis= 0)
    C3std =  np.std(EEGoi, axis=1)[2]
    wct, awct, freq = calc_cmc(EDCstd, C3std, sampling_rate)
    plot(EDCstd, C3std, wct, awct, freq, "STD of one channel + mean of EDC over 20 Eochs")
    
    # Calculates the CMC of the mean of one channel and the mean of the EDC
    EDCstd = np.mean(EDC_Epochs, axis= 0)
    C3std =  np.mean(EEGoi, axis=1)[2]
    wct, awct, freq = calc_cmc(EDCstd, C3std, sampling_rate)
    plot(EDCstd, C3std, wct, awct, freq, "Mean of one channel over 20 Eochs")