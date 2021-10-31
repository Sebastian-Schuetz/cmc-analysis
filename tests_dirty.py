# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 13:30:21 2021

@author: Sebastian
"""

from test_data_gen import gen_dirty_sin_wave
from analyse_data import calc_cmc, calc_cmc_epoched
from data_plot import plot
import matplotlib as mpl


# Coherence of random signals
def dirty_test_signal(frequency, duration, sampling_rate, name):
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
    sig1 = gen_dirty_sin_wave(frequency, duration, sampling_rate)
    sig2 = gen_dirty_sin_wave(frequency, duration, sampling_rate)
    wct, awct, freq = calc_cmc(sig1, sig2, sampling_rate)
    return plot(sig1, sig2, wct, awct, freq, name)
    

def dirty_test_signal_epoched(frequency, duration, sampling_rate, epochs, name):
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
    epochs1 = [gen_dirty_sin_wave(frequency, duration, sampling_rate) for i in range(epochs)]
    epochs2 = [gen_dirty_sin_wave(frequency, duration, sampling_rate) for i in range(epochs)]

    wct, awct, freq = calc_cmc_epoched(epochs1, epochs2, sampling_rate)
    return plot(epochs1[0], epochs2[0], wct, awct, freq, name)


if __name__ == "__main__":
    fig_dirty_short =      dirty_test_signal(24, 10, 1000, "dirty - whole signal (short)")
    fig_dirty_long =       dirty_test_signal(24, 100, 1000, "dirty - whole signal (long)")
    fig_dirty_5_epoche =   dirty_test_signal_epoched(24, 10, 1000, 5, "dirty - 5 Epochs")
    fig_dirty_20_epoche =  dirty_test_signal_epoched(24, 10, 1000, 20, "dirty - 20 Epochs")
    
    # Better quality, but rediculas sizes (code below ~700 Mb pdf!!!)
    # from matplotlib.backends.backend_pdf import PdfPages
    # with PdfPages('dirty_data.pdf') as pdf:
    #     for f in fig_dirty_short:
    #         pdf.savefig(f)
    #     for f in fig_dirty_long:
    #         pdf.savefig(f)
    #     for f in fig_dirty_5_epoche:
    #         pdf.savefig(f)
    #     for f in fig_dirty_20_epoche:
    #         pdf.savefig(f)
    
    i = 0
    mpl.rcParams['agg.path.chunksize'] = 10000 # needed for saving. Hard coded limit in agg backend (see: https://github.com/matplotlib/matplotlib/issues/5907)
    for f in fig_dirty_short:
        f.savefig("./plots/baseline/" + "dirty_" + f'{i:02d}'+".png", dpi=1200)
        i += 1
    for f in fig_dirty_long:
        f.savefig("./plots/baseline/" + "dirty_" + f'{i:02d}'+".png", dpi=1200)
        i += 1
    for f in fig_dirty_5_epoche:
        f.savefig("./plots/baseline/" + "dirty_" + f'{i:02d}'+".png", dpi=1200)
        i += 1
    for f in fig_dirty_20_epoche:
        f.savefig("./plots/baseline/" + "dirty_" + f'{i:02d}'+".png", dpi=1200)
        i += 1