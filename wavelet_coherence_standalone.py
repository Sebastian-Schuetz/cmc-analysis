# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 15:54:59 2021

@author: Sebastian
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 09:09:01 2021

@author: Sebastian
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import pandas as pd
import liesl
from scipy import signal,stats
from mne.filter import filter_data
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import pandas as pd
from scipy import signal, stats
from sklearn.cross_decomposition import CCA
from mne.filter import filter_data, notch_filter


import pycwt as wavelet
import time

from joblib import Parallel, delayed
import multiprocessing

sampling_rate = 1000
std_threshold = 0.5
peak_size_thresh = 0.2

chansel=[
 'FC3',
 'C5',
 'C3',
 'C1',
 'CP3',
 
 'FC4',
 'C2',
 'C4',
 'C6',
 'CP4']
 
def annot_max(x,y, ax=None):
    # https://stackoverflow.com/questions/43374920/how-to-automatically-annotate-maximum-value-in-pyplot
    ymax_idx = (np.diff(np.sign(np.diff(y))) < 0).nonzero()[0] + 1 
    xmax_val = x[ymax_idx]
    ymax_val = y[ymax_idx]
    
    for i, (xmax, ymax) in enumerate(zip(xmax_val, ymax_val)):
    
        text= "x={:.3f}, y={:.3f}".format(xmax, ymax)
        if not ax:
            ax=plt.gca()
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
        kw = dict(xycoords='data',textcoords="axes fraction",
                  arrowprops=arrowprops, bbox=bbox_props)
        ax.annotate(text, xy=(xmax, ymax), xytext=(0.96-((1/len(xmax_val))*i),0.96-((1/len(xmax_val))*i)), **kw)


def calculate_cmc(chan_EEG, chan_EMG, chan_nam, chan_idx):


    mother = wavelet.Morlet(6)

    cohs_wave = []
    for eeg_e, edc_e in zip(EEG_epochs, EDC_epochs):
        try:
            wct, awct, coi, freq, sig = wavelet.wct(signal.detrend(eeg_e[:, chan_idx]), signal.detrend(edc_e), dt=1.0/sampling_rate, dj=0.05, wavelet=mother, sig=False)
            #wct, awct, coi, freq, sig = wavelet.wct(eeg_e[:, chan_idx], edc_e, dt=1.0/sampling_rate, dj=0.125, J=864, wavelet=mother, sig=False)
            freq_of_int = np.where(np.logical_and(freq>=5, freq<=1000))[0]
            cohs_wave.append(wct.T[:, freq_of_int])
            print("finished epoche")
        except:
            print("jumped epoche")
    
    #plt.figure()
    dat = []
    for i in range(len(freq_of_int)):
        dat.append([freq[freq_of_int[i]], np.mean(np.abs(np.mean(cohs_wave, axis = 0)[:, i]))])
    # plt.plot(np.array(dat)[:,0], np.array(dat)[:,1])
    # plt.title("avg of coherence: " + chan_nam)
    # annot_max(np.array(dat)[:,0], np.array(dat)[:,1])
    
    # # Plotting the "normal" coh for reference
    # cohs = []
    # for edc_e, EEG_e in zip(EDC_epochs, EEG_epochs):
    #     f, coh = signal.coherence(EEG_e.T, edc_e, fs=sampling_rate, nperseg=4000, noverlap=750)
    #     cohs.append(coh[chan_idx])
    # m = np.mean(cohs, axis=0)
    # f_of_int = np.where(np.logical_and(f>=5, f<=1000))[0]
    # plt.plot(f[f_of_int], m[f_of_int])
    # plt.show()
    return (chan_nam, np.array(dat)[:,0], np.array(dat)[:,1])

def prep_data(file):
    streams = liesl.XDFFile(file)

    #common avg reref
    ref = np.tile(np.mean(streams['eego'].time_series[:,:64],axis=1), (64,1)).T
    streams['eego'].time_series[:,:64] = streams['eego'].time_series[:,:64]-ref
    # 1. Bandpass filter
    EEG= filter_data(streams['eego'].time_series[:,:64].astype(float).T,sfreq=sampling_rate ,h_freq=200,l_freq=1).T
    EEG = notch_filter(EEG.T,Fs=sampling_rate ,freqs=[50]).T
    edc = filter_data(streams['eego'].time_series[:,63+9].astype(float).T,sfreq=sampling_rate ,h_freq=200,l_freq=1)
    edc = notch_filter(edc,Fs=sampling_rate ,freqs=[50])
    
    
    # 2. Segment into 15 seconds epoch
    
    # 2.1 get the timestamps of the epoch start
    marker = streams['reiz-marker']
    contracttimes = [marker.time_stamps[i] for i,v in enumerate(marker.time_series) if \
                v[0] == "anspannen"]
    eegocontracttimes = [np.argmin(np.abs(streams['eego'].time_stamps - ts)) for ts in contracttimes]    
    relaxtimes = [marker.time_stamps[i] for i,v in enumerate(marker.time_series) if \
                v[0] == "entspannen"]
    eegorelaxtimes = [np.argmin(np.abs(streams['eego'].time_stamps - ts)) for ts in relaxtimes]
    
    
    # 3. Get rid of useless channels (Done beforehand ->easier)
    sel = [streams['eego'].channel_labels.index(ch) for ch in chansel]
    EEG = EEG[:, sel]
    
    EDC_epochs = []
    EEG_epochs = []
    for ts in eegocontracttimes:
        EDC_epochs.append(edc[ts:ts+sampling_rate*15])
        EEG_epochs.append(EEG[ts:ts+sampling_rate*15, :])
    
    return EDC_epochs, EEG_epochs

if __name__ == "__main__":
    file_path = input("Enter file path: ")
    #file_path = r"D:\Sebastian\Medizin\Doktorarbeit\Software\Github-Repos\cmc-test\data\SeSctest_0\right_30.xdf"
    
    EDC_epochs, EEG_epochs = prep_data(file_path)
    t0_p = time.time()
    res_parr = Parallel(n_jobs=10)(delayed(calculate_cmc)(EEG_epochs, EDC_epochs, name, i) for i, name in enumerate(chansel))
    # without matplotlibplot
    print("Parallel" + str(time.time()-t0_p))
    
    fig, axs = plt.subplots(10, sharex=True, sharey=True)
    
    coh_avg = []
    for i, (name, frequencies, coherence) in enumerate(res_parr):
        freq_of_int = np.where(np.logical_and(frequencies>=5, frequencies<=50))[0]
        axs[i].plot(frequencies[freq_of_int], coherence[freq_of_int])
        axs[i].set_title(name)
        coh_avg.append(coherence[freq_of_int])
    plt.figure()
    plt.plot(frequencies[freq_of_int], np.mean(coh_avg, axis=0))
        
        #annot_max(frequencies[freq_of_int], coherence[freq_of_int], axs[i])

        
    for name, frequencies, coherence in res_parr:
        plt.figure()
        plt.title(name)
        freq_of_int = np.where(np.logical_and(frequencies>=5, frequencies<=50))[0]
        plt.plot(frequencies[freq_of_int], coherence[freq_of_int])
        annot_max(frequencies[freq_of_int], coherence[freq_of_int])
        plt.show()
    
    
    # print("Seriell")
    # p0_s = time.time()
    # for i, name in enumerate(chansel):
    #     t0 = time.time()
    #     calculate_cmc(EEG_epochs, EDC_epochs, name, i)
    #     print(time.time() - t0) # 236.22006630897522
    # print("Seriell" + str(time.time() - p0_s))
    
    
    # paralell: 586.0367043018341 s
    # 235.2396891117096
    # 234.16607570648193
    # 232.85907793045044
    # 233.2404146194458
    # 234.65290141105652
    # 234.98860955238342
    # 228.0771496295929
    # 235.69420981407166
    # total 1868.9191272258759