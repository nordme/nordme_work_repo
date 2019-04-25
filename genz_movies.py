#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import os.path as op
import mne
import numpy as np


# set variables

vis_or_aud = 'auditory' # 'visual' or 'auditory'

signed = False

dSPM = True

if signed:
    tag = '/signed/'
    clim = {'kind': 'percent', 'pos_lims': np.arange(96, 101, 2)}
else:
   tag = '/'
   clim = {'kind': 'percent', 'lims': np.arange(96, 101, 2)}

if dSPM:
    aves_dir = '/brainstudio/MEG/genz/genz_proc/active/twa_hp/dSPM_ave/%s%s' % (vis_or_aud, tag)
    movie_path = '/brainstudio/MEG/genz/genz_proc/active/twa_hp/movies/dSPM/%s%s' % (vis_or_aud, tag)
    method = 'dSPM'
else:
    aves_dir = '/brainstudio/MEG/genz/genz_proc/active/twa_hp/eLORETA_ave/%s%s' % (vis_or_aud, tag)
    movie_path = '/brainstudio/MEG/genz/genz_proc/active/twa_hp/movies/eLORETA/%s%s' % (vis_or_aud, tag)
    method = 'eLORETA'


# enter the names of the stc files you wish to turn into movies

# stcs = ['both_9_SPN_faces_correct_signed']

stcs = [s for s in os.listdir(aves_dir) if '-lh' in s and 'both' in s]

# read in the stc and plot it

for stc in stcs:
    stc_plot = mne.read_source_estimate(op.join(aves_dir, '%s' % stc))

    plot = stc_plot.plot(subject='fsaverage', surface='inflated', hemi='split', colormap='cool', views=['lat', 'med'],
                         size=800, clim=clim, title='method=%s 98+ percent peak' % method)

    # save the movie of the difference plot

    save_name = op.join(movie_path, '%s.mov' % stc)

    plot.save_movie(fname=save_name, time_dilation=24, framerate=20, interpolation='linear')

    plot.close()


