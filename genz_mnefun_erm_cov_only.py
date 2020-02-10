# -*- coding: utf-8 -*-
"""
GenZ pilot analysis script.

"""
# for genz 232: use 'EOG062' as the ECG channel; use ['ECG063', 'EOG061'] as the EOG channels

import os
import os.path as op
import mnefun
import numpy as np
from genz_score import (score, aud_in_names, aud_in_numbers)


fixed_or_twa = 'twa'
# raw_dir = '/storage/genz_active/t1/%s_hp/' % fixed_or_twa

raw_dir = '/home/nordme/data/genz/'

if fixed_or_twa == 'twa':
    trans_to = 'twa'
else:
    trans_to = (0.0, 0.0, 0.04)

# subjs = [x for x in os.listdir(raw_dir) if op.isdir('%s%s' % (raw_dir, x)) and 'genz' in x]
subjs = ['erica_peterson']
subjs.sort()

params = mnefun.Params(tmin=-0.1, tmax=0.75, t_adjust=0, n_jobs=12,
                       decim=4, n_jobs_mkl=1, proj_sfreq=200,
                       n_jobs_fir=12, n_jobs_resample=12,
                       filter_length='auto', lp_cut=80., bmin=-0.1,
                       lp_trans='auto', bem_type='inner_skull', fwd_mindist=0.0)

params.subjects = subjs
params.work_dir = raw_dir
params.subject_indices = np.arange(len(params.subjects))
#params.subject_indices = np.setdiff1d(np.arange(len(params.subjects)), [])
params.dates = [(2014, 10, 14)] * len(params.subjects)
params.structurals = ['fsaverage']
params.subject_run_indices = None
# params.subjects_dir = '/storage/anat/subjects/'
params.subjects_dir = '/home/nordme/data/genz/anat/'
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
params.trans_to = trans_to
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
params.inv_names = []
params.inv_runs = []
params.pick_events_cov = None
params.proj_nums = [[1, 1, 0],  # ECG: grad/mag/eeg
                    [1, 1, 0],  # EOG
                    [0, 0, 0]]  # Continuous (from ERM)
params.on_missing = 'ignore'  # some subjects will not complete the paradigm
params.in_names = aud_in_names
params.in_numbers = aud_in_numbers
params.epochs_prefix = 'All'
params.cov_method = 'empirical'
params.compute_rank = True
params.cov_rank = None
params.force_erm_cov_rank_full = False
params.runs_empty = ['%s_erm_01'] # use the empty room covariance
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
        dict(analysis='All', name='aud'),
    ],
    sensor=[
        dict(analysis='All', name='aud', times=aud_times),
    ],
    sensor_topo=[
        dict(analysis='All', name='aud'),
    ],
#    snr=[
#        dict(analysis='Split', name='aud_faces_learn_s1'),
#        dict(analysis='Split', name='aud_emojis_learn_s1'),
#        dict(analysis='Split', name='aud_thumbs_learn_s1'),
#    ],
    source_alignment=True,
    psd=False,  # often slow
)
default = True

mnefun.do_processing(
    params,
#    fetch_raw=False,  # Fetch raw recording files from acq machine
    do_score=False,  # do scoring
#    push_raw=False,  # Push raw files and SSS script to SSS workstation
    do_sss=False, # Run SSS remotely
#    fetch_sss=False,  # Fetch SSSed files
#    do_ch_fix=False,  # Fix channel ordering
    gen_ssp=False,  # Generate SSP vectors
    apply_ssp=False,  # Apply SSP vectors and filtering
    write_epochs=False,  # Write epochs to disk
    gen_covs=False,  # Generate covariances
    gen_fwd=True,  # Generate forward solutions (and source space if needed)
    gen_inv=False,  # Generate inverses
    gen_report=False,
    print_status=False,
)
