# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 18:47:04 2021

@author: Sebastian
"""

from analyse_data import calc_cmc
from test_data_gen import gen_random_signal
from data_plot import plot
import matplotlib as mpl
from joblib import Parallel, delayed
import numpy as np
import liesl



def get_epochs_from_file(filepath, chansel, epoche_dur, sampling_rate, idx):
    """
    Loads the epochs from the coresponding file

    Parameters
    ----------
    filepath : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    streams = liesl.XDFFile(filepath)

    #common avg reref
    ref = np.tile(np.mean(streams['eego'].time_series[:,:64],axis=1), (64,1)).T
    streams['eego'].time_series[:,:64] = streams['eego'].time_series[:,:64]-ref
    
    marker = streams['reiz-marker']
    contracttimes = [marker.time_stamps[i] for i,v in enumerate(marker.time_series) if \
                v[0] == "anspannen"]
    eegocontracttimes = [np.argmin(np.abs(streams['eego'].time_stamps - ts)) for ts in contracttimes]    
    relaxtimes = [marker.time_stamps[i] for i,v in enumerate(marker.time_series) if \
                v[0] == "entspannen"]
    eegorelaxtimes = [np.argmin(np.abs(streams['eego'].time_stamps - ts)) for ts in relaxtimes]
    
    # 3. Get rid of useless channels (Done beforehand ->easier)
    EEG = streams['eego'].time_series[:,:64].astype(float)
    edc = streams['eego'].time_series[:,63+idx].astype(float)
    sel = [streams['eego'].channel_labels.index(ch) for ch in chansel]
    EEG = EEG[:, sel]
    
    EDC_epochs = []
    EEG_epochs = []
    for ts in eegocontracttimes:
        EDC_epochs.append(edc[ts:ts+sampling_rate*epoche_dur])
        EEG_epochs.append(EEG[ts:ts+sampling_rate*epoche_dur, :])
    
    return EDC_epochs, EEG_epochs





if __name__ == "__main__":
    edc, eeg = get_epochs_from_file(r"D:\Sebastian\Medizin\Doktorarbeit\Software\Github-Repos\cmc-test\data\day1\healthy_side_pre_R001.xdf",\
                                  ["C3"], 10, 2000, 9)
    
        
        
    def parameter_test(edc, eeg, sampling_rate, dj=0.05, s0=-1, J=-1, f0=20, deltaj0=0.06, t=0):
        wct_ =  []
        
        for i in range(2):
            try:
                wct, awct, freq = calc_cmc(edc[i], eeg[i].flatten(), sampling_rate, dj=dj, s0=-1, J=-1, f0=f0, deltaj0=deltaj0)
                #figs =  plot(edc[i], eeg[i].flatten(), wct, awct, freq, "wavelets epoched")
                wct_.append(wct)
            except:
                print("returned none")
                
        try:
            figs =  plot(edc[i], eeg[i].flatten(), np.mean(wct_, axis=0), awct, freq, "eego: dj={}, f0={}, dj0={}".format(dj, f0, deltaj0))
            mpl.rcParams['agg.path.chunksize'] = 10000 # needed for saving. Hard coded limit in agg backend (see: https://github.com/matplotlib/matplotlib/issues/5907)
            if figs is not None:
                for f in figs:
                    f.savefig("./plots/eego01/" + "wave_" + f'{t:03d}'+".png", dpi=1200)
                    t += 1
                print(t)
        except:
            print("Error")
            
    def randomness_test(edc, eeg, sampling_rate, dj=0.05, s0=-1, J=-1, f0=20, deltaj0=0.06, t=0):
        wct_ =  []
        
        for i in range(2):
            try:
                wct, awct, freq = calc_cmc(edc[i], eeg[i].flatten(), sampling_rate, dj=dj, s0=-1, J=-1, f0=f0, deltaj0=deltaj0)
                wct_r, awct_r, freq_r = calc_cmc(gen_random_signal(10, sampling_rate), gen_random_signal(10, sampling_rate), sampling_rate, dj=dj, s0=-1, J=-1, f0=f0, deltaj0=deltaj0)
                A = wct - wct_r
                
                wct_.append(np.clip(A, 0, 1))
            except:
                print("returned none")
                
        try:
            
            figs =  plot(edc[i], eeg[i].flatten(), np.mean(wct_, axis=0), awct, freq, "eego: dj={}, f0={}, dj0={}".format(dj, f0, deltaj0))
            mpl.rcParams['agg.path.chunksize'] = 10000 # needed for saving. Hard coded limit in agg backend (see: https://github.com/matplotlib/matplotlib/issues/5907)
            if figs is not None:
                for f in figs:
                    f.savefig("./plots/eego04/" + "wave-rand_" + f'{t:03d}'+".png", dpi=1200)
                    t += 1
                print(t)
        except:
            print("Error")
            
    def relax_test(edc, eeg, sampling_rate, dj=0.05, s0=-1, J=-1, f0=20, deltaj0=0.06, t=0):
        wct_ =  []
        
        for i in range(5):
            try:
                wct, awct, freq = calc_cmc(edc[i][:5*sampling_rate], eeg[i].flatten()[:5*sampling_rate], sampling_rate, dj=dj, s0=-1, J=-1, f0=f0, deltaj0=deltaj0)
                wct_r, awct_r, freq_r = calc_cmc(edc[i][5*sampling_rate:], eeg[i].flatten()[5*sampling_rate:], sampling_rate, dj=dj, s0=-1, J=-1, f0=f0, deltaj0=deltaj0)
                A = wct - wct_r
                
                wct_.append(A)
            except:
                print("returned none")
                
        try:
            
            figs =  plot(edc[i], eeg[i].flatten(), np.clip(np.mean(wct_, axis=0), 0, 1), awct, freq, "eego: dj={}, f0={}, dj0={}".format(dj, f0, deltaj0))
            mpl.rcParams['agg.path.chunksize'] = 10000 # needed for saving. Hard coded limit in agg backend (see: https://github.com/matplotlib/matplotlib/issues/5907)
            if figs is not None:
                for f in figs:
                    f.savefig("./plots/eego04/" + "wave-rand_" + f'{t:03d}'+".png", dpi=1200)
                    t += 1
                print(t)
        except:
            print("Error")
            
    def shifted_test(edc, eeg, sampling_rate, dj=0.05, s0=-1, J=-1, f0=20, deltaj0=0.06, t=0):
        
        wct_ =  []
        
        for i in range(2):
            if t == 0:
                edc_s = edc[i]
                eeg_s = eeg[i].flatten()
            else:
                edc_s = edc[i][(t*2):]
                eeg_s = eeg[i].flatten()[:-(t*2)]
            try:
                wct, awct, freq = calc_cmc(edc_s, eeg_s, sampling_rate, dj=dj, s0=-1, J=-1, f0=f0, deltaj0=deltaj0)
                #figs =  plot(edc[i], eeg[i].flatten(), wct, awct, freq, "wavelets epoched")
                wct_.append(wct)
            except:
                print("returned none")
                
        try:
            figs =  plot(edc_s, eeg_s, np.mean(wct_, axis=0), awct, freq, "eego: dj={}, f0={}, dj0={}, shift={}".format(dj, f0, deltaj0, t))
            mpl.rcParams['agg.path.chunksize'] = 10000 # needed for saving. Hard coded limit in agg backend (see: https://github.com/matplotlib/matplotlib/issues/5907)
            if figs is not None:
                k = 0
                for f in figs:
                    f.savefig("./plots/eego02/" + "wave_" + f'{t:03d}'+ "_" + f'{k:03d}'+".png", dpi=1200)
                    k += 1
                print(k)
        except:
            print("Error")
                
    def eeg_test(eeg1, eeg2, sampling_rate, dj=0.05, s0=-1, J=-1, f0=20, deltaj0=0.06, t=0):
        wct_ =  []
        
        for i in range(2):
            try:
                wct, awct, freq = calc_cmc(eeg1[i].flatten(), eeg2[i].flatten(), sampling_rate, dj=dj, s0=-1, J=-1, f0=f0, deltaj0=deltaj0)
                #figs =  plot(edc[i], eeg[i].flatten(), wct, awct, freq, "wavelets epoched")
                wct_.append(wct)
            except:
                print("returned none")
                
        try:
            figs =  plot(eeg1[i].flatten(), eeg2[i].flatten(), np.mean(wct_, axis=0), awct, freq, "eego: dj={}, f0={}, dj0={}".format(dj, f0, deltaj0))
            mpl.rcParams['agg.path.chunksize'] = 10000 # needed for saving. Hard coded limit in agg backend (see: https://github.com/matplotlib/matplotlib/issues/5907)
            if figs is not None:
                for f in figs:
                    f.savefig("./plots/eego03/" + "wave_" + f'{t:03d}'+".png", dpi=1200)
                    t += 1
                print(t)
        except:
            print("Error")
        
            
            
    dj = [0.05]
    f0 = [6, 8, 10, 14, 20]
    dj0 = [0.006, 0.06, 0.6, 1.2, 6]
    
    res = [[d, f, dj]    for d in dj
                         for f in f0
                         for dj in dj0]
    
    #Parallel(n_jobs=8)(delayed(parameter_test)(edc, eeg, 2000, d, -1, -1, f, dj, i*4) for i, (d,f,dj) in enumerate(res))
    
    Parallel(n_jobs=8)(delayed(shifted_test)(edc, eeg, 2000, 0.05, -1, -1, 14, 0.06, i) for i in range(75))
    
    from sklearn.preprocessing import StandardScaler
    d = StandardScaler().fit_transform(edc)
    
