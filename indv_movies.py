# -*- coding: utf-8 -*-

import os
import os.path as op
import mne
import numpy as np

# set variables

signed = False
inv_method = 'dSPM'
subj_dir = '/data/acdc/'
subjects = ['erica_peterson']
backend = 'mavayi'

if signed:
    tag = '/signed/'
    clim = {'kind': 'percent', 'pos_lims': np.arange(96, 101, 2)}
else:
    tag = '/'
    clim = {'kind': 'percent', 'lims': [96, 98, 100]}

# stc_options = ['al01',
#                'al02',
#                'al03',
#                'fl01',
#                'fl02',
#                'fl03',
#                'el01',
#                'el02',
#                'el03',
#                'tl01',
#                'tl02',
#                'tl03']

stc_options = ['oddball1_dSPM',
               'oddball2_dSPM',
               'standard_dSPM',
               ]

# read in the stc and plot it

for subject in subjects:
    print('Working on the movie for subject %s' % subject)
#    stcs_dir = op.join(subj_dir, subject, '%s_stc' % inv_method, 'auditory')
    stcs_dir = op.join(subj_dir, subject, 'stcs')
    movie_dir = op.join(subj_dir, subject, 'movies')
    stc_names = ['%s_%s' % (subject, x) for x in stc_options]
    for name in stc_names:
        stc = mne.read_source_estimate(op.join(stcs_dir, name))
        title = 'stc: %s method: %s (96+ pctl)' % (name, inv_method)
        plot = stc.plot(subject=subject, surface='inflated', hemi='split', colormap='cool', views=['lat', 'med'],
                              clim=clim, title=title, time_viewer=True, size=(800, 800), show_traces=True)
        save_name = op.join(movie_dir, '%s_percent.mov' % (name))
        plot.save_movie(filename=save_name, time_dilation=24, framerate=20, interpolation='linear')
        plot.close()