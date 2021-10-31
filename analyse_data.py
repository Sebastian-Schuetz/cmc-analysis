# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 09:37:10 2021

@author: Sebastian
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import signal,stats
from mne.filter import filter_data
import numpy as np
import scipy as sp
from scipy import signal, stats
from mne.filter import filter_data, notch_filter



import pycwt as wavelet

from joblib import Parallel, delayed
import multiprocessing

def calc_cmc(chan1, chan2, sampling_rate, dj=0.05, s0=-1, J=-1, f0=6, deltaj0=0.6):
    """
    

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
        Morlet wave number. For the Morlet wavelet. The default is 6.
    deltaj0 : TYPE, optional
        Factor for scale averaging. For the Morlet wavelet. The default is 0.6.

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


def calc_cmc_epoched(epochs1, epochs2, sampling_rate, dj=0.05, s0=-1, J=-1, f0=6, deltaj0=0.6):
    wct_ =  []
    awct_ = []
    freq_ = []
    for e1, e2 in zip(epochs1, epochs2):
        wct, awct, freq = calc_cmc(e1, e2, sampling_rate, dj, s0, J, f0=6, deltaj0=0.6)
        wct_.append(wct)
        awct_.append(awct)
        freq_.append(freq)
    
    return np.mean(wct_, axis=0), np.mean(awct_, axis=0), np.mean(freq_, axis=0)
    