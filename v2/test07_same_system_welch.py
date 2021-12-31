# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 20:46:03 2021

@author: Sebastian
"""

from load_data import load_xdf_file, get_chan_of_interest
from handle_cmc import calc_cmc_epoched_welch
from plot_figure import plot_welch_compare



if __name__ == '__main__':

    #file = r"D:\Sebastian\Medizin\Doktorarbeit\Software\Github-Repos\cmc-test\data\right_30.xdf"
    file = r"D:\Sebastian\Medizin\Doktorarbeit\Software\Github-Repos\cmc-test\data\G005_d1\dominant_side_CMC_pre_R001.xdf"
    epoche_dur = 10
    emg_idx = [9]
    
    EDC_Epochs, EEG_Epochs, sampling_rate, channel_names = load_xdf_file(file, epoche_dur, emg_idx, clean_EEG=True)
    C3 = get_chan_of_interest(EEG_Epochs, "C3", channel_names)
    wct, freq = calc_cmc_epoched_welch(EDC_Epochs, C3, sampling_rate)
    
    
    emg_idx = [11]
    ECR_Epochs, EEG_Epochs, sampling_rate, channel_names = load_xdf_file(file, epoche_dur, emg_idx, clean_EEG=True)
    C3 = get_chan_of_interest(EEG_Epochs, "C3", channel_names)
    wct2, freq2 = calc_cmc_epoched_welch(ECR_Epochs, C3, sampling_rate)
    
    file = r"D:\Sebastian\Medizin\Doktorarbeit\Software\Github-Repos\cmc-test\data\G005_d1\dominant_side_CMC_post_R001.xdf"
    epoche_dur = 10
    emg_idx = [9]
    
    EDC_Epochs, EEG_Epochs, sampling_rate, channel_names = load_xdf_file(file, epoche_dur, emg_idx, clean_EEG=True)
    C3 = get_chan_of_interest(EEG_Epochs, "C3", channel_names)
    wct3, freq = calc_cmc_epoched_welch(EDC_Epochs, C3, sampling_rate)
    
    
    emg_idx = [11]
    ECR_Epochs, EEG_Epochs, sampling_rate, channel_names = load_xdf_file(file, epoche_dur, emg_idx, clean_EEG=True)
    C3 = get_chan_of_interest(EEG_Epochs, "C3", channel_names)
    wct4, freq2 = calc_cmc_epoched_welch(ECR_Epochs, C3, sampling_rate)
    
    import numpy as np
    #plot_welch(EDC_Epochs[0], C3[0], np.mean(wct, axis=0), wct, np.mean(freq, axis=0), "Test 01 - old method")
    plot_welch_compare(np.mean(wct, axis=0),np.mean(wct2, axis=0), np.mean(wct3, axis=0),np.mean(wct4, axis=0), np.mean(freq, axis=0), "EDC - Welch", "ECR - Welch")
