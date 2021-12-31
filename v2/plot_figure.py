# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 18:52:01 2021

@author: Sebastian
"""

import numpy as np
from mne.viz import plot_topomap
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
    axs[1].plot(sig2)
    if not show_plot:
        plt.close()
    return fig

def plot_all_signals(sigs, name, show_plot):
    """
    Plots all Signals over all Epochs in seperate subplots -> for fast visual inspection

    Parameters
    ----------
    sigs : TYPE
        DESCRIPTION.
    name : TYPE
        DESCRIPTION.
    show_plot : TYPE
        DESCRIPTION.

    Returns
    -------
    fig : TYPE
        DESCRIPTION.

    """
    fig, axs = plt.subplots(len(sigs))
    fig.suptitle("Signals: " + name)
    for i, s in enumerate(sigs):
        axs[i].plot(s)
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
    axes = plt.axes()
    axes.set_ylim([0, 0.8])
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
    axes = plt.axes()
    axes.set_ylim([0.2, 0.6])
    plt.plot(freq[freq_of_int], coh)
    plt.title("Coherence over frequency : " + name)
    plt.show
    if not show_plot:
        plt.close()
    return fig
    
def plot_coh_over_freq_welch(wct, freq, name, fmin, fmax, show_plot, path = None):
    freq_of_int = np.where(np.logical_and(freq>=fmin, freq<=fmax))[0]
    coh = wct[freq_of_int]
    fig = plt.figure()
    plt.plot(freq[freq_of_int], coh)
    plt.title("Coherence over frequency : " + name)
    plt.show
    
    if path is not None:
        plt.savefig(path, dpi=600)
        plt.close()
        
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
    contourf_ = ax.contourf(T, S, wct[freq_of_int], 256, levels = np.linspace(0,0.75,35))
    
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

def plot_welch(sig1, sig2, wct, awct, freq, name, show_plot=True):
    fmin=5
    fmax=50
    fig1 = plot_signals(sig1, sig2, name, show_plot)
    fig2 = plot_coh_over_freq_welch(wct, freq, name, fmin, fmax, show_plot)
    
    return [fig1, fig2]

def plot_welch_compare(wct1, wct2, wct3, wct4, freq, name1, name2, show_plot=True):
    fmin=5
    fmax=50
    fig1 = plot_compare_coherence_over_frequency(wct1, wct2, wct3, wct4, freq, name1, name2, fmin, fmax, show_plot)
    return fig1

def plot_compare(wct1, wct2, wct3, wct4, freq, name1, name2, show_plot=True):
    fmin=5
    fmax=50
    fig1 = plot_compare_coherence_over_frequency(wct1, wct2, wct3, wct4, freq, name1, name2, fmin, fmax, show_plot)
    fig2 = plot_compare_coh_2d(wct1, wct2, freq, name1, name2, fmin, fmax, show_plot)
    if wct3 is not None:
        fig3 = plot_compare_coh_2d(wct3, wct4, freq, name1 + " - Post", name2 + " - Post", fmin, fmax, show_plot)
        return [fig1, fig2, fig3]
    
    return [fig1, fig2]

def plot_compare_coherence_over_frequency(wct1, wct2, wct3, wct4, freq, name1, name2, fmin, fmax,  show_plot):
    """
    Same as coherence over frequency, just plottes two next to each other

    Parameters
    ----------
    wct1 : TYPE
        DESCRIPTION.
    wct2 : TYPE
        DESCRIPTION.
    freq : TYPE
        DESCRIPTION.
    name1 : TYPE
        DESCRIPTION.
    name2 : TYPE
        DESCRIPTION.
    fmin : TYPE
        DESCRIPTION.
    fmax : TYPE
        DESCRIPTION.
    show_plot : TYPE
        DESCRIPTION.

    Returns
    -------
    fig : TYPE
        DESCRIPTION.

    """
    
    freq_of_int = np.where(np.logical_and(freq>=fmin, freq<=fmax))[0]
    coh1 = [np.mean(wct1[foi]) for foi in freq_of_int]
    coh2 = [np.mean(wct2[foi]) for foi in freq_of_int]
    coh3 = [np.mean(wct3[foi]) for foi in freq_of_int]
    coh4 = [np.mean(wct4[foi]) for foi in freq_of_int]
    
    fig, axs = plt.subplots(1,2)
    axs[0].set_title("Coh over freq : " + name1)
    axs[0].set_ylim([0.2, 0.6])
    axs[0].plot(freq[freq_of_int], coh1, label="Pre")
    if wct3 is not None:
        axs[0].plot(freq[freq_of_int], coh3, label="Post")
        axs[0].legend()
    
    axs[1].set_title("Coh over freq : " + name2)
    axs[1].set_ylim([0.2, 0.6])
    axs[1].plot(freq[freq_of_int], coh2, label="Pre")
    if wct4 is not None:
        axs[1].plot(freq[freq_of_int], coh4, label="Post")
        axs[1].legend()
    
    plt.show()
    if not show_plot:
        plt.close()
    return fig

def plot_compare_coh_2d(wct1, wct2, freq, name1, name2, fmin, fmax, show_plot):
    freq_of_int = np.where(np.logical_and(freq>=fmin, freq<=fmax))[0]
    coh1 = [np.mean(wct1[foi]) for foi in freq_of_int]
    coh2 = [np.mean(wct2[foi]) for foi in freq_of_int]
    
    fig, axs = plt.subplots(1,2)
    
    T1, S1 = np.meshgrid(np.arange(0, len(wct1[0]), 1), freq[freq_of_int])
    contourf_ = axs[0].contourf(T1, S1, wct1[freq_of_int], 256, levels = np.linspace(0,0.75,35))
    plt.colorbar(contourf_, ax=axs[0])
    axs[0].set_title("2D-Coh: " + name1)
    axs[0].set_ylabel("Frequency (Hz)")
    axs[0].set_xlabel("Time (Ticks, NOT ms)")
    
    T2, S2 = np.meshgrid(np.arange(0, len(wct2[0]), 1), freq[freq_of_int])
    contourf2_ = axs[1].contourf(T2, S2, wct2[freq_of_int], 256, levels = np.linspace(0,0.75,35))
    plt.colorbar(contourf2_, ax=axs[1])
    axs[1].set_title("2D-Coh: " + name2)
    axs[1].set_ylabel("Frequency (Hz)")
    axs[1].set_xlabel("Time (Ticks, NOT ms)")   

    if not show_plot:
        plt.close()
    return fig


def get_channel_pos(channel_labels):
    from mne.channels import read_layout

    layout = read_layout("EEG1005")
    return (
        np.asanyarray([layout.pos[layout.names.index(ch)] for ch in channel_labels])[
            :, 0:2
        ]
        - 0.5
    ) / 5




def plot_topomaps(data, freqs, channels, w, h, clim, name="", path=None):
    
    pos = get_channel_pos(channels)
    fig, axs = plt.subplots(h, w)
    fig.suptitle(name)
    
    for i in range(h):
        for j in range(w):            
            axs[i, j].set_title("{:.2f}".format(freqs[i*w + j]) + " Hz")
            im, cm = plot_topomap(data[i*w + j, :], pos, mask = None, outlines = "head", \
                         vmin = clim[0], vmax = clim[1], axes = axs[i, j], cmap='RdBu_r')
    
    ax_x_start = 0.92
    ax_x_width = 0.04
    ax_y_start = 0.1
    ax_y_height = 0.8
    cbar_ax = fig.add_axes([ax_x_start, ax_y_start, ax_x_width, ax_y_height])
    clb = fig.colorbar(im, cax=cbar_ax)

    if path is not None:
        plt.savefig(path, dpi=600)
        plt.close()
    #plot_topomap(data,pos, mask = None, outlines = "head", vmin = clim[0], vmax = clim[1], axes = axs[0])
