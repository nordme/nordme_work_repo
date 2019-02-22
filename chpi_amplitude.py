# -*- coding: utf-8 -*-

import mne
import os
import os.path as op
import numpy as np
from mne.chpi import _get_hpi_info
from scipy import linalg



def plot_chpi_amplitude(raw, win_length, n_harmonics=None, show=True,
                      verbose=True, save_path=os.getcwd(), fname=None):

    import matplotlib.pyplot as plt
    from mne.io.pick import pick_types


    # plotting parameters
    legend_fontsize = 10
    title_fontsize = 10
    tick_fontsize = 10
    label_fontsize = 10

    # get some info from fiff
    sfreq = raw.info['sfreq']
    linefreq = raw.info['line_freq']
    if n_harmonics is not None:
        linefreqs = (np.arange(n_harmonics + 1) + 1) * linefreq
    else:
        linefreqs = np.arange(linefreq, raw.info['lowpass'], linefreq)
    buflen = int(win_length * sfreq)
    if buflen <= 0:
        raise ValueError('Window length should be >0')
    cfreqs = _get_hpi_info(raw.info)[0]
    cfreqs.sort()
    if verbose:
        print('Nominal cHPI frequencies: %s Hz' % cfreqs)
        print('Sampling frequency: %s Hz' % sfreq)
        print('Using line freqs: %s Hz' % linefreqs)
        print('Using buffers of %s samples = %s seconds\n'
              % (buflen, buflen/sfreq))

    pick_meg = pick_types(raw.info, meg=True, exclude=[])
    pick_mag = pick_types(raw.info, meg='mag', exclude=[])
    pick_grad = pick_types(raw.info, meg='grad', exclude=[])
    nchan = len(pick_meg)

    # put grad and mag indices into an array that already has meg channels only
    pick_mag_ = np.in1d(pick_meg, pick_mag).nonzero()[0]
    pick_grad_ = np.in1d(pick_meg, pick_grad).nonzero()[0]

    # create general linear model for the data
    t = np.arange(buflen) / float(sfreq)
    model = np.empty((len(t), 2+2*(len(linefreqs)+len(cfreqs))))
    model[:, 0] = t
    model[:, 1] = np.ones(t.shape)
    print(model.shape)

    # add sine and cosine term for each freq
    allfreqs = np.concatenate([linefreqs, cfreqs])
    model[:, 2::2] = np.cos(2 * np.pi * t[:, np.newaxis] * allfreqs)
    model[:, 3::2] = np.sin(2 * np.pi * t[:, np.newaxis] * allfreqs)
    inv_model = linalg.pinv(model)

    # drop last buffer to avoid overrun
    bufs = np.arange(0, raw.n_times, buflen)[:-1]

    tvec = bufs/sfreq
    snr_avg_grad = np.zeros([len(cfreqs), len(bufs)])
    hpi_pow_grad = np.zeros([len(cfreqs), len(bufs)])
    hpi_pow_mean = np.zeros([len(cfreqs), len(bufs)])
    resid_vars = np.zeros([nchan, len(bufs)])

    # derive hpi power for each buffer
    for ind, buf0 in enumerate(bufs):
        if verbose:
            print('Buffer %s/%s' % (ind+1, len(bufs)))
        megbuf = raw[pick_meg, buf0:buf0+buflen][0].T
        coeffs = np.dot(inv_model, megbuf)
        coeffs_hpi = coeffs[2+2*len(linefreqs):]
        resid_vars[:, ind] = np.var(megbuf-np.dot(model, coeffs), 0)
        # get total power by combining sine and cosine terms
        # sinusoidal of amplitude A has power of A**2/2
        hpi_pow = (coeffs_hpi[0::2, :]**2 + coeffs_hpi[1::2, :]**2)/2
        hpi_pow_grad[:, ind] = hpi_pow[:, pick_grad_].mean(1)
        hpi_pow_mean[:, ind] = hpi_pow.mean(1)

    overall_mean_pow = hpi_pow_mean.mean(1)

    mean_1 = overall_mean_pow[0]
    mean_2 = overall_mean_pow[1]
    mean_3 = overall_mean_pow[2]
    mean_4 = overall_mean_pow[3]
    mean_5 = overall_mean_pow[4]

    # initiate plotting
    cfreqs_legend = ['%s Hz' % fre for fre in cfreqs]
    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=False)

    # make the amplitude by time plot
    print('Graphing cHPI amplitude for file %s ' % fname)
    amps = ax1.plot(tvec, hpi_pow_mean.T)
    ax1.set_xlim([5, 15])
    ax1.set(ylabel='Power (fT/c2)')
    ax1.yaxis.label.set_fontsize(label_fontsize)
    ax1.set_title('Amplitude of cHPI coils',
                 fontsize=title_fontsize)
    ax1.tick_params(axis='both', which='major', labelsize=tick_fontsize)
    box = ax1.get_position()
    ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    sind = np.argsort(snr_avg_grad.mean(axis=1))[::-1]   # order curve legends according to mean of data
    handles = [amps[i] for i in sind]
    labels = [cfreqs_legend[i] for i in sind]
    ax1.legend(handles, labels,
              prop={'size': legend_fontsize}, bbox_to_anchor=(1.02, 0.5, ),
              loc='center left', borderpad=1)

    # make the overall mean amplitude plot
    coils = [cfreqs_legend]
    means = (overall_mean_pow[0], overall_mean_pow[1], overall_mean_pow[2], overall_mean_pow[3], overall_mean_pow[4])
    colors = ('b', 'y', 'g', 'r', 'm')
    x_range = np.arange(1,6,1)
    bars = ax2.bar(x=x_range, height=means, align='center', color=colors, width=0.8, bottom=None)


    fig.savefig(op.join(save_path[:-4] + '_ampl.png'))

