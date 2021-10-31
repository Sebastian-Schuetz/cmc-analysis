# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 09:45:22 2021

@author: Sebastian
"""
from test_data_gen import gen_random_signal
from analyse_data import calc_cmc, calc_cmc_epoched
from data_plot import plot
import matplotlib as mpl


# Coherence of random signals
def random_test_signal(duration, sampling_rate, name):
    """
    Calculates the wavelet-Coh between two random signals, using the whole 
    signal, without added epochs

    Parameters
    ----------
    duration : TYPE
        DESCRIPTION.
    sampling_rate : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    sig1 = gen_random_signal(duration, sampling_rate)
    sig2 = gen_random_signal(duration, sampling_rate)
    wct, awct, freq = calc_cmc(sig1, sig2, sampling_rate)
    return plot(sig1, sig2, wct, awct, freq, name)
    

def random_test_signal_epoched(duration, sampling_rate, epochs, name):
    """
    Calculates the wavelet coherence using our epoched approach

    Parameters
    ----------
    duration : TYPE
        DESCRIPTION.
    sampling_rate : TYPE
        DESCRIPTION.
    epochs : TYPE
        DESCRIPTION.
    name : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    epochs1 = [gen_random_signal(duration, sampling_rate) for i in range(epochs)]
    epochs2 = [gen_random_signal(duration, sampling_rate) for i in range(epochs)]

    wct, awct, freq = calc_cmc_epoched(epochs1, epochs2, sampling_rate)
    return plot(epochs1[0], epochs2[0], wct, awct, freq, name)


if __name__ == "__main__":
    fig_random_short =      random_test_signal(10, 1000, "random - whole signal (short)")
    fig_random_long =       random_test_signal(100, 1000, "random - whole signal (long)")
    fig_random_5_epoche =   random_test_signal_epoched(10, 1000, 5, "random - 5 Epochs")
    fig_random_20_epoche =  random_test_signal_epoched(10, 1000, 20, "random - 20 Epochs")
    
    
    i = 0
    mpl.rcParams['agg.path.chunksize'] = 10000 # needed for saving. Hard coded limit in agg backend (see: https://github.com/matplotlib/matplotlib/issues/5907)
    for f in fig_random_short:
        f.savefig("./plots/baseline/" + "random_" + f'{i:02d}'+".png", dpi=1200)
        i += 1
    for f in fig_random_long:
        f.savefig("./plots/baseline/" + "random_" + f'{i:02d}'+".png", dpi=1200)
        i += 1
    for f in fig_random_5_epoche:
        f.savefig("./plots/baseline/" + "random_" + f'{i:02d}'+".png", dpi=1200)
        i += 1
    for f in fig_random_20_epoche:
        f.savefig("./plots/baseline/" + "random_" + f'{i:02d}'+".png", dpi=1200)
        i += 1