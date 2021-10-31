# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 09:24:19 2021

@author: Sebastian
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_signals(sig1, sig2, name, show_plot):
    """
    Plots the two signals in two seperate subplots

    Parameters
    ----------
    sig1 : TYPE
        DESCRIPTION.
    sig2 : TYPE
        DESCRIPTION.
    name : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    fig, axs = plt.subplots(2)
    fig.suptitle("Signals : " + name)
    axs[0].plot(sig1)
    axs[1].plot(sig1)
    if not show_plot:
        plt.close()
    return fig
    
def plot_coh_over_time(wct, freq, name, fmin, fmax, show_plot):
    """
    Plots the calculated coherence over the course of the signal, within the
    specified frequency band

    Parameters
    ----------
    wct : TYPE
        DESCRIPTION.
    freq : TYPE
        DESCRIPTION.
    name : TYPE
        DESCRIPTION.
    fmin : TYPE, optional
        DESCRIPTION. The default is 5.
    fmax : TYPE, optional
        DESCRIPTION. The default is 50.

    Returns
    -------
    None.

    """
    freq_of_int = np.where(np.logical_and(freq>=fmin, freq<=fmax))[0]
    
    fig = plt.figure()
    for foi in freq_of_int:
        plt.plot(wct[foi], label=str(round(freq[foi], 2)))
    plt.legend(ncol=2)
    plt.title("Coherence over time : " + name)
    plt.show()
    if not show_plot:
        plt.close()
    return fig

def plot_coh_over_freq(wct, freq, name, fmin, fmax, show_plot):
    """
    Plots the average coherence for a given frequency vs the frequency

    Parameters
    ----------
    wct : TYPE
        DESCRIPTION.
    freq : TYPE
        DESCRIPTION.
    name : TYPE
        DESCRIPTION.
    fmin : TYPE
        DESCRIPTION.
    fmax : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    freq_of_int = np.where(np.logical_and(freq>=fmin, freq<=fmax))[0]
    coh = [np.mean(wct[foi]) for foi in freq_of_int]
    fig = plt.figure()
    plt.plot(freq[freq_of_int], coh)
    plt.title("Coherence over frequency : " + name)
    plt.show
    if not show_plot:
        plt.close()
    return fig
    
def plot_coh_2d(wct, freq, name, fmin, fmax, show_plot):
    """
    Creates a 2D-Plot, showing the coherence in the time and frequency domain

    Parameters
    ----------
    wct : TYPE
        DESCRIPTION.
    freq : TYPE
        DESCRIPTION.
    name : TYPE
        DESCRIPTION.
    fmin : TYPE
        DESCRIPTION.
    fmax : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    fig, ax = plt.subplots()

    freq_of_int = np.where(np.logical_and(freq>=fmin, freq<=fmax))[0]
    T, S = np.meshgrid(np.arange(0, len(wct[0]), 1), freq[freq_of_int])
    contourf_ = ax.contourf(T, S, wct[freq_of_int], 256)
    
    fig.colorbar(contourf_)
    
    # Fancy up the plot
    ax.set_title("2D-coherence over freq and time : " + name)
    ax.set_ylabel('Frequency (Hz)')
    ax.set_xlabel('Time (in ticks, not ms!!)')
    if not show_plot:
        plt.close()
    return fig

def plot(sig1, sig2, wct, awct, freq, name, show_plot=True):
    fmin=5
    fmax=50
    fig1 = plot_signals(sig1, sig2, name, show_plot)
    fig2 = plot_coh_over_time(wct, freq, name, fmin, fmax, show_plot)
    fig3 = plot_coh_over_freq(wct, freq, name, fmin, fmax, show_plot)
    fig4 = plot_coh_2d(wct, freq, name, fmin, fmax, show_plot)
    
    return [fig1, fig2, fig3, fig4]
