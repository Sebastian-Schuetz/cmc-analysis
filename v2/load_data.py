# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 18:10:33 2021

@author: Sebastian
"""
import mne
import liesl
import numpy as np
from pyprep.find_noisy_channels import NoisyChannels

def load_xdf_file(path, epoche_dur, emg_idx=[9], clean_EEG=True):
    """
    Loads an xdf file and returns the (optional) filterd data, cut 
    in epochs

    Parameters
    ----------
    path : TYPE
        DESCRIPTION.
    epoche_dur : TYPE
        DESCRIPTION.
    emg_idx : TYPE, optional
        DESCRIPTION. The default is [9].
    clean_EEG : TYPE, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    EDC_epochs : TYPE
        DESCRIPTION.
    EEG_epochs : TYPE
        DESCRIPTION.
    sampling_rate : TYPE
        DESCRIPTION.
    channel_labels : TYPE
        DESCRIPTION.

    """

    streams = liesl.XDFFile(path)
    marker = streams['reiz-marker']
    contracttimes = [marker.time_stamps[i] for i,v in enumerate(marker.time_series) if \
                v[0] == "anspannen"]
    eegocontracttimes = [np.argmin(np.abs(streams['eego'].time_stamps - ts)) for ts in contracttimes]    
    
    
    sampling_rate = int(streams['eego'].nominal_srate)
    channel_labels = streams['eego'].channel_labels[:64]
    
    EEG = streams['eego'].time_series[:,:64].astype(float)
    
    if clean_EEG:
        EEG = np.asarray(EEG,dtype = np.float64)
        EEG = mne.filter.notch_filter(EEG.T,sampling_rate,50)
    
    edc = streams['eego'].time_series[:,63+np.array(emg_idx)].astype(float)

        
    if type(epoche_dur) != tuple:
        epoche_dur = (0, epoche_dur)

    EDC_epochs = []
    EEG_epochs = []
    for ts in eegocontracttimes:
        EDC_epochs.append(np.squeeze(edc[ts+sampling_rate*epoche_dur[0]:ts+sampling_rate*epoche_dur[1], :]))
        
        if clean_EEG:
            info = mne.create_info(channel_labels, sfreq = sampling_rate, ch_types = "eeg")
            info.set_montage('standard_1020')
            raw = mne.io.RawArray(EEG[:, ts+sampling_rate*epoche_dur[0]:ts+sampling_rate*epoche_dur[1]], info)

            nd = NoisyChannels(raw)
            nd.find_bad_by_correlation()
            nd.find_bad_by_hfnoise()
            nd.find_bad_by_deviation()
            print("Bad channels: ",nd.get_bads())
            
            raw.info['bads'] = nd.get_bads()
            raw.interpolate_bads()

            
            raw.set_eeg_reference(ref_channels='average')
            # perform surface laplacian
            raw = mne.preprocessing.compute_current_source_density(raw)
            EEG_epochs.append(raw._data.T)
        else:
            EEG_epochs.append(np.squeeze(EEG[ts+sampling_rate*epoche_dur[0]:ts+sampling_rate*epoche_dur[1], :]))
    
    return EDC_epochs, EEG_epochs, sampling_rate, channel_labels


def get_chan_of_interest(EEG_Epochs, chan_of_int, chan_names):
    """
    Returns the corresponding EEG Channel

    Parameters
    ----------
    EEG_Epochs : TYPE
        DESCRIPTION.
    chan_of_int : TYPE
        DESCRIPTION.
    chan_names : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    ind = chan_names.index(chan_of_int)
    return list(np.array(EEG_Epochs)[:,:,ind])


if __name__ == "__main__":
    path = r"D:\Sebastian\Medizin\Doktorarbeit\Software\Github-Repos\cmc-test\data\right_30.xdf"
    EDC, EEG, fs, names = load_xdf_file(path, 10)