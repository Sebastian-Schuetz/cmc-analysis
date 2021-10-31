# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 14:32:19 2021

@author: Sebastian
"""

from test_data_gen import gen_artifical_signal
from analyse_data import calc_cmc, calc_cmc_epoched
from data_plot import plot
import matplotlib as mpl
from joblib import Parallel, delayed


def create_artificial_signal(frequency, duration, sampling_rate, freqs, durs):
    sig1 = gen_artifical_signal([frequency], [duration], sampling_rate)
    sig2 = gen_artifical_signal(freqs, durs, sampling_rate)
    
    return sig1, sig2


def test_parameters(sig1, sig2, sampling_rate, dj, s0, J, name):
    try: 
        wct, awct, freq = calc_cmc(sig1, sig2, sampling_rate, dj, s0, J)
        if min(freq) < 50:
            return plot(sig1, sig2, wct, awct, freq, name, show_plot=False)
        else:
            return None
    except:
        return None
    

def test_and_save(sig1, sig2, sampling_rate, d, s, j, i, tag):
    figs = test_parameters(sig1, sig2, 1000, d, s, j, \
                       "para. art. whole (s): dj={}, s0={}, J={}".format(d, s, j))
    mpl.rcParams['agg.path.chunksize'] = 10000 # needed for saving. Hard coded limit in agg backend (see: https://github.com/matplotlib/matplotlib/issues/5907)
    if figs is not None:
        for f in figs:
            f.savefig("./plots/parameters"+ tag +"/" + "par_" + f'{i:03d}'+".png", dpi=1200)
            i += 1
        print(i)


def test1():
    dj = [0.05, 0.01, 0.005, 0.1, 0.2]      # Spacing between scales
    s0 = [-1, 0.001, 0.0001, 0.01, 0.1, 1]  # Smallest scale of wavelet
    J  = [-1, 100, 250, 500, 1000, 2000]    # Scales below 1
    
    sig1, sig2 = create_artificial_signal(24, 10, 1000, [24, 5], [5, 5])

    res = [[d, s, j]    for d in dj
                        for s in s0
                        for j in J]
    
    Parallel(n_jobs=8)(delayed(test_and_save)(sig1, sig2, 1000, d, s, j, i*4, "01") for i, (d,s,j) in enumerate(res))

def test2():
    dj = [0.05, 0.01, 0.005]      # Spacing between scales
    s0 = [0.001, 0.0001, 0.000001]  # Smallest scale of wavelet
    J  = [1000, 2000, 5000, 10000]    # Scales below 1
    
    sig1, sig2 = create_artificial_signal(24, 10, 1000, [24, 5], [5, 5])

    res = [[d, s, j]    for d in dj
                        for s in s0
                        for j in J]
    
    Parallel(n_jobs=10)(delayed(test_and_save)(sig1, sig2, 1000, d, s, j, i*4, "02") for i, (d,s,j) in enumerate(res))




if __name__ == "__main__":

    
    test2()
    
    

    # mpl.rcParams['agg.path.chunksize'] = 10000 # needed for saving. Hard coded limit in agg backend (see: https://github.com/matplotlib/matplotlib/issues/5907)
    # for d in dj:
    #     for s in s0:
    #         for j in J:
    #             figs = test_parameters(sig1, sig2, 1000, d, s, j, \
    #                                    "para. art. whole (s): dj={}, s0={}, J={}".format(d, s, j))
    #             if figs is not None:
    #                 for f in figs:
    #                     f.savefig("./plots/parameters/" + "par_" + f'{i:03d}'+".png", dpi=1200)
    #                     i += 1
    #                 print(i)