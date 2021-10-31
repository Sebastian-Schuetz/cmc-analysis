# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 19:54:48 2021

@author: Sebastian

Changes the parameters of the Morelet wavelet
"""

from test_data_gen import gen_artifical_signal, gen_mixed_signal, gen_random_signal
from analyse_data import calc_cmc, calc_cmc_epoched
from data_plot import plot
import matplotlib as mpl
from joblib import Parallel, delayed

def create_artificial_signal(frequency, duration, sampling_rate, freqs, durs):
    sig1 = gen_artifical_signal([frequency], [duration], sampling_rate)
    sig2 = gen_artifical_signal(freqs, durs, sampling_rate)
    
    return sig1, sig2


def test_parameters(sig1, sig2, sampling_rate, dj, s0, J, name, f0, dj0):
    try: 
        wct, awct, freq = calc_cmc(sig1, sig2, sampling_rate, dj, s0, J, f0, dj0)
        if min(freq) < 50:
            return plot(sig1, sig2, wct, awct, freq, name, show_plot=False)
        else:
            return None
    except:
        return None
    
def test_and_save(sig1, sig2, sampling_rate, d, s, j, i, tag, f0, dj0):
    figs = test_parameters(sig1, sig2, 1000, d, s, j, \
                       "wave. art. whole (s): dj={}, f0={}, dj0={}".format(d, f0, dj0), f0, dj0)
    mpl.rcParams['agg.path.chunksize'] = 10000 # needed for saving. Hard coded limit in agg backend (see: https://github.com/matplotlib/matplotlib/issues/5907)
    if figs is not None:
        for f in figs:
            f.savefig("./plots/wavelets"+ tag +"/" + "wave_" + f'{i:03d}'+".png", dpi=1200)
            i += 1
        print(i)
        
        
def test1():
    dj = [0.05]
    f0 = [6, 8, 10, 14]
    dj0 = [0.06, 0.6, 1.2, 6]

    sig1, sig2 = create_artificial_signal(24, 10, 1000, [24, 5], [5, 5])

    res = [[d, f, dj]    for d in dj
                         for f in f0
                         for dj in dj0]
    
    Parallel(n_jobs=8)(delayed(test_and_save)(sig1, sig2, 1000, d, -1, -1, i*4, "01", f, dj) for i, (d,f,dj) in enumerate(res))
    # for i, (d, f, dj) in enumerate(res):
    #     test_and_save(sig1, sig2, 1000, d, -1, -1, i*4, "01", f, dj)
    
def test2():
    dj = [0.05]
    f0 = [13, 14, 15, 16, 20]
    dj0 = [0.06, 0.01, 0.005]

    sig1, sig2 = create_artificial_signal(24, 10, 1000, [24, 5], [5, 5])

    res = [[d, f, dj]    for d in dj
                         for f in f0
                         for dj in dj0]
    
    Parallel(n_jobs=8)(delayed(test_and_save)(sig1, sig2, 1000, d, -1, -1, i*4, "02", f, dj) for i, (d,f,dj) in enumerate(res))    


def test3():
    # Test, if multiple peaks are detectable
    sig1 = gen_mixed_signal([24, 22], 10, 1000)
    sig2 = gen_mixed_signal([24, 22, 26], 10, 1000)
    
    test_and_save(sig1, sig2, 1000, 0.05, -1, -1, 0, "03", 20, 0.06)
    
def test4():
    sig1 = gen_random_signal(10, 1000)
    sig2 = gen_random_signal(10, 1000)
    test_and_save(sig1, sig2, 1000, 0.05, -1, -1, 0, "04", 20, 0.06)
    
if __name__ == "__main__":
    test4()