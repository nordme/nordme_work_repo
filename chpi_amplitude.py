# -*- coding: utf-8 -*-

import mne
import os
import os.path as op
import numpy as np
from mne.chpi import _get_hpi_info
from scipy import linalg



def plot_chpi_amplitude(raw, win_length, n_harmonics=None, show=True,
                      verbose=True, fname=None):

    import matplotlib.pyplot as plt
    from mne.io.pick import pick_types
    import matplotlib.patches as mp


# derive amplitudes

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

    # add sine and cosine term for each freq
    allfreqs = np.concatenate([linefreqs, cfreqs])
    model[:, 2::2] = np.cos(2 * np.pi * t[:, np.newaxis] * allfreqs)
    model[:, 3::2] = np.sin(2 * np.pi * t[:, np.newaxis] * allfreqs)
    inv_model = linalg.pinv(model)

    # code for using the full time interval
    # bufs = np.arange(0, raw.n_times, buflen)[:-1] ## drop last buffer to avoid overrun

    # only use 10 sec interval from 5 to 15 seconds
    if sfreq == 2000:
        bufs = np.arange(12000, 30001, buflen)
    else:
        bufs = np.arange(6000, 15001, buflen)

    tvec = bufs/sfreq
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

    # derive mean power for each coil
    overall_mean_pow = hpi_pow_mean.mean(1)

    mean_1 = overall_mean_pow[0]
    mean_2 = overall_mean_pow[1]
    mean_3 = overall_mean_pow[2]
    mean_4 = overall_mean_pow[3]
    mean_5 = overall_mean_pow[4]

# initiate plotting
    print('Graphing cHPI amplitude for file %s ' % fname)
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    # create parameters for plotting use later
    cfreqs_legend = ['%s Hz' % fre for fre in cfreqs]
    legend_fontsize = 9
    title_fontsize = 11
    tick_fontsize = 9
    label_fontsize = 10
    means = (mean_1, mean_2, mean_3, mean_4, mean_5)
    mean_max = max(means)
    y_height = 3.5e-20
    colors = ('C0', 'C1', 'C2', 'C3', 'C4')
    x_range = np.arange(1,6,1)
    x_labels = ['83 Hz', '143 Hz', '203 Hz', '263 Hz', '323 Hz']

# make the amplitude by time plot

    amps = ax1.plot(tvec, hpi_pow_mean.T)
    # x and y axes
    ax1.set_xlim([6, 15])
    ax1.set(ylabel='Power (fT/c2)', xlabel='Time (seconds)')
    # ax1.set_ylim(1.1*mean_max)
    ax1.yaxis.label.set_fontsize(label_fontsize)
    ax1.set_title('Amplitude of cHPI coils over 10 sec',
                 fontsize=title_fontsize, y=1.04)
    ax1.tick_params(axis='both', which='major', labelsize=tick_fontsize)
    # deal with where the plot shows up in the figure
    box = ax1.get_position()
    ax1.set_position([box.x0-0.02, box.y0, box.width * 0.8, box.height])
    # create legend for plot
    sind = np.argsort(hpi_pow_grad.mean(axis=1))[::-1]   # order curve legends according to mean of data
    handles = [amps[i] for i in sind]
    labels = [cfreqs_legend[i] for i in sind]
    ax1.legend(handles, labels,
              prop={'size': legend_fontsize}, loc='upper left', bbox_to_anchor=(1.0, 1.0))

# make the mean amplitude bar chart

    # title
    ax2.set_title('Coil Mean Power', y=1.04)
    # adjust x axis
    ax2.set_xlim(0,6)
    ax2.set_xticks([1,2,3,4,5])
    ax2.set_xticklabels(x_labels)
    ax2.set_xlabel('Coil Frequencies')
    ax2.tick_params(axis='both', labelsize=tick_fontsize)
    # adjust y axis
    ax2.set_ylim(0, y_height)
    ax2.set_ylabel('Power (fT/cm2)')
    ax2.set_yscale('linear')
    # deal with where the plot shows up in the figure
    box2 = ax2.get_position()
    ax2.set_position([box2.x0+0.02, box2.y0, box2.width * 0.8, box2.height])
    # create a legend for the plot
    bar1 = '%5.3f' % (mean_1 * (10 ** 20))
    bar2 = '%5.3f' % (mean_2 * (10 ** 20))
    bar3 = '%5.3f' % (mean_3 * (10 ** 20))
    bar4 = '%5.3f' % (mean_4 * (10 ** 20))
    bar5 = '%5.3f' % (mean_5 * (10 ** 20))
    bp = mp.Patch(color='C0', label='%s (83 Hz)' % bar1)
    orp = mp.Patch(color='C1', label='%s (143 Hz)' % bar2)
    gp = mp.Patch(color='C2', label='%s (203 Hz)' % bar3)
    rp = mp.Patch(color='C3', label='%s (263 Hz)' % bar4)
    pp = mp.Patch(color='C4', label='%s (323 Hz)' % bar5)
    ax2.legend(handles=[bp, orp, gp, rp, pp], prop={'size': legend_fontsize}, loc='upper left', bbox_to_anchor=(1.0, 1.0))
    # make the bars
    ax2.bar(x=x_range, height=means, align='center', color=colors, width=0.8, bottom=None)
    # close and save figure
    plt.close(fig1)
    # fig1.savefig(op.join(save_path[:-4] + '_ampl.png'))


    return fig1



def print_chpi_amplitude(raw, win_length, n_harmonics=None, show=True,
                      verbose=True, fname=None):

    import matplotlib.pyplot as plt
    from mne.io.pick import pick_types
    import matplotlib.patches as mp


# derive amplitudes

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

    # add sine and cosine term for each freq
    allfreqs = np.concatenate([linefreqs, cfreqs])
    model[:, 2::2] = np.cos(2 * np.pi * t[:, np.newaxis] * allfreqs)
    model[:, 3::2] = np.sin(2 * np.pi * t[:, np.newaxis] * allfreqs)
    inv_model = linalg.pinv(model)

    # code for using the full time interval
    # bufs = np.arange(0, raw.n_times, buflen)[:-1] ## drop last buffer to avoid overrun

    # only use 10 sec interval from 5 to 15 seconds
    if sfreq == 2000:
        bufs = np.arange(12000, 30001, buflen)
    else:
        bufs = np.arange(6000, 15001, buflen)

    tvec = bufs/sfreq
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

    # derive mean power for each coil
    overall_mean_pow = hpi_pow_mean.mean(1)

    mean_1 = overall_mean_pow[0]
    mean_2 = overall_mean_pow[1]
    mean_3 = overall_mean_pow[2]
    mean_4 = overall_mean_pow[3]
    mean_5 = overall_mean_pow[4]

    # print the mean power values

    means = [['Amplitudes for %s' % fname],
             ['coil 1 mean power:', mean_1*1e20],
             ['coil 2 mean power:', mean_2*1e20],
             ['coil 3 mean power:', mean_3*1e20],
             ['coil 4 mean power:', mean_4*1e20],
             ['coil 5 mean power:', mean_5*1e20]]

    return means

def print_snr(raw, win_length, n_harmonics=None, show=True,
                      verbose=False, fname=None):

    from mne.io.pick import pick_types

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
    # grad and mag indices into an array that already has meg channels only
    pick_mag_ = np.in1d(pick_meg, pick_mag).nonzero()[0]
    pick_grad_ = np.in1d(pick_meg, pick_grad).nonzero()[0]

    # create general linear model for the data
    t = np.arange(buflen) / float(sfreq)
    model = np.empty((len(t), 2+2*(len(linefreqs)+len(cfreqs))))
    model[:, 0] = t
    model[:, 1] = np.ones(t.shape)
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
    snr_avg_mag = np.zeros([len(cfreqs), len(bufs)])
    resid_vars = np.zeros([nchan, len(bufs)])
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
        # divide average HPI power by average variance
        snr_avg_grad[:, ind] = hpi_pow_grad[:, ind] / \
            resid_vars[pick_grad_, ind].mean()
        snr_avg_mag[:, ind] = hpi_pow[:, pick_mag_].mean(1) / \
            resid_vars[pick_mag_, ind].mean()

    # get mean SNR values

    snr_avg_grad1 = 10*np.log10(snr_avg_grad)

    snr_means = snr_avg_grad1.mean(1)
    snr1 = snr_means[0]
    snr2 = snr_means[1]
    snr3 = snr_means[2]
    snr4 = snr_means[3]
    snr5 = snr_means[4]


    # print snr values per coil per file
    print('SNR for gradiometers:')
    print('Coil 1: %d; \n Coil 2: %d \n Coil 3: %d \n Coil 4: %d \n Coil 5: %d' % (snr1, snr2, snr3, snr4, snr5))

    return snr_means