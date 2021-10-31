# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 14:14:56 2021

@author: Sebastian
"""

from test_data_gen import gen_artifical_signal
from analyse_data import calc_cmc, calc_cmc_epoched
from data_plot import plot
import matplotlib as mpl


# Coherence of random signals
def artificial_test_signal(frequency, duration, sampling_rate, name, freqs, durs):
    """
    Calculates the wavelet-Coh between two signals, using the whole 
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
    sig1 = gen_artifical_signal([frequency], [duration], sampling_rate)
    sig2 = gen_artifical_signal(freqs, durs, sampling_rate)
    wct, awct, freq = calc_cmc(sig1, sig2, sampling_rate)
    return plot(sig1, sig2, wct, awct, freq, name)
    

def artificial_test_signal_epoched(frequency, duration, sampling_rate, epochs, name, freqs, durs):
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
    epochs1 = [gen_artifical_signal([frequency], [duration], sampling_rate) for i in range(epochs)]
    epochs2 = [gen_artifical_signal(freqs, durs, sampling_rate) for i in range(epochs)]

    wct, awct, freq = calc_cmc_epoched(epochs1, epochs2, sampling_rate)
    return plot(epochs1[0], epochs2[0], wct, awct, freq, name)


if __name__ == "__main__":
    fig_artificial_short =      artificial_test_signal(24, 10, 1000, "artificial - whole signal (short)", [24, 5], [5, 5])
    fig_artificial_long =       artificial_test_signal(24, 100, 1000, "artificial - whole signal (long)", [24, 5], [50, 50])
    fig_artificial_5_epoche =   artificial_test_signal_epoched(24, 10, 1000, 5, "artificial - 5 Epochs", [24, 5], [5, 5])
    fig_artificial_20_epoche =  artificial_test_signal_epoched(24, 10, 1000, 20, "artificial - 20 Epochs", [24, 5], [5, 5])
    

    
    i = 0
    mpl.rcParams['agg.path.chunksize'] = 10000 # needed for saving. Hard coded limit in agg backend (see: https://github.com/matplotlib/matplotlib/issues/5907)
    for f in fig_artificial_short:
        f.savefig("./plots/baseline/" + "artificial_" + f'{i:02d}'+".png", dpi=1200)
        i += 1
    for f in fig_artificial_long:
        f.savefig("./plots/baseline/" + "artificial_" + f'{i:02d}'+".png", dpi=1200)
        i += 1
    for f in fig_artificial_5_epoche:
        f.savefig("./plots/baseline/" + "artificial_" + f'{i:02d}'+".png", dpi=1200)
        i += 1
    for f in fig_artificial_20_epoche:
        f.savefig("./plots/baseline/" + "artificial_" + f'{i:02d}'+".png", dpi=1200)
        i += 1