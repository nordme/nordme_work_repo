#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import os.path as op
import mne
import mnefun
import numpy as np

def pacc_score(p, subjects):

    events = mne.find




raw_dir = '/home/nordme/data/pitchacc/'

# subjects

subjects = [x for x in os.listdir(raw_dir) if op.isdir(op.join(raw_dir, x)) and 'pitchacc' in x]


# INITIALIZE

pacc_params = mnefun.Params(tmin=-0.05, tmax=1.0, n_jobs=6,
                       decim=1, n_jobs_mkl=1, proj_sfreq=250,
                       n_jobs_fir=6, n_jobs_resample=6,
                       filter_length='auto', epochs_type='fif', lp_cut=100.,
                       bmin=-0.05, plot_raw=False)

# GENERAL
pacc_params.work_dir = '/home/nordme/data/pitchacc/'
pacc_params.subjects = subjects
pacc_params.run_names = ['%s'] # this parameter allows you to have multiple files per subject; generally condition name is the variable
pacc_params.subject_indices = np.arange(len(subjects))
pacc_params.subject_run_indices = None
pacc_params.subjects_dir = None
pacc_params.disp_files = True # display files --- this parameter has your script say the files its working on

# SSS
pacc_params.sws_ssh = 'nordme@kasga.ilabs.uw.edu'  # kasga
pacc_params.sws_dir = '/data07/nordme/genz'
pacc_params.sss_type = 'python'
pacc_params.tsss_dur = 4.
pacc_params.trans_to = 'twa'  # where to transform head positions to
pacc_params.sss_format = 'float'  # output type for MaxFilter
pacc_params.movecomp = 'inter'
pacc_params.int_order = 6
pacc_params.ext_order = 3
pacc_params.st_correlation = .98
pacc_params.sss_origin = 'auto'
pacc_params.sss_regularize = 'in'
pacc_params.filter_chpi = True

# parameters for filtering
pacc_params.cont_lp = 5
pacc_params.phase = 'zero-double'
pacc_params.fir_window = 'hann'
pacc_params.fir_design = 'firwin2'

# params for movement comp
pacc_params.rotation_limit = np.inf
pacc_params.translation_limit = np.inf
pacc_params.coil_bad_count_duration_limit = np.inf  # for annotations
pacc_params.coil_dist_limit = 0.005
pacc_params.coil_t_window = 0.2  # default is same as maxfilter
pacc_params.coil_t_step_min = 0.01

# SSP
pacc_params.get_projs_from = range(len(pacc_params.run_names))
pacc_params.proj_nums = [[1, 1, 0],  # ECG: grad/mag/eeg
                         [0, 0, 0],  # EOG
                         [0, 0, 0]]
pacc_params.proj_ave = False


# EPOCHS

pacc_params.score = None
pacc_params.analyses = ['All', 'Split']

pacc_params.in_names = ['pitches', 'speech']
pacc_params.in_numbers = [4, 8]

pacc_params.out_names = [['All'], ['Split']]
pacc_params.out_numbers = [[1,1], [1, 2]]

#out_numbers: Event numbers to convert to (e.g., [[1, 1, 2, 3, 3], ...] would create
# three event types, where the first two and last two event types from
# the original list get collapsed over).

# epoching settings

# must_match: Indices from the original in_names that must match in event counts
#        before collapsing. List of lists

pacc_params.on_missing = 'warning'  # for epochs

# epoch rejection

pacc_params.auto_bad = None  # max number of events disqualified by channel before channel becomes excluded automatically
pacc_params.auto_bad_reject = None
pacc_params.auto_bad_flat = None
pacc_params.autoreject_thresholds = False
pacc_params.reject = dict()
pacc_params.flat = dict(grad=1e-13, mag=1e-15)
# pacc_params.ssp_eog_reject = dict(grad=3500e-13, mag=4.0e-12)
# pacc_params.ssp_ecg_reject = dict(grad=3500e-13, mag=4.0e-12)

# pacc_params.auto_bad_reject = dict(grad=3500e-13, mag=4.0e-12)
# pacc_params.auto_bad_flat = dict(grad=1e-13, mag=1e-15)


# COVARIANCE

# covariance
pacc_params.pick_events_cov = pick_cov_events_pacc # Function to pick a subset of events to use to make a covariance
pacc_params.cov_method = 'empirical'
pacc_params.cov_rank = 'full'

# FORWARDS

# boolean for whether data set(s) have an individual mri
pacc_params.on_process = None
pacc_params.structurals = pacc_params.subjects


# INVERSES

pacc_params.inv_names = None  # this parameter lets you separate inverse solutions (i.e. between conditions)
pacc_params.inv_runs = None  # how many files per inverse solution


# REPORTS

pacc_params.plot_drop_logs = False  # plot drop logs after do_preprocessing_
pacc_params.report_params = dict(
    good_hpi_count=True,
    head_movement=True,
    psd=True,
    ssp_topomaps=True,
    source_alignment=True,
    bem=True,
    source=None,
    )

# JOBS

mnefun.do_processing(
    pacc_params,
    do_score = False,
    do_sss = False,
    gen_ssp = False,
    apply_ssp = False,
    write_epochs = True,
    gen_covs = False,  # Generate covariances
    gen_fwd = False,  # Generate forward solutions (and source space if needed)
    gen_inv = False,  # Generate inverses
    gen_report = False,
    print_status = True
)

