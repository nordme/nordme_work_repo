# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import os.path as op
import time
import warnings

import numpy as np

import mne
from mne import read_proj
from mne.io import read_raw_fif
from mne.viz import plot_projs_topomap
from mne.viz._3d import plot_head_positions
from mne.viz import plot_snr_estimate
from mne.report import Report


import matplotlib.pyplot as plt
from mnefun import plot_chpi_snr_raw
from chpi_amplitude import plot_chpi_amplitude

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


# create the graphs

for file in fnames:
    if 'square' in file:
        f_path = op.join(raw_dir, file)
        save_path = op.join(save_dir, file)
        # graph snr
        raw = mne.io.read_raw_fif(f_path, allow_maxshield=True)
        t_window = 1
        fig = plot_chpi_snr_raw(raw, t_window, show=False, verbose=False)
        fig.set_size_inches(10, 5)
        fig.subplots_adjust(0.1, 0.1, 0.8, 0.95, wspace=0, hspace=0.5)
        plt.close()
        fig.savefig(op.join(save_path[:-4] + '_snr.png'))

        # graph amplitude
        fig1 = plot_chpi_amplitude(raw, win_length=1, n_harmonics=None, save_path=save_path, fname=file)
        plt.close()




