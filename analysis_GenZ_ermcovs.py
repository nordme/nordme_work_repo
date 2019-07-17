# -*- coding: utf-8 -*-
"""
GenZ pilot analysis script.

"""
# for genz 232: use 'EOG062' as the ECG channel; use ['ECG063', 'EOG061'] as the EOG channels

import os
import os.path as op
import mnefun
import numpy as np
from genz_score import (score, aud_in_names, aud_in_numbers,
                   pick_aud_cov_events, pick_vis_cov_events)

#raw_dir = '/brainstudio/MEG/genz/genz_proc/active/twa_hp/'
raw_dir = '/home/nordme/data/genz_active/'

subjs = [x for x in os.listdir(raw_dir) if op.isdir('%s%s' % (raw_dir, x)) and 'genz516' in x]


params = mnefun.Params(tmin=-0.1, tmax=0.75, t_adjust=0, n_jobs=12,
                       decim=4, n_jobs_mkl=1, proj_sfreq=200,
                       n_jobs_fir=12, n_jobs_resample=12,
                       filter_length='auto', lp_cut=80., bmin=-0.1,
                       lp_trans='auto', bem_type='inner_skull')


params.subjects = subjs

params.work_dir = '/home/nordme/data/genz_active/'

# params.work_dir = '/brainstudio/MEG/genz/genz_proc/active/twa_hp/'

params.subject_indices = [0]
#params.subject_indices = np.setdiff1d(np.arange(len(params.subjects)), [])
params.dates = [(2014, 10, 14)] * len(params.subjects)
params.structurals = params.subjects
params.subject_run_indices = None
params.subjects_dir = op.join('/brainstudio', 'MEG', 'genz', 'anatomy')
params.score = score
params.run_names = [
    '%s_emojis_learn_01',
    '%s_thumbs_learn_01',
    '%s_faces_learn_01',
    '%s_emojis_test_01',
    '%s_faces_test_01',
    '%s_thumbs_test_01',
]
# params.acq_ssh = 'maggie@minea.ilabs.uw.edu'
params.acq_dir = ['/brainstudio/MEG/genz']
params.sws_ssh = 'nordme@kasga.ilabs.uw.edu'  # kasga
params.sws_dir = '/data07/nordme/genz'
params.sss_type = 'python'
params.sss_regularize = 'in'
params.st_correlation = 0.98
params.trans_to = (.0, .0, 0.04)
params.tsss_dur = 20.
params.movecomp = 'inter'
params.coil_t_window = 'auto'
# Trial rejection
params.reject = dict()
params.auto_bad_reject = None
params.ssp_ecg_reject = None
params.flat = dict(grad=1e-13, mag=1e-15)
# Which runs and trials to use
params.get_projs_from = np.arange(6)
params.inv_names = ['%s_aud', '%s_vis']
params.inv_runs = [np.arange(3, 6), np.arange(0, 3)]
params.pick_events_cov = pick_aud_cov_events
params.proj_nums = [[1, 1, 0],  # ECG: grad/mag/eeg
                    [1, 1, 0],  # EOG
                    [0, 0, 0]]  # Continuous (from ERM)
params.on_missing = 'ignore'  # some subjects will not complete the paradigm
params.in_names = aud_in_names
params.in_numbers = aud_in_numbers
params.cov_method = 'empirical'
params.runs_empty = ['%s_erm_01'] # add in the empty room covariance
params.bem_type = '5120'
# The ones we actually want
params.analyses = [
    'All',
    'Split',
    ]
params.out_names = [
    ['aud', 'vis_onset'],
    params.in_names,
    ]
params.out_numbers = [  # these don't matter as long as they don't overlap...
    [1] * (3 * 12 + 3 * 3) + [2],
    100000 * np.arange(1, len(params.in_names) + 1),
    ]
# do not trial count match for now
params.must_match = [[]] * len(params.analyses)
aud_times = [0.09, 0.25]
vis_times = [0.17, 0.22]
#params.report_params.update(  # add a couple of nice diagnostic plots
#    bem=False,  # Using a surrogate
#    whitening=[
#        dict(analysis='All', name='aud',
#             cov='%s-80-sss-cov.fif'),
#        dict(analysis='Split', name='aud/emojis/learn/s01',
#             cov='%s-80-sss-cov.fif'),
#        dict(analysis='All', name='vis_onset',
#             cov='%s-80-sss-cov.fif'),
#    ],
#    sensor=[
#        dict(analysis='All', name='aud', times=aud_times),
#        dict(analysis='Split', name='aud/emojis/learn/s01', times=aud_times),
#        dict(analysis='SPN', name='vis', times=vis_times),
#    ],
#    source=[
#        dict(analysis='All', name='aud',
#             inv='%s_aud-80-sss-meg-free-inv.fif', times=aud_times,
#             views=['lat', 'caudal'], size=(800, 800)),
#        dict(analysis='Split', name='aud/emojis/learn/s01',
#             inv='%s_aud-80-sss-meg-free-inv.fif', times=aud_times,
#             views=['lat', 'caudal'], size=(800, 800)),
#        dict(analysis='SPN', name='vis',
#             inv='%s_vis-80-sss-meg-free-inv.fif', times=vis_times,
#              views=['lat', 'caudal'], size=(800, 800)),
#    ],
#    psd=False,  # often slow
#)
params.report_params.update(  # add a couple of nice diagnostic plots
    bem=False,  # Using a surrogate
    whitening=[
        dict(analysis='All', name='aud',
             cov='%s-80-sss-cov.fif'),
        dict(analysis='Split', name='aud/emojis/learn/s01',
             cov='%s-80-sss-cov.fif'),
    ],
    sensor=[
        dict(analysis='All', name='aud', times=aud_times),
        dict(analysis='Split', name='aud/emojis/learn/s01', times=aud_times),
    ],
    sensor_topo=[
        dict(analysis='All', name='aud'),
        dict(analysis='Split', name='aud/emojis/learn/s01'),
    ],
#    snr=[
#        dict(analysis='Split', name='aud_faces_learn_s1'),
#        dict(analysis='Split', name='aud_emojis_learn_s1'),
#        dict(analysis='Split', name='aud_thumbs_learn_s1'),
#    ],
    source_alignment=False,
    psd=False,  # often slow
)
default = True


mnefun.do_processing(
    params,
    fetch_raw=False,  # Fetch raw recording files from acq machine
    do_score=True,  # do scoring
    push_raw=False,  # Push raw files and SSS script to SSS workstation
    do_sss=True, # Run SSS remotely
    fetch_sss=True,  # Fetch SSSed files
    do_ch_fix=False,  # Fix channel ordering
    gen_ssp=True,  # Generate SSP vectors
    apply_ssp=True,  # Apply SSP vectors and filtering
    write_epochs=True,  # Write epochs to disk
    gen_covs=False,  # Generate covariances
    gen_fwd=False,  # Generate forward solutions (and source space if needed)
    gen_inv=False,  # Generate inverses
    gen_report=False,
    print_status=True,
)
