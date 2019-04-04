#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import os.path as op
import mne
import numpy as np


# set important variables

raw_dir = '/home/nordme/data/genz/genz_active/'
# raw_dir = '/brainstudio/MEG/genz/genz_proc/active/'
anat_dir = '/brainstudio/MEG/genz/anatomy/'

subjects = []

subject = 'genz131_9a'


# state which conditions you want to subtract

cond_1 =

cond_2 =





ave1 = 0

ave2 = 0

groups = []

by age:
    by gender and age:

    by age:

altogether:



for group in groups:
    for subject in group:

        # read in the source estimates

        diff_1 = mne.read_source_estimate()

        diff_2 = mne.read_source_estimate()

        # create the sums, then create the mean data

        ave1 += diff_1

        ave2 += diff_2

    ave1 /= len(subjects)

    assert ave1.data.ndim == 2 and ave1.data.shape[0] == 8196

    ave1.save()

    ave2 /= len(subjects)

    assert ave2.data.ndim == 2 and ave2.data.shape[0] == 8196

    ave2.save()

    # take the differences of the two means

    diff = ave1-ave2

    assert diff.data.ndim == 2 and diff.data.shape[0] == 8196

    # plot the difference

    diff_plot = diff.plot(surface='inflated', hemi='split', colormap='cool', views = ['lat', 'med'], size=800)

    # save the movie of the difference plot

    save_name =

    diff_plot.save_movie(fname=save_name, time_dilation=24, framerate=20, interpolation='linear')


