# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import os.path as op
import mne
import matplotlib.pyplot as plt
from mnefun import (plot_chpi_snr_raw, plot_good_coils)
from chpi_amplitude import plot_chpi_amplitude, print_chpi_amplitude

import itertools

# set global variables

raw_dir = '/home/nordme/data/cHPI_test/raw/'
save_dir = '/home/nordme/data/cHPI_test/images/'
fnames = []

# create the set of file names

coils = ['one_back', 'two_back', 'three_back', 'four_back', 'five_back', 'line', 'square']
heights = ['d0', 'd1', 'd2', 'd3', 'd4', 'd5']
samples = ['1000_330', '2000_330', '2000_660']

products = list(itertools.product(*[coils, heights, samples]))

for product in products:
    fname = '%s_%s_%s_raw.fif' % (product[0], product[1], product[2])
    fnames.append(fname)


# choose what you want to plot

graph_snr = True

graph_amplitude = True

graph_distances = True

print_amplitudes = True

# create the graphs

fnames = ['/home/nordme/data/cHPI_test/Mar_4/low_int_2_d0_1000_330_raw.fif']

for file in fnames:
    f_path = op.join(raw_dir, file)
    save_path = op.join(save_dir, file)
    raw = mne.io.read_raw_fif(f_path, allow_maxshield=True)
    t_window = 1

    # graph snr
    if graph_snr:
        fig = plot_chpi_snr_raw(raw, t_window, show=False, verbose=False)
        fig.set_size_inches(10, 5)
        fig.subplots_adjust(0.1, 0.1, 0.8, 0.95, wspace=0, hspace=0.5)
        plt.close()
        fig.savefig(op.join(save_path[:-4] + '_snr.png'))

    # graph amplitude
    if graph_amplitude:
        fig1 = plot_chpi_amplitude(raw, win_length=1, n_harmonics=None, fname=file)
        fig1.savefig(op.join(save_path[:-4] + '_ampl.png'))
        plt.close()

    # graph coil distances over time
    if graph_distances:
        fig2 = plot_good_coils(raw, t_step=1, t_window=t_window)
        fig2.savefig(op.join(save_path[:-4] + 'coil_dist.png'))
        plt.close()

    if print_amplitudes:
        print('Amplitudes for %s' % file)
        print(print_chpi_amplitude(raw, win_length=1, n_harmonics=None, fname=file))