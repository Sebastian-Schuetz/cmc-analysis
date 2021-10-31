# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 09:23:28 2021

@author: Sebastian
"""

import numpy as np

def gen_sin_wave(freq=24, duration=5, sampling_rate=1000):
    t = np.arange(duration*sampling_rate)
    return np.sin(2*np.pi*freq * (t/sampling_rate))

def gen_dirty_sin_wave(freq=24, duration=5, sampling_rate=1000, noise_floor=0.001):
    rng = np.random.default_rng()
    
    s = gen_sin_wave(freq, duration, sampling_rate)
    r = rng.normal(scale=np.sqrt(noise_floor * sampling_rate / 2), size=s.shape)
    
    return s+r

def gen_mixed_signal(freqs=[], duration=5, sampling_rate=1000, noise_floor=0.001):
    s = gen_dirty_sin_wave(freqs[0], duration, sampling_rate, noise_floor)
    s = np.array(s)
    for f in freqs[1:]:
        s += np.array(gen_dirty_sin_wave(f, duration, sampling_rate, noise_floor)[1])

    return s.tolist()
    

def gen_random_signal(duration=5, sampling_rate=1000):
    rng = np.random.default_rng()
    r = rng.random(size = duration*sampling_rate)
    return r

def gen_artifical_signal(freqs, durations, sampling_rate):
    """
    Generates an artifical signal, with different frequencies, following each other

    Parameters
    ----------
    freqs : List
        DESCRIPTION.
    durations : List
        DESCRIPTION.
    sampling_rate : int
        DESCRIPTION.

    Returns
    -------
    None.

    """
    signal = []
    for f, d in zip(freqs, durations):
        signal.extend(gen_dirty_sin_wave(f, d, sampling_rate))
    return signal