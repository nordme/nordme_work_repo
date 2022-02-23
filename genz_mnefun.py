# -*- coding: utf-8 -*-
"""
GenZ pilot analysis script.

"""
# for genz 232: use 'EOG062' as the ECG channel; use ['ECG063', 'EOG061'] as the EOG channels

import os
import os.path as op
import mnefun
import numpy as np
from genz_score import (score, aud_in_names, aud_in_numbers, pick_aud_cov_events)

# raw_dir = ''

fixed_or_twa = 'twa'
# raw_dir = '/storage/genz_active/t1/%s_hp/' % fixed_or_twa
raw_dir = '/data/genz/'
if fixed_or_twa == 'twa':
    trans_to = 'twa'
else:
    trans_to = (0.0, 0.0, 0.04)
lp_cut = 80

#subjs = [x for x in os.listdir(raw_dir) if op.isdir('%s%s' % (raw_dir, x)) and 'genz' in x]
subjs = ['erica_peterson']
subjs.sort()

params = mnefun.Params(tmin=-0.1, tmax=0.75, t_adjust=0, n_jobs=8,
                       decim=4, n_jobs_mkl=8, proj_sfreq=200,
                       n_jobs_fir=8, n_jobs_resample=8,
                       filter_length='auto', lp_cut=80., bmin=-0.1,
                       lp_trans='auto', bem_type='inner_skull')

params.subjects = subjs
params.work_dir = raw_dir
params.subject_indices = np.arange(len(params.subjects))
#params.subject_indices = np.setdiff1d(np.arange(len(params.subjects)), [])
params.dates = [(2014, 10, 14)] * len(params.subjects)
params.structurals = params.subjects
params.subject_run_indices = None
params.subjects_dir = '/data/anat_subjects/'
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
params.mf_autobad = True
params.mf_autobad_type = 'python'
params.hp_type = 'python'
# Trial rejection
params.reject = dict(grad=2000e-13, mag=6000e-15)
params.flat = dict(grad=1e-13, mag=1e-15)
params.ssp_ecg_reject = params.reject
params.ssp_eog_reject = params.reject
params.proj_nums = [[1, 1, 0],  # ECG: grad/mag/eeg
                    [1, 1, 0],  # EOG
                    [0, 0, 0]]  # Continuous (from ERM)
params.get_projs_from = np.arange(6)
params.plot_drop_logs = True
# Which runs and trials to use
params.inv_names = ['%s'] # gen_covs works, but list index out of range tb during reports step
params.inv_runs = [np.arange(6)]
params.pick_events_cov = pick_aud_cov_events
params.on_missing = 'ignore'  # some subjects will not complete the paradigm
params.every_other = True
params.in_names = aud_in_names
params.in_numbers = aud_in_numbers
params.cov_method = 'shrunk'
params.compute_rank = True
params.cov_rank = None
params.cov_rank_method = 'compute_rank'
params.cov_rank_tol = 5e-2
params.force_erm_cov_rank_full = False
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
params.must_match = [None] * len(params.analyses)
times = [0.05, 0.105, 0.220, 0.550]
cov = '%s-' + str(lp_cut) + '-sss-cov.fif'
inv = '%s-' + str(lp_cut) + '-sss-meg-inv.fif'

show = [{'projs': True, "analysis":'Split', "name":'aud/%s/learn/s%02d' % (kind, syl), "times":times, "cov":cov, "inv":inv}
        for kind in ('emojis', 'faces', 'thumbs')
        for syl in (1,2,3)]

params.report_params.update(  # add a couple of nice diagnostic plots
    good_hpi_count=True,
    raw_segments=True,
    chpi_snr=False,
    head_movement=False,
    ssp_topomaps=True,
    drop_log=True,
    covariance=cov,
    whitening=show,
    sensor=show,
    snr=False,
    source=show,
    source_alignment=True,
    psd=True  # often slow
)
default = True

mnefun.do_processing(
    params,
    do_score=False,  # do scoring
    do_sss=False, # Run SSS remotely
    gen_ssp=False,  # Generate SSP vectors
    apply_ssp=False,  # Apply SSP vectors and filtering
    write_epochs=False,  # Write epochs to disk
    gen_covs=False,  # Generate covariances
    gen_fwd=False,  # Generate forward solutions (and source space if needed)
    gen_inv=False,  # Generate inverses
    gen_report=True,
    print_status=False,
)
