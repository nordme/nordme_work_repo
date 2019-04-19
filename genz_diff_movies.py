#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import os.path as op
import mne
import numpy as np


# set variables

# aves_dir = '/home/nordme/data/genz/genz_active/magtd_stc_aves/'
aves_dir = '/home/nordme/data/genz/genz_active/stc_aves/'
# raw_dir = '/brainstudio/MEG/genz/genz_proc/active/'
anat_dir = '/brainstudio/MEG/genz/anatomy/'
movie_path = '/home/nordme/data/genz/genz_active/movies/'

subjects = []

subject = 'genz131_9a'


# state which conditions you want to subtract

cond_1 = 'both_7_al01'

cond_2 = 'both_7_al02'


# read in the morphed, grand averaged stcs and take the difference

ave1_path = op.join(aves_dir, cond_1)

ave2_path = op.join(aves_dir, cond_2)

ave1 = mne.read_source_estimate(ave1_path)

ave2 = mne.read_source_estimate(ave2_path)

diff = ave1-ave2

assert diff.data.ndim == 2 and diff.data.shape[0] == 8196

# plot the difference

diff_plot = diff.plot(subject='fsaverage', surface='inflated', hemi='split', colormap='cool', views=['lat', 'med'], size=800)

# save the movie of the difference plot

save_name = op.join(movie_path, '%s_minus_%s.mov' % (cond_1, cond_2))

diff_plot.save_movie(fname=save_name, time_dilation=24, framerate=20, interpolation='linear')
