# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 18:48:10 2021

@author: Sebastian

TODO: Add welch method for comparision
"""

import numpy as np
import pycwt as wavelet
from scipy import signal


def calc_cmc(chan1, chan2, sampling_rate, dj=0.05, s0=-1, J=-1, f0=20, deltaj0=0.06):
    """
    Calculates the CMC using wavelets    
    
    Parameters
    ----------
    chan1 : TYPE
        DESCRIPTION.
    chan2 : TYPE
        DESCRIPTION.
    sampling_rate : TYPE
        DESCRIPTION.
    dj : TYPE, optional
        Spacing between discrete scales. For the coherence. The default is 0.05.
    s0 : TYPE, optional
        Smallest scale of the wavelet. For the coherence. The default is -1.
    J : TYPE, optional
        Number of scales less one. For the coherence. The default is -1.
    f0 : TYPE, optional
        Morlet wave number. For the Morlet wavelet. The default is 20.
    deltaj0 : TYPE, optional
        Factor for scale averaging. For the Morlet wavelet. The default is 0.06.

    Returns
    -------
    wct : TYPE
        DESCRIPTION.
    awct : TYPE
        DESCRIPTION.
    freq : TYPE
        DESCRIPTION.

    """
    
    mother = wavelet.Morlet(f0=f0, deltaj0=deltaj0)
    try:
        wct, awct, coi, freq, sig = wavelet.wct(signal.detrend(chan1),  \
                                                signal.detrend(chan2),  \
                                                dt=1.0/sampling_rate,   \
                                                dj=dj,                \
                                                s0=s0,                  \
                                                J = J,                 \
                                                wavelet=mother, sig=False)
        print("finished epoche")
        return wct, awct, freq
    except:
        print("jumped epoche")
        return None


def calc_cmc_welch(chan1, chan2, sampling_rate):
    """
    Calculates the CMC just like Niko. Gives us a frequency, resolution of 4 Hz

    Parameters
    ----------
    chan1 : TYPE
        DESCRIPTION.
    chan2 : TYPE
        DESCRIPTION.
    sampling_rate : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    f, Cxy = signal.coherence(chan1, chan2, fs=sampling_rate, nperseg=(1/2)*sampling_rate, noverlap=(1/8)*sampling_rate)
    return f, Cxy,

def calc_cmc_epoched_welch(EDC, EEG, sampling_rate):
    _Cxy = []
    _f = []
    
    for edc, eeg in zip(EDC, EEG):
        f, Cxy = calc_cmc_welch(edc.flatten(), eeg.flatten(), sampling_rate)
        _f.append(f)
        _Cxy.append(Cxy)
        
    return _Cxy, _f

def calc_cmc_epoched(EDC, EEG, sampling_rate, dj=0.05, s0=-1, J=-1, f0=20, deltaj0=0.06):
    """
    Same as the method above, just returns the average over all the epochs

    Parameters
    ----------
    chan1 : TYPE
        DESCRIPTION.
    chan2 : TYPE
        DESCRIPTION.
    sampling_rate : TYPE
        DESCRIPTION.
    dj : TYPE, optional
        DESCRIPTION. The default is 0.05.
    s0 : TYPE, optional
        DESCRIPTION. The default is -1.
    J : TYPE, optional
        DESCRIPTION. The default is -1.
    f0 : TYPE, optional
        DESCRIPTION. The default is 20.
    deltaj0 : TYPE, optional
        DESCRIPTION. The default is 0.06.

    Returns
    -------
    None.

    """
    wct_ =  []
    awct_ = []
    freq_ = []
    
    for edc, eeg in zip(EDC, EEG):
        try:
            wct, awct, freq = calc_cmc(edc.flatten(), eeg.flatten(), sampling_rate, dj=dj, s0=-1, J=-1, f0=f0, deltaj0=deltaj0)
            #figs =  plot(edc[i], eeg[i].flatten(), wct, awct, freq, "wavelets epoched")
            wct_.append(wct)
            awct_.append(awct)
            freq_.append(freq)
        except:
            print("returned none")
    
    return wct_, awct_, freq_