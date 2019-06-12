#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import os.path as op
import mne
import mnefun
import numpy as np
from prek_score import (prek_score, prek_in_names, prek_in_numbers, prek_out_names, prek_out_numbers, pick_cov_events_prek)

raw_dir = '/home/nordme/data/prek/twa_hp/'

# subjects

subjects = [x for x in os.listdir(raw_dir) if op.isdir(op.join(raw_dir, x)) and 'prek' in x]


# INITIALIZE

prek_params = mnefun.Params(tmin=-0.05, tmax=1.0, n_jobs=6,
                       decim=2, n_jobs_mkl=1, proj_sfreq=250,
                       n_jobs_fir=6, n_jobs_resample=6,
                       filter_length='auto', epochs_type='fif', lp_cut=100.,
                       bmin=-0.05, plot_raw=False)

# GENERAL
prek_params.work_dir = '/home/nordme/data/prek/twa_hp/'
prek_params.subjects = subjects
prek_params.run_names = ['%s_erp_pre',] # this parameter allows you to have multiple files per subject; generally condition name is the variable
prek_params.subject_indices = np.arange(len(subjects))
prek_params.subject_run_indices = None
prek_params.subjects_dir = None
prek_params.disp_files = True # display files --- this parameter has your script say the files its working on

# SSS
prek_params.sws_ssh = 'nordme@kasga.ilabs.uw.edu'  # kasga
prek_params.sws_dir = '/data07/nordme/genz'
prek_params.sss_type = 'python'
prek_params.tsss_dur = 4.
prek_params.trans_to = 'twa'  # where to transform head positions to
prek_params.sss_format = 'float'  # output type for MaxFilter
prek_params.movecomp = 'inter'
prek_params.int_order = 8
prek_params.ext_order = 3
prek_params.st_correlation = .98
prek_params.sss_origin = 'auto'
prek_params.sss_regularize = 'in'
prek_params.filter_chpi = True

# parameters for filtering
prek_params.cont_lp = 5
prek_params.phase = 'zero-double'
prek_params.fir_window = 'hann'
prek_params.fir_design = 'firwin2'

# params for movement comp
prek_params.rotation_limit = np.inf
prek_params.translation_limit = np.inf
prek_params.coil_bad_count_duration_limit = np.inf  # for annotations
prek_params.coil_dist_limit = 0.005
prek_params.coil_t_window = 0.2  # default is same as maxfilter
prek_params.coil_t_step_min = 0.01

# SSP
prek_params.get_projs_from = range(len(prek_params.run_names))
prek_params.proj_nums = [[1, 1, 0],  # ECG: grad/mag/eeg
                         [1, 1, 0],  # EOG
                         [0, 0, 0]]
prek_params.proj_ave = False


# EPOCHS

prek_params.score = prek_score

prek_params.in_names = prek_in_names   # Names of input events (from list files after scoring is done).
prek_params.in_numbers = prek_in_numbers  # Event numbers (in scored event files) associated with each name.

prek_params.analyses = ['Split']

prek_params.out_names = prek_out_names  # Event types to make out of old ones.
prek_params.out_numbers = prek_out_numbers

#out_numbers: Event numbers to convert to (e.g., [[1, 1, 2, 3, 3], ...] would create
# three event types, where the first two and last two event types from
# the original list get collapsed over).

# epoching settings

# must_match: Indices from the original in_names that must match in event counts
#        before collapsing. List of lists

prek_params.must_match = [[0, 1, 2]]
prek_params.on_missing = 'warning'  # for epochs

# epoch rejection

prek_params.auto_bad = None  # max number of events disqualified by channel before channel becomes excluded automatically
prek_params.auto_bad_reject = None
prek_params.auto_bad_flat = None
prek_params.autoreject_thresholds = False
prek_params.reject = dict()
prek_params.flat = dict(grad=1e-13, mag=1e-15)
# prek_params.ssp_eog_reject = dict(grad=3500e-13, mag=4.0e-12)
# prek_params.ssp_ecg_reject = dict(grad=3500e-13, mag=4.0e-12)

# prek_params.auto_bad_reject = dict(grad=3500e-13, mag=4.0e-12)
# prek_params.auto_bad_flat = dict(grad=1e-13, mag=1e-15)


# COVARIANCE

# covariance
prek_params.pick_events_cov = pick_cov_events_prek # Function to pick a subset of events to use to make a covariance
prek_params.cov_method = 'empirical'
prek_params.cov_rank = 'full'

# FORWARDS

# boolean for whether data set(s) have an individual mri
prek_params.on_process = None
prek_params.structurals = prek_params.subjects


# INVERSES

prek_params.inv_names = None  # this parameter lets you separate inverse solutions (i.e. between conditions)
prek_params.inv_runs = None  # how many files per inverse solution


# REPORTS

prek_params.plot_drop_logs = False  # plot drop logs after do_preprocessing_
prek_params.report_params = dict(
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
    prek_params,
    do_score = True,
    do_sss = True,
    gen_ssp = True,
    apply_ssp = True,
    write_epochs = True,
    gen_covs = False,  # Generate covariances
    gen_fwd = False,  # Generate forward solutions (and source space if needed)
    gen_inv = False,  # Generate inverses
    gen_report = False,
    print_status = True
)

